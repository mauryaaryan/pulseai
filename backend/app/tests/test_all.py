import requests
import json
import time

BASE_URL = 'http://127.0.0.1:5000'

def test_root():
    print(requests.get(f"{BASE_URL}/").json())

def test_book_appointment():
    data = {
        "name": "Rahul Sharma",
        "age": 35,
        "phone": "9876543210",
        "email": "rahul@test.com",
        "doctor_name": "Dr. Mehta",
        "time_slot": "10:00 AM",
        "symptoms": "chest pain and breathlessness",
        "risk_score": 90,
        "risk_level": "High"
    }
    response = requests.post(f"{BASE_URL}/book-appointment", json=data)
    print("Booking Status Code:", response.status_code)
    print("Booking JSON:", json.dumps(response.json(), indent=2))

def test_save_prescription():
    data = {
        "appointment_id": 1,
        "patient_email": "test@gmail.com",
        "patient_name": "Rahul Sharma",
        "doctor_name": "Dr. Mehta",
        "diagnosis": "Hypertension",
        "medicines": ["Amlodipine 5mg - once daily", "Aspirin 75mg - once daily"],
        "notes": "Rest and avoid stress."
    }
    response = requests.post(f"{BASE_URL}/save-prescription", json=data)
    print("Prescription Status Code:", response.status_code)
    print("Prescription JSON:", json.dumps(response.json(), indent=2))

if __name__ == '__main__':
    print("--- 1. Testing Root ---")
    test_root()
    time.sleep(1)
    print("\n--- 2. Testing Booking ---")
    test_book_appointment()
    time.sleep(1)
    print("\n--- 3. Testing Prescription ---")
    test_save_prescription()
