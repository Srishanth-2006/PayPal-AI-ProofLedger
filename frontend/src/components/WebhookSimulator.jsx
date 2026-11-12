import React, { useState } from 'react';
import { Radio, Send, Terminal, RefreshCw } from 'lucide-react';
import { simulateWebhook } from '../services/api';

const EVENT_PRESETS = [
  {
    event: 'CHECKOUT.ORDER.APPROVED',
    name: 'Order Approved by Buyer',
    desc: 'Simulates buyer completing the PayPal checkout approval, triggering backend authorization hold.',
    color: 'text-cyan-400'
  },
  {
    event: 'CUSTOMER.DISPUTE.CREATED',
    name: 'Customer Dispute Raised',
    desc: 'Simulates buyer filing a dispute in the PayPal Resolution Center, triggering automated 1-Click Dispute Pack assembly.',
    color: 'text-rose-400'
  },
  {
    event: 'PAYMENT.AUTHORIZATION.VOIDED',
    name: 'Payment Authorization Voided',
    desc: 'Simulates expiration or release of the authorization hold, returning 100% of escrow funds to buyer.',
    color: 'text-amber-400'
  }
];

export default function WebhookSimulator({ milestones, onRefresh }) {
  const [selectedMilestoneId, setSelectedMilestoneId] = useState(milestones[0]?.id || '');
  const [selectedEvent, setSelectedEvent] = useState('CUSTOMER.DISPUTE.CREATED');
  const [sending, setSending] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleSimulate = async () => {
    if (!selectedMilestoneId) {
      setError('Please select a target milestone.');
      return;
    }
    try {
      setSending(true);
      setError(null);
      const res = await simulateWebhook(selectedEvent, selectedMilestoneId);
      setResult(res);
      onRefresh();
    } catch (err) {
      setError(err.message);
    } finally {
      setSending(false);
    }
  };

  const activeMilestone = milestones.find(m => m.id === selectedMilestoneId);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-black text-white tracking-tight flex items-center space-x-2">
          <span>PayPal Webhook Simulator & Event Pipeline</span>
          <span className="text-xs bg-amber-950 text-amber-400 border border-amber-800 px-2.5 py-0.5 rounded-full font-mono">
            Sandbox Events
          </span>
        </h1>
        <p className="text-xs text-slate-400 mt-0.5">
          Simulate official PayPal Webhook events to test autonomous escrow lifecycle, status updates, and automated dispute packaging.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Controls Card */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 space-y-5">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <Radio className="w-4 h-4 text-amber-400 animate-pulse" />
            <span>Configure Webhook Event</span>
          </h3>

          {/* Milestone Target */}
          <div>
            <label className="text-xs font-semibold text-slate-300 block mb-1.5">
              Select Target Milestone:
            </label>
            <select
              value={selectedMilestoneId}
              onChange={e => setSelectedMilestoneId(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
            >
              {milestones.map(m => (
                <option key={m.id} value={m.id}>
                  {m.title} (${m.amount} USD) - Status: [{m.status}]
                </option>
              ))}
            </select>
          </div>

          {/* Event presets */}
          <div className="space-y-2">
            <label className="text-xs font-semibold text-slate-300 block">
              Select Event Type:
            </label>
            <div className="space-y-2">
              {EVENT_PRESETS.map((ep, idx) => (
                <div
                  key={idx}
                  onClick={() => setSelectedEvent(ep.event)}
                  className={`p-3 rounded-xl border cursor-pointer transition flex items-start space-x-3 ${
                    selectedEvent === ep.event
                      ? 'bg-amber-950/40 border-amber-600/80 text-white'
                      : 'bg-slate-950 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  <input
                    type="radio"
                    name="webhook_event"
                    checked={selectedEvent === ep.event}
                    onChange={() => setSelectedEvent(ep.event)}
                    className="mt-1"
                  />
                  <div className="flex-1">
                    <span className="font-bold text-xs text-white block">{ep.name}</span>
                    <span className="font-mono text-[10px] text-amber-400 block">{ep.event}</span>
                    <p className="text-[11px] text-slate-400 mt-1">{ep.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {error && (
            <div className="p-3 bg-rose-950/60 border border-rose-800 rounded-xl text-rose-300 text-xs">
              {error}
            </div>
          )}

          <button
            onClick={handleSimulate}
            disabled={sending || !selectedMilestoneId}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-amber-600 to-yellow-500 hover:opacity-95 text-slate-950 font-black text-xs flex items-center justify-center space-x-2 shadow-lg shadow-amber-500/20 transition cursor-pointer"
          >
            {sending ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                <span>Dispatching Webhook...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4 text-slate-950" />
                <span>Simulate & Dispatch Webhook Event</span>
              </>
            )}
          </button>
        </div>

        {/* Live Terminal Output Card */}
        <div className="bg-slate-950 border border-slate-800 rounded-2xl p-6 flex flex-col justify-between font-mono text-xs space-y-4">
          <div className="space-y-3">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center space-x-2 text-slate-300">
                <Terminal className="w-4 h-4 text-amber-400" />
                <span className="font-bold">PayPal Webhook Dispatcher Console</span>
              </div>
              <span className="text-[10px] text-slate-500">POST /api/webhooks/paypal</span>
            </div>

            {/* Target Milestone Status */}
            {activeMilestone && (
              <div className="bg-slate-900 p-3 rounded-xl border border-slate-800 text-[11px] space-y-1">
                <div>Target ID: <span className="text-cyan-400">{activeMilestone.id}</span></div>
                <div>Current State: <span className="text-emerald-400 font-bold">{activeMilestone.status}</span></div>
                <div>PayPal Order ID: <span className="text-slate-300">{activeMilestone.paypal_order_id}</span></div>
                <div>Auth Hold ID: <span className="text-slate-300">{activeMilestone.paypal_authorization_id || 'N/A'}</span></div>
              </div>
            )}

            {/* Response Console */}
            <div className="p-3 bg-black/60 rounded-xl border border-slate-900 min-h-[160px] text-[11px] overflow-x-auto text-slate-300">
              {sending ? (
                <div className="text-amber-400 animate-pulse">
                  &gt; Sending HTTP POST to webhook receiver with PayPal HMAC signature...
                </div>
              ) : result ? (
                <div className="space-y-1 text-emerald-400">
                  <div>&gt; HTTP 200 OK — Webhook Processed Successfully!</div>
                  <pre className="text-cyan-300 mt-2">
                    {JSON.stringify(result, null, 2)}
                  </pre>
                </div>
              ) : (
                <div className="text-slate-600 italic">
                  &gt; Ready. Select an event preset above and click 'Dispatch' to trigger a realistic PayPal webhook event.
                </div>
              )}
            </div>
          </div>

          <div className="pt-2 text-[10px] text-slate-500 border-t border-slate-900">
            Complies with PayPal Webhook Headers: <code className="text-slate-400">PAYPAL-AUTH-ALGO</code>, <code className="text-slate-400">PAYPAL-CERT-URL</code>, and <code className="text-slate-400">PAYPAL-TRANSMISSION-SIG</code>
          </div>
        </div>
      </div>
    </div>
  );
}
