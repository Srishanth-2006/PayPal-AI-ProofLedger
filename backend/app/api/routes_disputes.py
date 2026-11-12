from typing import Optional
from fastapi import APIRouter, HTTPException, Response
from app.services.dispute_service import dispute_service
from app.models.schemas import DisputeEvidencePack

router = APIRouter(prefix="/disputes", tags=["Dispute Protection"])

@router.get("/{milestone_id}/pack", response_model=DisputeEvidencePack)
def get_evidence_pack(milestone_id: str, dispute_reference: Optional[str] = None):
    try:
        return dispute_service.generate_dispute_pack(milestone_id, dispute_reference)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/{milestone_id}/download-pdf")
def download_evidence_pdf(milestone_id: str, dispute_reference: Optional[str] = None):
    try:
        pdf_bytes = dispute_service.generate_pdf_evidence_pack(milestone_id, dispute_reference)
        filename = f"ProofLedger_DisputePack_{milestone_id[:8]}.pdf"
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
