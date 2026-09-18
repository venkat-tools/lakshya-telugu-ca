# -*- coding: utf-8 -*-
"""
Interactive Web View for Daily Telugu Editorial Analysis & Mains Answer Studio (/editorials_hub).
"""

from editorials_data import get_all_editorials

def render_editorials_hub_html(selected_paper="all"):
    all_ed = get_all_editorials()
    if selected_paper != "all":
        display_ed = [e for e in all_ed if selected_paper.lower() in e["newspaper"].lower()]
    else:
        display_ed = all_ed

    ed_cards = ""
    for idx, ed in enumerate(display_ed, 1):
        prelims_items = "".join([f'<li class="flex items-start gap-2"><span class="text-rose-500 font-bold shrink-0">✦</span><span>{item}</span></li>' for item in ed["prelims_facts"]])
        pros_items = "".join([f'<li class="flex items-start gap-2"><span class="text-emerald-600 font-bold shrink-0">✔</span><span>{p}</span></li>' for p in ed["mains_dimensions"]["pros"]])
        cons_items = "".join([f'<li class="flex items-start gap-2"><span class="text-amber-600 font-bold shrink-0">✖</span><span>{c}</span></li>' for c in ed["mains_dimensions"]["cons"]])
        terms_items = "".join([f'<div class="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"><strong class="text-indigo-900 block mb-0.5">{t["term"]}:</strong><span class="text-slate-700">{t["meaning"]}</span></div>' for t in ed["key_terms"]])

        # Format Model Answer if available
        ma = ed.get("model_answer")
        ma_html = ""
        if ma:
            body_pts_html = "".join([f'<li class="mb-2">{pt}</li>' for pt in ma["structure"]["body_points"]])
            ma_html = f"""
            <!-- Model Answer Accordion Box -->
            <div class="mt-4 pt-4 border-t border-amber-200/80">
              <button onclick="toggleModelAnswer('{ed['id']}')" class="w-full bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-600 hover:to-amber-700 text-slate-950 font-black text-xs sm:text-sm py-2.5 px-4 rounded-xl flex items-center justify-between transition shadow-xs cursor-pointer">
                <span class="flex items-center gap-2">
                  <i class="fa-solid fa-graduation-cap"></i>
                  <span>🎯 ప్రామాణిక మెయిన్స్ మోడల్ సమాధానం (Model Answer - {ma.get('marks', '10M')})</span>
                </span>
                <span id="ma-icon-{ed['id']}" class="text-xs bg-amber-200/80 px-2 py-0.5 rounded font-bold">చూడండి ▼</span>
              </button>

              <div id="ma-content-{ed['id']}" class="hidden mt-3 bg-amber-50/70 border border-amber-300/80 rounded-2xl p-5 space-y-4 text-xs sm:text-sm text-slate-800 leading-relaxed shadow-inner">
                <div class="flex justify-between items-center pb-2 border-b border-amber-200 text-xs font-bold text-amber-900">
                  <span>📖 {ma.get('title', 'మోడల్ ఆన్సర్ ఫ్రేమ్‌వర్క్')}</span>
                  <span>పదాల పరిమితి: {ma.get('word_count', '180')}</span>
                </div>
                <div>
                  <strong class="text-amber-950 block mb-1 font-black">1. పీఠిక / పరిచయం (Introduction):</strong>
                  <p class="text-slate-700 pl-2 border-l-2 border-amber-400">{ma['structure']['introduction']}</p>
                </div>
                <div>
                  <strong class="text-amber-950 block mb-1 font-black">2. ప్రధాన ముఖ్యాంశాలు (Body of the Answer):</strong>
                  <ul class="space-y-2 list-disc list-inside text-slate-800 pl-1">{body_pts_html}</ul>
                </div>
                <div>
                  <strong class="text-amber-950 block mb-1 font-black">3. ముగింపు & ముందుచూపు (Conclusion & Way Forward):</strong>
                  <p class="text-slate-700 pl-2 border-l-2 border-emerald-500 bg-emerald-50/50 p-2.5 rounded-r-xl">{ma['structure']['conclusion']}</p>
                </div>
              </div>
            </div>
            """

        ed_cards += f"""
        <article class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6" id="{ed['id']}">
          <!-- Top Tag Bar -->
          <div class="flex flex-wrap justify-between items-center gap-3 border-b border-slate-100 pb-4">
            <div class="flex items-center gap-2.5">
              <span class="px-3 py-1 bg-rose-100 text-rose-800 text-xs font-black rounded-lg">{ed['newspaper']}</span>
              <span class="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-lg">{ed['category']}</span>
            </div>
            <span class="text-xs text-slate-500 font-semibold">తేదీ: {ed['date']}</span>
          </div>

          <!-- Title & Context -->
          <div>
            <h3 class="text-lg sm:text-2xl font-black text-slate-900 leading-snug">{ed['title']}</h3>
            <p class="text-xs sm:text-sm text-slate-600 mt-2 leading-relaxed bg-slate-50 p-4 rounded-xl border border-slate-200/80">
              <strong class="text-slate-900 font-bold">📌 నేపథ్యం (Context):</strong> {ed['context']}
            </p>
          </div>

          <!-- 2-Column Split: Prelims Facts & Mains Dimensions -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
            <!-- Prelims Highlights -->
            <div class="bg-gradient-to-br from-rose-50/70 to-orange-50/50 border border-rose-200/80 rounded-2xl p-5 space-y-3">
              <h4 class="font-black text-rose-950 text-sm flex items-center gap-2">
                <span>🎯</span> <span>ప్రిలిమ్స్ హై-యీల్డ్ ఫ్యాక్ట్స్ (Prelims Pointers)</span>
              </h4>
              <ul class="space-y-2 text-xs sm:text-sm text-slate-800 leading-relaxed">
                {prelims_items}
              </ul>
            </div>

            <!-- Mains Dimensions -->
            <div class="bg-gradient-to-br from-blue-50/70 to-indigo-50/50 border border-blue-200/80 rounded-2xl p-5 space-y-3">
              <h4 class="font-black text-blue-950 text-sm flex items-center gap-2">
                <span>✍️</span> <span>మెయిన్స్ విశ్లేషణ (Core Arguments)</span>
              </h4>
              <div class="space-y-2.5 text-xs sm:text-sm text-slate-800">
                <div>
                  <strong class="text-emerald-900 block mb-1 font-bold">అనుకూల అంశాలు (Pros & Advantages):</strong>
                  <ul class="space-y-1 pl-1">{pros_items}</ul>
                </div>
                <div class="pt-1">
                  <strong class="text-amber-900 block mb-1 font-bold">సవాళ్లు / ఆందోళనలు (Challenges):</strong>
                  <ul class="space-y-1 pl-1">{cons_items}</ul>
                </div>
                <div class="pt-2 border-t border-blue-200/60 text-[11px] text-indigo-950">
                  <strong class="font-bold">ముగింపు & పరిష్కార మార్గం:</strong> {ed['mains_dimensions']['way_forward']}
                </div>
              </div>
            </div>
          </div>

          <!-- Key Vocabulary & Exam Definitions -->
          <div class="space-y-2.5">
            <h4 class="text-xs font-extrabold uppercase tracking-wider text-slate-500">కీలక సంపాదకీయ పదకోశం (Key Vocabulary)</h4>
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
              {terms_items}
            </div>
          </div>

          <!-- Practice Question & Interactive Answer Pad -->
          <div class="p-5 bg-gradient-to-br from-amber-50 to-orange-50/40 border border-amber-300 rounded-2xl space-y-4">
            <div class="space-y-1.5">
              <span class="text-[10px] font-black uppercase tracking-wider bg-amber-500 text-slate-950 px-2 py-0.5 rounded">డైలీ మెయిన్స్ ప్రశ్న (Question of the Day)</span>
              <p class="text-xs sm:text-sm font-bold text-slate-900 leading-relaxed">{ed['practice_question']}</p>
            </div>

            <!-- Interactive Answer Studio / Notepad Toggle -->
            <div>
              <div class="flex flex-wrap items-center justify-between gap-2 mb-2">
                <button onclick="toggleNotepad('{ed['id']}')" class="text-xs font-bold text-indigo-700 hover:text-indigo-900 flex items-center gap-1.5 bg-indigo-50 border border-indigo-200 px-3 py-1.5 rounded-lg transition cursor-pointer">
                  <i class="fa-solid fa-pen-fancy"></i>
                  <span>✍️ ఇక్కడే ప్రాక్టీస్ ఆన్సర్ రాయండి (15-Min Timer)</span>
                </button>
              </div>

              <!-- Collapsible Notepad -->
              <div id="notepad-{ed['id']}" class="hidden space-y-3 bg-white p-4 rounded-xl border border-amber-200 shadow-xs">
                <div class="flex justify-between items-center text-xs font-bold text-slate-600 pb-2 border-b border-slate-100">
                  <div class="flex items-center gap-2">
                    <span>⏱️ టైమర్:</span>
                    <span id="timer-{ed['id']}" class="text-rose-600 font-mono font-black text-sm">15:00</span>
                    <button onclick="startTimer('{ed['id']}')" class="px-2 py-0.5 bg-emerald-100 text-emerald-800 rounded hover:bg-emerald-200 text-[11px]">ప్రారంభించు</button>
                    <button onclick="pauseTimer('{ed['id']}')" class="px-2 py-0.5 bg-amber-100 text-amber-800 rounded hover:bg-amber-200 text-[11px]">ఆపు</button>
                  </div>
                  <div>
                    <span>పదాలు:</span> <span id="word-count-{ed['id']}" class="text-blue-600 font-mono font-bold">0 / 200</span>
                  </div>
                </div>

                <textarea 
                  id="textarea-{ed['id']}" 
                  oninput="updateWordCount('{ed['id']}')"
                  rows="6" 
                  placeholder="మీ సమాధానాన్ని ఇక్కడ తెలుగు లేదా ఇంగ్లీషులో టైప్ చేయండి (పీఠిక, ముఖ్య పాయింట్లు, ముగింపు)..."
                  class="w-full text-xs sm:text-sm p-3 border border-slate-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-500 font-normal leading-relaxed text-slate-800 bg-slate-50/50"
                ></textarea>

                <div class="flex justify-between items-center text-[11px] text-slate-500">
                  <span>💡 చిట్కా: పీఠికతో మొదలుపెట్టి 4-5 బుల్లెట్ పాయింట్లతో ముగించండి.</span>
                  <button onclick="saveAnswerDraft('{ed['id']}')" class="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded-lg transition">డ్రాఫ్ట్ సేవ్ చేయి</button>
                </div>
              </div>
            </div>

            <!-- Model Answer Accordion -->
            {ma_html}
          </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>డైలీ తెలుగు ఎడిటోరియల్ విశ్లేషణ & మెయిన్స్ ఆన్సర్ స్టూడియో - లక్ష్య పోటీ పరీక్షలు</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Mandali&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif; }}
    @media print {{
      .no-print {{ display: none !important; }}
      body {{ background: white; }}
    }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen pb-16">

  <!-- Top Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-30 shadow-md no-print border-b border-slate-800">
    <div class="max-w-6xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> హోమ్‌పేజీ
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>📰</span> <span>డైలీ తెలుగు ఎడిటోరియల్ విశ్లేషణ & మెయిన్స్ స్టూడియో</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5 cursor-pointer">
          <i class="fa-solid fa-print"></i> ప్రింట్ నోట్స్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-6xl mx-auto px-4 py-6 space-y-6">

    <!-- Hero Announcement -->
    <div class="bg-gradient-to-r from-red-950 via-slate-900 to-rose-950 text-white p-6 sm:p-7 rounded-3xl shadow-xl space-y-2 border border-rose-900/50">
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-rose-600 text-white">
          100% EXAM-ORIENTED
        </span>
        <span class="text-xs text-rose-300 font-semibold">రాజకీయాలు లేని స్వచ్ఛమైన పరీక్షా విశ్లేషణ & మోడల్ సమాధానాలు</span>
      </div>
      <h2 class="text-xl sm:text-2xl font-black text-white">ప్రధాన దినపత్రికల సంపాదకీయాల పరీక్షా సారాంశం</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
        ఈనాడు, సాక్షి, ది హిందూ పత్రికలలో ప్రచురితమయ్యే సంపాదకీయాల నుండి ప్రిలిమ్స్ ఫ్యాక్ట్స్, మెయిన్స్ పాయింట్లు మరియు ప్రతి ప్రశ్నకు పూర్తి స్థాయి మోడల్ సమాధానాలు.
      </p>
    </div>

    <!-- Newspaper Filter Bar -->
    <div class="flex flex-wrap items-center gap-2 no-print">
      <a href="/editorials_hub" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition {'bg-slate-900 text-white border-slate-900 shadow-sm' if selected_paper == 'all' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300'}">
        🌟 అన్ని సంపాదకీయాలు ({len(all_ed)})
      </a>
      <a href="/editorials_hub?paper=eenadu" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition {'bg-slate-900 text-white border-slate-900 shadow-sm' if selected_paper == 'eenadu' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300'}">
        📰 ఈనాడు సంపాదకీయం
      </a>
      <a href="/editorials_hub?paper=sakshi" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition {'bg-slate-900 text-white border-slate-900 shadow-sm' if selected_paper == 'sakshi' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300'}">
        📰 సాక్షి ఎడిటోరియల్
      </a>
      <a href="/editorials_hub?paper=hindu" class="px-4 py-2 rounded-xl text-xs sm:text-sm font-bold border transition {'bg-slate-900 text-white border-slate-900 shadow-sm' if selected_paper == 'hindu' else 'bg-white text-slate-700 hover:bg-slate-100 border-slate-300'}">
        📰 ది హిందూ (Telugu Crux)
      </a>
    </div>

    <!-- Editorial Cards Stream -->
    <div class="space-y-6">
      {ed_cards}
    </div>

  </main>

  <script>
    // Accordion Toggle for Model Answer
    function toggleModelAnswer(id) {{
      const box = document.getElementById('ma-content-' + id);
      const icon = document.getElementById('ma-icon-' + id);
      if (box.classList.contains('hidden')) {{
        box.classList.remove('hidden');
        icon.innerText = 'దాచు ▲';
      }} else {{
        box.classList.add('hidden');
        icon.innerText = 'చూడండి ▼';
      }}
    }}

    // Notepad Toggle
    function toggleNotepad(id) {{
      const pad = document.getElementById('notepad-' + id);
      pad.classList.toggle('hidden');
    }}

    // Word Count Tracker
    function updateWordCount(id) {{
      const ta = document.getElementById('textarea-' + id);
      const counter = document.getElementById('word-count-' + id);
      const text = ta.value.trim();
      const words = text ? text.split(' ').filter(Boolean).length : 0;
      counter.innerText = words + ' / 200';
      if (words > 200) {{
        counter.className = 'text-rose-600 font-mono font-black';
      }} else {{
        counter.className = 'text-blue-600 font-mono font-bold';
      }}
    }}

    // Timer Implementation
    const timers = {{}};
    function startTimer(id) {{
      if (timers[id] && timers[id].interval) return;
      let timeLeft = timers[id] ? timers[id].timeLeft : 15 * 60;
      const el = document.getElementById('timer-' + id);
      
      timers[id] = {{
        timeLeft: timeLeft,
        interval: setInterval(() => {{
          timeLeft--;
          timers[id].timeLeft = timeLeft;
          if (timeLeft <= 0) {{
            clearInterval(timers[id].interval);
            timers[id].interval = null;
            el.innerText = 'సమయం ముగిసింది!';
            alert('⏰ 15 నిమిషాల సమయం ముగిసింది! మీ సమాధానాన్ని మోడల్ సమాధానంతో సరిపోల్చుకోండి.');
            return;
          }}
          const m = Math.floor(timeLeft / 60);
          const s = timeLeft % 60;
          el.innerText = (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
        }}, 1000)
      }};
    }}

    function pauseTimer(id) {{
      if (timers[id] && timers[id].interval) {{
        clearInterval(timers[id].interval);
        timers[id].interval = null;
      }}
    }}

    function saveAnswerDraft(id) {{
      const ta = document.getElementById('textarea-' + id);
      localStorage.setItem('mains_draft_' + id, ta.value);
      alert('✅ మీ సమాధానం బ్రౌజర్‌లో సేవ్ చేయబడింది!');
    }}

    // Restore drafts on load
    window.addEventListener('DOMContentLoaded', () => {{
      document.querySelectorAll('textarea').forEach(ta => {{
        const id = ta.id.replace('textarea-', '');
        const saved = localStorage.getItem('mains_draft_' + id);
        if (saved) {{
          ta.value = saved;
          updateWordCount(id);
        }}
      }});
    }});
  </script>
</body>
</html>
"""
    return html
