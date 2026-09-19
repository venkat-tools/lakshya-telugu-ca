# -*- coding: utf-8 -*-
"""
Dedicated Daily Current Affairs & Exam Practice Quiz Capsule PDF Generator.
Format: Study Material / Coaching Institute Handbook style (No newspaper layout, no external portal ads).
Sections:
1. ముఖ్యాంశాలు (Categorized Subject Notes with Key Exam Facts)
2. స్పీడ్ రివిజన్ వన్-లైనర్స్ (High-Yield Speed Revision One-Liners)
3. డైలీ ప్రాక్టీస్ టెస్ట్ (5 Exam Standard MCQs with OMR format)
4. సమాధానాలు & సమగ్ర వివరణలు (Answer Key & Detailed Syllabus-aligned Explanations)
"""

import os
import re
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

CATEGORY_TITLES = {
    "education": ("🎓 విద్యా, ఉద్యోగాలు & నోటిఫికేషన్లు", "Education, Recruitment & Exam Syllabus"),
    "regional": ("🌾 ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రభుత్వ పథకాలు", "AP & TS Welfare Schemes, Governance & Policies"),
    "economy": ("📈 భారత ఆర్థిక వ్యవస్థ & బ్యాంకింగ్", "Indian Economy, Banking, RBI & Fiscal Policy"),
    "science_tech": ("🚀 సైన్స్, టెక్నాలజీ & అంతరిక్ష పరిశోధనలు", "Science & Tech, ISRO, Space Missions & Defence"),
    "national": ("🏛️ జాతీయ అంశాలు, రాజ్యాంగం & పాలిటీ", "National Affairs, Constitution & Landmark Verdicts"),
    "environment": ("🌍 పర్యావరణం & సాగునీటి ప్రాజెక్టులు", "Environment, Biodiversity & Major Irrigation Projects"),
    "sports_awards": ("🏆 క్రీడలు, అవార్డులు & రికార్డులు", "Sports, National Awards & Global Records"),
    "appointments": ("👤 ముఖ్య నియామకాలు & కమిషన్లు", "Key Constitutional & Institutional Appointments")
}

