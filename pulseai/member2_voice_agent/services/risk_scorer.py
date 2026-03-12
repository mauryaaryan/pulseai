import uuid
from datetime import datetime
from utils.medical_dictionaries import COMORBIDITIES

class RiskScorer:
    """Calculates risk based on a 4-factor weighted model."""
    
    def calculate_risk_score(self, session_id: str, nlp_analysis: dict) -> dict:
        s_score = self._calculate_symptom_severity(nlp_analysis["symptoms"])
        u_score = self._calculate_medical_urgency(nlp_analysis["symptoms"], nlp_analysis["detected_patterns"])
        c_score = self._calculate_comorbidity_risk(nlp_analysis["comorbidities"])
        d_score = self._calculate_duration_trend(nlp_analysis["symptoms"])

        # Weights applied exactly as specified
        total_score_exact = (s_score * 0.40) + (u_score * 0.30) + (c_score * 0.20) + (d_score * 0.10)
        total_score = min(round(total_score_exact), 100)

        risk_level = self._determine_risk_level(total_score)
        
        reasoning = self._generate_risk_explanation(total_score, s_score, u_score, c_score, d_score, nlp_analysis)

        return {
            "analysis_id": str(uuid.uuid4()),
            "session_id": session_id,
            "symptom_severity_score": s_score,
            "urgency_score": u_score,
            "comorbidity_score": int(c_score),
            "duration_trend_score": d_score,
            "total_risk_score": total_score,
            "risk_level": risk_level,
            "risk_reasoning": reasoning,
            "recommended_priority": self._get_priority_recommendation(risk_level, nlp_analysis["detected_patterns"])
        }

    def _calculate_symptom_severity(self, symptoms: list) -> int:
        if not symptoms: return 0
        points = 0
        severe_count = 0
        for s in symptoms:
            if s['severity'] == 'severe':
                points += 30
                severe_count += 1
            elif s['severity'] == 'moderate':
                points += 15
            else:
                points += 5
        
        if severe_count > 1:
            points += 5
            
        return min(points, 100)

    def _calculate_medical_urgency(self, symptoms: list, patterns: list) -> int:
        points = 0
        for s in symptoms:
            if s['name'] in ['chest pain', 'severe chest pain', 'shortness of breath']:
                points += 25
            elif s['name'] in ['breathlessness']:
                points += 10
            elif s['context_score'] > 80:
                points += 20
        
        if len(patterns) > 0:
            points += 20
            
        return min((points * 100) // 55 if points <= 55 else points, 100) 

    def _calculate_comorbidity_risk(self, comorbidities: list) -> float:
        if not comorbidities: return 0.0
        points = 0
        for c in comorbidities:
            points += COMORBIDITIES.get(c, 0)
        
        if len(comorbidities) > 1:
            points *= 1.2
            
        # Normalizing to 100 scale based on max expected around 50 points
        return min((points * 100) // 20 if points <= 20 else points * 5, 100)

    def _calculate_duration_trend(self, symptoms: list) -> int:
        points = 0
        for s in symptoms:
            if "day" in s['duration'] or "hour" in s['duration']:
                points += 50
        return min(points, 100)

    def _determine_risk_level(self, score: int) -> str:
        if score <= 35: return "LOW"
        if score <= 65: return "MEDIUM"
        return "HIGH"

    def _generate_risk_explanation(self, total, s, u, c, d, nlp) -> str:
        exp = f"Calculated score: {total}/100. "
        if s > 0: exp += f"Base severity logic applied based on contextual symptoms ({len(nlp['symptoms'])} identified). "
        if u > 0: exp += "Critical symptoms/patterns identified increasing urgency weight. "
        if c > 0: exp += f"Comorbidities ({', '.join(nlp['comorbidities'])}) acted as multipliers. "
        if d > 0: exp += "Acute timeline elevated trends risk."
        return exp

    def _get_priority_recommendation(self, level: str, patterns: list) -> str:
        if "cardiac_pattern" in patterns or level == "HIGH":
            return "Urgent: Schedule same-day or next-day appointment."
        elif level == "MEDIUM":
            return "Schedule within 3-5 days. Preference for earlier due to elevated factors."
        return "Schedule routine appointment."
