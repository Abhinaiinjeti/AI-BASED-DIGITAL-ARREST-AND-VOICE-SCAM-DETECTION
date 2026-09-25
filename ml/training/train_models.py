"""
Model Training and Comparison Module
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Trains and compares:
1. Logistic Regression
2. Multinomial Naive Bayes
3. Linear Support Vector Machine (LinearSVC with CalibratedClassifierCV)

Features:
- TF-IDF extraction (n-gram (1, 2), fit strictly on training set)
- Binary classification: Legitimate (0) vs Scam (1)
- Category classification: Real dataset scam categories
- Honest validation comparison: Best model selected strictly on validation F1
- Final evaluation on held-out test split
- Saves models, vectorizer, and full evaluation reports
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.naive_bayes import MultinomialNB
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
PROCESSED_DIR = BASE_DIR / "data" / "processed"
MODELS_DIR = BASE_DIR / "models"
DOCS_DIR = BASE_DIR / "docs"


def evaluate_predictions(y_true, y_pred, y_prob=None, average="weighted"):
    """Compute comprehensive evaluation metrics."""
    acc = float(accuracy_score(y_true, y_pred))
    prec_macro = float(precision_score(y_true, y_pred, average="macro", zero_division=0))
    prec_weighted = float(precision_score(y_true, y_pred, average="weighted", zero_division=0))
    rec_macro = float(recall_score(y_true, y_pred, average="macro", zero_division=0))
    rec_weighted = float(recall_score(y_true, y_pred, average="weighted", zero_division=0))
    f1_macro = float(f1_score(y_true, y_pred, average="macro", zero_division=0))
    f1_weighted = float(f1_score(y_true, y_pred, average="weighted", zero_division=0))
    cm = confusion_matrix(y_true, y_pred).tolist()

    return {
        "accuracy": acc,
        "precision_macro": prec_macro,
        "precision_weighted": prec_weighted,
        "recall_macro": rec_macro,
        "recall_weighted": rec_weighted,
        "f1_macro": f1_macro,
        "f1_weighted": f1_weighted,
        "confusion_matrix": cm,
    }


def train_and_evaluate():
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION")
    print("Machine Learning Training & Multi-Model Benchmarking Pipeline")
    print("=" * 65)

    # 1. Load stratified dataset splits
    train_path = PROCESSED_DIR / "train.csv"
    val_path = PROCESSED_DIR / "val.csv"
    test_path = PROCESSED_DIR / "test.csv"

    if not (train_path.exists() and val_path.exists() and test_path.exists()):
        raise FileNotFoundError("Processed dataset splits not found. Run clean_and_merge.py first.")

    train_df = pd.read_csv(train_path)
    val_df = pd.read_csv(val_path)
    test_df = pd.read_csv(test_path)

    print(f"[*] Loaded datasets: Train={len(train_df)}, Val={len(val_df)}, Test={len(test_df)}")

    # 2. Extract features: TF-IDF fitted strictly on train_df
    print("\n[*] Fitting TF-IDF Vectorizer on training data...")
    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        min_df=2,
        max_features=12000,
        sublinear_tf=True,
    )
    X_train = vectorizer.fit_transform(train_df["cleaned_text"].fillna(""))
    X_val = vectorizer.transform(val_df["cleaned_text"].fillna(""))
    X_test = vectorizer.transform(test_df["cleaned_text"].fillna(""))

    print(f"    Vocabulary size: {len(vectorizer.vocabulary_)} features")

    # Labels
    y_train_binary = train_df["label"].values
    y_val_binary = val_df["label"].values
    y_test_binary = test_df["label"].values

    # Category Labels
    cat_encoder = LabelEncoder()
    y_train_cat = cat_encoder.fit_transform(train_df["scam_category"].values)
    y_val_cat = cat_encoder.transform(val_df["scam_category"].values)
    y_test_cat = cat_encoder.transform(test_df["scam_category"].values)

    # 3. Model definitions
    candidate_models = {
        "Logistic Regression": LogisticRegression(
            C=1.5, max_iter=1000, class_weight="balanced", random_state=42
        ),
        "Multinomial Naive Bayes": MultinomialNB(alpha=0.1),
        "Linear SVM": CalibratedClassifierCV(
            LinearSVC(C=1.0, class_weight="balanced", random_state=42, dual="auto"),
            cv=3,
        ),
    }

    comparison_results = {}
    fitted_models = {}

    print("\n" + "=" * 65)
    print("BENCHMARKING CANDIDATE MODELS ON VALIDATION SET (BINARY)")
    print("=" * 65)

    for name, model in candidate_models.items():
        print(f"\n[*] Training {name}...")
        model.fit(X_train, y_train_binary)
        val_preds = model.predict(X_val)
        val_probs = model.predict_proba(X_val) if hasattr(model, "predict_proba") else None

        metrics = evaluate_predictions(y_val_binary, val_preds, val_probs)
        comparison_results[name] = {
            "validation_metrics": metrics,
            "validation_report": classification_report(
                y_val_binary, val_preds, target_names=["Legitimate", "Scam"], output_dict=True
            ),
        }
        fitted_models[name] = model

        print(f"    Validation Accuracy:          {metrics['accuracy']:.4f}")
        print(f"    Validation Macro F1:          {metrics['f1_macro']:.4f}")
        print(f"    Validation Weighted F1:       {metrics['f1_weighted']:.4f}")
        print(f"    Validation Weighted Precision:{metrics['precision_weighted']:.4f}")
        print(f"    Validation Weighted Recall:   {metrics['recall_weighted']:.4f}")

    # 4. Select the winner objectively based on validation Macro F1
    winner_name = max(
        comparison_results,
        key=lambda k: comparison_results[k]["validation_metrics"]["f1_macro"],
    )
    print("\n" + "=" * 65)
    print(f"[+] BEST MODEL SELECTED BASED ON VALIDATION F1: {winner_name}")
    print("=" * 65)

    best_model = fitted_models[winner_name]

    # 5. Evaluate the winner on the held-out TEST set
    test_preds = best_model.predict(X_test)
    test_probs = best_model.predict_proba(X_test) if hasattr(best_model, "predict_proba") else None
    test_metrics = evaluate_predictions(y_test_binary, test_preds, test_probs)
    test_report_dict = classification_report(
        y_test_binary, test_preds, target_names=["Legitimate", "Scam"], output_dict=True
    )

    print("\n" + "=" * 65)
    print(f"FINAL EVALUATION ON HELD-OUT TEST SET ({winner_name})")
    print("=" * 65)
    print(f"Test Accuracy:           {test_metrics['accuracy']:.4f}")
    print(f"Test Macro F1:           {test_metrics['f1_macro']:.4f}")
    print(f"Test Weighted F1:        {test_metrics['f1_weighted']:.4f}")
    print(f"Test Weighted Precision: {test_metrics['precision_weighted']:.4f}")
    print(f"Test Weighted Recall:    {test_metrics['recall_weighted']:.4f}")
    print("\nClassification Report (Test):")
    print(classification_report(y_test_binary, test_preds, target_names=["Legitimate", "Scam"]))

    # 6. Also train the multi-class scam category classifier using the winning architecture
    print("\n[*] Training Multi-Class Scam Category Classifier...")
    if "Logistic" in winner_name:
        category_model = LogisticRegression(
            C=1.5, max_iter=1000, class_weight="balanced", random_state=42
        )
    elif "Naive Bayes" in winner_name:
        category_model = MultinomialNB(alpha=0.1)
    else:
        category_model = CalibratedClassifierCV(
            LinearSVC(C=1.0, class_weight="balanced", random_state=42, dual="auto"),
            cv=3,
        )

    category_model.fit(X_train, y_train_cat)
    cat_val_preds = category_model.predict(X_val)
    cat_val_metrics = evaluate_predictions(y_val_cat, cat_val_preds)
    print(f"    Category Classifier Val Macro F1: {cat_val_metrics['f1_macro']:.4f}")

    # 7. Save model artifacts
    classifier_path = MODELS_DIR / "classifier.joblib"
    category_classifier_path = MODELS_DIR / "category_classifier.joblib"
    vectorizer_path = MODELS_DIR / "tfidf_vectorizer.joblib"
    encoder_path = MODELS_DIR / "label_encoder.joblib"
    metadata_path = MODELS_DIR / "metadata.json"
    comparison_path = MODELS_DIR / "model_comparison.json"

    joblib.dump(best_model, classifier_path)
    joblib.dump(category_model, category_classifier_path)
    joblib.dump(vectorizer, vectorizer_path)
    joblib.dump(cat_encoder, encoder_path)

    # Metadata
    metadata = {
        "project_title": "AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION",
        "timestamp": datetime.now().isoformat(),
        "selected_model": winner_name,
        "vocabulary_size": len(vectorizer.vocabulary_),
        "num_train_samples": len(train_df),
        "num_val_samples": len(val_df),
        "num_test_samples": len(test_df),
        "categories": list(cat_encoder.classes_),
        "test_metrics": test_metrics,
        "test_report": test_report_dict,
        "selection_rationale": (
            f"{winner_name} achieved the highest Macro F1 score on the validation set "
            f"({comparison_results[winner_name]['validation_metrics']['f1_macro']:.4f}) "
            "across imbalanced multilingual Indic scam distributions."
        ),
    }

    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    with open(comparison_path, "w", encoding="utf-8") as f:
        json.dump(comparison_results, f, indent=2)

    print(f"\n[+] Saved primary classifier: {classifier_path}")
    print(f"[+] Saved category classifier: {category_classifier_path}")
    print(f"[+] Saved TF-IDF vectorizer:  {vectorizer_path}")
    print(f"[+] Saved Label encoder:       {encoder_path}")
    print(f"[+] Saved Metadata:            {metadata_path}")
    print(f"[+] Saved Comparison JSON:     {comparison_path}")

    # 8. Generate markdown model evaluation report
    generate_markdown_report(comparison_results, winner_name, test_metrics, metadata)


def generate_markdown_report(comparison_results, winner_name, test_metrics, metadata):
    """Generate docs/model_evaluation_report.md."""
    report_path = DOCS_DIR / "model_evaluation_report.md"

    rows = []
    for model_name, res in comparison_results.items():
        v = res["validation_metrics"]
        rows.append(
            f"| **{model_name}** | {v['accuracy']*100:.2f}% | {v['precision_macro']*100:.2f}% | "
            f"{v['recall_macro']*100:.2f}% | {v['f1_macro']*100:.2f}% | {v['f1_weighted']*100:.2f}% |"
        )

    content = f"""# Machine Learning Model Evaluation Report
## AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

**Official Project Prototype Benchmarking Results**
**Date:** {metadata['timestamp']}

---

### 1. Methodology & Pipeline

- **Feature Representation:** TF-IDF Vectorizer with unigrams & bigrams (1, 2), sublinear term frequency, top 12,000 features.
- **Fitting Constraint:** Vectorizer was fitted strictly on the training partition (3,388 samples) to prevent data leakage.
- **Candidate Architectures Compared:**
  1. Logistic Regression (L2 regularization, balanced class weights)
  2. Multinomial Naive Bayes (Laplace smoothing $\\alpha=0.1$)
  3. Linear Support Vector Machine (LinearSVC with CalibratedClassifierCV probability output)
- **Selection Criterion:** Validation Macro F1 score across stratified Indic classes.

---

### 2. Validation Set Model Comparison

| Model Architecture | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 |
|-------------------|----------|-----------------|--------------|----------|-------------|
{chr(10).join(rows)}

### 3. Model Selection Decision

> **Winner:** **{winner_name}**
>
> **Rationale:** {metadata['selection_rationale']}

---

### 4. Final Held-Out Test Evaluation ({winner_name})

Evaluated on 726 unseen test samples:

- **Test Accuracy:** `{test_metrics['accuracy']*100:.2f}%`
- **Test Macro Precision:** `{test_metrics['precision_macro']*100:.2f}%`
- **Test Macro Recall:** `{test_metrics['recall_macro']*100:.2f}%`
- **Test Macro F1:** `{test_metrics['f1_macro']*100:.2f}%`
- **Test Weighted F1:** `{test_metrics['f1_weighted']*100:.2f}%`

#### Confusion Matrix (Test Set):
```
                       Predicted Legitimate    Predicted Scam
Actual Legitimate:             {test_metrics['confusion_matrix'][0][0]}                     {test_metrics['confusion_matrix'][0][1]}
Actual Scam:                   {test_metrics['confusion_matrix'][1][0]}                     {test_metrics['confusion_matrix'][1][1]}
```

---

### 5. Multi-Class Scam Categories Supported

The companion category classifier classifies samples into the authentic ground truth categories present in the training corpus:
{chr(10).join(f"- `{cat}`" for cat in metadata['categories'])}
"""

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[+] Model Evaluation Report saved to {report_path}")


if __name__ == "__main__":
    train_and_evaluate()
