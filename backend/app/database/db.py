import sqlite3
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Any
from app.config import settings

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Milestones
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS milestones (
        id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        currency TEXT NOT NULL DEFAULT 'USD',
        client_name TEXT NOT NULL,
        client_email TEXT NOT NULL,
        contractor_name TEXT NOT NULL,
        contractor_email TEXT NOT NULL,
        specifications TEXT NOT NULL,
        auto_capture_on_pass INTEGER NOT NULL DEFAULT 1,
        status TEXT NOT NULL,
        paypal_order_id TEXT,
        paypal_authorization_id TEXT,
        paypal_capture_id TEXT,
        paypal_approval_url TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
    )
    """)

    # 2. Proof Deliverables
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS proofs (
        proof_id TEXT PRIMARY KEY,
        milestone_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_hash TEXT NOT NULL,
        file_size_bytes INTEGER NOT NULL,
        notes TEXT,
        submitted_at TEXT NOT NULL,
        FOREIGN KEY (milestone_id) REFERENCES milestones (id)
    )
    """)

    # 3. AI Verdicts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS verdicts (
        milestone_id TEXT PRIMARY KEY,
        confidence_score INTEGER NOT NULL,
        verdict TEXT NOT NULL,
        criteria_checklist TEXT NOT NULL,
        summary_reasoning TEXT NOT NULL,
        fraud_risk_score INTEGER NOT NULL DEFAULT 0,
        visual_anomalies TEXT NOT NULL,
        evaluator_model TEXT NOT NULL,
        evaluated_at TEXT NOT NULL,
        FOREIGN KEY (milestone_id) REFERENCES milestones (id)
    )
    """)

    # 4. Cryptographic Proof Ledger Blocks
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ledger_blocks (
        block_index INTEGER PRIMARY KEY,
        timestamp TEXT NOT NULL,
        event_type TEXT NOT NULL,
        milestone_id TEXT NOT NULL,
        data_hash TEXT NOT NULL,
        previous_hash TEXT NOT NULL,
        block_hash TEXT NOT NULL,
        payload TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

def save_milestone(m: dict) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO milestones (
        id, title, description, amount, currency, client_name, client_email,
        contractor_name, contractor_email, specifications, auto_capture_on_pass,
        status, paypal_order_id, paypal_authorization_id, paypal_capture_id,
        paypal_approval_url, created_at, updated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(id) DO UPDATE SET
        title=excluded.title,
        description=excluded.description,
        amount=excluded.amount,
        currency=excluded.currency,
        client_name=excluded.client_name,
        client_email=excluded.client_email,
        contractor_name=excluded.contractor_name,
        contractor_email=excluded.contractor_email,
        specifications=excluded.specifications,
        auto_capture_on_pass=excluded.auto_capture_on_pass,
        status=excluded.status,
        paypal_order_id=excluded.paypal_order_id,
        paypal_authorization_id=excluded.paypal_authorization_id,
        paypal_capture_id=excluded.paypal_capture_id,
        paypal_approval_url=excluded.paypal_approval_url,
        updated_at=excluded.updated_at
    """, (
        m["id"], m["title"], m["description"], m["amount"], m.get("currency", "USD"),
        m["client_name"], m["client_email"], m["contractor_name"], m["contractor_email"],
        json.dumps(m["specifications"]) if isinstance(m["specifications"], list) else m["specifications"],
        1 if m.get("auto_capture_on_pass", True) else 0,
        m["status"], m.get("paypal_order_id"), m.get("paypal_authorization_id"),
        m.get("paypal_capture_id"), m.get("paypal_approval_url"),
        m["created_at"], m.get("updated_at", m["created_at"])
    ))
    conn.commit()
    conn.close()

def get_milestone(milestone_id: str) -> Optional[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM milestones WHERE id = ?", (milestone_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    data = dict(row)
    data["specifications"] = json.loads(data["specifications"])
    data["auto_capture_on_pass"] = bool(data["auto_capture_on_pass"])
    
    # fetch proof
    cursor.execute("SELECT * FROM proofs WHERE milestone_id = ?", (milestone_id,))
    p_row = cursor.fetchone()
    if p_row:
        data["proof"] = dict(p_row)
    else:
        data["proof"] = None
        
    # fetch verdict
    cursor.execute("SELECT * FROM verdicts WHERE milestone_id = ?", (milestone_id,))
    v_row = cursor.fetchone()
    if v_row:
        v_data = dict(v_row)
        v_data["criteria_checklist"] = json.loads(v_data["criteria_checklist"])
        v_data["visual_anomalies"] = json.loads(v_data["visual_anomalies"])
        data["verdict"] = v_data
    else:
        data["verdict"] = None

    conn.close()
    return data

def list_milestones() -> list[dict]:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM milestones ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        m = get_milestone(r["id"])
        if m:
            results.append(m)
    return results

def save_proof(p: dict) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO proofs (
        proof_id, milestone_id, file_name, file_path, file_hash, file_size_bytes, notes, submitted_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(proof_id) DO UPDATE SET
        file_name=excluded.file_name,
        file_path=excluded.file_path,
        file_hash=excluded.file_hash,
        file_size_bytes=excluded.file_size_bytes,
        notes=excluded.notes,
        submitted_at=excluded.submitted_at
    """, (
        p["proof_id"], p["milestone_id"], p["file_name"], p["file_path"],
        p["file_hash"], p["file_size_bytes"], p.get("notes"), p["submitted_at"]
    ))
    conn.commit()
    conn.close()

def save_verdict(v: dict) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO verdicts (
        milestone_id, confidence_score, verdict, criteria_checklist, summary_reasoning,
        fraud_risk_score, visual_anomalies, evaluator_model, evaluated_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(milestone_id) DO UPDATE SET
        confidence_score=excluded.confidence_score,
        verdict=excluded.verdict,
        criteria_checklist=excluded.criteria_checklist,
        summary_reasoning=excluded.summary_reasoning,
        fraud_risk_score=excluded.fraud_risk_score,
        visual_anomalies=excluded.visual_anomalies,
        evaluator_model=excluded.evaluator_model,
        evaluated_at=excluded.evaluated_at
    """, (
        v["milestone_id"], v["confidence_score"], v["verdict"],
        json.dumps(v["criteria_checklist"]) if isinstance(v["criteria_checklist"], list) else v["criteria_checklist"],
        v["summary_reasoning"], v.get("fraud_risk_score", 0),
        json.dumps(v.get("visual_anomalies", [])) if isinstance(v.get("visual_anomalies"), list) else v.get("visual_anomalies", "[]"),
        v.get("evaluator_model", "ProofLedger-VisionOracle-v1"),
        v["evaluated_at"]
    ))
    conn.commit()
    conn.close()
