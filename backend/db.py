import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "current_affairs.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Table for Daily Current Affairs Articles
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        summary TEXT NOT NULL,
        detailed_notes TEXT,
        exam_relevance TEXT,
        tags TEXT,
        source TEXT,
        created_at TEXT
    )
    """)

    # Table for Daily Practice Quiz / MCQs
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL,
        explanation TEXT NOT NULL,
        exam_tag TEXT
    )
    """)

    # Table for Quick Revision One-Liners
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS one_liners (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        point TEXT NOT NULL
    )
    """)

    # Table for Sync tracking
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sync_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        synced_at TEXT NOT NULL,
        date TEXT NOT NULL,
        articles_count INTEGER,
        status TEXT
    )
    """)

    # Table for User-Uploaded Educational PDFs & Study Materials
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS uploaded_materials (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        category TEXT NOT NULL,
        filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER,
        total_pages INTEGER,
        extracted_summary TEXT,
        articles_created INTEGER DEFAULT 0,
        quizzes_created INTEGER DEFAULT 0,
        uploaded_at TEXT
    )
    """)

    conn.commit()
    conn.close()

def insert_article(date, category, title, summary, detailed_notes="", exam_relevance="", tags="", source=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO articles (date, category, title, summary, detailed_notes, exam_relevance, tags, source, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, category, title, summary, detailed_notes, exam_relevance, tags, source, datetime.now().isoformat()))
    article_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return article_id

def insert_quiz(date, category, question, a, b, c, d, correct, explanation, exam_tag=""):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO quiz_questions (date, category, question, option_a, option_b, option_c, option_d, correct_option, explanation, exam_tag)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (date, category, question, a, b, c, d, correct, explanation, exam_tag))
    qid = cursor.lastrowid
    conn.commit()
    conn.close()
    return qid

def insert_one_liner(date, category, point):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO one_liners (date, category, point)
        VALUES (?, ?, ?)
    """, (date, category, point))
    lid = cursor.lastrowid
    conn.commit()
    conn.close()
    return lid

def get_articles(date=None, category=None, search_query=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM articles WHERE 1=1"
    params = []

    if date:
        query += " AND date = ?"
        params.append(date)
    if category and category != "all":
        query += " AND category = ?"
        params.append(category)
    if search_query:
        query += " AND (title LIKE ? OR summary LIKE ? OR detailed_notes LIKE ? OR tags LIKE ?)"
        wildcard = f"%{search_query}%"
        params.extend([wildcard, wildcard, wildcard, wildcard])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_quiz_by_date(date=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM quiz_questions WHERE 1=1"
    params = []
    if date:
        query += " AND date = ?"
        params.append(date)
    query += " ORDER BY id ASC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_one_liners_by_date(date=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM one_liners WHERE 1=1"
    params = []
    if date:
        query += " AND date = ?"
        params.append(date)
    query += " ORDER BY id ASC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def get_available_dates():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT date FROM articles ORDER BY date DESC")
    dates = [row["date"] for row in cursor.fetchall()]
    conn.close()
    return dates

def get_stats(date=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    if date:
        cursor.execute("SELECT COUNT(*) FROM articles WHERE date = ?", (date,))
        articles_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM quiz_questions WHERE date = ?", (date,))
        quiz_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM one_liners WHERE date = ?", (date,))
        one_liners_count = cursor.fetchone()[0]
    else:
        cursor.execute("SELECT COUNT(*) FROM articles")
        articles_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM quiz_questions")
        quiz_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM one_liners")
        one_liners_count = cursor.fetchone()[0]

    cursor.execute("SELECT category, COUNT(*) as count FROM articles GROUP BY category")
    category_counts = {row["category"]: row["count"] for row in cursor.fetchall()}

    conn.close()
    return {
        "articles_count": articles_count,
        "quiz_count": quiz_count,
        "one_liners_count": one_liners_count,
        "categories": category_counts
    }

def insert_uploaded_material(title, category, filename, file_path, file_size=0, total_pages=1, extracted_summary="", articles_created=0, quizzes_created=0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO uploaded_materials (title, category, filename, file_path, file_size, total_pages, extracted_summary, articles_created, quizzes_created, uploaded_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (title, category, filename, file_path, file_size, total_pages, extracted_summary, articles_created, quizzes_created, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    mid = cursor.lastrowid
    conn.commit()
    conn.close()
    return mid

def get_uploaded_materials(category=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM uploaded_materials"
    params = []
    if category and category != "all":
        query += " WHERE category = ?"
        params.append(category)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def delete_uploaded_material(material_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT filename, title, file_path FROM uploaded_materials WHERE id = ?", (material_id,))
    row = cursor.fetchone()
    if row:
        if row["file_path"] and os.path.exists(row["file_path"]):
            try:
                os.remove(row["file_path"])
            except Exception:
                pass
        # Clean up any articles and quizzes created from this file
        cursor.execute("DELETE FROM articles WHERE detailed_notes LIKE ?", (f"%{row['filename']}%",))
        cursor.execute("DELETE FROM articles WHERE source LIKE ?", (f"%{row['filename']}%",))
        cursor.execute("DELETE FROM quiz_questions WHERE exam_tag LIKE ?", (f"%{row['filename']}%",))
        cursor.execute("DELETE FROM quiz_questions WHERE exam_tag LIKE ?", (f"%{row['title'][:25]}%",))

    cursor.execute("DELETE FROM uploaded_materials WHERE id = ?", (material_id,))
    conn.commit()
    conn.close()
    return True
