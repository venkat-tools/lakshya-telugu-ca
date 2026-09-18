# -*- coding: utf-8 -*-
import sqlite3
from db import get_connection
from mock_tests_data import SUBJECT_MOCK_TESTS
from appsc_group2_data import (
    get_appsc_group2_full_mock,
    get_appsc_group2_pyqs,
    get_appsc_group2_by_section,
    APPSC_GROUP2_SECTIONS
)

def get_all_50_mock_questions():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM quiz_questions ORDER BY id ASC')
    db_questions = [dict(row) for row in c.fetchall()]

    all_questions = []
    seen = set()
    for q in db_questions:
        if q['question'] not in seen:
            all_questions.append({
                'id': q['id'],
                'question': q['question'],
                'option_a': q['option_a'],
                'option_b': q['option_b'],
                'option_c': q['option_c'],
                'option_d': q['option_d'],
                'correct_option': q['correct_option'],
                'explanation': q['explanation'],
                'exam_tag': q.get('exam_tag', 'APPSC / TSPSC'),
                'category': q.get('category', 'జాతీయం')
            })
            seen.add(q['question'])

    for subj in SUBJECT_MOCK_TESTS.values():
        for q in subj['questions']:
            if q['question'] not in seen:
                all_questions.append({
                    'id': q['id'],
                    'question': q['question'],
                    'option_a': q['option_a'],
                    'option_b': q['option_b'],
                    'option_c': q['option_c'],
                    'option_d': q['option_d'],
                    'correct_option': q['correct_option'],
                    'explanation': q['explanation'],
                    'exam_tag': subj['title'],
                    'category': subj['title']
                })
                seen.add(q['question'])

    if len(all_questions) < 50:
        c.execute('SELECT * FROM articles ORDER BY id DESC')
        articles = [dict(row) for row in c.fetchall()]
        for art in articles:
            if len(all_questions) >= 50:
                break
            q_text = f"【{art.get('category', 'జాతీయం')}】 {art['title']} — ఈ అంశానికి సంబంధించి క్రింది వాటిలో సరైన ప్రకటన ఏది?"
            if q_text not in seen:
                all_questions.append({
                    'id': 500 + art['id'],
                    'question': q_text,
                    'option_a': art['summary'],
                    'option_b': 'ఈ అంశం కేవలం అంతర్జాతీయ దౌత్య ఒప్పందాలకు మాత్రమే పరిమితమైనది.',
                    'option_c': 'ఈ విధానం 2020 కంటే ముందే రద్దు చేయబడిన పాత నిబంధన.',
                    'option_d': 'పైవేవీ కావు.',
                    'correct_option': 'A',
                    'explanation': f"{art['summary']}. పరీక్షల ప్రాముఖ్యత: {art.get('detailed_notes') or art.get('exam_relevance') or 'పోటీ పరీక్షలకు ఎంతో ముఖ్యం'}",
                    'exam_tag': art.get('exam_relevance') or 'APPSC / TSPSC / UPSC',
                    'category': art.get('category', 'జాతీయం')
                })
                seen.add(q_text)

    conn.close()
    return all_questions[:50]

