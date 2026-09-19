# -*- coding: utf-8 -*-
"""
Daily Live CBT Mock Test Data & Scoring Engine.
Generates 20 standard exam questions daily:
- 5 Fresh Daily Current Affairs MCQs for today
- 15 Core General Studies Questions (Polity, History, Geography, Economy, Schemes & Science)
Time Allowed: 15 minutes (900 seconds)
Marking Scheme: +1 for Correct, -0.33 for Wrong, 0 for Unattempted.
"""

import os
import sys
import random
import hashlib
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_today():
    return datetime.now(IST).strftime("%Y-%m-%d")

GS_STATIC_POOL = [
    # Polity
    {
        "id": "pol_1",
        "subject": "భారత రాజ్యాంగం & వ్యవస్థ (Polity)",
        "question": "భారత రాజ్యాంగంలో ప్రాథమిక హక్కుల రక్షకుడు (Guarantor of Fundamental Rights) గా ఎవరిని పేర్కొంటారు?",
        "options": ["A) భారత రాష్ట్రపతి", "B) సుప్రీంకోర్టు మరియు హైకోర్టులు", "C) భారత పార్లమెంట్", "D) ప్రధాన మంత్రి"],
        "correct_option": "B",
        "explanation": "ఆర్టికల్ 32 ప్రకారం సుప్రీంకోర్టు, ఆర్టికల్ 226 ప్రకారం హైకోర్టులు ప్రాథమిక హక్కుల రక్షణ కోసం రిట్‌లను (Writs) జారీ చేసే అధికారాన్ని కలిగి ఉన్నాయి."
    },
    {
        "id": "pol_2",
        "subject": "భారత రాజ్యాంగం & వ్యవస్థ (Polity)",
        "question": "భారత రాజ్యాంగ ప్రవేశికలో సమాజవాద, లౌకిక, సమగ్రత (Socialist, Secular, Integrity) అనే పదాలను ఏ రాజ్యాంగ సవరణ ద్వారా చేర్చారు?",
        "options": ["A) 42వ రాజ్యాంగ సవరణ చట్టం, 1976", "B) 44వ రాజ్యాంగ సవరణ చట్టం, 1978", "C) 52వ రాజ్యాంగ సవరణ చట్టం, 1985", "D) 86వ రాజ్యాంగ సవరణ చట్టం, 2002"],
        "correct_option": "A",
        "explanation": "1976లో ఇందిరాగాంధీ ప్రభుత్వ హయాంలో చేసిన 42వ రాజ్యాంగ సవరణ చట్టం (మినీ కాన్‌స్టిట్యూషన్) ద్వారా ప్రవేశికలో సమాజవాద, లౌకిక, సమగ్రత అనే మూడు పదాలు చేర్చబడ్డాయి."
    },
    {
        "id": "pol_3",
        "subject": "భారత రాజ్యాంగం & వ్యవస్థ (Polity)",
        "question": "పంచాయతీరాజ్ వ్యవస్థకు రాజ్యాంగ ప్రతిపత్తి కల్పించిన 73వ రాజ్యాంగ సవరణ ద్వారా చేర్చబడిన షెడ్యూల్ ఏది?",
        "options": ["A) 9వ షెడ్యూల్", "B) 10వ షెడ్యూల్", "C) 11వ షెడ్యూల్", "D) 12వ షెడ్యూల్"],
        "correct_option": "C",
        "explanation": "73వ సవరణ ద్వారా 11వ షెడ్యూల్‌ను చేర్చారు. ఇందులో పంచాయతీలకు సంబంధించి 29 అధికార విధులు నిర్దేశించబడ్డాయి."
    },
    {
        "id": "pol_4",
        "subject": "భారత రాజ్యాంగం & వ్యవస్థ (Polity)",
        "question": "రాష్ట్రపతిని తొలగించే మహాభియోగ తీర్మానం (Impeachment) ప్రక్రియను రాజ్యాంగంలోని ఏ ఆర్టికల్ నిర్దేశిస్తుంది?",
        "options": ["A) ఆర్టికల్ 52", "B) ఆర్టికల్ 61", "C) ఆర్టికల్ 72", "D) ఆర్టికల్ 123"],
        "correct_option": "B",
        "explanation": "ఆర్టికల్ 61 ప్రకారం రాజ్యాంగ ఉల్లంఘన కారణంతో పార్లమెంట్‌లోని ఏ సభలోనైనా రాష్ట్రపతిపై మహాభియోగ తీర్మానాన్ని ప్రవేశపెట్టవచ్చు."
    },
    {
        "id": "pol_5",
        "subject": "భారత రాజ్యాంగం & వ్యవస్థ (Polity)",
        "question": "కేంద్ర ఎన్నికల కమిషనర్ల నియామక సెలక్షన్ కమిటీలో తాజా చట్టం ప్రకారం సభ్యులు ఎవరు?",
        "options": ["A) ప్రధానమంత్రి, లోక్‌సభ స్పీకర్, హోంమంత్రి", "B) ప్రధానమంత్రి, లోక్‌సభ ప్రతిపక్ష నేత, కేంద్ర కేబినెట్ మంత్రి", "C) సుప్రీంకోర్టు ప్రధాన న్యాయమూర్తి, రాష్ట్రపతి, ఉపరాష్ట్రపతి", "D) కేంద్ర న్యాయశాఖ మంత్రి మరియు అటార్నీ జనరల్"],
        "correct_option": "B",
        "explanation": "నూతన చట్టం ప్రకారం ప్రధాని అధ్యక్షతన ఏర్పడే సెలక్షన్ కమిటీలో ప్రధానమంత్రి, లోక్‌సభలో ప్రతిపక్ష నేత మరియు ప్రధాని నామినేట్ చేసే ఒక కేంద్ర కేబినెట్ మంత్రి ఉంటారు."
    },

    # History
    {
        "id": "hist_1",
        "subject": "భారతీయ చరిత్ర (History)",
        "question": "సింధు లోయ నాగరికత (హరప్పా సంస్కృతి) లో ప్రసిద్ధ మహా స్నానవాటిక (The Great Bath) క్రింది ఏ నగరంలో బయల్పడింది?",
        "options": ["A) హరప్పా", "B) మొహంజొదారో", "C) లోథాల్", "D) కాళీబంగన్"],
        "correct_option": "B",
        "explanation": "సింధు నది ఒడ్డున ఉన్న మొహంజొదారో వద్ద విశాలమైన మహా స్నానవాటిక బయల్పడింది. ఇది నాటి ఇంజనీరింగ్ ప్రతిభకు నిదర్శనం."
    },
    {
        "id": "hist_2",
        "subject": "భారతీయ చరిత్ర (History)",
        "question": "క్రీ.శ. 72 లో నాల్గవ బౌద్ధ సంగీతి (4th Buddhist Council) ఎవరి కాలంలో, ఎక్కడ నిర్వహించబడింది?",
        "options": ["A) అశోకుడు - పాటలీపుత్ర", "B) కాలాశోకుడు - వైశాలి", "C) కనిష్కుడు - కాశ్మీర్ (కుందలవనం)", "D) అజాతశత్రువు - రాజగృహ"],
        "correct_option": "C",
        "explanation": "కుషాను చక్రవర్తి కనిష్కుడి ఆస్థానంలో కాశ్మీర్‌లోని కుందలవనంలో 4వ బౌద్ధ సంగీతి జరిగింది. ఇక్కడే బౌద్ధం మహాయానం, హీనయానంగా చీలింది."
    },
    {
        "id": "hist_3",
        "subject": "భారతీయ చరిత్ర (History)",
        "question": "1857 సిపాయిల తిరుగుబాటు సమయంలో బ్రిటిష్ గవర్నర్ జనరల్ ఎవరు?",
        "options": ["A) లార్డ్ డల్హౌసీ", "B) లార్డ్ కానింగ్", "C) లార్డ్ కర్జన్", "D) లార్డ్ విలియం బెంటింక్"],
        "correct_option": "B",
        "explanation": "1857 ప్రథమ స్వాతంత్ర్య సంగ్రామం సమయంలో లార్డ్ కానింగ్ గవర్నర్ జనరల్‌గా ఉన్నారు. 1858 విక్టోరియా రాణి ప్రకటన తర్వాత ఆయనే తొలి వైస్రాయ్ అయ్యారు."
    },
    {
        "id": "hist_4",
        "subject": "భారతీయ చరిత్ర (History)",
        "question": "విజయనగర సామ్రాజ్యాన్ని సందర్శించిన ప్రముఖ పోర్చుగీస్ యాత్రికుడు డొమింగో పేస్ ఎవరి కాలంలో విజయనగరాన్ని సందర్శించారు?",
        "options": ["A) మొదటి హరిహర రాయలు", "B) ప్రౌఢ దేవరాయలు", "C) శ్రీకృష్ణదేవరాయలు", "D) అళియ రామరాయలు"],
        "correct_option": "C",
        "explanation": "తులువ వంశ చక్రవర్తి శ్రీకృష్ణదేవరాయల పాలనాకాలంలో (1520-22) పోర్చుగీస్ యాత్రికుడు డొమింగో పేస్ విజయనగరాన్ని సందర్శించి రాయల వైభవాన్ని ప్రస్తుతించాడు."
    },
    {
        "id": "hist_5",
        "subject": "భారతీయ చరిత్ర (History)",
        "question": "మౌర్యుల కాలంలో కళింగ యుద్ధం యొక్క భయానకతను, ధర్మవిజయ ఆకాంక్షను వివరించే అశోకుని శాసనం ఏది?",
        "options": ["A) 13వ ప్రధాన శిలాశాసనం", "B) 7వ స్తంభ శాసనం", "C) రుమ్మిన్‌దేయ్ శాసనం", "D) మస్కి శిలాశాసనం"],
        "correct_option": "A",
        "explanation": "అశోకుని 13వ శిలాశాసనం కళింగ యుద్ధ తీవ్రతను మరియు దాని తర్వాత అశోకుడు యుద్ధాన్ని విడనాడి బౌద్ధాన్ని స్వీకరించిన వైనాన్ని వివరిస్తుంది."
    },

    # Economy
    {
        "id": "eco_1",
        "subject": "భారత ఆర్థిక వ్యవస్థ (Economy)",
        "question": "భారత రిజర్వ్ బ్యాంక్ (RBI) ద్రవ్య విధాన కమిటీ (Monetary Policy Committee - MPC) లో మొత్తం ఎంతమంది సభ్యులు ఉంటారు?",
        "options": ["A) 4 గురు", "B) 5 గురు", "C) 6 గురు", "D) 8 మంది"],
        "correct_option": "C",
        "explanation": "ఆర్బీఐ ఎంపీసీలో మొత్తం 6 మంది ఉంటారు (3 ఆర్బీఐ నుండి మరియు 3 కేంద్ర ప్రభుత్వ నామినేటెడ్ సభ్యులు)."
    },
    {
        "id": "eco_2",
        "subject": "భారత ఆర్థిక వ్యవస్థ (Economy)",
        "question": "భారతదేశంలో వస్తు మరియు సేవల పన్ను (GST) ఏ రాజ్యాంగ సవరణ చట్టం ద్వారా అమల్లోకి వచ్చింది?",
        "options": ["A) 100వ సవరణ చట్టం", "B) 101వ సవరణ చట్టం", "C) 103వ సవరణ చట్టం", "D) 105వ సవరణ చట్టం"],
        "correct_option": "B",
        "explanation": "101వ రాజ్యాంగ సవరణ చట్టం 2016 ద్వారా భారతదేశంలో 2017 జూలై 1 నుంచి జీఎస్టీ వ్యవస్థ అమల్లోకి వచ్చింది."
    },
    {
        "id": "eco_3",
        "subject": "భారత ఆర్థిక వ్యవస్థ (Economy)",
        "question": "భారతదేశంలో ద్రవ్యోల్బణాన్ని (Inflation) లెక్కించడానికి ఆర్బీఐ ప్రామాణికంగా తీసుకునే సూచీ ఏది?",
        "options": ["A) టోకు ధరల సూచీ (WPI)", "B) వినియోగదారుల ధరల సూచీ (CPI - Combined)", "C) పారిశ్రామికోత్పత్తి సూచీ (IIP)", "D) ఎగుమతుల సూచీ"],
        "correct_option": "B",
        "explanation": "ఉర్జిత్ పటేల్ కమిటీ సిఫారసుల ప్రకారం ఆర్బీఐ 2014 నుంచి కన్స్యూమర్ ప్రైస్ ఇండెక్స్ (CPI Combined) ను ద్రవ్యోల్బణానికి ప్రామాణికంగా తీసుకుంటోంది."
    },
    {
        "id": "eco_4",
        "subject": "భారత ఆర్థిక వ్యవస్థ (Economy)",
        "question": "నీతి ఆయోగ్ (NITI Aayog) పాలక మండలి (Governing Council) కి అధ్యక్షుడు ఎవరు?",
        "options": ["A) భారత రాష్ట్రపతి", "B) ప్రధాన మంత్రి", "C) కేంద్ర ఆర్థిక మంత్రి", "D) నీతి ఆయోగ్ వైస్ చైర్మన్"],
        "correct_option": "B",
        "explanation": "నీతి ఆయోగ్ చైర్మన్‌గా ప్రధానమంత్రి ఉంటారు. పాలక మండలిలో అన్ని రాష్ట్రాల ముఖ్యమంత్రులు మరియు కేంద్రపాలిత ప్రాంతాల లెఫ్టినెంట్ గవర్నర్లు సభ్యులుగా ఉంటారు."
    },

    # Geography & Environment
    {
        "id": "geo_1",
        "subject": "భూగోళశాస్త్రం (Geography)",
        "question": "భారత ప్రామాణిక రేఖాంశం (82° 30' తూర్పు రేఖాంశం) ఆంధ్రప్రదేశ్‌లోని ఏ నగరం మీదుగా వెళుతుంది?",
        "options": ["A) విశాఖపట్నం", "B) కాకినాడ", "C) విజయవాడ", "D) గుంటూరు"],
        "correct_option": "B",
        "explanation": "82° 30' తూర్పు రేఖాంశం (IST) ఆంధ్రప్రదేశ్‌లోని కాకినాడ నగరం మీదుగా ప్రయాణిస్తుంది."
    },
    {
        "id": "geo_2",
        "subject": "భూగోళశాస్త్రం (Geography)",
        "question": "దక్షిణ భారతదేశంలో ఎత్తైన పర్వత శిఖరం ఏది?",
        "options": ["A) అనైముడి (ఆనమలై)", "B) దొడ్డబెట్ట (నీలగిరి)", "C) మహేంద్రగిరి", "D) జిందాగడ (అరకు)"],
        "correct_option": "A",
        "explanation": "కేరళలోని ఆనమలై కొండల్లో ఉన్న అనైముడి (2,695 మీటర్లు) దక్షిణ భారతదేశం మరియు పశ్చిమ కనుమలలోనే అత్యంత ఎత్తైన శిఖరం."
    },
    {
        "id": "geo_3",
        "subject": "భూగోళశాస్త్రం (Geography)",
        "question": "ఆంధ్రప్రదేశ్ మరియు తమిళనాడు సరిహద్దుల్లో విస్తరించి ఉన్న ప్రసిద్ధ ఉప్పునీటి సరస్సు ఏది?",
        "options": ["A) కొల్లేరు సరస్సు", "B) పులికాట్ సరస్సు", "C) సాంబార్ సరస్సు", "D) చిల్కా సరస్సు"],
        "correct_option": "B",
        "explanation": "పులికాట్ సరస్సు ఏపీ (తిరుపతి జిల్లా) మరియు తమిళనాడు సరిహద్దుల్లో ఉన్న భారతదేశపు రెండవ అతిపెద్ద ఉప్పునీటి సరస్సు."
    },
    {
        "id": "geo_4",
        "subject": "సైన్స్ & టెక్నాలజీ (Science & Tech)",
        "question": "ఇస్రో ప్రయోగించిన చంద్రయాన్-3 ల్యాండర్ చంద్రుడి దక్షిణ ధ్రువంపై దిగిన ప్రదేశానికి ప్రధాని మోదీ ఏ పేరు పెట్టారు?",
        "options": ["A) తిరంగా పాయింట్", "B) శివశక్తి పాయింట్", "C) భారత్ పాయింట్", "D) విక్రమ్ పాయింట్"],
        "correct_option": "B",
        "explanation": "చంద్రయాన్-3 ల్యాండర్ తాకిన ప్రదేశానికి శివశక్తి పాయింట్ అని పేరు పెట్టారు. ఆగస్టు 23ను జాతీయ అంతరిక్ష దినోత్సవంగా ప్రకటించారు."
    },

    # Welfare Schemes
    {
        "id": "sch_1",
        "subject": "ఏపీ & తెలంగాణ ప్రభుత్వ పథకాలు (Schemes)",
        "question": "ఆంధ్రప్రదేశ్ ప్రభుత్వ దీపం-2 పథకం నిబంధనల ప్రకారం అర్హులైన మహిళకు ఏడాదికి ఎన్ని ఉచిత సిలిండర్లు లభిస్తాయి?",
        "options": ["A) 2 సిలిండర్లు", "B) 3 సిలిండర్లు", "C) 4 సిలిండర్లు", "D) 6 సిలిండర్లు"],
        "correct_option": "B",
        "explanation": "ఎన్నికల సూపర్ సిక్స్ హామీలలో భాగంగా తెల్ల రేషన్ కార్డు కలిగిన ప్రతి పేద కుటుంబానికి ఏడాదికి 3 ఉచిత ఎల్పీజీ సిలిండర్లు అందిస్తారు."
    },
    {
        "id": "sch_2",
        "subject": "ఏపీ & తెలంగాణ ప్రభుత్వ పథకాలు (Schemes)",
        "question": "తెలంగాణ ప్రభుత్వ మహాలక్ష్మి పథకం ద్వారా మహిళలకు ఉచిత బస్సు ప్రయాణం కల్పించిన ఆర్టీసీ బస్సు రకాలు ఏవి?",
        "options": ["A) కేవలం సిటీ ఆర్డినరీ మాత్రమే", "B) పల్లెవెలుగు మరియు ఎక్స్‌ప్రెస్ బస్సులు", "C) గరుడ మరియు వోల్వో బస్సులు", "D) అంతర్రాష్ట్ర లగ్జరీ బస్సులు"],
        "correct_option": "B",
        "explanation": "మహాలక్ష్మి పథకం కింద తెలంగాణ నివాసితులైన బాలికలు, మహిళలు TSRTC పల్లెవెలుగు మరియు ఎక్స్‌ప్రెస్ బస్సుల్లో జీరో టికెట్ ద్వారా ఉచితంగా ప్రయాణించవచ్చు."
    }
]

