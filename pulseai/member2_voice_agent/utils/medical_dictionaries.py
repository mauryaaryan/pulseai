# Critical Symptoms requiring immediate evaluation
CRITICAL_SYMPTOMS = {
    "chest pain", "severe chest pain", "sharp chest pain",
    "breathlessness", "shortness of breath", "difficulty breathing",
    "loss of consciousness", "unconscious", "fainting",
    "severe headache", "worst headache of life",
    "facial drooping", "arm weakness", "speech difficulty",
    "severe bleeding", "uncontrolled bleeding",
    "severe abdominal pain", "suicidal thoughts"
}

# Serious Conditions
SERIOUS_CONDITIONS = {
    "heart attack", "myocardial infarction", "acute coronary syndrome",
    "stroke", "tia", "transient ischemic attack",
    "pneumonia", "pulmonary embolism",
    "asthma attack", "respiratory failure",
    "meningitis", "encephalitis",
    "sepsis", "severe infection"
}

# Comorbidities with risk weights
COMORBIDITIES = {
    "diabetes": 5,
    "hypertension": 4,
    "high blood pressure": 4,
    "heart disease": 10,
    "asthma": 6,
    "copd": 8,
    "chronic obstructive pulmonary disease": 8,
    "kidney disease": 8,
    "cancer": 10,
    "hiv": 9,
    "aids": 9
}

# Symptom Clusters (Pattern detection)
SYMPTOM_CLUSTERS = {
    "cardiac_pattern": ["chest pain", "breathlessness", "dizziness"],
    "respiratory_pattern": ["breathlessness", "cough", "chest pain"],
    "neurological_pattern": ["dizziness", "headache", "numbness", "facial drooping", "weakness"],
    "systemic_infection": ["fever", "chills", "malaise", "fatigue", "sweating"]
}

# Severity Descriptors mapping to normalized severity levels
SEVERITY_DESCRIPTORS = {
    "mild": ["slight", "minor", "light", "mild", "a little"],
    "moderate": ["medium", "significant", "considerable", "moderate", "somewhat"],
    "severe": ["intense", "extreme", "unbearable", "excruciating", "sharp", "crushing", "severe", "worst"]
}

# Points for different severity levels
SEVERITY_POINTS = {
    "mild": 5,
    "moderate": 15,
    "severe": 30
}
