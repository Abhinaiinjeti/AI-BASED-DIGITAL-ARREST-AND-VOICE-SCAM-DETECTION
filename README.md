# AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

> **Production-Style Academic Major B.Tech Capstone Project**  
> An integrated, explainable AI risk detection and decision-support system to defend citizens against digital arrest coercion and voice-based telecom scams across India.

---

## 1. Project Overview

**"AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION"** is an AI cybersecurity decision-support system designed to combat the surging epidemic of telecom fraud in India. Fraudsters frequently impersonate law enforcement personnel (Police, Central Bureau of Investigation [CBI], Enforcement Directorate [ED], Customs, and Courts), holding victims under psychological "Digital Arrest" via WhatsApp or Skype video calls under threat of immediate non-bailable arrest warrants.

This prototype provides an end-to-end defense pipeline accepting either:
1. **Suspicious Text/Message/Conversation:** Extortion messages, WhatsApp chats, SMS, or call transcripts.
2. **Recorded Voice/Audio:** Phone call recordings or live microphone input (WAV, MP3, M4A, OGG, WebM).

The system analyzes the input through a 7-stage pipeline and outputs:
- **Fraud/Scam Classification:** Legitimate vs Scam.
- **Scam Category:** Authentic ground-truth categories (e.g., `police_digital_arrest`, `police_blackmail`, `bank_kyc`, `telugu_telecom_fraud`, `none`).
- **Composite Risk Score:** A holistic index from **0 to 100**.
- **Risk Level:** `LOW RISK` (0-25), `SUSPICIOUS` (26-50), `HIGH RISK` (51-75), `VERY HIGH RISK` (76-100).
- **Model Statistical Confidence:** ML probability (e.g., 91.2%), strictly distinguished from Risk Score.
- **Detected Suspicious Indicators:** 6 core coercive pillars with severity badges and matched verbatim text evidence.
- **Contextual Safety Advisory:** Actionable emergency guidance with direct links to the National Cyber Crime Reporting Portal (`cybercrime.gov.in`) and Toll-Free Helpline **1930**.

---

## 2. Key Features

- **Domain-Preserving NLP Preprocessor:** Retains critical legal, police, and banking terms (`police`, `CBI`, `ED`, `arrest`, `OTP`, `UPI`, `bank`, `account`, `money`, `immediately`, `warrant`, `FIR`, `narcotics`, `Aadhaar`, `customs`) across training and inference.
- **Multilingual Support:** Supports **English**, **Hindi (Devanagari)**, **Hinglish (Roman Script)**, and native **Telugu**. Honestly reports `"Language uncertain"` if detection confidence is ambiguous.
- **Speech-to-Text Voice Processing:** Fast, free, local audio validation and transcription feeding directly into the text classification pipeline.
- **Explainable Rule-Based Indicator Engine:** Transparent pattern matching across 6 coercion vectors (Authority Impersonation, Legal Threats, Video Isolation, Fabricated Charges, Financial Extortion, and Urgency).
- **Privacy-First SQLite History:** Does **not** store raw conversational text or audio recordings by default. Only anonymized scores and metadata are logged locally.
- **Cybersecurity UI & Visual Pipeline:** Built with React 19, Tailwind CSS, and Framer Motion, featuring an animated semicircular SVG risk gauge, live pipeline stage indicator, and real session analytics.

---

## 3. Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 19, Vite 8, Tailwind CSS, Lucide React, Recharts, Framer Motion |
| **Backend API** | Python 3.12, FastAPI, Uvicorn, Pydantic v2 |
| **Machine Learning** | Scikit-learn (Logistic Regression, Multinomial Naive Bayes, Linear SVM), TF-IDF, Pandas, NumPy, Joblib |
| **Speech Processing** | Faster-Whisper / SpeechRecognition, SoundFile, ImageIO-FFmpeg |
| **Database** | SQLite3 (Local metadata audit logging) |
| **Primary Dataset** | INDICA / IndiF Benchmark (`vikrant-vikram/INDICA` on Hugging Face) |
| **Secondary Dataset** | Indian Cyber Scam PhoneCall 10k (`ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset` on Hugging Face) |

---

## 4. System Architecture

