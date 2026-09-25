"""
Inference Module
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Loads trained artifacts and provides unified text prediction:
- Binary scam classification (Scam vs Legitimate)
- Confidence probability
- Ground truth scam category prediction
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple
import joblib

from ml.preprocessing.pipeline import TextPreprocessor

BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"


class ScamPredictor:
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.classifier = None
        self.category_classifier = None
        self.vectorizer = None
        self.label_encoder = None
        self.metadata = {}
        self._load_models()

    def _load_models(self):
        classifier_path = MODELS_DIR / "classifier.joblib"
        category_path = MODELS_DIR / "category_classifier.joblib"
        vectorizer_path = MODELS_DIR / "tfidf_vectorizer.joblib"
        encoder_path = MODELS_DIR / "label_encoder.joblib"
        meta_path = MODELS_DIR / "metadata.json"

        if not (classifier_path.exists() and vectorizer_path.exists()):
            raise FileNotFoundError(
                "Trained model artifacts not found in models/. Run train_models.py first."
            )

        self.classifier = joblib.load(classifier_path)
        self.vectorizer = joblib.load(vectorizer_path)

        if category_path.exists():
            self.category_classifier = joblib.load(category_path)
        if encoder_path.exists():
            self.label_encoder = joblib.load(encoder_path)
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

    def predict(self, raw_text: str) -> Dict[str, Any]:
        """
        Run inference on raw input text.
        Returns:
            cleaned_text, is_scam, binary_label, confidence, scam_category, category_probabilities
        """
        cleaned = self.preprocessor.clean_text(raw_text)
        if not cleaned:
            return {
                "cleaned_text": "",
                "is_scam": False,
                "confidence": 0.5,
                "scam_category": "none",
                "label": "Legitimate",
            }

        # Vectorize
        X = self.vectorizer.transform([cleaned])

        # Binary prediction
        binary_pred = int(self.classifier.predict(X)[0])
        if hasattr(self.classifier, "predict_proba"):
            probs = self.classifier.predict_proba(X)[0]
            confidence = float(probs[binary_pred])
            scam_prob = float(probs[1]) if len(probs) > 1 else (1.0 if binary_pred == 1 else 0.0)
        else:
            confidence = 0.95
            scam_prob = 1.0 if binary_pred == 1 else 0.0

        # Category prediction
        category = "none"
        if self.category_classifier is not None and self.label_encoder is not None:
            cat_idx = self.category_classifier.predict(X)[0]
            category = str(self.label_encoder.inverse_transform([cat_idx])[0])

        return {
            "cleaned_text": cleaned,
            "is_scam": bool(binary_pred == 1),
            "label": "Scam" if binary_pred == 1 else "Legitimate",
            "confidence": round(confidence, 4),
            "scam_probability": round(scam_prob, 4),
            "scam_category": category,
        }


# Singleton instance
_predictor = None

def get_predictor() -> ScamPredictor:
    global _predictor
    if _predictor is None:
        _predictor = ScamPredictor()
    return _predictor
