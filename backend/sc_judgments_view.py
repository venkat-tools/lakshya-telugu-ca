# -*- coding: utf-8 -*-
"""
Supreme Court 30 Landmark Judgments (1950-2026) Interactive Hub View.
Renders high-yield visual compendium with search, era/category filters, collapsible details, and MCQs.
"""

import json
from sc_judgments_data import SC_LANDMARK_JUDGMENTS

def render_sc_judgments_html():
    judgments_json = json.dumps(SC_LANDMARK_JUDGMENTS, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>⚖️ సుప్రీంకోర్టు 30 చారిత్రక తీర్పులు (1950-2026) | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-primary: #090e1a;
            --bg-card: #111a2e;
            --bg-card-hover: #182542;
            --accent-gold: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-purple: #8b5cf6;
            --accent-rose: #f43f5e;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e293b;
            --radius-md: 12px;
            --radius-lg: 18px;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            -webkit-tap-highlight-color: transparent;
        }}
        body {{
            font-family: 'Outfit', 'Mandali', sans-serif;
            background: linear-gradient(135deg, #060a14 0%, #0d162b 50%, #080e1c 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 90px;
        }}

        /* Navbar */
        .top-navbar {{
            background: rgba(9, 14, 26, 0.95);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border-color);
            position: sticky;
            top: 0;
            z-index: 100;
            padding: 12px 20px;
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
            background: linear-gradient(135deg, #8b5cf6, #3b82f6);
            color: white;
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
        .nav-btn-primary {{
            background: linear-gradient(135deg, #f59e0b, #d97706);
            color: #1e1b4b;
            border: none;
            font-weight: 800;
        }}
        .nav-btn-primary:hover {{
            background: linear-gradient(135deg, #fbbf24, #f59e0b);
            color: #0f172a;
            transform: translateY(-1px);
        }}

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 16px;
        }}

        /* Hero Header */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.15), rgba(59, 130, 246, 0.12));
            border: 1px solid rgba(139, 92, 246, 0.35);
            border-radius: var(--radius-lg);
            padding: 28px 24px;
            margin-bottom: 24px;
            text-align: center;
            position: relative;
            overflow: hidden;
        }}
        .hero-banner h1 {{
            font-size: 1.85rem;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .hero-banner p {{
            font-size: 0.95rem;
            color: var(--text-muted);
            max-width: 820px;
            margin: 0 auto 16px auto;
            line-height: 1.6;
        }}
        .hero-badges {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .hero-badge-pill {{
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            color: #cbd5e1;
            font-weight: 600;
        }}

        /* Search & Filter Bar */
        .controls-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 18px 20px;
            margin-bottom: 24px;
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        .search-box {{
            position: relative;
            width: 100%;
        }}
        .search-box i {{
            position: absolute;
            left: 16px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 1rem;
        }}
        .search-input {{
            width: 100%;
            background: #080d1a;
            border: 1px solid #334155;
            border-radius: var(--radius-md);
            padding: 12px 16px 12px 46px;
            color: white;
            font-size: 0.95rem;
            font-family: inherit;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-input:focus {{
            border-color: var(--accent-cyan);
        }}
        .category-pills {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            padding-bottom: 4px;
            scrollbar-width: none;
        }}
        .category-pills::-webkit-scrollbar {{
            display: none;
        }}
        .cat-pill {{
            background: #0a1122;
            border: 1px solid #1e293b;
            color: var(--text-muted);
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 0.8rem;
            font-weight: 600;
            white-space: nowrap;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .cat-pill:hover, .cat-pill.active {{
            background: var(--accent-purple);
            color: white;
            border-color: var(--accent-purple);
        }}

        /* Judgments Grid / Feed */
        .judgments-grid {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 18px;
        }}
        .judgment-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 22px;
            transition: all 0.2s ease;
            position: relative;
        }}
        .judgment-card:hover {{
            border-color: #3b82f6;
            background: var(--bg-card-hover);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 12px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.07);
            padding-bottom: 12px;
        }}
        .case-title-area {{
            flex: 1;
        }}
        .case-num {{
            font-size: 0.75rem;
            font-weight: 800;
            color: var(--accent-gold);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 4px;
        }}
        .case-name {{
            font-size: 1.2rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.4;
        }}
        .year-badge {{
            background: linear-gradient(135deg, #3b82f6, #1d4ed8);
            color: white;
            padding: 4px 12px;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 800;
            white-space: nowrap;
        }}
        .meta-tags {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}
        .meta-tag {{
            background: #0d1830;
            border: 1px solid #1e3a5f;
            color: #93c5fd;
            font-size: 0.75rem;
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
        }}
        .meta-tag.bench {{
            border-color: #6366f1;
            color: #c7d2fe;
            background: #1e1b4b;
        }}
        .meta-tag.ratio {{
            border-color: #10b981;
            color: #a7f3d0;
            background: #064e3b;
        }}
        .verdict-box {{
            background: #070d1c;
            border-left: 4px solid var(--accent-cyan);
            padding: 14px 16px;
            border-radius: 0 10px 10px 0;
            margin-bottom: 14px;
            font-size: 0.92rem;
            line-height: 1.65;
            color: #e2e8f0;
        }}
        .verdict-box b {{
            color: var(--accent-cyan);
        }}
        .exam-impact-box {{
            background: rgba(245, 158, 11, 0.08);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 0.84rem;
            color: #fde68a;
            margin-bottom: 14px;
            line-height: 1.5;
        }}
        .exam-impact-box b {{
            color: #fbbf24;
        }}

        /* MCQ interactive box */
        .mcq-container {{
            background: #0a1122;
            border: 1px dashed #334155;
            border-radius: var(--radius-md);
            padding: 14px;
            margin-top: 12px;
        }}
        .mcq-title {{
            font-size: 0.8rem;
            font-weight: 800;
            color: #a855f7;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .mcq-question {{
            font-size: 0.88rem;
            font-weight: 700;
            color: #f1f5f9;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .mcq-options {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 6px;
            margin-bottom: 10px;
        }}
        .mcq-opt {{
            background: #111a2e;
            border: 1px solid #1e293b;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.82rem;
            color: #cbd5e1;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .mcq-opt:hover {{
            background: #1e293b;
            border-color: #3b82f6;
        }}
        .mcq-opt.correct {{
            background: rgba(16, 185, 129, 0.2) !important;
            border-color: #10b981 !important;
            color: #34d399 !important;
            font-weight: bold;
        }}
        .mcq-opt.wrong {{
            background: rgba(239, 68, 68, 0.2) !important;
            border-color: #ef4444 !important;
            color: #f87171 !important;
        }}
        .mcq-explanation {{
            background: #050a14;
            border-left: 3px solid #10b981;
            padding: 8px 12px;
            font-size: 0.8rem;
            color: #cbd5e1;
            display: none;
            margin-top: 8px;
            border-radius: 0 6px 6px 0;
            line-height: 1.5;
        }}

        /* Fullscreen toggle */
        .fullscreen-active header,
        .fullscreen-active .top-navbar {{
            display: none !important;
        }}

        @media (max-width: 640px) {{
            .hero-banner h1 {{
                font-size: 1.4rem;
            }}
            .card-header {{
                flex-direction: column;
            }}
            .year-badge {{
                align-self: flex-start;
            }}
            .mcq-options {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>

    <!-- Navbar -->
    <header class="top-navbar" id="mainHeader">
        <a href="/" class="brand-link">
            <span class="brand-badge">లక్ష్య 2026</span>
            <span class="brand-title">⚖️ సుప్రీంకోర్టు 30 తీర్పులు</span>
        </a>
        <div class="nav-actions">
            <button class="nav-btn" onclick="toggleFullScreenMode()" title="ట్యాబ్స్ దాచు / చూపించు">
                <i class="fa-solid fa-expand"></i> <span id="toggleText">పూర్తి స్క్రీన్</span>
            </button>
            <a href="/frontend/pdfs/supreme_court_landmark_cases_handbook.pdf" target="_blank" class="nav-btn nav-btn-primary">
                <i class="fa-solid fa-file-pdf"></i> డౌన్‌లోడ్ PDF
            </a>
            <a href="/" class="nav-btn">
                <i class="fa-solid fa-house"></i> హోమ్
            </a>
        </div>
    </header>

    <div class="container">
        <!-- Hero Banner -->
        <div class="hero-banner">
            <h1>⚖️ సుప్రీంకోర్టు 30 చారిత్రక తీర్పులు (1950–2026)</h1>
            <p>
                స్వతంత్ర భారతదేశ రాజ్యాంగ ప్రస్థానంలో ఏ.కె. గోపాలన్ (1950) నుండి 2024 ఎస్సీ ఉపవర్గీకరణ మరియు ఎలక్టోరల్ బాండ్ల రద్దు వరకు అత్యున్నత ధర్మాసనం వెలువరించిన సమగ్ర మైలురాళ్ళు.
            </p>
            <div class="hero-badges">
                <span class="hero-badge-pill"><i class="fa-solid fa-scale-balanced" style="color:#a855f7;"></i> 30 రాజ్యాంగ తీర్పులు</span>
                <span class="hero-badge-pill"><i class="fa-solid fa-landmark" style="color:#38bdf8;"></i> ధర్మాసనం & మెజారిటీ రేషియో</span>
                <span class="hero-badge-pill"><i class="fa-solid fa-book-open" style="color:#fbbf24;"></i> సంబంధిత ఆర్టికల్స్ & బేసిక్ స్ట్రక్చర్</span>
                <span class="hero-badge-pill"><i class="fa-solid fa-circle-check" style="color:#34d399;"></i> 30 ప్రాక్టీస్ MCQs</span>
            </div>
        </div>

        <!-- Search & Filter Controls -->
        <div class="controls-panel">
            <div class="search-box">
                <i class="fa-solid fa-magnifying-glass"></i>
                <input type="text" id="judgmentSearch" class="search-input" placeholder="కేసు పేరు, సంవత్సరం, ఆర్టికల్ (ఉదా: 21, 356, 368, కేశవానంద, గోప్యత, రిజర్వేషన్లు)..." oninput="filterJudgments()">
            </div>
            <div class="category-pills" id="categoryPills">
                <div class="cat-pill active" onclick="setCategoryFilter('all', this)">అన్నీ (30)</div>
                <div class="cat-pill" onclick="setCategoryFilter('ప్రాథమిక హక్కులు', this)">ప్రాథమిక హక్కులు</div>
                <div class="cat-pill" onclick="setCategoryFilter('రాజ్యాంగ సవరణ', this)">మౌలిక స్వరూపం & సవరణలు</div>
                <div class="cat-pill" onclick="setCategoryFilter('రిజర్వేషన్లు', this)">రిజర్వేషన్లు & సామాజిక న్యాయం</div>
                <div class="cat-pill" onclick="setCategoryFilter('సమాఖ్య', this)">సమాఖ్య & ఆర్టికల్ 356</div>
                <div class="cat-pill" onclick="setCategoryFilter('ఎన్నికలు', this)">ఎన్నికల సంస్కరణలు & నోటా</div>
                <div class="cat-pill" onclick="setCategoryFilter('మహిళా', this)">మహిళా హక్కులు & సమానత్వం</div>
                <div class="cat-pill" onclick="setCategoryFilter('న్యాయ', this)">న్యాయ నియామకాలు & కొలీజియం</div>
            </div>
        </div>

        <!-- Judgments List -->
        <div class="judgments-grid" id="judgmentsGrid">
            <!-- Rendered by JS -->
        </div>
    </div>

    <script>
        const judgmentsData = {judgments_json};
        let activeCategory = 'all';

        function init() {{
            renderJudgments(judgmentsData);
        }}

        function setCategoryFilter(category, element) {{
            activeCategory = category;
            document.querySelectorAll('.cat-pill').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
            filterJudgments();
        }}

        function filterJudgments() {{
            const query = document.getElementById('judgmentSearch').value.toLowerCase().trim();
            const filtered = judgmentsData.filter(j => {{
                // Category match
                const matchCategory = (activeCategory === 'all') || 
                    j.category.toLowerCase().includes(activeCategory.toLowerCase()) ||
                    j.case_name.toLowerCase().includes(activeCategory.toLowerCase());

                if (!matchCategory) return false;
                if (!query) return true;

                // Search match across case_name, year, articles, core_verdict, basic_structure_elements
                return (
                    j.case_name.toLowerCase().includes(query) ||
                    j.year.includes(query) ||
                    j.articles.toLowerCase().includes(query) ||
                    j.core_verdict.toLowerCase().includes(query) ||
                    j.basic_structure_elements.toLowerCase().includes(query) ||
                    j.bench.toLowerCase().includes(query)
                );
            }});

            renderJudgments(filtered);
        }}

        function renderJudgments(items) {{
            const grid = document.getElementById('judgmentsGrid');
            if (items.length === 0) {{
                grid.innerHTML = `
                    <div style="text-align:center; padding:50px 20px; color:var(--text-muted); background:var(--bg-card); border-radius:var(--radius-lg); border:1px solid var(--border-color);">
                        <i class="fa-solid fa-gavel" style="font-size:2.5rem; color:#f59e0b; margin-bottom:12px;"></i>
                        <h3 style="color:white; margin-bottom:6px;">తీర్పులు లభించలేదు</h3>
                        <p>మీ శోధన పదాలను మార్చి తిరిగి ప్రయత్నించండి.</p>
                    </div>
                `;
                return;
            }}

            let html = '';
            items.forEach((j, index) => {{
                const mcq = j.mcq;
                const optHtml = mcq.options.map(opt => `
                    <button class="mcq-opt" onclick="checkMcq(this, '${{opt.replace(/'/g, "\\\'")}}', '${{mcq.ans.replace(/'/g, "\\\'")}}', 'exp_${{j.id}}')">
                        ${{opt}}
                    </button>
                `).join('');

                html += `
                <div class="judgment-card" id="${{j.id}}">
                    <div class="card-header">
                        <div class="case-title-area">
                            <div class="case-num">ల్యాండ్‌మార్క్ తీర్పు #${{j.id.replace('sc_', '')}} &bull; ${{j.category}}</div>
                            <h2 class="case-name">${{j.case_name}}</h2>
                        </div>
                        <span class="year-badge">${{j.year}}</span>
                    </div>

                    <div class="meta-tags">
                        <span class="meta-tag bench"><i class="fa-solid fa-users"></i> ${{j.bench}}</span>
                        <span class="meta-tag ratio"><i class="fa-solid fa-scale-balanced"></i> రేషియో: ${{j.ratio}}</span>
                        <span class="meta-tag"><i class="fa-solid fa-bookmark"></i> ${{j.articles}}</span>
                    </div>

                    <div class="verdict-box">
                        <b>⚖️ ప్రధాన తీర్పు (Core Ruling):</b><br>
                        ${{j.core_verdict}}
                    </div>

                    <div class="exam-impact-box">
                        <b>🎯 పరీక్షల ప్రాధాన్యత & మౌలిక స్వరూపం:</b><br>
                        ${{j.exam_significance}}<br>
                        <span style="display:inline-block; margin-top:4px; color:#cbd5e1; font-size:0.8rem;">
                            <b>కీలక సూత్రాలు:</b> ${{j.basic_structure_elements}}
                        </span>
                    </div>

                    <div class="mcq-container">
                        <div class="mcq-title"><i class="fa-solid fa-circle-question"></i> పరీక్ష ప్రాక్టీస్ ప్రశ్న</div>
                        <div class="mcq-question">${{mcq.q}}</div>
                        <div class="mcq-options">
                            ${{optHtml}}
                        </div>
                        <div class="mcq-explanation" id="exp_${{j.id}}">
                            <b style="color:#34d399;"><i class="fa-solid fa-check"></i> సరైన సమాధానం:</b> ${{mcq.ans}}<br>
                            <b>వివరణ:</b> ${{mcq.exp}}
                        </div>
                    </div>
                </div>
                `;
            }});

            grid.innerHTML = html;
        }}

        function checkMcq(btn, selected, correct, expId) {{
            const parent = btn.parentElement;
            const buttons = parent.querySelectorAll('.mcq-opt');
            buttons.forEach(b => {{
                b.disabled = true;
                if (b.innerText.trim() === correct.trim()) {{
                    b.classList.add('correct');
                }}
            }});

            if (selected.trim() !== correct.trim()) {{
                btn.classList.add('wrong');
            }}

            const expDiv = document.getElementById(expId);
            if (expDiv) {{
                expDiv.style.display = 'block';
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
