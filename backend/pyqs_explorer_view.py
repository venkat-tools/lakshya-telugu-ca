# -*- coding: utf-8 -*-
"""
Interactive Web View for APPSC & TSPSC PYQs Deep Explorer & Analytics (/pyqs_explorer).
Features multi-dimensional filters (Subject, Exam, Year), search, and interactive solution peeker.
"""

from pyqs_explorer_data import get_pyqs_explorer_data

def render_pyqs_explorer_html():
    data = get_pyqs_explorer_data()
    analytics = data["analytics"]
    questions = data["questions"]

    # Cutoffs table HTML
    cutoff_rows = ""
    for c in analytics["cutoffs"]:
        cutoff_rows += f"""
        <tr class="border-b border-slate-100 hover:bg-slate-50 transition text-xs sm:text-sm">
          <td class="p-3 font-bold text-slate-900">{c['exam']}</td>
          <td class="p-3 font-mono font-bold text-slate-700">{c['total_marks']}</td>
          <td class="p-3 font-mono font-bold text-rose-600">{c['negative_mark']}</td>
          <td class="p-3 font-black text-emerald-700 bg-emerald-50/50">{c['open_cutoff']}</td>
          <td class="p-3 text-slate-600 text-xs">{c['notes']}</td>
        </tr>
        """

    # Subject weightage cards
    dist_cards = ""
    for sd in analytics["subject_distribution"]:
        dist_cards += f"""
        <div class="p-3 bg-white border border-slate-200 rounded-xl shadow-2xs text-center space-y-1">
          <span class="text-xs font-bold text-slate-500 block truncate">{sd['subject']}</span>
          <span class="text-base sm:text-lg font-black text-indigo-950 block">{sd['count']} ప్రశ్నలు</span>
          <span class="text-[11px] font-black text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full inline-block">{sd['percentage']}</span>
        </div>
        """

    # Questions Cards HTML
    opt_letters = ["A", "B", "C", "D"]
    q_cards = ""
    for idx, q in enumerate(questions, 1):
        corr = q["key"].upper()
        opts_html = ""
        for opt_idx, opt_text in enumerate(q["options"]):
            letter = opt_letters[opt_idx]
            opts_html += f"""
            <div class="pyq-opt p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm flex items-start gap-2.5 font-medium cursor-pointer hover:bg-indigo-50 transition" onclick="checkPyqOpt(this, '{letter}', '{corr}')">
              <span class="opt-letter w-6 h-6 rounded-full bg-slate-200 text-slate-800 text-xs font-black flex items-center justify-center shrink-0">{letter}</span>
              <span class="text-slate-800 leading-relaxed">{opt_text}</span>
            </div>
            """

        q_cards += f"""
        <article class="pyq-card bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4" data-subject="{q['subject']}" data-exam="{q['exam']}" data-year="{q['year']}" data-query="{q['question'].lower()} {q['explanation'].lower()}">
          <div class="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-2.5">
            <div class="flex items-center gap-2">
              <span class="bg-indigo-600 text-white font-black text-xs px-2.5 py-0.5 rounded-md">ప్రశ్న {idx}</span>
              <span class="bg-slate-100 text-slate-800 font-bold text-xs px-2.5 py-0.5 rounded-md border border-slate-200">{q['subject']}</span>
            </div>
            <div class="flex items-center gap-2">
              <span class="bg-amber-100 text-amber-900 font-black text-[11px] px-2 py-0.5 rounded-md">{q['exam']} ({q['year']})</span>
            </div>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed whitespace-pre-line">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex flex-wrap items-center justify-between gap-2">
            <button type="button" onclick="toggleSolution('pyq_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>అధికారిక కీ & వివరణ చూడండి</span>
            </button>
            <span class="text-[11px] font-semibold text-slate-500 italic">మూలం: {q['source']}</span>
          </div>

          <div id="sol_pyq_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
            <div class="flex items-center gap-2 font-black text-emerald-900">
              <span class="px-2 py-0.5 bg-emerald-600 text-white rounded text-xs">అధికారిక కీ: ఆప్షన్ {corr}</span>
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
  <title>APPSC & TSPSC గత ప్రశ్నల (PYQs) డీప్ ఎక్స్‌ప్లోరర్ - లక్ష్య</title>
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
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🔍</span> <span>APPSC & TSPSC గత ప్రశ్నల (PYQs) డీప్ ఎక్స్‌ప్లోరర్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/appsc_tspsc_solved_pyqs_master.pdf" download="appsc_tspsc_solved_pyqs_master.pdf" class="text-xs bg-amber-400 hover:bg-amber-300 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-file-pdf"></i> సాల్వ్డ్ PYQs PDF
        </a>
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Banner & Cutoffs Analytics -->
    <div class="bg-gradient-to-r from-slate-950 via-indigo-950 to-slate-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-4 border border-indigo-900/40 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-indigo-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          అధికారిక పరీక్షల విశ్లేషణ (2017–2024)
        </span>
        <span class="text-xs text-indigo-200 font-medium">అధికారిక కీలతో సమగ్ర సమాధానాలు</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">గత ప్రశ్నల లోతైన విశ్లేషణ & కటాఫ్ అనలిటిక్స్</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        APPSC గ్రూప్-2 (2024, 2019), TSPSC గ్రూప్-1 మరియు పోలీస్ SI పరీక్షల్లో వచ్చిన ప్రశ్నలు, కటాఫ్‌లు మరియు నెగెటివ్ మార్కింగ్ ప్రభావంపై సంపూర్ణ పరిశీలన.
      </p>

      <!-- Cutoffs Table Card -->
      <div class="bg-slate-900/90 border border-slate-700/80 rounded-2xl overflow-hidden p-4 space-y-2">
        <h4 class="text-xs sm:text-sm font-black text-amber-300 flex items-center gap-2">
          <i class="fa-solid fa-trophy text-amber-400"></i> అధికారిక ప్రిలిమ్స్ కటాఫ్ వివరాలు (Cutoff Trends):
        </h4>
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="text-slate-400 text-[11px] uppercase border-b border-slate-700">
                <th class="p-2.5">పరీక్ష పేరు</th>
                <th class="p-2.5">మొత్తం మార్కులు</th>
                <th class="p-2.5">నెగెటివ్ మార్క్</th>
                <th class="p-2.5">ఓపెన్ కటాఫ్</th>
                <th class="p-2.5">కీలక పరిశీలనలు</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-800">
              {cutoff_rows}
            </tbody>
          </table>
        </div>
      </div>

      <!-- Subject Weightage Grid -->
      <div class="space-y-2 pt-1">
        <h4 class="text-xs font-black text-slate-300 uppercase tracking-wider">సబ్జెక్ట్-వైజ్ ప్రశ్నల వెయిటేజ్:</h4>
        <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 text-slate-900">
          {dist_cards}
        </div>
      </div>
    </div>

    <!-- Multi-Dimensional Filter Bar (no-print) -->
    <div class="no-print bg-white border border-slate-200 p-4 sm:p-5 rounded-2xl shadow-sm space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-100 pb-3">
        <h3 class="text-sm sm:text-base font-black text-slate-900 flex items-center gap-2">
          <i class="fa-solid fa-filter text-indigo-600"></i>
          <span>మల్టీ-ఫిల్టర్ ఎక్స్‌ప్లోరర్:</span>
        </h3>
        <span id="matchCountBadge" class="text-xs font-bold bg-indigo-50 text-indigo-900 px-3 py-1 rounded-full border border-indigo-200">
          {len(questions)} ప్రశ్నలు అందుబాటులో ఉన్నాయి
        </span>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 text-xs sm:text-sm font-semibold">
        <!-- Subject Filter -->
        <div>
          <label class="block text-slate-500 text-[11px] font-bold uppercase mb-1">సబ్జెక్ట్ ఎంచుకోండి:</label>
          <select id="subjectFilter" onchange="filterPyqs()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none">
            <option value="all">అన్ని సబ్జెక్టులు</option>
            <option value="భారతీయ సమాజం">భారతీయ సమాజం</option>
            <option value="భారత & AP చరిత్ర">భారత & AP చరిత్ర</option>
            <option value="భౌగోళికం & పర్యావరణం">భౌగోళికం & పర్యావరణం</option>
            <option value="పాలిటీ & రాజ్యాంగం">పాలిటీ & రాజ్యాంగం</option>
            <option value="మెంటల్ ఎబిలిటీ">మెంటల్ ఎబిలిటీ</option>
            <option value="కరెంట్ అఫైర్స్ & ఎకానమీ">కరెంట్ అఫైర్స్ & ఎకానమీ</option>
          </select>
        </div>

        <!-- Exam Filter -->
        <div>
          <label class="block text-slate-500 text-[11px] font-bold uppercase mb-1">పరీక్ష ఎంచుకోండి:</label>
          <select id="examFilter" onchange="filterPyqs()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none">
            <option value="all">అన్ని పరీక్షలు</option>
            <option value="APPSC Group 2">APPSC గ్రూప్-2</option>
            <option value="TSPSC Group 1">TSPSC గ్రూప్-1</option>
            <option value="AP Police SI">AP పోలీస్ SI</option>
          </select>
        </div>

        <!-- Year Filter -->
        <div>
          <label class="block text-slate-500 text-[11px] font-bold uppercase mb-1">సంవత్సరం:</label>
          <select id="yearFilter" onchange="filterPyqs()" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none">
            <option value="all">అన్ని సంవత్సరాలు</option>
            <option value="2024">2024</option>
            <option value="2023">2023</option>
            <option value="2019">2019</option>
          </select>
        </div>

        <!-- Keyword Search -->
        <div>
          <label class="block text-slate-500 text-[11px] font-bold uppercase mb-1">కీవర్డ్ సెర్చ్:</label>
          <input type="text" id="keywordFilter" onkeyup="filterPyqs()" placeholder="సెర్చ్ చేయండి (ఉదా: సంస్కృతీకరణ, నదులు)..." class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:outline-none text-xs">
        </div>
      </div>
    </div>

    <!-- Questions Grid -->
    <div id="questionsContainer" class="space-y-4">
      {q_cards}
    </div>

  </main>

  <script>
    function toggleSolution(id) {{
      const el = document.getElementById('sol_' + id);
      if (el) {{
        el.classList.toggle('hidden');
      }}
    }}

    function checkPyqOpt(el, userLetter, correctLetter) {{
      const parent = el.closest('.pyq-card');
      const allOpts = parent.querySelectorAll('.pyq-opt');
      allOpts.forEach(opt => {{
        opt.classList.remove('bg-emerald-100', 'border-emerald-400', 'bg-rose-100', 'border-rose-400');
      }});

      if (userLetter === correctLetter) {{
        el.classList.add('bg-emerald-100', 'border-emerald-400');
      }} else {{
        el.classList.add('bg-rose-100', 'border-rose-400');
        // highlight correct one
        allOpts.forEach(opt => {{
          if (opt.querySelector('.opt-letter').innerText.trim() === correctLetter) {{
            opt.classList.add('bg-emerald-100', 'border-emerald-400');
          }}
        }});
      }}
    }}

    function filterPyqs() {{
      const subj = document.getElementById('subjectFilter').value;
      const exam = document.getElementById('examFilter').value;
      const yr = document.getElementById('yearFilter').value;
      const qry = document.getElementById('keywordFilter').value.toLowerCase().trim();

      const cards = document.querySelectorAll('.pyq-card');
      let visible = 0;

      cards.forEach(card => {{
        const cSubj = card.getAttribute('data-subject');
        const cExam = card.getAttribute('data-exam');
        const cYr = card.getAttribute('data-year');
        const cQry = card.getAttribute('data-query') || '';

        const subjMatch = (subj === 'all' || cSubj === subj);
        const examMatch = (exam === 'all' || cExam === exam);
        const yrMatch = (yr === 'all' || cYr === yr);
        const qryMatch = (!qry || cQry.includes(qry));

        if (subjMatch && examMatch && yrMatch && qryMatch) {{
          card.style.display = '';
          visible++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      const badge = document.getElementById('matchCountBadge');
      if (badge) {{
        badge.innerText = visible + ' ప్రశ్నలు సరిపోలాయి';
      }}
    }}
  </script>
</body>
</html>"""

    return html
