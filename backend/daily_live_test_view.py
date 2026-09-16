# -*- coding: utf-8 -*-
"""
Interactive CBT Examination Hall & Leaderboard Web View (/daily_live_test).
Features 15-min countdown timer, -0.33 negative marking, instant scorecard & state ranking.
"""

import json
from daily_live_test_data import get_live_test_questions
from leaderboard_db import get_top_leaderboard_entries

def render_daily_live_test_html():
    questions = get_live_test_questions()
    qs_json = json.dumps(questions, ensure_ascii=False)
    leaderboard = get_top_leaderboard_entries(20)

    board_rows = ""
    for idx, e in enumerate(leaderboard, 1):
        medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else f"#{idx}"))
        bg_cls = "bg-amber-50/60 font-bold" if idx <= 3 else "hover:bg-slate-50"
        board_rows += f"""
        <tr class="border-b border-slate-100 {bg_cls} text-xs sm:text-sm">
          <td class="p-3 text-center">{medal}</td>
          <td class="p-3 font-black text-slate-900">{e['name']}</td>
          <td class="p-3 text-slate-600">{e['district']}</td>
          <td class="p-3 text-slate-500">{e.get('target_exam', 'APPSC/TSPSC')}</td>
          <td class="p-3 text-center text-emerald-700 font-extrabold">{e['net_score']} / 20</td>
          <td class="p-3 text-center text-slate-700">{e['accuracy']}%</td>
          <td class="p-3 text-center text-slate-500">{e['time_spent']}</td>
        </tr>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>లైవ్ డైలీ మాక్ టెస్ట్ & స్టేట్ లీడర్‌బోర్డ్ - లక్ష్య పోటీ పరీక్షలు</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800;900&family=Mandali&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
  <style>
    body {{ font-family: 'Plus Jakarta Sans', 'Mandali', sans-serif; }}
    @media print {{
      .no-print {{ display: none !important; }}
    }}
  </style>
</head>
<body class="bg-slate-100 text-slate-900 min-h-screen pb-16 flex flex-col">

  <!-- Header -->
  <header class="bg-slate-900 text-white sticky top-0 z-30 shadow-md no-print border-b border-slate-800">
    <div class="max-w-7xl mx-auto px-4 py-3 flex flex-wrap justify-between items-center gap-3">
      <div class="flex items-center gap-3">
        <a href="/" class="text-xs bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg border border-slate-700 transition flex items-center gap-1.5 font-bold">
          <i class="fa-solid fa-arrow-left"></i> హోమ్‌పేజీ
        </a>
        <h1 class="text-sm sm:text-base font-black flex items-center gap-2">
          <span>🏆</span> <span>లైవ్ డైలీ మాక్ టెస్ట్ (20 MCQs - 15 నిమిషాలు)</span>
        </h1>
      </div>

      <!-- Exam Timer Display -->
      <div id="examTimerBox" class="flex items-center gap-3">
        <div class="flex items-center gap-2 bg-slate-800 border border-slate-700 px-3.5 py-1.5 rounded-xl">
          <i class="fa-solid fa-stopwatch text-amber-400 text-sm animate-pulse"></i>
          <span class="text-xs text-slate-400 font-bold">మిగిలిన సమయం:</span>
          <span id="timerText" class="text-sm sm:text-base font-black text-amber-300 font-mono">15:00</span>
        </div>
        <button onclick="submitExamEarly()" id="topSubmitBtn" class="text-xs bg-rose-600 hover:bg-rose-500 text-white font-black px-4 py-1.5 rounded-xl transition shadow-md flex items-center gap-1.5">
          <i class="fa-solid fa-flag-checkered"></i> పరీక్ష ముగించు
        </button>
      </div>
    </div>
  </header>

  <main class="max-w-7xl mx-auto px-4 py-6 flex-1 w-full space-y-6">

    <!-- Candidate Registration Bar (If not submitted yet) -->
    <div id="candidateBar" class="bg-white border border-slate-200 rounded-2xl p-4 shadow-sm flex flex-wrap items-center justify-between gap-3 no-print">
      <div class="flex flex-wrap items-center gap-3 flex-1">
        <div class="flex items-center gap-2">
          <span class="text-xs font-black text-slate-700">మీ పేరు:</span>
          <input type="text" id="candidateName" value="పోటీ పరీక్షార్థి" class="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1 text-xs font-bold text-slate-800 w-36 sm:w-48 outline-none focus:ring-1 focus:ring-blue-500" />
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-black text-slate-700">మీ జిల్లా:</span>
          <input type="text" id="candidateDistrict" value="విశాఖపట్నం" class="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1 text-xs font-bold text-slate-800 w-32 outline-none focus:ring-1 focus:ring-blue-500" />
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs font-black text-slate-700">లక్ష్య పరీక్ష:</span>
          <select id="candidateExam" class="bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1 text-xs font-bold text-slate-800 outline-none">
            <option value="APPSC Group 2">APPSC Group 2</option>
            <option value="APPSC Group 1">APPSC Group 1</option>
            <option value="TSPSC Group 1">TSPSC Group 1</option>
            <option value="TSPSC Group 2">TSPSC Group 2</option>
            <option value="పోలీస్ SI / PC">పోలీస్ SI / PC</option>
          </select>
        </div>
      </div>
      <div class="flex items-center gap-2 text-xs text-rose-700 bg-rose-50 border border-rose-200 px-3 py-1 rounded-xl font-bold">
        <span>⚠️ నెగెటివ్ మార్కింగ్: సరైన ప్రశ్నకు +1.0 | తప్పు ప్రశ్నకు -0.33</span>
      </div>
    </div>

    <!-- Live Test CBT Layout (2 columns: Question area + Palette) -->
    <div id="testArea" class="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
      
      <!-- Left 3 Cols: Active Question Display -->
      <div class="lg:col-span-3 bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm space-y-6">
        <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 pb-3">
          <div class="flex items-center gap-2">
            <span class="px-3 py-1 bg-blue-600 text-white text-xs font-black rounded-lg" id="qNumberBadge">ప్రశ్న 1 / 20</span>
            <span class="px-2.5 py-0.5 bg-slate-100 text-slate-700 text-xs font-bold rounded-lg" id="qSubjectBadge">జనరల్ స్టడీస్</span>
          </div>
          <button type="button" onclick="toggleReviewFlag()" id="flagBtn" class="text-xs bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 font-bold px-3 py-1 rounded-lg transition flex items-center gap-1.5">
            <i class="fa-regular fa-bookmark"></i>
            <span id="flagBtnText">రివ్యూ కోసం మార్క్ చేయి</span>
          </button>
        </div>

        <h3 class="text-base sm:text-lg font-black text-slate-900 leading-relaxed min-h-[60px]" id="questionText">
          ప్రశ్న లోడ్ అవుతోంది...
        </h3>

        <!-- Options Container -->
        <div class="space-y-3" id="optionsContainer">
          <!-- Options rendered via JS -->
        </div>

        <!-- Navigation Action Buttons -->
        <div class="flex flex-wrap justify-between items-center gap-3 pt-6 border-t border-slate-100">
          <div class="flex items-center gap-2">
            <button type="button" onclick="prevQuestion()" id="prevBtn" class="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 text-xs font-black rounded-xl transition flex items-center gap-1.5 border border-slate-300">
              <i class="fa-solid fa-chevron-left"></i> మునుపటి
            </button>
            <button type="button" onclick="clearOption()" class="px-3 py-2 bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-bold rounded-xl transition border border-rose-200">
              ఎంపిక తొలగించు
            </button>
          </div>
          <button type="button" onclick="nextQuestion()" id="nextBtn" class="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white text-xs font-black rounded-xl transition flex items-center gap-1.5 shadow-sm">
            తర్వాతి ప్రశ్న <i class="fa-solid fa-chevron-right"></i>
          </button>
        </div>
      </div>

      <!-- Right 1 Col: Question Palette -->
      <div class="bg-white border border-slate-200 rounded-3xl p-5 shadow-sm space-y-4">
        <h4 class="font-black text-xs uppercase tracking-wider text-slate-700 flex justify-between items-center">
          <span>ప్రశ్నల ప్యాలెట్ (Palette)</span>
          <span class="text-blue-600 font-bold" id="attemptedCounter">0 / 20</span>
        </h4>

        <!-- Legend -->
        <div class="grid grid-cols-2 gap-2 text-[10px] font-bold text-slate-600 pb-2 border-b border-slate-100">
          <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-emerald-500"></span> సమాధానమిచ్చినవి</div>
          <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-slate-200"></span> ఇవ్వనివి</div>
          <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded bg-purple-500"></span> రివ్యూ మార్క్డ్</div>
          <div class="flex items-center gap-1.5"><span class="w-3 h-3 rounded border-2 border-blue-600 bg-blue-50"></span> ప్రస్తుత ప్రశ్న</div>
        </div>

        <!-- Palette Grid 1-20 -->
        <div class="grid grid-cols-5 gap-2" id="paletteGrid">
          <!-- Populated by JS -->
        </div>

        <div class="pt-4 border-t border-slate-100">
          <button type="button" onclick="submitExamEarly()" class="w-full py-3 bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white text-xs font-black rounded-xl transition shadow-md flex items-center justify-center gap-2">
            <i class="fa-solid fa-check-circle"></i>
            <span>పరీక్షను సబ్మిట్ చేయండి</span>
          </button>
        </div>
      </div>

    </div>

    <!-- Result / Scorecard Modal (Hidden initially) -->
    <div id="resultModal" class="hidden bg-white border-2 border-emerald-500/40 rounded-3xl p-6 sm:p-8 shadow-xl space-y-6 animate-fadeIn">
      <div id="scorecardContent">
        <!-- Rendered via JS after evaluation -->
      </div>
    </div>

    <!-- State Leaderboard Section -->
    <section class="bg-white border border-slate-200 rounded-3xl p-6 sm:p-8 shadow-sm space-y-4">
      <div class="flex flex-wrap justify-between items-center gap-3 border-b border-slate-100 pb-4">
        <div>
          <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
            <span>🏅</span> <span>నేటి రాష్ట్ర స్థాయి ర్యాంకింగ్ లీడర్‌బోర్డ్ (State-Wide Leaderboard)</span>
          </h3>
          <p class="text-xs text-slate-500 mt-0.5">నెగెటివ్ మార్కింగ్ తర్వాత వచ్చిన నెట్ స్కోర్ ఆధారంగా ర్యాంకింగ్</p>
        </div>
        <span class="text-xs bg-indigo-50 text-indigo-700 border border-indigo-200 px-3 py-1 rounded-xl font-black">
          లైవ్ అభ్యర్థుల డేటా
        </span>
      </div>

      <div class="overflow-x-auto">
        <table class="w-full text-left border-collapse">
          <thead>
            <tr class="bg-slate-50 text-slate-700 text-xs uppercase tracking-wider border-b border-slate-200">
              <th class="p-3 text-center">ర్యాంక్</th>
              <th class="p-3">అభ్యర్థి పేరు</th>
              <th class="p-3">జిల్లా</th>
              <th class="p-3">లక్ష్య పరీక్ష</th>
              <th class="p-3 text-center">నెట్ స్కోరు (-0.33)</th>
              <th class="p-3 text-center">ఖచ్చితత్వం (Accuracy)</th>
              <th class="p-3 text-center">సమయం</th>
            </tr>
          </thead>
          <tbody id="leaderboardBody">
            {board_rows}
          </tbody>
        </table>
      </div>
    </section>

  </main>

  <script>
    const questions = {qs_json};
    let currentIdx = 0;
    const userAnswers = {{}};
    const reviewFlags = {{}};
    let totalSeconds = 900; // 15 minutes
    let timerInterval = null;
    let examSubmitted = false;

    // Timer logic
    function startTimer() {{
      timerInterval = setInterval(() => {{
        if (totalSeconds <= 0) {{
          clearInterval(timerInterval);
          submitExamEarly(true);
          return;
        }}
        totalSeconds--;
        const mins = Math.floor(totalSeconds / 60);
        const secs = totalSeconds % 60;
        document.getElementById("timerText").textContent = 
          (mins < 10 ? "0" : "") + mins + ":" + (secs < 10 ? "0" : "") + secs;
      }}, 1000);
    }}

    function renderQuestion(idx) {{
      currentIdx = idx;
      const q = questions[idx];
      document.getElementById("qNumberBadge").textContent = `ప్రశ్న ${{idx + 1}} / ${{questions.length}}`;
      document.getElementById("qSubjectBadge").textContent = q.subject || "జనరల్ స్టడీస్";
      document.getElementById("questionText").textContent = q.question;

      // Update flag button
      const isFlagged = reviewFlags[q.id];
      const flagBtn = document.getElementById("flagBtn");
      if (isFlagged) {{
        flagBtn.className = "text-xs bg-purple-600 text-white font-bold px-3 py-1 rounded-lg transition flex items-center gap-1.5";
        document.getElementById("flagBtnText").textContent = "రివ్యూ మార్క్ చేయబడింది";
      }} else {{
        flagBtn.className = "text-xs bg-purple-50 hover:bg-purple-100 text-purple-700 border border-purple-200 font-bold px-3 py-1 rounded-lg transition flex items-center gap-1.5";
        document.getElementById("flagBtnText").textContent = "రివ్యూ కోసం మార్క్ చేయి";
      }}

      // Options
      const optLetters = ["A", "B", "C", "D"];
      let optsHtml = "";
      const chosen = userAnswers[q.id];

      q.options.forEach((optText, oIdx) => {{
        const letter = optLetters[oIdx];
        const isSelected = (chosen === letter);
        const borderCls = isSelected ? "border-blue-600 bg-blue-50/70 shadow-sm" : "border-slate-200 bg-slate-50 hover:bg-slate-100";
        const badgeCls = isSelected ? "bg-blue-600 text-white" : "bg-slate-200 text-slate-800";

        optsHtml += `
        <div onclick="selectOption('${{letter}}')" class="p-4 rounded-2xl border-2 ${{borderCls}} cursor-pointer transition flex items-start gap-3">
          <span class="w-7 h-7 rounded-full ${{badgeCls}} font-black text-xs flex items-center justify-center shrink-0">${{letter}}</span>
          <span class="text-xs sm:text-sm font-bold text-slate-800 leading-relaxed">${{optText}}</span>
        </div>
        `;
      }});

      document.getElementById("optionsContainer").innerHTML = optsHtml;
      document.getElementById("prevBtn").disabled = (idx === 0);
      document.getElementById("nextBtn").innerHTML = (idx === questions.length - 1) ? 
        'పూర్తయింది <i class="fa-solid fa-check"></i>' : 'తర్వాతి ప్రశ్న <i class="fa-solid fa-chevron-right"></i>';

      updatePalette();
    }}

    function selectOption(letter) {{
      const q = questions[currentIdx];
      userAnswers[q.id] = letter;
      renderQuestion(currentIdx);
    }}

    function clearOption() {{
      const q = questions[currentIdx];
      delete userAnswers[q.id];
      renderQuestion(currentIdx);
    }}

    function toggleReviewFlag() {{
      const q = questions[currentIdx];
      if (reviewFlags[q.id]) {{
        delete reviewFlags[q.id];
      }} else {{
        reviewFlags[q.id] = true;
      }}
      renderQuestion(currentIdx);
    }}

    function nextQuestion() {{
      if (currentIdx < questions.length - 1) {{
        renderQuestion(currentIdx + 1);
      }}
    }}

    function prevQuestion() {{
      if (currentIdx > 0) {{
        renderQuestion(currentIdx - 1);
      }}
    }}

    function updatePalette() {{
      let html = "";
      let answeredCount = 0;

      questions.forEach((q, idx) => {{
        const isAnswered = !!userAnswers[q.id];
        const isFlagged = !!reviewFlags[q.id];
        const isCurrent = (idx === currentIdx);

        if (isAnswered) answeredCount++;

        let bg = "bg-slate-100 text-slate-700";
        if (isFlagged) bg = "bg-purple-600 text-white";
        else if (isAnswered) bg = "bg-emerald-500 text-white";

        let currentRing = isCurrent ? "ring-2 ring-blue-600 font-black scale-105" : "";

        html += `
        <button type="button" onclick="renderQuestion(${{idx}})" class="h-9 rounded-xl text-xs font-bold transition flex items-center justify-center ${{bg}} ${{currentRing}}">
          ${{idx + 1}}
        </button>
        `;
      }});

      document.getElementById("paletteGrid").innerHTML = html;
      document.getElementById("attemptedCounter").textContent = `${{answeredCount}} / ${{questions.length}}`;
    }}

    async function submitExamEarly(isTimeout = false) {{
      if (examSubmitted) return;
      if (!isTimeout) {{
        const answered = Object.keys(userAnswers).length;
        if (!confirm(`మీరు మొత్తం 20 ప్రశ్నలలో ${{answered}} ప్రశ్నలకు సమాధానమిచ్చారు. పరీక్షను సబ్మిట్ చేయమంటారా?`)) {{
          return;
        }}
      }}

      examSubmitted = true;
      clearInterval(timerInterval);

      const name = document.getElementById("candidateName").value || "పోటీ పరీక్షార్థి";
      const district = document.getElementById("candidateDistrict").value || "విశాఖపట్నం";
      const exam = document.getElementById("candidateExam").value || "APPSC Group 2";
      const spentMins = 14 - Math.floor(totalSeconds / 60);
      const spentSecs = 60 - (totalSeconds % 60);
      const timeSpentStr = `${{spentMins}}:${{spentSecs < 10 ? "0" : ""}}${{spentSecs}}`;

      try {{
        const res = await fetch("/api/live_test/submit", {{
          method: "POST",
          headers: {{ "Content-Type": "application/json" }},
          body: JSON.stringify({{
            name: name,
            district: district,
            target_exam: exam,
            answers: userAnswers,
            time_spent: timeSpentStr
          }})
        }});
        const data = await res.json();
        if (data.success) {{
          showScorecard(data.scorecard, data.review);
        }} else {{
          alert("స్కోర్ లెక్కింపులో లోపం ఏర్పడింది.");
        }}
      }} catch (e) {{
        alert("సర్వర్ ఎర్రర్ ఏర్పడింది.");
      }}
    }}

    function showScorecard(card, review) {{
      document.getElementById("testArea").classList.add("hidden");
      document.getElementById("candidateBar").classList.add("hidden");
      document.getElementById("examTimerBox").classList.add("hidden");

      const modal = document.getElementById("resultModal");
      modal.classList.remove("hidden");

      let reviewHtml = "";
      review.forEach((r, idx) => {{
        const optLetters = ["A", "B", "C", "D"];
        let opts = "";
        r.options.forEach((text, oIdx) => {{
          const l = optLetters[oIdx];
          let border = "border-slate-200 bg-slate-50";
          if (l === r.correct_key) border = "border-emerald-500 bg-emerald-50 text-emerald-900 font-bold";
          else if (l === r.chosen && r.status === "wrong") border = "border-rose-500 bg-rose-50 text-rose-900";
          opts += `<div class="p-2.5 rounded-xl border ${{border}} text-xs flex gap-2"><strong>${{l}}:</strong> <span>${{text}}</span></div>`;
        }});

        const statusBadge = r.status === "correct" ? 
          '<span class="px-2 py-0.5 bg-emerald-100 text-emerald-800 text-xs font-black rounded">✅ సరియైనది (+1.0)</span>' :
          (r.status === "wrong" ? '<span class="px-2 py-0.5 bg-rose-100 text-rose-800 text-xs font-black rounded">❌ తప్పు (-0.33)</span>' :
          '<span class="px-2 py-0.5 bg-slate-100 text-slate-700 text-xs font-bold rounded">⚪ వదిలేసినవి (0.0)</span>');

        reviewHtml += `
        <div class="p-5 bg-white border border-slate-200 rounded-2xl space-y-3">
          <div class="flex justify-between items-center text-xs">
            <span class="font-black text-slate-800">ప్రశ్న ${{idx + 1}}</span>
            ${{statusBadge}}
          </div>
          <p class="text-xs sm:text-sm font-bold text-slate-900">${{r.question}}</p>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">${{opts}}</div>
          <div class="p-3 bg-slate-50 rounded-xl text-xs text-slate-700 border border-slate-200">
            <strong class="text-emerald-900 block mb-1">వివరణ:</strong> ${{r.explanation}}
          </div>
        </div>
        `;
      }});

      modal.innerHTML = `
        <div class="space-y-6">
          <div class="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white p-6 rounded-3xl text-center space-y-3">
            <span class="px-3 py-1 bg-amber-400 text-slate-950 text-xs font-black rounded-full uppercase">
              లైవ్ టెస్ట్ స్కోర్‌కార్డ్
            </span>
            <h2 class="text-2xl sm:text-4xl font-black text-amber-300">${{card.net_score}} / 20</h2>
            <p class="text-xs sm:text-sm text-slate-300">
              అభినందనలు ${{card.name}}! మీ రాష్ట్ర స్థాయి ర్యాంక్: <strong>#${{card.rank}}</strong> (పర్సంటైల్: <strong>${{card.percentile}}%</strong>)
            </p>
          </div>

          <!-- Stats 4-Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div class="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-center">
              <span class="text-xs text-emerald-800 font-bold block">సరైనవి (+1.0)</span>
              <strong class="text-xl font-black text-emerald-700">${{card.correct}}</strong>
            </div>
            <div class="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-center">
              <span class="text-xs text-rose-800 font-bold block">తప్పులు (-0.33)</span>
              <strong class="text-xl font-black text-rose-700">${{card.wrong}}</strong>
            </div>
            <div class="p-4 bg-slate-50 border border-slate-200 rounded-2xl text-center">
              <span class="text-xs text-slate-600 font-bold block">ఖచ్చితత్వం (Accuracy)</span>
              <strong class="text-xl font-black text-slate-800">${{card.accuracy}}%</strong>
            </div>
            <div class="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl text-center">
              <span class="text-xs text-indigo-800 font-bold block">సమయం</span>
              <strong class="text-xl font-black text-indigo-700">${{card.time_spent}}</strong>
            </div>
          </div>

          <!-- Detailed Question-by-Question Review -->
          <div class="space-y-4 pt-4 border-t border-slate-200">
            <h3 class="text-base font-black text-slate-900">📝 సమగ్ర ప్రశ్నల సమీక్ష & అధికారిక వివరణలు:</h3>
            <div class="space-y-4">${{reviewHtml}}</div>
          </div>
        </div>
      `;

      modal.scrollIntoView({{ behavior: "smooth" }});
    }}

    // Init
    renderQuestion(0);
    startTimer();
  </script>
</body>
</html>
"""
    return html