def generate_omr_test_html(material_id=None):
    if material_id:
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM uploaded_materials WHERE id = ?", (material_id,))
        row = c.fetchone()
        if row:
            mat = dict(row)
            c.execute("SELECT * FROM quiz_questions WHERE exam_tag LIKE ? OR category = ? ORDER BY id DESC LIMIT 50",
                      (f"%{mat['title'][:20]}%", mat.get('category', '')))
            questions = [dict(r) for r in c.fetchall()]
            if len(questions) < 15:
                c.execute("SELECT * FROM quiz_questions ORDER BY id DESC LIMIT 50")
                for r in c.fetchall():
                    rd = dict(r)
                    if not any(q['question'] == rd['question'] for q in questions):
                        questions.append(rd)
                    if len(questions) >= 25:
                        break
            conn.close()
            test_heading = f"లక్ష్య CA • {mat['title']} ప్రత్యేక OMR మాక్ టెస్ట్"
            test_sub = f"అప్‌లోడ్ చేసిన స్టడీ మెటీరియల్ ఆధారిత పరీక్ష ({mat.get('category', 'విద్యా').upper()}) • {len(questions)} ప్రశ్నలు"
        else:
            conn.close()
            questions = get_all_50_mock_questions()
            test_heading = "లక్ష్య CA • గ్రాండ్ మాక్ టెస్ట్ పేపర్ & OMR షీట్"
            test_sub = "APPSC, TSPSC & UPSC రియల్ ఎగ్జామ్ సిమ్యులేషన్ (50 ప్రశ్నలు)"
    else:
        questions = get_all_50_mock_questions()
        test_heading = "లక్ష్య CA • గ్రాండ్ మాక్ టెస్ట్ పేపర్ & OMR షీట్"
        test_sub = "APPSC, TSPSC & UPSC రియల్ ఎగ్జామ్ సిమ్యులేషన్ (50 ప్రశ్నలు)"

    total_q = len(questions)

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{test_heading}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', sans-serif;
      color: #020617;
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
      .q-card {{ page-break-inside: avoid; border: 1.5px solid #94a3b8 !important; }}
    }}
    .omr-circle {{
      width: 22px;
      height: 22px;
      border: 1.5px solid #0f172a;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 11px;
      font-weight: 800;
    }}
  </style>
</head>
<body class="p-4 md:p-8">

  <!-- Print Toolbar -->
  <div class="no-print max-w-4xl mx-auto mb-6 flex justify-between items-center bg-white p-4 rounded-xl shadow-md border border-slate-200">
    <div>
      <h2 class="font-black text-slate-900 text-lg">📄 {test_heading}</h2>
      <p class="text-xs font-bold text-slate-600">{test_sub}</p>
    </div>
    <div class="flex gap-2">
      <button onclick="window.print()" class="bg-rose-600 hover:bg-rose-700 text-white font-extrabold text-xs sm:text-sm px-4 py-2 rounded-lg shadow transition">
        🖨️ టెస్ట్ పేపర్ & OMR ప్రింట్
      </button>
      <button onclick="window.close()" class="bg-slate-100 text-slate-700 font-bold text-xs px-3 py-2 rounded-lg">
        మూసివేయి
      </button>
    </div>
  </div>

  <div class="max-w-4xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-300 overflow-hidden">
    
    <!-- EXAM HEADER -->
    <div class="bg-gradient-to-r from-blue-900 to-indigo-950 text-white p-6 sm:p-8 border-b-4 border-amber-400">
      <div class="flex justify-between items-start">
        <div>
          <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase">
            అధికారిక మాక్ టెస్ట్ సిరీస్ • OMR ఎడిషన్
          </span>
          <h1 class="text-2xl sm:text-3xl font-black mt-2 tracking-tight">లక్ష్య పోటీ పరీక్షల గ్రాండ్ మాక్ టెస్ట్</h1>
          <p class="text-blue-200 text-xs sm:text-sm font-semibold mt-1">APPSC • TSPSC • UPSC • SI/CONSTABLE • BANKING & SSC</p>
        </div>
        <div class="text-right">
          <div class="text-xl font-black text-amber-400">టెస్ట్ కోడ్: CA-2026</div>
          <div class="text-xs text-blue-200 font-bold">సమయం: 60 నిమిషాలు</div>
          <div class="text-xs text-blue-200 font-bold">గరిష్ట మార్కులు: {total_q}</div>
        </div>
      </div>

      <!-- Candidate Box -->
      <div class="mt-5 grid grid-cols-1 sm:grid-cols-3 gap-3 bg-white/10 p-3 rounded-xl border border-white/20 text-xs">
        <div><b>అభ్యర్థి పేరు:</b> ___________________</div>
        <div><b>హాల్ టికెట్ నెం:</b> _________________</div>
        <div><b>పరీక్ష తేదీ:</b> ______________________</div>
      </div>
    </div>

    <!-- PART 1: QUESTIONS -->
    <div class="p-6 sm:p-8 space-y-5">
      <div class="border-b-2 border-slate-800 pb-2 flex justify-between items-center">
        <h2 class="text-base sm:text-lg font-black text-slate-950">విభాగం - 1: ప్రశ్న పత్రం (Question Paper)</h2>
        <span class="text-xs font-bold text-slate-600">రుణాత్మక మార్కులు: 1/3rd</span>
      </div>

      <div class="space-y-4">
