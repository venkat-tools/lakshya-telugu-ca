# -*- coding: utf-8 -*-
"""
Monthly & Weekly Magazine Booklet Generator for Telugu Current Affairs.
Generates an exam-ready, beautifully styled publication with cover page,
table of contents, categorized topics, and special question bank.
Supports both:
1. Monthly PDF Magazine (మాస పత్రిక)
2. Weekly PDF Capsule / Booklet (వారం వారీ బుక్‌లెట్)
"""

import os
from datetime import datetime, timedelta
from db import get_connection, get_available_dates

MONTH_NAMES_TELUGU = {
    "01": "జనవరి", "02": "ఫిబ్రవరి", "03": "మార్చి", "04": "ఏప్రిల్",
    "05": "మే", "06": "జూన్", "07": "జులై", "08": "ఆగస్టు",
    "09": "సెప్టెంబర్", "10": "అక్టోబర్", "11": "నవంబర్", "12": "డిసెంబర్"
}

CATEGORY_HEADINGS = [
    ("national", "🏛️ జాతీయ ముఖ్యాంశాలు (National Affairs)"),
    ("regional", "🌾 ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రాంతీయ పరిణామాలు (AP & TS Affairs)"),
    ("economy", "📈 ఆర్థిక రంగం & బ్యాంకింగ్ సంస్కరణలు (Economy & Banking)"),
    ("science_tech", "🚀 సైన్స్, టెక్నాలజీ & పర్యావరణం (Science, Tech & Environment)"),
    ("sports_awards", "🏆 క్రీడలు, అవార్డులు & వ్యక్తులు (Sports, Awards & Persons in News)"),
    ("appointments", "👤 ముఖ్యమైన నియామకాలు (Key Appointments)")
]

