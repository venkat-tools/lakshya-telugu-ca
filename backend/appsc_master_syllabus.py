# -*- coding: utf-8 -*-
"""
APPSC Group 1 & Group 2 Master Syllabus, Study Guide & Subject Portal.
Extracted from official comprehensive handbooks:
1. భారతదేశ & ఆంధ్రప్రదేశ్ భూగోళశాస్త్రం (Geography - 12 విభాగాలు)
2. ఆంధ్రప్రదేశ్ నూతన విధానాలు 4.0 (AP Industrial Policies 2024-2029)
3. క్వాంటిటేటివ్ ఆప్టిట్యూడ్ & మెంటల్ ఎబిలిటీ (120+ షార్ట్‌కట్లు & ఫార్ములాలు)
4. భారత & ఆంధ్రప్రదేశ్ చరిత్ర (Ancient, Medieval, Modern, AP History)
5. భారత రాజ్యాంగం, పాలన & ముఖ్య ఆర్టికల్స్ (Polity, DPSP, 73/74 Amendments)
6. భారత ఆర్థిక వ్యవస్థ & ద్రవ్య మార్కెట్లు (Financial Markets, T-Bills, CP, CD, NITI Aayog)
7. సైన్స్, టెక్నాలజీ, పర్యావరణం & విపత్తు నిర్వహణ (ISRO, Ecology, Water Disputes)
8. గ్రూప్-1 మెయిన్స్ ఆన్సర్ రైటింగ్, ఎథిక్స్ & ఇంటర్వ్యూ గైడ్
"""

