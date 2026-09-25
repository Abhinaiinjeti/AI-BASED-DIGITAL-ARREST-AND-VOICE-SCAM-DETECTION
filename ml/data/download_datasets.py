"""
Dataset Ingestion Module
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Downloads and extracts verified real-world scam and fraud text datasets:
1. Secondary Dataset: Indian Cyber Scam PhoneCall / 10k Dataset (Hinglish/English)
2. Primary Dataset: INDICA / IndiF text subset (English, Hindi, Telugu)
"""

import os
import sys
import tarfile
import requests
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"
INDIAN_SCAM_DIR = RAW_DATA_DIR / "indian_scam"
INDICA_DIR = RAW_DATA_DIR / "indica"

INDIAN_SCAM_URL = (
    "https://huggingface.co/datasets/ysangam/"
    "Indian_Cyber_Scam_PhoneCall_Hinglish_Dataset/resolve/main/"
    "India_Cyber_Scam_Hinglish_Dataset.csv"
)

INDICA_TEXT_URL = (
    "https://huggingface.co/datasets/vikrant-vikram/INDICA/resolve/main/Text_samples.tar.gz"
)


def download_file(url: str, dest_path: Path, chunk_size: int = 1024 * 1024) -> bool:
    """Download a file with progress reporting."""
    print(f"[*] Downloading {url} -> {dest_path}")
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()
        total_size = int(response.headers.get("content-length", 0))
        downloaded = 0
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(
                            f"\r    Downloaded {downloaded / (1024*1024):.2f}MB / "
                            f"{total_size / (1024*1024):.2f}MB ({percent:.1f}%)",
                            end="",
                            flush=True,
                        )
                    else:
                        print(
                            f"\r    Downloaded {downloaded / (1024*1024):.2f}MB",
                            end="",
                            flush=True,
                        )
        print("\n[+] Download complete.")
        return True
    except Exception as e:
        print(f"\n[-] Error downloading from {url}: {e}")
        if dest_path.exists():
            dest_path.unlink()
        return False


def download_indian_scam_dataset() -> bool:
    """Download the Indian Cyber Scam 10k CSV dataset."""
    dest = INDIAN_SCAM_DIR / "India_Cyber_Scam_Hinglish_Dataset.csv"
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"[i] Indian Cyber Scam dataset already exists at {dest} ({dest.stat().st_size} bytes)")
        return True
    return download_file(INDIAN_SCAM_URL, dest)


def download_and_extract_indica_subset(max_samples_per_lang: int = 1500) -> bool:
    """
    Stream and extract target language subsets (Telugu, Hindi, English)
    from the INDICA Text_samples archive without keeping unneeded languages.
    """
    target_prefixes = {
        "Text_samples/Text_telugu": "telugu",
        "Text_samples/Text_hindi": "hindi",
        "Text_samples/Text_english": "english",
    }

    INDICA_DIR.mkdir(parents=True, exist_ok=True)
    tar_archive_path = INDICA_DIR / "Text_samples.tar.gz"

    # Step 1: Download archive if not present
    if not tar_archive_path.exists() or tar_archive_path.stat().st_size < 100000:
        print("[*] Downloading INDICA Text_samples.tar.gz archive (~77MB)...")
        success = download_file(INDICA_TEXT_URL, tar_archive_path)
        if not success:
            print("[-] Could not download INDICA text archive.")
            return False
    else:
        print(f"[i] INDICA text archive already exists at {tar_archive_path}")

    # Step 2: Extract relevant languages
    print("[*] Extracting target language subsets (English, Hindi, Telugu)...")
    extracted_counts = {lang: 0 for lang in target_prefixes.values()}

    try:
        with tarfile.open(tar_archive_path, "r:gz") as tar:
            for member in tar:
                # Find matching target prefix
                matched_lang = None
                for prefix, lang in target_prefixes.items():
                    if member.name.startswith(prefix) and member.isfile() and member.name.endswith(".txt"):
                        matched_lang = lang
                        break

                if matched_lang:
                    if extracted_counts[matched_lang] < max_samples_per_lang:
                        # Extract this file
                        tar.extract(member, path=INDICA_DIR)
                        extracted_counts[matched_lang] += 1
                        if extracted_counts[matched_lang] % 250 == 0:
                            print(
                                f"    Extracted {extracted_counts[matched_lang]} samples for {matched_lang}"
                            )

        print("[+] INDICA extraction summary:")
        for lang, count in extracted_counts.items():
            print(f"    - {lang.capitalize()}: {count} samples extracted")
        return True
    except Exception as e:
        print(f"[-] Error extracting INDICA archive: {e}")
        return False


def main():
    print("=" * 60)
    print("AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION")
    print("Dataset Ingestion Pipeline")
    print("=" * 60)

    print("\n1. Ingesting Secondary Dataset (Indian Cyber Scam 10k)...")
    scam_ok = download_indian_scam_dataset()

    print("\n2. Ingesting Primary Dataset (INDICA / IndiF text subsets)...")
    indica_ok = download_and_extract_indica_subset()

    if scam_ok or indica_ok:
        print("\n[+] Ingestion step completed successfully.")
    else:
        print("\n[-] Ingestion encountered issues. Check network connection.")


if __name__ == "__main__":
    main()
