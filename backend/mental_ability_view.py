# -*- coding: utf-8 -*-
"""
Interactive Web View for Mental Ability & Aptitude Shortcuts Engine (/mental_ability_hub).
"""

from mental_ability_data import get_mental_ability_data

def render_mental_ability_html():
    data = get_mental_ability_data()
    topics = data["topics"]

    topic_sections = ""
    for t in topics:
        problems_html = ""
        for p_idx, p in enumerate(t["problems"], 1):
            problems_html += f"""
            <div class="problem-box p-4 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-3">
              <div class="flex items-center justify-between border-b border-slate-100 pb-2">
                <span class="text-xs font-black text-indigo-900 bg-indigo-50 px-2.5 py-0.5 rounded-md">సమస్య {p_idx}</span>
                <span class="text-xs font-black text-emerald-800 bg-emerald-100 px-2.5 py-0.5 rounded-md">సమాధానం: {p['ans']}</span>
              </div>
              <p class="text-xs sm:text-sm font-black text-slate-900 leading-relaxed">{p['q']}</p>
              
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1 text-xs sm:text-sm">
                <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
                  <span class="text-[11px] font-black text-slate-500 uppercase flex items-center gap-1">
                    <i class="fa-solid fa-hourglass text-slate-400"></i> సాంప్రదాయ పద్ధతి:
                  </span>
                  <p class="text-slate-700 leading-relaxed font-medium">{p['traditional']}</p>
                </div>
                <div class="p-3 bg-emerald-50/70 border border-emerald-300 rounded-xl space-y-1">
                  <span class="text-[11px] font-black text-emerald-800 uppercase flex items-center gap-1">
                    <i class="fa-solid fa-bolt text-amber-500"></i> ఎగ్జామ్ షార్ట్‌కట్ ట్రిక్ (Speed Trick):
                  </span>
                  <p class="text-emerald-950 font-bold leading-relaxed">{p['shortcut']}</p>
                </div>
              </div>
            </div>
            """

        topic_sections += f"""
        <div class="topic-section space-y-4 pt-2" id="topic-{t['id']}">
          <div class="p-4 bg-gradient-to-r from-slate-900 to-blue-950 text-white rounded-2xl shadow-sm flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <span class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-amber-400 text-lg">
                <i class="fa-solid {t.get('icon', 'fa-calculator')}"></i>
              </span>
              <div>
                <h3 class="text-base sm:text-lg font-black text-white">{t['name']}</h3>
                <p class="text-xs text-slate-300 font-medium">షార్ట్‌కట్ సూత్రాలు & స్టెప్-బై-స్టెప్ పోలికలు</p>
              </div>
            </div>
          </div>

          <!-- Formula Cheatsheet Box -->
          <div class="p-4 bg-amber-50 border-2 border-amber-300 rounded-2xl space-y-1.5 shadow-2xs">
            <span class="text-xs font-black text-amber-900 uppercase tracking-wider flex items-center gap-1.5">
              <i class="fa-solid fa-key text-amber-600"></i> ఎగ్జామ్ స్పీడ్ ఫార్ములా చీట్‌షీట్ (Cheat Codes):
            </span>
            <pre class="text-xs sm:text-sm font-mono font-bold text-slate-800 whitespace-pre-wrap leading-relaxed">{t['cheat_formula']}</pre>
          </div>

          <div class="space-y-3">
            {problems_html}
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్ షార్ట్‌కట్ ప్రాక్టీస్ ఇంజిన్ - లక్ష్య</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Mandali&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif; }}
    @media print {{
      .no-print {{ display: none !important; }}
      body {{ background: white; }}
    }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen pb-16">

  <!-- Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-30 shadow-md no-print border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/appsc_syllabus" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🧮</span> <span>మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్ షార్ట్‌కట్ హబ్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/quantitative_aptitude_120_shortcuts.pdf" download="quantitative_aptitude_120_shortcuts.pdf" class="text-xs bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-file-pdf"></i> 120 షార్ట్‌కట్స్ PDF
        </a>
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Banner -->
    <div class="bg-gradient-to-r from-slate-950 via-blue-950 to-slate-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-blue-900/40 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-cyan-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          APPSC గ్రూప్-2 ప్రిలిమ్స్ (30 Marks Section)
        </span>
        <span class="text-xs text-blue-200 font-medium">నాన్-మ్యాథ్స్ అభ్యర్థులకు కూడా 25+ మార్కుల గ్యారంటీ</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">స్పీడ్ మ్యాథ్స్ & లాజికల్ రీజనింగ్ షార్ట్‌కట్ ఇంజిన్</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        క్లాక్స్, క్యాలెండర్స్, పని-కాలం, రైళ్లు, శాతాలు, నిష్పత్తులలో సంప్రదాయ సుదీర్ఘ లెక్కల స్థానంలో 5 నుండి 10 సెకన్లలో సమాధానం రాబట్టే పరీక్షా షార్ట్‌కట్స్ మరియు స్పీడ్ ఫార్ములాలు.
      </p>

      <!-- Topic Jump Pills (no-print) -->
      <div class="no-print pt-2 flex flex-wrap gap-2 text-xs font-bold">
        <a href="#topic-clocks" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-cyan-400 rounded-xl text-slate-300 transition flex items-center gap-1.5">
          <i class="fa-solid fa-clock text-cyan-400"></i> గడియారాలు
        </a>
        <a href="#topic-calendars" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-amber-400 rounded-xl text-slate-300 transition flex items-center gap-1.5">
          <i class="fa-solid fa-calendar text-amber-400"></i> క్యాలెండర్లు
        </a>
        <a href="#topic-time_work" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-emerald-400 rounded-xl text-slate-300 transition flex items-center gap-1.5">
          <i class="fa-solid fa-briefcase text-emerald-400"></i> పని & కాలం
        </a>
        <a href="#topic-speed_distance" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-rose-400 rounded-xl text-slate-300 transition flex items-center gap-1.5">
          <i class="fa-solid fa-train text-rose-400"></i> రైళ్లు & వేగం
        </a>
        <a href="#topic-percentages_profit" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-purple-400 rounded-xl text-slate-300 transition flex items-center gap-1.5">
          <i class="fa-solid fa-percent text-purple-400"></i> శాతాలు & లాభనష్టాలు
        </a>
        <a href="#topic-ratios_averages" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-teal-400 rounded-xl text-slate-300 transition flex items-center gap-1.5">
          <i class="fa-solid fa-scale-unbalanced text-teal-400"></i> అలగేషన్లు & సగటులు
        </a>
      </div>
    </div>

    <!-- Topics Grid -->
    <div class="space-y-8">
      {topic_sections}
    </div>

  </main>
</body>
</html>"""

    return html
