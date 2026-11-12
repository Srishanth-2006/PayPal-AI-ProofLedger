import os
import uuid
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.config import settings
from app.database.db import get_milestone, save_milestone, save_proof, save_verdict
from app.models.schemas import MilestoneStatus, ProofMetadata, AIVerdict
from app.services.ai_oracle import ai_oracle
from app.services.paypal_service import paypal_service
from app.services.ledger_service import append_block

router = APIRouter(prefix="/proof", tags=["Proof & AI Oracle"])

def calculate_sha256(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()

@router.post("/{milestone_id}/submit")
async def submit_proof_and_evaluate(
    milestone_id: str,
    file: UploadFile = File(...),
    notes: Optional[str] = Form(None)
):
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
        
    if m["status"] not in (MilestoneStatus.ESCROW_LOCKED.value, MilestoneStatus.NEEDS_REVIEW.value, MilestoneStatus.PROOF_SUBMITTED.value):
        raise HTTPException(
            status_code=400,
            detail=f"Milestone cannot accept proof in '{m['status']}' status. Must be ESCROW_LOCKED or NEEDS_REVIEW."
        )

    # 1. Read file and validate size and format
    content = await file.read()
    if len(content) == 0:
        raise HTTPException(status_code=400, detail="Deliverable file cannot be empty (0 bytes).")
    if len(content) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Deliverable file exceeds maximum allowed size of 25MB.")
        
    ext = Path(file.filename or "deliverable.jpg").suffix.lower() or ".jpg"
    if ext not in (".jpg", ".jpeg", ".png", ".webp"):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported deliverable format '{ext}'. ProofLedger supports JPG, PNG, and WebP photographic proof."
        )

    file_hash = calculate_sha256(content)
    file_size = len(content)
    
    proof_id = f"PRF-{uuid.uuid4().hex[:10].upper()}"
    dest_filename = f"{milestone_id}_{proof_id}{ext}"
    dest_path = Path(settings.UPLOAD_FOLDER) / dest_filename
    
    with open(dest_path, "wb") as f:
        f.write(content)
        
    now_iso = datetime.now(timezone.utc).isoformat()
    proof_dict = {
        "proof_id": proof_id,
        "milestone_id": milestone_id,
        "file_name": file.filename or dest_filename,
        "file_path": str(dest_path),
        "file_hash": file_hash,
        "file_size_bytes": file_size,
        "notes": notes,
        "submitted_at": now_iso
    }
    save_proof(proof_dict)
    
    # 2. Append PROOF_SUBMITTED to Cryptographic Ledger
    append_block(
        event_type="PROOF_SUBMITTED",
        milestone_id=milestone_id,
        payload={
            "proof_id": proof_id,
            "file_name": proof_dict["file_name"],
            "sha256_hash": file_hash,
            "size_bytes": file_size,
            "contractor_notes": notes
        }
    )
    
    # Update milestone to PROOF_SUBMITTED
    m["status"] = MilestoneStatus.PROOF_SUBMITTED.value
    m["updated_at"] = now_iso
    save_milestone(m)

    # 3. Autonomous Multimodal AI Oracle Evaluation
    verdict: AIVerdict = await ai_oracle.evaluate_deliverable(
        milestone_title=m["title"],
        milestone_description=m["description"],
        specifications=m["specifications"],
        file_path=str(dest_path),
        file_hash=file_hash,
        contractor_notes=notes
    )
    v_dict = verdict.model_dump()
    v_dict["milestone_id"] = milestone_id
    save_verdict(v_dict)

    # 4. Append AI_VERIFIED to Ledger
    append_block(
        event_type="AI_VERIFIED",
        milestone_id=milestone_id,
        payload={
            "verdict": verdict.verdict,
            "confidence_score": verdict.confidence_score,
            "fraud_risk_score": verdict.fraud_risk_score,
            "evaluator_model": verdict.evaluator_model,
            "criteria_summary": f"{sum(1 for c in verdict.criteria_checklist if c.satisfied)}/{len(verdict.criteria_checklist)} passed",
            "proof_sha256": file_hash
        }
    )

    # 5. Autonomous Financial Settlement Gate
    if verdict.verdict == "PASS" and verdict.confidence_score >= settings.AI_MIN_PASS_SCORE:
        if m.get("auto_capture_on_pass") and m.get("paypal_authorization_id"):
            cap_resp = await paypal_service.capture_authorization(
                authorization_id=m["paypal_authorization_id"],
                amount=m["amount"],
                currency=m["currency"],
                note_to_payer=f"ProofLedger Autonomous Agent: Deliverable verified (Score {verdict.confidence_score}%). Released."
            )
            cap_id = cap_resp.get("id") or f"CAP-SANDBOX-{uuid.uuid4().hex[:10].upper()}"
            m["status"] = MilestoneStatus.COMPLETED.value
            m["paypal_capture_id"] = cap_id
            m["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_milestone(m)
            
            append_block(
                event_type="PAYMENT_CAPTURED",
                milestone_id=milestone_id,
                payload={
                    "milestone_id": milestone_id,
                    "paypal_authorization_id": m["paypal_authorization_id"],
                    "paypal_capture_id": cap_id,
                    "amount": m["amount"],
                    "currency": m["currency"],
                    "trigger": "AUTONOMOUS_AI_RELEASE",
                    "reason": f"AI confidence {verdict.confidence_score}% >= threshold {settings.AI_MIN_PASS_SCORE}%"
                }
            )
        else:
            m["status"] = MilestoneStatus.PROOF_SUBMITTED.value
            save_milestone(m)
    elif verdict.verdict == "NEEDS_REVIEW":
        m["status"] = MilestoneStatus.NEEDS_REVIEW.value
        m["updated_at"] = datetime.now(timezone.utc).isoformat()
        save_milestone(m)
    else: # FAIL
        if m.get("paypal_authorization_id"):
            # Autonomously void hold to release funds back to client
            await paypal_service.void_authorization(
                authorization_id=m["paypal_authorization_id"],
                reason=f"ProofLedger AI Oracle: Verification failed (Score {verdict.confidence_score}%). Authorization voided."
            )
            m["status"] = MilestoneStatus.VOIDED.value
            m["updated_at"] = datetime.now(timezone.utc).isoformat()
            save_milestone(m)
            
            append_block(
                event_type="PAYMENT_VOIDED",
                milestone_id=milestone_id,
                payload={
                    "milestone_id": milestone_id,
                    "paypal_authorization_id": m["paypal_authorization_id"],
                    "trigger": "AUTONOMOUS_AI_FRAUD_PREVENTION",
                    "reason": f"AI confidence {verdict.confidence_score}% failed threshold"
                }
            )
        else:
            m["status"] = MilestoneStatus.VOIDED.value
            save_milestone(m)

    return get_milestone(milestone_id)
