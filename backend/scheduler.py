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
from datetime import datetime
from scraper import sync_daily_news
from telegram_bot import broadcast_daily_digest, load_config as load_tg_config

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
    cfg["updated_at"] = datetime.now().isoformat()
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    return cfg

def run_daily_job():
    """
    Executes the morning job:
    1. Syncs news for today
    2. Broadcasts to Telegram if enabled
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    print(f"⏰ [{datetime.now().strftime('%H:%M:%S')}] డైలీ మార్నింగ్ షెడ్యూలర్ రన్ అవుతోంది... ({today_str})")
    
    cfg = load_scheduler_config()
    results = {}
    
    # Step 1: Sync News
    try:
        sync_res = sync_daily_news(target_date=today_str)
        results["sync"] = sync_res
        print(f"✅ వార్తల సేకరణ పూర్తయింది: {sync_res.get('articles_added', 0)} వార్తలు జోడించబడ్డాయి.")
    except Exception as e:
        results["sync_error"] = str(e)
        print(f"❌ వార్తల సేకరణలో లోపం: {e}")

    # Step 2: Send to Telegram
    if cfg.get("auto_telegram"):
        tg_cfg = load_tg_config()
        if tg_cfg.get("bot_token") and tg_cfg.get("chat_id"):
            try:
                tg_res = broadcast_daily_digest(date=today_str)
                results["telegram"] = tg_res
                print(f"✅ టెలిగ్రామ్ బ్రాడ్‌కాస్ట్ పూర్తయింది: {tg_res.get('quizzes_sent', 0)} క్విజ్ పోల్స్ పంపబడ్డాయి.")
            except Exception as e:
                results["telegram_error"] = str(e)
                print(f"❌ టెలిగ్రామ్ బ్రాడ్‌కాస్ట్‌లో లోపం: {e}")
        else:
            results["telegram_status"] = "Telegram not configured"

    # Update config
    cfg["last_run_date"] = today_str
    cfg["last_run_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cfg["last_status"] = "Success"
    with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)

    return results

def scheduler_worker():
    """Background daemon loop checking time every 30 seconds"""
    print("⏰ ఆటోమేటిక్ మార్నింగ్ షెడ్యూలర్ బ్యాక్‌గ్రౌండ్ థ్రెడ్ ప్రారంభమైంది.")
    while True:
        try:
            cfg = load_scheduler_config()
            if cfg.get("enabled"):
                target_time = cfg.get("scheduled_time", "07:00")
                now = datetime.now()
                current_hm = now.strftime("%H:%M")
                today_str = now.strftime("%Y-%m-%d")

                # If current time is at or past target time and hasn't run today yet
                if current_hm >= target_time and cfg.get("last_run_date") != today_str:
                    run_daily_job()

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
