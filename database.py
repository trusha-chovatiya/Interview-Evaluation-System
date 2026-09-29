import sqlite3


DB_NAME = "interview.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL UNIQUE,
            cv REAL DEFAULT 0,
            confidence REAL DEFAULT 0,
            communication REAL DEFAULT 0,
            knowledge REAL DEFAULT 0,
            remark TEXT,
            FOREIGN KEY(student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


def add_student(name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO students (name) VALUES (?)",
            (name,)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False

    conn.close()
    return success


def update_student(student_id, name):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE students SET name = ? WHERE id = ?",
            (name, student_id)
        )
        conn.commit()
        success = True
    except sqlite3.IntegrityError:
        success = False

    conn.close()
    return success


def delete_student(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM marks WHERE student_id = ?",
        (student_id,)
    )

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()


def get_students():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            s.id,
            s.name,
            COALESCE(m.cv, 0) AS cv,
            COALESCE(m.confidence, 0) AS confidence,
            COALESCE(m.communication, 0) AS communication,
            COALESCE(m.knowledge, 0) AS knowledge,
            COALESCE(m.remark, '') AS remark
        FROM students s
        LEFT JOIN marks m
        ON s.id = m.student_id
        ORDER BY s.id
    """)

    students = cursor.fetchall()
    conn.close()

    return students


def save_marks(
    student_id,
    cv,
    confidence,
    communication,
    knowledge,
    remark
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO marks
        (
            student_id,
            cv,
            confidence,
            communication,
            knowledge,
            remark
        )
        VALUES (?, ?, ?, ?, ?, ?)

        ON CONFLICT(student_id)
        DO UPDATE SET
            cv = excluded.cv,
            confidence = excluded.confidence,
            communication = excluded.communication,
            knowledge = excluded.knowledge,
            remark = excluded.remark
    """, (
        student_id,
        cv,
        confidence,
        communication,
        knowledge,
        remark
    ))

    conn.commit()
    conn.close()


def delete_marks(student_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM marks WHERE student_id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()


def initialize_default_students():
    students = [
        "Trusha",
        "Khushi",
        "Manasvi",
        "Yashvi",
        "Kajal",
        "Paresh",
        "Pritam",
        "Krish",
        "Deepak",
        "Meet"
    ]

    conn = get_connection()
    cursor = conn.cursor()

    for student in students:
        cursor.execute(
            "INSERT OR IGNORE INTO students (name) VALUES (?)",
            (student,)
        )

    conn.commit()
    conn.close()