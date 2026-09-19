# -*- coding: utf-8 -*-
"""
Automatic Dual-Slot Daily Scheduler for Telugu Current Affairs (IST Timezone).
Slot 1: Morning 07:00 AM IST (News Sync, E-Paper PDF, Capsule PDF & Digest Broadcast)
Slot 2: Evening 07:00 PM IST (Interactive Quiz Polls & Daily Live CBT Mock Test Broadcast)
"""

import os
import json
import time
import threading
from datetime import datetime, timezone, timedelta
from scraper import sync_daily_news
from telegram_bot import broadcast_daily_digest, broadcast_evening_quiz_polls, load_config as load_tg_config

# India Standard Time (IST is UTC + 5:30)
IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    """Returns current datetime in Indian Standard Time (IST)"""
    return datetime.now(IST)

def get_ist_today():
    """Returns current date in YYYY-MM-DD in Indian Standard Time (IST)"""
    return datetime.now(IST).strftime("%Y-%m-%d")

SCHEDULER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "scheduler_config.json")

def load_scheduler_config():
    cfg = {
        "enabled": True,
        "morning_time": "07:00",
        "evening_time": "19:00",
        "scheduled_time": "07:00",
        "auto_telegram": True,
        "last_morning_run_date": None,
        "last_evening_run_date": None,
        "last_run_date": None,
        "last_status": "Idle"
    }
    if os.path.exists(SCHEDULER_CONFIG_PATH):
        try:
            with open(SCHEDULER_CONFIG_PATH, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                cfg.update(loaded)
                # Backward compatibility
                if "scheduled_time" in loaded and "morning_time" not in loaded:
                    cfg["morning_time"] = loaded["scheduled_time"]
                return cfg
        except Exception:
            pass
    return cfg

def save_scheduler_config(enabled=True, morning_time="07:00", evening_time="19:00", scheduled_time=None, auto_telegram=True):
    cfg = load_scheduler_config()
    cfg["enabled"] = bool(enabled)
    cfg["morning_time"] = str(morning_time or scheduled_time or "07:00").strip()
    cfg["scheduled_time"] = cfg["morning_time"]
    cfg["evening_time"] = str(evening_time or "19:00").strip()
    cfg["auto_telegram"] = bool(auto_telegram)
    cfg["updated_at"] = get_ist_now().isoformat()
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return cfg

def run_morning_job(date=None):
    """
    Slot 1: Morning Job (07:00 AM IST)
    1. Syncs news for today in IST
    2. Ensures 5 exam MCQs are ready
    3. Generates Today's E-Paper PDF & Daily CA Capsule PDF
    4. Broadcasts Morning Digest & PDFs to Telegram
    """
    target_date = date or get_ist_today()
    now_ist = get_ist_now()
    print(f"⏰ [{now_ist.strftime('%H:%M:%S')} IST] 🌅 డైలీ మార్నింగ్ షెడ్యూలర్ రన్ అవుతోంది... ({target_date})")
    
    cfg = load_scheduler_config()
    results = {"slot": "morning", "date": target_date}
    
    # 1. Sync News
    try:
        sync_res = sync_daily_news(target_date=target_date)
        results["sync"] = sync_res
        print(f"✅ వార్తల సేకరణ పూర్తయింది: {sync_res.get('articles_added', 0)} వార్తలు జోడించబడ్డాయి.")
    except Exception as e:
        results["sync_error"] = str(e)
        print(f"❌ వార్తల సేకరణలో లోపం: {e}")

    # 2. Ensure 5 MCQs
    try:
        from quiz_generator import ensure_daily_quizzes
        quizzes = ensure_daily_quizzes(target_date)
        results["quizzes_count"] = len(quizzes)
        print(f"✅ 5 పరీక్షా క్విజ్ ప్రశ్నలు సిద్ధం చేయబడ్డాయి: {len(quizzes)} ప్రశ్నలు.")
    except Exception as e:
        results["quiz_error"] = str(e)
        print(f"❌ క్విజ్ తయారీలో లోపం: {e}")

    # 3. Generate Today's Fresh E-Paper PDF
    try:
        from pdf_generator import generate_epaper_pdf
        pdf_path = generate_epaper_pdf(target_date, force_refresh=True)
        results["pdf"] = pdf_path
        print(f"✅ నేటి ({target_date}) ఈ-పేపర్ PDF సిద్ధమైంది: {pdf_path}")
    except Exception as e:
        results["pdf_error"] = str(e)
        print(f"❌ PDF తయారీలో లోపం: {e}")

    # 4. Generate Today's Fresh Daily CA & Quiz Capsule PDF
    try:
        from daily_ca_quiz_pdf import generate_ca_quiz_pdf
        ca_quiz_pdf_path = generate_ca_quiz_pdf(target_date, force_refresh=True)
        results["ca_quiz_pdf"] = ca_quiz_pdf_path
        print(f"✅ నేటి ({target_date}) డైలీ CA & క్విజ్ క్యాప్సూల్ PDF సిద్ధమైంది: {ca_quiz_pdf_path}")
    except Exception as e:
        results["ca_quiz_pdf_error"] = str(e)
        print(f"❌ డైలీ CA & క్విజ్ PDF తయారీలో లోపం: {e}")

    # 5. Send to Telegram (Morning Digest)
    if cfg.get("auto_telegram", True):
        tg_cfg = load_tg_config()
        if tg_cfg.get("bot_token") and tg_cfg.get("chat_id"):
            try:
                tg_res = broadcast_daily_digest(date=target_date)
                results["telegram"] = tg_res
                print(f"✅ మార్నింగ్ టెలిగ్రామ్ బ్రాడ్‌కాస్ట్ పూర్తయింది.")
            except Exception as e:
                results["telegram_error"] = str(e)
                print(f"❌ టెలిగ్రామ్ బ్రాడ్‌కాస్ట్‌లో లోపం: {e}")
        else:
            results["telegram_status"] = "Telegram not configured"

    # Update config
    cfg["last_morning_run_date"] = target_date
    cfg["last_run_date"] = target_date
    cfg["last_morning_run_time"] = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    cfg["last_status"] = "Morning Run Success"
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    return results

def run_evening_job(date=None):
    """
    Slot 2: Evening Job (07:00 PM / 19:00 IST)
    1. Broadcasts Interactive Quiz Polls
    2. Sends Daily Live CBT Mock Test link & Schemes Handbook link
    """
    target_date = date or get_ist_today()
    now_ist = get_ist_now()
    print(f"⏰ [{now_ist.strftime('%H:%M:%S')} IST] 🌙 డైలీ ఈవెనింగ్ షెడ్యూలర్ రన్ అవుతోంది... ({target_date})")
    
    cfg = load_scheduler_config()
    results = {"slot": "evening", "date": target_date}

    if cfg.get("auto_telegram", True):
        tg_cfg = load_tg_config()
        if tg_cfg.get("bot_token") and tg_cfg.get("chat_id"):
            try:
                tg_res = broadcast_evening_quiz_polls(date=target_date)
                results["telegram"] = tg_res
                print(f"✅ ఈవెనింగ్ క్విజ్ పోల్స్ బ్రాడ్‌కాస్ట్ పూర్తయింది: {tg_res.get('quizzes_sent', 0)} పోల్స్ పంపబడ్డాయి.")
            except Exception as e:
                results["telegram_error"] = str(e)
                print(f"❌ ఈవెనింగ్ బ్రాడ్‌కాస్ట్‌లో లోపం: {e}")
        else:
            results["telegram_status"] = "Telegram not configured"

    cfg["last_evening_run_date"] = target_date
    cfg["last_evening_run_time"] = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    cfg["last_status"] = "Evening Run Success"
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    return results

def run_daily_job(date=None):
    """Executes morning cycle (backward compatible)"""
    return run_morning_job(date=date)

def scheduler_worker():
    """Background daemon loop checking IST time every 30 seconds for Dual Slots"""
    print("⏰ ఆటోమేటిక్ డ్యూయల్-స్లాట్ షెడ్యూలర్ ప్రారంభమైంది (Morning 07:00 AM & Evening 07:00 PM IST).")
    
    time.sleep(5)
    try:
        cfg = load_scheduler_config()
        now_ist = get_ist_now()
        morning_target = cfg.get("morning_time", "07:00")
        current_hm = now_ist.strftime("%H:%M")
        today_str = now_ist.strftime("%Y-%m-%d")
        
        if cfg.get("enabled", True):
            if current_hm >= morning_target and cfg.get("last_morning_run_date") != today_str:
                print(f"🚀 [Startup Catch-up] నేటి ({today_str}) మార్నింగ్ జాబ్ వెంటనే రన్ చేస్తున్నాం...")
                run_morning_job(today_str)
    except Exception as e:
        print(f"Startup catch-up error: {e}")

    while True:
        try:
            cfg = load_scheduler_config()
            if cfg.get("enabled", True):
                morning_time = cfg.get("morning_time", "07:00")
                evening_time = cfg.get("evening_time", "19:00")
                now_ist = get_ist_now()
                current_hm = now_ist.strftime("%H:%M")
                today_str = now_ist.strftime("%Y-%m-%d")

                # Morning slot check
                if current_hm >= morning_time and current_hm < evening_time:
                    if cfg.get("last_morning_run_date") != today_str:
                        run_morning_job(today_str)

                # Evening slot check
                if current_hm >= evening_time:
                    if cfg.get("last_evening_run_date") != today_str:
                        run_evening_job(today_str)

            time.sleep(30)
        except Exception as e:
            print(f"Scheduler worker error: {e}")
            time.sleep(30)

def start_scheduler_thread():
    t = threading.Thread(target=scheduler_worker, daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    print("టెస్టింగ్ మార్నింగ్ & ఈవెనింగ్ జాబ్స్...")
    res_m = run_morning_job()
    print("మార్నింగ్ రన్ ఫలితం:", res_m)
    res_e = run_evening_job()
    print("ఈవెనింగ్ రన్ ఫలితం:", res_e)
