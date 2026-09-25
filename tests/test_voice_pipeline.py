"""
Automated Verification Suite: Voice Analysis & Speech-to-Text Pipeline
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Tests 4 scenarios:
1. WhatsApp Voice Note (.ogg / Opus) -> Extortion Scam
2. Call Recording (.mp3) -> Extortion Scam
3. Uncompressed Audio (.wav) -> Extortion Scam
4. Silent Audio (.wav) -> No speech detected (HTTP 422)
"""

import sys
import json
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

test_files = [
    {
        "name": "WhatsApp OGG Recording (Extortion Scam)",
        "path": BASE_DIR / "data" / "sample_audio" / "WhatsApp_Ptt_test.ogg",
        "expected_speech": True,
        "expected_classification": "Scam",
    },
    {
        "name": "MP3 Recording (Extortion Scam)",
        "path": BASE_DIR / "data" / "sample_audio" / "digital_arrest_sample.mp3",
        "expected_speech": True,
        "expected_classification": "Scam",
    },
    {
        "name": "WAV Recording (Extortion Scam)",
        "path": BASE_DIR / "data" / "sample_audio" / "digital_arrest_sample.wav",
        "expected_speech": True,
        "expected_classification": "Scam",
    },
    {
        "name": "Silent Audio (No Speech)",
        "path": BASE_DIR / "data" / "sample_audio" / "pure_silence.wav",
        "expected_speech": False,
        "expected_classification": None,
    },
]


def run_tests():
    print("=================================================================")
    print("RUNNING COMPREHENSIVE VOICE PIPELINE TEST")
    print("=================================================================\n")

    all_passed = True

    for t in test_files:
        p = t["path"]
        print(f"--- Testing: {t['name']} ---")
        print(f"File: {p.name} (exists: {p.exists()}, size: {p.stat().st_size if p.exists() else 0} bytes)")

        if not p.exists():
            print(f"ERROR: File not found: {p}")
            all_passed = False
            continue

        with open(p, "rb") as f:
            response = client.post(
                "/api/analyze/audio",
                files={"file": (p.name, f, "application/octet-stream")},
                data={"language": "auto"},
            )

        print(f"HTTP Status: {response.status_code}")

        if t["expected_speech"]:
            if response.status_code != 200:
                print(f"FAILED: Expected 200 OK, got {response.status_code}: {response.text}")
                all_passed = False
                continue
            data = response.json()
            print("Success:", data.get("success"))
            print("Audio Format:", data.get("audio_format"))
            print("Speech Detected:", data.get("speech_detected"))
            print("Detected Language:", data.get("language"), f"(Confidence: {data.get('language_confidence')})")
            print("Transcript Preview:", (data.get("transcript") or "")[:90] + "...")
            print("ML Classification:", data.get("classification"), f"(Confidence: {data.get('model_confidence')})")
            print("Scam Category:", data.get("scam_category"))
            print("Risk Score:", data.get("risk_score"), f"({data.get('risk_level')})")
            print("Is Digital Arrest:", data.get("is_digital_arrest"))
            print("Indicators Count:", len(data.get("indicators", [])))
            print("Diagnostics:", json.dumps(data.get("diagnostics", {}), indent=2))

            # Assertions
            if not data.get("success") or not data.get("transcript"):
                print("FAILED: Transcript is empty!")
                all_passed = False
            elif data.get("classification") != t["expected_classification"]:
                print(f"FAILED: Expected classification {t['expected_classification']}, got {data.get('classification')}")
                all_passed = False
            else:
                print("PASSED!")
        else:
            # Expected no speech
            if response.status_code == 422:
                detail = response.json().get("detail", "")
                print("Expected 422 No Speech Detected. Detail:", detail)
                if "no speech" in detail.lower() or "silent" in detail.lower():
                    print("PASSED (Correctly distinguished silence)!")
                else:
                    print("FAILED: Detail did not mention no speech/silence:", detail)
                    all_passed = False
            elif response.status_code == 200 and not response.json().get("speech_detected"):
                print("PASSED (Speech not detected)!")
            else:
                print(f"FAILED: Unexpected status code {response.status_code}: {response.text}")
                all_passed = False

        print("\n")

    print("=================================================================")
    if all_passed:
        print("ALL 4 AUDIO PIPELINE TESTS PASSED PERFECTLY!")
    else:
        print("SOME TESTS FAILED - CHECK OUTPUT ABOVE")
    print("=================================================================")
    return all_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
