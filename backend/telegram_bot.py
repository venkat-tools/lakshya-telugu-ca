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
SUBSCRIBERS_PATH = os.path.join(os.path.dirname(__file__), "subscribers.json")

def load_config():
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"bot_token": "", "chat_id": ""}

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
        f"📰 <b>లక్ష్య డైలీ తెలుగు ఈ-పేపర్ ఎడిషన్ (PDF)</b>\n"
        f"📅 <b>తేదీ: {date}</b>\n\n"
        f"📊 <b>విశేషాలు:</b>\n"
        f"• ఈనాడు, సాక్షి, నమస్తే తెలంగాణ 56 ఆర్టికల్స్ సమగ్ర విశ్లేషణ\n"
        f"• ఒక వరుస ముఖ్యాంశాలు (Quick Revision One-Liners)\n"
        f"• వివరణలతో కూడిన 5 ప్రాక్టీస్ MCQs ప్రశ్నలు\n\n"
        f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={date}\n"
        f"🌐 <b>ఆన్‌లైన్ డిజిటల్ ఈ-పేపర్:</b>\n"
        f"👉 https://lakshya-telugu-ca.onrender.com/epaper?date={date}\n\n"
        f"🎯 <i>APPSC • TSPSC • UPSC • SSC విజేతల ప్రత్యేక ఎడిషన్</i>"
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

    target_chats = [str(chat_id)] if chat_id else load_subscribers()
    if not target_chats:
        cfg = load_config()
        if cfg.get("chat_id"):
            target_chats = [str(cfg["chat_id"])]

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

    return {
        "success": True,
        "message": f"{date} నాటి డైజెస్ట్, క్విజ్ పోల్స్ మరియు ఈ-పేపర్ PDF {len(target_chats)} మందికి టెలిగ్రామ్‌కు విజయవంతంగా పంపబడ్డాయి!",
        "articles_sent": len(articles),
        "quizzes_sent": sent_polls,
        "pdf_sent": pdf_sent_count > 0,
        "subscribers_count": len(target_chats)
    }

if __name__ == "__main__":
    cfg = load_config()
    print("Telegram Config:", cfg)
