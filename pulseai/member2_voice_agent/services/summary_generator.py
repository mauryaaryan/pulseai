import uuid
import json

class SummaryGenerator:
    """Generates medical summaries based on NLP findings and Risk evaluations."""

    def generate_summary(self, session_id: str, nlp_analysis: dict, risk_analysis: dict, format_type: str = "structured") -> dict:
        summary_text = ""
        key_findings = self._extract_key_findings(nlp_analysis, risk_analysis)
        
        if format_type == "concise":
            summary_text = self._generate_concise_summary(nlp_analysis, risk_analysis)
        elif format_type == "detailed":
            summary_text = self._generate_detailed_summary(nlp_analysis, risk_analysis)
        else: # structured default
            summary_text = json.dumps(key_findings)

        return {
            "summary_id": str(uuid.uuid4()),
            "session_id": session_id,
            "format": format_type,
            "summary_text": summary_text,
            "key_findings": key_findings
        }

    def _extract_key_findings(self, nlp, risk) -> dict:
        chief_complaint = "Unknown"
        if nlp["symptoms"]:
            # sort symptoms by context score descending to find chief complaint
            sorted_symp = sorted(nlp["symptoms"], key=lambda k: k.get('context_score', 0), reverse=True)
            chief_complaint = sorted_symp[0]["name"]
            
        return {
            "chief_complaint": chief_complaint,
            "symptoms": nlp["symptoms"],
            "comorbidities": nlp["comorbidities"],
            "clinical_pattern": nlp["detected_patterns"][0] if nlp["detected_patterns"] else "none",
            "risk_score": risk["total_risk_score"],
            "risk_level": risk["risk_level"],
            "recommendation": risk["recommended_priority"]
        }

    def _generate_concise_summary(self, nlp, risk) -> str:
        chief = self._extract_key_findings(nlp, risk)["chief_complaint"]
        
        symptoms_str = "\n".join([f"- {s['name'].title()}: {s['severity'].title()}, Triggered by: {', '.join(s['triggers']) if s['triggers'] else 'None reported'}" for s in nlp['symptoms']])
        comorb_str = "\n".join([f"- {c.title()} " for c in nlp['comorbidities']]) if nlp['comorbidities'] else "None reported"
        patterns_str = ", ".join(nlp['detected_patterns']) if nlp['detected_patterns'] else "None specific"
        
        return f"""CHIEF COMPLAINT: {chief.title()}

SYMPTOM DETAILS:
{symptoms_str}

RELEVANT MEDICAL HISTORY:
{comorb_str}

RISK ASSESSMENT: {risk['risk_level']} (Score {risk['total_risk_score']}/100)
Pattern: {patterns_str}
Reasoning: {risk['risk_reasoning']}

RECOMMENDATION: {risk['recommended_priority']}
"""

    def _generate_detailed_summary(self, nlp, risk) -> str:
        # A simple expansion of the concise format for completeness.
        base = self._generate_concise_summary(nlp, risk)
        return "DETAILED MEDICAL INTAKE REPORT\n" + "-"*30 + "\n" + base + "\n\nEnd of auto-generated physician report."

