# -*- coding: utf-8 -*-
"""
Static GK Super-Fast Pocketbook View.
Renders responsive, interactive Telugu pocketbook with instant search, category filters, and flashcard cards.
"""

import json
from static_gk_data import STATIC_GK_CATEGORIES

def render_static_gk_html():
    categories_json = json.dumps(STATIC_GK_CATEGORIES, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🇮🇳 స్టాటిక్ జీకే సూపర్-ఫాస్ట్ పాకెట్‌బుక్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {{
            --bg-primary: #070d1e;
            --bg-card: #0e1938;
            --bg-card-hover: #162552;
            --accent-gold: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e3366;
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
            background: linear-gradient(135deg, #050a17 0%, #09142e 50%, #060e22 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 80px;
        }}

        /* Navbar */
        .top-navbar {{
            background: rgba(7, 13, 30, 0.95);
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
            font-size: 24px;
            background: linear-gradient(135deg, #3b82f6, #06b6d4);
            padding: 6px 12px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.35);
        }}
        .brand-text h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
        }}
        .brand-text p {{
            font-size: 0.8rem;
            color: var(--accent-cyan);
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
            border-color: var(--accent-cyan);
        }}
        .nav-btn.pdf-btn {{
            background: linear-gradient(135deg, var(--accent-gold), #d97706);
            color: #070d1e;
            font-weight: 800;
            border: none;
        }}

        .container {{
            max-width: 1150px;
            margin: 0 auto;
            padding: 24px 16px;
        }}

        /* Hero */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(59, 130, 246, 0.12) 100%);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 24px;
        }}
        .hero-banner h2 {{
            font-size: 1.55rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .hero-banner p {{
            color: #cbd5e1;
            font-size: 0.92rem;
            line-height: 1.6;
        }}

        /* Search & Filter Row */
        .search-filter-box {{
            display: flex;
            gap: 14px;
            margin-bottom: 22px;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
        }}
        .search-input-wrap {{
            position: relative;
            flex: 1;
            min-width: 280px;
            max-width: 450px;
        }}
        .search-input-wrap input {{
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 10px 14px 10px 38px;
            border-radius: 20px;
            font-size: 0.88rem;
            outline: none;
            transition: border-color 0.2s;
        }}
        .search-input-wrap input:focus {{
            border-color: var(--accent-cyan);
            box-shadow: 0 0 12px rgba(6, 182, 212, 0.3);
        }}
        .search-input-wrap i {{
            position: absolute;
            left: 14px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        /* Category Pills */
        .cat-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 24px;
        }}
        .cat-pill {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 7px 14px;
            border-radius: 20px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .cat-pill:hover, .cat-pill.active {{
            background: linear-gradient(135deg, #2563eb, #06b6d4);
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }}

        /* Section Cards */
        .cat-section {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 24px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        }}
        .cat-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 12px;
            margin-bottom: 16px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .cat-header h3 {{
            font-size: 1.22rem;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .cat-badge {{
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-gold);
            border: 1px solid rgba(245, 158, 11, 0.3);
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 0.76rem;
            font-weight: 700;
        }}

        /* Two-Column Facts Grid */
        .facts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 12px;
        }}
        .fact-card {{
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.07);
            border-radius: 8px;
            padding: 12px 16px;
            display: flex;
            flex-direction: column;
            gap: 4px;
            transition: all 0.2s;
        }}
        .fact-card:hover {{
            background: rgba(255, 255, 255, 0.07);
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
        }}
        .fact-label {{
            font-size: 0.82rem;
            color: var(--text-muted);
            font-weight: 500;
        }}
        .fact-val {{
            font-size: 0.98rem;
            font-weight: 700;
            color: #f1f5f9;
            line-height: 1.4;
        }}
        .fact-val b {{
            color: var(--accent-gold);
        }}
    </style>
</head>
<body>

    <!-- Top Navigation Header -->
    <header class="top-navbar">
        <a href="/" class="brand-box">
            <span class="brand-icon">🇮🇳</span>
            <div class="brand-text">
                <h1>లక్ష్య స్టాటిక్ జీకే సూపర్-ఫాస్ట్ పాకెట్‌బుక్</h1>
                <p>APPSC, TSPSC, SSC, RRB 2026 రాపిడ్ రివిజన్ పోర్టల్</p>
            </div>
        </a>
        <div class="nav-actions">
            <a href="/frontend/pdfs/static_gk_master_pocketbook.pdf" target="_blank" class="nav-btn pdf-btn">
                📄 మాస్టర్ పాకెట్‌బుక్ PDF
            </a>
            <a href="/" class="nav-btn">🏠 హోమ్ డ్యాష్‌బోర్డ్</a>
        </div>
    </header>

    <div class="container">
        <!-- Hero Introduction -->
        <section class="hero-banner">
            <h2><span>⚡</span> పరీక్షా హాల్లోకి వెళ్లే ముందు 5 నిమిషాల రాపిడ్ రివిజన్ డెక్</h2>
            <p>
                పోటీ పరీక్షల్లో ఎట్టి పరిస్థితుల్లోనూ మిస్ కాకూడని అత్యున్నత స్టాటిక్ జీకే వాస్తవాలు. ప్రథములు, జాతీయ పార్కులు, డ్యాములు, 
                అణు విద్యుత్ కేంద్రాలు, మేజర్ పోర్టులు, యునెస్కో ప్రదేశాలు మరియు అంతర్జాతీయ సంస్థల సారాంశం ఒకే చోట.
            </p>
        </section>

        <!-- Search and Filter Bar -->
        <div class="search-filter-box">
            <div class="search-input-wrap">
                <i class="fa-solid fa-magnifying-glass"></i>
                <input type="text" id="searchInput" placeholder="ఏదైనా అంశం సెర్చ్ చేయండి (ఉదా: పార్క్, పోలవరం, డ్యామ్, ఇస్రో)..." oninput="handleSearch()">
            </div>
            <div style="font-size:0.84rem; color:var(--text-muted);">
                మొత్తం విభాగాలు: <b style="color:var(--accent-cyan);">{len(STATIC_GK_CATEGORIES)}</b>
            </div>
        </div>

        <!-- Category Jump Pills -->
        <div class="cat-pills" id="pillsContainer">
            <button class="cat-pill active" onclick="filterCategory('all')">అన్నీ ఒకేసారి</button>
            <!-- Injected via Python/JS -->
        </div>

        <!-- Content Area -->
        <div id="contentArea">
            <!-- Injected by JS -->
        </div>
    </div>

    <script>
        const ALL_CATEGORIES = {categories_json};
        let activeCat = 'all';
        let searchQuery = '';

        function init() {{
            renderPills();
            renderCategories();
        }}

        function renderPills() {{
            const pillsBox = document.getElementById('pillsContainer');
            let html = `<button class="cat-pill active" onclick="filterCategory('all', event)">అన్నీ ఒకేసారి</button>`;
            ALL_CATEGORIES.forEach(c => {{
                html += `<button class="cat-pill" onclick="filterCategory('${{c.id}}', event)"><i class="fa-solid ${{c.icon}}"></i> ${{c.title.split('(')[0]}}</button>`;
            }});
            pillsBox.innerHTML = html;
        }}

        function filterCategory(catId, evt) {{
            activeCat = catId;
            document.querySelectorAll('.cat-pill').forEach(p => p.classList.remove('active'));
            if (evt && evt.target) {{
                const targetBtn = evt.target.closest('.cat-pill');
                if (targetBtn) targetBtn.classList.add('active');
            }}
            renderCategories();
        }}

        function handleSearch() {{
            searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();
            renderCategories();
        }}

        function renderCategories() {{
            const contentBox = document.getElementById('contentArea');
            let html = '';

            const filteredCategories = ALL_CATEGORIES.filter(c => {{
                if (activeCat !== 'all' && c.id !== activeCat) return false;
                if (searchQuery === '') return true;

                // Check title or items
                if (c.title.toLowerCase().includes(searchQuery)) return true;
                return c.items.some(item => 
                    item.label.toLowerCase().includes(searchQuery) || 
                    item.value.toLowerCase().includes(searchQuery)
                );
            }});

            if (filteredCategories.length === 0) {{
                contentBox.innerHTML = `
                <div style="text-align:center; padding: 50px 20px; color: var(--text-muted);">
                    <i class="fa-solid fa-magnifying-glass" style="font-size:2rem; margin-bottom:12px; color:var(--accent-cyan);"></i>
                    <h3>శోధన ఫలితాలు లభించలేదు</h3>
                    <p>దయచేసి వేరే కీవర్డ్‌తో ప్రయత్నించండి.</p>
                </div>
                `;
                return;
            }}

            filteredCategories.forEach(c => {{
                let itemsToShow = c.items;
                if (searchQuery !== '') {{
                    itemsToShow = c.items.filter(item => 
                        item.label.toLowerCase().includes(searchQuery) || 
                        item.value.toLowerCase().includes(searchQuery)
                    );
                }}

                if (itemsToShow.length === 0) return;

                const factsHtml = itemsToShow.map(item => `
                    <div class="fact-card">
                        <span class="fact-label">${{item.label}}</span>
                        <span class="fact-val">${{item.value}}</span>
                    </div>
                `).join('');

                html += `
                <section class="cat-section" id="sec_${{c.id}}">
                    <div class="cat-header">
                        <h3><i class="fa-solid ${{c.icon}}" style="color:var(--accent-cyan);"></i> ${{c.title}}</h3>
                        <span class="cat-badge">${{c.badge}}</span>
                    </div>
                    <div class="facts-grid">
                        ${{factsHtml}}
                    </div>
                </section>
                `;
            }});

            contentBox.innerHTML = html;
        }}

        window.onload = init;
    </script>
</body>
</html>
"""
    return html
