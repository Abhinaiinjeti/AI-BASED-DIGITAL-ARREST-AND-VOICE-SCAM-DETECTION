"""
Digital Arrest & Scam Indicator Engine
AI-BASED DIGITAL ARREST AND VOICE SCAM DETECTION

Transparent, rule- and pattern-based explainable indicator engine covering:
1. Authority Impersonation (Police, CBI, ED, Customs, Cyber Cell, Court)
2. Arrest & Legal Threats (Arrest warrant, FIR, Jail, Non-bailable warrant)
3. Financial Demands (Transfer money, UPI, RBI verification account, OTP)
4. Urgency & Intimidation (Immediate, 10/15 minutes, Do not disconnect)
5. Fear & Coercion (Drugs in parcel, Money laundering, Aadhaar misuse)
6. Isolation & Video-call Surveillance (Stay on video call, Skype, Camera on)

Supports English, Hinglish, Hindi, and Telugu patterns.
Returns structured explainable indicators with matched quotes and severity.
"""

import re
from typing import List, Dict, Any


class DigitalArrestIndicatorEngine:
    def __init__(self):
        self.rules = self._compile_rules()

    def _compile_rules(self) -> List[Dict[str, Any]]:
        return [
            # 1. Authority Impersonation
            {
                "id": "AUTH_IMPERSONATION",
                "indicator": "Law Enforcement / Authority Impersonation",
                "category": "Authority Impersonation",
                "severity": "high",
                "explanation": "Caller or sender falsely claims to represent police, CBI, ED, customs, or judicial authorities.",
                "patterns": [
                    r"\b(?:cbi|enforcement directorate|ed officer|cyber\s*crime\s*(?:cell|police|branch)|customs\s*officer|supreme\s*court|trai|mha|interpol)\b",
                    r"\b(?:police\s*(?:officer|inspector|commissioner|headquarters|station|sub-inspector)|dcp|acp)\b",
                    r"\b(?:thana|pulis|adhikari|cbi\s*afsar|kothwali)\b",
                    # Hindi Devanagari
                    r"(?:सीबीआई|ईडी|पुलिस|कस्टम्स|साइबर\s*क्राइम|थाना|अधिकारी|न्यायालय|सुप्रीम\s*कोर्ट)",
                    # Telugu Script
                    r"(?:పోలీస్|సిబిఐ|ఈడి|కస్టమ్స్|సైబర్\s*క్రైమ్|పోలీస్\s*స్టేషన్|అధికారి|కోర్టు)",
                ],
            },

            # 2. Arrest & Legal Threats (Core Digital Arrest Signal)
            {
                "id": "ARREST_LEGAL_THREAT",
                "indicator": "Arrest Warrant / Legal Threat",
                "category": "Arrest / Legal Threat",
                "severity": "critical",
                "explanation": "Intimidation using threats of immediate arrest, non-bailable warrants, FIRs, or imprisonment.",
                "patterns": [
                    r"\b(?:digital\s*arrest|under\s*arrest|arrest\s*warrant|non[- ]bailable\s*warrant|you\s*will\s*be\s*arrested)\b",
                    r"\b(?:fir\s*registered|criminal\s*case|send\s*police\s*to\s*your\s*house|raid\s*your\s*house)\b",
                    r"\b(?:jail\s*bheja|giraftaar|giraftari|warrant\s*jari|hiraasat|mukadma)\b",
                    # Hindi Devanagari
                    r"(?:डिजिटल\s*अरेस्ट|गिरफ्तार|वारंट|जेल|मुकदमा|एफआईआर|गैर-जमानती)",
                    # Telugu Script
                    r"(?:డిజిటల్\s*అరెస్ట్|అరెస్ట్|వారెంట్|జైలు|కేసు|ఎఫ్ఐఆర్|అరెస్టు\s*చేస్తాము)",
                ],
            },

            # 3. Video-call Surveillance & Isolation (Defining Digital Arrest Mechanism)
            {
                "id": "VIDEO_CALL_ISOLATION",
                "indicator": "Video Call Isolation & Digital Confinement",
                "category": "Video-call / Isolation",
                "severity": "critical",
                "explanation": "Demanding the victim remain continuously on a video call (Skype/WhatsApp) to isolate them from help.",
                "patterns": [
                    r"\b(?:stay\s*on\s*video\s*call|keep\s*camera\s*on|do\s*not\s*disconnect|remain\s*on\s*call)\b",
                    r"\b(?:skype\s*call|whatsapp\s*video|virtual\s*custody|lock\s*(?:the|your)\s*door|do\s*not\s*tell\s*anyone)\b",
                    r"\b(?:camera\s*chalu\s*rakho|call\s*mat\s*kaato|kisi\s*ko\s*mat\s*batao|kamra\s*band\s*karo)\b",
                    # Hindi Devanagari
                    r"(?:वीडियो\s*कॉल\s*पर\s*रहें|कैमरा\s*ऑन\s*रखें|कॉल\s*मत\s*काटना|किसी\s*को\s*मत\s*बताना|कमरा\s*बंद)",
                    # Telugu Script
                    r"(?:వీడియో\s*కాల్|కెమెరా\s*ఆన్|కాల్\s*కట్\s*చేయవద్దు|ఎవరికీ\s*చెప్పవద్దు)",
                ],
            },

            # 4. Fabricated Charges (Narcotics / Money Laundering / Aadhaar misuse)
            {
                "id": "FABRICATED_CHARGES",
                "indicator": "Fabricated Charges & Blackmail",
                "category": "Fear / Manipulation",
                "severity": "high",
                "explanation": "Fabricating allegations of drugs in parcels, illegal money transfers, or Aadhaar identity theft.",
                "patterns": [
                    r"\b(?:parcel\s*(?:contains|has)\s*(?:drugs|mdma|contraband|narcotics)|taiwan|cambodia)\b",
                    r"\b(?:money\s*laundering|illegal\s*transaction|aadhaar\s*(?:card\s*)?misuse|sim\s*cards\s*issued\s*on\s*your\s*name)\b",
                    r"\b(?:nashedi|drugs\s*pakda|dharapakad|kala\s*dhan|hawala|aadhaar\s*link)\b",
                    # Hindi Devanagari
                    r"(?:नशीले\s*पदार्थ|मनी\s*लॉन्ड्रिंग|आधार\s*दुरुपयोग|ड्रग्स|पार्सल|अवैध\s*लेनदेन)",
                    # Telugu Script
                    r"(?:డ్రగ్స్|మనీ\s*లాండరింగ్|ఆధార్\s*దుర్వినియోగం|పార్శిల్|అక్రమ\s*లావాదేవీలు)",
                ],
            },

            # 5. Financial Demands & Extortion
            {
                "id": "FINANCIAL_DEMAND",
                "indicator": "Financial Transfer / Extortion Demand",
                "category": "Financial Demands",
                "severity": "high",
                "explanation": "Demanding direct funds transfer, bail security deposit, or verification payment to a 'safe RBI account'.",
                "patterns": [
                    r"\b(?:transfer\s*(?:money|funds|amount)|send\s*money|deposit\s*into\s*account|security\s*deposit)\b",
                    r"\b(?:rbi\s*(?:verification|clearance|safe)\s*account|clearance\s*fee|bail\s*money|fine\s*payment)\b",
                    r"\b(?:upi|neft|rtgs|otp|bank\s*details|card\s*number|cvv|pin)\b",
                    r"\b(?:paisa\s*transfer|khate\s*mein\s*bhejo|jurmana|zamanat\s*rashi|otp\s*batao)\b",
                    # Hindi Devanagari
                    r"(?:पैसे\s*भेजें|खाते\s*में\s*जमा|ओटीपी|यूपीआई|जुर्माना|जमानत\s*राशि|आरबीआई\s*वेरिफिकेशन)",
                    # Telugu Script
                    r"(?:డబ్బులు\s*పంపండి|ఖాతాలో\s*డిపాజిట్|ఓటీపీ|యూపీఐ|జరిమానా|చెల్లింపు)",
                ],
            },

            # 6. Urgency & Coercive Pressure
            {
                "id": "URGENCY_PRESSURE",
                "indicator": "Urgency & Coercive Pressure",
                "category": "Urgency",
                "severity": "medium",
                "explanation": "Creating extreme panic and time pressure to prevent the victim from seeking second opinions.",
                "patterns": [
                    r"\b(?:immediately|right\s*now|within\s*(?:5|10|15|20|30)\s*minutes|urgent\s*action|time\s*is\s*running\s*out)\b",
                    r"\b(?:do\s*not\s*delay|turant|abhi\s*ke\s*abhi|fauran|jald\s*se\s*jald)\b",
                    # Hindi Devanagari
                    r"(?:तुरंत|अभी\s*के\s*अभी|१०\s*मिनट|समय\s*नहीं\s*है|जल्द\s*से\s*जल्द)",
                    # Telugu Script
                    r"(?:వెంటనే|ఇప్పుడే|తక్షణమే|ఆలస్యం\s*చేయవద్దు)",
                ],
            },
        ]

    def scan_indicators(self, text: str) -> List[Dict[str, Any]]:
        """
        Scan text against all indicator rules and return structured findings.
        """
        if not text:
            return []

        detected = []
        lower_text = text.lower()

        for rule in self.rules:
            matched_evidence = []
            for pattern_str in rule["patterns"]:
                regex = re.compile(pattern_str, re.IGNORECASE)
                for match in regex.finditer(text):
                    snippet = match.group(0).strip()
                    # Capture brief context around match
                    start = max(0, match.start() - 20)
                    end = min(len(text), match.end() + 20)
                    context_snippet = text[start:end].strip()
                    matched_evidence.append(context_snippet)

            if matched_evidence:
                # Deduplicate evidence
                unique_evidence = list(dict.fromkeys(matched_evidence))[:3]
                detected.append({
                    "id": rule["id"],
                    "indicator": rule["indicator"],
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "explanation": rule["explanation"],
                    "evidence": unique_evidence[0] if unique_evidence else "",
                    "all_evidence": unique_evidence,
                    "match_count": len(matched_evidence),
                })

        return detected


# Singleton
indicator_engine = DigitalArrestIndicatorEngine()
