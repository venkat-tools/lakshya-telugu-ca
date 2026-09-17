# -*- coding: utf-8 -*-
"""
View renderer for Awards, Sports & Key Personalities 2025-2026 Master Hub.
"""
import json
try:
    from awards_sports_data import AWARDS_SPORTS_DATA
except ImportError:
    from backend.awards_sports_data import AWARDS_SPORTS_DATA

def render_awards_sports_html():
    data = AWARDS_SPORTS_DATA
    data_json = json.dumps(data, ensure_ascii=False)
    
    categories_html = ""
    for cat in data["categories"]:
        points_html = "".join([f'<li class="mb-3 text-slate-700 leading-relaxed"><i class="fa-solid fa-circle-check text-amber-500 mr-2 text-sm"></i>{p}</li>' for p in cat["points"]])
        categories_html += f"""
        <div class="category-card bg-white rounded-2xl p-6 shadow-sm border border-slate-200/80 mb-6 hover:shadow-md transition-all" data-category="{cat['id']}">
            <div class="flex items-center gap-3 mb-4 pb-3 border-b border-slate-100">
                <div class="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-lg">
                    <i class="fa-solid {cat['icon']}"></i>
                </div>
                <h3 class="text-xl font-bold text-slate-800">{cat['title']}</h3>
            </div>
            <ul class="list-none pl-1">
                {points_html}
            </ul>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>అవార్డులు, క్రీడలు & ప్రముఖ వ్యక్తులు 2025-2026 | లక్ష్య TSPSC & APPSC</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Mandali&family=Suranna&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif;
            background-color: #f8fafc;
        }}
        .telugu-font {{
            font-family: 'Mandali', sans-serif;
        }}
        .hide-tab {{
            display: none !important;
        }}
    </style>
</head>
<body class="text-slate-800 min-h-screen">
    <!-- Top Header -->
    <header class="bg-gradient-to-r from-amber-700 via-amber-800 to-slate-900 text-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center gap-3">
                <a href="/" class="p-2 rounded-xl bg-white/10 hover:bg-white/20 text-white transition-all text-sm flex items-center gap-2">
                    <i class="fa-solid fa-arrow-left"></i> హోమ్
                </a>
                <div class="w-10 h-10 rounded-xl bg-amber-500/20 border border-amber-400/30 flex items-center justify-center text-amber-300 text-xl">
                    <i class="fa-solid fa-trophy"></i>
                </div>
                <div>
                    <h1 class="text-lg sm:text-2xl font-black tracking-tight">{data["title"]}</h1>
                    <p class="text-xs text-amber-200">APPSC & TSPSC హై-యీల్డ్ కంపైలేషన్ (2024–2026) | 30 ప్రాక్టీస్ MCQs</p>
                </div>
            </div>
            
            <div class="flex items-center gap-2">
                <button id="toggle-tabs-btn" onclick="toggleFullScreenReading()" class="px-3 py-1.5 rounded-lg bg-white/10 hover:bg-white/20 text-xs font-semibold flex items-center gap-1.5 border border-white/10 transition-all">
                    <i class="fa-solid fa-expand"></i> <span>ట్యాబ్స్ దాచు / చూపించు</span>
                </button>
                <a href="/static/pdfs/awards_sports_personalities_2026.pdf" download class="px-4 py-2 rounded-xl bg-amber-500 hover:bg-amber-400 text-slate-950 font-bold text-sm flex items-center gap-2 shadow-lg shadow-amber-500/20 transition-all">
                    <i class="fa-solid fa-file-pdf text-base"></i>
                    <span>PDF డౌన్‌లోడ్</span>
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <!-- Overview Banner -->
        <div class="bg-gradient-to-br from-amber-50 to-orange-50 border border-amber-200 rounded-3xl p-6 sm:p-8 mb-8 shadow-sm">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                <div>
                    <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-amber-200 text-amber-900 mb-2">
                        <i class="fa-solid fa-bullseye"></i> 100% EXAM ORIENTED
                    </span>
                    <h2 class="text-2xl sm:text-3xl font-extrabold text-slate-900 mb-2">అవార్డులు, క్రీడలు & నియామకాలు మెగా డైజెస్ట్</h2>
                    <p class="text-slate-700 max-w-3xl leading-relaxed text-sm sm:text-base">
                        {data["overview"]["summary"]}
                    </p>
                </div>
                <div class="bg-white px-5 py-4 rounded-2xl border border-amber-200 text-center shadow-sm shrink-0">
                    <div class="text-2xl font-black text-amber-700">30 MCQs</div>
                    <div class="text-xs font-bold text-slate-500 mt-0.5">సమగ్ర వివరణలతో</div>
                </div>
            </div>
        </div>

        <!-- Controls: Search & Tabs -->
        <div id="controls-bar" class="flex flex-col lg:flex-row justify-between items-stretch lg:items-center gap-4 mb-6">
            <!-- Filter Tabs -->
            <div class="flex items-center gap-2 overflow-x-auto pb-2 scrollbar-none">
                <button onclick="switchTab('all')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-slate-900 text-white shadow-sm transition-all shrink-0" data-target="all">
                    అన్నీ
                </button>
                <button onclick="switchTab('sec_bharat_ratna_padma')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 transition-all shrink-0" data-target="sec_bharat_ratna_padma">
                    భారతరత్న & పద్మ
                </button>
                <button onclick="switchTab('sec_nobel_2024_2025')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 transition-all shrink-0" data-target="sec_nobel_2024_2025">
                    నోబెల్ బహుమతులు
                </button>
                <button onclick="switchTab('sec_cinema_literature')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 transition-all shrink-0" data-target="sec_cinema_literature">
                    సినిమా & సాహిత్యం
                </button>
                <button onclick="switchTab('sec_sports_olympics')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 transition-all shrink-0" data-target="sec_sports_olympics">
                    ఒలింపిక్స్ & పారాలింపిక్స్
                </button>
                <button onclick="switchTab('sec_cricket_chess')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 transition-all shrink-0" data-target="sec_cricket_chess">
                    క్రికెట్ & చెస్
                </button>
                <button onclick="switchTab('sec_appointments_personalities')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-white text-slate-600 hover:bg-slate-100 border border-slate-200 transition-all shrink-0" data-target="sec_appointments_personalities">
                    కీలక నియామకాలు
                </button>
                <button onclick="switchTab('tab_mcqs')" class="tab-btn px-4 py-2 rounded-xl text-sm font-bold bg-amber-100 text-amber-900 hover:bg-amber-200 border border-amber-300 transition-all shrink-0" data-target="tab_mcqs">
                    🎯 30 ప్రాక్టీస్ MCQs
                </button>
            </div>

            <!-- Live Search Bar -->
            <div class="relative w-full lg:w-72">
                <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-3.5 text-slate-400 text-sm"></i>
                <input type="text" id="searchInput" onkeyup="filterContent()" placeholder="టాపిక్ లేదా పేరును శోధించండి..." class="w-full pl-10 pr-4 py-2 text-sm bg-white border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-amber-500 transition-all">
            </div>
        </div>

        <!-- Notes Content Container -->
        <div id="notes-view">
            {categories_html}
        </div>

        <!-- MCQs Practice View (Hidden by Default until tab clicked) -->
        <div id="mcqs-view" class="hidden">
            <div class="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm mb-6">
                <div class="flex flex-wrap justify-between items-center gap-4 pb-6 mb-6 border-b border-slate-100">
                    <div>
                        <h3 class="text-xl font-black text-slate-900">🎯 30 ప్రాక్టీస్ మాక్ ప్రశ్నలు (APPSC / TSPSC లెవల్)</h3>
                        <p class="text-xs text-slate-500 mt-1">సరియైన సమాధానాన్ని ఎంచుకోండి, వెంటనే సాధన ఫలితం మరియు సమగ్ర వివరణను చూడండి.</p>
                    </div>
                    <div class="flex items-center gap-3">
                        <div class="px-4 py-2 rounded-xl bg-slate-900 text-white font-bold text-sm">
                            స్కోరు: <span id="quiz-score" class="text-amber-400">0</span> / 30
                        </div>
                        <button onclick="resetQuiz()" class="px-3 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-all">
                            <i class="fa-solid fa-rotate-right mr-1"></i> రీసెట్
                        </button>
                    </div>
                </div>

                <div id="mcq-list" class="space-y-6">
                    <!-- Loaded dynamically via JS -->
                </div>
            </div>
        </div>
    </main>

    <script>
        const appData = {data_json};
        let userAnswers = {{}};
        let currentScore = 0;

        function switchTab(tabId) {{
            // Update active tab button style
            document.querySelectorAll('.tab-btn').forEach(btn => {{
                if (btn.getAttribute('data-target') === tabId) {{
                    btn.classList.add('bg-slate-900', 'text-white');
                    btn.classList.remove('bg-white', 'text-slate-600', 'bg-amber-100', 'text-amber-900');
                }} else {{
                    btn.classList.remove('bg-slate-900', 'text-white');
                    if (btn.getAttribute('data-target') === 'tab_mcqs') {{
                        btn.classList.add('bg-amber-100', 'text-amber-900');
                    }} else {{
                        btn.classList.add('bg-white', 'text-slate-600');
                    }}
                }}
            }});

            const notesView = document.getElementById('notes-view');
            const mcqsView = document.getElementById('mcqs-view');

            if (tabId === 'tab_mcqs') {{
                notesView.classList.add('hidden');
                mcqsView.classList.remove('hidden');
            }} else {{
                mcqsView.classList.add('hidden');
                notesView.classList.remove('hidden');

                const cards = document.querySelectorAll('.category-card');
                cards.forEach(card => {{
                    if (tabId === 'all' || card.getAttribute('data-category') === tabId) {{
                        card.style.display = 'block';
                    }} else {{
                        card.style.display = 'none';
                    }}
                }});
            }}
        }}

        function filterContent() {{
            const q = document.getElementById('searchInput').value.toLowerCase();
            const cards = document.querySelectorAll('.category-card');
            cards.forEach(card => {{
                const text = card.innerText.toLowerCase();
                if (text.includes(q)) {{
                    card.style.display = 'block';
                }} else {{
                    card.style.display = 'none';
                }}
            }});
        }}

        function toggleFullScreenReading() {{
            const controls = document.getElementById('controls-bar');
            controls.classList.toggle('hide-tab');
        }}

        function renderMCQs() {{
            const container = document.getElementById('mcq-list');
            container.innerHTML = '';
            
            appData.mcqs.forEach((mcq, idx) => {{
                const card = document.createElement('div');
                card.className = 'p-5 sm:p-6 rounded-2xl bg-slate-50 border border-slate-200/80 transition-all';
                card.id = `q-card-${{idx}}`;

                let optionsHtml = '';
                mcq.options.forEach((opt, optIdx) => {{
                    optionsHtml += `
                        <button onclick="selectOption(${{idx}}, ${{optIdx}})" id="opt-btn-${{idx}}-${{optIdx}}" class="w-full text-left p-3.5 rounded-xl border border-slate-200 bg-white hover:border-amber-400 text-sm font-medium text-slate-700 transition-all flex items-start gap-3">
                            <span class="w-6 h-6 rounded-full bg-slate-100 flex items-center justify-center text-xs font-bold shrink-0 text-slate-600 mt-0.5">${{String.fromCharCode(65 + optIdx)}}</span>
                            <span>${{opt}}</span>
                        </button>
                    `;
                }});

                card.innerHTML = `
                    <div class="flex items-start gap-3 mb-4">
                        <span class="w-8 h-8 rounded-xl bg-amber-500 text-slate-950 font-black flex items-center justify-center text-sm shrink-0">${{idx + 1}}</span>
                        <h4 class="text-base font-bold text-slate-900 leading-snug">${{mcq.question}}</h4>
                    </div>
                    <div class="space-y-2.5 mb-4">
                        ${{optionsHtml}}
                    </div>
                    <div id="explanation-${{idx}}" class="hidden p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-950 text-xs sm:text-sm leading-relaxed">
                        <div class="font-bold flex items-center gap-1.5 mb-1 text-emerald-800">
                            <i class="fa-solid fa-lightbulb"></i> సమగ్ర వివరణ:
                        </div>
                        ${{mcq.explanation}}
                    </div>
                `;
                container.appendChild(card);
            }});
        }}

        function selectOption(qIdx, optIdx) {{
            if (userAnswers[qIdx] !== undefined) return; // Already answered
            userAnswers[qIdx] = optIdx;

            const q = appData.mcqs[qIdx];
            const isCorrect = (optIdx === q.answer);
            const selectedBtn = document.getElementById(`opt-btn-${{qIdx}}-${{optIdx}}`);
            const correctBtn = document.getElementById(`opt-btn-${{qIdx}}-${{q.answer}}`);
            const expBox = document.getElementById(`explanation-${{qIdx}}`);

            if (isCorrect) {{
                selectedBtn.classList.add('bg-emerald-50', 'border-emerald-500', 'text-emerald-800');
                currentScore++;
            }} else {{
                selectedBtn.classList.add('bg-rose-50', 'border-rose-500', 'text-rose-800');
                correctBtn.classList.add('bg-emerald-50', 'border-emerald-500', 'text-emerald-800');
            }}

            document.getElementById('quiz-score').innerText = currentScore;
            expBox.classList.remove('hidden');
        }}

        function resetQuiz() {{
            userAnswers = {{}};
            currentScore = 0;
            document.getElementById('quiz-score').innerText = '0';
            renderMCQs();
        }}

        // Initialize
        renderMCQs();
    </script>
</body>
</html>
"""
