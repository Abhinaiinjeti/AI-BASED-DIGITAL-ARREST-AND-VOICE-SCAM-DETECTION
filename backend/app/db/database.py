"""
SQLite Database Module for Privacy-First History & Analytics
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Stores:
- Analysis metadata (timestamp, input_type, detected_language, classification, risk_level, risk_score)
- Privacy-first: Does NOT store raw sensitive conversation text or audio by default.
- Provides queries for real aggregate stats and history audit trails.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any, Optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DB_DIR = BASE_DIR / "backend" / "data"
DB_PATH = DB_DIR / "scam_detection.db"


def get_db_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Initialize database tables."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            input_type TEXT NOT NULL,         -- 'text' or 'voice'
            detected_language TEXT NOT NULL,
            classification TEXT NOT NULL,     -- 'Scam' or 'Legitimate'
            scam_category TEXT NOT NULL,      -- e.g. 'police_digital_arrest', 'none'
            risk_level TEXT NOT NULL,         -- 'LOW', 'SUSPICIOUS', 'HIGH', 'VERY HIGH'
            risk_score INTEGER NOT NULL,      -- 0 to 100
            model_confidence REAL NOT NULL,   -- 0.0 to 1.0
            indicator_count INTEGER NOT NULL,
            is_digital_arrest INTEGER NOT NULL DEFAULT 0,
            duration_seconds REAL DEFAULT 0.0
        )
    """)

    conn.commit()
    conn.close()


def record_analysis(
    input_type: str,
    detected_language: str,
    classification: str,
    scam_category: str,
    risk_level: str,
    risk_score: int,
    model_confidence: float,
    indicator_count: int,
    is_digital_arrest: bool = False,
    duration_seconds: float = 0.0,
) -> int:
    """Insert a privacy-preserving analysis record."""
    conn = get_db_connection()
    cursor = conn.cursor()

    timestamp = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO analysis_history (
            timestamp, input_type, detected_language, classification,
            scam_category, risk_level, risk_score, model_confidence,
            indicator_count, is_digital_arrest, duration_seconds
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        timestamp,
        input_type,
        detected_language,
        classification,
        scam_category,
        risk_level,
        int(risk_score),
        float(model_confidence),
        int(indicator_count),
        1 if is_digital_arrest else 0,
        float(duration_seconds),
    ))

    record_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return record_id


def get_history(limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
    """Retrieve recent analysis history."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM analysis_history
        ORDER BY id DESC
        LIMIT ? OFFSET ?
    """, (limit, offset))

    rows = cursor.fetchall()
    conn.close()

    return [dict(r) for r in rows]


def clear_history():
    """Purge all history records for privacy."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM analysis_history")
    conn.commit()
    conn.close()


def get_aggregate_stats() -> Dict[str, Any]:
    """
    Compute aggregate dashboard statistics from REAL database records.
    Returns empty structures if no analyses have been performed.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM analysis_history")
    total_count = cursor.fetchone()[0]

    if total_count == 0:
        conn.close()
        return {
            "has_data": False,
            "total_analyses": 0,
            "scam_detections": 0,
            "digital_arrest_detections": 0,
            "high_risk_detections": 0,
            "text_analyses": 0,
            "voice_analyses": 0,
            "avg_risk_score": 0.0,
            "risk_distribution": [],
            "category_distribution": [],
            "language_distribution": [],
        }

    # Counts
    cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE classification = 'Scam'")
    scam_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE is_digital_arrest = 1")
    da_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE risk_level IN ('HIGH', 'VERY HIGH')")
    high_risk_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE input_type = 'text'")
    text_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM analysis_history WHERE input_type = 'voice'")
    voice_count = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(risk_score) FROM analysis_history")
    avg_score = round(cursor.fetchone()[0] or 0.0, 1)

    # Risk level distribution
    cursor.execute("SELECT risk_level, COUNT(*) as count FROM analysis_history GROUP BY risk_level")
    risk_dist = [{"level": r["risk_level"], "count": r["count"]} for r in cursor.fetchall()]

    # Category distribution
    cursor.execute("SELECT scam_category, COUNT(*) as count FROM analysis_history GROUP BY scam_category")
    cat_dist = [{"category": r["scam_category"], "count": r["count"]} for r in cursor.fetchall()]

    # Language distribution
    cursor.execute("SELECT detected_language, COUNT(*) as count FROM analysis_history GROUP BY detected_language")
    lang_dist = [{"language": r["detected_language"], "count": r["count"]} for r in cursor.fetchall()]

    conn.close()

    return {
        "has_data": True,
        "total_analyses": total_count,
        "scam_detections": scam_count,
        "digital_arrest_detections": da_count,
        "high_risk_detections": high_risk_count,
        "text_analyses": text_count,
        "voice_analyses": voice_count,
        "avg_risk_score": avg_score,
        "risk_distribution": risk_dist,
        "category_distribution": cat_dist,
        "language_distribution": lang_dist,
    }


# Auto-initialize on import
init_db()
