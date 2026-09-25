"""
Language Identification Service
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Supports:
- English
- Hindi (Devanagari script)
- Telugu (Telugu script)
- Hinglish (Hindi written in Roman/Latin script)

Performs honest confidence scoring.
If confidence is insufficient, displays 'Language uncertain' as required.
"""

import re
from typing import Dict, Any
from langdetect import detect_langs
from langdetect.lang_detect_exception import LangDetectException


class LanguageService:
    # Unicode Ranges
    TELUGU_RANGE = re.compile(r"[\u0C00-\u0C7F]")
    DEVANAGARI_RANGE = re.compile(r"[\u0900-\u097F]")

    # Hinglish common phonetic markers
    HINGLISH_WORDS = {
        "aapka", "aapki", "aapke", "hai", "hain", "kijiye", "karo", "karna", "hoga",
        "hogi", "bhejo", "paisa", "paise", "rupaye", "thana", "giraftaar", "turant",
        "ghante", "mein", "nahin", "nahi", "raha", "rahe", "rahi", "bol", "bola",
        "ghar", "namaskar", "namaste", "beta", "darwaza", "khol", "kripya", "chalan",
        "khata", "sambandhit", "parivar", "police", "adhikari"
    }

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect language of the input text.
        Returns: { 'language': str, 'confidence': float, 'is_uncertain': bool, 'script': str }
        """
        if not text or len(text.strip()) < 3:
            return {
                "language": "Language uncertain",
                "confidence": 0.0,
                "is_uncertain": True,
                "script": "unknown",
            }

        cleaned = text.strip()
        total_chars = len(cleaned)

        # 1. Native Telugu script detection
        telugu_matches = len(self.TELUGU_RANGE.findall(cleaned))
        if telugu_matches / max(1, total_chars) > 0.15:
            conf = min(0.99, round(0.70 + (telugu_matches / total_chars) * 0.3, 2))
            return {
                "language": "Telugu",
                "confidence": conf,
                "is_uncertain": False,
                "script": "Telugu",
            }

        # 2. Native Devanagari script detection (Hindi)
        dev_matches = len(self.DEVANAGARI_RANGE.findall(cleaned))
        if dev_matches / max(1, total_chars) > 0.15:
            conf = min(0.99, round(0.70 + (dev_matches / total_chars) * 0.3, 2))
            return {
                "language": "Hindi",
                "confidence": conf,
                "is_uncertain": False,
                "script": "Devanagari",
            }

        # 3. Check for Hinglish (Latin script with Hindi phonetic vocabulary)
        words = re.findall(r"\b[a-zA-Z]+\b", cleaned.lower())
        if words:
            hinglish_hits = sum(1 for w in words if w in self.HINGLISH_WORDS)
            hinglish_ratio = hinglish_hits / len(words)
            if hinglish_ratio >= 0.15 or hinglish_hits >= 2:
                conf = min(0.95, round(0.65 + hinglish_ratio * 0.3, 2))
                return {
                    "language": "Hinglish",
                    "confidence": conf,
                    "is_uncertain": False,
                    "script": "Latin",
                }

        # 4. Standard langdetect for English and other languages
        try:
            detected = detect_langs(cleaned)
            if detected:
                top = detected[0]
                if top.lang == "en" and top.prob >= 0.65:
                    return {
                        "language": "English",
                        "confidence": round(float(top.prob), 2),
                        "is_uncertain": False,
                        "script": "Latin",
                    }
                elif top.lang == "hi" and top.prob >= 0.70:
                    return {
                        "language": "Hindi",
                        "confidence": round(float(top.prob), 2),
                        "is_uncertain": False,
                        "script": "Devanagari",
                    }
                elif top.lang == "te" and top.prob >= 0.70:
                    return {
                        "language": "Telugu",
                        "confidence": round(float(top.prob), 2),
                        "is_uncertain": False,
                        "script": "Telugu",
                    }
                elif top.prob < 0.60:
                    return {
                        "language": "Language uncertain",
                        "confidence": round(float(top.prob), 2),
                        "is_uncertain": True,
                        "script": "Latin",
                    }
        except LangDetectException:
            pass

        # Fallback if uncertain
        return {
            "language": "Language uncertain",
            "confidence": 0.40,
            "is_uncertain": True,
            "script": "unknown",
        }


# Singleton
language_service = LanguageService()
