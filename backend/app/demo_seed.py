import uuid
import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from app.config import settings
from app.database.db import get_milestone, save_milestone, save_proof, save_verdict, init_db
from app.services.ledger_service import append_block, ensure_genesis_block
from app.models.schemas import MilestoneStatus

def create_sample_images():
    upload_dir = Path(settings.UPLOAD_FOLDER)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Pass image
    pass_img_path = upload_dir / "sample_hvac_pass.jpg"
    if not pass_img_path.exists():
        img = Image.new('RGB', (800, 600), color=(30, 41, 59))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(50, 50), (750, 550)], outline=(16, 185, 129), width=4)
        draw.text((80, 80), "PROOFLEDGER CONTRACTOR DELIVERABLE", fill=(255, 255, 255))
        draw.text((80, 120), "Milestone: HVAC Dual-Run Capacitor Replacement", fill=(148, 163, 184))
        
        # Component boxes
        draw.rectangle([(100, 200), (350, 450)], outline=(59, 130, 246), width=2, fill=(15, 23, 42))
        draw.text((120, 220), "[CAPACITOR UNIT]", fill=(96, 165, 250))
        draw.text((120, 260), "Status: 45/5 uF 440V Wired", fill=(226, 232, 240))
        draw.text((120, 300), "Terminals: Herm / Fan / C Secure", fill=(226, 232, 240))
        
        draw.rectangle([(420, 200), (700, 450)], outline=(16, 185, 129), width=2, fill=(15, 23, 42))
        draw.text((440, 220), "[DIGITAL MANIFOLD GAUGE]", fill=(52, 211, 153))
        draw.text((440, 260), "Suction Line: 68.4 PSI (STABLE)", fill=(226, 232, 240))
        draw.text((440, 300), "Target Range: 60 - 70 PSI", fill=(226, 232, 240))
        draw.text((440, 340), "Grid Sync & Grounding: PASS", fill=(226, 232, 240))
        
        draw.text((80, 500), "Forensic Timestamp: 2026-11-10T14:30:00Z | Tech: Dave Vance (#HVAC-88)", fill=(100, 116, 139))
        img.save(pass_img_path, "JPEG", quality=95)

    # 2. Fail / Deficient image
    fail_img_path = upload_dir / "sample_hvac_fail.jpg"
    if not fail_img_path.exists():
        img = Image.new('RGB', (800, 600), color=(69, 10, 10))
        draw = ImageDraw.Draw(img)
        draw.rectangle([(50, 50), (750, 550)], outline=(239, 68, 68), width=4)
        draw.text((80, 80), "DEFICIENT DELIVERABLE PROOF - FAIL EXAMPLE", fill=(255, 255, 255))
        draw.rectangle([(100, 200), (700, 450)], outline=(220, 38, 38), width=2, fill=(26, 5, 5))
        draw.text((120, 230), "WARNING: Exposed copper wiring detected", fill=(248, 113, 113))
        draw.text((120, 280), "Missing Manifold Gauge Reading (Pressure unverified)", fill=(248, 113, 113))
        draw.text((120, 330), "Original capacitor not visible", fill=(248, 113, 113))
        draw.text((80, 500), "Forensic Status: Non-compliant with contractual specifications", fill=(153, 27, 27))
        img.save(fail_img_path, "JPEG", quality=90)