def render_ca_quiz_html(date=None):
    """Generate clean, elegant study capsule booklet HTML"""
    today_str = datetime.now().strftime("%Y-%m-%d")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else today_str

    raw_articles = get_articles(date=date)
    articles = []
    seen_titles = set()
    for a in raw_articles:
        src = a.get("source", "")
        tags = a.get("tags", "")
        cat = a.get("category", "")
        if src.startswith("PDF:") or "యూజర్ అప్‌లోడ్" in tags or cat == "study_material":
            continue
        if a["title"] not in seen_titles:
            articles.append(a)
            seen_titles.add(a["title"])

    raw_one_liners = get_one_liners_by_date(date=date)
    one_liners = []
    seen_ol = set()
    for ol in raw_one_liners:
        p = ol.get("point", "")
        if any(bad in p for bad in ["విషయ సూచిక", "అప్‌లోడ్", "PDF:", "Target groups"]):
            continue
        if p not in seen_ol:
            one_liners.append(ol)
            seen_ol.add(p)

    raw_quizzes = get_quiz_by_date(date=date)
    quizzes = [q for q in raw_quizzes if "ఇటీవల అప్‌లోడ్ చేసిన స్టడీ మెటీరియల్" not in q.get("question", "") and not (q.get("exam_tag") or "").startswith("PDF")]

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
  <title>లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రాక్టీస్ క్విజ్ క్యాప్సూల్ - {date}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700;800;900&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', 'Outfit', sans-serif;
      color: #0f172a;
      background: #f8fafc;
      line-height: 1.65;
    }}
    .study-card {{
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    .page-break {{
      page-break-before: always;
      break-before: page;
    }}
    @media print {{
      *, *::before, *::after {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
      }}
      body {{ background: #fff !important; font-size: 10.5pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .container-capsule {{ max-width: 100% !important; padding: 0 !important; margin: 0 !important; box-shadow: none !important; border: none !important; }}
    }}
  </style>
</head>
<body class="p-2 sm:p-6">

  <!-- No-Print Top Action Bar -->
  <div class="no-print max-w-4xl mx-auto mb-4 flex flex-wrap justify-between items-center bg-white p-4 rounded-xl shadow border border-slate-200 gap-2">
    <div>
      <h1 class="font-bold text-slate-800 text-base sm:text-lg flex items-center gap-2">
        <span>📑</span> డైలీ కరెంట్ అఫైర్స్ & ప్రాక్టీస్ క్విజ్ క్యాప్సూల్ • {date}
      </h1>
      <p class="text-xs text-slate-500 font-medium">పోటీ పరీక్షల స్టడీ మెటీరియల్ బుక్‌లెట్ (APPSC • TSPSC • UPSC • SSC • బ్యాంకింగ్)</p>
    </div>
    <div class="flex gap-2">
      <button onclick="window.print()" class="bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>🖨️ PDF సేవ్ / ప్రింట్</span>
      </button>
      <a href="/api/ca_quiz/pdf?date={date}" download class="bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>📥 డైరెక్ట్ PDF డౌన్‌లోడ్</span>
      </a>
      <a href="/api/epaper/pdf?date={date}" target="_blank" class="bg-slate-800 hover:bg-slate-900 text-white font-bold text-xs sm:text-sm px-3.5 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>📰 ఈ-పేపర్ వెర్షన్</span>
      </a>
    </div>
  </div>

  <div class="container-capsule max-w-4xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-300 p-6 sm:p-10">

    <!-- COVER / HEADER BANNER -->
    <header class="border-b-4 border-indigo-900 pb-5 mb-6 text-center">
      <div class="flex justify-between items-center border-b border-slate-200 pb-2 mb-3 text-xs font-bold text-slate-600">
        <span class="bg-indigo-900 text-white px-2.5 py-0.5 rounded uppercase text-[10px] tracking-wider">డైలీ స్టడీ క్యాప్సూల్</span>
        <span class="text-indigo-950 font-black">📅 {date} ({day_name})</span>
        <span class="text-slate-500">APPSC • TSPSC • UPSC GS ప్రత్యేకం</span>
      </div>

      <div class="py-2">
        <h1 class="text-2xl sm:text-4xl font-black text-indigo-950 tracking-tight leading-tight">
          లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రాక్టీస్ క్విజ్
        </h1>
        <p class="text-xs sm:text-sm font-bold text-slate-700 mt-1">
          పోటీ పరీక్షల సిలబస్ ఆధారిత సమగ్ర నోట్స్ & 5 ప్రాక్టీస్ ప్రశ్నలు (వివరణలతో)
        </p>
      </div>

      <!-- Metrics Pill -->
      <div class="mt-4 grid grid-cols-3 bg-indigo-50 border border-indigo-200 rounded-xl py-2 px-4 text-center text-xs font-bold text-indigo-950 gap-2">
        <div>📌 సమగ్ర విశ్లేషణ: <span class="text-indigo-700 font-black">{len(articles)} అంశాలు</span></div>
        <div>⚡ స్పీడ్ రివిజన్: <span class="text-indigo-700 font-black">{len(one_liners)} పాయింట్లు</span></div>
        <div>📝 ప్రాక్టీస్ క్విజ్: <span class="text-indigo-700 font-black">{len(quizzes)} MCQs</span></div>
      </div>
    </header>

    <!-- SECTION 1: DETAILED CURRENT AFFAIRS NOTES -->
    <div class="mb-10">
      <div class="bg-indigo-900 text-white px-4 py-2.5 rounded-xl font-black text-base flex items-center justify-between mb-6 shadow">
        <span>📖 విభాగం-1: సమగ్ర కరెంట్ అఫైర్స్ విశ్లేషణ (Daily Notes)</span>
        <span class="text-xs font-normal text-indigo-200">{len(articles)} కథనాలు</span>
      </div>
"""

    # Render each category
    for cat_key, (cat_telugu, cat_eng) in CATEGORY_TITLES.items():
        cat_arts = by_cat.get(cat_key, [])
        if not cat_arts:
            continue

        html += f"""
      <div class="mb-8">
        <div class="border-b-2 border-indigo-600 pb-1.5 mb-4 flex items-center justify-between">
          <h2 class="text-base sm:text-lg font-black text-indigo-950 flex items-center gap-2">
            {cat_telugu}
          </h2>
          <span class="text-xs font-bold text-slate-500">{cat_eng}</span>
        </div>

        <div class="space-y-6">
        """

        for art in cat_arts:
            source = art.get("source") or "అధికారిక నివేదిక"
            relevance = art.get("exam_relevance") or "పోటీ పరీక్షల సిలబస్"
            summary = art.get("summary", "")
            notes = art.get("detailed_notes", "")

            html += f"""
          <div class="study-card bg-slate-50/80 border border-slate-200 rounded-xl p-4 sm:p-5 hover:border-indigo-400 transition shadow-sm">
            <div class="flex flex-wrap justify-between items-center text-[11px] font-bold text-slate-500 mb-2 gap-1.5">
              <span class="bg-indigo-100 text-indigo-900 px-2.5 py-0.5 rounded font-black">🏛️ {source}</span>
              <span class="bg-purple-100 text-purple-900 border border-purple-200 px-2 py-0.5 rounded">🎯 సిలబస్: {relevance}</span>
            </div>

            <h3 class="text-sm sm:text-base font-black text-slate-900 leading-snug mb-2">
              {art['title']}
            </h3>

            <div class="text-xs text-slate-700 leading-relaxed font-normal text-justify mb-3">
              {summary}
            </div>

            {f'''<div class="bg-white border-l-4 border-indigo-600 p-3 rounded-r-lg border border-slate-200 text-xs text-slate-800 leading-relaxed whitespace-pre-line shadow-xs">
              <span class="font-black text-indigo-950 text-xs block mb-1">📌 పరీక్షల కీలక అంశాలు & సిలబస్ విశ్లేషణ (Key Exam Facts):</span>{notes}
            </div>''' if notes else ''}
          </div>
            """

        html += """
        </div>
      </div>
        """

    # SECTION 2: SPEED REVISION ONE-LINERS
    if one_liners:
        html += f"""
      <div class="page-break pt-4 mb-10">
        <div class="bg-amber-600 text-white px-4 py-2.5 rounded-xl font-black text-base flex items-center justify-between mb-5 shadow">
          <span>⚡ విభాగం-2: స్పీడ్ రివిజన్ వన్-లైనర్స్ (High-Yield Speed Revision)</span>
          <span class="text-xs font-normal text-amber-100">{len(one_liners)} పాయింట్లు</span>
        </div>

        <div class="bg-amber-50/70 border border-amber-200 rounded-xl p-4 sm:p-5">
          <ul class="space-y-2.5 text-xs sm:text-sm text-slate-800">
        """
        for ol in one_liners:
            html += f"""
            <li class="study-card flex items-start gap-2 leading-relaxed">
              <span class="text-amber-700 font-black mt-0.5">▪</span>
              <span class="font-semibold text-slate-900">{ol['point']}</span>
            </li>
            """
        html += """
          </ul>
        </div>
      </div>
        """

    # SECTION 3: PRACTICE MCQS WITH OMR
    if quizzes:
        html += f"""
      <div class="page-break pt-4 mb-8">
        <div class="bg-emerald-700 text-white px-4 py-2.5 rounded-xl font-black text-base flex items-center justify-between mb-5 shadow">
          <span>📝 విభాగం-3: నేటి డైలీ ప్రాక్టీస్ క్విజ్ (Self-Assessment MCQs)</span>
          <span class="text-xs font-normal text-emerald-100">సొంతంగా సాధన చేయండి</span>
        </div>

        <p class="text-xs text-slate-500 font-medium mb-4 italic">
          గమనిక: క్రింది ప్రశ్నలకు సరైన సమాధానాలను గుర్తించి OMR బబుల్‌ను పూరించండి. వివరణాత్మక కీ పేజీ చివరన ఇవ్వబడింది.
        </p>

        <div class="space-y-5">
        """
        for idx, q in enumerate(quizzes[:5], 1):
            html += f"""
          <div class="study-card bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs">
            <div class="flex justify-between items-center font-bold mb-2">
              <span class="bg-emerald-600 text-white px-2.5 py-0.5 rounded text-[11px]">ప్రశ్న {idx}</span>
              <span class="text-slate-500 text-[11px]">🎯 {q.get('exam_tag', 'APPSC / TSPSC Group 1 & 2')}</span>
            </div>

            <p class="font-bold text-slate-900 text-sm mb-3 leading-snug">
              {q['question']}
            </p>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 mb-3">
              <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
                <span class="inline-block w-4 h-4 rounded-full border-2 border-slate-400 text-center text-[10px] leading-3 font-bold"></span>
                <span><b>A)</b> {q['option_a']}</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
                <span class="inline-block w-4 h-4 rounded-full border-2 border-slate-400 text-center text-[10px] leading-3 font-bold"></span>
                <span><b>B)</b> {q['option_b']}</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
                <span class="inline-block w-4 h-4 rounded-full border-2 border-slate-400 text-center text-[10px] leading-3 font-bold"></span>
                <span><b>C)</b> {q['option_c']}</span>
              </div>
              <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
                <span class="inline-block w-4 h-4 rounded-full border-2 border-slate-400 text-center text-[10px] leading-3 font-bold"></span>
                <span><b>D)</b> {q['option_d']}</span>
              </div>
            </div>
          </div>
            """
        html += """
        </div>
      </div>
        """

        # SECTION 4: ANSWERS & EXPLANATIONS
        html += """
      <div class="page-break pt-4 mb-6">
        <div class="bg-slate-900 text-white px-4 py-2.5 rounded-xl font-black text-base flex items-center justify-between mb-5 shadow">
          <span>🔑 విభాగం-4: సమాధానాలు & సమగ్ర వివరణలు (Answer Key & Explanations)</span>
          <span class="text-xs font-normal text-slate-300">సిలబస్ విశ్లేషణ</span>
        </div>

        <div class="space-y-3">
        """
        for idx, q in enumerate(quizzes[:5], 1):
            html += f"""
          <div class="study-card bg-emerald-50/80 border border-emerald-300 rounded-xl p-3.5 text-xs text-slate-800">
            <div class="font-black text-emerald-950 mb-1 flex items-center gap-2">
              <span class="bg-emerald-700 text-white px-2 py-0.5 rounded text-[10px]">ప్రశ్న {idx} సమాధానం: {q['correct_option']}</span>
              <span class="text-slate-600 text-[11px]">({q.get('exam_tag', 'APPSC/TSPSC')})</span>
            </div>
            <div class="text-slate-700 leading-relaxed font-medium">
              {q.get('explanation', '')}
            </div>
          </div>
            """
        html += """
        </div>
      </div>
        """

    # FOOTER
    html += f"""
    <footer class="mt-8 pt-4 border-t-2 border-slate-300 text-center text-xs text-slate-500">
      <p class="font-bold text-slate-800 text-sm">© 2026 లక్ష్య కరెంట్ అఫైర్స్ • సమగ్ర పోటీ పరీక్షల డిజిటల్ అకాడమీ</p>
      <p class="mt-1">మొబైల్ వెబ్ యాప్: https://lakshya-telugu-ca.onrender.com | టెలిగ్రామ్ ఛానల్ & బోట్: @venkat_telugu_ca_bot</p>
      <p class="text-[10px] text-slate-400 mt-1">APPSC గ్రూప్-1, 2, 3 • TSPSC గ్రూప్-1, 2, 3 • UPSC సివిల్స్ GS • పోలీస్ SI & కానిస్టేబుల్ పరీక్షల ప్రత్యేకం</p>
    </footer>

  </div>
