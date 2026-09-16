# -*- coding: utf-8 -*-
"""
Interactive Web View for Constitutional Amendments & Landmark Judgments (/amendments_judgments).
"""

from amendments_judgments_data import get_amendments_judgments_data

def render_amendments_judgments_html():
    data = get_amendments_judgments_data()
    amendments = data["amendments"]
    judgments = data["judgments"]
    mcqs = data["mcqs"]

    # Amendments HTML
    am_cards = ""
    for am in amendments:
        am_cards += f"""
        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-2">
          <div class="flex justify-between items-start gap-2">
            <h4 class="font-black text-slate-900 text-sm sm:text-base">{am['num']}</h4>
            <span class="px-2.5 py-0.5 bg-amber-100 text-amber-900 text-xs font-black rounded">{am['importance']}</span>
          </div>
          <p class="text-xs sm:text-sm text-slate-700 leading-relaxed font-medium">{am['key_changes']}</p>
        </div>
        """

    # Judgments HTML
    jd_cards = ""
    for jd in judgments:
        jd_cards += f"""
        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-2.5">
          <div class="flex flex-wrap justify-between items-start gap-2 border-b border-slate-100 pb-2">
            <h4 class="font-black text-indigo-950 text-sm sm:text-base">⚖️ {jd['case']}</h4>
            <span class="px-2.5 py-0.5 bg-indigo-50 text-indigo-700 text-xs font-bold rounded">{jd['bench']}</span>
          </div>
          <p class="text-xs sm:text-sm text-slate-800 leading-relaxed"><strong class="text-slate-900 font-bold">తీర్పు సారాంశం:</strong> {jd['ruling']}</p>
          <div class="text-[11px] text-emerald-800 bg-emerald-50 p-2 rounded-lg border border-emerald-200 font-semibold">
            📌 పరీక్షా ప్రాధాన్యత: {jd['exam_relevance']}
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
            <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">⚖️ {q['exam_tag']}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('am_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_am_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
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
  <title>భారత రాజ్యాంగ సవరణలు & సుప్రీంకోర్టు చారిత్రక తీర్పులు - లక్ష్య పోటీ పరీక్షలు</title>
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
          <span>⚖️</span> <span>భారత రాజ్యాంగ సవరణలు (1-106) & సుప్రీంకోర్టు తీర్పులు</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/constitution_amendments_judgments_guide.pdf" download="constitution_amendments_judgments_guide.pdf" class="text-xs bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
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
    <div class="bg-gradient-to-r from-slate-950 via-purple-950 to-indigo-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-purple-900/60 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          పాలిటీ స్పెషల్ ఎడిషన్ (Polity Core)
        </span>
        <span class="text-xs text-purple-200 font-medium">1951 నుండి 2024 వరకు సమగ్ర క్రోనాలజీ</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">రాజ్యాంగ సవరణల ప్రస్థానం & మైలురాయి తీర్పులు</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        1వ సవరణ నుండి 106వ మహిళా రిజర్వేషన్ల సవరణ వరకు కీలక సవరణల విశ్లేషణ, కేశవానంద భారతి మౌలిక స్వరూప సిద్ధాంతం, ఎస్.ఆర్. బొమ్మై, పుట్టస్వామి తీర్పులు మరియు పరీక్షల ప్రశ్నలు.
      </p>
    </div>

    <!-- Amendments Section -->
    <section class="space-y-4">
      <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
        <span>📜</span> <span>కీలక రాజ్యాంగ సవరణల సమగ్ర జాబితా (1st to 106th Amendments)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {am_cards}
      </div>
    </section>

    <!-- Landmark Judgments Section -->
    <section class="space-y-4">
      <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
        <span>⚖️</span> <span>సుప్రీంకోర్టు చారిత్రాత్మక తీర్పులు (Landmark Judgments)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {jd_cards}
      </div>
    </section>

    <!-- MCQs Section -->
    <section class="space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📝</span> <span>సవరణలు & తీర్పుల ప్రాక్టీస్ ప్రశ్నలు (High-Yield MCQs)</span>
        </h3>
        <button onclick="toggleAllSolutions()" class="text-xs bg-slate-800 hover:bg-slate-700 text-white font-bold px-3 py-1.5 rounded-lg no-print">
          అన్ని సమాధానాలు చూపించు
        </button>
      </div>

      <div class="space-y-4">
        {mcq_cards}
      </div>
    </section>

  </main>

  <script>
    function toggleSolution(id) {{
      const sol = document.getElementById("sol_" + id);
      if (sol) {{
        sol.classList.toggle("hidden");
      }}
    }}

    let allShown = false;
    function toggleAllSolutions() {{
      allShown = !allShown;
      document.querySelectorAll(".solution-box").forEach(el => {{
        if (allShown) el.classList.remove("hidden");
        else el.classList.add("hidden");
      }});
    }}
  </script>
</body>
</html>
"""
    return html
