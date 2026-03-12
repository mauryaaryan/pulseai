from flask import Blueprint, request, jsonify
from database.queries import get_latest_risk_analysis, get_session
from services.summary_generator import SummaryGenerator
from services.nlp_analyzer import NLPAnalyzer
import json

summary_bp = Blueprint('summary', __name__)
generator = SummaryGenerator()
analyzer = NLPAnalyzer()

@summary_bp.route('/risk-analysis/<session_id>', methods=['GET'])
def risk_analysis(session_id):
    risk = get_latest_risk_analysis(session_id)
    if not risk:
        return jsonify({"error": "No risk analysis found"}), 404
        
    return jsonify({
        "risk_score": risk["total_risk_score"],
        "risk_level": risk["risk_level"],
        "factor_breakdown": {
            "symptom_severity_score": risk["symptom_severity_score"],
            "urgency_score": risk["urgency_score"],
            "comorbidity_score": risk["comorbidity_score"],
            "duration_trend_score": risk["duration_trend_score"]
        },
        "risk_reasoning": risk["risk_reasoning"]
    }), 200

@summary_bp.route('/generate-summary', methods=['POST'])
def generate_summary():
    data = request.json
    session_id = data.get("session_id")
    fmt = data.get("format", "structured")
    
    session = get_session(session_id)
    if not session:
        return jsonify({"error": "Session missing"}), 404
        
    transcript = session["edited_transcript"] or session["original_transcript"]
    risk = get_latest_risk_analysis(session_id)
    
    if not transcript or not risk:
         return jsonify({"error": "Data incomplete"}), 400
         
    # Quick regen of NLP for formatting, in production we might cache this in DB
    nlp_an = analyzer.analyze_transcript(transcript)
    
    summary = generator.generate_summary(session_id, nlp_an, risk, fmt)
    
    return jsonify({
        "summary": summary
    }), 200

@summary_bp.route('/send-summary-to-doctor', methods=['POST'])
def send_summary_to_doctor():
    # Placeholder integration simulation
    data = request.json
    session_id = data.get("session_id")
    
    return jsonify({
        "status": "sent",
        "delivery_timestamp": "timestamp",
        "doctor_notification": True
    }), 200
