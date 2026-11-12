import React, { useState } from 'react';
import { Plus, Lock, CheckCircle2, FileText, ArrowRight, ShieldCheck, Layers } from 'lucide-react';
import { createMilestone } from '../services/api';

const PRESET_TEMPLATES = [
  {
    name: 'HVAC Capacitor & Calibration',
    amount: 250.00,
    title: 'HVAC Capacitor Replacement & Pressure Gauge Calibration',
    description: 'Commercial refrigeration maintenance: replace dual run capacitor and calibrate manifold pressure between 60-70 PSI.',
    contractor_name: 'Dave Vance (Vance HVAC)',
    contractor_email: 'dave@vancehvac.test',
    specifications: [
      'Original malfunctioning capacitor removed',
      'New brand-name dual run capacitor securely wired with spade connectors',
      'Analog or digital manifold gauge showing stable pressure reading between 60-70 PSI',
      'Work area clean with no exposed cut copper'
    ]
  },
  {
    name: 'Smart Contract Audit Bounty',
    amount: 1500.00,
    title: 'Web3 Escrow Smart Contract Audit & Formal Verification',
    description: 'Security audit of Solidity escrow contracts with automated test suite and signed auditor certificate.',
    contractor_name: 'Sarah Lin, Lead Auditor',
    contractor_email: 'sarah@linforensics.test',
    specifications: [
      'Automated Slither & Mythril vulnerability scanner logs with 0 critical findings',
      '100% branch test coverage suite for Vault.sol and EscrowManager.sol',
      'Remediation verification signed with auditor PGP signature'
    ]
  },
  {
    name: 'Solar Array Grid Sync',
    amount: 480.00,
    title: 'Solar Array Micro-Inverter Grounding & Grid Sync',
    description: 'Inspect and mount 12x Enphase IQ8+ micro-inverters, verify ground continuity, and confirm grid synchronization LED.',
    contractor_name: 'Alex Rivera Solar Field Services',
    contractor_email: 'alex@riverasolar.test',
    specifications: [
      'Enphase IQ8+ micro-inverters securely clamped to aluminum rail',
      'Multimeter reading confirming AC 240V +/- 5V',
      'Status LED showing continuous solid green grid lock'
    ]
  },
  {
    name: '🤖 Agentic AI Data Bounty',
    amount: 320.00,
    title: 'Autonomous AI Market Intelligence Crawler & Schema Sync',
    description: 'Autonomous AI agent extracts real-time supplier price trends, validates schema, and compiles JSON delivery hash.',
    contractor_name: 'ScraperBot-v4 (Autonomous Agent)',
    contractor_email: 'agent-bot4@autonomous-commerce.ai',
    specifications: [
      'Structured JSON dataset with verified schema validation for 500+ SKU price entries',
      'Data freshness timestamp within past 60 minutes',
      'Automated test report verifying 0 parsing errors and 100% field parity'
    ]
  }
];

