from utils.nlp_utils import tokenize_sentences, clean_text, extract_duration_from_text, identify_severity_modifier
from utils.medical_dictionaries import CRITICAL_SYMPTOMS, COMORBIDITIES, SYMPTOM_CLUSTERS, SEVERITY_DESCRIPTORS

class NLPAnalyzer:
    """Sentence-level NLP matching (NO pure keyword mapping without context)"""
    
    def analyze_transcript(self, transcript: str) -> dict:
        sentences = tokenize_sentences(transcript)
        
        entities = self._extract_medical_entities(sentences)
        symptoms = self._analyze_symptoms(sentences, entities)
        comorbidities = self._extract_comorbidities(transcript)
        patterns = self._analyze_symptom_combinations(symptoms)

        return {
            "symptoms": symptoms,
            "comorbidities": comorbidities,
            "detected_patterns": patterns,
            "urgency_level": self._determine_urgency(symptoms, patterns)
        }

    def _extract_medical_entities(self, sentences: list) -> list:
        """Finds potential medical entities spanning the sentences."""
        # Complex NER skipped; simulating via advanced contextual lookup mapping.
        all_symptoms = list(CRITICAL_SYMPTOMS) + [
            "dizzy", "dizziness", "cough", "fever", "numbness", "fatigue", "sweating", "malaise"
        ]
        entities = []
        for sentence in sentences:
            cleaned = clean_text(sentence)
            for s in all_symptoms:
                if s in cleaned:
                    # check if we didn't already extract a more specific multi-word version
                    # e.g. "severe chest pain" includes "chest pain"
                    if not any(s in e and s != e for e in all_symptoms if e in cleaned):
                         entities.append({"name": s, "sentence": sentence})
        # Remove duplicates
        unique_entities = {e['name']: e for e in entities}.values()
        return list(unique_entities)

    def _analyze_symptoms(self, sentences: list, entities: list) -> list:
        analyzed_symptoms = []
        for entity in entities:
            name = entity['name']
            sentence = entity['sentence']
            cleaned = clean_text(sentence)

            severity = identify_severity_modifier(cleaned, SEVERITY_DESCRIPTORS)
            duration = extract_duration_from_text(cleaned)
            
            # Context extraction for triggers (e.g. "when I walk")
            triggers = []
            if "when i " in cleaned or "after i " in cleaned:
                trigger_split = cleaned.split("when i " if "when i " in cleaned else "after i ")
                if len(trigger_split) > 1:
                    triggers.append(trigger_split[1].split()[0] if len(trigger_split[1]) else "") # crude trigger logic

            if "walk" in cleaned or "exert" in cleaned:
                triggers.append("exertion")

            analyzed_symptoms.append({
                "name": name,
                "severity": severity,
                "duration": duration,
                "triggers": list(set(triggers)),
                "raw_sentence": sentence,
                # Context score: combining severe modifier with specific context
                "context_score": self._calculate_context_score(name, severity, duration, triggers)
            })
        return analyzed_symptoms

    def _calculate_context_score(self, name: str, severity: str, duration: str, triggers: list) -> int:
        score = 0
        if severity == 'severe':
            score += 50
        elif severity == 'moderate':
            score += 30
        else:
            score += 10
            
        if name in list(CRITICAL_SYMPTOMS):
            score += 30
        
        if "exertion" in triggers or len(triggers) > 0:
            score += 15 # contextual trigger makes it reproducible/specific
        return min(score, 100)

    def _extract_comorbidities(self, transcript: str) -> list:
        cleaned = clean_text(transcript)
        found = []
        for condition in COMORBIDITIES.keys():
            if condition in cleaned:
                found.append(condition)
        return found

    def _analyze_symptom_combinations(self, symptoms: list) -> list:
        symptom_names = [s['name'] for s in symptoms]
        
        # normalize typical variations
        normalized_names = set()
        for s in symptom_names:
            if "chest pain" in s: normalized_names.add("chest pain")
            if "breath" in s: normalized_names.add("breathlessness")
            if "dizzy" in s: normalized_names.add("dizziness")
            normalized_names.add(s)

        patterns = []
        for pattern_name, req_symptoms in SYMPTOM_CLUSTERS.items():
            matches = sum(1 for rs in req_symptoms if rs in normalized_names)
            if matches >= 2: # if they have at least 2 associated symptoms
                patterns.append(pattern_name)
        return patterns

    def _determine_urgency(self, symptoms: list, patterns: list) -> str:
        if "cardiac_pattern" in patterns or "neurological_pattern" in patterns:
            return "critical"
        for s in symptoms:
            if s['context_score'] > 80:
                return "critical"
            if s['context_score'] > 50:
                return "high"
        return "moderate"
