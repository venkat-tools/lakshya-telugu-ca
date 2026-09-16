# -*- coding: utf-8 -*-
"""
Interactive Subject-Wise Chapter Practice Tests Web View (/subject_tests).
Renders interactive CBT practice tests with instant scoring, timer, and Telugu explanations.
"""

from subject_tests_data import get_all_subject_tests

def render_subject_tests_html(selected_subject="history"):
    all_tests = get_all_subject_tests()
    current_test = all_tests.get(selected_subject, all_tests["history"])

    # Subject tabs
    nav_tabs = ""
    for k, v in all_tests.items():
        is_active = (k == selected_subject)
        active_cls = "bg-indigo-700 text-white font-black shadow-md border-indigo-700" if is_active else "bg-white text-slate-700 hover:bg-slate-100 border-slate-300 font-bold"
        nav_tabs += f"""
        <a href="/subject_tests?subject={k}" class="px-4 py-2.5 rounded-xl border text-xs sm:text-sm flex items-center gap-2 transition {active_cls}">
          <span>{v['icon']}</span>
          <span>{v['title'].split('(')[0].strip()}</span>
          <span class="text-[10px] px-2 py-0.5 rounded-full { 'bg-white/20 text-white' if is_active else 'bg-slate-100 text-slate-600' } font-black">{len(v['questions'])} Qs</span>
        </a>
        """

    # Build question cards
    q_cards = ""
    for idx, q in enumerate(current_test["questions"], 1):
        corr = q["correct"].upper()
        q_cards += f"""
        <div class="q-card bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4" data-correct="{corr}" id="q_{q['id']}">
          <div class="flex justify-between items-start gap-3">
            <span class="bg-indigo-100 text-indigo-900 font-black text-xs px-3 py-1 rounded-lg">ప్రశ్న {idx} / {len(current_test['questions'])}</span>
            <span class="text-[11px] font-bold text-slate-500">ID: {q['id']}</span>
          </div>
          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>
          
          <div class="options-grid grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <button type="button" onclick="selectOpt(this, '{q['id']}', 'A')" class="opt-btn text-left p-3 rounded-xl border border-slate-200 text-xs sm:text-sm font-semibold hover:border-indigo-500 hover:bg-indigo-50/40 transition flex items-start gap-2.5" data-opt="A">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-800 text-xs font-black flex items-center justify-center shrink-0 opt-badge">A</span>
              <span class="opt-text">{q['a']}</span>
            </button>
            <button type="button" onclick="selectOpt(this, '{q['id']}', 'B')" class="opt-btn text-left p-3 rounded-xl border border-slate-200 text-xs sm:text-sm font-semibold hover:border-indigo-500 hover:bg-indigo-50/40 transition flex items-start gap-2.5" data-opt="B">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-800 text-xs font-black flex items-center justify-center shrink-0 opt-badge">B</span>
              <span class="opt-text">{q['b']}</span>
            </button>
            <button type="button" onclick="selectOpt(this, '{q['id']}', 'C')" class="opt-btn text-left p-3 rounded-xl border border-slate-200 text-xs sm:text-sm font-semibold hover:border-indigo-500 hover:bg-indigo-50/40 transition flex items-start gap-2.5" data-opt="C">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-800 text-xs font-black flex items-center justify-center shrink-0 opt-badge">C</span>
              <span class="opt-text">{q['c']}</span>
            </button>
            <button type="button" onclick="selectOpt(this, '{q['id']}', 'D')" class="opt-btn text-left p-3 rounded-xl border border-slate-200 text-xs sm:text-sm font-semibold hover:border-indigo-500 hover:bg-indigo-50/40 transition flex items-start gap-2.5" data-opt="D">
              <span class="w-6 h-6 rounded-full bg-slate-100 text-slate-800 text-xs font-black flex items-center justify-center shrink-0 opt-badge">D</span>
              <span class="opt-text">{q['d']}</span>
            </button>
          </div>

          <div class="explanation-box hidden mt-3 p-3.5 bg-indigo-50 border border-indigo-200 rounded-xl text-xs space-y-1">
            <div class="font-black text-indigo-950 flex items-center gap-1.5">
              <span>💡 సమగ్ర సమాధాన వివరణ:</span>
              <span class="bg-indigo-600 text-white px-2 py-0.5 rounded text-[10px] font-black">సరైన ఆప్షన్: {corr}</span>
            </div>
            <p class="text-slate-700 leading-relaxed font-medium">{q['explanation']}</p>
          </div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{current_test['title']} - APPSC & TSPSC చాప్టర్ టెస్ట్స్</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Mandali&family=Suranna&family=Tiro+Telugu&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {{
      font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif;
    }}
    .opt-correct {{
      background-color: #ecfdf5 !important;
      border-color: #10b981 !important;
      color: #065f46 !important;
    }}
    .opt-correct .opt-badge {{
      background-color: #10b981 !important;
      color: #ffffff !important;
    }}
    .opt-wrong {{
      background-color: #fef2f2 !important;
      border-color: #ef4444 !important;
      color: #991b1b !important;
    }}
    .opt-wrong .opt-badge {{
      background-color: #ef4444 !important;
      color: #ffffff !important;
    }}
    @media print {{
      .no-print {{ display: none !important; }}
      .explanation-box {{ display: block !important; }}
      body {{ background: white; }}
    }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen pb-16">

  <!-- Top Sticky Navigation -->
  <header class="bg-slate-900 text-white sticky top-0 z-30 shadow-md no-print border-b border-slate-800">
    <div class="max-w-5xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/syllabus" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ & PDF హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>📝</span> <span>సబ్జెక్ట్ చాప్టర్ ప్రాక్టీస్ టెస్ట్స్</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="text-xs bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> టెస్ట్ ప్రింట్ / సేవ్
        </button>
        <div id="scoreBadge" class="bg-amber-400 text-slate-950 font-black text-xs px-3 py-1.5 rounded-lg">
          స్కోర్: 0 / {len(current_test['questions'])}
        </div>
      </div>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 py-6 space-y-6">

    <!-- Header Banner -->
    <div class="bg-gradient-to-r from-indigo-900 via-indigo-800 to-slate-900 text-white p-6 rounded-3xl shadow-lg space-y-3">
      <div class="flex flex-wrap items-center justify-between gap-2">
        <span class="bg-indigo-500/30 border border-indigo-400/30 text-indigo-200 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          🎯 APPSC & TSPSC గ్రూప్ 1 & 2 • 150 హై-యీల్డ్ MCQs ప్రాక్టీస్
        </span>
        <span class="text-xs text-indigo-300 font-bold">
          నెగెటివ్ మార్కింగ్: 0.33 | టైమర్: 30 నిమిషాలు
        </span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black">{current_test['title']}</h2>
      <p class="text-xs sm:text-sm text-indigo-200 leading-relaxed font-medium">{current_test['description']}</p>
    </div>

    <!-- Subject Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto pb-2 no-print">
      {nav_tabs}
    </div>

    <!-- Questions List -->
    <div class="space-y-4" id="questionsContainer">
      {q_cards}
    </div>

    <!-- Bottom Submit / Reset Bar -->
    <div class="sticky bottom-4 z-20 bg-slate-900/95 backdrop-blur-md text-white p-4 rounded-2xl shadow-2xl flex justify-between items-center border border-slate-800 no-print">
      <div>
        <div class="text-xs font-bold text-slate-400">ప్రస్తుత ఫలితం:</div>
        <div class="text-base sm:text-xl font-black text-amber-400" id="finalResultText">మొత్తం 30 ప్రశ్నలకు సమాధానాలు గుర్తించండి</div>
      </div>
      <div class="flex gap-2">
        <button onclick="revealAllAnswers()" class="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl text-xs sm:text-sm font-bold transition flex items-center gap-1.5">
          <i class="fa-solid fa-eye"></i> అన్ని సమాధానాలు చూపించు
        </button>
        <button onclick="location.reload()" class="px-3 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs sm:text-sm font-bold transition">
          <i class="fa-solid fa-rotate-right"></i> రీసెట్
        </button>
      </div>
    </div>

  </main>

  <script>
    let userAnswers = {{}};
    let totalQuestions = {len(current_test['questions'])};
    let score = 0;

    function selectOpt(btn, qId, chosenOpt) {{
      const card = document.getElementById('q_' + qId);
      if (!card) return;

      const correctOpt = card.getAttribute('data-correct');
      const allBtns = card.querySelectorAll('.opt-btn');

      // Disable further clicks on this card
      allBtns.forEach(b => {{
        b.classList.remove('opt-correct', 'opt-wrong');
        b.disabled = true;
      }});

      userAnswers[qId] = chosenOpt;

      if (chosenOpt === correctOpt) {{
        btn.classList.add('opt-correct');
      }} else {{
        btn.classList.add('opt-wrong');
        // highlight correct one
        allBtns.forEach(b => {{
          if (b.getAttribute('data-opt') === correctOpt) {{
            b.classList.add('opt-correct');
          }}
        }});
      }}

      // Show explanation
      const expBox = card.querySelector('.explanation-box');
      if (expBox) expBox.classList.remove('hidden');

      // Update score
      recalcScore();
    }}

    function recalcScore() {{
      let correctCount = 0;
      let attempted = Object.keys(userAnswers).length;
      document.querySelectorAll('.q-card').forEach(card => {{
        const qId = card.id.replace('q_', '');
        const corr = card.getAttribute('data-correct');
        if (userAnswers[qId] === corr) {{
          correctCount++;
        }}
      }});

      score = correctCount;
      document.getElementById('scoreBadge').innerText = `స్కోర్: ${{score}} / ${{totalQuestions}}`;
      document.getElementById('finalResultText').innerText = `పూర్తయినవి: ${{attempted}}/${{totalQuestions}} • సరైనవి: ${{score}} (శాతం: ${{Math.round((score/totalQuestions)*100)}}%)`;
    }}

    function revealAllAnswers() {{
      document.querySelectorAll('.q-card').forEach(card => {{
        const correctOpt = card.getAttribute('data-correct');
        const allBtns = card.querySelectorAll('.opt-btn');
        allBtns.forEach(b => {{
          b.disabled = true;
          if (b.getAttribute('data-opt') === correctOpt) {{
            b.classList.add('opt-correct');
          }}
        }});
        const expBox = card.querySelector('.explanation-box');
        if (expBox) expBox.classList.remove('hidden');
      }});
      recalcScore();
    }}
  </script>
</body>
</html>"""
    return html
