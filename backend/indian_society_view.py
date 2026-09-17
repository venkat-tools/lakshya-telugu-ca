# -*- coding: utf-8 -*-
"""
Interactive Web View for Indian Society Master Compendium (/indian_society_hub).
Covers Structure of Indian Society, Social Issues, and Welfare Mechanism & Safeguards.
"""

from indian_society_data import get_indian_society_data

def render_indian_society_html():
    data = get_indian_society_data()
    units = data["units"]
    mcqs = data.get("mcqs", [])

    units_html = ""
    for u in units:
        topics_html = ""
        for top in u["topics"]:
            details_li = "".join([f"<li class='text-slate-700 leading-relaxed font-medium'><i class='fa-solid fa-circle-dot text-indigo-600 text-xs mr-2'></i>{d}</li>" for d in top["details"]])
            
            theorists_badge = ""
            if "theorists" in top and top["theorists"]:
                theorists_badge = f"""
                <div class="text-[11px] text-purple-950 bg-purple-50 p-2.5 rounded-xl border border-purple-200 font-bold flex items-center gap-1.5">
                  <i class="fa-solid fa-graduation-cap text-purple-700"></i>
                  <span>కీలక సామాజిక శాస్త్రవేత్తలు & సిద్ధాంతాలు: {top['theorists']}</span>
                </div>
                """

            topics_html += f"""
            <div class="topic-card p-5 bg-white border border-slate-200 rounded-2xl shadow-2xs hover:shadow-md transition space-y-3" data-name="{top['name'].lower()}">
              <div class="flex items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
                <h4 class="font-black text-slate-900 text-base sm:text-lg leading-snug">{top['name']}</h4>
                <span class="px-2.5 py-0.5 bg-indigo-50 text-indigo-900 text-xs font-black rounded-lg border border-indigo-200">కోర్ సిలబస్</span>
              </div>
              <p class="text-xs sm:text-sm text-slate-800 font-semibold bg-slate-50 p-3 rounded-xl border border-slate-100">{top['core_concepts']}</p>
              
              <div class="space-y-1.5 pt-1">
                <h5 class="text-xs font-black uppercase text-slate-500 tracking-wider">ముఖ్యమైన పరీక్షా ముఖ్యాంశాలు:</h5>
                <ul class="space-y-1.5 text-xs sm:text-sm">
                  {details_li}
                </ul>
              </div>

              {theorists_badge}
            </div>
            """

        units_html += f"""
        <div class="unit-section space-y-4 pt-2" id="{u['id']}">
          <div class="p-4 bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl shadow-sm flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <span class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-amber-400 text-lg">
                <i class="fa-solid {u['icon']}"></i>
              </span>
              <div>
                <h3 class="text-base sm:text-lg font-black text-white">{u['title']}</h3>
                <p class="text-xs text-slate-300 font-medium">సిద్ధాంతాలు, కేస్ స్టడీలు, చట్టాలు & రాజ్యాంగ నిబంధనలు</p>
              </div>
            </div>
            <span class="px-3 py-1 bg-white/10 rounded-full text-xs font-bold text-slate-200 border border-white/10">
              {len(u['topics'])} అధ్యాయాలు
            </span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            {topics_html}
          </div>
        </div>
        """

    # MCQs HTML
    mcq_cards = ""
    opt_letters = ["A", "B", "C", "D"]
    for idx, q in enumerate(mcqs, 1):
        corr = q["key"].upper()
        opts_html = ""
        for opt_idx, opt_text in enumerate(q["options"]):
            letter = opt_letters[opt_idx]
            opts_html += f"""
            <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm flex items-start gap-2.5 font-medium">
              <span class="w-6 h-6 rounded-full bg-slate-200 text-slate-800 text-xs font-black flex items-center justify-center shrink-0">{letter}</span>
              <span class="text-slate-800 leading-relaxed">{opt_text}</span>
            </div>
            """

        mcq_cards += f"""
        <article class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4">
          <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-2.5">
            <span class="bg-indigo-100 text-indigo-900 font-black text-xs px-2.5 py-0.5 rounded-md">ప్రశ్న {idx}</span>
            <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">👥 {q.get('exam_tag', 'భారతీయ సమాజం')}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('soc_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_soc_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
            <div class="flex items-center gap-2 font-black text-emerald-900">
              <span class="px-2 py-0.5 bg-emerald-600 text-white rounded text-xs">సరైన సమాధానం: ఆప్షన్ {corr}</span>
            </div>
            <p class="text-slate-800 leading-relaxed pt-1">{q['explanation']}</p>
          </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>భారతీయ సమాజం (Indian Society - 30 మార్కులు) సమగ్ర మాస్టర్ హబ్ - లక్ష్య</title>
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
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/appsc_syllabus" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>👥</span> <span>భారతీయ సమాజం (Indian Society - 30 Marks)</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/indian_society_master_compendium.pdf" download="indian_society_master_compendium.pdf" class="text-xs bg-amber-400 hover:bg-amber-300 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-file-pdf"></i> మాస్టర్ PDF డౌన్‌లోడ్
        </a>
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-8">

    <!-- Hero Banner -->
    <div class="bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-indigo-900/40 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          APPSC గ్రూప్-2 ప్రిలిమ్స్ స్పెషల్ (30 Marks Section)
        </span>
        <span class="text-xs text-indigo-200 font-medium">సంపూర్ణ పాఠ్య ప్రణాళిక & సాధన ప్రశ్నలు</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">భారతీయ సమాజం, సామాజిక సమస్యలు & సంక్షేమ యంత్రాంగం</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        కుటుంబం, వివాహం, బంధుత్వం, కుల వ్యవస్థ (సంస్కృతీకరణ), 75 PVTGs తెగలు, మహిళల స్థితిగతులు, కులతత్వం, మతతత్వం, పేదరికం, SC/ST అట్రాసిటీల చట్టం, PESA 1996, దివ్యాంగుల హక్కులు మరియు రాజ్యాంగ రక్షణల సమగ్ర అధ్యయనం.
      </p>

      <!-- Unit Jump Pills (no-print) -->
      <div class="no-print pt-3 flex flex-wrap gap-2">
        <a href="#unit_1" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-amber-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-people-roof text-amber-400"></i> యూనిట్ 1: సామాజిక నిర్మాణం
        </a>
        <a href="#unit_2" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-rose-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-triangle-exclamation text-rose-400"></i> యూనిట్ 2: సామాజిక సమస్యలు
        </a>
        <a href="#unit_3" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-emerald-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-scale-balanced text-emerald-400"></i> యూనిట్ 3: సంక్షేమ చట్టాలు & రక్షణలు
        </a>
      </div>
    </div>

    <!-- Units Section -->
    <section class="space-y-8">
      {units_html}
    </section>

    <!-- MCQs Section -->
    <section class="space-y-4 pt-4 border-t border-slate-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📝</span> <span>భారతీయ సమాజం ప్రాక్టీస్ ప్రశ్నలు (High-Yield MCQs)</span>
        </h3>
        <span class="text-xs font-black text-indigo-950 bg-indigo-100 px-3 py-1 rounded-full">
          {len(mcqs)} ప్రశ్నలు & సమగ్ర వివరణలు
        </span>
      </div>
      <div class="grid grid-cols-1 gap-4">
        {mcq_cards}
      </div>
    </section>

  </main>

  <script>
    function toggleSolution(id) {{
      const el = document.getElementById('sol_' + id);
      if (el) {{
        el.classList.toggle('hidden');
      }}
    }}
  </script>
</body>
</html>"""

    return html
