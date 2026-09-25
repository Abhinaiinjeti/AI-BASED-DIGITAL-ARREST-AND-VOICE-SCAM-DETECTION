import React from 'react';
import { ShieldAlert, Activity, FileText, Mic, BarChart3, History, HelpCircle, Info } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, backendStatus }) {
  const navItems = [
    { id: 'home', label: 'Home', icon: Activity },
    { id: 'text', label: 'Text Analysis', icon: FileText },
    { id: 'voice', label: 'Voice Analysis', icon: Mic },
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'history', label: 'History', icon: History },
    { id: 'how-it-works', label: 'How It Works', icon: HelpCircle },
    { id: 'about', label: 'About', icon: Info },
  ];

  return (
    <header className="sticky top-0 z-50 glass-panel border-b border-slate-800 bg-[#080C14]/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-18">
          
          {/* Brand & Exact Title */}
          <div 
            onClick={() => setActiveTab('home')}
            className="flex items-center space-x-3 cursor-pointer group"
          >
            <div className="w-10 h-10 rounded-xl bg-cyan-950/80 border border-cyan-500/40 flex items-center justify-center text-cyan-400 group-hover:border-cyan-400 group-hover:shadow-[0_0_15px_rgba(6,182,212,0.4)] transition-all">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <div>
              <div className="text-sm font-bold tracking-wider text-slate-100 flex items-center gap-2">
                <span>AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION</span>
              </div>
              <p className="text-[11px] text-cyan-400 font-mono tracking-wide">
                CYBERSECURITY DECISION-SUPPORT SYSTEM
              </p>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden lg:flex items-center space-x-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activeTab === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActiveTab(item.id)}
                  className={`flex items-center space-x-2 px-3.5 py-2 rounded-lg text-xs font-medium transition-all ${
                    isActive
                      ? 'bg-cyan-950/70 text-cyan-300 border border-cyan-500/40 shadow-[0_0_12px_rgba(6,182,212,0.2)]'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                  }`}
                >
                  <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>

          {/* Backend Status Badge */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-700/60 text-xs">
              <span className={`w-2 h-2 rounded-full ${backendStatus.online ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'}`} />
              <span className="text-slate-300 font-mono text-[11px]">
                {backendStatus.online ? 'BACKEND LIVE' : 'CONNECTING...'}
              </span>
            </div>
          </div>

        </div>

        {/* Mobile Navigation Bar */}
        <div className="lg:hidden flex items-center space-x-1 py-2 border-t border-slate-800/80 overflow-x-auto">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`flex items-center space-x-1.5 px-2.5 py-1.5 rounded-md text-[11px] whitespace-nowrap transition-all ${
                  isActive
                    ? 'bg-cyan-950 text-cyan-300 border border-cyan-500/40'
                    : 'text-slate-400 hover:text-slate-200'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </div>

      </div>
    </header>
  );
}
