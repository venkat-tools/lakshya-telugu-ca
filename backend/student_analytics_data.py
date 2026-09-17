# -*- coding: utf-8 -*-
"""
Student Performance Analytics & Weakness Diagnoser Data.
Defines examination benchmarks, subject weightages, and diagnostic rule engines.
"""

APPSC_GROUP2_BENCHMARKS = {
    "exam_name": "APPSC Group-2 Prelims (Screening Test)",
    "total_marks": 150,
    "total_questions": 150,
    "negative_marking": 0.333,
    "recommended_target_score": 105,
    "official_cutoff_2024": 92.00,
    "qualifying_threshold": 60.0,
    "sections": [
        {
            "id": "history",
            "name": "భారత & ఆంధ్రప్రదేశ్ చరిత్ర (History)",
            "weightage": 30,
            "target_score": 24,
            "hub_url": "/appsc_master_portal",
            "weakness_tip": "ప్రాచీన-మధ్యయుగ రాజవంశాల శాసనాలు, శాతవాహనుల నిర్మాణాలు మరియు ఆధునిక ఆంధ్రోద్యమం (1913 బాపట్ల సభ, శ్రీభాగ్ ఒప్పందం) పై ఎక్కువ శ్రద్ధ పెట్టండి."
        },
        {
            "id": "geography",
            "name": "భౌగోళికం & 26 జిల్లాలు (Geography)",
            "weightage": 30,
            "target_score": 23,
            "hub_url": "/districts_handbook",
            "weakness_tip": "ఆంధ్రప్రదేశ్ 26 జిల్లాల సరిహద్దులు, నదుల జన్మస్థలాలు, తీరరేఖ (974 కి.మీ) మరియు పోర్టులు-ఖనిజ వనరుల మ్యాప్‌లను పరిశీలించండి."
        },
        {
            "id": "society",
            "name": "భారతీయ సమాజం (Indian Society)",
            "weightage": 30,
            "target_score": 25,
            "hub_url": "/indian_society_hub",
            "weakness_tip": "కుటుంబం-బంధుత్వం సిద్ధాంతాలు (ఎం.ఎన్. శ్రీనివాస్, ఇరావతి కార్వే), 75 PVTGs తెగలు, SC/ST చట్టం 1989 మరియు PESA 1996 చట్టాలను క్షుణ్ణంగా రివిజన్ చేయండి."
        },
        {
            "id": "mental_ability",
            "name": "మెంటల్ ఎబిలిటీ & రీజనింగ్ (Mental Ability)",
            "weightage": 30,
            "target_score": 25,
            "hub_url": "/mental_ability_hub",
            "weakness_tip": "శాతాలు, లాభనష్టాలు, పని-కాలం మరియు క్లాక్స్-క్యాలెండర్స్ 120 షార్ట్‌కట్ సూత్రాల ఫార్ములా డెక్ ను డైలీ 20 నిమిషాలు ప్రాక్టీస్ చేయండి."
        },
        {
            "id": "current_affairs",
            "name": "కరెంట్ అఫైర్స్ & పాలసీలు (Current Affairs)",
            "weightage": 30,
            "target_score": 24,
            "hub_url": "/",
            "weakness_tip": "గత 12 నెలల జాతీయ-అంతర్జాతీయ సదస్సులు, కేంద్ర-రాష్ట్ర బడ్జెట్ కేటాయింపులు, ఇస్రో మిషన్లు మరియు ప్రముఖ అవార్డులను రివైజ్ చేయండి."
        }
    ]
}

DEMO_STUDENT_PROFILE = {
    "student_name": "ఆస్పిరెంట్ (Demo Mode)",
    "overall_accuracy": 68.5,
    "tests_attempted": 14,
    "total_questions_solved": 420,
    "estimated_score_150": 88.5,
    "planner_completed_days": 24,
    "planner_total_days": 60,
    "subject_scores": {
        "history": {"correct": 21, "wrong": 5, "unattempted": 4, "accuracy": 70.0, "status": "మధ్యస్థం (Good)"},
        "geography": {"correct": 19, "wrong": 6, "unattempted": 5, "accuracy": 63.3, "status": "మధ్యస్థం (Average)"},
        "society": {"correct": 14, "wrong": 9, "unattempted": 7, "accuracy": 46.7, "status": "బలహీనత (Weak Alert)"},
        "mental_ability": {"correct": 23, "wrong": 4, "unattempted": 3, "accuracy": 76.7, "status": "బలం (Strong)"},
        "current_affairs": {"correct": 20, "wrong": 6, "unattempted": 4, "accuracy": 66.7, "status": "మధ్యస్థం (Good)"}
    }
}

def get_student_analytics_benchmarks():
    return APPSC_GROUP2_BENCHMARKS

def get_demo_student_profile():
    return DEMO_STUDENT_PROFILE
