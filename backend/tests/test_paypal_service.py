import asyncio
from app.services.paypal_service import paypal_service

def test_paypal_create_escrow_order():
    order = asyncio.run(paypal_service.create_escrow_order(
        milestone_id="test-order-101",
        amount=250.00,
        currency="USD",
        title="Test Escrow Milestone"
    ))
    assert "id" in order
    assert order["intent"] == "AUTHORIZE"
    assert len(order["purchase_units"]) == 1
    assert order["purchase_units"][0]["amount"]["value"] == "250.00"

def test_paypal_authorize_order():
    auth_resp = asyncio.run(paypal_service.authorize_order("ORD-SANDBOX-TEST"))
    assert "status" in auth_resp
    authorizations = auth_resp["purchase_units"][0]["payments"]["authorizations"]
    assert len(authorizations) >= 1
    assert authorizations[0]["status"] == "CREATED"

def test_paypal_capture_authorization():
    cap_resp = asyncio.run(paypal_service.capture_authorization(
        authorization_id="AUTH-SANDBOX-TEST",
        amount=250.00,
        currency="USD",
        note_to_payer="Deliverable verified"
    ))
    assert cap_resp["status"] == "COMPLETED"
    assert "id" in cap_resp

def test_paypal_void_authorization():
    void_resp = asyncio.run(paypal_service.void_authorization(
        authorization_id="AUTH-SANDBOX-TEST",
        reason="Test cancel"
    ))
    assert void_resp["status"] == "VOIDED"
