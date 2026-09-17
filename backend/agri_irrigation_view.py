# -*- coding: utf-8 -*-
"""
AP & Telangana Agriculture, Irrigation & Aquaculture Interactive Hub View.
"""

import json
from agri_irrigation_data import get_agri_irrigation_data

def render_agri_irrigation_html():
    data = get_agri_irrigation_data()
    data_json = json.dumps(data, ensure_ascii=False)

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌾 AP & TS వ్యవసాయం, సాగునీరు & ఆక్వా హబ్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-primary: #060f14;
            --bg-card: #0c1c24;
            --bg-card-hover: #132a36;
            --accent-emerald: #10b981;
            --accent-teal: #14b8a6;
            --accent-gold: #f59e0b;
            --accent-cyan: #06b6d4;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e3a47;
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
            background: linear-gradient(135deg, #04090c 0%, #09171f 50%, #050d12 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 90px;
        }}

        /* Navbar */
        .top-navbar {{
            background: rgba(6, 15, 20, 0.95);
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
            background: linear-gradient(135deg, #059669, #10b981);
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
            background: #0f2732;
            border: 1px solid #1e4557;
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
            background: #183e4f;
            color: white;
        }}
        .nav-btn-primary {{
            background: linear-gradient(135deg, #10b981, #059669);
            color: white;
            border: none;
            font-weight: 800;
        }}
        .nav-btn-primary:hover {{
            background: linear-gradient(135deg, #34d399, #10b981);
            transform: translateY(-1px);
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 16px;
        }}

        /* Hero Banner */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(6, 182, 212, 0.1));
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: var(--radius-lg);
            padding: 28px 24px;
            margin-bottom: 24px;
            text-align: center;
        }}
        .hero-banner h1 {{
            font-size: 1.85rem;
            font-weight: 900;
            color: #ffffff;
            margin-bottom: 10px;
        }}
        .hero-banner p {{
            font-size: 0.95rem;
            color: var(--text-muted);
            max-width: 820px;
            margin: 0 auto 16px auto;
            line-height: 1.6;
        }}
        .stat-pills {{
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }}
        .stat-pill {{
            background: rgba(12, 28, 36, 0.8);
            border: 1px solid rgba(16, 185, 129, 0.2);
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            color: #6ee7b7;
            font-weight: 600;
        }}

        /* Search & Filter Bar */
        .controls-panel {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 16px 20px;
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
        }}
        .search-input {{
            width: 100%;
            background: #060e13;
            border: 1px solid #1e3a47;
            border-radius: var(--radius-md);
            padding: 12px 16px 12px 46px;
            color: white;
            font-size: 0.95rem;
            font-family: inherit;
            outline: none;
        }}
        .search-input:focus {{
            border-color: var(--accent-emerald);
        }}
        .category-pills {{
            display: flex;
            gap: 8px;
            overflow-x: auto;
            scrollbar-width: none;
        }}
        .category-pills::-webkit-scrollbar {{
            display: none;
        }}
        .cat-pill {{
            background: #07151c;
            border: 1px solid #16323f;
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
            background: var(--accent-emerald);
            color: #062b1b;
            border-color: var(--accent-emerald);
            font-weight: 800;
        }}

        /* Section Cards */
        .section-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 20px;
        }}
        .sec-title {{
            font-size: 1.25rem;
            font-weight: 800;
            color: #34d399;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 10px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            padding-bottom: 10px;
        }}
        .points-list {{
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}
        .point-item {{
            background: #08151c;
            border-left: 4px solid var(--accent-teal);
            border-radius: 0 10px 10px 0;
            padding: 12px 16px;
            font-size: 0.92rem;
            line-height: 1.65;
            color: #e2e8f0;
        }}
        .point-item b {{
            color: #67e8f9;
        }}

        /* MCQs Section */
        .mcq-panel {{
            background: #081720;
            border: 1px dashed #1e4557;
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-top: 24px;
        }}
        .mcq-card {{
            background: #0b202c;
            border: 1px solid #1a3d4d;
            border-radius: var(--radius-md);
            padding: 16px;
            margin-bottom: 14px;
        }}
        .mcq-q {{
            font-weight: 700;
            font-size: 0.95rem;
            color: #ffffff;
            margin-bottom: 10px;
        }}
        .mcq-opts {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 8px;
            margin-bottom: 10px;
        }}
        .mcq-btn {{
            background: #07151c;
            border: 1px solid #1a3947;
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #cbd5e1;
            cursor: pointer;
            text-align: left;
            transition: all 0.15s;
        }}
        .mcq-btn:hover {{
            background: #122b38;
            border-color: #38bdf8;
        }}
        .mcq-btn.correct {{
            background: rgba(16, 185, 129, 0.2) !important;
            border-color: #10b981 !important;
            color: #34d399 !important;
            font-weight: bold;
        }}
        .mcq-btn.wrong {{
            background: rgba(239, 68, 68, 0.2) !important;
            border-color: #ef4444 !important;
            color: #f87171 !important;
        }}
        .mcq-exp {{
            background: #040c10;
            border-left: 3px solid #10b981;
            padding: 8px 12px;
            font-size: 0.8rem;
            color: #cbd5e1;
            display: none;
            margin-top: 8px;
            border-radius: 0 6px 6px 0;
        }}

        /* Fullscreen Toggle */
        .fullscreen-active header,
        .fullscreen-active .top-navbar {{
            display: none !important;
        }}
    </style>
