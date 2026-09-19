# -*- coding: utf-8 -*-
"""
Main Flask Application for Daily Current Affairs (తెలుగు పోటీ పరీక్షల డ్యాష్‌బోర్డ్)
Provides REST API endpoints and serves frontend files.
"""

from flask import Flask, jsonify, request, send_from_directory, Response, render_template_string
import os
import sys
import json
import threading
from datetime import datetime, timezone, timedelta
from tts import generate_telugu_audio

# India Standard Time (IST is UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

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
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100 MB upload limit

@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({"success": False, "error": "ఫైల్ పరిమాణం చాలా పెద్దది (గరిష్టంగా 100MB వరకు అనుమతి)."}), 413

# Ensure DB has tables and initial seed data
init_db()
populate_seed_data()

# Startup check: ensure today's news (IST) is synced in DB
def ensure_today_synced():
    try:
        import threading
        def _sync_worker():
            import time
            time.sleep(2)
            today_ist = datetime.now(IST).strftime("%Y-%m-%d")
            dates = get_available_dates()
            if today_ist not in dates:
                print(f"🔄 [Startup Auto-Sync] నేటి ({today_ist}) వార్తలు డేటాబేస్‌లో లేవు, సింక్ చేస్తున్నాం...")
                sync_daily_news(target_date=today_ist)
                from quiz_generator import ensure_daily_quizzes
                ensure_daily_quizzes(date=today_ist)
                try:
                    generate_epaper_pdf(today_ist, force_refresh=True)
                except Exception as pdf_e:
                    print(f"Startup PDF compilation error: {pdf_e}")
                print(f"✅ [Startup Auto-Sync] నేటి ({today_ist}) వార్తలు, క్విజ్ మరియు ఈ-పేపర్ PDF విజయవంతంగా సిద్ధమయ్యాయి.")
        threading.Thread(target=_sync_worker, daemon=True).start()
    except Exception as e:
        print("Startup sync error:", e)

ensure_today_synced()

# Start background morning scheduler thread
start_scheduler_thread()