"""

    for idx, q in enumerate(questions, 1):
        html += f"""
        <div class="q-card bg-slate-50/70 border border-slate-300 rounded-xl p-4">
          <div class="flex justify-between items-center text-xs mb-1.5">
            <span class="font-black text-blue-800 bg-blue-100 px-2 py-0.5 rounded">ప్రశ్న {idx}</span>
            <span class="font-bold text-slate-500">🎯 {q.get('exam_tag', 'General Studies')}</span>
          </div>
          <p class="text-sm sm:text-base font-black text-slate-950 mb-3 leading-snug">{q['question']}</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-bold text-slate-900">
            <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center font-black">A</span>
              <span>{q['option_a']}</span>
            </div>
            <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center font-black">B</span>
              <span>{q['option_b']}</span>
            </div>
            <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center font-black">C</span>
              <span>{q['option_c']}</span>
            </div>
            <div class="p-2 bg-white border border-slate-200 rounded-lg flex items-center gap-2">
              <span class="w-5 h-5 rounded-full bg-slate-100 border border-slate-300 flex items-center justify-center font-black">D</span>
              <span>{q['option_d']}</span>
            </div>
          </div>
        </div>
        """

    # PART 2: OMR SHEET
    html += f"""
      </div>
    </div>

    <!-- OMR ANSWER SHEET (PRINTABLE) -->
    <div class="page-break"></div>
    <div class="p-6 sm:p-10 border-t-8 border-rose-600 bg-slate-50/50">
      <div class="text-center border-b-2 border-slate-900 pb-4 mb-6">
        <span class="text-xs font-black bg-rose-600 text-white px-3 py-1 rounded-full uppercase">ప్రింటబుల్ OMR షీట్</span>
        <h2 class="text-xl sm:text-2xl font-black text-slate-950 mt-2">లక్ష్య మాక్ టెస్ట్ OMR ఆన్సర్ షీట్</h2>
        <p class="text-xs font-bold text-slate-600 mt-1">నీలం లేదా నలుపు బాల్ పాయింట్ పెన్ మాత్రమే ఉపయోగించి బబుల్స్ పూర్తిగా నింపండి</p>
      </div>

      <!-- Candidate Box -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 bg-white p-4 rounded-xl border-2 border-slate-800 text-xs font-bold mb-6">
        <div>అభ్యర్థి పేరు: ________________</div>
        <div>రోల్ నంబర్: _________________</div>
        <div>టెస్ట్ కోడ్: CA-2026</div>
        <div>పరీక్ష కేంద్రం: ____________________</div>
      </div>

      <!-- Bubbling Grid -->
      <div class="bg-white p-6 rounded-xl border-2 border-slate-800 shadow-sm">
        <h3 class="text-center font-black text-slate-900 text-sm mb-4 pb-2 border-b border-slate-200">
          సమాధానాలు గుర్తించే ప్రదేశం (RESPONSE SHEET)
        </h3>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-x-8 gap-y-2">
    """

    for idx in range(1, total_q + 1):
        html += f"""
        <div class="flex items-center justify-between py-1 border-b border-slate-100 text-xs font-bold">
          <span class="w-8 font-black text-slate-800">Q{idx}.</span>
          <div class="flex items-center gap-3">
            <div class="omr-circle">A</div>
            <div class="omr-circle">B</div>
            <div class="omr-circle">C</div>
            <div class="omr-circle">D</div>
          </div>
        </div>
        """

    html += f"""
        </div>

        <div class="mt-8 pt-6 border-t-2 border-dashed border-slate-300 flex justify-between text-xs font-black text-slate-800">
          <div>అభ్యర్థి సంతకం: ____________________</div>
          <div>ఇన్విజిలేటర్ సంతకం: ____________________</div>
          <div>పొందిన మార్కులు: ______ / {total_q}</div>
        </div>
      </div>
    </div>

    <!-- PART 3: ANSWER KEY & DETAILED EXPLANATIONS -->
    <div class="page-break"></div>
    <div class="p-6 sm:p-8 border-t-8 border-emerald-600 bg-white">
      <div class="border-b-2 border-emerald-700 pb-3 mb-6">
        <h2 class="text-xl font-black text-emerald-950">📝 సమాధానాల కీ & సమగ్ర వివరణలు (Answer Key & Explanations)</h2>
        <p class="text-xs font-bold text-slate-600 mt-1">పరీక్ష పూర్తయిన తర్వాత మీ సమాధానాలను సరిచూసుకోండి</p>
      </div>

      <!-- Quick Answer Grid -->
      <div class="mb-8 p-4 bg-emerald-50/70 border-2 border-emerald-300 rounded-xl">
        <h4 class="font-black text-emerald-950 text-xs mb-2">క్విక్ ఆన్సర్ కీ టేబుల్:</h4>
        <div class="grid grid-cols-5 sm:grid-cols-10 gap-1.5 text-center text-xs font-black">
    """

    for idx, q in enumerate(questions, 1):
        html += f"""<div class="p-1 bg-white border border-emerald-200 rounded"><span class="text-slate-500 font-bold">{idx}:</span> <span class="text-emerald-700 font-black">{q['correct_option']}</span></div>"""

    html += """
        </div>
      </div>

      <!-- Detailed Explanations -->
      <div class="space-y-4">
    """

    for idx, q in enumerate(questions, 1):
        html += f"""
        <div class="p-3.5 bg-slate-50 rounded-xl border border-slate-200 text-xs font-medium">
          <p class="font-black text-slate-900 mb-1">ప్రశ్న {idx}. {q['question']}</p>
          <p class="font-black text-emerald-800 mb-1">✔ సరైన సమాధానం: ఆప్షన్ {q['correct_option']}</p>
          <p class="text-slate-700 font-semibold leading-relaxed">{q['explanation']}</p>
        </div>
        """

    html += """
      </div>
    </div>

  </div>
