# -*- coding: utf-8 -*-
"""
Mains Descriptive Answer Writing & Evaluation Portal View.
Renders responsive, interactive Telugu answer writing practice interface with split comparison and timer.
"""

import json
from mains_descriptive_data import MAINS_QUESTIONS

def render_mains_descriptive_html():
    questions_json = json.dumps(MAINS_QUESTIONS, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>✍️ మెయిన్స్ డిస్క్రిప్టివ్ ఆన్సర్ రైటింగ్ పోర్టల్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0a0f1d;
            --bg-card: #131b2e;
            --bg-card-hover: #1b2640;
            --accent-gold: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #213054;
            --radius-md: 12px;
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
            background: linear-gradient(135deg, #070b16 0%, #0d1527 50%, #080e1d 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 80px;
        }}

        /* Navbar */
        .top-navbar {{
            background: rgba(10, 15, 29, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 12px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .brand-box {{
            display: flex;
            align-items: center;
            gap: 12px;
            text-decoration: none;
            color: inherit;
        }}
        .brand-icon {{
            font-size: 26px;
            background: linear-gradient(135deg, #f59e0b, #ea580c);
            padding: 6px 12px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(245, 158, 11, 0.35);
        }}
        .brand-text h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
        }}
        .brand-text p {{
            font-size: 0.8rem;
            color: var(--accent-gold);
        }}
        .nav-actions {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .nav-btn {{
            background: #1e293b;
            color: #e2e8f0;
            border: 1px solid var(--border-color);
            padding: 7px 14px;
            border-radius: 8px;
            font-size: 0.84rem;
            cursor: pointer;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            transition: all 0.2s;
        }}
        .nav-btn:hover {{
            background: #334155;
            color: #ffffff;
            border-color: var(--accent-gold);
        }}
        .nav-btn.pdf-btn {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #070b16;
            font-weight: 700;
            border: none;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 16px;
        }}

        /* Hero */
        .hero-section {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.12) 0%, rgba(6, 182, 212, 0.1) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 24px;
        }}
        .hero-section h2 {{
            font-size: 1.55rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .hero-section p {{
            color: #cbd5e1;
            font-size: 0.94rem;
            line-height: 1.6;
        }}

        /* Paper Filter Pills */
        .filter-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 20px;
        }}
        .paper-pill {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 0.84rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .paper-pill.active, .paper-pill:hover {{
            background: linear-gradient(135deg, #f59e0b, #ea580c);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(245, 158, 11, 0.3);
        }}

        /* Workspace Grid: Questions list + Writing Workspace */
        .workspace-grid {{
            display: grid;
            grid-template-columns: 360px 1fr;
            gap: 22px;
        }}
        @media (max-width: 900px) {{
            .workspace-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        /* Sidebar: Questions List */
        .questions-sidebar {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 16px;
            max-height: 780px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .sidebar-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .q-item-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 12px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .q-item-card:hover {{
            background: rgba(255, 255, 255, 0.07);
            border-color: var(--accent-gold);
        }}
        .q-item-card.selected {{
            border-color: var(--accent-gold);
            background: rgba(245, 158, 11, 0.15);
        }}
        .q-item-meta {{
            font-size: 0.74rem;
            color: var(--accent-cyan);
            font-weight: 600;
            margin-bottom: 4px;
        }}
        .q-item-title {{
            font-size: 0.88rem;
            font-weight: 600;
            color: #ffffff;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        /* Main Workspace */
        .main-writing-area {{
            display: flex;
            flex-direction: column;
            gap: 20px;
        }}

        /* Active Question Display */
        .active-question-card {{
            background: linear-gradient(135deg, #15223e 0%, #101b33 100%);
            border: 2px solid #283e70;
            border-radius: var(--radius-md);
            padding: 20px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }}
        .aq-badge {{
            display: inline-block;
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 8px;
        }}
        .aq-text {{
            font-size: 1.22rem;
            font-weight: 700;
            color: #ffffff;
            line-height: 1.5;
            margin-bottom: 12px;
        }}
        .aq-details {{
            display: flex;
            gap: 16px;
            font-size: 0.82rem;
            color: var(--text-muted);
            flex-wrap: wrap;
        }}

        /* Timer and Writing Tools Bar */
        .tools-bar {{
            background: #111a30;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 12px 18px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .timer-box {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .timer-display {{
            font-size: 1.3rem;
            font-weight: 800;
            color: var(--accent-gold);
            background: rgba(0,0,0,0.3);
            padding: 4px 12px;
            border-radius: 6px;
            font-variant-numeric: tabular-nums;
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}
        .btn-tool {{
            background: #1f2d50;
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 0.82rem;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-tool:hover {{
            background: #2b3e70;
            border-color: var(--accent-cyan);
        }}
        .word-stats {{
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 0.84rem;
            color: #cbd5e1;
        }}
        .word-badge {{
            color: var(--accent-emerald);
            font-weight: 700;
        }}

        /* Textarea Editor */
        .writing-pad {{
            width: 100%;
            height: 280px;
            background: #0d1527;
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            color: #f1f5f9;
            font-size: 1.05rem;
            line-height: 1.8;
            padding: 16px;
            font-family: 'Outfit', 'Mandali', sans-serif;
            resize: vertical;
            outline: none;
            transition: border-color 0.2s;
        }}
        .writing-pad:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 15px rgba(6, 182, 212, 0.2);
        }}

        /* Actions Bar */
        .action-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .btn-compare {{
            background: linear-gradient(135deg, var(--accent-emerald), #059669);
            color: #ffffff;
            font-weight: 700;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 0.95rem;
            transition: all 0.2s;
        }}
        .btn-compare:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(16, 185, 129, 0.5);
        }}

        /* Split Comparison / Model Answer Box */
        .model-answer-section {{
            background: #111b33;
            border: 2px solid #223766;
            border-radius: var(--radius-md);
            padding: 22px;
            display: none;
            animation: fadeIn 0.3s ease-in-out;
        }}
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        .model-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .model-header h3 {{
            font-size: 1.2rem;
            color: var(--accent-gold);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .model-block {{
            margin-bottom: 16px;
        }}
        .model-block-title {{
            font-size: 0.88rem;
            font-weight: 700;
            color: var(--accent-cyan);
            margin-bottom: 6px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .model-block-content {{
            font-size: 0.94rem;
            line-height: 1.7;
            color: #e2e8f0;
            background: rgba(0,0,0,0.25);
            padding: 12px 16px;
            border-radius: 8px;
            border-left: 3px solid var(--accent-cyan);
        }}
        .model-block-content ul {{
            padding-left: 18px;
        }}
        .model-block-content li {{
            margin-bottom: 6px;
        }}

        /* Self-Evaluation Rubric */
        .rubric-box {{
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 8px;
            padding: 16px;
            margin-top: 18px;
        }}
        .rubric-title {{
            font-size: 0.95rem;
            font-weight: 700;
            color: var(--accent-gold);
            margin-bottom: 10px;
        }}
        .rubric-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
            font-size: 0.88rem;
            color: #e2e8f0;
            cursor: pointer;
        }}
        .rubric-item input {{
            accent-color: var(--accent-gold);
            width: 17px;
            height: 17px;
        }}
    </style>
</head>
<body>

    <!-- Top Navigation Header -->
    <header class="top-navbar">
        <a href="/" class="brand-box">
            <span class="brand-icon">✍️</span>
            <div class="brand-text">
                <h1>లక్ష్య మెయిన్స్ డిస్క్రిప్టివ్ ఆన్సర్ రైటింగ్ పోర్టల్</h1>
                <p>APPSC & TSPSC Group-1 / Group-2 మోడల్ ఆన్సర్స్ & ఎవాల్యుయేషన్</p>
            </div>
        </a>
        <div class="nav-actions">
            <a href="/frontend/pdfs/appsc_mains_answer_writing_handbook.pdf" target="_blank" class="nav-btn pdf-btn">
                📄 మాస్టర్ హ్యాండ్‌బుక్ PDF
            </a>
            <a href="/" class="nav-btn">🏠 హోమ్ డ్యాష్‌బోర్డ్</a>
        </div>
    </header>

    <div class="container">
        <!-- Hero Introduction -->
        <section class="hero-section">
            <h2><span>📑</span> మెయిన్స్ ఆన్సర్ రైటింగ్ డిజిటల్ ప్యాడ్ – మోడల్ సమాధానాలతో స్వీయ విశ్లేషణ</h2>
            <p>
                మెయిన్స్ పరీక్షలో అధిక మార్కులు సాధించాలంటే కేవలం చదవడం మాత్రమే సరిపోదు; సమయ పరిమితిలో (10-15 నిమిషాలు) నిర్దిష్ట పదాల పరిధిలో (150-200 పదాలు) ఆన్సర్ నిర్మించడం అత్యంత ముఖ్యం. 
                ఇక్కడ ప్రశ్నను ఎంచుకుని టైమర్ ఆన్ చేసి రాయడం ప్రారంభించండి, ఆపై అధికారిక మోడల్ సమాధానంతో సరిచూసుకోండి!
            </p>
        </section>

        <!-- Paper Filter Pills -->
        <div class="filter-row">
            <button class="paper-pill active" onclick="filterPaper('all')">అన్ని పేపర్లు ({len(MAINS_QUESTIONS)})</button>
            <button class="paper-pill" onclick="filterPaper('Paper-I')">పేపర్-1: సమాజం & మహిళలు</button>
            <button class="paper-pill" onclick="filterPaper('Paper-II')">పేపర్-2: పాలిటీ & చరిత్ర</button>
            <button class="paper-pill" onclick="filterPaper('Paper-III')">పేపర్-3: ఆర్థిక వ్యవస్థ & అభివృద్ధి</button>
            <button class="paper-pill" onclick="filterPaper('Paper-IV')">పేపర్-4: సైన్స్ & విపత్తులు</button>
        </div>

        <!-- Main Workspace -->
        <div class="workspace-grid">
            <!-- Sidebar: Questions -->
            <aside class="questions-sidebar">
                <div class="sidebar-title">
                    <span>ప్రశ్నల జాబితా ({len(MAINS_QUESTIONS)})</span>
                    <span style="font-size:0.75rem; color:var(--text-muted);">క్లిక్ చేసి రాయండి</span>
                </div>
                <div id="questionsList">
                    <!-- Injected by JS -->
                </div>
            </aside>

            <!-- Writing Pad Area -->
            <main class="main-writing-area">
                <!-- Selected Question Display -->
                <div class="active-question-card">
                    <span class="aq-badge" id="aqPaper">Paper-III: Economy</span>
                    <h3 class="aq-text" id="aqText">ప్రశ్న లోడ్ అవుతోంది...</h3>
                    <div class="aq-details">
                        <span>🎯 సబ్జెక్ట్: <b id="aqSubj" style="color:#ffffff;">-</b></span>
                        <span>⏱️ కాలపరిమితి: <b id="aqTimeLimit" style="color:var(--accent-gold);">10 నిమిషాలు</b></span>
                        <span>📝 పరిమితి: <b id="aqWordLimit" style="color:var(--accent-cyan);">150 పదాలు</b></span>
                    </div>
                </div>

                <!-- Writing Tools & Timer Bar -->
                <div class="tools-bar">
                    <div class="timer-box">
                        <span class="timer-display" id="timerDisplay">10:00</span>
                        <button class="btn-tool" id="btnTimerToggle" onclick="toggleTimer()">▶ ప్రారంభించు</button>
                        <button class="btn-tool" onclick="resetTimer()">🔄 రీసెట్</button>
                    </div>
                    <div class="word-stats">
                        <span>పదాలు: <span class="word-badge" id="lblWordCount">0</span> / <span id="lblTargetWords">150</span></span>
                        <span>అక్షరాలు: <b id="lblCharCount" style="color:#ffffff;">0</b></span>
                    </div>
                </div>

                <!-- Textarea -->
                <textarea 
                    class="writing-pad" 
                    id="txtAnswerPad" 
                    placeholder="మీ సమాధానాన్ని ఇక్కడ తెలుగులో టైప్ చేయండి... (పరిచయం, ముఖ్య విశ్లేషణ, ప్రభుత్వ చర్యలు, ముగింపు క్రమంలో నిర్మించండి)"
                    oninput="updateWordStats()"
                ></textarea>

                <!-- Actions -->
                <div class="action-row">
                    <div style="display:flex; gap:8px;">
                        <button class="btn-tool" onclick="saveCurrentDraft()">💾 డ్రాఫ్ట్ సేవ్</button>
                        <button class="btn-tool" onclick="exportAnswer()">📥 సేవ్ .txt</button>
                    </div>
                    <button class="btn-compare" onclick="toggleModelAnswer()">
                        🔍 మోడల్ సమాధానంతో సరిచూడండి
                    </button>
                </div>

                <!-- Model Answer Display -->
                <div class="model-answer-section" id="modelAnswerSec">
                    <div class="model-header">
                        <h3>🏆 అధికారిక మోడల్ సమాధానం & విశ్లేషణ</h3>
                        <button class="btn-tool" onclick="toggleModelAnswer()">✕ మూసివేయి</button>
                    </div>

                    <div class="model-block">
                        <div class="model-block-title">1. పరిచయం (Introduction & Context)</div>
                        <div class="model-block-content" id="modelIntro"></div>
                    </div>

                    <div class="model-block">
                        <div class="model-block-title">2. ప్రధాన విశ్లేషణ & అంశాలు (Core Body Points)</div>
                        <div class="model-block-content" id="modelBody"></div>
                    </div>

                    <div class="model-block">
                        <div class="model-block-title">3. ప్రభుత్వ చర్యలు & రాజ్యాంగ రక్షణలు (Govt Initiatives)</div>
                        <div class="model-block-content" id="modelGovt"></div>
                    </div>

                    <div class="model-block">
                        <div class="model-block-title">4. ముగింపు & ముందున్న మార్గం (Way Forward & Conclusion)</div>
                        <div class="model-block-content" id="modelConclusion"></div>
                    </div>

                    <!-- Self Evaluation Rubric -->
                    <div class="rubric-box">
                        <div class="rubric-title">📊 మీ సమాధానం స్వీయ మూల్యాంకన చెక్‌లిస్ట్ (Self Evaluation Rubric):</div>
                        <label class="rubric-item">
                            <input type="checkbox" onchange="calcSelfScore()">
                            <span>పరిచయంలో అంశం యొక్క నేపథ్యం / డెఫినిషన్ స్పష్టంగా రాయబడిందా? (2 మార్కులు)</span>
                        </label>
                        <label class="rubric-item">
                            <input type="checkbox" onchange="calcSelfScore()">
                            <span>ప్రధాన భాగంలో గణాంకాలు, కమిటీల సిఫార్సులు పొందుపరిచారా? (4 మార్కులు)</span>
                        </label>
                        <label class="rubric-item">
                            <input type="checkbox" onchange="calcSelfScore()">
                            <span>ప్రభుత్వ పథకాలు లేదా రాజ్యాంగ ఆర్టికల్స్ ప్రస్తావించారా? (2 మార్కులు)</span>
                        </label>
                        <label class="rubric-item">
                            <input type="checkbox" onchange="calcSelfScore()">
                            <span>ఆశావాద మరియు నిర్మాణాత్మక ముగింపు ఇచ్చారా? (2 మార్కులు)</span>
                        </label>
                        <div style="margin-top:10px; font-weight:700; color:var(--accent-gold);">
                            స్వీయ స్కోరు: <span id="lblScore">0</span> / 10 మార్కులు
                        </div>
                    </div>
                </div>
            </main>
        </div>
    </div>

    <script>
        const ALL_QUESTIONS = {questions_json};
        let currentQIndex = 0;
        let activeFilter = 'all';
        let timerSec = 600; // 10 mins default
        let timerInterval = null;
        let isTimerRunning = false;

        function init() {{
            renderQuestionsList();
            loadQuestion(0);
        }}

        function filterPaper(paper) {{
            activeFilter = paper;
            document.querySelectorAll('.paper-pill').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            renderQuestionsList();
        }}

        function renderQuestionsList() {{
            const listEl = document.getElementById('questionsList');
            const filtered = ALL_QUESTIONS.filter(q => {{
                if (activeFilter === 'all') return true;
                return q.paper.startsWith(activeFilter);
            }});

            listEl.innerHTML = filtered.map((q, i) => {{
                const globalIndex = ALL_QUESTIONS.findIndex(x => x.id === q.id);
                const isSelected = globalIndex === currentQIndex;
                return `
                <div class="q-item-card ${{isSelected ? 'selected' : ''}}" onclick="loadQuestion(${{globalIndex}})">
                    <div class="q-item-meta">${{q.paper}}</div>
                    <div class="q-item-title">${{q.question}}</div>
                </div>
                `;
            }}).join('');
        }}

        function loadQuestion(index) {{
            // Save draft of previous before switching
            saveCurrentDraft();

            currentQIndex = index;
            const q = ALL_QUESTIONS[index];
            if (!q) return;

            document.getElementById('aqPaper').textContent = q.paper;
            document.getElementById('aqText').textContent = q.question;
            document.getElementById('aqSubj').textContent = q.subject;
            
            // Set word limit & timer
            const is15m = q.question.includes('200') || q.question.includes('15 మార్కులు');
            const targetWords = is15m ? 200 : 150;
            const targetMinutes = is15m ? 15 : 10;

            document.getElementById('aqWordLimit').textContent = targetWords + ' పదాలు';
            document.getElementById('aqTimeLimit').textContent = targetMinutes + ' నిమిషాలు';
            document.getElementById('lblTargetWords').textContent = targetWords;

            // Reset Timer
            resetTimer(targetMinutes * 60);

            // Populate Model Answer
            document.getElementById('modelIntro').textContent = q.model_answer.intro;
            
            const bodyHtml = '<ul>' + q.model_answer.body_points.map(pt => `<li>${{pt}}</li>`).join('') + '</ul>';
            document.getElementById('modelBody').innerHTML = bodyHtml;

            document.getElementById('modelGovt').textContent = q.model_answer.govt_steps;
            document.getElementById('modelConclusion').textContent = q.model_answer.conclusion;

            // Hide Model answer on new load
            document.getElementById('modelAnswerSec').style.display = 'none';

            // Load student's saved draft from localStorage
            const savedAnswer = localStorage.getItem('mains_draft_' + q.id) || '';
            document.getElementById('txtAnswerPad').value = savedAnswer;
            updateWordStats();

            // Refresh selection highlight
            renderQuestionsList();
        }}

        function updateWordStats() {{
            const text = document.getElementById('txtAnswerPad').value.trim();
            const words = text === '' ? 0 : text.split(/\\s+/).length;
            document.getElementById('lblWordCount').textContent = words;
            document.getElementById('lblCharCount').textContent = text.length;

            const target = parseInt(document.getElementById('lblTargetWords').textContent) || 150;
            const badge = document.getElementById('lblWordCount');
            if (words > target + 20) {{
                badge.style.color = 'var(--accent-rose)';
            }} else if (words >= target - 20) {{
                badge.style.color = 'var(--accent-emerald)';
            }} else {{
                badge.style.color = 'var(--accent-gold)';
            }}
        }}

        function saveCurrentDraft() {{
            const q = ALL_QUESTIONS[currentQIndex];
            if (!q) return;
            const text = document.getElementById('txtAnswerPad').value;
            localStorage.setItem('mains_draft_' + q.id, text);
        }}

        function toggleModelAnswer() {{
            const sec = document.getElementById('modelAnswerSec');
            if (sec.style.display === 'block') {{
                sec.style.display = 'none';
            }} else {{
                sec.style.display = 'block';
                sec.scrollIntoView({{ behavior: 'smooth' }});
            }}
        }}

        function toggleTimer() {{
            if (isTimerRunning) {{
                clearInterval(timerInterval);
                isTimerRunning = false;
                document.getElementById('btnTimerToggle').textContent = '▶ కొనసాగించు';
            }} else {{
                isTimerRunning = true;
                document.getElementById('btnTimerToggle').textContent = '⏸ పాజ్';
                timerInterval = setInterval(() => {{
                    if (timerSec > 0) {{
                        timerSec--;
                        renderTimer();
                    }} else {{
                        clearInterval(timerInterval);
                        isTimerRunning = false;
                        document.getElementById('btnTimerToggle').textContent = 'సమయం ముగిసింది';
                        alert('సమయం ముగిసింది! మీ సమాధానాన్ని పూర్తి చేసి మోడల్ ఆన్సర్‌తో సరిచూసుకోండి.');
                    }}
                }}, 1000);
            }}
        }}

        function resetTimer(newSeconds = null) {{
            clearInterval(timerInterval);
            isTimerRunning = false;
            document.getElementById('btnTimerToggle').textContent = '▶ ప్రారంభించు';
            if (newSeconds !== null) {{
                timerSec = newSeconds;
            }} else {{
                const is15m = ALL_QUESTIONS[currentQIndex].question.includes('200');
                timerSec = is15m ? 900 : 600;
            }}
            renderTimer();
        }}

        function renderTimer() {{
            const m = Math.floor(timerSec / 60);
            const s = timerSec % 60;
            document.getElementById('timerDisplay').textContent = 
                (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
        }}

        function exportAnswer() {{
            const q = ALL_QUESTIONS[currentQIndex];
            const text = document.getElementById('txtAnswerPad').value;
            if (!text.trim()) {{
                alert('దయచేసి ఎగుమతి చేయడానికి ముందు కొంత సమాధానాన్ని టైప్ చేయండి.');
                return;
            }}
            const content = `APPSC / TSPSC MAINS DESCRIPTIVE ANSWER\n\nPaper: ${{q.paper}}\nSubject: ${{q.subject}}\nQuestion: ${{q.question}}\n\nMy Answer:\n${{text}}\n\nGenerated via Lakshya Telugu Current Affairs Portal`;
            const blob = new Blob([content], {{ type: 'text/plain;charset=utf-8' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `mains_answer_${{q.id}}.txt`;
            a.click();
        }}

        function calcSelfScore() {{
            const checked = document.querySelectorAll('.rubric-item input:checked').length;
            const marksPerItem = [2, 4, 2, 2];
            let score = 0;
            const checkboxes = document.querySelectorAll('.rubric-item input');
            checkboxes.forEach((cb, idx) => {{
                if (cb.checked) {{
                    score += marksPerItem[idx];
                }}
            }});
            document.getElementById('lblScore').textContent = score;
        }}

        window.onload = init;
    </script>
</body>
</html>
"""
    return html
