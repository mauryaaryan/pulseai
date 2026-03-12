import requests
import json
from datetime import datetime

import os
from dotenv import load_dotenv

load_dotenv()
RESEND_API_KEY = os.environ.get('RESEND_API_KEY', '')

def send_prescription_email(patient_email, patient_name, doctor_name, diagnosis, medicines, notes):
    url = "https://api.resend.com/emails"
    
    headers = {
        "Authorization": f"Bearer {RESEND_API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Format the medicines into an HTML numbered list
    medicines_list_html = "".join([f"<li>{med}</li>" for med in medicines])
    current_date = datetime.now().strftime("%B %d, %Y")
    
    # Professional HTML Email Template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #333; line-height: 1.6; margin: 0; padding: 0; }}
            .container {{ max-width: 600px; margin: 20px auto; border: 1px solid #e2e8f0; border-radius: 8px; overflow: hidden; }}
            .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; }}
            .header h1 {{ margin: 0; font-size: 24px; font-weight: 600; }}
            .content {{ padding: 30px; background-color: #f8fafc; }}
            .section {{ margin-bottom: 25px; background: white; padding: 20px; border-radius: 6px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); }}
            h2 {{ color: #1e293b; font-size: 18px; margin-top: 0; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; }}
            .meta-info {{ margin-bottom: 20px; color: #64748b; font-size: 14px; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px; }}
            ol {{ padding-left: 20px; margin: 0; }}
            li {{ margin-bottom: 8px; font-weight: 500; color: #0f172a; }}
            .notes {{ font-style: italic; color: #475569; }}
            .footer {{ text-align: center; padding: 20px; font-size: 12px; color: #94a3b8; background-color: #f1f5f9; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>PulseAI Medical Center</h1>
            </div>
            
            <div class="content">
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>Please find your medical prescription attached below.</p>
                
                <div class="meta-info">
                    <strong>Consulting Doctor:</strong> {doctor_name}<br>
                    <strong>Date:</strong> {current_date}
                </div>
                
                <div class="section">
                    <h2>Diagnosis</h2>
                    <p style="color: #ef4444; font-weight: bold;">{diagnosis}</p>
                </div>
                
                <div class="section">
                    <h2>Prescribed Medicines</h2>
                    <ol>
                        {medicines_list_html}
                    </ol>
                </div>
                
                <div class="section">
                    <h2>Additional Notes</h2>
                    <p class="notes">{notes}</p>
                </div>
            </div>
            
            <div class="footer">
                This is a digitally generated prescription by PulseAI.<br>
                For any medical emergencies, please visit the hospital immediately.
            </div>
        </div>
    </body>
    </html>
    """

    data = {
        "from": "PulseAI <onboarding@resend.dev>",
        "to": [patient_email],
        "subject": "Your Prescription from PulseAI",
        "html": html_content
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        # Resend returns 200 on success
        if response.status_code in [200, 201]:
            print(f"[SUCCESS] Successfully sent prescription email to {patient_email}")
            return True
        else:
            print(f"[ERROR] Failed to send email. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API Connection Error: {str(e)}")
        return False

# Simple test block
if __name__ == '__main__':
    print("Testing Resend API Email Function...")
    test_medicines = [
        "Paracetamol 500mg - 1 tablet twice a day after meals",
        "Amoxicillin 250mg - 1 capsule every 8 hours",
        "Cough Syrup - 2 teaspoons before sleep"
    ]
    
    success = send_prescription_email(
        patient_email="ashutoshcmishra720@gmail.com", 
        patient_name="Ashutosh Mishra",
        doctor_name="Dr. Mehta",
        diagnosis="Acute Bronchitis and Viral Fever",
        medicines=test_medicines,
        notes="Please rest for at least 3 days. Drink plenty of warm fluids. Return for a checkup if fever persists beyond 48 hours."
    )
    
    if success:
        print("Test passed: function returned True.")
    else:
        print("Note: Test likely failed because RESEND_API_KEY is not set to a valid key.")