def get_daily_live_test(date=None):
    """
    Returns exactly 20 questions for the Daily CBT Mock Test:
    - 5 Dynamic Today's CA MCQs
    - 15 Rotated Static GS MCQs
    Deterministic per date!
    """
    target_date = date or get_ist_today()
    
    daily_ca_questions = []
    try:
        from db import get_quiz_by_date
        db_quizzes = get_quiz_by_date(date=target_date)
        if not db_quizzes:
            from quiz_generator import ensure_daily_quizzes
            db_quizzes = ensure_daily_quizzes(date=target_date)
            
        for q in db_quizzes:
            opts = [
                f"A) {q.get('option_a', '')}",
                f"B) {q.get('option_b', '')}",
                f"C) {q.get('option_c', '')}",
                f"D) {q.get('option_d', '')}"
            ]
            daily_ca_questions.append({
                "id": f"ca_{q.get('id', len(daily_ca_questions)+1)}",
                "subject": "నేటి సమకాలీన అంశాలు (Current Affairs)",
                "question": q.get("question", ""),
                "options": opts,
                "correct_option": q.get("correct_option", "A").upper().strip(),
                "explanation": q.get("explanation", "")
            })
    except Exception as e:
        print(f"Error loading daily CA quizzes: {e}")

    selected_ca = daily_ca_questions[:5]
    seed_int = int(hashlib.md5(target_date.encode()).hexdigest()[:8], 16)
    rng = random.Random(seed_int)
    
    shuffled_gs = list(GS_STATIC_POOL)
    rng.shuffle(shuffled_gs)
    
    needed_gs = 20 - len(selected_ca)
    selected_gs = shuffled_gs[:needed_gs]
    
    all_questions = selected_ca + selected_gs
    
    client_questions = []
    for idx, item in enumerate(all_questions, 1):
        client_questions.append({
            "q_no": idx,
            "q_id": item["id"],
            "subject": item["subject"],
            "question": item["question"],
            "options": item["options"]
        })
        
    return {
        "success": True,
        "date": target_date,
        "total_questions": len(all_questions),
        "duration_minutes": 15,
        "total_marks": 20.0,
        "negative_marking": 0.33,
        "questions": client_questions,
        "_internal_bank": all_questions
    }

