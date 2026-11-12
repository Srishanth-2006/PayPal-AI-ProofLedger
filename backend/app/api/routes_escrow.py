import uuid
from typing import Optional, Any
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from app.models.schemas import MilestoneCreate, MilestoneResponse, MilestoneStatus, AuthorizeOrderRequest, VoidAuthorizationRequest
from app.database.db import save_milestone, get_milestone, list_milestones
from app.services.paypal_service import paypal_service
from app.services.ledger_service import append_block, get_all_blocks

router = APIRouter(prefix="/escrow", tags=["Escrow"])

@router.post("/create", response_model=MilestoneResponse)
async def create_milestone_escrow(payload: MilestoneCreate):
    milestone_id = f"MS-{uuid.uuid4().hex[:8].upper()}"
    now_iso = datetime.now(timezone.utc).isoformat()
    
    # 1. Create PayPal Order with intent=AUTHORIZE
    order_data = await paypal_service.create_escrow_order(
        milestone_id=milestone_id,
        amount=payload.amount,
        currency=payload.currency,
        title=payload.title
    )
    
    order_id = order_data["id"]
    approval_url = None
    for link in order_data.get("links", []):
        if link.get("rel") == "approve":
            approval_url = link.get("href")
            break

    client_email = payload.clientEmail or payload.client_email
    worker_email = payload.workerEmail or payload.contractor_email
    specs = payload.specifications if payload.specifications else ["Deliverable satisfies all contractual specifications."]

    milestone_dict = {
        "id": milestone_id,
        "title": payload.title,
        "description": payload.description or payload.title,
        "amount": payload.amount,
        "currency": payload.currency,
        "client_name": payload.client_name,
        "client_email": client_email,
        "contractor_name": payload.contractor_name,
        "contractor_email": worker_email,
        "specifications": specs,
        "auto_capture_on_pass": payload.auto_capture_on_pass,
        "status": MilestoneStatus.DRAFT.value,
        "paypal_order_id": order_id,
        "paypal_authorization_id": None,
        "paypal_capture_id": None,
        "paypal_approval_url": approval_url,
        "created_at": now_iso,
        "updated_at": now_iso
    }
    
    save_milestone(milestone_dict)
    
    # Append to Cryptographic Ledger
    append_block(
        event_type="ESCROW_CREATED",
        milestone_id=milestone_id,
        payload={
            "milestone_id": milestone_id,
            "title": payload.title,
            "amount": payload.amount,
            "currency": payload.currency,
            "paypal_order_id": order_id,
            "intent": "AUTHORIZE",
            "client": payload.client_name,
            "contractor": payload.contractor_name,
            "criteria_count": len(specs)
        }
    )
    
    return get_milestone(milestone_id)

@router.get("/milestones")
def list_milestones_wrapped():
    """Compatibility route matching Node.js proof-ledger API: { milestones: [...] }"""
    return {"milestones": list_milestones()}

@router.get("/milestones/{milestone_id}")
def get_milestone_wrapped(milestone_id: str):
    """Compatibility route matching Node.js proof-ledger API: { milestone: ..., events: [...] }"""
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
    events = get_all_blocks(milestone_id)
    return {"milestone": m, "events": events}

@router.get("/ledger")
def get_ledger_wrapped():
    """Compatibility route matching Node.js proof-ledger API: { events: [...] }"""
    return {"events": get_all_blocks()}

@router.get("/order/{order_id}")
async def get_order_details(order_id: str):
    """Compatibility route inspecting a PayPal order"""
    try:
        return await paypal_service.get_order(order_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("", response_model=list[MilestoneResponse])
def get_all_milestones():
    return list_milestones()

@router.get("/{milestone_id}", response_model=MilestoneResponse)
def get_single_milestone(milestone_id: str):
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return m

@router.post("/{milestone_id}/authorize", response_model=MilestoneResponse)
async def authorize_escrow(milestone_id: str, req: AuthorizeOrderRequest):
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")

    if m["status"] != MilestoneStatus.DRAFT.value:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot authorize milestone in '{m['status']}' status. Only DRAFT milestones can be authorized."
        )
        
    order_id = (req.order_id if (req and req.order_id) else m.get("paypal_order_id"))
    if not order_id:
        raise HTTPException(status_code=400, detail="Missing paypal_order_id for authorization hold.")

    auth_resp = await paypal_service.authorize_order(order_id)
    
    # Extract authorization id
    auth_id = None
    try:
        auth_id = auth_resp["purchase_units"][0]["payments"]["authorizations"][0]["id"]
    except (KeyError, IndexError):
        auth_id = f"AUTH-SANDBOX-{uuid.uuid4().hex[:10].upper()}"

    now_iso = datetime.now(timezone.utc).isoformat()
    m["status"] = MilestoneStatus.ESCROW_LOCKED.value
    m["paypal_authorization_id"] = auth_id
    m["updated_at"] = now_iso
    save_milestone(m)
    
    # Append to Cryptographic Ledger
    append_block(
        event_type="ESCROW_AUTHORIZED",
        milestone_id=milestone_id,
        payload={
            "milestone_id": milestone_id,
            "paypal_order_id": order_id,
            "paypal_authorization_id": auth_id,
            "amount": m["amount"],
            "currency": m["currency"],
            "hold_status": "ACTIVE_ESCROW_HOLD",
            "note": "Funds locked on PayPal rails. Guaranteed for contractor upon AI deliverable verification."
        }
    )
    
    return get_milestone(milestone_id)