</body>
</html>"""

    return html

def generate_group2_omr_test_html(mode="full", section_id=None):
    if mode == "pyqs":
        questions = get_appsc_group2_pyqs()
        test_title = "APPSC గ్రూప్-2 గత పరీక్షల ప్రశ్నలు (Official PYQs - 2024 & 2019)"
        sub_title = "అధికారిక పరీక్ష ప్రశ్నలు, ఆన్సర్ కీ & సమగ్ర వివరణలు"
    elif mode == "section" and section_id:
        questions = get_appsc_group2_by_section(section_id)
        sec_meta = next((s for s in APPSC_GROUP2_SECTIONS if s["id"] == section_id), {"name": section_id})
        test_title = f"APPSC గ్రూప్-2 {sec_meta['name']} ప్రాక్టీస్ టెస్ట్"
        sub_title = f"విభాగం ప్రత్యేక టెస్ట్ ({len(questions)} ప్రశ్నలు)"
    else:
        questions = get_appsc_group2_full_mock()
        test_title = "APPSC గ్రూప్-2 ప్రిలిమ్స్ గ్రాండ్ మాక్ టెస్ట్ (మొత్తం సిలబస్ కలిపి)"
        sub_title = "అన్ని 5 విభాగాలు కలిపి: చరిత్ర • జాగ్రఫీ • సొసైటీ • కరెంట్ అఫైర్స్ • రీజనింగ్ (150 Qs - 150 Mins)"

    total_q = len(questions)

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{test_title} • OMR టెస్ట్ పేపర్</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&family=Outfit:wght@400;600;700&display=swap">
  <style>
    body {{
      font-family: 'Noto Sans Telugu', sans-serif;
      color: #020617;
      background: #f8fafc;
      line-height: 1.6;
    }}
    @media print {{
      *, *::before, *::after {{
        -webkit-print-color-adjust: exact !important;
        print-color-adjust: exact !important;
        color-adjust: exact !important;
      }}
      body {{ background: #fff !important; font-size: 9pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
      .q-card {{ page-break-inside: avoid; border: 1px solid #cbd5e1 !important; }}
    }}
    .omr-circle {{
      width: 20px;
      height: 20px;
      border: 1.5px solid #0f172a;
      border-radius: 50%;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      font-size: 10px;
      font-weight: 800;
    }}
  </style>
</head>
<body class="p-3 md:p-6">

  <!-- Print Toolbar -->
  <div class="no-print max-w-5xl mx-auto mb-6 flex flex-wrap justify-between items-center gap-3 bg-white p-4 rounded-xl shadow-md border border-slate-200">
    <div>
      <h2 class="font-black text-slate-900 text-lg">🎯 {test_title}</h2>
      <p class="text-xs font-bold text-slate-600">{sub_title} • {total_q} ప్రశ్నలు • నెగటివ్ మార్కింగ్: 0.33</p>
    </div>
    <div class="flex gap-2">
      <button onclick="window.print()" class="bg-blue-700 hover:bg-blue-800 text-white font-extrabold text-xs sm:text-sm px-4 py-2 rounded-lg shadow transition flex items-center gap-1.5">
        🖨️ 150 Qs పేపర్ & OMR ప్రింట్ / PDF
      </button>
      <button onclick="window.close()" class="bg-slate-100 text-slate-700 font-bold text-xs px-3 py-2 rounded-lg">
        మూసివేయి
      </button>
    </div>
  </div>

  <div class="max-w-5xl mx-auto space-y-6">

    <!-- PART 1: QUESTION PAPER -->
    <div class="bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      <!-- Exam Header -->
      <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 text-center border-b-4 border-amber-400">
        <span class="inline-block bg-amber-400 text-slate-950 font-black text-xs px-3 py-1 rounded-full uppercase tracking-wider mb-2">
          ఆంధ్రప్రదేశ్ పబ్లిక్ సర్వీస్ కమిషన్ (APPSC) • గ్రూప్-2 సర్వీసెస్
        </span>
        <h1 class="text-xl sm:text-2xl font-black">{test_title}</h1>
        <p class="text-xs sm:text-sm text-blue-200 font-bold mt-1">స్క్రీనింగ్ టెస్ట్ (జనరల్ స్టడీస్ & మెంటల్ ఎబిలిటీ) • మొత్తం సిలబస్</p>
        
        <div class="mt-4 pt-4 border-t border-blue-800/80 grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-bold">
          <div class="bg-blue-950/50 p-2 rounded-lg border border-blue-800">మొత్తం ప్రశ్నలు: <span class="text-amber-300 font-black">{total_q}</span></div>
          <div class="bg-blue-950/50 p-2 rounded-lg border border-blue-800">గరిష్ట మార్కులు: <span class="text-amber-300 font-black">{total_q}</span></div>
          <div class="bg-blue-950/50 p-2 rounded-lg border border-blue-800">వ్యవధి: <span class="text-amber-300 font-black">{total_q} నిమిషాలు</span></div>
          <div class="bg-blue-950/50 p-2 rounded-lg border border-blue-800">నెగటివ్ మార్కింగ్: <span class="text-rose-400 font-black">1/3 (-0.33)</span></div>
        </div>
      </div>

      <!-- General Instructions -->
      <div class="p-4 bg-slate-50 border-b border-slate-200 text-xs font-semibold text-slate-700 leading-relaxed">
        <h3 class="font-black text-slate-900 mb-1">ముఖ్య సూచనలు (Important Instructions):</h3>
        <ol class="list-decimal pl-5 space-y-0.5">
          <li>ఈ ప్రశ్నపత్రంలో మొత్తం 5 విభాగాలు కలవు: (1) భారతీయ చరిత్ర, (2) భూగోళశాస్త్రం, (3) భారతీయ సమాజం, (4) సమకాలీన అంశాలు, (5) మెంటల్ ఎబిలిటీ.</li>
          <li>ప్రతి ప్రశ్నకు 1 మార్కు కేటాయించబడింది. ప్రతి తప్పు సమాధానానికి 0.33 మార్కులు మినహాయించబడతాయి.</li>
          <li>OMR షీట్‌లో బ్లూ లేదా బ్లాక్ బాల్ పాయింట్ పెన్నుతో మాత్రమే సరైన వృత్తాన్ని పూర్తిగా పూరించాలి.</li>
        </ol>
      </div>

      <!-- Questions Grid -->
      <div class="p-6 space-y-4">
    """

    current_sec = None
    for idx, q in enumerate(questions, 1):
        sec_name = q.get("section_name", "")
        if sec_name != current_sec:
            current_sec = sec_name
            html += f"""
            <div class="pt-4 pb-2 border-b-2 border-blue-600 mb-3 mt-4">
              <h3 class="text-sm font-black text-blue-900 bg-blue-50 px-3 py-1.5 rounded-lg inline-block">
                📌 విభాగం: {sec_name}
              </h3>
            </div>
            """

        pyq_badge = f"""<span class="bg-amber-100 text-amber-900 text-[10px] font-black px-2 py-0.5 rounded ml-2 border border-amber-300">★ PYQ {q.get('pyq_year', '')}</span>""" if q.get("is_pyq") else ""

        html += f"""
        <div class="q-card p-3.5 bg-white rounded-xl border border-slate-200 shadow-2xs">
          <div class="flex justify-between items-start gap-2 mb-2">
            <h4 class="font-bold text-xs sm:text-sm text-slate-900 leading-snug">
              <span class="font-black text-blue-700">{idx}.</span> {q['question']}
            </h4>
            {pyq_badge}
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs text-slate-700 pl-4">
            <div class="p-1.5 bg-slate-50 rounded border border-slate-100 font-semibold">(A) {q['option_a']}</div>
            <div class="p-1.5 bg-slate-50 rounded border border-slate-100 font-semibold">(B) {q['option_b']}</div>
            <div class="p-1.5 bg-slate-50 rounded border border-slate-100 font-semibold">(C) {q['option_c']}</div>
            <div class="p-1.5 bg-slate-50 rounded border border-slate-100 font-semibold">(D) {q['option_d']}</div>
          </div>
        </div>
        """

    html += f"""
      </div>
    </div>

    <!-- PART 2: REALISTIC OMR ANSWER SHEET -->
    <div class="page-break"></div>
    <div class="bg-white rounded-2xl shadow-sm border-2 border-slate-900 p-6">
      <div class="border-4 border-slate-900 p-4">
        
        <div class="text-center border-b-2 border-slate-900 pb-3 mb-4">
          <h2 class="text-lg font-black text-slate-900">APPSC GROUP-2 SCREENING TEST • OMR ANSWER SHEET</h2>
          <p class="text-[11px] font-bold text-slate-600">అధికారిక OMR సమాధాన పత్రం • 150 ప్రశ్నలు</p>
        </div>

        <!-- Candidate Details Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 p-3 bg-slate-50 border border-slate-300 rounded-lg text-xs font-bold mb-5">
          <div>అభ్యర్థి పేరు: ___________________________</div>
          <div>హాల్ టికెట్ నంబర్: [ &nbsp; ][ &nbsp; ][ &nbsp; ][ &nbsp; ][ &nbsp; ][ &nbsp; ]</div>
          <div>పరీక్ష తేదీ: ___/___/2026</div>
        </div>

        <!-- OMR Grid: 3 columns of 50 questions each -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
    """

    for col in range(3):
        start_q = col * 50 + 1
        end_q = min((col + 1) * 50, total_q)
        html += f"""<div class="space-y-1.5 border border-slate-200 p-2 rounded-lg bg-slate-50/50">"""
        for q_num in range(start_q, end_q + 1):
            html += f"""
            <div class="flex items-center justify-between px-1 py-0.5 bg-white border border-slate-100 rounded">
              <span class="font-black text-slate-700 w-7 text-[11px]">{q_num}.</span>
              <div class="flex items-center space-x-1.5">
                <span class="omr-circle">A</span>
                <span class="omr-circle">B</span>
                <span class="omr-circle">C</span>
                <span class="omr-circle">D</span>
              </div>
            </div>
            """
        html += """</div>"""

    html += f"""
        </div>

        <div class="mt-6 pt-4 border-t-2 border-dashed border-slate-400 flex justify-between text-xs font-black text-slate-800">
          <div>అభ్యర్థి సంతకం: ____________________</div>
          <div>ఇన్విజిలేటర్ సంతకం: ____________________</div>
          <div>పొందిన మార్కులు: ______ / {total_q}</div>
        </div>
      </div>
    </div>

    <!-- PART 3: ANSWER KEY & DETAILED EXPLANATIONS -->
    <div class="page-break"></div>
    <div class="p-6 border-t-8 border-emerald-600 bg-white rounded-2xl border border-slate-200 shadow-sm">
      <div class="border-b-2 border-emerald-700 pb-3 mb-5">
        <h2 class="text-xl font-black text-emerald-950">📝 సమాధానాల కీ & సమగ్ర వివరణలు (Answer Key & Explanations)</h2>
        <p class="text-xs font-bold text-slate-600 mt-1">APPSC గ్రూప్-2 సిలబస్ ప్రామాణిక వివరణలు</p>
      </div>

      <!-- Quick Answer Grid -->
      <div class="mb-6 p-4 bg-emerald-50/70 border-2 border-emerald-300 rounded-xl">
        <h4 class="font-black text-emerald-950 text-xs mb-2">సత్వర ఆన్సర్ కీ (Quick Answer Key):</h4>
        <div class="grid grid-cols-5 sm:grid-cols-10 gap-1.5 text-center text-xs font-black">
    """

    for idx, q in enumerate(questions, 1):
        html += f"""<div class="p-1 bg-white border border-emerald-200 rounded"><span class="text-slate-500 font-bold">{idx}:</span> <span class="text-emerald-700 font-black">{q['correct_option']}</span></div>"""

    html += """
        </div>
      </div>

      <!-- Detailed Explanations -->
      <div class="space-y-3">
    """

    for idx, q in enumerate(questions, 1):
        pyq_note = f" (APPSC గ్రూప్-2 {q.get('pyq_year')} ప్రిలిమ్స్ ప్రశ్న)" if q.get("is_pyq") else ""
        html += f"""
        <div class="p-3 bg-slate-50 rounded-xl border border-slate-200 text-xs font-medium">
          <p class="font-black text-slate-900 mb-1">ప్రశ్న {idx}. [{q.get('section_name', '')}] {q['question']}{pyq_note}</p>
          <p class="font-black text-emerald-800 mb-1">✔ సరైన సమాధానం: ఆప్షన్ {q['correct_option']}</p>
          <p class="text-slate-700 font-semibold leading-relaxed whitespace-pre-line">{q['explanation']}</p>
        </div>
        """

    html += """
      </div>
    </div>

  </div>
</body>
</html>"""

    return html
