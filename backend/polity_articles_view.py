# -*- coding: utf-8 -*-
"""
Interactive Web View for Indian Polity Articles Fast-Search Directory (/polity_articles).
Covers Articles 1 to 395 categorized with Telugu explanations, search filters, and MCQs.
"""

from polity_articles_data import get_polity_articles_data

def render_polity_articles_html():
    data = get_polity_articles_data()
    parts = data["parts"]
    mcqs = data.get("mcqs", [])

    # Generate Parts & Articles HTML
    parts_html = ""
    for p_idx, part in enumerate(parts, 1):
        articles_html = ""
        for art in part["key_articles"]:
            articles_html += f"""
            <div class="article-card p-4 sm:p-5 bg-white border border-slate-200 rounded-2xl shadow-2xs hover:shadow-md transition space-y-2" data-article="{art['art'].lower()}" data-text="{art['title'].lower()} {art['desc'].lower()}">
              <div class="flex items-center justify-between gap-2 border-b border-slate-100 pb-2">
                <span class="px-2.5 py-1 bg-amber-500/10 text-amber-800 text-xs sm:text-sm font-black rounded-lg border border-amber-500/20 font-mono">
                  🏛️ {art['art']}
                </span>
                <span class="text-[11px] font-bold text-slate-500">{part['part']}</span>
              </div>
              <h4 class="font-black text-slate-900 text-sm sm:text-base leading-snug">{art['title']}</h4>
              <p class="text-xs sm:text-sm text-slate-700 leading-relaxed font-medium">{art['desc']}</p>
            </div>
            """

        parts_html += f"""
        <div class="part-section space-y-4 pt-2" id="part-{p_idx}">
          <div class="p-4 bg-gradient-to-r from-slate-900 to-indigo-950 text-white rounded-2xl shadow-sm flex flex-wrap items-center justify-between gap-3">
            <div>
              <span class="text-amber-400 text-xs font-black uppercase tracking-wider">{part['part']}</span>
              <h3 class="text-base sm:text-lg font-black text-white">{part['title']}</h3>
            </div>
            <span class="px-3 py-1 bg-white/10 rounded-full text-xs font-bold text-slate-200 border border-white/10">
              {part['articles_range']}
            </span>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
            {articles_html}
          </div>
        </div>
        """

    # Generate MCQs HTML
    mcq_cards = ""
    opt_letters = ["A", "B", "C", "D"]
    for idx, q in enumerate(mcqs, 1):
        corr = q["key"].upper()
        opts_html = ""
        for opt_idx, opt_text in enumerate(q["options"]):
            letter = opt_letters[opt_idx]
            opts_html += f"""
            <div class="p-3 bg-slate-50 border border-slate-200 rounded-xl text-xs sm:text-sm flex items-start gap-2.5 font-medium">
              <span class="w-6 h-6 rounded-full bg-slate-200 text-slate-800 text-xs font-black flex items-center justify-center shrink-0">{letter}</span>
              <span class="text-slate-800 leading-relaxed">{opt_text}</span>
            </div>
            """

        mcq_cards += f"""
        <article class="bg-white border border-slate-200 rounded-2xl p-5 sm:p-6 shadow-sm space-y-4">
          <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-2.5">
            <span class="bg-amber-100 text-amber-900 font-black text-xs px-2.5 py-0.5 rounded-md">ప్రశ్న {idx}</span>
            <span class="bg-slate-100 text-slate-700 font-bold text-[11px] px-2 py-0.5 rounded-md">🏛️ {q.get('exam_tag', 'APPSC/TSPSC పాలిటీ')}</span>
          </div>

          <h3 class="text-sm sm:text-base font-black text-slate-900 leading-relaxed">{q['question']}</h3>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
            {opts_html}
          </div>

          <div class="pt-2 flex items-center justify-between">
            <button type="button" onclick="toggleSolution('art_{q['id']}')" class="text-xs bg-slate-100 hover:bg-slate-200 text-slate-800 font-bold px-3.5 py-1.5 rounded-lg border border-slate-300 transition flex items-center gap-1.5">
              <i class="fa-solid fa-lightbulb text-amber-500"></i>
              <span>సమాధానం & వివరణ చూడండి</span>
            </button>
            <span class="text-xs font-bold text-slate-400">అధికారిక కీ</span>
          </div>

          <div id="sol_art_{q['id']}" class="solution-box hidden mt-3 p-4 bg-emerald-50/70 border border-emerald-200 rounded-xl space-y-1.5 text-xs sm:text-sm">
            <div class="flex items-center gap-2 font-black text-emerald-900">
              <span class="px-2 py-0.5 bg-emerald-600 text-white rounded text-xs">సరైన సమాధానం: ఆప్షన్ {corr}</span>
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
  <title>భారత రాజ్యాంగ ఆర్టికల్స్ (1-395) మాస్టర్ గైడ్ & డైరెక్టరీ - లక్ష్య</title>
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
          <span>🏛️</span> <span>భారత రాజ్యాంగ ఆర్టికల్స్ (1-395) మాస్టర్ డైరెక్టరీ</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <a href="/pdfs/indian_polity_articles_master_guide.pdf" download="indian_polity_articles_master_guide.pdf" class="text-xs bg-amber-400 hover:bg-amber-300 text-slate-950 font-black px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5 shadow-sm">
          <i class="fa-solid fa-file-pdf"></i> మాస్టర్ PDF డౌన్‌లోడ్
        </a>
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
          <i class="fa-solid fa-print"></i> ప్రింట్
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 space-y-8">

    <!-- Hero Banner -->
    <div class="bg-gradient-to-r from-slate-950 via-amber-950/70 to-slate-950 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3 border border-amber-900/40 relative overflow-hidden">
      <div class="flex flex-wrap items-center justify-between gap-3">
        <span class="bg-amber-400 text-slate-950 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
          ఇండియన్ పాలిటీ హై-ఈల్డ్ కోర్ (Polity Core)
        </span>
        <span class="text-xs text-amber-200 font-medium">ఆర్టికల్ 1 నుండి 395 వరకు సమగ్ర వివరణ</span>
      </div>
      <h2 class="text-xl sm:text-3xl font-black text-white">భారత రాజ్యాంగం – సమగ్ర ఆర్టికల్స్ ఫాస్ట్-సెర్చ్ రివిజన్ హబ్</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-4xl leading-relaxed">
        APPSC Group 1, Group 2, TSPSC, UPSC, SI/Constable మరియు డిప్యూటీ కలెక్టర్ పరీక్షలకు అవసరమైన అన్ని ముఖ్యమైన రాజ్యాంగ ఆర్టికల్స్, వాటి అంతరార్థాలు, తెలుగు తాత్పర్యం మరియు సాధన ప్రశ్నలు.
      </p>

      <!-- Search & Filter Controls (no-print) -->
      <div class="no-print pt-3 flex flex-col sm:flex-row gap-3">
        <div class="relative flex-1">
          <i class="fa-solid fa-search absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-sm"></i>
          <input type="text" id="articleSearchInput" onkeyup="filterArticles()" placeholder="ఆర్టికల్ నంబర్ లేదా అంశం సెర్చ్ చేయండి (ఉదా: 21, ఉపరాష్ట్రపతి, ఆర్థిక సంఘం)..." class="w-full pl-10 pr-4 py-2.5 bg-slate-900/90 border border-amber-500/40 rounded-xl text-white placeholder-slate-400 text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-amber-400">
        </div>
        <button onclick="resetSearch()" class="px-4 py-2.5 bg-slate-800 hover:bg-slate-700 text-xs sm:text-sm font-bold rounded-xl text-slate-300 transition">
          రీసెట్
        </button>
      </div>
    </div>

    <!-- Articles Section -->
    <section class="space-y-6">
      <div class="flex flex-wrap items-center justify-between gap-3 border-b border-slate-200 pb-3">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📜</span> <span>రాజ్యాంగ భాగాలు & ముఖ్య ఆర్టికల్స్ (Constitutional Parts & Key Articles)</span>
        </h3>
        <span id="articleCountBadge" class="text-xs font-bold text-indigo-900 bg-indigo-50 px-3 py-1 rounded-full border border-indigo-200">
          అన్ని ఆర్టికల్స్ అందుబాటులో ఉన్నాయి
        </span>
      </div>

      <div id="articlesContainer" class="space-y-8">
        {parts_html}
      </div>
    </section>

    <!-- MCQs Section -->
    <section class="space-y-4 pt-4 border-t border-slate-200">
      <div class="flex justify-between items-center">
        <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
          <span>📝</span> <span>ఆర్టికల్స్ ప్రాక్టీస్ ప్రశ్నలు (High-Yield MCQs)</span>
        </h3>
        <span class="text-xs font-black text-amber-800 bg-amber-100 px-3 py-1 rounded-full">
          {len(mcqs)} ప్రశ్నలు
        </span>
      </div>
      <div class="grid grid-cols-1 gap-4">
        {mcq_cards}
      </div>
    </section>

  </main>

  <script>
    function toggleSolution(id) {{
      const el = document.getElementById('sol_' + id);
      if (el) {{
        el.classList.toggle('hidden');
      }}
    }}

    function filterArticles() {{
      const query = document.getElementById('articleSearchInput').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.article-card');
      let visibleCount = 0;

      cards.forEach(card => {{
        const art = card.getAttribute('data-article') || '';
        const text = card.getAttribute('data-text') || '';
        if (!query || art.includes(query) || text.includes(query)) {{
          card.style.display = '';
          visibleCount++;
        }} else {{
          card.style.display = 'none';
        }}
      }});

      // Hide empty part sections
      const sections = document.querySelectorAll('.part-section');
      sections.forEach(sec => {{
        const visibleCards = sec.querySelectorAll('.article-card:not([style*="display: none"])');
        if (visibleCards.length === 0 && query !== '') {{
          sec.style.display = 'none';
        }} else {{
          sec.style.display = '';
        }}
      }});

      const badge = document.getElementById('articleCountBadge');
      if (badge) {{
        badge.innerText = query ? visibleCount + ' ఆర్టికల్స్ సరిపోలాయి' : 'అన్ని ఆర్టికల్స్ అందుబాటులో ఉన్నాయి';
      }}
    }}

    function resetSearch() {{
      const input = document.getElementById('articleSearchInput');
      if (input) {{
        input.value = '';
        filterArticles();
      }}
    }}
  </script>
</body>
</html>"""

    return html
