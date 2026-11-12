import React from 'react';
import { Cpu, CheckCircle2, AlertTriangle, XCircle, ShieldCheck, Search } from 'lucide-react';

export default function LiveAiScanner({ scanning, verdict, proofUrl }) {
  if (!scanning && !verdict) return null;

  return (
    <div className="bg-slate-900 border border-slate-700/80 rounded-2xl p-6 shadow-2xl space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
            <Cpu className={`w-5 h-5 text-white ${scanning ? 'animate-spin' : ''}`} />
          </div>
          <div>
            <h3 className="text-base font-bold text-white flex items-center space-x-2">
              <span>Multimodal AI Verification Oracle</span>
              {scanning && (
                <span className="text-[10px] bg-cyan-950 text-cyan-400 border border-cyan-800 px-2 py-0.5 rounded-full font-mono animate-pulse">
                  SCANNING DELIVERABLE...
                </span>
              )}
            </h3>
            <p className="text-xs text-slate-400">
              Forensic inspection comparing submitted proof against contractual criteria
            </p>
          </div>
        </div>

        {verdict && (
          <div className="flex items-center space-x-2">
            <span className="text-xs text-slate-400">Oracle Model:</span>
            <span className="text-xs font-mono text-cyan-300 bg-cyan-950/60 px-2 py-1 rounded-md border border-cyan-800/40">
              {verdict.evaluator_model}
            </span>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 items-start">
        {/* Left Column: Visual Scanner Box */}
        <div className="relative rounded-xl overflow-hidden border border-slate-700 bg-slate-950 aspect-[4/3] flex items-center justify-center group shadow-inner">
          {proofUrl ? (
            <img
              src={proofUrl}
              alt="Submitted Deliverable"
              className="w-full h-full object-cover"
            />
          ) : (
            <div className="text-center text-slate-500 p-4">
              <Search className="w-8 h-8 mx-auto mb-2 opacity-50" />
              <span>Deliverable image rendered here</span>
            </div>
          )}

          {/* Laser Scan Line Animation */}
          {scanning && (
            <div className="absolute inset-0 pointer-events-none overflow-hidden">
              <div className="w-full h-1 bg-gradient-to-r from-transparent via-cyan-400 to-transparent shadow-[0_0_15px_#22d3ee] animate-scanline"></div>
              <div className="absolute inset-0 bg-cyan-500/10 backdrop-blur-[1px]"></div>
              <div className="absolute top-4 left-4 bg-black/70 px-2.5 py-1 rounded text-[11px] font-mono text-cyan-300 border border-cyan-500/40">
                FORENSIC SCAN: RUNNING (PASS 1/2)
              </div>
            </div>
          )}

          {/* Verification Watermark */}
          {verdict && !scanning && (
            <div className="absolute bottom-3 right-3 bg-black/80 backdrop-blur border border-slate-700/80 rounded-lg px-2.5 py-1 text-[11px] font-mono text-slate-300">
              Confidence: <span className={verdict.confidence_score >= 85 ? 'text-emerald-400 font-bold' : 'text-rose-400 font-bold'}>
                {verdict.confidence_score}%
              </span>
            </div>
          )}
        </div>

        {/* Right Column: Criteria Audit & Verdict */}
        <div className="space-y-4">
          {/* Scanning Progress state */}
          {scanning && (
            <div className="py-8 space-y-3 text-center">
              <div className="w-12 h-12 rounded-full border-3 border-cyan-400 border-t-transparent animate-spin mx-auto"></div>
              <p className="text-sm font-semibold text-cyan-300">AI Oracle Analyzing Visual Evidence...</p>
              <p className="text-xs text-slate-400 max-w-sm mx-auto">
                Validating resolution clarity, capacitor wiring terminals, manifold gauge 60-70 PSI reading, and detecting any visual tampering...
              </p>
            </div>
          )}

          {verdict && !scanning && (
            <>
              {/* Verdict Banner */}
              <div className={`p-4 rounded-xl border flex items-center justify-between ${
                verdict.verdict === 'PASS'
                  ? 'bg-emerald-950/40 border-emerald-800/80 text-emerald-300'
                  : verdict.verdict === 'NEEDS_REVIEW'
                  ? 'bg-amber-950/40 border-amber-800/80 text-amber-300'
                  : 'bg-rose-950/40 border-rose-800/80 text-rose-300'
              }`}>
                <div className="flex items-center space-x-3">
                  {verdict.verdict === 'PASS' ? (
                    <CheckCircle2 className="w-6 h-6 text-emerald-400 flex-shrink-0" />
                  ) : verdict.verdict === 'NEEDS_REVIEW' ? (
                    <AlertTriangle className="w-6 h-6 text-amber-400 flex-shrink-0" />
                  ) : (
                    <XCircle className="w-6 h-6 text-rose-400 flex-shrink-0" />
                  )}
                  <div>
                    <span className="text-xs uppercase tracking-wider font-bold block">
                      Oracle Determination
                    </span>
                    <span className="text-base font-extrabold text-white">
                      {verdict.verdict === 'PASS' && 'VERIFIED (PASS) — FUNDS SETTLED'}
                      {verdict.verdict === 'NEEDS_REVIEW' && 'MUTUAL REVIEW REQUIRED'}
                      {verdict.verdict === 'FAIL' && 'VERIFICATION FAILED — HOLD VOIDED'}
                    </span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-xs text-slate-400 block">Confidence Score</span>
                  <span className="text-2xl font-black font-mono text-white">
                    {verdict.confidence_score}%
                  </span>
                </div>
              </div>

              {/* Forensic Reasoning */}
              <div className="bg-slate-950/60 p-3.5 rounded-xl border border-slate-800 text-xs text-slate-300 leading-relaxed">
                <span className="font-bold text-slate-200 block mb-1">Forensic Analysis:</span>
                {verdict.summary_reasoning}
              </div>

              {/* Criteria Checklist Breakdown */}
              <div className="space-y-2">
                <span className="text-xs font-bold text-slate-300 block">
                  Contractual Specifications Checklist:
                </span>
                <div className="space-y-1.5 max-h-48 overflow-y-auto pr-1">
                  {verdict.criteria_checklist.map((item, idx) => (
                    <div
                      key={idx}
                      className="p-2.5 bg-slate-950/80 rounded-lg border border-slate-800 flex items-start space-x-2.5 text-xs"
                    >
                      {item.satisfied ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0 mt-0.5" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                      )}
                      <div className="flex-1">
                        <div className="flex justify-between">
                          <span className="font-semibold text-white">{item.criterion}</span>
                          <span className={`font-mono text-[10px] ${item.satisfied ? 'text-emerald-400' : 'text-rose-400'}`}>
                            {item.confidence.toFixed(0)}%
                          </span>
                        </div>
                        <p className="text-[11px] text-slate-400 mt-0.5">{item.visual_evidence}</p>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Fraud and Security Risk */}
              <div className="flex items-center justify-between text-xs text-slate-400 bg-slate-800/40 px-3 py-2 rounded-lg border border-slate-700/60">
                <div className="flex items-center space-x-2">
                  <ShieldCheck className="w-4 h-4 text-cyan-400" />
                  <span>Fraud & Tamper Risk Score:</span>
                </div>
                <span className={`font-mono font-bold ${verdict.fraud_risk_score > 30 ? 'text-rose-400' : 'text-emerald-400'}`}>
                  {verdict.fraud_risk_score}% ({verdict.fraud_risk_score > 30 ? 'HIGH RISK' : 'LOW RISK'})
                </span>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
