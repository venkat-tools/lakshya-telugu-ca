# -*- coding: utf-8 -*-
"""
Interactive Web View for AP & TS Schemes Eligibility & Comparison Matrix (/schemes_matrix).
"""

from schemes_matrix_data import get_schemes_matrix_data

def render_schemes_matrix_html():
    schemes = get_schemes_matrix_data()

    cards_html = ""
    for s in schemes:
        state_badge = '<span class="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-black rounded-md">ఆంధ్రప్రదేశ్</span>' if s["state"] == "ఆంధ్రప్రదేశ్" else '<span class="px-2.5 py-0.5 bg-blue-100 text-blue-800 text-xs font-black rounded-md">తెలంగాణ</span>'

        cards_html += f"""
        <article class="scheme-item bg-white border border-slate-200 rounded-3xl p-6 shadow-sm space-y-4" data-state="{s['state']}" data-cat="{s['category']}">
          <div class="flex flex-wrap justify-between items-start gap-2 border-b border-slate-100 pb-3">
            <div class="flex items-center gap-2">
              {state_badge}
              <span class="px-2.5 py-0.5 bg-slate-100 text-slate-700 text-xs font-bold rounded-md">{s['category']}</span>
            </div>
            <span class="text-xs font-black text-indigo-900 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-200">బడ్జెట్: {s['budget']}</span>
          </div>

          <div>
            <h4 class="text-base sm:text-lg font-black text-slate-900 leading-snug">{s['scheme']}</h4>
            <p class="text-xs sm:text-sm text-emerald-900 font-bold bg-emerald-50/70 p-3 rounded-xl border border-emerald-200 mt-2">
              💰 ఆర్థిక ప్రయోజనం: {s['benefit']}
            </p>
          </div>

          <!-- 4-Grid Parameters -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-700">
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <strong class="text-slate-900 block mb-0.5 font-bold">ఆదాయ పరిమితి (Income):</strong>
              <span>{s['income_limit']}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <strong class="text-slate-900 block mb-0.5 font-bold">వయోపరిమితి & అర్హత:</strong>
              <span>{s['age_limit']}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <strong class="text-slate-900 block mb-0.5 font-bold">భూమి నిబంధన (Land):</strong>
              <span>{s['land_limit']}</span>
            </div>
            <div class="p-3 bg-slate-50 rounded-xl border border-slate-200">
              <strong class="text-slate-900 block mb-0.5 font-bold">నోడల్ శాఖ & DBT పోర్టల్:</strong>
              <span class="text-indigo-800 font-semibold">{s['nodal_dept']} ({s['portal']})</span>
            </div>
          </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>AP & TS ప్రభుత్వ పథకాల అర్హతల పోలిక మ్యాట్రిక్స్ - లక్ష్య పోటీ పరీక్షలు</title>
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
          <span>🌾</span> <span>AP & TS సంక్షేమ పథకాల సమగ్ర పోలిక మ్యాట్రిక్స్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Card -->
    <div class="bg-gradient-to-r from-emerald-950 via-slate-900 to-teal-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-2 border border-emerald-900/60 relative overflow-hidden">
      <div class="flex items-center gap-2">
        <span class="bg-amber-400 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded-full uppercase tracking-wider">
          SCHEMES COMPARISON MATRIX
        </span>
        <span class="text-xs text-emerald-300 font-semibold">ఆంధ్రప్రదేశ్ సూపర్ సిక్స్ vs తెలంగాణ 6 గ్యారెంటీలు</span>
      </div>
      <h2 class="text-xl sm:text-2xl font-black text-white">పథకాల లబ్ధి, ఆదాయ పరిమితి, వయస్సు & నోడల్ శాఖల పోలిక</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
        పోటీ పరీక్షలలో తరచుగా అడిగే అర్హత నిబంధనలు, ఆదాయ పరిమితులు, బడ్జెట్ కేటాయింపులు మరియు డీబీటీ పోర్టల్స్ సమగ్ర సమాచారం.
      </p>
    </div>

    <!-- Filters Bar -->
    <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-3 no-print">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <!-- State Pills -->
        <div class="flex items-center gap-2">
          <span class="text-xs font-black text-slate-700">రాష్ట్రం:</span>
          <button onclick="filterState('all')" class="state-btn active px-3 py-1 rounded-lg text-xs font-bold bg-slate-900 text-white" data-state="all">అన్నీ</button>
          <button onclick="filterState('ఆంధ్రప్రదేశ్')" class="state-btn px-3 py-1 rounded-lg text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-300" data-state="ఆంధ్రప్రదేశ్">ఆంధ్రప్రదేశ్</button>
          <button onclick="filterState('తెలంగాణ')" class="state-btn px-3 py-1 rounded-lg text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-300" data-state="తెలంగాణ">తెలంగాణ</button>
        </div>

        <!-- Search input -->
        <input 
          type="text" 
          id="schemeSearch" 
          onkeyup="searchSchemes()" 
          placeholder="పథకం పేరుతో వెతకండి (ఉదా: రైతు, దీపం, మహాలక్ష్మి)..."
          class="bg-slate-50 border border-slate-300 rounded-xl px-3.5 py-1.5 text-xs text-slate-800 w-64 outline-none focus:ring-1 focus:ring-emerald-500"
        />
      </div>
    </div>

    <!-- Schemes Cards Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-5" id="schemesContainer">
      {cards_html}
    </div>

  </main>

  <script>
    let activeState = 'all';

    function filterState(st) {{
      activeState = st;
      document.querySelectorAll('.state-btn').forEach(btn => {{
        if (btn.getAttribute('data-state') === st) {{
          btn.className = 'state-btn active px-3 py-1 rounded-lg text-xs font-bold bg-slate-900 text-white';
        }} else {{
          btn.className = 'state-btn px-3 py-1 rounded-lg text-xs font-bold bg-slate-100 text-slate-700 hover:bg-slate-200 border border-slate-300';
        }}
      }});
      applyFilters();
    }}

    function searchSchemes() {{
      applyFilters();
    }}

    function applyFilters() {{
      const query = document.getElementById('schemeSearch').value.toLowerCase().trim();
      document.querySelectorAll('.scheme-item').forEach(card => {{
        const cardState = card.getAttribute('data-state');
        const text = card.textContent.toLowerCase();
        const matchesState = (activeState === 'all' || cardState === activeState);
        const matchesSearch = (!query || text.includes(query));

        if (matchesState && matchesSearch) {{
          card.classList.remove('hidden');
        }} else {{
          card.classList.add('hidden');
        }}
      }});
    }}
  </script>
</body>
</html>
"""
    return html
