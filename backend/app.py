# -*- coding: utf-8 -*-
"""
Main Flask Application for Daily Current Affairs (తెలుగు పోటీ పరీక్షల డ్యాష్‌బోర్డ్)
Provides REST API endpoints and serves frontend files.
"""

from flask import Flask, jsonify, request, send_from_directory, Response, render_template_string
import os
import sys
import json
from datetime import datetime
from tts import generate_telugu_audio

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from db import (
    init_db,
    get_connection,
    get_articles,
    get_quiz_by_date,
    get_one_liners_by_date,
    get_available_dates,
    get_stats
)
from scraper import sync_daily_news
from seed_data import populate_seed_data
from telegram_bot import load_config, save_config, send_telegram_message, broadcast_daily_digest, send_daily_epaper_pdf, send_epapers_directory
from scheduler import start_scheduler_thread, load_scheduler_config, save_scheduler_config, run_daily_job
from magazine import render_magazine_html
from pdf_generator import render_epaper_html, generate_epaper_pdf, OFFICIAL_TELUGU_EPAPERS
from mock_tests_data import SUBJECT_MOCK_TESTS
from omr_generator import generate_omr_test_html, get_all_50_mock_questions, generate_group2_omr_test_html
from appsc_group2_data import (
    get_appsc_group2_full_mock,
    get_appsc_group2_by_section,
    get_appsc_group2_pyqs,
    get_appsc_group2_quick_test,
    get_appsc_group2_metadata,
    APPSC_GROUP2_SECTIONS
)

FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path="")
app.config['JSON_AS_ASCII'] = False  # Keep Telugu characters untranslated in JSON

# Ensure DB has tables and initial seed data
init_db()
populate_seed_data()

# Start background morning scheduler thread
start_scheduler_thread()

# Start background Telegram bot polling thread when hosted on cloud
def start_embedded_bot():
    try:
        import threading
        from run_bot import start_bot_polling
        bot_thread = threading.Thread(target=start_bot_polling, daemon=True)
        bot_thread.start()
        print("🤖 [Embedded Bot] టెలిగ్రామ్ బోట్ బ్యాక్‌గ్రౌండ్ థ్రెడ్ ప్రారంభమైంది.")
    except Exception as e:
        print("⚠️ Embedded bot error:", e)

if os.environ.get("RENDER") or os.environ.get("START_EMBEDDED_BOT"):
    start_embedded_bot()

# ----------------- Frontend Routes -----------------
@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/magazine")
def magazine_view():
    period_type = request.args.get("type", "monthly")
    month = request.args.get("month")
    start_date = request.args.get("start")
    end_date = request.args.get("end")

    if period_type == "monthly" and not month:
        dates = get_available_dates()
        month = dates[0][:7] if dates else datetime.now().strftime("%Y-%m")
        
    html_content = render_magazine_html(
        period_type=period_type,
        year_month=month,
        start_date=start_date,
        end_date=end_date
    )
    return html_content

@app.route("/epaper")
@app.route("/api/epaper")
def epaper_view():
    date = request.args.get("date")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")
    return render_epaper_html(date=date)

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(FRONTEND_DIR, path)

# ----------------- API Endpoints -----------------
@app.route("/api/affairs", methods=["GET"])
def api_articles():
    date = request.args.get("date")
    category = request.args.get("category", "all")
    q = request.args.get("q")
    
    # If no date specified, default to latest available date
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else None

    articles = get_articles(date=date, category=category, search_query=q)
    return jsonify({
        "success": True,
        "date": date,
        "category": category,
        "total": len(articles),
        "data": articles
    })

