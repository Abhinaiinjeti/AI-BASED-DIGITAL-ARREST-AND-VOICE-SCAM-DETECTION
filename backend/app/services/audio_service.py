"""
Audio Transcription & Preprocessing Pipeline
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Pipeline:
Uploaded Audio (OGG/Opus, MP3, WAV, M4A, WebM, AAC, FLAC)
       ↓
Validate file (size, format, existence)
       ↓
FFmpeg audio conversion & normalization
       ↓
16 kHz Mono 16-bit PCM WAV
       ↓
Faster-Whisper (base, CPU int8, automatic language detection)
       ↓
Cleaned Transcript & Audio Diagnostics
       ↓
Downstream NLP / ML Classifier & Risk Engine
"""

import os
import re
import sys
import wave
import shutil
import tempfile
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np

# Configure structured logging
logger = logging.getLogger("voice_pipeline")
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s", datefmt="%H:%M:%S"))
    logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Faster-Whisper lazy singleton
_whisper_model = None

# Human-readable language map for Whisper language codes
WHISPER_LANGUAGES = {
    "en": "English",
    "hi": "Hindi",
    "te": "Telugu",
    "ta": "Tamil",
    "bn": "Bengali",
    "mr": "Marathi",
    "gu": "Gujarati",
    "kn": "Kannada",
    "ml": "Malayalam",
    "pa": "Punjabi",
    "ur": "Urdu",
    "or": "Odia",
    "as": "Assamese",
}


def get_ffmpeg_path() -> Optional[str]:
    """
    Locate the FFmpeg binary using:
    1. Explicit environment variables (FFMPEG_BINARY, FFMPEG_PATH)
    2. imageio-ffmpeg bundled binary
    3. System PATH
    """
    for env_var in ("FFMPEG_BINARY", "FFMPEG_PATH"):
        val = os.environ.get(env_var)
        if val and Path(val).exists():
            return str(Path(val).resolve())

    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and Path(exe).exists():
            return str(Path(exe).resolve())
    except Exception:
        pass

    sys_ffmpeg = shutil.which("ffmpeg")
    if sys_ffmpeg:
        return sys_ffmpeg

    return None


def get_audio_metadata(ffmpeg_exe: str, file_path: Path) -> Dict[str, Any]:
    """
    Extract format, duration, sample rate, channels, and size using FFmpeg probe.
    """
    size_bytes = file_path.stat().st_size if file_path.exists() else 0
    ext = file_path.suffix.lower().replace(".", "").upper()

    metadata = {
        "filename": file_path.name,
        "format": ext,
        "codec": ext,
        "duration": 0.0,
        "sample_rate": 0,
        "channels": 1,
        "size_bytes": size_bytes,
    }

    try:
        cmd = [ffmpeg_exe, "-hide_banner", "-i", str(file_path)]
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        err = proc.stderr or ""

        # Duration: HH:MM:SS.ss
        dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", err)
        if dur_match:
            h, m, s = dur_match.groups()
            metadata["duration"] = round(int(h) * 3600 + int(m) * 60 + float(s), 2)

        # Stream Audio: codec, sample_rate, channels
        stream_match = re.search(r"Stream.*Audio:\s*([^,\s]+).*?,\s*(\d{4,6})\s*Hz,\s*([^,\s]+)", err)
        if stream_match:
            codec, sr, ch_str = stream_match.groups()
            metadata["codec"] = codec.upper()
            metadata["format"] = f"{ext} / {codec.upper()}"
            metadata["sample_rate"] = int(sr)
            if "mono" in ch_str.lower():
                metadata["channels"] = 1
            elif "stereo" in ch_str.lower():
                metadata["channels"] = 2
            else:
                m_ch = re.search(r"(\d+)", ch_str)
                metadata["channels"] = int(m_ch.group(1)) if m_ch else 1
    except Exception as e:
        logger.warning(f"[VOICE] Metadata probe exception: {e}")

    return metadata


