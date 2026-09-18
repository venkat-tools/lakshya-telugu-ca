# -*- coding: utf-8 -*-
"""
Standalone Telegram Bot Service for Telugu Current Affairs.
Listens for user commands: /start, /today, /quiz, /oneliners, /help
"""

import time
import requests
import sys
import os
from datetime import datetime
from telegram_bot import load_config, broadcast_daily_digest, send_telegram_message, send_telegram_quiz_poll, add_subscriber, send_monthly_magazine_telegram, load_channels, add_channel, remove_channel, send_daily_bulletin_audio
from db import get_articles, get_quiz_by_date, get_one_liners_by_date, get_available_dates

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def check_and_send_daily_notification():
    try:
        from scheduler import load_scheduler_config, save_scheduler_config, get_ist_now, get_ist_today
        cfg = load_scheduler_config()
        if not cfg.get("enabled", True):
            return

        now_ist = get_ist_now()
        today_str = get_ist_today()
        target_time = cfg.get("scheduled_time", "07:00")
        current_hm = now_ist.strftime("%H:%M")

        # If current IST time is past target time and hasn't been sent today
        if current_hm >= target_time and cfg.get("last_run_date") != today_str:
            print(f"⏰ [Auto Notification] నేటి డైలీ కరెంట్ అఫైర్స్ బ్రాడ్‌కాస్ట్ ప్రారంభం ({today_str} IST)...")
            res = broadcast_daily_digest(date=today_str)
            if res.get("success"):
                cfg["last_run_date"] = today_str
                cfg["last_run_time"] = now_ist.strftime("%Y-%m-%d %H:%M:%S IST")
                cfg["last_status"] = "Success"
                import os, json
                SCHEDULER_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "scheduler_config.json")
                with open(SCHEDULER_CONFIG_PATH, "w", encoding="utf-8") as f:
                    json.dump(cfg, f, ensure_ascii=False, indent=2)
                print(f"✅ [Auto Notification] టెలిగ్రామ్ నోటిఫికేషన్ విజయవంతంగా పంపబడింది! ({res.get('quizzes_sent', 0)} క్విజ్ పోల్స్)")
    except Exception as e:
        print(f"⚠️ Auto Notification Error: {e}")