</head>
<body>

    <!-- Top Navbar -->
    <header class="top-navbar" id="mainHeader">
        <a href="/" class="brand-link">
            <span class="brand-badge">లక్ష్య 2026</span>
            <span class="brand-title">🌾 AP & TS వ్యవసాయం & సాగునీరు</span>
        </a>
        <div class="nav-actions">
            <button class="nav-btn" onclick="toggleFullScreenMode()" title="ట్యాబ్స్ దాచు / చూపించు">
                <i class="fa-solid fa-expand"></i> <span id="toggleText">పూర్తి స్క్రీన్</span>
            </button>
            <a href="/frontend/pdfs/ap_ts_agriculture_irrigation_master.pdf" target="_blank" class="nav-btn nav-btn-primary">
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
            <h1>🌾 ఆంధ్రప్రదేశ్ & తెలంగాణ వ్యవసాయం, సాగునీటి ప్రాజెక్టులు & ఆక్వాకల్చర్</h1>
            <p>
                AP GSVA లో 34-36% వాటా కలిగిన వ్యవసాయ రంగం, పోలవరం జాతీయ ప్రాజెక్ట్ (సెక్షన్ 90), కృష్ణా-గోదావరి ట్రిబ్యునల్స్, ఆక్వాకల్చర్ రొయ్యల ఎగుమతులు మరియు 2025-26 MSP గణాంకాల సమగ్ర గైడ్.
            </p>
            <div class="stat-pills">
                <span class="stat-pill">🌾 నికర సాగు: 60.5 లక్షల హెక్టార్లు</span>
                <span class="stat-pill">🌊 పోలవరం నిల్వ: 194.6 TMC</span>
                <span class="stat-pill">🍤 ఆక్వా ఎగుమతులు: దేశంలోనే 35-40% వాటా</span>
                <span class="stat-pill">🥭 పండ్ల ఉత్పత్తి: దేశంలో నంబర్ 1</span>
            </div>
        </div>

        <!-- Controls -->
        <div class="controls-panel">
            <div class="search-box">
                <i class="fa-solid fa-magnifying-glass"></i>
                <input type="text" id="agriSearch" class="search-input" placeholder="పంట, ప్రాజెక్ట్, నది, MSP, పోలవరం, ఆక్వా, ఒంగోలు జాతిని వెతకండి..." oninput="filterContent()">
            </div>
            <div class="category-pills" id="categoryPills">
                <div class="cat-pill active" onclick="setFilter('all', this)">అన్నీ</div>
                <div class="cat-pill" onclick="setFilter('sec_crops_msp', this)">పంటలు & MSP</div>
                <div class="cat-pill" onclick="setFilter('sec_irrigation_projects', this)">సాగునీరు & పోలవరం</div>
                <div class="cat-pill" onclick="setFilter('sec_river_disputes', this)">నదీ జల వివాదాలు (KWDT)</div>
                <div class="cat-pill" onclick="setFilter('sec_horticulture_aqua', this)">ఉద్యానవనం & ఆక్వాకల్చర్</div>
                <div class="cat-pill" onclick="setFilter('sec_livestock_schemes', this)">పశుసంపద & పథకాలు</div>
            </div>
        </div>

        <!-- Sections Container -->
        <div id="sectionsContainer">
            <!-- Populated by JS -->
        </div>

        <!-- MCQs Panel -->
        <div class="mcq-panel">
            <h3 style="font-size:1.3rem; font-weight:800; color:#34d399; margin-bottom:16px;">
                <i class="fa-solid fa-circle-question"></i> వ్యవసాయం & సాగునీరు ప్రాక్టీస్ ప్రశ్నలు (MCQs):
            </h3>
            <div id="mcqList">
                <!-- Populated by JS -->
            </div>
        </div>
    </div>

    <script>
        const agriData = {data_json};
        let activeFilter = 'all';

        function init() {{
            renderSections();
            renderMCQs();
        }}

        function setFilter(filterId, el) {{
            activeFilter = filterId;
            document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
            el.classList.add('active');
            filterContent();
        }}

        function filterContent() {{
            const query = document.getElementById('agriSearch').value.toLowerCase().trim();
            const container = document.getElementById('sectionsContainer');

            let filtered = agriData.core_sections.filter(sec => {{
                if (activeFilter !== 'all' && sec.id !== activeFilter) return false;
                if (!query) return true;
                if (sec.title.toLowerCase().includes(query)) return true;
                return sec.points.some(pt => pt.toLowerCase().includes(query));
            }});

            if (filtered.length === 0) {{
                container.innerHTML = `
                    <div style="text-align:center; padding:40px; color:var(--text-muted);">
                        <h3>ఫలితాలు లభించలేదు</h3>
                        <p>దయచేసి వేరే కీవర్డ్‌తో శోధించండి.</p>
                    </div>
                `;
                return;
            }}

            container.innerHTML = filtered.map(sec => `
                <div class="section-card">
                    <h2 class="sec-title"><i class="fa-solid ${{sec.icon}}"></i> ${{sec.title}}</h2>
                    <ul class="points-list">
                        ${{sec.points.filter(pt => !query || pt.toLowerCase().includes(query)).map(pt => `
                            <li class="point-item">${{pt}}</li>
                        `).join('')}}
                    </ul>
                </div>
            `).join('');
        }}

        function renderSections() {{
            filterContent();
        }}

        function renderMCQs() {{
            const mcqBox = document.getElementById('mcqList');
            mcqBox.innerHTML = agriData.mcqs.map((m, idx) => `
                <div class="mcq-card">
                    <div class="mcq-q">${{idx + 1}}. ${{m.q}}</div>
                    <div class="mcq-opts">
                        ${{m.options.map(opt => `
                            <button class="mcq-btn" onclick="checkAnswer(this, '${{opt.replace(/'/g, "\\\\\\'")}}', '${{m.ans.replace(/'/g, "\\\\\\'")}}', 'exp_${{idx}}')">
                                ${{opt}}
                            </button>
                        `).join('')}}
                    </div>
                    <div class="mcq-exp" id="exp_${{idx}}">
                        <b style="color:#34d399;">✓ సరైన సమాధానం:</b> ${{m.ans}}<br>
                        <b>వివరణ:</b> ${{m.exp}}
                    </div>
                </div>
            `).join('');
        }}

        function checkAnswer(btn, selected, correct, expId) {{
            const parent = btn.parentElement;
            parent.querySelectorAll('.mcq-btn').forEach(b => {{
                b.disabled = true;
                if (b.innerText.trim() === correct.trim()) {{
                    b.classList.add('correct');
                }}
            }});
            if (selected.trim() !== correct.trim()) {{
                btn.classList.add('wrong');
            }}
            const expEl = document.getElementById(expId);
            if (expEl) expEl.style.display = 'block';
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