export default function ClientEscrowView({
  milestones,
  onRefresh,
  onOpenPayPalModal,
  onOpenDisputeModal,
  onSelectMilestoneForWork
}) {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [filter, setFilter] = useState('ALL');
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    amount: 250.00,
    currency: 'USD',
    client_name: 'Apex Commercial Properties LLC',
    client_email: 'client@apexproperties.test',
    contractor_name: 'Dave Vance HVAC Tech',
    contractor_email: 'dave@vancehvac.test',
    specifications: [
      'Original malfunctioning capacitor removed',
      'New brand-name dual run capacitor securely wired',
      'Analog or digital manifold gauge showing stable pressure reading between 60-70 PSI'
    ],
    auto_capture_on_pass: true
  });
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleApplyTemplate = (tpl) => {
    setFormData(prev => ({
      ...prev,
      title: tpl.title,
      description: tpl.description,
      amount: tpl.amount,
      contractor_name: tpl.contractor_name,
      contractor_email: tpl.contractor_email,
      specifications: [...tpl.specifications]
    }));
  };

  const handleAddSpec = () => {
    setFormData(prev => ({
      ...prev,
      specifications: [...prev.specifications, '']
    }));
  };

  const handleRemoveSpec = (idx) => {
    setFormData(prev => ({
      ...prev,
      specifications: prev.specifications.filter((_, i) => i !== idx)
    }));
  };

  const handleSpecChange = (idx, val) => {
    setFormData(prev => {
      const copy = [...prev.specifications];
      copy[idx] = val;
      return { ...prev, specifications: copy };
    });
  };

  const handleCreateSubmit = async (e) => {
    e.preventDefault();
    try {
      setSubmitting(true);
      setError(null);
      const filteredSpecs = formData.specifications.filter(s => s.trim().length > 0);
      if (filteredSpecs.length === 0) {
        throw new Error('At least one deliverable specification criterion is required.');
      }
      await createMilestone({
        ...formData,
        amount: parseFloat(formData.amount),
        specifications: filteredSpecs
      });
      setShowCreateModal(false);
      onRefresh();
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  // KPIs
  const totalLocked = milestones
    .filter(m => m.status === 'ESCROW_LOCKED')
    .reduce((sum, m) => sum + m.amount, 0);

  const totalSettled = milestones
    .filter(m => m.status === 'COMPLETED')
    .reduce((sum, m) => sum + m.amount, 0);

  const filteredMilestones = filter === 'ALL'
    ? milestones
    : milestones.filter(m => m.status === filter);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Top Banner & Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Client Escrow Dashboard</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Lock milestone funds with PayPal Orders v2 two-step authorization. Funds are released autonomously upon AI verification.
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-[#003087] via-[#0070BA] to-cyan-500 hover:opacity-95 text-white font-bold text-xs shadow-lg shadow-blue-500/20 transition cursor-pointer self-start sm:self-auto"
        >
          <Plus className="w-4 h-4" />
          <span>Create Milestone Escrow</span>
        </button>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Active Escrow Holds</span>
            <div className="p-2 rounded-lg bg-cyan-950/60 border border-cyan-800/60 text-cyan-400">
              <Lock className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black font-mono text-cyan-400">${totalLocked.toFixed(2)}</span>
            <span className="text-xs text-slate-500 ml-1.5 font-medium">USD Held</span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Guaranteed on PayPal rails</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">AI-Verified & Settled</span>
            <div className="p-2 rounded-lg bg-emerald-950/60 border border-emerald-800/60 text-emerald-400">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black font-mono text-emerald-400">${totalSettled.toFixed(2)}</span>
            <span className="text-xs text-slate-500 ml-1.5 font-medium">USD Settled</span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Zero human middleman fees</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Total Milestones</span>
            <div className="p-2 rounded-lg bg-purple-950/60 border border-purple-800/60 text-purple-400">
              <Layers className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black font-mono text-white">{milestones.length}</span>
            <span className="text-xs text-slate-500 ml-1.5 font-medium">Engagements</span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Tracked in Proof Ledger</p>
        </div>

        <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg relative overflow-hidden">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-400">Dispute Defense Shield</span>
            <div className="p-2 rounded-lg bg-blue-950/60 border border-blue-800/60 text-blue-400">
              <ShieldCheck className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-3">
            <span className="text-2xl font-black font-mono text-blue-400">100%</span>
            <span className="text-xs text-slate-500 ml-1.5 font-medium">Evidence Ready</span>
          </div>
          <p className="text-[11px] text-slate-500 mt-1">Cryptographic SHA-256 seal</p>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-3 overflow-x-auto text-xs">
        {['ALL', 'ESCROW_LOCKED', 'COMPLETED', 'DRAFT', 'VOIDED', 'DISPUTED'].map((st) => (
          <button
            key={st}
            onClick={() => setFilter(st)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition ${
              filter === st
                ? 'bg-slate-800 text-white border border-slate-700'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            {st.replace('_', ' ')}
          </button>
        ))}
      </div>

      {/* Milestones Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {filteredMilestones.map((m) => (
          <div
            key={m.id}
            className="bg-slate-900/90 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-xl transition space-y-4 flex flex-col justify-between"
          >
            <div className="space-y-3">
              {/* Header Status & Price */}
              <div className="flex items-start justify-between gap-3">
                <div>
                  <span className={`inline-block px-2.5 py-0.5 rounded-full text-[10px] font-extrabold uppercase tracking-wider mb-1.5 border ${
                    m.status === 'ESCROW_LOCKED'
                      ? 'bg-cyan-950 text-cyan-400 border-cyan-800'
                      : m.status === 'COMPLETED'
                      ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                      : m.status === 'DRAFT'
                      ? 'bg-amber-950 text-amber-400 border-amber-800'
                      : m.status === 'DISPUTED'
                      ? 'bg-rose-950 text-rose-400 border-rose-800'
                      : 'bg-slate-800 text-slate-400 border-slate-700'
                  }`}>
                    {m.status.replace('_', ' ')}
                  </span>
                  <h3 className="text-base font-bold text-white leading-snug">{m.title}</h3>
                </div>
                <div className="text-right flex-shrink-0">
                  <span className="text-xl font-black font-mono text-emerald-400">
                    ${m.amount.toFixed(2)}
                  </span>
                  <span className="text-[10px] text-slate-500 block uppercase font-mono">{m.currency}</span>
                </div>
              </div>

              <p className="text-xs text-slate-400 leading-relaxed line-clamp-2">{m.description}</p>

              {/* Parties */}
              <div className="text-[11px] text-slate-400 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800 space-y-1">
                <div className="flex justify-between">
                  <span>Client:</span>
                  <span className="text-slate-200 font-medium">{m.client_name}</span>
                </div>
                <div className="flex justify-between">
                  <span>Contractor:</span>
                  <span className="text-slate-200 font-medium">{m.contractor_name}</span>
                </div>
              </div>

              {/* Specifications preview */}
              <div className="space-y-1.5">
                <span className="text-[11px] font-semibold text-slate-400 block">Verification Criteria:</span>
                <ul className="space-y-1">
                  {m.specifications.slice(0, 3).map((spec, i) => (
                    <li key={i} className="text-xs text-slate-300 flex items-start space-x-1.5">
                      <span className="text-cyan-400 font-bold">•</span>
                      <span className="truncate">{spec}</span>
                    </li>
                  ))}
                  {m.specifications.length > 3 && (
                    <li className="text-[11px] text-slate-500 italic pl-3">
                      +{m.specifications.length - 3} more contractual conditions
                    </li>
                  )}
                </ul>
              </div>

              {/* PayPal identifiers */}
              <div className="text-[10px] font-mono text-slate-500 space-y-0.5 border-t border-slate-800/80 pt-2">
                <div>Order: <span className="text-slate-400">{m.paypal_order_id || 'Pending'}</span></div>
                {m.paypal_authorization_id && (
                  <div>Auth Hold: <span className="text-cyan-400">{m.paypal_authorization_id}</span></div>
                )}
                {m.paypal_capture_id && (
                  <div>Capture Settled: <span className="text-emerald-400">{m.paypal_capture_id}</span></div>
                )}
              </div>
            </div>

            {/* Action Buttons */}
            <div className="pt-3 border-t border-slate-800 flex items-center justify-between gap-2">
              {m.status === 'DRAFT' && (
                <button
                  onClick={() => onOpenPayPalModal(m)}
                  className="w-full py-2.5 px-3 rounded-xl bg-[#FFC439] hover:bg-[#F4B41A] text-slate-950 font-bold text-xs flex items-center justify-center space-x-2 shadow-md transition cursor-pointer"
                >
                  <Lock className="w-3.5 h-3.5 text-slate-950" />
                  <span>Lock Escrow with PayPal</span>
                </button>
              )}

              {m.status === 'ESCROW_LOCKED' && (
                <div className="w-full flex items-center justify-between gap-2">
                  <button
                    onClick={() => onSelectMilestoneForWork(m)}
                    className="flex-1 py-2 px-3 rounded-xl bg-gradient-to-r from-emerald-600 to-teal-500 hover:opacity-90 text-white font-semibold text-xs flex items-center justify-center space-x-1.5 transition cursor-pointer"
                  >
                    <span>Submit Proof as Contractor</span>
                    <ArrowRight className="w-3.5 h-3.5" />
                  </button>
                  <button
                    onClick={() => onOpenDisputeModal(m.id)}
                    className="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
                    title="View Evidence Pack"
                  >
                    <FileText className="w-4 h-4" />
                  </button>
                </div>
              )}

              {(m.status === 'COMPLETED' || m.status === 'VOIDED' || m.status === 'DISPUTED') && (
                <div className="w-full flex items-center justify-between gap-2">
                  <div className="text-xs text-slate-400 flex items-center space-x-1.5">
                    <ShieldCheck className="w-4 h-4 text-emerald-400" />
                    <span>Ledger Sealed</span>
                  </div>
                  <button
                    onClick={() => onOpenDisputeModal(m.id)}
                    className="py-1.5 px-3 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs flex items-center space-x-1.5 border border-slate-700 transition cursor-pointer"
                  >
                    <FileText className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Dispute Pack</span>
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Create Milestone Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
          <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
            <div className="p-5 border-b border-slate-800 flex items-center justify-between">
              <div>
                <h3 className="text-lg font-bold text-white">Create Milestone Escrow</h3>
                <p className="text-xs text-slate-400">Configured with PayPal Orders v2 two-step authorization</p>
              </div>
              <button
                onClick={() => setShowCreateModal(false)}
                className="text-slate-400 hover:text-white p-1 rounded-lg hover:bg-slate-800"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleCreateSubmit} className="p-6 overflow-y-auto space-y-4 text-xs">
              {/* Preset Selector */}
              <div>
                <label className="text-slate-400 font-semibold block mb-1.5">
                  Or load a pre-configured scenario:
                </label>
                <div className="grid grid-cols-3 gap-2">
                  {PRESET_TEMPLATES.map((tpl, idx) => (
                    <button
                      key={idx}
                      type="button"
                      onClick={() => handleApplyTemplate(tpl)}
                      className="p-2 rounded-xl bg-slate-950 hover:bg-slate-800 border border-slate-800 text-left transition text-slate-300 hover:text-white flex flex-col justify-between"
                    >
                      <span className="font-bold truncate text-[11px] block">{tpl.name}</span>
                      <span className="text-[10px] text-cyan-400 font-mono mt-1">${tpl.amount} USD</span>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <label className="text-slate-300 font-semibold block mb-1">Milestone Title</label>
                <input
                  type="text"
                  required
                  value={formData.title}
                  onChange={e => setFormData({ ...formData, title: e.target.value })}
                  placeholder="e.g. HVAC Capacitor Replacement & Pressure Calibration"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div>
                <label className="text-slate-300 font-semibold block mb-1">Scope Description</label>
                <textarea
                  rows={2}
                  value={formData.description}
                  onChange={e => setFormData({ ...formData, description: e.target.value })}
                  placeholder="Detailed description of contractual deliverable"
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 font-semibold block mb-1">Escrow Hold Amount ($)</label>
                  <input
                    type="number"
                    step="0.01"
                    min="1"
                    required
                    value={formData.amount}
                    onChange={e => setFormData({ ...formData, amount: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 font-mono text-emerald-400 font-bold focus:outline-none focus:border-cyan-500"
                  />
                </div>
                <div>
                  <label className="text-slate-300 font-semibold block mb-1">Currency</label>
                  <select
                    value={formData.currency}
                    onChange={e => setFormData({ ...formData, currency: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-cyan-500"
                  >
                    <option value="USD">USD ($)</option>
                    <option value="EUR">EUR (€)</option>
                    <option value="GBP">GBP (£)</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-slate-300 font-semibold block mb-1">Client Name</label>
                  <input
                    type="text"
                    required
                    value={formData.client_name}
                    onChange={e => setFormData({ ...formData, client_name: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="text-slate-300 font-semibold block mb-1">Contractor Name</label>
                  <input
                    type="text"
                    required
                    value={formData.contractor_name}
                    onChange={e => setFormData({ ...formData, contractor_name: e.target.value })}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white"
                  />
                </div>
              </div>

              {/* Specifications checklist builder */}
              <div className="space-y-2">
                <div className="flex items-center justify-between">
                  <label className="text-slate-300 font-semibold">
                    Contractual Release Criteria (Evaluated by Multimodal AI)
                  </label>
                  <button
                    type="button"
                    onClick={handleAddSpec}
                    className="text-cyan-400 hover:text-cyan-300 font-bold text-[11px]"
                  >
                    + Add Criterion
                  </button>
                </div>
                {formData.specifications.map((spec, i) => (
                  <div key={i} className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={spec}
                      onChange={e => handleSpecChange(i, e.target.value)}
                      placeholder={`Criterion ${i + 1} e.g. Manifold gauge 60-70 PSI`}
                      className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-white text-xs"
                    />
                    {formData.specifications.length > 1 && (
                      <button
                        type="button"
                        onClick={() => handleRemoveSpec(i)}
                        className="text-rose-400 hover:text-rose-300 px-2 py-1 rounded"
                      >
                        ✕
                      </button>
                    )}
                  </div>
                ))}
              </div>

              {error && (
                <div className="p-3 bg-rose-950/60 border border-rose-800 rounded-xl text-rose-300">
                  {error}
                </div>
              )}

              <div className="pt-3 border-t border-slate-800 flex items-center justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-5 py-2 rounded-xl bg-gradient-to-r from-[#003087] to-[#0070BA] text-white font-bold shadow-lg shadow-blue-500/20 hover:opacity-95 cursor-pointer"
                >
                  {submitting ? 'Creating Escrow...' : 'Create Escrow Milestone'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
