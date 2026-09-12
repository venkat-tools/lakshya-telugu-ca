# -*- coding: utf-8 -*-
"""
Printable Study Handbooks for APPSC / TSPSC Exams:
1. Welfare Schemes & Budget 2026 Handbook (/schemes_handbook)
2. Mains Descriptive Model Answers Bank (/mains_answer_bank)
3. APPSC Group 1, 2, 3 Multi-Exam OMR Test Paper (/omr_appsc_all)
"""

from schemes_budget_data import get_all_schemes, get_schemes_quizzes
from mains_descriptive_data import get_all_mains_questions
from ap_history_data import get_all_ap_history_topics, get_appsc_exam_questions, APPSC_EXAM_TYPES

def render_schemes_handbook_html():
    schemes = get_all_schemes()
    ap_sch = [s for s in schemes if s.get("category") == "ap"]
    ts_sch = [s for s in schemes if s.get("category") == "telangana"]
    ctr_sch = [s for s in schemes if s.get("category") == "central"]
    quizzes = get_schemes_quizzes()

    def make_cards(s_list, color_theme):
        cards = ""
        for s in s_list:
            pyq = f'<div class="text-[11px] bg-rose-50 text-rose-950 p-2 rounded-lg border border-rose-200 font-bold"><b>🏆 PYQ:</b> {s["pyq_note"]}</div>' if s.get("pyq_note") else ''
            cards += f"""
            <div class="scheme-card bg-slate-50 border border-slate-200 rounded-2xl p-4 space-y-2.5 hover:border-{color_theme}-500 transition">
              <div class="flex justify-between items-start gap-2">
                <h3 class="text-base font-black text-slate-900">{s['telugu_name']}</h3>
                <span class="bg-{color_theme}-100 text-{color_theme}-900 text-[10px] font-black px-2 py-0.5 rounded-md shrink-0">{s['name']}</span>
              </div>
              <div class="text-xs text-blue-800 font-bold">🏢 నోడల్ శాఖ: {s['dept']}</div>
              <div class="bg-white p-3 rounded-xl border border-slate-200 text-xs space-y-1.5">
                <p><b class="text-emerald-800">💰 ఆర్థిక లబ్ధి:</b> {s['benefit']}</p>
                <p><b class="text-indigo-800">🎯 అర్హత ప్రమాణాలు:</b> {s['eligibility']}</p>
              </div>
              <div class="text-xs text-slate-700 whitespace-pre-line leading-relaxed bg-{color_theme}-50/40 p-2.5 rounded-xl border border-{color_theme}-200">
                <b>📌 పథకం ముఖ్యాంశాలు:</b>\n{s['key_facts']}
              </div>
              <div class="text-[11px] bg-amber-50 text-amber-950 p-2 rounded-lg border border-amber-200 font-semibold">
                <b>📊 బడ్జెట్ కేటాయింపులు:</b> {s['budget_note']}
              </div>
              {pyq}
            </div>
            """
        return cards

    cards_ap = make_cards(ap_sch, "emerald")
    cards_ts = make_cards(ts_sch, "rose")
    cards_ctr = make_cards(ctr_sch, "blue")

    quiz_cards = ""
    for idx, q in enumerate(quizzes, 1):
        opts_html = "".join([f'<div class="p-1.5 bg-slate-50 border rounded text-xs {"font-bold text-emerald-800 bg-emerald-50 border-emerald-300" if opt == q["answer"] else ""}">• {opt}</div>' for opt in q['options']])
        quiz_cards += f"""
        <div class="scheme-card bg-white border border-slate-200 rounded-2xl p-4 space-y-2 text-xs">
          <div class="flex justify-between items-center font-bold">
            <span class="bg-slate-800 text-white px-2 py-0.5 rounded text-[10px]">ప్రశ్న {idx}</span>
            <span class="text-slate-500 font-bold">📂 {q['category'].upper()}</span>
          </div>
          <p class="font-black text-slate-900 text-sm">{q['question']}</p>
          <div class="grid grid-cols-2 gap-1.5 font-medium my-2">
            {opts_html}
          </div>
          <div class="bg-emerald-50 border border-emerald-200 rounded p-2 text-emerald-950 font-semibold">
            <span class="text-emerald-800 font-bold">✔ సరైన సమాధానం: {q['answer']}</span> — {q['explanation']}
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ప్రభుత్వ సంక్షేమ పథకాలు & బడ్జెట్ 2026 సమగ్ర హ్యాండ్‌బుక్ | APPSC & TSPSC</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&display=swap">
  <style>
    body {{ font-family: 'Noto Sans Telugu', sans-serif; background: #f8fafc; color: #0f172a; }}
    @media print {{
      *, *::before, *::after {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; }}
      body {{ background: #fff !important; font-size: 10pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
      .scheme-card {{ break-inside: avoid; page-break-inside: avoid; }}
    }}
  </style>
</head>
<body class="p-3 sm:p-6">

  <!-- Action Bar -->
  <div class="no-print max-w-5xl mx-auto mb-5 flex justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
    <a href="/" class="text-xs font-bold bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition">← డ్యాష్‌బోర్డ్‌కు వెళ్ళు</a>
    <h1 class="text-sm sm:text-base font-black text-slate-900">🌾 ప్రభుత్వ సంక్షేమ పథకాలు & బడ్జెట్ 2026 హ్యాండ్‌బుక్</h1>
    <button onclick="window.print()" class="bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs px-4 py-2 rounded-xl shadow transition">🖨️ PDF గా సేవ్ / ప్రింట్</button>
  </div>

  <div class="max-w-5xl mx-auto bg-white rounded-3xl shadow-xl border border-slate-300 p-6 sm:p-10 space-y-8">
    <header class="border-b-4 border-slate-900 pb-5 text-center">
      <div class="inline-flex items-center gap-2 bg-gradient-to-r from-emerald-600 to-teal-700 text-white text-xs font-black px-3.5 py-1 rounded-full uppercase mb-2">
        🎯 APPSC గ్రూప్ 1, 2, 3 • TSPSC • UPSC స్పెషల్
      </div>
      <h1 class="text-2xl sm:text-4xl font-black text-slate-950 mb-2">ప్రభుత్వ సంక్షేమ పథకాలు & బడ్జెట్ 2026 హ్యాండ్‌బుక్</h1>
      <p class="text-xs sm:text-sm font-bold text-slate-600">ఆంధ్రప్రదేశ్ 'సూపర్ సిక్స్', తెలంగాణ 'ఆరు గ్యారెంటీలు' & కేంద్ర ఫ్లాగ్‌షిప్ పథకాల సమగ్ర విశ్లేషణ</p>
    </header>

    <!-- Part 1: AP Super Six -->
    <section class="space-y-4">
      <div class="bg-emerald-50 border-l-4 border-emerald-600 px-4 py-2.5 rounded-r-xl flex justify-between items-center">
        <div>
          <h2 class="text-base sm:text-lg font-black text-emerald-950">🚩 ఆంధ్రప్రదేశ్ కూటమి ప్రభుత్వం - 'సూపర్ సిక్స్' పథకాలు</h2>
          <p class="text-xs text-emerald-800">తల్లికి వందనం, అన్నదాత సుఖీభవ, దీపం-2, ఉచిత బస్సు, నిరుద్యోగ భృతి, ఆడబిడ్డ నిధి</p>
        </div>
        <span class="bg-emerald-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">{len(ap_sch)} పథకాలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_ap}
      </div>
    </section>

    <!-- Part 2: Telangana Six Guarantees -->
    <section class="space-y-4 pt-4 border-t-2 border-slate-200">
      <div class="bg-rose-50 border-l-4 border-rose-600 px-4 py-2.5 rounded-r-xl flex justify-between items-center">
        <div>
          <h2 class="text-base sm:text-lg font-black text-rose-950">🌾 తెలంగాణ కాంగ్రెస్ ప్రభుత్వం - 'ఆరు గ్యారెంటీలు'</h2>
          <p class="text-xs text-rose-800">మహాలక్ష్మి, గృహజ్యోతి, రైతు భరోసా, ఇందిరమ్మ ఇండ్లు, చేయూత, యువ వికాసం</p>
        </div>
        <span class="bg-rose-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">{len(ts_sch)} పథకాలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_ts}
      </div>
    </section>

    <!-- Part 3: Central Schemes -->
    <section class="space-y-4 pt-4 border-t-2 border-slate-200">
      <div class="bg-blue-50 border-l-4 border-blue-600 px-4 py-2.5 rounded-r-xl flex justify-between items-center">
        <div>
          <h2 class="text-base sm:text-lg font-black text-blue-950">🇮🇳 కేంద్ర ప్రభుత్వ ఫ్లాగ్‌షిప్ సంక్షేమ పథకాలు</h2>
          <p class="text-xs text-blue-800">పీఎం సూర్య ఘర్, పీఎం కిసాన్, ఆయుష్మాన్ భారత్, లఖ్‌పతి దీదీ</p>
        </div>
        <span class="bg-blue-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">{len(ctr_sch)} పథకాలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {cards_ctr}
      </div>
    </section>

    <!-- Part 4: Schemes MCQs -->
    <section class="space-y-4 pt-4 border-t-2 border-slate-200 page-break">
      <div class="bg-slate-900 text-white px-4 py-3 rounded-xl flex justify-between items-center">
        <div>
          <h2 class="text-base sm:text-lg font-black">📝 పథకాలు & బడ్జెట్ ప్రాక్టీస్ MCQs & వివరణలు</h2>
          <p class="text-xs text-slate-300">పూర్వ పరీక్షల సరళి ఆధారంగా</p>
        </div>
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-2.5 py-1 rounded-lg">{len(quizzes)} ప్రశ్నలు</span>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        {quiz_cards}
      </div>
    </section>

  </div>
</body>
</html>"""
    return html