def convert_to_pcm_wav(input_path: Path, output_wav_path: Optional[Path] = None) -> Path:
    """
    Robustly convert any audio file (OGG/Opus, MP3, M4A, WebM, etc.) to
    standard 16 kHz Mono 16-bit PCM WAV using FFmpeg.
    """
    ffmpeg_exe = get_ffmpeg_path()
    if not ffmpeg_exe:
        raise RuntimeError(
            "FFmpeg executable not found. FFmpeg is required to decode and normalize audio files to 16 kHz PCM WAV."
        )

    if output_wav_path is None:
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp.close()
        output_wav_path = Path(tmp.name)

    cmd = [
        ffmpeg_exe,
        "-y",
        "-i", str(input_path),
        "-ar", "16000",
        "-ac", "1",
        "-c:a", "pcm_s16le",
        str(output_wav_path)
    ]

    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except subprocess.CalledProcessError as e:
        err_msg = e.stderr.decode("utf-8", errors="replace") if e.stderr else str(e)
        logger.error(f"[VOICE] FFmpeg error: {err_msg}")
        raise RuntimeError(f"FFmpeg conversion failed: {err_msg[:300]}")

    if not output_wav_path.exists() or output_wav_path.stat().st_size == 0:
        raise RuntimeError("FFmpeg completed but generated an empty or non-existent WAV file.")

    return output_wav_path


def check_audio_energy(wav_path: Path, rms_threshold: float = 0.001) -> float:
    """
    Calculate audio RMS energy to distinguish actual audio/speech from pure silence.
    Returns RMS value between 0.0 and 1.0.
    """
    try:
        with wave.open(str(wav_path), "rb") as wf:
            frames = wf.readframes(wf.getnframes())
            if not frames:
                return 0.0
            samples = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
            if len(samples) == 0:
                return 0.0
            return float(np.sqrt(np.mean(samples**2)))
    except Exception:
        return 0.05  # Default to non-zero if calculation fails


