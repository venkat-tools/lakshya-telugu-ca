# -*- coding: utf-8 -*-
"""
APPSC Group-2 Paper-2 (150 Marks: AP History & Indian Constitution) Master Portal View.
Provides:
1. 150-Question CBT/OMR Exam Simulator with -0.33 negative marking and timer.
2. 10-Unit Comprehensive Revision Notes.
"""

import json
from group2_paper2_data import get_paper2_syllabus, get_paper2_notes, get_paper2_mock_questions

def render_group2_paper2_html():
    syllabus = get_paper2_syllabus()
    notes = get_paper2_notes()
    questions = get_paper2_mock_questions()

    syllabus_json = json.dumps(syllabus, ensure_ascii=False)
    notes_json = json.dumps(notes, ensure_ascii=False)
    questions_json = json.dumps(questions, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 APPSC Group-2 పేపర్-2 (150 Marks) మెగా పోర్టల్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-primary: #0a0f1d;
            --bg-card: #121a2e;
            --bg-card-alt: #18233c;
            --accent-gold: #f59e0b;
            --accent-blue: #3b82f6;
            --accent-emerald: #10b981;
            --accent-purple: #8b5cf6;
            --accent-rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e293b;
            --radius-md: 10px;
            --radius-lg: 16px;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}
        body {{
            font-family: 'Outfit', 'Mandali', sans-serif;
            background: linear-gradient(135deg, #070b16 0%, #0d1527 50%, #080e1a 100%);
            color: var(--text-main);
            min-height: 100vh;
        }}

        /* Navbar */
        .top-navbar {{
            background: rgba(10, 15, 29, 0.96);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 10px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }}
        .brand-link {{
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: inherit;
        }}
        .brand-badge {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #0f172a;
            font-weight: 800;
            font-size: 0.8rem;
            padding: 4px 10px;
            border-radius: 6px;
        }}
        .brand-title {{
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .nav-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-btn {{
            background: #1e293b;
            border: 1px solid #334155;
            color: #f1f5f9;
            padding: 8px 14px;
            border-radius: var(--radius-md);
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .nav-btn:hover {{
            background: #334155;
            color: white;
        }}
        .timer-badge {{
            background: #1e1b4b;
            border: 1px solid #6366f1;
            color: #a5b4fc;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.95rem;
            font-weight: 800;
            font-family: monospace;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Mode Switcher Tabs */
        .mode-tabs {{
            display: flex;
            background: #0d1629;
            border-bottom: 1px solid var(--border-color);
            padding: 6px 20px;
            gap: 12px;
        }}
        .mode-tab-btn {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            padding: 10px 18px;
            font-size: 0.9rem;
            font-weight: 700;
            cursor: pointer;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: all 0.2s;
        }}
        .mode-tab-btn.active {{
            background: #1e293b;
            color: #f59e0b;
        }}

        /* Main Container */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 16px;
        }}

        /* Exam Simulator Layout */
        .exam-layout {{
            display: grid;
            grid-template-columns: 1fr 340px;
            gap: 20px;
            align-items: start;
        }}
        @media (max-width: 992px) {{
            .exam-layout {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Question Box Area */
        .question-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 24px;
            min-height: 480px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .q-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .q-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .q-badge {{
            background: #3b82f6;
            color: white;
            font-size: 0.82rem;
            font-weight: 800;
            padding: 4px 10px;
            border-radius: 6px;
        }}
        .q-unit {{
            font-size: 0.8rem;
            color: var(--accent-gold);
            font-weight: 700;
        }}
        .marks-badge {{
            font-size: 0.75rem;
            color: #94a3b8;
            background: #0c1322;
            padding: 4px 8px;
            border-radius: 4px;
            border: 1px solid #1e293b;
        }}
        .q-text {{
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.6;
            color: #ffffff;
            margin-bottom: 24px;
        }}
        .options-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
            margin-bottom: 24px;
        }}
        .opt-label {{
            background: #0a1122;
            border: 1px solid #1e293b;
            border-radius: var(--radius-md);
            padding: 14px 18px;
            display: flex;
            align-items: center;
            gap: 14px;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 0.95rem;
            color: #cbd5e1;
        }}
        .opt-label:hover {{
            background: #14203a;
            border-color: #3b82f6;
        }}
        .opt-label.selected {{
            background: rgba(59, 130, 246, 0.15);
            border-color: #3b82f6;
            color: #ffffff;
            font-weight: 700;
        }}
        .opt-label input[type="radio"] {{
            accent-color: #3b82f6;
            width: 18px;
            height: 18px;
        }}

        /* Action Buttons */
        .q-actions {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding-top: 16px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            flex-wrap: wrap;
        }}
        .action-btn {{
            padding: 10px 18px;
            border-radius: var(--radius-md);
            font-size: 0.88rem;
            font-weight: 700;
            cursor: pointer;
            border: 1px solid #334155;
            background: #1e293b;
            color: #f1f5f9;
            display: inline-flex;
            align-items: center;
            gap: 8px;
            transition: all 0.15s;
        }}
        .action-btn:hover {{
            background: #334155;
        }}
        .action-btn.btn-save {{
            background: linear-gradient(135deg, #10b981, #059669);
            border: none;
            color: white;
        }}
        .action-btn.btn-save:hover {{
            background: linear-gradient(135deg, #34d399, #10b981);
        }}
        .action-btn.btn-review {{
            background: #581c87;
            border-color: #7e22ce;
            color: #e9d5ff;
        }}
        .action-btn.btn-review:hover {{
            background: #6b21a8;
        }}

        /* Palette Sidebar */
        .palette-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 18px;
        }}
        .section-switch-btns {{
            display: flex;
            gap: 6px;
            margin-bottom: 14px;
        }}
        .sec-switch-btn {{
            flex: 1;
            padding: 8px 10px;
            font-size: 0.78rem;
            font-weight: 800;
            background: #090e1a;
            border: 1px solid #1e293b;
            border-radius: 8px;
            color: var(--text-muted);
            cursor: pointer;
            transition: all 0.2s;
        }}
        .sec-switch-btn.active {{
            background: #3b82f6;
            color: white;
            border-color: #3b82f6;
        }}
        .palette-stats {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 6px;
            margin-bottom: 14px;
            font-size: 0.74rem;
        }}
        .stat-item {{
            background: #0a1122;
            padding: 6px 10px;
            border-radius: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .stat-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        .palette-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 6px;
            max-height: 380px;
            overflow-y: auto;
            padding-right: 4px;
        }}
        .palette-btn {{
            aspect-ratio: 1;
            border-radius: 8px;
            border: 1px solid #1e293b;
            background: #0a1122;
            color: #94a3b8;
            font-size: 0.8rem;
            font-weight: 800;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
        }}
        .palette-btn:hover {{
            background: #1e293b;
            color: white;
        }}
        .palette-btn.current {{
            border: 2px solid #38bdf8 !important;
            color: #38bdf8;
        }}
        .palette-btn.answered {{
            background: #065f46;
            border-color: #10b981;
            color: #ecfdf5;
        }}
        .palette-btn.review {{
            background: #581c87;
            border-color: #a855f7;
            color: #faf5ff;
        }}
        .palette-btn.review-answered {{
            background: #701a75;
            border-color: #f43f5e;
            color: #fff;
            position: relative;
        }}
        .submit-all-btn {{
            width: 100%;
            margin-top: 14px;
            padding: 12px;
            border-radius: var(--radius-md);
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #0f172a;
            border: none;
            font-size: 0.95rem;
            font-weight: 900;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .submit-all-btn:hover {{
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            transform: translateY(-1px);
        }}

        /* Score Modal / View */
        .result-view {{
            display: none;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 30px;
            text-align: center;
        }}
        .score-circle {{
            width: 140px;
            height: 140px;
            border-radius: 50%;
            background: radial-gradient(circle, #1e293b, #0a1122);
            border: 4px solid var(--accent-gold);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px auto;
        }}
        .score-val {{
            font-size: 2.2rem;
            font-weight: 900;
            color: var(--accent-gold);
        }}
        .score-denom {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}
        .results-summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 14px;
            margin: 24px 0;
        }}
        .res-stat-card {{
            background: #090e1a;
            border: 1px solid #1e293b;
            border-radius: 10px;
            padding: 14px;
        }}
        .res-stat-val {{
            font-size: 1.4rem;
            font-weight: 900;
            margin-top: 4px;
        }}

        /* Solutions Review Box */
        .solutions-box {{
            margin-top: 30px;
            text-align: left;
        }}
        .sol-card {{
            background: #0c1324;
            border: 1px solid #1e293b;
            border-radius: var(--radius-md);
            padding: 16px;
            margin-bottom: 12px;
        }}
        .sol-header {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 6px;
        }}
        .sol-q {{
            font-weight: 700;
            color: #fff;
            margin-bottom: 10px;
        }}
        .sol-ans {{
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid #10b981;
            padding: 8px 12px;
            border-radius: 0 6px 6px 0;
            font-size: 0.88rem;
            color: #34d399;
            margin-bottom: 6px;
        }}
        .sol-exp {{
            font-size: 0.82rem;
            color: #cbd5e1;
            line-height: 1.5;
            background: #050811;
            padding: 8px 12px;
            border-radius: 6px;
        }}

        /* Study Notes View */
        .notes-view {{
            display: none;
        }}
        .unit-note-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 20px;
            margin-bottom: 18px;
        }}
        .unit-note-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 10px;
            margin-bottom: 14px;
        }}
        .unit-note-header h3 {{
            font-size: 1.1rem;
            font-weight: 800;
            color: #ffffff;
        }}
        .unit-note-points {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .unit-note-points li {{
            font-size: 0.92rem;
            line-height: 1.6;
            color: #e2e8f0;
            position: relative;
            padding-left: 20px;
        }}
        .unit-note-points li::before {{
            content: "👉";
            position: absolute;
            left: 0;
            top: 2px;
            font-size: 0.8rem;
        }}

        /* Fullscreen Toggle */
        .fullscreen-active header,
        .fullscreen-active .top-navbar,
        .fullscreen-active .mode-tabs {{
            display: none !important;
        }}
    </style>
</head>
<body>

    <!-- Top Navbar -->
    <header class="top-navbar" id="mainHeader">
        <a href="/" class="brand-link">
            <span class="brand-badge">APPSC Group-2</span>
            <span class="brand-title">🎯 పేపర్-2 మెగా పోర్టల్ (150 Marks)</span>
        </a>
        <div class="nav-actions">
            <div class="timer-badge" id="examTimer">
                <i class="fa-solid fa-clock"></i> <span id="timerDisplay">150:00</span>
            </div>
            <button class="nav-btn" onclick="toggleFullScreenMode()" title="ట్యాబ్స్ దాచు / చూపించు">
                <i class="fa-solid fa-expand"></i> <span id="toggleText">పూర్తి స్క్రీన్</span>
            </button>
            <a href="/" class="nav-btn">
                <i class="fa-solid fa-house"></i> హోమ్
            </a>
        </div>
    </header>

    <!-- Mode Tabs -->
    <div class="mode-tabs">
        <button class="mode-tab-btn active" id="tabExam" onclick="switchMode('exam')">
            <i class="fa-solid fa-file-pen"></i> 150-ప్రశ్నల OMR/CBT మాక్ టెస్ట్
        </button>
        <button class="mode-tab-btn" id="tabNotes" onclick="switchMode('notes')">
            <i class="fa-solid fa-book-open-reader"></i> 10 యూనిట్ల సమగ్ర రివిజన్ నోట్స్
        </button>
    </div>

    <div class="container">
        <!-- Exam Simulator View -->
        <div id="examViewArea" class="exam-layout">
            <!-- Left: Question Display Card -->
            <div class="question-card" id="questionBox">
                <div>
                    <div class="q-header">
                        <div class="q-meta">
                            <span class="q-badge" id="qBadge">Q. 1 / 150</span>
                            <span class="q-unit" id="qUnit">యూనిట్ 1: శాతవాహనులు</span>
                        </div>
                        <div class="marks-badge">
                            సరైనది: <b>+1</b> | తప్పు: <b>-0.33</b>
                        </div>
                    </div>

                    <div class="q-text" id="qText">
                        ప్రశ్న లోడ్ అవుతోంది...
                    </div>

                    <div class="options-list" id="optionsContainer">
                        <!-- Options injected by JS -->
                    </div>
                </div>

                <div class="q-actions">
                    <button class="action-btn" onclick="prevQuestion()"><i class="fa-solid fa-arrow-left"></i> మునుపటి</button>
                    <button class="action-btn btn-review" onclick="markForReview()"><i class="fa-solid fa-bookmark"></i> రివ్యూ కోసం మార్క్</button>
                    <button class="action-btn" onclick="clearCurrentAnswer()"><i class="fa-solid fa-rotate-left"></i> క్లియర్</button>
                    <button class="action-btn btn-save" onclick="saveAndNext()">సేవ్ & తదుపరి <i class="fa-solid fa-arrow-right"></i></button>
                </div>
            </div>

            <!-- Right: Question Palette -->
            <div class="palette-panel">
                <div class="section-switch-btns">
                    <button class="sec-switch-btn active" id="secBtnA" onclick="switchSection('sec_a')">
                        📜 సెక్షన్ A (AP చరిత్ర)
                    </button>
                    <button class="sec-switch-btn" id="secBtnB" onclick="switchSection('sec_b')">
                        🏛️ సెక్షన్ B (పాలిటీ)
                    </button>
                </div>

                <div class="palette-stats">
                    <div class="stat-item"><div class="stat-dot" style="background:#10b981;"></div> సమాధానం ఇచ్చారు: <b id="statAnswered">0</b></div>
                    <div class="stat-item"><div class="stat-dot" style="background:#94a3b8;"></div> ఇవ్వలేదు: <b id="statUnanswered">150</b></div>
                    <div class="stat-item"><div class="stat-dot" style="background:#a855f7;"></div> రివ్యూ: <b id="statReview">0</b></div>
                    <div class="stat-item"><div class="stat-dot" style="background:#3b82f6;"></div> ప్రస్తుత ప్రశ్న: <b id="statCurrent">1</b></div>
                </div>

                <div class="palette-grid" id="paletteGrid">
                    <!-- 150 circles rendered by JS -->
                </div>

                <button class="submit-all-btn" onclick="confirmSubmitExam()">
                    <i class="fa-solid fa-paper-plane"></i> పరీక్షను సమర్పించు (Submit Test)
                </button>
            </div>
        </div>

        <!-- Result View (Hidden until submitted) -->
        <div id="resultViewArea" class="result-view">
            <h2 style="font-size:1.8rem; font-weight:900; color:#fff; margin-bottom:12px;">🎉 పరీక్ష ఫలితాల విశ్లేషణ (Result Report)</h2>
            <p style="color:var(--text-muted); margin-bottom:20px;">APPSC Group-2 పేపర్-2 (150 మార్కులు - 1/3rd నెగెటివ్ మార్కింగ్ వర్తింపు)</p>

            <div class="score-circle">
                <div class="score-val" id="netScoreVal">0.0</div>
                <div class="score-denom">/ 150 మార్కులు</div>
            </div>

            <div id="performanceBadge" style="display:inline-block; padding:8px 20px; border-radius:30px; font-weight:800; font-size:1rem; margin-bottom:24px;"></div>

            <div class="results-summary-grid">
                <div class="res-stat-card">
                    <div style="color:#10b981; font-weight:700;"><i class="fa-solid fa-circle-check"></i> సరైన సమాధానాలు</div>
                    <div class="res-stat-val" style="color:#34d399;" id="resCorrect">0</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">+1 మార్కు ఒక్కోదానికి</div>
                </div>
                <div class="res-stat-card">
                    <div style="color:#f43f5e; font-weight:700;"><i class="fa-solid fa-circle-xmark"></i> తప్పు సమాధానాలు</div>
                    <div class="res-stat-val" style="color:#f87171;" id="resWrong">0</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">-0.33 మార్కు తగ్గింపు</div>
                </div>
                <div class="res-stat-card">
                    <div style="color:#94a3b8; font-weight:700;"><i class="fa-solid fa-circle-minus"></i> సమాధానం ఇవ్వనివి</div>
                    <div class="res-stat-val" style="color:#cbd5e1;" id="resSkipped">0</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">0 మార్కులు</div>
                </div>
                <div class="res-stat-card">
                    <div style="color:#38bdf8; font-weight:700;"><i class="fa-solid fa-bullseye"></i> ఖచ్చితత్వం (Accuracy)</div>
                    <div class="res-stat-val" style="color:#38bdf8;" id="resAccuracy">0%</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">సరిచూసుకున్న శాతం</div>
                </div>
                <div class="res-stat-card">
                    <div style="color:#f59e0b; font-weight:700;"><i class="fa-solid fa-landmark"></i> సెక్షన్ A (AP చరిత్ర)</div>
                    <div class="res-stat-val" style="color:#fbbf24;" id="resSecA">0 / 75</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">చరిత్ర స్కోర్</div>
                </div>
                <div class="res-stat-card">
                    <div style="color:#a855f7; font-weight:700;"><i class="fa-solid fa-scale-balanced"></i> సెక్షన్ B (రాజ్యాంగం)</div>
                    <div class="res-stat-val" style="color:#c084fc;" id="resSecB">0 / 75</div>
                    <div style="font-size:0.75rem; color:#94a3b8;">పాలిటీ స్కోర్</div>
                </div>
            </div>

            <div style="margin:20px 0;">
                <button class="action-btn" onclick="location.reload()"><i class="fa-solid fa-rotate-right"></i> మళ్లీ పరీక్ష రాయండి</button>
            </div>

            <div class="solutions-box" id="solutionsContainer">
                <h3 style="font-size:1.3rem; font-weight:800; color:#fff; margin-bottom:16px;">
                    📝 150 ప్రశ్నల పూర్తి సమాధానాలు మరియు వివరణలు (Full Answer Key & Explanations):
                </h3>
                <div id="solutionsList">
                    <!-- Solutions injected by JS -->
                </div>
            </div>
        </div>

        <!-- Study Notes View Area -->
        <div id="notesViewArea" class="notes-view">
            <!-- Rendered by JS -->
        </div>
    </div>

    <script>
        const syllabusData = {syllabus_json};
        const notesData = {notes_json};
        const questionsData = {questions_json};

        let currentQIndex = 0;
        let userAnswers = {{}}; // q_no: selectedOption
        let reviewStatus = {{}}; // q_no: bool
        let timerSeconds = 150 * 60;
        let timerInterval = null;
        let isSubmitted = false;

        function init() {{
            renderPalette();
            loadQuestion(0);
            startTimer();
            renderNotes();
        }}

        function startTimer() {{
            timerInterval = setInterval(() => {{
                if (timerSeconds <= 0) {{
                    clearInterval(timerInterval);
                    alert("పరీక్ష సమయం ముగిసింది! మీ జవాబులు ఆటోమేటిక్‌గా సమర్పించబడుతున్నాయి.");
                    submitExam();
                    return;
                }}
                timerSeconds--;
                const mins = Math.floor(timerSeconds / 60);
                const secs = timerSeconds % 60;
                document.getElementById('timerDisplay').innerText = 
                    `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }}, 1000);
        }}

        function loadQuestion(index) {{
            if (index < 0 || index >= questionsData.length) return;
            currentQIndex = index;
            const q = questionsData[index];

            document.getElementById('qBadge').innerText = `Q. ${{q.q_no}} / 150`;
            document.getElementById('qUnit').innerText = `${{q.section_name}} &bull; ${{q.unit}}`;
            document.getElementById('qText').innerText = `${{q.q_no}}. ${{q.question}}`;
            document.getElementById('statCurrent').innerText = q.q_no;

            // Highlight section button
            if (q.section === 'sec_a') {{
                document.getElementById('secBtnA').classList.add('active');
                document.getElementById('secBtnB').classList.remove('active');
            }} else {{
                document.getElementById('secBtnB').classList.add('active');
                document.getElementById('secBtnA').classList.remove('active');
            }}

            const optsDiv = document.getElementById('optionsContainer');
            const selectedOpt = userAnswers[q.q_no];

            optsDiv.innerHTML = q.options.map(opt => `
                <label class="opt-label ${{selectedOpt === opt ? 'selected' : ''}}" onclick="selectOption('${{opt.replace(/'/g, "\\\\\\'")}}')">
                    <input type="radio" name="opt_choice" value="${{opt.replace(/'/g, "\\\\\\'")}}" ${{selectedOpt === opt ? 'checked' : ''}}>
                    <span>${{opt}}</span>
                </label>
            `).join('');

            updatePaletteItem(index);
        }}

        function selectOption(val) {{
            const q = questionsData[currentQIndex];
            userAnswers[q.q_no] = val;
            loadQuestion(currentQIndex);
            updateStats();
        }}

        function clearCurrentAnswer() {{
            const q = questionsData[currentQIndex];
            delete userAnswers[q.q_no];
            loadQuestion(currentQIndex);
            updateStats();
        }}

        function markForReview() {{
            const q = questionsData[currentQIndex];
            reviewStatus[q.q_no] = !reviewStatus[q.q_no];
            updatePaletteItem(currentQIndex);
            updateStats();
            if (currentQIndex < questionsData.length - 1) {{
                loadQuestion(currentQIndex + 1);
            }}
        }}

        function saveAndNext() {{
            if (currentQIndex < questionsData.length - 1) {{
                loadQuestion(currentQIndex + 1);
            }} else {{
                alert("మీరు చివరి ప్రశ్న వద్ద ఉన్నారు. పరీక్ష పూర్తి అయితే 'పరీక్షను సమర్పించు' బటన్ నొక్కండి.");
            }}
        }}

        function prevQuestion() {{
            if (currentQIndex > 0) {{
                loadQuestion(currentQIndex - 1);
            }}
        }}

        function renderPalette() {{
            const grid = document.getElementById('paletteGrid');
            grid.innerHTML = questionsData.map((q, idx) => `
                <button class="palette-btn" id="pbtn_${{idx}}" onclick="loadQuestion(${{idx}})">
                    ${{q.q_no}}
                </button>
            `).join('');
        }}

        function updatePaletteItem(idx) {{
            const q = questionsData[idx];
            const btn = document.getElementById(`pbtn_${{idx}}`);
            if (!btn) return;

            // Remove state classes
            btn.className = 'palette-btn';

            if (idx === currentQIndex) {{
                btn.classList.add('current');
            }}

            const hasAns = !!userAnswers[q.q_no];
            const isRev = !!reviewStatus[q.q_no];

            if (isRev && hasAns) {{
                btn.classList.add('review-answered');
            }} else if (isRev) {{
                btn.classList.add('review');
            }} else if (hasAns) {{
                btn.classList.add('answered');
            }}
        }}

        function updateStats() {{
            const ansCount = Object.keys(userAnswers).length;
            const revCount = Object.values(reviewStatus).filter(Boolean).length;
            document.getElementById('statAnswered').innerText = ansCount;
            document.getElementById('statUnanswered').innerText = 150 - ansCount;
            document.getElementById('statReview').innerText = revCount;

            questionsData.forEach((_, idx) => updatePaletteItem(idx));
        }}

        function switchSection(sec) {{
            if (sec === 'sec_a') {{
                loadQuestion(0);
            }} else {{
                loadQuestion(75);
            }}
        }}

        function confirmSubmitExam() {{
            const ansCount = Object.keys(userAnswers).length;
            const unans = 150 - ansCount;
            const conf = confirm(`మీరు మొత్తం 150 లో ${{ansCount}} ప్రశ్నలకు సమాధానం ఇచ్చారు. ${{unans}} ప్రశ్నలు మిగిలి ఉన్నాయి.\n\nపరీక్షను నిజంగానే సమర్పించాలనుకుంటున్నారా?`);
            if (conf) {{
                submitExam();
            }}
        }}

        function submitExam() {{
            clearInterval(timerInterval);
            isSubmitted = true;

            let correct = 0;
            let wrong = 0;
            let skipped = 0;

            let secACorrect = 0;
            let secAWrong = 0;
            let secBCorrect = 0;
            let secBWrong = 0;

            questionsData.forEach(q => {{
                const userAns = userAnswers[q.q_no];
                if (!userAns) {{
                    skipped++;
                }} else if (userAns.trim() === q.answer.trim()) {{
                    correct++;
                    if (q.section === 'sec_a') secACorrect++; else secBCorrect++;
                }} else {{
                    wrong++;
                    if (q.section === 'sec_a') secAWrong++; else secBWrong++;
                }}
            }});

            const netScore = Math.max(0, (correct * 1.0) - (wrong * 0.33));
            const secANet = Math.max(0, (secACorrect * 1.0) - (secAWrong * 0.33));
            const secBNet = Math.max(0, (secBCorrect * 1.0) - (secBWrong * 0.33));
            const attempted = correct + wrong;
            const accuracy = attempted > 0 ? Math.round((correct / attempted) * 100) : 0;

            // Display Results
            document.getElementById('examViewArea').style.display = 'none';
            document.getElementById('resultViewArea').style.display = 'block';

            document.getElementById('netScoreVal').innerText = netScore.toFixed(2);
            document.getElementById('resCorrect').innerText = correct;
            document.getElementById('resWrong').innerText = wrong;
            document.getElementById('resSkipped').innerText = skipped;
            document.getElementById('resAccuracy').innerText = `${{accuracy}}%`;
            document.getElementById('resSecA').innerText = `${{secANet.toFixed(1)}} / 75`;
            document.getElementById('resSecB').innerText = `${{secBNet.toFixed(1)}} / 75`;

            const badge = document.getElementById('performanceBadge');
            if (netScore >= 110) {{
                badge.style.background = 'linear-gradient(135deg, #10b981, #059669)';
                badge.style.color = '#ffffff';
                badge.innerText = "🌟 అద్భుతం! టాప్ ర్యాంక్ ఖాయం (State Top-10 Bracket)";
            }} else if (netScore >= 90) {{
                badge.style.background = 'linear-gradient(135deg, #3b82f6, #1d4ed8)';
                badge.style.color = '#ffffff';
                badge.innerText = "🎯 వెరీ గుడ్! మెయిన్స్ సెలెక్షన్ జోన్ (Safe Selection Zone)";
            }} else if (netScore >= 70) {{
                badge.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
                badge.style.color = '#0f172a';
                badge.innerText = "⚡ మంచి ప్రయత్నం! మరోసారి రివిజన్ అవసరం (Borderline)";
            }} else {{
                badge.style.background = 'linear-gradient(135deg, #ef4444, #dc2626)';
                badge.style.color = '#ffffff';
                badge.innerText = "📚 బలహీనమైన సబ్జెక్టులపై దృష్టి పెట్టండి (Needs Heavy Practice)";
            }}

            // Render Solutions
            const solList = document.getElementById('solutionsList');
            solList.innerHTML = questionsData.map(q => {{
                const uAns = userAnswers[q.q_no];
                const isCorr = uAns && uAns.trim() === q.answer.trim();
                const statusTag = !uAns 
                    ? `<span style="color:#94a3b8; font-weight:700;">[సమాధానం ఇవ్వలేదు]</span>` 
                    : (isCorr ? `<span style="color:#10b981; font-weight:700;">[సరిగ్గా రాశారు ✓]</span>` : `<span style="color:#ef4444; font-weight:700;">[తప్పుగా రాశారు ✗]</span>`);

                return `
                <div class="sol-card">
                    <div class="sol-header">
                        <span>#${{q.q_no}} &bull; ${{q.section_name}} &bull; ${{q.unit}}</span>
                        <span>${{statusTag}}</span>
                    </div>
                    <div class="sol-q">${{q.q_no}}. ${{q.question}}</div>
                    <div class="sol-ans">
                        <b>✓ సరైన సమాధానం:</b> ${{q.answer}} 
                        ${{uAns && !isCorr ? `<span style="color:#f87171; margin-left:10px;">(మీ ఎంపిక: ${{uAns}})</span>` : ''}}
                    </div>
                    <div class="sol-exp">
                        <b>వివరణ:</b> ${{q.explanation}}
                    </div>
                </div>
                `;
            }}).join('');

            window.scrollTo({{ top: 0, behavior: 'smooth' }});
        }}

        function renderNotes() {{
            const container = document.getElementById('notesViewArea');
            container.innerHTML = `
                <div style="margin-bottom:20px; text-align:center;">
                    <h2 style="font-size:1.8rem; font-weight:900; color:#fff; margin-bottom:8px;">📚 APPSC గ్రూప్-2 పేపర్-2 సమగ్ర రివిజన్ నోట్స్</h2>
                    <p style="color:var(--text-muted);">ఆంధ్రప్రదేశ్ సాంఘిక సాంస్కృతిక చరిత్ర (5 యూనిట్లు) & భారత రాజ్యాంగం (5 యూనిట్లు)</p>
                </div>
            ` + notesData.map(n => `
                <div class="unit-note-card">
                    <div class="unit-note-header">
                        <h3>${{n.title}}</h3>
                        <span style="background:#1e3a8a; color:#93c5fd; padding:3px 10px; border-radius:6px; font-size:0.75rem; font-weight:800;">${{n.section}}</span>
                    </div>
                    <ul class="unit-note-points">
                        ${{n.points.map(pt => `<li>${{pt}}</li>`).join('')}}
                    </ul>
                </div>
            `).join('');
        }}

        function switchMode(mode) {{
            if (mode === 'exam') {{
                document.getElementById('tabExam').classList.add('active');
                document.getElementById('tabNotes').classList.remove('active');
                if (!isSubmitted) {{
                    document.getElementById('examViewArea').style.display = 'grid';
                    document.getElementById('resultViewArea').style.display = 'none';
                }} else {{
                    document.getElementById('resultViewArea').style.display = 'block';
                    document.getElementById('examViewArea').style.display = 'none';
                }}
                document.getElementById('notesViewArea').style.display = 'none';
            }} else {{
                document.getElementById('tabNotes').classList.add('active');
                document.getElementById('tabExam').classList.remove('active');
                document.getElementById('examViewArea').style.display = 'none';
                document.getElementById('resultViewArea').style.display = 'none';
                document.getElementById('notesViewArea').style.display = 'block';
            }}
        }}

        function toggleFullScreenMode() {{
            document.body.classList.toggle('fullscreen-active');
            const isFull = document.body.classList.contains('fullscreen-active');
            const btnText = document.getElementById('toggleText');
            if (btnText) {{
                btnText.innerText = isFull ? 'ట్యాబ్స్ చూపించు' : 'పూర్తి స్క్రీన్';
            }}
        }}

        window.onload = init;
    </script>
</body>
</html>
"""
    return html
