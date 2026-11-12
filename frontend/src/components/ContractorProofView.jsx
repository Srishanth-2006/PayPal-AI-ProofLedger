import React, { useState, useEffect } from 'react';
import confetti from 'canvas-confetti';
import { UploadCloud, CheckCircle2, ShieldCheck, Cpu, Sparkles, RefreshCw } from 'lucide-react';
import LiveAiScanner from './LiveAiScanner';
import { submitProof, getSampleDeliverables } from '../services/api';

export default function ContractorProofView({
  milestones,
  selectedMilestone,
  onSelectMilestone,
  onRefresh,
  onOpenDisputeModal
}) {
  const [activeMilestoneId, setActiveMilestoneId] = useState(() => 
    selectedMilestone ? selectedMilestone.id : (milestones.find(m => m.status === 'ESCROW_LOCKED')?.id || milestones[0]?.id || '')
  );
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(() => 
    selectedMilestone?.proof ? `/uploads/${selectedMilestone.proof.file_name}` : null
  );
  const [contractorNotes, setContractorNotes] = useState('');
  const [samples, setSamples] = useState([]);
  const [scanning, setScanning] = useState(false);
  const [verdict, setVerdict] = useState(() => selectedMilestone?.verdict || null);
  const [settledAlert, setSettledAlert] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getSampleDeliverables().then(setSamples).catch(() => {});
  }, []);

  const activeMilestone = milestones.find(m => m.id === activeMilestoneId) || milestones[0];

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setVerdict(null);
      setSettledAlert(null);
    }
  };

  const handleSelectSample = async (sample) => {
    try {
      setError(null);
      setVerdict(null);
      setSettledAlert(null);
      // Fetch sample image as Blob
      const res = await fetch(sample.url);
      const blob = await res.blob();
      const file = new File([blob], sample.filename, { type: 'image/jpeg' });
      setSelectedFile(file);
      setPreviewUrl(sample.url);
      setContractorNotes(`Tested deliverable: ${sample.name}`);
    } catch (err) {
      setError('Could not load sample deliverable: ' + err.message);
    }
  };

  const handleSubmitProof = async () => {
    if (!selectedFile) {
      setError('Please select or load a deliverable proof image.');
      return;
    }
    if (!activeMilestone) return;

    try {
      setScanning(true);
      setError(null);
      setVerdict(null);
      setSettledAlert(null);

      const formData = new FormData();
      formData.append('file', selectedFile);
      if (contractorNotes) {
        formData.append('notes', contractorNotes);
      }

      // Simulate slight visual scanning delay for dramatic UX presentation
      await new Promise(r => setTimeout(r, 1200));

      const updatedMilestone = await submitProof(activeMilestone.id, formData);
      setVerdict(updatedMilestone.verdict);

      if (updatedMilestone.verdict && updatedMilestone.verdict.verdict === 'PASS') {
        // Trigger celebration confetti!
        confetti({
          particleCount: 80,
          spread: 70,
          origin: { y: 0.6 }
        });
        setSettledAlert({
          type: 'SUCCESS',
          title: 'PayPal Payment Settled Autonomously!',
          message: `The AI Oracle verified all criteria (Confidence: ${updatedMilestone.verdict.confidence_score}%). PayPal Authorization # ${updatedMilestone.paypal_authorization_id} has been captured! Funds landed in contractor's wallet.`
        });
      } else if (updatedMilestone.verdict && updatedMilestone.verdict.verdict === 'FAIL') {
        setSettledAlert({
          type: 'FAIL',
          title: 'Proof Verification Failed & Hold Voided',
          message: `Deliverable failed contractual specifications (Confidence: ${updatedMilestone.verdict.confidence_score}%). PayPal authorization voided to protect client balance.`
        });
      }

      onRefresh();
    } catch (err) {
      setError(err.message);
    } finally {
      setScanning(false);
    }
  };

  if (!activeMilestone) {
    return (
      <div className="py-20 text-center text-slate-400">
        No active escrow milestones available. Please switch to the Client view to create one.
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Header & Milestone Selector */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-black text-white tracking-tight">Contractor Deliverable & AI Verification</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Submit work deliverables to the ProofLedger Autonomous AI Oracle. Passes trigger instant PayPal release.
          </p>
        </div>

        {/* Milestone Dropdown */}
        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400">Target Milestone:</span>
          <select
            value={activeMilestoneId}
            onChange={e => {
              setActiveMilestoneId(e.target.value);
              const m = milestones.find(item => item.id === e.target.value);
              if (m) {
                onSelectMilestone(m);
                setVerdict(m.verdict || null);
                setPreviewUrl(m.proof ? `/uploads/${m.proof.file_name}` : null);
              }
            }}
            className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-medium focus:outline-none focus:border-cyan-500"
          >
            {milestones.map(m => (
              <option key={m.id} value={m.id}>
                {m.title} (${m.amount} USD) - [{m.status}]
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Contract Terms Banner */}
      <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800 pb-3">
          <div>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider block">Contract Terms & Escrow</span>
            <h2 className="text-lg font-black text-white">{activeMilestone.title}</h2>
          </div>
          <div className="flex items-center space-x-3">
            <div className="text-right">
              <span className="text-xs text-slate-400 block">Locked Escrow Payout</span>
              <span className="text-xl font-black font-mono text-emerald-400">
                ${activeMilestone.amount.toFixed(2)} {activeMilestone.currency}
              </span>
            </div>
            <span className={`px-2.5 py-1 rounded-full text-xs font-bold uppercase border ${
              activeMilestone.status === 'ESCROW_LOCKED'
                ? 'bg-cyan-950 text-cyan-400 border-cyan-800'
                : activeMilestone.status === 'COMPLETED'
                ? 'bg-emerald-950 text-emerald-400 border-emerald-800'
                : 'bg-slate-800 text-slate-300 border-slate-700'
            }`}>
              {activeMilestone.status.replace('_', ' ')}
            </span>
          </div>
        </div>

        {/* Deliverable Specifications Checklist */}
        <div className="space-y-2">
          <span className="text-xs font-semibold text-slate-300 block">
            Required Contractual Specifications to Release Funds:
          </span>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
            {activeMilestone.specifications.map((spec, i) => (
              <div key={i} className="flex items-start space-x-2 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800/80 text-xs text-slate-200">
                <CheckCircle2 className="w-4 h-4 text-cyan-400 flex-shrink-0 mt-0.5" />
                <span>{spec}</span>
              </div>
            ))}
          </div>
        </div>

        <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 bg-slate-950 p-2.5 rounded-xl border border-slate-800">
          <div>PayPal Authorization Hold: <span className="text-cyan-400">{activeMilestone.paypal_authorization_id || 'Hold Pending Approval'}</span></div>
          <div>Client: <span className="text-slate-300">{activeMilestone.client_name}</span></div>
        </div>
      </div>

      {/* Proof Submission & Quick Test Samples */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Upload Zone */}
        <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-2xl p-5 space-y-4">
          <h3 className="text-sm font-bold text-white flex items-center space-x-2">
            <UploadCloud className="w-4 h-4 text-cyan-400" />
            <span>Upload Deliverable Proof</span>
          </h3>

          {/* Quick Preset Samples for Judges */}
          <div className="space-y-1.5">
            <span className="text-[11px] text-slate-400 block font-semibold">
              Or 1-click test with preloaded hackathon samples:
            </span>
            <div className="space-y-1.5">
              {samples.map((s, idx) => (
                <button
                  key={idx}
                  type="button"
                  onClick={() => handleSelectSample(s)}
                  className="w-full text-left p-2 rounded-xl bg-slate-950 hover:bg-slate-800/80 border border-slate-800 hover:border-cyan-600/50 transition flex items-center justify-between group cursor-pointer"
                >
                  <div>
                    <span className="text-xs font-bold text-slate-200 group-hover:text-cyan-300 block">
                      {s.name}
                    </span>
                    <span className="text-[10px] text-slate-400">{s.expected_outcome}</span>
                  </div>
                  <Sparkles className="w-3.5 h-3.5 text-slate-500 group-hover:text-cyan-400" />
                </button>
              ))}
            </div>
          </div>

          {/* File input box */}
          <label className="border-2 border-dashed border-slate-700 hover:border-cyan-500 rounded-xl p-4 flex flex-col items-center justify-center text-center cursor-pointer bg-slate-950/40 hover:bg-slate-950/80 transition space-y-2">
            <UploadCloud className="w-8 h-8 text-cyan-400" />
            <span className="text-xs font-semibold text-slate-200">
              {selectedFile ? selectedFile.name : 'Choose local image/photo'}
            </span>
            <span className="text-[10px] text-slate-500">JPG, PNG, or WebP up to 15MB</span>
            <input type="file" accept="image/*" onChange={handleFileChange} className="hidden" />
          </label>

          {/* Notes */}
          <div>
            <label className="text-[11px] text-slate-400 block mb-1">Contractor Notes (Optional)</label>
            <input
              type="text"
              value={contractorNotes}
              onChange={e => setContractorNotes(e.target.value)}
              placeholder="e.g. Capacitor wired, manifold reading 68 PSI"
              className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white placeholder-slate-600 focus:outline-none focus:border-cyan-500"
            />
          </div>

          {error && (
            <div className="p-3 bg-rose-950/60 border border-rose-800 rounded-xl text-rose-300 text-xs">
              {error}
            </div>
          )}

          {/* Trigger Button */}
          <button
            onClick={handleSubmitProof}
            disabled={scanning || !selectedFile}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-emerald-600 via-teal-600 to-cyan-600 hover:opacity-95 text-white font-extrabold text-xs flex items-center justify-center space-x-2 shadow-lg shadow-teal-500/20 transition cursor-pointer disabled:opacity-50"
          >
            {scanning ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                <span>AI Oracle Inspecting Deliverable...</span>
              </>
            ) : (
              <>
                <Cpu className="w-4 h-4" />
                <span>Submit & Inspect with Multimodal AI</span>
              </>
            )}
          </button>
        </div>

        {/* AI Scanner & Result Display */}
        <div className="lg:col-span-2 space-y-4">
          {settledAlert && (
            <div className={`p-4 rounded-2xl border flex items-start space-x-3 text-xs animate-bounce-once ${
              settledAlert.type === 'SUCCESS'
                ? 'bg-emerald-950/50 border-emerald-800 text-emerald-200'
                : 'bg-rose-950/50 border-rose-800 text-rose-200'
            }`}>
              <ShieldCheck className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <span className="font-bold text-sm block">{settledAlert.title}</span>
                <p className="mt-0.5">{settledAlert.message}</p>
                <div className="mt-2 flex items-center space-x-2">
                  <button
                    onClick={() => onOpenDisputeModal(activeMilestone.id)}
                    className="px-3 py-1 rounded-lg bg-emerald-800/80 hover:bg-emerald-700 text-white font-semibold transition"
                  >
                    View Official Dispute Pack
                  </button>
                </div>
              </div>
            </div>
          )}

          <LiveAiScanner
            scanning={scanning}
            verdict={verdict}
            proofUrl={previewUrl}
            specifications={activeMilestone.specifications}
          />
        </div>
      </div>
    </div>
  );
}