def fetch_period_data(period_type="monthly", year_month=None, start_date=None, end_date=None):
    """Fetch all articles, quizzes, and one-liners for the requested period"""
    conn = get_connection()
    cursor = conn.cursor()

    if period_type == "weekly":
        if not end_date:
            end_date = datetime.now().strftime("%Y-%m-%d")
        if not start_date:
            start_dt = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=6)
            start_date = start_dt.strftime("%Y-%m-%d")
        
        cursor.execute("""
            SELECT * FROM articles 
            WHERE date >= ? AND date <= ? 
            ORDER BY category, date DESC, id DESC
        """, (start_date, end_date))
        articles = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT * FROM quiz_questions 
            WHERE date >= ? AND date <= ? 
            ORDER BY date DESC, id ASC
        """, (start_date, end_date))
        quizzes = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT * FROM one_liners 
            WHERE date >= ? AND date <= ? 
            ORDER BY date DESC, id ASC
        """, (start_date, end_date))
        one_liners = [dict(row) for row in cursor.fetchall()]

        period_title = f"వీక్లీ స్పెషల్ బుక్‌లెట్ ({start_date} నుంచి {end_date})"
        sub_title = "గత 7 రోజుల సంపూర్ణ కరెంట్ అఫైర్స్ & ప్రాక్టీస్ ప్రశ్నలు"
    else:
        # Monthly
        if not year_month:
            year_month = datetime.now().strftime("%Y-%m")
        cursor.execute("""
            SELECT * FROM articles 
            WHERE date LIKE ? 
            ORDER BY category, date DESC, id DESC
        """, (f"{year_month}%",))
        articles = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT * FROM quiz_questions 
            WHERE date LIKE ? 
            ORDER BY date DESC, id ASC
        """, (f"{year_month}%",))
        quizzes = [dict(row) for row in cursor.fetchall()]

        cursor.execute("""
            SELECT * FROM one_liners 
            WHERE date LIKE ? 
            ORDER BY date DESC, id ASC
        """, (f"{year_month}%",))
        one_liners = [dict(row) for row in cursor.fetchall()]

        parts = year_month.split("-")
        y = parts[0]
        m = parts[1] if len(parts) > 1 else "09"
        m_name = MONTH_NAMES_TELUGU.get(m, m)
        period_title = f"{m_name} {y} - మాస పత్రిక (Monthly Magazine)"
        sub_title = f"{m_name} నెల సంపూర్ణ సమగ్ర కరెంట్ అఫైర్స్ & క్వశ్చన్ బ్యాంక్"

    conn.close()

    # Filter and deduplicate for high-yield exam quality
    try:
        from scraper import is_exam_worthy_content
    except Exception:
        def is_exam_worthy_content(t):
            return True

    try:
        from pdf_generator import is_exam_worthy
    except Exception:
        def is_exam_worthy(a):
            return is_exam_worthy_content(a.get("title", ""))

    seen_titles = set()
    clean_articles = []
    for a in articles:
        norm = a.get("title", "").strip().lower()
        if norm not in seen_titles and is_exam_worthy(a):
            seen_titles.add(norm)
            clean_articles.append(a)
    
    # Fallback to recent articles if range has too few
    if len(clean_articles) < 5:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles ORDER BY date DESC, id DESC LIMIT 35")
        for a in [dict(row) for row in cursor.fetchall()]:
            norm = a.get("title", "").strip().lower()
            if norm not in seen_titles and is_exam_worthy(a):
                seen_titles.add(norm)
                clean_articles.append(a)
        conn.close()

    # Cap to top 40 high-yield articles
    clean_articles = clean_articles[:40]

    if not quizzes:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM quiz_questions ORDER BY date DESC, id DESC LIMIT 20")
        quizzes = [dict(row) for row in cursor.fetchall()]
        conn.close()

    seen_ol = set()
    clean_one_liners = []
    for ol in one_liners:
        norm = ol.get("point", "").strip().lower()
        if norm not in seen_ol and is_exam_worthy_content(norm):
            seen_ol.add(norm)
            clean_one_liners.append(ol)

    if len(clean_one_liners) < 5:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM one_liners ORDER BY date DESC, id DESC LIMIT 30")
        for ol in [dict(row) for row in cursor.fetchall()]:
            norm = ol.get("point", "").strip().lower()
            if norm not in seen_ol and is_exam_worthy_content(norm):
                seen_ol.add(norm)
                clean_one_liners.append(ol)
        conn.close()

    clean_one_liners = clean_one_liners[:50]

    return clean_articles, quizzes, clean_one_liners, period_title, sub_title

def render_magazine_html(period_type="monthly", year_month=None, start_date=None, end_date=None):
    articles, quizzes, one_liners, period_title, sub_title = fetch_period_data(
        period_type=period_type, 
        year_month=year_month, 
        start_date=start_date, 
        end_date=end_date
    )

    # Group articles by category
    by_category = {}
    for art in articles:
        cat = art["category"]
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(art)

    badge_label = "వీక్లీ బుక్‌లెట్" if period_type == "weekly" else "మాస పత్రిక"
    header_gradient = "from-emerald-950 via-teal-950 to-slate-950" if period_type == "weekly" else "from-blue-900 via-indigo-950 to-slate-950"

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>లక్ష్య CA - {period_title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800&family=Outfit:wght@400;600;700&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', 'Outfit', sans-serif;
      color: #0f172a;
      background: #f8fafc;
      line-height: 1.65;
    }}
    @media print {{
      *, *::before, *::after {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }}
      body {{ background: #fff !important; font-size: 11pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
      .magazine-container {{ max-width: 100% !important; padding: 0 !important; margin: 0 !important; }}
      .magazine-card {{ page-break-inside: avoid !important; border: 2px solid #cbd5e1 !important; border-left: 6px solid #2563eb !important; border-radius: 12px !important; margin-bottom: 20px !important; }}
    }}
  </style>
</head>
<body class="p-4 md:p-8">

  <!-- Print Action Toolbar -->
  <div class="no-print max-w-4xl mx-auto mb-6 flex justify-between items-center bg-white p-4 rounded-xl shadow-md border border-slate-200">
    <div>
      <h2 class="font-bold text-slate-800 text-lg">📚 {period_title}</h2>
      <p class="text-xs text-slate-500">{sub_title} - ప్రింట్ లేదా PDF లో సేవ్ చేసుకోండి</p>
    </div>
    <div class="flex gap-2">
      <button onclick="window.print()" class="bg-blue-600 hover:bg-blue-700 text-white font-semibold text-xs sm:text-sm px-4 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        <span>🖨️ PDF గా సేవ్ / ప్రింట్</span>
      </button>
      <button onclick="window.close()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs sm:text-sm px-3 py-2 rounded-lg transition">
        మూసివేయి
      </button>
    </div>
  </div>

  <div class="magazine-container max-w-4xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
    
    <!-- COVER PAGE -->
    <div class="bg-gradient-to-br {header_gradient} text-white p-8 md:p-14 flex flex-col justify-between min-h-[480px]">
      <div class="flex justify-between items-start border-b border-blue-800/80 pb-6">
        <div>
          <span class="bg-amber-400 text-slate-950 text-xs font-bold px-3 py-1 rounded-full uppercase tracking-wider">
            {badge_label} • పోటీ పరీక్షల ప్రత్యేకం
          </span>
          <h1 class="text-3xl md:text-5xl font-extrabold mt-3 tracking-tight">లక్ష్య కరెంట్ అఫైర్స్</h1>
          <p class="text-blue-200 text-sm md:text-base mt-1">APPSC • TSPSC • UPSC • SSC • BANKING • POLICE</p>
        </div>
        <div class="text-right">
          <div class="text-xl md:text-2xl font-black text-amber-400">{badge_label}</div>
          <div class="text-sm font-bold text-blue-200">ప్రత్యేక ఎడిషన్</div>
        </div>
      </div>

      <div class="my-8">
        <h3 class="text-lg font-bold text-amber-300 mb-3">{period_title}</h3>
        <p class="text-sm text-slate-200 mb-4">{sub_title}</p>
        <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 text-xs sm:text-sm text-slate-200">
          <li class="flex items-center gap-2">✔ ఈనాడు, సాక్షి, నమస్తే తెలంగాణ వార్తా విశ్లేషణలు</li>
          <li class="flex items-center gap-2">✔ కేంద్ర, రాష్ట్ర సంక్షేమ పథకాలు & జీవోలు</li>
          <li class="flex items-center gap-2">✔ ఆర్థికం, బడ్జెట్ & బ్యాంకింగ్ సంస్కరణలు</li>
          <li class="flex items-center gap-2">✔ సైన్స్, టెక్నాలజీ & ఇస్రో నూతన మైలురాళ్ళు</li>
          <li class="flex items-center gap-2">✔ {len(articles)} సమగ్ర ఆర్టికల్స్ & {len(one_liners)} ఒక వరుస ముఖ్యాంశాలు</li>
          <li class="flex items-center gap-2">✔ {len(quizzes)} ప్రాక్టీస్ ప్రశ్నలతో స్పెషల్ క్వశ్చన్ బ్యాంక్</li>
        </ul>
      </div>

      <div class="border-t border-blue-800/80 pt-4 flex justify-between items-center text-xs text-blue-300">
        <span>ప్రచురణ: Antigravity Smart Daily Digest</span>
        <span>అధికారిక తెలుగు పరీక్షల ఎడిషన్</span>
      </div>
    </div>

    <!-- QUICK STATS BAR -->
    <div class="bg-slate-100 p-4 border-b border-slate-200 grid grid-cols-3 text-center text-xs sm:text-sm font-semibold">
      <div>📰 ఆర్టికల్స్: <span class="text-blue-700 font-bold">{len(articles)}</span></div>
      <div>⚡ వన్-లైనర్స్: <span class="text-amber-700 font-bold">{len(one_liners)}</span></div>
      <div>📝 ప్రాక్టీస్ MCQs: <span class="text-emerald-700 font-bold">{len(quizzes)}</span></div>
    </div>

    <!-- CONTENT -->
    <div class="p-6 md:p-10 space-y-10">
"""

    # Add Categorized Articles
    for cat_key, cat_title in CATEGORY_HEADINGS:
        cat_articles = by_category.get(cat_key, [])
        if not cat_articles:
            continue

        html += f"""
        <section class="category-block">
          <div class="border-b-2 border-blue-600 pb-2 mb-5">
            <h2 class="text-lg md:text-xl font-bold text-blue-900">{cat_title}</h2>
          </div>
          <div class="space-y-5">
        """

        for art in cat_articles:
            source_badge = f"<span class='text-amber-700 font-semibold'>[{art.get('source', 'తెలుగు దినపత్రికలు')}]</span>" if art.get("source") else ""
            html += f"""
            <div class="magazine-card bg-white border-2 border-slate-200 rounded-xl p-4 sm:p-5 border-l-4 border-l-blue-600 shadow-2xs">
              <div class="flex justify-between items-center text-xs text-slate-700 font-bold mb-2">
                <span class="font-black text-blue-800">📅 {art['date']} {source_badge}</span>
                <span class="bg-purple-50 border border-purple-200 text-purple-900 px-2.5 py-0.5 rounded-md font-bold">🎯 {art['exam_relevance']}</span>
              </div>
              <h3 class="text-base sm:text-lg font-black text-slate-950 mb-2 leading-snug">{art['title']}</h3>
              <p class="text-xs sm:text-sm font-semibold text-slate-900 mb-3 leading-relaxed">{art['summary']}</p>
              
              {f'<div class="bg-blue-50/90 p-3.5 rounded-xl border border-blue-200 text-xs sm:text-sm text-slate-950 whitespace-pre-line leading-relaxed font-bold"><b class="text-blue-950 flex items-center gap-1 mb-1">📘 పరీక్షల కీలక నోట్స్ (Exam Takeaways):</b>{art["detailed_notes"]}</div>' if art.get("detailed_notes") else ''}
            </div>
            """

        html += """
          </div>
        </section>
        """

    # Add One-Liners Section
    if one_liners:
        html += f"""
        <div class="page-break"></div>
        <section class="bg-amber-50 border border-amber-200 rounded-xl p-6">
          <h2 class="text-lg md:text-xl font-bold text-amber-900 mb-4 pb-2 border-b border-amber-300">
            ⚡ ఒక వరుస ముఖ్యాంశాలు (Quick Revision One-Liners)
          </h2>
          <ul class="space-y-2.5 text-xs sm:text-sm text-slate-800">
        """
        for ol in one_liners:
            html += f"<li class='flex items-start gap-2'><span>▪</span> <span>{ol['point']}</span></li>"
        html += """
          </ul>
        </section>
        """

    # Add Question Bank Section
    if quizzes:
        html += f"""
        <div class="page-break"></div>
        <section class="mt-8">
          <div class="border-b-2 border-emerald-600 pb-2 mb-6">
            <h2 class="text-lg md:text-xl font-bold text-emerald-900">
              📝 స్పెషల్ ప్రాక్టీస్ క్వశ్చన్ బ్యాంక్ ({len(quizzes)} MCQs)
            </h2>
            <p class="text-xs text-slate-500">సమాధానాలు మరియు సమగ్ర వివరణలతో</p>
          </div>
          <div class="space-y-5">
        """
        for idx, q in enumerate(quizzes, 1):
            html += f"""
            <div class="magazine-card bg-slate-50 border border-slate-200 rounded-xl p-4 sm:p-5">
              <div class="flex justify-between items-center text-xs mb-2">
                <span class="font-bold text-emerald-800 bg-emerald-100 px-2 py-0.5 rounded">ప్రశ్న {idx}</span>
                <span class="text-slate-500">📅 {q['date']} • 🎯 {q['exam_tag']}</span>
              </div>
              <p class="text-sm font-bold text-slate-900 mb-3">{q['question']}</p>
              
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs mb-3">
                <div class="p-2 bg-white border rounded">A) {q['option_a']}</div>
                <div class="p-2 bg-white border rounded">B) {q['option_b']}</div>
                <div class="p-2 bg-white border rounded">C) {q['option_c']}</div>
                <div class="p-2 bg-white border rounded">D) {q['option_d']}</div>
              </div>

              <div class="bg-emerald-50 border border-emerald-200 rounded-lg p-2.5 text-xs text-emerald-900">
                <p class="font-bold text-emerald-800 mb-0.5">✔ సరైన సమాధానం: ఆప్షన్ {q['correct_option']}</p>
                <p>{q['explanation']}</p>
              </div>
            </div>
            """
        html += """
          </div>
        </section>
        """

    html += """
      <div class="text-center pt-8 border-t border-slate-200 text-xs text-slate-400">
        © 2026 లక్ష్య కరెంట్ అఫైర్స్ • APPSC / TSPSC / UPSC విజేతల కోసం
      </div>
    </div>
  </div>
</body>
</html>
"""
    return html

