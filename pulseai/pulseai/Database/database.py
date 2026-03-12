import sqlite3

def get_connection():
    return sqlite3.connect('healthcare.db')

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create doctors table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS doctors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        specialization TEXT,
        available_slots TEXT
    )
    ''')
    
    # Create patients table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        phone TEXT,
        email TEXT
    )
    ''')
    
    # Create appointments table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_name TEXT,
        time_slot TEXT,
        symptoms TEXT,
        risk_score INTEGER,
        risk_level TEXT,
        status TEXT DEFAULT 'pending'
    )
    ''')
    
    # Create prescriptions table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prescriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        appointment_id INTEGER,
        diagnosis TEXT,
        medicines TEXT,
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    conn.commit()
    conn.close()

def insert_mock_data():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if doctors table is empty
    cursor.execute('SELECT COUNT(*) FROM doctors')
    count = cursor.fetchone()[0]
    
    if count == 0:
        # Insert 3 doctors
        doctors_data = [
            ('Dr. Mehta', 'Cardiologist', '10:00 AM / 11:00 AM / 12:00 PM'),
            ('Dr. Sharma', 'General Physician', '9:00 AM / 2:00 PM / 4:00 PM'),
            ('Dr. Patel', 'Neurologist', '11:00 AM / 3:00 PM / 5:00 PM')
        ]
        cursor.executemany('''
        INSERT INTO doctors (name, specialization, available_slots)
        VALUES (?, ?, ?)
        ''', doctors_data)
        
        # Insert 5 mock patients
        patients_data = [
            ('Ravi Kumar', 45, '9876543210', 'ravi@example.com'),
            ('Sunita Sharma', 32, '8765432109', 'sunita@example.com'),
            ('Amit Singh', 28, '7654321098', 'amit@example.com'),
            ('Priya Patel', 50, '6543210987', 'priya@example.com'),
            ('Vikram Verma', 60, '5432109876', 'vikram@example.com')
        ]
        cursor.executemany('''
        INSERT INTO patients (name, age, phone, email)
        VALUES (?, ?, ?, ?)
        ''', patients_data)
        
        # Insert 5 mock appointments (2 high, 2 medium, 1 low)
        appointments_data = [
            # High risk: 80-100
            (1, 'Dr. Mehta', '10:00 AM', 'Severe chest pain, shortness of breath', 90, 'High', 'pending'),
            (2, 'Dr. Patel', '11:00 AM', 'Sudden severe headache, blurred vision', 85, 'High', 'pending'),
            # Medium risk: 40-74
            (3, 'Dr. Sharma', '9:00 AM', 'Persistent high fever, cough', 65, 'Medium', 'pending'),
            (4, 'Dr. Sharma', '2:00 PM', 'Severe stomach ache persisting for 2 days', 50, 'Medium', 'pending'),
            # Low risk: 0-39
            (5, 'Dr. Mehta', '11:00 AM', 'Routine heart checkup', 15, 'Low', 'pending')
        ]
        cursor.executemany('''
        INSERT INTO appointments (patient_id, doctor_name, time_slot, symptoms, risk_score, risk_level, status)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', appointments_data)
        
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    insert_mock_data()
    print("Database initialized and mock data inserted.")
