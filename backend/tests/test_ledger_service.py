import pytest
import json
from app.services.ledger_service import (
    ensure_genesis_block, append_block, get_all_blocks, verify_chain_integrity, compute_sha256, canonical_json
)
from app.database.db import init_db, get_db_connection

def setup_module():
    init_db()
    ensure_genesis_block()

def test_genesis_block_exists():
    blocks = get_all_blocks()
    assert len(blocks) >= 1
    genesis = blocks[0]
    assert genesis["block_index"] == 0
    assert genesis["event_type"] == "GENESIS"
    assert genesis["previous_hash"] == "0" * 64

def test_append_block_and_verify():
    b = append_block(
        event_type="TEST_EVENT",
        milestone_id="test-ms-001",
        payload={"action": "test", "value": 123}
    )
    assert b["index"] > 0
    assert b["event_type"] == "TEST_EVENT"
    assert len(b["block_hash"]) == 64

    # Verify chain integrity
    report = verify_chain_integrity()
    assert report["is_valid"] is True
    assert report["total_blocks"] >= 2

def test_tamper_detection():
    # Insert a tampered block directly into DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ledger_blocks ORDER BY block_index DESC LIMIT 1")
    last_block = dict(cursor.fetchone())
    
    # Tamper payload
    tampered_payload = {"action": "tampered_hack", "value": 999999}
    cursor.execute(
        "UPDATE ledger_blocks SET payload = ? WHERE block_index = ?",
        (json.dumps(tampered_payload), last_block["block_index"])
    )
    conn.commit()
    conn.close()

    # Integrity verification must detect tampering!
    tamper_report = verify_chain_integrity()
    assert tamper_report["is_valid"] is False
    assert "mismatch" in tamper_report["reason"] or "altered" in tamper_report["reason"]

    # Restore valid payload
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE ledger_blocks SET payload = ? WHERE block_index = ?",
        (last_block["payload"], last_block["block_index"])
    )
    conn.commit()
    conn.close()

    # Verification must be valid again
    restored_report = verify_chain_integrity()
    assert restored_report["is_valid"] is True
