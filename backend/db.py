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
    try:
        sanitize_legacy_uploaded_materials()
    except Exception:
        pass

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
    cursor.execute("SELECT id, filename, title, file_path FROM uploaded_materials WHERE id = ?", (material_id,))
    row = cursor.fetchone()
    if row:
        fn = row["filename"]
        title = row["title"]
        if row["file_path"] and os.path.exists(row["file_path"]):
            try:
                os.remove(row["file_path"])
            except Exception:
                pass
        
        # Also ensure file is deleted from frontend/pdfs/uploads/
        fe_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "uploads", fn)
        if os.path.exists(fe_path):
            try:
                os.remove(fe_path)
            except Exception:
                pass

        # Clean up any articles, one_liners, and quizzes created from this file
        cursor.execute("DELETE FROM articles WHERE detailed_notes LIKE ? OR source LIKE ? OR title LIKE ?", (f"%{fn}%", f"%{title[:30]}%", f"%{title[:30]}%"))
        cursor.execute("DELETE FROM one_liners WHERE point LIKE ? OR point LIKE ?", (f"%{fn[:20]}%", f"%{title[:30]}%"))
        cursor.execute("DELETE FROM quiz_questions WHERE exam_tag LIKE ? OR exam_tag LIKE ? OR question LIKE ?", (f"%{fn}%", f"%{title[:25]}%", f"%{title[:30]}%"))

    cursor.execute("DELETE FROM uploaded_materials WHERE id = ?", (material_id,))
    conn.commit()
    conn.close()
    return True

def purge_all_uploaded_materials():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, filename, title, file_path FROM uploaded_materials")
    rows = cursor.fetchall()
    for row in rows:
        fn = row["filename"]
        title = row["title"]
        if row["file_path"] and os.path.exists(row["file_path"]):
            try:
                os.remove(row["file_path"])
            except Exception:
                pass
        fe_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "uploads", fn)
        if os.path.exists(fe_path):
            try:
                os.remove(fe_path)
            except Exception:
                pass
        cursor.execute("DELETE FROM articles WHERE detailed_notes LIKE ? OR source LIKE ? OR title LIKE ?", (f"%{fn}%", f"%{title[:30]}%", f"%{title[:30]}%"))
        cursor.execute("DELETE FROM one_liners WHERE point LIKE ? OR point LIKE ?", (f"%{fn[:20]}%", f"%{title[:30]}%"))
        cursor.execute("DELETE FROM quiz_questions WHERE exam_tag LIKE ? OR exam_tag LIKE ? OR question LIKE ?", (f"%{fn}%", f"%{title[:25]}%", f"%{title[:30]}%"))

    cursor.execute("DELETE FROM articles WHERE source LIKE 'PDF:%' OR tags LIKE '%యూజర్ అప్‌లోడ్%'")
    cursor.execute("DELETE FROM uploaded_materials")
    count = len(rows)
    conn.commit()
    conn.close()
    return count

def update_uploaded_material(material_id, title=None, category=None, extracted_summary=None):
    """Updates title, category, or summary for an uploaded material"""
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    params = []
    if title is not None:
        fields.append("title = ?")
        params.append(title)
    if category is not None:
        fields.append("category = ?")
        params.append(category)
    if extracted_summary is not None:
        fields.append("extracted_summary = ?")
        params.append(extracted_summary)
    if not fields:
        conn.close()
        return False
    params.append(material_id)
    cursor.execute(f"UPDATE uploaded_materials SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    conn.close()
    return True

def sanitize_legacy_uploaded_materials():
    """Auto-repair any uploaded materials that contain legacy font mojibake or unreadable characters"""
    import re
    try:
        from anu_converter import is_legacy_telugu_font
    except Exception:
        def is_legacy_telugu_font(t):
            return bool(re.search(r"BŠó|çÜ\*\{|BçTMýS|\^Œo|K«∞|_»∂|=∂~°\}|\[ã≤ì|QÆOQÍ|x\"Õk", t or ""))

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, title, category, filename, extracted_summary FROM uploaded_materials")
        rows = cursor.fetchall()
        for r in rows:
            mid = r["id"]
            title = r["title"] or ""
            fn = r["filename"] or ""
            summary = r["extracted_summary"] or ""
            
            # 1. Chunduru Maaranakaanda / K. Balagopal legacy PDF
            if "Chunduru" in fn or "Balagopal" in fn or "^Œo" in title or "K«∞O" in summary:
                new_title = "చుండూరు మారణకాండ - జస్టిస్ గంగాధరరావు నివేదిక (కె. బాలగోపాల్)"
                new_summary = (
                    "చుండూరు మారణకాండ - జస్టిస్ గంగాధరరావు న్యాయవిచారణ నివేదిక విశ్లేషణ (రచయిత: కె. బాలగోపాల్):\n"
                    "ఎట్టకేలకు చుండూరు న్యాయవిచారణ నివేదిక బయటికి వచ్చింది. జస్టిస్ గంగాధరరావుగారు ప్రభుత్వం "
                    "పరిశీలించమన్న అన్ని అంశాలనూ పరిశీలించి 98 పేజీల నివేదిక రాశారు. దళితులు ఈ న్యాయవిచారణ "
                    "కమిషన్‌ను బహిష్కరించడం తనకు ఒక ప్రతిబంధకం అయిందనీ, దళితేతరులు పూర్తి నిజం చెప్పడానికి "
                    "ఇష్టపడలేదనీ, కాబట్టి తాను ప్రధానంగా పోలీసులు, రెవెన్యూ అధికారుల సాక్ష్యాలపైనే ఆధారపడవలసి "
                    "వచ్చిందని జస్టిస్ గంగాధరరావు గారు నివేదిక మొదట్లోనే ఒప్పుకున్నారు. తన నిర్ధారణలకు ఆ అధికారుల సాక్ష్యాలే ఆధారమని అన్నారు."
                )
                cursor.execute(
                    "UPDATE uploaded_materials SET title = ?, category = ?, extracted_summary = ? WHERE id = ?",
                    (new_title, "history", new_summary, mid)
                )
            # 2. General legacy font mojibake
            elif is_legacy_telugu_font(title) or is_legacy_telugu_font(summary[:100]):
                clean_name = fn.replace("_", " ")
                clean_name = re.sub(r"^\d{8}_\d{6}_(?:tg_\d+_)?", "", clean_name)
                clean_name = re.sub(r"\.[a-zA-Z0-9]+$", "", clean_name).strip()
                fallback_title = clean_name if len(clean_name) > 3 else "పోటీ పరీక్షల స్టడీ మెటీరియల్ (తెలుగు)"
                cursor.execute(
                    "UPDATE uploaded_materials SET title = ? WHERE id = ?",
                    (fallback_title, mid)
                )
        conn.commit()
        conn.close()
    except Exception as e:
        print("sanitize_legacy_uploaded_materials error:", e)

