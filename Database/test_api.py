import requests
import json

url = 'http://127.0.0.1:5000/book-appointment'

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

print(f"Sending POST request to {url}")
print("Payload:", json.dumps(data, indent=2))
print("-" * 40)

try:
    response = requests.post(url, json=data)
    print("Status Code:", response.status_code)
    print("Response JSON:", json.dumps(response.json(), indent=2))
except requests.exceptions.RequestException as e:
    print("Error connecting to the API:", str(e))
