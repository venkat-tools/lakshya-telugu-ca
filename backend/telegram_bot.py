# -*- coding: utf-8 -*-
"""
Telegram Bot Integration for Daily Telugu Current Affairs & E-Papers.
Supports:
1. Daily Highlights & One-Liners notification (with safe HTML escaping)
2. Interactive Quiz Polls (Single/Multiple choice)
3. Full Daily E-Paper PDF Magazine dispatch (sendDocument)
4. Official Telugu E-Papers (Eenadu, Sakshi, Andhra Jyothy, NT News) directory
"""

import requests
import json
import os
import html
from datetime import datetime, timezone, timedelta
from db import get_articles, get_quiz_by_date, get_one_liners_by_date, get_available_dates

IST = timezone(timedelta(hours=5, minutes=30))

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "telegram_config.json")
DEFAULT_BOT_TOKEN = "8858325846:AAFiO2N3ymKzPIe1lFC8doEru3WPmIjx9UM"
DEFAULT_CHAT_ID = "5405953028"

def load_config():
    bot_token = ""
    chat_id = ""
    enabled = True
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                bot_token = cfg.get("bot_token", "").strip()
                chat_id = str(cfg.get("chat_id", "")).strip()
                enabled = cfg.get("enabled", True)
        except Exception:
            pass

    if not bot_token:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not chat_id:
        chat_id = os.environ.get("TELEGRAM_CHAT_ID", "").strip()

    if not bot_token:
        bot_token = DEFAULT_BOT_TOKEN
    if not chat_id:
        chat_id = DEFAULT_CHAT_ID

    return {
        "bot_token": bot_token,
        "chat_id": chat_id,
        "enabled": enabled
    }

SUBSCRIBERS_PATH = os.path.join(os.path.dirname(__file__), "subscribers.json")
CHANNELS_PATH = os.path.join(os.path.dirname(__file__), "channels.json")

