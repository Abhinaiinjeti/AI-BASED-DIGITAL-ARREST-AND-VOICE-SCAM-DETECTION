import React, { useState } from 'react';
import { 
  Mic, 
  Send, 
  RotateCcw, 
  FileAudio, 
  Globe2, 
  AlertCircle, 
  Volume2, 
  Quote,
  CheckCircle2
} from 'lucide-react';
import AudioRecorder from '../components/AudioRecorder';
import PipelineAnimation from '../components/PipelineAnimation';
import ResultView from '../components/ResultView';
import { analyzeAudio } from '../api/client';

export default function VoiceAnalysis() {
  const [selectedAudioBlob, setSelectedAudioBlob] = useState(null);
  const [selectedFileName, setSelectedFileName] = useState('');
  const [selectedLanguage, setSelectedLanguage] = useState('auto');
  const [isProcessing, setIsProcessing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMsg, setErrorMsg] = useState('');

  const handleAudioReady = (blob, fileName) => {
    setSelectedAudioBlob(blob);
    setSelectedFileName(fileName);
    setAnalysisResult(null);
    setErrorMsg('');
  };

  const handleAnalyze = async () => {
    if (!selectedAudioBlob) {
      setErrorMsg('Please record or upload an audio file first.');
      return;
    }

    setErrorMsg('');
    setIsProcessing(true);
    setAnalysisResult(null);

    try {
      const res = await analyzeAudio(selectedAudioBlob, selectedFileName, selectedLanguage);
      setTimeout(() => {
        setAnalysisResult(res);
        setIsProcessing(false);
      }, 700);
    } catch (err) {
      setErrorMsg(err.message || 'Speech recognition analysis failed.');
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setSelectedAudioBlob(null);
    setSelectedFileName('');
    setAnalysisResult(null);
    setErrorMsg('');
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800/80 pb-6">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 font-mono text-xs font-bold uppercase tracking-wider">
            <Mic className="w-4 h-4" />
            <span>SPEECH-TO-TEXT & AUDIO PIPELINE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-100 mt-1">
            Voice & Call Recording Scam Analysis
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Analyze suspicious extortion phone calls or voice messages using Faster-Whisper speech-to-text and downstream NLP classification.
          </p>
        </div>

        {/* Language Override */}
        <div className="flex items-center space-x-2 bg-slate-900/90 p-2 rounded-xl border border-slate-800 text-xs">
          <Globe2 className="w-4 h-4 text-cyan-400 shrink-0" />
          <span className="text-slate-400 font-mono text-[11px]">SPEECH LANG:</span>
          <select
            value={selectedLanguage}
            onChange={(e) => setSelectedLanguage(e.target.value)}
            className="bg-slate-950 border border-slate-700/80 rounded-lg px-2.5 py-1 text-slate-200 text-xs focus:outline-none focus:border-cyan-500"
          >
            <option value="auto">Auto-Detect Speech</option>
            <option value="en">English</option>
            <option value="hi">Hindi</option>
            <option value="te">Telugu</option>
          </select>
        </div>
      </div>

      {/* Audio Recorder & Upload Studio */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-5">
        
        {errorMsg && (
          <div className="p-3 rounded-xl bg-rose-950/70 border border-rose-500/50 flex items-center space-x-2 text-rose-300 text-xs">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        <AudioRecorder
          onAudioReady={handleAudioReady}
          disabled={isProcessing}
        />

        {/* Action Button Bar */}
        <div className="flex items-center justify-between pt-2 border-t border-slate-800/80">
          <button
            onClick={handleReset}
            disabled={!selectedAudioBlob && !analysisResult}
            className="px-4 py-2 rounded-xl text-xs font-medium text-slate-400 hover:text-slate-200 hover:bg-slate-800/60 disabled:opacity-30 disabled:pointer-events-none transition-colors flex items-center space-x-1.5"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset Audio</span>
          </button>

          <button
            onClick={handleAnalyze}
            disabled={isProcessing || !selectedAudioBlob}
            className="px-7 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-teal-500 hover:from-cyan-400 hover:to-teal-400 text-slate-950 font-bold text-xs tracking-wider uppercase flex items-center space-x-2 shadow-[0_0_20px_rgba(6,182,212,0.3)] disabled:opacity-40 disabled:pointer-events-none transition-all"
          >
            {isProcessing ? (
              <>
                <span className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin"></span>
                <span>Transcribing & Analyzing...</span>
              </>
            ) : (
              <>
                <Send className="w-4 h-4" />
                <span>ANALYZE VOICE RECORDING</span>
              </>
            )}
          </button>
        </div>

      </div>

      {/* Visual Pipeline Animation */}
      {(isProcessing || analysisResult) && (
        <PipelineAnimation
          isProcessing={isProcessing}
          stages={analysisResult?.pipeline_stages || []}
          inputType="voice"
        />
      )}

      {/* Audio Transcript Card */}
      {analysisResult?.transcript && (
        <div className="p-6 rounded-2xl glass-panel border border-cyan-500/30 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
              <Quote className="w-4 h-4" />
              <span>Transcribed Speech Output (Whisper)</span>
            </span>
            <span className="text-[11px] font-mono text-slate-400">
              Duration: {analysisResult.audio_duration ? `${analysisResult.audio_duration}s` : 'N/A'}
            </span>
          </div>
          <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 font-mono text-xs text-slate-200 leading-relaxed">
            "{analysisResult.transcript}"
          </div>
        </div>
      )}

      {/* Result Section */}
      {analysisResult && (
        <ResultView
          result={analysisResult}
          onReset={handleReset}
        />
      )}

    </div>
  );
}
