# -*- coding: utf-8 -*-
"""
Interactive Web View for AP & TS Economic Survey and Budget 2026 Master Guide (/budget_economy_guide).
"""

from budget_economy_data import get_budget_economy_data

def render_budget_economy_html(state_filter="all"):
    data = get_budget_economy_data()
    ap = data["ap"]
    ts = data["ts"]
    mcqs = data["mcqs"]

    # Sector HTML
    ap_sec_html = ""
    for sec in ap["sectoral_growth"]:
        ap_sec_html += f"""
        <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
          <div class="flex justify-between text-xs sm:text-sm font-bold">
            <span class="text-slate-800">{sec['sector']}</span>
            <span class="text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">వాటా: {sec['share']} | వృద్ధి: {sec['growth']}</span>
          </div>
          <p class="text-[11px] text-slate-600">{sec['highlights']}</p>
        </div>
        """

    ts_sec_html = ""
    for sec in ts["sectoral_growth"]:
        ts_sec_html += f"""
        <div class="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-1">
          <div class="flex justify-between text-xs sm:text-sm font-bold">
            <span class="text-slate-800">{sec['sector']}</span>
            <span class="text-blue-700 bg-blue-50 px-2 py-0.5 rounded border border-blue-200">వాటా: {sec['share']} | వృద్ధి: {sec['growth']}</span>
          </div>
          <p class="text-[11px] text-slate-600">{sec['highlights']}</p>
        </div>
        """

    # Schemes HTML
    ap_sch_html = ""
    for sch in ap["super_six_schemes"]:
        ap_sch_html += f"""
        <div class="p-4 bg-white border border-slate-200 rounded-xl shadow-2xs space-y-1.5">
          <div class="flex justify-between items-start gap-2">
            <h5 class="font-bold text-slate-900 text-sm">{sch['name']}</h5>
            <span class="text-xs font-black text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded shrink-0">{sch['allocation']}</span>
          </div>
          <p class="text-xs text-slate-700 leading-relaxed">{sch['benefit']}</p>
          <div class="text-[11px] text-slate-500 font-medium">🎯 లబ్ధిదారులు: {sch['target']}</div>
        </div>
        """

    ts_sch_html = ""
    for sch in ts["six_guarantees"]:
        ts_sch_html += f"""
        <div class="p-4 bg-white border border-slate-200 rounded-xl shadow-2xs space-y-1.5">
          <div class="flex justify-between items-start gap-2">
            <h5 class="font-bold text-slate-900 text-sm">{sch['name']}</h5>
            <span class="text-xs font-black text-blue-800 bg-blue-100 px-2 py-0.5 rounded shrink-0">{sch['allocation']}</span>
          </div>
          <p class="text-xs text-slate-700 leading-relaxed">{sch['benefit']}</p>
          <div class="text-[11px] text-slate-500 font-medium">🎯 లబ్ధిదారులు: {sch['target']}</div>
        </div>
        """

    # Projects HTML
    proj_html = ""
    for p in (ap["key_projects"] + ts["key_projects"]):
        fact = p.get('capacity') or p.get('key_fact', '')
        proj_html += f"""
        <div class="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
          <h4 class="font-black text-slate-900 text-sm flex items-center gap-1.5">
            <span class="text-amber-600">⚡</span> {p['name']}
          </h4>
          <p class="text-xs text-slate-700 leading-relaxed">{p['status']}</p>
          <div class="text-[11px] text-indigo-700 font-bold bg-indigo-50 p-2 rounded border border-indigo-100">
            📌 పరీక్షా ముఖ్యాంశం: {fact}
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
            <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm flex items-start gap-2.5 font-medium opt-item" data-letter="{letter}">
              <span class="w-6 h-6 rounded-full bg-slate-200 text-slate-800 text-xs font-black flex items-center justify-center shrink-0">{letter}</span>
              <span class="text-slate-800 leading-relaxed">{opt_text}</span>
            </div>
            """

        mcq_cards += f"""
        <article class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4" id="mcq_{q['id']}">
          <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="bg-amber-100 text-amber-900 font-black text-xs px-2.5 py-0.5 rounded-md">పరీక్ష ప్రశ్న {idx}</span>
              <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">📊 {q['exam_tag']}</span>
            </div>
            <span class="text-xs text-slate-500 font-semibold">బడ్జెట్ & సర్వే ఆధారితం</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
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
  <title>AP & TS ఎకనామిక్ సర్వే & బడ్జెట్ 2026 మాస్టర్ గైడ్ - లక్ష్య పోటీ పరీక్షలు</title>
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
          <span>📊</span> <span>AP & TS ఎకనామిక్ సర్వే & బడ్జెట్ 2026 మాస్టర్ గైడ్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/ap_ts_budget_economic_survey_master.pdf" download="ap_ts_budget_economic_survey_master.pdf" class="text-xs bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
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
    <div class="bg-gradient-to-r from-slate-950 via-indigo-950 to-blue-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-indigo-900/60 relative overflow-hidden">
      <div class="absolute -right-10 -bottom-10 w-64 h-64 bg-emerald-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          APPSC & TSPSC స్పెషల్ ఎకానమీ ఎడిషన్ 2026
        </span>
        <span class="text-xs text-slate-300 font-medium">అధికారిక బడ్జెట్ ప్రసంగాలు & సోషియో-ఎకనామిక్ సర్వే నివేదికల ఆధారంగా</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">ఆంధ్రప్రదేశ్ & తెలంగాణ బడ్జెట్, ఎకనామిక్ సర్వే & సంక్షేమ పథకాలు</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        GSDP వృద్ధి రేట్లు, రంగాల వారీ విశ్లేషణ, తలసరి ఆదాయం, రెవెన్యూ & ద్రవ్య లోటు, ఆంధ్రప్రదేశ్ సూపర్ సిక్స్ పథకాలు, తెలంగాణ ఆరు గ్యారెంటీలు మరియు కీలక మౌలిక వసతుల ప్రాజెక్టుల సమగ్ర సమాచారం.
      </p>
    </div>

    <!-- Comparative Scorecard -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
      <!-- AP Card -->
      <div class="bg-white border-2 border-emerald-500/30 rounded-2xl p-5 shadow-sm space-y-3">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-black text-emerald-800 text-base">🏛️ ఆంధ్రప్రదేశ్ బడ్జెట్ 2024-25</h3>
          <span class="text-xs bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded font-bold">AP</span>
        </div>
        <div class="space-y-2 text-xs sm:text-sm text-slate-700">
          <div class="flex justify-between"><span>మొత్తం బడ్జెట్ పరిమాణం:</span> <strong class="text-slate-900">{ap['total_outlay']}</strong></div>
          <div class="flex justify-between"><span>రెవెన్యూ వ్యయం:</span> <strong>{ap['revenue_expenditure']}</strong></div>
          <div class="flex justify-between"><span>మూలధన వ్యయం (Capital Outlay):</span> <strong>{ap['capital_expenditure']}</strong></div>
          <div class="flex justify-between"><span>ద్రవ్య లోటు (Fiscal Deficit):</span> <strong class="text-rose-600">{ap['fiscal_deficit']}</strong></div>
          <div class="flex justify-between"><span>తలసరి ఆదాయం (PCI):</span> <strong class="text-emerald-700 font-black">{ap['per_capita_income']['ap_pci']}</strong></div>
        </div>
      </div>

      <!-- TS Card -->
      <div class="bg-white border-2 border-blue-500/30 rounded-2xl p-5 shadow-sm space-y-3">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-black text-blue-800 text-base">🏛️ తెలంగాణ బడ్జెట్ 2024-25</h3>
          <span class="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded font-bold">TS</span>
        </div>
        <div class="space-y-2 text-xs sm:text-sm text-slate-700">
          <div class="flex justify-between"><span>మొత్తం బడ్జెట్ పరిమాణం:</span> <strong class="text-slate-900">{ts['total_outlay']}</strong></div>
          <div class="flex justify-between"><span>రెవెన్యూ వ్యయం:</span> <strong>{ts['revenue_expenditure']}</strong></div>
          <div class="flex justify-between"><span>మూలధన వ్యయం (Capital Outlay):</span> <strong>{ts['capital_expenditure']}</strong></div>
          <div class="flex justify-between"><span>ద్రవ్య లోటు (Fiscal Deficit):</span> <strong class="text-rose-600">{ts['fiscal_deficit']}</strong></div>
          <div class="flex justify-between"><span>తలసరి ఆదాయం (PCI):</span> <strong class="text-blue-700 font-black">{ts['per_capita_income']['ts_pci']}</strong></div>
        </div>
      </div>

      <!-- All-India Comparison Card -->
      <div class="bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 rounded-2xl p-5 shadow-sm space-y-3">
        <div class="flex justify-between items-center border-b border-amber-200 pb-2">
          <h3 class="font-black text-amber-900 text-base">🇮🇳 జాతీయ సగటు పోలిక (Comparison)</h3>
          <span class="text-xs bg-amber-200 text-amber-900 px-2 py-0.5 rounded font-bold">India</span>
        </div>
        <div class="space-y-2 text-xs sm:text-sm text-slate-800">
          <div class="flex justify-between"><span>భారత తలసరి ఆదాయం (PCI):</span> <strong>{ap['per_capita_income']['all_india_pci']}</strong></div>
          <div class="p-2 bg-white/80 rounded-lg text-[11px] leading-relaxed border border-amber-200">
            <strong>ఏపీ:</strong> {ap['per_capita_income']['ap_lead']}<br>
            <strong>తెలంగాణ:</strong> {ts['per_capita_income']['ts_lead']}
          </div>
          <div class="text-[11px] text-slate-600 pt-1 font-medium">
            * రిజర్వ్ బ్యాంక్ ఆఫ్ ఇండియా (RBI) మరియు NSO అధికారిక డేటా.
          </div>
        </div>
      </div>
    </div>

    <!-- Sectoral Distribution Section -->
    <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-5">
      <h3 class="text-lg font-black text-slate-900 flex items-center gap-2 border-b pb-3">
        <span>📈</span> <span>రాష్ట్ర ఆర్థిక వ్యవస్థలో రంగాల వారీ వాటాలు (Sectoral Growth & Shares)</span>
      </h3>
      
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- AP Sectors -->
        <div class="space-y-3">
          <h4 class="font-extrabold text-emerald-800 text-sm flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500"></span> ఆంధ్రప్రదేశ్ రంగాల వారీ భాగస్వామ్యం
          </h4>
          <div class="space-y-2.5">
            {ap_sec_html}
          </div>
        </div>

        <!-- TS Sectors -->
        <div class="space-y-3">
          <h4 class="font-extrabold text-blue-800 text-sm flex items-center gap-2">
            <span class="w-2.5 h-2.5 rounded-full bg-blue-500"></span> తెలంగాణ రంగాల వారీ భాగస్వామ్యం
          </h4>
          <div class="space-y-2.5">
            {ts_sec_html}
          </div>
        </div>
      </div>
    </section>

    <!-- Welfare Schemes Section (Super Six & Six Guarantees) -->
    <section class="space-y-6">
      <div class="flex justify-between items-center">
        <h3 class="text-lg sm:text-xl font-black text-slate-900 flex items-center gap-2">
          <span>🌾</span> <span>ఫ్లాగ్‌షిప్ సంక్షేమ పథకాలు (AP Super Six vs TS 6 Guarantees)</span>
        </h3>
        <span class="text-xs text-slate-500 font-semibold no-print">పరీక్షలలో వచ్చే ముఖ్య పథకాలు</span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- AP Super Six -->
        <div class="space-y-4">
          <div class="bg-gradient-to-r from-emerald-800 to-teal-800 text-white p-4 rounded-2xl shadow-sm">
            <h4 class="font-black text-base">🌾 ఆంధ్రప్రదేశ్ 'సూపర్ సిక్స్' పథకాలు (2024-29)</h4>
            <p class="text-xs text-emerald-200 mt-0.5">మహిళలు, రైతులు, విద్యార్థులు & యువత సాధికారత</p>
          </div>
          <div class="space-y-3">
            {ap_sch_html}
          </div>
        </div>

        <!-- TS Six Guarantees -->
        <div class="space-y-4">
          <div class="bg-gradient-to-r from-blue-800 to-indigo-800 text-white p-4 rounded-2xl shadow-sm">
            <h4 class="font-black text-base">🏛️ తెలంగాణ 'ఆరు గ్యారెంటీలు' (2024-29)</h4>
            <p class="text-xs text-blue-200 mt-0.5">సామాజిక న్యాయం & ప్రజా పాలన పథకాలు</p>
          </div>
          <div class="space-y-3">
            {ts_sch_html}
          </div>
        </div>
      </div>
    </section>

    <!-- Key Mega Projects & Corridors -->
    <section class="bg-white border border-slate-200 rounded-2xl p-6 shadow-sm space-y-5">
      <h3 class="text-lg font-black text-slate-900 flex items-center gap-2 border-b pb-3">
        <span>🏗️</span> <span>కీలక నీటిపారుదల, రాజధాని & పారిశ్రామిక ప్రాజెక్టులు</span>
      </h3>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {proj_html}
      </div>
    </section>

    <!-- Practice MCQs Section -->
    <section class="space-y-4">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📝</span> <span>బడ్జెట్ & సర్వే ఆధారిత పరీక్షా ప్రశ్నలు (High-Yield Practice MCQs)</span>
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
