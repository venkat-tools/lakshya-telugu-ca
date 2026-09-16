# -*- coding: utf-8 -*-
"""
HTML renderer for Daily Telugu E-Papers & PDF Directory Hub.
Serves a clean, responsive portal for all Telugu newspapers and daily PDFs.
"""

from datetime import datetime, timezone, timedelta
from pdf_generator import OFFICIAL_TELUGU_EPAPERS
from db import get_available_dates

IST = timezone(timedelta(hours=5, minutes=30))

def render_epapers_directory_html():
    dates = get_available_dates()
    today_date = dates[0] if dates else datetime.now(IST).strftime("%Y-%m-%d")
    
    date_obj = datetime.strptime(today_date, "%Y-%m-%d") if "-" in today_date else datetime.now(IST)
    days_telugu = ["సోమవారం", "మంగళవారం", "బుధవారం", "గురువారం", "శుక్రవారం", "శనివారం", "ఆదివారం"]
    day_name = days_telugu[date_obj.weekday()]

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>డైలీ తెలుగు ఈ-న్యూస్‌పేపర్స్ & PDF డైరెక్టరీ - లక్ష్య కరెంట్ అఫైర్స్</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700;900&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', 'Outfit', sans-serif;
      background-color: #f8fafc;
      color: #0f172a;
    }}
    .glow-hover:hover {{
      box-shadow: 0 10px 25px -5px rgba(59, 130, 246, 0.2);
    }}
  </style>
