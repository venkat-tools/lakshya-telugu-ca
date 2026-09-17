# -*- coding: utf-8 -*-
"""
Personalized Audio Revision Player & Podcast Hub View.
Renders responsive, interactive Telugu auditory revision portal.
"""

import json
from audio_revision_data import AUDIO_TRACKS

def render_audio_revision_html():
    tracks_json = json.dumps(AUDIO_TRACKS, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎧 పర్సనలైజ్డ్ ఆడియో రివిజన్ ప్లేయర్ & పాడ్‌కాస్ట్ హబ్ | లక్ష్య 2026</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@300;400;500;600;700;800&family=Suranna&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0b1329;
            --bg-card: #131f42;
            --bg-card-hover: #1c2b59;
            --accent-gold: #f59e0b;
            --accent-cyan: #06b6d4;
            --accent-purple: #8b5cf6;
            --accent-emerald: #10b981;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --border-color: #233566;
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
            background: linear-gradient(135deg, #070d1e 0%, #0d1b3e 50%, #06112c 100%);
            color: var(--text-main);
            min-height: 100vh;
            padding-bottom: 80px;
        }}
        
        /* Top Navigation Header */
        .top-navbar {{
            background: rgba(11, 19, 41, 0.95);
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
            font-size: 28px;
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
            padding: 6px 12px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
        }}
        .brand-text h1 {{
            font-size: 1.15rem;
            font-weight: 700;
            color: #ffffff;
            letter-spacing: -0.3px;
        }}
        .brand-text p {{
            font-size: 0.8rem;
            color: var(--accent-cyan);
            font-weight: 500;
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
            font-size: 0.85rem;
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

        /* Container */
        .container {{
            max-width: 1050px;
            margin: 0 auto;
            padding: 24px 16px;
        }}

        /* Hero Banner */
        .hero-banner {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(6, 182, 212, 0.15) 100%);
            border: 1px solid rgba(139, 92, 246, 0.3);
            border-radius: var(--radius-lg);
            padding: 24px;
            margin-bottom: 24px;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        .hero-banner h2 {{
            font-size: 1.6rem;
            font-weight: 800;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .hero-banner p {{
            color: #cbd5e1;
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        /* Master Player Card */
        .master-player {{
            background: linear-gradient(180deg, #182854 0%, #111d40 100%);
            border: 2px solid #2d4580;
            border-radius: var(--radius-lg);
            padding: 26px;
            margin-bottom: 28px;
            box-shadow: 0 12px 35px rgba(0, 0, 0, 0.5);
            position: relative;
            overflow: hidden;
        }}
        .master-player::before {{
            content: '';
            position: absolute;
            top: -50px;
            right: -50px;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, rgba(6, 182, 212, 0.25) 0%, transparent 70%);
            pointer-events: none;
        }}
        .player-header {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 18px;
            flex-wrap: wrap;
            gap: 12px;
        }}
        .track-info {{
            flex: 1;
            min-width: 250px;
        }}
        .track-badge {{
            display: inline-block;
            background: rgba(245, 158, 11, 0.2);
            color: var(--accent-gold);
            border: 1px solid rgba(245, 158, 11, 0.4);
            padding: 3px 10px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .track-title {{
            font-size: 1.35rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 4px;
            line-height: 1.4;
        }}
        .track-speaker {{
            font-size: 0.88rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Audio Wave Visualizer */
        .visualizer-container {{
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 4px;
            margin: 16px 0;
            background: rgba(0, 0, 0, 0.25);
            border-radius: 10px;
            padding: 0 16px;
        }}
        .wave-bar {{
            width: 4px;
            height: 8px;
            background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 2px;
            transition: height 0.15s ease;
        }}
        .wave-playing .wave-bar:nth-child(2n) {{
            animation: bounce 0.6s infinite alternate ease-in-out;
        }}
        .wave-playing .wave-bar:nth-child(2n+1) {{
            animation: bounce 0.8s infinite alternate-reverse ease-in-out;
        }}
        .wave-playing .wave-bar:nth-child(3n) {{
            animation: bounce 0.5s infinite alternate ease-in-out 0.2s;
        }}
        @keyframes bounce {{
            0% {{ height: 6px; }}
            100% {{ height: 38px; }}
        }}

        /* Progress Bar */
        .progress-wrapper {{
            margin-bottom: 18px;
        }}
        .progress-bar-container {{
            width: 100%;
            height: 8px;
            background: #233566;
            border-radius: 4px;
            cursor: pointer;
            position: relative;
        }}
        .progress-fill {{
            height: 100%;
            width: 0%;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple));
            border-radius: 4px;
            position: relative;
        }}
        .progress-thumb {{
            position: absolute;
            right: -6px;
            top: -4px;
            width: 16px;
            height: 16px;
            background: #ffffff;
            border-radius: 50%;
            box-shadow: 0 2px 6px rgba(0,0,0,0.5);
            display: none;
        }}
        .progress-bar-container:hover .progress-thumb {{
            display: block;
        }}
        .time-labels {{
            display: flex;
            justify-content: space-between;
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-top: 6px;
            font-variant-numeric: tabular-nums;
        }}

        /* Controls */
        .player-controls {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .btn-round {{
            background: #1e2e5c;
            border: 1px solid var(--border-color);
            color: #ffffff;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .btn-round:hover {{
            background: #2b3f7a;
            border-color: var(--accent-cyan);
            transform: scale(1.05);
        }}
        .btn-play-master {{
            width: 58px;
            height: 58px;
            font-size: 1.5rem;
            background: linear-gradient(135deg, var(--accent-gold), #ea580c);
            border: none;
            box-shadow: 0 6px 20px rgba(245, 158, 11, 0.4);
        }}
        .btn-play-master:hover {{
            transform: scale(1.08);
            box-shadow: 0 8px 25px rgba(245, 158, 11, 0.6);
        }}

        /* Speed and Autoplay Controls */
        .player-subcontrols {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-top: 20px;
            padding-top: 16px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            flex-wrap: wrap;
            gap: 12px;
        }}
        .speed-group {{
            display: flex;
            align-items: center;
            gap: 6px;
            background: #0d1733;
            padding: 4px 8px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        .speed-group span {{
            font-size: 0.78rem;
            color: var(--text-muted);
            margin-right: 4px;
        }}
        .btn-speed {{
            background: transparent;
            border: none;
            color: #94a3b8;
            padding: 3px 8px;
            border-radius: 6px;
            font-size: 0.8rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .btn-speed.active {{
            background: var(--accent-cyan);
            color: #070d1e;
        }}
        .toggle-autoplay {{
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
            font-size: 0.85rem;
            color: #cbd5e1;
        }}
        .toggle-autoplay input {{
            accent-color: var(--accent-cyan);
            width: 16px;
            height: 16px;
            cursor: pointer;
        }}

        /* Filter Pills & Search */
        .filter-section {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 14px;
        }}
        .filter-pills {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }}
        .pill-btn {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 8px 14px;
            border-radius: 20px;
            font-size: 0.84rem;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .pill-btn:hover, .pill-btn.active {{
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
            color: #ffffff;
            border-color: transparent;
            box-shadow: 0 4px 12px rgba(139, 92, 246, 0.3);
        }}
        .search-box {{
            position: relative;
            min-width: 240px;
            flex: 1;
            max-width: 320px;
        }}
        .search-box input {{
            width: 100%;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            color: #ffffff;
            padding: 9px 14px 9px 36px;
            border-radius: 20px;
            font-size: 0.85rem;
            outline: none;
        }}
        .search-box input:focus {{
            border-color: var(--accent-cyan);
        }}
        .search-icon {{
            position: absolute;
            left: 12px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        /* Tracks List */
        .tracks-grid {{
            display: flex;
            flex-direction: column;
            gap: 14px;
        }}
        .track-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-md);
            padding: 18px 20px;
            display: flex;
            align-items: flex-start;
            gap: 18px;
            transition: all 0.2s;
        }}
        .track-card:hover {{
            background: var(--bg-card-hover);
            border-color: #3b528b;
            transform: translateY(-2px);
        }}
        .track-card.active-track {{
            border-color: var(--accent-cyan);
            background: #1a2a5e;
            box-shadow: 0 4px 18px rgba(6, 182, 212, 0.2);
        }}
        .btn-card-play {{
            background: linear-gradient(135deg, var(--accent-purple), var(--accent-cyan));
            border: none;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            color: #ffffff;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-size: 1.15rem;
            cursor: pointer;
            flex-shrink: 0;
            box-shadow: 0 4px 10px rgba(139, 92, 246, 0.3);
            transition: all 0.2s;
        }}
        .btn-card-play:hover {{
            transform: scale(1.1);
        }}
        .track-card-content {{
            flex: 1;
        }}
        .card-meta {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 6px;
            flex-wrap: wrap;
        }}
        .card-subj {{
            font-size: 0.78rem;
            font-weight: 600;
            color: var(--accent-cyan);
            background: rgba(6, 182, 212, 0.12);
            padding: 2px 8px;
            border-radius: 12px;
        }}
        .card-dur {{
            font-size: 0.78rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .card-title {{
            font-size: 1.08rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 6px;
            line-height: 1.4;
        }}
        .card-summary {{
            font-size: 0.86rem;
            color: #cbd5e1;
            line-height: 1.5;
            margin-bottom: 12px;
        }}
        .card-actions {{
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .btn-script-toggle {{
            background: transparent;
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #93c5fd;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 0.78rem;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            transition: all 0.15s;
        }}
        .btn-script-toggle:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: #ffffff;
            border-color: #93c5fd;
        }}
        .script-drawer {{
            margin-top: 12px;
            padding: 14px;
            background: rgba(0, 0, 0, 0.35);
            border-left: 3px solid var(--accent-cyan);
            border-radius: 6px;
            font-size: 0.88rem;
            line-height: 1.7;
            color: #e2e8f0;
            display: none;
            white-space: pre-line;
        }}

        @media (max-width: 640px) {{
            .hero-banner h2 {{ font-size: 1.25rem; }}
            .track-title {{ font-size: 1.15rem; }}
            .master-player {{ padding: 18px; }}
            .player-controls {{ gap: 10px; }}
            .btn-play-master {{ width: 50px; height: 50px; font-size: 1.3rem; }}
        }}
    </style>
</head>
<body>

    <!-- Top Navigation Header -->
    <header class="top-navbar">
        <a href="/" class="brand-box">
            <span class="brand-icon">🎧</span>
            <div class="brand-text">
                <h1>లక్ష్య తెలుగు ఆడియో రివిజన్ & పాడ్‌కాస్ట్ హబ్</h1>
                <p>APPSC & TSPSC 2026 స్మార్ట్ లిజనింగ్ పోర్టల్</p>
            </div>
        </a>
        <div class="nav-actions">
            <a href="/" class="nav-btn">🏠 హోమ్ డ్యాష్‌బోర్డ్</a>
            <a href="/appsc_master_portal" class="nav-btn">📚 సిలబస్ బుక్స్</a>
        </div>
    </header>

    <div class="container">
        <!-- Hero Introduction -->
        <section class="hero-banner">
            <h2><span>📻</span> పరీక్షా రివిజన్ ఇప్పుడు మీ చెవుల్లో – ప్రయాణంలోనూ ప్రిపరేషన్!</h2>
            <p>
                ప్రయాణాలు చేస్తున్నప్పుడు, మార్నింగ్ వాకింగ్ లేదా విశ్రాంతి తీసుకుంటున్న సమయంలో కళ్లకు శ్రమ లేకుండా కీలకమైన తెలుగు సిలబస్ అంశాలను వినండి. 
                అధికారిక తెలుగు లెక్చరర్ నరేషన్‌తో కూడిన 8 హై-ఈల్డ్ పాడ్‌కాస్ట్ ట్రాక్‌లు మరియు రాపిడ్ రివిజన్ సూత్రాలు ఇక్కడ అందుబాటులో ఉన్నాయి.
            </p>
        </section>

        <!-- Master Sticky Audio Player -->
        <section class="master-player" id="masterPlayer">
            <div class="player-header">
                <div class="track-info">
                    <span class="track-badge" id="playerBadge">డైలీ స్పెషల్</span>
                    <h3 class="track-title" id="playerTitle">నేటి డైలీ కరెంట్ అఫైర్స్ టాప్ 10 హెడ్‌లైన్స్ & విశ్లేషణ</h3>
                    <div class="track-speaker">
                        <span>🎙️ లెక్చరర్: <b id="playerSpeaker" style="color:#ffffff;">లక్ష్య డిజిటల్ లెక్చరర్</b></span>
                        <span>•</span>
                        <span id="playerSubject" style="color:var(--accent-cyan);">కరెంట్ అఫైర్స్</span>
                    </div>
                </div>
            </div>

            <!-- Wave Visualizer -->
            <div class="visualizer-container" id="visualizer">
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
                <div class="wave-bar"></div>
            </div>

            <!-- Progress Bar -->
            <div class="progress-wrapper">
                <div class="progress-bar-container" id="progressBar" onclick="seekAudio(event)">
                    <div class="progress-fill" id="progressFill">
                        <div class="progress-thumb"></div>
                    </div>
                </div>
                <div class="time-labels">
                    <span id="timeCurrent">00:00</span>
                    <span id="timeDuration">08:30</span>
                </div>
            </div>

            <!-- Control Buttons -->
            <div class="player-controls">
                <button class="btn-round" title="మునుపటి ట్రాక్ (Previous)" onclick="playPrevTrack()">⏮</button>
                <button class="btn-round" title="10 సెకన్లు వెనక్కి (Rewind 10s)" onclick="seekRelative(-10)">⏪ 10s</button>
                <button class="btn-round btn-play-master" id="btnMasterPlay" title="ప్లే / పాజ్" onclick="togglePlay()">▶</button>
                <button class="btn-round" title="10 సెకన్లు ముందుకు (Forward 10s)" onclick="seekRelative(10)">10s ⏩</button>
                <button class="btn-round" title="తర్వాతి ట్రాక్ (Next)" onclick="playNextTrack()">⏭</button>
            </div>

            <!-- Subcontrols: Speed & Autoplay -->
            <div class="player-subcontrols">
                <div class="speed-group">
                    <span>వేగం (Speed):</span>
                    <button class="btn-speed" onclick="setSpeed(0.75)">0.75x</button>
                    <button class="btn-speed active" onclick="setSpeed(1.0)">1.0x</button>
                    <button class="btn-speed" onclick="setSpeed(1.25)">1.25x</button>
                    <button class="btn-speed" onclick="setSpeed(1.5)">1.5x</button>
                    <button class="btn-speed" onclick="setSpeed(2.0)">2.0x</button>
                </div>
                <label class="toggle-autoplay">
                    <input type="checkbox" id="chkAutoplay" checked>
                    <span>కంటిన్యూయస్ ఆటోప్లే (Auto-Next)</span>
                </label>
            </div>
        </section>

        <!-- Search and Filters -->
        <section class="filter-section">
            <div class="filter-pills">
                <button class="pill-btn active" onclick="filterCategory('all')">అన్నీ ({len(AUDIO_TRACKS)})</button>
                <button class="pill-btn" onclick="filterCategory('bulletins')">డైలీ బులెటిన్లు</button>
                <button class="pill-btn" onclick="filterCategory('polity_society')">పాలిటీ & సమాజం</button>
                <button class="pill-btn" onclick="filterCategory('history_geo')">చరిత్ర & జాగ్రఫీ</button>
                <button class="pill-btn" onclick="filterCategory('science_eco')">సైన్స్ & ఎకానమీ</button>
                <button class="pill-btn" onclick="filterCategory('shortcuts')">ఆప్టిట్యూడ్ షార్ట్‌కట్స్</button>
            </div>
            <div class="search-box">
                <span class="search-icon">🔍</span>
                <input type="text" id="searchInput" placeholder="టాపిక్ లేదా సబ్జెక్ట్ సెర్చ్ చేయండి..." oninput="handleSearch()">
            </div>
        </section>

        <!-- Tracks List -->
        <section class="tracks-grid" id="tracksGrid">
            <!-- Dynamic Injection -->
        </section>
    </div>

    <!-- Hidden Native Audio Element -->
    <audio id="nativeAudio"></audio>

    <script>
        const ALL_TRACKS = {tracks_json};
        let currentTrackIndex = 0;
        let isPlaying = false;
        let currentPlaybackRate = 1.0;
        let activeCategory = 'all';
        let searchQuery = '';

        const nativeAudio = document.getElementById('nativeAudio');
        const visualizer = document.getElementById('visualizer');
        const btnMasterPlay = document.getElementById('btnMasterPlay');
        const progressFill = document.getElementById('progressFill');
        const timeCurrent = document.getElementById('timeCurrent');
        const timeDuration = document.getElementById('timeDuration');

        // Speech synthesis fallback engine
        let synth = window.speechSynthesis;
        let speechUtterance = null;
        let synthTimer = null;
        let synthElapsed = 0;
        let synthTotal = 180;

        function init() {{
            renderTrackList();
            loadTrack(0, false);
            setupAudioEvents();
        }}

        function setupAudioEvents() {{
            nativeAudio.addEventListener('timeupdate', () => {{
                if (nativeAudio.duration) {{
                    const pct = (nativeAudio.currentTime / nativeAudio.duration) * 100;
                    progressFill.style.width = pct + '%';
                    timeCurrent.textContent = formatTime(nativeAudio.currentTime);
                    timeDuration.textContent = formatTime(nativeAudio.duration);
                }}
            }});

            nativeAudio.addEventListener('ended', () => {{
                onTrackFinished();
            }});
        }}

        function loadTrack(index, autoPlay = true) {{
            currentTrackIndex = index;
            const track = ALL_TRACKS[index];
            if (!track) return;

            // Update UI Labels
            document.getElementById('playerTitle').textContent = track.title;
            document.getElementById('playerBadge').textContent = track.badge;
            document.getElementById('playerSpeaker').textContent = track.speaker;
            document.getElementById('playerSubject').textContent = track.subject;
            timeDuration.textContent = track.duration;
            timeCurrent.textContent = '00:00';
            progressFill.style.width = '0%';

            // Stop ongoing speech if any
            if (synth && synth.speaking) {{
                synth.cancel();
            }}
            clearInterval(synthTimer);

            // Highlight Active Card
            document.querySelectorAll('.track-card').forEach((card, i) => {{
                if (card.dataset.id === track.id) {{
                    card.classList.add('active-track');
                }} else {{
                    card.classList.remove('active-track');
                }}
            }});

            if (track.audio_url && track.audio_url.trim() !== '') {{
                nativeAudio.src = track.audio_url;
                nativeAudio.playbackRate = currentPlaybackRate;
                if (autoPlay) playAudio();
            }} else {{
                // Synthesize from Telugu script
                nativeAudio.src = '';
                if (autoPlay) playSpeech(track.script);
            }}
        }}

        function togglePlay() {{
            if (isPlaying) {{
                pauseAll();
            }} else {{
                const track = ALL_TRACKS[currentTrackIndex];
                if (nativeAudio.src && nativeAudio.src !== window.location.href) {{
                    playAudio();
                }} else {{
                    playSpeech(track.script);
                }}
            }}
        }}

        function playAudio() {{
            nativeAudio.play().then(() => {{
                setPlayingState(true);
            }}).catch(e => {{
                console.warn("Audio play failed, falling back to speech synth:", e);
                playSpeech(ALL_TRACKS[currentTrackIndex].script);
            }});
        }}

        function playSpeech(text) {{
            if (!synth) {{
                alert("మీ బ్రౌజర్ ఆడియో స్పీచ్‌ను సపోర్ట్ చేయడం లేదు.");
                return;
            }}
            synth.cancel();
            clearInterval(synthTimer);

            speechUtterance = new SpeechSynthesisUtterance(text);
            speechUtterance.lang = 'te-IN';
            speechUtterance.rate = currentPlaybackRate;

            // Attempt to pick a Telugu or Indian voice
            const voices = synth.getVoices();
            const teVoice = voices.find(v => v.lang.startsWith('te') || v.lang.includes('IN'));
            if (teVoice) speechUtterance.voice = teVoice;

            synthElapsed = 0;
            const words = text.split(/\\s+/).length;
            synthTotal = Math.max(30, Math.round(words / 2.5)); // Est duration

            speechUtterance.onstart = () => {{
                setPlayingState(true);
                synthTimer = setInterval(() => {{
                    synthElapsed++;
                    const pct = Math.min(100, (synthElapsed / synthTotal) * 100);
                    progressFill.style.width = pct + '%';
                    timeCurrent.textContent = formatTime(synthElapsed);
                    timeDuration.textContent = formatTime(synthTotal);
                }}, 1000);
            }};

            speechUtterance.onend = () => {{
                clearInterval(synthTimer);
                onTrackFinished();
            }};

            speechUtterance.onerror = () => {{
                clearInterval(synthTimer);
                setPlayingState(false);
            }};

            synth.speak(speechUtterance);
        }}

        function pauseAll() {{
            if (nativeAudio.src) {{
                nativeAudio.pause();
            }}
            if (synth && synth.speaking) {{
                synth.cancel();
            }}
            clearInterval(synthTimer);
            setPlayingState(false);
        }}

        function setPlayingState(playing) {{
            isPlaying = playing;
            if (playing) {{
                btnMasterPlay.innerHTML = '⏸';
                visualizer.classList.add('wave-playing');
            }} else {{
                btnMasterPlay.innerHTML = '▶';
                visualizer.classList.remove('wave-playing');
            }}
        }}

        function onTrackFinished() {{
            setPlayingState(false);
            const isAutoplay = document.getElementById('chkAutoplay').checked;
            if (isAutoplay) {{
                playNextTrack();
            }}
        }}

        function playNextTrack() {{
            const nextIdx = (currentTrackIndex + 1) % ALL_TRACKS.length;
            loadTrack(nextIdx, true);
        }}

        function playPrevTrack() {{
            const prevIdx = (currentTrackIndex - 1 + ALL_TRACKS.length) % ALL_TRACKS.length;
            loadTrack(prevIdx, true);
        }}

        function seekRelative(seconds) {{
            if (nativeAudio.src && !nativeAudio.paused) {{
                nativeAudio.currentTime = Math.max(0, Math.min(nativeAudio.duration, nativeAudio.currentTime + seconds));
            }} else if (synth && synth.speaking) {{
                // Speech synthesis does not support arbitrary seeking, restart with notification
                playSpeech(ALL_TRACKS[currentTrackIndex].script);
            }}
        }}

        function seekAudio(e) {{
            if (nativeAudio.src && nativeAudio.duration) {{
                const rect = document.getElementById('progressBar').getBoundingClientRect();
                const pos = (e.clientX - rect.left) / rect.width;
                nativeAudio.currentTime = pos * nativeAudio.duration;
            }}
        }}

        function setSpeed(rate) {{
            currentPlaybackRate = rate;
            document.querySelectorAll('.btn-speed').forEach(btn => {{
                if (parseFloat(btn.textContent) === rate) {{
                    btn.classList.add('active');
                }} else {{
                    btn.classList.remove('active');
                }}
            }});
            if (nativeAudio) nativeAudio.playbackRate = rate;
            if (isPlaying && synth && synth.speaking) {{
                playSpeech(ALL_TRACKS[currentTrackIndex].script);
            }}
        }}

        function filterCategory(cat) {{
            activeCategory = cat;
            document.querySelectorAll('.pill-btn').forEach(btn => {{
                btn.classList.remove('active');
            }});
            event.target.classList.add('active');
            renderTrackList();
        }}

        function handleSearch() {{
            searchQuery = document.getElementById('searchInput').value.toLowerCase().trim();
            renderTrackList();
        }}

        function renderTrackList() {{
            const grid = document.getElementById('tracksGrid');
            const filtered = ALL_TRACKS.filter(t => {{
                const matchesCat = activeCategory === 'all' || t.category === activeCategory;
                const matchesSearch = searchQuery === '' || 
                    t.title.toLowerCase().includes(searchQuery) || 
                    t.subject.toLowerCase().includes(searchQuery) ||
                    t.summary.toLowerCase().includes(searchQuery);
                return matchesCat && matchesSearch;
            }});

            if (filtered.length === 0) {{
                grid.innerHTML = `<div style="text-align:center; padding: 40px; color: var(--text-muted);">
                    <h3>🔍 ఫలితాలు కనుగొనబడలేదు</h3>
                    <p>దయచేసి వేరే కీవర్డ్ లేదా కేటగిరీని ఎంచుకోండి.</p>
                </div>`;
                return;
            }}

            grid.innerHTML = filtered.map((track, i) => {{
                const globalIndex = ALL_TRACKS.findIndex(t => t.id === track.id);
                const isCurrent = globalIndex === currentTrackIndex;
                return `
                <div class="track-card ${{isCurrent ? 'active-track' : ''}}" data-id="${{track.id}}">
                    <button class="btn-card-play" onclick="loadTrack(${{globalIndex}}, true)" title="ప్లే చేయండి">
                        ${{isCurrent && isPlaying ? '⏸' : '▶'}}
                    </button>
                    <div class="track-card-content">
                        <div class="card-meta">
                            <span class="card-subj">${{track.subject}}</span>
                            <span class="card-dur">⏱️ ${{track.duration}} నిమిషాలు</span>
                            <span class="track-badge">${{track.badge}}</span>
                        </div>
                        <h4 class="card-title">${{track.title}}</h4>
                        <p class="card-summary">${{track.summary}}</p>
                        <div class="card-actions">
                            <button class="btn-script-toggle" onclick="toggleScript('script_${{track.id}}')">
                                📝 స్క్రిప్ట్ చదవండి / దాచండి
                            </button>
                        </div>
                        <div class="script-drawer" id="script_${{track.id}}">
                            ${{track.script}}
                        </div>
                    </div>
                </div>
                `;
            }}).join('');
        }}

        function toggleScript(id) {{
            const drawer = document.getElementById(id);
            if (drawer.style.display === 'block') {{
                drawer.style.display = 'none';
            }} else {{
                drawer.style.display = 'block';
            }}
        }}

        function formatTime(seconds) {{
            if (isNaN(seconds)) return '00:00';
            const m = Math.floor(seconds / 60);
            const s = Math.floor(seconds % 60);
            return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
        }}

        window.onload = init;
    </script>
</body>
</html>
"""
    return html
