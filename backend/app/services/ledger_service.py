import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Optional
from app.database.db import get_db_connection

GENESIS_PREV_HASH = "0" * 64

def compute_sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()

def canonical_json(data: Any) -> str:
    return json.dumps(data, sort_keys=True, separators=(',', ':'), default=str)

def get_latest_block() -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ledger_blocks ORDER BY block_index DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()
    if not row:
        return None
    d = dict(row)
    d["payload"] = json.loads(d["payload"])
    return d

def ensure_genesis_block():
    latest = get_latest_block()
    if latest is not None:
        return
    
    timestamp = "2026-10-01T00:00:00.000000Z"
    event_type = "GENESIS"
    milestone_id = "00000000-0000-0000-0000-000000000000"
    payload = {
        "network": "PayPal AI Hackathon 2026",
        "protocol": "ProofLedger-v1.0",
        "description": "Genesis block for autonomous escrow & multimodal milestone verification."
    }
    data_hash = compute_sha256(canonical_json(payload))
    prev_hash = GENESIS_PREV_HASH
    
    header = f"0:{timestamp}:{event_type}:{milestone_id}:{prev_hash}:{data_hash}"
    block_hash = compute_sha256(header)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ledger_blocks (
        block_index, timestamp, event_type, milestone_id, data_hash, previous_hash, block_hash, payload
    ) VALUES (0, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, event_type, milestone_id, data_hash, prev_hash, block_hash, json.dumps(payload)))
    conn.commit()
    conn.close()

def append_block(event_type: str, milestone_id: str, payload: dict) -> dict:
    ensure_genesis_block()
    latest = get_latest_block()
    
    next_index = latest["block_index"] + 1 if latest else 0
    prev_hash = latest["block_hash"] if latest else GENESIS_PREV_HASH
    timestamp = datetime.now(timezone.utc).isoformat()
    
    data_hash = compute_sha256(canonical_json(payload))
    header = f"{next_index}:{timestamp}:{event_type}:{milestone_id}:{prev_hash}:{data_hash}"
    block_hash = compute_sha256(header)
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO ledger_blocks (
        block_index, timestamp, event_type, milestone_id, data_hash, previous_hash, block_hash, payload
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (next_index, timestamp, event_type, milestone_id, data_hash, prev_hash, block_hash, json.dumps(payload)))
    conn.commit()
    conn.close()
    
    return {
        "index": next_index,
        "timestamp": timestamp,
        "event_type": event_type,
        "milestone_id": milestone_id,
        "data_hash": data_hash,
        "previous_hash": prev_hash,
        "block_hash": block_hash,
        "payload": payload
    }

def get_all_blocks(milestone_id: Optional[str] = None) -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if milestone_id:
        cursor.execute("SELECT * FROM ledger_blocks WHERE milestone_id = ? OR block_index = 0 ORDER BY block_index ASC", (milestone_id,))
    else:
        cursor.execute("SELECT * FROM ledger_blocks ORDER BY block_index ASC")
    rows = cursor.fetchall()
    conn.close()
    
    blocks = []
    for r in rows:
        b = dict(r)
        b["payload"] = json.loads(b["payload"])
        blocks.append(b)
    return blocks

def verify_chain_integrity() -> dict:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM ledger_blocks ORDER BY block_index ASC")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return {"is_valid": True, "total_blocks": 0, "message": "Ledger is empty."}
        
    prev_hash = GENESIS_PREV_HASH
    for i, r in enumerate(rows):
        b = dict(r)
        if b["block_index"] != i:
            return {
                "is_valid": False,
                "broken_index": i,
                "reason": f"Block index sequence mismatch: expected {i}, found {b['block_index']}"
            }
        
        if b["previous_hash"] != prev_hash:
            return {
                "is_valid": False,
                "broken_index": i,
                "reason": f"Previous hash mismatch at block {i}: expected {prev_hash}, found {b['previous_hash']}"
            }
            
        payload = json.loads(b["payload"])
        recalculated_data_hash = compute_sha256(canonical_json(payload))
        if recalculated_data_hash != b["data_hash"]:
            return {
                "is_valid": False,
                "broken_index": i,
                "reason": f"Data payload hash mismatch at block {i}: payload has been altered!"
            }
            
        header = f"{b['block_index']}:{b['timestamp']}:{b['event_type']}:{b['milestone_id']}:{b['previous_hash']}:{b['data_hash']}"
        recalculated_block_hash = compute_sha256(header)
        if recalculated_block_hash != b["block_hash"]:
            return {
                "is_valid": False,
                "broken_index": i,
                "reason": f"Block hash invalid at block {i}: header calculation mismatch!"
            }
            
        prev_hash = b["block_hash"]
        
    return {
        "is_valid": True,
        "total_blocks": len(rows),
        "latest_block_hash": prev_hash,
        "message": f"Cryptographic integrity verified across {len(rows)} sequential blocks. Zero tampering detected."
    }
