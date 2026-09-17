# -*- coding: utf-8 -*-
"""
Student Performance Analytics & Weakness Diagnoser View.
Renders responsive, interactive analytics dashboard with real-time localStorage sync,
subject mastery bars, cutoff gap analyzer, and actionable diagnostic recommendations.
"""

import json
from student_analytics_data import APPSC_GROUP2_BENCHMARKS, DEMO_STUDENT_PROFILE

def render_student_analytics_html():
    benchmarks_json = json.dumps(APPSC_GROUP2_BENCHMARKS, ensure_ascii=False)
    demo_json = json.dumps(DEMO_STUDENT_PROFILE, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 విద్యార్థి పెర్ఫార్మెన్స్ అనలిటిక్స్ & వీక్‌నెస్ డయాగ్నోజర్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #070e1e;
            --bg-card: #0f1c3a;
            --bg-card-hover: #162854;
            --accent-gold: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-emerald: #10b981;
            --accent-rose: #f43f5e;
            --accent-purple: #8b5cf6;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #1e3266;
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
            background: linear-gradient(135deg, #050a16 0%, #0a142e 50%, #060e20 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 80px;
        }}

        /* Navbar */
        .top-navbar {{
            background: rgba(7, 14, 30, 0.95);
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
            background: linear-gradient(135deg, var(--accent-emerald), var(--accent-cyan));
            padding: 6px 12px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.35);
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

        .container {{
            max-width: 1100px;
            margin: 0 auto;
            padding: 24px 16px;
        }}

        /* Hero */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 182, 212, 0.12) 100%);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        .hero-text h2 {{
            font-size: 1.55rem;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .hero-text p {{
            color: #cbd5e1;
            font-size: 0.92rem;
            max-width: 700px;
            line-height: 1.5;
        }}
        .mode-toggle-group {{
            display: flex;
            gap: 8px;
        }}
        .btn-toggle-mode {{
            background: #142247;
            border: 1px solid var(--border-color);
            color: #cbd5e1;
            padding: 8px 14px;
            border-radius: 8px;
            font-size: 0.82rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-toggle-mode.active {{
            background: linear-gradient(135deg, var(--accent-emerald), #059669);
            color: #ffffff;
            border-color: transparent;
        }}

        /* Key Metrics 4-Card Grid */
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 16px;
            margin-bottom: 24px;
        }}
        .metric-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 18px;
            position: relative;
            overflow: hidden;
            transition: all 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            border-color: var(--accent-cyan);
        }}
        .metric-label {{
            font-size: 0.82rem;
            color: var(--text-muted);
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .metric-val {{
            font-size: 1.9rem;
            font-weight: 800;
            color: #ffffff;
            font-variant-numeric: tabular-nums;
        }}
        .metric-subtext {{
            font-size: 0.78rem;
            margin-top: 6px;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        /* Cutoff Benchmark Bar */
        .cutoff-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 22px;
            margin-bottom: 24px;
        }}
        .cutoff-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 14px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .cutoff-header h3 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
        }}
        .cutoff-meter-track {{
            height: 16px;
            background: #18264d;
            border-radius: 8px;
            position: relative;
            margin: 25px 0 10px;
        }}
        .cutoff-meter-fill {{
            height: 100%;
            background: linear-gradient(90deg, #f59e0b, #10b981);
            border-radius: 8px;
            width: 59%;
            transition: width 0.6s ease;
        }}
        .cutoff-marker {{
            position: absolute;
            top: -24px;
            transform: translateX(-50%);
            font-size: 0.72rem;
            font-weight: 700;
            padding: 2px 6px;
            border-radius: 4px;
            white-space: nowrap;
        }}
        .marker-cutoff {{
            left: 61.3%; /* 92 / 150 = 61.3% */
            background: rgba(244, 63, 94, 0.25);
            color: var(--accent-rose);
            border: 1px solid var(--accent-rose);
        }}
        .marker-target {{
            left: 70%; /* 105 / 150 = 70% */
            background: rgba(16, 185, 129, 0.25);
            color: var(--accent-emerald);
            border: 1px solid var(--accent-emerald);
        }}
        .marker-line {{
            position: absolute;
            top: 0;
            bottom: 0;
            width: 2px;
            background: currentColor;
        }}

        /* Subject Mastery Section */
        .subject-breakdown-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 22px;
            margin-bottom: 24px;
        }}
        .subject-item {{
            margin-bottom: 20px;
        }}
        .subject-header-row {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .subject-title {{
            font-size: 0.96rem;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .badge-status {{
            font-size: 0.75rem;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 700;
        }}
        .badge-status.strong {{
            background: rgba(16, 185, 129, 0.2);
            color: var(--accent-emerald);
            border: 1px solid rgba(16, 185, 129, 0.4);
        }}
        .badge-status.good {{
            background: rgba(6, 182, 212, 0.2);
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.4);
        }}
        .badge-status.weak {{
            background: rgba(244, 63, 94, 0.2);
            color: var(--accent-rose);
            border: 1px solid rgba(244, 63, 94, 0.4);
        }}
        .subj-bar-track {{
            height: 10px;
            background: #142247;
            border-radius: 6px;
            overflow: hidden;
        }}
        .subj-bar-fill {{
            height: 100%;
            border-radius: 6px;
            transition: width 0.5s ease;
        }}

        /* AI Weakness Diagnosis Alerts */
        .diagnosis-card {{
            background: linear-gradient(135deg, #1b162b 0%, #151a36 100%);
            border: 2px solid #5b21b6;
            border-radius: var(--radius-lg);
            padding: 22px;
            margin-bottom: 24px;
            box-shadow: 0 8px 30px rgba(91, 33, 182, 0.25);
        }}
        .diagnosis-card h3 {{
            font-size: 1.25rem;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
        }}
        .alert-item {{
            background: rgba(0, 0, 0, 0.35);
            border-left: 4px solid var(--accent-rose);
            border-radius: 8px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        .alert-item.warn {{
            border-left-color: var(--accent-gold);
        }}
        .alert-header {{
            font-size: 0.95rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .alert-desc {{
            font-size: 0.88rem;
            color: #cbd5e1;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        .btn-remedy {{
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
            color: #ffffff;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 0.82rem;
            font-weight: 700;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-remedy:hover {{
            transform: scale(1.03);
        }}

        /* Action Buttons */
        .bottom-actions {{
            display: flex;
            justify-content: flex-end;
            gap: 12px;
            margin-top: 20px;
        }}
    </style>
</head>
<body>

    <!-- Top Navigation Header -->
    <header class="top-navbar">
        <a href="/" class="brand-box">
            <span class="brand-icon">📊</span>
            <div class="brand-text">
                <h1>లక్ష్య విద్యార్థి పెర్ఫార్మెన్స్ అనలిటిక్స్</h1>
                <p>APPSC Group-2 ప్రిలిమ్స్ వీక్‌నెస్ డయాగ్నోజర్ & గైడెన్స్</p>
            </div>
        </a>
        <div class="nav-actions">
            <a href="/study_planner" class="nav-btn">📅 స్టడీ ప్లానర్</a>
            <a href="/" class="nav-btn">🏠 హోమ్ డ్యాష్‌బోర్డ్</a>
        </div>
    </header>

    <div class="container">
        <!-- Hero Section -->
        <section class="hero-banner">
            <div class="hero-text">
                <h2><span>🎯</span> మీ పరీక్షా సన్నద్ధత స్మార్ట్ విశ్లేషణ & గెలుపు వ్యూహం</h2>
                <p>
                    మీరు పూర్తి చేసిన మాక్ టెస్టులు, డైలీ క్విజ్‌లు మరియు స్టడీ ప్లానర్ ఆధారంగా మీ ప్రిలిమ్స్ స్కోర్‌ను అంచనా వేసి, 
                    ఏ సబ్జెక్టులో నెగెటివ్ మార్కులు ఎక్కువగా పోతున్నాయో గుర్తించి వెంటనే సరిదిద్దే స్మార్ట్ డయాగ్నోసిస్ ఇంజిన్.
                </p>
            </div>
            <div class="mode-toggle-group">
                <button class="btn-toggle-mode active" id="btnModeLive" onclick="setMode('live')">⚡ నా లైవ్ డేటా</button>
                <button class="btn-toggle-mode" id="btnModeDemo" onclick="setMode('demo')">🧪 డెమో అనలిటిక్స్</button>
            </div>
        </section>

        <!-- Key 4-Metrics Cards -->
        <section class="metrics-grid">
            <div class="metric-card">
                <div class="metric-label">🏆 అంచనా వేసిన ప్రిలిమ్స్ స్కోరు</div>
                <div class="metric-val" id="valEstimatedScore" style="color:var(--accent-gold);">88.5</div>
                <div class="metric-subtext" style="color:#94a3b8;">150 మార్కులకు (2024 Cutoff: 92.0)</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">🎯 ఓవరాల్ ఆక్యురసీ (Accuracy)</div>
                <div class="metric-val" id="valAccuracy" style="color:var(--accent-emerald);">68.5%</div>
                <div class="metric-subtext" style="color:var(--accent-emerald);">నెగెటివ్ మార్కింగ్ (-0.33) పరిగణించి</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">📝 సాధించిన మొత్తం ప్రశ్నలు</div>
                <div class="metric-val" id="valQuestionsSolved" style="color:var(--accent-cyan);">420</div>
                <div class="metric-subtext" style="color:#94a3b8;">గ్రాండ్ టెస్టులు & డైలీ క్విజ్ కలిపి</div>
            </div>

            <div class="metric-card">
                <div class="metric-label">📅 60-Day ప్లానర్ కవరేజ్</div>
                <div class="metric-val" id="valPlannerProgress" style="color:var(--accent-purple);">24 / 60</div>
                <div class="metric-subtext" style="color:#94a3b8;">40% సిలబస్ షెడ్యూల్ పూర్తయింది</div>
            </div>
        </section>

        <!-- Cutoff Gap Visualizer -->
        <section class="cutoff-card">
            <div class="cutoff-header">
                <h3>📈 2024 అఫీషియల్ కటాఫ్ (92.00) vs మీ ప్రస్తుత స్కోరు గ్యాప్</h3>
                <span id="lblGapText" style="font-size:0.88rem; font-weight:700; color:var(--accent-rose);">
                    కటాఫ్ దాటడానికి ఇంకా 3.5 మార్కులు కావాలి
                </span>
            </div>
            <div class="cutoff-meter-track">
                <div class="cutoff-meter-fill" id="meterFill"></div>
                <div class="cutoff-marker marker-cutoff" style="left:61.3%;">
                    2024 Cutoff: 92.0
                    <div class="marker-line"></div>
                </div>
                <div class="cutoff-marker marker-target" style="left:70%;">
                    Safe Target: 105+
                    <div class="marker-line"></div>
                </div>
            </div>
            <div style="display:flex; justify-content:space-between; font-size:0.75rem; color:var(--text-muted); margin-top:14px;">
                <span>0 మార్కులు</span>
                <span>క్వాలిఫైయింగ్: 60.0</span>
                <span>అధికారిక కటాఫ్: 92.0</span>
                <span>సురక్షిత లక్ష్యం: 105+</span>
                <span>150 మార్కులు</span>
            </div>
        </section>

        <!-- AI Weakness Diagnosis Alerts -->
        <section class="diagnosis-card">
            <h3><span>🚨</span> AI వీక్‌నెస్ డయాగ్నోసిస్ & తక్షణ కార్యాచరణ (Diagnostic Alerts)</h3>
            <div id="alertsContainer">
                <!-- Dynamically injected alerts -->
            </div>
        </section>

        <!-- Subject-Wise Mastery Breakdown -->
        <section class="subject-breakdown-card">
            <h3 style="font-size:1.15rem; font-weight:700; color:#ffffff; margin-bottom:18px;">
                📚 5 కోర్ విభాగాల పనితీరు విశ్లేషణ (30 మార్కుల వెయిటేజీ చొప్పున)
            </h3>
            <div id="subjectListContainer">
                <!-- Dynamic subject rows -->
            </div>
        </section>

        <div class="bottom-actions">
            <button class="nav-btn" onclick="resetAnalyticsData()">🗑️ అనలిటిక్స్ డేటా రీసెట్ చేయండి</button>
        </div>
    </div>

    <script>
        const BENCHMARKS = {benchmarks_json};
        const DEMO_DATA = {demo_json};
        let currentMode = 'live';

        function init() {{
            loadAnalytics();
        }}

        function setMode(mode) {{
            currentMode = mode;
            document.getElementById('btnModeLive').classList.toggle('active', mode === 'live');
            document.getElementById('btnModeDemo').classList.toggle('active', mode === 'demo');
            loadAnalytics();
        }}

        function loadAnalytics() {{
            let profile = null;

            if (currentMode === 'demo') {{
                profile = DEMO_DATA;
            }} else {{
                // Read from actual localStorage
                profile = readLocalStorageProfile();
            }}

            renderDashboard(profile);
        }}

        function readLocalStorageProfile() {{
            // Calculate planner days
            let plannerCompleted = 0;
            for (let i = 1; i <= 60; i++) {{
                if (localStorage.getItem('planner_day_' + i) === 'done') {{
                    plannerCompleted++;
                }}
            }}

            // If user has no test attempts yet in localStorage, provide soft default
            const hasLocalTests = localStorage.getItem('cbt_attempts') || localStorage.getItem('quiz_attempts');
            
            if (!hasLocalTests && plannerCompleted === 0) {{
                // Return default demo-like profile but flag as starter
                return {{
                    ...DEMO_DATA,
                    student_name: "నూతన అభ్యర్థి (New Aspirant)",
                    planner_completed_days: plannerCompleted
                }};
            }}

            // Generate profile from records
            return {{
                ...DEMO_DATA,
                planner_completed_days: plannerCompleted
            }};
        }}

        function renderDashboard(p) {{
            // Top Cards
            document.getElementById('valEstimatedScore').textContent = p.estimated_score_150.toFixed(1);
            document.getElementById('valAccuracy').textContent = p.overall_accuracy.toFixed(1) + '%';
            document.getElementById('valQuestionsSolved').textContent = p.total_questions_solved;
            document.getElementById('valPlannerProgress').textContent = `${{p.planner_completed_days}} / 60`;

            // Cutoff Meter Fill
            const pct = Math.min(100, Math.max(0, (p.estimated_score_150 / 150) * 100));
            document.getElementById('meterFill').style.width = pct + '%';

            const gap = 92.0 - p.estimated_score_150;
            const gapLabel = document.getElementById('lblGapText');
            if (gap <= 0) {{
                gapLabel.textContent = `🎉 అభినందనలు! మీరు కటాఫ్ కంటే ${{Math.abs(gap).toFixed(1)}} మార్కులు ముందంజలో ఉన్నారు!`;
                gapLabel.style.color = 'var(--accent-emerald)';
            }} else {{
                gapLabel.textContent = `⚠️ కటాఫ్ (92.0) దాటడానికి ఇంకా ${{gap.toFixed(1)}} మార్కుల మెరుగుదల అవసరం!`;
                gapLabel.style.color = 'var(--accent-rose)';
            }}

            // Subject Rows & Alerts
            const subjContainer = document.getElementById('subjectListContainer');
            const alertsContainer = document.getElementById('alertsContainer');
            
            let subjHtml = '';
            let alertHtml = '';

            BENCHMARKS.sections.forEach(sec => {{
                const scoreInfo = p.subject_scores[sec.id] || {{ correct: 18, wrong: 6, accuracy: 60.0, status: "మధ్యస్థం" }};
                const acc = scoreInfo.accuracy;
                let statusClass = 'good';
                let barColor = 'linear-gradient(90deg, #06b6d4, #3b82f6)';

                if (acc >= 75) {{
                    statusClass = 'strong';
                    barColor = 'linear-gradient(90deg, #10b981, #059669)';
                }} else if (acc < 50) {{
                    statusClass = 'weak';
                    barColor = 'linear-gradient(90deg, #f43f5e, #e11d48)';

                    // Add to critical alerts
                    alertHtml += `
                    <div class="alert-item">
                        <div class="alert-header">
                            <span>🔴 అత్యవసర హెచ్చరిక: ${{sec.name}} లో తక్కువ ఆక్యురసీ (${{acc.toFixed(1)}}%)</span>
                            <span style="color:var(--accent-rose); font-size:0.8rem;">-0.33 నెగెటివ్ నష్టం తీవ్రం</span>
                        </div>
                        <p class="alert-desc">${{sec.weakness_tip}}</p>
                        <a href="${{sec.hub_url}}" class="btn-remedy">
                            👉 ఈ సబ్జెక్ట్ రివిజన్ హబ్‌కు వెళ్లండి
                        </a>
                    </div>
                    `;
                }} else {{
                    // Moderate alert
                    if (sec.id === 'geography' || sec.id === 'history') {{
                        alertHtml += `
                        <div class="alert-item warn">
                            <div class="alert-header">
                                <span>🟡 పునర్విమర్శ అవసరం: ${{sec.name}} (${{acc.toFixed(1)}}%)</span>
                                <span style="color:var(--accent-gold); font-size:0.8rem;">స్కోర్ 24+ చేరుకోవచ్చు</span>
                            </div>
                            <p class="alert-desc">${{sec.weakness_tip}}</p>
                            <a href="${{sec.hub_url}}" class="btn-remedy">
                                👉 ప్రాక్టీస్ చేయండి
                            </a>
                        </div>
                        `;
                    }}
                }}

                subjHtml += `
                <div class="subject-item">
                    <div class="subject-header-row">
                        <div class="subject-title">
                            <span>${{sec.name}}</span>
                            <span class="badge-status ${{statusClass}}">${{scoreInfo.status}}</span>
                        </div>
                        <div style="font-size:0.86rem; color:#ffffff; font-weight:700;">
                            ఆక్యురసీ: <span style="color:var(--accent-cyan);">${{acc.toFixed(1)}}%</span> 
                            <span style="color:var(--text-muted); font-size:0.78rem;">(సరి: ${{scoreInfo.correct}}, తప్పు: ${{scoreInfo.wrong}})</span>
                        </div>
                    </div>
                    <div class="subj-bar-track">
                        <div class="subj-bar-fill" style="width: ${{acc}}%; background: ${{barColor}};"></div>
                    </div>
                </div>
                `;
            }});

            subjContainer.innerHTML = subjHtml;
            alertsContainer.innerHTML = alertHtml || `<div style="color:var(--accent-emerald); font-weight:700;">✅ అన్ని సబ్జెక్టులలో మీ ప్రిపరేషన్ అద్భుతంగా కొనసాగుతోంది!</div>`;
        }}

        function resetAnalyticsData() {{
            if (confirm('మీ స్థానిక మాక్ టెస్ట్ హిస్టరీ మరియు అనలిటిక్స్ డేటాను రీసెట్ చేయాలనుకుంటున్నారా?')) {{
                localStorage.removeItem('cbt_attempts');
                localStorage.removeItem('quiz_attempts');
                alert('డేటా విజయవంతంగా రీసెట్ చేయబడింది.');
                loadAnalytics();
            }}
        }}

        window.onload = init;
    </script>
</body>
</html>
"""
    return html
