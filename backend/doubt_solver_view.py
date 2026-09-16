# -*- coding: utf-8 -*-
"""
Interactive Web View for Telugu AI Exam Doubt Solver (/doubt_solver).
"""

from doubt_solver import get_suggested_doubts

def render_doubt_solver_html():
    suggestions = get_suggested_doubts()
    suggest_pills = ""
    for s in suggestions:
        suggest_pills += f"""
        <button type="button" onclick="askPreset('{s['query']}')" class="px-3 py-1.5 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-bold rounded-xl border border-slate-300 transition text-left">
          💡 {s['title']}
        </button>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>తెలుగు AI ఎగ్జామ్ డౌట్ సాల్వర్ - లక్ష్య పోటీ పరీక్షలు</title>
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
<body class="bg-slate-100 text-slate-900 min-h-screen pb-16 flex flex-col">

  <!-- Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-30 shadow-md no-print border-b border-slate-800">
    <div class="max-w-5xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> హోమ్‌పేజీ
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🤖</span> <span>తెలుగు AI ఎగ్జామ్ డౌట్ సాల్వర్ (Study Buddy)</span>
        </h1>
      </div>
      <div class="flex items-center gap-2">
        <span class="text-xs bg-emerald-950 text-emerald-300 border border-emerald-800/80 px-2.5 py-1 rounded-lg font-black flex items-center gap-1.5">
          <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> లైవ్ ఆన్‌లైన్
        </span>
      </div>
    </div>
  </header>

  <main class="max-w-5xl mx-auto px-4 py-6 flex-1 w-full space-y-6">

    <!-- Hero Card -->
    <div class="bg-gradient-to-r from-indigo-950 via-slate-900 to-purple-950 text-white p-6 sm:p-7 rounded-3xl shadow-xl space-y-3 border border-indigo-900/60">
      <div class="flex items-center gap-2">
        <span class="px-2.5 py-0.5 rounded-full text-[10px] font-black uppercase tracking-wider bg-indigo-500 text-white">
          APPSC & TSPSC AI ASSISTANT
        </span>
        <span class="text-xs text-indigo-300 font-semibold">సిలబస్, రాజ్యాంగం, చరిత్ర & పథకాలపై తక్షణ సందేహ నివృత్తి</span>
      </div>
      <h2 class="text-xl sm:text-2xl font-black text-white">మీ పోటీ పరీక్షల సందేహాన్ని తెలుగులో అడగండి!</h2>
      <p class="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
        రాజ్యాంగ అధికరణలు, చారిత్రక ఆధారాలు, ఆర్థిక గణాంకాలు మరియు గత పరీక్షల ప్రశ్నలతో (PYQs) కూడిన సమగ్ర వివరణ తక్షణమే పొందండి.
      </p>
    </div>

    <!-- Suggested Doubts Bar -->
    <div class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm space-y-2 no-print">
      <h3 class="text-xs font-black text-slate-700 uppercase tracking-wider flex items-center gap-1.5">
        <span>⚡</span> <span>తరచుగా అడిగే పరీక్షా ప్రశ్నలు (Quick Questions):</span>
      </h3>
      <div class="flex flex-wrap gap-2">
        {suggest_pills}
      </div>
    </div>

    <!-- Question Input Form -->
    <div class="bg-white border-2 border-indigo-500/40 rounded-2xl p-4 sm:p-5 shadow-md no-print space-y-3">
      <div class="flex flex-col sm:flex-row gap-3">
        <input 
          type="text" 
          id="doubtInput" 
          placeholder="మీ సందేహాన్ని ఇక్కడ టైప్ చేయండి (ఉదా: ఆర్టికల్ 32 విశేషాలు, శాతవాహనుల నాణేలు, పోలవరం నిధులు)..."
          class="flex-1 bg-slate-50 border border-slate-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 font-medium text-slate-900"
          onkeydown="if(event.key === 'Enter') submitDoubt()"
        />
        <button 
          type="button" 
          id="askBtn" 
          onclick="submitDoubt()" 
          class="px-6 py-3 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-black text-sm rounded-xl transition shadow-md flex items-center justify-center gap-2 shrink-0">
          <i class="fa-solid fa-paper-plane"></i>
          <span>సందేహం అడగండి</span>
        </button>
      </div>
      <div class="text-[11px] text-slate-500 font-medium">
        💡 చిట్కా: ప్రశ్నను స్పష్టంగా అడగండి. ఉదా: "ఆర్టికల్ 356 రాష్ట్రపతి పాలన", "సూపర్ సిక్స్ పథకాలు", "శాతవాహనుల చరిత్ర".
      </div>
    </div>

    <!-- Result / Answer Container -->
    <div id="answerContainer" class="space-y-4">
      <!-- Default Welcome Card -->
      <div class="bg-white border border-slate-200 rounded-2xl p-6 text-center space-y-2 text-slate-600" id="emptyState">
        <div class="w-12 h-12 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center text-xl mx-auto font-black">
          🤖
        </div>
        <h4 class="font-black text-slate-900 text-base">మీ సందేహం కోసం వేచి చూస్తున్నాం!</h4>
        <p class="text-xs text-slate-500 max-w-md mx-auto">
          పైనున్న ఇన్పుట్ బాక్స్‌లో మీ ప్రశ్నను టైప్ చేయండి లేదా పైనున్న క్విక్ బటన్‌లలో దేనినైనా క్లిక్ చేయండి.
        </p>
      </div>

      <div id="activeAnswer" class="hidden"></div>
    </div>

  </main>

  <script>
    async function submitDoubt() {{
      const input = document.getElementById("doubtInput");
      const query = input.value.trim();
      if (!query) return;

      const askBtn = document.getElementById("askBtn");
      askBtn.disabled = true;
      askBtn.innerHTML = '<span class="inline-block animate-spin mr-1">⏳</span> వెతుకుతోంది...';

      try {{
        const res = await fetch("/api/doubt_solver/ask", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{ query: query }})
        }});
        const data = await res.json();
        if (data.success && data.answer) {{
          renderAnswer(data.answer);
        }} else {{
          alert("సమాధానం పొందడంలో లోపం ఏర్పడింది.");
        }}
      }} catch (e) {{
        alert("సర్వర్ ఎర్రర్ ఏర్పడింది.");
      }} finally {{
        askBtn.disabled = false;
        askBtn.innerHTML = '<i class="fa-solid fa-paper-plane"></i> <span>సందేహం అడగండి</span>';
      }}
    }}

    function askPreset(presetQuery) {{
      document.getElementById("doubtInput").value = presetQuery;
      submitDoubt();
    }}

    function renderAnswer(ans) {{
      document.getElementById("emptyState").classList.add("hidden");
      const container = document.getElementById("activeAnswer");
      container.classList.remove("hidden");

      let pointersHtml = "";
      if (ans.exam_pointers) {{
        pointersHtml = ans.exam_pointers.map(p => '<li class="flex items-start gap-2"><span class="text-indigo-600 font-bold">✦</span><span>' + p + '</span></li>').join("");
      }}

      let pyqHtml = "";
      if (ans.pyq) {{
        let opts = ans.pyq.options ? ans.pyq.options.map(o => '<span class="px-2 py-1 bg-slate-100 rounded text-xs text-slate-800">' + o + '</span>').join(" ") : "";
        pyqHtml = `
        <div class="mt-4 p-4 bg-amber-50/90 border border-amber-300 rounded-2xl space-y-2">
          <div class="flex justify-between items-center text-xs font-black text-amber-900">
            <span>📝 సంబంధిత గత పరీక్షా ప్రశ్న (Related PYQ)</span>
          </div>
          <p class="text-xs sm:text-sm font-bold text-slate-900">${{ans.pyq.q}}</p>
          <div class="flex flex-wrap gap-2 pt-1">${{opts}}</div>
          <div class="text-xs font-black text-emerald-800 bg-emerald-100 p-2 rounded-lg mt-1 border border-emerald-200">
            ✅ సరైన సమాధానం & పరీక్ష రిఫరెన్స్: ${{ans.pyq.ans}}
          </div>
        </div>
        `;
      }}

      container.innerHTML = `
        <article class="bg-white border-2 border-indigo-200 rounded-3xl p-6 sm:p-8 shadow-md space-y-5 animate-fadeIn">
          <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-3">
            <span class="px-3 py-1 bg-indigo-100 text-indigo-900 text-xs font-black rounded-lg">📂 ${{ans.subject}}</span>
            <span class="text-xs text-slate-400 font-semibold">AI Verified Exam Note</span>
          </div>

          <h3 class="text-lg sm:text-2xl font-black text-slate-900">${{ans.title}}</h3>

          <!-- Definition -->
          <div class="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-1">
            <strong class="text-xs uppercase tracking-wider text-slate-500 font-extrabold block">🎯 త్వరిత నిర్వచనం & సారాంశం:</strong>
            <p class="text-xs sm:text-sm text-slate-800 leading-relaxed font-medium">${{ans.definition}}</p>
          </div>

          <!-- Context -->
          <div class="space-y-1.5">
            <h4 class="text-xs uppercase tracking-wider text-indigo-900 font-black">📜 సిలబస్ & రాజ్యాంగ / చారిత్రక నేపథ్యం:</h4>
            <p class="text-xs sm:text-sm text-slate-700 leading-relaxed">${{ans.context}}</p>
          </div>

          <!-- Exam Pointers -->
          <div class="p-5 bg-gradient-to-br from-indigo-50/80 to-purple-50/50 border border-indigo-200 rounded-2xl space-y-2.5">
            <h4 class="text-xs font-black text-indigo-950 uppercase tracking-wider">💡 పరీక్షల్లో గుర్తుంచుకోవాల్సిన హై-యీల్డ్ పాయింట్లు:</h4>
            <ul class="space-y-2 text-xs sm:text-sm text-slate-800">
              ${{pointersHtml}}
            </ul>
          </div>

          ${{pyqHtml}}

          <!-- Ranker's Tip -->
          <div class="p-3.5 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-medium flex items-start gap-2">
            <span class="font-black text-sm">🌟</span>
            <div><strong class="font-black">ర్యాంకర్స్ రివిజన్ టిప్:</strong> ${{ans.tip}}</div>
          </div>
        </article>
      `;

      container.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}
  </script>
</body>
</html>
"""
    return html
