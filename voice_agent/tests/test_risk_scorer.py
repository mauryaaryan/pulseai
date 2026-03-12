import unittest
from services.risk_scorer import RiskScorer

class TestRiskScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = RiskScorer()

    def test_risk_calculation_medium(self):
        nlp_data = {
            "symptoms": [
                {"name": "chest pain", "severity": "severe", "duration": "2 days", "triggers": ["exertion"], "context_score": 95},
                {"name": "breathlessness", "severity": "moderate", "duration": "2 days", "triggers": ["exertion"], "context_score": 85}
            ],
            "comorbidities": ["diabetes", "hypertension"],
            "detected_patterns": ["cardiac_pattern"]
        }

        res = self.scorer.calculate_risk_score("session-123", nlp_data)
        
        # High score expected given cardiac pattern
        self.assertGreaterEqual(res['total_risk_score'], 35)
        self.assertIn(res['risk_level'], ["MEDIUM", "HIGH"])

    def test_risk_calculation_low(self):
        nlp_data = {
            "symptoms": [
                {"name": "fatigue", "severity": "mild", "duration": "1 week", "triggers": [], "context_score": 10}
            ],
            "comorbidities": [],
            "detected_patterns": []
        }

        res = self.scorer.calculate_risk_score("session-456", nlp_data)
        self.assertEqual(res['risk_level'], "LOW")

if __name__ == '__main__':
    unittest.main()
