import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from app.demo_seed import seed_demo_data

client = TestClient(app)

def setup_module():
    seed_demo_data()

def test_api_health():
    resp = client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "HEALTHY"

def test_list_milestones():
    resp = client.get("/api/escrow")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_create_and_authorize_milestone():
    payload = {
        "title": "Solar Array Inverter Diagnostic",
        "description": "Verify AC output at 240V and inverter green LED",
        "amount": 350.00,
        "currency": "USD",
        "client_name": "SolarTech Labs",
        "client_email": "client@solartech.test",
        "contractor_name": "Field Ops Team",
        "contractor_email": "contractor@solartech.test",
        "specifications": [
            "Inverter firmly mounted",
            "AC output verified at 240V"
        ],
        "auto_capture_on_pass": True
    }
    create_resp = client.post("/api/escrow/create", json=payload)
    assert create_resp.status_code == 200
    created = create_resp.json()
    assert created["status"] == "DRAFT"
    assert created["paypal_order_id"] is not None
    ms_id = created["id"]

    # Authorize escrow
    auth_resp = client.post(
        f"/api/escrow/{ms_id}/authorize",
        json={"order_id": created["paypal_order_id"]}
    )
    assert auth_resp.status_code == 200
    authorized = auth_resp.json()
    assert authorized["status"] == "ESCROW_LOCKED"
    assert authorized["paypal_authorization_id"] is not None

def test_ledger_integrity_endpoint():
    resp = client.get("/api/ledger/verify")
    assert resp.status_code == 200
    report = resp.json()
    assert report["is_valid"] is True
    assert report["total_blocks"] > 0

def test_dispute_pack_export_json_and_pdf():
    # Use pre-seeded milestone ms-audit-9902
    resp_json = client.get("/api/disputes/ms-audit-9902/pack")
    assert resp_json.status_code == 200
    pack = resp_json.json()
    assert "pack_id" in pack
    assert "integrity_signature" in pack
    assert pack["status"] == "VERIFIED_SELLER_PROTECTION_READY"

    # Test PDF download
    resp_pdf = client.get("/api/disputes/ms-audit-9902/download-pdf")
    assert resp_pdf.status_code == 200
    assert resp_pdf.headers["content-type"] == "application/pdf"
    assert len(resp_pdf.content) > 1000

def test_proof_submission_and_autonomous_capture():
    # Create milestone
    payload = {
        "title": "Substation Wiring Verification",
        "description": "Inspect wiring and verify pressure calibration",
        "amount": 280.00,
        "currency": "USD",
        "client_name": "PowerGrid Systems",
        "client_email": "ops@powergrid.test",
        "contractor_name": "Grid Tech",
        "contractor_email": "tech@gridtech.test",
        "specifications": [
            "Wiring properly connected",
            "Manifold gauge in operating range"
        ],
        "auto_capture_on_pass": True
    }
    m = client.post("/api/escrow/create", json=payload).json()
    ms_id = m["id"]

    # Authorize
    client.post(f"/api/escrow/{ms_id}/authorize", json={"order_id": m["paypal_order_id"]})

    # Submit proof
    img_path = Path(settings.UPLOAD_FOLDER) / "sample_hvac_pass.jpg"
    with open(img_path, "rb") as f:
        files = {"file": ("sample_hvac_pass.jpg", f, "image/jpeg")}
        res = client.post(f"/api/proof/{ms_id}/submit", files=files, data={"notes": "All checks green"})
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "COMPLETED"
        assert data["verdict"]["verdict"] == "PASS"
        assert data["paypal_capture_id"] is not None