def seed_demo_data():
    init_db()
    ensure_genesis_block()
    create_sample_images()
    
    upload_dir = Path(settings.UPLOAD_FOLDER)
    pass_img_path = upload_dir / "sample_hvac_pass.jpg"
    with open(pass_img_path, "rb") as f:
        pass_hash = hashlib.sha256(f.read()).hexdigest()

    # Seed Milestone 1: ESCROW_LOCKED (Ready for Contractor proof submission!)
    ms1_id = "ms-hvac-7701"
    if not get_milestone(ms1_id):
        m1 = {
            "id": ms1_id,
            "title": "HVAC Capacitor Replacement & Pressure Gauge Calibration",
            "description": "Commercial refrigeration maintenance: replace dual run capacitor and calibrate manifold pressure between 60-70 PSI.",
            "amount": 250.00,
            "currency": "USD",
            "client_name": "Apex Commercial Properties LLC",
            "client_email": "facilities@apexcommercial.test",
            "contractor_name": "Dave Vance (Vance HVAC)",
            "contractor_email": "dave@vancehvac.test",
            "specifications": [
                "Original malfunctioning capacitor removed",
                "New brand-name dual run capacitor securely wired with spade connectors",
                "Analog or digital manifold gauge showing stable pressure reading between 60-70 PSI",
                "Work area clean with no exposed cut copper"
            ],
            "auto_capture_on_pass": True,
            "status": MilestoneStatus.ESCROW_LOCKED.value,
            "paypal_order_id": "ORD-SANDBOX-7701A",
            "paypal_authorization_id": "AUTH-SANDBOX-7701AUTH",
            "paypal_capture_id": None,
            "paypal_approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=ORD-SANDBOX-7701A",
            "created_at": "2026-11-10T10:00:00Z",
            "updated_at": "2026-11-10T10:05:00Z"
        }
        save_milestone(m1)
        append_block("ESCROW_CREATED", ms1_id, {"title": m1["title"], "amount": 250.00, "client": m1["client_name"]})
        append_block("ESCROW_AUTHORIZED", ms1_id, {
            "auth_id": m1["paypal_authorization_id"],
            "amount": 250.00,
            "hold": "ACTIVE_ESCROW_HOLD"
        })

    # Seed Milestone 2: COMPLETED (Smart contract audit, settled and verified)
    ms2_id = "ms-audit-9902"
    if not get_milestone(ms2_id):
        m2 = {
            "id": ms2_id,
            "title": "Web3 Escrow Smart Contract Audit & Formal Verification",
            "description": "Comprehensive security assessment of Solidity escrow contracts with automated test suite and signed auditor certificate.",
            "amount": 1500.00,
            "currency": "USD",
            "client_name": "Nexus DeFi Foundation",
            "client_email": "security@nexusdefi.test",
            "contractor_name": "Sarah Lin, Lead Auditor",
            "contractor_email": "sarah@linforensics.test",
            "specifications": [
                "Automated Slither & Mythril vulnerability scanner logs with 0 critical findings",
                "100% branch test coverage suite for Vault.sol and EscrowManager.sol",
                "Remediation verification signed with auditor PGP signature"
            ],
            "auto_capture_on_pass": True,
            "status": MilestoneStatus.COMPLETED.value,
            "paypal_order_id": "ORD-SANDBOX-9902A",
            "paypal_authorization_id": "AUTH-SANDBOX-9902AUTH",
            "paypal_capture_id": "CAP-SANDBOX-9902CAPTURED",
            "paypal_approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=ORD-SANDBOX-9902A",
            "created_at": "2026-11-09T08:00:00Z",
            "updated_at": "2026-11-09T14:30:00Z"
        }
        save_milestone(m2)
        save_proof({
            "proof_id": "PRF-AUDIT-9902",
            "milestone_id": ms2_id,
            "file_name": "sample_hvac_pass.jpg",
            "file_path": str(pass_img_path),
            "file_hash": pass_hash,
            "file_size_bytes": pass_img_path.stat().st_size,
            "notes": "Formal verification report complete. All test suites passing with 100% coverage.",
            "submitted_at": "2026-11-09T14:20:00Z"
        })
        save_verdict({
            "milestone_id": ms2_id,
            "confidence_score": 96,
            "verdict": "PASS",
            "criteria_checklist": [
                {"criterion": m2["specifications"][0], "satisfied": True, "confidence": 98.0, "visual_evidence": "Zero high/critical warnings verified in static analysis output."},
                {"criterion": m2["specifications"][1], "satisfied": True, "confidence": 95.0, "visual_evidence": "All 48 unit tests passing across branch coverage."},
                {"criterion": m2["specifications"][2], "satisfied": True, "confidence": 97.0, "visual_evidence": "Cryptographic PGP audit certificate verified."}
            ],
            "summary_reasoning": "Contractual deliverables fully satisfied with 96% confidence. Autonomous PayPal settlement executed.",
            "fraud_risk_score": 1,
            "visual_anomalies": [],
            "evaluator_model": "ProofLedger-VisionOracle-v1.4",
            "evaluated_at": "2026-11-09T14:25:00Z"
        })
        append_block("ESCROW_CREATED", ms2_id, {"title": m2["title"], "amount": 1500.00})
        append_block("ESCROW_AUTHORIZED", ms2_id, {"auth_id": m2["paypal_authorization_id"]})
        append_block("PROOF_SUBMITTED", ms2_id, {"sha256": pass_hash, "file": "sample_hvac_pass.jpg"})
        append_block("AI_VERIFIED", ms2_id, {"verdict": "PASS", "confidence": 96})
        append_block("PAYMENT_CAPTURED", ms2_id, {"capture_id": m2["paypal_capture_id"], "amount": 1500.00})

    # Seed Milestone 3: DRAFT (Solar Installation)
    ms3_id = "ms-solar-4403"
    if not get_milestone(ms3_id):
        m3 = {
            "id": ms3_id,
            "title": "Solar Array Micro-Inverter Grounding & Grid Sync",
            "description": "Inspect and mount 12x Enphase IQ8+ micro-inverters, verify ground continuity, and confirm grid synchronization LED.",
            "amount": 480.00,
            "currency": "USD",
            "client_name": "GreenValley Estates Eco-Homes",
            "client_email": "renewables@greenvalley.test",
            "contractor_name": "Alex Rivera Solar Field Services",
            "contractor_email": "alex@riverasolar.test",
            "specifications": [
                "Enphase IQ8+ micro-inverters securely clamped to aluminum rail",
                "Multimeter reading confirming AC 240V +/- 5V",
                "Status LED showing continuous solid green grid lock"
            ],
            "auto_capture_on_pass": True,
            "status": MilestoneStatus.DRAFT.value,
            "paypal_order_id": "ORD-SANDBOX-4403A",
            "paypal_authorization_id": None,
            "paypal_capture_id": None,
            "paypal_approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=ORD-SANDBOX-4403A",
            "created_at": "2026-11-11T09:00:00Z",
            "updated_at": "2026-11-11T09:00:00Z"
        }
        save_milestone(m3)
        append_block("ESCROW_CREATED", ms3_id, {"title": m3["title"], "amount": 480.00, "status": "DRAFT"})

    # Seed Milestone 4: ESCROW_LOCKED (Ready for Deficient / Rejection Flow Demonstration)
    ms4_id = "ms-refrig-8805"
    if not get_milestone(ms4_id):
        m4 = {
            "id": ms4_id,
            "title": "Industrial Chiller Wiring & Pressure Calibration",
            "description": "Critical cooling maintenance: terminal spade wiring and 65 PSI stable pressure verification.",
            "amount": 350.00,
            "currency": "USD",
            "client_name": "CryoLogistics Cold Chain Inc.",
            "client_email": "operations@cryologistics.test",
            "contractor_name": "Apex Thermal Techs",
            "contractor_email": "service@apexthermal.test",
            "specifications": [
                "Dual run capacitor wired with no exposed cut copper",
                "Manifold gauge showing stable pressure between 60-70 PSI",
                "Grounding terminal continuity verified"
            ],
            "auto_capture_on_pass": True,
            "status": MilestoneStatus.ESCROW_LOCKED.value,
            "paypal_order_id": "ORD-SANDBOX-8805A",
            "paypal_authorization_id": "AUTH-SANDBOX-8805AUTH",
            "paypal_capture_id": None,
            "paypal_approval_url": "https://www.sandbox.paypal.com/checkoutnow?token=ORD-SANDBOX-8805A",
            "created_at": "2026-11-11T11:00:00Z",
            "updated_at": "2026-11-11T11:05:00Z"
        }
        save_milestone(m4)
        append_block("ESCROW_CREATED", ms4_id, {"title": m4["title"], "amount": 350.00, "client": m4["client_name"]})
        append_block("ESCROW_AUTHORIZED", ms4_id, {
            "auth_id": m4["paypal_authorization_id"],
            "amount": 350.00,
            "hold": "ACTIVE_ESCROW_HOLD"
        })
