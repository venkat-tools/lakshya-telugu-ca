# -*- coding: utf-8 -*-
"""
District Master Guide Web View (/districts_guide).
Renders comprehensive 26 AP and TS districts compendium for competitive exams.
"""

from districts_master_data import get_all_districts, get_ap_districts, get_ts_districts

def render_districts_guide_html(state_filter="all"):
    if state_filter == "ap":
        districts = get_ap_districts()
        page_title = "ఆంధ్రప్రదేశ్ 26 నూతన జిల్లాల సమగ్ర దర్శిని (AP Districts Compendium)"
    elif state_filter == "ts":
        districts = get_ts_districts()
        page_title = "తెలంగాణ జిల్లాల సమగ్ర దర్శిని (TS Districts Compendium)"
    else:
        districts = get_all_districts()
        page_title = "ఆంధ్రప్రదేశ్ (26 జిల్లాలు) & తెలంగాణ సమగ్ర జిల్లా దర్శిని"

    cards_html = ""
    for idx, d in enumerate(districts, 1):
        state_badge = "bg-blue-100 text-blue-900 border-blue-200" if d.get("state") == "AP" else "bg-rose-100 text-rose-900 border-rose-200"
        cards_html += f"""
        <article class="district-card bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4 hover:border-blue-500 transition" id="dist_{d['id']}">
          <div class="flex flex-wrap justify-between items-start gap-2 border-b border-slate-100 pb-3">
            <div>
              <span class="text-[10px] font-black uppercase px-2 py-0.5 rounded border {state_badge}">
                {d.get('state')} జిల్లా #{idx}
              </span>
              <h3 class="text-base sm:text-lg font-black text-slate-900 mt-1">{d['name']}</h3>
              <p class="text-xs text-blue-800 font-bold">🏢 జిల్లా కేంద్రం (HQ): {d['hq']}</p>
            </div>
            <span class="text-xs font-mono text-slate-400 font-bold">ID: {d['id']}</span>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div class="p-3 bg-blue-50/60 border border-blue-100 rounded-xl space-y-1">
              <p class="font-black text-blue-950 flex items-center gap-1.5">
                <span>🌊 నదులు & కాలువలు:</span>
              </p>
              <p class="text-slate-700 font-medium">{d['rivers']}</p>
            </div>
            <div class="p-3 bg-indigo-50/60 border border-indigo-100 rounded-xl space-y-1">
              <p class="font-black text-indigo-950 flex items-center gap-1.5">
                <span>🏗️ సాగునీటి & విద్యుత్ ప్రాజెక్టులు:</span>
              </p>
              <p class="text-slate-700 font-medium">{d['projects']}</p>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
            <div class="p-3 bg-amber-50/60 border border-amber-100 rounded-xl space-y-1">
              <p class="font-black text-amber-950 flex items-center gap-1.5">
                <span>⛏️ ఖనిజ సంపద:</span>
              </p>
              <p class="text-slate-700 font-medium">{d['minerals']}</p>
            </div>
            <div class="p-3 bg-emerald-50/60 border border-emerald-100 rounded-xl space-y-1">
              <p class="font-black text-emerald-950 flex items-center gap-1.5">
                <span>🏭 పరిశ్రమలు & ఓడరేవులు / సెజ్ లు:</span>
              </p>
              <p class="text-slate-700 font-medium">{d['industries']}</p>
            </div>
          </div>

          <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1">
            <p class="font-black text-slate-800 flex items-center gap-1.5">
              <span>🏛️ చారిత్రక & పర్యాటక ప్రదేశాలు:</span>
            </p>
            <p class="text-slate-700 font-medium">{d['tourist_historical']}</p>
          </div>

          <div class="p-3 bg-purple-50 border border-purple-200 rounded-xl text-xs space-y-1">
            <p class="font-black text-purple-950 flex items-center gap-1.5">
              <span>🎯 పోటీ పరీక్షల ముఖ్యాంశం (High-Yield Takeaway):</span>
            </p>
            <p class="text-purple-900 font-semibold leading-relaxed">{d['exam_highlights']}</p>
          </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title} - లక్ష్య పోటీ పరీక్షలు</title>
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
    <div class="max-w-6xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/syllabus" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🗺️</span> <span>AP & TS సమగ్ర జిల్లా దర్శిని</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/ap_ts_districts_master_handbook.pdf" download class="text-xs bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-download"></i> జిల్లా దర్శిని PDF
        </a>
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Banner -->
    <div class="bg-gradient-to-r from-blue-950 via-indigo-950 to-slate-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-blue-800/60">
      <div class="flex justify-between items-center">
        <span class="bg-amber-400 text-slate-950 text-[10px] font-black px-3 py-0.5 rounded-full uppercase tracking-wider">
          APPSC & TSPSC సమగ్ర ప్రొఫైల్స్
        </span>
        <span class="text-xs text-blue-200 font-bold">మొత్తం: {len(districts)} జిల్లాలు</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black">{page_title}</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed font-medium">
        ఆంధ్రప్రదేశ్ పునర్వ్యవస్థీకరించిన 26 జిల్లాలు మరియు తెలంగాణ జిల్లాల భౌగోళిక విస్తీర్ణం, నదులు, ప్రాజెక్టులు, ఖనిజ సంపద, పరిశ్రమలు, చారిత్రక అంశాలు & పోటీ పరీక్షల కీలక సమాచారం.
      </p>
    </div>

    <!-- Filter Buttons & Search -->
    <div class="flex flex-wrap justify-between items-center gap-3 no-print">
      <div class="flex items-center gap-2">
        <a href="/districts_guide?state=all" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition { 'bg-blue-600 text-white border-blue-600 shadow-md' if state_filter == 'all' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300' }">
          మొత్తం జిల్లాలు ({len(districts)})
        </a>
        <a href="/districts_guide?state=ap" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition { 'bg-blue-600 text-white border-blue-600 shadow-md' if state_filter == 'ap' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300' }">
          🚩 ఆంధ్రప్రదేశ్ (26 జిల్లాలు)
        </a>
        <a href="/districts_guide?state=ts" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition { 'bg-rose-600 text-white border-rose-600 shadow-md' if state_filter == 'ts' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300' }">
          🌾 తెలంగాణ
        </a>
      </div>
      <div class="relative w-full sm:w-72">
        <input type="text" id="distSearch" oninput="filterDistricts()" placeholder="జిల్లా, నది, ప్రాజెక్ట్ లేదా ఖనిజం శోధించండి..." class="w-full text-xs px-3.5 py-2 pl-9 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white shadow-xs">
        <i class="fa-solid fa-search text-slate-400 absolute left-3 top-2.5 text-xs"></i>
      </div>
    </div>

    <!-- Districts Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5" id="districtsGrid">
      {cards_html}
    </div>

  </main>

  <script>
    function filterDistricts() {{
      const query = document.getElementById('distSearch').value.toLowerCase();
      document.querySelectorAll('.district-card').forEach(card => {{
        const text = card.innerText.toLowerCase();
        if (text.includes(query)) {{
          card.style.display = '';
        }} else {{
          card.style.display = 'none';
        }}
      }});
    }}
  </script>
</body>
</html>"""
    return html
