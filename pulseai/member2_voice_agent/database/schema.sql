CREATE TABLE IF NOT EXISTS patient_sessions (
    session_id TEXT PRIMARY KEY,
    patient_id TEXT,
    appointment_id TEXT,
    doctor_id TEXT,
    original_transcript TEXT,
    edited_transcript TEXT,
    version INTEGER DEFAULT 1,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

CREATE TABLE IF NOT EXISTS risk_analysis (
    analysis_id TEXT PRIMARY KEY,
    session_id TEXT,
    symptom_severity_score INTEGER,
    urgency_score INTEGER,
    comorbidity_score INTEGER,
    duration_trend_score INTEGER,
    total_risk_score INTEGER,
    risk_level TEXT,
    risk_reasoning TEXT,
    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES patient_sessions(session_id)
);

CREATE TABLE IF NOT EXISTS symptom_entities (
    entity_id TEXT PRIMARY KEY,
    session_id TEXT,
    symptom_name TEXT,
    severity_level TEXT,
    duration TEXT,
    characteristics TEXT,
    FOREIGN KEY(session_id) REFERENCES patient_sessions(session_id)
);

CREATE TABLE IF NOT EXISTS medical_summaries (
    summary_id TEXT PRIMARY KEY,
    session_id TEXT,
    summary_text TEXT,
    summary_format TEXT,
    key_findings TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_to_doctor_at TIMESTAMP,
    FOREIGN KEY(session_id) REFERENCES patient_sessions(session_id)
);

CREATE TABLE IF NOT EXISTS transcript_edit_history (
    history_id TEXT PRIMARY KEY,
    session_id TEXT,
    version_number INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    previous_content TEXT,
    new_content TEXT,
    changes TEXT,
    FOREIGN KEY(session_id) REFERENCES patient_sessions(session_id)
);
