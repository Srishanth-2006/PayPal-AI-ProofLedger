import React, { useState } from 'react';
import { X, Lock, ShieldCheck, ArrowRight, Loader2 } from 'lucide-react';
import { authorizeMilestone } from '../services/api';

export default function PayPalButtonModal({ milestone, isOpen, onClose, onSuccess }) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  if (!isOpen || !milestone) return null;

  const handleAuthorize = async () => {
    try {
      setLoading(true);
      setError(null);
      const res = await authorizeMilestone(milestone.id, milestone.paypal_order_id);
      onSuccess(res);
      onClose();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm animate-fade-in">
      <div className="bg-slate-900 border border-slate-700/80 rounded-2xl max-w-md w-full shadow-2xl overflow-hidden">
        {/* PayPal Header */}
        <div className="bg-gradient-to-r from-[#003087] to-[#0070BA] p-4 text-white flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="font-black italic text-xl tracking-wider">PayPal</span>
            <span className="text-[10px] bg-amber-400 text-slate-950 px-2 py-0.5 rounded font-bold uppercase tracking-wider">
              Sandbox
            </span>
          </div>
          <button onClick={onClose} className="p-1 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 space-y-4">
          <div className="text-center space-y-1">
            <h3 className="text-lg font-bold text-white">Approve Escrow Authorization Hold</h3>
            <p className="text-xs text-slate-400">
              Orders v2 <span className="font-mono text-cyan-400">intent: "AUTHORIZE"</span>
            </p>
          </div>

          {/* Transaction Summary Card */}
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700/60 space-y-3">
            <div className="flex justify-between items-center text-sm border-b border-slate-700/60 pb-2">
              <span className="text-slate-400">Milestone</span>
              <span className="font-semibold text-white truncate max-w-[200px] text-right">{milestone.title}</span>
            </div>
            <div className="flex justify-between items-center text-sm border-b border-slate-700/60 pb-2">
              <span className="text-slate-400">Escrow Hold Amount</span>
              <span className="font-bold text-emerald-400 font-mono text-base">
                ${milestone.amount.toFixed(2)} {milestone.currency}
              </span>
            </div>
            <div className="flex justify-between items-center text-xs text-slate-400">
              <span>Order Reference ID</span>
              <span className="font-mono text-slate-300">{milestone.paypal_order_id}</span>
            </div>
          </div>

          {/* Explain Two-Step Authorization */}
          <div className="bg-cyan-950/40 border border-cyan-800/40 rounded-xl p-3 flex items-start space-x-3 text-xs text-cyan-300">
            <ShieldCheck className="w-5 h-5 text-cyan-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-bold text-cyan-200">Guaranteed Escrow Protection:</span> Your funds will be temporarily placed on hold by PayPal rails. Funds are <b>not released</b> to the contractor until the ProofLedger Multimodal AI verifies the deliverable against agreed specifications.
            </div>
          </div>

          {/* Sandbox Buyer Profile */}
          <div className="text-xs text-slate-400 bg-slate-950/60 p-2.5 rounded-lg border border-slate-800">
            <div className="flex justify-between">
              <span>Sandbox Buyer:</span>
              <span className="text-slate-200 font-mono">{milestone.client_email}</span>
            </div>
            <div className="flex justify-between mt-1">
              <span>Preloaded Sandbox Balance:</span>
              <span className="text-emerald-400 font-mono font-semibold">$5,000.00 USD</span>
            </div>
          </div>

          {error && (
            <div className="p-3 bg-rose-950/50 border border-rose-800/60 rounded-xl text-rose-300 text-xs">
              {error}
            </div>
          )}

          {/* PayPal Style Action Button */}
          <div className="pt-2">
            <button
              onClick={handleAuthorize}
              disabled={loading}
              className="w-full py-3.5 px-4 rounded-full bg-[#FFC439] hover:bg-[#F4B41A] active:scale-[0.98] text-slate-900 font-extrabold text-sm flex items-center justify-center space-x-2 shadow-lg shadow-amber-500/20 transition-all cursor-pointer"
            >
              {loading ? (
                <>
                  <Loader2 className="w-4 h-4 animate-spin text-slate-900" />
                  <span>Locking Escrow on PayPal Rails...</span>
                </>
              ) : (
                <>
                  <Lock className="w-4 h-4 text-slate-900" />
                  <span>Lock Escrow with PayPal</span>
                  <ArrowRight className="w-4 h-4 text-slate-900" />
                </>
              )}
            </button>
            <p className="text-[11px] text-center text-slate-500 mt-2">
              PayPal Orders v2 API • Real-Time Authorization Hold
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
