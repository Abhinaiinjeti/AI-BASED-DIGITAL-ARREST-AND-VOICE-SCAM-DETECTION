import React, { useState } from 'react';
import { AlertTriangle, ShieldAlert, AlertCircle, Info, ChevronDown, ChevronUp, Quote } from 'lucide-react';

export default function IndicatorCard({ indicator }) {
  const [expanded, setExpanded] = useState(false);

  const getSeverityBadge = (sev) => {
    switch (sev.toLowerCase()) {
      case 'critical':
        return {
          bg: 'bg-rose-950/80 border-rose-500/60 text-rose-300',
          icon: ShieldAlert,
          label: 'CRITICAL',
        };
      case 'high':
        return {
          bg: 'bg-orange-950/80 border-orange-500/50 text-orange-300',
          icon: AlertTriangle,
          label: 'HIGH SEVERITY',
        };
      case 'medium':
        return {
          bg: 'bg-amber-950/80 border-amber-500/50 text-amber-300',
          icon: AlertCircle,
          label: 'MEDIUM SEVERITY',
        };
      default:
        return {
          bg: 'bg-slate-800/80 border-slate-600/50 text-slate-300',
          icon: Info,
          label: 'INFORMATIONAL',
        };
    }
  };

  const badge = getSeverityBadge(indicator.severity);
  const Icon = badge.icon;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/70 p-4 transition-all hover:border-slate-700/80">
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start space-x-3">
          <div className="mt-0.5 p-2 rounded-lg bg-slate-800/80 border border-slate-700/60 text-slate-200">
            <Icon className="w-4 h-4 text-cyan-400" />
          </div>
          <div>
            <div className="flex flex-wrap items-center gap-2">
              <h4 className="text-sm font-bold text-slate-100">
                {indicator.indicator}
              </h4>
              <span className={`px-2 py-0.5 rounded-full text-[10px] font-mono font-bold border ${badge.bg}`}>
                {badge.label}
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1 leading-relaxed">
              {indicator.explanation}
            </p>
          </div>
        </div>

        {indicator.all_evidence && indicator.all_evidence.length > 1 && (
          <button
            onClick={() => setExpanded(!expanded)}
            className="text-slate-400 hover:text-slate-200 p-1 rounded-md transition-colors"
            title="Toggle extra matches"
          >
            {expanded ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
          </button>
        )}
      </div>

      {/* Primary Evidence Quote */}
      {indicator.evidence && (
        <div className="mt-3 p-2.5 rounded-lg bg-slate-950/80 border border-slate-800/80 flex items-start space-x-2">
          <Quote className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
          <div className="text-xs font-mono text-slate-300 leading-snug">
            <span className="text-slate-500 text-[10px] uppercase block tracking-wider mb-0.5">
              Triggering Evidence in Text:
            </span>
            <span className="text-cyan-200 bg-cyan-950/40 px-1 py-0.5 rounded border border-cyan-800/50">
              "{indicator.evidence}"
            </span>
          </div>
        </div>
      )}

      {/* Expanded Multiple Matches */}
      {expanded && indicator.all_evidence && indicator.all_evidence.length > 1 && (
        <div className="mt-2 pl-4 border-l-2 border-slate-800 space-y-1.5 pt-1">
          <span className="text-[10px] font-mono text-slate-500 uppercase">
            Additional Matched Contexts ({indicator.all_evidence.length}):
          </span>
          {indicator.all_evidence.slice(1).map((ev, i) => (
            <div key={i} className="text-xs font-mono text-slate-400">
              • "{ev}"
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
