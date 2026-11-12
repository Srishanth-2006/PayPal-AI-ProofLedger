import sys
import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    # 16:9 widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette
    BG_DARK = RGBColor(11, 15, 25)         # #0B0F19
    CARD_BG = RGBColor(15, 23, 42)         # #0F172A
    CARD_BORDER = RGBColor(30, 41, 59)     # #1E293B
    TEXT_WHITE = RGBColor(255, 255, 255)
    TEXT_MUTED = RGBColor(148, 163, 184)   # #94A3B8
    PAYPAL_BLUE = RGBColor(0, 112, 186)    # #0070BA
    CYAN_ACCENT = RGBColor(0, 207, 222)    # #00CFDE
    EMERALD = RGBColor(16, 185, 129)       # #10B981
    AMBER = RGBColor(245, 158, 11)         # #F59E0B
    ROSE = RGBColor(244, 63, 94)           # #F43F5E

    screenshots_dir = Path(r"C:\Users\Srishanth S\.gemini\antigravity\brain\9c227675-50d6-4456-aa30-0ff1fb2d4db5")
    
    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background() # no line

    def add_header(slide, category, title, subtitle=None):
        # Category pill
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.4))
        tf = cat_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = category.upper()
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = CYAN_ACCENT

        # Title
        t_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.6))
        tf2 = t_box.text_frame
        tf2.word_wrap = True
        p2 = tf2.paragraphs[0]
        p2.text = title
        p2.font.size = Pt(24)
        p2.font.bold = True
        p2.font.color.rgb = TEXT_WHITE

        # Subtitle
        if subtitle:
            s_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.25), Inches(11.7), Inches(0.4))
            tf3 = s_box.text_frame
            tf3.word_wrap = True
            p3 = tf3.paragraphs[0]
            p3.text = subtitle
            p3.font.size = Pt(13)
            p3.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, text_items, accent_color=None):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_BG
        card.line.color.rgb = accent_color or CARD_BORDER
        card.line.width = Pt(1.5 if accent_color else 1)

        tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), width - Inches(0.4), height - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(14)
        p.font.bold = True
        p.font.color.rgb = accent_color or TEXT_WHITE
        p.space_after = Pt(8)

        for item in text_items:
            p2 = tf.add_paragraph()
            p2.text = f"•  {item}"
            p2.font.size = Pt(11)
            p2.font.color.rgb = TEXT_MUTED
            p2.space_after = Pt(4)

    # -------------------------------------------------------------
    # SLIDE 1: Title Slide
    # -------------------------------------------------------------
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    # Top badge
    top_badge = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(5.2), Inches(0.45))
    top_badge.fill.solid()
    top_badge.fill.fore_color.rgb = RGBColor(0, 48, 135)
    top_badge.line.fill.background()
    tb = top_badge.text_frame
    p = tb.paragraphs[0]
    p.text = "⚡ PAYPAL AI HACKATHON 2026 SUBMISSION"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE
    p.alignment = PP_ALIGN.CENTER

    # Title
    t_box = s1.shapes.add_textbox(Inches(0.8), Inches(1.8), Inches(11.5), Inches(1.4))
    tf = t_box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ProofLedger"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = TEXT_WHITE

    p2 = tf.add_paragraph()
    p2.text = "Autonomous AI Escrow & Milestone Verification Platform"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = CYAN_ACCENT

    p3 = tf.add_paragraph()
    p3.text = "Trustless settlement powered by PayPal Orders v2 Authorization Holds, Multimodal AI Vision, and SHA-256 Proof Chaining."
    p3.font.size = Pt(14)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(8)

    # 3 Stat Cards on Title
    add_card(s1, Inches(0.8), Inches(4.5), Inches(3.6), Inches(2.2), "🤖 Target Track: Agentic Commerce", [
        "Autonomous AI decision engine",
        "Auto-captures payment on PASS (>=60%)",
        "Auto-voids hold on FAIL (<60%)",
        "True two-way programmatic commerce"
    ], CYAN_ACCENT)

    add_card(s1, Inches(4.8), Inches(4.5), Inches(3.6), Inches(2.2), "💳 Powered by PayPal Orders v2", [
        "Uses intent: AUTHORIZE for safe holds",
        "Funds locked without immediate transfer",
        "Programmatic capture/void lifecycle",
        "1-Click Dispute Defense PDF bundle"
    ], PAYPAL_BLUE)

    add_card(s1, Inches(8.8), Inches(4.5), Inches(3.6), Inches(2.2), "🛡️ Production-Grade Quality", [
        "FastAPI Backend + React 18 UI",
        "21/21 Pytest suite passing (100%)",
        "SHA-256 chained immutable ledger",
        "Zero-tampering cryptographic audits"
    ], EMERALD)

    # -------------------------------------------------------------
    # SLIDE 2: The Problem
    # -------------------------------------------------------------
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Problem & Opportunity", "The $1.5 Trillion Gig Economy Trust Crisis", 
               "Freelance commerce is broken by payment anxiety, delayed releases, and high-friction disputes.")

    add_card(s2, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "⚠️ 30% Non-Payment Rate", [
        "Over 30% of global freelancers report unpaid or severely delayed milestones.",
        "Contractors are forced to work on promises, exposing them to financial vulnerability.",
        "Lack of legal recourse for cross-border and remote digital workers."
    ], ROSE)

    add_card(s2, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "🔒 Client Fear of Incomplete Work", [
        "Clients dread paying 100% upfront for fear of receiving substandard or unfinished deliverables.",
        "Clients have no automated way to verify physical work (HVAC, solar, hardware) or technical audits.",
        "Manual inspection creates friction, friction creates delayed payouts."
    ], AMBER)

    add_card(s2, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "💸 Traditional Escrow is Slow & Expensive", [
        "Conventional platforms (Upwork, Escrow.com) charge 10% to 20% in hefty commission fees.",
        "Disputes take 2 to 6 weeks of human mediation and manual ticket filing.",
        "Both parties lose time, money, and mutual confidence."
    ], CYAN_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 3: The Solution
    # -------------------------------------------------------------
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "The Solution: ProofLedger", "Autonomous, Trustless Milestone Escrow", 
               "Combining PayPal financial rails with an autonomous multimodal AI verification oracle.")

    # Image on left
    client_img = screenshots_dir / "live_client_view.png"
    if client_img.exists():
        s3.shapes.add_picture(str(client_img), Inches(0.8), Inches(1.8), width=Inches(6.8))

    add_card(s3, Inches(7.9), Inches(1.8), Inches(4.6), Inches(4.9), "✨ Key Platform Capabilities", [
        "1. PayPal Authorization Hold: Client locks escrow using PayPal Orders v2 (intent: AUTHORIZE). Funds are reserved safely.",
        "2. Objective Contract Criteria: Contracts specify verifiable checklist items (pressure ranges, schema checks, wiring specs).",
        "3. Multimodal AI Vision Oracle: Computer vision evaluates contractor proof photos/deliverables against contractual specifications.",
        "4. Autonomous Settlement Gate: Score >= 60% releases payment via /capture; Score < 60% voids hold via /void.",
        "5. Cryptographic Proof Ledger: SHA-256 block-chained audit trail with continuous mathematical verification.",
        "6. 1-Click Dispute Defense Pack: Official ReportLab PDF evidence bundle for PayPal Resolution Center."
    ], CYAN_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 4: Architecture & Workflow
    # -------------------------------------------------------------
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Architecture", "End-to-End Autonomous Escrow Pipeline", 
               "From client contract initiation to cryptographic settlement.")

    add_card(s4, Inches(0.8), Inches(1.8), Inches(2.7), Inches(4.8), "1. Lock Escrow 🔒", [
        "Client defines milestone & criteria.",
        "PayPal Orders v2 created with intent: 'AUTHORIZE'.",
        "Client approves hold on PayPal Sandbox.",
        "Funds reserved for 29 days.",
        "Status: ESCROW_LOCKED."
    ], PAYPAL_BLUE)

    add_card(s4, Inches(3.8), Inches(1.8), Inches(2.7), Inches(4.8), "2. Submit Proof 📸", [
        "Contractor completes milestone work.",
        "Uploads photographic or digital deliverable proof.",
        "SHA-256 hash computed on upload.",
        "Proof permanently stamped.",
        "Status: PROOF_SUBMITTED."
    ], CYAN_ACCENT)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(2.7), Inches(4.8), "3. AI Evaluation 🤖", [
        "Multimodal AI Vision Oracle inspects deliverable.",
        "Forensic edge & contrast verification.",
        "Independent criteria checklist scoring.",
        "Confidence & fraud risk score generated."
    ], AMBER)

    add_card(s4, Inches(9.8), Inches(1.8), Inches(2.7), Inches(4.8), "4. Settle & Ledger ⚡", [
        "PASS (>=60%): Calls PayPal /capture. Contractor paid!",
        "FAIL (<60%): Calls PayPal /void. Client refunded!",
        "Block appended to SHA-256 Ledger.",
        "Dispute Pack PDF generated on demand."
    ], EMERALD)

    # -------------------------------------------------------------
    # SLIDE 5: PayPal API Integration
    # -------------------------------------------------------------
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Deep PayPal API Integration", "Leveraging PayPal Orders v2 for Trustless Escrow", 
               "Reimagining authorization holds as an autonomous programmable escrow mechanism.")

    add_card(s5, Inches(0.8), Inches(1.8), Inches(5.6), Inches(2.3), "🔐 Two-Step Authorization Hold Lifecycle", [
        "POST /v2/checkout/orders (intent: 'AUTHORIZE') reserves buyer funds.",
        "POST /v2/checkout/orders/{id}/authorize locks the hold programmatically.",
        "Funds remain reserved in PayPal escrow without transferring until verified.",
        "Graceful fallback layer for simulated/offline sandbox environments."
    ], PAYPAL_BLUE)

    add_card(s5, Inches(0.8), Inches(4.3), Inches(5.6), Inches(2.5), "⚡ Autonomous Financial Execution", [
        "Auto-Capture: POST /v2/payments/authorizations/{id}/capture executes when AI passes.",
        "Auto-Void: POST /v2/payments/authorizations/{id}/void cancels hold when AI fails.",
        "Zero Human Delay: Money moves programmatically based on AI judgment.",
        "State Machine Guards: Strict validation prevents duplicate captures or voids."
    ], EMERALD)

    # Webhook Simulator Screenshot on right
    webhook_img = screenshots_dir / "live_webhook_simulator.png"
    if webhook_img.exists():
        s5.shapes.add_picture(str(webhook_img), Inches(6.8), Inches(1.8), width=Inches(5.7))

    # -------------------------------------------------------------
    # SLIDE 6: AI Oracle & Multimodal Verification
    # -------------------------------------------------------------
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Autonomous AI Oracle", "Multimodal Vision Verification Engine", 
               "Objective criteria scoring that protects both contractors and clients.")

    # Scanner screenshot on left
    scanner_img = screenshots_dir / "live_contractor_scanner.png"
    if scanner_img.exists():
        s6.shapes.add_picture(str(scanner_img), Inches(0.8), Inches(1.8), width=Inches(6.4))

    add_card(s6, Inches(7.5), Inches(1.8), Inches(5.0), Inches(4.9), "🧠 How the AI Oracle Decides", [
        "Multimodal Forensic Analysis: Inspects resolution, edge variance, luminance, and contrast.",
        "Independent Criteria Checklist: Breaks the contract into atomic specifications and validates each individually.",
        "Visual Evidence Documentation: Outputs observable evidence rationale for every checklist item.",
        "Dual-Pathway Settlement: Happy path (PASS >=60%) triggers PayPal capture. Rejection path (FAIL <60%) triggers PayPal void.",
        "Responsible AI Overrides: Humans retain full governance with Manual Release and Manual Void controls.",
        "Evaluator Models: Pluggable architecture supporting Gemini 1.5/2.0 Flash, Vision LLMs, or calibrated offline oracles."
    ], CYAN_ACCENT)

    # -------------------------------------------------------------
    # SLIDE 7: Cryptographic Ledger & Dispute Pack
    # -------------------------------------------------------------
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Auditability & Seller Protection", "Cryptographic Proof Ledger & Dispute Defense Pack", 
               "Mathematical proof that guarantees zero tampering and immediate dispute resolution.")

    # Ledger screenshot on left
    ledger_img = screenshots_dir / "live_proof_ledger.png"
    if ledger_img.exists():
        s7.shapes.add_picture(str(ledger_img), Inches(0.8), Inches(1.8), width=Inches(5.7))

    # Dispute pack screenshot on right
    dispute_img = screenshots_dir / "live_dispute_pack_modal.png"
    if dispute_img.exists():
        s7.shapes.add_picture(str(dispute_img), Inches(6.8), Inches(1.8), width=Inches(5.7))

    # -------------------------------------------------------------
    # SLIDE 8: Technical Excellence
    # -------------------------------------------------------------
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Technical Rigor & Quality", "Production-Ready Full-Stack Implementation", 
               "Fully tested, benchmarked, and integrated codebase.")

    add_card(s8, Inches(0.8), Inches(1.8), Inches(3.7), Inches(4.8), "✅ 21/21 Tests Passing (100%)", [
        "Comprehensive Pytest test suite.",
        "test_ai_oracle.py (11 tests): Edge cases, fraud detection, low-contrast checks.",
        "test_escrow_api.py (6 tests): State guards, creation, proof validation.",
        "test_ledger_service.py (3 tests): Hash chaining & tamper detection.",
        "test_paypal_service.py (1 test): Orders v2 auth & capture."
    ], EMERALD)

    add_card(s8, Inches(4.8), Inches(1.8), Inches(3.7), Inches(4.8), "⚡ Modern Enterprise Stack", [
        "FastAPI Backend: High-concurrency async Python with automatic OpenAPI docs.",
        "SQLite Persistence: Full ACID transactions for financial ledger integrity.",
        "React 18 + Tailwind: Responsive dashboard, Plus Jakarta Sans typography.",
        "ReportLab Engine: Generates signed 2-page forensic PDF dispute packs on the fly."
    ], CYAN_ACCENT)

    add_card(s8, Inches(8.8), Inches(1.8), Inches(3.7), Inches(4.8), "🔄 Unified Architecture", [
        "Integrated Node.js Reference: Cleanly preserved in node-reference/.",
        "Full API Parity: Supports both FastAPI and Express microservice payloads.",
        "Automated Playwright Suite: Programmatic demo recording and test bots in scripts/.",
        "MIT Open Source: Clean, extensible codebase ready for enterprise adoption."
    ], AMBER)

    # -------------------------------------------------------------
    # SLIDE 9: Market Impact & Business Model
    # -------------------------------------------------------------
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Market Impact & Monetization", "Empowering the Future of Autonomous Commerce", 
               "Scalable, high-margin, and transformative across multiple multibillion-dollar verticals.")

    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "🌍 Multi-Vertical Market Opportunity", [
        "Freelance Software & Design: Web3 audits, UI design, bug bounties ($1.5T Gig Economy).",
        "Physical Services & Maintenance: HVAC, solar installation, commercial refrigeration ($500B Facility Services).",
        "AI Agent-to-Agent Commerce: Autonomous data bounty scrapers, model evaluation tasks, dataset labeling.",
        "IP Licensing & B2B Milestones: Automated contract payouts based on verifiable milestones.",
        "Reduces platform dispute overhead by up to 90% through photographic AI verification."
    ], CYAN_ACCENT)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "💰 Sustainable Business Model", [
        "1.5% Micro-Fee on Successful Settlements: Far lower than Upwork's 10% or Escrow.com's 3.25%, driving massive volume.",
        "Enterprise Dispute Pack SaaS: Premium forensic PDF audit trails for commercial contractors ($49/month).",
        "PayPal Transaction Volume Multiplier: Drives high-volume, high-trust cross-border authorization hold transactions through PayPal rails.",
        "Zero Human Overhead: Near 100% gross margin on automated settlement evaluations."
    ], EMERALD)

    # -------------------------------------------------------------
    # SLIDE 10: Conclusion & Hackathon Winning Verdict
    # -------------------------------------------------------------
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Summary & Conclusion", "Why ProofLedger Wins the PayPal AI Hackathon", 
               "The definitive benchmark for Agentic Commerce and PayPal + AI integration.")

    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.6), Inches(4.8), "🏆 Why ProofLedger Stands Out", [
        "⭐ Genuine Agentic Commerce: An AI agent that moves real money bidirectionally (auto-capture on pass, auto-void on fail).",
        "⭐ Deep PayPal Integration: Full Orders v2 authorization hold lifecycle, sandbox tested and verified.",
        "⭐ Solves a Real $1.5T Problem: Eliminates freelance payment delays, fraud, and painful dispute arbitration.",
        "⭐ Cryptographic Trust: SHA-256 block-chained immutable ledger guarantees zero data tampering.",
        "⭐ 100% Complete & Tested: Working production UI, 21/21 passing tests, automated recording suite."
    ], CYAN_ACCENT)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.7), Inches(4.8), "🔗 Project Links & Verification", [
        "GitHub Repository: https://github.com/Srishanth-2006/PayPal-AI-ProofLedger",
        "Demo Video: demo_recording/proofledger_master_demo_extended_2m45s.mp4",
        "Live Sandbox Credentials: Mode Active (APP-60P95806HB658054R)",
        "Test Buyer Account: sb-lvrp753178518@personal.example.com",
        "Test Merchant Account: sb-lw0is53787803@business.example.com",
        "Local Run Command: python -m uvicorn app.main:app --port 8000"
    ], PAYPAL_BLUE)

    output_path = Path(r"c:\Users\Srishanth S\Desktop\Sri folder\PayPal AI Hackathon\ProofLedger_PayPal_AI_Hackathon_Pitch_Deck.pptx")
    prs.save(str(output_path))
    print(f"Presentation saved successfully to: {output_path}")

if __name__ == "__main__":
    create_deck()
