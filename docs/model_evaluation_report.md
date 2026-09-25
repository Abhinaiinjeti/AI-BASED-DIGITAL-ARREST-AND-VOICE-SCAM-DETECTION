# Machine Learning Model Evaluation Report
## AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

**Official Project Prototype Benchmarking Results**
**Date:** 2026-09-25T20:27:13.064183

---

### 1. Methodology & Pipeline

- **Feature Representation:** TF-IDF Vectorizer with unigrams & bigrams (1, 2), sublinear term frequency, top 12,000 features.
- **Fitting Constraint:** Vectorizer was fitted strictly on the training partition (3,388 samples) to prevent data leakage.
- **Candidate Architectures Compared:**
  1. Logistic Regression (L2 regularization, balanced class weights)
  2. Multinomial Naive Bayes (Laplace smoothing $\alpha=0.1$)
  3. Linear Support Vector Machine (LinearSVC with CalibratedClassifierCV probability output)
- **Selection Criterion:** Validation Macro F1 score across stratified Indic classes.

---

### 2. Validation Set Model Comparison

| Model Architecture | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 |
|-------------------|----------|-----------------|--------------|----------|-------------|
| **Logistic Regression** | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% |
| **Multinomial Naive Bayes** | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% |
| **Linear SVM** | 100.00% | 100.00% | 100.00% | 100.00% | 100.00% |

### 3. Model Selection Decision

> **Winner:** **Logistic Regression**
>
> **Rationale:** Logistic Regression achieved the highest Macro F1 score on the validation set (1.0000) across imbalanced multilingual Indic scam distributions.

---

### 4. Final Held-Out Test Evaluation (Logistic Regression)

Evaluated on 726 unseen test samples:

- **Test Accuracy:** `100.00%`
- **Test Macro Precision:** `100.00%`
- **Test Macro Recall:** `100.00%`
- **Test Macro F1:** `100.00%`
- **Test Weighted F1:** `100.00%`

#### Confusion Matrix (Test Set):
```
                       Predicted Legitimate    Predicted Scam
Actual Legitimate:             228                     0
Actual Scam:                   0                     498
```

---

### 5. Multi-Class Scam Categories Supported

The companion category classifier classifies samples into the authentic ground truth categories present in the training corpus:
- `aadhaar`
- `amazon`
- `bank_kyc`
- `customer_service_impersonation`
- `lottery`
- `none`
- `police_blackmail`
- `police_digital_arrest`
- `relative`
- `telugu_telecom_fraud`
