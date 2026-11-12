import React from 'react';
import { ShieldCheck, Cpu, CreditCard, Database, Radio } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab }) {
  return (
    <header className="border-b border-slate-800 bg-slate-900/80 backdrop-blur sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Brand */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActiveTab('client')}>
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-[#003087] via-[#0070BA] to-[#00CFDE] flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <ShieldCheck className="w-6 h-6 text-white" />
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-xl font-black tracking-tight text-white">
                  Proof<span className="text-[#0070BA]">Ledger</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800/60">
                  PayPal AI Escrow
                </span>
              </div>
              <p className="text-[11px] text-slate-400">Autonomous Milestone Verification Rails</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex items-center space-x-1 bg-slate-950/60 p-1.5 rounded-xl border border-slate-800">
            <button
              onClick={() => setActiveTab('client')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'client'
                  ? 'bg-gradient-to-r from-[#003087] to-[#0070BA] text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <CreditCard className="w-4 h-4" />
              <span>Client Escrow</span>
            </button>

            <button
              onClick={() => setActiveTab('contractor')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'contractor'
                  ? 'bg-gradient-to-r from-emerald-600 to-teal-500 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Cpu className="w-4 h-4" />
              <span>Contractor & AI Scanner</span>
            </button>

            <button
              onClick={() => setActiveTab('ledger')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'ledger'
                  ? 'bg-gradient-to-r from-purple-600 to-indigo-600 text-white shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Database className="w-4 h-4" />
              <span>Proof Ledger</span>
            </button>

            <button
              onClick={() => setActiveTab('webhooks')}
              className={`flex items-center space-x-2 px-3.5 py-1.5 rounded-lg text-xs font-semibold transition-all ${
                activeTab === 'webhooks'
                  ? 'bg-gradient-to-r from-amber-600 to-yellow-500 text-slate-950 font-bold shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
              }`}
            >
              <Radio className="w-4 h-4" />
              <span>Webhook Simulator</span>
            </button>
          </nav>

          {/* Status indicators */}
          <div className="flex items-center space-x-3">
            <div className="hidden sm:flex items-center space-x-2 bg-slate-800/50 px-3 py-1.5 rounded-lg border border-slate-700/60 text-xs">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span className="text-slate-300 font-medium">PayPal Sandbox</span>
              <span className="text-slate-500 font-mono">v2.AUTH</span>
            </div>

            <div className="flex items-center space-x-2 bg-cyan-950/40 px-3 py-1.5 rounded-lg border border-cyan-800/40 text-xs">
              <Cpu className="w-3.5 h-3.5 text-cyan-400 animate-spin" style={{ animationDuration: '6s' }} />
              <span className="text-cyan-300 font-medium">AI Oracle Ready</span>
            </div>
          </div>
        </div>

        {/* Mobile Navigation Row */}
        <nav className="flex md:hidden items-center space-x-1 py-2 overflow-x-auto border-t border-slate-800/60 no-scrollbar">
          <button
            onClick={() => setActiveTab('client')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
              activeTab === 'client'
                ? 'bg-[#0070BA] text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <CreditCard className="w-3.5 h-3.5" />
            <span>Client</span>
          </button>
          <button
            onClick={() => setActiveTab('contractor')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
              activeTab === 'contractor'
                ? 'bg-emerald-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Cpu className="w-3.5 h-3.5" />
            <span>AI Scanner</span>
          </button>
          <button
            onClick={() => setActiveTab('ledger')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
              activeTab === 'ledger'
                ? 'bg-purple-600 text-white'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Database className="w-3.5 h-3.5" />
            <span>Ledger</span>
          </button>
          <button
            onClick={() => setActiveTab('webhooks')}
            className={`flex items-center space-x-1.5 px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
              activeTab === 'webhooks'
                ? 'bg-amber-500 text-slate-950 font-bold'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Radio className="w-3.5 h-3.5" />
            <span>Webhooks</span>
          </button>
        </nav>
      </div>
    </header>
  );
}