def render_mains_answer_bank_html():
    questions = get_all_mains_questions()

    cards = ""
    for idx, q in enumerate(questions, 1):
        ma = q["model_answer"]
        body_lis = "".join([f'<li class="mb-1.5">{bp}</li>' for bp in ma["body_points"]])

        cards += f"""
        <article class="mains-card bg-white border border-slate-300 rounded-2xl p-5 sm:p-6 space-y-4 shadow-sm">
          <div class="flex justify-between items-center border-b border-slate-200 pb-2">
            <span class="bg-purple-100 text-purple-900 text-xs font-black px-3 py-1 rounded-md">ప్రశ్న {idx} • {q['paper']}</span>
            <span class="text-xs font-bold text-slate-500">విభాగం: {q['subject']}</span>
          </div>

          <h3 class="text-base sm:text-lg font-black text-slate-950 leading-snug">
            {q['question']}
          </h3>

          <div class="space-y-3 text-xs sm:text-sm">
            <!-- 1. Intro -->
            <div class="bg-blue-50/70 p-3 rounded-xl border border-blue-200">
              <h4 class="font-black text-blue-950 mb-1 flex items-center gap-1">
                <span>📌 1. పరిచయం (Introduction & Context):</span>
              </h4>
              <p class="text-slate-800 leading-relaxed text-justify">{ma['intro']}</p>
            </div>

            <!-- 2. Body -->
            <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
              <h4 class="font-black text-slate-950 mb-1.5 flex items-center gap-1">
                <span>📊 2. ముఖ్య విశ్లేషణ & అంశాలు (Core Body Points):</span>
              </h4>
              <ul class="list-disc pl-5 text-slate-800 space-y-1 text-justify leading-relaxed">
                {body_lis}
              </ul>
            </div>

            <!-- 3. Govt Steps -->
            <div class="bg-emerald-50/70 p-3 rounded-xl border border-emerald-200">
              <h4 class="font-black text-emerald-950 mb-1 flex items-center gap-1">
                <span>🏛️ 3. ప్రభుత్వ విధానాలు & చర్యలు (Government Initiatives):</span>
              </h4>
              <p class="text-slate-800 leading-relaxed text-justify">{ma['govt_steps']}</p>
            </div>

            <!-- 4. Conclusion -->
            <div class="bg-amber-50/70 p-3 rounded-xl border border-amber-200">
              <h4 class="font-black text-amber-950 mb-1 flex items-center gap-1">
                <span>🎯 4. ముగింపు & ముందున్న మార్గం (Way Forward & Conclusion):</span>
              </h4>
              <p class="text-slate-800 leading-relaxed text-justify">{ma['conclusion']}</p>
            </div>
          </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APPSC గ్రూప్-1 & గ్రూప్-2 మెయిన్స్ మోడల్ ఆన్సర్స్ బ్యాంక్ | Mains Handbook</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;500;600;700;800;900&display=swap">
  <style>
    body {{ font-family: 'Noto Sans Telugu', sans-serif; background: #f8fafc; color: #0f172a; }}
    @media print {{
      *, *::before, *::after {{ -webkit-print-color-adjust: exact !important; print-color-adjust: exact !important; color-adjust: exact !important; }}
      body {{ background: #fff !important; font-size: 10pt; color: #000 !important; }}
      .no-print {{ display: none !important; }}
      .page-break {{ page-break-before: always; }}
      .mains-card {{ break-inside: avoid; page-break-inside: avoid; }}
    }}
  </style>
</head>
<body class="p-3 sm:p-6">

  <!-- Action Bar -->
  <div class="no-print max-w-4xl mx-auto mb-5 flex justify-between items-center bg-white p-4 rounded-2xl shadow-sm border border-slate-200">
    <a href="/" class="text-xs font-bold bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition">← డ్యాష్‌బోర్డ్‌కు వెళ్ళు</a>
    <h1 class="text-sm sm:text-base font-black text-slate-900">✍️ మెయిన్స్ డిస్క్రిప్టివ్ మోడల్ ఆన్సర్స్ బ్యాంక్</h1>
    <button onclick="window.print()" class="bg-purple-600 hover:bg-purple-700 text-white font-bold text-xs px-4 py-2 rounded-xl shadow transition">🖨️ PDF గా సేవ్ / ప్రింట్</button>
  </div>

  <div class="max-w-4xl mx-auto bg-white rounded-3xl shadow-xl border border-slate-300 p-6 sm:p-10 space-y-8">
    <header class="border-b-4 border-slate-900 pb-5 text-center">
      <div class="inline-flex items-center gap-2 bg-gradient-to-r from-purple-600 to-indigo-700 text-white text-xs font-black px-3.5 py-1 rounded-full uppercase mb-2">
        🎯 APPSC గ్రూప్-1 & గ్రూప్-2 మెయిన్స్ స్పెషల్
      </div>
      <h1 class="text-2xl sm:text-4xl font-black text-slate-950 mb-2">మెయిన్స్ డిస్క్రిప్టివ్ మోడల్ ఆన్సర్స్ మాన్యువల్</h1>
      <p class="text-xs sm:text-sm font-bold text-slate-600">ప్రామాణిక 4-అంచెల విధానం (పరిచయం, ముఖ్య విశ్లేషణ, ప్రభుత్వ చర్యలు, ముగింపు) తో కూడిన మోడల్ సమాధానాలు</p>
    </header>

    <div class="space-y-6">
      {cards}
    </div>
  </div>
</body>
</html>"""
    return html

