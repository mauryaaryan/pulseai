import uuid
from flask import Blueprint, request, jsonify
from services.voice_processor import VoiceProcessor
from services.nlp_analyzer import NLPAnalyzer
from services.risk_scorer import RiskScorer
from database.queries import create_session, update_session_transcript, save_risk_analysis, complete_session_db

voice_bp = Blueprint('voice', __name__)

processor = VoiceProcessor()
analyzer = NLPAnalyzer()
scorer = RiskScorer()

@voice_bp.route('/start-session', methods=['POST'])
def start_session():
    data = request.json
    session_id = str(uuid.uuid4())
    create_session(
        session_id=session_id,
        patient_id=data.get('patient_id', 'unknown'),
        appointment_id=data.get('appointment_id', 'unknown'),
        doctor_id=data.get('doctor_id', 'unknown')
    )
    return jsonify({
        "session_id": session_id,
        "status": "active"
    }), 200

@voice_bp.route('/process-stream', methods=['POST'])
def process_stream():
    data = request.json
    res = processor.buffer_audio_chunk(
        session_id=data.get('session_id'),
        audio_chunk=data.get('audio_chunk'),
        chunk_index=data.get('chunk_index')
    )
    return jsonify(res), 200

@voice_bp.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.json
    session_id = data.get('session_id')
    audio_path = data.get('audio_file_path', 'dummy.wav')
    
    # 1. Voice to Text
    transcript, metadata = processor.transcribe_audio(audio_path)
    update_session_transcript(session_id, transcript)
    
    # 2. NLP Analysis
    nlp_analysis = analyzer.analyze_transcript(transcript)
    
    # 3. Risk Calculation
    risk_analysis = scorer.calculate_risk_score(session_id, nlp_analysis)
    save_risk_analysis(risk_analysis)
    
    return jsonify({
        "transcript": transcript,
        "metadata": metadata,
        "risk_analysis": {
            "risk_score": risk_analysis["total_risk_score"],
            "risk_level": risk_analysis["risk_level"],
            "recommended_priority": risk_analysis["recommended_priority"]
        },
        "analysis_status": "complete"
    }), 200

@voice_bp.route('/complete-session/<session_id>', methods=['POST'])
def complete_session(session_id):
    complete_session_db(session_id)
    return jsonify({
        "session_id": session_id,
        "status": "completed",
        "summary_generated": True
    }), 200
