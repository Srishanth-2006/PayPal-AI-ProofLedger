import React, { useState, useEffect } from 'react';
import { ShieldCheck, Clock, ArrowDown, Copy, Check, RefreshCw } from 'lucide-react';
import { getLedgerBlocks, verifyLedgerIntegrity } from '../services/api';

export default function ProofLedgerView({ selectedMilestoneId }) {
  const [blocks, setBlocks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [integrityReport, setIntegrityReport] = useState(null);
  const [verifying, setVerifying] = useState(false);
  const [filterEvent, setFilterEvent] = useState('ALL');
  const [copiedHash, setCopiedHash] = useState(null);

  const loadBlocks = async () => {
    try {
      setLoading(true);
      const data = await getLedgerBlocks();
      setBlocks(data);
      // Automatically run integrity check
      const report = await verifyLedgerIntegrity();
      setIntegrityReport(report);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBlocks();
  }, [selectedMilestoneId]);

  const handleManualVerify = async () => {
    try {
      setVerifying(true);
      const report = await verifyLedgerIntegrity();
      setIntegrityReport(report);
    } catch (err) {
      console.error(err);
    } finally {
      setVerifying(false);
    }
  };

  const handleCopy = (text) => {
    navigator.clipboard.writeText(text);
    setCopiedHash(text);
    setTimeout(() => setCopiedHash(null), 1500);
  };

  const filteredBlocks = filterEvent === 'ALL'
    ? blocks
    : blocks.filter(b => b.event_type === filterEvent);

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header & Verification Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight flex items-center space-x-2">
            <span>Cryptographic Proof Ledger</span>
            <span className="text-xs bg-purple-950 text-purple-400 border border-purple-800 px-2.5 py-0.5 rounded-full font-mono">
              SHA-256 Linked
            </span>
          </h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Immutable, audit-ready event log binding PayPal authorizations, multimodal AI verdicts, and deliverable hashes.
          </p>
        </div>

        <button
          onClick={handleManualVerify}
          disabled={verifying}
          className="flex items-center space-x-2 px-4 py-2 rounded-xl bg-gradient-to-r from-purple-600 to-indigo-600 hover:opacity-95 text-white font-bold text-xs shadow-lg shadow-purple-500/20 transition cursor-pointer self-start sm:self-auto"
        >
          <RefreshCw className={`w-4 h-4 ${verifying ? 'animate-spin' : ''}`} />
          <span>Verify Chain Integrity</span>
        </button>
      </div>

      {/* Integrity Report Banner */}
      {integrityReport && (
        <div className={`p-4 rounded-2xl border flex items-center justify-between ${
          integrityReport.is_valid
            ? 'bg-emerald-950/40 border-emerald-800/80 text-emerald-300'
            : 'bg-rose-950/40 border-rose-800/80 text-rose-300'
        }`}>
          <div className="flex items-center space-x-3">
            <ShieldCheck className="w-6 h-6 text-emerald-400 flex-shrink-0" />
            <div>
              <span className="font-bold text-sm block">
                {integrityReport.is_valid ? 'Chain Cryptographically Valid & Sealed' : 'Tamper Alert Detected!'}
              </span>
              <p className="text-xs text-slate-400 mt-0.5">{integrityReport.message}</p>
            </div>
          </div>
          <div className="text-right font-mono text-xs hidden sm:block">
            <span className="text-slate-400 block">Total Verified Blocks</span>
            <span className="text-base font-bold text-white">{integrityReport.total_blocks}</span>
          </div>
        </div>
      )}

      {/* Filter Tabs */}
      <div className="flex items-center space-x-2 border-b border-slate-800 pb-3 overflow-x-auto text-xs">
        {['ALL', 'GENESIS', 'ESCROW_CREATED', 'ESCROW_AUTHORIZED', 'PROOF_SUBMITTED', 'AI_VERIFIED', 'PAYMENT_CAPTURED', 'DISPUTE_RAISED'].map(ev => (
          <button
            key={ev}
            onClick={() => setFilterEvent(ev)}
            className={`px-3 py-1.5 rounded-lg font-semibold transition ${
              filterEvent === ev
                ? 'bg-purple-950/80 text-purple-300 border border-purple-800'
                : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
            }`}
          >
            {ev.replace(/_/g, ' ')}
          </button>
        ))}
      </div>

      {/* Blockchain Blocks List */}
      <div className="space-y-4">
        {loading ? (
          <div className="py-20 text-center text-slate-500">
            <div className="w-8 h-8 border-2 border-purple-500 border-t-transparent rounded-full animate-spin mx-auto mb-3"></div>
            Loading blockchain state...
          </div>
        ) : filteredBlocks.length === 0 ? (
          <div className="py-16 text-center text-slate-500 bg-slate-900 rounded-2xl border border-slate-800">
            No ledger events matching filter.
          </div>
        ) : (
          filteredBlocks.map((block, idx) => (
            <div key={block.block_index} className="relative">
              {idx > 0 && (
                <div className="flex justify-center -my-2 mb-2 relative z-10">
                  <div className="p-1 rounded-full bg-slate-800 border border-slate-700 text-slate-400">
                    <ArrowDown className="w-3 h-3" />
                  </div>
                </div>
              )}

              <div className="bg-slate-900/90 border border-slate-800 hover:border-slate-700 rounded-2xl p-5 shadow-xl transition space-y-3">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-800 pb-3">
                  <div className="flex items-center space-x-3">
                    <span className="font-mono text-sm font-black px-2.5 py-1 rounded-lg bg-slate-950 border border-slate-800 text-purple-400">
                      BLOCK #{String(block.block_index).padStart(3, '0')}
                    </span>
                    <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider border ${
                      block.event_type === 'GENESIS'
                        ? 'bg-blue-950 text-blue-400 border-blue-800'
                        : block.event_type === 'ESCROW_CREATED'
                        ? 'bg-amber-950 text-amber-400 border-amber-800'
                        : block.event_type.includes('AUTHORIZED')
                        ? 'bg-cyan-950 text-cyan-400 border-cyan-800'
                        : block.event_type === 'PROOF_SUBMITTED'
                        ? 'bg-indigo-950 text-indigo-400 border-indigo-800'
                        : block.event_type === 'AI_VERIFIED'
                        ? 'bg-purple-950 text-purple-400 border-purple-800'
                        : block.event_type.includes('CAPTURED')
                        ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                        : 'bg-rose-950 text-rose-400 border-rose-800'
                    }`}>
                      {block.event_type.replace(/_/g, ' ')}
                    </span>
                  </div>

                  <div className="flex items-center space-x-2 text-xs text-slate-400 font-mono">
                    <Clock className="w-3.5 h-3.5 text-slate-500" />
                    <span>{new Date(block.timestamp).toLocaleString()}</span>
                  </div>
                </div>

                {/* Hashes Row */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                  <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                    <div className="overflow-hidden">
                      <span className="text-[10px] text-slate-500 uppercase block font-semibold">Block Hash (SHA-256)</span>
                      <span className="font-mono text-purple-300 truncate block text-[11px]">{block.block_hash}</span>
                    </div>
                    <button
                      onClick={() => handleCopy(block.block_hash)}
                      className="p-1 rounded text-slate-400 hover:text-white"
                      title="Copy Hash"
                    >
                      {copiedHash === block.block_hash ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>

                  <div className="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                    <div className="overflow-hidden">
                      <span className="text-[10px] text-slate-500 uppercase block font-semibold">Previous Hash Link</span>
                      <span className="font-mono text-slate-400 truncate block text-[11px]">{block.previous_hash}</span>
                    </div>
                    <button
                      onClick={() => handleCopy(block.previous_hash)}
                      className="p-1 rounded text-slate-400 hover:text-white"
                      title="Copy Hash"
                    >
                      {copiedHash === block.previous_hash ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                    </button>
                  </div>
                </div>

                {/* Payload View */}
                <div className="bg-slate-950/80 rounded-xl p-3 border border-slate-800 text-[11px] font-mono">
                  <span className="text-slate-500 block mb-1">Payload Content:</span>
                  <pre className="text-cyan-300 overflow-x-auto whitespace-pre-wrap leading-tight">
                    {JSON.stringify(block.payload, null, 2)}
                  </pre>
                </div>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