def load_subscribers():
    subscribers = set()
    cfg = load_config()
    if cfg.get("chat_id"):
        subscribers.add(str(cfg["chat_id"]))
    if os.path.exists(SUBSCRIBERS_PATH):
        try:
            with open(SUBSCRIBERS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    for s in data:
                        if s:
                            subscribers.add(str(s))
        except Exception:
            pass
    return list(subscribers)

def add_subscriber(chat_id):
    if not chat_id:
        return
    subscribers = set(load_subscribers())
    subscribers.add(str(chat_id))
    try:
        with open(SUBSCRIBERS_PATH, "w", encoding="utf-8") as f:
            json.dump(list(subscribers), f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def load_channels():
    """Load list of registered Telegram broadcast channels and study groups"""
    if os.path.exists(CHANNELS_PATH):
        try:
            with open(CHANNELS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def add_channel(channel_id, title=""):
    """Register a Telegram channel or group for auto-broadcast"""
    if not channel_id:
        return load_channels()
    channels = load_channels()
    cid_str = str(channel_id).strip()
    for ch in channels:
        if ch.get("channel_id") == cid_str:
            if title:
                ch["title"] = title
            break
    else:
        channels.append({"channel_id": cid_str, "title": title or cid_str})
    try:
        with open(CHANNELS_PATH, "w", encoding="utf-8") as f:
            json.dump(channels, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return channels

def remove_channel(channel_id):
    """Remove a channel from auto-broadcast"""
    channels = [ch for ch in load_channels() if ch.get("channel_id") != str(channel_id).strip()]
    try:
        with open(CHANNELS_PATH, "w", encoding="utf-8") as f:
            json.dump(channels, f, ensure_ascii=False, indent=2)
    except Exception:
        pass
    return channels

def save_config(bot_token, chat_id):
    config = {
        "bot_token": bot_token.strip(),
        "chat_id": chat_id.strip()
    }
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    add_subscriber(chat_id.strip())
    return config

def send_telegram_message(text, token=None, chat_id=None):
    """Send text message to Telegram using HTML parse mode"""
    config = load_config()
    token = token or config.get("bot_token")
    chat_id = chat_id or config.get("chat_id")

    if not token or not chat_id:
        return {"success": False, "error": "Bot Token లేదా Chat ID కాన్ఫిగర్ చేయలేదు."}

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    try:
        res = requests.post(url, json=payload, timeout=15)
        data = res.json()
        if data.get("ok"):
            return {"success": True, "result": data}
        return {"success": False, "error": data.get("description", "టెలిగ్రామ్ ఎర్రర్")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_telegram_document(file_path, caption="", filename=None, token=None, chat_id=None):
    """Send document / PDF file to Telegram"""
    config = load_config()
    token = token or config.get("bot_token")
    chat_id = chat_id or config.get("chat_id")

    if not token or not chat_id:
        return {"success": False, "error": "Bot Token లేదా Chat ID కాన్ఫిగర్ చేయలేదు."}

    if not os.path.exists(file_path):
        return {"success": False, "error": f"ఫైల్ కనుగొనబడలేదు: {file_path}"}

    url = f"https://api.telegram.org/bot{token}/sendDocument"
    upload_name = filename or os.path.basename(file_path)

    try:
        with open(file_path, "rb") as f:
            files = {"document": (upload_name, f, "application/pdf")}
            data = {
                "chat_id": chat_id,
                "caption": caption[:1024],
                "parse_mode": "HTML"
            }
            res = requests.post(url, data=data, files=files, timeout=60)
            res_data = res.json()
            if res_data.get("ok"):
                return {"success": True, "result": res_data}
            return {"success": False, "error": res_data.get("description", "టెలిగ్రామ్ డాక్యుమెంట్ ఎర్రర్")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def send_telegram_audio(audio_path, caption="", title="డైలీ కరెంట్ అఫైర్స్ ఆడియో బులెటిన్", performer="లక్ష్య స్టడీ టీమ్", token=None, chat_id=None):
    """Send native audio/podcast file to Telegram (sendAudio)"""
    config = load_config()
    token = token or config.get("bot_token")
    chat_id = chat_id or config.get("chat_id")

    if not token or not chat_id:
        return {"success": False, "error": "Bot Token లేదా Chat ID కాన్ఫిగర్ చేయలేదు."}

    if not os.path.exists(audio_path):
        return {"success": False, "error": f"ఆడియో ఫైల్ కనుగొనబడలేదు: {audio_path}"}

    url = f"https://api.telegram.org/bot{token}/sendAudio"
    upload_name = os.path.basename(audio_path)

    try:
        with open(audio_path, "rb") as f:
            files = {"audio": (upload_name, f, "audio/mpeg")}
            data = {
                "chat_id": chat_id,
                "caption": caption[:1024],
                "parse_mode": "HTML",
                "title": title,
                "performer": performer
            }
            res = requests.post(url, data=data, files=files, timeout=60)
            res_data = res.json()
            if res_data.get("ok"):
                return {"success": True, "result": res_data}
            return {"success": False, "error": res_data.get("description", "టెలిగ్రామ్ ఆడియో ఎర్రర్")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_daily_bulletin_audio(date=None, token=None, chat_id=None):
    """Generate and send today's Telugu Exam Audio Podcast Bulletin to Telegram"""
    from tts import generate_daily_bulletin_audio
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

    audio_path = generate_daily_bulletin_audio(date=date)
    if not audio_path or not os.path.exists(audio_path):
        return {"success": False, "error": "ఆడియో బులెటిన్ జనరేట్ చేయడం సాధ్యపడలేదు."}

    caption = (
        f"🎙️ <b>లక్ష్య డైలీ కరెంట్ అఫైర్స్ ఆడియో పాడ్‌కాస్ట్ బులెటిన్</b>\n"
        f"📅 <b>తేదీ: {date}</b>\n"
        f"───────────────────────\n"
        f"🎧 5 నిమిషాల సమగ్ర ముఖ్యాంశాలు, వన్‌లైనర్స్ & పరీక్ష విశ్లేషణ.\n"
        f"🚗 ప్రయాణాల్లో, పనుల్లో ఉన్నప్పుడు వినడానికి అత్యంత అనుకూలం!\n\n"
        f"📥 పూర్తి PDF: https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}"
    )

    return send_telegram_audio(
        audio_path=audio_path,
        caption=caption,
        title=f"లక్ష్య కరెంట్ అఫైర్స్ బులెటిన్ ({date})",
        performer="లక్ష్య స్టడీ అకాడమీ",
        token=token,
        chat_id=chat_id
    )

def send_telegram_quiz_poll(question, options, correct_index, explanation="", token=None, chat_id=None):
    """Send native Telegram Quiz Poll"""
    config = load_config()
    token = token or config.get("bot_token")
    chat_id = chat_id or config.get("chat_id")

    if not token or not chat_id:
        return {"success": False, "error": "Bot Token లేదా Chat ID కాన్ఫిగర్ చేయలేదు."}

    url = f"https://api.telegram.org/bot{token}/sendPoll"
    payload = {
        "chat_id": chat_id,
        "question": question[:300],
        "options": json.dumps(options[:10]),
        "correct_option_id": int(correct_index),
        "type": "quiz",
        "explanation": explanation[:200] if explanation else "సరైన సమాధానం",
        "is_anonymous": False
    }
    try:
        res = requests.post(url, json=payload, timeout=10)
        data = res.json()
        if data.get("ok"):
            return {"success": True, "result": data}
        return {"success": False, "error": data.get("description", "టెలిగ్రామ్ పోల్ ఎర్రర్")}
    except Exception as e:
        return {"success": False, "error": str(e)}

def send_daily_epaper_pdf(date=None, token=None, chat_id=None):
    """Generate and send today's Telugu E-Paper PDF to Telegram"""
    from pdf_generator import generate_epaper_pdf
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

    caption = (
        f"🎯 <b>లక్ష్య డైలీ తెలుగు ఈ-పేపర్ (100% పోటీ పరీక్షల ప్రత్యేక ఎడిషన్)</b>\n"
        f"📅 <b>తేదీ: {date}</b>\n"
        f"───────────────────────\n\n"
        f"📌 <b>హై-యీల్డ్ ఎగ్జామ్ కంటెంట్ (Zero Fillers):</b>\n"
        f"• 🏛️ జాతీయ అంశాలు: కొవింద్ కమిటీ జమిలి ఎన్నికల సిఫార్సులు (ఆర్టికల్ 83, 172), ఎన్నికల సంఘం నియామకాలు\n"
        f"• 🌾 AP & TS: ఎన్టీఆర్ భరోసా ₹4,000 పెంపు, పోలవరం-అమరావతి నిధులు, తెలంగాణ 6 గ్యారెంటీలు, కుల గణన 2026\n"
        f"• 📈 ఆర్థికం: ఆర్బీఐ యూపీఐ నిబంధనలు, ఎన్‌ఎస్‌ఈ ఫెర్వానీ కమిటీ ఐపీఓ, CPI ద్రవ్యోల్బణం (3.65%)\n"
        f"• 🚀 సైన్స్ & స్పేస్: ఇస్రో చంద్రయాన్-4 శాంపిల్ రిటర్న్, ఆర్మీ మ్యూల్ రోబోటిక్స్\n"
        f"• ⚡ 12 ఒక వరుస రివిజన్ ముఖ్యాంశాలు (Quick Revision)\n"
        f"• 📝 5 స్టాండర్డ్ ప్రాక్టీస్ MCQs (సమగ్ర తెలుగు వివరణలతో)\n\n"
        f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}\n"
        f"🌐 <b>ఆన్‌లైన్ డిజిటల్ ఈ-పేపర్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/epaper?date={date}\n\n"
        f"🏆 <i>APPSC • TSPSC • UPSC • SSC • బ్యాంకింగ్ అభ్యర్థుల ప్రత్యేకం</i>"
    )

    pdf_path = generate_epaper_pdf(date=date)
    if not pdf_path or not os.path.exists(pdf_path):
        fallback_msg = (
            f"📰 <b>లక్ష్య డైలీ తెలుగు ఈ-పేపర్ ఎడిషన్ (PDF) - {date}</b>\n\n"
            f"📥 <b>నేటి PDF డౌన్‌లోడ్ లింక్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}\n\n"
            f"📖 <b>ఆన్‌లైన్ రీడర్ (HD పేపర్ మోడ్):</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/epaper?date={date}\n\n"
            f"🗞️ <b>ఈనాడు, సాక్షి అధికారిక ఈ-పేపర్స్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/epapers_directory"
        )
        return send_telegram_message(fallback_msg, token=token, chat_id=chat_id)

    res = send_telegram_document(
        file_path=pdf_path,
        caption=caption,
        filename=f"Lakshya_Telugu_EPaper_{date}.pdf",
        token=token,
        chat_id=chat_id
    )

    if not res.get("success"):
        # Send fallback with clickable direct download link if document sending encounters an issue
        fallback_msg = (
            f"📰 <b>లక్ష్య డైలీ తెలుగు ఈ-పేపర్ ఎడిషన్ (PDF) - {date}</b>\n\n"
            f"📥 <b>నేటి PDF డౌన్‌లోడ్ లింక్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}\n\n"
            f"📖 <b>ఆన్‌లైన్ రీడర్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/epaper?date={date}"
        )
        send_telegram_message(fallback_msg, token=token, chat_id=chat_id)

    return res

def send_daily_ca_quiz_pdf(date=None, token=None, chat_id=None):
    """Generate and send today's Dedicated Daily CA & Practice Quiz Capsule PDF to Telegram"""
    from daily_ca_quiz_pdf import generate_ca_quiz_pdf
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

    caption = (
        f"📚 <b>లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రాక్టీస్ క్విజ్ క్యాప్సూల్</b>\n"
        f"📅 <b>తేదీ: {date}</b>\n"
        f"───────────────────────\n\n"
        f"🎯 <b>పోటీ పరీక్షల హ్యాండ్‌బుక్ స్టడీ మెటీరియల్ ఫార్మాట్ (Zero Ads, Single Column):</b>\n"
        f"1️⃣ <b>సబ్జెక్ట్ వైజ్ స్టడీ నోట్స్:</b> కీ ఎగ్జామ్ పాయింటర్లు & సిలబస్ విశ్లేషణ\n"
        f"2️⃣ <b>స్పీడ్ రివిజన్ వన్-లైనర్స్:</b> చివరి నిమిషం ప్రిపరేషన్ బుల్లెట్లు\n"
        f"3️⃣ <b>డైలీ ప్రాక్టీస్ క్విజ్:</b> APPSC/TSPSC నూతన మోడల్ ప్రశ్నలు + OMR సర్కిల్స్\n"
        f"4️⃣ <b>కీ & సమగ్ర వివరణలు:</b> ప్రతి ప్రశ్నకు బ్యాక్‌గ్రౌండ్ & సిలబస్ లింకేజ్\n\n"
        f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/api/ca_quiz/pdf?date={date}\n"
        f"🌐 <b>ఆన్‌లైన్ క్యాప్సూల్ రీడర్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/ca_quiz?date={date}\n\n"
        f"🏆 <i>గ్రూప్-1, గ్రూప్-2, పోలీస్, డీఎస్సీ, బ్యాంకింగ్ అభ్యర్థులకు అత్యుత్తమ రివిజన్ స్టడీ మెటీరియల్</i>"
    )

    pdf_path = generate_ca_quiz_pdf(date=date)
    if not pdf_path or not os.path.exists(pdf_path):
        fallback_msg = (
            f"📚 <b>లక్ష్య డైలీ కరెంట్ అఫైర్స్ & క్విజ్ క్యాప్సూల్ (PDF) - {date}</b>\n\n"
            f"📥 <b>నేటి స్టడీ మెటీరియల్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/api/ca_quiz/pdf?date={date}\n\n"
            f"📖 <b>ఆన్‌లైన్ క్యాప్సూల్ రీడర్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/ca_quiz?date={date}"
        )
        return send_telegram_message(fallback_msg, token=token, chat_id=chat_id)

    res = send_telegram_document(
        file_path=pdf_path,
        caption=caption,
        filename=f"Lakshya_Daily_CA_Quiz_{date}.pdf",
        token=token,
        chat_id=chat_id
    )

    if not res.get("success"):
        fallback_msg = (
            f"📚 <b>లక్ష్య డైలీ కరెంట్ అఫైర్స్ & క్విజ్ క్యాప్సూల్ (PDF) - {date}</b>\n\n"
            f"📥 <b>నేటి స్టడీ మెటీరియల్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/api/ca_quiz/pdf?date={date}\n\n"
            f"📖 <b>ఆన్‌లైన్ క్యాప్సూల్ రీడర్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/ca_quiz?date={date}"
        )
        send_telegram_message(fallback_msg, token=token, chat_id=chat_id)

    return res

def send_epapers_directory(date=None, token=None, chat_id=None):
    """Send official Telugu E-Papers directory links to Telegram"""
    from pdf_generator import OFFICIAL_TELUGU_EPAPERS
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

    msg = (
        f"🗞️ <b>డైలీ తెలుగు ఈ-న్యూస్‌పేపర్స్ & PDF డౌన్‌లోడ్ హబ్</b>\n"
        f"📅 <b>తేదీ: {date}</b>\n"
        f"───────────────────────\n\n"
        f"📥 <b>1. లక్ష్య డైలీ కరెంట్ అఫైర్స్ ఈ-పేపర్ PDF:</b>\n"
        f"• 56+ పోటీ పరీక్షల వార్తలు, ఒక వరుస ముఖ్యాంశాలు & 5 క్విజ్ ప్రశ్నలు\n"
        f"👉 <b>డైరెక్ట్ PDF డౌన్‌లోడ్:</b>\n"
        f"https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}\n"
        f"👉 <b>ఆన్‌లైన్ డిజిటల్ ఈ-పేపర్ రీడర్:</b>\n"
        f"https://lakshya-telugu-ca.onrender.com/epaper?date={date}\n\n"
        f"📰 <b>2. ప్రముఖ దినపత్రికల అధికారిక PDF ఈ-పేపర్స్ (జిల్లాల వారీగా):</b>\n"
    )
    for ep in OFFICIAL_TELUGU_EPAPERS:
        msg += f"• <b>{ep['name']}</b>\n  🔗 {ep['url']}\n  <i>({ep['description']})</i>\n\n"

    msg += (
        f"🌐 <b>వెబ్‌సైట్‌లో అన్ని ఈ-పేపర్స్ డైరెక్టరీ:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/epapers_directory\n\n"
        f"💡 <i>చిట్కా: పూర్తి PDF డాక్యుమెంట్ మీ టెలిగ్రామ్‌లోనే పొందడానికి <b>/epaper</b> లేదా <b>/pdf</b> అని టైప్ చేయండి!</i>"
    )
    return send_telegram_message(msg, token=token, chat_id=chat_id)

def broadcast_daily_digest(date=None, token=None, chat_id=None):
    """
    Format and broadcast full daily current affairs, one-liners,
    interactive quiz polls, AND the complete Daily E-Paper PDF to Telegram.
    """
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")

    from quiz_generator import ensure_daily_quizzes

    articles = get_articles(date=date)
    one_liners = get_one_liners_by_date(date=date)
    quizzes = ensure_daily_quizzes(date)

    if not articles and not one_liners:
        return {"success": False, "error": f"{date} తేదీకి ఎటువంటి సమాచారం అందుబాటులో లేదు."}

    # 1. Format Header & Highlights Message with safe HTML escaping
    msg = f"🎯 <b>పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్ నోటిఫికేషన్</b>\n"
    msg += f"📅 <b>తేదీ: {date}</b>\n"
    msg += f"───────────────────────\n\n"

    cat_icons = {
        "national": "🏛️ [జాతీయం]",
        "regional": "🌾 [AP & TS]",
        "economy": "📈 [ఆర్థికం]",
        "science_tech": "🚀 [సైన్స్ & టెక్]",
        "sports_awards": "🏆 [క్రీడలు & అవార్డులు]",
        "appointments": "👤 [నియామకాలు]"
    }

    msg += "📰 <b>నేటి ప్రధాన ముఖ్యాంశాలు:</b>\n"
    for idx, art in enumerate(articles[:5], 1):
        icon = cat_icons.get(art.get("category"), "🔹")
        s_title = html.escape(art.get("title", ""))
        s_summary = html.escape(art.get("summary", "")[:180])
        msg += f"\n<b>{idx}. {icon} {s_title}</b>\n"
        msg += f"👉 {s_summary}...\n"
        if art.get("exam_relevance"):
            s_er = html.escape(art["exam_relevance"])
            msg += f"<i>🎯 పరీక్ష ప్రాముఖ్యత: {s_er}</i>\n"

    # Quick Revision One-Liners
    if one_liners:
        msg += f"\n\n⚡ <b>ఒక వరుస ముఖ్యాంశాలు (Quick Revision):</b>\n"
        for idx, ol in enumerate(one_liners[:6], 1):
            s_point = html.escape(ol.get("point", ""))
            msg += f"• {s_point}\n"

    # Daily E-Papers & PDF links
    msg += f"\n\n📰 <b>నేటి డైలీ తెలుగు ఈ-పేపర్ PDF & న్యూస్‌పేపర్స్ లింక్స్:</b>\n"
    msg += f"📥 <b>డైలీ కరెంట్ అఫైర్స్ E-Paper PDF డౌన్‌లోడ్:</b>\n👉 https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}\n"
    msg += f"📖 <b>ఆన్‌లైన్ ఈ-పేపర్ రీడర్:</b>\n👉 https://lakshya-telugu-ca.onrender.com/epaper?date={date}\n"
    msg += f"🗞️ <b>ఈనాడు, సాక్షి, ఆంధ్రజ్యోతి అధికారిక E-Papers:</b>\n👉 https://lakshya-telugu-ca.onrender.com/epapers_directory\n"

    msg += f"\n🌐 <b>లైవ్ వెబ్ యాప్ (24/7):</b> https://lakshya-telugu-ca.onrender.com\n"
    msg += f"📱 <b>మొబైల్ యాక్సెస్:</b> https://tinyurl.com/lakshya-telugu-2026"

    if chat_id:
        target_chats = [str(chat_id)]
    else:
        all_targets = set(load_subscribers())
        for ch in load_channels():
            if ch.get("channel_id"):
                all_targets.add(str(ch["channel_id"]))
        cfg = load_config()
        if cfg.get("chat_id"):
            all_targets.add(str(cfg["chat_id"]))
        target_chats = list(all_targets)

    option_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    sent_polls = 0
    pdf_sent_count = 0

    for cid in target_chats:
        # 1. Send Digest Message
        send_res = send_telegram_message(msg, token=token, chat_id=cid)
        if not send_res.get("success"):
            print(f"Failed to send digest message to {cid}:", send_res)

        # 2. Send Native Quiz Polls (Today's fresh 5 questions)
        for q in quizzes[:5]:
            correct_idx = option_map.get(q.get("correct_option", "A").upper(), 0)
            opts = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
            poll_res = send_telegram_quiz_poll(
                question=f"❓ [డైలీ క్విజ్ {date}] {q['question']}"[:255],
                options=[o[:100] for o in opts],
                correct_index=correct_idx,
                explanation=q.get("explanation", "")[:200],
                token=token,
                chat_id=cid
            )
            if poll_res.get("success"):
                sent_polls += 1

        # 3. Send Daily E-Paper PDF Document
        pdf_res = send_daily_epaper_pdf(date=date, token=token, chat_id=cid)
        if pdf_res.get("success"):
            pdf_sent_count += 1

        # 4. Send Dedicated Daily CA & Quiz Capsule PDF Document
        ca_quiz_res = send_daily_ca_quiz_pdf(date=date, token=token, chat_id=cid)
        if ca_quiz_res.get("success"):
            pdf_sent_count += 1

    return {
        "success": True,
        "message": f"{date} నాటి డైజెస్ట్, క్విజ్ పోల్స్, ఈ-పేపర్ మరియు డైలీ CA & క్విజ్ బుక్‌లెట్ PDF {len(target_chats)} మందికి టెలిగ్రామ్‌కు విజయవంతంగా పంపబడ్డాయి!",
        "articles_sent": len(articles),
        "quizzes_sent": sent_polls,
        "pdf_sent": pdf_sent_count > 0,
        "subscribers_count": len(target_chats)
    }


def send_monthly_magazine_telegram(month="2026-09", token=None, chat_id=None):
    """Send pre-compiled Monthly Current Affairs Magazine PDF to Telegram"""
    from magazine import generate_magazine_pdf
    caption = (
        f"📘 <b>లక్ష్య తెలుగు కరెంట్ అఫైర్స్ మాస పత్రిక (Monthly Magazine Special)</b>\n"
        f"📅 <b>ఎడిషన్: {month}</b>\n"
        f"───────────────────────\n\n"
        f"📌 <b>మాస పత్రిక ప్రధాన ముఖ్యాంశాలు (34 పేజీలు):</b>\n"
        f"• 🏛️ 6 ప్రధాన సిలబస్ విభాగాలు (జాతీయం, AP & TS, ఆర్థికం, సైన్స్ & స్పేస్, క్రీడలు, నియామకాలు)\n"
        f"• ⚡ 50 ఒక వరుస క్విక్ రివిజన్ రౌండప్ (50 One-Liners Round-Up)\n"
        f"• 📝 22 స్టాండర్డ్ పరీక్ష ప్రాక్టీస్ ప్రశ్నలు (సమగ్ర వివరణలతో)\n"
        f"• 🏆 100% పోటీ పరీక్షల ప్రమాణాలు (Zero Fillers & Non-Exam Content)\n\n"
        f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/api/magazine/pdf?month={month}\n\n"
        f"📖 <b>ఆన్‌లైన్ డిజిటల్ మాగజైన్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/magazine?month={month}\n\n"
        f"🎯 <i>APPSC • TSPSC గ్రూప్ 1, 2, 3 • UPSC • SSC ప్రత్యేకం</i>"
    )

    pdf_path = generate_magazine_pdf(year_month=month, force_refresh=False)
    if not pdf_path or not os.path.exists(pdf_path):
        # Check static frontend path
        static_p = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "pdfs", "Lakshya_September_2026_Monthly_Magazine.pdf")
        if os.path.exists(static_p):
            pdf_path = static_p

    if not pdf_path or not os.path.exists(pdf_path):
        fallback_msg = (
            f"📘 <b>లక్ష్య కరెంట్ అఫైర్స్ మాస పత్రిక ({month})</b>\n\n"
            f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/api/magazine/pdf?month={month}\n\n"
            f"📖 <b>ఆన్‌లైన్ రీడర్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/magazine?month={month}"
        )
        return send_telegram_message(fallback_msg, token=token, chat_id=chat_id)

    res = send_telegram_document(
        file_path=pdf_path,
        caption=caption,
        filename=f"Lakshya_Monthly_Magazine_{month}.pdf",
        token=token,
        chat_id=chat_id
    )
    if not res.get("success"):
        fallback_msg = (
            f"📘 <b>లక్ష్య కరెంట్ అఫైర్స్ మాస పత్రిక ({month})</b>\n\n"
            f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/api/magazine/pdf?month={month}\n\n"
            f"📖 <b>ఆన్‌లైన్ రీడర్:</b>\n"
            f"👉 https://lakshya-telugu-ca.onrender.com/magazine?month={month}"
        )
        send_telegram_message(fallback_msg, token=token, chat_id=chat_id)
    return res

if __name__ == "__main__":
    cfg = load_config()
    print("Telegram Config:", cfg)
