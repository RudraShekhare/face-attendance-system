import sqlite3
import pandas as pd

DB_PATH = "../attendance.db"
CSV_PATH = "../attendance.csv"
EXCEL_PATH = "../attendance.xlsx"

def export_attendance():
    # Connect to the SQLite DB
    conn = sqlite3.connect(DB_PATH)

    # Read entire table into pandas DataFrame
    df = pd.read_sql_query("SELECT * FROM attendance", conn)
    conn.close()

    # Save to CSV
    df.to_csv(CSV_PATH, index=False)
    print(f"[INFO] Attendance exported to {CSV_PATH}")

    # Save to Excel
    df.to_excel(EXCEL_PATH, index=False)
    print(f"[INFO] Attendance exported to {EXCEL_PATH}")

if __name__ == "__main__":
    export_attendance()
