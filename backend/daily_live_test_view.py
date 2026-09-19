# -*- coding: utf-8 -*-
"""
Interactive Computer Based Test (CBT) Live Mock Test View.
Route: /daily_live_test
Features:
- Real-time 15:00 Countdown timer with auto-submit
- Question Palette with 4 states (Answered, Not Answered, Marked for Review, Not Visited)
- Standard APPSC/TSPSC marking scheme (+1 / -0.33)
- Instant Animated Scorecard with Detailed Explanations
"""

from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def render_daily_live_test_html(date=None):
    if not date:
        date = datetime.now(IST).strftime("%Y-%m-%d")
        
    return f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>లక్ష్య డైలీ ఆన్‌లైన్ లైవ్ మాక్ టెస్ట్ (CBT) - {date}</title>
  <!-- PWA Meta -->
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#1e3a8a">
  <link rel="icon" type="image/jpeg" href="/lakshya_logo.jpg">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body {{
      font-family: 'Nirmala UI', 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: #f8fafc;
      color: #0f172a;
    }}
    .palette-btn {{
      transition: all 0.15s ease-in-out;
    }}
    .palette-answered {{ background-color: #16a34a !important; color: white !important; }}
    .palette-not-answered {{ background-color: #dc2626 !important; color: white !important; }}
    .palette-review {{ background-color: #9333ea !important; color: white !important; }}
    .palette-not-visited {{ background-color: #e2e8f0; color: #475569; }}
    .palette-current {{ ring: 3px solid #2563eb; transform: scale(1.08); font-weight: 900; }}
  </style>
</head>
<body class="min-h-screen flex flex-col bg-slate-100">

  <!-- Top CBT Header -->
  <header class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white shadow-md sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center space-x-3">
        <a href="/" class="p-1.5 bg-blue-800/80 hover:bg-blue-700 rounded-lg text-white transition" title="డ్యాష్‌బోర్డ్‌కు వెళ్లండి">
          <i data-lucide="arrow-left" class="w-5 h-5"></i>
        </a>
        <div>
          <h1 class="text-base sm:text-lg font-black tracking-tight flex items-center gap-2">
            🎯 లక్ష్య డైలీ లైవ్ మాక్ టెస్ట్ (CBT)
            <span class="bg-emerald-500 text-white text-2xs uppercase tracking-wider px-2 py-0.5 rounded-full font-bold animate-pulse">LIVE</span>
          </h1>
          <p class="text-xs text-slate-300">తేదీ: {date} • APPSC & TSPSC తాజా సిలబస్ ప్రామాణికం</p>
        </div>
      </div>

      <!-- Real-time Timer Box -->
      <div class="flex items-center space-x-3">
        <div id="timerContainer" class="bg-slate-800/90 border border-slate-700 px-3.5 py-1.5 rounded-xl flex items-center space-x-2 shadow-inner">
          <i data-lucide="clock" id="timerIcon" class="w-5 h-5 text-amber-400"></i>
          <div>
            <div class="text-2xs text-slate-400 uppercase tracking-wider font-semibold">మిగిలిన సమయం</div>
            <div id="timerDisplay" class="text-lg font-black text-amber-300 font-mono leading-none">15:00</div>
          </div>
        </div>
        <button onclick="confirmSubmit()" class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm px-4 py-2 rounded-xl transition shadow-md flex items-center space-x-1.5">
          <i data-lucide="check-circle-2" class="w-4 h-4"></i>
          <span>సమర్పించు</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Offline Banner -->
  <div id="offlineNotice" class="hidden bg-amber-500 text-slate-950 text-xs font-bold py-1.5 px-4 text-center">
    📡 మీరు ఆఫ్‌లైన్‌లో ఉన్నారు. టెస్ట్ పూర్తి చేసి మీ మార్కులను ఇక్కడే చూసుకోవచ్చు.
  </div>

  <!-- Loading State -->
  <div id="testLoading" class="flex-1 flex flex-col items-center justify-center p-8">
    <div class="w-12 h-12 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
    <p class="text-base font-bold text-slate-700">నేటి 20 ప్రాక్టీస్ ప్రశ్నలు లోడ్ అవుతున్నాయి...</p>
    <p class="text-xs text-slate-500 mt-1">డైలీ కరెంట్ అఫైర్స్ & జనరల్ స్టడీస్ నిపుణుల ప్రశ్నల బృందం</p>
  </div>

  <!-- Main CBT Test Interface -->
  <main id="cbtTestContainer" class="hidden flex-1 max-w-7xl w-full mx-auto p-3 sm:p-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
    
    <!-- Left: Question & Options Area (3 cols) -->
    <div class="lg:col-span-3 flex flex-col bg-white rounded-2xl shadow-sm border border-slate-200 overflow-hidden">
      
      <!-- Question Subheader -->
      <div class="bg-slate-50 border-b border-slate-200 px-5 py-3.5 flex flex-wrap justify-between items-center gap-2">
        <div class="flex items-center space-x-2">
          <span id="currentQBadge" class="bg-blue-600 text-white text-xs font-black px-2.5 py-1 rounded-lg">
            ప్రశ్న 1 / 20
          </span>
          <span id="currentSubjectBadge" class="bg-blue-100 text-blue-800 text-xs font-bold px-2.5 py-1 rounded-lg">
            సమకాలీన అంశాలు
          </span>
        </div>
        <div class="text-xs text-slate-500 font-semibold">
          మార్కింగ్: <span class="text-emerald-600 font-bold">+1.00</span> | <span class="text-rose-600 font-bold">-0.33</span>
        </div>
      </div>

      <!-- Question Text -->
      <div class="p-6 flex-1">
        <h2 id="questionText" class="text-base sm:text-lg font-bold text-slate-900 leading-relaxed mb-6">
          ప్రశ్న లోడ్ అవుతోంది...
        </h2>

        <!-- Radio Options Container -->
        <div id="optionsContainer" class="space-y-3">
          <!-- Dynamically populated -->
        </div>
      </div>

      <!-- Action Footer Controls -->
      <div class="bg-slate-50 border-t border-slate-200 p-4 flex flex-wrap justify-between items-center gap-3">
        <div class="flex items-center space-x-2">
          <button onclick="markForReview()" class="bg-purple-100 hover:bg-purple-200 text-purple-800 border border-purple-300 font-bold text-xs sm:text-sm px-3.5 py-2 rounded-xl transition flex items-center space-x-1.5">
            <i data-lucide="flag" class="w-4 h-4"></i>
            <span>రివ్యూ కోసం ఉంచు (Review)</span>
          </button>
          <button onclick="clearResponse()" class="bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold text-xs sm:text-sm px-3.5 py-2 rounded-xl transition flex items-center space-x-1.5">
            <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
            <span>క్లియర్ చేయి</span>
          </button>
        </div>

        <div class="flex items-center space-x-2">
          <button id="prevBtn" onclick="navigateQuestion(-1)" class="bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xs sm:text-sm px-4 py-2 rounded-xl transition disabled:opacity-40 disabled:cursor-not-allowed flex items-center space-x-1">
            <i data-lucide="chevron-left" class="w-4 h-4"></i>
            <span>మునుపటిది</span>
          </button>
          <button id="nextBtn" onclick="saveAndNext()" class="bg-blue-600 hover:bg-blue-500 text-white font-black text-xs sm:text-sm px-5 py-2 rounded-xl transition shadow-sm flex items-center space-x-1">
            <span>సేవ్ & నెక్స్ట్</span>
            <i data-lucide="chevron-right" class="w-4 h-4"></i>
          </button>
        </div>
      </div>

    </div>

    <!-- Right: Question Palette & Overview (1 col) -->
    <div class="lg:col-span-1 flex flex-col space-y-4">
      
      <!-- Palette Card -->
      <div class="bg-white rounded-2xl p-4 shadow-sm border border-slate-200">
        <h3 class="text-xs font-black uppercase text-slate-500 tracking-wider mb-3">ప్రశ్నల ప్యాలెట్ (Question Palette)</h3>
        
        <!-- Palette Grid -->
        <div id="paletteGrid" class="grid grid-cols-5 gap-2 mb-4">
          <!-- 20 Buttons generated dynamically -->
        </div>

        <!-- Palette Legends -->
        <div class="pt-3 border-t border-slate-200 grid grid-cols-2 gap-2 text-2xs font-semibold text-slate-600">
          <div class="flex items-center space-x-1.5">
            <span class="w-3.5 h-3.5 rounded bg-emerald-600 inline-block"></span>
            <span>సమాధానం ఇచ్చినవి (<span id="countAnswered">0</span>)</span>
          </div>
          <div class="flex items-center space-x-1.5">
            <span class="w-3.5 h-3.5 rounded bg-rose-600 inline-block"></span>
            <span>ఇవ్వనివి (<span id="countNotAnswered">0</span>)</span>
          </div>
          <div class="flex items-center space-x-1.5">
            <span class="w-3.5 h-3.5 rounded bg-purple-600 inline-block"></span>
            <span>రివ్యూ (<span id="countReview">0</span>)</span>
          </div>
          <div class="flex items-center space-x-1.5">
            <span class="w-3.5 h-3.5 rounded bg-slate-200 inline-block"></span>
            <span>సందర్శించనివి (<span id="countNotVisited">20</span>)</span>
          </div>
        </div>

        <!-- Submit Button in Palette -->
        <button onclick="confirmSubmit()" class="mt-4 w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-black text-sm py-2.5 rounded-xl shadow-md transition flex items-center justify-center space-x-2">
          <i data-lucide="send" class="w-4 h-4"></i>
          <span>పరీక్షను ముగించు (Submit)</span>
        </button>
      </div>

      <!-- Guidelines Reminder Card -->
      <div class="bg-blue-50/70 border border-blue-200 rounded-2xl p-4 text-xs text-blue-900 space-y-1.5">
        <div class="font-bold flex items-center gap-1.5 text-blue-950">
          <i data-lucide="info" class="w-4 h-4 text-blue-600"></i>
          <span>పరీక్ష సూచనలు</span>
        </div>
        <p>• ప్రతి సరైన ప్రశ్నకు +1 మార్కు లభిస్తుంది.</p>
        <p>• ప్రతి తప్పు ప్రశ్నకు 1/3 (-0.33) మార్కు కోత విధించబడుతుంది.</p>
        <p>• 15 నిమిషాలు పూర్తి కాగానే టెస్ట్ ఆటోమేటిక్‌గా సమర్పించబడుతుంది.</p>
      </div>

    </div>

  </main>

  <!-- Result & Scorecard Modal / Screen -->
  <section id="resultContainer" class="hidden flex-1 max-w-5xl w-full mx-auto p-4 sm:p-6 my-auto">
    <div class="bg-white rounded-3xl shadow-xl border border-slate-200 overflow-hidden">
      
      <!-- Top Score Header Banner -->
      <div id="resultBanner" class="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 sm:p-8 text-center relative">
        <div class="inline-flex items-center gap-2 bg-amber-400 text-slate-950 text-xs font-black px-3.5 py-1 rounded-full uppercase tracking-wider mb-2" id="resBadge">
          🏆 టాపర్ లెవెల్
        </div>
        <h2 class="text-2xl sm:text-3xl font-black mb-1">మీ పరీక్ష ఫలితాల నివేదిక</h2>
        <p id="resFeedback" class="text-xs sm:text-sm text-slate-200 max-w-xl mx-auto">
          అద్భుతమైన ప్రతిభ! మీ ప్రిపరేషన్ అగ్రస్థానంలో ఉంది.
        </p>

        <!-- Main Score Counter -->
        <div class="mt-6 flex justify-center items-baseline gap-2">
          <span id="finalScoreVal" class="text-5xl sm:text-6xl font-black text-amber-300 font-mono">0.00</span>
          <span class="text-xl sm:text-2xl text-slate-300 font-bold">/ 20 మార్కులు</span>
        </div>
        <div class="text-xs text-slate-300 mt-1">
          ఖచ్చితత్వం (Accuracy): <span id="accuracyVal" class="font-black text-white">0%</span>
        </div>
      </div>

      <!-- Quick Metrics Grid -->
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 p-5 bg-slate-50 border-b border-slate-200 text-center">
        <div class="bg-white p-3.5 rounded-2xl border border-slate-200 shadow-2xs">
          <div class="text-2xs text-slate-400 uppercase font-bold">రాసినవి (Attempted)</div>
          <div id="resAttempted" class="text-xl font-black text-slate-800 mt-0.5">0</div>
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-emerald-200 bg-emerald-50/40 shadow-2xs">
          <div class="text-2xs text-emerald-600 uppercase font-bold">సరైనవి (Correct)</div>
          <div id="resCorrect" class="text-xl font-black text-emerald-600 mt-0.5">0</div>
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-rose-200 bg-rose-50/40 shadow-2xs">
          <div class="text-2xs text-rose-600 uppercase font-bold">తప్పులు (Wrong)</div>
          <div id="resIncorrect" class="text-xl font-black text-rose-600 mt-0.5">0</div>
        </div>
        <div class="bg-white p-3.5 rounded-2xl border border-amber-200 bg-amber-50/40 shadow-2xs">
          <div class="text-2xs text-amber-700 uppercase font-bold">నెగెటివ్ కోత</div>
          <div id="resNegative" class="text-xl font-black text-rose-600 mt-0.5">-0.00</div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="p-4 bg-white border-b border-slate-200 flex flex-wrap justify-between items-center gap-3">
        <h3 class="text-base font-black text-slate-800 flex items-center gap-2">
          <i data-lucide="file-check-2" class="w-5 h-5 text-blue-600"></i>
          <span>20 ప్రశ్నల సమగ్ర సమాధానాలు & వివరణలు</span>
        </h3>
        <div class="flex items-center space-x-2">
          <button onclick="retakeTest()" class="bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs sm:text-sm px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5">
            <i data-lucide="rotate-ccw" class="w-4 h-4"></i>
            <span>రీ-టెస్ట్ తీసుకోండి</span>
          </button>
          <a href="/api/ca_quiz/pdf?date={date}" download class="bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs sm:text-sm px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5">
            <i data-lucide="download" class="w-4 h-4"></i>
            <span>నేటి PDF నోట్స్</span>
          </a>
          <a href="/" class="bg-slate-200 hover:bg-slate-300 text-slate-800 font-bold text-xs sm:text-sm px-3.5 py-1.5 rounded-xl transition flex items-center space-x-1.5">
            <i data-lucide="home" class="w-4 h-4"></i>
            <span>హోమ్</span>
          </a>
        </div>
      </div>

      <!-- Detailed Review List -->
      <div id="reviewContainer" class="p-4 sm:p-6 space-y-4 max-h-[60vh] overflow-y-auto">
        <!-- Rendered dynamically -->
      </div>

    </div>
  </section>

  <!-- Submit Confirmation Modal -->
  <div id="confirmModal" class="hidden fixed inset-0 z-50 bg-slate-950/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border border-slate-200">
      <div class="w-12 h-12 rounded-2xl bg-amber-100 text-amber-600 flex items-center justify-center mb-4">
        <i data-lucide="help-circle" class="w-6 h-6"></i>
      </div>
      <h3 class="text-lg font-black text-slate-900 mb-2">పరీక్షను సమర్పించాలనుకుంటున్నారా?</h3>
      <p class="text-xs text-slate-600 mb-4 leading-relaxed">
        మీరు ఒకసారి సబ్మిట్ చేసిన తర్వాత సమాధానాలను మార్చలేరు. మీ స్కోరు కార్డు మరియు వివరణలు తక్షణమే ప్రదర్శించబడతాయి.
      </p>
      
      <!-- Mini Summary in Modal -->
      <div class="bg-slate-50 p-3.5 rounded-xl border border-slate-200 mb-5 grid grid-cols-3 gap-2 text-center text-xs font-bold">
        <div>
          <span class="text-slate-400 block text-2xs uppercase">సమాధానం ఇచ్చినవి</span>
          <span id="modalAnswered" class="text-emerald-600 text-sm">0</span>
        </div>
        <div>
          <span class="text-slate-400 block text-2xs uppercase">రాయనివి</span>
          <span id="modalRemaining" class="text-rose-600 text-sm">20</span>
        </div>
        <div>
          <span class="text-slate-400 block text-2xs uppercase">రివ్యూ</span>
          <span id="modalReview" class="text-purple-600 text-sm">0</span>
        </div>
      </div>

      <div class="flex justify-end space-x-3">
        <button onclick="closeConfirmModal()" class="px-4 py-2 rounded-xl text-slate-700 bg-slate-100 hover:bg-slate-200 font-bold text-xs transition">
          తిరిగి పరీక్షకు వెళ్ళు
        </button>
        <button onclick="submitTestNow()" class="px-5 py-2 rounded-xl text-white bg-emerald-600 hover:bg-emerald-500 font-black text-xs transition shadow-md">
          అవును, సబ్మిట్ చేయండి
        </button>
      </div>
    </div>
  </div>

  <script>
    // State Variables
    let testData = null;
    let questions = [];
    let currentIndex = 0;
    let answers = {{}};
    let qStatus = {{}}; // 'not_visited', 'not_answered', 'answered', 'review'
    let timerSeconds = 15 * 60;
    let timerInterval = null;
    const testDate = "{date}";

    // Initialize CBT App
    async function initCBT() {{
      lucide.createIcons();
      window.addEventListener('offline', () => document.getElementById('offlineNotice').classList.remove('hidden'));
      window.addEventListener('online', () => document.getElementById('offlineNotice').classList.add('hidden'));

      try {{
        const res = await fetch(`/api/live_test?date=${{testDate}}`);
        const json = await res.json();
        if (json.success && json.questions && json.questions.length > 0) {{
          testData = json;
          questions = json.questions;
          
          // Initialize status for 20 questions
          for (let i = 0; i < questions.length; i++) {{
            qStatus[i] = 'not_visited';
          }}
          qStatus[0] = 'not_answered';

          renderPalette();
          renderQuestion(0);
          startTimer();

          document.getElementById('testLoading').classList.add('hidden');
          document.getElementById('cbtTestContainer').classList.remove('hidden');
          lucide.createIcons();
        }} else {{
          document.getElementById('testLoading').innerHTML = '<p class="text-rose-600 font-bold">ప్రశ్నలు లోడ్ చేయడంలో లోపం తలెత్తింది. దయచేసి పేజీని రీఫ్రెష్ చేయండి.</p>';
        }}
      }} catch (err) {{
        console.error('Fetch error:', err);
        document.getElementById('testLoading').innerHTML = '<p class="text-rose-600 font-bold">కనెక్షన్ లోపం. దయచేసి ఇంటర్నెట్ సరిచూసుకోండి.</p>';
      }}
    }}

    // Render Question Palette
    function renderPalette() {{
      const grid = document.getElementById('paletteGrid');
      grid.innerHTML = '';
      
      let ansCount = 0, notAnsCount = 0, revCount = 0, notVisCount = 0;

      questions.forEach((q, idx) => {{
        const st = qStatus[idx];
        if (st === 'answered') ansCount++;
        else if (st === 'not_answered') notAnsCount++;
        else if (st === 'review') revCount++;
        else notVisCount++;

        const btn = document.createElement('button');
        btn.className = `palette-btn h-9 rounded-lg font-black text-xs flex items-center justify-center cursor-pointer shadow-2xs ${{
          st === 'answered' ? 'palette-answered' :
          st === 'not_answered' ? 'palette-not-answered' :
          st === 'review' ? 'palette-review' : 'palette-not-visited'
        }} ${{idx === currentIndex ? 'palette-current ring-2 ring-blue-600 ring-offset-1' : ''}}`;
        btn.textContent = idx + 1;
        btn.onclick = () => jumpToQuestion(idx);
        grid.appendChild(btn);
      }});

      document.getElementById('countAnswered').textContent = ansCount;
      document.getElementById('countNotAnswered').textContent = notAnsCount;
      document.getElementById('countReview').textContent = revCount;
      document.getElementById('countNotVisited').textContent = notVisCount;
    }}

    // Render Question
    function renderQuestion(idx) {{
      currentIndex = idx;
      const q = questions[idx];

      if (qStatus[idx] === 'not_visited') {{
        qStatus[idx] = 'not_answered';
      }}

      document.getElementById('currentQBadge').textContent = `ప్రశ్న ${{idx + 1}} / ${{questions.length}}`;
      document.getElementById('currentSubjectBadge').textContent = q.subject || 'జనరల్ స్టడీస్';
      document.getElementById('questionText').textContent = `${{idx + 1}}. ${{q.question}}`;

      // Render Options
      const container = document.getElementById('optionsContainer');
      container.innerHTML = '';

      const currentSelected = answers[idx + 1];

      q.options.forEach((optStr) => {{
        const optKey = optStr.trim().charAt(0).toUpperCase();
        const isChecked = (currentSelected === optKey);

        const label = document.createElement('label');
        label.className = `flex items-center p-3.5 sm:p-4 rounded-xl border cursor-pointer transition select-none ${{
          isChecked 
            ? 'bg-blue-50/80 border-blue-600 text-blue-950 font-bold shadow-2xs' 
            : 'bg-white border-slate-200 hover:bg-slate-50 text-slate-800'
        }}`;

        label.innerHTML = `
          <input type="radio" name="cbt_option" value="${{optKey}}" ${{isChecked ? 'checked' : ''}} class="w-4 h-4 text-blue-600 focus:ring-blue-500 mr-3.5">
          <span class="text-xs sm:text-sm leading-relaxed">${{optStr}}</span>
        `;

        label.onclick = () => {{
          selectOption(optKey);
        }};

        container.appendChild(label);
      }});

      // Update Nav buttons
      document.getElementById('prevBtn').disabled = (idx === 0);
      document.getElementById('nextBtn').innerHTML = (idx === questions.length - 1)
        ? '<span>సేవ్ & రివ్యూ</span><i data-lucide="check" class="w-4 h-4"></i>'
        : '<span>సేవ్ & నెక్స్ట్</span><i data-lucide="chevron-right" class="w-4 h-4"></i>';

      renderPalette();
      lucide.createIcons();
    }}

    function selectOption(key) {{
      answers[currentIndex + 1] = key;
      qStatus[currentIndex] = 'answered';
      renderQuestion(currentIndex);
    }}

    function saveAndNext() {{
      if (currentIndex < questions.length - 1) {{
        jumpToQuestion(currentIndex + 1);
      }} else {{
        confirmSubmit();
      }}
    }}

    function navigateQuestion(direction) {{
      const target = currentIndex + direction;
      if (target >= 0 && target < questions.length) {{
        jumpToQuestion(target);
      }}
    }}

    function jumpToQuestion(idx) {{
      renderQuestion(idx);
    }}

    function markForReview() {{
      qStatus[currentIndex] = 'review';
      if (currentIndex < questions.length - 1) {{
        jumpToQuestion(currentIndex + 1);
      }} else {{
        renderPalette();
      }}
    }}

    function clearResponse() {{
      delete answers[currentIndex + 1];
      qStatus[currentIndex] = 'not_answered';
      renderQuestion(currentIndex);
    }}

    // Timer Countdown
    function startTimer() {{
      const display = document.getElementById('timerDisplay');
      const box = document.getElementById('timerContainer');
      const icon = document.getElementById('timerIcon');

      timerInterval = setInterval(() => {{
        timerSeconds--;
        if (timerSeconds <= 0) {{
          clearInterval(timerInterval);
          submitTestNow();
          return;
        }}

        const mins = Math.floor(timerSeconds / 60);
        const secs = timerSeconds % 60;
        display.textContent = `${{mins.toString().padStart(2, '0')}}:${{secs.toString().padStart(2, '0')}}`;

        if (timerSeconds <= 120) {{
          box.classList.add('bg-rose-950', 'border-rose-600', 'animate-pulse');
          display.classList.add('text-rose-400');
          icon.classList.add('text-rose-400');
        }}
      }}, 1000);
    }}

    // Confirm Submit Modal
    function confirmSubmit() {{
      let ans = 0, rev = 0;
      Object.keys(qStatus).forEach(k => {{
        if (qStatus[k] === 'answered') ans++;
        else if (qStatus[k] === 'review') rev++;
      }});

      document.getElementById('modalAnswered').textContent = ans;
      document.getElementById('modalRemaining').textContent = (questions.length - ans);
      document.getElementById('modalReview').textContent = rev;
      document.getElementById('confirmModal').classList.remove('hidden');
      lucide.createIcons();
    }}

    function closeConfirmModal() {{
      document.getElementById('confirmModal').classList.add('hidden');
    }}

    // Submit Test and Evaluate
    async function submitTestNow() {{
      if (timerInterval) clearInterval(timerInterval);
      closeConfirmModal();

      document.getElementById('cbtTestContainer').classList.add('hidden');
      document.getElementById('testLoading').classList.remove('hidden');
      document.getElementById('testLoading').innerHTML = '<div class="w-12 h-12 border-4 border-emerald-600 border-t-transparent rounded-full animate-spin mb-4"></div><p class="text-base font-bold text-slate-800">మీ పరీక్ష సమాధానాలు మూల్యాంకనం చేయబడుతున్నాయి...</p>';

      try {{
        const res = await fetch('/api/live_test/submit', {{
          method: 'POST',
          headers: {{ 'Content-Type': 'application/json' }},
          body: JSON.stringify({{
            date: testDate,
            answers: answers
          }})
        }});
        const result = await res.json();
        if (result.success) {{
          renderResult(result);
        }} else {{
          alert('సబ్మిట్ చేయడంలో లోపం: ' + (result.error || 'Server error'));
        }}
      }} catch (err) {{
        console.error('Submit error:', err);
        alert('నెట్‌వర్క్ లోపం. దయచేసి తిరిగి ప్రయత్నించండి.');
      }}
    }}

    function renderResult(data) {{
      document.getElementById('testLoading').classList.add('hidden');
      document.getElementById('resultContainer').classList.remove('hidden');

      document.getElementById('finalScoreVal').textContent = Number(data.final_score).toFixed(2);
      document.getElementById('accuracyVal').textContent = `${{data.accuracy}}%`;
      document.getElementById('resBadge').textContent = data.badge;
      document.getElementById('resFeedback').textContent = data.feedback;

      document.getElementById('resAttempted').textContent = data.attempted;
      document.getElementById('resCorrect').textContent = data.correct;
      document.getElementById('resIncorrect').textContent = data.incorrect;
      document.getElementById('resNegative').textContent = `-${{data.negative_deduction}}`;

      const reviewContainer = document.getElementById('reviewContainer');
      reviewContainer.innerHTML = '';

      data.review.forEach((item) => {{
        const card = document.createElement('div');
        card.className = `p-4 sm:p-5 rounded-2xl border transition ${{
          item.is_correct 
            ? 'bg-emerald-50/40 border-emerald-200' 
            : item.is_attempted 
              ? 'bg-rose-50/40 border-rose-200' 
              : 'bg-slate-50 border-slate-200'
        }}`;

        let statusHtml = '';
        if (item.is_correct) {{
          statusHtml = '<span class="text-emerald-700 bg-emerald-100 font-bold text-xs px-2.5 py-1 rounded-lg">✓ సరైన సమాధానం (+1.00)</span>';
        }} else if (item.is_attempted) {{
          statusHtml = '<span class="text-rose-700 bg-rose-100 font-bold text-xs px-2.5 py-1 rounded-lg">✗ తప్పు సమాధానం (-0.33)</span>';
        }} else {{
          statusHtml = '<span class="text-slate-600 bg-slate-200 font-bold text-xs px-2.5 py-1 rounded-lg">⚪ సమాధానం ఇవ్వలేదు (0.00)</span>';
        }}

        card.innerHTML = `
          <div class="flex flex-wrap justify-between items-center gap-2 mb-2">
            <span class="text-xs font-black text-slate-500">ప్రశ్న ${{item.q_no}} • ${{item.subject}}</span>
            ${{statusHtml}}
          </div>
          <h4 class="text-sm sm:text-base font-bold text-slate-900 mb-3">${{item.q_no}}. ${{item.question}}</h4>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs mb-3">
            ${{item.options.map(opt => {{
              const k = opt.trim().charAt(0);
              const isUser = (item.user_choice === k);
              const isAns = (item.correct_option === k);
              return `
                <div class="p-2.5 rounded-xl border flex items-center justify-between ${{
                  isAns ? 'bg-emerald-100/70 border-emerald-400 font-bold text-emerald-950' :
                  isUser ? 'bg-rose-100/70 border-rose-400 font-bold text-rose-950' : 'bg-white border-slate-200 text-slate-700'
                }}">
                  <span>${{opt}}</span>
                  ${{isAns ? '<span class="text-emerald-700 font-black text-2xs uppercase">✓ కీ జవాబు</span>' : ''}}
                  ${{isUser && !isAns ? '<span class="text-rose-700 font-black text-2xs uppercase">✗ మీ ఎంపిక</span>' : ''}}
                </div>
              `;
            }}).join('')}}
          </div>

          <div class="bg-blue-50/70 border border-blue-200 p-3 rounded-xl text-xs text-slate-700 leading-relaxed">
            <b class="text-blue-950">💡 సమగ్ర వివరణ (Explanation):</b> ${{item.explanation}}
          </div>
        `;

        reviewContainer.appendChild(card);
      }});

      lucide.createIcons();
    }}

    function retakeTest() {{
      window.location.reload();
    }}

    // Auto load on ready
    window.addEventListener('DOMContentLoaded', initCBT);
  </script>
</body>
</html>"""
