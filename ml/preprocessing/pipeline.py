"""
Text Preprocessing Pipeline
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Implements a unified, reusable preprocessing pipeline used identically during:
1. Model training
2. Real-time inference (text & transcribed audio)

Guarantees preservation of critical scam indicators:
police, cbi, ed, arrest, otp, upi, bank, account, money, immediately,
warrant, fir, customs, aadhaar, court, cybercrime, etc.
"""

import re
import unicodedata
from typing import List, Union


class TextPreprocessor:
    """Domain-preserving multilingual text preprocessor."""

    # Key security tokens that must never be removed or altered
    PRESERVED_TOKENS = {
        "police",
        "cbi",
        "ed",
        "arrest",
        "otp",
        "upi",
        "bank",
        "account",
        "money",
        "immediately",
        "warrant",
        "fir",
        "customs",
        "narcotics",
        "aadhaar",
        "court",
        "trafficking",
        "parcels",
        "digital arrest",
        "thana",
        "giraftaar",
        "paisa",
        "kijiye",
        "turant",
        "dharapakad",
        "chalan",
    }

    # Regex patterns
    URL_PATTERN = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
    EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
    PHONE_PATTERN = re.compile(r"\b(?:\+91|91)?[-.\s]?[6-9]\d{9}\b")
    AMOUNT_PATTERN = re.compile(r"(?:₹|rs\.?|inr)\s*[\d,]+(?:\.\d+)?|\b\d+[\d,]*\s*(?:rupees|lakh|crore|hazaar)\b", re.IGNORECASE)
    WHITESPACE_PATTERN = re.compile(r"\s+")
    
    # Speaker tags common in conversational transcripts (e.g., "Speaker1:", "Speaker 2:")
    SPEAKER_TAG_PATTERN = re.compile(r"Speaker\s*\d+\s*:\s*", re.IGNORECASE)

    def __init__(self, remove_speaker_tags: bool = True):
        self.remove_speaker_tags = remove_speaker_tags

    def clean_text(self, text: Union[str, float, None]) -> str:
        """Clean a single text string."""
        if text is None:
            return ""
        if not isinstance(text, str):
            text = str(text)

        # 1. Unicode normalization (NFC ensures consistent Indic conjuncts)
        text = unicodedata.normalize("NFC", text)

        # 2. Remove speaker dialogue markers if present
        if self.remove_speaker_tags:
            text = self.SPEAKER_TAG_PATTERN.sub(" ", text)

        # 3. Replace URLs, Emails, Phone numbers, and Amounts with semantic tokens
        text = self.URL_PATTERN.sub(" <URL> ", text)
        text = self.EMAIL_PATTERN.sub(" <EMAIL> ", text)
        text = self.PHONE_PATTERN.sub(" <PHONE> ", text)
        text = self.AMOUNT_PATTERN.sub(" <AMOUNT> ", text)

        # 4. Lowercase Latin characters while preserving Indic scripts intact
        text = text.lower()

        # 5. Clean punctuation but preserve Indic scripts, word characters, and key tags
        # Keep Latin letters, digits, Indic characters (\u0900-\u097F for Hindi, \u0C00-\u0C7F for Telugu),
        # whitespace, and special placeholder brackets <>
        text = re.sub(r"[^\w\s<>\u0900-\u097F\u0C00-\u0C7F]", " ", text)

        # 6. Normalize multiple whitespaces
        text = self.WHITESPACE_PATTERN.sub(" ", text).strip()

        return text

    def transform(self, texts: List[Union[str, float, None]]) -> List[str]:
        """Clean a list or Series of texts."""
        return [self.clean_text(t) for t in texts]

    def __call__(self, text: Union[str, float, None]) -> str:
        return self.clean_text(text)


# Default preprocessor instance
default_preprocessor = TextPreprocessor()
