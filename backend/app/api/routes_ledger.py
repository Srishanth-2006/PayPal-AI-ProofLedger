from typing import Optional
from fastapi import APIRouter
from app.services.ledger_service import get_all_blocks, verify_chain_integrity

router = APIRouter(prefix="/ledger", tags=["Cryptographic Ledger"])

@router.get("/blocks")
def list_ledger_blocks(milestone_id: Optional[str] = None):
    return get_all_blocks(milestone_id=milestone_id)

@router.get("/verify")
def verify_ledger():
    return verify_chain_integrity()