class AudioService:
    ALLOWED_EXTENSIONS = {".ogg", ".opus", ".mp3", ".wav", ".m4a", ".webm", ".aac", ".flac", ".mp4"}
    MAX_FILE_SIZE_BYTES = 25 * 1024 * 1024  # 25 MB
    MAX_DURATION_SECONDS = 600  # 10 minutes

    def __init__(self, model_size: Optional[str] = None):
        self.model_size = model_size or os.environ.get("WHISPER_MODEL_SIZE", "base")

    def _get_whisper_model(self):
        """Lazily initialize and return the cached WhisperModel singleton."""
        global _whisper_model
        if _whisper_model is None:
            logger.info(f"[VOICE] Initializing Faster-Whisper model ('{self.model_size}', device='cpu', compute_type='int8')...")
            from faster_whisper import WhisperModel
            _whisper_model = WhisperModel(self.model_size, device="cpu", compute_type="int8")
            logger.info("[VOICE] Faster-Whisper model loaded successfully.")
        return _whisper_model

    def validate_audio_file(self, file_path: Path) -> Dict[str, Any]:
        """Validate audio file existence, format, and size."""
        if not file_path.exists():
            return {
                "valid": False,
                "error_type": "file_not_found",
                "error": f"Audio file not found: {file_path.name}",
            }

        ext = file_path.suffix.lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            allowed_list = ", ".join(sorted(self.ALLOWED_EXTENSIONS))
            return {
                "valid": False,
                "error_type": "unsupported_format",
                "error": f"Unsupported audio format '{ext}'. Supported formats: {allowed_list}",
            }

        size = file_path.stat().st_size
        if size == 0:
            return {
                "valid": False,
                "error_type": "empty_file",
                "error": "Uploaded audio file is empty (0 bytes).",
            }

        if size > self.MAX_FILE_SIZE_BYTES:
            return {
                "valid": False,
                "error_type": "file_too_large",
                "error": f"File size ({size / (1024 * 1024):.1f}MB) exceeds limit of 25MB.",
            }

        return {"valid": True, "format": ext.replace(".", "")}

    def transcribe(self, file_path: Path, language: Optional[str] = None) -> Dict[str, Any]:
        """
        Full Audio Processing Pipeline:
        1. Validation
        2. FFmpeg availability check
        3. Audio metadata probe & logging
        4. FFmpeg conversion to 16 kHz Mono 16-bit PCM WAV
        5. Silence / RMS check
        6. Faster-Whisper transcription with automatic or targeted language detection
        7. Segment concatenation & diagnostics extraction
        """
        # Step 1: Validation
        validation = self.validate_audio_file(file_path)
        if not validation["valid"]:
            return {
                "success": False,
                "error_type": validation["error_type"],
                "error": validation["error"],
                "transcript": "",
                "duration": 0.0,
            }

        # Step 2: FFmpeg Check
        ffmpeg_exe = get_ffmpeg_path()
        if not ffmpeg_exe:
            logger.error("[VOICE] FFmpeg binary not found on host system.")
            return {
                "success": False,
                "error_type": "ffmpeg_missing",
                "error": (
                    "FFmpeg is not installed or could not be located on the server. "
                    "FFmpeg is required to decode and normalize audio files (such as WhatsApp OGG/Opus and MP3). "
                    "Please ensure FFmpeg or imageio-ffmpeg is configured."
                ),
                "transcript": "",
                "duration": 0.0,
            }

        # Step 3: Probe Audio Metadata
        meta = get_audio_metadata(ffmpeg_exe, file_path)
        duration = meta.get("duration", 0.0)
        logger.info(
            f"[VOICE] Audio received: '{file_path.name}' | "
            f"Format: {meta.get('format')} | "
            f"Size: {meta.get('size_bytes')} bytes | "
            f"Duration: {duration}s | "
            f"Sample Rate: {meta.get('sample_rate')} Hz | "
            f"Channels: {meta.get('channels')}"
        )

        if duration > self.MAX_DURATION_SECONDS:
            return {
                "success": False,
                "error_type": "duration_exceeded",
                "error": f"Audio duration ({duration:.1f}s) exceeds the maximum limit of {self.MAX_DURATION_SECONDS}s.",
                "transcript": "",
                "duration": duration,
            }

        # Step 4: FFmpeg Conversion to 16kHz mono PCM WAV
        converted_wav: Optional[Path] = None
        try:
            logger.info(f"[VOICE] Converting audio to normalized 16 kHz Mono PCM WAV...")
            converted_wav = convert_to_pcm_wav(file_path)
            logger.info(f"[VOICE] Converted successfully: '{converted_wav.name}' ({converted_wav.stat().st_size} bytes)")

            # Step 5: Check audio energy / silence
            rms = check_audio_energy(converted_wav)
            logger.info(f"[VOICE] Audio RMS energy: {rms:.5f}")
            if rms < 0.0005:
                logger.warning("[VOICE] Audio RMS is near zero (silent audio detected).")
                return {
                    "success": False,
                    "error_type": "no_speech",
                    "error": "No speech detected in the audio file. The recording appears to be silent or contains no audible sound.",
                    "transcript": "",
                    "duration": duration,
                    "diagnostics": {
                        "filename": file_path.name,
                        "format": meta.get("format", file_path.suffix.upper()),
                        "duration": duration,
                        "sample_rate": meta.get("sample_rate", 0),
                        "channels": meta.get("channels", 1),
                        "converted_sample_rate": 16000,
                        "converted_channels": 1,
                        "speech_detected": False,
                        "detected_language": "None",
                        "detected_language_code": "none",
                        "language_confidence": 0.0,
                    },
                }

            # Step 6: Faster-Whisper Model & Transcription
            try:
                model = self._get_whisper_model()
            except Exception as e:
                logger.error(f"[VOICE] Failed to initialize Faster-Whisper model: {e}")
                return {
                    "success": False,
                    "error_type": "model_error",
                    "error": f"Speech recognition model failed to initialize: {str(e)}",
                    "transcript": "",
                    "duration": duration,
                }

            # Determine Whisper language argument
            whisper_lang = None
            if language and language.strip() and language.strip().lower() != "auto":
                whisper_lang = language.strip().lower()

            logger.info(f"[VOICE] Starting Faster-Whisper transcription (language override: {whisper_lang or 'auto'})...")
            
            segments, info = model.transcribe(
                str(converted_wav),
                beam_size=5,
                language=whisper_lang,
                vad_filter=False,  # Whisper native silence thresholds
            )

            # Step 7: Combine all segments
            segment_texts = []
            for seg in segments:
                t = seg.text.strip()
                if t:
                    segment_texts.append(t)

            transcript = " ".join(segment_texts).strip()

            detected_code = info.language if info and info.language else "en"
            detected_prob = round(float(info.language_probability), 4) if info and info.language_probability else 0.0
            detected_lang_name = WHISPER_LANGUAGES.get(detected_code, detected_code.title())

            logger.info(
                f"[VOICE] Faster-Whisper completed | "
                f"Detected language: {detected_lang_name} ({detected_code}, p={detected_prob:.2f}) | "
                f"Transcript length: {len(transcript)} chars | "
                f"Preview: '{transcript[:60]}...'"
            )

            # Step 8: Distinguish silence / no speech from failure
            if not transcript:
                logger.warning("[VOICE] Transcription produced 0 speech segments.")
                return {
                    "success": False,
                    "error_type": "no_speech",
                    "error": "No speech detected in the audio file. Please ensure the recording is clear and audible.",
                    "transcript": "",
                    "duration": duration or round(info.duration, 2),
                    "diagnostics": {
                        "filename": file_path.name,
                        "format": meta.get("format", file_path.suffix.upper()),
                        "duration": duration or round(info.duration, 2),
                        "sample_rate": meta.get("sample_rate", 0),
                        "channels": meta.get("channels", 1),
                        "converted_sample_rate": 16000,
                        "converted_channels": 1,
                        "speech_detected": False,
                        "detected_language": detected_lang_name,
                        "detected_language_code": detected_code,
                        "language_confidence": detected_prob,
                    },
                }

            # Final success response
            final_duration = round(duration if duration > 0 else (info.duration if info else 0.0), 2)
            diagnostics_data = {
                "filename": file_path.name,
                "format": meta.get("format", file_path.suffix.upper()),
                "duration": final_duration,
                "sample_rate": meta.get("sample_rate", 0),
                "channels": meta.get("channels", 1),
                "converted_sample_rate": 16000,
                "converted_channels": 1,
                "speech_detected": True,
                "detected_language": detected_lang_name,
                "detected_language_code": detected_code,
                "language_confidence": detected_prob,
            }

            return {
                "success": True,
                "transcript": transcript,
                "duration": final_duration,
                "detected_language": detected_lang_name,
                "detected_language_code": detected_code,
                "language_confidence": detected_prob,
                "speech_detected": True,
                "audio_format": meta.get("format", file_path.suffix.upper()),
                "diagnostics": diagnostics_data,
            }

        except Exception as e:
            logger.error(f"[VOICE] Transcription pipeline failure: {e}", exc_info=True)
            return {
                "success": False,
                "error_type": "transcription_error",
                "error": f"Audio processing or transcription failed: {str(e)}",
                "transcript": "",
                "duration": duration,
            }
        finally:
            # Ensure temporary converted WAV is safely removed
            if converted_wav and converted_wav.exists():
                try:
                    converted_wav.unlink()
                    logger.debug(f"[VOICE] Cleaned up temporary converted WAV: {converted_wav.name}")
                except Exception as e:
                    logger.warning(f"[VOICE] Could not remove temp WAV: {e}")


# Singleton instance
audio_service = AudioService(model_size="base")
