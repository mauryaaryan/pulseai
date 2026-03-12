import re
from typing import List

def tokenize_sentences(text: str) -> List[str]:
    """
    Split text into sentences accurately.
    In a real app, spacy's sentencizer is preferred, using regex for simplicity.
    """
    # Simple regex for splitting sentences based on punctuation, handling typical abbreviations slightly
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def clean_text(text: str) -> str:
    """Normalize text lowercasing and cleaning extra whitespace."""
    return re.sub(r'\s+', ' ', text).strip().lower()

def extract_duration_from_text(text: str) -> str:
    """Extract temporal phrases (e.g. 'for 2 days', 'since last week')."""
    # Basic regex to catch typical durations
    match = re.search(r'\b(for|since|during)\s+((the\s+)?(last\s+)?\d+\s+(days?|weeks?|months?|years?|hours?|mins?|minutes?))\b', text, re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return ""

def identify_severity_modifier(text: str, severity_dict: dict) -> str:
    """Identify if subjective adjectives imply mild, moderate, or severe."""
    words = text.lower().split()
    for level, descriptors in severity_dict.items():
        for descriptor in descriptors:
            if descriptor in words:
                return level
    return "moderate" # default assumption for an explicitly stated symptom without modifiers
