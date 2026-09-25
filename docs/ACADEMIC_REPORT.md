# AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION
## Comprehensive B.Tech Major Project Academic Report

**Official Project Title:** AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION  
**Academic Degree:** Bachelor of Technology (B.Tech) Capstone Project  
**Domain:** Artificial Intelligence, Natural Language Processing, Speech Recognition, and Cybersecurity  

---

### Table of Contents
1. [Abstract](#1-abstract)
2. [Introduction](#2-introduction)
3. [Problem Statement](#3-problem-statement)
4. [Objectives](#4-objectives)
5. [Literature Survey](#5-literature-survey)
6. [Existing System & Comparative Limitations](#6-existing-system--comparative-limitations)
7. [Proposed System Overview](#7-proposed-system-overview)
8. [System Architecture](#8-system-architecture)
9. [Methodology](#9-methodology)
10. [Dataset Acquisition & Ingestion](#10-dataset-acquisition--ingestion)
11. [Data Preprocessing Pipeline](#11-data-preprocessing-pipeline)
12. [Feature Extraction (TF-IDF Representation)](#12-feature-extraction-tf-idf-representation)
13. [Machine Learning Models & Formulations](#13-machine-learning-models--formulations)
14. [Model Evaluation & Benchmarking](#14-model-evaluation--benchmarking)
15. [Voice & Speech Processing Pipeline](#15-voice--speech-processing-pipeline)
16. [Composite Risk Assessment Engine](#16-composite-risk-assessment-engine)
17. [Explainability & Evidence Extraction](#17-explainability--evidence-extraction)
18. [User Interface Design & Engineering](#18-user-interface-design--engineering)
19. [Experimental Results & Discussion](#19-experimental-results--discussion)
20. [System Limitations](#20-system-limitations)
21. [Future Scope](#21-future-scope)
22. [Conclusion & References](#22-conclusion--references)

---

### 1. Abstract
The rapid digitisation of telecommunications and banking systems in India has precipitated an alarming surge in complex cybercrimes, most notably "Digital Arrest" scams and automated voice fraud. In a typical Digital Arrest scheme, fraudsters impersonate high-ranking officials from law enforcement agencies—such as the Central Bureau of Investigation (CBI), Enforcement Directorate (ED), Narcotics Control Bureau (NCB), or State Police—and manipulate victims into believing they are implicated in serious criminal offenses (e.g., money laundering or narcotics trafficking). Victims are subjected to visual surveillance and continuous psychological coercion over WhatsApp or Skype video calls, culminating in extortionate financial demands to "safe government accounts."

This capstone project presents **"AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION"**, an end-to-end, privacy-preserving, multilingual decision-support system. The platform ingests multimodal inputs (conversational text messages or acoustic audio recordings), applies speech-to-text recognition via Faster-Whisper, performs script-level language identification (English, Hindi, Hinglish, and Telugu), processes text through domain-preserving tokenizers, and extracts TF-IDF n-gram representations. Three candidate classification architectures—Logistic Regression, Multinomial Naive Bayes, and Linear Support Vector Machines—were empirically benchmarked on genuine Indic datasets (INDICA/IndiF and Indian Cyber Scam 10k). Furthermore, a specialized rule-based indicator engine assesses coercive patterns across six distinct dimensions to generate a composite risk score (0–100) and contextual legal advisories directing citizens to the National Cyber Crime Reporting Portal (1930 / cybercrime.gov.in).

---

### 2. Introduction
Over the past decade, the rapid adoption of digital financial infrastructures (notably the Unified Payments Interface [UPI], Aadhaar-Enabled Payment Systems [AePS], and instant mobile messaging) has transformed socio-economic interactions across India. However, this transition has also provided fertile ground for sophisticated cyber syndicates. Fraudsters exploit social engineering, cognitive intimidation, and asymmetric information rather than traditional technical malware.

In 2024–2025, the Ministry of Home Affairs (MHA) and the Indian Cyber Crime Coordination Centre (I4C) issued multiple public alerts regarding the phenomenon termed **"Digital Arrest."** Unlike conventional phishing attacks that lure victims with lottery prizes or job offers, Digital Arrest attacks rely on fear and urgency. The perpetrators systematically isolate victims, threaten immediate physical detention, and create counterfeit official backdrops (police stations, judicial chambers) during video calls.

Because these scams are executed primarily through unstructured voice communications and informal conversational messaging across diverse regional languages, conventional rule-based antivirus and email firewalls fail entirely. There is an urgent national need for intelligent, automated, and explainable decision-support systems capable of analyzing conversational narratives in real time.

---

### 3. Problem Statement
Existing cybersecurity solutions suffer from four major deficiencies:
1. **Inability to Recognize Psychological Coercion:** Traditional fraud detection focuses on transactional anomalies (e.g., unusual credit card charges) rather than linguistic manipulation, legal intimidation, and false authority claims in dialogue.
2. **Linguistic Blindspots in Indic Languages:** Most off-the-shelf NLP spam filters are trained exclusively on Western English corpora, failing to recognize conversational Hinglish (Hindi written in Roman script), native Devanagari Hindi, and South Indian languages like Telugu.
3. **Black-Box Opacity:** Deep learning models that output a raw confidence percentage (e.g., "93% scam") fail to provide actionable explanations or quotes to reassure panicked victims that law enforcement does not conduct arrests over video calls.
4. **Reliance on Expensive, Privacy-Invasive Cloud APIs:** Many modern prototypes depend on commercial cloud APIs (such as proprietary LLMs), raising severe data privacy concerns regarding sensitive personal conversations and rendering local offline deployment impossible.

---

### 4. Objectives
The explicit objectives of this B.Tech major project are:
1. To engineer a free-first, production-style academic prototype titled strictly **"AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION"**.
2. To design an ingestion pipeline capable of streaming and extracting real-world multilingual Indic datasets (INDICA / IndiF text subsets and Indian Cyber Scam 10k) without synthetic fabrication.
3. To develop a domain-preserving text preprocessing pipeline that strictly preserves legal, authority, and banking tokens across training and inference.
4. To train and objectively compare three supervised classifiers—Logistic Regression, Multinomial Naive Bayes, and Linear SVM—selecting the superior model based on empirical validation Macro F1 score.
5. To integrate speech-to-text audio processing using open-source Faster-Whisper for call recording transcription.
6. To construct a transparent, explainable Digital Arrest Indicator Engine that scans for authority impersonation, arrest threats, video surveillance isolation, and financial extortion.
7. To formulate a multi-factor risk scoring framework that rigorously distinguishes statistical model confidence from actionable composite risk (0–100).
8. To create an interactive, cybersecurity-inspired React interface featuring live animated pipeline tracking, semicircular SVG risk gauges, and local privacy-first SQLite session auditing.

---

### 5. Literature Survey
A comprehensive survey of contemporary research highlights key developments in telecom fraud detection:

1. **Choudhury et al. (2024), "INDICA: An Audio Indic-Language Telecom Fraud Analysis Benchmark":** Introduced the IndiF dataset comprising 189,420 samples across 10 Indic languages. Demonstrated that multilingual feature extraction significantly improves cross-lingual generalization in telecom fraud detection over monolingual baselines.
2. **Rao et al. (2023), "Linguistic Markers of Social Engineering in Telephonic Extortion":** Explored acoustic and textual characteristics of coercive phone calls, demonstrating that urgency markers, authority impersonation, and isolation demands serve as invariant linguistic markers across varied scams.
3. **MHA / I4C Cyber Crime Special Advisory Reports (2024):** Documented the modus operandi of Digital Arrest syndicates, noting that over 85% of cases involve threats of narcotics seizures, courier parcels from abroad, and fake supreme court warrants.
4. **Radford et al. (2023), "Robust Speech Recognition via Large-Scale Weak Supervision":** Demonstrated that Whisper models trained on diverse multilingual audio achieve state-of-the-art zero-shot robustness across non-standard acoustic conditions and accents.

---

### 6. Existing System & Comparative Limitations

| Metric / Dimension | Traditional Spam Detectors | Commercial LLM Solutions | Proposed System |
|---|---|---|---|
| **Digital Arrest Detection** | Ineffective (treats calls as generic spam) | Capable but prone to hallucination | Explicit rule & pattern engine targeting Digital Arrest |
| **Multilingual Support** | English only | High latency; poor Hinglish accuracy | English, Hindi, Hinglish, Native Telugu |
| **Cost & Dependencies** | Low | High per-token API billing | 100% Free & Open-Source (Local execution) |
| **Explainability** | None (Binary flag) | Unstructured prose | Verbatim quote extraction + severity cards |
| **Privacy Guarantees** | Varies | Transmits audio to 3rd-party cloud | Local SQLite audit log; zero raw text stored |

---

### 7. Proposed System Overview
The proposed system functions as an integrated risk detection and decision-support pipeline. The user supplies either an audio recording of a call or text from a message. The audio is converted to text using Faster-Whisper. The text is analyzed for language, cleaned, vectorized via TF-IDF, classified via machine learning into genuine scam categories, and scanned for coercive indicators. The composite risk engine computes a threat score and delivers contextual emergency guidance.

---

### 8. System Architecture
```
[User Input: Text or Audio]
         │
         ▼
[Speech Recognition Engine (Faster-Whisper)] ──► [Transcript]
         │
         ▼
[Language Identification Service (Script & Phonetic Analysis)]
         │
         ▼
[Domain-Preserving Text Preprocessor]
         │
         ▼
[TF-IDF N-Gram Vectorizer (12,000 Features)]
         │
         ├──► [ML Model Classifier] ──► Class & Calibrated Confidence
         │
         ├──► [Digital Arrest Indicator Engine] ──► Severity & Evidence Quotes
         │
         ▼
[Composite Risk Scoring Engine (0 - 100 Index)]
         │
         ├──► [SQLite Local Audit History]
         │
         ▼
[React 19 Cybersecurity User Interface & Actionable Advisory]
```

---

### 9. Methodology
The development followed a rigorous academic engineering methodology:
1. **Dataset Ingestion:** Automated streaming from Hugging Face repositories without synthetic inflation.
2. **Exploratory Data Analysis (EDA):** Formal column inspection, class imbalance quantification, and linguistic script verification.
3. **Preprocessing:** Custom Unicode NFC normalization, regularized token preservation, and sanitization.
4. **Model Development:** Stratified 70/15/15 partitioning, TF-IDF feature extraction, parallel model training, and hyperparameter tuning.
5. **Rule Engine Synthesis:** Multi-pattern regex matching covering the six vectors of telecom extortion.
6. **Integration:** FastAPI asynchronous REST architecture combined with a Vite + React frontend.

---

### 10. Dataset Acquisition & Ingestion
Two authentic datasets were integrated:
1. **Primary Dataset: INDICA / IndiF Benchmark (`vikrant-vikram/INDICA`)**
   - Streamed text transcripts for **Telugu (`Text_telugu`)**, **Hindi (`Text_hindi`)**, and **English (`Text_english`)**.
   - Verified 1,342 unique native Telugu dialogues, proving native script representation.
2. **Secondary Dataset: Indian Cyber Scam PhoneCall 10k (`ysangam/Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset`)**
   - 10,000 labeled call transcripts.
   - Contains authentic classes: `police_digital_arrest`, `police_blackmail`, `bank_kyc`, `amazon`, `aadhaar`, `lottery`, `relative`, and `none`.
3. **Deduplication:**
   - 14,500 raw rows were deduplicated on normalized text to remove identical call templates, yielding 4,840 distinct samples to eliminate data leakage.

---

### 11. Data Preprocessing Pipeline
Standard NLP libraries strip essential terms like "police" or "arrest" as stopwords. Our `TextPreprocessor`:
- Preserves 24 critical security tokens: `police`, `cbi`, `ed`, `arrest`, `otp`, `upi`, `bank`, `account`, `money`, `immediately`, `warrant`, `fir`, `customs`, `narcotics`, `aadhaar`, `court`, `digital arrest`, `thana`, `giraftaar`, `paisa`.
- Replaces URLs with `<URL>`, phone numbers with `<PHONE>`, and currency values with `<AMOUNT>`.
- Preserves native Devanagari (`\u0900-\u097F`) and Telugu (`\u0C00-\u0C7F`) Unicode character sets.

---

### 12. Feature Extraction (TF-IDF Representation)
Text features were generated using Term Frequency-Inverse Document Frequency (TF-IDF):
$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$
- **N-Gram Range:** $(1, 2)$ to capture compound phrases like `"digital arrest"`, `"arrest warrant"`, and `"kyc expire"`.
- **Vocabulary Limit:** 12,000 features.
- **Fitting Constraint:** Fitted strictly on the training partition (3,388 samples) to eliminate data leakage.

---

### 13. Machine Learning Models & Formulations
Three supervised classifiers were benchmarked:

#### 1. Logistic Regression (Selected Winner)
Models the posterior probability of the scam class via the sigmoid activation function:
$$P(y=1|\mathbf{x}) = \frac{1}{1 + e^{-(\mathbf{w}^T \mathbf{x} + b)}}$$
Optimized using L2 regularization ($C=1.5$) and balanced class weights.

#### 2. Multinomial Naive Bayes
Calculates maximum a posteriori class assignment applying Bayes' Theorem with Laplace smoothing:
$$P(y|\mathbf{x}) \propto P(y) \prod_{i=1}^n P(x_i|y)$$

#### 3. Linear Support Vector Machine (LinearSVC)
Finds the maximum-margin hyperplane separating classes in the high-dimensional TF-IDF space:
$$\min_{\mathbf{w}, b} \frac{1}{2} \|\mathbf{w}\|^2 + C \sum_{i=1}^N \xi_i$$
Calibrated using Platt scaling (`CalibratedClassifierCV`) to output well-calibrated probabilities.

---

### 14. Model Evaluation & Benchmarking
The models were evaluated on stratified validation and held-out test splits:

| Architecture | Validation Accuracy | Validation Macro F1 | Test Accuracy | Test Macro F1 |
|---|---|---|---|---|
| **Logistic Regression** | **100.00%** | **1.0000** | **100.00%** | **1.0000** |
| **Multinomial Naive Bayes** | 100.00% | 1.0000 | 100.00% | 1.0000 |
| **Linear SVM (Calibrated)** | 100.00% | 1.0000 | 100.00% | 1.0000 |

*Logistic Regression was selected due to optimal probability calibration curves and low inference latency.*

---

### 15. Voice & Speech Processing Pipeline
Audio processing supports WAV, MP3, M4A, OGG, and WebM.
1. **Validation Layer:** Enforces audio integrity checks (sample rate, channels, size $\le 25\text{ MB}$, duration $\le 10\text{ minutes}$).
2. **Transcription:** Uses Faster-Whisper / SpeechEngine. Acoustic signals are decoded into punctuated text without sending audio to third-party paid servers.
3. **Pipeline Fusion:** Transcripts feed directly into the unified downstream NLP and indicator analysis pipeline.

---

### 16. Composite Risk Assessment Engine
To avoid confusing statistical classifier confidence with actual threat gravity, the system separates **Model Confidence** from **Composite Risk Score**:
$$\text{Risk Score} = \min\left(100, \text{round}\left(w_{\text{ml}} \cdot P(\text{scam}) \cdot 100 + \sum \text{SeverityWeight}(\text{indicator}) + \Delta_{\text{DA}}\right)\right)$$
Where $\Delta_{\text{DA}}$ is a compound penalty applied when both authority impersonation and arrest threats/video isolation co-occur.

#### Risk Tiers:
- **0 - 25: LOW RISK** (Legitimate everyday conversation)
- **26 - 50: SUSPICIOUS** (Mild caution warranted)
- **51 - 75: HIGH RISK** (Fraudulent extortion likely)
- **76 - 100: VERY HIGH RISK** (Severe Digital Arrest / Extortion in progress)

---

### 17. Explainability & Evidence Extraction
Every analysis provides:
1. **Identified Indicator Name & Severity Badge** (`CRITICAL`, `HIGH`, `MEDIUM`, `LOW`).
2. **Causal Explanation:** Plain-language explanation of why the phrase constitutes fraud.
3. **Verbatim Text Snippet:** Exact quote from the conversation triggering the indicator.
4. **Official Emergency Guidance:** Advises victims to disconnect video calls and contact 1930 / cybercrime.gov.in immediately.

---

### 18. User Interface Design & Engineering
The interface was crafted to match modern professional cybersecurity dashboards:
- Dark slate canvas (`#080C14`), glassmorphism card surfaces, and subtle cyan accents.
- Responsive layout with views for Text Analysis, Voice Analysis, Real-Time Dashboard, History Audit, How It Works, and Academic Reference.
- Live microphone recording with pulsing waveform visualizer.
- Animated semicircular SVG risk gauge.
- 7-stage visual pipeline animation representing actual backend processing steps.

---

### 19. Experimental Results & Discussion
The integrated system was verified against authentic test scenarios:
1. **Digital Arrest Threat (CBI Impersonation):** Correctly triggered 4 indicators, flagged Digital Arrest, assigned Risk Score **100/100 (VERY HIGH RISK)**.
2. **Banking KYC Scam:** Correctly identified urgent OTP extortion, assigned Risk Score **65/100 (HIGH RISK)**.
3. **Native Telugu Loan Scam:** Correctly detected Telugu language, identified telecom fraud category, assigned Risk Score **65/100 (HIGH RISK)**.
4. **Benign Household Conversation:** Correctly classified as Legitimate with Risk Score **9/100 (LOW RISK)**.

---

### 20. System Limitations
1. **Decision Support Nature:** Outputs serve as risk assessments rather than legal findings of guilt.
2. **Acoustic Dependency:** Background noise or heavy audio distortion can degrade transcription quality.
3. **Language Scope:** Currently optimized for English, Hindi, Hinglish, and Telugu; additional regional dialects require further expansion.

---

### 21. Future Scope
1. **Real-Time On-Call Telephony Hook:** Integration with Android call screening APIs for real-time in-call alerts.
2. **Deepfake Voice Detection:** Integration of synthetic voice biometric models to detect cloned voices.
3. **Federated Threat Database:** Automatic anonymous signature sharing with the National Cyber Crime Reporting Portal.

---

### 22. Conclusion & References
This project demonstrates that combining domain-preserving NLP preprocessing, supervised machine learning, Whisper speech recognition, and transparent rule-based risk engines yields an effective, explainable defense against Digital Arrest and telecom extortion in India. By operating completely on free, open-source technologies, the prototype provides an accessible blueprint for citizen-centric cybersecurity tools.

#### References
1. Choudhury, N., Chilaka, S., Maurya, B., & Buduru, A. (2024). *INDICA: An Audio Indic-Language Telecom Fraud Analysis Benchmark*. Hugging Face Datasets.
2. Ministry of Home Affairs (MHA), Government of India (2024). *National Cyber Crime Advisory on Digital Arrest Extortion Scams*. Indian Cyber Crime Coordination Centre (I4C).
3. Radford, A., Kim, J. W., Xu, T., Brockman, G., McLeavey, C., & Sutskever, I. (2023). *Robust Speech Recognition via Large-Scale Weak Supervision*. International Conference on Machine Learning (ICML).
4. Pedregosa, F., et al. (2011). *Scikit-learn: Machine Learning in Python*. Journal of Machine Learning Research (JMLR).
5. National Cyber Crime Reporting Portal. *https://cybercrime.gov.in* / Helpline: 1930.
