import requests
from telegram_bot import load_config, send_telegram_message
from db import get_articles, get_one_liners_by_date

config = load_config()
token = config.get("bot_token")
chat_id = config.get("chat_id")

articles = get_articles(date="2026-09-12")
ols = get_one_liners_by_date(date="2026-09-12")

print("Articles count for 2026-09-12:", len(articles))
print("One-liners count for 2026-09-12:", len(ols))

msg = "🎯 <b>పోటీ పరీక్షల డైలీ కరెంట్ అఫైర్స్ నోటిఫికేషన్</b>\n"
msg += "📅 <b>తేదీ: 2026-09-12</b>\n"
msg += "───────────────────────\n\n"

msg += "📰 <b>నేటి ప్రధాన ముఖ్యాంశాలు:</b>\n"
for idx, art in enumerate(articles[:5], 1):
    t = art['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    s = art['summary'][:180].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    msg += f"\n<b>{idx}. {t}</b>\n👉 {s}...\n"
    if art.get("exam_relevance"):
        er = art['exam_relevance'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        msg += f"<i>🎯 పరీక్ష ప్రాముఖ్యత: {er}</i>\n"

if ols:
    msg += "\n\n⚡ <b>ఒక వరుస ముఖ్యాంశాలు (Quick Revision):</b>\n"
    for idx, ol in enumerate(ols[:6], 1):
        p = ol['point'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        msg += f"• {p}\n"

msg += "\n📱 <b>మొబైల్ యాప్ లింక్ (4G/5G):</b> https://tinyurl.com/lakshya-telugu-2026\n"
msg += "🌐 <i>డెస్క్‌టాప్ డ్యాష్‌బోర్డ్: http://localhost:5000</i>"

print("Message length:", len(msg))

res = send_telegram_message(msg, token=token, chat_id=chat_id)
print("Send result:", res)
