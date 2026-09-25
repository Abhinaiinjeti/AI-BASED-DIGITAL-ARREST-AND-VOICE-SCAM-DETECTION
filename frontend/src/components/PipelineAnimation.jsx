import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Globe2, 
  Wrench, 
  Binary, 
  BrainCircuit, 
  ShieldAlert, 
  CheckCircle2, 
  ChevronRight,
  Mic
} from 'lucide-react';

export default function PipelineAnimation({ stages = [], isProcessing = false, inputType = 'text' }) {
  const defaultStages = [
    {
      id: 'input',
      name: inputType === 'voice' ? 'Voice Audio' : 'Text Input',
      desc: inputType === 'voice' ? 'Audio stream uploaded' : 'Raw message received',
      icon: inputType === 'voice' ? Mic : FileText,
    },
    {
      id: 'language',
      name: 'Language Identification',
      desc: 'Indic scripts & Hinglish detection',
      icon: Globe2,
    },
    {
      id: 'preprocessing',
      name: 'Domain Preprocessing',
      desc: 'Preserves legal & authority keywords',
      icon: Wrench,
    },
    {
      id: 'tfidf',
      name: 'TF-IDF Vectorization',
      desc: 'Unigram & Bigram feature extraction',
      icon: Binary,
    },
    {
      id: 'ml_classifier',
      name: 'Machine Learning Model',
      desc: 'Trained Scikit-Learn Classifier',
      icon: BrainCircuit,
    },
    {
      id: 'indicator_engine',
      name: 'Indicator & Risk Engine',
      desc: 'Digital Arrest coercion patterns',
      icon: ShieldAlert,
    },
    {
      id: 'result',
      name: 'Explainable Outcome',
      desc: 'Final risk score & advisory',
      icon: CheckCircle2,
    },
  ];

  const [activeStep, setActiveStep] = useState(isProcessing ? 0 : defaultStages.length - 1);

  useEffect(() => {
    if (isProcessing) {
      setActiveStep(0);
      const interval = setInterval(() => {
        setActiveStep((prev) => {
          if (prev < defaultStages.length - 1) {
            return prev + 1;
          }
          clearInterval(interval);
          return prev;
        });
      }, 350);
      return () => clearInterval(interval);
    } else {
      setActiveStep(defaultStages.length - 1);
    }
  }, [isProcessing]);

  return (
    <div className="w-full glass-panel rounded-2xl p-5 border border-slate-800/90 overflow-hidden">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="relative flex h-2.5 w-2.5">
            <span className={`animate-ping absolute inline-flex h-full w-full rounded-full opacity-75 ${isProcessing ? 'bg-cyan-400' : 'bg-emerald-400'}`}></span>
            <span className={`relative inline-flex rounded-full h-2.5 w-2.5 ${isProcessing ? 'bg-cyan-500' : 'bg-emerald-500'}`}></span>
          </span>
          <span className="text-xs font-mono font-bold tracking-wider text-slate-300 uppercase">
            {isProcessing ? 'AI Pipeline Processing Stages...' : 'Verified AI Pipeline Stages'}
          </span>
        </div>
        <span className="text-[11px] font-mono text-cyan-400">
          7-STAGE REAL-TIME PIPELINE
        </span>
      </div>

      {/* Horizontal Step Pipeline */}
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 relative">
        {defaultStages.map((step, idx) => {
          const Icon = step.icon;
          const isDone = idx <= activeStep;
          const isCurrent = idx === activeStep && isProcessing;

          // Matched actual stage output from backend if available
          const stageOutput = stages.find((s) => s.stage_id.includes(step.id) || step.id.includes(s.stage_id));

          return (
            <div
              key={step.id}
              className={`p-3 rounded-xl border flex flex-col justify-between transition-all duration-300 relative ${
                isCurrent
                  ? 'bg-cyan-950/80 border-cyan-400/80 shadow-[0_0_15px_rgba(6,182,212,0.4)] scale-102 z-10'
                  : isDone
                  ? 'bg-slate-900/90 border-slate-700/80 text-slate-200'
                  : 'bg-slate-950/40 border-slate-800/50 text-slate-600 opacity-50'
              }`}
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-mono font-semibold text-slate-500">
                    0{idx + 1}
                  </span>
                  <Icon
                    className={`w-4 h-4 ${
                      isCurrent
                        ? 'text-cyan-300 animate-bounce'
                        : isDone
                        ? 'text-cyan-400'
                        : 'text-slate-600'
                    }`}
                  />
                </div>
                <div className={`text-xs font-bold leading-snug ${isDone ? 'text-slate-100' : 'text-slate-500'}`}>
                  {step.name}
                </div>
              </div>

              <div className="mt-2 text-[10px] text-slate-400 leading-tight">
                {stageOutput ? (
                  <span className="text-cyan-300 font-mono font-medium block truncate" title={stageOutput.output_summary}>
                    {stageOutput.output_summary}
                  </span>
                ) : (
                  <span className="text-slate-500 line-clamp-2">{step.desc}</span>
                )}
              </div>

              {/* Progress Particle Bar at bottom */}
              <div className="w-full bg-slate-800 h-1 rounded-full mt-3 overflow-hidden">
                <div
                  className={`h-full transition-all duration-300 ${
                    isDone ? 'bg-cyan-400 w-full' : 'w-0'
                  }`}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