def get_live_test_questions(date=None):
    """
    Returns question objects formatted for leaderboard_db and api_live_test_today
    with: id, question, options, key, explanation, subject.
    """
    test_data = get_daily_live_test(date=date)
    bank = test_data["_internal_bank"]
    formatted = []
    for item in bank:
        k = item["correct_option"].strip().upper()
        if len(k) > 1 and k[1] in [")", ".", ":", " "]:
            k = k[0]
        formatted.append({
            "id": item["id"],
            "question": item["question"],
            "options": item["options"],
            "key": k,
            "explanation": item["explanation"],
            "subject": item.get("subject", "General Studies")
        })
    return formatted

def evaluate_live_test(submitted_answers, date=None):
    """
    Evaluates candidate's submitted responses.
    submitted_answers: dict { "1": "B", "2": "A", ... }
    Returns score, accuracy, rank tier, detailed answers & explanations.
    """
    test_data = get_daily_live_test(date=date)
    bank = test_data["_internal_bank"]
    
    total_q = len(bank)
    attempted = 0
    correct = 0
    incorrect = 0
    unattempted = 0
    review_details = []
    
    for idx, item in enumerate(bank, 1):
        key = str(idx)
        user_choice = submitted_answers.get(key) or submitted_answers.get(f"q_{idx}") or submitted_answers.get(item["id"])
        
        if user_choice:
            user_choice = str(user_choice).strip().upper()
            if len(user_choice) > 1 and user_choice[1] in [")", ".", ":", " "]:
                user_choice = user_choice[0]
        else:
            user_choice = None
            
        correct_opt = item["correct_option"].upper().strip()
        if len(correct_opt) > 1 and correct_opt[1] in [")", ".", ":", " "]:
            correct_opt = correct_opt[0]
            
        is_correct = False
        is_attempted = user_choice is not None and user_choice != ""
        
        if is_attempted:
            attempted += 1
            if user_choice == correct_opt:
                correct += 1
                is_correct = True
            else:
                incorrect += 1
        else:
            unattempted += 1
            
        review_details.append({
            "q_no": idx,
            "subject": item["subject"],
            "question": item["question"],
            "options": item["options"],
            "user_choice": user_choice,
            "correct_option": correct_opt,
            "is_correct": is_correct,
            "is_attempted": is_attempted,
            "explanation": item["explanation"]
        })
        
    raw_positive = correct * 1.0
    negative_deduction = incorrect * 0.33
    final_score = round(max(0.0, raw_positive - negative_deduction), 2)
    percentage = round((final_score / total_q) * 100, 1)
    accuracy = round((correct / attempted * 100), 1) if attempted > 0 else 0.0
    
    if final_score >= 16:
        badge = "🏆 టాపర్ లెవెల్ (Outstanding!)"
        feedback = "అద్భుతమైన ప్రతిభ! మీ ప్రిపరేషన్ అగ్రస్థానంలో ఉంది. ఇదే వేగంతో పరీక్ష వరకు కొనసాగించండి."
        badge_color = "emerald"
    elif final_score >= 12:
        badge = "🥇 అద్భుతమైన స్కోరు (Excellent)"
        feedback = "చాలా మంచి స్కోర్! తప్పుగా పెట్టిన ప్రశ్నల వివరణలను సమీక్షించండి."
        badge_color = "blue"
    elif final_score >= 8:
        badge = "🥈 మంచి ప్రయత్నం (Good Attempt)"
        feedback = "మంచి ప్రయత్నం! నెగెటివ్ మార్కులను తగ్గించడానికి మరింత శ్రద్ధ వహించండి."
        badge_color = "amber"
    else:
        badge = "📚 మరింత సాధన అవసరం (Need Practice)"
        feedback = "డైలీ కరెంట్ అఫైర్స్ నోట్స్ మరియు మాస్టర్ హ్యాండ్‌బుక్ రెగ్యులర్‌గా చదవండి."
        badge_color = "rose"
        
    return {
        "success": True,
        "date": test_data["date"],
        "total_questions": total_q,
        "attempted": attempted,
        "correct": correct,
        "incorrect": incorrect,
        "unattempted": unattempted,
        "raw_positive": raw_positive,
        "negative_deduction": round(negative_deduction, 2),
        "final_score": final_score,
        "percentage": percentage,
        "accuracy": accuracy,
        "badge": badge,
        "badge_color": badge_color,
        "feedback": feedback,
        "review": review_details
    }
