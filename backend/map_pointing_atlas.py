# -*- coding: utf-8 -*-
"""
Printable Map Pointing Study Atlas & Cheat-Sheet for APPSC Group 2 & General Studies.
"""

from map_pointing_data import get_all_map_points, get_map_pointing_quiz_questions

def render_map_pointing_atlas_html():
    all_points = get_all_map_points()
    ap_pts = [p for p in all_points if p.get("domain") == "ap"]
    ind_pts = [p for p in all_points if p.get("domain") == "india"]
    wld_pts = [p for p in all_points if p.get("domain") == "world"]
    quizzes = get_map_pointing_quiz_questions()

    cards_ap = ""
    for p in ap_pts:
        pyq_div = f'<div class="text-[11px] bg-rose-50 text-rose-900 p-2 rounded-lg border border-rose-200 font-bold"><b>PYQ:</b> {p["pyq"]}</div>' if p.get("pyq") else ''
        cards_ap += f"""
        <div class="atlas-card bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-2 hover:border-emerald-400 transition">
          <div class="flex justify-between items-start gap-2">
            <h3 class="text-sm sm:text-base font-black text-slate-900">{p['telugu_name']}</h3>
            <span class="bg-emerald-100 text-emerald-900 text-[11px] font-black px-2 py-0.5 rounded-md shrink-0">{p.get('district', 'AP')}</span>
          </div>
          <div class="text-[11px] text-blue-700 font-bold">📂 {p['category']}</div>
          <div class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-white p-2.5 rounded-xl border border-slate-200">{p['key_facts']}</div>
          <div class="text-[11px] bg-amber-50 text-amber-950 p-2 rounded-lg border border-amber-200 font-semibold"><b>🎯 పరీక్షల ప్రాధాన్యత:</b> {p['exam_significance']}</div>
          {pyq_div}
        </div>
        """

    cards_ind = ""
    for p in ind_pts:
        pyq_div = f'<div class="text-[11px] bg-rose-50 text-rose-900 p-2 rounded-lg border border-rose-200 font-bold"><b>PYQ:</b> {p["pyq"]}</div>' if p.get("pyq") else ''
        cards_ind += f"""
        <div class="atlas-card bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-2 hover:border-blue-400 transition">
          <div class="flex justify-between items-start gap-2">
            <h3 class="text-sm sm:text-base font-black text-slate-900">{p['telugu_name']}</h3>
            <span class="bg-blue-100 text-blue-900 text-[11px] font-black px-2 py-0.5 rounded-md shrink-0">{p.get('state', 'భారతదేశం')}</span>
          </div>
          <div class="text-[11px] text-blue-700 font-bold">📂 {p['category']}</div>
          <div class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-white p-2.5 rounded-xl border border-slate-200">{p['key_facts']}</div>
          <div class="text-[11px] bg-amber-50 text-amber-950 p-2 rounded-lg border border-amber-200 font-semibold"><b>🎯 పరీక్షల ప్రాధాన్యత:</b> {p['exam_significance']}</div>
          {pyq_div}
        </div>
        """

    cards_wld = ""
    for p in wld_pts:
        pyq_div = f'<div class="text-[11px] bg-rose-50 text-rose-900 p-2 rounded-lg border border-rose-200 font-bold"><b>PYQ:</b> {p["pyq"]}</div>' if p.get("pyq") else ''
        cards_wld += f"""
        <div class="atlas-card bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-2 hover:border-purple-400 transition">
          <div class="flex justify-between items-start gap-2">
            <h3 class="text-sm sm:text-base font-black text-slate-900">{p['telugu_name']}</h3>
            <span class="bg-purple-100 text-purple-900 text-[11px] font-black px-2 py-0.5 rounded-md shrink-0">{p.get('region', 'ప్రపంచం')}</span>
          </div>
          <div class="text-[11px] text-purple-700 font-bold">📂 {p['category']}</div>
          <div class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-white p-2.5 rounded-xl border border-slate-200">{p['key_facts']}</div>
          <div class="text-[11px] bg-amber-50 text-amber-950 p-2 rounded-lg border border-amber-200 font-semibold"><b>🎯 పరీక్షల ప్రాధాన్యత:</b> {p['exam_significance']}</div>
          {pyq_div}
        </div>
        """

    cards_quiz = ""
    for idx, q in enumerate(quizzes, 1):
        opt_html = ""
        for opt in q['options']:
            is_ans = (opt == q['answer'])
            cls = "bg-emerald-50 text-emerald-900 border-emerald-300 font-bold" if is_ans else "bg-slate-50 border-slate-200 text-slate-700"
            opt_html += f'<div class="p-1.5 border rounded {cls}">• {opt}</div>'

        cards_quiz += f"""
        <div class="atlas-card bg-white border border-slate-200 rounded-2xl p-4 space-y-2 text-xs">
          <div class="flex justify-between items-center font-bold">
            <span class="bg-slate-800 text-white px-2 py-0.5 rounded text-[10px]">ప్రశ్న {idx}</span>
            <span class="text-slate-500 font-bold">📍 {q['location_name'].split('(')[0]}</span>
          </div>
          <p class="font-black text-slate-900 text-sm leading-snug">{q['question']}</p>
          <div class="grid grid-cols-2 gap-1.5 font-medium my-2">
            {opt_html}
          </div>
          <div class="bg-emerald-50 border border-emerald-200 rounded p-2 text-emerald-950 font-semibold leading-relaxed">
            <span class="text-emerald-800 font-bold">✔ సరైన సమాధానం: {q['answer']}</span> — {q['explanation']}
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>మ్యాప్ పాయింటింగ్ స్టడీ అట్లాస్ & క్విక్ రివిజన్ గైడ్ | APPSC గ్రూప్-2 & GS</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700;900&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', 'Outfit', sans-serif;
      color: #0f172a;
      background: #f8fafc;
      line-height: 1.6;
    }}
    @media print {{
      *, *::before, *::after {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }}
      body {{ background: #fff !important; font-size: 10pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
      .atlas-card {{ break-inside: avoid; page-break-inside: avoid; }}
    }}
  </style>
</head>
<body class="p-3 sm:p-6">

  <!-- Top Action Bar -->
  <div class="no-print max-w-6xl mx-auto mb-5 flex flex-wrap justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-slate-200 gap-3">
    <div class="flex items-center gap-3">
      <a href="/" class="text-xs sm:text-sm font-bold bg-slate-100 hover:bg-slate-200 text-slate-700 px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
        <span>← డ్యాష్‌బోర్డ్‌కు వెళ్ళు</span>
      </a>
      <span class="text-xs text-slate-400">|</span>
      <h1 class="text-sm sm:text-base font-black text-slate-900 flex items-center gap-2">
        <span>🗺️</span> పోటీ పరీక్షల స్మార్ట్ మ్యాప్ పాయింటింగ్ అట్లాస్
      </h1>
    </div>
    <div class="flex items-center gap-2">
      <button onclick="window.print()" class="bg-blue-600 hover:bg-blue-700 text-white font-black text-xs sm:text-sm px-4 py-2 rounded-xl shadow transition flex items-center gap-1.5">
        <span>🖨️ PDF గా సేవ్ / ప్రింట్</span>
      </button>
    </div>
  </div>

  <div class="max-w-6xl mx-auto bg-white rounded-3xl shadow-xl border border-slate-300 p-6 sm:p-10 space-y-10">

    <!-- ATLAS MASTHEAD -->
    <header class="border-b-4 border-slate-900 pb-6 text-center">
      <div class="inline-flex items-center gap-2 bg-gradient-to-r from-teal-600 to-emerald-700 text-white text-xs font-black px-3.5 py-1 rounded-full uppercase tracking-wider mb-2">
        <span>🎯 APPSC గ్రూప్-2 • గ్రూప్-1 • TSPSC • UPSC స్పెషల్</span>
      </div>
      <h1 class="text-2xl sm:text-4xl font-black text-slate-950 tracking-tight mb-2">
        భౌగోళిక మ్యాప్ పాయింటింగ్ అట్లాస్ & రివిజన్ మాన్యువల్
      </h1>
      <p class="text-sm sm:text-base font-bold text-slate-600 max-w-3xl mx-auto">
        ఆంధ్రప్రదేశ్, భారతదేశం మరియు ప్రపంచ సమకాలీన వ్యూహాత్మక ప్రాంతాలు, పోర్టులు, ప్రాజెక్టులు, కనుమలు, జలసంధుల సమగ్ర సమాచారం
      </p>

      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-6 bg-slate-900 text-white p-3.5 rounded-2xl text-xs font-bold">
        <div>🚩 ఆంధ్రప్రదేశ్ అంశాలు: <span class="text-emerald-400 font-black">{len(ap_pts)}</span></div>
        <div>🇮🇳 భారతదేశం అంశాలు: <span class="text-amber-400 font-black">{len(ind_pts)}</span></div>
        <div>🌐 ప్రపంచ వ్యూహాత్మక పాయింట్లు: <span class="text-sky-400 font-black">{len(wld_pts)}</span></div>
        <div>📝 క్విజ్ ప్రాక్టీస్ ప్రశ్నలు: <span class="text-rose-400 font-black">{len(quizzes)}</span></div>
      </div>
    </header>

    <!-- PART 1: AP -->
    <section class="space-y-4">
      <div class="bg-emerald-50 border-l-4 border-emerald-600 px-4 py-2.5 rounded-r-xl flex justify-between items-center">
        <div>
          <h2 class="text-lg sm:text-xl font-black text-emerald-950 flex items-center gap-2">
            <span>🚩</span> భాగం 1: ఆంధ్రప్రదేశ్ మ్యాప్ పాయింటింగ్ (AP Geography, Ports & Projects)
          </h2>
          <p class="text-xs text-emerald-800 font-medium">పోర్టులు, నదులు, డ్యామ్‌లు, కొండలు, సరస్సులు మరియు ఖనిజ క్లస్టర్లు</p>
        </div>
        <span class="bg-emerald-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">{len(ap_pts)} అంశాలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_ap}
      </div>
    </section>

    <!-- PART 2: INDIA -->
    <section class="space-y-4 pt-4 border-t-2 border-slate-200">
      <div class="bg-blue-50 border-l-4 border-blue-600 px-4 py-2.5 rounded-r-xl flex justify-between items-center">
        <div>
          <h2 class="text-lg sm:text-xl font-black text-blue-950 flex items-center gap-2">
            <span>🇮🇳</span> భాగం 2: భారతదేశం మ్యాప్ పాయింటింగ్ (India Geography & Landmarks)
          </h2>
          <p class="text-xs text-blue-800 font-medium">హిమాలయ కనుమలు, చానల్స్, అణు విద్యుత్ & అంతరిక్ష కేంద్రాలు, శిఖరాలు</p>
        </div>
        <span class="bg-blue-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">{len(ind_pts)} అంశాలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_ind}
      </div>
    </section>

    <!-- PART 3: WORLD -->
    <section class="space-y-4 pt-4 border-t-2 border-slate-200">
      <div class="bg-purple-50 border-l-4 border-purple-600 px-4 py-2.5 rounded-r-xl flex justify-between items-center">
        <div>
          <h2 class="text-lg sm:text-xl font-black text-purple-950 flex items-center gap-2">
            <span>🌐</span> భాగం 3: ప్రపంచ వ్యూహాత్మక జలసంధులు & చోక్‌పాయింట్స్ (World Geopolitics)
          </h2>
          <p class="text-xs text-purple-800 font-medium">హార్ముజ్, బాబ్-ఎల్-మందేబ్, మలక్కా, సూయజ్, దక్షిణ చైనా సముద్రం</p>
        </div>
        <span class="bg-purple-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">{len(wld_pts)} అంశాలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_wld}
      </div>
    </section>

    <!-- PART 4: QUIZ -->
    <section class="space-y-4 pt-4 border-t-2 border-slate-200 page-break">
      <div class="bg-slate-900 text-white px-4 py-3 rounded-xl flex justify-between items-center">
        <div>
          <h2 class="text-lg sm:text-xl font-black flex items-center gap-2">
            <span>📝</span> భాగం 4: గత మరియు ప్రాక్టీస్ మ్యాప్ పాయింటింగ్ ప్రశ్నలు (MCQs & Solutions)
          </h2>
          <p class="text-xs text-slate-300">పూర్తి సమాధానాలు మరియు తెలుగు విశ్లేషణలతో</p>
        </div>
        <span class="bg-amber-500 text-slate-950 text-xs font-black px-2.5 py-1 rounded-lg">{len(quizzes)} ప్రశ్నలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_quiz}
      </div>
    </section>

    <!-- Footer -->
    <footer class="text-center pt-6 border-t border-slate-200 text-xs text-slate-500">
      <p class="font-bold text-slate-700">లక్ష్య డైలీ కరెంట్ అఫైర్స్ & మ్యాప్ పాయింటింగ్ అట్లాస్ • APPSC & TSPSC స్పెషల్</p>
      <p class="mt-1">అభ్యర్థుల విజయమే లక్ష్యంగా రూపొందించబడింది • 2026</p>
    </footer>

  </div>

</body>
</html>
"""
    return html
