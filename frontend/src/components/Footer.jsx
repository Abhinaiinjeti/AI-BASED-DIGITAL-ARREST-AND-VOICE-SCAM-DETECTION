import React from 'react';
import { Shield, Lock, AlertTriangle, ExternalLink } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800/80 bg-[#060910] text-slate-400 py-10 px-4 mt-auto">
      <div className="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 text-xs">
        
        {/* Column 1: Identity & Official Title */}
        <div className="space-y-3">
          <div className="flex items-center space-x-2 text-slate-200 font-bold text-sm">
            <Shield className="w-5 h-5 text-cyan-400" />
            <span>AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            A production-style academic prototype combining Natural Language Processing, 
            Speech-to-Text, Machine Learning classifiers, and transparent rule-based risk engines 
            to combat telecom coercion and cyber extortion in India.
          </p>
          <div className="text-[11px] text-cyan-500/80 font-mono">
            B.Tech Major Project Prototype • Free-First Architecture
          </div>
        </div>

        {/* Column 2: Privacy & Responsible AI */}
        <div className="space-y-3 border-l md:border-l border-slate-800 md:pl-6">
          <div className="flex items-center space-x-2 text-slate-200 font-semibold">
            <Lock className="w-4 h-4 text-emerald-400" />
            <span>Privacy & Ethical AI Commitment</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            This system runs strictly as an AI risk detection and decision-support assistant. 
            No raw conversational audio or sensitive text messages are permanently stored without 
            explicit consent. Never input authentic banking passwords or real OTPs.
          </p>
          <p className="text-slate-500 text-[11px]">
            The system does not claim 100% infallible certainty and provides explainable probability indicators.
          </p>
        </div>

        {/* Column 3: Emergency Helplines */}
        <div className="space-y-3 border-l md:border-l border-slate-800 md:pl-6">
          <div className="flex items-center space-x-2 text-slate-200 font-semibold">
            <AlertTriangle className="w-4 h-4 text-amber-400" />
            <span>National Cyber Crime Reporting</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            If you or someone you know is currently being coerced or threatened with digital arrest, 
            immediately report to official government channels:
          </p>
          <div className="space-y-1.5 font-mono text-[11px]">
            <a 
              href="https://cybercrime.gov.in" 
              target="_blank" 
              rel="noreferrer"
              className="flex items-center space-x-1.5 text-cyan-400 hover:text-cyan-300 transition-colors"
            >
              <span>Portal: cybercrime.gov.in</span>
              <ExternalLink className="w-3 h-3" />
            </a>
            <div className="text-rose-400 font-bold">
              National Helpline: Dial 1930 (Toll Free)
            </div>
          </div>
        </div>

      </div>

      <div className="max-w-7xl mx-auto mt-8 pt-6 border-t border-slate-800/60 flex flex-col sm:flex-row items-center justify-between text-[11px] text-slate-500">
        <div>
          Official Title: <span className="text-slate-400 font-medium">AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION</span>
        </div>
        <div className="mt-2 sm:mt-0 font-mono">
          Scikit-Learn • Faster-Whisper • FastAPI • React
        </div>
      </div>
    </footer>
  );
}
