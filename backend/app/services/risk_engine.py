"""
Risk Scoring & Explainability Engine
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Calculates an integrated Risk Score (0 - 100) combining:
1. Machine Learning classification confidence & probability
2. Detected rule-based indicators and their severities
3. Digital arrest coercion markers (Video isolation, Authority impersonation, Arrest threats)

Distinguishes:
- Model Confidence (ML probability, e.g., 91%)
- Risk Score (Holistic threat index, e.g., 87/100)

Risk Tiers:
- 0 - 25: LOW RISK
- 26 - 50: SUSPICIOUS
- 51 - 75: HIGH RISK
- 76 - 100: VERY HIGH RISK
"""

from typing import List, Dict, Any


class RiskEngine:
    # Severity weighting factors (Configurable)
    SEVERITY_WEIGHTS = {
        "critical": 25,
        "high": 18,
        "medium": 10,
        "low": 5,
    }

    # ML probability weight (base contribution out of 100)
    ML_BASE_WEIGHT = 45.0

    def calculate_risk(
        self,
        ml_prediction: Dict[str, Any],
        indicators: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Calculate composite risk score and generate contextual explanations.
        """
        is_scam = ml_prediction.get("is_scam", False)
        ml_confidence = ml_prediction.get("confidence", 0.5)
        scam_prob = ml_prediction.get("scam_probability", 1.0 if is_scam else 0.0)

        # 1. Base score from ML probability
        base_score = scam_prob * self.ML_BASE_WEIGHT

        # 2. Indicator severity accumulation
        indicator_score = 0
        has_digital_arrest_pattern = False
        indicator_ids = {ind["id"] for ind in indicators}

        for ind in indicators:
            sev = ind.get("severity", "low")
            indicator_score += self.SEVERITY_WEIGHTS.get(sev, 5)

        # 3. Check specific Digital Arrest compound pattern
        # (Authority + Arrest threat OR Video isolation + Arrest threat)
        if (
            ("AUTH_IMPERSONATION" in indicator_ids and "ARREST_LEGAL_THREAT" in indicator_ids)
            or ("VIDEO_CALL_ISOLATION" in indicator_ids and "ARREST_LEGAL_THREAT" in indicator_ids)
            or ("ARREST_LEGAL_THREAT" in indicator_ids and "FINANCIAL_DEMAND" in indicator_ids)
        ):
            has_digital_arrest_pattern = True
            indicator_score += 15  # Compound digital arrest escalation bonus

        # 4. Total unclipped score
        raw_score = base_score + indicator_score

        # If ML flagged legitimate and NO indicators found, cap at low risk
        if not is_scam and not indicators:
            final_score = min(20, round(raw_score))
        elif is_scam and not indicators:
            # ML detected scam from vocabulary patterns but no specific regex rule triggered
            final_score = min(60, max(35, round(base_score + 15)))
        else:
            final_score = min(100, max(0, round(raw_score)))

        # 5. Determine Risk Tier
        if final_score <= 25:
            risk_level = "LOW"
            risk_badge = "LOW RISK"
            color_theme = "emerald"
        elif final_score <= 50:
            risk_level = "SUSPICIOUS"
            risk_badge = "SUSPICIOUS"
            color_theme = "yellow"
        elif final_score <= 75:
            risk_level = "HIGH"
            risk_badge = "HIGH RISK"
            color_theme = "orange"
        else:
            risk_level = "VERY HIGH"
            risk_badge = "VERY HIGH RISK"
            color_theme = "rose"

        # 6. Generate contextual recommendation
        recommendation = self._generate_recommendation(
            risk_level, has_digital_arrest_pattern, indicator_ids
        )

        return {
            "risk_score": final_score,
            "risk_level": risk_level,
            "risk_badge": risk_badge,
            "color_theme": color_theme,
            "is_digital_arrest": has_digital_arrest_pattern,
            "model_confidence": round(ml_confidence, 4),
            "scam_probability": round(scam_prob, 4),
            "recommendation": recommendation,
        }

    def _generate_recommendation(
        self,
        risk_level: str,
        is_digital_arrest: bool,
        indicator_ids: set,
    ) -> str:
        """Generate specific, actionable advisory."""
        if is_digital_arrest or ("ARREST_LEGAL_THREAT" in indicator_ids and "AUTH_IMPERSONATION" in indicator_ids):
            return (
                "🚨 CRITICAL DIGITAL ARREST ALERT: Under Indian Law, Police, CBI, ED, and Judicial Courts "
                "NEVER conduct trials, investigations, or issue arrest warrants via WhatsApp/Skype video calls. "
                "Disconnect immediately. DO NOT transfer any funds to 'RBI verification' accounts. "
                "Immediately file a complaint on the National Cyber Crime Reporting Portal at https://cybercrime.gov.in "
                "or call the National Cyber Crime Helpline at 1930."
            )
        elif "FINANCIAL_DEMAND" in indicator_ids and "AUTH_IMPERSONATION" in indicator_ids:
            return (
                "⚠️ URGENT FINANCIAL WARNING: Government and police agencies never demand money via UPI, QR codes, "
                "or personal bank accounts. Never disclose OTPs, passwords, or banking credentials. "
                "Block the caller and report the incident on cybercrime.gov.in."
            )
        elif risk_level in ("HIGH", "VERY HIGH"):
            return (
                "⚠️ HIGH FRAUD RISK: This conversation exhibits multiple known cyber fraud characteristics. "
                "Do not click any provided links, do not share sensitive personal information, and discontinue "
                "communication. Contact official customer support through their verified public website."
            )
        elif risk_level == "SUSPICIOUS":
            return (
                "ℹ️ SUSPICIOUS ACTIVITY: This message contains potential warning indicators. "
                "Verify the caller's credentials independently before taking any requested actions or sharing information."
            )
        else:
            return (
                "✅ LOW RISK: No significant scam patterns detected. Exercise normal cybersecurity hygiene and "
                "never share private financial credentials with unsolicited contacts."
            )


# Singleton
risk_engine = RiskEngine()
