from flask import Blueprint, request, jsonify
from services.transcript_manager import TranscriptManager
from services.nlp_analyzer import NLPAnalyzer
from services.risk_scorer import RiskScorer
from database.queries import save_risk_analysis, get_latest_risk_analysis

transcript_bp = Blueprint('transcript', __name__)

manager = TranscriptManager()
analyzer = NLPAnalyzer()
scorer = RiskScorer()

@transcript_bp.route('/get-transcript/<session_id>', methods=['GET'])
def get_transcript(session_id):
    result = manager.get_transcript(session_id)
    if not result:
        return jsonify({"error": "Not found"}), 404
    return jsonify(result), 200

@transcript_bp.route('/update-transcript', methods=['POST'])
def update_transcript():
    data = request.json
    session_id = data.get("session_id")
    edited_text = data.get("edited_transcript")
    
    # 1. Update version
    manager.update_transcript(session_id, edited_text)
    
    # 2. Re-trigger NLP
    nlp_analysis = analyzer.analyze_transcript(edited_text)
    
    # 3. Recalculate Risk
    new_risk = scorer.calculate_risk_score(session_id, nlp_analysis)
    
    # 4. Fetch old risk for comparison before saving
    old_risk = get_latest_risk_analysis(session_id)
    old_score = old_risk['total_risk_score'] if old_risk else None
    
    save_risk_analysis(new_risk)
    
    state = manager.get_transcript(session_id)
    
    return jsonify({
        "session_id": session_id,
        "updated_transcript": edited_text,
        "version": state["version"] if state else 2,
        "old_risk_score": old_score,
        "new_risk_score": new_risk["total_risk_score"],
        "new_risk_level": new_risk["risk_level"],
        "reanalysis_triggered": True
    }), 200
