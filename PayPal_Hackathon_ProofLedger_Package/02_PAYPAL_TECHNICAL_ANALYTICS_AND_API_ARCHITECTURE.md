# PayPal Developer Platform: Technical Analytics & Architecture

This document synthesizes deep technical research into PayPal's developer rails, internal mechanics, transaction lifecycles, and comparison with other payment networks (Venmo, Xoom, UPI).

---

## 1. How PayPal Really Works Under the Hood

### The Dual-Layer Architecture: Internal Ledger vs. Banking Settlement
Most people assume PayPal moves bank money instantly. In reality, PayPal is an **asynchronous internal ledger**:

```
[Buyer Bank / Card] ──(2-3 Days ACH/Card rails)──> [PayPal Omnibus Account]
                                                          │
[Buyer PayPal Balance] ───(Instant Ledger Transfer)───> [Seller PayPal Balance]
                                                          │
[Seller PayPal Balance] ──(1-3 Days Withdrawal)───────> [Seller Bank Account]
```

1. **Instant Internal Ledger:** When User A sends \$50 to User B, no external bank money moves immediately. PayPal merely updates its internal database:
   * `Debit: User A -$50.00`
   * `Credit: User B +$50.00`
   This is why the user experience feels instantaneous.
2. **Delayed Real Settlement:** Behind the scenes, PayPal initiates an automated clearing house (ACH) pull or credit card network charge to fund that balance. The actual bank money arrives at PayPal 1 to 3 business days later.
3. **Risk Exposure & Holds:** Because PayPal credits the seller *before* the buyer's bank money clears, PayPal assumes the default risk. To protect itself, PayPal deploys automated risk algorithms that freeze funds, impose rolling reserves (e.g. 5–10% held for 60–90 days), or hold payments for up to 21–30 days on high-risk or new accounts.

---

## 2. Comparing Payment Ecosystems: PayPal vs. Venmo vs. Xoom vs. UPI

| Dimension | PayPal (Global) | Venmo (US Social P2P) | Xoom (Cross-Border Remittance) | UPI (India Instant Rail) |
| :--- | :--- | :--- | :--- | :--- |
| **Geographic Reach** | 200+ countries, 25+ currencies | US only, USD only | US/EU/UK to 160+ countries | India domestic only |
| **Core Mechanism** | Closed-loop internal ledger | Closed-loop ledger + social feed | Pre-funded local partner payout | Direct bank-to-bank switch (IMPS/NPCI) |
| **Buyer Protection** | Yes (180-day dispute window) | No (unless marked as goods/services) | No (remittance recipient receives cash/deposit) | No built-in buyer escrow/chargeback |
| **Developer API** | Comprehensive REST APIs & Webhooks | Integrated via PayPal JS SDK button | No public developer API | Bank aggregators / UPI intent |
| **Sore Spots / Gaps** | Account freezes, high fees, dispute delays | Scams via cancellation windows | Hidden exchange rate margins (2–4%) | Immediate irreversibility of mistaken transfers |

---

## 3. Transaction Lifecycle: Capture vs. Authorize

PayPal's Orders v2 API provides two fundamental payment intents:

### A. Immediate Capture (`intent: "CAPTURE"`)
* **Flow:** `Create Order` $\rightarrow$ `Buyer Approves` $\rightarrow$ `Capture Order`.
* **Use Case:** Standard eCommerce checkout (books, clothes).
* **Limitation:** Funds leave the buyer immediately. If the merchant fails to deliver or the buyer is scammed, resolving the issue requires filing a formal, protracted dispute.

### B. Two-Step Escrow Hold (`intent: "AUTHORIZE"`) — *The Foundation of ProofLedger*
* **Flow:** `Create Order` $\rightarrow$ `Buyer Approves` $\rightarrow$ `Authorize Order` $\rightarrow$ `(Hold for up to 29 days)` $\rightarrow$ `Capture` OR `Void`.
* **How Authorization Works:**
  1. The buyer's bank or PayPal balance places a guaranteed hold on the funds.
  2. The buyer cannot spend those held funds elsewhere.
  3. However, the money has **not** been transferred to the merchant yet!
  4. If the job succeeds: Merchant calls `/v2/payments/authorizations/{id}/capture`.
  5. If the job fails or proof is fraudulent: Merchant or platform calls `/v2/payments/authorizations/{id}/void`. The hold vanishes, and 100% of the money is released back to the buyer instantly without dispute fees or processing friction.

---

## 4. PayPal REST API Endpoints Required

For a production-grade hackathon integration, ProofLedger uses the following official endpoints:

### 1. OAuth2 Authentication
* **Endpoint:** `POST /v1/oauth2/token`
* **Headers:** `Authorization: Basic base64(client_id:client_secret)`
* **Body:** `grant_type=client_credentials`
* **Response:** Bearer access token valid for 9 hours.

### 2. Create Escrow Order
* **Endpoint:** `POST /v2/checkout/orders`
* **Payload:**
```json
{
  "intent": "AUTHORIZE",
  "purchase_units": [
    {
      "reference_id": "MILESTONE_101",
      "description": "Milestone 1: Smart Contract Audit & Unit Tests",
      "amount": {
        "currency_code": "USD",
        "value": "250.00"
      }
    }
  ],
  "application_context": {
    "return_url": "http://localhost:3000/escrow/approved",
    "cancel_url": "http://localhost:3000/escrow/cancelled",
    "user_action": "CONTINUE"
  }
}
```

### 3. Authorize the Payment (Hold Funds)
* **Endpoint:** `POST /v2/checkout/orders/{order_id}/authorize`
* **Response:** Returns an `authorization_id` with status `CREATED`.

### 4. Capture Payment (Release Held Funds upon AI Approval)
* **Endpoint:** `POST /v2/payments/authorizations/{authorization_id}/capture`
* **Payload:**
```json
{
  "amount": {
    "currency_code": "USD",
    "value": "250.00"
  },
  "final_capture": true,
  "note_to_payer": "ProofLedger AI: Deliverable verified (Score 96%). Payment released."
}
```

### 5. Void Authorization (Cancel Hold if Proof Fails)
* **Endpoint:** `POST /v2/payments/authorizations/{authorization_id}/void`
* **Outcome:** Releases the hold instantly back to the client's wallet.

---

## 5. PayPal Sandbox Best Practices & Quirks

When building and testing for hackathon judges:
1. **Never hardcode credentials:** Use environment variables (`PAYPAL_CLIENT_ID`, `PAYPAL_CLIENT_SECRET`, `PAYPAL_API_BASE=https://api-m.sandbox.paypal.com`).
2. **Use Sandbox Accounts:** Create a dedicated *Business Account* (to receive captures) and a *Personal Account* (with preloaded \$5,000 USD sandbox balance to approve authorizations) in the PayPal Developer Dashboard.
3. **Capture Idempotency:** Always store the PayPal `authorization_id` against your milestone in your local ledger database to prevent accidental double-captures.
