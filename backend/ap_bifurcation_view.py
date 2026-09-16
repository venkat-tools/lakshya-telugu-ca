# -*- coding: utf-8 -*-
"""
Interactive Web View for AP Reorganisation Act 2014 Master Guide (/ap_bifurcation_guide).
"""

from ap_bifurcation_data import get_bifurcation_data

def render_ap_bifurcation_html():
    data = get_bifurcation_data()
    ov = data["overview"]
    parts = data["parts"]
    schedules = data["schedules"]
    mcqs = data["mcqs"]

    # Parts HTML
    parts_html = ""
    for p in parts:
        parts_html += f"""
        <div class="p-5 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-2">
          <div class="flex justify-between items-start gap-2">
            <h4 class="font-black text-slate-900 text-sm sm:text-base">{p['part']}</h4>
            <span class="px-2.5 py-0.5 bg-blue-100 text-blue-900 text-xs font-black rounded">{p['title']}</span>
          </div>
          <p class="text-xs sm:text-sm text-slate-700 leading-relaxed">{p['details']}</p>
        </div>
        """

    # Schedules HTML
    sched_rows = ""
    for s in schedules:
        sched_rows += f"""
        <tr class="border-b border-slate-100 text-xs sm:text-sm hover:bg-slate-50">
          <td class="p-3 font-black text-blue-900 whitespace-nowrap">{s['num']}</td>
          <td class="p-3 font-bold text-slate-800">{s['subject']}</td>
          <td class="p-3 text-slate-600 leading-relaxed">{s['content']}</td>
        </tr>
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
            <span class="bg-blue-100 text-blue-900 font-black text-xs px-2.5 py-0.5 rounded-md">ప్రశ్న {idx}</span>
            <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">📂 {q['exam_tag']}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('bf_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_bf_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
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
  <title>ఆంధ్రప్రదేశ్ పునర్విభజన చట్టం 2014 మాస్టర్ గైడ్ - లక్ష్య పోటీ పరీక్షలు</title>
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
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ & PDF హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>📜</span> <span>ఆంధ్రప్రదేశ్ పునర్విభజన చట్టం 2014 మాస్టర్ గైడ్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/ap_reorganisation_act_master_guide.pdf" download="ap_reorganisation_act_master_guide.pdf" class="text-xs bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
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
    <div class="bg-gradient-to-r from-slate-950 via-blue-950 to-indigo-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-blue-900/60 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          APPSC గ్రూప్ 1 & 2 స్పెషల్ సిలబస్ (15-20 మార్కులు)
        </span>
        <span class="text-xs text-blue-200 font-medium">Act No. 6 of 2014</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">ఆంధ్రప్రదేశ్ పునర్విభజన చట్టం, 2014 సమగ్ర విశ్లేషణ</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        మొత్తం 108 సెక్షన్లు, 12 భాగాలు, 13 షెడ్యూళ్లు, పోలవరం (సెక్షన్ 90), రాజధాని నిధులు (సెక్షన్ 94), ఆస్తుల విభజన వివాదాలు (షెడ్యూల్ 9 & 10) మరియు పరీక్షోపయుక్త ప్రశ్నలు.
      </p>
    </div>

    <!-- Overview Key Metrics Cards -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm text-center">
        <span class="text-xs text-slate-500 font-bold block">లోక్‌సభ ఆమోదం</span>
        <strong class="text-sm sm:text-base font-black text-slate-900">{ov['passed_lok_sabha']}</strong>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm text-center">
        <span class="text-xs text-slate-500 font-bold block">రాజ్యసభ ఆమోదం</span>
        <strong class="text-sm sm:text-base font-black text-slate-900">{ov['passed_rajya_sabha']}</strong>
      </div>
      <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm text-center">
        <span class="text-xs text-slate-500 font-bold block">రాష్ట్రపతి ఆమోదం</span>
        <strong class="text-sm sm:text-base font-black text-slate-900">{ov['president_assent']}</strong>
      </div>
      <div class="bg-white border-2 border-emerald-500/40 rounded-2xl p-4 shadow-sm text-center">
        <span class="text-xs text-emerald-800 font-bold block">నియమిత దినం (Appointed Day)</span>
        <strong class="text-sm sm:text-base font-black text-emerald-700">{ov['appointed_day']}</strong>
      </div>
    </div>

    <!-- 12 Parts Detailed Section -->
    <section class="space-y-4">
      <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
        <span>📑</span> <span>చట్టంలోని 12 భాగాలు & కీలక సెక్షన్ల సారాంశం (108 Sections)</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {parts_html}
      </div>
    </section>

    <!-- 13 Schedules Section -->
    <section class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
      <h3 class="text-lg font-black text-slate-900 flex items-center gap-2 border-b pb-3">
        <span>📋</span> <span>పునర్విభజన చట్టంలోని 13 షెడ్యూళ్ల సమగ్ర పట్టిక (13 Schedules)</span>
      </h3>
      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 text-slate-700 text-xs uppercase tracking-wider border-b border-slate-200">
              <th class="p-3 whitespace-nowrap">షెడ్యూల్</th>
              <th class="p-3 whitespace-nowrap">విషయం</th>
              <th class="p-3">ప్రధానాంశాలు & పరీక్ష ముఖ్యాంశాలు</th>
            </tr>
          </thead>
          <tbody>
            {sched_rows}
          </tbody>
        </table>
      </div>
    </section>

    <!-- MCQs Section -->
    <section class="space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📝</span> <span>AP పునర్విభజన చట్టం ప్రాక్టీస్ ప్రశ్నలు (Official APPSC MCQs)</span>
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
