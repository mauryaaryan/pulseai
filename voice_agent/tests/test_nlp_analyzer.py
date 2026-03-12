import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import unittest
from services.nlp_analyzer import NLPAnalyzer

class TestNLPAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = NLPAnalyzer()

    def test_sentence_tokenization(self):
        text = "I have chest pain. It hurts when I walk."
        result = self.analyzer.analyze_transcript(text)
        self.assertTrue(len(result['symptoms']) >= 1)

    def test_contextual_extraction_not_just_keywords(self):
        """Test that 'severe chest pain' evaluates contextually correctly compared to just 'chest pain'"""
        severe_text = "I have been experiencing severe chest pain."
        mild_text = "I have mild chest pain."

        severe_res = self.analyzer.analyze_transcript(severe_text)
        mild_res = self.analyzer.analyze_transcript(mild_text)

        severe_score = severe_res['symptoms'][0]['context_score']
        mild_score = mild_res['symptoms'][0]['context_score']

        self.assertGreater(severe_score, mild_score)
        
    def test_trigger_extraction(self):
        text = "I feel breathless when I walk"
        res = self.analyzer.analyze_transcript(text)
        
        symptom = res['symptoms'][0]
        self.assertIn("exertion", symptom['triggers'])

    def test_pattern_detection(self):
        text = "I have chest pain and breathlessness and sometimes I feel dizzy."
        res = self.analyzer.analyze_transcript(text)
        self.assertIn("cardiac_pattern", res['detected_patterns'])
        self.assertEqual(res['urgency_level'], "critical")

if __name__ == '__main__':
    unittest.main()
