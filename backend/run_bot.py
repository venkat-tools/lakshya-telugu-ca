# -*- coding: utf-8 -*-
"""
Standalone Telegram Bot Service for Telugu Current Affairs.
Listens for user commands: /start, /today, /quiz, /oneliners, /help
"""

import time
import requests
import sys
from datetime import datetime
from telegram_bot import load_config, broadcast_daily_digest, send_telegram_message, send_telegram_quiz_poll
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
                if not msg or "text" not in msg:
                    continue

                chat_id = msg["chat"]["id"]
                text = msg["text"].strip()
                user_name = msg.get("from", {}).get("first_name", "మిత్రమా")

                dates = get_available_dates()
                today_date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")

                if text == "/start" or text == "/help":
                    welcome = (
                        f"నమస్కారం {user_name}! 🙏\n\n"
                        f"🎯 <b>లక్ష్య తెలుగు డైలీ కరెంట్ అఫైర్స్ & ఈ-పేపర్ బోట్</b>కు స్వాగతం!\n"
                        f"(APPSC, TSPSC, UPSC, SSC, Banking Special)\n\n"
                        f"📋 <b>కమాండ్స్:</b>\n"
                        f"👉 <b>/history</b> - AP చరిత్ర & గ్రూప్స్ 1, 2, 3 గ్రాండ్ టెస్ట్ 🏛️\n"
                        f"👉 <b>/schemes</b> - సంక్షేమ పథకాలు 2026 (సూపర్ సిక్స్ & 6 గ్యారెంటీలు) 🌾\n"
                        f"👉 <b>/mains</b> - గ్రూప్ 1 & 2 మెయిన్స్ మోడల్ సమాధానాలు ✍️\n"
                        f"👉 <b>/group2</b> లేదా <b>/mock</b> - APPSC గ్రూప్-2 గ్రాండ్ టెస్ట్ (150 Qs) & PYQs 🎯\n"
                        f"👉 <b>/map</b> - మ్యాప్ పాయింటింగ్ అట్లాస్ (AP, India, World) 🗺️\n"
                        f"👉 <b>/epaper</b> లేదా <b>/pdf</b> - నేటి పూర్తి తెలుగు ఈ-పేపర్ PDF (డౌన్‌లోడ్)\n"
                        f"👉 <b>/papers</b> - ఈనాడు, సాక్షి, ఆంధ్రజ్యోతి అధికారిక ఈ-పేపర్స్ లింక్స్\n"
                        f"👉 <b>/today</b> - నేటి 56 ఆర్టికల్స్ ముఖ్యాంశాలు\n"
                        f"👉 <b>/quiz</b> - నేటి 5 ప్రాక్టీస్ క్విజ్ పోల్స్ (MCQs)\n"
                        f"👉 <b>/oneliners</b> - ఒక వరుస ముఖ్యాంశాలు (Quick Revision)\n"
                        f"👉 <b>/mobile</b> - మొబైల్ యాప్ లింక్ (4G/5G TinyURL)\n"
                        f"👉 <b>/all</b> - నేటి మొత్తం డైజెస్ట్ + క్విజ్ + ఈ-పేపర్ PDF పొందండి\n"
                    )
                    send_telegram_message(welcome, token=token, chat_id=chat_id)

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

                elif text == "/epaper" or text == "/pdf":
                    from telegram_bot import send_daily_epaper_pdf, send_epapers_directory
                    send_telegram_message(f"⏳ <b>{today_date} నాటి తెలుగు ఈ-పేపర్ PDF సిద్ధం చేయబడుతోంది...</b>\nదయచేసి ఒక్క క్షణం వేచి ఉండండి.", token=token, chat_id=chat_id)
                    send_daily_epaper_pdf(date=today_date, token=token, chat_id=chat_id)
                    send_epapers_directory(token=token, chat_id=chat_id)

                elif text == "/papers":
                    from telegram_bot import send_epapers_directory
                    send_epapers_directory(token=token, chat_id=chat_id)

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
                    resp += f"\n🌐 <b>మొత్తం {len(articles)} ఆర్టికల్స్ మొబైల్ లో చదవండి:</b> https://lakshya-telugu-ca.onrender.com"
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

                elif text == "/all":
                    broadcast_daily_digest(date=today_date, token=token, chat_id=chat_id)

        except KeyboardInterrupt:
            print("\nబోట్ ఆపివేయబడింది.")
            break
        except Exception as e:
            print("Polling Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    start_bot_polling()
