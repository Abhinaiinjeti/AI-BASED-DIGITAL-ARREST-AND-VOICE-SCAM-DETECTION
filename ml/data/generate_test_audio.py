"""
Audio Test Utility
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Creates sample test audio files in data/sample_audio/ to test audio validation
and speech recognition pipeline.
"""

import math
import wave
import struct
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SAMPLE_AUDIO_DIR = BASE_DIR / "data" / "sample_audio"


def generate_sample_wav(filename: str = "test_tone.wav", duration_sec: float = 3.0):
    """Generate a clean mono 16-bit 16kHz PCM WAV file."""
    SAMPLE_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    out_path = SAMPLE_AUDIO_DIR / filename

    sample_rate = 16000
    num_samples = int(sample_rate * duration_sec)
    frequency = 440.0  # 440 Hz A tone

    with wave.open(str(out_path), "wb") as wav:
        wav.setnchannels(1)  # Mono
        wav.setsampwidth(2)  # 16-bit
        wav.setframerate(sample_rate)

        for i in range(num_samples):
            # Sine wave with gentle decay
            decay = 1.0 - (i / num_samples) * 0.2
            val = int(32767.0 * 0.3 * decay * math.sin(2.0 * math.pi * frequency * (i / sample_rate)))
            wav.writeframes(struct.pack("<h", val))

    print(f"[+] Created test WAV file: {out_path} ({duration_sec}s, {sample_rate}Hz)")
    return out_path


if __name__ == "__main__":
    generate_sample_wav()