@router.post("/authorize/{milestone_id}", response_model=MilestoneResponse)
async def authorize_escrow_compat(milestone_id: str):
    """Compatibility route: Idempotently authorizes or returns cached hold"""
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
    if m.get("paypal_authorization_id"):
        return m
    return await authorize_escrow(milestone_id, AuthorizeOrderRequest(order_id=m.get("paypal_order_id")))

@router.post("/{milestone_id}/capture", response_model=MilestoneResponse)
async def capture_escrow(milestone_id: str):
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
    if m["status"] in (MilestoneStatus.COMPLETED.value, MilestoneStatus.VOIDED.value):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot capture milestone in '{m['status']}' status. Escrow is already finalized."
        )
    if not m.get("paypal_authorization_id"):
        raise HTTPException(status_code=400, detail="Cannot capture milestone without active PayPal authorization hold.")
        
    cap_resp = await paypal_service.capture_authorization(
        authorization_id=m["paypal_authorization_id"],
        amount=m["amount"],
        currency=m["currency"],
        note_to_payer=f"ProofLedger: Milestone '{m['title']}' completed. Payment settled."
    )
    
    cap_id = cap_resp.get("id") or f"CAP-SANDBOX-{uuid.uuid4().hex[:10].upper()}"
    now_iso = datetime.now(timezone.utc).isoformat()
    m["status"] = MilestoneStatus.COMPLETED.value
    m["paypal_capture_id"] = cap_id
    m["updated_at"] = now_iso
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
            "status": "SETTLED_TO_CONTRACTOR"
        }
    )
    
    return get_milestone(milestone_id)

@router.post("/{milestone_id}/void", response_model=MilestoneResponse)
async def void_escrow(milestone_id: str, req: VoidAuthorizationRequest):
    m = get_milestone(milestone_id)
    if not m:
        raise HTTPException(status_code=404, detail="Milestone not found")
    if m["status"] in (MilestoneStatus.COMPLETED.value, MilestoneStatus.VOIDED.value):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot void milestone in '{m['status']}' status. Escrow is already finalized."
        )
    if not m.get("paypal_authorization_id"):
        raise HTTPException(status_code=400, detail="Cannot void milestone without active PayPal authorization hold.")
        
    await paypal_service.void_authorization(
        authorization_id=m["paypal_authorization_id"],
        reason=req.reason or "Proof failed criteria or canceled by mutual agreement"
    )
    
    now_iso = datetime.now(timezone.utc).isoformat()
    m["status"] = MilestoneStatus.VOIDED.value
    m["updated_at"] = now_iso
    save_milestone(m)
    
    append_block(
        event_type="PAYMENT_VOIDED",
        milestone_id=milestone_id,
        payload={
            "milestone_id": milestone_id,
            "paypal_authorization_id": m["paypal_authorization_id"],
            "reason": req.reason,
            "hold_status": "VOIDED_FUNDS_RELEASED_TO_CLIENT"
        }
    )
    
    return get_milestone(milestone_id)

@router.post("/manual-release/{milestone_id}", response_model=MilestoneResponse)
async def manual_release_alias(milestone_id: str):
    """Compatibility route: Human override capture"""
    return await capture_escrow(milestone_id)

@router.post("/manual-void/{milestone_id}", response_model=MilestoneResponse)
async def manual_void_alias(milestone_id: str):
    """Compatibility route: Human override void"""
    return await void_escrow(milestone_id, VoidAuthorizationRequest(reason="Manual human-approved void"))

@router.post("/submit-proof/{milestone_id}")
async def submit_proof_compatibility(
    milestone_id: str,
    proof: Optional[UploadFile] = File(None),
    file: Optional[UploadFile] = File(None),
    notes: Optional[str] = Form(None)
):
    """Compatibility route matching Node.js submit-proof endpoint"""
    upload = proof or file
    if not upload:
        raise HTTPException(status_code=400, detail="proof file required")
    from app.api.routes_proof import submit_proof_and_evaluate
    res = await submit_proof_and_evaluate(milestone_id=milestone_id, file=upload, notes=notes)
    proof_obj = res.get("proof") or {}
    return {
        "milestone": res,
        "verdict": res.get("verdict"),
        "proofUrl": f"/uploads/{proof_obj.get('file_name', '')}",
        "proofHash": proof_obj.get("file_hash", "")
    }
