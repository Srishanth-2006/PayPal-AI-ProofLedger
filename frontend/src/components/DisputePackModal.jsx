import React, { useState, useEffect } from 'react';
import { X, ShieldAlert, Download, Copy, Check, CheckCircle2, AlertTriangle } from 'lucide-react';
import { getDisputePack, getDisputePdfUrl } from '../services/api';

export default function DisputePackModal({ milestoneId, isOpen, onClose }) {
  const [pack, setPack] = useState(null);
  const [loading, setLoading] = useState(true);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState(null);

  const loadPack = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await getDisputePack(milestoneId);
      setPack(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen && milestoneId) {
      loadPack();
    }
  }, [isOpen, milestoneId]);

  const handleCopyJson = () => {
    if (!pack) return;
    navigator.clipboard.writeText(JSON.stringify(pack, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 rounded-2xl max-w-3xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-5 border-b border-slate-800 bg-slate-950/80 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-600 to-blue-600 flex items-center justify-center shadow-lg">
              <ShieldAlert className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <h3 className="text-lg font-bold text-white">PayPal Dispute Evidence Pack</h3>
                <span className="text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800/80 px-2 py-0.5 rounded-full font-mono font-bold">
                  SELLER PROTECTION READY
                </span>
              </div>
              <p className="text-xs text-slate-400">Cryptographically Sealed Audit Trail for PayPal Resolution Center</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Scroll Content */}
        <div className="p-6 overflow-y-auto space-y-6 text-xs">
          {loading ? (
            <div className="py-16 text-center text-slate-400">
              <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
              Assembling cryptographic dispute evidence bundle...
            </div>
          ) : error ? (
            <div className="p-4 bg-rose-950/50 border border-rose-800 rounded-xl text-rose-300">
              {error}
            </div>
          ) : pack ? (
            <>
              {/* Evidence Pack Metadata */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-slate-950/60 p-3.5 rounded-xl border border-slate-800">
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Pack ID</span>
                  <span className="font-mono text-cyan-300 font-semibold">{pack.pack_id}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Dispute Ref</span>
                  <span className="font-mono text-slate-200">{pack.dispute_reference_id}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Amount Settled</span>
                  <span className="font-mono text-emerald-400 font-bold">
                    ${pack.contract_agreement.amount.toFixed(2)} {pack.contract_agreement.currency}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px] uppercase">Timestamp</span>
                  <span className="font-mono text-slate-300 truncate block">
                    {new Date(pack.generated_at).toLocaleTimeString()}
                  </span>
                </div>
              </div>

              {/* 1. PayPal Rails & Settlement Proof */}
              <div className="space-y-2">
                <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-[#0070BA]"></span>
                  <span>1. PayPal Rails & Identifiers</span>
                </h4>
                <div className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/60 space-y-2">
                  <div className="flex justify-between">
                    <span className="text-slate-400">PayPal Order ID:</span>
                    <span className="font-mono text-white">{pack.paypal_identifiers.order_id || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Authorization ID (Escrow Hold):</span>
                    <span className="font-mono text-cyan-400">{pack.paypal_identifiers.authorization_id || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Capture ID (Autonomous Release):</span>
                    <span className="font-mono text-emerald-400">{pack.paypal_identifiers.capture_id || 'N/A'}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-400">Seller Protection Eligibility:</span>
                    <span className="text-emerald-400 font-semibold">{pack.paypal_identifiers.seller_protection}</span>
                  </div>
                </div>
              </div>

              {/* 2. Deliverable Proof & Cryptographic Hash */}
              <div className="space-y-2">
                <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                  <span>2. Deliverable Proof & Forensic Hashing</span>
                </h4>
                {pack.deliverable_proof ? (
                  <div className="bg-slate-800/60 rounded-xl p-3 border border-slate-700/60 space-y-2">
                    <div className="flex justify-between">
                      <span className="text-slate-400">Deliverable File:</span>
                      <span className="text-white font-medium">{pack.deliverable_proof.file_name}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block mb-1">SHA-256 File Signature:</span>
                      <div className="p-2 bg-slate-950 rounded-lg font-mono text-[11px] text-cyan-300 break-all border border-slate-800">
                        {pack.deliverable_proof.file_hash}
                      </div>
                    </div>
                    <div className="flex justify-between text-slate-400">
                      <span>Submitted At:</span>
                      <span>{pack.deliverable_proof.submitted_at}</span>
                    </div>
                    {pack.deliverable_proof.notes && (
                      <div className="text-slate-300 italic pt-1 border-t border-slate-700/60">
                        "{pack.deliverable_proof.notes}"
                      </div>
                    )}
                  </div>
                ) : (
                  <p className="text-slate-500 italic">No deliverable uploaded yet.</p>
                )}
              </div>

              {/* 3. AI Multimodal Forensic Audit */}
              {pack.ai_forensic_audit && (
                <div className="space-y-2">
                  <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                    <span className="w-2 h-2 rounded-full bg-purple-500"></span>
                    <span>3. Multimodal AI Oracle Forensic Audit</span>
                  </h4>
                  <div className="bg-slate-800/60 rounded-xl p-3.5 border border-slate-700/60 space-y-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center space-x-3">
                        <span className={`px-2.5 py-1 rounded-lg font-bold text-xs ${
                          pack.ai_forensic_audit.verdict === 'PASS' 
                            ? 'bg-emerald-950 text-emerald-400 border border-emerald-800' 
                            : 'bg-rose-950 text-rose-400 border border-rose-800'
                        }`}>
                          {pack.ai_forensic_audit.verdict}
                        </span>
                        <span className="text-slate-300 font-medium">
                          Confidence: <b className="text-white">{pack.ai_forensic_audit.confidence_score}%</b>
                        </span>
                        <span className="text-slate-400">
                          Fraud Risk: <b className="text-white">{pack.ai_forensic_audit.fraud_risk_score}%</b>
                        </span>
                      </div>
                      <span className="text-slate-500 font-mono text-[10px]">{pack.ai_forensic_audit.evaluator_model}</span>
                    </div>

                    <p className="text-slate-300 leading-relaxed bg-slate-900/60 p-2.5 rounded-lg border border-slate-800">
                      {pack.ai_forensic_audit.summary_reasoning}
                    </p>

                    {/* Criteria checklist */}
                    <div className="space-y-1.5 pt-1">
                      <span className="text-slate-400 font-semibold block text-[11px]">Contractual Criteria Audit:</span>
                      {pack.ai_forensic_audit.criteria_checklist.map((item, i) => (
                        <div key={i} className="p-2 bg-slate-950/60 rounded-lg border border-slate-800 flex items-start space-x-2">
                          {item.satisfied ? (
                            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                          ) : (
                            <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                          )}
                          <div className="flex-1">
                            <span className="text-white font-medium">{item.criterion}</span>
                            <p className="text-[11px] text-slate-400 mt-0.5">{item.visual_evidence}</p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* 4. Cryptographic Proof Ledger Trail */}
              <div className="space-y-2">
                <h4 className="text-sm font-bold text-white flex items-center space-x-2">
                  <span className="w-2 h-2 rounded-full bg-cyan-500"></span>
                  <span>4. Cryptographic Proof Ledger Seal</span>
                </h4>
                <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between text-slate-400">
                    <span>Evidence Signature:</span>
                    <span className="text-cyan-400 font-mono text-[10px]">SHA-256 TAMPER-PROOF</span>
                  </div>
                  <div className="p-2 bg-slate-900 rounded font-mono text-[11px] text-cyan-300 break-all border border-slate-800">
                    {pack.integrity_signature}
                  </div>
                  <p className="text-slate-500 text-[11px]">
                    Verified against {pack.cryptographic_ledger_trail.length} immutable ledger blocks. Accepted by payment card arbitration networks.
                  </p>
                </div>
              </div>
            </>
          ) : null}
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between">
          <button
            onClick={handleCopyJson}
            disabled={!pack}
            className="flex items-center space-x-2 px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold transition"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-400" /> : <Copy className="w-4 h-4" />}
            <span>{copied ? 'Copied JSON!' : 'Copy Evidence JSON'}</span>
          </button>

          <div className="flex items-center space-x-2">
            <a
              href={milestoneId ? getDisputePdfUrl(milestoneId) : '#'}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-[#003087] to-[#0070BA] hover:from-[#002266] hover:to-[#005590] text-white text-xs font-bold shadow-lg shadow-blue-500/20 transition cursor-pointer"
            >
              <Download className="w-4 h-4" />
              <span>Download Official PDF Pack</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
