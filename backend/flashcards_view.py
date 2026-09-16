# -*- coding: utf-8 -*-
"""
Interactive 3D Revision Flashcards Deck Web View (/flashcards_deck).
Renders 300+ 3D flip flashcards for rapid memorization and exam revision.
"""

import json
from flashcards_data import get_all_flashcards, get_flashcard_categories

def render_flashcards_deck_html(selected_category="all"):
    all_cards = get_all_flashcards()
    cats = get_flashcard_categories()

    cards_data_json = json.dumps(all_cards, ensure_ascii=False)

    nav_tabs = f"""
    <button type="button" onclick="filterCat('all')" class="cat-btn active px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold border transition bg-indigo-600 text-white border-indigo-600 shadow-md" data-cat="all">
      🌟 అన్నీ ({len(all_cards)})
    </button>
    """
    for k, v in cats.items():
        nav_tabs += f"""
        <button type="button" onclick="filterCat('{k}')" class="cat-btn px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold border transition bg-white text-slate-700 hover:bg-slate-100 border-slate-300" data-cat="{k}">
          {v['name']} ({v['total']})
        </button>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ఎగ్జామ్ ర్యాంకర్స్ రివిజన్ ఫ్లాష్‌కార్డ్స్ (300+ Cards) - లక్ష్య పోటీ పరీక్షలు</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Mandali&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif; }}
    .perspective-1000 {{ perspective: 1000px; }}
    .flip-card-inner {{
      position: relative;
      width: 100%;
      height: 100%;
      transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
      transform-style: preserve-3d;
    }}
    .flip-card.flipped .flip-card-inner {{
      transform: rotateY(180deg);
    }}
    .flip-front, .flip-back {{
      position: absolute;
      width: 100%;
      height: 100%;
      -webkit-backface-visibility: hidden;
      backface-visibility: hidden;
      border-radius: 1.5rem;
    }}
    .flip-back {{
      transform: rotateY(180deg);
    }}
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen flex flex-col">

  <!-- Header -->
  <header class="bg-slate-950/80 border-b border-slate-800 sticky top-0 z-30 backdrop-blur-md">
    <div class="max-w-5xl mx-auto px-4 py-3 flex justify-between items-center">
      <div class="flex items-center gap-3">
        <a href="/syllabus" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> సిలబస్ హబ్
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🗂️</span> <span>3D రివిజన్ ఫ్లాష్‌కార్డ్స్ (300+ Cards)</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <span id="masteredBadge" class="bg-emerald-500/20 text-emerald-300 border border-emerald-500/30 text-xs font-black px-2.5 py-1 rounded-lg">
          గుర్తున్నవి: 0
        </span>
        <button onclick="shuffleCards()" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold px-3 py-1.5 rounded-lg border border-slate-700 transition" title="షఫుల్ చేయండి">
          <i class="fa-solid fa-shuffle"></i>
        </button>
      </div>
    </div>
  </header>

  <!-- Main Container -->
  <main class="max-w-4xl mx-auto px-4 py-6 flex-1 flex flex-col items-center justify-center space-y-6 w-full">

    <!-- Categories Filter Tabs -->
    <div class="flex items-center gap-2 overflow-x-auto max-w-full pb-1">
      {nav_tabs}
    </div>

    <!-- Progress & Counter -->
    <div class="w-full max-w-lg flex justify-between items-center text-xs font-bold text-slate-400">
      <span id="cardCounter">కార్డ్ 1 / 300</span>
      <span id="categoryLabel" class="bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded-md border border-indigo-800">రాజ్యాంగం & పాలిటీ</span>
    </div>

    <!-- 3D Flip Card Container -->
    <div class="w-full max-w-lg h-80 sm:h-96 perspective-1000 cursor-pointer select-none" onclick="toggleFlip()">
      <div id="flashcardElement" class="flip-card flip-card-inner">
        
        <!-- Front Side -->
        <div class="flip-front bg-gradient-to-br from-slate-800 to-slate-900 border-2 border-indigo-500/40 p-6 sm:p-8 flex flex-col justify-between shadow-2xl">
          <div class="flex justify-between items-center text-xs font-black">
            <span class="bg-indigo-600 text-white px-3 py-1 rounded-full" id="frontTag">ప్రాథమిక హక్కులు</span>
            <span class="text-indigo-300"><i class="fa-solid fa-rotate mr-1"></i> తిప్పడానికి క్లిక్ చేయండి</span>
          </div>
          <div class="my-auto text-center">
            <h2 id="frontText" class="text-lg sm:text-2xl font-black text-white leading-relaxed">
              భారత రాజ్యాంగంలో ఆర్టికల్ 14 దేనిని సూచిస్తుంది?
            </h2>
          </div>
          <div class="text-center text-xs text-slate-400 font-semibold">
            (కీబోర్డ్ స్పేస్‌బార్ లేదా క్లిక్ చేయండి)
          </div>
        </div>

        <!-- Back Side -->
        <div class="flip-back bg-gradient-to-br from-indigo-950 via-slate-900 to-slate-950 border-2 border-emerald-500/50 p-6 sm:p-8 flex flex-col justify-between shadow-2xl">
          <div class="flex justify-between items-center text-xs font-black">
            <span class="bg-emerald-600 text-white px-3 py-1 rounded-full">సమాధానం & విశ్లేషణ</span>
            <span class="text-emerald-300"><i class="fa-solid fa-check mr-1"></i> అధికారిక వివరణ</span>
          </div>
          <div class="my-auto text-center">
            <p id="backText" class="text-sm sm:text-lg font-bold text-emerald-100 leading-relaxed">
              చట్టం ముందు అందరూ సమానులే (Equality before Law) మరియు చట్టం ద్వారా సమాన రక్షణ (Equal Protection of Laws).
            </p>
          </div>
          <div class="flex justify-center gap-3 pt-2">
            <button type="button" onclick="event.stopPropagation(); markMastered(true)" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs px-4 py-2 rounded-xl transition flex items-center gap-1.5 shadow-md">
              <i class="fa-solid fa-thumbs-up"></i> గుర్తుంది
            </button>
            <button type="button" onclick="event.stopPropagation(); markMastered(false)" class="bg-slate-800 hover:bg-slate-700 text-amber-300 font-bold text-xs px-4 py-2 rounded-xl transition flex items-center gap-1.5 border border-slate-700">
              <i class="fa-solid fa-repeat"></i> మళ్లీ చూడాలి
            </button>
          </div>
        </div>

      </div>
    </div>

    <!-- Navigation Controls -->
    <div class="flex items-center gap-4">
      <button onclick="prevCard()" class="w-12 h-12 rounded-2xl bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-700 shadow-md">
        <i class="fa-solid fa-arrow-left text-base"></i>
      </button>
      <button onclick="toggleFlip()" class="px-6 py-3 rounded-2xl bg-indigo-600 hover:bg-indigo-500 text-white font-black text-sm flex items-center gap-2 transition shadow-lg">
        <i class="fa-solid fa-repeat"></i> కార్డ్ తిప్పు (Flip)
      </button>
      <button onclick="nextCard()" class="w-12 h-12 rounded-2xl bg-slate-800 hover:bg-slate-700 text-white flex items-center justify-center transition border border-slate-700 shadow-md">
        <i class="fa-solid fa-arrow-right text-base"></i>
      </button>
    </div>

  </main>

  <script>
    const allCardsData = {cards_data_json};
    let currentCards = [...allCardsData];
    let currentIndex = 0;
    let masteredCount = 0;

    function renderCurrentCard() {{
      const card = currentCards[currentIndex];
      if (!card) return;
      document.getElementById('frontText').innerText = card.front;
      document.getElementById('backText').innerText = card.back;
      document.getElementById('frontTag').innerText = card.tag || card.cat.toUpperCase();
      document.getElementById('categoryLabel').innerText = card.cat.toUpperCase();
      document.getElementById('cardCounter').innerText = `కార్డ్ ${{currentIndex + 1}} / ${{currentCards.length}}`;
      // unflip
      document.getElementById('flashcardElement').classList.remove('flipped');
    }}

    function toggleFlip() {{
      document.getElementById('flashcardElement').classList.toggle('flipped');
    }}

    function nextCard() {{
      if (currentIndex < currentCards.length - 1) {{
        currentIndex++;
      }} else {{
        currentIndex = 0;
      }}
      renderCurrentCard();
    }}

    function prevCard() {{
      if (currentIndex > 0) {{
        currentIndex--;
      }} else {{
        currentIndex = currentCards.length - 1;
      }}
      renderCurrentCard();
    }}

    function markMastered(isMastered) {{
      if (isMastered) masteredCount++;
      document.getElementById('masteredBadge').innerText = `గుర్తున్నవి: ${{masteredCount}}`;
      nextCard();
    }}

    function shuffleCards() {{
      currentCards.sort(() => Math.random() - 0.5);
      currentIndex = 0;
      renderCurrentCard();
    }}

    function filterCat(cat) {{
      document.querySelectorAll('.cat-btn').forEach(btn => {{
        if (btn.getAttribute('data-cat') === cat) {{
          btn.className = "cat-btn active px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold border transition bg-indigo-600 text-white border-indigo-600 shadow-md";
        }} else {{
          btn.className = "cat-btn px-3.5 py-1.5 rounded-xl text-xs sm:text-sm font-bold border transition bg-white text-slate-700 hover:bg-slate-100 border-slate-300";
        }}
      }});
      if (cat === 'all') {{
        currentCards = [...allCardsData];
      }} else {{
        currentCards = allCardsData.filter(c => c.cat === cat);
      }}
      currentIndex = 0;
      renderCurrentCard();
    }}

    // Keyboard navigation
    window.addEventListener('keydown', (e) => {{
      if (e.code === 'Space') {{
        e.preventDefault();
        toggleFlip();
      }} else if (e.code === 'ArrowRight') {{
        nextCard();
      }} else if (e.code === 'ArrowLeft') {{
        prevCard();
      }}
    }});

    renderCurrentCard();
  </script>
</body>
</html>"""
    return html
