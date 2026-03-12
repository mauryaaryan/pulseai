import sqlite3
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(ROOT_DIR, 'Database', 'healthcare.db')

def get_db():
    return sqlite3.connect(DB_PATH)

def setup_demo_data():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM prescriptions")
    if cursor.fetchone()[0] == 0:
        demo_prescriptions = [
            (1, 'Hypertension', 'Amlodipine 5mg once daily and Aspirin 75mg once daily', 'Rest and avoid stress.'),
            (2, 'Migraine', 'Sumatriptan 50mg as needed and Paracetamol 500mg twice daily', 'Avoid bright lights.')
        ]
        cursor.executemany("INSERT INTO prescriptions (appointment_id, diagnosis, medicines, notes) VALUES (?, ?, ?, ?)", demo_prescriptions)
        conn.commit()
    conn.close()
    print("Demo data ready")

def display_table_data(table_name):
    print(f"--- Data in '{table_name}' table ---")
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Columns: {', '.join(columns)}")
    
    for row in rows:
        print(row)
    print("-" * 40 + "\n")
    conn.close()

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'setup':
        setup_demo_data()
    else:
        display_table_data('doctors')
        display_table_data('appointments')
        display_table_data('prescriptions')
