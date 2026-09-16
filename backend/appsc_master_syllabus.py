# -*- coding: utf-8 -*-
"""
APPSC Group 1 & Group 2 Complete Master Textbook, Syllabus & Subject Portal.
Exhaustive, encyclopedic coverage extracted from official textbooks & handbooks:
1. భారత & ఆంధ్రప్రదేశ్ సమగ్ర చరిత్ర (Ancient, Medieval, Modern, Andhra Movement & 2014 Act)
2. ఆంధ్రప్రదేశ్ & భారత భూగోళశాస్త్రం (Ekam IAS 112-Page Textbook + RC Reddy 222-Page Notes)
3. విపత్తు నిర్వహణ (Disaster Management - RC Reddy 88-Page Notes & 2005 Act)
4. ఆంధ్రప్రదేశ్ నూతన విధానాలు 4.0 (AP Industrial Policies 2024–2029)
5. మెంటల్ ఎబిలిటీ & ఆప్టిట్యూడ్ (228-Page Master Textbook & 120 Formula Shortcuts)
6. భారత రాజ్యాంగం, పాలన & ముఖ్య ఆర్టికల్స్ (Articles 1-395, DPSP, 73/74 Amendments)
7. భారత ఆర్థిక వ్యవస్థ & ద్రవ్య మార్కెట్లు (Ekam IAS Financial Markets Guide)
8. 115+ సాల్వ్డ్ APPSC అసలైన పరీక్షల ప్రశ్నలు (MCQs Interactive Hub)
9. గ్రూప్-1 మెయిన్స్ ఆన్సర్ రైటింగ్, ఎథిక్స్ & ఇంటర్వ్యూ గైడ్
"""

