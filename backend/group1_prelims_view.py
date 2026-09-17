# -*- coding: utf-8 -*-
"""
APPSC Group-1 Prelims (240 Marks) Mega Grand Simulator View.
Paper 1 (120 Marks) & Paper 2 (120 Marks) with APPSC negative marking (-0.33).
"""

import json
try:
    from group1_prelims_data import GROUP1_SYLLABUS, GROUP1_REVISION_NOTES, GROUP1_QUESTIONS
except ImportError:
    from backend.group1_prelims_data import GROUP1_SYLLABUS, GROUP1_REVISION_NOTES, GROUP1_QUESTIONS

def render_group1_prelims_html():
    syllabus_json = json.dumps(GROUP1_SYLLABUS, ensure_ascii=False)
    notes_json = json.dumps(GROUP1_REVISION_NOTES, ensure_ascii=False)
    questions_json = json.dumps(GROUP1_QUESTIONS, ensure_ascii=False)

    return f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎯 APPSC Group-1 ప్రిలిమ్స్ (240 Marks) మెగా గ్రాండ్ సిమ్యులేటర్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body {{
            font-family: 'Outfit', 'Mandali', sans-serif;
            background-color: #0b132b;
            color: #f8fafc;
        }}
        .telugu-font {{
            font-family: 'Mandali', sans-serif;
        }}
        .palette-btn {{
            width: 32px;
            height: 32px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: bold;
            border-radius: 8px;
            transition: all 0.15s ease;
        }}
        .palette-btn.unvisited {{
            background-color: #1e293b;
            color: #94a3b8;
            border: 1px solid #334155;
        }}
        .palette-btn.answered {{
            background-color: #059669;
            color: #ffffff;
            border: 1px solid #10b981;
        }}
        .palette-btn.unanswered {{
            background-color: #e11d48;
            color: #ffffff;
            border: 1px solid #f43f5e;
        }}
        .palette-btn.review {{
            background-color: #7c3aed;
            color: #ffffff;
            border: 1px solid #8b5cf6;
        }}
        .palette-btn.active {{
            outline: 2px solid #f59e0b;
            outline-offset: 2px;
        }}
        .hide-tab {{
            display: none !important;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col">
    <!-- Header -->
    <header class="bg-slate-900/90 border-b border-slate-800 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 py-3 sm:px-6 flex flex-wrap justify-between items-center gap-3">
            <div class="flex items-center gap-3">
                <a href="/" class="p-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 transition-all text-xs flex items-center gap-1.5">
                    <i class="fa-solid fa-arrow-left"></i> హోమ్
                </a>
                <div class="w-9 h-9 rounded-xl bg-amber-500/20 border border-amber-400/30 flex items-center justify-center text-amber-400 font-black text-sm">
                    G1
                </div>
                <div>
                    <h1 class="text-base sm:text-lg font-black text-white">APPSC Group-1 ప్రిలిమ్స్ గ్రాండ్ సిమ్యులేటర్</h1>
                    <p class="text-[11px] text-amber-300">మొత్తం: 240 మార్కులు (పేపర్-1: 120M | పేపర్-2: 120M) | నెగెటివ్ మార్కింగ్: -0.33</p>
                </div>
            </div>
            
            <div class="flex items-center gap-2.5">
                <div class="bg-slate-800 border border-slate-700 rounded-xl px-3 py-1.5 flex items-center gap-2">
                    <i class="fa-solid fa-clock text-amber-400 text-sm"></i>
                    <span id="timer-display" class="font-mono font-bold text-sm text-white">120:00</span>
                </div>
                <button id="toggle-tabs-btn" onclick="toggleHeaderTabs()" class="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition-all">
                    <i class="fa-solid fa-expand"></i> <span>ట్యాబ్స్ దాచు / చూపించు</span>
                </button>
                <button onclick="confirmSubmitTest()" class="px-3.5 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 shadow-lg shadow-emerald-600/20 transition-all">
                    <i class="fa-solid fa-paper-plane"></i> సబ్మిట్ పరీక్ష
                </button>
            </div>
        </div>
    </header>

    <!-- Navigation Sub-bar -->
    <nav id="sub-nav-bar" class="bg-slate-950/80 border-b border-slate-800 px-4 py-2">
        <div class="max-w-7xl mx-auto flex items-center justify-between overflow-x-auto gap-3">
            <div class="flex items-center gap-2">
                <button onclick="switchView('exam')" id="btn-view-exam" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-amber-500 text-slate-950 transition-all">
                    <i class="fa-solid fa-desktop mr-1"></i> CBT ఎగ్జామ్ రూమ్
                </button>
                <button onclick="switchView('notes')" id="btn-view-notes" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition-all">
                    <i class="fa-solid fa-book-open mr-1"></i> 8 యూనిట్ల రివిజన్ నోట్స్
                </button>
                <button onclick="switchView('analysis')" id="btn-view-analysis" class="px-3 py-1.5 rounded-lg text-xs font-bold bg-slate-800 text-slate-300 hover:bg-slate-700 transition-all">
                    <i class="fa-solid fa-chart-pie mr-1"></i> పరీక్ష ఫలితాలు & ర్యాంకు
                </button>
            </div>

            <!-- Paper Toggle in Exam Mode -->
            <div id="paper-toggle-strip" class="flex items-center gap-1 bg-slate-900 p-1 rounded-xl border border-slate-800">
                <button onclick="switchPaper(1)" id="btn-paper-1" class="px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white transition-all">
                    పేపర్-1 (GS 120M)
                </button>
                <button onclick="switchPaper(2)" id="btn-paper-2" class="px-3 py-1 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition-all">
                    పేపర్-2 (సైన్స్ & ఆప్టిట్యూడ్ 120M)
                </button>
            </div>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6">
        <!-- 1. EXAM ROOM VIEW -->
        <div id="view-exam" class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <!-- Question Question Card (Left 8 cols) -->
            <div class="lg:col-span-8 flex flex-col justify-between bg-slate-900/90 border border-slate-800 rounded-3xl p-6 sm:p-8 min-h-[520px] shadow-xl">
                <div>
                    <!-- Meta Header -->
                    <div class="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
                        <div class="flex items-center gap-2">
                            <span id="current-paper-label" class="px-2.5 py-1 rounded-md bg-blue-500/20 text-blue-400 border border-blue-500/30 text-xs font-bold">పేపర్ 1</span>
                            <span class="text-xs text-slate-400">ప్రశ్న సంఖ్య: <b id="current-q-num" class="text-white text-sm">1</b> / 120</span>
                        </div>
                        <div class="flex items-center gap-2 text-xs">
                            <span class="text-emerald-400 font-bold">+1.0 మార్కు</span>
                            <span class="text-slate-600">|</span>
                            <span class="text-rose-400 font-bold">-0.33 నెగెటివ్</span>
                        </div>
                    </div>

                    <!-- Question Text -->
                    <h3 id="q-text" class="text-base sm:text-lg font-bold text-slate-100 leading-relaxed mb-6">
                        <!-- Loaded dynamically -->
                    </h3>

                    <!-- Options Container -->
                    <div id="q-options" class="space-y-3 mb-6">
                        <!-- Loaded dynamically -->
                    </div>
                </div>

                <!-- Bottom Navigation Buttons -->
                <div class="flex flex-wrap items-center justify-between gap-3 pt-4 border-t border-slate-800">
                    <div class="flex items-center gap-2">
                        <button onclick="markForReview()" class="px-3.5 py-2 rounded-xl bg-purple-950/80 text-purple-300 hover:bg-purple-900 border border-purple-800 text-xs font-semibold transition-all flex items-center gap-1.5">
                            <i class="fa-solid fa-bookmark"></i> మార్క్ ఫర్ రివ్యూ
                        </button>
                        <button onclick="clearResponse()" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-semibold border border-slate-700 transition-all">
                            సమాధానం రద్దు
                        </button>
                    </div>

                    <div class="flex items-center gap-2">
                        <button onclick="prevQuestion()" id="btn-prev" class="px-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold border border-slate-700 transition-all flex items-center gap-1.5">
                            <i class="fa-solid fa-chevron-left"></i> వెనుకకు
                        </button>
                        <button onclick="nextQuestion()" id="btn-next" class="px-5 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 text-xs font-bold shadow-lg shadow-amber-500/20 transition-all flex items-center gap-1.5">
                            తదుపరి <i class="fa-solid fa-chevron-right"></i>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Question Palette (Right 4 cols) -->
            <div class="lg:col-span-4 bg-slate-900/90 border border-slate-800 rounded-3xl p-5 shadow-xl flex flex-col justify-between">
                <div>
                    <h4 class="text-sm font-bold text-slate-200 mb-3 flex items-center justify-between">
                        <span>ప్రశ్నల ప్యాలెట్ (Question Palette)</span>
                        <span id="palette-paper-badge" class="text-xs text-amber-400 font-semibold">పేపర్ 1</span>
                    </h4>

                    <!-- Palette Legend -->
                    <div class="grid grid-cols-2 gap-2 text-[10.5px] text-slate-400 mb-4 bg-slate-950 p-2.5 rounded-xl border border-slate-800">
                        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-emerald-600"></span> సమాధానమిచ్చినవి (<span id="count-answered">0</span>)</div>
                        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-rose-600"></span> సమాధానం ఇవ్వనివి (<span id="count-unanswered">0</span>)</div>
                        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-purple-600"></span> రివ్యూ లో ఉంచినవి (<span id="count-review">0</span>)</div>
                        <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-slate-800 border border-slate-700"></span> చూడనివి (<span id="count-unvisited">120</span>)</div>
                    </div>

                    <!-- Scrollable Buttons Grid -->
                    <div id="palette-grid" class="grid grid-cols-6 sm:grid-cols-8 lg:grid-cols-6 gap-2 max-h-[360px] overflow-y-auto pr-1 scrollbar-thin">
                        <!-- Loaded dynamically -->
                    </div>
                </div>

                <div class="pt-4 border-t border-slate-800 mt-4">
                    <button onclick="confirmSubmitTest()" class="w-full py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs transition-all flex items-center justify-center gap-2">
                        <i class="fa-solid fa-circle-check"></i> మొత్తం 240 మార్కులకు సబ్మిట్ చేయండి
                    </button>
                </div>
            </div>
        </div>

        <!-- 2. REVISION NOTES VIEW -->
        <div id="view-notes" class="hidden space-y-6">
            <div class="bg-gradient-to-r from-blue-900/40 to-slate-900 border border-blue-800/40 rounded-3xl p-6 sm:p-8">
                <h3 class="text-xl sm:text-2xl font-black text-white mb-2">APPSC Group-1 ప్రిలిమ్స్ 8 యూనిట్ల సమగ్ర రివిజన్ నోట్స్</h3>
                <p class="text-slate-300 text-xs sm:text-sm">ప్రిలిమ్స్ పరీక్షకు వెళ్లే ముందు తప్పక చదవాల్సిన హై-యీల్డ్ పాయింట్లు, చారిత్రక రాజవంశాలు, రాజ్యాంగ ఆర్టికల్స్, ఎకానమీ మరియు సైన్స్ సంక్షిప్త విశ్లేషణ.</p>
            </div>

            <div id="notes-cards-container" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <!-- Dynamically populated -->
            </div>
        </div>

        <!-- 3. RESULTS & ANALYSIS VIEW -->
        <div id="view-analysis" class="hidden">
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8 mb-6">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 pb-6 border-b border-slate-800">
                    <div>
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/30">APPSC GROUP-1 PRELIMS SCORECARD</span>
                        <h2 class="text-2xl sm:text-3xl font-black text-white mt-2">పరీక్ష ఫలితాలు & పనితీరు విశ్లేషణ</h2>
                        <p class="text-xs text-slate-400 mt-1">నెగెటివ్ మార్కింగ్ (-0.33) లెక్కించబడిన వాస్తవ మార్కులు</p>
                    </div>
                    <div class="bg-slate-950 border border-slate-800 px-6 py-4 rounded-2xl text-center">
                        <div class="text-xs text-slate-400 font-bold">గ్రాండ్ టోటల్ స్కోరు</div>
                        <div id="final-total-score" class="text-3xl sm:text-4xl font-black text-amber-400">0.00 / 240</div>
                        <div id="final-percentage" class="text-xs font-bold text-emerald-400 mt-0.5">0.0%</div>
                    </div>
                </div>

                <!-- Paper Breakdown Cards -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
                    <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800">
                        <h4 class="text-sm font-bold text-blue-400 mb-2">పేపర్ - 1 (జనరల్ స్టడీస్ - 120M)</h4>
                        <div class="flex justify-between items-center text-xs text-slate-300 mb-1">
                            <span>సరైనవి: <b id="p1-res-correct" class="text-emerald-400">0</b></span>
                            <span>తప్పులు: <b id="p1-res-wrong" class="text-rose-400">0</b></span>
                            <span>వదిలేసినవి: <b id="p1-res-skipped" class="text-slate-500">120</b></span>
                        </div>
                        <div class="text-lg font-black text-white mt-2">మార్కులు: <span id="p1-res-net" class="text-amber-400">0.00</span> / 120</div>
                    </div>

                    <div class="p-5 rounded-2xl bg-slate-950 border border-slate-800">
                        <h4 class="text-sm font-bold text-purple-400 mb-2">పేపర్ - 2 (ఆప్టిట్యూడ్ & సైన్స్ - 120M)</h4>
                        <div class="flex justify-between items-center text-xs text-slate-300 mb-1">
                            <span>సరైనవి: <b id="p2-res-correct" class="text-emerald-400">0</b></span>
                            <span>తప్పులు: <b id="p2-res-wrong" class="text-rose-400">0</b></span>
                            <span>వదిలేసినవి: <b id="p2-res-skipped" class="text-slate-500">120</b></span>
                        </div>
                        <div class="text-lg font-black text-white mt-2">మార్కులు: <span id="p2-res-net" class="text-amber-400">0.00</span> / 120</div>
                    </div>
                </div>

                <!-- Expected Cutoff & Advice Box -->
                <div class="p-5 rounded-2xl bg-blue-950/40 border border-blue-800/40 text-xs sm:text-sm text-blue-200 leading-relaxed">
                    <div class="font-bold flex items-center gap-2 mb-1 text-blue-300 text-sm">
                        <i class="fa-solid fa-calculator"></i> కటాఫ్ & మెయిన్స్ ప్రిపరేషన్ అంచనా:
                    </div>
                    గత APPSC గ్రూప్-1 ప్రిలిమ్స్ ట్రెండ్స్ ప్రకారం, జనరల్/ఓపెన్ కేటగిరీ కటాఫ్ సుమారు 105–115 మార్కుల మధ్య ఉంటుంది. 100+ మార్కులు దాటిన అభ్యర్థులు వెంటనే డిస్క్రిప్టివ్ మెయిన్స్ (Paper-I to Paper-V) కు తీవ్ర సాధన ప్రారంభించాలి.
                </div>
            </div>

            <!-- Review Questions Accordion Container -->
            <div class="bg-slate-900 border border-slate-800 rounded-3xl p-6 sm:p-8">
                <h3 class="text-lg font-bold text-white mb-4">సమగ్ర సమాధానాల కీ & వివరణలు (Detailed Answer Key)</h3>
                <div id="review-questions-container" class="space-y-4">
                    <!-- Populated after submission -->
                </div>
            </div>
        </div>
    </main>

    <script>
        const syllabusData = {syllabus_json};
        const notesData = {notes_json};
        const questionsData = {questions_json};

        let currentPaper = 1;
        let currentQIndex = 0; // 0 to 119
        let responses = {{
            1: Array(120).fill(null),
            2: Array(120).fill(null)
        }};
        let reviewStatus = {{
            1: Array(120).fill(false),
            2: Array(120).fill(false)
        }};
        let visitedStatus = {{
            1: Array(120).fill(false),
            2: Array(120).fill(false)
        }};

        let timeLeftSeconds = 120 * 60;
        let timerInterval = null;
        let testSubmitted = false;

        function startTimer() {{
            timerInterval = setInterval(() => {{
                if (timeLeftSeconds <= 0) {{
                    clearInterval(timerInterval);
                    autoSubmitTest();
                    return;
                }}
                timeLeftSeconds--;
                const mins = Math.floor(timeLeftSeconds / 60);
                const secs = timeLeftSeconds % 60;
                document.getElementById('timer-display').innerText = 
                    `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;
            }}, 1000);
        }}

        function switchView(viewName) {{
            document.getElementById('view-exam').classList.add('hidden');
            document.getElementById('view-notes').classList.add('hidden');
            document.getElementById('view-analysis').classList.add('hidden');

            document.getElementById('btn-view-exam').classList.replace('bg-amber-500', 'bg-slate-800');
            document.getElementById('btn-view-exam').classList.replace('text-slate-950', 'text-slate-300');
            document.getElementById('btn-view-notes').classList.replace('bg-amber-500', 'bg-slate-800');
            document.getElementById('btn-view-notes').classList.replace('text-slate-950', 'text-slate-300');
            document.getElementById('btn-view-analysis').classList.replace('bg-amber-500', 'bg-slate-800');
            document.getElementById('btn-view-analysis').classList.replace('text-slate-950', 'text-slate-300');

            const activeBtn = document.getElementById(`btn-view-${{viewName}}`);
            activeBtn.classList.replace('bg-slate-800', 'bg-amber-500');
            activeBtn.classList.replace('text-slate-300', 'text-slate-950');

            document.getElementById(`view-${{viewName}}`).classList.remove('hidden');

            const paperStrip = document.getElementById('paper-toggle-strip');
            if (viewName === 'exam') {{
                paperStrip.style.display = 'flex';
            }} else {{
                paperStrip.style.display = 'none';
            }}
        }}

        function switchPaper(paperNum) {{
            currentPaper = paperNum;
            currentQIndex = 0;

            const btn1 = document.getElementById('btn-paper-1');
            const btn2 = document.getElementById('btn-paper-2');
            if (paperNum === 1) {{
                btn1.className = 'px-3 py-1 rounded-lg text-xs font-bold bg-blue-600 text-white transition-all';
                btn2.className = 'px-3 py-1 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition-all';
                document.getElementById('current-paper-label').innerText = 'పేపర్ 1';
                document.getElementById('palette-paper-badge').innerText = 'పేపర్ 1';
            }} else {{
                btn2.className = 'px-3 py-1 rounded-lg text-xs font-bold bg-purple-600 text-white transition-all';
                btn1.className = 'px-3 py-1 rounded-lg text-xs font-bold text-slate-400 hover:text-white transition-all';
                document.getElementById('current-paper-label').innerText = 'పేపర్ 2';
                document.getElementById('palette-paper-badge').innerText = 'పేపర్ 2';
            }}

            renderPalette();
            loadQuestion();
        }}

        function loadQuestion() {{
            visitedStatus[currentPaper][currentQIndex] = true;

            const qList = (currentPaper === 1) ? questionsData.paper_1 : questionsData.paper_2;
            const q = qList[currentQIndex];

            document.getElementById('current-q-num').innerText = currentQIndex + 1;
            document.getElementById('q-text').innerText = q.question;

            const container = document.getElementById('q-options');
            container.innerHTML = '';

            q.options.forEach((opt, optIdx) => {{
                const isSelected = responses[currentPaper][currentQIndex] === optIdx;
                const optBtn = document.createElement('button');
                optBtn.className = `w-full text-left p-3.5 rounded-2xl border transition-all flex items-start gap-3 text-sm ${{
                    isSelected ? 'bg-amber-500/20 border-amber-500 text-amber-200' : 'bg-slate-950/60 border-slate-800 text-slate-200 hover:border-slate-700'
                }}`;
                optBtn.onclick = () => selectOption(optIdx);
                optBtn.innerHTML = `
                    <span class="w-6 h-6 rounded-lg ${{isSelected ? 'bg-amber-500 text-slate-950' : 'bg-slate-800 text-slate-400'}} flex items-center justify-center text-xs font-bold shrink-0 mt-0.5">${{String.fromCharCode(65 + optIdx)}}</span>
                    <span class="leading-relaxed">${{opt}}</span>
                `;
                container.appendChild(optBtn);
            }});

            document.getElementById('btn-prev').disabled = (currentQIndex === 0);
            document.getElementById('btn-prev').style.opacity = (currentQIndex === 0) ? '0.4' : '1';

            updatePaletteCounts();
            highlightPaletteActive();
        }}

        function selectOption(optIdx) {{
            responses[currentPaper][currentQIndex] = optIdx;
            loadQuestion();
            renderPalette();
        }}

        function clearResponse() {{
            responses[currentPaper][currentQIndex] = null;
            loadQuestion();
            renderPalette();
        }}

        function markForReview() {{
            reviewStatus[currentPaper][currentQIndex] = !reviewStatus[currentPaper][currentQIndex];
            renderPalette();
        }}

        function nextQuestion() {{
            if (currentQIndex < 119) {{
                currentQIndex++;
                loadQuestion();
            }} else if (currentPaper === 1) {{
                // Advance to paper 2
                switchPaper(2);
            }}
        }}

        function prevQuestion() {{
            if (currentQIndex > 0) {{
                currentQIndex--;
                loadQuestion();
            }}
        }}

        function renderPalette() {{
            const grid = document.getElementById('palette-grid');
            grid.innerHTML = '';

            for (let i = 0; i < 120; i++) {{
                const btn = document.createElement('button');
                btn.innerText = i + 1;
                btn.onclick = () => {{
                    currentQIndex = i;
                    loadQuestion();
                }};

                let stateClass = 'unvisited';
                if (reviewStatus[currentPaper][i]) {{
                    stateClass = 'review';
                }} else if (responses[currentPaper][i] !== null) {{
                    stateClass = 'answered';
                }} else if (visitedStatus[currentPaper][i]) {{
                    stateClass = 'unanswered';
                }}

                btn.className = `palette-btn ${{stateClass}}`;
                btn.id = `palette-btn-${{i}}`;
                grid.appendChild(btn);
            }}

            highlightPaletteActive();
            updatePaletteCounts();
        }}

        function highlightPaletteActive() {{
            document.querySelectorAll('.palette-btn').forEach(b => b.classList.remove('active'));
            const activeBtn = document.getElementById(`palette-btn-${{currentQIndex}}`);
            if (activeBtn) activeBtn.classList.add('active');
        }}

        function updatePaletteCounts() {{
            let answered = 0, unanswered = 0, review = 0, unvisited = 0;
            for (let i = 0; i < 120; i++) {{
                if (reviewStatus[currentPaper][i]) review++;
                else if (responses[currentPaper][i] !== null) answered++;
                else if (visitedStatus[currentPaper][i]) unanswered++;
                else unvisited++;
            }}
            document.getElementById('count-answered').innerText = answered;
            document.getElementById('count-unanswered').innerText = unanswered;
            document.getElementById('count-review').innerText = review;
            document.getElementById('count-unvisited').innerText = unvisited;
        }}

        function toggleHeaderTabs() {{
            const subNav = document.getElementById('sub-nav-bar');
            subNav.classList.toggle('hide-tab');
        }}

        function confirmSubmitTest() {{
            if (confirm('మీరు ఖచ్చితంగా మొత్తం 240 మార్కుల పరీక్షను సబ్మిట్ చేయాలనుకుంటున్నారా?')) {{
                submitTest();
            }}
        }}

        function autoSubmitTest() {{
            alert('సమయం ముగిసింది! మీ పరీక్ష ఆటోమేటిక్‌గా సబ్మిట్ చేయబడుతోంది.');
            submitTest();
        }}

        function submitTest() {{
            clearInterval(timerInterval);
            testSubmitted = true;

            // Evaluate Paper 1
            let p1Correct = 0, p1Wrong = 0, p1Skipped = 0;
            questionsData.paper_1.forEach((q, idx) => {{
                const userAns = responses[1][idx];
                if (userAns === null) {{
                    p1Skipped++;
                }} else if (userAns === q.answer) {{
                    p1Correct++;
                }} else {{
                    p1Wrong++;
                }}
            }});
            const p1Net = Math.max(0, (p1Correct * 1.0) - (p1Wrong * 0.33));

            // Evaluate Paper 2
            let p2Correct = 0, p2Wrong = 0, p2Skipped = 0;
            questionsData.paper_2.forEach((q, idx) => {{
                const userAns = responses[2][idx];
                if (userAns === null) {{
                    p2Skipped++;
                }} else if (userAns === q.answer) {{
                    p2Correct++;
                }} else {{
                    p2Wrong++;
                }}
            }});
            const p2Net = Math.max(0, (p2Correct * 1.0) - (p2Wrong * 0.33));

            const totalScore = p1Net + p2Net;
            const percentage = ((totalScore / 240) * 100).toFixed(1);

            // Populate Scorecard
            document.getElementById('final-total-score').innerText = `${{totalScore.toFixed(2)}} / 240`;
            document.getElementById('final-percentage').innerText = `${{percentage}}% శాతము`;

            document.getElementById('p1-res-correct').innerText = p1Correct;
            document.getElementById('p1-res-wrong').innerText = p1Wrong;
            document.getElementById('p1-res-skipped').innerText = p1Skipped;
            document.getElementById('p1-res-net').innerText = p1Net.toFixed(2);

            document.getElementById('p2-res-correct').innerText = p2Correct;
            document.getElementById('p2-res-wrong').innerText = p2Wrong;
            document.getElementById('p2-res-skipped').innerText = p2Skipped;
            document.getElementById('p2-res-net').innerText = p2Net.toFixed(2);

            // Populate Review Questions
            const revContainer = document.getElementById('review-questions-container');
            revContainer.innerHTML = '';

            const appendReviewItems = (paperNum, qList) => {{
                qList.forEach((q, idx) => {{
                    const uAns = responses[paperNum][idx];
                    const isCorrect = (uAns === q.answer);
                    const isSkipped = (uAns === null);

                    const qDiv = document.createElement('div');
                    qDiv.className = `p-4 sm:p-5 rounded-2xl border text-xs sm:text-sm ${{
                        isCorrect ? 'bg-emerald-950/20 border-emerald-800/40' : (isSkipped ? 'bg-slate-950 border-slate-800' : 'bg-rose-950/20 border-rose-800/40')
                    }}`;

                    const uAnsText = isSkipped ? '<span class="text-slate-500">సమాధానం ఇవ్వలేదు</span>' : q.options[uAns];
                    const cAnsText = q.options[q.answer];

                    qDiv.innerHTML = `
                        <div class="flex items-center justify-between mb-2">
                            <span class="font-bold text-amber-400">పేపర్-${{paperNum}} | Q.${{idx + 1}}</span>
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold ${{
                                isCorrect ? 'bg-emerald-500/20 text-emerald-300' : (isSkipped ? 'bg-slate-800 text-slate-400' : 'bg-rose-500/20 text-rose-300')
                            }}">
                                ${{isCorrect ? '✓ సరియైనది (+1.0)' : (isSkipped ? 'వదిలేసినది (0.0)' : '✗ తప్పు (-0.33)')}}
                            </span>
                        </div>
                        <p class="font-semibold text-slate-200 mb-3">${{q.question}}</p>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mb-3">
                            <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                                <span class="text-[10px] text-slate-400 block">మీ సమాధానం:</span>
                                <span class="font-medium ${{isCorrect ? 'text-emerald-400' : 'text-rose-400'}}">${{uAnsText}}</span>
                            </div>
                            <div class="p-2.5 rounded-xl bg-slate-900 border border-slate-800">
                                <span class="text-[10px] text-slate-400 block">సరైన సమాధానం:</span>
                                <span class="font-medium text-emerald-400">${{cAnsText}}</span>
                            </div>
                        </div>
                        <div class="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-slate-300 leading-relaxed text-xs">
                            <b class="text-amber-300">వివరణ:</b> ${{q.explanation}}
                        </div>
                    `;
                    revContainer.appendChild(qDiv);
                }});
            }};

            appendReviewItems(1, questionsData.paper_1);
            appendReviewItems(2, questionsData.paper_2);

            switchView('analysis');
        }}

        function renderNotes() {{
            const notesContainer = document.getElementById('notes-cards-container');
            notesContainer.innerHTML = '';

            notesData.forEach(n => {{
                const card = document.createElement('div');
                card.className = 'bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-sm';
                
                const pts = n.points.map(p => `
                    <li class="mb-2.5 text-xs sm:text-sm text-slate-300 leading-relaxed flex items-start gap-2">
                        <i class="fa-solid fa-circle-check text-amber-400 mt-1 text-xs shrink-0"></i>
                        <span>${{p}}</span>
                    </li>
                `).join('');

                card.innerHTML = `
                    <h4 class="text-base font-bold text-amber-300 pb-3 mb-3 border-b border-slate-800 flex items-center gap-2">
                        <i class="fa-solid fa-layer-group"></i> ${{n.subject}}
                    </h4>
                    <ul class="list-none">
                        ${{pts}}
                    </ul>
                `;
                notesContainer.appendChild(card);
            }});
        }}

        // Initialize
        renderPalette();
        loadQuestion();
        renderNotes();
        startTimer();
    </script>
</body>
</html>
"""
