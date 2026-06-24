import sqlite3
from typing import List, Tuple, Optional
from datetime import date

DB_PATH = "patients.db"


def get_connection(path: str = DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(path: str = DB_PATH):
    conn = get_connection(path)
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        full_name TEXT NOT NULL,
        dob TEXT,
        email TEXT,
        glucose REAL,
        haemoglobin REAL,
        cholesterol REAL,
        remarks TEXT
    )
    """
    )
    conn.commit()
    conn.close()


def add_patient(full_name: str, dob: str, email: str, glucose: float, haemoglobin: float, cholesterol: float, remarks: str, path: str = DB_PATH) -> int:
    conn = get_connection(path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO patients (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks) VALUES (?,?,?,?,?,?,?)",
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks),
    )
    conn.commit()
    last_id = cursor.lastrowid
    conn.close()
    return last_id


def get_all_patients(path: str = DB_PATH) -> List[sqlite3.Row]:
    conn = get_connection(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_patient(pid: int, path: str = DB_PATH) -> Optional[sqlite3.Row]:
    conn = get_connection(path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients WHERE id=?", (pid,))
    row = cursor.fetchone()
    conn.close()
    return row


def update_patient(pid: int, full_name: str, dob: str, email: str, glucose: float, haemoglobin: float, cholesterol: float, remarks: str, path: str = DB_PATH) -> None:
    conn = get_connection(path)
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE patients SET full_name=?, dob=?, email=?, glucose=?, haemoglobin=?, cholesterol=?, remarks=? WHERE id=?
        """,
        (full_name, dob, email, glucose, haemoglobin, cholesterol, remarks, pid),
    )
    conn.commit()
    conn.close()


def delete_patient(pid: int, path: str = DB_PATH) -> None:
    conn = get_connection(path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE id=?", (pid,))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
