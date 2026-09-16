# -*- coding: utf-8 -*-
"""
Interactive Web View for Sunday Weekly Current Affairs Digest & 50-MCQ Mega Test (/weekly_digest).
"""

from weekly_compiler import get_weekly_digest_data

def render_weekly_digest_html():
    data = get_weekly_digest_data()
    edition = data["edition"]
    questions = data["questions"]
    articles = data["articles"]

    # Articles HTML
    art_html = ""
    for a in articles:
        title = a["title"] if isinstance(a, dict) else a[3]
        summary = a["summary"] if isinstance(a, dict) else a[4]
        cat = a.get("category", "జనరల్") if isinstance(a, dict) else a[2]
        art_html += f"""
        <div class="p-4 bg-white border border-slate-200 rounded-2xl shadow-2xs space-y-1.5">
          <span class="px-2 py-0.5 bg-blue-100 text-blue-900 text-[10px] font-black rounded">{cat}</span>
          <h4 class="text-sm font-black text-slate-900 leading-snug">{title}</h4>
          <p class="text-xs text-slate-600 leading-relaxed">{summary}</p>
        </div>
        """

    # 50 MCQs HTML
    mcq_cards = ""
    opt_letters = ["A", "B", "C", "D"]
    for idx, q in enumerate(questions, 1):
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
            <span class="bg-purple-100 text-purple-900 font-black text-xs px-2.5 py-0.5 rounded-md">సండే టెస్ట్ ప్రశ్న {idx} / 50</span>
            <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">📂 {q['subject']}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('wm_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_wm_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
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
  <title>సండే వీక్లీ కరెంట్ అఫైర్స్ & 50 Qs మెగా టెస్ట్ - లక్ష్య పోటీ పరీక్షలు</title>
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
        <a href="/" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> హోమ్‌పేజీ
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🗓️</span> <span>సండే వీక్లీ కరెంట్ అఫైర్స్ & 50 Qs మెగా టెస్ట్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్ బుక్‌లెట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-8">

    <!-- Hero Card -->
    <div class="bg-gradient-to-r from-purple-950 via-slate-900 to-indigo-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-purple-900/60 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          సండే వీక్లీ స్పెషల్ ఎడిషన్
        </span>
        <span class="text-xs text-purple-200 font-medium">{edition['dates_range']}</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">{edition['title']}</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        {edition['lead_story']}
      </p>
    </div>

    <!-- Mode Selector Tabs -->
    <div class="flex items-center gap-3 border-b border-slate-200 pb-3 no-print">
      <button onclick="switchMode('test')" id="btnTabTest" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-black bg-purple-600 text-white shadow-sm flex items-center gap-2">
        <span>📝 50 ప్రశ్నల సండే మెగా టెస్ట్</span>
      </button>
      <button onclick="switchMode('roundup')" id="btnTabRoundup" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold bg-white text-slate-700 hover:bg-slate-100 border border-slate-300 flex items-center gap-2">
        <span>📖 వారం ముఖ్యాంశాలు (Round-up)</span>
      </button>
    </div>

    <!-- Test Container -->
    <div id="testContainer" class="space-y-4">
      <div class="flex justify-between items-center">
        <span class="text-xs font-bold text-slate-500">వారం కరెంట్ అఫైర్స్ & జీఎస్ పై 50 ప్రామాణిక ప్రశ్నలు</span>
        <button onclick="toggleAllSolutions()" class="text-xs bg-slate-800 hover:bg-slate-700 text-white font-bold px-3 py-1.5 rounded-lg no-print">
          అన్ని సమాధానాలు చూపించు
        </button>
      </div>
      <div class="space-y-4">
        {mcq_cards}
      </div>
    </div>

    <!-- Roundup Container (Hidden by default) -->
    <div id="roundupContainer" class="hidden space-y-4">
      <h3 class="text-base font-black text-slate-900">📰 నేటి వారపు ప్రధాన ఆర్టికల్స్ సంకలనం:</h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {art_html}
      </div>
    </div>

  </main>

  <script>
    function switchMode(mode) {{
      if (mode === 'test') {{
        document.getElementById('testContainer').classList.remove('hidden');
        document.getElementById('roundupContainer').classList.add('hidden');
        document.getElementById('btnTabTest').className = 'px-4 py-2 rounded-xl text-xs sm:text-sm font-black bg-purple-600 text-white shadow-sm flex items-center gap-2';
        document.getElementById('btnTabRoundup').className = 'px-4 py-2 rounded-xl text-xs sm:text-sm font-bold bg-white text-slate-700 hover:bg-slate-100 border border-slate-300 flex items-center gap-2';
      }} else {{
        document.getElementById('testContainer').classList.add('hidden');
        document.getElementById('roundupContainer').classList.remove('hidden');
        document.getElementById('btnTabRoundup').className = 'px-4 py-2 rounded-xl text-xs sm:text-sm font-black bg-purple-600 text-white shadow-sm flex items-center gap-2';
        document.getElementById('btnTabTest').className = 'px-4 py-2 rounded-xl text-xs sm:text-sm font-bold bg-white text-slate-700 hover:bg-slate-100 border border-slate-300 flex items-center gap-2';
      }}
    }}

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