# Start background Telegram bot polling thread when hosted on cloud
def start_embedded_bot():
    def _run_bot_worker():
        # Prevent multiple gunicorn workers from concurrent getUpdates polling (avoids Telegram 409 Conflict)
        try:
            import tempfile, fcntl
            lock_path = os.path.join(tempfile.gettempdir(), "lakshya_bot_polling.lock")
            lock_file = open(lock_path, "w")
            try:
                fcntl.flock(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except (BlockingIOError, IOError):
                print("🤖 [Embedded Bot] Another gunicorn worker is already polling. Skipping.")
                return
        except ImportError:
            pass  # Windows or environment without fcntl

        try:
            from run_bot import start_bot_polling
            print("🤖 [Embedded Bot] టెలిగ్రామ్ బోట్ బ్యాక్‌గ్రౌండ్ థ్రెడ్ ప్రారంభమైంది.")
            start_bot_polling()
        except Exception as e:
            print("⚠️ Embedded bot error:", e)

    import threading
    threading.Thread(target=_run_bot_worker, daemon=True).start()

if os.environ.get("RENDER") or os.environ.get("START_EMBEDDED_BOT"):
    start_embedded_bot()

# Keep-Alive Worker: Self-pings every 10 minutes to prevent Render free-tier sleep
def start_keep_alive_worker():
    def _pinger():
        import time
        import urllib.request
        import threading
        ping_url = os.environ.get("RENDER_EXTERNAL_URL", "https://lakshya-telugu-ca.onrender.com") + "/api/ping"
        time.sleep(45)
        while True:
            try:
                req = urllib.request.Request(ping_url, headers={"User-Agent": "Lakshya-KeepAlive/1.0"})
                with urllib.request.urlopen(req, timeout=15) as res:
                    pass
                print(f"💓 [Keep-Alive] సర్వర్ పింగ్ విజయవంతం: {ping_url}")
            except Exception as e:
                pass
            time.sleep(600)  # Ping every 10 minutes

    threading.Thread(target=_pinger, daemon=True).start()

if os.environ.get("RENDER") or os.environ.get("START_KEEP_ALIVE"):
    start_keep_alive_worker()

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
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

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
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

    from quiz_generator import ensure_daily_quizzes
    quizzes = ensure_daily_quizzes(date=date)
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
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

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
        from quiz_generator import ensure_daily_quizzes
        target_date = date or result.get("date")
        if target_date:
            ensure_daily_quizzes(target_date)
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

# ----------------- Health & Keep-Alive -----------------
@app.route("/api/ping", methods=["GET"])
@app.route("/api/health", methods=["GET"])
def api_health():
    now_ist = datetime.now(IST)
    dates = get_available_dates()
    return jsonify({
        "status": "healthy",
        "app": "Lakshya Telugu Current Affairs",
        "ist_time": now_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
        "today_date": now_ist.strftime("%Y-%m-%d"),
        "total_available_dates": len(dates),
        "latest_date": dates[0] if dates else None,
        "uptime": "online 24/7"
    })

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

@app.route("/api/telegram/test", methods=["POST", "GET"])
def api_telegram_test():
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    token = data.get("bot_token") or request.args.get("bot_token")
    chat_id = data.get("chat_id") or request.args.get("chat_id")
    test_msg = "🔔 <b>టెస్ట్ అలర్ట్:</b> మీ తెలుగు కరెంట్ అఫైర్స్ టెలిగ్రామ్ బోట్ విజయవంతంగా కనెక్ట్ అయింది! 🚀"
    res = send_telegram_message(test_msg, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/telegram/send", methods=["POST", "GET"])
def api_telegram_send():
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    date = data.get("date") or request.args.get("date")
    token = data.get("bot_token") or request.args.get("bot_token")
    chat_id = data.get("chat_id") or request.args.get("chat_id")
    res = broadcast_daily_digest(date=date, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/telegram/send_epaper_pdf", methods=["POST", "GET"])
def api_telegram_send_epaper_pdf():
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    date = request.args.get("date") or data.get("date")
    token = request.args.get("bot_token") or data.get("bot_token")
    chat_id = request.args.get("chat_id") or data.get("chat_id")
    res = send_daily_epaper_pdf(date=date, token=token, chat_id=chat_id)
    return jsonify(res)


@app.route("/api/telegram/channels", methods=["GET", "POST", "DELETE"])
def api_telegram_channels():
    from telegram_bot import load_channels, add_channel, remove_channel
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        channel_id = data.get("channel_id") or request.args.get("channel_id")
        title = data.get("title") or request.args.get("title", "")
        if not channel_id:
            return jsonify({"success": False, "error": "Channel ID / Username అవసరం."}), 400
        chs = add_channel(channel_id, title)
        return jsonify({"success": True, "message": "ఛానల్ విజయవంతంగా సేవ్ చేయబడింది!", "channels": chs})
    elif request.method == "DELETE":
        data = request.get_json(silent=True) or {}
        channel_id = data.get("channel_id") or request.args.get("channel_id")
        chs = remove_channel(channel_id)
        return jsonify({"success": True, "message": "ఛానల్ తొలగించబడింది!", "channels": chs})
    else:
        return jsonify({"success": True, "channels": load_channels()})

@app.route("/api/telegram/send_monthly_magazine", methods=["POST", "GET"])
def api_telegram_send_monthly():
    from telegram_bot import send_monthly_magazine_telegram
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    month = data.get("month") or request.args.get("month", "2026-09")
    token = data.get("bot_token") or request.args.get("bot_token")
    chat_id = data.get("chat_id") or request.args.get("chat_id")
    res = send_monthly_magazine_telegram(month=month, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/epaper/pdf", methods=["GET"])
def api_epaper_pdf():
    date = request.args.get("date")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")
    
    pdf_path = generate_epaper_pdf(date=date)
    if not pdf_path or not os.path.exists(pdf_path):
        fallback_today = os.path.join(FRONTEND_DIR, "pdfs", "daily_epaper_today.pdf")
        if os.path.exists(fallback_today):
            pdf_path = fallback_today
        else:
            return jsonify({"success": False, "error": "PDF జనరేట్ చేయడం సాధ్యపడలేదు."}), 500
    
    return send_from_directory(
        os.path.dirname(pdf_path),
        os.path.basename(pdf_path),
        as_attachment=True,
        download_name=f"Lakshya_Telugu_EPaper_{date}.pdf"
    )


@app.route("/api/magazine/pdf", methods=["GET"])
@app.route("/api/magazine/download", methods=["GET"])
def api_magazine_pdf():
    month = request.args.get("month", "2026-09")
    as_download = request.args.get("download", "0") == "1" or request.path.endswith("/download")
    
    cache_dir = os.path.join(os.path.dirname(__file__), "pdf_cache")
    candidates = [
        os.path.join(FRONTEND_DIR, "pdfs", "Lakshya_September_2026_Monthly_Magazine.pdf"),
        os.path.join(FRONTEND_DIR, "pdfs", f"Lakshya_{month}_Monthly_Magazine.pdf"),
        os.path.join(cache_dir, f"Lakshya_Telugu_Monthly_{month}.pdf")
    ]
    pdf_path = None
    for p in candidates:
        if os.path.exists(p) and os.path.getsize(p) > 1000:
            pdf_path = p
            break
            
    if not pdf_path:
        from magazine import generate_magazine_pdf
        pdf_path = generate_magazine_pdf(year_month=month, force_refresh=False)

    if not pdf_path or not os.path.exists(pdf_path):
        return jsonify({"success": False, "error": "మాస పత్రిక PDF సిద్ధంగా లేదు."}), 404

    return send_from_directory(
        os.path.dirname(pdf_path),
        os.path.basename(pdf_path),
        as_attachment=as_download,
        download_name=f"Lakshya_Monthly_Magazine_{month}.pdf",
        mimetype="application/pdf"
    )


@app.route("/api/audio/daily_bulletin", methods=["GET"])
def api_audio_daily_bulletin():
    voice = (request.args.get("voice") or "mohan").lower().strip()
    frontend_audio_dir = os.path.join(FRONTEND_DIR, "audio")
    static_file = os.path.join(frontend_audio_dir, f"daily_bulletin_{voice}.mp3")
    if os.path.exists(static_file) and os.path.getsize(static_file) > 10000:
        resp = send_from_directory(
            frontend_audio_dir,
            f"daily_bulletin_{voice}.mp3",
            mimetype="audio/mpeg"
        )
        resp.headers["Cache-Control"] = "no-cache, must-revalidate"
        resp.headers["Accept-Ranges"] = "bytes"
        return resp

    from tts import generate_daily_bulletin_audio
    date = request.args.get("date")
    audio_path = generate_daily_bulletin_audio(date=date, voice=voice)
    if not audio_path or not os.path.exists(audio_path):
        return jsonify({"success": False, "error": "ఆడియో బులెటిన్ అందుబాటులో లేదు."}), 404
    resp = send_from_directory(
        os.path.dirname(audio_path),
        os.path.basename(audio_path),
        mimetype="audio/mpeg"
    )
    resp.headers["Cache-Control"] = "no-cache, must-revalidate"
    resp.headers["Accept-Ranges"] = "bytes"
    return resp

@app.route("/api/telegram/send_bulletin_audio", methods=["POST", "GET"])
def api_telegram_send_audio():
    from telegram_bot import send_daily_bulletin_audio
    try:
        data = request.get_json(silent=True) or {}
    except Exception:
        data = {}
    date = request.args.get("date") or data.get("date")
    token = request.args.get("bot_token") or data.get("bot_token")
    chat_id = request.args.get("chat_id") or data.get("chat_id")
    res = send_daily_bulletin_audio(date=date, token=token, chat_id=chat_id)
    return jsonify(res)

@app.route("/api/audio/tracks", methods=["GET"])
def api_audio_tracks():
    from audio_revision_data import get_all_audio_tracks
    tracks = get_all_audio_tracks()
    compact = []
    for t in tracks:
        c = dict(t)
        compact.append(c)
    return jsonify({"success": True, "tracks": compact})

@app.route("/api/audio/track/<track_id>", methods=["GET"])
def api_audio_syllabus_track(track_id):
    voice = (request.args.get("voice") or "mohan").lower().strip()
    frontend_audio_dir = os.path.join(FRONTEND_DIR, "audio")
    static_file = os.path.join(frontend_audio_dir, f"{track_id}_{voice}.mp3")
    if os.path.exists(static_file) and os.path.getsize(static_file) > 10000:
        resp = send_from_directory(
            frontend_audio_dir,
            f"{track_id}_{voice}.mp3",
            mimetype="audio/mpeg"
        )
        resp.headers["Cache-Control"] = "no-cache, must-revalidate"
        resp.headers["Accept-Ranges"] = "bytes"
        return resp

    from tts import generate_syllabus_audio_track
    audio_path = generate_syllabus_audio_track(track_id, voice=voice)
    if not audio_path or not os.path.exists(audio_path):
        return jsonify({"success": False, "error": "ఆడియో ట్రాక్ అందుబాటులో లేదు."}), 404
    resp = send_from_directory(
        os.path.dirname(audio_path),
        os.path.basename(audio_path),
        mimetype="audio/mpeg"
    )
    resp.headers["Cache-Control"] = "no-cache, must-revalidate"
    resp.headers["Accept-Ranges"] = "bytes"
    return resp

@app.route("/epapers_directory", methods=["GET"])
@app.route("/epapers", methods=["GET"])
def epapers_directory_view():
    from epapers_directory import render_epapers_directory_html
    return render_epapers_directory_html()

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

@app.route("/api/scheduler/trigger", methods=["POST", "GET"])
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
    voice = request.args.get("voice", "mohan")
    if not text:
        return jsonify({"error": "Text is required"}), 400
    audio_bytes = generate_telugu_audio(text, voice=voice)
    return Response(audio_bytes, mimetype="audio/mpeg")

@app.route("/api/audio/article/<int:article_id>", methods=["GET"])
def api_audio_article(article_id):
    voice = request.args.get("voice", "mohan")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT title, summary FROM articles WHERE id = ?", (article_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Article not found"}), 404
    
    text = f"{row['title']}. {row['summary']}"
    audio_bytes = generate_telugu_audio(text, voice=voice)
    return Response(audio_bytes, mimetype="audio/mpeg")

@app.route("/api/audio/daily", methods=["GET"])
def api_audio_daily():
    date = request.args.get("date")
    voice = request.args.get("voice", "mohan")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else None
    
    articles = get_articles(date=date)
    if not articles:
        return jsonify({"error": "No articles found"}), 404

    text = f"పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్. తేదీ {date}. "
    for idx, a in enumerate(articles[:6], 1):
        text += f"ముఖ్యాంశం {idx}. {a['title']}. {a['summary']}. "

    audio_bytes = generate_telugu_audio(text, voice=voice)
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


@app.route("/api/mains", methods=["GET"])
def api_mains():
    from mains_descriptive_data import get_all_mains_questions
    qs = get_all_mains_questions()
    return jsonify({
        "success": True,
        "total": len(qs),
        "questions": qs
    })

@app.route("/api/subject_tests", methods=["GET"])
def api_subject_tests():
    from subject_tests_data import get_all_subject_tests
    return jsonify({
        "success": True,
        "tests": get_all_subject_tests()
    })

@app.route("/api/subject_tests/<subject_id>", methods=["GET"])
def api_subject_test_single(subject_id):
    from subject_tests_data import get_subject_test
    test = get_subject_test(subject_id)
    if not test:
        return jsonify({"success": False, "error": f"{subject_id} సబ్జెక్ట్ టెస్ట్ లభించలేదు."}), 404
    return jsonify({
        "success": True,
        "subject": subject_id,
        "test": test
    })

@app.route("/subject_tests", methods=["GET"])
def subject_tests_view():
    from flask import make_response
    from subject_tests_view import render_subject_tests_html
    subj = request.args.get("subject", "history")
    resp = make_response(render_subject_tests_html(subj))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


# ----------------- Solved PYQs Master Hub Endpoints -----------------
@app.route("/api/pyqs_hub", methods=["GET"])
def api_pyqs_hub():
    from pyqs_master_data import get_all_pyq_papers, get_all_pyq_questions
    return jsonify({
        "success": True,
        "papers": get_all_pyq_papers(),
        "total_questions": len(get_all_pyq_questions()),
        "questions": get_all_pyq_questions()
    })

@app.route("/api/pyqs_hub/<paper_id>", methods=["GET"])
def api_pyqs_paper(paper_id):
    from pyqs_master_data import get_pyq_paper
    p = get_pyq_paper(paper_id)
    if not p:
        return jsonify({"success": False, "error": f"{paper_id} పేపర్ లభించలేదు."}), 404
    return jsonify({
        "success": True,
        "paper": p
    })

@app.route("/pyqs_hub", methods=["GET"])
def pyqs_hub_view():
    from flask import make_response
    from pyqs_view import render_pyqs_hub_html
    paper = request.args.get("paper", "all")
    resp = make_response(render_pyqs_hub_html(paper))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

# ----------------- Rapid Revision Flashcards Deck Endpoints -----------------
@app.route("/api/flashcards_deck", methods=["GET"])
def api_flashcards_deck():
    from flashcards_data import get_all_flashcards, get_flashcard_categories
    cat = request.args.get("cat", "all")
    from flashcards_data import get_flashcards_by_category
    cards = get_flashcards_by_category(cat)
    return jsonify({
        "success": True,
        "total": len(cards),
        "categories": get_flashcard_categories(),
        "cards": cards
    })

@app.route("/flashcards_deck", methods=["GET"])
def flashcards_deck_view():
    from flask import make_response
    from flashcards_view import render_flashcards_deck_html
    cat = request.args.get("cat", "all")
    resp = make_response(render_flashcards_deck_html(cat))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

# ----------------- Districts Master Guide Endpoints -----------------
@app.route("/api/districts_guide", methods=["GET"])
def api_districts_guide():
    from districts_master_data import get_all_districts, get_ap_districts, get_ts_districts
    state = request.args.get("state", "all")
    if state == "ap":
        data = get_ap_districts()
    elif state == "ts":
        data = get_ts_districts()
    else:
        data = get_all_districts()
    return jsonify({
        "success": True,
        "total": len(data),
        "districts": data
    })

@app.route("/districts_guide", methods=["GET"])
def districts_guide_view():
    from flask import make_response
    from districts_view import render_districts_guide_html
    state = request.args.get("state", "all")
    resp = make_response(render_districts_guide_html(state))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

# ----------------- AP & TS Budget & Economic Survey 2026 Endpoints -----------------
@app.route("/api/budget_economy", methods=["GET"])
def api_budget_economy():
    from budget_economy_data import get_budget_economy_data
    return jsonify({
        "success": True,
        "data": get_budget_economy_data()
    })

@app.route("/budget_economy_guide", methods=["GET"])
def budget_economy_guide_view():
    from flask import make_response
    from budget_economy_view import render_budget_economy_html
    state = request.args.get("state", "all")
    resp = make_response(render_budget_economy_html(state))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Daily Telugu Editorial Analysis Endpoints -----------------
@app.route("/api/editorials", methods=["GET"])
def api_editorials():
    from editorials_data import get_all_editorials
    paper = request.args.get("paper", "all")
    all_ed = get_all_editorials()
    if paper != "all":
        all_ed = [e for e in all_ed if paper.lower() in e["newspaper"].lower()]
    return jsonify({
        "success": True,
        "total": len(all_ed),
        "editorials": all_ed
    })

@app.route("/editorials_hub", methods=["GET"])
def editorials_hub_view():
    from flask import make_response
    from editorials_view import render_editorials_hub_html
    paper = request.args.get("paper", "all")
    resp = make_response(render_editorials_hub_html(paper))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Telugu AI Exam Doubt Solver Endpoints -----------------
@app.route("/api/doubt_solver/ask", methods=["POST"])
def api_doubt_solver_ask():
    from doubt_solver import solve_exam_doubt
    body = request.get_json() or {}
    query = body.get("query", "").strip()
    if not query:
        return jsonify({"success": False, "error": "సందేహం ఖాళీగా ఉండకూడదు"}), 400
    answer = solve_exam_doubt(query)
    return jsonify({
        "success": True,
        "answer": answer
    })

@app.route("/api/doubt_solver/suggested", methods=["GET"])
def api_doubt_solver_suggested():
    from doubt_solver import get_suggested_doubts
    return jsonify({
        "success": True,
        "suggestions": get_suggested_doubts()
    })

@app.route("/doubt_solver", methods=["GET"])
def doubt_solver_view():
    from flask import make_response
    from doubt_solver_view import render_doubt_solver_html
    resp = make_response(render_doubt_solver_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Live Daily Mock Test & State Leaderboard Endpoints -----------------
@app.route("/api/live_test/today", methods=["GET"])
def api_live_test_today():
    from daily_live_test_data import get_live_test_questions
    qs = get_live_test_questions()
    # Strip answers from client test payload
    safe_qs = []
    for q in qs:
        safe_qs.append({
            "id": q["id"],
            "question": q["question"],
            "options": q["options"],
            "subject": q.get("subject", "General Studies")
        })
    return jsonify({
        "success": True,
        "total": len(safe_qs),
        "time_minutes": 15,
        "negative_marking": 0.33,
        "questions": safe_qs
    })

@app.route("/api/live_test/submit", methods=["POST"])
def api_live_test_submit():
    from leaderboard_db import evaluate_and_submit_test
    body = request.get_json() or {}
    name = body.get("name", "పోటీ పరీక్షార్థి")
    district = body.get("district", "ఆంధ్రప్రదేశ్")
    target_exam = body.get("target_exam", "APPSC Group 2")
    answers = body.get("answers", {})
    time_spent = body.get("time_spent", "15:00")

    result = evaluate_and_submit_test(name, district, target_exam, answers, time_spent)
    return jsonify(result)

@app.route("/api/live_test/leaderboard", methods=["GET"])
def api_live_test_leaderboard():
    from leaderboard_db import get_top_leaderboard_entries
    limit = int(request.args.get("limit", 50))
    board = get_top_leaderboard_entries(limit)
    return jsonify({
        "success": True,
        "total": len(board),
        "leaderboard": board
    })

@app.route("/daily_live_test", methods=["GET"])
def daily_live_test_view():
    from flask import make_response
    from daily_live_test_view import render_daily_live_test_html
    resp = make_response(render_daily_live_test_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

@app.route("/appsc_syllabus", methods=["GET"])
@app.route("/syllabus", methods=["GET"])
@app.route("/appsc_master_portal", methods=["GET"])
def appsc_syllabus_view():
    from flask import make_response
    from appsc_master_syllabus import render_appsc_syllabus_html
    resp = make_response(render_appsc_syllabus_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp

# ----------------- AP Reorganisation Act 2014 Master Guide Endpoints -----------------
@app.route("/api/ap_bifurcation", methods=["GET"])
def api_ap_bifurcation():
    from ap_bifurcation_data import get_bifurcation_data
    return jsonify({
        "success": True,
        "data": get_bifurcation_data()
    })

@app.route("/ap_bifurcation_guide", methods=["GET"])
def ap_bifurcation_guide_view():
    from flask import make_response
    from ap_bifurcation_view import render_ap_bifurcation_html
    resp = make_response(render_ap_bifurcation_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Constitutional Amendments & SC Judgments Hub Endpoints -----------------
@app.route("/api/amendments_judgments", methods=["GET"])
def api_amendments_judgments():
    from amendments_judgments_data import get_amendments_judgments_data
    return jsonify({
        "success": True,
        "data": get_amendments_judgments_data()
    })

@app.route("/amendments_judgments", methods=["GET"])
def amendments_judgments_view():
    from flask import make_response
    from amendments_judgments_view import render_amendments_judgments_html
    resp = make_response(render_amendments_judgments_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Sunday Weekly Current Affairs Digest & Mega Test Endpoints -----------------
@app.route("/api/weekly_digest/data", methods=["GET"])
def api_weekly_digest_data():
    from weekly_compiler import get_weekly_digest_data
    return jsonify({
        "success": True,
        "data": get_weekly_digest_data()
    })

@app.route("/weekly_digest", methods=["GET"])
def weekly_digest_view():
    from flask import make_response
    from weekly_digest_view import render_weekly_digest_html
    resp = make_response(render_weekly_digest_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- AP & TS Schemes Comparison & Eligibility Matrix Endpoints -----------------
@app.route("/api/schemes_matrix", methods=["GET"])
def api_schemes_matrix():
    from schemes_matrix_data import get_schemes_matrix_data
    return jsonify({
        "success": True,
        "schemes": get_schemes_matrix_data()
    })

@app.route("/schemes_matrix", methods=["GET"])
def schemes_matrix_view():
    from flask import make_response
    from schemes_matrix_view import render_schemes_matrix_html
    resp = make_response(render_schemes_matrix_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp


# ----------------- Indian Polity Articles (1-395) Fast-Search Directory Endpoints -----------------
@app.route("/api/polity_articles", methods=["GET"])
def api_polity_articles():
    from polity_articles_data import get_polity_articles_data
    return jsonify({
        "success": True,
        "data": get_polity_articles_data()
    })

@app.route("/polity_articles", methods=["GET"])
def polity_articles_view():
    from flask import make_response
    from polity_articles_view import render_polity_articles_html
    resp = make_response(render_polity_articles_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Science, Technology & Defense 2025-2026 Mega Revision Hub Endpoints -----------------
@app.route("/api/science_tech", methods=["GET"])
def api_science_tech():
    from science_tech_data import get_science_tech_data
    return jsonify({
        "success": True,
        "data": get_science_tech_data()
    })

@app.route("/science_tech_hub", methods=["GET"])
def science_tech_hub_view():
    from flask import make_response
    from science_tech_view import render_science_tech_html
    resp = make_response(render_science_tech_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Environment, Biodiversity & Climate Change Master Hub Endpoints -----------------
@app.route("/api/environment", methods=["GET"])
def api_environment():
    from environment_data import get_environment_data
    return jsonify({
        "success": True,
        "data": get_environment_data()
    })

@app.route("/environment_hub", methods=["GET"])
def environment_hub_view():
    from flask import make_response
    from environment_view import render_environment_html
    resp = make_response(render_environment_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Central Government Flagship Schemes 2026 Master Handbook Endpoints -----------------
@app.route("/api/central_schemes", methods=["GET"])
def api_central_schemes():
    from central_schemes_data import get_central_schemes_data
    return jsonify({
        "success": True,
        "data": get_central_schemes_data()
    })

@app.route("/central_schemes", methods=["GET"])
def central_schemes_view():
    from flask import make_response
    from central_schemes_view import render_central_schemes_html
    resp = make_response(render_central_schemes_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp


# ----------------- Indian Society (30 Marks) Master Hub Endpoints -----------------
@app.route("/api/indian_society", methods=["GET"])
def api_indian_society():
    from indian_society_data import get_indian_society_data
    return jsonify({
        "success": True,
        "data": get_indian_society_data()
    })

@app.route("/indian_society_hub", methods=["GET"])
def indian_society_hub_view():
    from flask import make_response
    from indian_society_view import render_indian_society_html
    resp = make_response(render_indian_society_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- 60-Day Smart Daily Study Planner & Syllabus Tracker Endpoints -----------------
@app.route("/api/study_planner", methods=["GET"])
def api_study_planner():
    from study_planner_data import get_study_planner_data
    return jsonify({
        "success": True,
        "data": get_study_planner_data()
    })

@app.route("/study_planner", methods=["GET"])
def study_planner_view():
    from flask import make_response
    from study_planner_view import render_study_planner_html
    resp = make_response(render_study_planner_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- APPSC & TSPSC PYQs Deep Explorer & Analytics Endpoints -----------------
@app.route("/api/pyqs_explorer", methods=["GET"])
def api_pyqs_explorer():
    from pyqs_explorer_data import get_pyqs_explorer_data
    return jsonify({
        "success": True,
        "data": get_pyqs_explorer_data()
    })

@app.route("/pyqs_explorer", methods=["GET"])
def pyqs_explorer_view():
    from flask import make_response
    from pyqs_explorer_view import render_pyqs_explorer_html
    resp = make_response(render_pyqs_explorer_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Mental Ability & Aptitude Shortcuts Practice Engine Endpoints -----------------
@app.route("/api/mental_ability_hub", methods=["GET"])
def api_mental_ability_hub():
    from mental_ability_data import get_mental_ability_data
    return jsonify({
        "success": True,
        "data": get_mental_ability_data()
    })

@app.route("/mental_ability_hub", methods=["GET"])
def mental_ability_hub_view():
    from flask import make_response
    from mental_ability_view import render_mental_ability_html
    resp = make_response(render_mental_ability_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Audio Revision Player & Podcast Hub Endpoints -----------------
@app.route("/api/audio_revision", methods=["GET"])
def api_audio_revision():
    from audio_revision_data import get_all_audio_tracks
    return jsonify({
        "success": True,
        "data": get_all_audio_tracks()
    })

@app.route("/audio_revision", methods=["GET"])
@app.route("/audio_hub", methods=["GET"])
def audio_revision_view():
    from flask import make_response
    from audio_revision_view import render_audio_revision_html
    resp = make_response(render_audio_revision_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Mains Descriptive Answer Writing & Evaluation Portal Endpoints -----------------
@app.route("/api/mains_descriptive", methods=["GET"])
def api_mains_descriptive():
    from mains_descriptive_data import get_all_mains_questions
    return jsonify({
        "success": True,
        "data": get_all_mains_questions()
    })

@app.route("/mains_descriptive_portal", methods=["GET"])
def mains_descriptive_portal_view():
    from flask import make_response
    from mains_descriptive_view import render_mains_descriptive_html
    resp = make_response(render_mains_descriptive_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Student Performance Analytics & Weakness Diagnoser Endpoints -----------------
@app.route("/api/student_analytics", methods=["GET"])
def api_student_analytics():
    from student_analytics_data import get_student_analytics_benchmarks, get_demo_student_profile
    return jsonify({
        "success": True,
        "benchmarks": get_student_analytics_benchmarks(),
        "demo_profile": get_demo_student_profile()
    })

@app.route("/student_analytics", methods=["GET"])
def student_analytics_view():
    from flask import make_response
    from student_analytics_view import render_student_analytics_html
    resp = make_response(render_student_analytics_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Static GK Super-Fast Pocketbook Endpoints -----------------
@app.route("/api/static_gk", methods=["GET"])
def api_static_gk():
    from static_gk_data import get_all_static_gk_categories
    return jsonify({
        "success": True,
        "data": get_all_static_gk_categories()
    })

@app.route("/static_gk_pocketbook", methods=["GET"])
def static_gk_pocketbook_view():
    from flask import make_response
    from static_gk_view import render_static_gk_html
    resp = make_response(render_static_gk_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Supreme Court 30 Landmark Judgments Endpoints -----------------
@app.route("/api/sc_judgments", methods=["GET"])
def api_sc_judgments():
    from sc_judgments_data import get_all_landmark_judgments
    return jsonify({
        "success": True,
        "data": get_all_landmark_judgments()
    })

@app.route("/sc_judgments_hub", methods=["GET"])
def sc_judgments_hub_view():
    from flask import make_response
    from sc_judgments_view import render_sc_judgments_html
    resp = make_response(render_sc_judgments_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- APPSC Group-2 Paper-2 Mega Mains Portal Endpoints -----------------
@app.route("/api/group2_paper2", methods=["GET"])
def api_group2_paper2():
    from group2_paper2_data import get_paper2_syllabus, get_paper2_notes, get_paper2_mock_questions
    return jsonify({
        "success": True,
        "syllabus": get_paper2_syllabus(),
        "notes": get_paper2_notes(),
        "questions": get_paper2_mock_questions()
    })

@app.route("/group2_paper2_master", methods=["GET"])
def group2_paper2_master_view():
    from flask import make_response
    from group2_paper2_view import render_group2_paper2_html
    resp = make_response(render_group2_paper2_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- PWA Manifest & Service Worker Endpoints -----------------
@app.route("/manifest.json", methods=["GET"])
def pwa_manifest():
    return send_from_directory(FRONTEND_DIR, "manifest.json", mimetype="application/manifest+json")

@app.route("/service-worker.js", methods=["GET"])
def pwa_service_worker():
    from flask import make_response
    resp = make_response(send_from_directory(FRONTEND_DIR, "service-worker.js", mimetype="application/javascript"))
    resp.headers["Service-Worker-Allowed"] = "/"
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

@app.route("/sw.js", methods=["GET"])
def pwa_sw():
    from flask import make_response
    resp = make_response(send_from_directory(FRONTEND_DIR, "sw.js", mimetype="application/javascript"))
    resp.headers["Service-Worker-Allowed"] = "/"
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- AP & TS Agriculture & Irrigation Hub Endpoints -----------------
@app.route("/api/agri_irrigation", methods=["GET"])
def api_agri_irrigation():
    from agri_irrigation_data import get_agri_irrigation_data
    return jsonify({
        "success": True,
        "data": get_agri_irrigation_data()
    })

@app.route("/agri_irrigation_hub", methods=["GET"])
def agri_irrigation_hub_view():
    from flask import make_response
    from agri_irrigation_view import render_agri_irrigation_html
    resp = make_response(render_agri_irrigation_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Awards, Sports & Personalities 2025-2026 Endpoints -----------------
@app.route("/api/awards_sports", methods=["GET"])
def api_awards_sports():
    from awards_sports_data import AWARDS_SPORTS_DATA
    return jsonify({
        "success": True,
        "data": AWARDS_SPORTS_DATA
    })

@app.route("/awards_sports_hub", methods=["GET"])
def awards_sports_hub_view():
    from flask import make_response
    from awards_sports_view import render_awards_sports_html
    resp = make_response(render_awards_sports_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- APPSC Group-1 Prelims 240M Simulator Endpoints -----------------
@app.route("/api/group1_prelims", methods=["GET"])
def api_group1_prelims():
    from group1_prelims_data import GROUP1_SYLLABUS, GROUP1_REVISION_NOTES, GROUP1_QUESTIONS
    return jsonify({
        "success": True,
        "syllabus": GROUP1_SYLLABUS,
        "notes": GROUP1_REVISION_NOTES,
        "questions": GROUP1_QUESTIONS
    })

@app.route("/group1_prelims_master", methods=["GET"])
def group1_prelims_master_view():
    from flask import make_response
    from group1_prelims_view import render_group1_prelims_html
    resp = make_response(render_group1_prelims_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- AP & TS Tribal Heritage & PESA Hub Endpoints -----------------
@app.route("/api/tribal_heritage", methods=["GET"])
def api_tribal_heritage():
    from tribal_heritage_data import TRIBAL_HERITAGE_DATA
    return jsonify({
        "success": True,
        "data": TRIBAL_HERITAGE_DATA
    })

@app.route("/tribal_heritage_hub", methods=["GET"])
def tribal_heritage_hub_view():
    from flask import make_response
    from tribal_heritage_view import render_tribal_heritage_html
    resp = make_response(render_tribal_heritage_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Educational PDF Uploader & Auto-Sync Endpoints -----------------
@app.route("/api/upload_pdf", methods=["POST"])
def api_upload_pdf():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "దయచేసి PDF ఫైల్‌ను అప్‌లోడ్ చేయండి."}), 400
    file = request.files["file"]
    if not file or not file.filename or not file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "కేవలం .pdf ఫార్మాట్ ఫైల్స్ మాత్రమే అనుమతించబడతాయి."}), 400

    # Students and teachers can upload study PDFs freely without admin pin
    title = request.form.get("title", "").strip()
    category = request.form.get("category", "education").strip()
    # Default to 0 so uploads do not pollute daily current affairs feed
    sync_articles = request.form.get("sync_articles", "0") == "1"
    sync_quizzes = request.form.get("sync_quizzes", "0") == "1"

    try:
        from pdf_extractor import process_uploaded_pdf
        res = process_uploaded_pdf(
            file_input=file,
            custom_title=title,
            category=category,
            sync_to_website=sync_articles,
            extract_quizzes=sync_quizzes
        )
        return jsonify({"success": True, "message": "PDF విజయవంతంగా డిజిటల్ లైబ్రరీలో భద్రపరచబడింది!", "data": res})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/uploaded_materials", methods=["GET"])
@app.route("/api/pdf_materials", methods=["GET"])
def api_uploaded_materials():
    from db import get_uploaded_materials
    category = request.args.get("category")
    materials = get_uploaded_materials(category=category)
    return jsonify({"success": True, "materials": materials})

@app.route("/api/uploaded_materials/<int:mid>", methods=["DELETE", "POST"])
def api_delete_uploaded_material(mid):
    pin = request.args.get("pin", "").strip() or request.form.get("pin", "").strip()
    if pin != "lakshya2026":
        return jsonify({"success": False, "error": "PDF ని తొలగించడానికి కేవలం అడ్మిన్ కు మాత్రమే అనుమతి ఉంది. సరైన పిన్ అవసరం."}), 403
    from db import delete_uploaded_material
    delete_uploaded_material(mid)
    return jsonify({"success": True, "message": "స్టడీ మెటీరియల్ విజయవంతంగా తొలగించబడింది."})

@app.route("/api/uploaded_materials/purge_all", methods=["DELETE", "POST"])
def api_purge_all_materials():
    pin = request.args.get("pin", "").strip() or request.form.get("pin", "").strip()
    if pin != "lakshya2026":
        return jsonify({"success": False, "error": "అన్ని PDF లను తొలగించడానికి కేవలం అడ్మిన్ కు మాత్రమే అనుమతి ఉంది. సరైన పిన్ అవసరం."}), 403
    from db import purge_all_uploaded_materials
    count = purge_all_uploaded_materials()
    return jsonify({"success": True, "message": f"మొత్తం {count} అప్‌లోడ్ చేసిన స్టడీ PDF లు మరియు ఫైళ్లు విజయవంతంగా తొలగించబడ్డాయి."})

@app.route("/pdf_upload_hub", methods=["GET"])
def pdf_upload_hub_view():
    from flask import make_response
    from pdf_upload_view import render_pdf_upload_html
    resp = make_response(render_pdf_upload_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

@app.route("/pdfs/uploads/<path:filename>", methods=["GET"])
def serve_uploaded_pdf(filename):
    uploads_dir = os.path.join(FRONTEND_DIR, "pdfs", "uploads")
    return send_from_directory(uploads_dir, filename, mimetype="application/pdf")


# ----------------- 1-Click OMR Mock Test & Question Paper Generator -----------------
@app.route("/api/omr_test_print", methods=["GET"])
def api_omr_test_print():
    from flask import make_response
    from omr_generator import generate_omr_test_html
    mat_id = request.args.get("material_id")
    resp = make_response(generate_omr_test_html(material_id=mat_id))
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

# ----------------- Telegram Channels & Groups Broadcaster Endpoints -----------------
@app.route("/telegram_channels_hub", methods=["GET"])
def telegram_channels_hub_view():
    from flask import make_response
    from telegram_channels_view import render_telegram_channels_html
    resp = make_response(render_telegram_channels_html())
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, max-age=0"
    return resp

@app.route("/api/telegram/channels", methods=["GET"])
def api_telegram_channels_list():
    from telegram_bot import load_channels
    return jsonify({"success": True, "channels": load_channels()})

@app.route("/api/telegram/channels/add", methods=["POST"])
def api_telegram_channels_add():
    data = request.get_json() or {}
    cid = data.get("channel_id", "").strip()
    title = data.get("title", "").strip()
    if not cid:
        return jsonify({"success": False, "error": "దయచేసి ఛానల్ ID లేదా యూజర్‌నేమ్ నమోదు చేయండి."}), 400
    from telegram_bot import add_channel
    channels = add_channel(channel_id=cid, title=title)
    return jsonify({"success": True, "channels": channels})

@app.route("/api/telegram/channels/remove", methods=["POST"])
def api_telegram_channels_remove():
    data = request.get_json() or {}
    cid = data.get("channel_id", "").strip()
    if not cid:
        return jsonify({"success": False, "error": "ఛానల్ ID అవసరం."}), 400
    from telegram_bot import remove_channel
    channels = remove_channel(channel_id=cid)
    return jsonify({"success": True, "channels": channels})

@app.route("/api/telegram/channels/test", methods=["POST"])
def api_telegram_channels_test():
    data = request.get_json() or {}
    cid = data.get("channel_id", "").strip()
    if not cid:
        return jsonify({"success": False, "error": "ఛానల్ ID అవసరం."}), 400
    from telegram_bot import send_telegram_message, load_config
    cfg = load_config()
    token = cfg.get("bot_token")
    test_msg = (
        f"🔔 <b>లక్ష్య తెలుగు కరెంట్ అఫైర్స్ - కనెక్టివిటీ టెస్ట్</b>\n"
        f"ఈ ఛానల్ (@venkat_telugu_ca_bot) కి విజయవంతంగా అనుసంధానించబడింది! 🎉\n"
        f"ప్రతిరోజూ ఉదయం 7:00 గంటలకు ఇక్కడ పూర్తి ఈ-పేపర్ PDF, ముఖ్యాంశాలు మరియు క్విజ్ పోల్స్ పోస్ట్ చేయబడతాయి."
    )
    res = send_telegram_message(test_msg, token=token, chat_id=cid)
    return jsonify(res)

@app.route("/api/telegram/channels/broadcast_now", methods=["POST"])
def api_telegram_channels_broadcast_now():
    from telegram_bot import broadcast_daily_digest
    res = broadcast_daily_digest()
    return jsonify(res)

if __name__ == "__main__":
    print("==================================================================")
    print("🚀 తెలుగు పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్ డ్యాష్‌బోర్డ్ ప్రారంభమైంది!")
    print("🌐 బ్రౌజర్‌లో ఓపెన్ చేయండి: http://localhost:5000")
    print("==================================================================")
    app.run(host="0.0.0.0", port=5000, debug=True)