</head>
<body class="min-h-screen bg-slate-50 text-slate-900 flex flex-col justify-between">

  <!-- TOP BAR -->
  <header class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white sticky top-0 z-50 shadow-md">
    <div class="max-w-6xl mx-auto px-4 py-3.5 flex flex-wrap items-center justify-between gap-3">
      <div class="flex items-center gap-3">
        <a href="/" class="flex items-center gap-2 hover:opacity-90 transition">
          <span class="text-2xl">📰</span>
          <div>
            <h1 class="font-black text-lg sm:text-xl tracking-tight leading-none">లక్ష్య ఈ-పేపర్ హబ్</h1>
            <span class="text-[11px] text-blue-200">డైలీ తెలుగు దినపత్రికలు & కాంపిటీటివ్ PDFలు</span>
          </div>
        </a>
      </div>

      <div class="flex items-center gap-2 flex-wrap text-xs font-bold">
        <a href="/" class="bg-white/10 hover:bg-white/20 text-white px-3 py-1.5 rounded-lg border border-white/20 transition">
          🏠 హోమ్
        </a>
        <a href="/appsc_syllabus" class="bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 px-3 py-1.5 rounded-lg border border-amber-400/30 transition">
          📚 APPSC సిలబస్
        </a>
        <a href="/epaper?date={today_date}" class="bg-blue-600 hover:bg-blue-500 text-white px-3.5 py-1.5 rounded-lg font-black shadow transition flex items-center gap-1.5">
          <span>📖</span> ఆన్‌లైన్ పేపర్
        </a>
        <a href="/api/epaper/pdf?date={today_date}" target="_blank" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3.5 py-1.5 rounded-lg font-black shadow transition flex items-center gap-1.5">
          <span>📥</span> PDF డౌన్‌లోడ్
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-6xl mx-auto px-4 py-8 flex-1 w-full">

    <!-- HERO SECTION -->
    <div class="bg-gradient-to-br from-indigo-900 via-blue-900 to-slate-900 rounded-3xl p-6 sm:p-10 text-white shadow-xl mb-10 relative overflow-hidden">
      <div class="absolute -right-10 -bottom-10 opacity-10 text-[180px] select-none pointer-events-none">📰</div>
      <div class="relative z-10 max-w-3xl">
        <div class="inline-flex items-center gap-2 bg-blue-500/30 border border-blue-400/40 px-3 py-1 rounded-full text-xs font-bold text-blue-200 mb-3">
          <span>📅</span> {today_date} ({day_name}) ఎడిషన్ సిద్ధంగా ఉంది
        </div>
        <h2 class="text-2xl sm:text-4xl font-black tracking-tight mb-3 leading-snug">
          డైలీ తెలుగు ఈ-న్యూస్‌పేపర్స్ & కాంపిటీటివ్ ఎగ్జామ్స్ PDF డైరెక్టరీ
        </h2>
        <p class="text-slate-200 text-sm sm:text-base leading-relaxed mb-6 font-medium">
          APPSC, TSPSC, UPSC, SSC మరియు బ్యాంకింగ్ అభ్యర్థుల కోసం ఈనాడు, సాక్షి, నమస్తే తెలంగాణ తదితర ప్రముఖ దినపత్రికల నుండి సేకరించిన పరీక్షల విశ్లేషణ, ఒక వరుస ముఖ్యాంశాలు మరియు అధికారిక PDF ఈ-పేపర్స్ ఒకేచోట!
        </p>

        <!-- ACTION BUTTONS -->
        <div class="flex flex-wrap gap-3">
          <a href="/api/epaper/pdf?date={today_date}" target="_blank" class="bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black px-6 py-3 rounded-xl shadow-lg hover:shadow-emerald-500/25 transition flex items-center gap-2 text-sm sm:text-base">
            <span class="text-lg">📥</span> నేటి లక్ష్య ఈ-పేపర్ PDF డౌన్‌లోడ్ (4.2 MB)
          </a>
          <a href="/epaper?date={today_date}" class="bg-white/15 hover:bg-white/25 text-white font-bold px-5 py-3 rounded-xl border border-white/30 backdrop-blur transition flex items-center gap-2 text-sm sm:text-base">
            <span>📖</span> బ్రౌజర్‌లో చదవండి (HD మోడ్)
          </a>
          <a href="https://t.me/venkat_telugu_ca_bot" target="_blank" class="bg-sky-500/30 hover:bg-sky-500/40 text-sky-200 font-bold px-4 py-3 rounded-xl border border-sky-400/40 transition flex items-center gap-2 text-sm">
            <span>✈️</span> టెలిగ్రామ్ బోట్
          </a>
        </div>
      </div>
    </div>

    <!-- FEATURED CARD: TODAY'S LAKSHYA COMPILED EPAPER -->
    <section class="mb-10">
      <div class="bg-white border-2 border-blue-500/30 rounded-2xl p-6 sm:p-8 shadow-sm glow-hover transition">
        <div class="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div class="flex items-center gap-2 mb-2">
              <span class="bg-blue-600 text-white text-[11px] font-black px-2.5 py-0.5 rounded-full uppercase">అధికారిక ప్రత్యేక సంచిక</span>
              <span class="text-slate-500 text-xs font-semibold">తేదీ: {today_date}</span>
            </div>
            <h3 class="text-xl sm:text-2xl font-black text-slate-900 mb-2">
              🎯 లక్ష్య డైలీ కరెంట్ అఫైర్స్ కాంపిటీటివ్ ఈ-పేపర్ (Full PDF)
            </h3>
            <p class="text-slate-600 text-xs sm:text-sm leading-relaxed mb-4">
              ఈనాడు, సాక్షి, నమస్తే తెలంగాణ దినపత్రికల నుండి సేకరించిన <b>56+ సమగ్ర వార్తా విశ్లేషణలు</b>, క్విక్ రివిజన్ <b>ఒక వరుస ముఖ్యాంశాలు</b> మరియు వివరణలతో కూడిన <b>5 ప్రాక్టీస్ క్విజ్ ప్రశ్నలు</b> కలిగిన పూర్తి వార్తాపత్రిక పి.డి.ఎఫ్.
            </p>
            <div class="flex flex-wrap items-center gap-4 text-xs font-bold text-slate-700">
              <span class="flex items-center gap-1 text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-md">✔ 56 ఆర్టికల్స్ విశ్లేషణ</span>
              <span class="flex items-center gap-1 text-blue-700 bg-blue-50 px-2.5 py-1 rounded-md">✔ Quick Revision One-Liners</span>
              <span class="flex items-center gap-1 text-purple-700 bg-purple-50 px-2.5 py-1 rounded-md">✔ 5 MCQs & Explanations</span>
              <span class="flex items-center gap-1 text-amber-700 bg-amber-50 px-2.5 py-1 rounded-md">✔ APPSC / TSPSC స్పెషల్</span>
            </div>
          </div>

          <div class="flex md:flex-col gap-2 shrink-0">
            <a href="/api/epaper/pdf?date={today_date}" target="_blank" class="flex-1 md:flex-none text-center bg-blue-600 hover:bg-blue-700 text-white font-black px-5 py-3 rounded-xl shadow transition text-sm flex items-center justify-center gap-2">
              <span>📥</span> PDF డౌన్‌లోడ్
            </a>
            <a href="/epaper?date={today_date}" class="flex-1 md:flex-none text-center bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-5 py-3 rounded-xl transition text-sm flex items-center justify-center gap-2">
              <span>👀</span> పేపర్ వ్యూ
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- OFFICIAL TELUGU NEWSPAPERS GRID -->
    <section class="mb-12">
      <div class="flex items-center justify-between mb-6 flex-wrap gap-2">
        <div>
          <h3 class="text-xl sm:text-2xl font-black text-slate-900 flex items-center gap-2">
            <span>🗞️</span> ప్రముఖ తెలుగు దినపత్రికల అధికారిక ఈ-పేపర్స్
          </h3>
          <p class="text-xs sm:text-sm text-slate-500">
            మీరు నేరుగా క్రింది లింక్‌ల ద్వారా జిల్లాల వారీగా అధికారిక PDF ఈ-పేపర్స్ ఉచితంగా చదువుకోవచ్చు:
          </p>
        </div>
        <span class="text-xs font-black bg-blue-50 text-blue-800 px-3 py-1 rounded-full border border-blue-200">
          అధికారిక పోర్టల్స్
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
"""

    for ep in OFFICIAL_TELUGU_EPAPERS:
        html += f"""
        <div class="bg-white border border-slate-200 hover:border-blue-500 rounded-2xl p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between group">
          <div>
            <div class="flex items-center justify-between mb-3">
              <span class="text-2xl">{ep.get('icon', '📰')}</span>
              <span class="text-[10px] font-black uppercase tracking-wider bg-slate-100 group-hover:bg-blue-50 text-slate-600 group-hover:text-blue-700 px-2 py-0.5 rounded transition">
                {ep.get('tag', 'Daily')}
              </span>
            </div>
            <h4 class="font-black text-base sm:text-lg text-slate-900 group-hover:text-blue-600 transition mb-1">
              {ep['name']}
            </h4>
            <p class="text-xs text-slate-500 leading-relaxed mb-4">
              {ep['description']}
            </p>
          </div>

          <div class="pt-3 border-t border-slate-100 flex items-center justify-between">
            <span class="text-[11px] font-semibold text-slate-400">డైలీ ఎడిషన్</span>
            <a href="{ep['url']}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 bg-blue-50 hover:bg-blue-600 text-blue-700 hover:text-white px-3.5 py-1.5 rounded-lg text-xs font-bold transition">
              <span>ఓపెన్ చేయండి</span>
              <span>↗</span>
            </a>
          </div>
        </div>
        """

    html += f"""
      </div>
    </section>

    <!-- TELEGRAM BOT COMMANDS GUIDE -->
    <section class="bg-gradient-to-r from-sky-50 to-indigo-50 border border-sky-200 rounded-2xl p-6 sm:p-8">
      <div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
        <div class="max-w-2xl">
          <div class="inline-flex items-center gap-1.5 bg-sky-100 text-sky-800 text-xs font-black px-2.5 py-0.5 rounded-full mb-2">
            <span>🤖</span> టెలిగ్రామ్ బోట్ సేవలు (24/7 ఉచితం)
          </div>
          <h3 class="text-lg sm:text-xl font-black text-slate-900 mb-2">
            టెలిగ్రామ్‌లో డైలీ ఈ-పేపర్స్ & క్విజ్‌లు పొందండి
          </h3>
          <p class="text-xs sm:text-sm text-slate-600 leading-relaxed mb-3">
            మా టెలిగ్రామ్ బోట్‌లో క్రింది కమాండ్స్ టైప్ చేయడం ద్వారా నేరుగా మీ మొబైల్‌కే ఈ-పేపర్ PDFలు మరియు క్విజ్ పోల్స్ అందుతాయి:
          </p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-semibold text-slate-800">
            <div class="bg-white/80 p-2 rounded-lg border border-sky-100">👉 <b class="text-sky-700">/epaper</b> లేదా <b class="text-sky-700">/pdf</b> - నేటి పూర్తి ఈ-పేపర్ PDF</div>
            <div class="bg-white/80 p-2 rounded-lg border border-sky-100">👉 <b class="text-sky-700">/papers</b> - అన్ని ప్రముఖ పత్రికల ఈ-పేపర్ లింక్స్</div>
            <div class="bg-white/80 p-2 rounded-lg border border-sky-100">👉 <b class="text-sky-700">/syllabus</b> - APPSC గ్రూప్స్ మాస్టర్ సిలబస్ & 6 బుక్స్</div>
            <div class="bg-white/80 p-2 rounded-lg border border-sky-100">👉 <b class="text-sky-700">/today</b> - నేటి 56 వార్తా ముఖ్యాంశాలు</div>
          </div>
        </div>

        <div class="shrink-0 w-full md:w-auto text-center">
          <a href="https://t.me/venkat_telugu_ca_bot" target="_blank" class="w-full inline-flex items-center justify-center gap-2 bg-sky-600 hover:bg-sky-700 text-white font-black px-6 py-3 rounded-xl shadow-md transition text-sm">
            <span>✈️</span> బోట్‌ను స్టార్ట్ చేయండి
          </a>
          <span class="block text-[11px] text-slate-500 mt-1.5">@venkat_telugu_ca_bot</span>
        </div>
      </div>
    </section>

  </main>

  <!-- FOOTER -->
  <footer class="bg-white border-t border-slate-200 mt-12 py-6 text-center text-xs text-slate-500">
    <div class="max-w-6xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
      <p class="font-bold text-slate-700">
        © 2026 లక్ష్య కరెంట్ అఫైర్స్ • APPSC • TSPSC • UPSC విజేతల ప్రత్యేకం
      </p>
      <div class="flex items-center gap-4 font-semibold">
        <a href="/" class="hover:text-blue-600">హోమ్</a>
        <a href="/appsc_syllabus" class="hover:text-blue-600">APPSC సిలబస్</a>
        <a href="/epaper" class="hover:text-blue-600">ఈ-పేపర్</a>
        <a href="/omr_group2" class="hover:text-blue-600">గ్రాండ్ టెస్ట్</a>
      </div>
    </div>
  </footer>

</body>
</html>
"""
    return html
