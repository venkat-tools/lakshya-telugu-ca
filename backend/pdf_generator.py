# -*- coding: utf-8 -*-
"""
Telugu Daily E-Paper & PDF Generator for Exam Aspirants.
Compiles daily news from Eenadu, Sakshi, Namasthe Telangana, etc.
into an exam-focused, newspaper-style Daily E-Paper PDF.
"""

import os
import subprocess
from datetime import datetime
from db import get_articles, get_quiz_by_date, get_one_liners_by_date, get_available_dates

PDF_CACHE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "pdf_cache"))
os.makedirs(PDF_CACHE_DIR, exist_ok=True)

def get_browser_executable():
    import shutil
    candidates = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser",
        "/usr/lib/chromium/chromium",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    for name in ["msedge", "google-chrome", "google-chrome-stable", "chromium", "chromium-browser"]:
        found = shutil.which(name)
        if found:
            return found
    return None

EDGE_EXE = get_browser_executable() or r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

OFFICIAL_TELUGU_EPAPERS = [
    {
        "name": "ఈనాడు (Eenadu E-Paper)",
        "icon": "📰",
        "url": "https://epaper.eenadu.net",
        "description": "ఆంధ్రప్రదేశ్ & తెలంగాణ అన్ని జిల్లాల ఎడిషన్లు",
        "tag": "AP & TS All Districts"
    },
    {
        "name": "సాక్షి (Sakshi E-Paper)",
        "icon": "📰",
        "url": "https://epaper.sakshi.com",
        "description": "మెయిన్ ఎడిషన్, జిల్లా టాబ్లాయిడ్లు మరియు ఫన్డే మ్యాగజైన్",
        "tag": "Main & District Editions"
    },
    {
        "name": "ఆంధ్రజ్యోతి (Andhra Jyothy E-Paper)",
        "icon": "📰",
        "url": "https://epaper.andhrajyothy.com",
        "description": "సమగ్ర వార్తలు మరియు సంపాదకీయం (Editorial)",
        "tag": "Daily E-Paper"
    },
    {
        "name": "నమస్తే తెలంగాణ (Namasthe Telangana)",
        "icon": "📰",
        "url": "https://epaper.ntnews.com",
        "description": "తెలంగాణ ప్రాంతీయ వార్తలు & బతుకమ్మ స్పెషల్",
        "tag": "TS Special Edition"
    },
    {
        "name": "ప్రజాశక్తి (Prajasakti E-Paper)",
        "icon": "📰",
        "url": "https://epaper.prajasakti.com",
        "description": "ప్రజా సమస్యలు, సామాజిక-ఆర్థిక విశ్లేషణలు",
        "tag": "Social & Economy Focus"
    },
    {
        "name": "వార్త (Vaartha E-Paper)",
        "icon": "📰",
        "url": "https://epaper.vaartha.com",
        "description": "జాతీయ, అంతర్జాతీయ మరియు రాష్ట్ర ముఖ్యాంశాలు",
        "tag": "Daily Telugu Newspaper"
    },
    {
        "name": "సూర్య (Suryaa E-Paper)",
        "icon": "📰",
        "url": "https://epaper.suryaa.com",
        "description": "ఆంధ్రప్రదేశ్ & తెలంగాణ దినపత్రిక",
        "tag": "Daily Edition"
    },
    {
        "name": "మన తెలంగాణ (Mana Telangana)",
        "icon": "📰",
        "url": "https://epaper.manatelangana.news",
        "description": "తెలంగాణ సమగ్ర వార్తలు & జిల్లా ఎడిషన్లు",
        "tag": "TS News"
    },
    {
        "name": "ది హిందూ (The Hindu E-Paper)",
        "icon": "🗞️",
        "url": "https://epaper.thehindu.com",
        "description": "UPSC & సివిల్ సర్వీసెస్ ఎగ్జామ్స్ స్టాండర్డ్ నేషనల్ న్యూస్",
        "tag": "UPSC & Civil Services"
    },
    {
        "name": "ఇండియన్ ఎక్స్‌ప్రెస్ (The Indian Express)",
        "icon": "🗞️",
        "url": "https://epaper.indianexpress.com",
        "description": "ఎక్స్‌ప్లైన్డ్ (Explained) & కాంపిటీటివ్ ఎడిటోరియల్స్",
        "tag": "National & Editorial"
    }
]

