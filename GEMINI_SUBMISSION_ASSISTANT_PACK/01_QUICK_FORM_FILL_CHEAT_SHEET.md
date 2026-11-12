# ⚡ Devpost Quick Form-Fill Cheat Sheet

> **Use this file for immediate, 1-to-1 copy-paste into Devpost fields.**

---

### 1. Project Title
```text
ProofLedger — Autonomous AI Escrow & Milestone Verification Platform
```

---

### 2. Tagline / Elevator Pitch (Max 200 characters)
```text
Trustless milestone escrow powered by PayPal Orders v2 authorization holds, multimodal AI vision verification, and cryptographic proof chaining.
```

---

### 3. Track / Category Checkboxes to Select
Check ALL of the following categories on Devpost:
- [x] **Grand Prize ($12,000)** — Best overall project combining technical innovation, PayPal API integration, and AI capabilities.
- [x] **Best Use of Agentic Commerce ($5,000)** — [⭐ PRIMARY FOCUS] Autonomous AI agent evaluating deliverables and autonomously triggering PayPal captures (on PASS) and voids (on FAIL).
- [x] **Best Use of PayPal + AI ($5,000)** — Deep programmatic synergy between PayPal authorization holds and multimodal vision forensics.
- [x] **Most Impactful ($5,000)** — Directly solves the $1.5 Trillion freelance gig economy non-payment and dispute crisis.
- [x] **Most Creative ($5,000)** — Novel reimagining of PayPal authorization holds (`intent: AUTHORIZE`) as an autonomous escrow oracle.
- [x] **Best Demo Delivery ($5,000)** — Full 1080p synchronized screen walkthrough and ReportLab PDF proof bundle.

---

### 4. Links Section

- **GitHub Source Code Repository URL:**  
  `https://github.com/Srishanth-2006/PayPal-AI-ProofLedger`

- **Demo Video URL:**  
  *(Paste the link to your uploaded YouTube / Vimeo / Loom video of `proofledger_demo_exact_2m45s.mp4`)*

- **Presentation / Pitch Deck URL (Optional):**  
  `https://github.com/Srishanth-2006/PayPal-AI-ProofLedger/blob/main/ProofLedger_PayPal_AI_Hackathon_Pitch_Deck.pptx`

---

### 5. "Built With" Technology Tags (Comma-separated)
```text
paypal-orders-v2, paypal-api, python, fastapi, react, tailwindcss, vite, computer-vision, multimodal-ai, sha-256, blockchain, sqlite, reportlab, pytest, playwright
```

---

### 6. Testing Instructions & Credentials for Judges (CRITICAL)

**Copy-paste this exact block into the "Testing Instructions" field:**

```markdown
### 🔑 Judge Testing & Verification Guide

ProofLedger is connected live to the PayPal Developer Sandbox with pre-configured OAuth2 credentials. Judges can test the entire autonomous settlement lifecycle locally or inspect our automated test suite.

#### 1. PayPal Sandbox Mode: Active & Verified
- **PayPal Client ID:** Configured in `backend/.env.example`
- **Verified App ID:** `APP-60P95806HB658054R`
- **Environment:** `https://api-m.sandbox.paypal.com`

#### 2. Test Accounts for PayPal Buyer Approval Flow:
- **Sandbox Personal (Buyer) Account:** `sb-lvrp753178518@personal.example.com`
- **Sandbox Business (Merchant) Account:** `sb-lw0is53787803@business.example.com`

#### 3. How to Run Locally in 3 Steps:
```bash
# Clone the repository
git clone https://github.com/Srishanth-2006/PayPal-AI-ProofLedger.git
cd PayPal-AI-ProofLedger

# Run the FastAPI Backend & React UI (Serves on port 8000)
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --port 8000

# Open Dashboard in Browser:
# http://localhost:8000
```

#### 4. Automated Test Verification:
Run the full Pytest test suite (all 21 tests pass in ~44 seconds):
```bash
pytest backend/tests -v
```

#### 5. Live Cryptographic Verification:
Inspect the SHA-256 tamper-proof ledger endpoint in your browser:
`http://localhost:8000/api/ledger/verify` (Returns: `tampering_detected: false`).
```

---

### 7. Custom Questions (If Asked on Devpost)

- **Q: Which PayPal APIs did you integrate?**  
  **Answer:** PayPal Orders v2 REST API (`POST /v2/checkout/orders` with `intent: "AUTHORIZE"`, `POST /v2/checkout/orders/{id}/authorize`, `POST /v2/payments/authorizations/{id}/capture`, `POST /v2/payments/authorizations/{id}/void`), OAuth2 token caching, and real-time webhook receivers.

- **Q: How does your project use AI?**  
  **Answer:** Multimodal computer vision analysis. Our AI Oracle breaks contract specifications into objective criteria checklists, forensically inspects uploaded photographic deliverables (resolution, contrast, component presence, meter readings), and autonomously triggers PayPal captures on PASS ($\ge$60%) or voids on FAIL (<60%).

- **Q: What is the repository license?**  
  **Answer:** MIT License (Open Source).