</body>
</html>
"""
    return html

def generate_ca_quiz_pdf(date=None, force_refresh=False):
    """
    Renders clean study booklet HTML and generates
    Lakshya_Daily_CA_Quiz_{date}.pdf
    Returns the absolute path to the generated PDF.
    """
    today_str = datetime.now().strftime("%Y-%m-%d")
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else today_str

    # Auto-sync check if needed
    from db import get_articles
    existing_arts = get_articles(date=date)
    if len(existing_arts) < 5:
        try:
            from scraper import sync_daily_news
            from quiz_generator import ensure_daily_quizzes
            sync_daily_news(target_date=date)
            ensure_daily_quizzes(date=date)
        except Exception as sync_err:
            print(f"Auto-sync during CA Quiz PDF generation error: {sync_err}")

    pdf_filename = f"Lakshya_Daily_CA_Quiz_{date}.pdf"
    out_pdf_path = os.path.join(PDF_CACHE_DIR, pdf_filename)
    static_pdf_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", pdf_filename)
    fallback_today = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "daily_ca_quiz_today.pdf")

    # 1. Return cached if exists and not force refresh
    if os.path.exists(out_pdf_path) and not force_refresh and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path

    # 2. Return static if exists and not force refresh
    if os.path.exists(static_pdf_path) and not force_refresh and os.path.getsize(static_pdf_path) > 1000:
        return static_pdf_path

    # 3. Generate HTML and convert via headless browser
    browser_exe = get_browser_executable()
    if browser_exe:
        html_content = render_ca_quiz_html(date=date)
        temp_html_path = os.path.join(PDF_CACHE_DIR, f"temp_ca_quiz_{date}.html")
        try:
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            file_uri = f"file:///{temp_html_path.replace(os.sep, '/')}"
            cmd = f'"{browser_exe}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{out_pdf_path}" "{file_uri}"'
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=40)

            # Copy freshly generated PDF to static directory
            if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
                import shutil
                try:
                    os.makedirs(os.path.dirname(static_pdf_path), exist_ok=True)
                    shutil.copy2(out_pdf_path, static_pdf_path)
                    if date == today_str:
                        shutil.copy2(out_pdf_path, fallback_today)
                except Exception as cp_err:
                    print(f"Error copying generated CA Quiz PDF to frontend: {cp_err}")
        except Exception as e:
            print(f"CA Quiz PDF generation error: {e}")
        finally:
            if os.path.exists(temp_html_path):
                try:
                    os.remove(temp_html_path)
                except Exception:
                    pass

    if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path

    if date == today_str and os.path.exists(fallback_today) and os.path.getsize(fallback_today) > 1000:
        return fallback_today

    return None

if __name__ == "__main__":
    print("Testing Daily CA & Quiz PDF Generation...")
    pdf = generate_ca_quiz_pdf(force_refresh=True)
    print("Generated PDF:", pdf)
    if pdf and os.path.exists(pdf):
        print("Size:", os.path.getsize(pdf), "bytes")