def generate_magazine_pdf(year_month="2026-09", force_refresh=False):
    """
    Renders the Monthly Magazine HTML and compiles it to a high-resolution PDF.
    """
    import subprocess
    from pdf_generator import get_browser_executable, PDF_CACHE_DIR
    
    pdf_filename = f"Lakshya_September_2026_Monthly_Magazine.pdf" if year_month == "2026-09" else f"Lakshya_Monthly_Magazine_{year_month}.pdf"
    out_pdf_path = os.path.join(PDF_CACHE_DIR, pdf_filename)
    static_pdf_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", pdf_filename)

    if os.path.exists(out_pdf_path) and not force_refresh and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path

    if os.path.exists(static_pdf_path) and not force_refresh and os.path.getsize(static_pdf_path) > 1000:
        return static_pdf_path

    browser_exe = get_browser_executable()
    if browser_exe:
        html_content = render_magazine_html(period_type="monthly", year_month=year_month)
        temp_html_path = os.path.join(PDF_CACHE_DIR, f"temp_mag_{year_month}.html")
        try:
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            file_uri = f"file:///{temp_html_path.replace(os.sep, '/')}"
            cmd = f'"{browser_exe}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{out_pdf_path}" "{file_uri}"'
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)

            if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
                import shutil
                try:
                    os.makedirs(os.path.dirname(static_pdf_path), exist_ok=True)
                    shutil.copy2(out_pdf_path, static_pdf_path)
                except Exception as cp_err:
                    print(f"Error copying magazine PDF to frontend: {cp_err}")
        except Exception as e:
            print(f"Magazine PDF generation error: {e}")
        finally:
            if os.path.exists(temp_html_path):
                try:
                    os.remove(temp_html_path)
                except Exception:
                    pass

    if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path
    if os.path.exists(static_pdf_path) and os.path.getsize(static_pdf_path) > 1000:
        return static_pdf_path
    return None

