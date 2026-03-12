from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from database import init_db, insert_mock_data

app = Flask(__name__)
CORS(app)

# Initialize DB and mock data when app starts
init_db()
insert_mock_data()

def get_connection():
    conn = sqlite3.connect('healthcare.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/get-doctors', methods=['GET'])
def get_doctors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM doctors")
    rows = cursor.fetchall()
    
    doctors = []
    for row in rows:
        doc = dict(row)
        # Split available_slots string into a list
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
    if not data:
        return jsonify({"success": False, "message": "No data provided"}), 400
        
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # 1. Insert into patients table
        cursor.execute('''
            INSERT INTO patients (name, age, phone, email)
            VALUES (?, ?, ?, ?)
        ''', (data.get('name'), data.get('age'), data.get('phone'), data.get('email')))
        
        patient_id = cursor.lastrowid
        
        # 2. Insert into appointments table
        cursor.execute('''
            INSERT INTO appointments (patient_id, doctor_name, time_slot, symptoms, risk_score, risk_level, status)
            VALUES (?, ?, ?, ?, ?, ?, 'pending')
        ''', (
            patient_id, 
            data.get('doctor_name'), 
            data.get('time_slot'), 
            data.get('symptoms'), 
            data.get('risk_score'), 
            data.get('risk_level')
        ))
        
        appointment_id = cursor.lastrowid
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": "Appointment booked successfully", 
            "appointment_id": appointment_id
        }), 201
        
    except Exception as e:
        conn.rollback()
        return jsonify({"success": False, "message": str(e)}), 500
    finally:
        conn.close()

@app.route('/get-patient-appointments/<email>', methods=['GET'])
def get_patient_appointments(email):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if patient exists
    cursor.execute("SELECT id FROM patients WHERE email = ? ORDER BY id DESC LIMIT 1", (email,))
    patient = cursor.fetchone()
    
    if not patient:
        conn.close()
        return jsonify({"appointments": []})
        
    patient_id = patient['id']
    
    # Fetch appointments for this patient
    cursor.execute("SELECT * FROM appointments WHERE patient_id = ?", (patient_id,))
    rows = cursor.fetchall()
    
    appointments = [dict(row) for row in rows]
    conn.close()
    
    return jsonify({"appointments": appointments})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
