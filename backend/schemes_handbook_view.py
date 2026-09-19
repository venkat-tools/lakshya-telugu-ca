# -*- coding: utf-8 -*-
"""
Schemes Master Handbook Web Reader View.
Route: /schemes_handbook
Presents AP Super Six Schemes, TS 6 Guarantees, Budgets, and Practice MCQs.
Provides direct PDF download.
"""

from compile_schemes_handbook_pdf import AP_SCHEMES, TS_SCHEMES, SCHEME_MCQS

def render_schemes_handbook_html():
    ap_cards = ""
    for idx, sc in enumerate(AP_SCHEMES, 1):
        bullets = "".join([f'<li class="mb-1.5 text-xs text-slate-700 leading-relaxed">• {p}</li>' for p in sc["details"]])
        ap_cards += f"""
        <div class="bg-white rounded-2xl p-5 border border-blue-200 shadow-2xs hover:shadow-md transition">
          <div class="flex flex-wrap justify-between items-baseline gap-2 mb-2">
            <h3 class="text-base font-black text-blue-950">#{idx}. {sc['name']}</h3>
            <span class="text-xs font-bold text-blue-700 bg-blue-100 px-2.5 py-0.5 rounded-full">{sc['dept']}</span>
          </div>
          <div class="flex flex-wrap gap-4 text-xs font-semibold text-slate-600 bg-blue-50/50 p-2.5 rounded-xl mb-3 border border-blue-100">
            <div><b class="text-blue-900">💰 బడ్జెట్:</b> {sc['budget']}</div>
            <div><b class="text-blue-900">👥 లబ్ధిదారులు:</b> {sc['beneficiaries']}</div>
          </div>
          <ul class="space-y-1 list-none">
            {bullets}
          </ul>
        </div>
        """

    ts_cards = ""
    for idx, sc in enumerate(TS_SCHEMES, 1):
        bullets = "".join([f'<li class="mb-1.5 text-xs text-slate-700 leading-relaxed">• {p}</li>' for p in sc["details"]])
        ts_cards += f"""
        <div class="bg-white rounded-2xl p-5 border border-amber-200 shadow-2xs hover:shadow-md transition">
          <div class="flex flex-wrap justify-between items-baseline gap-2 mb-2">
            <h3 class="text-base font-black text-amber-950">#{idx}. {sc['name']}</h3>
            <span class="text-xs font-bold text-amber-800 bg-amber-100 px-2.5 py-0.5 rounded-full">{sc['dept']}</span>
          </div>
          <div class="flex flex-wrap gap-4 text-xs font-semibold text-slate-600 bg-amber-50/50 p-2.5 rounded-xl mb-3 border border-amber-100">
            <div><b class="text-amber-900">💰 బడ్జెట్:</b> {sc['budget']}</div>
            <div><b class="text-amber-900">👥 లబ్ధిదారులు:</b> {sc['beneficiaries']}</div>
          </div>
          <ul class="space-y-1 list-none">
            {bullets}
          </ul>
        </div>
        """

    mcq_cards = ""
    for idx, m in enumerate(SCHEME_MCQS, 1):
        opts = "".join([f'<div class="p-2 rounded-lg bg-slate-100 border border-slate-200 text-xs font-medium text-slate-700">{o}</div>' for o in m["opts"]])
        mcq_cards += f"""
        <div class="bg-white rounded-2xl p-5 border border-slate-200 shadow-2xs">
          <div class="text-xs font-black text-emerald-700 mb-1">ప్రశ్న {idx}</div>
          <h4 class="text-sm font-bold text-slate-900 mb-3">{m['q']}</h4>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3">
            {opts}
          </div>
          <div class="bg-emerald-50 border border-emerald-200 p-3 rounded-xl text-xs text-slate-700">
            <div class="font-black text-emerald-800 mb-1">✓ సరైన సమాధానం: {m['ans']}</div>
            <div><b>వివరణ:</b> {m['exp']}</div>
          </div>
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ఆంధ్రప్రదేశ్ & తెలంగాణ సంక్షేమ పథకాలు 2026 మాస్టర్ హ్యాండ్‌బుక్</title>
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body {{
      font-family: 'Nirmala UI', 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: #f8fafc;
      color: #0f172a;
    }}
  </style>
</head>
<body class="min-h-screen bg-slate-50 flex flex-col">

  <!-- Header -->
  <header class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white shadow-md sticky top-0 z-30">
    <div class="max-w-7xl mx-auto px-4 py-3.5 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center space-x-3">
        <a href="/" class="p-1.5 bg-blue-800/80 hover:bg-blue-700 rounded-lg text-white transition" title="హోమ్‌కు వెళ్లండి">
          <i data-lucide="arrow-left" class="w-5 h-5"></i>
        </a>
        <div>
          <h1 class="text-base sm:text-lg font-black tracking-tight flex items-center gap-2">
            🏛️ AP & TS సంక్షేమ పథకాలు 2026 మాస్టర్ గైడ్
          </h1>
          <p class="text-xs text-slate-300">సూపర్ సిక్స్ • ఆరు గ్యారెంటీలు • పారిశ్రామిక విధానాలు • మోడల్ బిట్స్</p>
        </div>
      </div>

      <div class="flex items-center space-x-2">
        <a href="/api/schemes/download" download class="bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500 text-slate-950 font-black text-xs sm:text-sm px-4 py-2 rounded-xl transition shadow-md flex items-center space-x-1.5">
          <i data-lucide="download" class="w-4 h-4"></i>
          <span>మాస్టర్ PDF డౌన్‌లోడ్</span>
        </a>
        <a href="/daily_live_test" class="bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm px-3.5 py-2 rounded-xl transition flex items-center space-x-1">
          <i data-lucide="play" class="w-4 h-4"></i>
          <span>లైవ్ టెస్ట్</span>
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Banner -->
  <div class="bg-gradient-to-br from-blue-950 via-slate-900 to-indigo-950 text-white py-8 px-4 border-b border-amber-500/30">
    <div class="max-w-5xl mx-auto text-center">
      <span class="inline-block bg-amber-400 text-slate-950 text-2xs font-black px-3 py-1 rounded-full uppercase tracking-wider mb-2">
        APPSC & TSPSC స్పెషల్ రిఫరెన్స్
      </span>
      <h2 class="text-2xl sm:text-3xl font-black mb-2">
        ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రభుత్వ సంక్షేమ పథకాలు & విధానాలు
      </h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-2xl mx-auto leading-relaxed">
        గ్రూప్-1, గ్రూప్-2 (పేపర్-2 AP స్కీమ్స్), గ్రూప్-3 మరియు పోలీస్ పరీక్షలకు అత్యంత కీలకమైన అధికారిక సమాచారం, తాజా జీవోలు మరియు బడ్జెట్ కేటాయింపులు.
      </p>
    </div>
  </div>

  <!-- Content Container -->
  <main class="max-w-6xl w-full mx-auto p-4 sm:p-6 flex-1 space-y-10">

    <!-- Section 1: AP Super Six -->
    <section>
      <div class="flex items-center space-x-2 mb-4 pb-2 border-b-2 border-blue-600">
        <span class="text-2xl">🏛️</span>
        <div>
          <h2 class="text-lg font-black text-blue-950">విభాగం 1: ఆంధ్రప్రదేశ్ సూపర్ సిక్స్ & నూతన సంక్షేమ పథకాలు</h2>
          <p class="text-xs text-slate-500">AP Super Six & Flagship Welfare Initiatives 2024-2026</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {ap_cards}
      </div>
    </section>

    <!-- Section 2: TS 6 Guarantees -->
    <section>
      <div class="flex items-center space-x-2 mb-4 pb-2 border-b-2 border-amber-600">
        <span class="text-2xl">🌾</span>
        <div>
          <h2 class="text-lg font-black text-amber-950">విభాగం 2: తెలంగాణ ఆరు గ్యారెంటీలు & ప్రజా పాలన పథకాలు</h2>
          <p class="text-xs text-slate-500">TS 6 Guarantees, Rythu Bharosa & Praja Palana</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {ts_cards}
      </div>
    </section>

    <!-- Section 3: Model MCQs -->
    <section>
      <div class="flex items-center space-x-2 mb-4 pb-2 border-b-2 border-emerald-600">
        <span class="text-2xl">📝</span>
        <div>
          <h2 class="text-lg font-black text-emerald-950">విభాగం 3: పోటీ పరీక్షల ప్రాక్టీస్ ప్రశ్నలు & వివరణలు</h2>
          <p class="text-xs text-slate-500">Standard Model MCQs on Schemes for APPSC / TSPSC</p>
        </div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {mcq_cards}
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-slate-900 text-white text-center py-6 text-xs text-slate-400 mt-12 border-t border-slate-800">
    <div class="max-w-4xl mx-auto px-4 space-y-2">
      <p>© 2026 లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రిపరేషన్ పోర్టల్ | 100% ఉచిత ఎగ్జామ్ స్టడీ మెటీరియల్స్</p>
      <div class="flex justify-center space-x-4 text-xs font-bold text-slate-300">
        <a href="/" class="hover:text-amber-400 transition">హోమ్</a>
        <span>•</span>
        <a href="/daily_live_test" class="hover:text-amber-400 transition">లైవ్ CBT టెస్ట్</a>
        <span>•</span>
        <a href="/api/schemes/download" class="hover:text-amber-400 transition">స్కీమ్స్ PDF</a>
        <span>•</span>
        <a href="https://t.me/venkat_telugu_ca_bot" target="_blank" class="hover:text-amber-400 transition">టెలిగ్రామ్ ఛానల్</a>
      </div>
    </div>
  </footer>

  <script>
    lucide.createIcons();
  </script>
</body>
</html>"""
