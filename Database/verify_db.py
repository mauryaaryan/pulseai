import sqlite3

def display_table_data(table_name):
    print(f"--- Data in '{table_name}' table ---")
    conn = sqlite3.connect('healthcare.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    
    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [col[1] for col in cursor.fetchall()]
    print(f"Columns: {', '.join(columns)}")
    
    for row in rows:
        print(row)
    print("-" * 40 + "\n")
    conn.close()

if __name__ == '__main__':
    display_table_data('doctors')
    display_table_data('appointments')