def start_bot_polling():
    config = load_config()
    token = config.get("bot_token")

    if not token:
        print("❌ Bot Token ఇంకా సెట్ చేయలేదు!")
        print("వెబ్ డ్యాష్‌బోర్డ్‌లో లేదా telegram_config.json లో మీ Telegram Bot Token నమోదు చేయండి.")
        return

    print("🤖 తెలుగు కరెంట్ అఫైర్స్ టెలిగ్రామ్ బోట్ రన్ అవుతోంది...")
    print("ఆపడానికి Ctrl+C ప్రెస్ చేయండి.")

    # 1. On startup catch-up check:
    check_and_send_daily_notification()

    last_update_id = 0
    option_map = {"A": 0, "B": 1, "C": 2, "D": 3}
    last_scheduler_check = time.time()

    while True:
        try:
            # Check scheduler every 60 seconds
            if time.time() - last_scheduler_check > 60:
                check_and_send_daily_notification()
                last_scheduler_check = time.time()

            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={last_update_id + 1}&timeout=30"
            res = requests.get(url, timeout=35)
            data = res.json()

            if not data.get("ok"):
                time.sleep(5)
                continue

            for update in data.get("result", []):
                last_update_id = update["update_id"]
                msg = update.get("message")
                if not msg:
                    continue

                chat_id = msg["chat"]["id"]
                add_subscriber(chat_id)
                doc = msg.get("document")
                caption = (msg.get("caption") or "").strip()
                text = (msg.get("text") or caption).strip()
                user_name = msg.get("from", {}).get("first_name", "మిత్రమా")

                if not text and not doc:
                    continue

                # Handle PDF Document Uploads
                if doc:
                    file_name = doc.get("file_name", "document.pdf")
                    mime_type = doc.get("mime_type", "")
                    is_pdf = file_name.lower().endswith(".pdf") or mime_type == "application/pdf"

                    if is_pdf:
                        admin_chat_id = config.get("chat_id") or "5405953028"
                        if str(chat_id) != str(admin_chat_id) and str(chat_id) != "5405953028":
                            no_perm_msg = (
                                "⚠️ <b>అనుమతి నిరాకరించబడింది!</b>\n\n"
                                "వెబ్‌సైట్‌లోకి PDF మెటీరియల్స్ అప్‌లోడ్ చేసే అధికారం కేవలం అడ్మిన్‌కు మాత్రమే ఉంది.\n"
                                "స్టడీ మెటీరియల్స్ కోసం <b>/material</b> లేదా <b>/syllabus</b> ఉపయోగించండి."
                            )
                            send_telegram_message(no_perm_msg, token=token, chat_id=chat_id)
                            continue

                        send_telegram_message(
                            f"⏳ <b>మీరు పంపిన PDF అందింది:</b> <code>{file_name}</code>\n\n"
                            f"<i>PDF నుండి సిలబస్ ముఖ్యాంశాలు, ఆర్టికల్స్ మరియు క్విజ్ MCQs సంగ్రహించి వెబ్‌సైట్‌లో అప్‌డేట్ చేస్తున్నాం... దయచేసి కొన్ని సెకన్లు వేచి ఉండండి.</i>",
                            token=token,
                            chat_id=chat_id
                        )

                        try:
                            file_id = doc["file_id"]
                            file_info_url = f"https://api.telegram.org/bot{token}/getFile?file_id={file_id}"
                            file_info_res = requests.get(file_info_url, timeout=30).json()

                            if not file_info_res.get("ok"):
                                raise RuntimeError("టెలిగ్రామ్ సర్వర్ నుండి ఫైల్ పాత్ పొందలేకపోయాము.")

                            tg_file_path = file_info_res["result"]["file_path"]
                            download_url = f"https://api.telegram.org/file/bot{token}/{tg_file_path}"
                            pdf_bytes = requests.get(download_url, timeout=120).content

                            import tempfile
                            temp_dir = tempfile.gettempdir()
                            temp_pdf_path = os.path.join(temp_dir, f"tg_{int(time.time())}_{file_name}")
                            with open(temp_pdf_path, "wb") as pf:
                                pf.write(pdf_bytes)

                            cat = "education"
                            check_str = (caption + " " + file_name).lower()
                            if any(k in check_str for k in ["polity", "రాజ్యాంగం", "పాలిటీ", "constitution"]):
                                cat = "polity"
                            elif any(k in check_str for k in ["history", "చరిత్ర"]):
                                cat = "history"
                            elif any(k in check_str for k in ["geography", "భూగోళ"]):
                                cat = "geography"
                            elif any(k in check_str for k in ["economy", "ఆర్థిక", "బడ్జెట్", "budget"]):
                                cat = "economy"
                            elif any(k in check_str for k in ["science", "సైన్స్", "isro", "tech"]):
                                cat = "scitech"
                            elif any(k in check_str for k in ["scheme", "పథకాలు", "సంక్షేమం", "welfare"]):
                                cat = "regional"

                            custom_title = caption if (caption and not caption.startswith("/")) else file_name.replace(".pdf", "").replace("_", " ").title()

                            from pdf_extractor import process_uploaded_pdf
                            result = process_uploaded_pdf(
                                file_input=temp_pdf_path,
                                custom_title=custom_title,
                                category=cat,
                                sync_to_website=True,
                                extract_quizzes=True
                            )

                            title = result["title"]
                            total_pages = result["total_pages"]
                            size_fmt = result["file_size_formatted"]
                            cat_name = result["category_name"]
                            articles_cnt = result["articles_created"]
                            quizzes_cnt = result["quizzes_created"]
                            pdf_url = result["pdf_url"]

                            success_msg = (
                                f"🎉 <b>PDF విజయవంతంగా వెబ్‌సైట్‌లో అప్‌డేట్ చేయబడింది!</b>\n"
                                f"───────────────────────\n"
                                f"📖 <b>మెటీరియల్:</b> {title}\n"
                                f"📄 <b>పేజీలు:</b> {total_pages} | <b>సైజ్:</b> {size_fmt}\n"
                                f"🏷️ <b>విభాగం:</b> {cat_name}\n"
                                f"📰 <b>వెబ్‌సైట్‌లో చేర్చిన ఆర్టికల్స్:</b> {articles_cnt} విభాగాలు\n"
                                f"📝 <b>జనరేట్ చేసిన ప్రాక్టీస్ MCQs:</b> {quizzes_cnt}\n\n"
                                f"🌐 <b>వెబ్‌సైట్ డిజిటల్ లైబ్రరీ లింక్:</b>\n"
                                f"👉 https://lakshya-telugu-ca.onrender.com/pdf_upload_hub\n\n"
                                f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్ లింక్:</b>\n"
                                f"👉 https://lakshya-telugu-ca.onrender.com{pdf_url}\n\n"
                                f"<i>విద్యార్థులు ఇప్పుడు వెబ్‌సైట్ మరియు డిజిటల్ లైబ్రరీలో ఈ స్టడీ మెటీరియల్‌ను చదువుకోవచ్చు!</i> 🚀"
                            )
                            send_telegram_message(success_msg, token=token, chat_id=chat_id)

                            try:
                                if os.path.exists(temp_pdf_path):
                                    os.remove(temp_pdf_path)
                            except Exception:
                                pass

                        except Exception as pe:
                            err_msg = f"❌ <b>PDF ప్రాసెసింగ్‌లో లోపం ఎదురైంది:</b>\n<code>{str(pe)[:300]}</code>"
                            send_telegram_message(err_msg, token=token, chat_id=chat_id)

                        continue

                dates = get_available_dates()
                today_date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")

                if text == "/start" or text == "/help":
                    welcome = (
                        f"నమస్కారం {user_name}! 🙏\n\n"
                        f"🎯 <b>లక్ష్య తెలుగు డైలీ కరెంట్ అఫైర్స్ & ఈ-పేపర్ బోట్</b>కు స్వాగతం!\n"
                        f"(APPSC, TSPSC, UPSC, SSC, Banking Special)\n\n"
                        f"📋 <b>ముఖ్యమైన కమాండ్స్:</b>\n"
                        f"👉 <b>/epaper</b> లేదా <b>/pdf</b> - నేటి పూర్తి తెలుగు ఈ-పేపర్ PDF డౌన్‌లోడ్ లింక్ & ఫైల్ 📥\n"
                        f"👉 <b>/papers</b> లేదా <b>/newspapers</b> - ఈనాడు, సాక్షి, ఆంధ్రజ్యోతి అధికారిక ఈ-పేపర్స్ PDF లింక్స్ 🗞️\n"
                        f"👉 <b>/today</b> - నేటి 56 ఆర్టికల్స్ ముఖ్యాంశాలు 📰\n"
                        f"👉 <b>/quiz</b> - నేటి 5 ప్రాక్టీస్ క్విజ్ పోల్స్ (MCQs) 📝\n"
                        f"👉 <b>/oneliners</b> - ఒక వరుస ముఖ్యాంశాలు (Quick Revision) ⚡\n"
                        f"👉 <b>/subscribe</b> - ప్రతిరోజూ ఉదయం ఆటోమేటిక్ PDF డెలివరీకి సబ్‌స్క్రైబ్ 🔔\n"
                        f"👉 <b>/syllabus</b> లేదా <b>/material</b> - APPSC గ్రూప్ 1 & 2 సమగ్ర సిలబస్ & 7 పుస్తకాలు (PDF) 📚\n"
                        f"👉 <b>/history</b> - భారత & AP చరిత్ర మాస్టర్ బుక్ (PDF) & టెస్ట్ 🏛️\n"
                        f"👉 <b>/schemes</b> - సంక్షేమ పథకాలు 2026 (సూపర్ సిక్స్ & 6 గ్యారెంటీలు) 🌾\n"
                        f"👉 <b>/mains</b> - గ్రూప్ 1 & 2 మెయిన్స్ మోడల్ సమాధానాలు ✍️\n"
                        f"👉 <b>/group2</b> లేదా <b>/mock</b> - APPSC గ్రూప్-2 గ్రాండ్ టెస్ట్ (150 Qs) & PYQs 🎯\n"
                        f"👉 <b>/map</b> - మ్యాప్ పాయింటింగ్ అట్లాస్ (AP, India, World) 🗺️\n"
                        f"👉 <b>/mobile</b> - మొబైల్ యాప్ లింక్ 📱\n"
                        f"👉 <b>/all</b> - నేటి మొత్తం డైజెస్ట్ + క్విజ్ + ఈ-పేపర్ PDF 🚀\n\
👉 <b>/monthly</b> - సెప్టెంబర్ 2026 మాస పత్రిక PDF (34 పేజీలు) 📘\n\
👉 <b>/audio</b> లేదా <b>/podcast</b> - నేటి 5-నిమిషాల కరెంట్ అఫైర్స్ ఆడియో బులెటిన్ (MP3) 🎙️\n\
👉 <b>/tests</b> - 150 చాప్టర్ ప్రాక్టీస్ MCQs (చరిత్ర, భౌగోళికం, సమాజం, ఆప్టిట్యూడ్) 📝\n\
👉 <b>/budget</b> - AP & TS ఎకనామిక్ సర్వే & బడ్జెట్ 2026 మాస్టర్ గైడ్ & PDF 📊\n\
👉 <b>/editorial</b> - డైలీ తెలుగు ఎడిటోరియల్ విశ్లేషణ (ఈనాడు, సాక్షి, ది హిందూ) 📰\n\
👉 <b>/ask [ప్రశ్న]</b> - తెలుగు AI ఎగ్జామ్ డౌట్ సాల్వర్ (ఉదా: /ask ఆర్టికల్ 32) 🤖\n\
👉 <b>/live_test</b> - డైలీ లైవ్ టైమ్డ్ మాక్ టెస్ట్ & స్టేట్ లీడర్‌బోర్డ్ 🏆\n\
👉 <b>/channels</b> - కనెక్ట్ అయిన టెలిగ్రామ్ ఛానల్స్ & గ్రూప్స్ జాబితా 📢\n\
👉 <b>/setchannel @channel_name</b> - కొత్త ఛానల్‌ను బ్రోడ్‌కాస్ట్‌కు లింక్ చేయండి 🔗\n\
👉 <b>/bifurcation</b> - AP పునర్విభజన చట్టం 2014 సమగ్ర గైడ్ & మాస్టర్ PDF 📜\n\
👉 <b>/amendments</b> - 1 నుండి 106 రాజ్యాంగ సవరణలు & 20 ల్యాండ్‌మార్క్ SC తీర్పులు ⚖️\n\
👉 <b>/weekly</b> - ఆదివారం వీక్లీ కరెంట్ అఫైర్స్ రివిజన్ & 50 MCQs మెగా టెస్ట్ 🗓️\n\
👉 <b>/matrix</b> - AP సూపర్ సిక్స్ & TS 6 గ్యారెంటీలు సంక్షేమ పథకాల పోలిక మేట్రిక్స్ 🌾\n\
👉 <b>/articles</b> - భారత రాజ్యాంగ ఆర్టికల్స్ (1-395) మాస్టర్ డైరెక్టరీ & PDF 🏛️\n\
👉 <b>/scitech</b> - సైన్స్, టెక్నాలజీ & రక్షణ రంగం 2025–2026 మెగా హబ్ & PDF 🛰️\n\
👉 <b>/environment</b> - పర్యావరణం, జీవవైవిధ్యం & క్లైమేట్ చేంజ్ హ్యాండ్‌బుక్ & PDF 🌍\n\
👉 <b>/centralschemes</b> - కేంద్ర ప్రభుత్వ పథకాలు 2026 (పీఎం సూర్య ఘర్, ఆయుష్మాన్ 70+) 💰\n\
👉 <b>/society</b> - భారతీయ సమాజం (30 మార్కులు) సమగ్ర మాస్టర్ హబ్ & PDF 👥\n\
👉 <b>/planner</b> - 60 రోజుల స్మార్ట్ డైలీ స్టడీ ప్లానర్ & సిలబస్ ట్రాకర్ 📅\n\
👉 <b>/pyqs</b> - APPSC & TSPSC గత ప్రశ్నల (PYQs) డీప్ ఎక్స్‌ప్లోరర్ & కటాఫ్స్ 🔍\n\
👉 <b>/aptitude</b> - మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్ షార్ట్‌కట్స్ ప్రాక్టీస్ ఇంజిన్ 🧮\n\
👉 <b>/audiorevision</b> - ఆడియో రివిజన్ ప్లేయర్ & 8 పాడ్‌కాస్ట్ ట్రాక్‌లు 🎧\n\
👉 <b>/mains</b> - మెయిన్స్ ఆన్సర్ రైటింగ్ డిజిటల్ పోర్టల్ & హ్యాండ్‌బుక్ PDF ✍️\n\
👉 <b>/analytics</b> - విద్యార్థి పెర్ఫార్మెన్స్ అనలిటిక్స్ & వీక్‌నెస్ డయాగ్నోజర్ 📊\n\
👉 <b>/staticgk</b> - స్టాటిక్ జీకే సూపర్-ఫాస్ట్ పాకెట్‌బుక్ & PDF 🇮🇳\n\
👉 <b>/atlas</b> - మ్యాప్ పాయింటింగ్ మాస్టర్ అట్లాస్ & PDF (AP, India, World) 🗺️\n\
👉 <b>/judgments</b> - సుప్రీంకోర్టు 30 చారిత్రక తీర్పులు (1950-2026) & PDF ⚖️\n\
👉 <b>/paper2</b> - APPSC గ్రూప్-2 పేపర్-2 (150 Marks) మెగా పోర్టల్ & మాక్ టెస్ట్ 🎯\n\
👉 <b>/agri</b> - AP & TS వ్యవసాయం, సాగునీరు & ఆక్వాకల్చర్ మాస్టర్ హబ్ & PDF 🌾\n\
👉 <b>/awards</b> - అవార్డులు, క్రీడలు & ప్రముఖ నియామకాలు 2025–2026 & PDF 🏆\n\
👉 <b>/group1</b> - APPSC Group-1 ప్రిలిమ్స్ (240 Marks) మెగా గ్రాండ్ సిమ్యులేటర్ 🎯\n\
👉 <b>/tribal</b> - AP & TS గిరిజన సంస్కృతి, PVTGs & PESA చట్టం హ్యాండ్‌బుక్ & PDF 📜\n\
👉 <b>/upload</b> - ఎడ్యుకేషనల్ PDF అప్‌లోడ్ పోర్టల్ & ఆటో-సింక్ గైడ్ 📤\n"
                    )
                    send_telegram_message(welcome, token=token, chat_id=chat_id)

                elif text in ["/upload", "/upload_pdf", "/pdfhub"]:
                    upload_msg = (
                        "📤 <b>లక్ష్య ఎడ్యుకేషనల్ PDF అప్‌లోడర్ & ఆటో-సింక్ హబ్</b>\n"
                        "───────────────────────\n"
                        "మీరు ఏవైనా ఎడ్యుకేషన్ నోట్స్, APPSC/TSPSC జీవోలు, మోడల్ పేపర్స్ PDF లను నేరుగా వెబ్‌సైట్‌లోకి అప్‌లోడ్ చేయవచ్చు!\n\n"
                        "📱 <b>రెండు సులువైన పద్ధతులు:</b>\n"
                        "1️⃣ <b>టెలిగ్రామ్ ద్వారా:</b> మీ మొబైల్ నుండి ఏదైనా స్టడీ PDF ని నేరుగా ఈ చాట్‌కు డాక్యుమెంట్‌గా పంపండి. బోట్ ఆటోమేటిక్‌గా అందులోని కంటెంట్‌ను సంగ్రహించి వెబ్‌సైట్‌లో అప్‌డేట్ చేస్తుంది!\n\n"
                        "2️⃣ <b>వెబ్ పోర్టల్ ద్వారా:</b> బ్రౌజర్‌లో డ్రాగ్ & డ్రాప్ ద్వారా అప్‌లోడ్ చేయడానికి క్రింది లింక్ క్లిక్ చేయండి:\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdf_upload_hub\n\n"
                        "🔑 <i>అడ్మిన్ సెక్యూరిటీ పిన్: <code>lakshya2026</code></i>"
                    )
                    send_telegram_message(upload_msg, token=token, chat_id=chat_id)

                elif text == "/subscribe":
                    sub_msg = (
                        f"✅ <b>సబ్‌స్క్రిప్షన్ విజయవంతమైంది!</b> 🙏\n\n"
                        f"మీరు డైలీ తెలుగు కరెంట్ అఫైర్స్ & ఈ-పేపర్ PDF ఆటోమేటిక్ డెలివరీకి విజయవంతంగా సబ్‌స్క్రైబ్ చేసుకున్నారు.\n"
                        f"⏰ ప్రతిరోజూ ఉదయం 7:00 గంటలకు (IST) నేటి పూర్తి ఈ-పేపర్ PDF, ముఖ్యాంశాలు మరియు క్విజ్ పోల్స్ మీ టెలిగ్రామ్‌కు నేరుగా వస్తాయి!\n\n"
                        f"📥 నేటి PDF ని ఇప్పుడే పొందడానికి <b>/pdf</b> లేదా <b>/epaper</b> అని టైప్ చేయండి."
                    )
                    send_telegram_message(sub_msg, token=token, chat_id=chat_id)

                elif text == "/syllabus" or text == "/material":
                    syl_msg = (
                        f"📚 <b>APPSC గ్రూప్ 1 & 2 సమగ్ర మాస్టర్ సిలబస్ & స్టడీ గైడ్ పోర్టల్</b>\n"
                        f"───────────────────────\n"
                        f"🎯 <b>8 సబ్జెక్టుల సమగ్ర సమాచారం & మెటీరియల్:</b>\n"
                        f"1️⃣ <b>భూగోళశాస్త్రం (Geography):</b> జియోమార్ఫాలజీ, డిస్‌కంటిన్యూటీలు, భూకంప తరంగాలు, పాస్ లు, నదులు, ప్రాజెక్టులు, 26 జిల్లాలు, ISFR 2023\n"
                        f"2️⃣ <b>AP పాలసీలు 4.0 (2024-2029):</b> ఇండస్ట్రియల్ పాలసీ, MSME 2030, ఫుడ్ ప్రాసెసింగ్, టెక్స్‌టైల్ TAG 4.0, ఎలక్ట్రానిక్స్, డ్రోన్ పాలసీ 4.0, పోర్టులు\n"
                        f"3️⃣ <b>మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్:</b> 120+ షార్ట్‌కట్ సూత్రాలు, మెన్సురేషన్ స్కేలింగ్, రైళ్లు, మిశ్రమాలు, క్లాక్స్, క్యాలెండర్, సిలాజిజమ్\n"
                        f"4️⃣ <b>భారత & AP చరిత్ర:</b> ప్రాచీన, మధ్యయుగ, ఆధునిక, శాతవాహనులు, విజయనగరం, 2014 పునర్విభజన చట్టం\n"
                        f"5️⃣ <b>రాజ్యాంగం & పాలిటీ:</b> ఆర్టికల్స్ 12-35, 44 UCC, 352-360 ఎమర్జెన్సీలు, 73/74 సవరణలు\n"
                        f"6️⃣ <b>ఎకానమీ & మనీ మార్కెట్:</b> మనీ మార్కెట్ సాధనాలు, ద్రవ్యోల్బణం, RBI పాలసీలు, నీతి ఆయోగ్ సూచీలు\n"
                        f"7️⃣ <b>సైన్స్, టెక్నాలజీ & పర్యావరణం:</b> ISRO/DRDO మిషన్లు, బయోస్పియర్ రిజర్వ్‌లు, పర్యావరణ ఒప్పందాలు\n"
                        f"8️⃣ <b>మెయిన్స్ ఆన్సర్ రైటింగ్ & ఎథిక్స్:</b> 4-దశల ఫ్రేమ్‌వర్క్, కేస్ స్టడీ టెక్నిక్స్, టాప్ స్కోరింగ్ మోడల్స్\n\n"
                        f"📚 <b>7 ఒరిజినల్ మాస్టర్ టెక్స్ట్‌బుక్స్ PDF హబ్:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/appsc_syllabus\n"
                        f"👉 📥 <b>చరిత్ర మాస్టర్ బుక్ (PDF):</b> https://lakshya-telugu-ca.onrender.com/pdfs/indian_and_ap_history_master_notes.pdf\n\n"
                        f"🖨️ <b>హై-క్వాలిటీ ప్రింట్ / PDF కూడా వెబ్‌సైట్‌లో డౌన్‌లోడ్ చేసుకోవచ్చు!</b>"
                    )
                    send_telegram_message(syl_msg, token=token, chat_id=chat_id)

                elif text == "/history" or text == "/aphistory":
                    from ap_history_data import get_ap_history_questions
                    hist_msg = (
                        f"🏛️ <b>ఆంధ్రప్రదేశ్ సమగ్ర చరిత్ర & APPSC గ్రూప్స్ 1, 2, 3 హబ్</b>\n"
                        f"───────────────────────\n"
                        f"📜 <b>సిలబస్ ముఖ్య విభాగాలు:</b>\n"
                        f"• శాతవాహనుల యుగం (నాసిక్ శాసనం, హాలుడు, నాగార్జునుడు)\n"
                        f"• ఇక్ష్వాకులు & విష్ణుకుండినులు (నాగార్జునకొండ, ఉండవల్లి గుహలు)\n"
                        f"• తూర్పు చాళుక్యులు (రాజరాజ నరేంద్రుడు, నన్నయ మహాభారతం)\n"
                        f"• కాకతీయుల వైభవం (రుద్రమదేవి, వేయిస్తంభాల గుడి, మోటుపల్లి)\n"
                        f"• రెడ్డిరాజుల యుగం (కొండవీడు, వేమన, శ్రీనాథుడు)\n"
                        f"• విజయనగర సామ్రాజ్యం (శ్రీకృష్ణదేవరాయలు, అముక్తమాల్యద)\n"
                        f"• ఆధునిక జాతీయోద్యమం (ఆంధ్రోద్యమం, పొట్టి శ్రీరాములు, 1953 ఆంధ్ర రాష్ట్రం)\n"
                        f"• 2014 AP పునర్విభజన చట్టం (12 భాగాలు, 108 సెక్షన్లు)\n\n"
                        f"📥 <b>భారత & AP సమగ్ర చరిత్ర మాస్టర్ బుక్ (PDF డౌన్‌లోడ్):</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/pdfs/indian_and_ap_history_master_notes.pdf\n\n"
                        f"🖨️ <b>గ్రూప్స్ 1, 2, 3 OMR టెస్ట్ పేపర్స్ & ఆన్సర్ కీస్ (PDF):</b>\n"
                        f"👉 గ్రూప్-1 (120 Qs): https://lakshya-telugu-ca.onrender.com/omr_appsc_all?exam=group1\n"
                        f"👉 గ్రూప్-2 (150 Qs): https://lakshya-telugu-ca.onrender.com/omr_appsc_all?exam=group2\n"
                        f"👉 గ్రూప్-3 (150 Qs): https://lakshya-telugu-ca.onrender.com/omr_appsc_all?exam=group3\n\n"
                        f"👇 <i>క్రింది AP చరిత్ర PYQ మోడల్ ప్రశ్నకు సమాధానం ఇవ్వండి:</i>"
                    )
                    send_telegram_message(hist_msg, token=token, chat_id=chat_id)
                    hist_qs = get_ap_history_questions()[:2]
                    for q in hist_qs:
                        c_idx = option_map.get(q.get("correct_option", "A").upper(), 0)
                        opts = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
                        send_telegram_quiz_poll(
                            question=f"🏛️ [AP చరిత్ర PYQ] {q['question']}"[:255],
                            options=[o[:100] for o in opts],
                            correct_index=c_idx,
                            explanation=q.get("explanation", "")[:200],
                            token=token,
                            chat_id=chat_id
                        )

                elif text == "/schemes" or text == "/budget":
                    from schemes_budget_data import get_schemes_quizzes
                    schemes_msg = (
                        f"🌾 <b>ప్రభుత్వ సంక్షేమ పథకాలు & బడ్జెట్ 2026 హబ్</b>\n"
                        f"<i>(APPSC & TSPSC 15-20 మార్కుల వెయిటేజీ)</i>\n\n"
                        f"🚩 <b>AP సూపర్ సిక్స్ పథకాలు:</b>\n"
                        f"• తల్లికి వందనం: ప్రతి విద్యార్థికి ₹15,000\n"
                        f"• అన్నదాత సుఖీభవ: రైతులకు ₹20,000 (కేంద్రం ₹6,000 + AP ₹14,000)\n"
                        f"• దీపం-2: ఏడాదికి 3 ఉచిత గ్యాస్ సిలిండర్లు\n"
                        f"• మహిళలకు RTC బస్సుల్లో ఉచిత ప్రయాణం\n"
                        f"• యువగళం: నిరుద్యోగ భృతి ₹3,000 & 20 లక్షల ఉద్యోగాలు\n"
                        f"• ఆడబిడ్డ నిధి: 18-59 ఏళ్ల మహిళలకు నెలకు ₹1,500\n\n"
                        f"🌾 <b>తెలంగాణ 6 గ్యారెంటీలు:</b>\n"
                        f"• మహాలక్ష్మి, గృహజ్యోతి (200 యూనిట్లు ఉచితం), రైతు భరోసా, ఇందిరమ్మ ఇండ్లు, చేయూత, యువ వికాసం\n\n"
                        f"📖 <b>సంక్షేమ పథకాల సమగ్ర హ్యాండ్‌బుక్ PDF:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/schemes_handbook\n\n"
                        f"👇 <i>క్రింది ప్రభుత్వ పథకాల ప్రశ్నకు సమాధానం ఇవ్వండి:</i>"
                    )
                    send_telegram_message(schemes_msg, token=token, chat_id=chat_id)
                    s_quizzes = get_schemes_quizzes()[:2]
                    for q in s_quizzes:
                        c_idx = q["options"].index(q["answer"]) if q["answer"] in q["options"] else 0
                        send_telegram_quiz_poll(
                            question=f"🌾 [సంక్షేమ పథకాలు] {q['question']}"[:255],
                            options=[o[:100] for o in q["options"]],
                            correct_index=c_idx,
                            explanation=q.get("explanation", "")[:200],
                            token=token,
                            chat_id=chat_id
                        )

                elif text == "/mains" or text == "/descriptive":
                    from mains_descriptive_data import get_all_mains_questions
                    mains_qs = get_all_mains_questions()
                    mains_msg = (
                        f"✍️ <b>APPSC గ్రూప్-1 & గ్రూప్-2 మెయిన్స్ మోడల్ సమాధానాల బ్యాంక్</b>\n"
                        f"<i>(అధికారిక ప్రామాణిక 4-దశల సమాధాన విధానం)</i>\n\n"
                        f"📝 <b>మోడల్ ప్రశ్న 1 ({mains_qs[0]['paper']}):</b>\n"
                        f"<b>{mains_qs[0]['question']}</b>\n\n"
                        f"📌 <b>పరిచయం:</b> {mains_qs[0]['model_answer']['intro'][:150]}...\n\n"
                        f"🏛️ <b>ప్రభుత్వ చర్యలు:</b> {mains_qs[0]['model_answer']['govt_steps'][:120]}...\n\n"
                        f"🎯 <b>ముగింపు:</b> {mains_qs[0]['model_answer']['conclusion'][:120]}...\n\n"
                        f"📖 <b>పూర్తి మెయిన్స్ ఆన్సర్ బ్యాంక్ (PDF ప్రింట్):</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/mains_answer_bank\n"
                        f"👉 http://localhost:5000/mains_answer_bank"
                    )
                    send_telegram_message(mains_msg, token=token, chat_id=chat_id)

                elif text == "/map" or text == "/mappointing":
                    from map_pointing_data import get_all_map_points, get_map_pointing_quiz_questions
                    pts = get_all_map_points()
                    map_msg = (
                        f"🗺️ <b>లక్ష్య మ్యాప్ పాయింటింగ్ ఎక్స్‌ప్లోరర్ & స్టడీ అట్లాస్</b>\n"
                        f"<i>(APPSC గ్రూప్-2 • గ్రూప్-1 • TSPSC • UPSC స్పెషల్)</i>\n\n"
                        f"🚩 <b>ఆంధ్రప్రదేశ్:</b> పోర్టులు, పోలవరం, శ్రీశైలం, కొల్లేరు, పులికాట్, తుమ్మలపల్లి, మంగంపేట, కోరింగ\n"
                        f"🇮🇳 <b>భారతదేశం:</b> నథూ లా, జోజి లా, షిప్కీ లా, 10 డిగ్రీ ఛానల్, కుడంకుళం, అనైముడి, సియాచిన్\n"
                        f"🌐 <b>ప్రపంచ చోక్‌పాయింట్స్:</b> హార్ముజ్, బాబ్-ఎల్-మందేబ్, మలక్కా, సూయజ్, దక్షిణ చైనా సముద్రం\n\n"
                        f"📖 <b>స్టడీ అట్లాస్ & క్విక్ రివిజన్ PDF:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/map_pointing_atlas\n"
                        f"👉 http://localhost:5000/map_pointing_atlas\n\n"
                        f"👇 <i>క్రింది మ్యాప్ పాయింటింగ్ మోడల్ ప్రశ్నకు సమాధానం ఇవ్వండి:</i>"
                    )
                    send_telegram_message(map_msg, token=token, chat_id=chat_id)
                    map_quizzes = get_map_pointing_quiz_questions()[:2]
                    for q in map_quizzes:
                        c_idx = q["options"].index(q["answer"]) if q["answer"] in q["options"] else 0
                        send_telegram_quiz_poll(
                            question=f"🗺️ [{q.get('location_name', '').split('(')[0].strip()}] {q['question']}"[:255],
                            options=[o[:100] for o in q["options"]],
                            correct_index=c_idx,
                            explanation=q.get("explanation", "")[:200],
                            token=token,
                            chat_id=chat_id
                        )

                elif text == "/group2" or text == "/mock":
                    from appsc_group2_data import get_appsc_group2_pyqs
                    send_telegram_message(
                        f"🎯 <b>APPSC గ్రూప్-2 సంపూర్ణ గ్రాండ్ మాక్ టెస్ట్ & PYQs (150 Qs)</b>\n"
                        f"───────────────────────\n"
                        f"🏛️ <b>భారతీయ చరిత్ర:</b> 30 ప్రశ్నలు\n"
                        f"🌍 <b>భూగోళశాస్త్రం:</b> 30 ప్రశ్నలు\n"
                        f"👥 <b>భారతీయ సమాజం:</b> 30 ప్రశ్నలు\n"
                        f"📰 <b>సమకాలీన అంశాలు:</b> 30 ప్రశ్నలు\n"
                        f"🧠 <b>మెంటల్ ఎబిలిటీ:</b> 30 ప్రశ్నలు\n"
                        f"───────────────────────\n"
                        f"⏱️ <b>వ్యవధి:</b> 150 నిమిషాలు | <b>నెగటివ్ మార్కింగ్:</b> 0.33\n\n"
                        f"🌐 <b>వెబ్ & మొబైల్‌లో 150 Qs గ్రాండ్ టెస్ట్ రాయండి:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com\n"
                        f"👉 http://localhost:5000\n\n"
                        f"🖨️ <b>150 Qs OMR పేపర్ & ఆన్సర్ కీ ప్రింట్ / PDF:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/omr_group2\n\n"
                        f"👇 <i>క్రింది APPSC గ్రూప్-2 అసలైన PYQ మోడల్ ప్రశ్నలకు సమాధానం ఇవ్వండి:</i>",
                        token=token,
                        chat_id=chat_id
                    )
                    pyqs = get_appsc_group2_pyqs()[:3]
                    for q in pyqs:
                        c_idx = option_map.get(q.get("correct_option", "A").upper(), 0)
                        opts = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
                        send_telegram_quiz_poll(
                            question=f"🎯 [{q.get('section_name')}] {q['question']}"[:255],
                            options=[o[:100] for o in opts],
                            correct_index=c_idx,
                            explanation=q.get("explanation", "")[:200],
                            token=token,
                            chat_id=chat_id
                        )

                elif text in ["/epaper", "/pdf", "/paper", "/newspaper"]:
                    from telegram_bot import send_daily_epaper_pdf, send_epapers_directory
                    send_telegram_message(
                        f"📰 <b>{today_date} నాటి తెలుగు ఈ-పేపర్ ఎడిషన్ (PDF)</b>\n"
                        f"───────────────────────\n\n"
                        f"📥 <b>డైరెక్ట్ PDF డౌన్‌లోడ్ లింక్ (1-Click Download):</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={today_date}\n\n"
                        f"📖 <b>ఆన్‌లైన్ డిజిటల్ ఈ-పేపర్ (HD పేపర్ మోడ్):</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/epaper?date={today_date}\n\n"
                        f"🗞️ <b>ఈనాడు, సాక్షి, ఆంధ్రజ్యోతి అధికారిక ఈ-పేపర్స్:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/epapers_directory\n\n"
                        f"⏳ <i>దయచేసి ఒక్క క్షణం వేచి ఉండండి, పూర్తి PDF ఫైల్ కూడా పంపుతున్నాము...</i>",
                        token=token, chat_id=chat_id
                    )
                    send_daily_epaper_pdf(date=today_date, token=token, chat_id=chat_id)
                    send_epapers_directory(date=today_date, token=token, chat_id=chat_id)

                elif text in ["/papers", "/newspapers", "/epapers", "/directory"]:
                    from telegram_bot import send_epapers_directory
                    send_epapers_directory(date=today_date, token=token, chat_id=chat_id)

                elif text == "/mobile":
                    mobile_msg = (
                        f"📱 <b>మొబైల్ ఫోన్ (4G / 5G డేటా) వెబ్ యాప్ లింక్:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com\n\n"
                        f"✨ ఈ లింక్‌తో మీరు ఎక్కడి నుంచైనా మొబైల్ బ్రౌజర్‌లో 24/7 ఆర్టికల్స్, క్విజ్‌లు మరియు గ్రాండ్ టెస్టులు చదువుకోవచ్చు!"
                    )
                    send_telegram_message(mobile_msg, token=token, chat_id=chat_id)

                elif text == "/today":
                    import html
                    articles = get_articles(date=today_date)
                    resp = f"📅 <b>తేదీ: {today_date} - నేటి టాప్ ఆర్టికల్స్ విశ్లేషణ</b>\n"
                    resp += f"📊 <i>(మొత్తం అందుబాటులో ఉన్నవి: {len(articles)} ఆర్టికల్స్)</i>\n───────────────────────\n"
                    for idx, a in enumerate(articles[:6], 1):
                        s_title = html.escape(a.get("title", ""))
                        s_sum = html.escape(a.get("summary", "")[:180])
                        resp += f"\n<b>{idx}. {s_title}</b>\n👉 {s_sum}...\n"
                        if a.get("exam_relevance"):
                            s_er = html.escape(a["exam_relevance"])
                            resp += f"<i>🎯 {s_er}</i>\n"
                    resp += f"\n📥 <b>నేటి ఈ-పేపర్ PDF డౌన్‌లోడ్:</b> https://lakshya-telugu-ca.onrender.com/api/epaper/pdf?date={today_date}\n"
                    resp += f"🌐 <b>మొత్తం {len(articles)} ఆర్టికల్స్ మొబైల్ లో చదవండి:</b> https://lakshya-telugu-ca.onrender.com"
                    send_telegram_message(resp, token=token, chat_id=chat_id)

                elif text == "/quiz":
                    from quiz_generator import ensure_daily_quizzes
                    quizzes = ensure_daily_quizzes(today_date)
                    if not quizzes:
                        send_telegram_message("ప్రస్తుతం ఈ తేదీకి క్విజ్ ప్రశ్నలు అందుబాటులో లేవు.", token=token, chat_id=chat_id)
                    else:
                        send_telegram_message(f"📝 <b>తేదీ: {today_date} - నేటి 5 ఇంటరాక్టివ్ క్విజ్ పోల్స్:</b>", token=token, chat_id=chat_id)
                        for q in quizzes[:5]:
                            c_idx = option_map.get(q.get("correct_option", "A").upper(), 0)
                            opts = [q["option_a"], q["option_b"], q["option_c"], q["option_d"]]
                            send_telegram_quiz_poll(
                                question=f"❓ [{today_date}] {q['question']}"[:255],
                                options=[o[:100] for o in opts],
                                correct_index=c_idx,
                                explanation=q.get("explanation", "")[:200],
                                token=token,
                                chat_id=chat_id
                            )

                elif text == "/oneliners":
                    import html
                    ols = get_one_liners_by_date(date=today_date)
                    resp = f"⚡ <b>తేదీ: {today_date} - ఒక వరుస ముఖ్యాంశాలు (Quick Revision):</b>\n───────────────────────\n\n"
                    for ol in ols[:12]:
                        s_pt = html.escape(ol.get("point", ""))
                        resp += f"• {s_pt}\n"
                    resp += f"\n🌐 <b>పూర్తి ముఖ్యాంశాల కోసం క్లిక్ చేయండి:</b> https://lakshya-telugu-ca.onrender.com"
                    send_telegram_message(resp, token=token, chat_id=chat_id)

                elif text == "/audio" or text == "/podcast":
                    send_telegram_message("🎙️ <b>నేటి 5 నిమిషాల కరెంట్ అఫైర్స్ ఆడియో పాడ్‌కాస్ట్ బులెటిన్ సిద్ధం చేయబడుతోంది... క్షణాల్లో మీ టెలిగ్రామ్‌కు వస్తుంది!</b>", token=token, chat_id=chat_id)
                    send_daily_bulletin_audio(date=today_date, token=token, chat_id=chat_id)

                elif text == "/monthly" or text == "/magazine":
                    send_telegram_message("📘 <b>సెప్టెంబర్ 2026 మాస పత్రిక PDF సిద్ధం చేయబడుతోంది... క్షణాల్లో మీ టెలిగ్రామ్‌కు వస్తుంది!</b>", token=token, chat_id=chat_id)
                    send_monthly_magazine_telegram(month="2026-09", token=token, chat_id=chat_id)

                elif text == "/tests" or text == "/subject_tests":
                    t_msg = (
                        f"📝 <b>APPSC & TSPSC సబ్జెక్ట్-వైజ్ చాప్టర్ టెస్ట్స్ హబ్ (150 MCQs)</b>\n"
                        f"───────────────────────\n\n"
                        f"🎯 <b>అందుబాటులో ఉన్న 5 ప్రధాన సబ్జెక్ట్స్ (30 MCQs Each):</b>\n"
                        f"1. 🏛️ చరిత్ర (సింధు నాగరికత, శాతవాహనులు, విజయనగరం, ఆధునిక ఏపీ)\n"
                        f"2. 🌍 భౌగోళికం (భూస్వరూపాలు, నదులు, తీరరేఖ, 26 జిల్లాలు, ఖనిజాలు)\n"
                        f"3. 👥 భారతీయ సమాజం (సామాజిక నిర్మాణం, చట్టాలు, మహిళలు, గిరిజనులు)\n"
                        f"4. 🧠 మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్ (షార్ట్‌కట్స్, శ్రేణులు, రీజనింగ్)\n"
                        f"5. 🌪️ విపత్తు నిర్వహణ (చట్టం 2005, సెండాయ్, తుఫానులు, కాలుష్యం)\n\n"
                        f"🌐 <b>ఇంటరాక్టివ్ ఆన్‌లైన్ టెస్ట్ రాయండి:</b>\n"
                        f"👉 https://lakshya-telugu-ca.onrender.com/subject_tests\n"
                        f"👉 http://localhost:5000/subject_tests\n\n"
                        f"💡 <i>వెబ్‌సైట్‌లో తక్షణ ఫలితాలు, మార్కులు మరియు వివరణలు పొందవచ్చు!</i>"
                    )
                    send_telegram_message(t_msg, token=token, chat_id=chat_id)

                elif text == "/channels":
                    chs = load_channels()
                    if not chs:
                        ch_text = (
                            f"📢 <b>కనెక్ట్ అయిన టెలిగ్రామ్ ఛానల్స్:</b> ఏవీ లేవు.\n\n"
                            f"మీ స్టడీ ఛానల్ లేదా గ్రూప్‌ను లింక్ చేయడానికి:\n"
                            f"👉 బోట్‌ను మీ ఛానల్‌లో అడ్మిన్‌గా చేర్చి <b>/setchannel @channel_username</b> అని టైప్ చేయండి."
                        )
                    else:
                        ch_text = f"📢 <b>కనెక్ట్ అయిన టెలిగ్రామ్ బ్రోడ్‌కాస్ట్ ఛానల్స్ ({len(chs)}):</b>\n───────────────────────\n"
                        for c in chs:
                            ch_text += f"• <b>{c.get('title', c.get('channel_id'))}</b> (ID: <code>{c.get('channel_id')}</code>)\n"
                        ch_text += f"\n✅ ప్రతిరోజూ ఉదయం 7 గంటలకు వీటన్నింటికీ ఈ-పేపర్ PDF ఆటోమేటిక్‌గా పంపబడుతుంది!"
                    send_telegram_message(ch_text, token=token, chat_id=chat_id)

                elif text.startswith("/setchannel"):
                    parts = text.split(maxsplit=2)
                    if len(parts) < 2:
                        send_telegram_message("⚠️ దయచేసి ఛానల్ యూజర్‌నేమ్ ఇవ్వండి. ఉదాహరణ: <code>/setchannel @telugugroups_study</code>", token=token, chat_id=chat_id)
                    else:
                        new_ch_id = parts[1].strip()
                        new_title = parts[2].strip() if len(parts) > 2 else new_ch_id
                        add_channel(new_ch_id, new_title)
                        send_telegram_message(f"✅ <b>ఛానల్ విజయవంతంగా నమోదు చేయబడింది!</b>\n📢 ఛానల్: <code>{new_ch_id}</code>\nఇకపై ఈ ఛానల్‌కు డైలీ ఈ-పేపర్ PDF & డైజెస్ట్ ఆటోమేటిక్‌గా బ్రాడ్‌కాస్ట్ అవుతుంది.", token=token, chat_id=chat_id)

                elif text == "/all":
                    broadcast_daily_digest(date=today_date, token=token, chat_id=chat_id)

                elif text == "/budget" or text == "/survey":
                    b_msg = (
                        "📊 <b>AP & TS ఎకనామిక్ సర్వే & బడ్జెట్ 2026 మాస్టర్ గైడ్ & PDF</b>\n"
                        "───────────────────────\n\n"
                        "🏛️ <b>ఆంధ్రప్రదేశ్ బడ్జెట్ 2024-25:</b> ₹2,94,421 కోట్లు (ద్రవ్య లోటు: 3.41%)\n"
                        "• తలసరి ఆదాయం: ₹2,42,479 (జాతీయ సగటు కంటే ₹56,625 అధికం)\n"
                        "• సూపర్ సిక్స్: తల్లికి వందనం (₹15,000), దీపం-2 (3 సిలిండర్లు), అన్నదాత సుఖీభవ (₹20,000)\n\n"
                        "🏛️ <b>తెలంగాణ బడ్జెట్ 2024-25:</b> ₹2,75,891 కోట్లు\n"
                        "• తలసరి ఆదాయం: ₹3,47,299 (దేశంలో అగ్రస్థానం, 86.9% ఎక్కువ)\n"
                        "• 6 గ్యారెంటీలు: మహాలక్ష్మి, రైతు భరోసా (₹15,000), గృహజ్యోతి (200u)\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/ap_ts_budget_economic_survey_master.pdf\n\n"
                        "🌐 <b>వెబ్ గైడ్:</b> https://lakshya-telugu-ca.onrender.com/budget_economy_guide"
                    )
                    send_telegram_message(b_msg, token=token, chat_id=chat_id)

                elif text == "/editorial" or text == "/editorials":
                    ed_msg = (
                        "📰 <b>డైలీ తెలుగు ఎడిటోరియల్ పరీక్షా విశ్లేషణ</b>\n"
                        "───────────────────────\n\n"
                        "1️⃣ <b>ఈనాడు:</b> జమిలి ఎన్నికల ప్రస్థానం - సమాఖ్య స్ఫూర్తి & ఆర్టికల్ 83, 172, 356\n"
                        "2️⃣ <b>సాక్షి:</b> పోలవరం ప్రాజెక్టు - ₹12,157 కోట్ల నిధులు & 41.15 మీటర్ల కాంటూర్\n"
                        "3️⃣ <b>ది హిందూ:</b> ద్రవ్యోల్బణం & వృద్ధి సమతౌల్యం - ఆర్బీఐ ఎంపీసీ (MPC) రేట్లు\n\n"
                        "💡 <i>ప్రిలిమ్స్ ఫ్యాక్ట్స్, మెయిన్స్ పాయింట్లు మరియు మోడల్ ప్రశ్నలతో వెబ్‌సైట్‌లో చదవండి:</i>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/editorials_hub"
                    )
                    send_telegram_message(ed_msg, token=token, chat_id=chat_id)

                elif text.startswith("/ask"):
                    q_parts = text.split(maxsplit=1)
                    if len(q_parts) < 2 or not q_parts[1].strip():
                        send_telegram_message("🤖 <b>తెలుగు AI ఎగ్జామ్ డౌట్ సాల్వర్</b>\nదయచేసి మీ సందేహాన్ని టైప్ చేయండి.\nఉదాహరణ: <code>/ask ఆర్టికల్ 32 ప్రాముఖ్యత ఏమిటి?</code>", token=token, chat_id=chat_id)
                    else:
                        from doubt_solver import solve_exam_doubt
                        query = q_parts[1].strip()
                        ans = solve_exam_doubt(query)
                        pointers = "\n".join([f"• {p}" for p in ans.get("exam_pointers", [])[:3]])
                        reply_msg = (
                            f"🤖 <b>AI ఎగ్జామ్ నోట్: {ans['title']}</b>\n"
                            f"📂 <i>{ans['subject']}</i>\n"
                            f"───────────────────────\n\n"
                            f"🎯 <b>నిర్వచనం & సారాంశం:</b>\n{ans['definition']}\n\n"
                            f"💡 <b>పరీక్ష పాయింట్లు:</b>\n{pointers}\n\n"
                            f"🌟 <b>ర్యాంకర్స్ టిప్:</b> {ans['tip']}\n\n"
                            f"🌐 <i>మరిన్ని సందేహాల కోసం: https://lakshya-telugu-ca.onrender.com/doubt_solver</i>"
                        )
                        send_telegram_message(reply_msg, token=token, chat_id=chat_id)

                elif text == "/live_test" or text == "/test_live":
                    lt_msg = (
                        "🏆 <b>లైవ్ డైలీ మాక్ టెస్ట్ (20 MCQs - 15 నిమిషాలు)</b>\n"
                        "───────────────────────\n\n"
                        "⚠️ <b>నిబంధనలు:</b>\n"
                        "• సమయం: 15 నిమిషాలు\n"
                        "• మార్కులు: సరైన ప్రశ్నకు +1.0 | తప్పు ప్రశ్నకు -0.33\n"
                        "• తక్షణమే రాష్ట్ర స్థాయి ర్యాంకింగ్ & లీడర్‌బోర్డ్ స్కోర్‌కార్డ్!\n\n"
                        "👉 <b>ఇప్పుడే లైవ్ టెస్ట్ రాయండి:</b>\n"
                        "https://lakshya-telugu-ca.onrender.com/daily_live_test"
                    )
                    send_telegram_message(lt_msg, token=token, chat_id=chat_id)

                elif text == "/bifurcation" or text == "/act2014":
                    bf_msg = (
                        "📜 <b>ఆంధ్రప్రదేశ్ పునర్విభజన చట్టం 2014 మాస్టర్ గైడ్ & PDF</b>\n"
                        "───────────────────────\n\n"
                        "🏛️ <b>చట్టం ప్రాథమిక అంశాలు:</b>\n"
                        "• చట్టం సంఖ్య: Act No. 6 of 2014\n"
                        "• రాష్ట్రపతి ఆమోదం: 1 మార్చి 2014 (ప్రణబ్ ముఖర్జీ)\n"
                        "• నియమిత దినం (Appointed Day): 2 జూన్ 2014\n"
                        "• మొత్తం భాగాలు: 12 | సెక్షన్లు: 108 | షెడ్యూల్స్: 13\n\n"
                        "⭐ <b>కీలక సెక్షన్లు:</b>\n"
                        "• సెక్షన్ 5: హైదరాబాద్ 10 ఏళ్లు ఉమ్మడి రాజధాని (2024 జూన్ 2తో గడువు ముగిసింది)\n"
                        "• సెక్షన్ 6: శివరామకృష్ణన్ కమిటీ (నూతన రాజధాని అధ్యయనం)\n"
                        "• సెక్షన్ 8: ఉమ్మడి రాజధానిలో గవర్నర్‌కు శాంతిభద్రతల ప్రత్యేకాధికారాలు\n"
                        "• సెక్షన్ 46: 14వ ఆర్థిక సంఘం రెవెన్యూ లోటు ప్రత్యేక గ్రాంట్లు\n"
                        "• సెక్షన్ 90: పోలవరం ప్రాజెక్టును జాతీయ ప్రాజెక్టుగా ప్రకటన\n"
                        "• సెక్షన్ 94: రాజధాని అమరావతి మౌలిక సదుపాయాలకు ప్రత్యేక ఆర్థిక సాయం\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/ap_reorganisation_act_master_guide.pdf\n\n"
                        "🌐 <b>వెబ్ గైడ్ & 50 ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/ap_bifurcation_guide"
                    )
                    send_telegram_message(bf_msg, token=token, chat_id=chat_id)

                elif text == "/amendments" or text == "/judgments":
                    am_msg = (
                        "⚖️ <b>భారత రాజ్యాంగ సవరణలు (1-106) & ల్యాండ్‌మార్క్ సుప్రీంకోర్టు తీర్పులు</b>\n"
                        "───────────────────────\n\n"
                        "📜 <b>కీలక రాజ్యాంగ సవరణలు:</b>\n"
                        "• 42వ సవరణ (1976): మినీ కాన్‌స్టిట్యూషన్ (పీఠికలో సోషలిస్ట్, సెక్యులర్, ఇంటిగ్రిటీ; ప్రాథమిక విధులు)\n"
                        "• 44వ సవరణ (1978): ఆస్తి హక్కు లీగల్ రైట్ (300A), అంతర్గత అల్లర్ల స్థానంలో సాయుధ తిరుగుబాటు\n"
                        "• 73 & 74వ సవరణలు (1992): పంచాయతీ రాజ్ (11వ షెడ్యూల్), మున్సిపాలిటీలు (12వ షెడ్యూల్)\n"
                        "• 101వ సవరణ (2016): జీఎస్టీ (GST) అమలు\n"
                        "• 103వ సవరణ (2019): EWS 10% రిజర్వేషన్లు (ఆర్టికల్ 15(6), 16(6))\n"
                        "• 106వ సవరణ (2023): నారీ శక్తి వందన్ అధినియం (మహిళలకు 33% రిజర్వేషన్)\n\n"
                        "🏛️ <b>20 చారిత్రాత్మక తీర్పులు:</b>\n"
                        "• కేశవానంద భారతి (1973): మూలతత్వ సిద్ధాంతం (Basic Structure Doctrine)\n"
                        "• మేనకా గాంధీ (1978): డ్యూ ప్రాసెస్ ఆఫ్ లా (ఆర్టికల్ 21 విస్తరణ)\n"
                        "• ఇందిరా సహానీ (1992): 50% రిజర్వేషన్ సీలింగ్ & క్రీమీ లేయర్\n"
                        "• జస్టిస్ పుట్టస్వామి (2017): రైట్ టు ప్రైవసీ ప్రాథమిక హక్కు\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/constitution_amendments_judgments_guide.pdf\n\n"
                        "🌐 <b>వెబ్ గైడ్ & ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/amendments_judgments"
                    )
                    send_telegram_message(am_msg, token=token, chat_id=chat_id)

                elif text == "/weekly" or text == "/weekly_digest":
                    wk_msg = (
                        "🗓️ <b>ఆదివారం వీక్లీ కరెంట్ అఫైర్స్ మెగా రివిజన్ & వీక్లీ టెస్ట్</b>\n"
                        "───────────────────────\n\n"
                        "📚 <b>ఈ వారం ముఖ్యాంశాలు:</b>\n"
                        "• వారం మొత్తం టాప్ 56 పరీక్షా ఆధారిత కరెంట్ అఫైర్స్\n"
                        "• 50+ క్విక్ రివిజన్ వన్-లైనర్స్ (One-Liners)\n"
                        "• 50-MCQ ఆదివారం గ్రాండ్ వీక్లీ టెస్ట్\n\n"
                        "🌐 <b>ఆన్‌లైన్‌లో వీక్లీ డైజెస్ట్ చదివి 50 MCQs టెస్ట్ రాయండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/weekly_digest"
                    )
                    send_telegram_message(wk_msg, token=token, chat_id=chat_id)

                elif text == "/matrix" or text == "/schemes_matrix":
                    mx_msg = (
                        "🌾 <b>AP సూపర్ సిక్స్ & TS 6 గ్యారెంటీలు సమగ్ర అర్హతల పోలిక మేట్రిక్స్</b>\n"
                        "───────────────────────\n\n"
                        "📊 <b>పోలిక పారామీటర్లు:</b>\n"
                        "• లబ్ధి మొత్తం (Benefit Amount)\n"
                        "• ఆదాయ పరిమితి (Income Ceiling / తెల్ల రేషన్ కార్డు)\n"
                        "• భూమి పరిమితి (Land Ceiling - మాగాణి / మెట్ట)\n"
                        "• వయో పరిమితి (Age Limit)\n"
                        "• నోడల్ శాఖ & డీబీటీ పోర్టల్ (DBT Portal)\n"
                        "• కేటాయించిన బడ్జెట్ (Budget Outlay)\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ పోలిక టేబుల్ & ఫిల్టర్లు చూడండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/schemes_matrix"
                    )
                    send_telegram_message(mx_msg, token=token, chat_id=chat_id)

                elif text == "/articles" or text == "/polity_articles":
                    art_msg = (
                        "🏛️ <b>భారత రాజ్యాంగ ఆర్టికల్స్ (1-395) మాస్టర్ డైరెక్టరీ & రివిజన్ హబ్</b>\n"
                        "───────────────────────\n\n"
                        "📜 <b>కీలక భాగాలు & ఆర్టికల్స్:</b>\n"
                        "• భాగం I (1-4): యూనియన్ & భూభాగం (ఆర్టికల్ 1-4)\n"
                        "• భాగం III (12-35): ప్రాథమిక హక్కులు (ఆర్టికల్ 14, 19, 21, 32 రిట్స్)\n"
                        "• భాగం IV (36-51): ఆదేశిక సూత్రాలు (DPSP - 40 పంచాయతీ, 44 UCC, 48A పర్యావరణం)\n"
                        "• భాగం IV-A (51A): 11 ప్రాథమిక విధులు\n"
                        "• భాగం V (52-151): కేంద్ర కార్యనిర్వాహక వర్గం, రాష్ట్రపతి (52-72), సుప్రీంకోర్టు (124-147)\n"
                        "• భాగం XVIII (352-360): జాతీయ, రాష్ట్రపతి పాలన, ఆర్థిక ఎమర్జెన్సీలు\n"
                        "• భాగం XX (368): రాజ్యాంగ సవరణ ప్రక్రియ\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/indian_polity_articles_master_guide.pdf\n\n"
                        "🌐 <b>ఫాస్ట్-సెర్చ్ డైరెక్టరీ & ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/polity_articles"
                    )
                    send_telegram_message(art_msg, token=token, chat_id=chat_id)

                elif text == "/scitech" or text == "/science_tech" or text == "/defense":
                    st_msg = (
                        "🛰️ <b>సైన్స్, టెక్నాలజీ & రక్షణ రంగం 2025–2026 మెగా హబ్</b>\n"
                        "───────────────────────\n\n"
                        "🚀 <b>ఇస్రో & అంతరిక్ష పరిశోధనలు:</b>\n"
                        "• గగన్‌యాన్ మానవ సహిత యాత్ర & వ్యోమమిత్ర రోబోట్ (HLVM3)\n"
                        "• చంద్రయాన్-4 (శాంపిల్ రిటర్న్) & శుక్రయాన్-1 (VOM 2028)\n"
                        "• భారతీయ అంతరిక్ష స్టేషన్ (BAS 2035) & నాసా-ఇస్రో నిసార్ (NISAR)\n\n"
                        "🛡️ <b>రక్షణ & స్వదేశీ పరిజ్ఞానం:</b>\n"
                        "• అగ్ని-5 MIRV టెక్నాలజీ (మిషన్ దివ్యాస్త్ర - ICBM)\n"
                        "• INS అరిఘాట్ SSBN అణు జలాంతర్గామి & జోరావర్ లైట్ ట్యాంక్\n"
                        "• LCA తేజస్ Mk1A & AMCA 5th Gen స్టెల్త్ ఫైటర్ జెట్\n\n"
                        "💻 <b>AI, క్వాంటం & సెమీకండక్టర్లు:</b>\n"
                        "• ఇండియాఏఐ మిషన్ (₹10,372 కోట్లు, 10,000+ GPUs)\n"
                        "• నేషనల్ క్వాంటం మిషన్ (NQM) & ధోలేరా సెమీకండక్టర్ ఫ్యాబ్\n"
                        "• బయోఈ3 పాలసీ (BioE3) & కార్-టి NexCAR19 క్యాన్సర్ థెరపీ\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/science_technology_defense_master.pdf\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ హబ్ & ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/science_tech_hub"
                    )
                    send_telegram_message(st_msg, token=token, chat_id=chat_id)

                elif text == "/environment" or text == "/biodiversity":
                    env_msg = (
                        "🌍 <b>పర్యావరణం, జీవవైవిధ్యం & క్లైమేట్ చేంజ్ మాస్టర్ నిధి</b>\n"
                        "───────────────────────\n\n"
                        "🌐 <b>వాతావరణ సదస్సులు & లక్ష్యాలు:</b>\n"
                        "• బాకూ COP29 & $300 బిలియన్ల NCQG క్లైమేట్ ఫైనాన్స్\n"
                        "• కున్మింగ్-మాంట్రియల్ 30x30 గ్లోబల్ బయోడైవర్సిటీ లక్ష్యం\n"
                        "• భారత పంచామృత ప్రతిజ్ఞలు & 2070 నెట్-జీరో కార్యాచరణ\n\n"
                        "🐅 <b>వన్యప్రాణి ప్రాజెక్టులు & రిజర్వ్‌లు:</b>\n"
                        "• ప్రాజెక్ట్ టైగర్ 50 ఏళ్లు (భారత్‌లో 3,682 పులులు, MP టైగర్ స్టేట్)\n"
                        "• ప్రాజెక్ట్ చీతా (కునో & గాంధీ సాగర్) & గజరాజ్ AI వ్యవస్థ\n"
                        "• భారతదేశంలో 85 రామ్‌సార్ చిత్తడి నేలలు (AP కొల్లేరు)\n"
                        "• సుప్రీంకోర్టు క్లైమేట్ జస్టిస్ ప్రాథమిక హక్కు తీర్పు (ఆర్టికల్ 14 & 21)\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/environment_biodiversity_master.pdf\n\n"
                        "🌐 <b>వెబ్ కాంపెండియం & ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/environment_hub"
                    )
                    send_telegram_message(env_msg, token=token, chat_id=chat_id)

                elif text == "/centralschemes" or text == "/schemes2026":
                    cs_msg = (
                        "💰 <b>కేంద్ర ప్రభుత్వ ప్రతిష్టాత్మక పథకాలు 2026 మాస్టర్ హ్యాండ్‌బుక్</b>\n"
                        "───────────────────────\n\n"
                        "🌟 <b>కీలక ఫ్లాగ్‌షిప్ పథకాలు & తాజా బడ్జెట్ నవీకరణలు:</b>\n"
                        "• పీఎం సూర్య ఘర్: 1 కోటి ఇళ్లకు 300 యూనిట్లు ఉచిత విద్యుత్ (₹78,000 సబ్సిడీ)\n"
                        "• ఆయుష్మాన్ భారత్ PMJAY: 70+ వయసున్న వృద్ధులందరికీ ఉచితంగా ₹5 లక్షల వార్షిక హెల్త్ కవర్\n"
                        "• పీఎం విశ్వకర్మ: 18 సాంప్రదాయ చేతివృత్తుల శ్రామికులకు ₹15,000 టూల్‌కిట్ & రాయితీ రుణాలు\n"
                        "• లఖ్‌పతీ దీదీ: 3 కోట్ల గ్రామీణ SHG మహిళలకు లక్ష రూపాయల వార్షిక ఆదాయం\n"
                        "• పీఎం ఇంటర్న్‌షిప్ స్కీమ్: టాప్ 500 కంపెనీలలో ₹5,000 స్టైఫండ్‌తో కోటి మంది యువతకు శిక్షణ\n"
                        "• PM-KISAN (₹6,000/సం.), PMFBY పంట బీమా, జల్ జీవన్ మిషన్ (55 lpcd)\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/central_government_schemes_master.pdf\n\n"
                        "🌐 <b>సమగ్ర హ్యాండ్‌బుక్ & ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/central_schemes"
                    )
                    send_telegram_message(cs_msg, token=token, chat_id=chat_id)

                elif text == "/society" or text == "/indiansociety":
                    soc_msg = (
                        "👥 <b>భారతీయ సమాజం (Indian Society - 30 మార్కులు) సమగ్ర మాస్టర్ హబ్</b>\n"
                        "───────────────────────\n\n"
                        "📚 <b>3 యూనిట్ల సిలబస్ ముఖ్యాంశాలు:</b>\n"
                        "1. <b>సామాజిక నిర్మాణం:</b> కుటుంబం, వివాహం, బంధుత్వం, కులం (సంస్కృతీకరణ), 75 PVTGs తెగలు, మహిళల హోదా\n"
                        "2. <b>సామాజిక సమస్యలు:</b> కులతత్వం, మతతత్వం, పేదరికం (టెండూల్కర్, MPI), బాలకార్మికులు, గృహహింస, POCSO\n"
                        "3. <b>సంక్షేమ చట్టాలు:</b> రాజ్యాంగ రక్షణలు (15, 16, 17, 330, 338), SC/ST అట్రాసిటీల చట్టం, PESA 1996, FRA 2006, RPwD 2016, PM-JANMAN\n\n"
                        "📥 <b>మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/indian_society_master_compendium.pdf\n\n"
                        "🌐 <b>వెబ్ హబ్ & 20 ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/indian_society_hub"
                    )
                    send_telegram_message(soc_msg, token=token, chat_id=chat_id)

                elif text == "/planner" or text == "/study_planner":
                    pln_msg = (
                        "📅 <b>60 రోజుల స్మార్ట్ డైలీ స్టడీ ప్లానర్ & సిలబస్ ట్రాకర్ (2026)</b>\n"
                        "───────────────────────\n\n"
                        "🎯 <b>9 వారాల మైక్రో-షెడ్యూల్:</b>\n"
                        "• వారం 1-2 (D1–12): భారత & ఆంధ్రప్రదేశ్ చరిత్ర\n"
                        "• వారం 3-4 (D13–24): భౌగోళికం (26 జిల్లాలు), విపత్తులు & పర్యావరణం\n"
                        "• వారం 5-6 (D25–36): భారతీయ సమాజం & సంక్షేమ చట్టాలు\n"
                        "• వారం 7-8 (D37–48): మెంటల్ ఎబిలిటీ, లాజిక్ & 120 షార్ట్‌కట్స్\n"
                        "• వారం 9 (D49–60): కరెంట్ అఫైర్స్ రివిజన్ & గ్రాండ్ మాక్ టెస్టులు\n\n"
                        "🌐 <b>మీ రోజువారీ ప్రోగ్రెస్ ట్రాక్ చేయండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/study_planner"
                    )
                    send_telegram_message(pln_msg, token=token, chat_id=chat_id)

                elif text == "/pyqs" or text == "/pyqs_explorer":
                    pyq_msg = (
                        "🔍 <b>APPSC & TSPSC గత ప్రశ్నల (PYQs) డీప్ ఎక్స్‌ప్లోరర్ & అనలిటిక్స్</b>\n"
                        "───────────────────────\n\n"
                        "📊 <b>విశ్లేషణ & ఫిల్టర్లు:</b>\n"
                        "• 2024 గ్రూప్-2 ప్రిలిమ్స్, 2019 స్క్రీనింగ్, TSPSC గ్రూప్-1, పోలీస్ SI పేపర్లు\n"
                        "• సబ్జెక్ట్-వైజ్, పరీక్ష-వైజ్ మరియు ఇయర్-వైజ్ ఫిల్టర్లు\n"
                        "• అధికారిక కటాఫ్ విశ్లేషణ (-0.33 నెగెటివ్ మార్కింగ్ స్ట్రాటజీ)\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ ఎక్స్‌ప్లోరర్‌లో ప్రాక్టీస్ చేయండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pyqs_explorer"
                    )
                    send_telegram_message(pyq_msg, token=token, chat_id=chat_id)

                elif text == "/aptitude" or text == "/shortcuts":
                    apt_msg = (
                        "🧮 <b>మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్ షార్ట్‌కట్ ప్రాక్టీస్ ఇంజిన్</b>\n"
                        "───────────────────────\n\n"
                        "⚡ <b>స్పీడ్ మ్యాథ్స్ & రీజనింగ్ ఫార్ములా డెక్:</b>\n"
                        "• గడియారాలు (θ = |30H - 11/2 M|), క్యాలెండర్లు (ఆడ్ డేస్ ట్రిక్)\n"
                        "• పని-కాలం (LCM ఎఫిషియన్సీ), రైళ్లు & వేగం (5/18 మార్పిడి)\n"
                        "• శాతాలు, లాభనష్టాలు & క్రాస్ అలగేషన్ రూల్\n"
                        "• సాంప్రదాయ పద్ధతి vs ఎగ్జామ్ షార్ట్‌కట్ పద్ధతి పోలికలు\n\n"
                        "📥 <b>120 షార్ట్‌కట్స్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/quantitative_aptitude_120_shortcuts.pdf\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ హబ్‌లో ప్రాక్టీస్ చేయండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/mental_ability_hub"
                    )
                    send_telegram_message(apt_msg, token=token, chat_id=chat_id)

                elif text == "/audiorevision" or text == "/audio_revision":
                    aud_msg = (
                        "🎧 <b>పర్సనలైజ్డ్ ఆడియో రివిజన్ ప్లేయర్ & పాడ్‌కాస్ట్ హబ్</b>\n"
                        "───────────────────────\n\n"
                        "📻 <b>8 హై-ఈల్డ్ ఆడియో పాడ్‌కాస్ట్ ట్రాక్‌లు:</b>\n"
                        "• డైలీ కరెంట్ అఫైర్స్ టాప్ 10 హెడ్‌లైన్స్ & విశ్లేషణ\n"
                        "• భారత రాజ్యాంగం టాప్ 50 ఆర్టికల్స్ రాపిడ్ రివిజన్\n"
                        "• భారతీయ సమాజం - సామాజిక నిర్మాణం, కుల వ్యవస్థ & PVTGs\n"
                        "• ఆధునిక ఏపీ చరిత్ర & 2014 పునర్విభజన చట్టం సారాంశం\n"
                        "• ఆంధ్రప్రదేశ్ 26 జిల్లాలు, పోర్టులు & సహజ వనరులు\n"
                        "• ఇస్రో 2025-26 మిషన్లు (గగన్‌యాన్, చంద్రయాన్-4) & AI విప్లవం\n"
                        "• బడ్జెట్ 2026 - ఫ్లాగ్‌షిప్ స్కీమ్స్ & సంక్షేమ నిధులు\n"
                        "• 120 ఆప్టిట్యూడ్ షార్ట్‌కట్ సూత్రాలు - సూపర్ ఫాస్ట్ కాలిక్యులేషన్స్\n\n"
                        "🌐 <b>ఆన్‌లైన్ ప్లేయర్‌లో వినండి (కంటిన్యూయస్ ప్లే & స్పీడ్ కంట్రోల్):</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/audio_revision"
                    )
                    send_telegram_message(aud_msg, token=token, chat_id=chat_id)

                elif text == "/mains" or text == "/mains_descriptive" or text == "/mainsportal":
                    mn_msg = (
                        "✍️ <b>APPSC & TSPSC మెయిన్స్ డిస్క్రిప్టివ్ ఆన్సర్ రైటింగ్ పోర్టల్</b>\n"
                        "───────────────────────\n\n"
                        "📝 <b>లక్షణాలు & మోడల్ సమాధానాలు:</b>\n"
                        "• 12 సమగ్ర మోడల్ Q&As (పేపర్ 1, 2, 3, 4)\n"
                        "• 4-స్టెప్ స్ట్రక్చర్: పరిచయం, ముఖ్య విశ్లేషణ, ప్రభుత్వ చర్యలు, ముగింపు\n"
                        "• ఇంటరాక్టివ్ డిజిటల్ రైటింగ్ ప్యాడ్ & రివర్స్ కౌంట్‌డౌన్ టైమర్ (10-15 నిమిషాలు)\n"
                        "• మోడల్ సమాధానంతో సరిపోల్చుకునే డ్యూయల్ వ్యూ & స్వీయ మూల్యాంకన రూబ్రిక్\n\n"
                        "📥 <b>మెయిన్స్ మాస్టర్ హ్యాండ్‌బుక్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/appsc_mains_answer_writing_handbook.pdf\n\n"
                        "🌐 <b>ఆన్‌లైన్ డిజిటల్ ప్యాడ్‌లో ప్రాక్టీస్ చేయండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/mains_descriptive_portal"
                    )
                    send_telegram_message(mn_msg, token=token, chat_id=chat_id)

                elif text == "/analytics" or text == "/student_analytics":
                    ana_msg = (
                        "📊 <b>విద్యార్థి పెర్ఫార్మెన్స్ అనలిటిక్స్ & వీక్‌నెస్ డయాగ్నోజర్</b>\n"
                        "───────────────────────\n\n"
                        "🎯 <b>స్మార్ట్ డయాగ్నోసిస్ విశేషాలు:</b>\n"
                        "• 150 మార్కులకు అంచనా వేసిన ప్రిలిమ్స్ స్కోరు & ఆక్యురసీ రేట్\n"
                        "• 2024 అఫీషియల్ కటాఫ్ (92.00) vs స్కోర్ గ్యాప్ బారోమీటర్\n"
                        "• 5 కోర్ సబ్జెక్టుల వారీగా బలం vs బలహీనత (Weakness Alerts)\n"
                        "• నెగెటివ్ మార్కింగ్ (-0.33) తగ్గించే టార్గెటెడ్ సబ్జెక్ట్ సూచనలు\n\n"
                        "🌐 <b>మీ వ్యక్తిగత పెర్ఫార్మెన్స్ స్కోర్‌కార్డ్ చూడండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/student_analytics"
                    )
                    send_telegram_message(ana_msg, token=token, chat_id=chat_id)

                elif text == "/staticgk" or text == "/gk" or text == "/static_gk":
                    gk_msg = (
                        "🇮🇳 <b>స్టాటిక్ జీకే సూపర్-ఫాస్ట్ మాస్టర్ పాకెట్‌బుక్ 2026</b>\n"
                        "───────────────────────\n\n"
                        "⚡ <b>8 కోర్ విభాగాలు (Ultra-High Yield):</b>\n"
                        "• భారతదేశం & ఆంధ్రప్రదేశ్ లో ప్రథములు (రాష్ట్రపతులు, సీఎంలు, అవార్డులు)\n"
                        "• జాతీయ పార్కులు, టైగర్ రిజర్వులు & కొల్లేరు రామ్‌సర్ సైట్\n"
                        "• ప్రముఖ ఆనకట్టలు, నదీ ప్రాజెక్టులు & పోలవరం, ధవళేశ్వరం\n"
                        "• అణు విద్యుత్ కేంద్రాలు, ఇస్రో షార్ (SHAR), BARC & CCMB\n"
                        "• మేజర్ పోర్టులు (విశాఖపట్నం సహా) & విమానాశ్రయాలు\n"
                        "• యునెస్కో ప్రపంచ వారసత్వ ప్రదేశాలు (43 సైట్లు) & ఆలయాలు\n"
                        "• 8 శాస్త్రీయ నృత్యాలు (కూచిపూడి) & సాంస్కృతిక ఉత్సవాలు\n"
                        "• ఐక్యరాజ్యసమితి, డబ్ల్యూహెచ్‌ఓ, ఐఎంఎఫ్, వరల్డ్ బ్యాంక్ ప్రధాన కార్యాలయాలు\n\n"
                        "📥 <b>మాస్టర్ పాకెట్‌బుక్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/static_gk_master_pocketbook.pdf\n\n"
                        "🌐 <b>రాపిడ్ సెర్చ్ పాకెట్‌బుక్ హబ్:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/static_gk_pocketbook"
                    )
                    send_telegram_message(gk_msg, token=token, chat_id=chat_id)

                elif text == "/atlas" or text == "/map_atlas":
                    atlas_msg = (
                        "🗺️ <b>మ్యాప్ పాయింటింగ్ మాస్టర్ అట్లాస్ & చీట్-షీట్ 2026</b>\n"
                        "───────────────────────\n\n"
                        "📍 <b>హై-స్కోరింగ్ లొకేషన్లు (AP, భారతదేశం, ప్రపంచం):</b>\n"
                        "• AP: పోలవరం, అమరావతి, ఆర్మాకొండ (1680m), పులికాట్ & కొల్లేరు, శ్రీహరికోట, జిందగడ\n"
                        "• భారతదేశం: పిర్ పంజాల్, జోజిలా, డెక్కన్ ట్రాప్స్, ఇందిరా పాయింట్, కాజిరంగా, సైలెంట్ వ్యాలీ\n"
                        "• ప్రపంచం: బాబ్-ఎల్-మండేబ్, హార్ముజ్ జలసంధి, సూయజ్ కాలువ, తైవాన్ జలసంధి, మలక్కా\n"
                        "• APPSC PYQs లింకేజ్ & పరీక్షల ప్రాధాన్యత విశ్లేషణ\n\n"
                        "📥 <b>మ్యాప్ పాయింటింగ్ మాస్టర్ అట్లాస్ PDF డౌన్‌లోడ్ చేసుకోండి (1.93 MB):</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/map_pointing_master_atlas.pdf\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ అట్లాస్ వెబ్ పోర్టల్:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/map_pointing_atlas"
                    )
                    send_telegram_message(atlas_msg, token=token, chat_id=chat_id)

                elif text == "/judgments" or text == "/sc_judgments":
                    judg_msg = (
                        "⚖️ <b>భారత సుప్రీంకోర్టు 30 చారిత్రక తీర్పులు (1950–2026)</b>\n"
                        "───────────────────────\n\n"
                        "🏛️ <b>కీలక ల్యాండ్‌మార్క్ తీర్పులు & బెంచ్ వివరాలు:</b>\n"
                        "• కేశవానంద భారతి (1973): రాజ్యాంగ మౌలిక స్వరూప సిద్ధాంతం (13గురు జడ్జిలు, 7:6)\n"
                        "• మేనకా గాంధీ (1978): డ్యూ ప్రాసెస్ ఆఫ్ లా, స్వర్ణ త్రయం (14, 19, 21)\n"
                        "• ఇందిరా సహానీ (1992): 27% OBC కోటా, 50% సీలింగ్, క్రీమీ లేయర్\n"
                        "• ఎస్.ఆర్. బొమ్మై (1994): ఆర్టికల్ 356 నియంత్రణ, లౌకికతత్వం, ఫ్లోర్ టెస్ట్\n"
                        "• పుట్టస్వామి (2017): గోప్యతా హక్కు (Right to Privacy) ఆర్టికల్ 21 కింద ప్రాథమిక హక్కు\n"
                        "• 2024 తీర్పులు: SC/ST ఉపవర్గీకరణ తీర్పు & ఎలక్టోరల్ బాండ్ల రద్దు తీర్పు\n\n"
                        "📥 <b>30 ల్యాండ్‌మార్క్ తీర్పుల మాస్టర్ హ్యాండ్‌బుక్ PDF:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/supreme_court_landmark_cases_handbook.pdf\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ జడ్జిమెంట్స్ హబ్ & 30 MCQs ప్రాక్టీస్:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/sc_judgments_hub"
                    )
                    send_telegram_message(judg_msg, token=token, chat_id=chat_id)

                elif text == "/paper2" or text == "/group2_paper2":
                    p2_msg = (
                        "🎯 <b>APPSC Group-2 పేపర్-2 (150 Marks) మెగా మెయిన్స్ పోర్టల్</b>\n"
                        "───────────────────────\n\n"
                        "📊 <b>సమగ్ర సిలబస్ & 150 మార్కుల వెయిటేజీ:</b>\n"
                        "• సెక్షన్ A (75M): ఆంధ్రప్రదేశ్ సామాజిక & సాంస్కృతిక చరిత్ర (5 యూనిట్లు)\n"
                        "• సెక్షన్ B (75M): భారత రాజ్యాంగం మరియు పరిపాలన ఓవర్‌వ్యూ (5 యూనిట్లు)\n\n"
                        "⏱️ <b>రియల్ CBT / OMR ఎగ్జామ్ సిమ్యులేటర్:</b>\n"
                        "• 150 నిమిషాల కౌంట్‌డౌన్ టైమర్\n"
                        "• APPSC అఫీషియల్ మార్కింగ్ స్కీమ్ (+1 సరైనది, -0.33 తప్పు)\n"
                        "• సెక్షన్ల వారీగా విశ్లేషణ, ఆక్యురసీ రేట్ & స్టేట్ బ్రాకెట్ ప్రిడిక్టర్\n"
                        "• 10 యూనిట్ల సమగ్ర తెలుగు రివిజన్ నోట్స్\n\n"
                        "🌐 <b>150-ప్రశ్నల గ్రాండ్ టెస్ట్ రాయడానికి ఇక్కడ క్లిక్ చేయండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/group2_paper2_master"
                    )
                    send_telegram_message(p2_msg, token=token, chat_id=chat_id)

                elif text == "/agri" or text == "/agri_irrigation":
                    agri_msg = (
                        "🌾 <b>ఆంధ్రప్రదేశ్ & తెలంగాణ వ్యవసాయం, సాగునీరు & ఆక్వాకల్చర్ మాస్టర్ గైడ్</b>\n"
                        "───────────────────────\n\n"
                        "🌿 <b>సిలబస్ ముఖ్య ముఖ్యాంశాలు:</b>\n"
                        "• ప్రధాన పంటలు, ఉత్పత్తి రికార్డులు & MSP 2025-26 ధరలు\n"
                        "• పోలవరం జాతీయ ప్రాజెక్ట్ (సెక్షన్ 90), ధవళేశ్వరం, ప్రకాశం బ్యారేజ్ & నాగార్జున సాగర్\n"
                        "• అంతర్రాష్ట్ర నదీ జల వివాదాలు (ఆర్టికల్ 262, బచావత్ & బ్రిజేష్ కుమార్ ట్రిబ్యునళ్లు)\n"
                        "• ఉద్యానవన పంటల్లో ఏపీ 1వ స్థానం & బ్లూ ఎకానమీ (ఆక్వా రొయ్యల ఎగుమతుల్లో 40% వాటా)\n"
                        "• 20వ పశుగణన, ఒంగోలు జాతి పశువులు & శ్వేత విప్లవం\n\n"
                        "📥 <b>వ్యవసాయం & సాగునీరు మాస్టర్ PDF డౌన్‌లోడ్ చేసుకోండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/ap_ts_agriculture_irrigation_master.pdf\n\n"
                        "🌐 <b>వెబ్ హబ్ & 12 ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/agri_irrigation_hub"
                    )
                    send_telegram_message(agri_msg, token=token, chat_id=chat_id)

                elif text == "/awards" or text == "/sports" or text == "/awards_sports":
                    aw_msg = (
                        "🏆 <b>అవార్డులు, క్రీడలు & ప్రముఖ వ్యక్తులు 2025–2026 మెగా డైజెస్ట్</b>\n"
                        "───────────────────────\n\n"
                        "🎖️ <b>హై-యీల్డ్ కంపైలేషన్:</b>\n"
                        "• భారతరత్న 2024 (పీవీ నరసింహారావు, ఎం.ఎస్. స్వామినాథన్, కర్పూరీ ఠాకూర్ తదితరులు)\n"
                        "• పద్మవిభూషణ్ (కొణిదెల చిరంజీవి, ఎం. వెంకయ్య నాయుడు)\n"
                        "• నోబెల్ బహుమతులు 2024–25 (AI న్యూరల్ నెట్స్, AlphaFold, microRNA, హాన్ కాంగ్)\n"
                        "• పారిస్ ఒలింపిక్స్ (నీరజ్ రజతం, మను భాకర్ డబుల్ కాంస్యం) & పారాలింపిక్స్ 29 పతకాలు\n"
                        "• 45వ చెస్ ఒలింపియాడ్ డబుల్ గోల్డ్ (డి. గుకేష్, అర్జున్ ఎరిగైసి 2800+ రేటింగ్)\n"
                        "• 51వ CJI సంజీవ్ ఖన్నా, 16వ ఆర్థిక సంఘం చైర్మన్ అరవింద్ పనగరియా, కాగ్ సంజయ్ మూర్తి\n\n"
                        "📥 <b>అవార్డులు & క్రీడలు మాస్టర్ డైజెస్ట్ PDF:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/awards_sports_personalities_2026.pdf\n\n"
                        "🌐 <b>ఇంటరాక్టివ్ హబ్ & 30 ప్రాక్టీస్ MCQs:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/awards_sports_hub"
                    )
                    send_telegram_message(aw_msg, token=token, chat_id=chat_id)

                elif text == "/group1" or text == "/group1_prelims":
                    g1_msg = (
                        "🎯 <b>APPSC Group-1 ప్రిలిమ్స్ (240 Marks) మెగా గ్రాండ్ సిమ్యులేటర్</b>\n"
                        "───────────────────────\n\n"
                        "📝 <b>డ్యూయల్ పేపర్ ఎగ్జామ్ స్ట్రక్చర్:</b>\n"
                        "• పేపర్-1: జనరల్ స్టడీస్ (120 ప్రశ్నలు - 120 మార్కులు)\n"
                        "• పేపర్-2: జనరల్ ఆప్టిట్యూడ్ & సైన్స్ (120 ప్రశ్నలు - 120 మార్కులు)\n"
                        "• నెగెటివ్ మార్కింగ్: ప్రతి తప్పు ప్రశ్నకు -0.33 మార్కులు\n\n"
                        "⏱️ <b>సిమ్యులేటర్ ఫీచర్లు:</b>\n"
                        "• రియల్-టైమ్ కౌంట్‌డౌన్ టైమర్ & క్వశ్చన్ ప్యాలెట్ (1-120 బటన్స్)\n"
                        "• తక్షణ ఆటో-ఇవాల్యుయేషన్ & కటాఫ్ బారోమీటర్\n"
                        "• 8 యూనిట్ల సమగ్ర తెలుగు రివిజన్ నోట్స్\n"
                        "• ప్రతి ప్రశ్నకు సమగ్ర తెలుగు సమాధానాల వివరణలు\n\n"
                        "🌐 <b>ఇప్పుడే 240 మార్కుల గ్రాండ్ టెస్ట్ ప్రారంభించండి:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/group1_prelims_master"
                    )
                    send_telegram_message(g1_msg, token=token, chat_id=chat_id)

                elif text == "/tribal" or text == "/tribal_heritage" or text == "/pesa":
                    tr_msg = (
                        "📜 <b>ఆంధ్రప్రదేశ్ & తెలంగాణ గిరిజన సంస్కృతి, PVTGs & PESA హ్యాండ్‌బుక్</b>\n"
                        "───────────────────────\n\n"
                        "🏕️ <b>కోర్ అంశాల విశ్లేషణ:</b>\n"
                        "• ఏపీలోని 7 PVTGs: చెంచు, కొండరెడ్డి, కొండసవర, గడబ, పోర్జ, తోటి, ఖోండ్\n"
                        "• గిరిజన జాతరలు: మేడారం సమ్మక్క-సారలమ్మ, నాగోబా, తీజ్, సీత్లా భవానీ\n"
                        "• సంప్రదాయ కళలు: గుస్సాడి (పద్మశ్రీ కనకరాజు), ధింసా, కొమ్ము కోయ, ఇడితల్ చిత్రకళ\n"
                        "• రాజ్యాంగ రక్షణలు: 5వ షెడ్యూల్ (ఆర్టికల్ 244(1)), ట్రైబ్స్ అడ్వైజరీ కౌన్సిల్ (TAC)\n"
                        "• శాసనాలు & తీర్పులు: భూరియా కమిటీ, PESA చట్టం 1996, FRA 2006 & చారిత్రక సమత కేసు (1997)\n\n"
                        "📥 <b>గిరిజన సంస్కృతి & PESA హ్యాండ్‌బుక్ PDF:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/pdfs/ap_ts_tribal_heritage_pesa_handbook.pdf\n\n"
                        "🌐 <b>వెబ్ హబ్ & 30 మోడల్ MCQs ప్రాక్టీస్:</b>\n"
                        "👉 https://lakshya-telugu-ca.onrender.com/tribal_heritage_hub"
                    )
                    send_telegram_message(tr_msg, token=token, chat_id=chat_id)
            print("\nబోట్ ఆపివేయబడింది.")
            break
        except Exception as e:
            print("Polling Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    start_bot_polling()
