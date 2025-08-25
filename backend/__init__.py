import sqlite3

DATABASE = "fyp_database.db"

def get_db_connection():
    """Creates and returns a database connection."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn
  
def initialize_database():
    """Creates necessary tables if they don’t exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        last_name TEXT NOT NULL,
        other_names TEXT NOT NULL,
        user_type TEXT CHECK(user_type IN ('student', 'teacher')) NOT NULL,
        matric_number TEXT UNIQUE DEFAULT NULL,
        title TEXT DEFAULT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS Tests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        test_code TEXT UNIQUE NOT NULL,
        title TEXT NOT NULL,
        description TEXT,
        strict INTEGER DEFAULT 0,
        questions_data TEXT NOT NULL, -- JSON format
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES User(id) ON DELETE CASCADE
    );

    CREATE TABLE IF NOT EXISTS Student_Test (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        test_id INTEGER NOT NULL,
        student_id INTEGER NOT NULL,
        answers TEXT NOT NULL, -- JSON format
        result TEXT DEFAULT NULL, -- JSON format
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (test_id) REFERENCES Tests(id) ON DELETE CASCADE,
        FOREIGN KEY (student_id) REFERENCES User(id) ON DELETE CASCADE,
        UNIQUE(test_id, student_id) -- Ensures one entry per student per test
    );
                         
    CREATE TABLE IF NOT EXISTS Rubrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        teacher_id INTEGER NOT NULL,
        title TEXT NOT NULL,
        rubric_data TEXT NOT NULL, -- JSON format
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (teacher_id) REFERENCES User(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()

# Auto-run database initialization when the module is imported
initialize_database()
