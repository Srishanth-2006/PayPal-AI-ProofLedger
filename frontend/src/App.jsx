import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import ClientEscrowView from './components/ClientEscrowView';
import ContractorProofView from './components/ContractorProofView';
import ProofLedgerView from './components/ProofLedgerView';
import WebhookSimulator from './components/WebhookSimulator';
import PayPalButtonModal from './components/PayPalButtonModal';
import DisputePackModal from './components/DisputePackModal';
import { getMilestones } from './services/api';
import { Shield, Sparkles } from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('client');
  const [milestones, setMilestones] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedMilestone, setSelectedMilestone] = useState(null);
  const [approvedBanner, setApprovedBanner] = useState(null);

  // Modals
  const [payPalModal, setPayPalModal] = useState({ isOpen: false, milestone: null });
  const [disputeModal, setDisputeModal] = useState({ isOpen: false, milestoneId: null });

  const loadMilestones = async () => {
    try {
      setLoading(true);
      const data = await getMilestones();
      setMilestones(data);
      if (!selectedMilestone && data.length > 0) {
        setSelectedMilestone(data[0]);
      } else if (selectedMilestone) {
        const updated = data.find(m => m.id === selectedMilestone.id);
        if (updated) setSelectedMilestone(updated);
      }
    } catch (err) {
      console.error('Failed to load milestones:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMilestones();

    // Check for PayPal return redirect (?milestone=... or /escrow/approved)
    const urlParams = new URLSearchParams(window.location.search);
    const msId = urlParams.get('milestone');
    const isApproved = window.location.pathname.includes('/escrow/approved') || urlParams.get('status') === 'approved';
    const isCancelled = window.location.pathname.includes('/escrow/cancelled') || urlParams.get('status') === 'cancelled';

    if (isCancelled) {
      setApprovedBanner({
        type: 'cancelled',
        message: 'PayPal authorization hold was cancelled by buyer. No funds were locked.'
      });
    } else if (msId && isApproved) {
      (async () => {
        try {
          const res = await fetch(`/api/escrow/${msId}/authorize`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({})
          });
          if (res.ok) {
            const data = await res.json();
            setApprovedBanner({
              type: 'success',
              message: `✅ PayPal Escrow Locked! Authorization hold active for ${msId}. Switched to Contractor Proof view.`
            });
            await loadMilestones();
            setSelectedMilestone(data);
            setActiveTab('contractor');
          }
        } catch (e) {
          console.error('Auto-authorize redirect error:', e);
        }
      })();
    }
  }, []);

  const handleOpenPayPalModal = (m) => {
    setPayPalModal({ isOpen: true, milestone: m });
  };

  const handlePayPalSuccess = (updatedMilestone) => {
    loadMilestones();
    // Switch to contractor view to let them submit proof
    setSelectedMilestone(updatedMilestone);
    setActiveTab('contractor');
  };

  const handleOpenDisputeModal = (milestoneId) => {
    setDisputeModal({ isOpen: true, milestoneId });
  };

  const handleSelectMilestoneForWork = (m) => {
    setSelectedMilestone(m);
    setActiveTab('contractor');
  };

  return (
    <div className="min-h-screen bg-[#0B0F19] text-slate-100 flex flex-col selection:bg-cyan-500 selection:text-black">
      {/* Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        stats={{ total: milestones.length }}
      />

      {/* Hackathon Top Ribbon */}
      <div className="bg-gradient-to-r from-[#003087] via-[#0070BA] to-cyan-600 px-4 py-1.5 text-center text-[11px] font-bold text-white shadow-inner flex items-center justify-center space-x-2">
        <Sparkles className="w-3.5 h-3.5 text-amber-300 animate-spin" style={{ animationDuration: '4s' }} />
        <span>PayPal AI Hackathon 2026 Submission • Autonomous AI Escrow & Milestone Verification Oracle</span>
        <span className="hidden md:inline-block bg-white/20 px-2 py-0.5 rounded text-[10px]">
          Target Tracks: Agentic Commerce ($5k) & Best Use of PayPal + AI ($5k)
        </span>
      </div>

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* PayPal Redirect Alert Banner */}
        {approvedBanner && (
          <div className={`mb-6 p-4 rounded-xl border flex items-center justify-between text-sm ${
            approvedBanner.type === 'success'
              ? 'bg-emerald-950/40 border-emerald-500/50 text-emerald-300'
              : 'bg-rose-950/40 border-rose-500/50 text-rose-300'
          }`}>
            <span>{approvedBanner.message}</span>
            <button
              onClick={() => setApprovedBanner(null)}
              className="text-xs px-2.5 py-1 rounded bg-white/10 hover:bg-white/20 text-white ml-4 transition"
            >
              Dismiss
            </button>
          </div>
        )}

        {loading && milestones.length === 0 ? (
          <div className="py-24 text-center text-slate-400">
            <div className="w-10 h-10 border-3 border-cyan-400 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
            Connecting to ProofLedger API & PayPal Sandbox...
          </div>
        ) : (
          <>
            {activeTab === 'client' && (
              <ClientEscrowView
                milestones={milestones}
                onRefresh={loadMilestones}
                onOpenPayPalModal={handleOpenPayPalModal}
                onOpenDisputeModal={handleOpenDisputeModal}
                onSelectMilestoneForWork={handleSelectMilestoneForWork}
              />
            )}

            {activeTab === 'contractor' && (
              <ContractorProofView
                milestones={milestones}
                selectedMilestone={selectedMilestone}
                onSelectMilestone={setSelectedMilestone}
                onRefresh={loadMilestones}
                onOpenDisputeModal={handleOpenDisputeModal}
              />
            )}

            {activeTab === 'ledger' && (
              <ProofLedgerView
                selectedMilestoneId={selectedMilestone?.id}
              />
            )}

            {activeTab === 'webhooks' && (
              <WebhookSimulator
                milestones={milestones}
                onRefresh={loadMilestones}
              />
            )}
          </>
        )}
      </main>

      {/* Modals */}
      <PayPalButtonModal
        milestone={payPalModal.milestone}
        isOpen={payPalModal.isOpen}
        onClose={() => setPayPalModal({ isOpen: false, milestone: null })}
        onSuccess={handlePayPalSuccess}
      />

      <DisputePackModal
        milestoneId={disputeModal.milestoneId}
        isOpen={disputeModal.isOpen}
        onClose={() => setDisputeModal({ isOpen: false, milestoneId: null })}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800/80 bg-slate-950/80 py-8 px-4 text-xs text-slate-500">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <Shield className="w-4 h-4 text-cyan-400" />
            <span className="font-bold text-slate-300">ProofLedger</span>
            <span>— Autonomous AI Escrow & Milestone Verification Powered by PayPal</span>
          </div>

          <div className="flex items-center space-x-6 text-[11px]">
            <span className="text-slate-400">
              Orders v2 <code className="text-cyan-400 font-mono">intent: "AUTHORIZE"</code> $\rightarrow$ Multimodal AI $\rightarrow$ <code className="text-emerald-400 font-mono">/capture</code>
            </span>
            <span className="text-slate-400">
              SHA-256 Proof Chaining
            </span>
            <span className="text-slate-400">
              ReportLab PDF Dispute Pack
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
