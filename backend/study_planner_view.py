# -*- coding: utf-8 -*-
"""
Interactive Web View for 60-Day Smart Daily Study Planner & Syllabus Tracker (/study_planner).
Features localStorage persistence, progress tracking, week filters, and study links.
"""

from study_planner_data import get_study_planner_data

def render_study_planner_html():
    data = get_study_planner_data()
    days = data["days"]

    days_html = ""
    for d in days:
        days_html += f"""
        <div class="day-card bg-white border border-slate-200 rounded-2xl p-4 sm:p-5 shadow-2xs hover:shadow-md transition space-y-3" data-day="{d['day']}" data-week="{d['week']}" data-subject="{d['subject']}">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
            <div class="flex items-center space-x-2">
              <span class="w-8 h-8 rounded-xl bg-slate-900 text-amber-400 font-black text-xs flex items-center justify-center">
                D{d['day']}
              </span>
              <span class="text-xs font-bold text-slate-500">వారం {d['week']}</span>
            </div>
            
            <div class="flex items-center space-x-2">
              <span class="px-2.5 py-0.5 rounded-lg text-xs font-black bg-indigo-50 text-indigo-900 border border-indigo-200">
                <i class="fa-solid {d['icon']} text-xs mr-1"></i> {d['subject']}
              </span>
              <label class="flex items-center space-x-1.5 cursor-pointer bg-slate-100 hover:bg-emerald-50 px-2.5 py-1 rounded-lg border border-slate-200 transition">
                <input type="checkbox" id="check-day-{d['day']}" onchange="toggleDayCompleted({d['day']})" class="w-4 h-4 rounded text-emerald-600 focus:ring-emerald-500">
                <span class="text-xs font-bold text-slate-700 select-none">పూర్తయింది</span>
              </label>
            </div>
          </div>

          <h4 class="font-black text-slate-900 text-sm sm:text-base leading-snug">{d['title']}</h4>
          <p class="text-xs sm:text-sm text-slate-600 leading-relaxed font-medium bg-slate-50 p-2.5 rounded-xl border border-slate-100">
            📌 {d['points']}
          </p>

          <div class="pt-1 flex flex-wrap items-center justify-between gap-2 text-xs font-bold">
            <a href="{d['mat_link']}" class="text-indigo-600 hover:text-indigo-800 flex items-center gap-1 bg-indigo-50/70 hover:bg-indigo-100 px-3 py-1.5 rounded-lg transition border border-indigo-200">
              <i class="fa-solid fa-book-open"></i> మెటీరియల్ చదవండి
            </a>
            <a href="{d['test_link']}" class="text-emerald-700 hover:text-emerald-900 flex items-center gap-1 bg-emerald-50 hover:bg-emerald-100 px-3 py-1.5 rounded-lg transition border border-emerald-200">
              <i class="fa-solid fa-pen-to-square"></i> ఆన్‌లైన్ టెస్ట్ సాధన
            </a>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>60 రోజుల స్మార్ట్ డైలీ స్టడీ ప్లానర్ & సిలబస్ ట్రాకర్ - లక్ష్య</title>
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
          <span>📅</span> <span>60 రోజుల స్మార్ట్ డైలీ స్టడీ ప్లానర్ 2026</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్లానర్ ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Banner & Progress Dashboard -->
    <div class="bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-4 border border-indigo-900/40 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          APPSC & TSPSC ప్రిలిమ్స్ 60 డేస్ ఛాలెంజ్
        </span>
        <span class="text-xs text-indigo-200 font-medium">క్రమశిక్షణతో కూడిన రోజువారీ మైక్రో-షెడ్యూల్</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">60 రోజుల సంపూర్ణ సిలబస్ ట్రాకర్ & సాధన డ్యాష్‌బోర్డ్</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        చరిత్ర, భౌగోళికం, భారతీయ సమాజం, మెంటల్ ఎబిలిటీ మరియు కరెంట్ అఫైర్స్ విభాగాలను 60 రోజుల్లో సంపూర్ణంగా పూర్తి చేయడానికి శాస్త్రీయంగా రూపొందించిన ప్రణాళిక. ప్రతి రోజు మీరు పూర్తి చేసిన అధ్యాయాన్ని టిక్ చేయండి; మీ ప్రోగ్రెస్ ఆటోమేటిక్‌గా సేవ్ అవుతుంది!
      </p>

      <!-- Progress Bar Container -->
      <div class="bg-slate-900/90 border border-indigo-500/30 p-4 rounded-2xl space-y-2">
        <div class="flex justify-between items-center text-xs font-black">
          <span class="text-slate-300 flex items-center gap-1.5">
            <i class="fa-solid fa-chart-line text-emerald-400"></i> మీ ప్రిపరేషన్ ప్రోగ్రెస్:
          </span>
          <span id="progressText" class="text-amber-300">0 / 60 రోజులు (0%) పూర్తి</span>
        </div>
        <div class="w-full bg-slate-800 h-3.5 rounded-full overflow-hidden p-0.5 border border-slate-700">
          <div id="progressBar" class="bg-gradient-to-r from-amber-400 via-emerald-400 to-indigo-500 h-full rounded-full transition-all duration-300" style="width: 0%"></div>
        </div>
      </div>

      <!-- Filter Controls (no-print) -->
      <div class="no-print pt-2 flex flex-wrap gap-2 text-xs font-bold">
        <button type="button" onclick="filterPlanner('all')" class="week-filter-btn active px-3 py-1.5 bg-white text-slate-900 rounded-xl transition">అన్నీ (60 Days)</button>
        <button type="button" onclick="filterPlanner('week_1_2')" class="week-filter-btn px-3 py-1.5 bg-slate-900/80 hover:bg-slate-800 text-slate-300 rounded-xl transition">వారం 1-2 (చరిత్ర)</button>
        <button type="button" onclick="filterPlanner('week_3_4')" class="week-filter-btn px-3 py-1.5 bg-slate-900/80 hover:bg-slate-800 text-slate-300 rounded-xl transition">వారం 3-4 (భౌగోళికం)</button>
        <button type="button" onclick="filterPlanner('week_5_6')" class="week-filter-btn px-3 py-1.5 bg-slate-900/80 hover:bg-slate-800 text-slate-300 rounded-xl transition">వారం 5-6 (సమాజం)</button>
        <button type="button" onclick="filterPlanner('week_7_8')" class="week-filter-btn px-3 py-1.5 bg-slate-900/80 hover:bg-slate-800 text-slate-300 rounded-xl transition">వారం 7-8 (మెంటల్ ఎబిలిటీ)</button>
        <button type="button" onclick="filterPlanner('week_9')" class="week-filter-btn px-3 py-1.5 bg-slate-900/80 hover:bg-slate-800 text-slate-300 rounded-xl transition">వారం 9 (రివిజన్ & మాక్స్)</button>
      </div>
    </div>

    <!-- Days Grid -->
    <div id="daysGrid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {days_html}
    </div>

  </main>

  <script>
    const STORAGE_KEY = 'lakshya_60_days_planner_v1';

    function loadCompletedDays() {{
      try {{
        const raw = localStorage.getItem(STORAGE_KEY);
        return raw ? JSON.parse(raw) : [];
      }} catch(e) {{
        return [];
      }}
    }}

    function saveCompletedDays(arr) {{
      try {{
        localStorage.setItem(STORAGE_KEY, JSON.stringify(arr));
      }} catch(e) {{}}
    }}

    function toggleDayCompleted(dayNum) {{
      let completed = loadCompletedDays();
      const chk = document.getElementById('check-day-' + dayNum);
      if (chk && chk.checked) {{
        if (!completed.includes(dayNum)) completed.push(dayNum);
      }} else {{
        completed = completed.filter(d => d !== dayNum);
      }}
      saveCompletedDays(completed);
      updateProgressDisplay();
    }}

    function updateProgressDisplay() {{
      const completed = loadCompletedDays();
      const total = 60;
      const count = completed.length;
      const pct = Math.round((count / total) * 100);

      // Update checkboxes
      for (let i = 1; i <= total; i++) {{
        const chk = document.getElementById('check-day-' + i);
        if (chk) {{
          chk.checked = completed.includes(i);
          const card = chk.closest('.day-card');
          if (card) {{
            if (completed.includes(i)) {{
              card.classList.add('border-emerald-400', 'bg-emerald-50/20');
            }} else {{
              card.classList.remove('border-emerald-400', 'bg-emerald-50/20');
            }}
          }}
        }}
      }}

      // Update Bar & Text
      const bar = document.getElementById('progressBar');
      const text = document.getElementById('progressText');
      if (bar) bar.style.width = pct + '%';
      if (text) text.innerText = count + ' / 60 రోజులు (' + pct + '%) పూర్తి';
    }}

    function filterPlanner(mode) {{
      const cards = document.querySelectorAll('.day-card');
      const btns = document.querySelectorAll('.week-filter-btn');
      btns.forEach(b => b.classList.remove('active', 'bg-white', 'text-slate-900'));
      event.target.classList.add('active', 'bg-white', 'text-slate-900');

      cards.forEach(card => {{
        const w = parseInt(card.getAttribute('data-week') || '1');
        if (mode === 'all') {{
          card.style.display = '';
        }} else if (mode === 'week_1_2' && (w === 1 || w === 2)) {{
          card.style.display = '';
        }} else if (mode === 'week_3_4' && (w === 3 || w === 4)) {{
          card.style.display = '';
        }} else if (mode === 'week_5_6' && (w === 5 || w === 6)) {{
          card.style.display = '';
        }} else if (mode === 'week_7_8' && (w === 7 || w === 8)) {{
          card.style.display = '';
        }} else if (mode === 'week_9' && w === 9) {{
          card.style.display = '';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}

    // Init on load
    document.addEventListener('DOMContentLoaded', updateProgressDisplay);
    updateProgressDisplay();
  </script>
</body>
</html>"""

    return html
