# ⚖️ ProofLedger — Node.js Reference Implementation

This directory contains the original Node.js / Express reference implementation of ProofLedger. It is fully interoperable with the ProofLedger frontend dashboard and implements the same core PayPal REST API v2 escrow lifecycle.

---

## Architecture Overview

- **Runtime**: Node.js 18+ · Express 4
- **PayPal Client**: REST API v2 OAuth2, Orders (`intent: "AUTHORIZE"`), Authorizations (`capture` / `void`)
- **AI Oracle**: OpenAI GPT-4o Vision or Deterministic Mock Mode
- **Ledger Storage**: Append-only cryptographic event log (`data/ledger.json`)
- **Port**: Defaults to `4000`

---

## Quickstart

```bash
cd node-reference/backend
npm install
cp .env.example .env
# Configure PAYPAL_CLIENT_ID and PAYPAL_CLIENT_SECRET
npm run dev
```

The Node.js backend serves endpoints at `http://localhost:4000/api/escrow/*`. The primary production backend in `backend/` runs FastAPI on `http://localhost:8000`.
