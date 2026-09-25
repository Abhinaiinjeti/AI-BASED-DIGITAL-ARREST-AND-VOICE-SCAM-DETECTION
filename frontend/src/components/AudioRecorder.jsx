import React, { useState, useRef, useEffect } from 'react';
import { Mic, Square, Play, Pause, UploadCloud, RotateCcw, Volume2, AlertCircle } from 'lucide-react';

export default function AudioRecorder({ onAudioReady, disabled = false }) {
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  const [audioUrl, setAudioUrl] = useState(null);
  const [audioBlob, setAudioBlob] = useState(null);
  const [fileName, setFileName] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);
  const audioPlayerRef = useRef(null);
  const fileInputRef = useRef(null);

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
      if (audioUrl) URL.revokeObjectURL(audioUrl);
    };
  }, [audioUrl]);

  // Start Live Recording
  const startRecording = async () => {
    setErrorMsg('');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      audioChunksRef.current = [];
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(audioChunksRef.current, { type: 'audio/wav' });
        const url = URL.createObjectURL(blob);
        setAudioBlob(blob);
        setAudioUrl(url);
        setFileName(`mic_recording_${Date.now()}.wav`);
        onAudioReady(blob, `mic_recording_${Date.now()}.wav`);

        // Stop all audio tracks
        stream.getTracks().forEach((track) => track.stop());
      };

      mediaRecorder.start(200); // 200ms chunk slices
      setIsRecording(true);
      setRecordingDuration(0);

      timerRef.current = setInterval(() => {
        setRecordingDuration((prev) => prev + 1);
      }, 1000);
    } catch (err) {
      setErrorMsg('Microphone access denied or unsupported browser. Please upload an audio file instead.');
    }
  };

  // Stop Live Recording
  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
      if (timerRef.current) clearInterval(timerRef.current);
    }
  };

  // Handle File Upload Drop / Selection
  const handleFileChange = (e) => {
    setErrorMsg('');
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.match(/\.(wav|mp3|m4a|ogg|opus|webm|aac|flac)$/i)) {
      setErrorMsg('Unsupported format. Supported: WAV, MP3, M4A, OGG, OPUS, WebM, AAC, FLAC.');
      return;
    }

    if (file.size > 25 * 1024 * 1024) {
      setErrorMsg('File exceeds 25 MB limit.');
      return;
    }

    const url = URL.createObjectURL(file);
    setAudioBlob(file);
    setAudioUrl(url);
    setFileName(file.name);
    setRecordingDuration(0);
    onAudioReady(file, file.name);
  };

  const resetAudio = () => {
    if (audioUrl) URL.revokeObjectURL(audioUrl);
    setAudioBlob(null);
    setAudioUrl(null);
    setFileName('');
    setRecordingDuration(0);
    setIsPlaying(false);
    setErrorMsg('');
    onAudioReady(null, '');
  };

  const togglePlayback = () => {
    if (!audioPlayerRef.current) return;
    if (isPlaying) {
      audioPlayerRef.current.pause();
      setIsPlaying(false);
    } else {
      audioPlayerRef.current.play();
      setIsPlaying(true);
    }
  };

  const formatTime = (secs) => {
    const mins = Math.floor(secs / 60);
    const rem = secs % 60;
    return `${mins.toString().padStart(2, '0')}:${rem.toString().padStart(2, '0')}`;
  };

  return (
    <div className="w-full space-y-4">
      {/* Error notification if mic access fails */}
      {errorMsg && (
        <div className="p-3 rounded-xl bg-rose-950/60 border border-rose-500/50 flex items-center space-x-2 text-rose-300 text-xs">
          <AlertCircle className="w-4 h-4 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {/* Main Recording & Upload Container */}
      {!audioBlob ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          
          {/* Card 1: Live Microphone Recording */}
          <div className="p-6 rounded-2xl glass-panel border border-slate-800 flex flex-col items-center justify-center text-center space-y-4">
            <div className="relative">
              {isRecording && (
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 opacity-75"></span>
              )}
              <div
                className={`w-20 h-20 rounded-full flex items-center justify-center transition-all ${
                  isRecording
                    ? 'bg-rose-600 text-white shadow-[0_0_25px_rgba(225,29,72,0.6)]'
                    : 'bg-cyan-950/80 text-cyan-400 border border-cyan-500/40 hover:border-cyan-400 cursor-pointer'
                }`}
                onClick={isRecording ? stopRecording : startRecording}
              >
                {isRecording ? <Square className="w-8 h-8" /> : <Mic className="w-8 h-8" />}
              </div>
            </div>

            <div>
              <h4 className="text-sm font-bold text-slate-100">
                {isRecording ? 'Recording Live Audio...' : 'Record Voice Directly'}
              </h4>
              <p className="text-xs text-slate-400 mt-1">
                {isRecording ? 'Click square button to finish recording' : 'Click microphone icon to start recording'}
              </p>
            </div>

            {/* Live Waveform Pulse Animation */}
            {isRecording ? (
              <div className="flex items-center space-x-1.5 h-8">
                {[40, 75, 90, 60, 100, 45, 80, 65, 95, 50, 85, 30].map((h, i) => (
                  <span
                    key={i}
                    className="w-1 bg-rose-400 rounded-full animate-pulse"
                    style={{
                      height: `${h}%`,
                      animationDelay: `${(i * 0.1).toFixed(1)}s`,
                    }}
                  />
                ))}
                <span className="font-mono text-xs text-rose-400 ml-2 font-bold">
                  {formatTime(recordingDuration)}
                </span>
              </div>
            ) : (
              <div className="text-[11px] font-mono text-slate-500">
                WAV mono 16kHz compatible
              </div>
            )}
          </div>

          {/* Card 2: Audio File Upload */}
          <div
            onClick={() => fileInputRef.current?.click()}
            className="p-6 rounded-2xl glass-panel border border-dashed border-slate-700/80 hover:border-cyan-500/60 cursor-pointer flex flex-col items-center justify-center text-center space-y-3 transition-all hover:bg-slate-900/50"
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".wav,.mp3,.m4a,.ogg,.opus,.webm,.aac,.flac"
              onChange={handleFileChange}
              className="hidden"
            />
            <div className="w-16 h-16 rounded-2xl bg-slate-900 border border-slate-700/80 flex items-center justify-center text-slate-400 group-hover:text-cyan-400">
              <UploadCloud className="w-8 h-8 text-cyan-400" />
            </div>
            <div>
              <h4 className="text-sm font-bold text-slate-100">
                Upload Suspicious Audio
              </h4>
              <p className="text-xs text-slate-400 mt-1">
                Drag and drop or browse from your device
              </p>
            </div>
            <div className="text-[11px] font-mono text-slate-500">
              Supported: WhatsApp OGG/Opus, MP3, WAV, M4A, WebM (Max 25MB)
            </div>
          </div>

        </div>
      ) : (
        /* Audio Preview Card */
        <div className="p-5 rounded-2xl glass-panel border border-cyan-500/30 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <button
                onClick={togglePlayback}
                className="w-12 h-12 rounded-xl bg-cyan-600 hover:bg-cyan-500 text-white flex items-center justify-center transition-colors shadow-lg"
              >
                {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
              </button>
              <div>
                <div className="text-xs font-mono font-bold text-slate-200 truncate max-w-xs sm:max-w-md">
                  {fileName}
                </div>
                <div className="text-[11px] text-cyan-400 font-mono flex items-center gap-1.5 mt-0.5">
                  <Volume2 className="w-3.5 h-3.5" />
                  <span>Audio Ready for Speech Recognition</span>
                </div>
              </div>
            </div>

            <button
              onClick={resetAudio}
              className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs text-slate-400 hover:text-rose-400 hover:bg-slate-800/60 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          </div>

          {/* HTML5 Audio Player Element */}
          <audio
            ref={audioPlayerRef}
            src={audioUrl}
            onEnded={() => setIsPlaying(false)}
            className="w-full h-8 mt-2"
            controls
          />
        </div>
      )}
    </div>
  );
}