@app.route("/api/article/<int:article_id>", methods=["GET"])
def api_get_single_article(article_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM articles WHERE id = ?", (article_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"success": True, "article": dict(row)})
    return jsonify({"success": False, "error": "ఆర్టికల్ కనుగొనబడలేదు"}), 404

@app.route("/api/article/category/<category>", methods=["GET"])
def api_get_article_by_category(category):
    date = request.args.get("date")
    conn = get_connection()
    c = conn.cursor()
    if date:
        c.execute("SELECT * FROM articles WHERE category = ? AND date = ? ORDER BY id DESC LIMIT 1", (category, date))
    else:
        c.execute("SELECT * FROM articles WHERE category = ? ORDER BY id DESC LIMIT 1", (category,))
    row = c.fetchone()
    conn.close()
    if row:
        return jsonify({"success": True, "article": dict(row)})
    return jsonify({"success": False, "error": "ఆర్టికల్ కనుగొనబడలేదు"}), 404

@app.route("/api/quiz", methods=["GET"])
def api_quiz():
    date = request.args.get("date")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else None

    quizzes = get_quiz_by_date(date=date)
    return jsonify({
        "success": True,
        "date": date,
        "total": len(quizzes),
        "data": quizzes
    })

@app.route("/api/one_liners", methods=["GET"])
def api_one_liners():
    date = request.args.get("date")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else None

    one_liners = get_one_liners_by_date(date=date)
    return jsonify({
        "success": True,
        "date": date,
        "total": len(one_liners),
        "data": one_liners
    })

@app.route("/api/dates", methods=["GET"])
def api_dates():
    dates = get_available_dates()
    return jsonify({
        "success": True,
        "dates": dates
    })

@app.route("/api/stats", methods=["GET"])
def api_stats():
    date = request.args.get("date")
    stats = get_stats(date=date)
    return jsonify({
        "success": True,
        "stats": stats
    })

@app.route("/api/sync", methods=["POST", "GET"])
def api_sync():
    date = request.args.get("date")
    try:
        result = sync_daily_news(target_date=date)
        return jsonify({
            "success": True,
            "message": "వార్తలు విజయవంతంగా సింక్ చేయబడ్డాయి!",
            "result": result
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# ----------------- Telegram Bot Endpoints -----------------
@app.route("/api/telegram/config", methods=["GET", "POST"])
def api_telegram_config():
    if request.method == "POST":
        data = request.json or {}
        token = data.get("bot_token", "").strip()
        chat_id = data.get("chat_id", "").strip()
        cfg = save_config(token, chat_id)
        saved_token = cfg.get("bot_token", "")
        masked_token = (saved_token[:6] + "..." + saved_token[-4:]) if len(saved_token) > 10 else ("Configured" if saved_token else "")
        return jsonify({
            "success": True,
            "message": "కాన్ఫిగరేషన్ సేవ్ చేయబడింది!",
            "config": {
                "has_token": bool(saved_token),
                "masked_token": masked_token,
                "chat_id": cfg.get("chat_id", "")
            }
        })
    
    cfg = load_config()
    token = cfg.get("bot_token", "")
    masked_token = (token[:6] + "..." + token[-4:]) if len(token) > 10 else ("Configured" if token else "")
    return jsonify({
        "success": True,
        "has_token": bool(token),
        "masked_token": masked_token,
        "chat_id": cfg.get("chat_id", "")
    })

@app.route("/api/telegram/test", methods=["POST"])
def api_telegram_test():
    data = request.json or {}
    token = data.get("bot_token")
    chat_id = data.get("chat_id")
    test_msg = "🔔 <b>టెస్ట్ అలర్ట్:</b> మీ తెలుగు కరెంట్ అఫైర్స్ టెలిగ్రామ్ బోట్ విజయవంతంగా కనెక్ట్ అయింది! 🚀"
    res = send_telegram_message(test_msg, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/telegram/send", methods=["POST"])
def api_telegram_send():
    data = request.json or {}
    date = data.get("date")
    token = data.get("bot_token")
    chat_id = data.get("chat_id")
    res = broadcast_daily_digest(date=date, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/telegram/send_epaper_pdf", methods=["POST"])
def api_telegram_send_epaper_pdf():
    data = request.json or {}
    date = data.get("date") or request.args.get("date")
    token = data.get("bot_token")
    chat_id = data.get("chat_id")
    res = send_daily_epaper_pdf(date=date, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/epaper/pdf", methods=["GET"])
def api_epaper_pdf():
    date = request.args.get("date")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")
    
    pdf_path = generate_epaper_pdf(date=date)
    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "error": "PDF జనరేట్ చేయడం సాధ్యపడలేదు."}), 500
    
    return send_from_directory(
        os.path.dirname(pdf_path),
        os.path.basename(pdf_path),
        as_attachment=True,
        download_name=f"Lakshya_Telugu_EPaper_{date}.pdf"
    )

@app.route("/api/epaper/links", methods=["GET"])
def api_epaper_links():
    return jsonify({
        "success": True,
        "epapers": OFFICIAL_TELUGU_EPAPERS
    })

# ----------------- Scheduler Endpoints -----------------
@app.route("/api/scheduler/config", methods=["GET", "POST"])
def api_scheduler_config():
    if request.method == "POST":
        data = request.json or {}
        enabled = data.get("enabled", True)
        time_val = data.get("scheduled_time", "07:00")
        auto_tg = data.get("auto_telegram", True)
        cfg = save_scheduler_config(enabled=enabled, scheduled_time=time_val, auto_telegram=auto_tg)
        return jsonify({"success": True, "message": "షెడ్యూలర్ సెట్టింగ్స్ సేవ్ చేయబడ్డాయి!", "config": cfg})
    
    cfg = load_scheduler_config()
    return jsonify({"success": True, "config": cfg})

@app.route("/api/scheduler/trigger", methods=["POST"])
def api_scheduler_trigger():
    res = run_daily_job()
    return jsonify({"success": True, "message": "డైలీ జాబ్ విజయవంతంగా రన్ అయింది!", "result": res})

# ----------------- Subject-wise Mock Tests Endpoints (Feature 4) -----------------
@app.route("/api/mock_tests", methods=["GET"])
def api_mock_tests_list():
    summary = {}
    for key, data in SUBJECT_MOCK_TESTS.items():
        summary[key] = {
            "key": key,
            "title": data["title"],
            "icon": data["icon"],
            "description": data["description"],
            "total_questions": len(data["questions"])
        }
    return jsonify({"success": True, "subjects": summary})

@app.route("/api/mock_tests/<subject>", methods=["GET"])
def api_mock_test_subject(subject):
    data = SUBJECT_MOCK_TESTS.get(subject)
    if not data:
        return jsonify({"success": False, "error": "సబ్జెక్ట్ అందుబాటులో లేదు"}), 404
    return jsonify({"success": True, "subject": subject, "data": data})

# ----------------- Native Telugu Audio TTS Endpoints -----------------
@app.route("/api/audio", methods=["GET"])
def api_audio_text():
    text = request.args.get("text", "").strip()
    if not text:
        return jsonify({"error": "Text is required"}), 400
    audio_bytes = generate_telugu_audio(text)
    return Response(audio_bytes, mimetype="audio/mpeg")

@app.route("/api/audio/article/<int:article_id>", methods=["GET"])
def api_audio_article(article_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, summary FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Article not found"}), 404
    
    text = f"{row['title']}. {row['summary']}"
    audio_bytes = generate_telugu_audio(text)
    return Response(audio_bytes, mimetype="audio/mpeg")

@app.route("/api/audio/daily", methods=["GET"])
def api_audio_daily():
    date = request.args.get("date")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else None
    
    articles = get_articles(date=date)
    if not articles:
        return jsonify({"error": "No articles found"}), 404

    text = f"పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్. తేదీ {date}. "
    for idx, a in enumerate(articles[:6], 1):
        text += f"ముఖ్యాంశం {idx}. {a['title']}. {a['summary']}. "

    audio_bytes = generate_telugu_audio(text)
    return Response(audio_bytes, mimetype="audio/mpeg")

# ----------------- Grand Mock Test Paper with OMR Sheet Route -----------------
@app.route("/omr_test")
def omr_test_view():
    return generate_omr_test_html()

@app.route("/omr_group2")
def omr_group2_view():
    mode = request.args.get("mode", "full")
    section_id = request.args.get("section")
    return generate_group2_omr_test_html(mode=mode, section_id=section_id)

# ----------------- 3D Revision Flashcards API -----------------
@app.route("/api/flashcards", methods=["GET"])
def api_flashcards():
    category = request.args.get("category", "all")
    exam = request.args.get("exam", "all")
    date = request.args.get("date")
    
    conn = get_connection()
    c = conn.cursor()
    
    # Query articles
    query = "SELECT * FROM articles"
    params = []
    conditions = []
    if category and category != "all":
        conditions.append("category = ?")
        params.append(category)
    if date:
        conditions.append("date = ?")
        params.append(date)
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id DESC LIMIT 50"
    c.execute(query, params)
    articles = [dict(row) for row in c.fetchall()]
    
    # Query quiz questions
    q_query = "SELECT * FROM quiz_questions"
    q_params = []
    q_conds = []
    if category and category != "all":
        q_conds.append("category = ?")
        q_params.append(category)
    if date:
        q_conds.append("date = ?")
        q_params.append(date)
    if q_conds:
        q_query += " WHERE " + " AND ".join(q_conds)
    q_query += " ORDER BY id DESC LIMIT 30"
    c.execute(q_query, q_params)
    quizzes = [dict(row) for row in c.fetchall()]
    conn.close()
    
    flashcards = []
    
    # Convert articles to flashcards
    for a in articles:
        if exam and exam != "all":
            exam_lower = exam.lower()
            tags_lower = (a.get("tags") or "").lower() + " " + (a.get("exam_relevance") or "").lower()
            if exam_lower not in tags_lower and exam_lower not in ["all", "మొత్తం"]:
                continue
        
        flashcards.append({
            "id": f"art_{a['id']}",
            "type": "article",
            "category": a.get("category", "national"),
            "date": a.get("date", ""),
            "exam_tags": a.get("tags") or a.get("exam_relevance") or "APPSC / TSPSC / UPSC",
            "source": a.get("source", "దినపత్రిక"),
            "front": a.get("title", ""),
            "back_summary": a.get("summary", ""),
            "back_details": a.get("detailed_notes") or a.get("exam_relevance") or "",
            "audio_text": f"{a.get('title', '')}. {a.get('summary', '')}"
        })
        
    # Convert quizzes to flashcards
    for q in quizzes:
        corr = q.get("correct_option", "A").upper()
        ans_text = q.get(f"option_{corr.lower()}", "")
        
        flashcards.append({
            "id": f"quiz_{q['id']}",
            "type": "quiz",
            "category": q.get("category", "national"),
            "date": q.get("date", ""),
            "exam_tags": q.get("exam_tag") or "APPSC / TSPSC",
            "source": "మాక్ క్విజ్",
            "front": q.get("question", ""),
            "back_summary": f"సరైన సమాధానం ({corr}): {ans_text}",
            "back_details": q.get("explanation", ""),
            "audio_text": f"ప్రశ్న: {q.get('question', '')}. సరైన సమాధానం: {ans_text}. వివరణ: {q.get('explanation', '')}"
        })
        
    return jsonify({
        "success": True,
        "total": len(flashcards),
        "data": flashcards
    })

# ----------------- CBT Mock Exam Questions API (Feature 1) -----------------
@app.route("/api/cbt_questions", methods=["GET"])
def api_cbt_questions():
    questions = get_all_50_mock_questions()
    return jsonify({
        "success": True,
        "total": len(questions),
        "duration_minutes": 45,
        "negative_marking": 0.33,
        "questions": questions
    })

# ----------------- APPSC Group 2 Full Syllabus Mock & PYQs API -----------------
@app.route("/api/appsc_group2/meta", methods=["GET"])
def api_appsc_group2_meta():
    return jsonify({
        "success": True,
        "metadata": get_appsc_group2_metadata()
    })

@app.route("/api/appsc_group2/questions", methods=["GET"])
def api_appsc_group2_questions():
    mode = request.args.get("mode", "full")  # full, quick, pyqs, section
    section_id = request.args.get("section", "")
    year = request.args.get("year", "")
    
    if mode == "pyqs":
        questions = get_appsc_group2_pyqs(year if year else None)
        duration = len(questions)
        title = f"APPSC గ్రూప్-2 గత సంవత్సరాల ప్రశ్నలు (Official PYQs {year or 'అన్నీ'})"
    elif mode == "quick":
        questions = get_appsc_group2_quick_test(50)
        duration = 50
        title = "APPSC గ్రూప్-2 మినీ గ్రాండ్ టెస్ట్ (50 ప్రశ్నలు - 5 విభాగాలు కలిపి)"
    elif mode == "section" and section_id:
        questions = get_appsc_group2_by_section(section_id)
        duration = 30
        sec_name = next((s["name"] for s in APPSC_GROUP2_SECTIONS if s["id"] == section_id), section_id)
        title = f"APPSC గ్రూప్-2 {sec_name} (30 ప్రశ్నలు)"
    else:
        # Full 150 questions combined
        questions = get_appsc_group2_full_mock()
        duration = 150
        title = "APPSC గ్రూప్-2 సంపూర్ణ గ్రాండ్ మాక్ టెస్ట్ (150 ప్రశ్నలు - మొత్తం 5 విభాగాలు కలిపి)"
        
    return jsonify({
        "success": True,
        "title": title,
        "mode": mode,
        "total": len(questions),
        "duration_minutes": duration,
        "negative_marking": 0.33,
        "sections": APPSC_GROUP2_SECTIONS,
        "questions": questions
    })

# ----------------- Telugu AI Study Mentor & Doubt Solver API (Feature 4) -----------------
@app.route("/api/ai_mentor", methods=["POST", "GET"])
def api_ai_mentor():
    if request.method == "POST":
        data = request.json or {}
        query = data.get("query", "").strip()
    else:
        query = request.args.get("query", "").strip()

    if not query:
        return jsonify({
            "success": False,
            "error": "దయచేసి మీ సందేహాన్ని టైప్ చేయండి."
        }), 400

    q_lower = query.lower()
    conn = get_connection()
    c = conn.cursor()

    # Search articles matching keywords
    keywords = [w for w in query.split() if len(w) > 2][:4]
    matched_articles = []
    if keywords:
        like_clauses = " OR ".join(["title LIKE ? OR summary LIKE ? OR detailed_notes LIKE ?" for _ in keywords])
        params = []
        for kw in keywords:
            params.extend([f"%{kw}%", f"%{kw}%", f"%{kw}%"])
        c.execute(f"SELECT * FROM articles WHERE {like_clauses} ORDER BY id DESC LIMIT 3", params)
        matched_articles = [dict(r) for r in c.fetchall()]

    # If no keyword match, get latest articles
    if not matched_articles:
        c.execute("SELECT * FROM articles ORDER BY id DESC LIMIT 2")
        matched_articles = [dict(r) for r in c.fetchall()]

    conn.close()

    # Formulate rich exam-focused response
    if "ఇస్రో" in query or "isro" in q_lower or "స్పేస్" in query or "space" in q_lower:
        topic_header = "🚀 ఇస్రో (ISRO) తాజా పరిణామాలు & సైన్స్-టెక్నాలజీ విశ్లేషణ"
        core_point = "ఇస్రో ప్రయోగాలు, శాటిలైట్ ప్రయోగ వేదికలు (శ్రీహరికోట సతీష్ ధావన్ స్పేస్ సెంటర్), SSLV, PSLV, GSLV లాంచ్ వెహికల్స్ మరియు అంతరిక్ష మిషన్లు (గగన్‌యాన్, చంద్రయాన్, ఆదిత్య L1) APPSC, TSPSC & UPSC పరీక్షలలో సైన్స్ & టెక్నాలజీ విభాగంలో ప్రధానమైనవి."
        exam_tips = [
            "ప్రయోగం జరిగిన తేదీ మరియు ఉపయోగించిన లాంచ్ వెహికల్ పేరు గుర్తుంచుకోవాలి.",
            "శాటిలైట్ యొక్క ప్రధాన ఉద్దేశం (కమ్యూనికేషన్, రిమోట్ సెన్సింగ్ లేదా నావిగేషన్).",
            "ఇస్రో ప్రస్తుత చైర్మన్ మరియు ముఖ్య డైరెక్టర్ల పేర్లు గ్రూప్-2 స్థాయి పరీక్షలకు కీలకం."
        ]
    elif "పథకం" in query or "పథకాలు" in query or "స్కీమ్" in query or "scheme" in q_lower:
        topic_header = "🌾 ప్రభుత్వ సంక్షేమ పథకాలు (Welfare Schemes Analysis)"
        core_point = "ఆంధ్రప్రదేశ్ మరియు తెలంగాణ రాష్ట్ర ప్రభుత్వాల సంక్షేమ పథకాలు, రైతు సంక్షేమం, మహిళా సాధికారత, విద్యా-వైద్య రంగాలు గ్రూప్స్ పరీక్షలలో 10 నుండి 15 మార్కులను కవర్ చేస్తాయి."
        exam_tips = [
            "పథకం ప్రారంభించిన తేదీ మరియు ప్రదేశం స్పష్టంగా చదవాలి.",
            "లబ్ధిదారుల అర్హత ప్రమాణాలు మరియు వార్షిక బడ్జెట్ కేటాయింపులు ముఖ్యం.",
            "పథకం కింద అందించే ప్రత్యక్ష ఆర్థిక సహాయం లేదా ఇన్సెంటివ్ వివరాలు గుర్తుపెట్టుకోవాలి."
        ]
    elif "ఆర్బీఐ" in query or "rbi" in q_lower or "బ్యాంక్" in query or "ద్రవ్యోల్బణం" in query or "economy" in q_lower or "ఆర్థికం" in query:
        topic_header = "📈 భారత ఆర్థిక వ్యవస్థ & బ్యాంకింగ్ ముఖ్యాంశాలు"
        core_point = "ఆర్బీఐ మానిటరీ పాలసీ కమిటీ (MPC) నిర్ణయాలు, రెపో రేటు, రివర్స్ రెపో రేటు, రిటైల్ ద్రవ్యోల్బణం (CPI) మరియు GDP వృద్ధి అంచనాలు సివిల్స్ మరియు గ్రూప్-1 ఎకానమీ విభాగంలో కీలకం."
        exam_tips = [
            "ద్రవ్యోల్బణాన్ని అదుపు చేయడానికి ఆర్బీఐ తీసుకునే క్వాంటిటేటివ్ చర్యలు (CRR, SLR, Repo).",
            "కేంద్ర బడ్జెట్ మరియు ఆర్థిక సర్వేలోని ముఖ్య అంకెలు, రెవెన్యూ లోటు వివరాలు."
        ]
    elif "రాజ్యాంగం" in query or "పాలిటీ" in query or "polity" in q_lower or "constitution" in q_lower or "ఆర్టికల్" in query:
        topic_header = "🏛️ భారత రాజ్యాంగం & పాలిటీ (Indian Polity & Governance)"
        core_point = "ప్రాథమిక హక్కులు (Articles 12-35), ఆదేశిక సూత్రాలు (Articles 36-51), ఎన్నికల సంఘం (Article 324), సుప్రీంకోర్టు తీర్పులు మరియు తాజా రాజ్యాంగ సవరణలు పరీక్షల్లో తప్పనిసరిగా వస్తాయి."
        exam_tips = [
            "సుప్రీంకోర్టు రాజ్యాంగ ధర్మాసనం ఇచ్చిన తాజా తీర్పులు మరియు ప్రాథమిక హక్కుల విస్తరణ.",
            "కేంద్ర-రాష్ట్ర సంబంధాలు మరియు గవర్నర్ అధికారాలకు సంబంధించిన ఆర్టికల్స్."
        ]
    else:
        topic_header = f"📚 పోటీ పరీక్షల స్మార్ట్ విశ్లేషణ: {query[:40]}"
        core_point = f"మీరు అడిగిన '{query}' అంశం ప్రస్తుత పోటీ పరీక్షల సిలబస్ (జనరల్ స్టడీస్ & సమకాలీన అంశాలు) లో ఎంతో ప్రాధాన్యత కలిగినది."
        exam_tips = [
            "ఈ అంశానికి సంబంధించిన చారిత్రక నేపథ్యం మరియు ప్రస్తుత తాజా పరిణామాలను కలిపి చదవాలి.",
            "పరీక్షలో నేరుగా ప్రశ్న అడగటమే కాకుండా విశ్లేషణాత్మక స్టేట్‌మెంట్ బేస్డ్ ప్రశ్నలు వచ్చే అవకాశం ఉంది."
        ]

    related_notes = []
    for a in matched_articles[:2]:
        related_notes.append({
            "title": a["title"],
            "summary": a["summary"],
            "date": a["date"],
            "category": a["category"]
        })

    return jsonify({
        "success": True,
        "query": query,
        "response": {
            "header": topic_header,
            "core_point": core_point,
            "exam_tips": exam_tips,
            "related_articles": related_notes
        }
    })

# ----------------- Map Pointing Hub Endpoints -----------------
@app.route("/api/map_pointing", methods=["GET"])
def api_map_pointing():
    from map_pointing_data import get_all_map_points, get_map_points_by_domain
    domain = request.args.get("domain", "all")
    points = get_map_points_by_domain(domain)
    return jsonify({
        "success": True,
        "total": len(points),
        "domain": domain,
        "data": points
    })

@app.route("/api/map_pointing/quiz", methods=["GET"])
def api_map_pointing_quiz():
    from map_pointing_data import get_map_pointing_quiz_questions
    domain = request.args.get("domain", "all")
    quizzes = get_map_pointing_quiz_questions(domain)
    return jsonify({
        "success": True,
        "total": len(quizzes),
        "domain": domain,
        "questions": quizzes
    })

@app.route("/map_pointing_atlas", methods=["GET"])
def map_pointing_atlas_view():
    from map_pointing_atlas import render_map_pointing_atlas_html
    return render_map_pointing_atlas_html()

# ----------------- AP History & Multi-Exam Endpoints -----------------
@app.route("/api/ap_history", methods=["GET"])
def api_ap_history():
    from ap_history_data import get_all_ap_history_topics, get_ap_history_questions
    return jsonify({
        "success": True,
        "topics": get_all_ap_history_topics(),
        "questions": get_ap_history_questions()
    })

@app.route("/api/appsc_exams", methods=["GET"])
def api_appsc_exams():
    from ap_history_data import get_appsc_exam_questions, APPSC_EXAM_TYPES
    exam_type = request.args.get("exam", "group2")
    info = APPSC_EXAM_TYPES.get(exam_type, APPSC_EXAM_TYPES["group2"])
    qs = get_appsc_exam_questions(exam_type)
    return jsonify({
        "success": True,
        "exam_type": exam_type,
        "info": info,
        "total": len(qs),
        "questions": qs
    })

# ----------------- Welfare Schemes & Budget Endpoints -----------------
@app.route("/api/schemes", methods=["GET"])
def api_schemes():
    from schemes_budget_data import get_schemes_by_category, get_schemes_quizzes
    category = request.args.get("category", "all")
    schemes = get_schemes_by_category(category)
    return jsonify({
        "success": True,
        "category": category,
        "total": len(schemes),
        "schemes": schemes,
        "quizzes": get_schemes_quizzes()
    })

# ----------------- Mains Model Answers Endpoints -----------------
@app.route("/api/mains/questions", methods=["GET"])
def api_mains_questions():
    from mains_descriptive_data import get_all_mains_questions
    qs = get_all_mains_questions()
    return jsonify({
        "success": True,
        "total": len(qs),
        "questions": qs
    })

# ----------------- Printable Handbooks & Multi-Exam OMR -----------------
@app.route("/schemes_handbook", methods=["GET"])
def schemes_handbook_view():
    from appsc_handbooks import render_schemes_handbook_html
    return render_schemes_handbook_html()

@app.route("/mains_answer_bank", methods=["GET"])
def mains_answer_bank_view():
    from appsc_handbooks import render_mains_answer_bank_html
    return render_mains_answer_bank_html()

@app.route("/omr_appsc_all", methods=["GET"])
def omr_appsc_all_view():
    from appsc_handbooks import render_omr_appsc_all_html
    exam_type = request.args.get("exam", "group2")
    return render_omr_appsc_all_html(exam_type)

if __name__ == "__main__":
    print("==================================================================")
    print("🚀 తెలుగు పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్ డ్యాష్‌బోర్డ్ ప్రారంభమైంది!")
    print("🌐 బ్రౌజర్‌లో ఓపెన్ చేయండి: http://localhost:5000")
    print("==================================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