```
                                      +------------------------+
                                      |   USER INPUT MODALITY  |
                                      +------------------------+
                                       /                      \
                                      /                        \
                       [Text Message / Transcript]        [Audio Call Recording]
                                    |                              |
                                    |                     +-----------------+
                                    |                     | Audio Validation|
                                    |                     +-----------------+
                                    |                              |
                                    |                     +-----------------+
                                    |                     | Speech-to-Text  |
                                    |                     | (Faster-Whisper)|
                                    |                     +-----------------+
                                    |                              |
                                    +--------------+---------------+
                                                   |
                                                   v
                                      +------------------------+
                                      |  Language Identification|
                                      |  (EN / HI / TE / HING) |
                                      +------------------------+
                                                   |
                                                   v
                                      +------------------------+
                                      | Text Preprocessing     |
                                      | (Preserves scam tokens)|
                                      +------------------------+
                                                   |
                                                   v
                                      +------------------------+
                                      | TF-IDF Feature Extractor|
                                      | (12,000 Unigram/Bigram)|
                                      +------------------------+
                                                   |
                         +-------------------------+-------------------------+
                         |                                                   |
                         v                                                   v
          +-----------------------------+                     +-----------------------------+
          |  Machine Learning Classifier|                     |   Digital Arrest Indicator  |
          |  (Logistic Regression Model)|                     |   Rule & Pattern Engine     |
          +-----------------------------+                     +-----------------------------+
                         |                                                   |
                         | [Probability & Class]                             | [Severity & Evidence]
                         |                                                   |
                         +-------------------------+-------------------------+
                                                   |
                                                   v
                                      +------------------------+
                                      | Composite Risk Engine  |
                                      | (0 - 100 Score & Tiers)|
                                      +------------------------+
                                                   |
                                                   v
                                      +------------------------+
                                      | Explainable Assessment |
                                      | & Helpline Advisory    |
                                      +------------------------+
                                                   |
                                                   v
                                      +------------------------+
                                      |  React Cybersecurity UI|
                                      |  & SQLite History Log  |
                                      +------------------------+
```

---

## 5. Dataset Ingestion & Verification

The project ingests authentic Indic data without synthetic generation:
1. **Primary Dataset (INDICA / IndiF):**
   - Streamed from Hugging Face (`vikrant-vikram/INDICA`).
   - Verified extraction of **1,342 native Telugu dialogue transcripts**, 1,406 Hindi dialogues, and 1,349 English fraud call transcripts.
2. **Secondary Dataset (Indian Cyber Scam 10k):**
   - 10,000 Hinglish and English call transcripts featuring authentic ground-truth labels for `police_digital_arrest` (1,776), `police_blackmail` (1,460), `bank_kyc` (718), and legitimate calls (`none`: 5,000).
3. **Data Splitting:**
   - 4,840 deduplicated unique samples stratified into **70% Train** (3,388 samples), **15% Validation** (726 samples), and **15% Test** (726 samples).

---

## 6. Machine Learning Model Evaluation

Three candidate models were trained and benchmarked using TF-IDF n-grams (1, 2) fitted strictly on the training partition:

| Model Architecture | Accuracy | Macro Precision | Macro Recall | Macro F1 | Weighted F1 |
|---|---|---|---|---|---|
| **Logistic Regression (Selected)** | **100.00%** | **100.00%** | **100.00%** | **1.0000** | **1.0000** |
| **Multinomial Naive Bayes** | 100.00% | 100.00% | 100.00% | 1.0000 | 1.0000 |
| **Linear SVM (Calibrated)** | 100.00% | 100.00% | 100.00% | 1.0000 | 1.0000 |

*Evaluation conducted on 726 held-out test samples. Model weights serialized to `models/classifier.joblib` and `models/metadata.json`.*

---

## 7. Installation & Quickstart

### Prerequisites
- Python 3.10+ (Verified on Python 3.12.10)
- Node.js 18+ (Verified on Node v24.19.0)
- Windows PowerShell or Bash terminal

### Step 1: Install Python Dependencies
```powershell
pip install -r requirements.txt
```

### Step 2: Ingest Datasets & Inspect
```powershell
# Ingest INDICA and Indian Cyber Scam subsets
python -m ml.data.download_datasets

# Inspect schema, class distributions, and Telugu availability
python -m ml.data.inspect_dataset

# Clean, deduplicate, and create stratified splits
python -m ml.data.clean_and_merge
```

### Step 3: Train & Benchmark ML Models
```powershell
python -m ml.training.train_models
```

### Step 4: Launch FastAPI Backend Server
```powershell
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend API docs available at: `http://127.0.0.1:8000/docs`*

### Step 5: Launch React Frontend Application
In a separate terminal:
```powershell
cd frontend
npm.cmd run dev
```
*Frontend opens at: `http://localhost:5173/`*

---

## 8. REST API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/health` | Service status, model readiness, and Whisper capability |
| `GET` | `/api/models/info` | Benchmark metadata, test metrics, and recognized categories |
| `POST` | `/api/analyze/text` | Full NLP analysis on text input |
| `POST` | `/api/analyze/audio` | Speech-to-text + NLP analysis on audio upload |
| `GET` | `/api/history` | Paginated SQLite analysis audit records |
| `DELETE` | `/api/history` | Purge local analysis history for user privacy |
| `GET` | `/api/stats` | Real session telemetry for analytics dashboard |
| `GET` | `/api/demos` | Authenticated pre-configured test demonstration scenarios |

---

## 9. Limitations & Scope

1. **Advisory Function:** This application serves strictly as an educational and operational risk detection decision-support tool. It does not replace formal law enforcement investigations.
2. **Audio Quality:** Audio transcription accuracy depends on acoustic clarity and background noise levels.
3. **Evolving Threat Vectors:** Cyber criminals continuously adapt phraseology. Periodic retraining on new NCRP/I4C crime trends is recommended.
