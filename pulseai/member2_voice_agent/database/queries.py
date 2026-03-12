import sqlite3
from database.connection import get_db_connection
from utils.logger import setup_logger

logger = setup_logger(__name__)

def execute_query(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Utility to execute SQLite queries safely."""
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        result = None
        if fetchone:
            row = cursor.fetchone()
            result = dict(row) if row else None
        elif fetchall:
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            
        if commit:
            conn.commit()
            
        return result
    except sqlite3.Error as e:
        logger.error(f"Database error executing query '{query}': {e}")
        return None
    finally:
        conn.close()

# Session Queries
def create_session(session_id, patient_id, appointment_id, doctor_id):
    query = """
    INSERT INTO patient_sessions (session_id, patient_id, appointment_id, doctor_id)
    VALUES (?, ?, ?, ?)
    """
    execute_query(query, (session_id, patient_id, appointment_id, doctor_id), commit=True)

def get_session(session_id):
    query = "SELECT * FROM patient_sessions WHERE session_id = ?"
    return execute_query(query, (session_id,), fetchone=True)

def update_session_transcript(session_id, transcript, is_edited=False, version_increase=0):
    if is_edited:
        query = """
        UPDATE patient_sessions 
        SET edited_transcript = ?, version = version + ?, updated_at = CURRENT_TIMESTAMP 
        WHERE session_id = ?
        """
        execute_query(query, (transcript, version_increase, session_id), commit=True)
    else:
        query = "UPDATE patient_sessions SET original_transcript = ? WHERE session_id = ?"
        execute_query(query, (transcript, session_id), commit=True)

def complete_session_db(session_id):
    query = "UPDATE patient_sessions SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE session_id = ?"
    execute_query(query, (session_id,), commit=True)

# Risk Queries
def save_risk_analysis(risk_data):
    query = """
    INSERT INTO risk_analysis 
    (analysis_id, session_id, symptom_severity_score, urgency_score, comorbidity_score, duration_trend_score, total_risk_score, risk_level, risk_reasoning)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    execute_query(query, (
        risk_data['analysis_id'], risk_data['session_id'], risk_data['symptom_severity_score'],
        risk_data['urgency_score'], risk_data['comorbidity_score'], risk_data['duration_trend_score'],
        risk_data['total_risk_score'], risk_data['risk_level'], risk_data['risk_reasoning']
    ), commit=True)

def get_latest_risk_analysis(session_id):
    query = "SELECT * FROM risk_analysis WHERE session_id = ? ORDER BY analysis_timestamp DESC LIMIT 1"
    return execute_query(query, (session_id,), fetchone=True)
