# -*- coding: utf-8 -*-
"""
Automatic Daily Morning Scheduler for Telugu Current Affairs.
Runs daily at the configured time (e.g. 07:00 AM),
fetches latest news, creates MCQs, and broadcasts to Telegram.
"""

import os
import json
import time
import threading
from datetime import datetime, timezone, timedelta
from scraper import sync_daily_news
from telegram_bot import broadcast_daily_digest, load_config as load_tg_config

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
    if os.path.exists(SCHEDULER_CONFIG_PATH):
        try:
            with open(SCHEDULER_CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "enabled": True,
        "scheduled_time": "07:00",
        "auto_telegram": True,
        "last_run_date": None,
        "last_status": "Idle"
    }

def save_scheduler_config(enabled=True, scheduled_time="07:00", auto_telegram=True):
    cfg = load_scheduler_config()
    cfg["enabled"] = bool(enabled)
    cfg["scheduled_time"] = str(scheduled_time).strip()
    cfg["auto_telegram"] = bool(auto_telegram)
    cfg["updated_at"] = get_ist_now().isoformat()
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return cfg

def run_daily_job(date=None):
    """
    Executes the morning job:
    1. Syncs news for today (or specified date) in IST
    2. Ensures 5 exam MCQs are ready
    3. Broadcasts to Telegram if enabled
    """
    target_date = date or get_ist_today()
    now_ist = get_ist_now()
    print(f"⏰ [{now_ist.strftime('%H:%M:%S')} IST] డైలీ మార్నింగ్ షెడ్యూలర్ రన్ అవుతోంది... ({target_date})")
    
    cfg = load_scheduler_config()
    results = {}
    
    # Step 1: Sync News
    try:
        sync_res = sync_daily_news(target_date=target_date)
        results["sync"] = sync_res
        print(f"✅ వార్తల సేకరణ పూర్తయింది: {sync_res.get('articles_added', 0)} వార్తలు జోడించబడ్డాయి.")
    except Exception as e:
        results["sync_error"] = str(e)
        print(f"❌ వార్తల సేకరణలో లోపం: {e}")

    # Step 2: Ensure 5 MCQs
    try:
        from quiz_generator import ensure_daily_quizzes
        quizzes = ensure_daily_quizzes(target_date)
        results["quizzes_count"] = len(quizzes)
        print(f"✅ 5 పరీక్షా క్విజ్ ప్రశ్నలు సిద్ధం చేయబడ్డాయి: {len(quizzes)} ప్రశ్నలు.")
    except Exception as e:
        results["quiz_error"] = str(e)
        print(f"❌ క్విజ్ తయారీలో లోపం: {e}")

    # Step 3: Send to Telegram
    if cfg.get("auto_telegram", True):
        tg_cfg = load_tg_config()
        if tg_cfg.get("bot_token") and tg_cfg.get("chat_id"):
            try:
                tg_res = broadcast_daily_digest(date=target_date)
                results["telegram"] = tg_res
                print(f"✅ టెలిగ్రామ్ బ్రాడ్‌కాస్ట్ పూర్తయింది: {tg_res.get('quizzes_sent', 0)} క్విజ్ పోల్స్ పంపబడ్డాయి.")
            except Exception as e:
                results["telegram_error"] = str(e)
                print(f"❌ టెలిగ్రామ్ బ్రాడ్‌కాస్ట్‌లో లోపం: {e}")
        else:
            results["telegram_status"] = "Telegram not configured"

    # Update config
    cfg["last_run_date"] = target_date
    cfg["last_run_time"] = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
    cfg["last_status"] = "Success"
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    return results

def scheduler_worker():
    """Background daemon loop checking IST time every 30 seconds"""
    print("⏰ ఆటోమేటిక్ మార్నింగ్ షెడ్యూలర్ బ్యాక్‌గ్రౌండ్ థ్రెడ్ ప్రారంభమైంది (IST Timezone).")
    
    # Startup catch-up: if server boots and it's already past scheduled_time, or news not synced yet today
    time.sleep(5)  # Wait 5 seconds for DB and Flask app to stabilize
    try:
        cfg = load_scheduler_config()
        now_ist = get_ist_now()
        target_time = cfg.get("scheduled_time", "07:00")
        current_hm = now_ist.strftime("%H:%M")
        today_str = now_ist.strftime("%Y-%m-%d")
        
        if cfg.get("enabled", True):
            if current_hm >= target_time and cfg.get("last_run_date") != today_str:
                print(f"🚀 [Startup Catch-up] నేటి ({today_str}) మార్నింగ్ జాబ్ ఇంకా రన్ కాలేదు. వెంటనే రన్ చేస్తున్నాం...")
                run_daily_job(today_str)
    except Exception as e:
        print(f"Startup catch-up error: {e}")

    while True:
        try:
            cfg = load_scheduler_config()
            if cfg.get("enabled", True):
                target_time = cfg.get("scheduled_time", "07:00")
                now_ist = get_ist_now()
                current_hm = now_ist.strftime("%H:%M")
                today_str = now_ist.strftime("%Y-%m-%d")

                # If current IST time is at or past target time and hasn't run today yet
                if current_hm >= target_time and cfg.get("last_run_date") != today_str:
                    run_daily_job(today_str)

            time.sleep(30)
        except Exception as e:
            print(f"Scheduler worker error: {e}")
            time.sleep(30)

def start_scheduler_thread():
    t = threading.Thread(target=scheduler_worker, daemon=True)
    t.start()
    return t

if __name__ == "__main__":
    print("టెస్టింగ్ డైలీ జాబ్...")
    res = run_daily_job()
    print("ఫలితం:", res)
