from enum import Enum
from typing import Optional, Any
from pydantic import BaseModel, Field

class MilestoneStatus(str, Enum):
    DRAFT = "DRAFT"
    ESCROW_LOCKED = "ESCROW_LOCKED"
    PROOF_SUBMITTED = "PROOF_SUBMITTED"
    AI_EVALUATING = "AI_EVALUATING"
    COMPLETED = "COMPLETED"
    NEEDS_REVIEW = "NEEDS_REVIEW"
    VOIDED = "VOIDED"
    DISPUTED = "DISPUTED"

class MilestoneCreate(BaseModel):
    title: str = Field(..., json_schema_extra={"example": "HVAC Capacitor Replacement & Calibration"})
    description: str = Field("", json_schema_extra={"example": "Replace dual-run capacitor and certify manifold pressure reading"})
    amount: float = Field(..., gt=0, json_schema_extra={"example": 250.00})
    currency: str = Field("USD", json_schema_extra={"example": "USD"})
    client_name: str = Field("Client Payer", json_schema_extra={"example": "Apex Properties LLC"})
    client_email: str = Field("client-buyer@proofledger.test", json_schema_extra={"example": "client-buyer@proofledger.test"})
    contractor_name: str = Field("Contractor Worker", json_schema_extra={"example": "Dave Vance HVAC Tech"})
    contractor_email: str = Field("contractor-seller@proofledger.test", json_schema_extra={"example": "contractor-seller@proofledger.test"})
    clientEmail: Optional[str] = None
    workerEmail: Optional[str] = None
    specifications: list[str] = Field(
        default_factory=list,
        json_schema_extra={
            "example": [
                "Original malfunctioning capacitor removed",
                "New brand-name dual run capacitor securely wired",
                "Analog or digital manifold gauge showing stable pressure reading between 60-70 PSI",
                "Work area clean with no exposed cut copper"
            ]
        }
    )
    auto_capture_on_pass: bool = Field(True, description="Autonomously capture PayPal hold if AI score >= 85%")

class CriterionCheck(BaseModel):
    criterion: str
    satisfied: bool
    confidence: float = Field(..., ge=0.0, le=100.0)
    visual_evidence: str

class AIVerdict(BaseModel):
    confidence_score: int = Field(..., ge=0, le=100)
    verdict: str = Field(..., description="PASS | NEEDS_REVIEW | FAIL")
    criteria_checklist: list[CriterionCheck]
    summary_reasoning: str
    fraud_risk_score: int = Field(0, ge=0, le=100)
    visual_anomalies: list[str] = Field(default_factory=list)
    evaluator_model: str = "ProofLedger-VisionOracle-v1"
    evaluated_at: str

class ProofMetadata(BaseModel):
    proof_id: str
    milestone_id: str
    file_name: str
    file_path: str
    file_hash: str
    file_size_bytes: int
    notes: Optional[str] = None
    submitted_at: str

class LedgerBlock(BaseModel):
    index: int
    timestamp: str
    event_type: str
    milestone_id: str
    data_hash: str
    previous_hash: str
    block_hash: str
    payload: dict[str, Any]

class MilestoneResponse(BaseModel):
    id: str
    title: str
    description: str
    amount: float
    currency: str
    client_name: str
    client_email: str
    contractor_name: str
    contractor_email: str
    specifications: list[str]
    auto_capture_on_pass: bool
    status: MilestoneStatus
    paypal_order_id: Optional[str] = None
    paypal_authorization_id: Optional[str] = None
    paypal_capture_id: Optional[str] = None
    paypal_approval_url: Optional[str] = None
    created_at: str
    updated_at: str
    proof: Optional[ProofMetadata] = None
    verdict: Optional[AIVerdict] = None

class AuthorizeOrderRequest(BaseModel):
    order_id: Optional[str] = None

class VoidAuthorizationRequest(BaseModel):
    reason: Optional[str] = "Milestone canceled or proof failed criteria"

class WebhookSimulationRequest(BaseModel):
    event_type: str
    milestone_id: str
    authorization_id: Optional[str] = None
    capture_id: Optional[str] = None
    dispute_id: Optional[str] = None

class DisputeEvidencePack(BaseModel):
    pack_id: str
    generated_at: str
    milestone_id: str
    dispute_reference_id: Optional[str] = None
    paypal_identifiers: dict[str, Any]
    contract_agreement: dict[str, Any]
    deliverable_proof: Optional[dict[str, Any]] = None
    ai_forensic_audit: Optional[dict[str, Any]] = None
    cryptographic_ledger_trail: list[dict[str, Any]]
    integrity_signature: str
    status: str = "VERIFIED_SELLER_PROTECTION_READY"