CATEGORY_LABELS = {
    "national": "🏛️ జాతీయ అంశాలు (National Affairs)",
    "regional": "🌾 ఆంధ్రప్రదేశ్ & తెలంగాణ (AP & TS Affairs)",
    "economy": "📈 ఆర్థిక రంగం & బ్యాంకింగ్ (Economy & Banking)",
    "science_tech": "🚀 సైన్స్, టెక్నాలజీ & పర్యావరణం (Science & Tech)",
    "sports_awards": "🏆 క్రీడలు & అవార్డులు (Sports & Awards)",
    "appointments": "👤 ప్రముఖ నియామకాలు (Appointments)"
}

def format_notes_html(notes):
    if not notes:
        return ""
    import re
    def repl(m):
        raw_url = m.group(0).rstrip('.,;:!?)>"\'')
        return (
            f'<a href="{raw_url}" target="_blank" rel="noopener noreferrer" '
            f'style="color: #1d4ed8; text-decoration: underline; font-weight: 800; word-break: break-all; cursor: pointer;" '
            f'onclick="window.open(\'{raw_url}\', \'_blank\'); return true;">{raw_url} ↗</a>'
            f'<br/>'
            f'<a href="{raw_url}" target="_blank" rel="noopener noreferrer" '
            f'style="display: inline-block; margin-top: 5px; padding: 4px 10px; background-color: #2563eb; color: #ffffff; border-radius: 6px; font-weight: 800; font-size: 11px; text-decoration: none; cursor: pointer; box-shadow: 0 1px 2px rgba(0,0,0,0.1);" '
            f'onclick="window.open(\'{raw_url}\', \'_blank\'); return true;">🌐 సంబంధిత వెబ్‌సైట్‌లో ఈ వార్తను ఓపెన్ చేయండి (Open Website ↗)</a>'
        )
    return re.sub(r'https?://[^\s<"]+', repl, notes)

