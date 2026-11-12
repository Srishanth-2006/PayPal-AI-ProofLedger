# PayPal AI Hackathon: Official Guide, Rules & Strategic Analytics

**Event:** PayPal AI Hackathon (*"Build What's Next with PayPal and AI"*)  
**Host Platform:** Devpost (`https://paypalaihackathon.devpost.com/`)  
**Sponsor:** PayPal Inc. (San Jose, CA, USA)  
**Administrator:** Devpost, Inc. (New York, NY, USA)  
**Total Prize Pool:** $67,500+ USD  

---

## 1. Key Dates & Critical Timeline

| Phase | Date / Time (Pacific Time) | Date / Time (Indian Standard Time) | Notes |
| :--- | :--- | :--- | :--- |
| **Submission Deadline** | **Thursday, Nov 12, 2026 @ 12:00 PM PT** | **Friday, Nov 13, 2026 @ 1:30 AM IST** | Hard cutoff on Devpost. No edits to entry after this. |
| **Judging Period** | Dec 1, 2026 (2:00 PM PT) – Dec 15, 2026 (8:00 AM PT) | Dec 2, 2026 – Dec 15, 2026 | Evaluated by expert panels and sponsor judges. |
| **Winners Announced** | Dec 21, 2026 @ 2:00 PM PT | Dec 22, 2026 @ 3:30 AM IST | Announced on Devpost and PayPal Developer channels. |

---

## 2. Prize Matrix & Target Tracks

### A. Grand Prizes (Open to All Submissions)
* **1st Place:** $12,000 USD
* **2nd Place:** $8,000 USD
* **3rd Place:** $5,000 USD

### B. Special Achievement Category Awards ($5,000 each)
* **Best Use of Agentic Commerce ($5,000 USD):** Awarded to projects where autonomous AI agents initiate, negotiate, verify, or execute commerce via PayPal.
* **Best Use of PayPal + AI ($5,000 USD):** Best synthesis of artificial intelligence (LLMs, computer vision, predictive agents) with PayPal's payment rails.
* **Most Impactful ($5,000 USD):** Real-world viability, solving acute consumer or business pain points.
* **Most Creative ($5,000 USD):** Most novel concept out of the box.
* **Best Demo Delivery ($5,000 USD):** Highest presentation quality, clearest video walkthrough (<3 min), compelling narrative.

### C. Sponsor Prizes (Partner Integrations)
* **Best Use of AG Grid:** 1st: $5,000 | 2nd: $2,000 | 3rd: $1,000
* **Best Use of APIMatic:** $1,000 + 6 mos business subscription (3 winners)
* **Best Use of Bryntum:** $1,000 (3 winners)
* **Best Use of Channel3:** $1,500 (1 winner)
* **Best Use of Render:** 1st: $1,000 credits | 2nd: $500 credits

---

## 3. Two-Stage Judging Rubric & Strategy

### Stage One: Pass / Fail Baseline
Judges screen for two simple requirements:
1. Reasonable fit with the hackathon theme (AI + Payments).
2. Genuine use of the PayPal Developer Platform (REST APIs or SDKs in the Sandbox).

### Stage Two: Scored Criteria (Equally Weighted - 20% Each)

```
┌─────────────────────────────────────────────────────────────┐
│                   Stage Two: 100 Points Total                │
├──────────────────────────┬──────────────────────────────────┤
│ 1. Technological (20%)   │ Deep use of PayPal & AI tooling  │
│ 2. Design & UX (20%)     │ Coherent, usable product flow    │
│ 3. Potential Impact (20%)│ Solves a genuine, tangible pain  │
│ 4. Innovation (20%)      │ Distinct from typical hack ideas │
│ 5. Presentation (20%)    │ Crisp, working <3-min demo video │
└──────────────────────────┴──────────────────────────────────┘
```

1. **Technological Implementation (20%):**
   * *What Judges Look For:* How thoroughly and skillfully does the project use the PayPal Developer Platform and AI tool(s)? Does it reflect genuine engineering effort and a working, non-trivial implementation?
   * *Strategy:* Use PayPal's two-step `AUTHORIZE` $\rightarrow$ `CAPTURE` / `VOID` workflow. Do not just drop a static PayPal button into a template.
2. **Design (20%):**
   * *What Judges Look For:* Complete, coherent user experience — not an unfinished wireframe or terminal script.
   * *Strategy:* Polished responsive UI with clear role separation (e.g., Client Milestone Setup vs Contractor Deliverable Verification).
3. **Potential Impact (20%):**
   * *What Judges Look For:* Credible, specific case for solving a real problem for a real audience.
   * *Strategy:* Target gig/freelance milestone payment risk (a \$1.5 trillion market).
4. **Innovation / Idea (20%):**
   * *What Judges Look For:* Creativity and novelty compared to existing tools.
   * *Strategy:* Frame the AI not just as a chatbot, but as an **Autonomous Escrow Oracle** that holds financial authority over real PayPal transactions.
5. **Presentation (20%):**
   * *What Judges Look For:* Does the video clearly demonstrate the project working end-to-end? Does it communicate problem, target audience, and solution in under 3 minutes?
   * *Strategy:* A structured video under 180 seconds: 30s Hook/Problem $\rightarrow$ 90s Live Working Demo $\rightarrow$ 30s Architecture $\rightarrow$ 30s Impact & Vision.

---

## 4. Mandatory Submission Deliverables Checklist

To qualify for prizes on Devpost, your submission MUST include:
- [ ] **Working Project Link / Test Credentials:** Live URL or clear sandbox test credentials (buyer and seller sandbox test accounts).
- [ ] **Public Code Repository:** GitHub, GitLab, or Bitbucket with an open-source license (MIT, Apache 2.0) and step-by-step setup instructions in `README.md`.
- [ ] **Public YouTube Demo Video:** Strictly **under 3 minutes (180 seconds)** showing the application working on screen. Judges are instructed not to watch past the 3-minute mark!
- [ ] **Devpost Text Write-up:** Detailed sections covering:
  - *Inspiration*
  - *What it does*
  - *How we built it*
  - *Challenges we ran into*
  - *Accomplishments that we're proud of*
  - *What we learned*
  - *What's next for the project*
- [ ] **Category Tags Checked:** Check the boxes for **Best Use of Agentic Commerce** and **Best Use of PayPal + AI**.
