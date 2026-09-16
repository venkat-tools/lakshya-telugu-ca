# -*- coding: utf-8 -*-
"""
Interactive PYQs Master Hub Web View (/pyqs_hub).
Renders official solved question papers with official keys and detailed Telugu solutions.
"""

from pyqs_master_data import get_all_pyq_papers, get_all_pyq_questions

def render_pyqs_hub_html(selected_paper="all"):
    papers = get_all_pyq_papers()
    all_questions = get_all_pyq_questions()

    if selected_paper != "all" and selected_paper in papers:
        display_qs = [q for q in all_questions if q.get("paper_id") == selected_paper]
        page_title = papers[selected_paper]["title"]
    else:
        display_qs = all_questions
        page_title = "APPSC & TSPSC అధికారిక సాల్వ్డ్ పేపర్స్ హబ్ (2017-2024)"

    # Nav buttons
    nav_tabs = f'''
    <a href="/pyqs_hub?paper=all" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition { "bg-blue-600 text-white border-blue-600 shadow-md" if selected_paper == "all" else "bg-white text-slate-700 hover:bg-slate-100 border-slate-300" }">
      🔍 అన్ని పేపర్లు ({len(all_questions)} Qs)
    </a>
    '''
    for p_id, p_info in papers.items():
        is_active = (selected_paper == p_id)
        nav_tabs += f'''
        <a href="/pyqs_hub?paper={p_id}" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition { "bg-blue-600 text-white border-blue-600 shadow-md" if is_active else "bg-white text-slate-700 hover:bg-slate-100 border-slate-300" }">
          📜 {p_info['title']} ({len(p_info['questions'])} Qs)
        </a>
        '''

    # Question Cards
    q_cards = ""
    for idx, q in enumerate(display_qs, 1):
        corr = q["key"].upper()
        opts_html = ""
        opt_letters = ["A", "B", "C", "D"]
        for opt_idx, opt_text in enumerate(q["options"]):
            letter = opt_letters[opt_idx] if opt_idx < 4 else f"O{opt_idx+1}"
            opts_html += f'''
            <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm flex items-start gap-2.5 font-medium opt-item" data-letter="{letter}">
              <span class="w-6 h-6 rounded-full bg-slate-200 text-slate-800 text-xs font-black flex items-center justify-center shrink-0 opt-badge">{letter}</span>
              <span class="text-slate-800 leading-relaxed">{opt_text}</span>
            </div>
            '''

        q_cards += f'''
        <article class="pyq-card bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4" id="pyq_{q["id"]}">
          <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="bg-blue-100 text-blue-900 font-black text-xs px-2.5 py-0.5 rounded-md">ప్రశ్న {idx}</span>
              <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">📂 {q.get("section", "General Studies")}</span>
            </div>
            <span class="text-xs text-slate-500 font-semibold">{q.get("paper_title", "")}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed whitespace-pre-line">{q["question"]}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="flex items-center justify-between pt-2">
            <button type="button" onclick="toggleSolution('sol_{q["id"]}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5 no-print">
              <span>💡 అధికారిక కీ & వివరణ చూపించు</span>
            </button>
            <span class="text-[11px] text-slate-400 font-mono">ID: {q["id"]}</span>
          </div>

          <div id="sol_{q["id"]}" class="solution-box hidden p-4 bg-emerald-50/80 border border-emerald-300 rounded-xl space-y-2 text-xs">
            <div class="flex items-center gap-2 font-black text-emerald-950">
              <span class="bg-emerald-600 text-white px-2 py-0.5 rounded text-[10px]">అధికారిక ఫైనల్ కీ: {corr}</span>
              <span>సమగ్ర విశ్లేషణ:</span>
            </div>
            <p class="text-emerald-900 leading-relaxed font-medium">{q["explanation"]}</p>
          </div>
        </article>
        '''

    html = f'''<!DOCTYPE html>
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
      .solution-box {{ display: block !important; }}
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
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ & PDF హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>📜</span> <span>APPSC & TSPSC అధికారిక సాల్వ్డ్ PYQs</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/appsc_tspsc_solved_pyqs_master.pdf" download="appsc_tspsc_solved_pyqs_master.pdf" class="text-xs bg-amber-500 hover:bg-amber-400 text-slate-950 font-black px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-file-pdf"></i> మాస్టర్ PDF డౌన్‌లోడ్
        </a>
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
        <button onclick="toggleAllSolutions()" class="text-xs bg-emerald-700 hover:bg-emerald-600 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-eye"></i> అన్ని సమాధానాలు
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Banner -->
    <div class="bg-gradient-to-r from-blue-950 via-slate-900 to-indigo-950 text-white p-6 rounded-3xl shadow-lg space-y-2 border border-blue-900/60">
      <div class="flex justify-between items-center">
        <span class="bg-amber-400 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded-full uppercase tracking-wider">
          అధికారిక ఫైనల్ కీ ఆధారంగా
        </span>
        <span class="text-xs text-blue-200 font-bold">మొత్తం: {len(display_qs)} ప్రశ్నలు</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black">{page_title}</h2>
      <p class="text-xs sm:text-sm text-slate-300 font-medium">
        APPSC గ్రూప్-2 2024 ప్రిలిమ్స్, 2019 స్క్రీనింగ్, TSPSC గ్రూప్ 1 & 2 అధికారిక ప్రశ్నలు మరియు సమగ్ర తెలుగు విశ్లేషణలు.
      </p>
    </div>

    <!-- Paper Filters -->
    <div class="flex items-center gap-2 overflow-x-auto pb-2 no-print">
      {nav_tabs}
    </div>

    <!-- Questions List -->
    <div class="space-y-4">
      {q_cards}
    </div>

  </main>

  <script>
    function toggleSolution(id) {{
      const el = document.getElementById(id);
      if (el) el.classList.toggle('hidden');
    }}

    let allShown = false;
    function toggleAllSolutions() {{
      allShown = !allShown;
      document.querySelectorAll('.solution-box').forEach(el => {{
        if (allShown) el.classList.remove('hidden');
        else el.classList.add('hidden');
      }});
    }}
  </script>
</body>
</html>'''
    return html
