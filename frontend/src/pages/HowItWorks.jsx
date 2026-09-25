import React from 'react';
import { 
  HelpCircle, 
  Mic, 
  FileText, 
  Binary, 
  Wrench, 
  BrainCircuit, 
  ShieldAlert, 
  CheckCircle2, 
  Languages, 
  Cpu, 
  Layers,
  ArrowDown
} from 'lucide-react';

export default function HowItWorks() {
  const steps = [
    {
      num: '01',
      title: 'Multimodal Input Ingestion',
      subtitle: 'Text or Voice Call Upload',
      icon: FileText,
      color: 'text-cyan-400',
      border: 'border-cyan-500/40',
      details: [
        'Accepts suspicious messages (SMS, WhatsApp, emails) or recorded audio calls (WAV, MP3, M4A, OGG).',
        'Validates audio duration, channels, sample rate, and size limits (max 25MB) to ensure processing stability.',
      ],
    },
    {
      num: '02',
      title: 'Speech-to-Text Transcription',
      subtitle: 'Powered by Faster-Whisper / Speech Engine',
      icon: Mic,
      color: 'text-teal-400',
      border: 'border-teal-500/40',
      details: [
        'Converts acoustic speech into precise conversational text transcripts.',
        'Supports Indian English, Hindi, and native Telugu dialects without requiring cloud APIs.',
        'Feeds the resulting transcript directly into the standardized text processing pipeline.',
      ],
    },
    {
      num: '03',
      title: 'Multilingual Script Identification',
      subtitle: 'Native Unicode Blocks & Hinglish Heuristics',
      icon: Languages,
      color: 'text-indigo-400',
      border: 'border-indigo-500/40',
      details: [
        'Analyzes script character ranges: Telugu (\\u0C00-\\u0C7F), Devanagari (\\u0900-\\u097F), and Latin scripts.',
        'Identifies Hinglish using conversational phonetic dictionaries (e.g., "aapka", "kijiye", "giraftaar", "paisa").',
        'Displays "Language uncertain" if detection confidence is below statistical threshold.',
      ],
    },
    {
      num: '04',
      title: 'Domain-Preserving Text Preprocessing',
      subtitle: 'Safeguards Coercive & Security Vocabulary',
      icon: Wrench,
      color: 'text-amber-400',
      border: 'border-amber-500/40',
      details: [
        'Standard NLP cleaners often remove punctuation and stopwords, erasing crucial scam markers.',
        'Our pipeline strictly PRESERVES domain indicators: police, CBI, ED, arrest, OTP, UPI, warrant, FIR, narcotics, Aadhaar, customs.',
        'Normalizes phone numbers to <PHONE>, URLs to <URL>, and currency amounts to <AMOUNT>.',
      ],
    },
    {
      num: '05',
      title: 'TF-IDF Statistical Feature Extraction',
      subtitle: 'Unigram and Bigram Feature Matrix',
      icon: Binary,
      color: 'text-purple-400',
      border: 'border-purple-500/40',
      details: [
        'Extracts sublinear term frequencies and inverse document frequencies across 12,000 vocabulary features.',
        'Captures compound word pairings like "digital arrest", "police warrant", "kyc expire", and "transfer money".',
        'Fitted strictly on the training partition (70%) to avoid any data leakage into validation or testing.',
      ],
    },
    {
      num: '06',
      title: 'Machine Learning Classification',
      subtitle: 'Evaluated: Logistic Regression, Naive Bayes, Linear SVM',
      icon: BrainCircuit,
      color: 'text-pink-400',
      border: 'border-pink-500/40',
      details: [
        'Three distinct supervised classifiers were trained and benchmarked on verified Indic datasets.',
        'Logistic Regression was selected based on validation Macro F1 score.',
        'Outputs calibrated probability confidence and predicts the specific scam category.',
      ],
    },
    {
      num: '07',
      title: 'Digital Arrest Indicator & Risk Engine',
      subtitle: 'Rule-Based Coercion Analysis + Composite Scoring',
      icon: ShieldAlert,
      color: 'text-rose-400',
      border: 'border-rose-500/40',
      details: [
        'Scans for the 6 core pillars of Digital Arrest: Authority Impersonation, Legal Threats, Video Isolation, Fabricated Charges, Financial Extortion, and Urgency.',
        'Synthesizes an integrated Risk Score (0 - 100) distinct from ML statistical confidence.',
        'Generates contextual emergency advisories directing users to National Cybercrime Helpline 1930.',
      ],
    },
  ];

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-12">
      
      {/* Header */}
      <div className="text-center space-y-3 max-w-3xl mx-auto">
        <div className="inline-flex items-center space-x-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider">
          <HelpCircle className="w-4 h-4" />
          <span>TECHNICAL ARCHITECTURE & METHODOLOGY</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-slate-100">
          How the Detection Engine Works
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 leading-relaxed">
          A step-by-step walkthrough of how audio recordings and text conversations travel through 
          our 7-stage AI risk analysis pipeline.
        </p>
      </div>

      {/* Sequential Steps Cards */}
      <div className="space-y-6 relative">
        {steps.map((step, idx) => {
          const Icon = step.icon;
          return (
            <div
              key={step.num}
              className="p-6 rounded-2xl glass-panel border border-slate-800 space-y-3 relative hover:border-slate-700 transition-all"
            >
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-800/80 pb-3">
                <div className="flex items-center space-x-3">
                  <span className="font-mono text-xs font-bold px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-700/80 text-cyan-400">
                    STAGE {step.num}
                  </span>
                  <h3 className="text-base font-bold text-slate-100 flex items-center gap-2">
                    <Icon className={`w-4 h-4 ${step.color}`} />
                    <span>{step.title}</span>
                  </h3>
                </div>
                <span className="text-xs font-mono text-slate-400">
                  {step.subtitle}
                </span>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 pt-2 text-xs text-slate-300">
                {step.details.map((point, pIdx) => (
                  <div key={pIdx} className="flex items-start space-x-2 bg-slate-950/60 p-3 rounded-xl border border-slate-850">
                    <CheckCircle2 className="w-3.5 h-3.5 text-cyan-400 shrink-0 mt-0.5" />
                    <span className="leading-relaxed">{point}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