def render_appsc_syllabus_html():
    return """<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>APPSC గ్రూప్ 1 & 2 సమగ్ర డిజిటల్ టెక్స్ట్‌బుక్ & మాస్టర్ సిలబస్ పోర్టల్ | లక్ష్య CA</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="icon" type="image/jpeg" href="/lakshya_logo.jpg">
  <link rel="apple-touch-icon" href="/lakshya_logo.jpg">
  <link rel="stylesheet" href="/styles.css?v=16">
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    @media print {
      .no-print { display: none !important; }
      body { background: white !important; color: black !important; font-size: 11pt; }
      .page-break { page-break-after: always; }
      .shadow-sm, .shadow-md, .shadow-lg { box-shadow: none !important; }
      .topic-card { border: 1px solid #ccc !important; background: white !important; color: black !important; }
    }
    .topic-card { transition: all 0.2s ease-in-out; }
    .topic-card:hover { border-color: rgba(99, 102, 241, 0.6); }
    .custom-scrollbar::-webkit-scrollbar { width: 6px; height: 6px; }
    .custom-scrollbar::-webkit-scrollbar-thumb { background-color: #94a3b8; border-radius: 4px; }
    .highlight-match { background-color: rgba(251, 191, 36, 0.35); border-radius: 2px; }
  </style>
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans antialiased">

  <!-- Top Announcement Bar -->
  <div class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white text-xs md:text-sm py-2 px-4 shadow-sm border-b border-indigo-800/40 no-print">
    <div class="max-w-7xl mx-auto flex justify-between items-center">
      <div class="flex items-center space-x-2">
        <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-amber-400 text-slate-950">
          🎯 అధికారిక మాస్టర్ టెక్స్ట్‌బుక్ పోర్టల్
        </span>
        <span class="truncate max-w-xs md:max-w-xl text-slate-200">
          APPSC గ్రూప్-1 & గ్రూప్-2 సంపూర్ణ పాఠ్య గ్రంథం • చరిత్ర, భూగోళశాస్త్రం (26 జిల్లాలు), విపత్తు నిర్వహణ, పాలసీలు 4.0 & 228 పేజీల మెంటల్ ఎబిలిటీ
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
  <header class="bg-slate-800/95 backdrop-blur border-b border-slate-700/60 sticky top-0 z-30 shadow-md no-print">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap justify-between items-center gap-4">
      <div class="flex items-center space-x-3">
        <img src="/lakshya_logo.jpg" alt="Logo" class="w-10 h-10 rounded-xl shadow-md border border-amber-400/40">
        <div>
          <h1 class="text-lg md:text-xl font-black text-white tracking-tight flex items-center gap-2">
            లక్ష్య • APPSC సమగ్ర డిజిటల్ టెక్స్ట్‌బుక్ హబ్
            <span class="text-xs bg-amber-400/20 text-amber-300 font-bold px-2.5 py-0.5 rounded-full border border-amber-400/30">Group 1 & 2 Full Book</span>
          </h1>
          <p class="text-xs text-slate-400 font-medium">అన్ని సబ్జెక్టుల లోతైన నోట్స్, 26 జిల్లాల డేటా, ఫార్ములాలు & 115+ సాల్వ్డ్ PYQs</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2.5">
        <button onclick="window.print()" class="bg-emerald-600 hover:bg-emerald-500 text-white px-3 py-1.5 rounded-lg text-xs sm:text-sm font-bold flex items-center space-x-1.5 transition shadow-sm">
          <i data-lucide="printer" class="w-4 h-4"></i>
          <span>ప్రింట్ / PDF డౌన్‌లోడ్</span>
        </button>
        <button onclick="shareToWhatsApp()" class="bg-green-600 hover:bg-green-500 text-white px-3 py-1.5 rounded-lg text-xs sm:text-sm font-bold flex items-center space-x-1.5 transition shadow-sm">
          <i data-lucide="share-2" class="w-4 h-4"></i>
          <span>వాట్సాప్ షేర్</span>
        </button>
      </div>
    </div>

    <!-- Subject Tabs Bar -->
    <div class="max-w-7xl mx-auto px-4 overflow-x-auto custom-scrollbar border-t border-slate-700/60 flex space-x-2 py-2 text-xs font-bold">
      <button onclick="switchTab('history')" id="tab-history" class="tab-btn px-3.5 py-2 rounded-lg bg-blue-600 text-white flex items-center gap-1.5 shrink-0 transition">
        <span>📜 చరిత్ర (భారత & ఏపీ పూర్తి బుక్)</span>
      </button>
      <button onclick="switchTab('geo')" id="tab-geo" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>🌍 భూగోళశాస్త్రం (Ekam & RC రెడ్డి 334 పేజీలు)</span>
      </button>
      <button onclick="switchTab('disaster')" id="tab-disaster" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>🚨 విపత్తు నిర్వహణ (RC రెడ్డి 88 పేజీలు)</span>
      </button>
      <button onclick="switchTab('policies')" id="tab-policies" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>💼 ఏపీ నూతన విధానాలు 4.0 (2024–2029)</span>
      </button>
      <button onclick="switchTab('aptitude')" id="tab-aptitude" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>🧮 మెంటల్ ఎబిలిటీ (228 పేజీల బుక్ & 120 షార్ట్‌కట్స్)</span>
      </button>
      <button onclick="switchTab('polity')" id="tab-polity" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>⚖️ రాజ్యాంగం & పాలన</span>
      </button>
      <button onclick="switchTab('economy')" id="tab-economy" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>💰 ఆర్థిక వ్యవస్థ & ద్రవ్య మార్కెట్లు</span>
      </button>
      <button onclick="switchTab('pyqs')" id="tab-pyqs" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>📝 115+ సాల్వ్డ్ APPSC ప్రశ్నలు (MCQs)</span>
      </button>
      <button onclick="switchTab('mains')" id="tab-mains" class="tab-btn px-3.5 py-2 rounded-lg bg-slate-800 text-slate-300 hover:bg-slate-700 flex items-center gap-1.5 shrink-0 transition">
        <span>✍️ మెయిన్స్ & ఎథిక్స్ గైడ్</span>
      </button>
    </div>
  </header>

  <!-- Container -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

    <!-- Search & Preparation Tracker -->
    <div class="bg-slate-800/90 border border-slate-700/80 p-4 rounded-2xl mb-6 shadow-sm flex flex-wrap items-center justify-between gap-4 no-print">
      <div class="flex items-center space-x-3 w-full md:w-auto">
        <div class="w-9 h-9 rounded-lg bg-amber-400/20 text-amber-400 flex items-center justify-center font-black">
          <i data-lucide="check-circle" class="w-5 h-5"></i>
        </div>
        <div>
          <h3 class="text-sm font-bold text-white">మీ ప్రిపరేషన్ చెక్‌లిస్ట్ ట్రాకర్</h3>
          <p class="text-xs text-slate-400" id="progressText">మీరు అధ్యయనం చేసిన అధ్యాయాలు టిక్ చేయండి (0 / 48 పూర్తి)</p>
        </div>
      </div>
      
      <!-- Real-time Subject Search Filter -->
      <div class="relative w-full md:w-72">
        <i data-lucide="search" class="w-4 h-4 absolute left-3 top-2.5 text-slate-400"></i>
        <input type="text" id="subjectSearch" onkeyup="filterTopics()" placeholder="సిలబస్‌లో శోధించండి (ఉదా: శాతవాహనులు, పోలవరం...)" class="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-blue-500">
      </div>

      <div class="w-full md:w-56 bg-slate-700 rounded-full h-2.5 overflow-hidden">
        <div id="progressBar" class="bg-gradient-to-r from-amber-400 to-emerald-500 h-2.5 rounded-full transition-all duration-300" style="width: 0%"></div>
      </div>
    </div>

    <!-- ==================== TAB 1: HISTORY (భారత & ఆంధ్రప్రదేశ్ సమగ్ర చరిత్ర) ==================== -->
    <section id="content-history" class="tab-content space-y-6">
      <div class="bg-gradient-to-r from-amber-950 via-slate-800 to-slate-900 border border-amber-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-amber-900/60 text-amber-300 px-3 py-1 rounded-full border border-amber-700/50">APPSC Group 1 & 2 • 30 మార్కులు</span>
          <span class="text-xs text-slate-400">ప్రాచీన, మధ్యయుగ, ఆధునిక భారతదేశం మరియు సమగ్ర ఆంధ్రప్రదేశ్ చరిత్ర</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారత & ఆంధ్రప్రదేశ్ చరిత్ర సంపూర్ణ పాఠ్య గ్రంథం (History Master Textbook)</h2>
        <p class="text-sm text-slate-300 mt-1">సింధు లోయ నాగరికత నుండి 1947 స్వాతంత్ర్యం వరకు మరియు శాతవాహనుల నుండి 2014 ఆంధ్రప్రదేశ్ పునర్విభజన చట్టం వరకు పూర్తి వివరాలు.</p>
      </div>

      <!-- Part 1: Ancient India -->
      <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-base font-bold text-amber-400 flex items-center gap-2">
            <span>🏛️ 1. ప్రాచీన భారతదేశ చరిత్ర (Ancient Indian History)</span>
          </h3>
          <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
            <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
            <span>చదివాను</span>
          </label>
        </div>
        
        <div class="space-y-4 text-xs text-slate-300 leading-relaxed">
          <!-- Indus Valley -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">🏺 సింధు లోయ నాగరికత (క్రీ.పూ. 2500 – 1750 - కాంస్య యుగం)</h4>
            <ul class="space-y-1.5 list-disc list-inside">
              <li><b>పరిశోధనలు & ప్రధాన నగరాలు:</b>
                <br>• <b>హరప్పా (1921):</b> దయారాం సాహ్ని కనుగొన్నారు. పంజాబ్ (పాకిస్తాన్) రావి నది ఒడ్డున ఉంది. 6 ధాన్యాగారాల వరుసలు, శవపేటిక ఖననం (R-37 సిమెట్రీ).
                <br>• <b>మొహెంజోదారో (1922):</b> ఆర్.డి. బెనర్జీ కనుగొన్నారు. సింధు నది ఒడ్డున ఉంది. సింధీ భాషలో 'మృతుల దిబ్బ' అని అర్థం. మహా స్నానవాటిక (Great Bath), కాంస్య నర్తకి విగ్రహం (Dancing Girl), గడ్డంతో ఉన్న పూజారి విగ్రహం, పశుపతి మహాదేవుని ముద్ర.
                <br>• <b>లోథాల్ (గుజరాత్):</b> ఎస్.ఆర్. రావు కనుగొన్నారు. భోగావో నది ఒడ్డున ఉంది. ప్రపంచంలోనే తొలి కృత్రిమ డాక్‌యార్డ్ (ఓడరేవు), వరి పొట్టు (Rice husk), చదరంగం బోర్డు, డబుల్ బరియల్.
                <br>• <b>కాళీబంగన్ (రాజస్థాన్):</b> ఘగ్గర్ నది ఒడ్డున ఉంది. నల్లని గాజులు అని అర్థం. నాగలితో దున్నిన పొలం, అగ్నిగుండాలు (Fire altars), ఒంటె ఎముకలు.
                <br>• <b>చాన్హుదారో (పాకిస్తాన్):</b> సిటాడెల్ (కోట) లేని ఏకైక నగరం. లిప్‌స్టిక్, కాటుక, పూసల తయారీ కర్మాగారం, సిరాబుడ్డి.
                <br>• <b>ధోలవీర (గుజరాత్ - కచ్):</b> యునెస్కో ప్రపంచ వారసత్వ సైట్. నగరం 3 భాగాలుగా విభజించబడింది (కోట, మధ్య నగరం, దిగువ నగరం). ప్రపంచంలోనే ప్రాచీన వర్షపు నీటి నిల్వ వ్యవస్థ (Water Harvesting Reservoirs), పెద్ద సైన్‌బోర్డ్.
                <br>• <b>బనవాలి (హర్యానా):</b> మట్టితో చేసిన బొమ్మ నాగలి, నాణ్యమైన బార్లీ ధాన్యం.
              </li>
              <li><b>నగర ప్రణాళిక & జీవన విధానం:</b> గ్రిడ్ పద్ధతి (గ్రిడ్ సిస్టమ్), కాల్చిన ఇటుకల నిర్మాణాలు, భూగర్భ మురుగునీటి పారుదల వ్యవస్థ (Underground drainage). లిపి: సర్పలేఖనం / బొమ్మల లిపి (Boustrophedon). తెలియని జంతువు: గుర్రం (స్పష్టమైన ఆధారాలు లేవు); తెలియని లోహం: ఇనుము (Iron).</li>
            </ul>
          </div>

          <!-- Vedic Period -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">📖 వేద నాగరికత & షోడశ మహాజనపదాలు</h4>
            <ul class="space-y-1.5 list-disc list-inside">
              <li><b>తొలి వేద కాలం (క్రీ.పూ. 1500–1000):</b> ఋగ్వేదం - 10 మండలాలు, 1028 సూక్తులు. 3వ మండలంలో గాయత్రీ మంత్రం (విశ్వామిత్రుడు), 10వ మండలంలోని పురుషసూక్తంలో తొలిసారి వర్ణ వ్యవస్థ ప్రస్తావన. సప్తసింధు ప్రాంతం. దశరాజన్ యుద్ధం (పురుష్ణి/రావి నది తీరాన సుదాసుడు 10 మంది రాజుల కూటమిపై విజయం). పాలనా సభలు: సభ (పెద్దల సభ), సమితి (ప్రజా ప్రతినిధి సభ), విధాత (పురాతన సభ).</li>
              <li><b>మలి వేద కాలం (క్రీ.పూ. 1000–600):</b> సామవేదం (భారతీయ సంగీత మూలం), యజుర్వేదం (యజ్ఞ యాగాదుల విధులు), అథర్వణవేదం (వైద్యం, ఆయుర్వేదం, మంత్ర తంత్రాలు). ఇనుము వాడకం ప్రారంభం (శ్యామ అయస్/కృష్ణ అయస్). ఉపనిషత్తులు (108 - 'సత్యమేవ జయతే' ముండకోపనిషత్తు నుండి తీసుకోబడింది). అరణ్యకాలు, బ్రాహ్మణాలు.</li>
              <li><b>షోడశ మహాజనపదాలు (16 రాజ్యాలు):</b> అంగుత్తర నికాయ (బౌద్ధ గ్రంథం), భగవతీ సూత్ర (జైన గ్రంథం) లో ప్రస్తావన. అత్యంత శక్తివంతమైనది: మగధ (రాజధాని గిరివ్రజ/రాజగృహ, తదుపరి పాటలీపుత్ర). దక్షిణ భారతదేశంలోని ఏకైక మహాజనపదం: <b>అశ్మక / అసక</b> (గోదావరి నది ఒడ్డున, రాజధాని పోతన/బోధన్).</li>
            </ul>
          </div>

          <!-- Jainism & Buddhism -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">☸️ జైన మతం & బౌద్ధ మతం</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mt-2">
              <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                <span class="font-bold text-amber-400">జైన మతం:</span>
                <br>• 24 మంది తీర్థంకరులు: 1వ తీర్థంకరుడు వృషభనాథుడు (ఆదినాథుడు). 23వ తీర్థంకరుడు పార్శ్వనాథుడు (4 సూత్రాలు: అహింస, సత్యం, అస్తేయం, అపరిగ్రహం).
                <br>• 24వ తీర్థంకరుడు <b>వర్ధమాన మహావీరుడు</b>: వైశాలి సమీపంలోని కుందగ్రామంలో జననం. 42వ ఏట జృంబికాగ్రామం వద్ద రుజుపాలికా నది ఒడ్డున సాల వృక్షం క్రింద కైవల్యం (జ్ఞానోదయం). పావాపురి వద్ద నిర్యాణం. 5వ సూత్రం 'బ్రహ్మచర్యం' చేర్చాడు.
                <br>• త్రిరత్నాలు: సమ్యక్ దర్శనం, సమ్యక్ జ్ఞానం, సమ్యక్ చరిత్ర.
                <br>• చీలిక: శ్వేతాంబరులు (స్థూలభద్రుడు), దిగంబరులు (భద్రబాహు).
              </div>
              <div class="bg-slate-950/60 p-3 rounded-lg border border-slate-800">
                <span class="font-bold text-amber-400">బౌద్ధ మతం:</span>
                <br>• <b>గౌతమ బుద్ధుడు (సిద్ధార్థుడు):</b> లుంబిని వనం (నేపాల్) లో జననం. గయలో నిరంజన నది ఒడ్డున రావి చెట్టు (బోధి వృక్షం) క్రింద జ్ఞానోదయం. సారనాథ్‌లోని డీర్ పార్క్‌లో తొలి ఉపన్యాసం (ధర్మచక్ర ప్రవర్తనం). కుశీనగరంలో మహా పరినిర్వాణం.
                <br>• నాలుగు ఆర్య సత్యాలు, అష్టాంగ మార్గం. త్రిపీటకాలు: వినయ పీఠకం (నియమాలు), సుత్త పీఠకం (బోధనలు), అభిధమ్మ పీఠకం (తత్వశాస్త్రం).
                <br>• <b>4 బౌద్ధ సంగీతులు (సభలు):</b>
                <br>1. రాజగృహ (క్రీ.పూ. 483, అజాతశత్రు, అధ్యక్షుడు: మహాకశ్యప)
                <br>2. వైశాలి (క్రీ.పూ. 383, కాలశోక, అధ్యక్షుడు: సబకామి)
                <br>3. పాటలీపుత్ర (క్రీ.పూ. 250, అశోకుడు, అధ్యక్షుడు: మొగ్గలిపుత్త తిస్స)
                <br>4. కుండలవనం/కాశ్మీర్ (క్రీ.శ. 72, కనిష్కుడు, అధ్యక్షుడు: వసుమిత్ర - హీనయాన, మహాయాన చీలిక).
              </div>
            </div>
          </div>

          <!-- Mauryan Empire & Guptas -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">👑 మౌర్య సామ్రాజ్యం & గుప్తుల స్వర్ణయుగం</h4>
            <ul class="space-y-1.5 list-disc list-inside">
              <li><b>మౌర్య సామ్రాజ్యం (క్రీ.పూ. 322–185):</b>
                <br>• <b>చంద్రగుప్త మౌర్యుడు:</b> చాణక్యుని (కౌటిల్యుడు/విష్ణుగుప్తుడు) సహాయంతో నందవంశపు ధననందుడిని ఓడించి స్థాపించాడు. కౌటిల్యుని 'అర్థశాస్త్రం' (సప్తాంగ సిద్ధాంతం - స్వామి, అమాత్య, జనపద, దుర్గ, కోశ, దండ, మిత్ర). గ్రీకు రాయబారి మెగస్తనీస్ రచించిన 'ఇండికా'. చంద్రగుప్తుడు చివరి దశలో జైనమతం స్వీకరించి భద్రబాహుతో కలిసి శ్రావణబెళగొళ వెళ్లి సల్లేఖన వ్రతం ద్వారా ప్రాణత్యాగం చేశాడు.
                <br>• <b>అశోక చక్రవర్తి (క్రీ.పూ. 268–232):</b> కళింగ యుద్ధం (క్రీ.పూ. 261). యుద్ధ భీభత్సాన్ని చూసి ఉపగుప్తుని ప్రభావంతో బౌద్ధం స్వీకరించి 'ధర్మవిజయం' సాధించాడు. 14 ప్రధాన శిలాశాసనాలు (13వ శిలాశాసనం కళింగ యుద్ధాన్ని వివరిస్తుంది). సారనాథ్ స్తంభంపై గల నాలుగు సింహాల చిహ్నం భారత జాతీయ చిహ్నంగా స్వీకరించబడింది.
              </li>
              <li><b>గుప్త సామ్రాజ్యం (క్రీ.శ. 319–550 - ప్రాచీన భారత స్వర్ణయుగం):</b>
                <br>• <b>సముద్రగుప్తుడు:</b> "భారత నెపోలియన్" (విన్సెంట్ స్మిత్). హరిసేనుడు రచించిన <b>అలహాబాద్ ప్రశస్తి (ప్రయాగ ప్రశస్తి)</b> శాసనం ఇతని దిగ్విజయాలను తెలుపుతుంది. అశ్వమేధ పరాక్రమ, కవిరాజు బిరుదులు (నాణేలపై వీణ వాయిస్తున్న చిత్రం).
                <br>• <b>రెండవ చంద్రగుప్తుడు (విక్రమాదిత్యుడు):</b> శకులను ఓడించి 'శకారి' బిరుదు పొందాడు. ఆస్థానంలో <b>నవరత్నాలు</b>: కాళిదాసు (అభిజ్ఞాన శాకుంతలం, మేఘదూతం, రఘువంశం), అమరసింహుడు (అమరకోశం), వరాహమిహిరుడు (బృహత్సంహిత), ధన్వంతరి (ఆయుర్వేదం). చైనా యాత్రికుడు ఫాహియాన్ సందర్శన. మెహ్రౌలీ ఇనుప స్తంభం.
                <br>• <b>శాస్త్ర విజ్ఞానం:</b> ఆర్యభట్ట (ఆర్యభట్టీయం, సూర్యసిద్ధాంతం - భూమి తనచుట్టూ తాను తిరుగుతుందని, సూర్యగ్రహణాల కారణాలను తొలిసారి నిరూపించాడు). కుమారగుప్తుడు ప్రపంచ ప్రసిద్ధ <b>నలంద విశ్వవిద్యాలయం</b> స్థాపించాడు.
              </li>
              <li><b>హర్షవర్ధనుడు (క్రీ.శ. 606–647):</b> పుష్యభూతి/వర్ధన వంశం. రాజధాని థానేశ్వర్ నుండి కనౌజ్ కు మార్చాడు. బాణభట్టుడు ('హర్షచరిత', 'కాదంబరి'). హర్షుడు స్వయంగా రత్నావళి, ప్రియదర్శిక, నాగానంద నాటకాలను రచించాడు. చైనా యాత్రికుల రారాజు <b>హుయాన్ త్సాంగ్</b> హర్షుని ఆస్థానాన్ని సందర్శించాడు ('సి-యు-కి' గ్రంథం). నర్మదా నది తీరాన జరిగిన యుద్ధంలో బాదామి చాళుక్య రాజు రెండవ పులకేశి చేతిలో హర్షుడు ఓడిపోయాడు (ఐహోల్ శాసనం).</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Part 2: Medieval India -->
      <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-base font-bold text-amber-400 flex items-center gap-2">
            <span>🏰 2. మధ్యయుగ భారతదేశ చరిత్ర (Medieval Indian History)</span>
          </h3>
          <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
            <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
            <span>చదివాను</span>
          </label>
        </div>
        
        <div class="space-y-4 text-xs text-slate-300 leading-relaxed">
          <!-- Delhi Sultanate -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">🕌 ఢిల్లీ సుల్తానేట్ (1206 – 1526 - 5 రాజవంశాలు)</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <p>• <b>బానిస వంశం (1206-1290):</b> కుతుబుద్దీన్ ఐబక్ (స్థాపకుడు, 'లాఖ్‌బక్ష్', కుతుబ్ మినార్ నిర్మాణం ప్రారంభించాడు). ఇల్తుత్‌మిష్ (కుతుబ్ మినార్ పూర్తి చేశాడు, 'చహల్‌గాని' 40 మంది సర్దార్ల కూటమి, వెండి టంకా & రాగి జిటల్ నాణేలు). రజియా సుల్తానా (ఢిల్లీని పాలించిన ఏకైక మహిళా సుల్తాన్). గియాసుద్దీన్ బాల్బన్ (రక్తం & ఇనుము విధానం, సిజ్దా & పైబోస్ ఆచారాలు, నౌరోజ్ పండుగ).</p>
                <p class="mt-2">• <b>ఖిల్జీ వంశం (1290-1320):</b> అల్లావుద్దీన్ ఖిల్జీ: మార్కెట్ సంస్కరణలు, నిత్యావసర వస్తువుల ధరల నియంత్రణ (షహానా-ఇ-మండి), సైన్యంలో గుర్రాలకు ముద్ర వేసే 'దాగ్', సైనికుల గుర్తింపు 'చెహ్రా' విధానాలు. మాలిక్ కాఫూర్ దక్షిణ భారత దండయాత్రలు (దేవగిరి, వరంగల్ కాకతీయులు, ద్వారసముద్రం, మధురై). అలై దర్వాజా నిర్మాత.</p>
              </div>
              <div>
                <p>• <b>తుగ్లక్ వంశం (1320-1414):</b> గియాసుద్దీన్ తుగ్లక్ (తుగ్లకాబాద్ నిర్మాత). మహమ్మద్ బిన్ తుగ్లక్ ("పండిత మూర్ఖుడు" - రాజధాని ఢిల్లీ నుండి దౌలతాబాద్ కు మార్పు 1327, రాగి/కాంస్య టోకెన్ కరెన్సీ, వ్యవసాయ శాఖ 'దివాన్-ఇ-కోహి'). ఇబ్న్ బటూటా ('కితాబ్-ఉల్-రెహ్లా'). ఫిరోజ్ షా తుగ్లక్: కాలువల తవ్వకం, జౌన్‌పూర్, హిస్సార్ నగరాల స్థాపన, జిజియా పన్ను బ్రాహ్మణులపై విధింపు.</p>
                <p class="mt-2">• <b>సయ్యద్ (1414-1451) & లోడీ వంశం (1451-1526):</b> లోడీలు ఢిల్లీని పాలించిన తొలి ఆఫ్ఘన్లు. సికందర్ లోడీ (1504లో ఆగ్రా నగరం స్థాపన). ఇబ్రహీం లోడీ (చివరి సుల్తాన్ - 1526 మొదటి పానిపట్ యుద్ధంలో బాబర్ చేతిలో ఓడిపోయాడు).</p>
              </div>
            </div>
          </div>

          <!-- Mughal Empire -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">🛡️ మొఘల్ సామ్రాజ్యం & మరాఠాలు</h4>
            <ul class="space-y-1.5 list-disc list-inside">
              <li><b>బాబర్ (1526-1530):</b> మొదటి పానిపట్ యుద్ధం (1526 ఏప్రిల్ 21 - తుగ్లమా సైనిక వ్యూహం, ఫిరంగుల వాడకం), ఖాన్వా యుద్ధం (1527 - రాణా సంగపై విజయం, 'గాజీ' బిరుదు). ఆత్మకథ: తుజుక్-ఇ-బాబరీ (బాబర్‌నామా).</li>
              <li><b>షేర్ షా సూరి (సూర్ వంశం 1540-1545):</b> చౌసా (1539), కనౌజ్ (1540) యుద్ధాల్లో హుమాయూన్‌ను ఓడించి పాలన సాగించాడు. గ్రాండ్ ట్రంక్ రోడ్ (GT Road) నిర్మాణం, నేటి రూపాయి మూల రూపమైన వెండి 'రూపియా' (Rupiya) నాణెం ప్రవేశపెట్టాడు. పోస్టల్ వ్యవస్థ పునరుద్ధరణ.</li>
              <li><b>అక్బర్ ది గ్రేట్ (1556-1605):</b> రెండవ పానిపట్ యుద్ధం (1556 - బైరామ్ ఖాన్ రక్షణలో హేముపై విజయం). పిల్గ్రిమ్ ట్యాక్స్ రద్దు (1563), జిజియా పన్ను రద్దు (1564). ఇబాదత్ ఖానా (1575), మహ్జర్ నామా (1579), దీన్-ఇ-ఇలాహీ (1582). రాజా తోడర్‌మల్ చేత భూమి శిస్తు బందోబస్తు విధానం (దహ్‌సాల పద్ధతి). మన్సబ్దారీ వ్యవస్థ (జాట్ మరియు సవార్). నవరత్నాలు: అబుల్ ఫజల్ ('అక్బర్‌నామా'), బీర్బల్, తాన్‌సేన్, ఫైజీ, తోడర్‌మల్, మాన్‌సింగ్. ఫతేపూర్ సిక్రి & బులంద్ దర్వాజా.</li>
              <li><b>జహంగీర్, షాజహాన్, ఔరంగజేబ్:</b> జహంగీర్ న్యాయ గంట (జంజీర్-ఇ-అద్ల్), కెప్టెన్ హాకిన్స్, సర్ థామస్ రో రాక. షాజహాన్ కాలం మొఘల్ వాస్తుకళా స్వర్ణయుగం (తాజ్‌మహల్, ఎర్రకోట, జామా మసీదు, నెమలి సింహాసనం). ఔరంగజేబ్ (ఆలంగీర్ - జిజియా పునఃప్రవేశం 1679, గురు తేజ్ బహదూర్ అమరత్వం, గోల్కొండ ఆక్రమణ 1687).</li>
              <li><b>మరాఠా సామ్రాజ్యం - ఛత్రపతి శివాజీ (1627-1680):</b> పూనా సమీపంలోని శివనేరి దుర్గంలో జననం. తోరణ, పురందర్ కోటల ఆక్రమణ. అఫ్జల్ ఖాన్ వధ (1659), షైస్తా ఖాన్‌పై మెరుపు దాడి (1663), సూరత్ దోపిడీ (1664). పురందర్ సంధి (1665 - రాజా జైసింగ్‌తో). 1674లో రాయగఢ్‌లో ఛత్రపతిగా పట్టాభిషేకం. అష్టప్రధాన్ మంత్రిమండలి (పీష్వా, సేనాపతి, అమాత్య తదితరులు). పన్నులు: చౌత్ (1/4 భాగం), సర్దేశ్‌ముఖి (1/10 భాగం). గెరిల్లా యుద్ధ తంత్రం (శివసూత్రం).</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Part 3: Modern India & Freedom Struggle -->
      <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-base font-bold text-amber-400 flex items-center gap-2">
            <span>🇮🇳 3. ఆధునిక భారతదేశం & జాతీయోద్యమం (Modern India & Freedom Movement)</span>
          </h3>
          <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
            <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
            <span>చదివాను</span>
          </label>
        </div>
        
        <div class="space-y-4 text-xs text-slate-300 leading-relaxed">
          <!-- British Expansion & 1857 Revolt -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">⚔️ బ్రిటిష్ ఆధిపత్య స్థాపన & 1857 ప్రథమ స్వాతంత్ర్య సంగ్రామం</h4>
            <ul class="space-y-1.5 list-disc list-inside">
              <li><b>కీలక యుద్ధాలు:</b> ప్లాసీ యుద్ధం (జూన్ 23, 1757 - రాబర్ట్ క్లైవ్ vs సిరాజుద్దౌలా), బక్సార్ యుద్ధం (అక్టోబర్ 22, 1764 - హెక్టర్ మున్రో vs మీర్ ఖాసిం కూటమి; 1765 అలహాబాద్ సంధి ద్వారా ఈస్ట్ ఇండియా కంపెనీకి బెంగాల్, బీహార్, ఒరిస్సా దివానీ హక్కులు లభించాయి).</li>
              <li><b>విస్తరణ విధానాలు:</b> లార్డ్ వెల్లెస్లీ 'సైన్య సహకార పద్ధతి' (1798 - తొలిగా చేరినది హైదరాబాద్ నిజాం అలీ ఖాన్). లార్డ్ డల్హౌసీ 'రాజ్యసంక్రమణ సిద్ధాంతం' (Doctrine of Lapse - సతారా 1848, సంబల్పూర్, ఉదయపూర్, ఝాన్సీ, నాగ్‌పూర్ ఆక్రమణ).</li>
              <li><b>1857 తిరుగుబాటు:</b> తక్షణ కారణం ఎన్‌ఫీల్డ్ తుపాకీ కొవ్వు తూటాలు. మార్చి 29, 1857న బారక్‌పూర్‌లో <b>మంగళ్ పాండే</b> తిరుగుబాటు. మే 10, 1857 మీరట్‌లో సైనికుల విప్లవం ప్రారంభం. నాయకులు: ఢిల్లీ (రెండవ బహదూర్ షా, భక్త్ ఖాన్), కాన్పూర్ (నానా సాహెబ్, తాంతియా తోపే), లక్నో (బేగం హజ్రత్ మహల్), ఝాన్సీ (రాణి లక్ష్మీబాయి), బీహార్ (కున్వర్ సింగ్). ఫలితం: 1858 నవంబర్ 1 విక్టోరియా రాణి ప్రకటన, కంపెనీ పాలన రద్దు, బ్రిటిష్ క్రౌన్ పాలన ప్రారంభం (లార్డ్ కానింగ్ తొలి వైస్రాయ్).</li>
            </ul>
          </div>

          <!-- Freedom Movement Phases -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">🚩 జాతీయోద్యమం మూడు దశలు (1885 – 1947)</h4>
            <div class="space-y-2">
              <p>• <b>మితవాద దశ (1885-1905):</b> 1885 డిసెంబర్ 28న బొంబాయిలో A.O. హ్యూమ్ చొరవతో ఇండియన్ నేషనల్ కాంగ్రెస్ (INC) స్థాపన (డబ్ల్యూ.సి. బెనర్జీ తొలి అధ్యక్షుడు). దాదాభాయ్ నౌరోజీ ('Poverty and Un-British Rule in India' - డ్రెయిన్ సిద్ధాంతం), గోపాలకృష్ణ గోఖలే (గాంధీజీ రాజకీయ గురువు, సర్వెంట్స్ ఆఫ్ ఇండియా సొసైటీ స్థాపకుడు).</p>
              <p>• <b>అతివాద దశ (1905-1920):</b> లాల్-బాల్-పాల్ & అరబిందో ఘోష్. 1905 అక్టోబర్ 16న లార్డ్ కర్జన్ బెంగాల్ విభజన; వందేమాతర / స్వదేశీ ఉద్యమం ప్రారంభం. 1906 ముస్లిం లీగ్ స్థాపన (ఢాకా). 1907 సూరత్ కాంగ్రెస్ చీలిక. 1909 మింటో-మార్లే సంస్కరణలు (ముస్లింలకు ప్రత్యేక నియోజకవర్గాలు). 1916 లక్నో ఒప్పందం (మితవాద-అతివాద కలయిక, కాంగ్రెస్-లీగ్ సంధి). 1916 హోమ్‌రూల్ ఉద్యమం (తిలక్ & అనిబిసెంట్).</p>
              <p>• <b>గాంధేయ యుగం (1915-1947):</b>
                <br>• 1915 జనవరి 9న గాంధీజీ దక్షిణాఫ్రికా నుండి రాక (ప్రవాసీ భారతీయ దివస్). చంపారన్ సత్యాగ్రహం (1917 - తీన్‌కథియా పద్ధతికి వ్యతిరేకం), అహ్మదాబాద్ మిల్లు సమ్మె (1918), ఖేడా సత్యాగ్రహం (1918).
                <br>• 1919 రౌలత్ చట్టం; 1919 ఏప్రిల్ 13న <b>జలియన్‌వాలాబాగ్ దురంతం</b> (జనరల్ డయర్ కాల్పులు, రవీంద్రనాథ్ ఠాగూర్ నైట్‌హుడ్ త్యాగం).
                <br>• <b>సహాయ నిరాకరణ ఉద్యమం (1920-1922):</b> 1922 ఫిబ్రవరి 4 చౌరీచౌరా హింసాత్మక ఘటనతో గాంధీజీ ఉద్యమాన్ని నిలిపివేశారు. 1923 స్వరాజ్ పార్టీ (చిత్తరంజన్ దాస్, మోతీలాల్ నెహ్రూ).
                <br>• 1927 సైమన్ కమిషన్ బహిష్కరణ (లాలా లజపతిరాయ్ లాఠీఛార్జ్‌లో మృతి). 1928 నెహ్రూ రిపోర్ట్. 1929 లాహోర్ కాంగ్రెస్ - <b>పూర్ణ స్వరాజ్</b> తీర్మానం (నెహ్రూ అధ్యక్షత).
                <br>• <b>శాసనోల్లంఘన ఉద్యమం & దండి మార్చ్ (1930):</b> మార్చి 12 నుండి ఏప్రిల్ 6 వరకు సబర్మతి నుండి దండి వరకు ఉప్పు సత్యాగ్రహ పాదయాత్ర. 1931 గాంధీ-ఇర్విన్ ఒప్పందం. రౌండ్ టేబుల్ సమావేశాలు. 1932 పూనా ఒప్పందం (గాంధీ-అంబేద్కర్ మధ్య చారిత్రక ఒప్పందం).
                <br>• 1935 భారత ప్రభుత్వ చట్టం (ప్రావిన్షియల్ అటానమీ, ఆర్బీఐ, ఫెడరల్ కోర్టు).
                <br>• <b>క్విట్ ఇండియా ఉద్యమం (1942):</b> ఆగస్టు 8న బొంబాయిలో 'డూ ఆర్ డై' (చేయండి లేదా చావండి) నినాదం. అరుణా అసఫ్ అలీ, ఉషా మెహతా అండర్‌గ్రౌండ్ రేడియో.
                <br>• <b>నేతాజీ సుభాష్ చంద్రబోస్:</b> ఫార్వర్డ్ బ్లాక్ (1939), ఆజాద్ హింద్ ఫౌజ్ (INA) - "ఢిల్లీ చలో", "జై హింద్".
                <br>• 1946 క్యాబినెట్ మిషన్, 1947 జూన్ 3 మౌంట్‌బాటన్ ప్లాన్, ఆగస్టు 15, 1947న భారత స్వాతంత్ర్యం.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- Part 4: Comprehensive Andhra Pradesh History -->
      <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-base font-bold text-amber-400 flex items-center gap-2">
            <span>🏛️ 4. సమగ్ర ఆంధ్రప్రదేశ్ చరిత్ర & ఉద్యమాలు (Comprehensive AP History)</span>
          </h3>
          <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
            <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
            <span>చదివాను</span>
          </label>
        </div>
        
        <div class="space-y-4 text-xs text-slate-300 leading-relaxed">
          <!-- Dynasties of AP -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">👑 ఆంధ్ర రాజవంశాల స్వర్ణయుగం</h4>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <p>• <b>శాతవాహనులు (క్రీ.పూ. 271 - క్రీ.శ. 3వ శతాబ్దం):</b>
                  <br>• స్థాపకుడు: శ్రీముఖుడు (కోటిలింగాల, ప్రతిష్ఠానపురం, ధాన్యకటకం/అమరావతి రాజధానులు).
                  <br>• 17వ రాజు హాలుడు: ప్రాకృతంలో <b>'గాథాసప్తశతి'</b> రచించి 'కవివత్సలుడు' అయ్యాడు. గుణాఢ్యుని బృహత్కథ, శర్వవర్మ కాతంత్ర వ్యాకరణం.
                  <br>• 23వ రాజు <b>గౌతమీపుత్ర శాతకర్ణి:</b> శాతవాహనులలో అగ్రగణ్యుడు. క్షహరాట వంశ నాశక, త్రిసముద్రతోయపీతవాహన, శక యుగం (క్రీ.శ. 78) ప్రారంభకుడు. తల్లి గౌతమీ బాలాశ్రీ వేయించిన నాసిక్ ప్రశస్తి శాసనం.
                  <br>• 27వ రాజు యజ్ఞశ్రీ శాతకర్ణి: ఓడ తెరచాప ముద్ర గల నాణేలు జారీ చేశాడు. ఆచార్య నాగార్జునునికి శ్రీపర్వతం (నాగార్జునకొండ) పై మహావిహారం నిర్మించాడు.
                  <br>• <b>ఆచార్య నాగార్జునుడు:</b> మాధ్యమికవాద బౌద్ధ సిద్ధాంతం, 'భారతీయ ఐన్‌స్టీన్'. సుహృల్లేఖ, ప్రజ్ఞాపారమిత శాస్త్రాల రచయిత.
                </p>
                <p class="mt-2">• <b>ఇక్ష్వాకులు (విజయపురి/నాగార్జునకొండ):</b> వాసిష్టీపుత్ర శ్రీశాంతమూలుడు (స్థాపకుడు, అశ్వమేధ యాగం). వీరపురుషదత్తుడు (దక్షిణ భారత అశోకుడు, బౌద్ధ విహారాల నిర్మాణం, స్త్రీల విరాళాలు).</p>
                <p class="mt-2">• <b>విష్ణుకుండినులు:</b> గోవిందవర్మ, మాధవవర్మ-II (11 అశ్వమేధాలు). రాజధానులు వినుకొండ, దెందులూరు. ఉండవల్లి అనంత పద్మనాభస్వామి గుహలు, మొగల్‌రాజపురం గుహాలయాల రూపకర్తలు.</p>
              </div>
              <div>
                <p>• <b>తూర్పు చాళుక్యులు (వేంగి - క్రీ.శ. 624-1070):</b> కుబ్జవిష్ణువర్ధనుడు స్థాపకుడు. గుణగ విజయాదిత్యుడు (గొప్పవాడు). <b>రాజరాజ నరేంద్రుడు</b> (రాజమండ్రి): ఆదికవి నన్నయ భట్టారకునితో మహాభారతంలోని ఆది, సభ, అరణ్య పర్వాల ఆంధ్రీకరణ చేయించి తెలుగు సాహిత్య యుగానికి పునాది వేశాడు.</p>
                <p class="mt-2">• <b>కాకతీయులు (వరంగల్ - క్రీ.శ. 1000-1323):</b> రుద్రదేవుడు (వేయి స్తంభాల గుడి 1163). గణపతిదేవుడు (సమైక్య ఆంధ్రదేశ పాలకుడు, మోటుపల్లి అభయ శాసనం ద్వారా విదేశీ వాణిజ్య ప్రోత్సాహం, రామప్ప దేవాలయం 1213 - UNESCO సైట్). <b>రాణి రుద్రమదేవి (1262-1289):</b> రుద్రదేవ మహారాజుగా పాలన, మార్కోపోలో మోటుపల్లి సందర్శించి ప్రశంసించాడు. ప్రతాపరుద్ర-II చివరి పాలకుడు.</p>
                <p class="mt-2">• <b>రెడ్డి రాజులు:</b> ప్రోలయ వేమారెడ్డి కొండవీడు రాజ్యం. శ్రీనాథ కవిసార్వభౌముడు (కాశీఖండం, పల్నాటి వీరచరిత్ర, ప్రౌఢదేవరాయల ఆస్థానంలో కనకాభిషేకం), ఎర్రాప్రగడ, వేమన సాహిత్యం.</p>
                <p class="mt-2">• <b>విజయనగర సామ్రాజ్యం (1336-1672):</b> హరిహర & బుక్కరాయల స్థాపన (హంపి). <b>శ్రీకృష్ణదేవరాయలు (1509-1529):</b> "ఆంధ్ర భోజుడు", తెలుగులో 'అముక్తమాల్యద', సంస్కృతంలో 'జాంబవతీ కళ్యాణం'. అష్టదిగ్గజ కవులు (అల్లసాని పెద్దన 'మనుచరిత్ర', తెనాలి రామకృష్ణ). 1565 తళ్ళికోట / రక్కసి-తంగడి యుద్ధంతో పతనం.</p>
              </div>
            </div>
          </div>

          <!-- Modern AP, Movement & 2014 Act -->
          <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-700/70">
            <h4 class="font-bold text-amber-300 text-sm mb-2">✊ ఆంధ్రోద్యమం, ప్రత్యేక రాష్ట్ర సాధన & 2014 విభజన చట్టం</h4>
            <ul class="space-y-1.5 list-disc list-inside">
              <li><b>సాంఘిక వైతాళికులు:</b> <b>కందుకూరి వీరేశలింగం</b> (ఆధునిక ఆంధ్ర వైతాళికుడు, 'వివేకవర్ధని', 1881 డిసెంబర్ 11న రాజమండ్రిలో తొలి వితంతు వివాహం, 'రాజశేఖర చరిత్ర' తొలి నవల). గురజాడ అప్పారావు ('కన్యాశుల్కం' నాటకం 1892). గిడుగు రామ్మూర్తి (వ్యావహారిక భాషోద్యమం).</li>
              <li><b>రంప విప్లవం (1922-1924):</b> <b>అల్లూరి సీతారామరాజు</b> మన్యం గిరిజనులతో బ్రిటిష్ వారి 1882 ఫారెస్ట్ యాక్ట్‌కు వ్యతిరేకంగా గెరిల్లా పోరాటం. చింతపల్లి, కృష్ణదేవిపేట ఠాణాలపై దాడులు. 1924 మే 7న కొయ్యూరు వద్ద మేజర్ రూథర్‌ఫర్డ్ కాల్చివేత.</li>
              <li><b>ఆంధ్ర రాష్ట్ర సాధన & శ్రీభాగ్ ఒప్పందం:</b> 1913 బాపట్లలో ప్రథమ ఆంధ్ర మహాసభ (బి.ఎన్. శర్మ అధ్యక్షత, కొండ వెంకటప్పయ్య). నవంబర్ 16, 1937న మద్రాసులో కోస్తా-రాయలసీమ నేతల మధ్య <b>శ్రీభాగ్ ఒప్పందం</b> (రాయలసీమకు రాజధాని/హైకోర్టు హామీ).</li>
              <li><b>అమరజీవి పొట్టి శ్రీరాములు బలిదానం:</b> మద్రాసులో బులుసు సాంబమూర్తి నివాసంలో 1952 అక్టోబర్ 19న ఆమరణ నిరాహారదీక్ష ప్రారంభం. <b>58 రోజుల సుదీర్ఘ దీక్ష అనంతరం డిసెంబర్ 15, 1952న అమరత్వం</b> పొందారు. ప్రధాని నెహ్రూ ప్రత్యేక రాష్ట్ర ప్రకటన చేశారు.</li>
              <li><b>ఆంధ్ర రాష్ట్రం & ఆంధ్రప్రదేశ్ ఆవిర్భావం:</b>
                <br>• <b>1953 అక్టోబర్ 1:</b> కర్నూలు రాజధానిగా, గుంటూరులో హైకోర్టుతో 11 జిల్లాలతో ప్రత్యేక ఆంధ్ర రాష్ట్రం అవతరణ (తొలి ముఖ్యమంత్రి: టంగుటూరి ప్రకాశం పంతులు "ఆంధ్రకేసరి", తొలి గవర్నర్: సి.ఎం. త్రివేది).
                <br>• <b>1956 నవంబర్ 1:</b> ఫజల్ అలీ కమిషన్ (SRC), ఫిబ్రవరి 20, 1956 నాటి పెద్దమనుషుల ఒప్పందం ప్రకారం ఆంధ్ర మరియు తెలంగాణ ప్రాంతాలు కలిసి హైదరాబాద్ రాజధానిగా ఉమ్మడి ఆంధ్రప్రదేశ్ అవతరించింది (తొలి సీఎం: నీలం సంజీవరెడ్డి).
              </li>
              <li><b>2014 ఆంధ్రప్రదేశ్ పునర్విభజన చట్టం (AP Reorganisation Act 2014):</b>
                <br>మార్చి 1, 2014న రాష్ట్రపతి ఆమోదం, జూన్ 2, 2014 నుండి అమలు. మొత్తం <b>12 భాగాలు, 108 సెక్షన్లు, 13 షెడ్యూళ్ళు</b>.
                <br>• సెక్షన్ 5: హైదరాబాద్ ఉమ్మడి రాజధానిగా 10 సంవత్సరాలు.
                <br>• సెక్షన్ 6: రాజధాని అధ్యయనానికి శివరామకృష్ణన్ కమిటీ.
                <br>• సెక్షన్ 46: ఉత్తరాంధ్ర & రాయలసీమ జిల్లాలకు ప్రత్యేక ఆర్థిక అభివృద్ధి ప్యాకేజీ.
                <br>• సెక్షన్ 90: పోలవరం ప్రాజెక్టుకు జాతీయ ప్రాజెక్టు హోదా (కేంద్ర ప్రభుత్వమే పూర్తి నిధులు సమకూరుస్తుంది).
                <br>• షెడ్యూల్ 13: విశాఖపట్నం రైల్వే జోన్, కడప స్టీల్ ప్లాంట్, పెట్రో కాంప్లెక్స్, గ్రీన్ ఫీల్డ్ రిఫైనరీ, ఐఐటీ తిరుపతి, ఐఐఎం వైజాగ్, ఎయిమ్స్ మంగళగిరి ఏర్పాటు హామీలు.
              </li>
            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 2: GEOGRAPHY (Ekam IAS 112-Page + RC Reddy 222-Page Notes) ==================== -->
    <section id="content-geo" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-blue-950 via-slate-800 to-slate-900 border border-blue-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-blue-900/60 text-blue-300 px-3 py-1 rounded-full border border-blue-700/50">Ekam IAS 112 పేజీల టెక్స్ట్‌బుక్ + RC రెడ్డి 222 పేజీల నోట్స్</span>
          <span class="text-xs text-slate-400">APPSC Group 1 & 2 • 30 మార్కులు</span>
        </div>
        <h2 class="text-2xl font-black text-white">ఆంధ్రప్రదేశ్ & భారత సమగ్ర భూగోళశాస్త్ర పాఠ్య గ్రంథం</h2>
        <p class="text-sm text-slate-300 mt-1">26 జిల్లాల పూర్తి ప్రొఫైల్, నదీ వ్యవస్థ, ప్రాజెక్టులు, నేలలు, అడవులు (ISFR), ఖనిజాలు, పారిశ్రామిక కారిడార్లు, జియోమార్ఫాలజీ & శీతోష్ణస్థితి.</p>
      </div>

      <!-- 26 Districts Master Table -->
      <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between items-start mb-3">
          <h3 class="text-base font-bold text-blue-400 flex items-center gap-2">
            <span>🗺️ ఆంధ్రప్రదేశ్ 26 జిల్లాల సమగ్ర ముఖచిత్రం (2022 పునర్విభజన)</span>
          </h3>
          <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
            <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
            <span>చదివాను</span>
          </label>
        </div>
        <p class="text-xs text-slate-300 mb-3">2022 ఏప్రిల్ 4న ఆంధ్రప్రదేశ్‌లో పార్లమెంటు నియోజకవర్గాల ప్రాతిపదికన 13 జిల్లాలను 26 జిల్లాలుగా పునర్విభజించారు. వైశాల్యంలో అతిపెద్ద జిల్లా <b>ప్రకాశం (14,322 చ.కి.మీ)</b>, అతిచిన్న జిల్లా <b>విశాఖపట్నం (1,048 చ.కి.మీ)</b>.</p>
        
        <div class="overflow-x-auto custom-scrollbar">
          <table class="w-full text-[11px] text-left border border-slate-700 rounded-lg">
            <thead class="bg-slate-900 text-blue-300 font-bold border-b border-slate-700">
              <tr>
                <th class="p-2">క్ర.సం.</th>
                <th class="p-2">జిల్లా పేరు</th>
                <th class="p-2">జిల్లా కేంద్రం</th>
                <th class="p-2">రెవెన్యూ డివిజన్లు</th>
                <th class="p-2">ముఖ్య నదులు / ప్రాజెక్టులు</th>
                <th class="p-2">పారిశ్రామిక & ఖనిజ ప్రాధాన్యత</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-slate-700/60 text-slate-300">
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">1</td><td class="p-2 font-bold text-white">శ్రీకాకుళం</td><td class="p-2">శ్రీకాకుళం</td><td class="p-2">శ్రీకాకుళం, టెక్కలి, పలాస</td><td class="p-2">వంశధార, నాగావళి, గొట్టా బ్యారేజ్</td><td class="p-2">జీడిపప్పు, భావనపాడు/మూలపేట పోర్టు, ఖాదీ (పాండూరు)</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">2</td><td class="p-2 font-bold text-white">విజయనగరం</td><td class="p-2">విజయనగరం</td><td class="p-2">విజయనగరం, బొబ్బిలి, చీపురుపల్లి</td><td class="p-2">చంపావతి, గోముఖి, సువర్ణముఖి</td><td class="p-2">మాంగనీస్, జనపనార పరిశ్రమ, బొబ్బిలి వీణలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">3</td><td class="p-2 font-bold text-white">పార్వతీపురం మన్యం</td><td class="p-2">పార్వతీపురం</td><td class="p-2">పార్వతీపురం, పాలకొండ</td><td class="p-2">నాగావళి, సువర్ణముఖి, వేగావతి, తోటపల్లి</td><td class="p-2">గిరిజన ప్రాంతం, ఉద్యాన పంటలు, రబ్బరు తోటలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">4</td><td class="p-2 font-bold text-white">అల్లూరి సీతారామరాజు</td><td class="p-2">పాడేరు</td><td class="p-2">పాడేరు, రంపచోడవరం, చింతూరు</td><td class="p-2">గోదావరి, శబరి, సీలేరు, పోలవరం బ్యాక్‌వాటర్</td><td class="p-2">అరకు కాఫీ (GI ట్యాగ్), బొర్రా గుహలు, బాక్సైట్, జలవిద్యుత్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">5</td><td class="p-2 font-bold text-white">విశాఖపట్నం</td><td class="p-2">విశాఖపట్నం</td><td class="p-2">విశాఖపట్నం, భీమునిపట్నం</td><td class="p-2">మేఘాద్రి గెడ్డ, ముడసర్లోవ</td><td class="p-2">వైజాగ్ స్టీల్, హిందుస్థాన్ షిప్‌యార్డ్, సహజ నౌకాశ్రయం, ఐటీ హబ్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">6</td><td class="p-2 font-bold text-white">అనకాపల్లి</td><td class="p-2">అనకాపల్లి</td><td class="p-2">అనకాపల్లి, నర్సీపట్నం</td><td class="p-2">శారద, వరాహ, తాండవ నదులు</td><td class="p-2">అనకాపల్లి బెల్లం మార్కెట్, బల్క్ డ్రగ్ పార్క్ (నక్కపల్లి), అచ్యుతాపురం SEZ</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">7</td><td class="p-2 font-bold text-white">కాకినాడ</td><td class="p-2">కాకినాడ</td><td class="p-2">కాకినాడ, పెద్దాపురం</td><td class="p-2">ఏలేరు నది, ఏలేరు రిజర్వాయర్</td><td class="p-2">డీప్ వాటర్ పోర్ట్, సహజవాయువు (KG బేసిన్), ఎరువుల కర్మాగారాలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">8</td><td class="p-2 font-bold text-white">డాక్టర్ బి.ఆర్. అంబేద్కర్ కోనసీమ</td><td class="p-2">అమలాపురం</td><td class="p-2">అమలాపురం, రామచంద్రపురం, కొత్తపేట</td><td class="p-2">గౌతమి, వశిష్ట గోదావరి శాఖలు</td><td class="p-2">కొబ్బరి, వరి, ఆక్వాకల్చర్, ఆయిల్ & గ్యాస్ నిల్వలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">9</td><td class="p-2 font-bold text-white">తూర్పు గోదావరి</td><td class="p-2">రాజమండ్రి</td><td class="p-2">రాజమండ్రి, కొవ్వూరు</td><td class="p-2">గోదావరి నది, ధవళేశ్వరం ఆనకట్ట</td><td class="p-2">పేపర్ మిల్స్, పూల నర్సరీలు (కడియం), సిరామిక్స్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">10</td><td class="p-2 font-bold text-white">పశ్చిమ గోదావరి</td><td class="p-2">భీమవరం</td><td class="p-2">భీమవరం, నరసాపురం</td><td class="p-2">గోదావరి డెల్టా కాలువలు</td><td class="p-2">ఆక్వాకల్చర్ హబ్ (రొయ్యల ఎగుమతి), లేస్ పరిశ్రమ (నరసాపురం)</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">11</td><td class="p-2 font-bold text-white">ఏలూరు</td><td class="p-2">ఏలూరు</td><td class="p-2">ఏలూరు, జంగారెడ్డిగూడెం, నూజివీడు</td><td class="p-2">తమ్మిలేరు, ఎర్రకాలువ, కొల్లేరు సరస్సు</td><td class="p-2">నూజివీడు మామిడి, కొల్లేరు చేపల పెంపకం, జూట్ పరిశ్రమ</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">12</td><td class="p-2 font-bold text-white">కృష్ణా</td><td class="p-2">మచిలీపట్నం</td><td class="p-2">మచిలీపట్నం, గుడివాడ, ఉయ్యూరు</td><td class="p-2">కృష్ణా డెల్టా, బందరు కాలువ</td><td class="p-2">మచిలీపట్నం గ్రీన్ ఫీల్డ్ పోర్ట్, కలంకారీ వస్త్రాలు, బంగారు ఆభరణాలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">13</td><td class="p-2 font-bold text-white">ఎన్టీఆర్ జిల్లా</td><td class="p-2">విజయవాడ</td><td class="p-2">విజయవాడ, నందిగామ, తిరువూరు</td><td class="p-2">కృష్ణా నది, ప్రకాశం బ్యారేజ్, బుడమేరు</td><td class="p-2">ఆటోనగర్ (ఆటోమొబైల్ హబ్), వాణిజ్య రాజధాని, కొండపల్లి బొమ్మలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">14</td><td class="p-2 font-bold text-white">గుంటూరు</td><td class="p-2">గుంటూరు</td><td class="p-2">గుంటూరు, తెనాలి</td><td class="p-2">కృష్ణా నది డెల్టా కాలువలు</td><td class="p-2">గుంటూరు మిర్చి యార్డ్ (ఆసియా అతిపెద్దది), పొగాకు బోర్డు, పత్తి జిన్నింగ్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">15</td><td class="p-2 font-bold text-white">పల్నాడు</td><td class="p-2">నరసరావుపేట</td><td class="p-2">నరసరావుపేట, సత్తెనపల్లి, గురజాల</td><td class="p-2">కృష్ణా నది, నాగార్జునసాగర్ కుడి కాలువ</td><td class="p-2">సున్నపురాయి, సిమెంట్ ఫ్యాక్టరీలు, కోటప్పకొండ</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">16</td><td class="p-2 font-bold text-white">బాపట్ల</td><td class="p-2">బాపట్ల</td><td class="p-2">బాపట్ల, చీరాల</td><td class="p-2">కొమ్మమూరు కాలువ, రోంపేరు</td><td class="p-2">చీరాల చేనేత (ఐటీసీ ప్యాకింగ్), వ్యవసాయ పరిశోధన కేంద్రాలు, సూర్యలంక బీచ్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">17</td><td class="p-2 font-bold text-white">ప్రకాశం</td><td class="p-2">ఒంగోలు</td><td class="p-2">ఒంగోలు, కనిగిరి, మార్కాపురం</td><td class="p-2">గుండ్లకమ్మ, మూసి, పాలేరు, వెలిగొండ</td><td class="p-2">గెలాక్సీ గ్రానైట్ (చీమకుర్తి), ఒంగోలు జాతి గిత్తలు, పలకల పరిశ్రమ (మార్కాపురం)</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">18</td><td class="p-2 font-bold text-white">శ్రీ పొట్టి శ్రీరాములు నెల్లూరు</td><td class="p-2">నెల్లూరు</td><td class="p-2">నెల్లూరు, కావలి, కందుకూరు, ఆత్మకూరు</td><td class="p-2">పెన్నా, స్వర్ణముఖి, సోమశిల ప్రాజెక్ట్</td><td class="p-2">రైస్ బౌల్, కృష్ణపట్నం ఓడరేవు, రొయ్యల సాగు, మైకా నిల్వలు (గూడూరు)</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">19</td><td class="p-2 font-bold text-white">కర్నూలు</td><td class="p-2">కర్నూలు</td><td class="p-2">కర్నూలు, ఆదోని, పత్తికొండ</td><td class="p-2">తుంగభద్ర, హంద్రీ, సుంకేసుల బ్యారేజ్</td><td class="p-2">ఓర్వకల్ సోలార్ పార్క్, డ్రోన్ సిటీ, సున్నపురాయి, పత్తి మార్కెట్ (ఆదోని)</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">20</td><td class="p-2 font-bold text-white">నంద్యాల</td><td class="p-2">నంద్యాల</td><td class="p-2">నంద్యాల, డోన్, ఆత్మకూరు</td><td class="p-2">కుందూ నది, శ్రీశైలం డ్యామ్ ప్రాజెక్ట్</td><td class="p-2">శ్రీశైలం మల్లన్న క్షేత్రం, నల్లమల అడవులు, సిమెంట్ పరిశ్రమలు, బెలూమ్ గుహలు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">21</td><td class="p-2 font-bold text-white">అనంతపురం</td><td class="p-2">అనంతపురం</td><td class="p-2">అనంతపురం, గుంతకల్లు, కళ్యాణదుర్గం</td><td class="p-2">పెన్నా, చిత్రಾವతి, HNSS కాలువలు</td><td class="p-2">వేరుశనగ సాగు, గుంతకల్లు రైల్వే జంక్షన్, పవన & సౌర విద్యుత్ ప్రాజెక్టులు</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">22</td><td class="p-2 font-bold text-white">శ్రీ సత్యసాయి</td><td class="p-2">పుట్టపర్తి</td><td class="p-2">పుట్టపర్తి, పెనుగొండ, కదిరి, ధర్మవరం</td><td class="p-2">చిత్రావతి, పెన్నా, కుషావతి</td><td class="p-2">కియా (KIA) మోటార్స్ కార్ల ప్లాంట్, ధర్మవరం పట్టు చీరలు, లేపాక్షి శిల్పకళ</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">23</td><td class="p-2 font-bold text-white">వైఎస్సార్ కడప</td><td class="p-2">కడప</td><td class="p-2">కడప, జమ్మలమడుగు, బద్వేల్</td><td class="p-2">పెన్నా, పాపాఘ్ని, కుందూ, గండికోట</td><td class="p-2">బారైటీస్ (మంగంపేట 98%), యురేనియం (తుమ్మలపల్లి), గండికోట కాన్యన్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">24</td><td class="p-2 font-bold text-white">అన్నమయ్య</td><td class="p-2">రాయచోటి</td><td class="p-2">రాయచోటి, మదనపల్లి, రాజంపేట</td><td class="p-2">బాహుదా, మండవ్య, చెయ్యేరు/అన్నమయ్య డ్యామ్</td><td class="p-2">మదనపల్లి టమాటా మార్కెట్, హార్సిలీ హిల్స్ వేసవి విడిది, పట్టు పరిశ్రమ</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">25</td><td class="p-2 font-bold text-white">చిత్తూరు</td><td class="p-2">చిత్తూరు</td><td class="p-2">చిత్తూరు, కుప్పం, పలమనేరు, నగరి</td><td class="p-2">కుశాస్థలి, పొన్నై నదులు</td><td class="p-2">బెల్లం, మామిడి గుజ్జు పరిశ్రమ, పాడి పరిశ్రమ, కుప్పం గ్రానైట్</td></tr>
              <tr class="hover:bg-slate-700/40"><td class="p-2 font-bold">26</td><td class="p-2 font-bold text-white">తిరుపతి</td><td class="p-2">తిరుపతి</td><td class="p-2">తిరుపతి, గూడూరు, శ్రీకాళహస్తి, సూళ్లూరుపేట</td><td class="p-2">స్వర్ణముఖి, పులికాట్ సరస్సు</td><td class="p-2">తిరుమల బాలాజీ, శ్రీహరికోట ఇస్రో (SHAR), శ్రీసిటీ SEZ, ఎలక్ట్రానిక్స్ హబ్</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Physical Geography & River Systems -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-blue-400 flex items-center gap-2">
              <span>🌊 ఆంధ్రప్రదేశ్ నదీ వ్యవస్థ & బహుళార్థసాధక ప్రాజెక్టులు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>గోదావరి నది (దక్షిణ గంగ - 1,465 కి.మీ):</b> మహారాష్ట్ర నాసిక్ త్రయంబకేశ్వర్ వద్ద జన్మిస్తుంది. ఏపీలో పోలవరం వద్ద మైదానంలోకి ప్రవేశించి <b>ధవళేశ్వరం ఆనకట్ట (సర్ ఆర్థర్ కాటన్ 1852)</b> వద్ద 7 శాఖలుగా చీలి బంగాళాఖాతంలో కలుస్తుంది (గౌతమి, వశిష్ట, వైనతేయ, ఆత్రేయ, భరద్వాజ, కౌశిక, తుల్య).
              <br>• <b>పోలవరం ప్రాజెక్ట్ (ఇందిరా సాగర్):</b> 194 TMCల స్థూల నిల్వ, 7.2 లక్షల ఎకరాల ఆయకట్టు, విశాఖకు 23.4 TMCల తాగునీరు, 960 MW జలవిద్యుత్, కృష్ణా-గోదావరి అనుసంధానం.
            </li>
            <li>• <b>కృష్ణా నది (1,400 కి.మీ):</b> మహాబలేశ్వర్ (మహారాష్ట్ర) వద్ద జన్మిస్తుంది. ప్రధాన ఉపనదులు: తుంగభద్ర, భీమా, కొయినా, మూసి, దిండి, మున్నేరు.
              <br>• ప్రాజెక్టులు: జూరాల, శ్రీశైలం (నీలం సంజీవరెడ్డి సాగర్), నాగార్జునసాగర్ (ప్రపంచంలోనే అతిపెద్ద రాతి కట్టడం - 1967), పులిచింతల (కేఎల్ రావు ప్రాజెక్ట్), ప్రకాశం బ్యారేజ్ (విజయవాడ - 1855).
            </li>
            <li>• <b>రాయలసీమ ఎత్తిపోతల & ప్రాజెక్టులు:</b> పోతిరెడ్డిపాడు హెడ్‌రెగ్యులేటర్, తెలుగు గంగ ప్రాజెక్ట్ (చెన్నైకి 15 TMC తాగునీరు), గాలేరు-నగరి (GNSS), హంద్రీ-నీవా (HNSS - 565 కి.మీ), వెలిగొండ ప్రాజెక్ట్ (నల్లమల గుండా 18.8 కి.మీ డబుల్ టన్నెల్).</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-blue-400 flex items-center gap-2">
              <span>🌾 నేలలు, అడవులు (ISFR 2023) & జీవవైవిధ్యం</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>నేలల విస్తీర్ణం (ICAR):</b>
              <br>1. <b>ఎరుపు నేలలు (Red Soils - 65%):</b> ఐరన్ ఆక్సైడ్ వల్ల ఎరుపు రంగు. నత్రజని, ఫాస్ఫరస్ తక్కువ. వేరుశనగ, పప్పుధాన్యాల సాగు.
              <br>2. <b>నల్లరేగడి నేలలు (Black/Regur Soils - 25%):</b> బసాల్ట్ శిలల శైథిల్యం, మాంట్ మోరిల్లోనైట్ బంకమన్ను. తేమను నిలుపుకునే గుణం ఎక్కువ. పత్తి, పొగాకు, మిరప సాగు.
              <br>3. <b>ఒండ్రు నేలలు (Alluvial - 5%):</b> అత్యంత సారవంతమైనవి (డెల్టా ప్రాంతాలు - వరి, చెరకు).
              <br>4. <b>లేటరైట్ నేలలు:</b> అధిక ఉష్ణోగ్రత, అధిక వర్షపాతం వల్ల లీచింగ్ ప్రక్రియతో ఏర్పడతాయి (జీడిమామిడి, కాఫీ).
            </li>
            <li>• <b>అటవీ విస్తీర్ణం (ISFR నివేదిక):</b> ఏపీ భౌగోళిక విస్తీర్ణంలో అడవులు దాదాపు <b>29,784 చ.కి.మీ (18.28%)</b>. రికార్డెడ్ ఫారెస్ట్ ఏరియా 22.86%.
              <br>• అతిపెద్ద అభయారణ్యం: <b>నాగార్జునసాగర్-శ్రీశైలం టైగర్ రిజర్వ్ (NSTR - 3,728 చ.కి.మీ)</b> - దేశంలోనే అతిపెద్ద పులుల అభయారణ్యం.
              <br>• బయోస్పియర్ రిజర్వ్: <b>శేషాచలం బయోస్పియర్ రిజర్వ్ (2010)</b> - ఎర్రచందనం (Pterocarpus santalinus) నిలయం.
              <br>• మడ అడవులు (Mangroves): <b>కోరింగ (కాకినాడ)</b> - దేశంలో సుందర్బన్స్ తర్వాత 2వ అతిపెద్ద మడ అడవులు.
              <br>• పక్షుల కేంద్రాలు: తేలినీలపురం (శ్రీకాకుళం - పెలికాన్లు), పులికాట్ & నేలపట్టు (నెల్లూరు - ఫ్లెమింగో ఫెస్టివల్), కొల్లేరు (రామ్‌సర్ చిత్తడి నేల సైట్).
            </li>
          </ul>
        </div>
      </div>

      <!-- Geomorphology & Climatology (RC Reddy Notes) -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-indigo-400 flex items-center gap-2">
              <span>🌐 భూస్వరూప శాస్త్రం & కాల గణన లెక్కలు (RC రెడ్డి నోట్స్)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>అక్షాంశాలు & రేఖాంశాలు:</b> మొత్తం అక్షాంశాలు 181 (భూమధ్యరేఖ అతిపెద్ద 'గ్రేట్ సర్కిల్'). 1° అక్షాంశం = దాదాపు 111 కి.మీ. మొత్తం రేఖాంశాలు 360. 0° గ్రీనిచ్ ప్రైమ్ మెరిడియన్, 180° అంతర్జాతీయ దినరేఖ (IDL - బేరింగ్ జలసంధి గుండా పోతుంది).</li>
            <li>• <b>సమయ గణన సూత్రం (Time Zone Formula):</b>
              <br>భూమి $360^\circ$ తిరగడానికి 24 గంటలు పడుతుంది $\Rightarrow 1^\circ = 4	ext{ నిమిషాలు}, 15^\circ = 1	ext{ గంట}$.
              <br>• గ్రీనిచ్ నుండి తూర్పునకు వెళ్లేకొద్దీ సమయాన్ని కలపాలి (EGA - East Gain Add).
              <br>• పశ్చిమానికి వెళ్లేకొద్దీ సమయాన్ని తీసివేయాలి (WLS - West Lose Subtract).
              <br>• భారత ప్రామాణిక రేఖాంశం (IST): $82rac{1}{2}^\circ$ తూర్పు రేఖాంశం (కాకినాడ, అలహాబాద్ మీదుగా వెళ్తుంది). గ్రీనిచ్ సమయం కంటే <b>+5 గంటల 30 నిమిషాలు ముందుంటుంది</b>.
            </li>
            <li>• <b>భూ అంతర్నిర్మాణ డిస్‌కంటిన్యూటీలు (Discontinuities):</b>
              <br>1. కాన్రాడ్: పై క్రస్ట్ (SIAL) & కింది క్రస్ట్ (SIMA) మధ్య
              <br>2. మోహోరోవిసిక్ (మోహో): క్రస్ట్ & మ్యాంటిల్ మధ్య
              <br>3. రెపెట్టి: ఎగువ మ్యాంటిల్ & దిగువ మ్యాంటిల్ మధ్య
              <br>4. గుటెన్‌బర్గ్: మ్యాంటిల్ & కోర్ (NIFE) మధ్య
              <br>5. లేమాన్: ఔటర్ కోర్ (ద్రవ) & ఇన్నర్ కోర్ (ఘన) మధ్య.
            </li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-indigo-400 flex items-center gap-2">
              <span>💨 శీతోష్ణస్థితి, పవనాలు & స్థానిక గాలులు (Local Winds)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>వాతావరణ ఆవరణాలు:</b> ట్రోపోస్పియర్ (0-13/18 కి.మీ, వాతావరణ మార్పులు, లాప్స్ రేట్ 1°C per 165m), స్ట్రాటోస్పియర్ (13-50 కి.మీ, ఓజోన్ పొర 25-35 కి.మీ, జెట్ విమానాల ప్రయాణం), మీసోస్పియర్ (50-80 కి.మీ, అతిశీతల పొర -100°C), థర్మోస్పియర్/అయనోస్పియర్ (80-400 కి.మీ, రేడియో తరంగాల పరావర్తనం, అరోరాలు).</li>
            <li>• <b>ప్రపంచ స్థానిక పవనాలు (Local Winds Table):</b>
              <br>• <b>లూ (Loo):</b> ఉత్తర భారతదేశంలో వేసవిలో వీచే వేడి గాలులు.
              <br>• <b>చినూక్ (Chinook - "మంచు భక్షకి/Snow Eater"):</b> రాకీ పర్వతాల తూర్పు వాలుల్లో వీచే వేడి పొడి గాలులు (అమెరికా, కెనడా).
              <br>• <b>ఫోయిన్ (Foehn):</b> ఆల్ప్స్ పర్వతాల మీదుగా స్విట్జర్లాండ్‌లో వీచే వేడి గాలులు.
              <br>• <b>హర్మట్టాన్ (Harmattan - "డాక్టర్ పవనాలు"):</b> సహారా నుండి పశ్చిమ ఆఫ్రికా తీరం వైపు వీచే పొడి గాలులు.
              <br>• <b>సిరోకో (Sirocco - "బ్లడ్ రెయిన్"):</b> సహారా నుండి ఇటలీ వైపు వీచి ఎర్రటి ధూళితో వర్షం కురిపించే గాలులు.
              <br>• <b>శాంటా అనా:</b> కాలిఫోర్నియా వేసవి వేడి గాలులు.
              <br>• <b>మిస్ట్రల్ & బోరా:</b> యూరప్‌లో వీచే అతి శీతల గాలులు.
            </li>
            <li>• <b>తుఫాను పూర్వపు వర్షాలు:</b> మామిడి జల్లులు (Mango Showers - ఏపీ & కేరళ), చెర్రీ బ్లోసమ్స్ (కర్ణాటక కాఫీ తోటలు), కాల్‌బైశాఖి (పశ్చిమ బెంగాల్ & ఒడిశా వరి, జనపనార), నార్వెస్టర్స్ (అస్సాం టీ తోటలు).</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 3: DISASTER MANAGEMENT (RC REDDY NOTES) ==================== -->
    <section id="content-disaster" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-red-950 via-slate-800 to-slate-900 border border-red-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-red-900/60 text-red-300 px-3 py-1 rounded-full border border-red-700/50">RC రెడ్డి IAS స్టడీ సర్కిల్ • రామన్ రాజు క్లాస్ నోట్స్</span>
          <span class="text-xs text-slate-400">APPSC గ్రూప్ 1, 2, 3 & AEE స్పెషల్</span>
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
        <p class="text-xs text-slate-300 mb-4 leading-relaxed">2004 హిందూ మహాసముద్ర సునామీ అనంతరం, భారత పార్లమెంట్ <b>డిసెంబర్ 23, 2005</b>న విపత్తు నిర్వహణ చట్టాన్ని ఆమోదించింది. ఇది దేశంలో సహాయ వితరణ విధానం నుండి ముందస్తు నివారణ & ఉపశమన విధానానికి మార్గదర్శకంగా నిలిచింది.</p>
        
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
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-red-300 flex items-center gap-2">
              <span>🌋 భూకంపాలు & సునామీలు (Earthquakes & Tsunamis)</span>
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
            <li>• <b>స్కేల్స్:</b> రిక్టర్ స్కేల్ (లాగరిథమిక్ 0-9 పరిమాణం), మెర్కల్లి స్కేల్ (1-12 తీవ్రత నష్టం).</li>
            <li>• <b>భారత సిస్మిక్ జోన్లు:</b> BIS ప్రకారం 4 జోన్లు (Zone II, III, IV, V). దేశంలో దాదాపు <b>59% భూభాగం</b> భూకంప ప్రమాద జోన్లలో ఉంది. జోన్ V అత్యంత ప్రమాదకరమైనది.</li>
            <li>• <b>సునామీ (Tsunami):</b> జపనీస్ పదం (Tsu = తీరం, Nami = అల). <b>26 డిసెంబర్ 2004</b> సుమత్రా భూకంపం (9.1 M) వల్ల వచ్చిన సునామీతో భారత్‌లో 10,000+ మంది ప్రాణాలు కోల్పోయారు.</li>
            <li>• <b>ITEWC:</b> ఇండియన్ సునామీ ఎర్లీ వార్నింగ్ సెంటర్ <b>INCOIS (హైదరాబాద్)</b> లో 2007లో ఏర్పాటయింది.</li>
          </ul>
        </div>

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
            <li>• <b>కరువు (Drought):</b> సాధారణ వర్షపాతం కన్నా 26-50% లోటు = మధ్యస్థ కరువు, 50% పైగా లోటు = తీవ్ర కరువు. దేశ సాగు విస్తీర్ణంలో 68% ప్రాంతం కరువుకు లోనవుతుంది. పథకాలు: DPAP (1973), DDP (1977).</li>
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
            <li>• <b>భోపాల్ గ్యాస్ విషాదం (డిసెంబర్ 2-3, 1984):</b> మధ్యప్రదేశ్‌లోని యూనియన్ కార్బైడ్ ఫ్యాక్టరీ నుండి విడుదలైన <b>మిథైల్ ఐసోసైనైట్ (MIC - C₂H₃NO)</b> వాయువు వల్ల వేలాది మంది ప్రాణాలు కోల్పోయారు. దేశంలో అతిపెద్ద పారిశ్రామిక విపత్తు.</li>
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

    <!-- ==================== TAB 4: AP POLICIES 4.0 (2024-2029) ==================== -->
    <section id="content-policies" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-emerald-950 via-slate-800 to-slate-900 border border-emerald-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-emerald-900/60 text-emerald-300 px-3 py-1 rounded-full border border-emerald-700/50">ఆంధ్రప్రదేశ్ ప్రభుత్వం • 2024–2029 అధికారిక జీవోలు</span>
          <span class="text-xs text-slate-400">21 పేజీల పూర్తి విధానాల సమాహారం</span>
        </div>
        <h2 class="text-2xl font-black text-white">ఆంధ్రప్రదేశ్ నూతన పారిశ్రామిక & రంగాలవారీ విధానాలు 4.0</h2>
        <p class="text-sm text-slate-300 mt-1">₹30 లక్షల కోట్ల పెట్టుబడుల లక్ష్యం, 5 లక్షల నూతన ఉద్యోగాలు, 10 రంగాల సమగ్ర విధానాలు, G.O. నంబర్లు మరియు ఆర్థిక రాయితీల విశ్లేషణ.</p>
      </div>

      <!-- Master Policies Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Policy 1 & 2 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-emerald-400 flex items-center gap-2">
              <span>🏭 1. ప్రైవేట్ పార్కులు & ఇండస్ట్రియల్ డెవలప్‌మెంట్ 4.0</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>ప్రైవేట్ పారిశ్రామిక పార్కుల విధానం 4.0:</b>
              <br>• ప్లగ్-అండ్-ప్లే మౌలిక సదుపాయాలతో ప్రైవేట్ భాగస్వామ్యంతో పారిశ్రామిక పార్కులు.
              <br>• భూ వినియోగ మార్పిడి (NALA), జోనింగ్, లేఅవుట్ మరియు స్టాంప్ డ్యూటీ ఛార్జీలు 100% మినహాయింపు.
              <br>• MSME పార్కులకు ₹3 కోట్ల వరకు లేదా ప్రాజెక్ట్ వ్యయంలో 30% మూలధన సబ్సిడీ.
              <br>• పెద్ద పారిశ్రామిక పార్కులకు (100 ఎకరాల పైబడి) మౌలిక వసతుల కల్పనకు ₹10 కోట్ల వరకు గ్రాంట్.
            </li>
            <li>• <b>AP ఇండస్ట్రియల్ డెవలప్‌మెంట్ పాలసీ 4.0 (AP IDP 4.0):</b>
              <br>• <b>లక్ష్యం:</b> ₹30 లక్షల కోట్ల తయారీ రంగ పెట్టుబడులు, 5 లక్షల కొత్త ఉద్యోగాలు.
              <br>• <b>రతన్ టాటా ఇన్నోవేషన్ హబ్:</b> అమరావతిలో ప్రధాన కేంద్రం, విశాఖపట్నం, రాజమండ్రి, తిరుపతి, అనంతపురంలో ప్రాంతీయ కేంద్రాలు.
              <br>• పారిశ్రామిక విద్యుత్‌పై యూనిట్‌కు ₹1 రాయితీ (5 సంవత్సరాలు).
              <br>• మహిళా మరియు SC/ST పారిశ్రామికవేత్తలకు అదనంగా 10% మూలధన రాయితీ.
            </li>
          </ul>
        </div>

        <!-- Policy 3 & 4 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-emerald-400 flex items-center gap-2">
              <span>🌱 2. MSME 2030 & ఫుడ్ ప్రాసెసింగ్ 4.0</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>AP MSME పాలసీ 4.0 (వన్ ఫ్యామిలీ - వన్ ఎంట్రప్రెన్యూర్):</b>
              <br>• రాష్ట్రంలోని మొత్తం <b>175 అసెంబ్లీ నియోజకవర్గాల్లో</b> MSME పార్కుల ఏర్పాటు.
              <br>• మైక్రో ఎంటర్‌ప్రైజెస్‌కు 35% మూలధన రాయితీ (గరిష్టంగా ₹35 లక్షలు).
              <br>• క్రెడిట్ గ్యారెంటీ ఫండ్ ట్రస్ట్ ఫర్ మైక్రో & స్మాల్ ఎంటర్‌ప్రైజెస్ (CGTMSE) వార్షిక గ్యారెంటీ రుసుము 100% రీయింబర్స్‌మెంట్.
              <br>• కాలుష్య నియంత్రణ పరికరాల కొనుగోలుపై 50% రాయితీ (₹10 లక్షల వరకు).
            </li>
            <li>• <b>AP సమగ్ర ఫుడ్ ప్రాసెసింగ్ విధానం 4.0 (G.O.Ms.No.71):</b>
              <br>• <b>లక్ష్యం:</b> ₹30,000 కోట్ల నూతన పెట్టుబడులు, 30 లక్షల మందికి ప్రత్యక్ష, పరోక్ష ఉపాధి.
              <br>• ఆక్వా, మామిడి, అరటి, మిరప, టమాటా ఆధారిత మెగా ఫుడ్ పార్కులకు 50% మూలధన రాయితీ.
              <br>• కోల్డ్ చైన్ నెట్‌వర్క్, ఎగుమతి నాణ్యతా ల్యాబ్‌ల స్థాపనకు ₹5 కోట్ల వరకు ఆర్థిక సహాయం.
            </li>
          </ul>
        </div>

        <!-- Policy 5 & 6 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-emerald-400 flex items-center gap-2">
              <span>🧵 3. టెక్స్‌టైల్ (TAG 4.0) & ఎలక్ట్రానిక్స్ (ECMP 4.0)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>టెక్స్‌టైల్, అపారెల్ & గార్మెంట్స్ విధానం 4.0 (G.O.Ms.No.89):</b>
              <br>• <b>లక్ష్యం:</b> ₹10,000 కోట్ల పెట్టుబడులు, 2 లక్షల మందికి ఉపాధి (70% మహిళలు).
              <br>• హిందూపురం, రాయదుర్గం, అనంతపురం, బ్రాండిక్స్ (విశాఖ) క్లస్టర్ల బలోపేతం.
              <br>• నూలు మిల్లులకు మరియు గార్మెంట్ యూనిట్లకు కరెంట్ ఛార్జీలపై యూనిట్‌కు ₹1.50 రాయితీ.
              <br>• మహిళా కార్మికులకు ప్రతినెలా ₹1,000 చొప్పున 3 సంవత్సరాలు జీతాల ప్రోత్సాహకం.
            </li>
            <li>• <b>ఎలక్ట్రానిక్స్ కాంపోనెంట్స్ తయారీ విధానం 4.0 (G.O.Ms.No.5):</b>
              <br>• <b>లక్ష్యం:</b> $50 బిలియన్ల వార్షిక ఉత్పత్తి లక్ష్యం, తిరుపతి-శ్రీసిటీ, కొప్పర్తి (కడప) ఎలక్ట్రానిక్స్ తయారీ క్లస్టర్లు (EMC).
              <br>• సెమీకండక్టర్ & డిస్‌ప్లే ఫ్యాబ్ విధానం 4.0 (G.O.Ms.No.7): కేంద్ర ప్రభుత్వ ప్రోత్సాహకాలతో పాటు రాష్ట్ర ప్రభుత్వం 40% అదనపు మూలధన సపోర్ట్.
            </li>
          </ul>
        </div>

        <!-- Policy 7 & 8 -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-emerald-400 flex items-center gap-2">
              <span>🛸 4. డ్రోన్ పాలసీ 4.0 & క్లీన్ ఎనర్జీ / SEMP EV విధానం</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>ఆంధ్రప్రదేశ్ డ్రోన్ పాలసీ 4.0 (G.O.Ms.No.18):</b>
              <br>• <b>ఓర్వకల్ డ్రోన్ సిటీ (కర్నూలు):</b> 300 ఎకరాల్లో డ్రోన్ టెస్టింగ్ ట్రాక్, తయారీ హబ్ మరియు శిక్షణ అకాడమీ.
              <br>• 40,000 మంది యువతకు డ్రోన్ పైలట్, అసెంబ్లింగ్ శిక్షణ.
              <br>• వ్యవసాయంలో ఎరువులు, పురుగుమందుల పిచికారీ కొరకు రైతులకు 5,000 డ్రోన్ల పంపిణీకి రాయితీ.
            </li>
            <li>• <b>సస్టైనబుల్ ఎలక్ట్రిక్ మొబిలిటీ విధానం 4.0 (G.O.Ms.No.88 - SEMP):</b>
              <br>• 2029 నాటికి 2 లక్షల ద్విచక్ర, 10,000 త్రిచక్ర, 20,000 వాణిజ్య EV వాహనాలు రోడ్లపైకి తేవడం.
              <br>• 100% APSRTC బస్సులను ఎలక్ట్రిక్ బస్సులుగా మార్చే కార్యాచరణ.
              <br>• EV ఛార్జింగ్ స్టేషన్ల స్థాపనకు కరెంట్ టారిఫ్‌లలో 25% రాయితీ, రోడ్ ట్యాక్స్ 100% మినహాయింపు.
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 5: MENTAL ABILITY & APTITUDE ==================== -->
    <section id="content-aptitude" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-cyan-950 via-slate-800 to-slate-900 border border-cyan-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-cyan-900/60 text-cyan-300 px-3 py-1 rounded-full border border-cyan-700/50">228 పేజీల సమగ్ర పాఠ్య పుస్తకం • 120+ షార్ట్‌కట్ ఫార్ములాలు</span>
          <span class="text-xs text-slate-400">APPSC Group 1 & 2 • 30 మార్కులు</span>
        </div>
        <h2 class="text-2xl font-black text-white">క్వాంటిటేటివ్ ఆప్టిట్యూడ్ & మెంటల్ ఎబిలిటీ మాస్టర్ బుక్</h2>
        <p class="text-sm text-slate-300 mt-1">సంపూర్ణ అధ్యాయాలు: క్షేత్రమితి, రైళ్ల లెక్కలు, మిశ్రమాలు, కాలం-పని, చక్రవడ్డీ-బారువడ్డీ, గడియారాలు, క్యాలెండర్, సిలాజిజమ్ & షార్ట్‌కట్లు.</p>
      </div>

      <!-- Quantitative Formulas Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Mensuration 2D & 3D -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-cyan-400 flex items-center gap-2">
              <span>📐 1. క్షేత్రమితి (Mensuration 2D & 3D)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>స్కేలింగ్ నియమం (Scaling Rule - గోల్డెన్ షార్ట్‌కట్):</b>
              <div class="bg-slate-900/90 p-2 rounded border border-slate-700 font-mono text-amber-300 text-center text-xs my-1">
                పొడవు/వ్యాసార్థం: k రెట్లు $\to$ వైశాల్యం: k² రెట్లు $\to$ ఘనపరిమాణం: k³ రెట్లు
              </div>
              ఉదాహరణ: గోళం వ్యాసార్థం 3 రెట్లు పెరిగితే వైశాల్యం $3^2=9$ రెట్లు, ఘనపరిమాణం $3^3=27$ రెట్లు పెరుగుతుంది.
            </li>
            <li>• <b>2D సూత్రాలు:</b>
              <br>• చతురస్రం: వైశాల్యం $A = a^2 = \frac{1}{2}d^2$, కర్ణం $d = a\sqrt{2}$.
              <br>• సమబాహు త్రిభుజం: వైశాల్యం $A = \frac{\sqrt{3}}{4}a^2$, ఎత్తు $h = \frac{\sqrt{3}}{2}a$.
              <br>• వృత్తం: వైశాల్యం $A = \pi r^2$, చుట్టుకొలత $P = 2\pi r$. అర్ధవృత్త చుట్టుకొలత $= \frac{36}{7}r$.
            </li>
            <li>• <b>3D సూత్రాలు:</b>
              <br>• సమఘనం (Cube): ఘనపరిమాణం $V = a^3$, మొత్తం ఉపరితల వైశాల్యం $TSA = 6a^2$, కర్ణం $d = a\sqrt{3}$.
              <br>• స్థూపం (Cylinder): ఘనపరిమాణం $V = \pi r^2 h$, వక్రతల వైశాల్యం $CSA = 2\pi rh$.
              <br>• శంకువు (Cone): ఘనపరిమాణం $V = \frac{1}{3}\pi r^2 h$, ఏటవాలు ఎత్తు $l = \sqrt{r^2 + h^2}$.
              <br>• గోళం (Sphere): ఘనపరిమాణం $V = \frac{4}{3}\pi r^3$, ఉపరితల వైశాల్యం $A = 4\pi r^2$.
            </li>
          </ul>
        </div>

        <!-- Trains, Speed & Distance -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-cyan-400 flex items-center gap-2">
              <span>🚆 2. రైళ్లు & సాపేక్ష వేగం (Trains & Relative Speed)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>వేగం యూనిట్ల మార్పిడి:</b>
              <div class="bg-slate-900/90 p-2 rounded border border-slate-700 font-mono text-cyan-300 text-center text-xs my-1">
                km/h నుండి m/s కి మార్చడానికి: × 5/18<br>
                m/s నుండి km/h కి మార్చడానికి: × 18/5
              </div>
            </li>
            <li>• <b>సాపేక్ష వేగం (Relative Speed):</b>
              <br>• రెండు రైళ్లు <b>ఎదురెదురుగా</b> వస్తే: వేగం = $S_1 + S_2$.
              <br>• రెండు రైళ్లు <b>ఒకే దిశలో</b> వెళ్తుంటే: వేగం = $|S_1 - S_2|$.
            </li>
            <li>• <b>రైలు వస్తువులను దాటడానికి పట్టే సమయం:</b>
              <br>• స్తంభం / మనిషిని దాటడానికి: సమయం $= \frac{\text{రైలు పొడవు }(L)}{S}$.
              <br>• ప్లాట్‌ఫారమ్ / వంతెన / సొరంగాన్ని దాటడానికి: సమయం $= \frac{L_{\text{రైలు}} + L_{\text{ప్లాట్‌ఫారమ్}}}{S}$.
            </li>
            <li>• <b>బోట్లు & ప్రవాహాలు:</b> ప్రవాహ దిశలో వేగం (Downstream) $= u + v$; ప్రవాహ వ్యతిరేక దిశలో వేగం (Upstream) $= u - v$. నిశ్చల నీటిలో పడవ వేగం $u = \frac{\text{Downstream} + \text{Upstream}}{2}$.</li>
          </ul>
        </div>

        <!-- Interest & Mixtures -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-cyan-400 flex items-center gap-2">
              <span>💰 3. వడ్డీ లెక్కలు & మిశ్రమాలు (Interest & Mixtures)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>చక్రవడ్డీ - బారువడ్డీ తేడా (CI - SI Difference):</b>
              <br>• 2 సంవత్సరాలకు: $\text{Difference} = P \left(\frac{R}{100}\right)^2$
              <br>• 3 సంవత్సరాలకు: $\text{Difference} = P \left(\frac{R}{100}\right)^2 \left(3 + \frac{R}{100}\right)$
            </li>
            <li>• <b>రూల్ ఆఫ్ 72 (Rule of 72):</b> చక్రవడ్డీతో సొమ్ము రెట్టింపు కావడానికి పట్టే కాలం $t \approx \frac{72}{R}$ సంవత్సరాలు. (ఉదా: 8% వడ్డీ అయితే $72/8 = 9$ ఏళ్లలో సొమ్ము రెట్టింపు అవుతుంది).</li>
            <li>• <b>మిశ్రమాల పునరావృత భర్తీ సూత్రం (Repeated Dilution):</b>
              <br>V పరిమాణం గల స్వచ్ఛమైన ద్రవం నుండి x లీటర్లు తీసివేసి నీటితో n సార్లు భర్తీ చేస్తే, మిగిలిన స్వచ్ఛమైన ద్రవం:
              <div class="bg-slate-900/90 p-2 rounded border border-slate-700 font-mono text-amber-300 text-center text-xs my-1">
                మిగిలిన పరిమాణం = V [ 1 - (x / V) ]ⁿ
              </div>
            </li>
            <li>• <b>లాభ నష్టాల స్పెషల్ కేసు:</b> రెండు వస్తువులను ఒకే అమ్మకం ధరకు అమ్మి, ఒకదానిపై x% లాభం, రెండవదానిపై x% నష్టం వస్తే, వ్యాపారంలో ఎల్లప్పుడూ <b>నష్టమే</b> వస్తుంది: $\text{నష్టం }\% = \left(\frac{x}{10}\right)^2\%$.</li>
          </ul>
        </div>

        <!-- Clocks, Calendar & Syllogism -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-cyan-400 flex items-center gap-2">
              <span>⏰ 4. గడియారాలు, క్యాలెండర్ & సిలాజిజమ్</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>గడియారంలో ముల్లుల మధ్య కోణం (Angle Formula):</b>
              <div class="bg-slate-900/90 p-2 rounded border border-slate-700 font-mono text-cyan-300 text-center text-xs my-1">
                కోణం (θ) = | 30H - (11/2)M |
              </div>
              ఉదాహరణ: 4 గంటల 20 నిమిషాల వద్ద కోణం: $|30(4) - 5.5(20)| = |120 - 110| = 10^\circ$.
            </li>
            <li>• <b>ముల్లుల స్థానాలు:</b> 1 గంటలో 1 సారి ఏకీభవిస్తాయి, 12 గంటల్లో 11 సార్లు, 24 గంటల్లో <b>22 సార్లు</b> ఏకీభవిస్తాయి (రెండు ముల్లులు సరళరేఖలో వ్యతిరేకంగా ఉండటం కూడా 22 సార్లు, లంబంగా 44 సార్లు).</li>
            <li>• <b>క్యాలెండర్ విషమ రోజులు (Odd Days):</b> సాధారణ సంవత్సరంలో 1 విషమ రోజు (52 వారాలు + 1 రోజు). లీపు సంవత్సరంలో 2 విషమ రోజులు. 100 సంవత్సరాల్లో 5, 200 ఏళ్లలో 3, 300 ఏళ్లలో 1, 400 ఏళ్లలో <b>0 విషమ రోజులు</b>.</li>
            <li>• <b>సిలాజిజమ్ (Syllogism - Either-Or నిబంధనలు):</b> రెండు ముగింపులలో ఒకే అంశాలు (Subject, Predicate) ఉండాలి, ఒకటి సకారాత్మకం (Positive) మరియు రెండవది నకారాత్మకం (Negative) అయి ఉండాలి, రెండూ వ్యక్తిగతంగా తప్పు (Individually False) కావాలి.</li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 6: POLITY & CONSTITUTION ==================== -->
    <section id="content-polity" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-purple-950 via-slate-800 to-slate-900 border border-purple-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-purple-900/60 text-purple-300 px-3 py-1 rounded-full border border-purple-700/50">APPSC Group 1 & 2 • 30 మార్కులు</span>
          <span class="text-xs text-slate-400">భారత రాజ్యాంగం, వ్యవస్థలు, హక్కులు & 73/74 సవరణలు</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారత రాజ్యాంగం, పాలన & ముఖ్య ఆర్టికల్స్ సమగ్ర గైడ్</h2>
        <p class="text-sm text-slate-300 mt-1">ప్రాథమిక హక్కులు (ఆర్టికల్స్ 12-35), ఆదేశిక సూత్రాలు, 73 & 74 సవరణలు, అత్యవసర అధికారాలు మరియు రాజ్యాంగ సంస్థలు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Fundamental Rights & DPSP -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-purple-400 flex items-center gap-2">
              <span>⚖️ 1. ప్రాథమిక హక్కులు & ఆదేశిక సూత్రాలు</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>భాగం III - ప్రాథమిక హక్కులు (ఆర్టికల్స్ 12–35 - అమెరికా నుండి గ్రహించబడినవి):</b>
              <br>• ఆర్టికల్ 14: చట్టం ముందు సమానత్వం, సమాన రక్షణ.
              <br>• ఆర్టికల్ 17: అస్పృశ్యత నివారణ (Untouchability).
              <br>• ఆర్టికల్ 19: 6 ప్రాథమిక స్వేచ్ఛలు (వాక్ స్వాతంత్య్రం, సమావేశం, సంఘం, సంచారం, నివాసం, వృత్తి).
              <br>• ఆర్టికల్ 21: జీవించే హక్కు & వ్యక్తిగత స్వేచ్ఛ (మేనకా గాంధీ కేసు 1978, కేఎస్ పుట్టస్వామి తీర్పు 2017 - గోప్యతా హక్కు).
              <br>• ఆర్టికల్ 21A: 6-14 ఏళ్ల పిల్లలకు ఉచిత నిర్బంధ విద్య (86వ సవరణ 2002).
              <br>• ఆర్టికల్ 32: రాజ్యాంగ పరిహార హక్కు (డా. అంబేద్కర్ దీనిని "రాజ్యాంగానికి ఆత్మ & హృదయం" అన్నారు). 5 రిట్లు: హెబియస్ కార్పస్, మాండమస్, ప్రొహిబిషన్, సెర్షియోరరి, కో-వారెంటో.
            </li>
            <li>• <b>భాగం IV - ఆదేశిక సూత్రాలు (DPSP - ఆర్టికల్స్ 36–51 - ఐర్లాండ్ నుండి గ్రహించబడినవి):</b>
              <br>• ఆర్టికల్ 40: గ్రామ పంచాయతీల ఏర్పాటు.
              <br>• ఆర్టికల్ 44: ఉమ్మడి పౌరస్మృతి (Uniform Civil Code - UCC).
              <br>• ఆర్టికల్ 45: 6 ఏళ్ల లోపు పిల్లలకు బాల్య సంరక్షణ & విద్య.
              <br>• ఆర్టికల్ 50: కార్యనిర్వాహక శాఖ నుండి న్యాయశాఖ వేరుచేయడం.
              <br>• ఆర్టికల్ 51: అంతర్జాతీయ శాంతి, భద్రతల పరిరక్షణ.
            </li>
            <li>• <b>భాగం IVA - ప్రాథమిక విధులు (ఆర్టికల్ 51A - USSR నుండి):</b> 42వ సవరణ 1976 (స్వరణ్ సింగ్ కమిటీ) ద్వారా 10 విధులు చేర్చారు. 86వ సవరణ 2002 ద్వారా 11వ విధి (తల్లిదండ్రులు పిల్లలకు విద్యావకాశం కల్పించడం) చేర్చబడింది.</li>
          </ul>
        </div>

        <!-- 73rd, 74th Amendments & Emergency -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-purple-400 flex items-center gap-2">
              <span>🗳️ 2. స్థానిక సంస్థలు (73 & 74 సవరణలు) & ఎమర్జెన్సీ</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>73వ రాజ్యాంగ సవరణ చట్టం (1992 - పంచాయతీరాజ్):</b>
              <br>• భాగం IX, ఆర్టికల్స్ 243 నుండి 243-O. <b>11వ షెడ్యూల్ (29 అంశాలు)</b>.
              <br>• 3-అంచెల వ్యవస్థ: గ్రామ పంచాయతీ, మండల పరిషత్, జిల్లా పరిషత్.
              <br>• ఆర్టికల్ 243D: మహిళలకు కనీసం 1/3 (33%) రిజర్వేషన్లు (ఏపీలో 50%).
              <br>• ఆర్టికల్ 243I: రాష్ట్ర ఆర్థిక సంఘం (SFC), ఆర్టికల్ 243K: రాష్ట్ర ఎన్నికల సంఘం (SEC).
              <br>• కమిటీలు: బల్వంతరాయ్ మెహతా (1957 - 3 అంచెలు), అశోక్ మెహతా (1977 - 2 అంచెలు), ఎల్.ఎం. సింఘ్వీ (1986 - రాజ్యాంగ హోదా).
            </li>
            <li>• <b>74వ రాజ్యాంగ సవరణ చట్టం (1992 - నగరపాలికలు):</b> భాగం IXA, ఆర్టికల్స్ 243P నుండి 243ZG, <b>12వ షెడ్యూల్ (18 అంశాలు)</b>.</li>
            <li>• <b>అత్యవసర అధికారాలు (భాగం XVIII):</b>
              <br>• <b>ఆర్టికల్ 352:</b> జాతీయ అత్యవసర పరిస్థితి (యుద్ధం, విదేశీ దురాక్రమణ, సాయుధ తిరుగుబాటు).
              <br>• <b>ఆర్టికల్ 356:</b> రాష్ట్రపతి పాలన (రాష్ట్రంలో రాజ్యాంగ యంత్రాంగం విఫలమైనప్పుడు).
              <br>• <b>ఆర్టికల్ 360:</b> ఆర్థిక అత్యవసర పరిస్థితి (భారతదేశంలో ఇప్పటివరకు ఒక్కసారి కూడా విధించలేదు).
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 7: ECONOMY & FINANCIAL MARKETS ==================== -->
    <section id="content-economy" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-yellow-950 via-slate-800 to-slate-900 border border-yellow-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-yellow-900/60 text-yellow-300 px-3 py-1 rounded-full border border-yellow-700/50">Ekam IAS సమగ్ర ఆర్థిక మార్కెట్ల గైడ్ (6 పేజీలు)</span>
          <span class="text-xs text-slate-400">APPSC Group 1 & 2 • 30 మార్కులు</span>
        </div>
        <h2 class="text-2xl font-black text-white">భారతీయ ఆర్థిక వ్యవస్థ & ద్రవ్య మార్కెట్ల సమగ్ర విశ్లేషణ</h2>
        <p class="text-sm text-slate-300 mt-1">మనీ మార్కెట్ వర్గీకరణ, ట్రెజరీ బిల్లులు (T-Bills), కమర్షియల్ పేపర్స్ (CP), సర్టిఫికేట్ ఆఫ్ డిపాజిట్ (CD), కాల్ మనీ, ఆర్బీఐ మానిటరీ పాలసీ & నీతి ఆయోగ్ సూచీలు.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
        <!-- Money Market Instruments (Ekam IAS Notes) -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-yellow-400 flex items-center gap-2">
              <span>🏦 1. భారతీయ ద్రవ్య మార్కెట్ సాధనాలు (Money Market Instruments)</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <p class="text-xs text-slate-400 mb-2">ద్రవ్య మార్కెట్ (Money Market) అనేది <b>1 సంవత్సరం లేదా అంతకంటే తక్కువ కాలపరిమితి</b> గల స్వల్పకాలిక నిధుల లావాదేవీల వ్యవస్థ. దీనిని ఆర్బీఐ (RBI) నియంత్రిస్తుంది.</p>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>ట్రెజరీ బిల్లులు (Treasury Bills - T-Bills):</b>
              <br>• కేంద్ర ప్రభుత్వం తరఫున స్వల్పకాలిక నగదు అవసరాల కొరకు ఆర్బీఐ వేలం వేస్తుంది.
              <br>• ఇవి జీరో-కూపన్ బాండ్లు (Zero-coupon bonds) - ముఖ విలువపై డిస్కౌంట్‌తో జారీ అయి, మెచ్యూరిటీ వద్ద పూర్తి ముఖ విలువను చెల్లిస్తారు.
              <br>• <b>మూడు రకాల కాలపరిమితులు:</b>
              <br>&nbsp;&nbsp;1. 91 రోజుల T-Bills (వారానికోసారి బుధవారం వేలం)
              <br>&nbsp;&nbsp;2. 182 రోజుల T-Bills (రెండు వారాలకోసారి వేలం)
              <br>&nbsp;&nbsp;3. 364 రోజుల T-Bills (రెండు వారాలకోసారి వేలం)
              <br>• కనీస పెట్టుబడి మొత్తం: <b>₹25,000</b> (మరియు దాని గుణిజాలు).
            </li>
            <li>• <b>క్యాష్ మేనేజ్‌మెంట్ బిల్స్ (CMBs):</b> అత్యంత స్వల్పకాలిక నగదు కొరత (91 రోజుల కంటే తక్కువ) కొరకు ప్రభుత్వం జారీ చేసే సాధనం (2010 లో ప్రారంభం).</li>
            <li>• <b>కమర్షియల్ పేపర్స్ (Commercial Paper - CP):</b> అత్యధిక క్రెడిట్ రేటింగ్ కలిగిన కార్పొరేట్ కంపెనీలు వర్కింగ్ క్యాపిటల్ కొరకు జారీ చేసే ప్రామిసరీ నోట్ (1990 లో ప్రవేశపెట్టారు). కాలపరిమితి: 7 రోజుల నుండి 1 సంవత్సరం వరకు. కనీస పెట్టుబడి: <b>₹5 లక్షలు</b>.</li>
            <li>• <b>సర్టిఫికేట్ ఆఫ్ డిపాజిట్ (CD):</b> షెడ్యూల్డ్ వాణిజ్య బ్యాంకులు మరియు ఆర్థిక సంస్థలు జారీ చేసే బదిలీ చేయగల డిపాజిట్ రసీదు (1989 లో ప్రారంభం). కాలపరిమితి: 7 రోజుల నుండి 1 సంవత్సరం. కనీసం ₹1 లక్ష.</li>
          </ul>
        </div>

        <!-- Inter-bank Money & RBI Monetary Policy -->
        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <div class="flex justify-between items-start mb-3">
            <h3 class="text-base font-bold text-yellow-400 flex items-center gap-2">
              <span>📊 2. ఇంటర్‌బ్యాంక్ మార్కెట్ & ఆర్బీఐ ద్రవ్య విధానం</span>
            </h3>
            <label class="flex items-center space-x-1.5 text-xs text-slate-400 cursor-pointer">
              <input type="checkbox" class="study-check rounded border-slate-700 text-amber-500" onchange="updateProgress()">
              <span>చదివాను</span>
            </label>
          </div>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>ఇంటర్‌బ్యాంక్ మార్కెట్ (కాల్ / నోటీస్ / టర్మ్ మనీ):</b>
              <br>• <b>కాల్ మనీ (Call Money):</b> కేవలం <b>1 రోజు (Overnight)</b> వ్యవధికి బ్యాంకులు పరస్పరం ఇచ్చిపుచ్చుకునే రుణాలు.
              <br>• <b>నోటీస్ మనీ (Notice Money):</b> <b>2 రోజుల నుండి 14 రోజుల</b> వ్యవధికి తీసుకునే నిధులు.
              <br>• <b>టర్మ్ మనీ (Term Money):</b> <b>15 రోజుల నుండి 1 సంవత్సరం</b> వరకు తీసుకునే రుణాలు.
            </li>
            <li>• <b>ఆర్బీఐ ద్రవ్యోల్బణ నియంత్రణ సాధనాలు (Monetary Tools):</b>
              <br>• <b>రెపో రేటు (Repo Rate):</b> వాణిజ్య బ్యాంకులకు ఆర్బీఐ ఇచ్చే స్వల్పకాలిక రుణాలపై వసూలు చేసే వడ్డీ రేటు. రెపో పెంచితే మార్కెట్లో ద్రవ్య సరఫరా తగ్గి ద్రవ్యోల్బణం అదుపులోకి వస్తుంది.
              <br>• <b>రివర్స్ రెపో రేటు:</b> ఆర్బీఐ వద్ద బ్యాంకులు డిపాజిట్ చేసిన మిగులు నిధులపై ఆర్బీఐ ఇచ్చే వడ్డీ రేటు.
              <br>• <b>CRR (నగదు నిల్వల నిష్పత్తి):</b> బ్యాంకులు తమ డిపాజిట్లలో తప్పనిసరిగా ఆర్బీఐ వద్ద ఉంచాల్సిన నగదు శాతం.
              <br>• <b>SLR (చట్టబద్ధ ద్రవ్యత్వ నిష్పత్తి):</b> బ్యాంకులు బంగారం, ప్రభుత్వ సెక్యూరిటీల రూపంలో నిల్వ ఉంచాల్సిన శాతం.
            </li>
            <li>• <b>ద్రవ్యోల్బణం కొలమానాలు:</b>
              <br>• <b>CPI (వినియోగదారుల ధరల సూచీ):</b> రిటైల్ ద్రవ్యోల్బణం. ఆర్బీఐ ద్రవ్య విధానానికి ప్రామాణికం (లక్ష్యం: 4% ± 2%).
              <br>• <b>WPI (టోకు ధరల సూచీ):</b> వాణిజ్య & పారిశ్రామిక మంత్రిత్వ శాఖ విడుదల చేస్తుంది.
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 8: SOLVED APPSC PYQS HUB ==================== -->
    <section id="content-pyqs" class="tab-content space-y-6 hidden">
      <div class="bg-gradient-to-r from-amber-950 via-slate-800 to-slate-900 border border-amber-800/40 p-6 rounded-2xl shadow-md">
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <span class="text-xs font-bold uppercase tracking-wider bg-amber-900/60 text-amber-300 px-3 py-1 rounded-full border border-amber-700/50">APPSC అధికారిక మునుపటి ప్రశ్నలు (PYQs)</span>
          <span class="text-xs text-slate-400">Group 1, Group 2, Group 3, AEE, Town Planning అసలైన ప్రశ్నలు</span>
        </div>
        <h2 class="text-2xl font-black text-white">115+ సాల్వ్డ్ APPSC ప్రశ్నలు & సమాధానాల నిధి</h2>
        <p class="text-sm text-slate-300 mt-1">మునుపటి అధికారిక పరీక్షల ప్రశ్నలు. ఆప్షన్ పై క్లిక్ చేయండి - సమాధానం మరియు అధికారిక విశ్లేషణను వెంటనే తెలుసుకోండి!</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-5" id="pyqQuizGrid">
        <!-- Q1 -->
        <div class="topic-card bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
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
        <div class="topic-card bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
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
        <div class="topic-card bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
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
        <div class="topic-card bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
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
        <div class="topic-card bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">Town Planning 2012</span>
            <span class="text-xs text-slate-400">Q.5</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">ఆంధ్రప్రదేశ్ తీరప్రాంతాన్ని వణికించిన దివిసీమ పెనుతుఫాను ఏ తేదీన సంభవించింది?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'నవంబర్ 15 కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) 15 నవంబర్ 1977</button>
            <button onclick="checkPyq(this, true, 'నవంబర్ 19, 1977న కృష్ణా జిల్లా దివిసీమను తాకింది. 6 మీటర్ల ఎత్తున ఉప్పెన అలలతో 10,000+ మంది ప్రాణాలు కోల్పోయారు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) 19 నవంబర్ 1977</button>
            <button onclick="checkPyq(this, false, 'తప్పు సంవత్సరం.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) 19 నవంబర్ 1978</button>
            <button onclick="checkPyq(this, false, 'తప్పు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) 25 అక్టోబర్ 1977</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>

        <!-- Q6 -->
        <div class="topic-card bg-slate-800 border border-slate-700 p-5 rounded-2xl shadow-sm">
          <div class="flex justify-between items-center mb-2">
            <span class="text-xs font-bold text-blue-400">APPSC Group-I Prelims</span>
            <span class="text-xs text-slate-400">Q.6</span>
          </div>
          <p class="text-sm font-semibold text-slate-100 mb-3">శాతవాహనుల కాలంలో 'గాథాసప్తశతి' గ్రంథాన్ని ప్రాకృతంలో రచించిన రాజు ఎవరు?</p>
          <div class="space-y-2 text-xs">
            <button onclick="checkPyq(this, false, 'గౌతమీపుత్ర శాతకర్ణి గొప్ప పాలకుడు కానీ రచయిత కాదు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">A) గౌతమీపుత్ర శాతకర్ణి</button>
            <button onclick="checkPyq(this, true, '17వ శాతవాహన రాజు హాలుడు గాథాసప్తశతిని రచించి కవివత్సలుడు అనే బిరుదు పొందాడు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">B) హాలుడు (Hala)</button>
            <button onclick="checkPyq(this, false, 'శ్రీముఖుడు రాజ్య స్థాపకుడు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">C) శ్రీముఖుడు</button>
            <button onclick="checkPyq(this, false, 'యజ్ఞశ్రీ శాతకర్ణి ఓడ గుర్తు నాణేలు ముద్రించాడు.')" class="w-full text-left p-2.5 rounded-lg bg-slate-900 hover:bg-slate-700 transition border border-slate-700">D) యజ్ఞశ్రీ శాతకర్ణి</button>
          </div>
          <div class="pyq-exp hidden mt-3 p-2.5 rounded-lg bg-slate-900/90 text-xs border border-slate-700"></div>
        </div>
      </div>
    </section>

    <!-- ==================== TAB 9: MAINS & ETHICS GUIDE ==================== -->
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
            <li>• <b>1. పరిచయం (Introduction - 2-3 లైన్లు):</b> ప్రశ్నలోని కీలక భావన నిర్వచనం, చారిత్రక/రాజ్యాంగ నేపథ్యం లేదా ఇటీవలి నివేదిక/కరెంట్ అఫైర్స్ సందర్భం.</li>
            <li>• <b>2. ప్రధాన భాగం (Body):</b> కారణాలు, ప్రభావాలు, సవాళ్లు, ప్రభుత్వ చర్యలు. బులెట్ పాయింట్లు, ఉపశీర్షికలు మరియు ఏపీ సంబంధిత ఉదాహరణలతో సమతుల్య విశ్లేషణ.</li>
            <li>• <b>3. వే ఫార్వర్డ్ & ముగింపు (Way Forward & Conclusion):</b> సమస్య పరిష్కారానికి ఆచరణాత్మక సూచనలు, రాజ్యాంగ విలువలతో కూడిన సకారాత్మక ముగింపు.</li>
            <li>• <b>సమయ నిర్వహణ:</b> 10% ప్లానింగ్ + 80% రాత + 10% రివిజన్. కఠినమైన ప్రశ్న వద్ద సమయం వృథా చేయకుండా సులభమైన వాటితో ప్రారంభించండి.</li>
          </ul>
        </div>

        <div class="topic-card bg-slate-800 border border-slate-700/80 rounded-2xl p-5 shadow-sm">
          <h3 class="text-base font-bold text-pink-300 mb-2">⚖️ ఎథిక్స్ సిద్ధాంతాలు, కేస్ స్టడీస్ & ఇంటర్వ్యూ</h3>
          <ul class="text-xs text-slate-300 space-y-2 leading-relaxed">
            <li>• <b>నైతిక సిద్ధాంతాలు:</b> యుటిలిటేరియనిజం (గరిష్ట మందికి గరిష్ట మేలు), డియోంటాలజీ (కర్తవ్యమే ప్రధానం - కాంట్), వర్చ్యూ ఎథిక్స్ (సచ్ఛీలత, నిష్పక్షపాతత, నిజాయితీ).</li>
            <li>• <b>కేస్ స్టడీ రాత విధానం:</b> సమస్య గుర్తింపు → వాటాదారులు (Stakeholders) → నైతిక వైరుధ్యాలు (Ethical Dilemmas) → సాధ్యమైన ప్రత్యామ్నాయాలు → ఉత్తమ చర్య & చట్టపరమైన కారణాలు.</li>
            <li>• <b>పారదర్శకత సాధనాలు:</b> సమాచార హక్కు చట్టం (RTI 2005), లోక్‌పాల్ & లోకాయుక్త, సిటిజన్ చార్టర్.</li>
            <li>• <b>ఇంటర్వ్యూ (Personality Test):</b> DAF (అప్లికేషన్ ఫారమ్) లో రాసిన ప్రతి అంశంపై పట్టు. హోమ్‌ స్టేట్ సమస్యలు, సమతుల్య దృక్పథం, నిజాయితీగా "తెలియదు" అని వినయంగా చెప్పడం.</li>
          </ul>
        </div>
      </div>
    </section>

  </main>

  <!-- Footer -->
  <footer class="bg-slate-950 border-t border-slate-800 text-slate-400 py-8 px-4 text-center text-xs no-print">
    <div class="max-w-7xl mx-auto space-y-2">
      <p class="text-slate-200 font-bold">లక్ష్య డైలీ తెలుగు కరెంట్ అఫైర్స్ & APPSC స్టడీ పోర్టల్</p>
      <p>APPSC Group 1, Group 2, Group 3, TSPSC, UPSC & పోలీస్ పరీక్షల సమగ్ర డిజిటల్ రిసోర్స్ హబ్</p>
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
        localStorage.setItem('appsc_full_topic_' + idx, cb.checked);
      });
      const pct = total > 0 ? Math.round((checkedCount / total) * 100) : 0;
      document.getElementById('progressBar').style.width = pct + '%';
      document.getElementById('progressText').innerText = `మీరు అధ్యయనం చేసిన అధ్యాయాలు: ${checkedCount} / ${total} (${pct}% పూర్తి)`;
    }

    // Load saved checklist progress
    window.addEventListener('DOMContentLoaded', () => {
      const checkboxes = document.querySelectorAll('.study-check');
      checkboxes.forEach((cb, idx) => {
        const saved = localStorage.getItem('appsc_full_topic_' + idx);
        if (saved === 'true') cb.checked = true;
      });
      updateProgress();
    });

    // Real-time Search Filter across all topic cards
    function filterTopics() {
      const query = document.getElementById('subjectSearch').value.toLowerCase().trim();
      const cards = document.querySelectorAll('.topic-card');
      
      cards.forEach(card => {
        const text = card.innerText.toLowerCase();
        if (!query || text.includes(query)) {
          card.style.display = '';
        } else {
          card.style.display = 'none';
        }
      });
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

    function shareToWhatsApp() {
      const text = encodeURIComponent("🎯 *లక్ష్య APPSC గ్రూప్ 1 & 2 సమగ్ర డిజిటల్ టెక్స్ట్‌బుక్ పోర్టల్!*\nభారత & ఏపీ సమగ్ర చరిత్ర, భూగోళశాస్త్రం (26 జిల్లాలు), విపత్తు నిర్వహణ, ఏపీ విధానాలు 4.0 & 228 పేజీల మెంటల్ ఎబిలిటీ:\n👉 https://lakshya-telugu-ca.onrender.com/appsc_syllabus");
      window.open('https://api.whatsapp.com/send?text=' + text, '_blank');
    }
  </script>
</body>
</html>
"""
