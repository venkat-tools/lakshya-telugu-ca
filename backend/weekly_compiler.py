# -*- coding: utf-8 -*-
"""
Sunday Weekly Current Affairs Compiler & Mega Test Engine.
Aggregates week's top affairs, 50-MCQ Sunday Mega Test, and 50+ one-liners.
"""

from db import get_articles, get_one_liners_by_date, get_quiz_by_date

WEEKLY_EDITIONS = [
    {
        "id": "week_2026_w37",
        "title": "సెప్టెంబర్ 2వ వారం (Sep 08 - Sep 16, 2026) సమగ్ర వీక్లీ రివిజన్ బుక్‌లెట్",
        "dates_range": "2026-09-08 నుండి 2026-09-16 వరకు",
        "lead_story": "రామ్ నాథ్ కొవింద్ కమిటీ నివేదిక & జమిలి ఎన్నికల బిల్లు ముసాయిదా, పోలవరం ₹12,157 కోట్ల నిధుల కార్యాచరణ, చంద్రయాన్-4 ప్రాజెక్ట్.",
        "weekly_stats": {
            "articles_count": 56,
            "one_liners_count": 50,
            "test_questions_count": 50
        }
    }
]

def get_weekly_mega_test_questions():
    from daily_live_test_data import get_live_test_questions
    from subject_tests_data import SUBJECT_TESTS
    from pyqs_master_data import get_all_pyq_questions

    # Combine 50 curated high-yield questions for Sunday Mega Test
    q_list = []
    # 20 from live test pool
    for q in get_live_test_questions():
        q_list.append({
            "id": "wm_" + str(q["id"]),
            "question": q["question"],
            "options": q["options"],
            "key": q["key"],
            "explanation": q["explanation"],
            "subject": q.get("subject", "General Studies")
        })

    # Add from subject tests
    for subj_key, subj_data in SUBJECT_TESTS.items():
        for sq in subj_data["questions"][:6]:
            opts = [sq.get("a", ""), sq.get("b", ""), sq.get("c", ""), sq.get("d", "")]
            q_list.append({
                "id": f"wm_{subj_key}_{sq['id']}",
                "question": sq["question"],
                "options": opts,
                "key": sq.get("correct", "A"),
                "explanation": sq.get("explanation", ""),
                "subject": subj_data["title"]
            })
            if len(q_list) >= 50:
                break
        if len(q_list) >= 50:
            break

    return q_list[:50]

def get_weekly_digest_data():
    edition = WEEKLY_EDITIONS[0]
    questions = get_weekly_mega_test_questions()

    # Get sample articles & one-liners from DB or fallback
    try:
        articles = get_articles()[:15]
    except Exception:
        articles = []

    return {
        "edition": edition,
        "questions": questions,
        "articles": articles
    }
