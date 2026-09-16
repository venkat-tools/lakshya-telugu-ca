# -*- coding: utf-8 -*-
"""
Leaderboard and Test Evaluation Manager for Daily Live Timed Mock Test.
Calculates +1.0 for correct, -0.33 for wrong, and maintains rank & percentiles.
"""

import json
import os
import uuid
from datetime import datetime
from daily_live_test_data import get_live_test_questions

DATA_FILE = os.path.join(os.path.dirname(__file__), "leaderboard_data.json")

DEFAULT_BENCHMARKS = [
    {"id": "bm_01", "name": "సురేష్ కుమార్ రెడ్డి", "district": "తిరుపతి", "target_exam": "APPSC Group 2", "attempted": 20, "correct": 19, "wrong": 1, "net_score": 18.67, "accuracy": 95.0, "time_spent": "10:15", "date": "2026-09-16"},
    {"id": "bm_02", "name": "కె. భవ్యశ్రీ", "district": "విశాఖపట్నం", "target_exam": "APPSC Group 1", "attempted": 20, "correct": 18, "wrong": 2, "net_score": 17.34, "accuracy": 90.0, "time_spent": "11:04", "date": "2026-09-16"},
    {"id": "bm_03", "name": "ఎం. నరేష్ గౌడ్", "district": "హైదరాబాద్", "target_exam": "TSPSC Group 2", "attempted": 19, "correct": 17, "wrong": 2, "net_score": 16.34, "accuracy": 89.5, "time_spent": "12:20", "date": "2026-09-16"},
    {"id": "bm_04", "name": "పి. లావణ్య", "district": "గుంటూరు", "target_exam": "APPSC Group 2", "attempted": 19, "correct": 16, "wrong": 3, "net_score": 15.01, "accuracy": 84.2, "time_spent": "12:55", "date": "2026-09-16"},
    {"id": "bm_05", "name": "వి. సాయి కృష్ణ", "district": "వరంగల్", "target_exam": "TSPSC Group 1", "attempted": 18, "correct": 15, "wrong": 3, "net_score": 14.01, "accuracy": 83.3, "time_spent": "13:40", "date": "2026-09-16"},
    {"id": "bm_06", "name": "డి. రాధాకృష్ణ", "district": "కృష్ణా", "target_exam": "పోలీస్ SI", "attempted": 20, "correct": 15, "wrong": 5, "net_score": 13.35, "accuracy": 75.0, "time_spent": "14:10", "date": "2026-09-16"}
]

def load_leaderboard():
    if not os.path.exists(DATA_FILE):
        save_leaderboard(DEFAULT_BENCHMARKS)
        return DEFAULT_BENCHMARKS
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return DEFAULT_BENCHMARKS

def save_leaderboard(entries):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)

def evaluate_and_submit_test(name, district, target_exam, user_answers, time_spent_str):
    questions = get_live_test_questions()
    q_map = {q["id"]: q for q in questions}

    total_questions = len(questions)
    correct_count = 0
    wrong_count = 0
    unattempted_count = 0

    detailed_review = []
    for q in questions:
        qid = q["id"]
        chosen = user_answers.get(qid)
        correct_key = q["key"].upper()

        if not chosen:
            unattempted_count += 1
            status = "unattempted"
        elif chosen.upper() == correct_key:
            correct_count += 1
            status = "correct"
        else:
            wrong_count += 1
            status = "wrong"

        detailed_review.append({
            "id": qid,
            "question": q["question"],
            "options": q["options"],
            "chosen": chosen,
            "correct_key": correct_key,
            "status": status,
            "explanation": q["explanation"],
            "subject": q.get("subject", "General Studies")
        })

    # Net score with -0.33 negative marking
    raw_score = correct_count * 1.0
    penalty = wrong_count * 0.33
    net_score = round(max(0.0, raw_score - penalty), 2)
    attempted_count = correct_count + wrong_count
    accuracy = round((correct_count / attempted_count * 100), 1) if attempted_count > 0 else 0.0

    entry = {
        "id": "live_" + str(uuid.uuid4())[:8],
        "name": name.strip() or "పరీక్షార్థి",
        "district": district.strip() or "ఆంధ్రప్రదేశ్",
        "target_exam": target_exam.strip() or "APPSC Group 2",
        "attempted": attempted_count,
        "correct": correct_count,
        "wrong": wrong_count,
        "net_score": net_score,
        "accuracy": accuracy,
        "time_spent": time_spent_str or "15:00",
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    leaderboard = load_leaderboard()
    leaderboard.append(entry)
    # Sort by net_score descending, then time
    leaderboard.sort(key=lambda x: x["net_score"], reverse=True)
    save_leaderboard(leaderboard)

    # Determine rank
    rank = 1
    for idx, e in enumerate(leaderboard, 1):
        if e["id"] == entry["id"]:
            rank = idx
            break

    total_participants = len(leaderboard)
    percentile = round(((total_participants - rank) / total_participants) * 100, 1) if total_participants > 1 else 100.0

    return {
        "success": True,
        "scorecard": {
            "name": entry["name"],
            "district": entry["district"],
            "target_exam": entry["target_exam"],
            "total_questions": total_questions,
            "attempted": attempted_count,
            "correct": correct_count,
            "wrong": wrong_count,
            "unattempted": unattempted_count,
            "net_score": net_score,
            "accuracy": accuracy,
            "time_spent": entry["time_spent"],
            "rank": rank,
            "total_candidates": total_participants,
            "percentile": percentile
        },
        "review": detailed_review
    }

def get_top_leaderboard_entries(limit=50):
    board = load_leaderboard()
    board.sort(key=lambda x: x["net_score"], reverse=True)
    return board[:limit]
