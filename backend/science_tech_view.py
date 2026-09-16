# -*- coding: utf-8 -*-
"""
Interactive Web View for Science, Technology & Defense 2025–2026 Mega Hub (/science_tech_hub).
"""

from science_tech_data import get_science_tech_data

def render_science_tech_html():
    data = get_science_tech_data()
    categories = data["categories"]
    mcqs = data.get("mcqs", [])

    cat_sections_html = ""
    for cat in categories:
        topics_html = ""
        for top in cat["topics"]:
            kps_html = "".join([f"<li class='text-slate-700 leading-relaxed font-medium'><i class='fa-solid fa-circle-check text-emerald-600 text-xs mr-1.5'></i>{kp}</li>" for kp in top["key_points"]])
            
            topics_html += f"""
            <div class="topic-card p-5 bg-white border border-slate-200 rounded-2xl shadow-2xs hover:shadow-md transition space-y-3" data-name="{top['name'].lower()}" data-agency="{top['agency'].lower()}">
              <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
                <span class="px-2.5 py-1 bg-indigo-50 text-indigo-900 text-xs font-black rounded-lg border border-indigo-200">
                  {top['agency']}
                </span>
                <span class="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 text-[11px] font-bold rounded-full">
                  {top['status']}
                </span>
              </div>
              <h4 class="font-black text-slate-900 text-base sm:text-lg leading-snug">{top['name']}</h4>
              <p class="text-xs sm:text-sm text-slate-800 font-semibold leading-relaxed bg-slate-50 p-3 rounded-xl border border-slate-100">{top['summary']}</p>
              
              <div class="space-y-1.5 pt-1">
                <h5 class="text-xs font-black uppercase text-slate-500 tracking-wider">కీలక పరీక్షా అంశాలు (Key Points):</h5>
                <ul class="space-y-1 text-xs sm:text-sm">
                  {kps_html}
                </ul>
              </div>

              <div class="text-[11px] text-amber-900 bg-amber-50/80 p-2.5 rounded-xl border border-amber-200 font-bold flex items-start gap-1.5">
                <i class="fa-solid fa-bullseye text-amber-600 mt-0.5 shrink-0"></i>
                <span>పరీక్షా ప్రాధాన్యత: {top['exam_relevance']}</span>
              </div>
            </div>
            """

        cat_sections_html += f"""
        <div class="cat-section space-y-4 pt-2" id="cat-{cat['id']}">
          <div class="p-4 bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl shadow-sm flex flex-wrap items-center justify-between gap-3">
            <div class="flex items-center gap-3">
              <span class="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center text-amber-400 text-lg">
                <i class="fa-solid {cat['icon']}"></i>
              </span>
              <div>
                <h3 class="text-base sm:text-lg font-black text-white">{cat['name']}</h3>
                <p class="text-xs text-slate-300 font-medium">తాజా పరిశోధనలు, ప్రాజెక్టులు మరియు రక్షణ పరిజ్ఞానం</p>
              </div>
            </div>
            <span class="px-3 py-1 bg-white/10 rounded-full text-xs font-bold text-slate-200 border border-white/10">
              {len(cat['topics'])} అంశాలు
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
            <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">🔬 {q.get('exam_tag', 'సైన్స్ & టెక్')}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('st_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_st_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
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
  <title>సైన్స్, టెక్నాలజీ & రక్షణ రంగం 2025-2026 మాస్టర్ హబ్ - లక్ష్య</title>
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
          <span>🛰️</span> <span>సైన్స్ & టెక్నాలజీ, డిఫెన్స్ 2025–2026 మెగా హబ్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/science_technology_defense_master.pdf" download="science_technology_defense_master.pdf" class="text-xs bg-cyan-400 hover:bg-cyan-300 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
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
        <span class="bg-cyan-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          సైన్స్ & టెక్నాలజీ స్పెషల్ ఎడిషన్
        </span>
        <span class="text-xs text-indigo-200 font-medium">2025–2026 పరీక్షలకు సమగ్ర రివిజన్</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">సైన్స్, టెక్నాలజీ & రక్షణ రంగం – జాతీయ సమగ్ర సమాహారం</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        గగన్‌యాన్, చంద్రయాన్-4, శుక్రయాన్, అగ్ని-5 MIRV (మిషన్ దివ్యాస్త్ర), INS అరిఘాట్, తేజస్ Mk1A, జోరావర్ ట్యాంక్, ఇండియాఏఐ మిషన్, క్వాంటం మిషన్, సెమీకండక్టర్లు మరియు BioE3 పాలసీల సంపూర్ణ తెలుగు విశ్లేషణ.
      </p>

      <!-- Category Jump Pills (no-print) -->
      <div class="no-print pt-3 flex flex-wrap gap-2">
        <a href="#cat-space" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-cyan-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-rocket text-cyan-400"></i> అంతరిక్షం & ఇస్రో
        </a>
        <a href="#cat-defense" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-rose-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-shield-halved text-rose-400"></i> రక్షణ & క్షిపణులు
        </a>
        <a href="#cat-ai_quantum" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-amber-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-microchip text-amber-400"></i> AI, క్వాంటం & చిప్స్
        </a>
        <a href="#cat-biotech_energy" class="px-3 py-1.5 bg-slate-900/90 border border-slate-700 hover:border-emerald-400 rounded-xl text-xs font-bold text-slate-200 transition flex items-center gap-1.5">
          <i class="fa-solid fa-dna text-emerald-400"></i> బయోటెక్ & గ్రీన్ ఎనర్జీ
        </a>
      </div>
    </div>

    <!-- Topics Section -->
    <section class="space-y-8">
      {cat_sections_html}
    </section>

    <!-- MCQs Section -->
    <section class="space-y-4 pt-4 border-t border-slate-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📝</span> <span>సైన్స్ & టెక్నాలజీ ప్రాక్టీస్ ప్రశ్నలు (High-Yield MCQs)</span>
        </h3>
        <span class="text-xs font-black text-cyan-950 bg-cyan-100 px-3 py-1 rounded-full">
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