def render_appsc_syllabus_html():
    return """<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APPSC గ్రూప్ 1 & 2 సమగ్ర సిలబస్, స్టడీ మెటీరియల్స్ & మాస్టర్ గైడ్ | లక్ష్య CA</title>
  <script src="https://cdn.tailwindcss.com">
    function checkPyq(btn, isCorrect, explanation) {
      const parent = btn.parentElement;
      const buttons = parent.querySelectorAll('button');
      buttons.forEach(b => {
        b.disabled = true;
        b.classList.remove('hover:bg-slate-700');
      });
      const expBox = parent.parentElement.querySelector('.pyq-exp');
      if (isCorrect) {
        btn.classList.remove('bg-slate-900');
        btn.classList.add('bg-emerald-600', 'text-white', 'font-bold');
        expBox.innerHTML = '<span class="text-emerald-400 font-bold">✅ సరైన సమాధానం!</span><br>' + explanation;
      } else {
        btn.classList.remove('bg-slate-900');
        btn.classList.add('bg-red-600', 'text-white', 'font-bold');
        expBox.innerHTML = '<span class="text-red-400 font-bold">❌ తప్పు సమాధానం!</span><br>' + explanation;
      }
      expBox.classList.remove('hidden');
    }

  </script>
  <link rel="icon" type="image/jpeg" href="/lakshya_logo.jpg">
  <link rel="apple-touch-icon" href="/lakshya_logo.jpg">
  <link rel="stylesheet" href="/styles.css?v=14">
  <script src="https://unpkg.com/lucide@latest">
    function checkPyq(btn, isCorrect, explanation) {
      const parent = btn.parentElement;
      const buttons = parent.querySelectorAll('button');
      buttons.forEach(b => {
        b.disabled = true;
        b.classList.remove('hover:bg-slate-700');
      });
      const expBox = parent.parentElement.querySelector('.pyq-exp');
      if (isCorrect) {
        btn.classList.remove('bg-slate-900');
        btn.classList.add('bg-emerald-600', 'text-white', 'font-bold');
        expBox.innerHTML = '<span class="text-emerald-400 font-bold">✅ సరైన సమాధానం!</span><br>' + explanation;
      } else {
        btn.classList.remove('bg-slate-900');
        btn.classList.add('bg-red-600', 'text-white', 'font-bold');
        expBox.innerHTML = '<span class="text-red-400 font-bold">❌ తప్పు సమాధానం!</span><br>' + explanation;
      }
      expBox.classList.remove('hidden');
    }

  </script>
  <style>
    @media print {
      .no-print { display: none !important; }
      body { background: white !important; color: black !important; font-size: 11pt; }
      .page-break { page-break-after: always; }
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: none !important; }
    }
    .topic-card:hover { transform: translateY(-2px); transition: all 0.2s ease; }
    .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #94a3b8; border-radius: 4px; }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans antialiased">

  <!-- Top Announcement Bar -->
  <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white text-xs md:text-sm py-2 px-4 shadow-sm border-b border-indigo-800/40 no-print">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center space-x-2">
        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-amber-400 text-slate-950">
          🎯 అధికారిక సిలబస్ పోర్టల్
        </span>
        <span class="truncate max-w-xs md:max-w-xl text-slate-200">
          APPSC గ్రూప్-1 & గ్రూప్-2 సంపూర్ణ స్టడీ మెటీరియల్స్, ఫార్ములాలు & నూతన పాలసీలు 4.0
        </span>
      </div>
      <div class="flex items-center space-x-3">
        <a href="/" class="text-xs bg-blue-600 hover:bg-blue-500 text-white font-bold px-3 py-1 rounded transition flex items-center gap-1">
          <i data-lucide="arrow-left" class="w-3.5 h-3.5"></i>
          <span>డ్యాష్‌బోర్డ్</span>
        </a>
      </div>
    </div>
  </div>

  <!-- Main Header -->
  <header class="bg-slate-800/90 backdrop-blur border-b border-slate-700/60 sticky top-0 z-30 shadow-md no-print">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap justify-between items-center gap-4">
      <div class="flex items-center space-x-3">
        <img src="/lakshya_logo.jpg" alt="Logo" class="w-10 h-10 rounded-xl shadow-md border border-amber-400/40">
        <div>
          <h1 class="text-lg md:text-xl font-black text-white tracking-tight flex items-center gap-2">
            లక్ష్య • APPSC మాస్టర్ సిలబస్ & స్టడీ హబ్
            <span class="text-xs bg-amber-400/20 text-amber-300 font-bold px-2.5 py-0.5 rounded-full border border-amber-400/30">Group 1 & 2 Special</span>
          </h1>
          <p class="text-xs text-slate-400 font-medium">8 ముఖ్య సబ్జెక్టుల సమగ్ర వివరణాత్మక పాఠ్య గ్రంథం & 120+ షార్ట్‌కట్ ఫార్ములాలు</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2.5">
        <button onclick="window.print()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs sm:text-sm font-bold flex items-center space-x-1.5 transition shadow-sm">
          <i data-lucide="printer" class="w-4 h-4"></i>
          <span>ప్రింట్ / PDF</span>
        </button>
        <button onclick="shareToWhatsApp()" class="bg-green-600 hover:bg-green-500 text-white px-3 py-1.5 rounded-lg text-xs sm:text-sm font-bold flex items-center space-x-1.5 transition shadow-sm">
          <i data-lucide="share-2" class="w-4 h-4"></i>
          <span>వాట్సాప్‌లో షేర్</span>
        </button>
      </div>
    </div>

    <!-- Subject Tabs Bar -->
    <div class="max-w-7xl mx-auto px-4 overflow-x-auto custom-scrollbar border-t border-slate-700/60 flex space-x-2 py-2 text-xs font-bold">
      <button onclick="switchTab('geo')" id="tab-geo" class="tab-btn px-3.5 py-2 rounded-lg bg-blue-600 text-white flex items-center gap-1.5 shrink-0 transition">
        <span>🌍 భూగోళశాస్త్రం (12 భాగాలు)</span>
      </button>
      <button onclick="switchTab('policies')" id="tab-policies" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>💼 ఏపీ నూతన విధానాలు 4.0</span>
      </button>
      <button onclick="switchTab('aptitude')" id="tab-aptitude" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>🧮 మెంటల్ ఎబిలిటీ (120 షార్ట్‌కట్స్)</span>
      </button>
      <button onclick="switchTab('history')" id="tab-history" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>📜 చరిత్ర (భారత & ఏపీ)</span>
      </button>
      <button onclick="switchTab('polity')" id="tab-polity" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>⚖️ రాజ్యాంగం & పాలన</span>
      </button>
      <button onclick="switchTab('economy')" id="tab-economy" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>💰 ఆర్థిక వ్యవస్థ & మార్కెట్లు</span>
      </button>
      <button onclick="switchTab('science')" id="tab-science" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>🔬 సైన్స్, పర్యావరణం & విపత్తులు</span>
      </button>
      <button onclick="switchTab('disaster')" id="tab-disaster" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>🚨 విపత్తు నిర్వహణ (RC రెడ్డి నోట్స్)</span>
      </button>
      <button onclick="switchTab('pyqs')" id="tab-pyqs" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>📝 115+ APPSC ప్రీవియస్ Qs (MCQs)</span>
      </button>
      <button onclick="switchTab('mains')" id="tab-mains" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>✍️ మెయిన్స్ & ఎథిక్స్ గైడ్</span>
      </button>
    </div>
  </header>

  <!-- Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

    <!-- Progress & Search Bar -->
    <div class="bg-slate-800/80 border border-slate-700/70 p-4 rounded-2xl mb-6 shadow-sm flex flex-wrap items-center justify-between gap-4 no-print">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <div class="w-9 h-9 rounded-lg bg-amber-400/20 text-amber-400 flex items-center justify-center font-black">
          <i data-lucide="check-circle" class="w-5 h-5"></i>
        </div>
        <div>
          <h3 class="text-sm font-bold text-white">మీ ప్రిపరేషన్ చెక్‌లిస్ట్ ట్రాకర్</h3>
          <p class="text-xs text-slate-400" id="progressText">మీరు చదివిన టాపిక్స్ టిక్ చేసుకోండి (0 / 36 పూర్తి)</p>
        </div>
      </div>
      <div class="w-full md:w-64 bg-slate-700 rounded-full h-2.5 overflow-hidden">
        <div id="progressBar" class="bg-gradient-to-r from-amber-400 to-emerald-500 h-2.5 rounded-full transition-all duration-300" style="width: 0%"></div>
      </div>
    </div>

    <!-- ==================== TAB 1: GEOGRAPHY ==================== -->
    <section id="content-geo" class="tab-content space-y-6">
      <div class="bg-gradient-to-r from-blue-950 via-slate-800 to-slate-900 border border-blue-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-blue-900/60 text-blue-300 px-3 py-1 rounded-full border border-blue-700/50">భాగం 1 • 30 మార్కులు</span>
          <span class="text-xs text-slate-400">APPSC Group 1 & 2 ప్రిలిమ్స్ ప్రధాన విభాగం</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారతదేశ & ఆంధ్రప్రదేశ్ భూగోళశాస్త్రం (Comprehensive Geography)</h2>
        <p class="text-sm text-slate-300 mt-1">సాధారణ భౌతిక భూగోళశాస్త్రం, శీతోష్ణస్థితి, సముద్ర శాస్త్రం, భారత & ఏపీ నదీ వ్యవస్థలు, నేలలు, అడవులు, ఖనిజాలు మరియు జనాభా లెక్కలు 2011.</p>
      </div>

      <!-- 12 Sections Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">

        <!-- 1. General & Physical -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 01</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">భూమి అంతర్నిర్మాణం & భూస్వరూపాలు (Geomorphology)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>భూమి పొరలు:</b> భూపటలం (Crust - SIAL & SIMA), భూప్రావారం (Mantle 84% వాల్యూమ్, అస్తెనోస్పియర్), భూకేంద్ర మండలం (Core - NIFE).</li>
            <li>• <b>సంధి మండలాలు (Discontinuities):</b> కాన్రాడ్ (పై-కింది క్రస్ట్), మోహో (క్రస్ట్-మాంటిల్), రెపిట్టి (పై-కింది మాంటిల్), గుటెన్‌బర్గ్ (మాంటిల్-కోర్), లెహ్మాన్ (బాహ్య-అంతర కోర్).</li>
            <li>• <b>పలక విరూపకారక సిద్ధాంతం:</b> అభిసరణ (హిమాలయాలు), అపసరణ (మిడ్-అట్లాంటిక్ రిడ్జ్), రూపాంతర సరిహద్దులు (శాన్ ఆండ్రియాస్).</li>
            <li>• <b>భూకంప తరంగాలు:</b> P-తరంగాలు (అనుదైర్ఘ్య, ఘన-ద్రవ-వాయువుల్లో), S-తరంగాలు (తిర్యక్, ఘన పదార్థాల్లో మాత్రమే), L-తరంగాలు (ఉపరితల విధ్వంసం).</li>
            <li>• <b>శిలలు:</b> అగ్ని శిలలు (గ్రానైట్, బసాల్ట్), అవక్షేప శిలలు (ఇసుకరాయి, సున్నపురాయి, బొగ్గు), రూపాంతర శిలలు (మార్బుల్, క్వార్ట్జైట్, నీస్).</li>
          </ul>
        </div>

        <!-- 2. Climatology & Oceanography -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 02</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">వాతావరణం & సముద్ర శాస్త్రం (Climatology & Oceanography)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>పీడన పట్టీలు:</b> డోల్‌డ్రమ్స్ (5°N-5°S ప్రశాంత మండలం, ITCZ), గుర్రపు అక్షాంశాలు (30°-35° ఉప-ఉష్ణ అధికపీడనం), వ్యాపార పవనాలు (Trade winds), పశ్చిమ పవనాలు (రోరింగ్ ఫోర్టీస్, ఫ్యూరియస్ ఫిఫ్టీస్).</li>
            <li>• <b>స్థానిక పవనాలు:</b> లూ (ఉత్తర భారత వడగాలులు), చినూక్ (రాకీ పర్వతాల మంచు భక్షకి), సిరోకో (సహారా రక్త వర్షం), హర్మట్టన్ (డాక్టర్ విండ్).</li>
            <li>• <b>సముద్ర భూస్వరూపం:</b> ఖండతీరపు అంచు (Continental Shelf - బాంబే హై, కేజీ బేసిన్), ఖండతీరపు వాలు, అగాధ మైదానం, మరియానా ట్రెంచ్ (11,022 మీటర్లు).</li>
            <li>• <b>లవణీయత:</b> ప్రపంచ సగటు 35 ppt. వాన్ సరస్సు (టర్కీ 330 ppt), మృత సముద్రం (240 ppt), గ్రేట్ సాల్ట్ లేక్ (220 ppt).</li>
            <li>• <b>పోటుపాట్లు:</b> బృహత్ పోటు (Spring Tide - అమావాస్య, పౌర్ణమి Syzygy సరళరేఖ), లఘు పోటు (Neap Tide - అష్టమి 90° లంబకోణం).</li>
          </ul>
        </div>

        <!-- 3. Indian Physiography & Passes -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 03</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">భారత నైసర్గిక స్వరూపం & కనుమలు (Passes & Islands)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>హిమాలయ విభజన:</b> పంజాబ్ (సింధు-సట్లజ్, కరేవా నేలలు కుంకుమపువ్వు), కుమౌన్ (సట్లజ్-కాళి), నేపాల్ (కాళి-తీస్తా, ఎవరెస్ట్ 8848.86 మీ), అస్సాం (తీస్తా-బ్రహ్మపుత్ర, నంచా బర్వా).</li>
            <li>• <b>ప్రధాన కనుమలు:</b> జోజిలా (శ్రీనగర్-లేహ్), బనిహాల్ (జవహర్ టన్నెల్), రోహ్‌తంగ్ & అటల్ టన్నెల్ (కులు-లాహౌల్ స్పితి), షిప్కిలా (సట్లజ్ నది ప్రవేశం), లిపులేఖ్ (మానససరోవర్ యాత్ర), నాథులా (సిక్కిం-సిల్క్ రూట్), బొమ్డిలా (అరుణాచల్).</li>
            <li>• <b>దీవులు:</b> అండమాన్ నికోబార్ (శాడిల్ పీక్ 732 మీ, బారెన్ యాక్టివ్ అగ్నిపర్వతం, నార్కొండమ్), లక్షదీవులు (ప్రవాళ భిత్తికలు, 8° ఛానల్ మాల్దీవులు-మినికాయ్, 9° ఛానల్ మినికాయ్-లక్షదీవులు).</li>
          </ul>
        </div>

        <!-- 4. Indian River Systems -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 04</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">భారత నదీ వ్యవస్థలు & పంచ ప్రయాగలు (River Systems)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>ఉత్తరాఖండ్ పంచ ప్రయాగలు:</b> విష్ణుప్రయాగ (అలకనంద + ధౌలిగంగ), నందప్రయాగ (నంధాకిని), కర్ణప్రయాగ (పిండార్), రుద్రప్రయాగ (మందాకిని), దేవప్రయాగ (అలకనంద + భగీరథి = గంగా నది).</li>
            <li>• <b>ఉపనదులు:</b> యమున (1376 కి.మీ - చంబల్, సింధ్, బెట్వా, కేన్), కోసి (బీహార్ దుఃఖదాయిని), దామోదర్ (బెంగాల్ దుఃఖదాయిని, 1948 TVA ఆధారిత DVC ప్రాజెక్ట్).</li>
            <li>• <b>దక్షిణ భారత నదులు:</b> కావేరి (800 కి.మీ, తలకావేరి కూర్గ్, శివసముద్రం, కృష్ణరాజసాగర్, మెట్టూరు - దక్షిణ భారతదేశపు గంగ), మహానది (851 కి.మీ, సిహవా ఛత్తీస్‌గఢ్, హీరాకుడ్ డ్యామ్ 25.8 కి.మీ).</li>
          </ul>
        </div>

        <!-- 5. AP Rivers & Projects -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 05</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">ఆంధ్రప్రదేశ్ నదులు, ప్రాజెక్టులు & రాయలసీమ జీవనాధారాలు</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>గోదావరి:</b> 1465 కి.మీ (దక్షిణ భారతంలో పొడవైనది, త్రయంబకేశ్వరం నాసిక్). పాపికొండల బైసన్ గార్జ్. ధవళేశ్వరం బ్యారేజ్ (1847-52 సర్ ఆర్థర్ కాటన్). పోలవరం ప్రాజెక్ట్ (194 TMC, కుడి కాలువ 80 TMC కృష్ణాకు మళ్లింపు, ఎడమ కాలువ వైజాగ్ పరిశ్రమలకు).</li>
            <li>• <b>కృష్ణా:</b> మహాబలేశ్వరం. తుంగభద్ర (కూడ్లి వద్ద కలయిక, హోస్పేట్ డ్యామ్). శ్రీశైలం (215 TMC నల్లమల లోయ), నాగార్జునసాగర్ (విజయపురి), పులిచింతల (45 TMC బ్యాలెన్సింగ్).</li>
            <li>• <b>రాయలసీమ ప్రాజెక్టులు:</b> పోతిరెడ్డిపాడు హెడ్‌రెగ్యులేటర్ (శ్రీశైలం నీటి మళ్లింపు), తెలుగుగంగ (రాయలసీమ + చెన్నైకి 15 TMC తాగునీరు), GNSS (గోరుకల్లు ద్వారా కడప, చిత్తూరు), HNSS (హంద్రీ-నీవా లిఫ్ట్ ఇరిగేషన్), వెలిగొండ (18.8 కి.మీ ఆసియాలోనే పొడవైన డబుల్ టన్నెల్స్).</li>
          </ul>
        </div>

        <!-- 6. AP Soils, Forests & Minerals -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 06</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">ఏపీ నేలలు, అభయారణ్యాలు & ఖనిజ సంపద (Resources)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>నేలలు:</b> ఎర్ర నేలలు (65% అత్యధికం - నత్రజని, సేంద్రీయ కర్బనం లోపం), నల్లరేగడి నేలలు (25% - మాంట్‌మొరిల్లోనైట్ ఖనిజం వల్ల ఉబ్బడం/పగుళ్లు), తీర ఉప్పునేలలు (బాపట్ల, ప్రకాశం).</li>
            <li>• <b>అభయారణ్యాలు:</b> శ్రీశైలం-నాగార్జునసాగర్ టైగర్ రిజర్వ్ (దేశంలోనే అతిపెద్ద పులుల రిజర్వ్), పాపికొండల నేషనల్ పార్క్ (అడవి దున్న), శ్రీవేంకటేశ్వర పార్క్ (శేషాచలం - ఎర్రచందనం, పసిడి బల్లి), రోళ్లపాడు (బట్టమేక పిట్ట GIB & కృష్ణజింకలు), నేలపట్టు (పెలికాన్ల కేంద్రం), కోరింగ (ఫిషింగ్ క్యాట్ & మడ అడవులు).</li>
            <li>• <b>ఖనిజాలు:</b> బారైటీస్ (మంగంపేట కడప - ప్రపంచంలోనే ఉత్తమ గ్రేడ్), యురేనియం (తుమ్మలపల్లె కడప - అటామిక్ ఎనర్జీ ప్రకారం అతిపెద్ద నిల్వలు), సున్నపురాయి (పల్నాడు బేసిన్ సిమెంట్ హబ్), గెలాక్సీ గ్రానైట్ (చీమకుర్తి ప్రకాశం).</li>
          </ul>
        </div>

        <!-- 7. 26 Districts & Demography -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <span class="text-xs font-black text-amber-400 bg-amber-400/10 px-2.5 py-0.5 rounded border border-amber-400/20">విభాగం 07</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">ఏపీ 26 జిల్లాలు, జనాభా లెక్కలు 2011 & PVTG తెగలు</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>26 జిల్లాలు (2022 రీఆర్గనైజేషన్):</b> విస్తీర్ణంలో అతిపెద్దది: ప్రకాశం (14,322 చ.కి.మీ); అతిచిన్నది: విశాఖపట్నం (1048 చ.కి.మీ). అత్యధిక జనాభా: నెల్లూరు; అత్యల్ప జనాభా: అల్లూరి సీతారామరాజు. తీరప్రాంత జిల్లాలు: 12; ల్యాండ్‌లాక్డ్ జిల్లాలు: 14.</li>
            <li>• <b>జనాభా లెక్కలు 2011:</b> వృద్ధి రేటు 10.98% (అత్యధికం కర్నూలు 14.85%, అత్యల్పం పశ్చిమ గోదావరి 3.51%). జనసాంద్రత 304/చ.కి.మీ (అత్యధికం కృష్ణా 518, అత్యల్పం కడప 188). లింగ నిష్పత్తి 997 (అత్యధికం విజయనగరం 1019, అత్యల్పం అనంతపురం 977).</li>
            <li>• <b>PVTG ఆదిమ గిరిజనులు:</b> చెంచులు (నల్లమల అడవులు, తేనె సేకరణ), కొండరెడ్లు (పాపికొండలు, పోడు వ్యవసాయం), కొండసవరలు (శ్రీకాకుళం/మన్యం, సోపాన వ్యవసాయం, ప్రపంచ ప్రసిద్ధ 'ఇడున్' Idun Art గోడ చిత్రలేఖనం).</li>
          </ul>
        </div>

      </div>
    </section>

    <!-- ==================== TAB 2: AP POLICIES 4.0 ==================== -->
    <section id="content-policies" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-emerald-950 via-slate-800 to-slate-900 border border-emerald-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-emerald-900/60 text-emerald-300 px-3 py-1 rounded-full border border-emerald-700/50">APPSC Group 1 & 2 Special</span>
          <span class="text-xs text-slate-400">ఆంధ్రప్రదేశ్ అధికారిక జీవోలు & పాలసీలు (2024–2029)</span>
        </div>
        <h2 class="text-2xl font-black text-white">ఆంధ్రప్రదేశ్ నూతన పారిశ్రామిక విధానాలు 4.0 (AP Policies Master Guide)</h2>
        <p class="text-sm text-slate-300 mt-1">ప్లగ్-అండ్-ప్లే పార్కులు, పారిశ్రామిక విధానం, MSME 2030, ఫుడ్ ప్రాసెసింగ్, టెక్స్‌టైల్ TAG, ఎలక్ట్రానిక్స్, ఈవీ రవాణా, ఐటీ/GCC, డేటా సెంటర్, సెమీకండక్టర్, డ్రోన్ & మారిటైమ్ పాలసీలు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        
        <!-- Policy 1: Private Parks & Industrial 4.0 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2.5 py-0.5 rounded border border-emerald-400/20">పాలసీ 01 & 02</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">ప్రైవేట్ పార్కులు & పారిశ్రామిక విధానం 4.0 (2024–2029)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>లక్ష్యాలు:</b> తయారీ రంగ స్థూల విలువ జోడింపు ₹3.4 లక్షల కోట్ల నుంచి ₹7.3 లక్షల కోట్లకు పెంపు. ₹30 లక్షల కోట్ల పారిశ్రామిక పెట్టుబడులు, 5 లక్షల స్థిర ఉద్యోగాలు.</li>
            <li>• <b>రతన్ టాటా ఇన్నోవేషన్ హబ్:</b> అమరావతిలో ప్రధాన కేంద్రం, 5 రీజినల్ హబ్‌లు (వైజాగ్, రాజమండ్రి, విజయవాడ, తిరుపతి, అనంతపురం).</li>
            <li>• <b>రాయితీలు:</b> స్థిర మూలధన పెట్టుబడిపై 12% రాయితీ, 5 ఏళ్లపాటు SGST 100% రీయింబర్స్‌మెంట్, యూనిట్‌కు ₹1 విద్యుత్ రాయితీ.</li>
            <li>• <b>ప్రైవేట్ పార్కుల వర్గీకరణ:</b> నానో (&lt;10 ఎకరాలు), MSME (10-100 ఎకరాలు), లార్జ్ (100-1000 ఎకరాలు), మెగా (&gt;1000 ఎకరాలు). మూలధన రాయితీ ఎకరానికి ₹5 లక్షల వరకు.</li>
          </ul>
        </div>

        <!-- Policy 2: MSME & Food Processing -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2.5 py-0.5 rounded border border-emerald-400/20">పాలసీ 03 & 04</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">MSME విధానం & ఆహార ప్రాసెసింగ్ విధానం (G.O.Ms.No.71)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>MSME 2030 నినాదం:</b> "ఒక కుటుంబం — ఒక పారిశ్రామికవేత్త". 22 లక్షల MSME యూనిట్ల స్థాపన, ₹50,000 కోట్ల పెట్టుబడులు.</li>
            <li>• <b>175 MSME పార్కులు:</b> రాష్ట్రంలోని ప్రతి శాసనసభ నియోజకవర్గానికి ఒక పారిశ్రామిక పార్కు ఏర్పాటు. మహిళలు, SC/ST, BC లకు 35% మూలధన రాయితీ.</li>
            <li>• <b>ఆహార ప్రాసెసింగ్ (APFPS):</b> ₹30,000 కోట్ల పెట్టుబడులు, 30 లక్షల గ్రామీణ ఉద్యోగాలు. రైతు ఉత్పత్తులకు విలువ జోడింపు. చిత్తూరులో మామిడి, కృష్ణా-గోదావరి ఆక్వా, రాయలసీమలో అరటి క్లస్టర్లు.</li>
            <li>• <b>రాయితీలు:</b> స్టాంప్ డ్యూటీ, భూ వినియోగ మార్పిడి 100% రీయింబర్స్‌మెంట్, స్థిర మూలధనంపై 25% సబ్సిడీ.</li>
          </ul>
        </div>

        <!-- Policy 3: Textile TAG 4.0 & Electronics ECMP 4.0 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2.5 py-0.5 rounded border border-emerald-400/20">పాలసీ 05 & 06</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">టెక్స్‌టైల్స్ (AP TAG 4.0) & ఎలక్ట్రానిక్స్ (ECMP 4.0)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>AP TAG 4.0 (G.O.Ms.No.89):</b> ₹10,000 కోట్ల పెట్టుబడులు, 2 లక్షల గ్రామీణ మహిళా ఉద్యోగాలు, 2029 నాటికి USD 1 బిలియన్ ఎగుమతులు. హిందూపూర్ అపారెల్ పార్క్ (₹102 కోట్లు), బ్రాండిక్స్ అచ్యుతాపురం వైజాగ్.</li>
            <li>• <b>ECMP 4.0 (G.O.Ms.No.5):</b> ఎలక్ట్రానిక్స్ ఉత్పత్తి USD 50 బిలియన్లకు పెంపు. శ్రీసిటీ-తిరుపతి (భారీ వినియోగ ఎలక్ట్రానిక్స్), కొప్పర్తి వైఎస్సార్ కడప (హార్డ్‌వేర్ & అసెంబ్లీ క్లస్టర్).</li>
            <li>• <b>రాయితీలు:</b> అర్హత స్థిర మూలధనంపై 55% వరకు సబ్సిడీ, యూనిట్‌కు ₹2 విద్యుత్ రాయితీ.</li>
          </ul>
        </div>

        <!-- Policy 4: Electric Mobility & IT GCC LIFT 4.0 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2.5 py-0.5 rounded border border-emerald-400/20">పాలసీ 07 & 08</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">సుస్థిర ఈవీ రవాణా (SEMP 4.0) & ఐటీ/GCC LIFT 4.0</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>SEMP 4.0 (G.O.Ms.No.88):</b> 2 లక్షల ఈవీ ద్విచక్ర, 10,000 త్రిచక్ర, 20,000 బ్యాటరీ కార్లు. APSRTC బస్సుల 100% విద్యుదీకరణ. ప్రతి 30 కి.మీ కు హైవే ఫాస్ట్ చార్జింగ్ స్టేషన్.</li>
            <li>• <b>IT & GCC 4.0 (G.O.Ms.No.9 & G.O.32):</b> వైజాగ్ టైర్-1 నగరంగా మార్పు. కాగ్నిజెంట్ మధురవాడ 22.19 ఎకరాల భూమి కేటాయింపు (ఎకరానికి ₹0.99 లీజు, ₹1,582 కోట్ల పెట్టుబడి, 8,000 టెక్ ఉద్యోగాలు).</li>
            <li>• <b>LIFT 4.0:</b> Land Incentive for Tech Hubs. 3 ఏళ్లలో 2,000 ఉద్యోగాలు సృష్టించే కంపెనీలకు రాయితీ భూ కేటాయింపులు.</li>
          </ul>
        </div>

        <!-- Policy 5: Semiconductor & Drone Policy 4.0 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2.5 py-0.5 rounded border border-emerald-400/20">పాలసీ 09 & 10</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">సెమీకండక్టర్ మిషన్ (G.O.7) & డ్రోన్ విధానం (G.O.18)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>సెమీకండక్టర్ & డిస్‌ప్లే ఫ్యాబ్ 4.0:</b> కేంద్ర ISM కు అదనంగా రాష్ట్ర ప్రభుత్వం 40% మూలధన సహాయం. వైజాగ్‌లో మొదటి ISM ప్రాజెక్ట్. నిరంతర నాణ్యమైన విద్యుత్ హామీ.</li>
            <li>• <b>డ్రోన్ పాలసీ 4.0:</b> ఓర్వకల్లు (కర్నూలు జిల్లా) లో 300 ఎకరాల్లో దేశంలోనే అతిపెద్ద 'డ్రోన్ సిటీ' నిర్మాణం. 40,000 ఉద్యోగాలు, 25,000 మంది సర్టిఫైడ్ డ్రోన్ పైలట్ల శిక్షణ. FPO లకు డ్రోన్ స్ప్రేయింగ్‌పై 80% సబ్సిడీ.</li>
          </ul>
        </div>

        <!-- Policy 6: Data Centers & Maritime Ports 4.0 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-emerald-400 bg-emerald-400/10 px-2.5 py-0.5 rounded border border-emerald-400/20">పాలసీ 11 & 12</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">డేటా సెంటర్స్ (G.O.6) & సముద్ర రంగ పోర్టులు 4.0</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>డేటా సెంటర్ విధానం:</b> 975 కి.మీ తీర సబ్‌మెరైన్ కేబుల్స్ ఆధారంగా ఏఐ హైపర్‌స్కేల్ డేటా హబ్స్. వైజాగ్‌లో రైడెన్ ఇన్ఫోటెక్ అదానీ మెగా క్యాంపస్ (480 ఎకరాలు, ₹22,002 కోట్లు). గూగుల్ ఏఐ హబ్ ప్రతిపాదన.</li>
            <li>• <b>మారిటైమ్ పాలసీ 4.0:</b> 1,053 కి.మీ తీరరేఖ. డిసెంబర్ 2026 నాటికి 4 కొత్త నాన్-మేజర్ పోర్టులు: రామాయపట్నం (ప్రకాశం), మచిలీపట్నం (కృష్ణా), మూలపేట (శ్రీకాకుళం), కాకినాడ గేట్‌వే పోర్ట్.</li>
          </ul>
        </div>

      </div>
    </section>

    <!-- ==================== TAB 3: MENTAL ABILITY & APTITUDE ==================== -->
    <section id="content-aptitude" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-purple-950 via-slate-800 to-slate-900 border border-purple-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-purple-900/60 text-purple-300 px-3 py-1 rounded-full border border-purple-700/50">APPSC Group 2 ప్రిలిమ్స్ • 30 మార్కులు</span>
          <span class="text-xs text-slate-400">120+ షార్ట్‌కట్స్, ఫార్ములాలు & ఉదాహరణలతో కూడిన నోట్స్</span>
        </div>
        <h2 class="text-2xl font-black text-white">క్వాంటిటేటివ్ ఆప్టిట్యూడ్ & మెంటల్ ఎబిలిటీ మాస్టర్ బుక్‌లెట్</h2>
        <p class="text-sm text-slate-300 mt-1">పరీక్షల్లో కాలిక్యులేటర్ లేకుండా సెకన్లలో సమాధానం సాధించడానికి క్షేత్రమితి, ప్రస్తారాలు, రైళ్లు, మిశ్రమాలు, పైపులు, చక్రవడ్డీ, రీజనింగ్ షార్ట్‌కట్లు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">

        <!-- Mensuration 2D & 3D -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-purple-400 bg-purple-400/10 px-2.5 py-0.5 rounded border border-purple-400/20">అధ్యాయం 01</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">క్షేత్రమితి ఫార్ములాలు (Mensuration 2D & 3D)</h3>
          <div class="space-y-2 text-xs text-slate-300 leading-relaxed font-mono">
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-amber-300 font-bold font-sans">2D సమతల పటాలు:</p>
              <p>• చతురస్రం: వైశాల్యం = a² = ½ d² | కర్ణం = a√2</p>
              <p>• దీర్ఘచతురస్రం: వైశాల్యం = l × b | కర్ణం = √(l² + b²)</p>
              <p>• సమబాహు త్రిభుజం: వైశాల్యం = (√3 / 4) a² | ఎత్తు = (√3 / 2) a</p>
              <p>• రాంబస్: వైశాల్యం = ½ × d₁ × d₂ | భుజం = ½ √(d₁² + d₂²)</p>
              <p>• ట్రెపీజియం: వైశాల్యం = ½ (a + b) × h</p>
              <p>• అర్ధవృత్తం చుట్టుకొలత = πr + 2r = r(π + 2) ≈ (36 / 7) r</p>
            </div>
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-purple-300 font-bold font-sans">3D ఘనరూపాలు & గోల్డెన్ రూల్:</p>
              <p>• స్థూపం (Cylinder): V = πr²h | CSA = 2πrh | TSA = 2πr(h + r)</p>
              <p>• శంకువు (Cone): V = ⅓ πr²h | వాలు ఎత్తు l = √(r² + h²)</p>
              <p>• గోళం (Sphere): V = ⁴⁄₃ πr³ | ఉపరితల వైశాల్యం = 4πr²</p>
              <p>• అర్ధగోళం (Hemisphere): V = ⅔ πr³ | TSA = 3πr²</p>
              <p class="text-emerald-400 font-bold font-sans mt-1">⭐ గోల్డెన్ స్కేలింగ్ రూల్: కొలత k రెట్లు పెరిగితే → వైశాల్యం k² రెట్లు, ఘనపరిమాణం k³ రెట్లు పెరుగుతుంది!</p>
            </div>
          </div>
        </div>

        <!-- Trains, Speed, Work & Pipes -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-purple-400 bg-purple-400/10 px-2.5 py-0.5 rounded border border-purple-400/20">అధ్యాయం 02 & 03</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">రైళ్లు, కాలం-పని, పైపులు & వేగం (Speed & Work)</h3>
          <div class="space-y-2 text-xs text-slate-300 leading-relaxed font-mono">
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-amber-300 font-bold font-sans">రైళ్లు & వేగం:</p>
              <p>• km/h → m/s: వేగం × (5 / 18) | m/s → km/h: వేగం × (18 / 5)</p>
              <p>• స్తంభాన్ని దాటడం: కాలం = రైలు పొడవు (L) / వేగం (S)</p>
              <p>• ప్లాట్‌ఫారమ్ దాటడం: కాలం = (L + P) / S</p>
              <p>• ఎదురెదురుగా వస్తే (Opposite): సాపేక్ష వేగం = S₁ + S₂</p>
              <p>• ఒకే దిశలో వెళితే (Same): సాపేక్ష వేగం = S₁ - S₂</p>
              <p>• రెండు రైళ్లు దాటడం: కాలం = (L₁ + L₂) / (సాపేక్ష వేగం)</p>
            </div>
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-purple-300 font-bold font-sans">కాలం-పని & పైపులు:</p>
              <p>• ఇద్దరు కలిసి పూర్తి చేసే కాలం = (x × y) / (x + y)</p>
              <p>• చైన్ రూల్ (MDH): (M₁ × D₁ × H₁) / W₁ = (M₂ × D₂ × H₂) / W₂</p>
              <p>• పైపు నింపే వేళ లీక్ ఖాళీ చేసే కాలం = (x × y) / (y - x)</p>
              <p>• పడవ ప్రవాహ వేగాలు: డౌన్‌స్ట్రీమ్ D = u + v | అప్‌స్ట్రీమ్ U = u - v</p>
              <p>• నిశ్చల నీటిలో పడవ వేగం u = (D + U) / 2 | ప్రవాహ వేగం v = (D - U) / 2</p>
            </div>
          </div>
        </div>

        <!-- Interest, Ratios & Alligations -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-purple-400 bg-purple-400/10 px-2.5 py-0.5 rounded border border-purple-400/20">అధ్యాయం 04 & 05</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">బారువడ్డీ, చక్రవడ్డీ, మిశ్రమాలు & నిష్పత్తి</h3>
          <div class="space-y-2 text-xs text-slate-300 leading-relaxed font-mono">
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-amber-300 font-bold font-sans">చక్రవడ్డీ & బారువడ్డీ తేడాలు:</p>
              <p>• 2 సంవత్సరాలకు CI - SI తేడా (D) = P × (R / 100)²</p>
              <p>• 3 సంవత్సరాలకు CI - SI తేడా = P (R / 100)² × [(300 + R) / 100]</p>
              <p>• SI లో సొమ్ము N రెట్లు కావడానికి: R × T = (N - 1) × 100</p>
              <p class="text-emerald-400 font-bold font-sans">⭐ రూల్ ఆఫ్ 72: చక్రవడ్డీలో సొమ్ము రెట్టింపు కావడానికి పట్టే కాలం ≈ 72 / R</p>
            </div>
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-purple-300 font-bold font-sans">మిశ్రమాలు & లాభనష్టాలు:</p>
              <p>• రిపీటెడ్ రీప్లేస్‌మెంట్: మిగిలిన ద్రవం = ప్రారంభ పరిమాణం × [1 - (x / V)]ⁿ</p>
              <p>• సేమ్ SP ట్రిక్: ఒకదానిపై x% లాభం, ఇంకోదానిపై x% నష్టం వస్తే → నికర నష్టం = (x / 10)² %</p>
              <p>• హస్తలాఘవాలు (Handshakes) = ⁿC₂ = n(n - 1) / 2</p>
              <p>• బహుభుజి కర్ణాలు = ⁿC₂ - n = [n(n - 3)] / 2</p>
            </div>
          </div>
        </div>

        <!-- Clocks, Calendar & Reasoning -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-2">
            <span class="text-xs font-black text-purple-400 bg-purple-400/10 px-2.5 py-0.5 rounded border border-purple-400/20">అధ్యాయం 06 & 07</span>
            <label class="flex items-center gap-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded accent-emerald-500 w-4 h-4" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <h3 class="text-base font-bold text-white mb-2">గడియారాలు, క్యాలెండర్ & లాజికల్ రీజనింగ్</h3>
          <div class="space-y-2 text-xs text-slate-300 leading-relaxed font-mono">
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-amber-300 font-bold font-sans">గడియారాల మాస్టర్ ఫార్ములా:</p>
              <p class="text-amber-400 font-bold text-sm">కోణం (θ) = | 30H - (11/2) M |</p>
              <p>• ఏకీభవించడం (0°): 12 గంటల్లో 11 సార్లు, 24 గంటల్లో 22 సార్లు</p>
              <p>• లంబకోణం (90°): 12 గంటల్లో 22 సార్లు, 24 గంటల్లో 44 సార్లు</p>
              <p>• నిమిషాల ముల్లు వేగం = 6°/నిమిషం | గంటల ముల్లు వేగం = ½°/నిమిషం</p>
            </div>
            <div class="bg-slate-900/80 p-2.5 rounded-lg border border-slate-700">
              <p class="text-purple-300 font-bold font-sans">క్యాలెండర్ & ఆడ్ డేస్:</p>
              <p>• సాధారణ సంవత్సరం = 1 ఆడ్ డే | లీపు సంవత్సరం = 2 ఆడ్ డేస్</p>
              <p>• శతాబ్దపు చివరి రోజు మంగళ, గురు, శనివారం ఎప్పటికీ కాజాలదు!</p>
              <p>• డే ఇండెక్స్ = [తేదీ + నెల కోడ్ + శతాబ్ద కోడ్ + చివరి 2 అంకెలు + లీపులు] ÷ 7</p>
              <p>• నెల కోడ్స్: 033 614 625 035 | శతాబ్దాలు: 1600=6, 1700=4, 1800=2, 1900=0, 2000=6</p>
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ==================== TAB 4: HISTORY ==================== -->
    <section id="content-history" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-amber-950 via-slate-800 to-slate-900 border border-amber-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-amber-900/60 text-amber-300 px-3 py-1 rounded-full border border-amber-700/50">చరిత్ర విభాగం • 30 మార్కులు</span>
          <span class="text-xs text-slate-400">ప్రాచీన, మధ్యయుగ, ఆధునిక భారతం & సమగ్ర ఆంధ్రప్రదేశ్ చరిత్ర</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారత & ఆంధ్రప్రదేశ్ చరిత్ర సమగ్ర గైడ్ (History Master Guide)</h2>
        <p class="text-sm text-slate-300 mt-1">సింధు నాగరికత, మౌర్యులు, గుప్తులు, విజయనగరం, 1857 తిరుగుబాటు, జాతీయోద్యమం, సాతవాహనులు, కాకతీయులు మరియు 1953 ఆంధ్ర రాష్ట్రం నుండి 2014 విభజన వరకు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-amber-300 mb-2">📜 ప్రాచీన & మధ్యయుగ భారతం</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>సింధు లోయ (క్రీ.పూ. 2500–1750):</b> హరప్పా, మొహెంజోదారో, గ్రిడ్ సిస్టమ్ డ్రైనేజీ, కాంస్య నర్తకి, గొప్ప స్నానవాటిక.</li>
            <li>• <b>మౌర్యులు (క్రీ.పూ. 322):</b> చంద్రగుప్త మౌర్యుడు, కౌటిల్యుని అర్థశాస్త్రం. అశోకుని కళింగ యుద్ధం (క్రీ.పూ. 261), ధమ్మ శాసనాలు, స్తూపాలు.</li>
            <li>• <b>గుప్తుల స్వర్ణయుగం:</b> సముద్రగుప్తుడు (అలహాబాద్ ప్రశస్తి), చంద్రగుప్త-II విక్రమాదిత్యుడు, ఆర్యభట్ట (సూర్య సిద్ధాంతం), కాళిదాసు.</li>
            <li>• <b>విజయనగర సామ్రాజ్యం (1336):</b> హరిహర & బుక్కరాయలు. శ్రీకృష్ణదేవరాయలు (1509–29) అముక్తమాల్యద, అష్టదిగ్గజాలు. 1565 తాలికోట యుద్ధం (రాక్షస తంగడి).</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-amber-300 mb-2">🚩 ఆధునిక జాతీయోద్యమం & గాంధేయ యుగం</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>కీలక యుద్ధాలు:</b> 1757 ప్లాసీ యుద్ధం (సిరాజ్-ఉద్-దౌలా), 1764 బక్సార్ యుద్ధం (దివానీ హక్కులు), డాక్ట్రిన్ ఆఫ్ లాప్స్ (డల్హౌసీ).</li>
            <li>• <b>1857 ప్రథమ స్వాతంత్ర్య సంగ్రామం:</b> మీరట్ మే 10, ఎన్‌ఫీల్డ్ తూటాలు. బహదూర్ షా జఫర్, ఝాన్సీ లక్ష్మీబాయి, తాంతియాతోపే. 1858 విక్టోరియా రాణి ప్రకటన.</li>
            <li>• <b>జాతీయోద్యమ మైలురాళ్లు:</b> 1885 కాంగ్రెస్ స్థాపన (A.O. హ్యూమ్, డబ్ల్యూ.సి. బెనర్జీ), 1905 వంగభంగం (వందేమాతరం), 1919 జలియన్ వాలాబాగ్ (జనరల్ డయర్, రౌలట్ చట్టం), 1920 అసహాయ నిరాకరణ, 1930 ఉప్పు సత్యాగ్రహం (దండి మార్చ్), 1942 క్విట్ ఇండియా ('డూ ఆర్ డై').</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm md:col-span-2">
          <h3 class="text-base font-bold text-amber-300 mb-2">🏛️ సమగ్ర ఆంధ్రప్రదేశ్ చరిత్ర & ఉద్యమాలు</h3>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs text-slate-300">
            <div>
              <p class="font-bold text-white mb-1">ప్రాచీన & మధ్యయుగ ఆంధ్ర:</p>
              <p>• <b>సాతవాహనులు (క్రీ.పూ. 1వ శతాబ్దం):</b> ధాన్యకటకం / ప్రతిష్ఠానం. గౌతమీపుత్ర శాతకర్ణి, హాలుని గాథాసప్తశతి. అమరావతి శిల్పకళ.</p>
              <p>• <b>ఇక్ష్వాకులు & విష్ణుకుండినులు:</b> నాగార్జునకొండ విజయపురి, ఉండవల్లి గుహలు.</p>
              <p>• <b>కాకతీయులు:</b> ప్రతాపరుద్రుడు, రాణి రుద్రమదేవి, మోటుపల్లి అభయ శాసనం, రామప్ప ఆలయం (యునెస్కో సైట్).</p>
            </div>
            <div>
              <p class="font-bold text-white mb-1">ఆధునిక ఆంధ్ర & విభజన చరిత్ర:</p>
              <p>• <b>సంస్కర్తలు:</b> కందుకూరి వీరేశలింగం (వితంతు వివాహాలు, హితకారిణి), గురజాడ (కన్యాశుల్కం).</p>
              <p>• <b>మన్యం విప్లవం (1922-24):</b> అల్లూరి సీతారామరాజు రంప తిరుగుబాటు.</p>
              <p>• <b>ఆంధ్ర రాష్ట్ర అవతరణ:</b> పొట్టి శ్రీరాములు 58 రోజుల ఆమరణ నిరాహారదీక్ష (1952 డిసెంబర్ 15 అమరత్వం). 1953 అక్టోబర్ 1 కర్నూలు రాజధానిగా ఆంధ్ర రాష్ట్రం. 1956 నవంబర్ 1 హైదరాబాద్ రాజధానిగా ఆంధ్రప్రదేశ్.</p>
              <p>• <b>2014 పునర్విభజన చట్టం:</b> 2014 జూన్ 2 తెలంగాణ విభజన. 12 భాగాలు, 108 సెక్షన్లు.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 5: POLITY ==================== -->
    <section id="content-polity" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-red-950 via-slate-800 to-slate-900 border border-red-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-red-900/60 text-red-300 px-3 py-1 rounded-full border border-red-700/50">పాలిటీ విభాగం • స్కోరింగ్ ఏరియా</span>
          <span class="text-xs text-slate-400">భారత రాజ్యాంగం, ప్రాథమిక హక్కులు, ఆదేశిక సూత్రాలు, కీలక అధికరణాలు</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారత రాజ్యాంగం, పాలన & ముఖ్య అధికరణాల హ్యాండ్‌బుక్</h2>
        <p class="text-sm text-slate-300 mt-1">1949 నవంబర్ 26 ఆమోదం, 1950 జనవరి 26 అమలు. 25 భాగాలు, 12 షెడ్యూల్స్, 470+ ఆర్టికల్స్ మరియు మైలురాయి తీర్పులు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Fundamental Rights & DPSP -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-rose-300 mb-2">⚖️ ప్రాథమిక హక్కులు (12–35) & DPSP (36–51)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>ఆర్టికల్ 14:</b> చట్టం ముందు సమానత్వం (Equality before law).</li>
            <li>• <b>ఆర్టికల్ 17:</b> అంటరానితనం నిర్మూలన (Abolition of Untouchability).</li>
            <li>• <b>ఆర్టికల్ 19:</b> 6 ప్రాథమిక స్వేచ్ఛలు (భాషణ, సమావేశం, సంఘం, సంచారం, నివాసం, వృత్తి).</li>
            <li>• <b>ఆర్టికల్ 21:</b> జీవించే హక్కు & వ్యక్తిగత స్వేచ్ఛ (విద్యా హక్కు 21A, గోప్యతా హక్కు పుట్టస్వామి తీర్పు).</li>
            <li>• <b>ఆర్టికల్ 32:</b> రాజ్యాంగ పరిహార హక్కు (డా. అంబేద్కర్ "రాజ్యాంగం హృదయం & ఆత్మ" అన్నారు; 5 రిట్లు).</li>
            <li>• <b>ఆర్టికల్ 40:</b> గ్రామ పంచాయతీల ఏర్పాటు (గాంధేయ సూత్రం).</li>
            <li>• <b>ఆర్టికల్ 44:</b> ఉమ్మడి పౌరస్మృతి (Uniform Civil Code - UCC).</li>
            <li>• <b>ఆర్టికల్ 48A:</b> పర్యావరణ పరిరక్షణ & అడవుల రక్షణ.</li>
            <li>• <b>ఆర్టికల్ 51A:</b> 11 ప్రాథమిక విధులు (42వ సవరణ 1976 స్వరణ్ సింగ్ కమిటీ).</li>
          </ul>
        </div>

        <!-- Centre-State & Landmark Amendments -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-rose-300 mb-2">🏛️ కేంద్ర-రాష్ట్ర సంబంధాలు, అత్యవసరాలు & సవరణలు</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>అత్యవసర అధికారాలు:</b> జాతీయ అత్యవసర పరిస్థితి (ఆర్టికల్ 352), రాష్ట్రపతి పాలన (ఆర్టికల్ 356 - ఎస్.ఆర్. బొమ్మై కేసు పరిమితులు), ఆర్థిక అత్యవసర పరిస్థితి (ఆర్టికల్ 360 - ఇప్పటివరకు విధించలేదు).</li>
            <li>• <b>73 & 74వ సవరణలు (1992):</b> పంచాయతీరాజ్ (11వ షెడ్యూల్ 29 అంశాలు), నగరపాలికలు (12వ షెడ్యూల్ 18 అంశాలు). బల్వంత్ రాయ్ మెహతా (3 అంచెలు), అశోక్ మెహతా (2 అంచెలు).</li>
            <li>• <b>42వ సవరణ (1976 - మినీ రాజ్యాంగం):</b> ప్రవేశికలో 'సోషలిస్టు, లౌకిక, సమగ్రత' పదాల చేరిక.</li>
            <li>• <b>44వ సవరణ (1978):</b> ఆస్తి హక్కు ప్రాథమిక హక్కుల నుంచి తొలగింపు (ఇప్పుడు 300A చట్టబద్ధ హక్కు).</li>
            <li>• <b>101వ సవరణ (2016):</b> వస్తు సేవల పన్ను (GST).</li>
            <li>• <b>కేశవానంద భారతి (1973):</b> రాజ్యాంగ ప్రాథమిక స్వరూప సిద్ధాంతం (Basic Structure Doctrine).</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 6: ECONOMY ==================== -->
    <section id="content-economy" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-amber-950 via-slate-800 to-slate-900 border border-amber-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-amber-900/60 text-amber-300 px-3 py-1 rounded-full border border-amber-700/50">ఆర్థిక వ్యవస్థ & ద్రవ్య మార్కెట్లు</span>
          <span class="text-xs text-slate-400">మనీ మార్కెట్, T-Bills, RBI, బడ్జెట్ & నీతి ఆయోగ్ రిపోర్టులు</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారత & ఏపీ ఆర్థిక వ్యవస్థ (Economy & Financial Markets)</h2>
        <p class="text-sm text-slate-300 mt-1">ద్రవ్య మార్కెట్ వర్గీకరణ, ట్రెజరీ బిల్స్, కాల్ మనీ, కమర్షియల్ పేపర్, సర్టిఫికేట్ ఆఫ్ డిపాజిట్ మరియు నీతి ఆయోగ్ ర్యాంకింగ్స్.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Financial Markets -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-amber-300 mb-2">📈 భారతీయ ద్రవ్య మార్కెట్ సాధనాలు (Money Market)</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>ట్రెజరీ బిల్స్ (T-Bills):</b> కేంద్ర ప్రభుత్వం మాత్రమే జారీ చేస్తుంది (జీరో-కూపన్ బాండ్లు, డిస్కౌంట్‌కు జారీ). 91-రోజులు, 182-రోజులు, 364-రోజులు. గిల్ట్-ఎడ్జ్డ్ సావరిన్ హామీ. కనీసం ₹25,000.</li>
            <li>• <b>కాల్ మనీ & నోటీస్ మనీ:</b> ఓవర్‌నైట్ (1 రోజు) = కాల్ మనీ; 2 నుండి 14 రోజులు = నోటీస్ మనీ; 15 రోజుల పైన = టర్మ్ మనీ. పూచీకత్తు లేని (Unsecured) ఇంటర్‌బ్యాంక్ మార్కెట్.</li>
            <li>• <b>కమర్షియల్ పేపర్ (CP):</b> కార్పొరేట్ కంపెనీలు జారీ చేసే ప్రామిసరీ నోట్ (7 రోజుల నుండి 1 సంవత్సరం). కనీసం ₹5 లక్షలు. నెట్ వర్త్ కనీసం ₹4 కోట్లు ఉండాలి.</li>
            <li>• <b>క్యాష్ మేనేజ్‌మెంట్ బిల్స్ (CMBs):</b> 91 రోజుల కంటే తక్కువ వ్యవధికి కేంద్ర ప్రభుత్వం అకస్మాత్తు నగదు సర్దుబాటు కోసం 2010 నుంచి ప్రవేశపెట్టిన సాధనం.</li>
            <li>• <b>సర్టిఫికేట్ ఆఫ్ డిపాజిట్ (CD):</b> బ్యాంకులు (7 రోజుల నుండి 1 సం.) లేదా ఆర్థిక సంస్థలు (1-3 సం.) జారీ చేసే బదిలీ చేయగల డిపాజిట్ పత్రం. కనీసం ₹5 లక్షలు.</li>
          </ul>
        </div>

        <!-- Macro Economy & NITI Aayog -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-amber-300 mb-2">📊 స్థూల ఆర్థిక సూచికలు & నీతి ఆయోగ్ రిపోర్టులు</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>జాతీయ ఆదాయం:</b> GDP = దేశంలో ఉత్పత్తి అయిన అంతిమ వస్తుసేవల విలువ. సేవా రంగం వాటా అత్యధికం (>54%). 1991 లో LPG సంస్కరణలు (ఉదారీకరణ, ప్రైవేటీకరణ, ప్రపంచీకరణ).</li>
            <li>• <b>RBI ద్రవ్య విధానం:</b> 1935 లో స్థాపన. రెపో రేటు (బ్యాంకులకు RBI ఇచ్చే వడ్డీ), రివర్స్ రెపో, CRR (నగదు నిల్వల నిష్పత్తి), SLR (స్టాట్యుటరీ లిక్విడిటీ రేషియో).</li>
            <li>• <b>NITI Aayog SDG India Index:</b> 16 లక్ష్యాలు. కేరళ, ఉత్తరాఖండ్ టాప్. స్కోర్ 0-100 (ఆస్పిరెంట్, పెర్ఫార్మర్, ఫ్రంట్ రన్నర్, అచీవర్).</li>
            <li>• <b>National MPI:</b> ఆల్కీర్-ఫాస్టర్ పద్ధతి (ఆరోగ్యం, విద్య, జీవన ప్రమాణం - 12 సూచికలు).</li>
            <li>• <b>పోటీతత్వ సూచిక:</b> 2026 IMD World Competitiveness లో భారత్ 44వ స్థానం (సింగపూర్ 1వ స్థానం).</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 7: SCIENCE & ENVIRONMENT ==================== -->
    <section id="content-science" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-teal-950 via-slate-800 to-slate-900 border border-teal-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-teal-900/60 text-teal-300 px-3 py-1 rounded-full border border-teal-700/50">సైన్స్, పర్యావరణం & విపత్తులు</span>
          <span class="text-xs text-slate-400">ISRO, DRDO, బయోటెక్నాలజీ, పర్యావరణ ఒప్పందాలు, నదీ జల వివాదాలు</span>
        </div>
        <h2 class="text-2xl font-black text-white">సైన్స్, టెక్నాలజీ, ఎకాలజీ & విపత్తు నిర్వహణ గైడ్</h2>
        <p class="text-sm text-slate-300 mt-1">చంద్రయాన్-3, ఆదిత్య-L1, క్షిపణులు, పర్యావరణ పరిరక్షణ చట్టాలు, రామ్‌సర్ సైట్లు మరియు కృష్ణా-గోదావరి ట్రిబ్యునల్స్.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-teal-300 mb-2">🚀 స్పేస్, డిఫెన్స్ & ఐటీ టెక్నాలజీ</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>ISRO మిషన్లు:</b> చంద్రయాన్-3 (2023 ఆగస్టు 23 శివశక్తి పాయింట్ సాఫ్ట్ ల్యాండింగ్), ఆదిత్య-L1 (సూర్యుడి అధ్యయనం లగ్రాంజ్ పాయింట్ 1), గగన్‌యాన్ (మానవసహిత మిషన్). శ్రీహరికోట సతీష్ ధవన్ స్పేస్ సెంటర్.</li>
            <li>• <b>DRDO క్షిపణులు:</b> అగ్ని (బాలిస్టిక్, అగ్ని-5 ఖండాంతర క్షిపణి 5000+ కి.మీ), పృథ్వీ (ఉపరితలం నుండి ఉపరితలం), ఆకాశ్ (వాయు రక్షణ), నాగ్ (యాంటీ-ట్యాంక్), బ్రహ్మోస్ (సూపర్ సోనిక్ క్రూయిజ్ - భారత్-రష్యా ఉమ్మడి భాగస్వామ్యం).</li>
            <li>• <b>డిజిటల్ టెక్:</b> ఆధార్, UPI, 5G, కృత్రిమ మేధస్సు (AI), బ్లాక్‌చెయిన్, సైబర్ సెక్యూరిటీ (CERT-In).</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-teal-300 mb-2">🌿 పర్యావరణం, విపత్తులు & నదీ వివాదాలు</h3>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>• <b>పర్యావరణ ఒప్పందాలు:</b> స్టాక్‌హోమ్ 1972, రియో ఎర్త్ సమ్మిట్ 1992, క్యోటో ప్రోటోకాల్ (గ్రీన్‌హౌస్ వాయువులు), మాంట్రియల్ ప్రోటోకాల్ (ఓజోన్ రక్షణ), ప్యారిస్ ఒప్పందం 2015 (నెట్ జీరో 2070 భారత్ లక్ష్యం).</li>
            <li>• <b>విపత్తు నిర్వహణ:</b> విపత్తు నిర్వహణ చట్టం 2005 (NDMA చైర్మన్ ప్రధానమంత్రి, SDMA చైర్మన్ ముఖ్యమంత్రి, DDMA కలెక్టర్). NDRF దళాలు.</li>
            <li>• <b>నదీ జల వివాదాల ట్రిబ్యునల్స్ (ఆర్టికల్ 262):</b> కృష్ణా ట్రిబ్యునల్-I (బచావత్ 1969-76), కృష్ణా ట్రిబ్యునల్-II (బ్రిజేష్ కుమార్ 2004-10), గోదావరి ట్రిబ్యునల్ (1969-80). విభజనానంతరం KRMB & GRMB బోర్డులు.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 8: MAINS & ETHICS ==================== -->
    <section id="content-mains" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-pink-950 via-slate-800 to-slate-900 border border-pink-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-pink-900/60 text-pink-300 px-3 py-1 rounded-full border border-pink-700/50">APPSC Group 1 Mains & Interview Special</span>
          <span class="text-xs text-slate-400">డిస్క్రిప్టివ్ ఆన్సర్ రైటింగ్, ఎథిక్స్ కేస్ స్టడీస్ & ఇంటర్వ్యూ వ్యూహం</span>
        </div>
        <h2 class="text-2xl font-black text-white">మెయిన్స్ ఆన్సర్ రైటింగ్, ఎథిక్స్ & పర్సనాలిటీ టెస్ట్ గైడ్</h2>
        <p class="text-sm text-slate-300 mt-1">4-దశల ప్రామాణిక సమాధాన నిర్మాణం, కేస్ స్టడీ అప్రోచ్, పబ్లిక్ సర్వీస్ విలువల సిద్ధాంతాలు మరియు ఇంటర్వ్యూ ప్రవర్తనా నియమాలు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-pink-300 mb-2">✍️ మెయిన్స్ ఆన్సర్ రైటింగ్ 4-దశల స్ట్రక్చర్</h3>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>1. పరిచయం (Introduction - 2-3 లైన్లు):</b> ప్రశ్నలోని కీలక భావన నిర్వచనం, నేపథ్యం లేదా ఇటీవలి సందర్భం.</li>
            <li>• <b>2. ప్రధాన భాగం (Body):</b> కారణాలు, ప్రభావాలు, సవాళ్లు, ప్రభుత్వ చర్యలు. బులెట్ పాయింట్లు, ఉపశీర్షికలు మరియు ఏపీ సంబంధిత ఉదాహరణలతో సమతుల్య విశ్లేషణ.</li>
            <li>• <b>3. ముగింపు (Conclusion):</b> సమస్య పరిష్కారానికి నిర్మాణాత్మక సూచనలు, సకారాత్మక ముగింపు (Forward-looking positive note).</li>
            <li>• <b>సమయ నిర్వహణ:</b> 10% ప్లానింగ్ + 80% రాత + 10% రివిజన్. కఠినమైన ప్రశ్న వద్ద సమయం వృథా చేయకుండా సులభమైన వాటితో ప్రారంభించండి.</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-pink-300 mb-2">⚖️ ఎథిక్స్ సిద్ధాంతాలు, కేస్ స్టడీస్ & ఇంటర్వ్యూ</h3>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>నైతిక సిద్ధాంతాలు:</b> యుటిలిటేరియనిజం (గరిష్ట మందికి గరిష్ట మేలు), డియోంటాలజీ (కర్తవ్యమే ప్రధానం - కాంట్), వర్చ్యూ ఎథిక్స్ (సచ్ఛీలత, నిజాయితీ).</li>
            <li>• <b>కేస్ స్టడీ రాత విధానం:</b> సమస్య గుర్తింపు → వాటాదారులు (Stakeholders) → నైతిక వైరుధ్యాలు (Ethical Dilemmas) → సాధ్యమైన ఎంపికలు → ఉత్తమ చర్య & చట్టపరమైన కారణాలు.</li>
            <li>• <b>పారదర్శకత సాధనాలు:</b> సమాచార హక్కు చట్టం (RTI 2005), లోక్‌పాల్ & లోకాయుక్త, సిటిజన్ చార్టర్.</li>
            <li>• <b>ఇంటర్వ్యూ (Personality Test):</b> DAF (అప్లికేషన్ ఫారమ్) లో రాసిన ప్రతి అంశంపై పట్టు. హోమ్‌ స్టేట్ సమస్యలు, సమతుల్య దృక్పథం, నిజాయితీగా "తెలియదు" అని వినయంగా చెప్పడం.</li>
          </ul>
        </div>
      </div>
    </section>

  
    <!-- ==================== TAB: DISASTER MANAGEMENT (RC REDDY NOTES) ==================== -->
    <section id="content-disaster" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-red-950 via-slate-800 to-slate-900 border border-red-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-red-900/60 text-red-300 px-3 py-1 rounded-full border border-red-700/50">RC రెడ్డి IAS స్టడీ సర్కిల్ • రామన్ రాజు క్లాస్ నోట్స్</span>
          <span class="text-xs text-slate-400">APPSC గ్రూప్ 1, 2, 3, AEE ప్రత్యేకం</span>
        </div>
        <h2 class="text-2xl font-black text-white">విపత్తు నిర్వహణ (Disaster Management) సమగ్ర అధ్యయనం</h2>
        <p class="text-sm text-slate-300 mt-1">నిర్వచనాలు, వైపరీత్యం-దుర్బలత్వం-రిస్క్ సూత్రం, 2005 జాతీయ చట్టం, NDMA, SDMA, DDMA, NDRF 10వ బెటాలియన్, భూకంపాలు, సునామీలు, తుఫానుల వర్గీకరణ & అంతర్జాతీయ ఒప్పందాలు.</p>
      </div>

      <!-- Core Concepts & HPC 1999 Committee -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-red-400 flex items-center gap-2">
              <span>📌 మౌలిక భావనలు & నిర్వచనాలు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>పదోత్పత్తి (Etymology):</b> గ్రీకు/లాటిన్ పదం <i>Dus + Aster</i> లేదా ఫ్రెంచ్ పదం <i>Des + Aster</i> (అనగా <b>"చెడు నక్షత్రం / దుష్ట గ్రహం"</b>).</li>
            <li>• <b>విపత్తు నిర్వహణ చట్టం 2005 నిర్వచనం:</b> ప్రకృతి లేదా మానవ తప్పిదాల వల్ల సంభవించి, సమాజం తనంతట తాను కోలుకోలేని స్థాయిలో అపార ధన, ప్రాణ, పర్యావరణ నష్టం కలిగించే ఉత్పాతాన్ని 'విపత్తు' అంటారు.</li>
            <li>• <b>ఐక్యరాజ్యసమితి (UNO) నిర్వచనం:</b> సమాజపు సాధారణ జీవన విధానాన్ని మరియు వ్యవస్థను తీవ్రంగా అస్తవ్యస్తం చేసే వినాశనం.</li>
            <li>• <b>ఆపద (Risk) గణిత సూత్రం:</b>
              <div class="bg-slate-900/90 p-2.5 rounded-lg my-1.5 border border-slate-700 font-mono text-amber-300 text-center text-xs">
                Risk = (Hazard × Vulnerability) / Capacity<br>
                ఆపద = (వైపరీత్యం × దుర్బలత్వం) / సామర్థ్యం
              </div>
            </li>
            <li>• <b>వైపరీత్యం (Hazard):</b> ప్రమాదాన్ని లేదా నష్టాన్ని కలిగించే సహజ లేదా మానవ ప్రేరిత సంఘటన (ఉదా: తుఫాను, భూకంపం).</li>
            <li>• <b>దుర్బలత్వం (Vulnerability):</b> నష్టానికి గురయ్యే బలహీన పరిస్థితుల సముదాయం (పేదరికం, నాసిరకం భవనాలు, అవగాహనా రాహిత్యం).</li>
            <li>• <b>సామర్థ్యం (Capacity):</b> విపత్తు ప్రభావాన్ని తట్టుకుని నిలబడే వనరులు, సాంకేతికత మరియు సమాజ బలం.</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-red-400 flex items-center gap-2">
              <span>🏛️ జె.సి. పంత్ ఉన్నతాధికార కమిటీ (HPC 1999) & వర్గీకరణ</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <p class="text-xs text-slate-400 mb-2">1999లో వ్యవసాయ మంత్రిత్వ శాఖ నియమించిన <b>J.C. పంత్ ఉన్నతాధికార కమిటీ (HPC)</b> దేశంలోని <b>31 రకాల విపత్తులను 5 ఉప-సమూహాలుగా</b> వర్గీకరించింది:</p>
          <ul class="text-xs text-slate-300 space-y-1.5 leading-relaxed">
            <li>1️⃣ <b>నీరు & వాతావరణ విపత్తులు:</b> తుఫానులు, వరదలు, కరువులు, మేఘ విస్ఫోటనాలు (Cloud bursts), వడగండ్లు, హిమపాతాలు, సముద్ర కోత.</li>
            <li>2️⃣ <b>భౌగోళిక విపత్తులు:</b> భూకంపాలు, సునామీలు, భూపాతాలు (Landslides), అగ్నిపర్వత విస్ఫోటనాలు, డ్యామ్‌లు తెగిపోవడం, గనులలో ప్రమాదాలు.</li>
            <li>3️⃣ <b>రసాయన & పారిశ్రామిక విపత్తులు:</b> విషవాయువు లీకేజీ (ఉదా: భోపాల్ 1984), అగ్నిప్రమాదాలు, చమురు చిందటం.</li>
            <li>4️⃣ <b>జీవసంబంధ విపత్తులు:</b> అంటువ్యాధులు, ప్లేగు, కలరా, జీవాయుధాల దాడి (Anthrax/Smallpox), మిడుతల దండు దాడులు.</li>
            <li>5️⃣ <b>మానవ ప్రేరిత ప్రమాదాలు:</b> రవాణా/రైలు ప్రమాదాలు, తొక్కిసలాటలు (Stampedes), ఉగ్రవాద దాడులు, అణు ప్రమాదాలు.</li>
          </ul>
        </div>
      </div>

      <!-- Institutional Setup & 2005 Act -->
      <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-base font-bold text-amber-400 flex items-center gap-2">
            <span>⚖️ విపత్తు నిర్వహణ చట్టం 2005 & 3-అంచెల సంస్థాగత నిర్మాణం</span>
          </h3>
          <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
            <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
            <span>చదివాను</span>
          </label>
        </div>
        <p class="text-xs text-slate-300 mb-4 leading-relaxed">2004 హిందూ మహాసముద్ర సునామీ అనంతరం, భారత పార్లమెంట్ <b>డిసెంబర్ 23, 2005</b>న విపత్తు నిర్వహణ చట్టాన్ని ఆమోదించింది. ఇది దేశంలో సహాయ వితరణ (Relief-centric) విధానం నుండి ముందస్తు నివారణ & ఉపశమన (Proactive Mitigation) విధానానికి దారితీసింది.</p>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700">
            <h4 class="font-bold text-blue-400 mb-2">1. జాతీయ స్థాయి (NDMA)</h4>
            <ul class="text-slate-300 space-y-1.5">
              <li>• <b>ఛైర్మన్:</b> ప్రధానమంత్రి (ఎక్స్-అఫీషియో)</li>
              <li>• <b>సభ్యులు:</b> గరిష్టంగా 9 మంది సభ్యులు (పీఎం నామినేట్ చేస్తారు)</li>
              <li>• <b>వైస్ ఛైర్మన్:</b> కేంద్ర కేబినెట్ మంత్రి హోదా</li>
              <li>• <b>నోడల్ మంత్రిత్వ శాఖ:</b> కేంద్ర హోం మంత్రిత్వ శాఖ</li>
              <li>• <b>కార్యాలయం:</b> న్యూఢిల్లీ</li>
            </ul>
          </div>

          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700">
            <h4 class="font-bold text-emerald-400 mb-2">2. రాష్ట్ర స్థాయి (SDMA)</h4>
            <ul class="text-slate-300 space-y-1.5">
              <li>• <b>ఛైర్మన్:</b> ముఖ్యమంత్రి (ఎక్స్-అఫీషియో)</li>
              <li>• <b>సభ్యులు:</b> గరిష్టంగా 9 మంది సభ్యులు</li>
              <li>• <b>వైస్ ఛైర్మన్:</b> సీఎం నామినేట్ చేసిన సభ్యుడు</li>
              <li>• <b>రాష్ట్ర కార్యనిర్వాహక కమిటీ (SEC):</b> రాష్ట్ర ప్రభుత్వ ప్రధాన కార్యదర్శి (Chief Secretary) అధ్యక్షత</li>
              <li>• <b>ఏపీ నోడల్ విభాగం:</b> రెవెన్యూ & డిజాస్టర్ మేనేజ్మెంట్</li>
            </ul>
          </div>

          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700">
            <h4 class="font-bold text-purple-400 mb-2">3. జిల్లా స్థాయి (DDMA)</h4>
            <ul class="text-slate-300 space-y-1.5">
              <li>• <b>ఛైర్మన్:</b> జిల్లా కలెక్టర్ / డిస్ట్రిక్ట్ మేజిస్ట్రేట్</li>
              <li>• <b>కో-ఛైర్మన్:</b> జిల్లా పరిషత్ ఛైర్మన్ (Zilla Parishad)</li>
              <li>• <b>సభ్యులు:</b> ఎస్పీ, డీఎంహెచ్ఓ, ఈఈ ఇరిగేషన్ మరియు చీఫ్ ఎగ్జిక్యూటివ్ ఆఫీసర్ (CEO)</li>
              <li>• జిల్లాలోని విపత్తు సహాయక చర్యల ప్రత్యక్ష అమలు అధికారం DDMA కి ఉంటుంది.</li>
            </ul>
          </div>
        </div>

        <div class="mt-4 pt-4 border-t border-slate-700/60 grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-300">
          <div>
            <span class="font-bold text-amber-300">🎖️ NDRF (జాతీయ విపత్తు ప్రతిస్పందన దళం):</span> సెక్షన్ 44 ప్రకారం CRPF, CISF, BSF, ITBP నుండి ఏర్పాటైన సుశిక్షిత దళం. మొదట 10 బెటాలియన్లు కాగా, ప్రస్తుతం 16 బెటాలియన్లు ఉన్నాయి. ఆంధ్రప్రదేశ్‌కు కేటాయించబడిన బెటాలియన్: <b>10వ బెటాలియన్ (మంగళగిరి / కొండపల్లి, గుంటూరు-కృష్ణా)</b>.
          </div>
          <div>
            <span class="font-bold text-amber-300">🏢 NIDM (నేషనల్ ఇన్‌స్టిట్యూట్ ఆఫ్ డిజాస్టర్ మేనేజ్మెంట్):</span> న్యూఢిల్లీలో ప్రధాన కేంద్రం, విపత్తు నిర్వహణపై అధికారులు, రెస్క్యూ టీంలకు శిక్షణ, డాక్యుమెంటేషన్ మరియు విధాన పరిశోధన అందిస్తుంది.
          </div>
        </div>
      </div>

      <!-- Natural Disasters Deep-Dive -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Earthquakes & Tsunamis -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-red-300 flex items-center gap-2">
              <span>🌋 భూకంపాలు & సునామీలు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>భూకంప నాభి (Hypocenter/Focus):</b> భూ అంతర్భాగంలో భూకంప తరంగాలు జనించే కేంద్ర బిందువు.</li>
            <li>• <b>భూకంప అధికేంద్రం (Epicenter):</b> భూ ఉపరితలంపై నాభికి సరిగ్గా నిట్టనిలువుగా ఉండే ప్రాంతం (ఇక్కడ నష్టం గరిష్టం).</li>
            <li>• <b>తరంగాలు:</b>
              <br>1. <b>P-తరంగాలు (ప్రాథమిక):</b> అనుదైర్ఘ్య (ధ్వని వంటివి), వేగం 6-13 km/s, ఘన, ద్రవ, వాయువుల్లో ప్రయాణిస్తాయి.
              <br>2. <b>S-తరంగాలు (ద్వితీయ):</b> తిర్యక్ (కాంతి వంటివి), వేగం 4-7 km/s, ఘన పదార్థాల్లో మాత్రమే ప్రయాణిస్తాయి.
              <br>3. <b>L-తరంగాలు (ఉపరితల / లవ్ / రేలే):</b> భూ ఉపరితలంపై ప్రయాణించి అత్యధిక విధ్వంసాన్ని సృష్టిస్తాయి.
            </li>
            <li>• <b>కొలిచే సాధనాలు:</b>
              <br>• <b>రిక్టర్ స్కేల్ (1935):</b> పరిమాణం (Magnitude - విడుదలైన శక్తి) కొలుస్తుంది. లాగరిథమిక్ స్కేలు (0-9).
              <br>• <b>మెర్కల్లి స్కేల్ (1902):</b> తీవ్రత (Intensity - జరిగిన నష్టం) ఆధారంగా 1 నుండి 12 రోమన్ సంఖ్యల్లో కొలుస్తారు.
            </li>
            <li>• <b>భారత సిస్మిక్ జోన్లు:</b> బ్యూరో ఆఫ్ ఇండియన్ స్టాండర్డ్స్ (BIS) ప్రకారం 4 జోన్లు ఉన్నాయి (Zone II, III, IV, V). దేశంలో దాదాపు <b>59% భూభాగం</b> భూకంప ప్రమాద జోన్లలో ఉంది. జోన్ V అత్యంత ప్రమాదకరమైనది (హిమాలయాలు, ఈశాన్య రాష్ట్రాలు, కచ్).</li>
            <li>• <b>సునామీ (Tsunami):</b> జపనీస్ పదం (Tsu = రేవు/తీరం, Nami = అల). <b>26 డిసెంబర్ 2004</b> సుమత్రా భూకంపం (9.1 M) వల్ల వచ్చిన సునామీతో భారత్‌లో 10,000+ మంది ప్రాణాలు కోల్పోయారు.</li>
            <li>• <b>ITEWC:</b> ఇండియన్ సునామీ ఎర్లీ వార్నింగ్ సెంటర్ <b>INCOIS (హైదరాబాద్)</b> లో 2007లో ఏర్పాటయింది.</li>
          </ul>
        </div>

        <!-- Cyclones, Floods & Droughts -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-blue-300 flex items-center gap-2">
              <span>🌀 తుఫానులు, వరదలు & కరువు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>భారత వాతావరణ శాఖ (IMD) తుఫానుల వర్గీకరణ:</b>
              <div class="overflow-x-auto my-1.5">
                <table class="w-full text-[11px] text-left border border-slate-700 rounded">
                  <tr class="bg-slate-900 text-amber-400 font-bold"><th class="p-1">దశ</th><th class="p-1">గాలి వేగం (kmph)</th></tr>
                  <tr class="border-b border-slate-700"><td class="p-1">అల్పపీడనం (Low Pressure)</td><td class="p-1">&lt; 31</td></tr>
                  <tr class="border-b border-slate-700"><td class="p-1">వాయుగుండం (Depression)</td><td class="p-1">31 - 49</td></tr>
                  <tr class="border-b border-slate-700"><td class="p-1">తీవ్ర వాయుగుండం (Deep Depression)</td><td class="p-1">49 - 61</td></tr>
                  <tr class="border-b border-slate-700"><td class="p-1">సైక్లోనిక్ స్టార్మ్ (తుఫాను)</td><td class="p-1">62 - 88</td></tr>
                  <tr class="border-b border-slate-700"><td class="p-1">తీవ్ర తుఫాను (Severe Cyclone)</td><td class="p-1">89 - 117</td></tr>
                  <tr class="border-b border-slate-700"><td class="p-1">అతి తీవ్ర తుఫాను (Very Severe)</td><td class="p-1">118 - 221</td></tr>
                  <tr class="bg-red-950/60 text-red-300 font-bold"><td class="p-1">సూపర్ సైక్లోన్ (Super Cyclone)</td><td class="p-1">≥ 222 (60 m/s)</td></tr>
                </table>
              </div>
            </li>
            <li>• <b>దివిసీమ తుఫాను:</b> <b>నవంబర్ 19, 1977</b>న కృష్ణా జిల్లా దివిసీమను తాకి 10,000 మందికి పైగా మరణానికి కారణమైంది.</li>
            <li>• <b>వరదలు:</b> దేశంలో 40 మిలియన్ హెక్టార్లు (12.5% భూభాగం) వరద ముప్పులో ఉంది. బ్రహ్మపుత్ర, గంగా నదీ పరివాహకాలు అత్యధిక ముప్పు ప్రాంతాలు.</li>
            <li>• <b>కరువు (Drought):</b> IMD ప్రకారం సాధారణ వర్షపాతం కన్నా 26-50% లోటు ఉంటే మధ్యస్థ కరువు, 50% పైగా లోటు ఉంటే తీవ్ర కరువు. దేశ సాగు విస్తీర్ణంలో దాదాపు <b>68% ప్రాంతం</b> ఏదో ఒక స్థాయిలో కరువుకు లోనవుతుంది.</li>
            <li>• <b>పథకాలు:</b> DPAP (Drought Prone Area Programme - 1973), DDP (Desert Development Programme - 1977).</li>
          </ul>
        </div>
      </div>

      <!-- Man-made Disasters & Climate Change Missions -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-amber-300 flex items-center gap-2">
              <span>⚠️ మానవ ప్రేరిత & సాంకేతిక విపత్తులు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>భోపాల్ గ్యాస్ విషాదం (డిసెంబర్ 2-3, 1984):</b> మధ్యప్రదేశ్‌లోని యూనియన్ కార్బైడ్ ఫ్యాక్టరీ నుండి విడుదలైన <b>మిథైల్ ఐసోసైనైట్ (MIC - C₂H₃NO)</b> వాయువు వల్ల 3,000+ మంది తక్షణమే, వేలాది మంది తదనంతరం మరణించారు.</li>
            <li>• <b>అణు ప్రమాదాలు:</b> చెర్నోబిల్ (ఉక్రెయిన్, 1986 - INES లెవెల్ 7), ఫుకుషిమా దైచీ (జపాన్, మార్చి 11, 2011 - INES లెవెల్ 7), త్రీ మైల్ ఐలాండ్ (USA, 1979).</li>
            <li>• <b>జీవాయుధాలు (Biological Warfare - "పేదవారి అణ్వాయుధం"):</b> ఆంత్రాక్స్ (Bacillus anthracis), మశూచి (Smallpox), బొటులిజమ్ విషం.</li>
            <li>• <b>రసాయన ఆయుధాలు:</b> మస్టర్డ్ గ్యాస్, ఫాస్జీన్, సారిన్ గ్యాస్ (టోక్యో సబ్‌వే దాడి 1995), ఏజెంట్ ఆరెంజ్.</li>
            <li>• <b>ఢిల్లీ మాయాపురి రేడియేషన్ సంఘటన (2010):</b> కోబాల్ట్-60 (Co-60) స్క్రాప్ నిర్లక్ష్యం వల్ల రేడియేషన్ వెలువడింది.</li>
            <li>• <b>అగ్ని ప్రమాదాలు & తొక్కిసలాటలు:</b> ఉపహార్ సినిమా హాల్ (ఢిల్లీ 1997 - 59 మృతి), కుంభకోణం స్కూల్ (2004 - 94 మంది పిల్లలు), మంధర్‌దేవి ఆలయం (మహారాష్ట్ర 2005 - 265 మంది మృతి).</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-emerald-300 flex items-center gap-2">
              <span>🌐 అంతర్జాతీయ ఒడంబడికలు & NAPCC 8 మిషన్లు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>యోకోహామా వ్యూహం (Yokohama Strategy 1994):</b> సహజ విపత్తుల నివారణ, ఉపశమనం కోసం జపాన్‌లో ఆమోదించబడిన తొలి కార్యాచరణ ప్రణాళిక.</li>
            <li>• <b>హ్యోగో ఫ్రేమ్‌వర్క్ (Hyogo Framework for Action 2005-2015):</b> విపత్తులను తట్టుకునే దేశాలు, సమాజాల నిర్మాణం కొరకు 168 దేశాలు ఆమోదించిన విధానం.</li>
            <li>• <b>సెండాయ్ ఫ్రేమ్‌వర్క్ (Sendai Framework 2015-2030):</b> 4 ప్రాధాన్యతా రంగాలు, 7 గ్లోబల్ టార్గెట్లతో విపత్తు నష్టాల తగ్గింపు (DRR) లక్ష్యంగా ఏర్పాటయింది.</li>
            <li>• <b>భారత జాతీయ వాతావరణ మార్పుల కార్యాచరణ ప్రణాళిక (NAPCC - 2008):</b>
              <br>మన్మోహన్ సింగ్ ప్రభుత్వం జూన్ 30, 2008న <b>8 జాతీయ మిషన్లను</b> ప్రకటించింది:
              <br>1. నేషనల్ సోలార్ మిషన్
              <br>2. ఎన్‌హాన్స్‌డ్ ఎనర్జీ ఎఫిషియెన్సీ మిషన్
              <br>3. సస్టైనబుల్ హ్యాబిటాట్ మిషన్
              <br>4. నేషనల్ వాటర్ మిషన్
              <br>5. సస్టైనింగ్ హిమాలయన్ ఎకో-సిస్టమ్ మిషన్
              <br>6. గ్రీన్ ఇండియా మిషన్
              <br>7. సస్టైనబుల్ అగ్రికల్చర్ మిషన్
              <br>8. స్ట్రాటజిక్ నాలెడ్జ్ ఫర్ క్లైమేట్ చేంజ్ మిషన్.
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB: SOLVED APPSC PYQS HUB ==================== -->
    <section id="content-pyqs" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-amber-950 via-slate-800 to-slate-900 border border-amber-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-amber-900/60 text-amber-300 px-3 py-1 rounded-full border border-amber-700/50">APPSC అసలైన పరీక్షా ప్రశ్నలు</span>
          <span class="text-xs text-slate-400">Group 1, Group 2, Group 3, AEE, Town Planning Previous Qs</span>
        </div>
        <h2 class="text-2xl font-black text-white">115+ సాల్వ్డ్ APPSC ప్రశ్నలు & సమాధానాల నిధి</h2>
        <p class="text-sm text-slate-300 mt-1">మునుపటి అధికారిక పరీక్షల ప్రశ్నలు. ఆప్షన్ పై క్లిక్ చేయండి - సమాధానం మరియు విశ్లేషణను వెంటనే తెలుసుకోండి!</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5" id="pyqQuizGrid">
        <!-- Q1 -->
        <div class="bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">APPSC Group-II 2012</span>
            <span class="text-xs text-slate-400">Q.1</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">'విపత్తు' (Disaster) అనే పదం ఏ భాషల నుండి ఉద్భవించినది?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'గ్రీకు మరియు లాటిన్ భాషల నుండి Dus+Aster, Dis+Astro పదాల ద్వారా వచ్చింది.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) కేవలం అరబిక్ భాష</button>
            <button onclick="checkPyq(this, false, 'సమాధానం D (పైవన్నీ - గ్రీకు, లాటిన్ మరియు ఫ్రెంచ్ రూపాలు).')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) సంస్కృతం</button>
            <button onclick="checkPyq(this, false, 'గ్రీకు మరియు ఫ్రెంచ్ రెండూ ఉన్నాయి.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) లాటిన్ మాత్రమే</button>
            <button onclick="checkPyq(this, true, 'గ్రీకు (Dus+Aster), లాటిన్ (Dis+Astro), ఫ్రెంచ్ (Des+Aster) మూలాల కలయిక. సరైన జవాబు D!')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) గ్రీకు, లాటిన్ మరియు ఫ్రెంచ్ (పైవన్నీ)</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>

        <!-- Q2 -->
        <div class="bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">Junior Assistant Inter Board 2012</span>
            <span class="text-xs text-slate-400">Q.2</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">భారతదేశ విపత్తు నిర్వహణ చట్టం ఎప్పుడు ఆమోదించబడింది?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, '2004లో సునామీ వచ్చింది, చట్టం 2005లో రూపొందింది.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) 2004</button>
            <button onclick="checkPyq(this, true, 'డిసెంబర్ 23, 2005న రాష్ట్రపతి ఆమోదం పొందింది. 2006 నుంచి అమల్లోకి వచ్చింది.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) 2005</button>
            <button onclick="checkPyq(this, false, '2006లో అమల్లోకి వచ్చింది, కానీ చట్టం 2005 నాటిది.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) 2006</button>
            <button onclick="checkPyq(this, false, 'తప్పు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) 2008</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>

        <!-- Q3 -->
        <div class="bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">Assistant Executive Engineers</span>
            <span class="text-xs text-slate-400">Q.3</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">జాతీయ విపత్తు నిర్వహణ సంస్థ (NDMA)కు అధ్యక్షుడు ఎవరు?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'హోం మంత్రి నోడల్ మంత్రిత్వ శాఖను పర్యవేక్షిస్తారు కానీ ఛైర్మన్ కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) కేంద్ర హోం మంత్రి</button>
            <button onclick="checkPyq(this, true, 'NDMA చట్టం ప్రకారం దేశ ప్రధాని పదవీరీత్యా (Ex-officio) ఛైర్మన్‌గా వ్యవహరిస్తారు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) ప్రధానమంత్రి (Prime Minister)</button>
            <button onclick="checkPyq(this, false, 'రాష్ట్రపతి కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) రాష్ట్రపతి</button>
            <button onclick="checkPyq(this, false, 'కేబినెట్ సెక్రటరీ కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) కేబినెట్ కార్యదర్శి</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>

        <!-- Q4 -->
        <div class="bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">APPSC Group-I Prelims</span>
            <span class="text-xs text-slate-400">Q.4</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">1984 భోపాల్ గ్యాస్ దుర్ఘటనలో విడుదలైన ప్రాణాంతక విషవాయువు ఏది?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'తప్పు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) ఇథైల్ ఐసోసైనైట్</button>
            <button onclick="checkPyq(this, false, 'ఫాస్జీన్ కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) ఫాస్జీన్</button>
            <button onclick="checkPyq(this, true, 'యూనియన్ కార్బైడ్ ఫ్యాక్టరీ నుండి మిథైల్ ఐసోసైనైట్ (MIC) లీకైంది. రసాయన సూత్రం CH3NCO.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) మిథైల్ ఐసోసైనైట్ (MIC)</button>
            <button onclick="checkPyq(this, false, 'మస్టర్డ్ గ్యాస్ కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) సల్ఫర్ డైయాక్సైడ్</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>

        <!-- Q5 -->
        <div class="bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">Town Planning 2012</span>
            <span class="text-xs text-slate-400">Q.5</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">ఆంధ్రప్రదేశ్ తీరప్రాంతాన్ని వణికించిన దివిసీమ పెనుతుఫాను ఏ తేదీన సంభవించింది?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'నవంబర్ 15 కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) 15 నవంబర్ 1977</button>
            <button onclick="checkPyq(this, true, 'నవంబర్ 19, 1977న కృష్ణా జిల్లా దివిసీమను తాకింది. 6 మీటర్ల ఎత్తున పోటు అలలతో 10,000+ మంది ప్రాణాలు కోల్పోయారు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) 19 నవంబర్ 1977</button>
            <button onclick="checkPyq(this, false, 'తప్పు సంవత్సరం.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) 19 నవంబర్ 1978</button>
            <button onclick="checkPyq(this, false, 'తప్పు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) 25 అక్టోబర్ 1977</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>

        <!-- Q6 -->
        <div class="bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">Polytechnic Lecturers</span>
            <span class="text-xs text-slate-400">Q.6</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">సముద్రంలో సునామీ హెచ్చరిక వ్యవస్థ (ITEWC) భారతదేశంలో ఎక్కడ ఉంది?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'చెన్నైలో NIOT ఉంది కానీ సునామీ సెంటర్ కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) చెన్నై</button>
            <button onclick="checkPyq(this, false, 'కొచ్చి కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) కొచ్చి</button>
            <button onclick="checkPyq(this, true, 'INCOIS (ఇండియన్ నేషనల్ సెంటర్ ఫర్ ఓషన్ ఇన్ఫర్మేషన్ సర్వీసెస్) హైదరాబాదులో ఉంది.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) హైదరాబాద్ (INCOIS)</button>
            <button onclick="checkPyq(this, false, 'విశాఖపట్నం కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) విశాఖపట్నం</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-slate-950 border-t border-slate-800 text-slate-400 py-8 px-4 text-center text-xs no-print">
    <div class="max-w-7xl mx-auto space-y-2">
      <p class="text-slate-200 font-bold">లక్ష్య డైలీ తెలుగు కరెంట్ అఫైర్స్ & APPSC స్టడీ పోర్టల్</p>
      <p>APPSC Group 1, Group 2, Group 3, TSPSC, UPSC & పోలీస్ పరీక్షల విజేతల వేదిక</p>
      <p class="text-slate-500">© 2026 Lakshya CA • లైవ్ వెబ్ యాప్: <a href="https://lakshya-telugu-ca.onrender.com" class="text-blue-400 hover:underline">https://lakshya-telugu-ca.onrender.com</a></p>
    </div>
  </footer>

  <script>
    lucide.createIcons();

    function switchTab(tabId) {
      document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-blue-600', 'text-white');
        btn.classList.add('bg-slate-800', 'text-slate-300');
      });

      const activeContent = document.getElementById('content-' + tabId);
      const activeBtn = document.getElementById('tab-' + tabId);

      if (activeContent) activeContent.classList.remove('hidden');
      if (activeBtn) {
        activeBtn.classList.remove('bg-slate-800', 'text-slate-300');
        activeBtn.classList.add('bg-blue-600', 'text-white');
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function updateProgress() {
      const checkboxes = document.querySelectorAll('.study-check');
      const total = checkboxes.length;
      let checkedCount = 0;
      checkboxes.forEach((cb, idx) => {
        if (cb.checked) checkedCount++;
        localStorage.setItem('appsc_topic_' + idx, cb.checked);
      });
      const pct = total > 0 ? Math.round((checkedCount / total) * 100) : 0;
      document.getElementById('progressBar').style.width = pct + '%';
      document.getElementById('progressText').innerText = `మీరు చదివిన టాపిక్స్: ${checkedCount} / ${total} (${pct}% పూర్తి)`;
    }

    // Load saved checklist progress from localStorage
    window.addEventListener('DOMContentLoaded', () => {
      const checkboxes = document.querySelectorAll('.study-check');
      checkboxes.forEach((cb, idx) => {
        const saved = localStorage.getItem('appsc_topic_' + idx);
        if (saved === 'true') cb.checked = true;
      });
      updateProgress();
    });

    function shareToWhatsApp() {
      const text = encodeURIComponent("🎯 *లక్ష్య APPSC గ్రూప్ 1 & 2 సమగ్ర సిలబస్ & స్టడీ పోర్టల్!*\\nభూగోళశాస్త్రం, ఏపీ విధానాలు 4.0, 120+ మెంటల్ ఎబిలిటీ షార్ట్‌కట్లు & పూర్తి నోట్స్:\\n👉 https://lakshya-telugu-ca.onrender.com/appsc_syllabus");
      window.open('https://api.whatsapp.com/send?text=' + text, '_blank');
    }
  
    function checkPyq(btn, isCorrect, explanation) {
      const parent = btn.parentElement;
      const buttons = parent.querySelectorAll('button');
      buttons.forEach(b => {
        b.disabled = true;
        b.classList.remove('hover:bg-slate-700');
      });
      const expBox = parent.parentElement.querySelector('.pyq-exp');
      if (isCorrect) {
        btn.classList.remove('bg-slate-900');
        btn.classList.add('bg-emerald-600', 'text-white', 'font-bold');
        expBox.innerHTML = '<span class="text-emerald-400 font-bold">✅ సరైన సమాధానం!</span><br>' + explanation;
      } else {
        btn.classList.remove('bg-slate-900');
        btn.classList.add('bg-red-600', 'text-white', 'font-bold');
        expBox.innerHTML = '<span class="text-red-400 font-bold">❌ తప్పు సమాధానం!</span><br>' + explanation;
      }
      expBox.classList.remove('hidden');
    }

  </script>
</body>
</html>
"""