def render_epaper_html(date=None):
    """
    Generate complete, beautiful, newspaper-styled HTML layout
    for the Daily Telugu E-Paper edition.
    """
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")

    articles = get_articles(date=date)
    one_liners = get_one_liners_by_date(date=date)
    quizzes = get_quiz_by_date(date=date)

    # Group articles by category
    by_cat = {}
    for a in articles:
        c = a.get("category", "national")
        if c not in by_cat:
            by_cat[c] = []
        by_cat[c].append(a)

    date_obj = datetime.strptime(date, "%Y-%m-%d") if "-" in date else datetime.now()
    days_telugu = ["సోమవారం", "మంగళవారం", "బుధవారం", "గురువారం", "శుక్రవారం", "శనివారం", "ఆదివారం"]
    day_name = days_telugu[date_obj.weekday()]

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>లక్ష్య డైలీ తెలుగు ఈ-పేపర్ - {date}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700;900&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', 'Outfit', sans-serif;
      color: #0f172a;
      background: #f1f5f9;
      line-height: 1.6;
    }}
    .newspaper-columns {{
      column-count: 2;
      column-gap: 2rem;
    }}
    a {{
      word-break: break-word;
      overflow-wrap: anywhere;
    }}
    @media (max-width: 768px) {{
      .newspaper-columns {{
        column-count: 1;
      }}
    }}
    .article-item {{
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    @media print {{
      *, *::before, *::after {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }}
      body {{ background: #fff !important; font-size: 10.5pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
      .newspaper-container {{ max-width: 100% !important; padding: 0 !important; margin: 0 !important; box-shadow: none !important; border: none !important; }}
    }}
  </style>
</head>
<body class="p-2 sm:p-6">

  <!-- No-Print Top Bar -->
  <div class="no-print max-w-5xl mx-auto mb-4 flex flex-wrap justify-between items-center bg-white p-4 rounded-xl shadow border border-slate-200 gap-2">
    <div>
      <h1 class="font-bold text-slate-800 text-base sm:text-lg flex items-center gap-2">
        <span>📰</span> లక్ష్య తెలుగు డైలీ ఈ-పేపర్ (E-Paper) • {date}
      </h1>
      <p class="text-xs text-slate-500">ఈనాడు, సాక్షి, నమస్తే తెలంగాణ సమగ్ర పరీక్షా విశ్లేషణ</p>
    </div>
    <div class="flex gap-2">
      <button onclick="window.print()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>🖨️ PDF గా సేవ్ / ప్రింట్</span>
      </button>
      <a href="/api/epaper/pdf?date={date}" download class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm px-3.5 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>📥 డైరెక్ట్ PDF డౌన్‌లోడ్</span>
      </a>
      <button onclick="sendPdfToTelegram('{date}')" id="tgSendBtn" class="bg-sky-500 hover:bg-sky-600 text-white font-bold text-xs sm:text-sm px-3.5 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>✈️ టెలిగ్రామ్‌కు పంపండి</span>
      </button>
    </div>
  </div>

  <div class="newspaper-container max-w-5xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-300 p-6 sm:p-10">

    <!-- NEWSPAPER MASTHEAD -->
    <header class="border-b-4 border-slate-900 pb-4 mb-6">
      <div class="flex flex-col sm:flex-row justify-between items-center border-b border-slate-300 pb-2 mb-3 text-xs text-slate-600 font-semibold gap-1">
        <div class="flex items-center gap-2">
          <span class="bg-red-600 text-white font-black px-2 py-0.5 rounded text-[10px] uppercase">డైలీ ఈ-పేపర్</span>
          <span>సంపుటి: 2026 • సంచిక: {date}</span>
        </div>
        <div class="font-bold text-slate-800">
          📅 {date} ({day_name}) • ఆంధ్రప్రదేశ్ & తెలంగాణ ఎడిషన్
        </div>
        <div>
          <span>APPSC • TSPSC • UPSC • BANKING స్పెషల్</span>
        </div>
      </div>

      <div class="text-center my-3">
        <h1 class="text-3xl sm:text-5xl font-black text-slate-950 tracking-tight leading-none mb-1">
          లక్ష్య తెలుగు ఈ-పేపర్
        </h1>
        <p class="text-xs sm:text-sm font-bold text-blue-900 tracking-wide">
          తెలుగు దినపత్రికల సమగ్ర కరెంట్ అఫైర్స్ & డైలీ ఎగ్జామ్ డైజెస్ట్
        </p>
        <p class="text-[11px] text-slate-500 mt-0.5">
          కవరేజ్: ఈనాడు • సాక్షి • ఆంధ్రజ్యోతి • నమస్తే తెలంగాణ • BBC న్యూస్ తెలుగు • ఏషియానెట్ • ABP దేశం
        </p>
      </div>

      <!-- Quick Metrics Bar -->
      <div class="grid grid-cols-4 bg-slate-900 text-white text-center py-2 px-3 rounded-lg text-xs font-bold gap-2">
        <div>📊 ప్రధాన ఆర్టికల్స్: <span class="text-amber-400">{len(articles)}</span></div>
        <div>⚡ ఒక వరుస ముఖ్యాంశాలు: <span class="text-amber-400">{len(one_liners)}</span></div>
        <div>📝 క్విజ్ ప్రశ్నలు: <span class="text-amber-400">{len(quizzes)}</span></div>
        <div>🎯 ప్రాముఖ్యత: <span class="text-emerald-400">గ్రూప్స్ & సివిల్స్</span></div>
      </div>
    </header>

    <!-- NEWSPAPER BODY -->
    <div class="space-y-8">
"""

    # Add each category
    for cat_key, cat_title in CATEGORY_LABELS.items():
        cat_arts = by_cat.get(cat_key, [])
        if not cat_arts:
            continue

        html += f"""
      <section class="border-b-2 border-slate-200 pb-6">
        <div class="bg-slate-100 border-l-4 border-blue-800 px-3 py-1.5 mb-4 flex justify-between items-center">
          <h2 class="text-base sm:text-lg font-black text-blue-950">{cat_title}</h2>
          <span class="text-xs font-bold text-slate-600">{len(cat_arts)} కథనాలు</span>
        </div>

        <div class="newspaper-columns">
        """

        for art in cat_arts:
            source = art.get("source") or "తెలుగు దినపత్రికలు"
            relevance = art.get("exam_relevance") or "పోటీ పరీక్షల ప్రత్యేకం"
            # Extract URL if available
            art_url = art.get("url")
            if not art_url and art.get("detailed_notes"):
                import re
                m_url = re.search(r'https?://[^\s<"]+', art.get("detailed_notes", ""))
                if m_url:
                    art_url = m_url.group(0).rstrip('.,;:!?)>"\'')

            html += f"""
          <article class="article-item mb-5 pb-4 border-b border-slate-200 last:border-none">
            <div class="flex items-center justify-between text-[11px] text-slate-500 font-bold mb-1 flex-wrap gap-1">
              <div class="flex items-center gap-1.5">
                <span class="text-blue-800 bg-blue-50 px-1.5 py-0.5 rounded font-black">[{source}]</span>
                {f'''<a href="{art_url}" target="_blank" rel="noopener noreferrer" class="bg-blue-600 hover:bg-blue-700 text-white px-2 py-0.5 rounded text-[10px] font-bold inline-flex items-center gap-1 no-underline cursor-pointer" style="background-color: #2563eb; color: #ffffff; text-decoration: none; padding: 2px 7px; border-radius: 4px; font-weight: bold; font-size: 10px;" onclick="window.open(\'{art_url}\', \'_blank\'); return true;">🌐 మూల కథనం ↗</a>''' if art_url else ''}
              </div>
              <span class="text-purple-700 bg-purple-50 px-1.5 py-0.5 rounded">🎯 {relevance}</span>
            </div>
            <h3 class="text-sm sm:text-base font-black text-slate-900 leading-snug mb-1.5 hover:text-blue-700">
              {f'''<a href="{art_url}" target="_blank" rel="noopener noreferrer" class="hover:underline text-slate-900" style="color: inherit; text-decoration: none;" onclick="window.open(\'{art_url}\', \'_blank\'); return true;">{art["title"]} <span style="color: #2563eb; font-size: 11px;">↗</span></a>''' if art_url else art['title']}
            </h3>
            <p class="text-xs text-slate-700 leading-relaxed text-justify mb-2">
              {art['summary']}
            </p>
            {f'''<div class="bg-blue-50/80 p-2.5 rounded-lg border border-blue-200 text-[11px] text-blue-950 font-bold leading-relaxed whitespace-pre-line">
              <span class="text-blue-800 font-black">📌 పరీక్షల కీలకాంశం:</span>\n{format_notes_html(art.get("detailed_notes", ""))}
            </div>''' if art.get("detailed_notes") else ''}
          </article>
            """

        html += """
        </div>
      </section>
        """

    # Add One-Liners Section
    if one_liners:
        html += f"""
      <section class="border-b-2 border-slate-200 pb-6">
        <div class="bg-amber-100 border-l-4 border-amber-600 px-3 py-1.5 mb-4 flex justify-between items-center">
          <h2 class="text-base sm:text-lg font-black text-amber-950">
            ⚡ ఒక వరుస ముఖ్యాంశాలు (Quick Revision One-Liners)
          </h2>
          <span class="text-xs font-bold text-amber-800">{len(one_liners)} ముఖ్యాంశాలు</span>
        </div>

        <div class="newspaper-columns text-xs text-slate-800 space-y-2">
        """
        for ol in one_liners:
            html += f"""
          <div class="article-item flex items-start gap-1.5 p-1.5 hover:bg-slate-50 rounded">
            <span class="text-amber-600 font-black">▪</span>
            <span class="font-medium leading-relaxed">{ol['point']}</span>
          </div>
            """
        html += """
        </div>
      </section>
        """

    # Add Daily Practice Quiz Section
    if quizzes:
        html += f"""
      <section class="border-b-2 border-slate-200 pb-6">
        <div class="bg-emerald-100 border-l-4 border-emerald-700 px-3 py-1.5 mb-4 flex justify-between items-center">
          <h2 class="text-base sm:text-lg font-black text-emerald-950">
            📝 నేటి డైలీ ప్రాక్టీస్ క్విజ్ (5 MCQs & Explanations)
          </h2>
          <span class="text-xs font-bold text-emerald-800">వివరణలతో</span>
        </div>

        <div class="space-y-4">
        """
        for idx, q in enumerate(quizzes[:5], 1):
            html += f"""
          <div class="article-item bg-slate-50 border border-slate-200 rounded-xl p-3.5 sm:p-4 text-xs">
            <div class="flex justify-between items-center font-bold mb-1.5">
              <span class="bg-emerald-600 text-white px-2 py-0.5 rounded text-[11px]">ప్రశ్న {idx}</span>
              <span class="text-slate-500">🎯 {q.get('exam_tag', 'APPSC / TSPSC')}</span>
            </div>
            <p class="font-bold text-slate-900 text-sm mb-2">{q['question']}</p>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 mb-2 font-medium">
              <div class="p-1.5 bg-white border rounded"><b>A)</b> {q['option_a']}</div>
              <div class="p-1.5 bg-white border rounded"><b>B)</b> {q['option_b']}</div>
              <div class="p-1.5 bg-white border rounded"><b>C)</b> {q['option_c']}</div>
              <div class="p-1.5 bg-white border rounded"><b>D)</b> {q['option_d']}</div>
            </div>
            <div class="bg-emerald-50 border border-emerald-200 rounded p-2 text-emerald-900 font-semibold">
              <span class="text-emerald-800 font-bold">✔ సరైన సమాధానం: {q['correct_option']}</span> — {q.get('explanation', '')}
            </div>
          </div>
            """
        html += """
        </div>
      </section>
        """

    # Official E-Papers Directory Section
    html += """
      <section class="bg-slate-50 border border-slate-200 rounded-xl p-5">
        <h3 class="text-sm sm:text-base font-black text-slate-900 mb-3 flex items-center gap-1.5">
          <span>🗞️</span> ప్రముఖ తెలుగు దినపత్రికల అధికారిక ఈ-పేపర్స్ (Official E-Paper Portals):
        </h3>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
    """
    for ep in OFFICIAL_TELUGU_EPAPERS:
        html += f"""
          <a href="{ep['url']}" target="_blank" class="block p-3 bg-white border border-slate-200 hover:border-blue-500 hover:shadow-md rounded-xl transition">
            <div class="font-bold text-slate-900 text-xs sm:text-sm flex items-center justify-between">
              <span>{ep['icon']} {ep['name']}</span>
              <span class="text-[10px] text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded font-black">ఓపెన్ ↗</span>
            </div>
            <p class="text-[11px] text-slate-500 mt-1">{ep['description']}</p>
          </a>
        """

    html += f"""
        </div>
      </section>
    </div>

    <!-- FOOTER -->
    <footer class="mt-8 pt-4 border-t-2 border-slate-300 text-center text-xs text-slate-500">
      <p class="font-bold text-slate-700">© 2026 లక్ష్య కరెంట్ అఫైర్స్ • APPSC / TSPSC / UPSC విద్యార్థుల ప్రత్యేకం</p>
      <p class="mt-1">మొబైల్ యాప్: https://tinyurl.com/lakshya-telugu-2026 | టెలిగ్రామ్ బోట్: @venkat_telugu_ca_bot</p>
    </footer>

  </div>

  <script>
    async function sendPdfToTelegram(date) {{
      const btn = document.getElementById('tgSendBtn');
      btn.disabled = true;
      btn.innerHTML = '⏳ పంపుతోంది...';
      try {{
        const res = await fetch('/api/telegram/send_epaper_pdf?date=' + date, {{ method: 'POST' }});
        const data = await res.json();
        if (data.success) {{
          alert('✅ తెలుగు ఈ-పేపర్ PDF మీ టెలిగ్రామ్‌కు విజయవంతంగా పంపబడింది!');
        }} else {{
          alert('⚠️ లోపం: ' + (data.error || 'టెలిగ్రామ్ పంపడంలో లోపం'));
        }}
      }} catch (e) {{
        alert('ఎర్రర్: ' + e.message);
      }} finally {{
        btn.disabled = false;
        btn.innerHTML = '✈️ టెలిగ్రామ్‌కు పంపండి';
      }}
    }}
  </script>
