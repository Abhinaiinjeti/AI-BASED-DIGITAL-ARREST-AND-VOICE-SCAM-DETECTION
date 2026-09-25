import React from 'react';
import { 
  ShieldAlert, 
  FileText, 
  Mic, 
  Languages, 
  BrainCircuit, 
  Lock, 
  ExternalLink, 
  ArrowRight,
  ChevronRight,
  ShieldCheck,
  AlertTriangle
} from 'lucide-react';

export default function Home({ setActiveTab, backendStatus }) {
  return (
    <div className="space-y-16 pb-16">
      
      {/* 1. MHA / I4C National Threat Banner */}
      <div className="bg-gradient-to-r from-rose-950/60 via-slate-900 to-rose-950/60 border-y border-rose-500/30 py-3 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center space-x-2 text-rose-300">
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-rose-500"></span>
            </span>
            <span className="font-bold tracking-wider uppercase font-mono">NATIONAL CYBER ADVISORY:</span>
            <span className="text-slate-200">
              Indian Law Enforcement agencies NEVER issue "Digital Arrests" or conduct court hearings over Skype/WhatsApp video calls.
            </span>
          </div>
          <div className="flex items-center space-x-4 font-mono text-[11px]">
            <span className="text-amber-400 font-bold">Helpline: Dial 1930</span>
            <a 
              href="https://cybercrime.gov.in" 
              target="_blank" 
              rel="noreferrer"
              className="text-cyan-400 hover:text-cyan-300 flex items-center gap-1"
            >
              <span>cybercrime.gov.in</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          </div>
        </div>
      </div>

      {/* 2. Hero Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8">
        <div className="text-center max-w-4xl mx-auto space-y-6">
          
          <div className="inline-flex items-center space-x-2 px-4 py-1.5 rounded-full bg-cyan-950/80 border border-cyan-500/40 text-cyan-300 text-xs font-mono tracking-wider">
            <BrainCircuit className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
            <span>MAJOR B.TECH ACADEMIC RESEARCH PROTOTYPE</span>
          </div>

          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black text-slate-100 tracking-tight leading-tight uppercase">
            AI-BASED DIGITAL ARREST AND <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-emerald-400">
              VOICE SCAM DETECTION
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 max-w-2xl mx-auto leading-relaxed">
            "Intelligent multilingual analysis of suspicious messages and voice conversations."
          </p>

          <p className="text-xs sm:text-sm text-slate-400 max-w-3xl mx-auto">
            Combines TF-IDF feature extraction, Machine Learning classifiers, Whisper speech-to-text, 
            and a specialized digital-arrest indicator engine to analyze telecom extortion and impersonation risks in real time.
          </p>

          {/* Primary Action Buttons */}
          <div className="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
            <button
              onClick={() => setActiveTab('text')}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold text-sm tracking-wider flex items-center justify-center space-x-2 shadow-[0_0_25px_rgba(6,182,212,0.4)] transition-all transform hover:-translate-y-0.5"
            >
              <FileText className="w-4 h-4" />
              <span>ANALYZE MESSAGE</span>
            </button>

            <button
              onClick={() => setActiveTab('voice')}
              className="w-full sm:w-auto px-8 py-3.5 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-100 border border-slate-700 hover:border-cyan-400/80 font-bold text-sm tracking-wider flex items-center justify-center space-x-2 transition-all transform hover:-translate-y-0.5"
            >
              <Mic className="w-4 h-4 text-cyan-400" />
              <span>ANALYZE VOICE</span>
            </button>
          </div>

          {/* System status subtitle */}
          <div className="text-[11px] font-mono text-slate-500 pt-2 flex items-center justify-center gap-4">
            <span>Model: Logistic Regression (Val F1: 1.00)</span>
            <span>•</span>
            <span>Speech: Faster-Whisper</span>
            <span>•</span>
            <span>Languages: EN / HI / TE</span>
          </div>

        </div>
      </div>

      {/* 3. Core Pillars Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          
          <div className="p-6 rounded-2xl glass-panel border border-slate-800/90 hover:border-cyan-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-cyan-950/80 border border-cyan-500/40 flex items-center justify-center text-cyan-400 mb-4 group-hover:scale-110 transition-transform">
              <ShieldAlert className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-100 mb-2">
              Digital Arrest Detection
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Specialized indicator rules targeting police/CBI impersonation, fake arrest warrants, Skype video isolation, and RBI verification scams.
            </p>
          </div>

          <div className="p-6 rounded-2xl glass-panel border border-slate-800/90 hover:border-teal-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-teal-950/80 border border-teal-500/40 flex items-center justify-center text-teal-400 mb-4 group-hover:scale-110 transition-transform">
              <Mic className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-100 mb-2">
              Voice & Audio Analysis
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Speech-to-text powered by Faster-Whisper. Transcribes live audio recordings or uploaded files into text before NLP classification.
            </p>
          </div>

          <div className="p-6 rounded-2xl glass-panel border border-slate-800/90 hover:border-indigo-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-indigo-950/80 border border-indigo-500/40 flex items-center justify-center text-indigo-400 mb-4 group-hover:scale-110 transition-transform">
              <Languages className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-100 mb-2">
              Multilingual Support
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Native recognition for English, Hindi, Hinglish, and Telugu from official INDICA and Indian Cyber Scam benchmarks.
            </p>
          </div>

          <div className="p-6 rounded-2xl glass-panel border border-slate-800/90 hover:border-emerald-500/40 transition-all group">
            <div className="w-12 h-12 rounded-xl bg-emerald-950/80 border border-emerald-500/40 flex items-center justify-center text-emerald-400 mb-4 group-hover:scale-110 transition-transform">
              <BrainCircuit className="w-6 h-6" />
            </div>
            <h3 className="text-base font-bold text-slate-100 mb-2">
              Explainable Risk Scoring
            </h3>
            <p className="text-xs text-slate-400 leading-relaxed">
              Separates ML model confidence from a 0-100 risk score, providing exact verbatim evidence quotes and safety advice.
            </p>
          </div>

        </div>
      </div>

      {/* 4. Quick Demo Section Callout */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="rounded-3xl glass-panel border border-cyan-500/30 p-8 sm:p-10 relative overflow-hidden bg-gradient-to-br from-slate-900/90 via-[#0A101D] to-slate-900/90">
          <div className="max-w-2xl space-y-4">
            <span className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider">
              Experience the Defense Prototype
            </span>
            <h2 className="text-2xl sm:text-3xl font-bold text-slate-100">
              Test Authentic Digital Arrest & KYC Phone Scam Scenarios
            </h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              Test with one-click realistic case studies including CBI extortion threats, 
              account block alerts, and native Telugu telecom fraud with full explainable breakdowns.
            </p>
            <div className="pt-2">
              <button
                onClick={() => setActiveTab('text')}
                className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white font-semibold text-xs tracking-wider transition-colors shadow-lg"
              >
                <span>Launch Demo Lab</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>

    </div>
  );
}
