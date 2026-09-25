import React from 'react';
import { 
  ShieldAlert, 
  CheckCircle2, 
  AlertTriangle, 
  FileText, 
  Download, 
  ExternalLink, 
  Globe2, 
  Cpu, 
  AlertOctagon,
  PhoneCall
} from 'lucide-react';
import RiskGauge from './RiskGauge';
import IndicatorCard from './IndicatorCard';

export default function ResultView({ result, onReset }) {
  if (!result) return null;

  const handleExportJSON = () => {
    const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(result, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute('href', dataStr);
    downloadAnchor.setAttribute('download', `scam_analysis_report_${Date.now()}.json`);
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div className="space-y-8 animate-fadeIn">
      
      {/* Header bar */}
      <div className="flex flex-wrap items-center justify-between gap-4 p-5 rounded-2xl glass-panel border border-slate-800">
        <div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-ping"></span>
            <span className="text-xs font-mono font-bold text-cyan-400 tracking-wider uppercase">
              ANALYSIS COMPLETE
            </span>
          </div>
          <h2 className="text-xl font-bold text-slate-100 mt-1">
            Multilingual Threat & Risk Assessment Report
          </h2>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={handleExportJSON}
            className="flex items-center space-x-1.5 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-700 text-xs font-medium transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            <span>Export JSON</span>
          </button>

          {onReset && (
            <button
              onClick={onReset}
              className="px-4 py-2 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold transition-colors shadow-md"
            >
              Analyze Another
            </button>
          )}
        </div>
      </div>

      {/* Main Grid: Left = Risk Gauge & Metadata, Right = Detected Indicators & Advisory */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column: Risk Gauge & ML Specs (5 cols) */}
        <div className="lg:col-span-5 space-y-5">
          {/* Animated Gauge */}
          <RiskGauge
            score={result.risk_score}
            riskLevel={result.risk_level}
            confidence={result.model_confidence}
          />

          {/* Model & Language Metadata Card */}
          <div className="p-5 rounded-2xl glass-panel border border-slate-800 space-y-3.5 text-xs">
            <h4 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider">
              Diagnostic Metadata
            </h4>

            <div className="flex items-center justify-between py-1.5 border-b border-slate-800/80">
              <span className="text-slate-400 flex items-center gap-1.5">
                <Globe2 className="w-3.5 h-3.5 text-cyan-400" />
                <span>Detected Language</span>
              </span>
              <span className="font-mono font-bold text-slate-200">
                {result.language} {result.is_language_uncertain ? '(Uncertain)' : `(${(result.language_confidence*100).toFixed(0)}%)`}
              </span>
            </div>

            <div className="flex items-center justify-between py-1.5 border-b border-slate-800/80">
              <span className="text-slate-400 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-cyan-400" />
                <span>ML Classification</span>
              </span>
              <span className={`font-mono font-bold px-2 py-0.5 rounded text-[11px] ${
                result.classification === 'Scam'
                  ? 'bg-rose-950 text-rose-300 border border-rose-800'
                  : 'bg-emerald-950 text-emerald-300 border border-emerald-800'
              }`}>
                {result.classification}
              </span>
            </div>

            <div className="flex items-center justify-between py-1.5 border-b border-slate-800/80">
              <span className="text-slate-400">Scam Category</span>
              <span className="font-mono text-cyan-300 font-semibold uppercase text-[11px]">
                {result.scam_category.replace(/_/g, ' ')}
              </span>
            </div>

            <div className="flex items-center justify-between py-1.5">
              <span className="text-slate-400">Digital Arrest Signature</span>
              <span className={`font-mono font-bold text-[11px] ${
                result.is_digital_arrest ? 'text-rose-400 animate-pulse' : 'text-slate-400'
              }`}>
                {result.is_digital_arrest ? 'DETECTED' : 'Not Flagged'}
              </span>
            </div>
          </div>
        </div>

        {/* Right Column: Contextual Safety Advisory & Detected Indicators (7 cols) */}
        <div className="lg:col-span-7 space-y-5">
          
          {/* Contextual Recommendation Banner */}
          <div className={`p-5 rounded-2xl border ${
            result.risk_level === 'VERY HIGH'
              ? 'bg-rose-950/70 border-rose-500/60 shadow-[0_0_20px_rgba(244,63,94,0.15)]'
              : result.risk_level === 'HIGH'
              ? 'bg-orange-950/70 border-orange-500/60'
              : result.risk_level === 'SUSPICIOUS'
              ? 'bg-amber-950/60 border-amber-500/50'
              : 'bg-emerald-950/60 border-emerald-500/50'
          }`}>
            <div className="flex items-start space-x-3">
              <AlertOctagon className={`w-5 h-5 shrink-0 mt-0.5 ${
                result.risk_level === 'VERY HIGH' || result.risk_level === 'HIGH'
                  ? 'text-rose-400'
                  : result.risk_level === 'SUSPICIOUS'
                  ? 'text-amber-400'
                  : 'text-emerald-400'
              }`} />
              <div className="space-y-2">
                <h4 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-200">
                  Contextual Safety Recommendation
                </h4>
                <p className="text-xs text-slate-100 leading-relaxed font-medium">
                  {result.recommendation}
                </p>

                {(result.risk_level === 'HIGH' || result.risk_level === 'VERY HIGH') && (
                  <div className="pt-2 flex flex-wrap items-center gap-3 text-[11px] font-mono">
                    <a
                      href="https://cybercrime.gov.in"
                      target="_blank"
                      rel="noreferrer"
                      className="px-3 py-1.5 rounded-lg bg-rose-900/80 hover:bg-rose-800 text-white font-bold flex items-center gap-1.5 transition-colors"
                    >
                      <ExternalLink className="w-3 h-3" />
                      <span>Report to cybercrime.gov.in</span>
                    </a>
                    <div className="px-3 py-1.5 rounded-lg bg-slate-900 text-amber-300 font-bold border border-amber-500/40 flex items-center gap-1.5">
                      <PhoneCall className="w-3 h-3" />
                      <span>Helpline: Dial 1930</span>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Detected Indicators List */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 text-cyan-400" />
                <h3 className="text-sm font-bold text-slate-100">
                  Detected Suspicious Indicators ({result.indicators.length})
                </h3>
              </div>
              <span className="text-[11px] font-mono text-slate-400">
                Transparent Rule & Pattern Engine
              </span>
            </div>

            {result.indicators.length > 0 ? (
              <div className="space-y-3">
                {result.indicators.map((ind, i) => (
                  <IndicatorCard key={i} indicator={ind} />
                ))}
              </div>
            ) : (
              <div className="p-8 text-center text-slate-500 text-xs font-mono">
                <CheckCircle2 className="w-8 h-8 text-emerald-500/70 mx-auto mb-2" />
                No malicious coercions or suspicious extortion indicators were detected.
              </div>
            )}
          </div>

        </div>

      </div>

    </div>
  );
}