</body>
</html>
"""
    return html

def generate_epaper_pdf(date=None, force_refresh=False):
    """
    Renders HTML to a temporary file and uses headless Edge
    to produce an exact, high-resolution Daily E-Paper PDF.
    Returns the absolute path to the generated PDF file.
    """
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")

    pdf_filename = f"Lakshya_Telugu_EPaper_{date}.pdf"
    out_pdf_path = os.path.join(PDF_CACHE_DIR, pdf_filename)
    static_pdf_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", pdf_filename)
    fallback_today = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "daily_epaper_today.pdf")

    # 1. Return cached PDF if already exists and refresh not forced
    if os.path.exists(out_pdf_path) and not force_refresh and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path

    # 2. Return pre-generated static PDF from frontend/pdfs if available
    if os.path.exists(static_pdf_path) and os.path.getsize(static_pdf_path) > 1000:
        return static_pdf_path

    # 3. Generate HTML and convert to PDF via headless browser if executable is found
    browser_exe = get_browser_executable()
    if browser_exe:
        html_content = render_epaper_html(date=date)
        temp_html_path = os.path.join(PDF_CACHE_DIR, f"temp_epaper_{date}.html")
        try:
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            file_uri = f"file:///{temp_html_path.replace(os.sep, '/')}"
            cmd = f'"{browser_exe}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{out_pdf_path}" "{file_uri}"'
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        except Exception as e:
            print(f"PDF generation error: {e}")
        finally:
            if os.path.exists(temp_html_path):
                try:
                    os.remove(temp_html_path)
                except Exception:
                    pass

    if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path

    # 4. Fallback to today's static pre-compiled PDF
    if os.path.exists(fallback_today) and os.path.getsize(fallback_today) > 1000:
        return fallback_today

    return None

if __name__ == "__main__":
    print("Testing Daily E-Paper PDF Generation...")
    pdf = generate_epaper_pdf("2026-09-12", force_refresh=True)
    print("Generated PDF:", pdf)
    if pdf:
        print("Size:", os.path.getsize(pdf), "bytes")
