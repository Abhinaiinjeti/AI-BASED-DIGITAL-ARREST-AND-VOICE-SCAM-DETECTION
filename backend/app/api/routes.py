"""
API Endpoints Router
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import List, Optional
from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query

from backend.app.api.schemas import (
    TextAnalysisRequest,
    AnalysisResponse,
    IndicatorItem,
    PipelineStageInfo,
    HistoryItem,
    StatsResponse,
    DemoPreset,
)
from backend.app.services.language_service import language_service
from backend.app.services.indicator_engine import indicator_engine
from backend.app.services.risk_engine import risk_engine
from backend.app.services.audio_service import audio_service
from backend.app.db.database import (
    record_analysis,
    get_history,
    clear_history,
    get_aggregate_stats,
)
from ml.inference.predict import get_predictor

router = APIRouter()


def build_pipeline_stages(
    text: str,
    lang_info: dict,
    ml_pred: dict,
    indicators: list,
    risk_res: dict,
    audio_dur: Optional[float] = None,
) -> List[PipelineStageInfo]:
    """Construct factual execution stages for the animated UI pipeline."""
    stages = []

    # Stage 0: Audio (if voice)
    if audio_dur is not None:
        stages.append(PipelineStageInfo(
            stage_id="audio_stt",
            name="Speech Recognition",
            description="Transcribed via Faster-Whisper",
            status="completed",
            output_summary=f"{audio_dur:.1f}s audio transcribed",
        ))

    # Stage 1: Input & Language
    stages.append(PipelineStageInfo(
        stage_id="language_id",
        name="Language Identification",
        description="Analyzed character scripts and phonetic dictionaries",
        status="completed",
        output_summary=f"{lang_info['language']} ({lang_info['confidence']*100:.0f}% confidence)",
    ))

    # Stage 2: Preprocessing
    stages.append(PipelineStageInfo(
        stage_id="preprocessing",
        name="Text Preprocessing",
        description="Preserved critical legal & authority tokens",
        status="completed",
        output_summary=f"{len(ml_pred['cleaned_text'].split())} normalized tokens",
    ))

    # Stage 3: TF-IDF & ML Classification
    stages.append(PipelineStageInfo(
        stage_id="ml_classifier",
        name="TF-IDF & ML Classifier",
        description="Vectorized and classified via trained model",
        status="completed",
        output_summary=f"{ml_pred['label']} ({ml_pred['confidence']*100:.1f}% confidence)",
    ))

    # Stage 4: Digital Arrest Indicator Engine
    stages.append(PipelineStageInfo(
        stage_id="indicator_engine",
        name="Digital Arrest Indicator Engine",
        description="Rule & pattern matching against coercive fraud vectors",
        status="completed",
        output_summary=f"{len(indicators)} suspicious indicators flagged",
    ))

    # Stage 5: Multi-Factor Risk Scoring
    stages.append(PipelineStageInfo(
        stage_id="risk_scoring",
        name="Risk & Explainability Engine",
        description="Synthesized composite risk score and contextual advisory",
        status="completed",
        output_summary=f"Risk Score {risk_res['risk_score']}/100 ({risk_res['risk_level']})",
    ))

    return stages


@router.get("/health")
def health_check():
    """Health check endpoint."""
    predictor = get_predictor()
    return {
        "status": "online",
        "project_title": "AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION",
        "model_loaded": predictor.classifier is not None,
        "selected_model": predictor.metadata.get("selected_model", "Unknown"),
        "whisper_ready": True,
    }


@router.get("/models/info")
def get_model_info():
    """Return trained model metadata and benchmark evaluation stats."""
    predictor = get_predictor()
    return predictor.metadata


@router.post("/analyze/text", response_model=AnalysisResponse)
def analyze_text(request: TextAnalysisRequest):
    """
    Execute full text analysis pipeline on suspicious message/text.
    """
    raw_text = request.text.strip()
    if not raw_text:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    predictor = get_predictor()

    # 1. Language Detection (Honest, returns 'Language uncertain' if ambiguous)
    if request.language:
        lang_info = {
            "language": request.language,
            "confidence": 1.0,
            "is_uncertain": False,
            "script": "manual_override",
        }
    else:
        lang_info = language_service.detect_language(raw_text)

    # 2. ML Prediction (TF-IDF + Classifier)
    ml_pred = predictor.predict(raw_text)

    # 3. Rule-based Digital Arrest Indicator Engine
    indicators_raw = indicator_engine.scan_indicators(raw_text)
    indicator_items = [IndicatorItem(**ind) for ind in indicators_raw]

    # 4. Composite Risk Engine
    risk_res = risk_engine.calculate_risk(ml_pred, indicators_raw)

    # 5. Log to SQLite database (Privacy-first: no raw sensitive text stored)
    record_analysis(
        input_type="text",
        detected_language=lang_info["language"],
        classification=ml_pred["label"],
        scam_category=ml_pred["scam_category"],
        risk_level=risk_res["risk_level"],
        risk_score=risk_res["risk_score"],
        model_confidence=ml_pred["confidence"],
        indicator_count=len(indicator_items),
        is_digital_arrest=risk_res["is_digital_arrest"],
    )

    # 6. Build animated pipeline stages
    stages = build_pipeline_stages(
        raw_text, lang_info, ml_pred, indicators_raw, risk_res
    )

    return AnalysisResponse(
        success=True,
        input_type="text",
        transcript=None,
        audio_duration=None,
        language=lang_info["language"],
        language_confidence=lang_info["confidence"],
        is_language_uncertain=lang_info["is_uncertain"],
        classification=ml_pred["label"],
        scam_category=ml_pred["scam_category"],
        model_confidence=ml_pred["confidence"],
        scam_probability=ml_pred["scam_probability"],
        risk_score=risk_res["risk_score"],
        risk_level=risk_res["risk_level"],
        risk_badge=risk_res["risk_badge"],
        color_theme=risk_res["color_theme"],
        is_digital_arrest=risk_res["is_digital_arrest"],
        indicators=indicator_items,
        recommendation=risk_res["recommendation"],
        pipeline_stages=stages,
    )


@router.post("/analyze/audio", response_model=AnalysisResponse)
async def analyze_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
):
    """
    Execute full voice analysis pipeline:
    Validate Audio -> FFmpeg Conversion -> Faster-Whisper Speech-to-Text -> Text Preprocessing -> ML -> Indicators -> Risk.
    """
    filename = file.filename or "recording.wav"
    ext = Path(filename).suffix.lower() if filename else ".wav"
    if ext not in audio_service.ALLOWED_EXTENSIONS:
        allowed_list = ", ".join(sorted(audio_service.ALLOWED_EXTENSIONS))
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format '{ext}'. Supported formats: {allowed_list}",
        )

    # Save to temporary file securely
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = Path(tmp.name)

    try:
        # Transcribe with Faster-Whisper
        whisper_lang = None
        if language and language.strip().lower() not in ("auto", "", "none"):
            whisper_lang = language.strip().lower()

        transcription = audio_service.transcribe(tmp_path, language=whisper_lang)

        if not transcription["success"]:
            err_type = transcription.get("error_type", "transcription_error")
            status_code = 422
            if err_type == "unsupported_format":
                status_code = 400
            elif err_type == "ffmpeg_missing":
                status_code = 503
            elif err_type == "model_error":
                status_code = 500

            raise HTTPException(
                status_code=status_code,
                detail=transcription.get("error", "Failed to transcribe audio."),
            )

        transcript_text = transcription["transcript"]
        audio_duration = transcription["duration"]
        detected_lang = transcription.get("detected_language", "English")
        lang_conf = transcription.get("language_confidence", 0.95)

        # Downstream NLP & ML Classification
        try:
            predictor = get_predictor()
            lang_info = language_service.detect_language(transcript_text)
            ml_pred = predictor.predict(transcript_text)
            indicators_raw = indicator_engine.scan_indicators(transcript_text)
            indicator_items = [IndicatorItem(**ind) for ind in indicators_raw]
            risk_res = risk_engine.calculate_risk(ml_pred, indicators_raw)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Downstream scam classification failed on extracted transcript: {str(e)}",
            )

        # Log to SQLite
        record_analysis(
            input_type="voice",
            detected_language=detected_lang,
            classification=ml_pred["label"],
            scam_category=ml_pred["scam_category"],
            risk_level=risk_res["risk_level"],
            risk_score=risk_res["risk_score"],
            model_confidence=ml_pred["confidence"],
            indicator_count=len(indicator_items),
            is_digital_arrest=risk_res["is_digital_arrest"],
            duration_seconds=audio_duration,
        )

        stages = build_pipeline_stages(
            transcript_text,
            lang_info,
            ml_pred,
            indicators_raw,
            risk_res,
            audio_dur=audio_duration,
        )

        return AnalysisResponse(
            success=True,
            input_type="voice",
            transcript=transcript_text,
            audio_duration=audio_duration,
            duration=audio_duration,
            audio_format=transcription.get("audio_format", ext.replace(".", "").upper()),
            speech_detected=True,
            language=detected_lang,
            language_confidence=lang_conf,
            is_language_uncertain=lang_info.get("is_uncertain", False),
            classification=ml_pred["label"],
            scam_category=ml_pred["scam_category"],
            model_confidence=ml_pred["confidence"],
            confidence=ml_pred["confidence"],
            scam_probability=ml_pred["scam_probability"],
            risk_score=risk_res["risk_score"],
            risk_level=risk_res["risk_level"],
            risk_badge=risk_res["risk_badge"],
            color_theme=risk_res["color_theme"],
            is_digital_arrest=risk_res["is_digital_arrest"],
            indicators=indicator_items,
            recommendation=risk_res["recommendation"],
            pipeline_stages=stages,
            diagnostics=transcription.get("diagnostics"),
        )

    finally:
        # Clean up temporary file
        if tmp_path.exists():
            tmp_path.unlink()


@router.get("/history", response_model=List[HistoryItem])
def get_analysis_history(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    """Retrieve recent analysis audit logs."""
    return get_history(limit=limit, offset=offset)


@router.delete("/history")
def delete_history():
    """Purge all history records for privacy compliance."""
    clear_history()
    return {"success": True, "message": "History purged successfully."}


@router.get("/stats", response_model=StatsResponse)
def get_statistics():
    """Retrieve real aggregate statistics for the dashboard."""
    return get_aggregate_stats()


@router.get("/demos", response_model=List[DemoPreset])
def get_demo_presets():
    """
    Return authentic test demonstrations clearly labeled as Demo Examples.
    """
    return [
        DemoPreset(
            id="demo_cbi_digital_arrest",
            title="Digital Arrest Threat (CBI / Mumbai Cyber Police)",
            category="police_digital_arrest",
            language="Hinglish",
            expected_risk="VERY HIGH",
            description="Classic Digital Arrest coercion: Accusation of MDMA narcotics found in customs parcel, demand to stay on Skype video call, and threat of non-bailable arrest warrant.",
            text="This is DCP Ramesh Kumar from Cyber Crime Branch. An international parcel sent from Taiwan in your name contains 150 grams of MDMA drugs and fake passports. A non-bailable arrest warrant has been issued against you under the NDPS Act. You are under digital arrest right now. Do not disconnect this WhatsApp video call and keep your camera turned on. You must transfer 50,000 rupees to the RBI security verification account within 15 minutes or police will raid your house immediately.",
        ),
        DemoPreset(
            id="demo_bank_kyc",
            title="Banking KYC Account Block Scam",
            category="bank_kyc",
            language="Hinglish",
            expected_risk="HIGH",
            description="Banking impersonation: False claim of account suspension within 2 hours unless immediate OTP is provided.",
            text="Ji namaskar, SBI bank head office se call hai. Aapka bank KYC document expire ho gaya hai aur aapka account 2 ghante mein permanently block ho jayega. Turant apne registered mobile number par aaya hua 6-digit OTP share kijiye aur pan card details update karein.",
        ),
        DemoPreset(
            id="demo_telugu_loan",
            title="Telugu Loan / Prize Fraud (Native Script)",
            category="telugu_telecom_fraud",
            language="Telugu",
            expected_risk="HIGH",
            description="Indic telecom fraud: Pre-approved instant loan with upfront processing fee demand in native Telugu script.",
            text="హలో నమస్కారం, మేము బ్యాంక్ కస్టమర్ సర్వీస్ నుండి కాల్ చేస్తున్నాము. మీ పేరుపై 5 లక్షల రూపాయల ప్రీ-అప్రూవ్డ్ రుణం మంజూరు చేయబడింది. వడ్డీ రేటు చాలా తక్కువగా ఉంది. ఈ మొత్తాన్ని వెంటనే మీ ఖాతాలో జమ చేయడానికి 2,500 ప్రాసెసింగ్ ఫీజును వెంటనే యూపీఐ ద్వారా బదిలీ చేయండి.",
        ),
        DemoPreset(
            id="demo_benign_convo",
            title="Legitimate Daily Conversation (Safe)",
            category="none",
            language="Hinglish",
            expected_risk="LOW",
            description="Normal everyday conversation regarding groceries and family arrival without any threats or financial demands.",
            text="Hello ji Beta ghar aa gaya hoon, darwaza khol do. Sham ke dinner ke liye sabzi le li hai. Project ka review meeting kaisa raha?",
        ),
    ]