def generate_weekly_pdf(end_date=None, force_refresh=False):
    """
    Renders the Weekly Booklet HTML and compiles it to a high-resolution PDF.
    """
    import subprocess
    from pdf_generator import get_browser_executable, PDF_CACHE_DIR
    
    if not end_date:
        dates = get_available_dates()
        end_date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")
    
    start_dt = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=6)
    start_date = start_dt.strftime("%Y-%m-%d")
    
    pdf_filename = f"Lakshya_Weekly_Capsule_{start_date}_to_{end_date}.pdf"
    out_pdf_path = os.path.join(PDF_CACHE_DIR, pdf_filename)
    static_pdf_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", pdf_filename)
    fallback_weekly = os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "weekly_capsule_current.pdf")

    if os.path.exists(out_pdf_path) and not force_refresh and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path
    if os.path.exists(static_pdf_path) and not force_refresh and os.path.getsize(static_pdf_path) > 1000:
        return static_pdf_path

    browser_exe = get_browser_executable()
    if browser_exe:
        html_content = render_magazine_html(period_type="weekly", start_date=start_date, end_date=end_date)
        temp_html_path = os.path.join(PDF_CACHE_DIR, f"temp_weekly_{end_date}.html")
        try:
            with open(temp_html_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            file_uri = f"file:///{temp_html_path.replace(os.sep, '/')}"
            cmd = f'"{browser_exe}" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf="{out_pdf_path}" "{file_uri}"'
            subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)

            if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
                import shutil
                try:
                    os.makedirs(os.path.dirname(static_pdf_path), exist_ok=True)
                    shutil.copy2(out_pdf_path, static_pdf_path)
                    shutil.copy2(out_pdf_path, fallback_weekly)
                except Exception as cp_err:
                    print(f"Error copying weekly PDF to frontend: {cp_err}")
        except Exception as e:
            print(f"Weekly PDF generation error: {e}")
        finally:
            if os.path.exists(temp_html_path):
                try:
                    os.remove(temp_html_path)
                except Exception:
                    pass

    if os.path.exists(out_pdf_path) and os.path.getsize(out_pdf_path) > 1000:
        return out_pdf_path
    if os.path.exists(static_pdf_path) and os.path.getsize(static_pdf_path) > 1000:
        return static_pdf_path
    if os.path.exists(fallback_weekly) and os.path.getsize(fallback_weekly) > 1000:
        return fallback_weekly
    return None
