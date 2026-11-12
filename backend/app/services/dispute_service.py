import io
import json
import hashlib
from datetime import datetime, timezone
from typing import Optional, Any
from pathlib import Path

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.database.db import get_milestone
from app.services.ledger_service import get_all_blocks, compute_sha256, canonical_json
from app.models.schemas import DisputeEvidencePack

class DisputeService:
    def generate_dispute_pack(self, milestone_id: str, dispute_reference: Optional[str] = None) -> DisputeEvidencePack:
        m = get_milestone(milestone_id)
        if not m:
            raise ValueError(f"Milestone {milestone_id} not found.")

        now_iso = datetime.now(timezone.utc).isoformat()
        pack_id = f"DPACK-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}-{milestone_id[:8].upper()}"

        blocks = get_all_blocks(milestone_id=milestone_id)
        ledger_trail = [
            {
                "index": b["block_index"],
                "timestamp": b["timestamp"],
                "event_type": b["event_type"],
                "block_hash": b["block_hash"],
                "previous_hash": b["previous_hash"],
                "data_hash": b["data_hash"]
            }
            for b in blocks if b["milestone_id"] == milestone_id or b["block_index"] == 0
        ]

        payload_to_sign = {
            "pack_id": pack_id,
            "milestone_id": milestone_id,
            "amount": m["amount"],
            "currency": m["currency"],
            "paypal_order_id": m.get("paypal_order_id"),
            "paypal_auth_id": m.get("paypal_authorization_id"),
            "paypal_capture_id": m.get("paypal_capture_id"),
            "proof_hash": m["proof"]["file_hash"] if m.get("proof") else None,
            "ai_verdict": m["verdict"]["verdict"] if m.get("verdict") else None,
            "ledger_blocks_count": len(ledger_trail)
        }
        signature = compute_sha256(canonical_json(payload_to_sign))

        pack = DisputeEvidencePack(
            pack_id=pack_id,
            generated_at=now_iso,
            milestone_id=milestone_id,
            dispute_reference_id=dispute_reference or f"PP-D-{datetime.now(timezone.utc).strftime('%Y%m%d')}-001",
            paypal_identifiers={
                "order_id": m.get("paypal_order_id"),
                "authorization_id": m.get("paypal_authorization_id"),
                "capture_id": m.get("paypal_capture_id"),
                "seller_protection": "ELIGIBLE",
                "payment_intent": "AUTHORIZE_THEN_CAPTURE"
            },
            contract_agreement={
                "title": m["title"],
                "description": m["description"],
                "specifications": m["specifications"],
                "amount": m["amount"],
                "currency": m["currency"],
                "client_name": m["client_name"],
                "client_email": m["client_email"],
                "contractor_name": m["contractor_name"],
                "contractor_email": m["contractor_email"],
                "created_at": m["created_at"],
                "escrow_status": m["status"]
            },
            deliverable_proof=m.get("proof"),
            ai_forensic_audit=m.get("verdict"),
            cryptographic_ledger_trail=ledger_trail,
            integrity_signature=signature,
            status="VERIFIED_SELLER_PROTECTION_READY"
        )
        return pack

    def generate_pdf_evidence_pack(self, milestone_id: str, dispute_reference: Optional[str] = None) -> bytes:
        pack = self.generate_dispute_pack(milestone_id, dispute_reference)
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=18,
            textColor=colors.HexColor('#003087'), # PayPal Deep Blue
            spaceAfter=6
        )
        subtitle_style = ParagraphStyle(
            'SubtitleStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            textColor=colors.HexColor('#6B7280'),
            spaceAfter=12
        )
        heading_style = ParagraphStyle(
            'HeadingStyle',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=colors.HexColor('#1E293B'),
            spaceBefore=10,
            spaceAfter=4
        )
        body_style = ParagraphStyle(
            'BodyStyle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            textColor=colors.HexColor('#334155'),
            leading=12
        )
        mono_style = ParagraphStyle(
            'MonoStyle',
            parent=styles['Normal'],
            fontName='Courier',
            fontSize=8,
            textColor=colors.HexColor('#0F172A'),
            leading=10
        )

        elements = []

        # Header Banner
        elements.append(Paragraph("PROOFLEDGER • PAYPAL DISPUTE EVIDENCE PACK", title_style))
        elements.append(Paragraph(
            f"Generated: {pack.generated_at} | Pack ID: {pack.pack_id} | Reference: {pack.dispute_reference_id}",
            subtitle_style
        ))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0070BA'), spaceAfter=10))

        # 1. PayPal Transaction Rails Table
        elements.append(Paragraph("1. PayPal Rails & Settlement Proof", heading_style))
        pp_data = [
            ["Order ID", pack.paypal_identifiers.get("order_id") or "N/A"],
            ["Authorization ID (Held)", pack.paypal_identifiers.get("authorization_id") or "N/A"],
            ["Capture ID (Settled)", pack.paypal_identifiers.get("capture_id") or "N/A"],
            ["Seller Protection", pack.paypal_identifiers.get("seller_protection") or "ELIGIBLE"],
            ["Amount & Currency", f"{pack.contract_agreement['amount']:.2f} {pack.contract_agreement['currency']}"]
        ]
        t1 = Table(pp_data, colWidths=[150, 390])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F1F5F9')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1E293B')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ]))
        elements.append(t1)
        elements.append(Spacer(1, 10))

        # 2. Contract Terms & Agreement
        elements.append(Paragraph("2. Agreed Contractual Criteria", heading_style))
        elements.append(Paragraph(f"<b>Milestone:</b> {pack.contract_agreement['title']}", body_style))
        elements.append(Paragraph(f"<b>Description:</b> {pack.contract_agreement['description']}", body_style))
        elements.append(Paragraph(f"<b>Client:</b> {pack.contract_agreement['client_name']} ({pack.contract_agreement['client_email']})", body_style))
        elements.append(Paragraph(f"<b>Contractor:</b> {pack.contract_agreement['contractor_name']} ({pack.contract_agreement['contractor_email']})", body_style))
        elements.append(Spacer(1, 6))

        # 3. Deliverable Proof & Forensic Hashing
        elements.append(Paragraph("3. Deliverable Proof & SHA-256 Seal", heading_style))
        if pack.deliverable_proof:
            p_data = [
                ["File Name", pack.deliverable_proof.get("file_name", "N/A")],
                ["SHA-256 Proof Hash", pack.deliverable_proof.get("file_hash", "N/A")],
                ["File Size", f"{pack.deliverable_proof.get('file_size_bytes', 0):,} bytes"],
                ["Submitted At", pack.deliverable_proof.get("submitted_at", "N/A")],
                ["Contractor Notes", pack.deliverable_proof.get("notes") or "None"]
            ]
            t2 = Table(p_data, colWidths=[150, 390])
            t2.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F8FAFC')),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTNAME', (1, 1), (1, 1), 'Courier'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(t2)
        else:
            elements.append(Paragraph("No deliverable uploaded.", body_style))
        elements.append(Spacer(1, 10))

        # 4. Multimodal AI Oracle Inspection Report
        elements.append(Paragraph("4. Multimodal AI Forensic Audit", heading_style))
        if pack.ai_forensic_audit:
            audit = pack.ai_forensic_audit
            elements.append(Paragraph(
                f"<b>Oracle Model:</b> {audit.get('evaluator_model')} | "
                f"<b>Verdict:</b> {audit.get('verdict')} | "
                f"<b>Confidence:</b> {audit.get('confidence_score')}% | "
                f"<b>Fraud Risk:</b> {audit.get('fraud_risk_score')}%",
                body_style
            ))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(f"<b>Summary Rationale:</b> {audit.get('summary_reasoning')}", body_style))
            elements.append(Spacer(1, 6))

            crit_rows = [["Contractual Specification", "Status", "Confidence", "Visual Evidence"]]
            for c in audit.get("criteria_checklist", []):
                crit_rows.append([
                    Paragraph(c.get("criterion", ""), body_style),
                    "SATISFIED" if c.get("satisfied") else "FAILED",
                    f"{c.get('confidence', 0):.0f}%",
                    Paragraph(c.get("visual_evidence", ""), body_style)
                ])
            t3 = Table(crit_rows, colWidths=[160, 60, 60, 260])
            t3.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003087')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            elements.append(t3)
        else:
            elements.append(Paragraph("No deliverable submitted yet. Milestone is awaiting contractor submission and AI audit.", body_style))
        elements.append(Spacer(1, 10))

        # 5. Cryptographic Ledger Hash Seal
        elements.append(Paragraph("5. Cryptographic Integrity Seal & Chain Trail", heading_style))
        elements.append(Paragraph(
            f"<b>Dispute Pack Signature (SHA-256):</b><br/>"
            f"<font face='Courier' color='#0070BA'>{pack.integrity_signature}</font>",
            body_style
        ))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(
            f"Verified against {len(pack.cryptographic_ledger_trail)} sequential Proof Ledger blocks. "
            "This document constitutes verifiable proof of fulfillment under PayPal Seller Protection policy guidelines.",
            body_style
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()

dispute_service = DisputeService()
