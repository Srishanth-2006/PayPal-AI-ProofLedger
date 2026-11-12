# START HERE: guide for Codex / Antigravity (PayPal AI Hackathon)

Written 2026-10-25. You are an AI assistant picking up work that was done with Claude (Claude Code desktop app). This folder holds a readable copy of the Claude conversation about this hackathon. Read this file first. Do not edit the chat file; it is a record.

## 1. What the work is
- **PayPal AI Hackathon** on Devpost (`https://paypalaihackathon.devpost.com/`). From the pasted Official Rules: submission period 1 Oct 2026 (9:15 am PT) to 12 Nov 2026 (12:00 pm PT); judging 1 to 15 Dec 2026; winners around 21 Dec 2026. Check the live page for the current rules, themes and prizes before relying on this.
- Owner: Srishanth S. Stage: **brainstorming only. No project has been chosen or built.**

## 2. Files
| File | What it is |
|---|---|
| `Claude chat - PayPal AI Hackathon - 04068954.md` | The only chat, 2026-10-24 (about 220 messages; the first message is the full pasted Official Rules, so the file is long at the top). |

## 3. What happened in the chat (in order)
1. The owner pasted the rules and asked to brainstorm project ideas (Claude was asked to ask about skills and team first; check the chat for the answers).
2. Claude browsed the hackathon page and brainstormed. The owner asked whether the ideas were new, then asked what themes/problem statements exist.
3. The owner asked to understand how PayPal really works. Claude explained step by step in simple words: PayPal sits between sender and receiver and keeps its own ledger; balances change in PayPal's records first and real bank money settles later; how this differs from UPI (Google Pay / PhonePe); then the software side with an example (orders created, risk check, bank approval, capture, webhook, payout).
4. The owner asked for a technical analysis of **Main PayPal, Venmo and Xoom**, including gaps. Claude wrote a section per service (how it works, gaps and sore spots; e.g. holds/reserves of 21 to 30 days, stacked fees such as about 3.49% + $0.49 plus international and currency spread, the fixed fee killing small payments, hidden settlement delay; Venmo is US-only, social, accessed by developers through the PayPal JavaScript SDK as a button).
5. The owner asked to turn the gaps into ideas buildable on the PayPal sandbox. Claude first checked what the sandbox supports (confirmed: create/authorize/capture/refund orders, void and reauthorize, batch payouts, webhooks including a simulate-event call, fee/net/exchange-rate fields; not confirmed: realistic disputes, fee accuracy, Venmo in sandbox, Xoom developer access). Four ideas followed:
   - **Idea 1: Payment safety net (Claude's pick).** Authorize instead of capture; an AI checks payee, note and pattern for scam signs; low risk captures, medium risk asks a trusted "guardian" to approve, high risk voids the hold. Uses `intent=AUTHORIZE`, capture/void, webhooks, refunds.
   - **Idea 2: Agent wallet with budgets.** One top-up, AI agents spend from an internal ledger under per-agent budgets, leftover refunded, providers paid in batched payouts.
   - **Idea 3: "What you actually keep" for freelancers.** Before sending an invoice, shows the net amount in the freelancer's own currency under each option; after payment reads the real fee and exchange-rate fields from the capture response. Risk: sandbox may not return real fees; least visually exciting.
   - **Idea 4: Pay-on-proof.** Payment is held, the worker uploads proof, vision plus an LLM check it, then the app captures or refunds; adds an automatic dispute pack. Risks: crypto prototypes do something similar; sandbox disputes unconfirmed.
   Claude's recommendation: start with Idea 1 (real documented weakness, uses native authorize/void, easy 3-minute demo, a team of 5+ can split into payment engine, AI risk scoring, guardian app, UI and demo); Idea 2 is the natural extension (fits "Best Use of Agentic Commerce"). Claude could not promise any idea is unbuilt. Its closing question was which idea to develop into a full design. Full text: search the chat file for `## Idea 1`.
6. Last request: "a clear picture of its working technically but in simple words, detailed explanation for each service". Claude answered with a simple model per service (Main PayPal, Venmo, then Xoom). The chat ends there; the owner had not yet picked an idea.

## 4. State at the end (2026-10-24)
- No idea selected, no code, no repo. The owner was still building understanding of PayPal and Venmo/Xoom.
- Honest caveats Claude raised: the freeze/lawsuit examples came from advocacy sites and forums (anecdotal); sandbox realism for disputes and fees is unconfirmed; Xoom has no developer access found.

## 5. How the owner likes to work
Simple, plain, point-wise explanations with worked examples; honest claims and caveats; asks "why" repeatedly, so explain mechanisms rather than listing features. Windows PC.

## 6. Raw originals
`C:\Users\Srishanth S\Desktop\Sri folder\Claude raw backup\` (folder name ends with `scratch-2026-10-24-14ca28`).

## 7. Suggested first message to the new tool
> Read `PayPal AI Hackathon/Claude/00_START_HERE_for_Codex_or_Antigravity.md`, then the last 40 messages of `Claude chat - PayPal AI Hackathon - 04068954.md`, starting from `## Idea 1`. Compare the four ideas against the current rules on the Devpost page and recommend one, then wait for my decision.
