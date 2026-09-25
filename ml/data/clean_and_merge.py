"""
Dataset Cleaning, Merging, and Stratified Splitting Module
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Merges:
1. Indian Cyber Scam PhoneCall Dataset (10k Hinglish & English calls with Digital Arrest, Bank KYC, etc.)
2. INDICA / IndiF Benchmark Subsets (Native Telugu scam calls, Hindi legit dialogues, English fraud calls)

Performs:
- Missing value removal
- Text preprocessing (preserving scam tokens)
- Deduplication to avoid data leakage
- Stratified 70% Train / 15% Validation / 15% Test split
"""

import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from ml.preprocessing.pipeline import TextPreprocessor

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
INDIAN_SCAM_PATH = RAW_DATA_DIR / "indian_scam" / "India_Cyber_Scam_Hinglish_Dataset.csv"
INDICA_DIR = RAW_DATA_DIR / "indica" / "Text_samples"


def load_indian_cyber_scam() -> pd.DataFrame:
    """Load and format the Indian Cyber Scam dataset."""
    print("[*] Loading Indian Cyber Scam dataset...")
    df = pd.read_csv(INDIAN_SCAM_PATH)

    # Standardize columns
    formatted = pd.DataFrame()
    formatted["text"] = df["text"].astype(str)
    formatted["label"] = df["label"].astype(int)
    formatted["scam_category"] = df["scam_category"].astype(str)
    formatted["language"] = df["language_style"].fillna("hinglish").astype(str)
    formatted["source_dataset"] = "indian_cyber_scam_10k"

    print(f"    Loaded {len(formatted)} records from Indian Cyber Scam.")
    return formatted


def load_indica_subset(max_per_lang: int = 1500) -> pd.DataFrame:
    """Load and format the INDICA text samples."""
    print("[*] Loading INDICA text samples (Telugu, Hindi, English)...")
    records = []

    # 1. Telugu (scam samples)
    telugu_dir = INDICA_DIR / "Text_telugu"
    if telugu_dir.exists():
        for txt_file in list(telugu_dir.rglob("*.txt"))[:max_per_lang]:
            try:
                content = txt_file.read_text(encoding="utf-8", errors="ignore").strip()
                if len(content) > 15:
                    records.append({
                        "text": content,
                        "label": 1,
                        "scam_category": "telugu_telecom_fraud",
                        "language": "telugu",
                        "source_dataset": "indica_indif",
                    })
            except Exception:
                pass

    # 2. Hindi (legitimate customer service / communication samples)
    hindi_dir = INDICA_DIR / "Text_hindi"
    if hindi_dir.exists():
        for txt_file in list(hindi_dir.rglob("*.txt"))[:max_per_lang]:
            try:
                content = txt_file.read_text(encoding="utf-8", errors="ignore").strip()
                if len(content) > 15:
                    records.append({
                        "text": content,
                        "label": 0,
                        "scam_category": "none",
                        "language": "hindi",
                        "source_dataset": "indica_indif",
                    })
            except Exception:
                pass

    # 3. English (fraud call transcripts)
    english_dir = INDICA_DIR / "Text_english"
    if english_dir.exists():
        for txt_file in list(english_dir.rglob("*.txt"))[:max_per_lang]:
            try:
                content = txt_file.read_text(encoding="utf-8", errors="ignore").strip()
                if len(content) > 15:
                    records.append({
                        "text": content,
                        "label": 1,
                        "scam_category": "customer_service_impersonation",
                        "language": "english",
                        "source_dataset": "indica_indif",
                    })
            except Exception:
                pass

    indica_df = pd.DataFrame(records)
    print(f"    Loaded {len(indica_df)} records from INDICA.")
    return indica_df


def clean_and_merge():
    """Clean, merge, deduplicate, and split datasets."""
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    preprocessor = TextPreprocessor()

    # Load both sources
    scam_df = load_indian_cyber_scam()
    indica_df = load_indica_subset()

    # Merge
    merged = pd.concat([scam_df, indica_df], ignore_index=True)
    print(f"\n[*] Total merged raw records: {len(merged)}")

    # Clean text
    print("[*] Running domain-preserving text preprocessor...")
    merged["cleaned_text"] = preprocessor.transform(merged["text"])

    # Remove empty or whitespace-only records
    merged = merged[merged["cleaned_text"].str.len() > 5].copy()

    # Deduplicate on cleaned_text to prevent identical template leakage
    # We keep the first instance of each unique cleaned text
    initial_count = len(merged)
    merged = merged.drop_duplicates(subset=["cleaned_text"]).reset_index(drop=True)
    print(f"[*] Deduplication: removed {initial_count - len(merged)} duplicate variations.")
    print(f"[*] Total unique samples for modeling: {len(merged)}")

    print("\nFinal Merged Dataset Breakdown:")
    print("  Label distribution:")
    print(merged["label"].value_counts())
    print("\n  Category distribution:")
    print(merged["scam_category"].value_counts())
    print("\n  Language distribution:")
    print(merged["language"].value_counts())

    # Save complete merged dataset
    merged_path = PROCESSED_DATA_DIR / "merged_dataset.csv"
    merged.to_csv(merged_path, index=False, encoding="utf-8")
    print(f"\n[+] Saved full processed dataset: {merged_path}")

    # Stratified Train/Val/Test Split (70% train, 15% val, 15% test)
    # Stratify by label + language to ensure balanced multilingual representation
    strat_key = merged["label"].astype(str) + "_" + merged["language"]
    
    # Handle rare classes in strat_key if any has count < 2
    counts = strat_key.value_counts()
    valid_strat = strat_key.isin(counts[counts >= 2].index)
    
    if valid_strat.all():
        train_df, temp_df = train_test_split(
            merged, test_size=0.30, random_state=42, stratify=strat_key
        )
        temp_strat_key = temp_df["label"].astype(str) + "_" + temp_df["language"]
        val_df, test_df = train_test_split(
            temp_df, test_size=0.50, random_state=42, stratify=temp_strat_key
        )
    else:
        # Fallback to stratifying on label
        train_df, temp_df = train_test_split(
            merged, test_size=0.30, random_state=42, stratify=merged["label"]
        )
        val_df, test_df = train_test_split(
            temp_df, test_size=0.50, random_state=42, stratify=temp_df["label"]
        )

    # Save splits
    train_path = PROCESSED_DATA_DIR / "train.csv"
    val_path = PROCESSED_DATA_DIR / "val.csv"
    test_path = PROCESSED_DATA_DIR / "test.csv"

    train_df.to_csv(train_path, index=False, encoding="utf-8")
    val_df.to_csv(val_path, index=False, encoding="utf-8")
    test_df.to_csv(test_path, index=False, encoding="utf-8")

    print("\n[+] Stratified Split Results:")
    print(f"    Train: {len(train_df)} samples ({len(train_df)/len(merged)*100:.1f}%) -> {train_path}")
    print(f"    Val:   {len(val_df)} samples ({len(val_df)/len(merged)*100:.1f}%) -> {val_path}")
    print(f"    Test:  {len(test_df)} samples ({len(test_df)/len(merged)*100:.1f}%) -> {test_path}")

    return train_df, val_df, test_df


if __name__ == "__main__":
    clean_and_merge()