def render_omr_appsc_all_html(exam_type="group2"):
    from ap_history_data import get_appsc_exam_questions, APPSC_EXAM_TYPES

    exam_info = APPSC_EXAM_TYPES.get(exam_type, APPSC_EXAM_TYPES["group2"])
    questions = get_appsc_exam_questions(exam_type)
    total_q = len(questions)

    q_cards = ""
    for idx, q in enumerate(questions, 1):
        q_cards += f"""
        <div class="exam-q-item p-3 border-b border-slate-200 text-xs avoid-break">
          <div class="flex justify-between items-center mb-1 font-bold">
            <span class="bg-slate-900 text-white px-2 py-0.5 rounded text-[10px]">ప్రశ్న {idx}</span>
            <span class="text-slate-500 font-bold">{q.get('pyq_tag') or q.get('section_name') or 'APPSC'}</span>
          </div>
          <p class="font-bold text-slate-900 text-sm mb-2">{q['question']}</p>
          <div class="grid grid-cols-2 gap-1 font-medium text-slate-800">
            <div class="p-1 border rounded bg-slate-50"><b>A)</b> {q['option_a']}</div>
            <div class="p-1 border rounded bg-slate-50"><b>B)</b> {q['option_b']}</div>
            <div class="p-1 border rounded bg-slate-50"><b>C)</b> {q['option_c']}</div>
            <div class="p-1 border rounded bg-slate-50"><b>D)</b> {q['option_d']}</div>
          </div>
        </div>
        """

    key_rows = ""
    for idx, q in enumerate(questions, 1):
        key_rows += f"""
        <div class="p-1.5 border rounded text-[11px] font-bold text-center bg-white">
          <span class="text-slate-600">Q{idx}:</span> <span class="text-emerald-700 font-black">{q['correct_option']}</span>
        </div>
        """

    omr_bubbles = '<div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-2.5">'
    for idx in range(1, total_q + 1):
        omr_bubbles += f"""
        <div class="flex items-center justify-between p-1.5 border border-slate-300 rounded-lg text-xs font-bold bg-white">
          <span class="w-6 text-slate-700">{idx}.</span>
          <div class="flex items-center gap-1.5">
            <div class="omr-circle">A</div>
            <div class="omr-circle">B</div>
            <div class="omr-circle">C</div>
            <div class="omr-circle">D</div>
          </div>
        </div>
        """
    omr_bubbles += '</div>'

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{exam_info['title']} | ఆఫ్‌లైన్ OMR టెస్ట్ పేపర్</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+Telugu:wght@400;600;700;800;900&display=swap">
  <style>
    body {{ font-family: 'Noto Sans Telugu', sans-serif; background: #f8fafc; color: #000; }}
    .avoid-break {{ break-inside: avoid; page-break-inside: avoid; }}
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
    @media print {{
      .no-print {{ display: none !important; }}
      body {{ background: #fff !important; font-size: 9.5pt; }}
      .page-break {{ page-break-before: always; }}
    }}
  </style>
</head>
<body class="p-2 sm:p-4">

  <!-- Top Action Bar -->
  <div class="no-print max-w-5xl mx-auto mb-4 flex justify-between items-center bg-white p-3 rounded-xl border shadow-sm">
    <div class="flex gap-2">
      <a href="/omr_appsc_all?exam=group1" class="text-xs font-bold px-3 py-1.5 rounded-lg border {'bg-amber-600 text-white' if exam_type == 'group1' else 'bg-slate-100'}">గ్రూప్-1 (120 Qs)</a>
      <a href="/omr_appsc_all?exam=group2" class="text-xs font-bold px-3 py-1.5 rounded-lg border {'bg-amber-600 text-white' if exam_type == 'group2' else 'bg-slate-100'}">గ్రూప్-2 (150 Qs)</a>
      <a href="/omr_appsc_all?exam=group3" class="text-xs font-bold px-3 py-1.5 rounded-lg border {'bg-amber-600 text-white' if exam_type == 'group3' else 'bg-slate-100'}">గ్రూప్-3 పంచాయతీ (150 Qs)</a>
    </div>
    <button onclick="window.print()" class="bg-rose-600 hover:bg-rose-700 text-white font-bold text-xs px-4 py-2 rounded-lg shadow">🖨️ టెస్ట్ పేపర్ + OMR ప్రింట్</button>
  </div>

  <div class="max-w-5xl mx-auto bg-white p-6 sm:p-10 border rounded-2xl shadow-md space-y-6">
    <header class="border-b-2 border-slate-900 pb-4 text-center">
      <h1 class="text-xl sm:text-2xl font-black">{exam_info['title']}</h1>
      <p class="text-xs font-bold text-slate-600 mt-1">{exam_info['description']}</p>
      <div class="flex justify-between items-center mt-3 text-xs font-bold border-t pt-2">
        <span>మొత్తం ప్రశ్నలు: {total_q}</span>
        <span>వ్యవధి: {exam_info['duration_minutes']} నిమిషాలు</span>
        <span>నెగటివ్ మార్కులు: 1/3 ({exam_info['negative_marking']})</span>
      </div>
    </header>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
      {q_cards}
    </div>

    <!-- OMR Bubble Sheet -->
    <div class="page-break pt-6 border-t-2 border-slate-900 space-y-4">
      <div class="text-center">
        <h2 class="text-lg font-black">ఆంధ్రప్రదేశ్ పబ్లిక్ సర్వీస్ కమిషన్ • OMR సమాధాన పత్రం (Answer Sheet)</h2>
        <p class="text-xs text-slate-500">హాల్ టికెట్ నంబర్ & ప్రశ్నాపత్రం కోడ్‌ను సరైన బబుల్స్ లో బ్లూ/బ్లాక్ బాల్ పాయింట్ పెన్నుతో పూరించండి.</p>
      </div>

      <div class="my-4">
        {omr_bubbles}
      </div>
    </div>

    <!-- Answer Key -->
    <div class="page-break pt-6 border-t-2 border-slate-900 space-y-3">
      <div class="bg-slate-900 text-white p-3 rounded-lg flex justify-between items-center">
        <h3 class="font-black text-sm">🎯 అధికారిక ప్రశ్నాపత్రం ఆన్సర్ కీ (Official Answer Key)</h3>
        <span class="text-xs font-bold text-amber-300">{total_q} ప్రశ్నలకు సమాధానాలు</span>
      </div>
      <div class="grid grid-cols-5 sm:grid-cols-10 gap-1.5">
        {key_rows}
      </div>
    </div>
  </div>
</body>
</html>"""
    return html