def test_state_machine_transition_guards():
    payload = {
        "title": "State Guard Testing",
        "description": "Test invalid transitions",
        "amount": 100.0,
        "currency": "USD",
        "client_name": "Guard Client",
        "client_email": "guard@client.test",
        "contractor_name": "Guard Worker",
        "contractor_email": "guard@worker.test",
        "specifications": ["Spec 1"],
        "auto_capture_on_pass": False
    }
    m = client.post("/api/escrow/create", json=payload).json()
    ms_id = m["id"]

    # 1. Cannot submit proof in DRAFT
    img_path = Path(settings.UPLOAD_FOLDER) / "sample_hvac_pass.jpg"
    with open(img_path, "rb") as f:
        bad_proof = client.post(f"/api/proof/{ms_id}/submit", files={"file": ("sample.jpg", f, "image/jpeg")})
        assert bad_proof.status_code == 400

    # 2. Authorize
    auth_resp = client.post(f"/api/escrow/{ms_id}/authorize", json={"order_id": m["paypal_order_id"]})
    assert auth_resp.status_code == 200

    # 3. Cannot authorize again
    dup_auth = client.post(f"/api/escrow/{ms_id}/authorize", json={"order_id": m["paypal_order_id"]})
    assert dup_auth.status_code == 400

    # 4. Capture
    cap_resp = client.post(f"/api/escrow/{ms_id}/capture")
    assert cap_resp.status_code == 200

    # 5. Cannot capture or void once COMPLETED
    dup_cap = client.post(f"/api/escrow/{ms_id}/capture")
    assert dup_cap.status_code == 400
    bad_void = client.post(f"/api/escrow/{ms_id}/void", json={"reason": "too late"})
    assert bad_void.status_code == 400

def test_proof_submission_validation_empty_and_bad_extension():
    # Create isolated milestone in ESCROW_LOCKED status
    create_res = client.post("/api/escrow/create", json={
        "title": "Validation Test Milestone",
        "description": "Validation test",
        "amount": 50.0,
        "currency": "USD",
        "client_name": "Client",
        "client_email": "client@test.com",
        "contractor_name": "Worker",
        "contractor_email": "worker@test.com",
        "specifications": ["Spec 1"]
    })
    ms_id = create_res.json()["id"]
    order_id = create_res.json()["paypal_order_id"]
    auth_res = client.post(f"/api/escrow/{ms_id}/authorize", json={
        "order_id": order_id
    })
    assert auth_res.status_code == 200

    # Empty 0-byte file
    empty_res = client.post(
        f"/api/proof/{ms_id}/submit",
        files={"file": ("empty.jpg", b"", "image/jpeg")}
    )
    assert empty_res.status_code == 400
    assert "cannot be empty" in empty_res.json()["detail"].lower()

    # Unsupported format (.exe)
    bad_ext_res = client.post(
        f"/api/proof/{ms_id}/submit",
        files={"file": ("malware.exe", b"MZ_EXE_HEADER", "application/octet-stream")}
    )
    assert bad_ext_res.status_code == 400
    assert "unsupported deliverable format" in bad_ext_res.json()["detail"].lower()


def test_webhook_order_approved_persists_authorization_id():
    # Create draft milestone
    payload = {
        "title": "Webhook Order Test",
        "description": "Verify webhook saves auth id",
        "amount": 175.0,
        "currency": "USD",
        "client_name": "Webhook Buyer",
        "client_email": "wb@buyer.test",
        "contractor_name": "Webhook Seller",
        "contractor_email": "wb@seller.test",
        "specifications": ["Spec 1"],
        "auto_capture_on_pass": True
    }
    m = client.post("/api/escrow/create", json=payload).json()
    ms_id = m["id"]
    order_id = m["paypal_order_id"]

    # Send CHECKOUT.ORDER.APPROVED webhook
    webhook_payload = {
        "event_type": "CHECKOUT.ORDER.APPROVED",
        "resource": {
            "id": order_id,
            "purchase_units": [{"reference_id": ms_id}]
        }
    }
    wh_resp = client.post("/api/webhooks/paypal", json=webhook_payload)
    assert wh_resp.status_code == 200

    # Fetch milestone and ensure paypal_authorization_id is persisted
    updated = client.get(f"/api/escrow/{ms_id}").json()
    assert updated["status"] == "ESCROW_LOCKED"
    assert updated["paypal_authorization_id"] is not None
    assert updated["paypal_authorization_id"].startswith("AUTH-")

