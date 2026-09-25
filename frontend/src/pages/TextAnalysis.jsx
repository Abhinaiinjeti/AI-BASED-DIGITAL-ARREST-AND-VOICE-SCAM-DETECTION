import React, { useState, useEffect } from 'react';
import { 
  FileText, 
  Send, 
  RotateCcw, 
  Sparkles, 
  Globe2, 
  AlertCircle, 
  ChevronRight,
  ShieldAlert
} from 'lucide-react';
import { analyzeText, fetchDemos } from '../api/client';
import PipelineAnimation from '../components/PipelineAnimation';
import ResultView from '../components/ResultView';

export default function TextAnalysis() {
  const [inputText, setInputText] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [isProcessing, setIsProcessing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [demoPresets, setDemoPresets] = useState([]);

  // Fetch demo presets on load
  useEffect(() => {
    fetchDemos()
      .then((demos) => setDemoPresets(demos))
      .catch(() => {});
  }, []);

  const wordCount = inputText.trim() ? inputText.trim().split(/\s+/).length : 0;
  const charCount = inputText.length;

  const handleAnalyze = async () => {
    if (!inputText.trim()) {
      setErrorMsg('Please enter or paste a message to analyze.');
      return;
    }
    setErrorMsg('');
    setIsProcessing(true);
    setAnalysisResult(null);

    try {
      const res = await analyzeText(inputText, selectedLanguage);
      // Brief aesthetic pause to show pipeline stages
      setTimeout(() => {
        setAnalysisResult(res);
        setIsProcessing(false);
      }, 700);
    } catch (err) {
      setErrorMsg(err.message || 'Analysis failed. Please verify that the backend is running.');
      setIsProcessing(false);
    }
  };

  const handleClear = () => {
    setInputText('');
    setAnalysisResult(null);
    setErrorMsg('');
  };

  const handleLoadDemo = (demo) => {
    setInputText(demo.text);
    setSelectedLanguage('auto');
    setAnalysisResult(null);
    setErrorMsg('');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider">
            <FileText className="w-4 h-4" />
            <span>NLP & INDIC LINGUISTIC PIPELINE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-100 mt-1">
            Suspicious Text & Conversation Analysis
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Analyze suspicious messages, SMS, WhatsApp chats, or extortion call transcripts in English, Hindi/Hinglish, and Telugu.
          </p>
        </div>

        {/* Language Selector */}
        <div className="flex items-center space-x-2 bg-slate-900/90 p-2 rounded-xl border border-slate-800 text-xs">
          <Globe2 className="w-4 h-4 text-cyan-400 shrink-0" />
          <span className="text-slate-400 font-mono text-[11px]">LANGUAGE:</span>
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="bg-slate-950 border border-slate-700/80 rounded-lg px-2.5 py-1 text-slate-200 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="auto">Auto-Detect Script</option>
            <option value="English">English</option>
            <option value="Hindi">Hindi (Devanagari)</option>
            <option value="Hinglish">Hinglish (Roman Script)</option>
            <option value="Telugu">Telugu (Native Script)</option>
          </select>
        </div>
      </div>

      {/* Demo Presets Palette */}
      {demoPresets.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs font-mono text-slate-400">
            <span className="flex items-center gap-1.5 font-bold text-cyan-400 uppercase tracking-wider text-[11px]">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Verified Demo Presets (Clearly Labeled Demo Examples)</span>
            </span>
            <span className="text-[10px] text-slate-500">
              Click any scenario to populate the input
            </span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-2.5">
            {demoPresets.map((demo) => (
              <button
                key={demo.id}
                onClick={() => handleLoadDemo(demo)}
                className="p-3 rounded-xl glass-panel border border-slate-800 hover:border-cyan-500/50 text-left transition-all hover:bg-slate-900/70 group"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className={`text-[10px] font-mono font-bold px-1.5 py-0.5 rounded ${
                    demo.expected_risk === 'VERY HIGH'
                      ? 'bg-rose-950 text-rose-300 border border-rose-800/80'
                      : demo.expected_risk === 'HIGH'
                      ? 'bg-orange-950 text-orange-300 border border-orange-800/80'
                      : 'bg-emerald-950 text-emerald-300 border border-emerald-800/80'
                  }`}>
                    {demo.expected_risk}
                  </span>
                  <span className="text-[10px] font-mono text-slate-400">
                    {demo.language}
                  </span>
                </div>
                <div className="text-xs font-bold text-slate-200 group-hover:text-cyan-300 transition-colors truncate">
                  {demo.title}
                </div>
                <div className="text-[11px] text-slate-500 line-clamp-2 mt-1 leading-snug">
                  {demo.description}
                </div>
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Main Text Input Studio */}
      <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
        
        {/* Error Alert */}
        {errorMsg && (
          <div className="p-3 rounded-xl bg-rose-950/70 border border-rose-500/50 flex items-center space-x-2 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <div className="relative">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            placeholder="Paste suspicious conversation transcript, message, or cyber extortion threat here... (e.g. 'DCP Kumar here from CBI. You are under digital arrest. Transfer 50000 rupees immediately...')"
            rows={7}
            className="w-full bg-slate-950/90 text-slate-100 rounded-xl p-4 border border-slate-700/80 focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 text-sm leading-relaxed placeholder:text-slate-600 focus:outline-none transition-all font-mono"
          />

          {/* Word and Character Count bar */}
          <div className="flex items-center justify-between text-[11px] font-mono text-slate-400 px-1 pt-1">
            <span>
              Words: <strong className="text-slate-200">{wordCount}</strong> | Characters: <strong className="text-slate-200">{charCount}</strong>
            </span>
            <span className="text-slate-500">
              Unicode NFC normalized • Domain token preservation active
            </span>
          </div>
        </div>

        {/* Buttons Action Bar */}
        <div className="flex items-center justify-between pt-2">
          <button
            onClick={handleClear}
            disabled={!inputText && !analysisResult}
            className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 disabled:opacity-30 disabled:pointer-events-none transition-colors flex items-center space-x-1.5"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Clear Input</span>
          </button>

          <button
            onClick={handleAnalyze}
            disabled={isProcessing || !inputText.trim()}
            className="px-7 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold text-xs tracking-wider uppercase flex items-center space-x-2 shadow-[0_0_20px_rgba(6,182,212,0.3)] disabled:opacity-40 disabled:pointer-events-none transition-all"
          >
            {isProcessing ? (
              <>
                <span className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></span>
                <span>Executing Pipeline...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>ANALYZE MESSAGE</span>
              </>
            )}
          </button>
        </div>

      </div>

      {/* Visual Processing Pipeline Animation */}
      {(isProcessing || analysisResult) && (
        <PipelineAnimation
          isProcessing={isProcessing}
          stages={analysisResult?.pipeline_stages || []}
          inputType="text"
        />
      )}

      {/* Result Display Section */}
      {analysisResult && (
        <ResultView
          result={analysisResult}
          onReset={handleClear}
        />
      )}

    </div>
  );
}
