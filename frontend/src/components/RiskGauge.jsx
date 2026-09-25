import React, { useEffect, useState } from 'react';
import { ShieldCheck, AlertCircle, AlertTriangle, ShieldAlert, Cpu } from 'lucide-react';

export default function RiskGauge({ score = 0, riskLevel = 'LOW', confidence = 0.5 }) {
  const [animatedScore, setAnimatedScore] = useState(0);

  useEffect(() => {
    let start = 0;
    const end = Math.min(100, Math.max(0, score));
    const duration = 1200; // ms
    const increment = end / (duration / 16);

    const timer = setInterval(() => {
      start += increment;
      if (start >= end) {
        setAnimatedScore(end);
        clearInterval(timer);
      } else {
        setAnimatedScore(Math.round(start));
      }
    }, 16);

    return () => clearInterval(timer);
  }, [score]);

  // Color mapping based on risk level
  const getTheme = () => {
    if (score <= 25) {
      return {
        stroke: '#10B981', // Emerald
        bgGlow: 'rgba(16, 185, 129, 0.15)',
        badgeBg: 'bg-emerald-950/80 border-emerald-500/50 text-emerald-400',
        text: 'text-emerald-400',
        icon: ShieldCheck,
        label: 'LOW RISK',
      };
    } else if (score <= 50) {
      return {
        stroke: '#FBBF24', // Amber/Yellow
        bgGlow: 'rgba(251, 191, 36, 0.15)',
        badgeBg: 'bg-amber-950/80 border-amber-500/50 text-amber-400',
        text: 'text-amber-400',
        icon: AlertCircle,
        label: 'SUSPICIOUS',
      };
    } else if (score <= 75) {
      return {
        stroke: '#F97316', // Orange
        bgGlow: 'rgba(249, 115, 22, 0.15)',
        badgeBg: 'bg-orange-950/80 border-orange-500/50 text-orange-400',
        text: 'text-orange-400',
        icon: AlertTriangle,
        label: 'HIGH RISK',
      };
    } else {
      return {
        stroke: '#EF4444', // Red
        bgGlow: 'rgba(239, 68, 68, 0.2)',
        badgeBg: 'bg-rose-950/80 border-rose-500/60 text-rose-400 shadow-[0_0_15px_rgba(239,68,68,0.3)]',
        text: 'text-rose-400',
        icon: ShieldAlert,
        label: 'VERY HIGH RISK',
      };
    }
  };

  const theme = getTheme();
  const Icon = theme.icon;

  // Gauge SVG calculations (radius = 80, circumference = 2 * PI * 80 = 502.65, semicircle = 251.32)
  const radius = 80;
  const strokeWidth = 14;
  const circumference = Math.PI * radius; // 180-degree semi-circle
  const strokeDashoffset = circumference - (animatedScore / 100) * circumference;

  return (
    <div className="flex flex-col items-center justify-center p-6 rounded-2xl glass-panel relative overflow-hidden">
      {/* Dynamic Background Glow */}
      <div 
        className="absolute inset-0 pointer-events-none transition-all duration-700 blur-2xl opacity-60"
        style={{ background: `radial-gradient(circle at center, ${theme.bgGlow} 0%, transparent 70%)` }}
      />

      <div className="relative z-10 flex flex-col items-center">
        {/* Semicircular Gauge SVG */}
        <div className="relative w-56 h-32 flex items-end justify-center">
          <svg className="w-56 h-32 overflow-visible" viewBox="0 0 200 110">
            {/* Background Track Arc */}
            <path
              d="M 20,100 A 80,80 0 0,1 180,100"
              fill="none"
              stroke="#1E293B"
              strokeWidth={strokeWidth}
              strokeLinecap="round"
            />
            {/* Animated Colored Progress Arc */}
            <path
              d="M 20,100 A 80,80 0 0,1 180,100"
              fill="none"
              stroke={theme.stroke}
              strokeWidth={strokeWidth}
              strokeDasharray={circumference}
              strokeDashoffset={strokeDashoffset}
              strokeLinecap="round"
              className="transition-all duration-300 ease-out"
              style={{
                filter: `drop-shadow(0 0 8px ${theme.stroke}66)`,
              }}
            />
          </svg>

          {/* Centered Score Counter */}
          <div className="absolute bottom-1 flex flex-col items-center">
            <span className="text-4xl font-extrabold tracking-tight font-mono text-slate-100">
              {animatedScore}
            </span>
            <span className="text-[11px] font-mono tracking-widest text-slate-400 uppercase">
              Score / 100
            </span>
          </div>
        </div>

        {/* Risk Level Badge */}
        <div className={`mt-3 px-4 py-1.5 rounded-full border text-xs font-bold tracking-wider flex items-center space-x-2 ${theme.badgeBg}`}>
          <Icon className="w-4 h-4" />
          <span>{theme.label}</span>
        </div>

        {/* Essential Distinction: Model Confidence vs Composite Risk Score */}
        <div className="mt-5 pt-4 border-t border-slate-800/80 w-full grid grid-cols-2 gap-3 text-center">
          <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800">
            <div className="text-[10px] text-slate-400 font-mono flex items-center justify-center gap-1">
              <Cpu className="w-3 h-3 text-cyan-400" />
              <span>MODEL CONFIDENCE</span>
            </div>
            <div className="text-base font-bold font-mono text-cyan-300 mt-0.5">
              {(confidence * 100).toFixed(1)}%
            </div>
          </div>

          <div className="p-2 rounded-lg bg-slate-900/60 border border-slate-800">
            <div className="text-[10px] text-slate-400 font-mono">
              COMPOSITE RISK
            </div>
            <div className={`text-base font-bold font-mono mt-0.5 ${theme.text}`}>
              {score} / 100
            </div>
          </div>
        </div>

        <p className="text-[10px] text-slate-500 mt-3 text-center max-w-xs leading-normal">
          *Model confidence represents ML statistical probability; Risk score combines ML output with coercive threat indicators.
        </p>

      </div>
    </div>
  );
}
