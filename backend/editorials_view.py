# -*- coding: utf-8 -*-
"""
Interactive Web View for Daily Telugu Editorial Analysis (/editorials_hub).
"""

from editorials_data import get_all_editorials

def render_editorials_hub_html(selected_paper="all"):
    all_ed = get_all_editorials()
    if selected_paper != "all":
        display_ed = [e for e in all_ed if selected_paper.lower() in e["newspaper"].lower()]
    else:
        display_ed = all_ed

    ed_cards = ""
    for ed in display_ed:
        prelims_items = "".join([f'<li class="flex items-start gap-2"><span class="text-rose-500 font-bold shrink-0">✦</span><span>{item}</span></li>' for item in ed["prelims_facts"]])
        pros_items = "".join([f'<li class="flex items-start gap-2"><span class="text-emerald-600 font-bold shrink-0">✔</span><span>{p}</span></li>' for p in ed["mains_dimensions"]["pros"]])
        cons_items = "".join([f'<li class="flex items-start gap-2"><span class="text-amber-600 font-bold shrink-0">✖</span><span>{c}</span></li>' for c in ed["mains_dimensions"]["cons"]])
        terms_items = "".join([f'<div class="p-2.5 bg-slate-50 border border-slate-200 rounded-lg text-xs"><strong class="text-indigo-900 block mb-0.5">{t["term"]}:</strong><span class="text-slate-700">{t["meaning"]}</span></div>' for t in ed["key_terms"]])

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

          <!-- Practice Question Card -->
          <div class="p-4 bg-amber-50/80 border border-amber-300/80 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div class="space-y-1">
              <span class="text-[10px] font-black uppercase tracking-wider bg-amber-200 text-amber-900 px-2 py-0.5 rounded">డైలీ మెయిన్స్ ప్రాక్టీస్ ప్రశ్న</span>
              <p class="text-xs sm:text-sm font-bold text-slate-900 leading-relaxed">{ed['practice_question']}</p>
            </div>
            <a href="/mains_answer_bank" class="shrink-0 px-3.5 py-2 bg-amber-500 hover:bg-amber-400 text-slate-950 font-black text-xs rounded-xl transition shadow-2xs">
              మోడల్ సమాధానాలు
            </a>
          </div>
        </article>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>డైలీ తెలుగు ఎడిటోరియల్ విశ్లేషణ - లక్ష్య పోటీ పరీక్షలు</title>
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
          <span>📰</span> <span>డైలీ తెలుగు ఎడిటోరియల్ విశ్లేషణ (ఈనాడు, సాక్షి, ది హిందూ)</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <button onclick="window.print()" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1.5 rounded-lg transition flex items-center gap-1.5">
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
        <span class="text-xs text-rose-300 font-semibold">రాజకీయాలు లేని స్వచ్ఛమైన పరీక్షా విశ్లేషణ</span>
      </div>
      <h2 class="text-xl sm:text-2xl font-black text-white">ప్రధాన దినపత్రికల సంపాదకీయాల పరీక్షా సారాంశం</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
        ఈనాడు, సాక్షి, ది హిందూ పత్రికలలో ప్రచురితమయ్యే సంపాదకీయాల నుండి యూపీఎస్సీ మరియు ఏపీపీఎస్సీ/టీఎస్‌పీఎస్సీ ప్రిలిమ్స్ ఫ్యాక్ట్స్, మెయిన్స్ పాయింట్లు మరియు మోడల్ ప్రశ్నల సంకలనం.
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
</body>
</html>
"""
    return html
