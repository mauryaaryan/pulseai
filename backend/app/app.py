import sys
import os
import sqlite3
import requests
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add the project root and Database folder to path so imports resolve correctly
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)
sys.path.insert(0, os.path.join(ROOT_DIR, 'Database'))

from database import init_db, insert_mock_data
from services.email_service import send_prescription_email

app = Flask(__name__)
CORS(app)

DB_PATH = os.path.join(ROOT_DIR, 'Database', 'healthcare.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ----- PORTED BOOKING API ROUTES -----
@app.route('/get-doctors', methods=['GET'])
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    rows = cursor.fetchall()
    
    doctors = []
    for row in rows:
        doc = dict(row)
        if doc['available_slots']:
            doc['available_slots'] = [slot.strip() for slot in doc['available_slots'].split('/')]
        else:
            doc['available_slots'] = []
        doctors.append(doc)
    conn.close()
    return jsonify(doctors)

@app.route('/book-appointment', methods=['POST'])
def book_appointment():
    data = request.json
    if not data: return jsonify({"success": False, "message": "No data provided"}), 400
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO patients (name, age, phone, email) VALUES (?, ?, ?, ?)', 
                      (data.get('name'), data.get('age'), data.get('phone'), data.get('email')))
        patient_id = cursor.lastrowid
        cursor.execute('''INSERT INTO appointments 
                          (patient_id, doctor_name, time_slot, symptoms, risk_score, risk_level, status)
                          VALUES (?, ?, ?, ?, ?, ?, 'pending')''', 
                      (patient_id, data.get('doctor_name'), data.get('time_slot'), 
                       data.get('symptoms'), data.get('risk_score'), data.get('risk_level')))
        conn.commit()
        return jsonify({"success": True, "message": "Appointment booked", "appointment_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

@app.route('/get-patient-appointments/<email>', methods=['GET'])
def get_patient_appointments(email):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM patients WHERE email = ? ORDER BY id DESC LIMIT 1", (email,))
    patient = cursor.fetchone()
    if not patient:
        conn.close()
        return jsonify({"appointments": []})
    cursor.execute("SELECT * FROM appointments WHERE patient_id = ?", (patient['id'],))
    appointments = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify({"appointments": appointments})


# ----- PORTED PRESCRIPTION API ROUTES -----
@app.route('/save-prescription', methods=['POST'])
def save_prescription():
    data = request.json
    if not data: return jsonify({"success": False, "message": "No data"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    try:
        medicines_list = data.get('medicines', [])
        medicines_str = ", ".join(medicines_list) if isinstance(medicines_list, list) else medicines_list
        
        cursor.execute('''INSERT INTO prescriptions (appointment_id, diagnosis, medicines, notes)
                          VALUES (?, ?, ?, ?)''', 
                      (data.get('appointment_id'), data.get('diagnosis'), medicines_str, data.get('notes')))
        conn.commit()
        
        email_sent = send_prescription_email(
            data.get('patient_email'), data.get('patient_name'), data.get('doctor_name'),
            data.get('diagnosis'), medicines_list, data.get('notes')
        )
        if not email_sent:
            return jsonify({"success": True, "message": "Prescription saved but email failed to send."}), 200
        return jsonify({"success": True, "message": "Prescription saved and email sent"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

@app.route('/get-prescription/<int:appointment_id>', methods=['GET'])
def get_prescription(appointment_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prescriptions WHERE appointment_id = ?", (appointment_id,))
    row = cursor.fetchone()
    conn.close()
    if not row: return jsonify({"found": False}), 404
    
    prescription = dict(row)
    prescription['medicines'] = [m.strip() for m in prescription['medicines'].split(',')] if prescription['medicines'] else []
    prescription['found'] = True
    return jsonify(prescription)

# ----- SYMPTOM API (MEMBER 2) -----
@app.route('/analyze-symptoms', methods=['POST'])
def analyze_symptoms():
    try:
        response = requests.post('http://localhost:5001/voice/transcribe', json=request.json)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException:
        return jsonify({
            "risk_score": 50,
            "risk_level": "Medium",
            "message": "Voice agent unavailable"
        }), 503

@app.route('/get-appointments', methods=['GET'])
def get_appointments():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT a.*, p.name as patient_name 
        FROM appointments a
        LEFT JOIN patients p ON a.patient_id = p.id
        ORDER BY a.risk_score DESC
    ''')
    rows = cursor.fetchall()
    appointments = [dict(row) for row in rows]
    conn.close()
    return jsonify({"appointments": appointments})

# ----- ROOT ENDPOINT -----
@app.route('/', methods=['GET'])
def index():
    return jsonify({
        "status": "PulseAI Backend Running",
        "version": "1.0",
        "team": "PulseAI",
        "routes": [
            "/get-doctors",
            "/book-appointment",
            "/get-patient-appointments/<email>",
            "/save-prescription",
            "/get-prescription/<appointment_id>",
            "/analyze-symptoms",
            "/get-appointments"
        ]
    })


if __name__ == '__main__':
    os.chdir(ROOT_DIR)  # Ensure relative paths resolve from project root
    init_db()
    insert_mock_data()
    print("Database Initialized via app.py. Starting Unified Server...")
    app.run(port=5000, debug=True)
