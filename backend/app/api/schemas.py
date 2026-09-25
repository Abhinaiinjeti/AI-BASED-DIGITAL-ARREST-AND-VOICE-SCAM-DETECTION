"""
Pydantic Schemas for API Requests & Responses
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class TextAnalysisRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=15000, description="Input message or conversation text")
    language: Optional[str] = Field(None, description="Optional manual language override")


class IndicatorItem(BaseModel):
    id: str
    indicator: str
    category: str
    severity: str
    explanation: str
    evidence: str
    all_evidence: List[str] = []
    match_count: int = 1


class PipelineStageInfo(BaseModel):
    stage_id: str
    name: str
    description: str
    status: str
    output_summary: str


class AnalysisResponse(BaseModel):
    success: bool
    input_type: str = "text"  # "text" or "voice"
    transcript: Optional[str] = None
    audio_duration: Optional[float] = None
    language: str
    language_confidence: float
    is_language_uncertain: bool = False
    classification: str       # "Scam" or "Legitimate"
    scam_category: str        # e.g. "police_digital_arrest", "bank_kyc", "none"
    model_confidence: float   # 0.0 to 1.0 (ML probability)
    scam_probability: float   # 0.0 to 1.0
    risk_score: int           # 0 to 100
    risk_level: str           # "LOW", "SUSPICIOUS", "HIGH", "VERY HIGH"
    risk_badge: str
    color_theme: str
    is_digital_arrest: bool
    indicators: List[IndicatorItem] = []
    recommendation: str
    pipeline_stages: List[PipelineStageInfo] = []
    error: Optional[str] = None


class HistoryItem(BaseModel):
    id: int
    timestamp: str
    input_type: str
    detected_language: str
    classification: str
    scam_category: str
    risk_level: str
    risk_score: int
    model_confidence: float
    indicator_count: int
    is_digital_arrest: int
    duration_seconds: float


class StatsResponse(BaseModel):
    has_data: bool
    total_analyses: int
    scam_detections: int
    digital_arrest_detections: int
    high_risk_detections: int
    text_analyses: int
    voice_analyses: int
    avg_risk_score: float
    risk_distribution: List[Dict[str, Any]]
    category_distribution: List[Dict[str, Any]]
    language_distribution: List[Dict[str, Any]]


class DemoPreset(BaseModel):
    id: str
    title: str
    category: str
    language: str
    expected_risk: str
    description: str
    text: str
