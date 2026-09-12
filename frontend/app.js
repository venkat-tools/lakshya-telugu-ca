// Telugu Daily Current Affairs Application Script

const API_BASE = ""; // Relative path to API

// Application State
const state = {
  currentDate: null,
  currentCategory: "all",
  currentTab: "articles",
  currentOneLinerCategory: "all",
  searchQuery: "",
  quizData: [],
  quizAnswers: {},
  articles: [],
  oneLiners: [],
  targetExam: localStorage.getItem("target_exam") || "all",
  flashcards: [],
  filteredFlashcards: [],
  currentFcIndex: 0,
  isFcFlipped: false,
  fcCategory: "all",
  fcMastered: JSON.parse(localStorage.getItem("fc_mastered") || "[]"),
  fcReview: JSON.parse(localStorage.getItem("fc_review") || "[]")
};

// Category Mapping
const CATEGORY_MAP = {
  national: { label: "🏛️ జాతీయం", class: "badge-national" },
  regional: { label: "🌾 AP & తెలంగాణ", class: "badge-regional" },
  economy: { label: "📈 ఆర్థికం & బ్యాంకింగ్", class: "badge-economy" },
  science_tech: { label: "🚀 సైన్స్ & టెక్నాలజీ", class: "badge-science_tech" },
  sports_awards: { label: "🏆 క్రీడలు & అవార్డులు", class: "badge-sports_awards" },
  appointments: { label: "👤 నియామకాలు", class: "badge-appointments" }
};

// DOM Elements
const dateSelect = document.getElementById("dateSelect");
const searchInput = document.getElementById("searchInput");
const syncBtn = document.getElementById("syncBtn");
const printBtn = document.getElementById("printBtn");
const resetQuizBtn = document.getElementById("resetQuizBtn");
const articlesContainer = document.getElementById("articlesContainer");
const quizContainer = document.getElementById("quizContainer");
const onelinersContainer = document.getElementById("onelinersContainer");
const tickerText = document.getElementById("tickerText");
const toast = document.getElementById("toast");
const toastMsg = document.getElementById("toastMsg");

// Tab Elements
const navTabs = document.querySelectorAll(".nav-tab");
const tabContents = document.querySelectorAll(".tab-content");
const catPills = document.querySelectorAll(".cat-pill");

// Init App
document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  updateClock();
  setInterval(updateClock, 1000);
  initDarkMode();
  initVoiceAudio();
  initBookmarks();
  initAnalyticsAndStreak();
  initBookletsModal();
  initArticleDetailModal();
  initWebNotifications();
  initTargetExam();
  initFlashcards();
  initStudyCalendarModal();
  initPwaInstall();
  initPodcastPlayer();
  initCbtExam();
  initAppscGroup2Hub();
  initMapPointingHub();
  initAiMentor();
  initSyllabusTracker();
  initVoiceSearch();
  initMindmaps();
  initApHistoryHub();
  initSchemesHub();
  initMainsHub();
  await loadAvailableDates();
  await refreshCurrentView();
  if (window.lucide) lucide.createIcons();

  // Register PWA Service Worker
  if ("serviceWorker" in navigator) {
    navigator.serviceWorker.register("/sw.js").then(() => {
      console.log("PWA Service Worker registered successfully!");
    }).catch(err => {
      console.log("Service worker registration failed:", err);
    });
  }
});

// Setup Event Listeners
function setupEventListeners() {
  // Tab Switching
  navTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const targetTab = tab.getAttribute("data-tab");
      switchTab(targetTab);
    });
  });

  // Category Filter
  catPills.forEach(pill => {
    pill.addEventListener("click", () => {
      catPills.forEach(p => {
        p.classList.remove("active", "bg-blue-600", "text-white");
        p.classList.add("bg-white", "text-slate-700");
      });
      pill.classList.add("active", "bg-blue-600", "text-white");
      pill.classList.remove("bg-white", "text-slate-700");

      state.currentCategory = pill.getAttribute("data-category");
      loadArticles();
    });
  });

  // Date Change
  dateSelect.addEventListener("change", async (e) => {
    state.currentDate = e.target.value;
    document.getElementById("printDate").textContent = `తేదీ: ${state.currentDate}`;
    state.quizAnswers = {};
    await refreshCurrentView();
  });

  // Live Search with Debounce
  let searchTimeout = null;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      state.searchQuery = e.target.value.trim();
      loadArticles();
    }, 250);
  });

  // News Sync
  syncBtn.addEventListener("click", handleSyncNews);

  // Print / PDF
  printBtn.addEventListener("click", () => {
    window.print();
  });

  // Telegram Modal Handlers
  setupTelegramHandlers();

  // Telugu E-Papers & PDF Hub Modal
  initEpaperModal();

  // Reset Quiz
  resetQuizBtn.addEventListener("click", () => {
    state.quizAnswers = {};
    renderQuiz();
    updateQuizScore();
    showToast("క్విజ్ మళ్లీ ప్రారంభమైంది!");
  });
}

// Clock Display
function updateClock() {
  const el = document.getElementById("todayDateTime");
  if (!el) return;
  const now = new Date();
  const options = { weekday: 'short', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  el.textContent = now.toLocaleDateString('te-IN', options);
}

// Switch Active Tab
function switchTab(tabName) {
  state.currentTab = tabName;
  navTabs.forEach(tab => {
    const isTarget = tab.getAttribute("data-tab") === tabName;
    if (isTarget) {
      tab.classList.add("active", "border-blue-600", "text-blue-600");
      tab.classList.remove("border-transparent", "text-slate-600");
    } else {
      tab.classList.remove("active", "border-blue-600", "text-blue-600");
      tab.classList.add("border-transparent", "text-slate-600");
    }
  });

  tabContents.forEach(content => {
    content.classList.add("hidden");
  });

  const catFilterBar = document.getElementById("categoryFilterBar");
  if (tabName === "articles") {
    document.getElementById("articlesSection").classList.remove("hidden");
    catFilterBar.classList.remove("hidden");
  } else if (tabName === "quiz") {
    document.getElementById("quizSection").classList.remove("hidden");
    catFilterBar.classList.add("hidden");
  } else if (tabName === "oneliners") {
    document.getElementById("onelinersSection").classList.remove("hidden");
    catFilterBar.classList.add("hidden");
  } else if (tabName === "mocktests") {
    document.getElementById("mocktestsSection").classList.remove("hidden");
    catFilterBar.classList.add("hidden");
    loadMockSubjects();
  } else if (tabName === "flashcards") {
    document.getElementById("flashcardsSection").classList.remove("hidden");
    catFilterBar.classList.add("hidden");
    loadFlashcards();
  }

  if (window.lucide) lucide.createIcons();
}

// Load Dates Dropdown
async function loadAvailableDates() {
  try {
    const res = await fetch(`${API_BASE}/api/dates`);
    const data = await res.json();
    if (data.success && data.dates.length > 0) {
      dateSelect.innerHTML = "";
      data.dates.forEach(d => {
        const opt = document.createElement("option");
        opt.value = d;
        opt.textContent = `📅 ${d}`;
        dateSelect.appendChild(opt);
      });
      state.currentDate = data.dates[0];
      document.getElementById("printDate").textContent = `తేదీ: ${state.currentDate}`;
    }
  } catch (err) {
    console.error("Error loading dates:", err);
  }
}

// Refresh Current Data
async function refreshCurrentView() {
  await Promise.all([
    loadArticles(),
    loadQuiz(),
    loadOneLiners(),
    loadStats()
  ]);
}

// Load Articles
async function loadArticles() {
  if (!state.currentDate) return;
  const url = `${API_BASE}/api/affairs?date=${state.currentDate}&category=${state.currentCategory}&q=${encodeURIComponent(state.searchQuery)}`;
  try {
    const res = await fetch(url);
    const result = await res.json();
    if (result.success) {
      state.articles = result.data;
      renderArticles();
      document.getElementById("tabCountArticles").textContent = result.total;
      document.getElementById("statArticles").textContent = result.total;

      // Update Ticker with top headline
      if (result.data.length > 0) {
        tickerText.textContent = `⚡ ముఖ్యాంశం: ${result.data[0].title}`;
      }
    }
  } catch (err) {
    console.error("Error loading articles:", err);
  }
}

// Render Articles
function renderArticles() {
  articlesContainer.innerHTML = "";
  const noMsg = document.getElementById("noArticlesMessage");

  if (state.articles.length === 0) {
    noMsg.classList.remove("hidden");
    return;
  }
  noMsg.classList.add("hidden");

  let articlesToRender = state.articles;
  if (state.targetExam && state.targetExam !== "all") {
    const target = state.targetExam.toLowerCase();
    const filtered = state.articles.filter(art => {
      const text = `${art.exam_relevance || ''} ${art.tags || ''} ${art.title || ''}`.toLowerCase();
      if (target === "appsc") return text.includes("appsc") || text.includes("గ్రూప్") || text.includes("ఆంధ్ర") || text.includes("ap ");
      if (target === "tspsc") return text.includes("tspsc") || text.includes("గ్రూప్") || text.includes("తెలంగాణ") || text.includes("ts ");
      if (target === "police") return text.includes("పోలీస్") || text.includes("si") || text.includes("కానిస్టేబుల్") || text.includes("police");
      if (target === "banking") return text.includes("బ్యాంక్") || text.includes("bank") || text.includes("rbi") || text.includes("ssc") || text.includes("rrb") || text.includes("ఆర్థిక");
      if (target === "upsc") return text.includes("upsc") || text.includes("సివిల్స్") || text.includes("ias") || text.includes("జాతీయం");
      return true;
    });
    if (filtered.length > 0) {
      articlesToRender = filtered;
    }
  }

// Helper to extract source link from article object or detailed_notes
function extractArticleUrl(art) {
  if (!art) return null;
  if (art.url && art.url.startsWith("http")) return art.url;
  if (art.detailed_notes) {
    const match = art.detailed_notes.match(/(https?:\/\/[^\s<"'>]+)/);
    if (match) return match[1];
  }
  return null;
}

// Helper to format detailed notes with clickable, high-contrast links
function formatDetailedNotes(notes) {
  if (!notes) return "";
  const lines = notes.split("\n");
  const formatted = lines.map(line => {
    const urlMatch = line.match(/(https?:\/\/[^\s<"'>]+)/);
    if (urlMatch) {
      const url = urlMatch[1];
      const prefix = line.substring(0, line.indexOf(url));
      return `${prefix}<a href="${url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-sky-400 hover:text-sky-300 underline font-black break-all px-1 py-0.5 rounded transition" title="సంబంధిత వెబ్‌సైట్‌లో ఈ వార్తను ఓపెన్ చేయండి">
        <span>${url}</span>
        <svg class="w-3.5 h-3.5 inline shrink-0 text-sky-400" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path></svg>
      </a>\n<div class="my-2"><a href="${url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white text-xs font-black rounded-lg shadow-sm transition hover:scale-[1.02] cursor-pointer">
        <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1"></path></svg>
        <span>🌐 సంబంధిత వెబ్‌సైట్‌లో పూర్తి కథనం ఓపెన్ చేయండి (Open Link ↗)</span>
      </a></div>`;
    }
    return line;
  });
  return formatted.join("\n");
}

  articlesToRender.forEach(art => {
    const catInfo = CATEGORY_MAP[art.category] || { label: "🏛️ జాతీయం", class: "badge-national" };
    const borderCls = `border-cat-${art.category}` || "border-cat-national";
    const artLink = extractArticleUrl(art);
    
    const card = document.createElement("div");
    card.className = `article-card bg-white rounded-2xl border ${borderCls} p-5 card-shadow flex flex-col justify-between`;
    card.innerHTML = `
      <div>
        <div class="flex flex-wrap justify-between items-center gap-2 mb-3">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span class="text-xs font-black px-2.5 py-1 rounded-md ${catInfo.class}">
              ${catInfo.label}
            </span>
            <span class="text-xs font-bold px-2 py-0.5 rounded-md source-tag-badge">
              📰 ${art.source ? art.source.split('(')[0].trim() : 'దినపత్రిక'}
            </span>
          </div>
          <span class="text-xs font-bold px-2.5 py-0.5 rounded-md exam-tag-badge">
            🎯 ${art.exam_relevance || "పోటీ పరీక్షల ప్రత్యేకం"}
          </span>
        </div>
        
        <h3 class="article-title text-base sm:text-lg font-black text-slate-950 mb-2.5 leading-snug tracking-tight">
          ${art.title}
        </h3>
        
        <p class="article-summary text-xs sm:text-sm text-slate-950 font-semibold mb-4 leading-relaxed">
          ${art.summary}
        </p>

        <!-- Detailed Notes Box (High Contrast with Clickable Links) -->
        ${art.detailed_notes ? `
          <div class="article-details rounded-xl p-3.5 text-xs sm:text-sm mb-3 space-y-1.5 shadow-2xs">
            <p class="article-details-header font-black flex items-center gap-1.5 text-xs sm:text-sm">
              <i data-lucide="bookmark" class="w-4 h-4"></i>
              <span>పరీక్షల కీలక అంశాలు & సమగ్ర నోట్స్ (Exam Takeaways):</span>
            </p>
            <div class="article-details-text whitespace-pre-line leading-relaxed font-bold">${formatDetailedNotes(art.detailed_notes)}</div>
          </div>
        ` : ''}
      </div>

      <div class="article-footer flex justify-between items-center pt-3 border-t border-slate-200 text-xs font-bold no-print gap-2">
        <div class="flex items-center gap-1.5 truncate">
          <span class="truncate max-w-[110px] text-slate-500">ఆధారం: ${art.source || "దినపత్రికలు"}</span>
          ${artLink ? `
            <a href="${artLink}" target="_blank" rel="noopener noreferrer" class="text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 bg-blue-50 dark:bg-blue-900/40 px-2 py-0.5 rounded border border-blue-200 dark:border-blue-700 text-[11px] font-black flex items-center gap-1 transition shadow-2xs hover:shadow-xs" title="మూల వార్తా వెబ్‌సైట్ ఓపెన్ చేయండి">
              <i data-lucide="external-link" class="w-3 h-3"></i>
              <span>ఓపెన్ ↗</span>
            </a>
          ` : ''}
        </div>
        <div class="flex items-center space-x-2">
          <button class="btn-audio-listen font-extrabold flex items-center gap-0.5" onclick="playArticleAudio(${art.id})" title="ఈ ఆర్టికల్ తెలుగు ఆడియో వినండి">
            <i data-lucide="volume-2" class="w-3.5 h-3.5"></i>
            <span>వినండి</span>
          </button>
          <button class="btn-bookmark font-extrabold flex items-center gap-0.5" onclick="toggleBookmark(${art.id}, '${art.title.replace(/'/g, "\\'")}', '${art.category}', '${art.date}')" title="ఈ ఆర్టికల్ సేవ్ చేసుకోండి">
            <i data-lucide="${isBookmarked(art.id) ? 'bookmark-check' : 'bookmark'}" class="w-3.5 h-3.5"></i>
            <span>${isBookmarked(art.id) ? 'సేవ్డ్' : 'సేవ్'}</span>
          </button>
          <button class="btn-copy font-extrabold flex items-center gap-0.5" onclick="navigator.clipboard.writeText('${art.title.replace(/'/g, "\\'")}\\n\\n${art.summary.replace(/'/g, "\\'")}'); showToast('నోట్స్ కాపీ చేయబడింది!');">
            <i data-lucide="copy" class="w-3.5 h-3.5"></i>
            <span>కాపీ</span>
          </button>
        </div>
      </div>
    `;
    articlesContainer.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

// Load Quiz
async function loadQuiz() {
  if (!state.currentDate) return;
  const url = `${API_BASE}/api/quiz?date=${state.currentDate}`;
  try {
    const res = await fetch(url);
    const result = await res.json();
    if (result.success) {
      state.quizData = result.data;
      document.getElementById("tabCountQuiz").textContent = result.total;
      document.getElementById("statQuiz").textContent = result.total;
      renderQuiz();
      updateQuizScore();
    }
  } catch (err) {
    console.error("Error loading quiz:", err);
  }
}

// Render Quiz Questions
function renderQuiz() {
  quizContainer.innerHTML = "";
  const noMsg = document.getElementById("noQuizMessage");

  if (state.quizData.length === 0) {
    noMsg.classList.remove("hidden");
    return;
  }
  noMsg.classList.add("hidden");

  state.quizData.forEach((q, index) => {
    const answered = state.quizAnswers[q.id];
    const card = document.createElement("div");
    card.className = "bg-white rounded-xl border border-slate-200 p-5 card-shadow";

    const options = [
      { key: "A", text: q.option_a },
      { key: "B", text: q.option_b },
      { key: "C", text: q.option_c },
      { key: "D", text: q.option_d }
    ];

    let optionsHtml = "";
    options.forEach(opt => {
      let optionClass = "bg-slate-50 border-slate-200 text-slate-800";
      let statusIcon = "";

      if (answered) {
        if (opt.key === q.correct_option) {
          optionClass = "correct";
          statusIcon = `<i data-lucide="check" class="w-4 h-4 text-emerald-600 ml-auto"></i>`;
        } else if (answered === opt.key && answered !== q.correct_option) {
          optionClass = "wrong";
          statusIcon = `<i data-lucide="x" class="w-4 h-4 text-red-600 ml-auto"></i>`;
        }
      }

      optionsHtml += `
        <div class="quiz-option border rounded-lg p-3 text-xs sm:text-sm flex items-center space-x-2.5 ${optionClass}" 
             data-qid="${q.id}" data-option="${opt.key}" onclick="handleQuizAnswer(${q.id}, '${opt.key}')">
          <span class="w-6 h-6 rounded-full border border-slate-300 flex items-center justify-center font-bold text-xs bg-white text-slate-700 shrink-0">
            ${opt.key}
          </span>
          <span class="flex-1">${opt.text}</span>
          ${statusIcon}
        </div>
      `;
    });

    card.innerHTML = `
      <div class="flex justify-between items-start gap-2 mb-3">
        <span class="text-xs font-bold px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-100">
          ప్రశ్న ${index + 1}
        </span>
        <span class="text-xs font-semibold text-slate-500">
          🎯 ${q.exam_tag || "General Studies"}
        </span>
      </div>
      
      <p class="text-sm sm:text-base font-bold text-slate-900 mb-4">
        ${q.question}
      </p>

      <div class="space-y-2 mb-3">
        ${optionsHtml}
      </div>

      <!-- Explanation (Shows after user answers) -->
      ${answered ? `
        <div class="mt-4 p-3.5 bg-emerald-50 border border-emerald-200 rounded-lg text-xs sm:text-sm text-emerald-900">
          <p class="font-bold flex items-center gap-1 text-emerald-800 mb-1">
            <i data-lucide="info" class="w-4 h-4"></i> సరైన సమాధానం: ఆప్షన్ ${q.correct_option}
          </p>
          <p class="leading-relaxed">${q.explanation}</p>
        </div>
      ` : ''}
    `;

    quizContainer.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

// Handle Quiz Option Selection
window.handleQuizAnswer = function(qid, selectedOption) {
  if (state.quizAnswers[qid]) return; // Already answered
  state.quizAnswers[qid] = selectedOption;
  renderQuiz();
  updateQuizScore();
};

// Update Quiz Score Counter
function updateQuizScore() {
  let correctCount = 0;
  const answeredCount = Object.keys(state.quizAnswers).length;

  state.quizData.forEach(q => {
    if (state.quizAnswers[q.id] === q.correct_option) {
      correctCount++;
    }
  });

  const total = state.quizData.length;
  document.getElementById("statScore").textContent = `${correctCount} / ${total}`;
}

// Load One-Liners
async function loadOneLiners() {
  if (!state.currentDate) return;
  const url = `${API_BASE}/api/one_liners?date=${state.currentDate}`;
  try {
    const res = await fetch(url);
    const result = await res.json();
    if (result.success) {
      state.oneLiners = result.data;
      document.getElementById("tabCountOneliners").textContent = result.total;
      document.getElementById("statOneliners").textContent = result.total;
      renderOneLiners();
    }
  } catch (err) {
    console.error("Error loading one-liners:", err);
  }
}

// Filter One-Liners by Category
window.filterOneLinersByCategory = function(category) {
  state.currentOneLinerCategory = category;
  
  // Update filter pill UI
  const pills = document.querySelectorAll(".oneliner-filter-pill");
  pills.forEach(pill => {
    const fnStr = pill.getAttribute("onclick") || "";
    if (fnStr.includes(`'${category}'`)) {
      pill.classList.add("active", "bg-blue-600", "text-white");
      pill.classList.remove("bg-white", "text-slate-700");
    } else {
      pill.classList.remove("active", "bg-blue-600", "text-white");
      pill.classList.add("bg-white", "text-slate-700");
    }
  });

  renderOneLiners();
};

// Open Article by Category (e.g. Science & Technology)
window.openArticleByCategory = async function(category) {
  // 1. Look in loaded articles
  let art = state.articles.find(a => a.category === category);
  
  // 2. Fetch directly from backend if not found
  if (!art) {
    try {
      const res = await fetch(`${API_BASE}/api/article/category/${category}?date=${state.currentDate || ''}`);
      const data = await res.json();
      if (data.success && data.article) {
        art = data.article;
      }
    } catch (e) {
      console.error("Error fetching article by category:", e);
    }
  }

  if (art) {
    openArticleDetail(art);
  } else {
    // Switch to articles tab and apply filter
    switchTab("articles");
    state.currentCategory = category;
    catPills.forEach(p => {
      if (p.getAttribute("data-category") === category) {
        p.classList.add("active", "bg-blue-600", "text-white");
        p.classList.remove("bg-white", "text-slate-700");
      } else {
        p.classList.remove("active", "bg-blue-600", "text-white");
        p.classList.add("bg-white", "text-slate-700");
      }
    });
    loadArticles();
    showToast(`${CATEGORY_MAP[category]?.label || category} విభాగం ఆర్టికల్స్ తెరవబడ్డాయి!`);
  }
};

// Render One-Liners (Quick Revision)
function renderOneLiners() {
  onelinersContainer.innerHTML = "";
  const noMsg = document.getElementById("noOnelinersMessage");

  let filtered = state.oneLiners;
  if (state.currentOneLinerCategory && state.currentOneLinerCategory !== "all") {
    filtered = filtered.filter(item => item.category === state.currentOneLinerCategory);
  }

  if (filtered.length === 0) {
    noMsg.classList.remove("hidden");
    return;
  }
  noMsg.classList.add("hidden");

  filtered.forEach(item => {
    const catInfo = CATEGORY_MAP[item.category] || { label: "🏛️ జాతీయం", class: "badge-national" };

    // Find best matching article for this one-liner
    let matchingArticle = null;
    if (state.articles && state.articles.length > 0) {
      const words = item.point.split(/[\s,–—:-]+/).filter(w => w.length > 3);
      matchingArticle = state.articles.find(a => {
        if (a.category === item.category) {
          return words.some(w => a.title.includes(w) || a.summary.includes(w));
        }
        return false;
      });
      if (!matchingArticle) {
        matchingArticle = state.articles.find(a => a.category === item.category);
      }
    }

    if (!matchingArticle) {
      matchingArticle = {
        id: item.id || 999,
        title: item.point,
        category: item.category,
        date: item.date || state.currentDate,
        source: "దినపత్రికల సారాంశం",
        exam_relevance: "APPSC / TSPSC / UPSC ప్రత్యేకం",
        summary: item.point,
        detailed_notes: `• సంబంధిత అంశం: ${item.point}\n• విభాగం: ${catInfo.label}\n• పరీక్షల ప్రాముఖ్యత: APPSC / TSPSC గ్రూప్స్ & ఇతర పోటీ పరీక్షలకు అత్యంత కీలకమైన అంశం.\n• అదనపు సమాచారం కోసం దినపత్రిక ఆర్టికల్స్ విభాగం చూడండి.`
      };
    }

    const li = document.createElement("li");
    li.className = "p-3.5 rounded-xl bg-white hover:bg-blue-50/60 border border-slate-200 transition duration-150 flex flex-col sm:flex-row justify-between sm:items-center gap-3 cursor-pointer group shadow-2xs hover:border-blue-300";
    li.title = "పూర్తి ఆర్టికల్, పరీక్షల నోట్స్ & ఆడియో కోసం క్లిక్ చేయండి";

    li.innerHTML = `
      <div class="flex items-start sm:items-center gap-3 flex-1">
        <button type="button" class="text-xs font-bold px-2.5 py-1 rounded-md ${catInfo.class} shrink-0 hover:scale-105 transition shadow-2xs flex items-center gap-1" title="${catInfo.label} పూర్తి ఆర్టికల్ చూడండి" onclick="event.stopPropagation(); openArticleByCategory('${item.category}')">
          <span>${catInfo.label}</span>
          <i data-lucide="chevron-right" class="w-3 h-3 opacity-60"></i>
        </button>
        <p class="text-xs sm:text-sm text-slate-800 font-medium leading-relaxed group-hover:text-blue-950">
          ${item.point}
        </p>
      </div>

      <div class="flex items-center gap-2 shrink-0 self-end sm:self-center">
        <button class="text-xs font-semibold text-blue-600 group-hover:text-blue-800 bg-blue-50 group-hover:bg-blue-100/90 px-3 py-1.5 rounded-lg flex items-center gap-1.5 transition border border-blue-100 shadow-2xs">
          <i data-lucide="book-open" class="w-3.5 h-3.5 text-blue-600"></i>
          <span>పూర్తి ఆర్టికల్</span>
          <i data-lucide="arrow-up-right" class="w-3 h-3 text-blue-500"></i>
        </button>
      </div>
    `;

    // Clicking anywhere on the row opens the full article
    li.addEventListener("click", () => {
      openArticleDetail(matchingArticle);
    });

    onelinersContainer.appendChild(li);
  });

  if (window.lucide) lucide.createIcons();
}

// Load Stats
async function loadStats() {
  if (!state.currentDate) return;
  try {
    const res = await fetch(`${API_BASE}/api/stats?date=${state.currentDate}`);
    const data = await res.json();
    if (data.success) {
      document.getElementById("statArticles").textContent = data.stats.articles_count;
      document.getElementById("statQuiz").textContent = data.stats.quiz_count;
      document.getElementById("statOneliners").textContent = data.stats.one_liners_count;
    }
  } catch (err) {
    console.error("Error loading stats:", err);
  }
}

// Handle News Sync
async function handleSyncNews() {
  syncBtn.disabled = true;
  syncBtn.innerHTML = `
    <i data-lucide="loader-2" class="w-3.5 h-3.5 animate-spin"></i>
    <span>సింక్ అవుతోంది...</span>
  `;
  if (window.lucide) lucide.createIcons();

  try {
    const res = await fetch(`${API_BASE}/api/sync?date=${state.currentDate || ''}`, {
      method: "POST"
    });
    const result = await res.json();
    if (result.success) {
      showToast("తాజా కరెంట్ అఫైర్స్ వార్తలు సింక్ అయ్యాయి!");
      await loadAvailableDates();
      await refreshCurrentView();
    } else {
      showToast("సింక్ ప్రక్రియలో లోపం ఏర్పడింది.");
    }
  } catch (err) {
    console.error("Error syncing news:", err);
    showToast("సర్వర్‌తో కనెక్షన్ లోపం.");
  } finally {
    syncBtn.disabled = false;
    syncBtn.innerHTML = `
      <i data-lucide="refresh-cw" class="w-3.5 h-3.5"></i>
      <span>వార్తలు సింక్ చేయి</span>
    `;
    if (window.lucide) lucide.createIcons();
  }
}

// Toast Helper
function showToast(msg) {
  toastMsg.textContent = msg;
  toast.classList.remove("translate-y-20", "opacity-0");
  toast.classList.add("translate-y-0", "opacity-100");
  setTimeout(() => {
    toast.classList.remove("translate-y-0", "opacity-100");
    toast.classList.add("translate-y-20", "opacity-0");
  }, 3000);
}

// Telegram Modal & API Handlers
function setupTelegramHandlers() {
  const modal = document.getElementById("telegramModal");
  const openBtn = document.getElementById("openTelegramModalBtn");
  const closeBtn = document.getElementById("closeTelegramModalBtn");
  const tokenInput = document.getElementById("tgBotToken");
  const chatIdInput = document.getElementById("tgChatId");
  const statusText = document.getElementById("tgStatusText");
  const testBtn = document.getElementById("tgTestBtn");
  const saveBtn = document.getElementById("tgSaveBtn");
  const sendDigestBtn = document.getElementById("tgSendDigestBtn");

  if (!modal || !openBtn) return;

  // Open & Load Config
  openBtn.addEventListener("click", async () => {
    modal.classList.remove("hidden");
    try {
      const res = await fetch(`${API_BASE}/api/telegram/config`);
      const data = await res.json();
      if (data.success) {
        if (data.chat_id) chatIdInput.value = data.chat_id;
        if (data.has_token) {
          statusText.textContent = `✅ బోట్ టోకెన్ కాన్ఫిగర్ చేయబడింది (${data.masked_token})`;
          statusText.className = "text-xs text-emerald-600 font-medium";
          tokenInput.placeholder = `టోకెన్ కాన్ఫిగర్ అయింది (${data.masked_token}) - మార్చాలనుకుంటేనే ఇవ్వండి`;
        } else {
          statusText.textContent = "⚠️ టోకెన్ ఇంకా కాన్ఫిగర్ చేయలేదు.";
          statusText.className = "text-xs text-amber-600 font-medium";
          tokenInput.placeholder = "ఉదా: 123456789:ABCdefGhIJkLmNoPQRstUVwxyz";
        }
      }

      // Load Scheduler Config
      const schedRes = await fetch(`${API_BASE}/api/scheduler/config`);
      const schedData = await schedRes.json();
      if (schedData.success) {
        const toggle = document.getElementById("schedulerToggle");
        const timeInput = document.getElementById("schedulerTime");
        const schedStatus = document.getElementById("schedulerStatus");
        if (toggle) toggle.checked = schedData.config.enabled;
        if (timeInput) timeInput.value = schedData.config.scheduled_time || "07:00";
        if (schedStatus) {
          schedStatus.textContent = schedData.config.enabled 
            ? `స్థితి: ఉదయం ${schedData.config.scheduled_time} కు ఆటోమేటిక్ అప్‌డేట్` 
            : `స్థితి: ఆటో షెడ్యూలర్ ఆఫ్ చేయబడింది`;
        }
      }
    } catch (e) {
      console.error(e);
    }
  });

  // Scheduler Trigger Now
  const triggerNowBtn = document.getElementById("triggerNowBtn");
  if (triggerNowBtn) {
    triggerNowBtn.addEventListener("click", async () => {
      triggerNowBtn.disabled = true;
      triggerNowBtn.textContent = "రన్ అవుతోంది...";
      try {
        const res = await fetch(`${API_BASE}/api/scheduler/trigger`, { method: "POST" });
        const data = await res.json();
        if (data.success) {
          showToast("డైలీ జాబ్ రన్ అయింది! తాజా వార్తలు & టెలిగ్రామ్ అప్‌డేట్ అయ్యాయి.");
          await refreshCurrentView();
        }
      } catch (e) {
        alert("రన్ చేయడంలో లోపం.");
      } finally {
        triggerNowBtn.disabled = false;
        triggerNowBtn.innerHTML = `<i data-lucide="play" class="w-3 h-3"></i>ఇప్పుడే రన్ చేయి`;
        if (window.lucide) lucide.createIcons();
      }
    });
  }

  // Close
  closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.add("hidden");
  });

  // Save Config
  saveBtn.addEventListener("click", async () => {
    const token = tokenInput.value.trim();
    const chatId = chatIdInput.value.trim();
    const schedToggle = document.getElementById("schedulerToggle");
    const schedTime = document.getElementById("schedulerTime");

    if (!chatId) {
      alert("దయచేసి Chat ID లేదా ఛానెల్ పేరు నమోదు చేయండి.");
      return;
    }
    saveBtn.disabled = true;
    try {
      // Save Telegram Config
      const res = await fetch(`${API_BASE}/api/telegram/config`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bot_token: token, chat_id: chatId })
      });

      // Save Scheduler Config
      if (schedToggle && schedTime) {
        await fetch(`${API_BASE}/api/scheduler/config`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            enabled: schedToggle.checked,
            scheduled_time: schedTime.value,
            auto_telegram: true
          })
        });
      }

      const data = await res.json();
      if (data.success) {
        showToast("అన్ని సెట్టింగ్స్ విజయవంతంగా సేవ్ చేయబడ్డాయి!");
        if (data.config && data.config.has_token) {
          statusText.textContent = `✅ బోట్ టోకెన్ కాన్ఫిగర్ చేయబడింది (${data.config.masked_token})`;
          statusText.className = "text-xs text-emerald-600 font-medium";
          tokenInput.value = "";
          tokenInput.placeholder = `టోకెన్ కాన్ఫిగర్ అయింది (${data.config.masked_token}) - మార్చాలనుకుంటేనే ఇవ్వండి`;
        } else {
          statusText.textContent = "✅ సెట్టింగ్స్ విజయవంతంగా సేవ్ అయ్యాయి.";
          statusText.className = "text-xs text-emerald-600 font-medium";
        }
      }
    } catch (e) {
      alert("సేవ్ చేయడంలో లోపం ఏర్పడింది.");
    } finally {
      saveBtn.disabled = false;
    }
  });

  // Test Message
  testBtn.addEventListener("click", async () => {
    const token = tokenInput.value.trim();
    const chatId = chatIdInput.value.trim();
    testBtn.disabled = true;
    testBtn.textContent = "పంపుతోంది...";
    try {
      const res = await fetch(`${API_BASE}/api/telegram/test`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ bot_token: token, chat_id: chatId })
      });
      const data = await res.json();
      if (data.success) {
        showToast("టెస్ట్ మెసేజ్ మీ టెలిగ్రామ్‌కు చేరింది!");
      } else {
        alert(`టెలిగ్రామ్ ఎర్రర్: ${data.error || 'కనెక్షన్ విఫలమైంది'}`);
      }
    } catch (e) {
      alert("టెస్ట్ మెసేజ్ పంపడంలో లోపం ఏర్పడింది.");
    } finally {
      testBtn.disabled = false;
      testBtn.innerHTML = `<i data-lucide="bell" class="w-3.5 h-3.5"></i><span>టెస్ట్ మెసేజ్ పంపు</span>`;
      if (window.lucide) lucide.createIcons();
    }
  });

  // Send Daily Digest + Quiz
  sendDigestBtn.addEventListener("click", async () => {
    const token = tokenInput.value.trim();
    const chatId = chatIdInput.value.trim();
    sendDigestBtn.disabled = true;
    sendDigestBtn.textContent = "డైజెస్ట్ పంపుతోంది...";
    try {
      const res = await fetch(`${API_BASE}/api/telegram/send`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ date: state.currentDate, bot_token: token, chat_id: chatId })
      });
      const data = await res.json();
      if (data.success) {
        showToast("నేటి కరెంట్ అఫైర్స్ & క్విజ్ టెలిగ్రామ్‌కు చేరాయి!");
        modal.classList.add("hidden");
      } else {
        alert(`ఎర్రర్: ${data.error || 'పంపడం విఫలమైంది'}`);
      }
    } catch (e) {
      alert("డైజెస్ట్ పంపడంలో లోపం ఏర్పడింది.");
    } finally {
      sendDigestBtn.disabled = false;
      sendDigestBtn.innerHTML = `<i data-lucide="send" class="w-3.5 h-3.5"></i><span>నేటి డైజెస్ట్ + క్విజ్ పంపు</span>`;
      if (window.lucide) lucide.createIcons();
    }
  });
}

// ==================== TELUGU E-PAPERS & PDF HUB ====================
function initEpaperModal() {
  const modal = document.getElementById("epaperModal");
  const openBtn = document.getElementById("openEpaperModalBtn");
  const closeBtn = document.getElementById("closeEpaperModalBtn");
  const sendTgBtn = document.getElementById("epaperSendTelegramBtn");
  const dateSpan = document.getElementById("epaperModalDate");
  const downloadLink = document.getElementById("epaperDownloadLink");
  const viewWebLink = document.getElementById("epaperViewWebLink");
  const tgStatus = document.getElementById("epaperTgStatus");

  if (!modal || !openBtn) return;

  openBtn.addEventListener("click", () => {
    const activeDate = state.currentDate || new Date().toISOString().split("T")[0];
    if (dateSpan) dateSpan.textContent = `తేదీ: ${activeDate}`;
    if (downloadLink) downloadLink.href = `/api/epaper/pdf?date=${activeDate}`;
    if (viewWebLink) viewWebLink.href = `/epaper?date=${activeDate}`;
    if (tgStatus) {
      tgStatus.classList.add("hidden");
      tgStatus.textContent = "";
    }
    modal.classList.remove("hidden");
    if (window.lucide) lucide.createIcons();
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.classList.add("hidden");
  });

  if (sendTgBtn) {
    sendTgBtn.addEventListener("click", async () => {
      const activeDate = state.currentDate || new Date().toISOString().split("T")[0];
      sendTgBtn.disabled = true;
      sendTgBtn.innerHTML = `<span class="animate-spin mr-1">⏳</span><span>టెలిగ్రామ్‌కు పంపుతోంది...</span>`;
      if (tgStatus) {
        tgStatus.classList.remove("hidden");
        tgStatus.textContent = "⏳ PDF జనరేట్ చేసి టెలిగ్రామ్‌కు అప్‌లోడ్ చేస్తోంది... దయచేసి 5 సెకన్లు వేచి ఉండండి...";
        tgStatus.className = "mt-2 text-xs font-semibold text-amber-300";
      }

      try {
        const res = await fetch(`${API_BASE}/api/telegram/send_epaper_pdf`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ date: activeDate })
        });
        const data = await res.json();
        if (data.success) {
          if (tgStatus) {
            tgStatus.textContent = "✅ తెలుగు ఈ-పేపర్ PDF మీ టెలిగ్రామ్‌కు విజయవంతంగా చేరింది!";
            tgStatus.className = "mt-2 text-xs font-semibold text-emerald-300";
          }
          showToast("తెలుగు ఈ-పేపర్ PDF టెలిగ్రామ్‌కు పంపబడింది!");
        } else {
          if (tgStatus) {
            tgStatus.textContent = `⚠️ ఎర్రర్: ${data.error || 'పంపడం విఫలమైంది'}`;
            tgStatus.className = "mt-2 text-xs font-semibold text-rose-300";
          }
        }
      } catch (err) {
        if (tgStatus) {
          tgStatus.textContent = "⚠️ సర్వర్ కనెక్షన్ లోపం.";
          tgStatus.className = "mt-2 text-xs font-semibold text-rose-300";
        }
      } finally {
        sendTgBtn.disabled = false;
        sendTgBtn.innerHTML = `<i data-lucide="send" class="w-4 h-4"></i><span>టెలిగ్రామ్‌కు PDF పంపండి</span>`;
        if (window.lucide) lucide.createIcons();
      }
    });
  }
}

// ==================== MOCK TESTS MODULE (Feature 4) ====================
const mockState = {
  activeSubject: null,
  questions: [],
  answers: {}
};

async function loadMockSubjects() {
  const grid = document.getElementById("mockSubjectsGrid");
  if (!grid) return;
  try {
    const res = await fetch(`${API_BASE}/api/mock_tests`);
    const data = await res.json();
    if (data.success) {
      grid.innerHTML = "";
      Object.values(data.subjects).forEach(sub => {
        const isActive = mockState.activeSubject === sub.key;
        const btn = document.createElement("button");
        btn.className = `text-left p-4 rounded-xl border transition flex flex-col justify-between ${isActive ? 'bg-purple-50 border-purple-500 shadow-sm' : 'bg-slate-50 hover:bg-slate-100 border-slate-200'}`;
        btn.innerHTML = `
          <div>
            <div class="flex justify-between items-center mb-2">
              <span class="text-xs font-bold px-2 py-0.5 rounded ${isActive ? 'bg-purple-600 text-white' : 'bg-slate-200 text-slate-700'}">
                ${sub.total_questions} ప్రశ్నలు
              </span>
              <i data-lucide="${sub.icon || 'book-open'}" class="w-5 h-5 ${isActive ? 'text-purple-600' : 'text-slate-400'}"></i>
            </div>
            <h4 class="text-sm font-bold text-slate-900 mb-1 leading-snug">${sub.title}</h4>
            <p class="text-xs text-slate-500 line-clamp-2">${sub.description}</p>
          </div>
          <span class="text-xs font-bold text-purple-700 mt-3 flex items-center gap-1">
            టెస్ట్ ప్రారంభించు &rarr;
          </span>
        `;
        btn.onclick = () => selectMockSubject(sub.key);
        grid.appendChild(btn);
      });

      if (!mockState.activeSubject && Object.keys(data.subjects).length > 0) {
        selectMockSubject(Object.keys(data.subjects)[0]);
      }
      if (window.lucide) lucide.createIcons();
    }
  } catch (e) {
    console.error("Error loading mock subjects:", e);
  }
}

async function selectMockSubject(subjectKey) {
  mockState.activeSubject = subjectKey;
  mockState.answers = {};
  const container = document.getElementById("mockQuestionsContainer");
  const badge = document.getElementById("mockScoreBadge");
  if (badge) badge.classList.remove("hidden");

  try {
    const res = await fetch(`${API_BASE}/api/mock_tests/${subjectKey}`);
    const data = await res.json();
    if (data.success) {
      mockState.questions = data.data.questions;
      renderMockQuestions();
      updateMockScore();
      loadMockSubjects();
    }
  } catch (e) {
    console.error("Error loading mock subject questions:", e);
  }
}

function renderMockQuestions() {
  const container = document.getElementById("mockQuestionsContainer");
  if (!container) return;
  container.innerHTML = "";

  mockState.questions.forEach((q, idx) => {
    const answered = mockState.answers[q.id];
    const card = document.createElement("div");
    card.className = "bg-white rounded-xl border border-slate-200 p-5 card-shadow";

    const options = [
      { key: "A", text: q.option_a },
      { key: "B", text: q.option_b },
      { key: "C", text: q.option_c },
      { key: "D", text: q.option_d }
    ];

    let optionsHtml = "";
    options.forEach(opt => {
      let optionClass = "bg-slate-50 border-slate-200 text-slate-800";
      let statusIcon = "";

      if (answered) {
        if (opt.key === q.correct_option) {
          optionClass = "correct";
          statusIcon = `<i data-lucide="check" class="w-4 h-4 text-emerald-600 ml-auto"></i>`;
        } else if (answered === opt.key && answered !== q.correct_option) {
          optionClass = "wrong";
          statusIcon = `<i data-lucide="x" class="w-4 h-4 text-red-600 ml-auto"></i>`;
        }
      }

      optionsHtml += `
        <div class="quiz-option border rounded-lg p-3 text-xs sm:text-sm flex items-center space-x-2.5 ${optionClass}" 
             onclick="handleMockAnswer(${q.id}, '${opt.key}')">
          <span class="w-6 h-6 rounded-full border border-slate-300 flex items-center justify-center font-bold text-xs bg-white text-slate-700 shrink-0">
            ${opt.key}
          </span>
          <span class="flex-1">${opt.text}</span>
          ${statusIcon}
        </div>
      `;
    });

    card.innerHTML = `
      <div class="flex justify-between items-start gap-2 mb-3">
        <span class="text-xs font-bold px-2 py-0.5 rounded bg-purple-100 text-purple-800">
          ప్రశ్న ${idx + 1} / ${mockState.questions.length}
        </span>
      </div>
      
      <p class="text-sm sm:text-base font-bold text-slate-900 mb-4">
        ${q.question}
      </p>

      <div class="space-y-2 mb-3">
        ${optionsHtml}
      </div>

      ${answered ? `
        <div class="mt-4 p-3.5 bg-emerald-50 border border-emerald-200 rounded-lg text-xs sm:text-sm text-emerald-900">
          <p class="font-bold flex items-center gap-1 text-emerald-800 mb-1">
            <i data-lucide="info" class="w-4 h-4"></i> సరైన సమాధానం: ఆప్షన్ ${q.correct_option}
          </p>
          <p class="leading-relaxed">${q.explanation}</p>
        </div>
      ` : ''}
    `;

    container.appendChild(card);
  });

  if (window.lucide) lucide.createIcons();
}

window.handleMockAnswer = function(qid, selectedOpt) {
  if (mockState.answers[qid]) return;
  mockState.answers[qid] = selectedOpt;
  renderMockQuestions();
  updateMockScore();
};

function updateMockScore() {
  let score = 0;
  mockState.questions.forEach(q => {
    if (mockState.answers[q.id] === q.correct_option) score++;
  });
  const text = document.getElementById("mockScoreText");
  if (text) text.textContent = `${score} / ${mockState.questions.length}`;
}

// ==================== FEATURE 1: NATIVE TELUGU VOICE AUDIO PLAYER ====================
let currentAudioPlayer = null;
let isPlayingAudio = false;

function initVoiceAudio() {
  const btn = document.getElementById("voiceAudioBtn");
  if (!btn) return;

  btn.addEventListener("click", () => {
    if (isPlayingAudio) {
      stopAudio();
    } else {
      playDailyAudio();
    }
  });
}

function stopAudio() {
  if (currentAudioPlayer) {
    currentAudioPlayer.pause();
    currentAudioPlayer.currentTime = 0;
    currentAudioPlayer = null;
  }
  isPlayingAudio = false;
  const btn = document.getElementById("voiceAudioBtn");
  const textEl = document.getElementById("voiceAudioText");
  if (textEl) textEl.textContent = "వార్తలు వినండి (Audio)";
  if (btn) {
    btn.classList.remove("bg-red-600");
    btn.classList.add("bg-indigo-700");
  }
  showToast("ఆడియో ఆపివేయబడింది.");
}

function playDailyAudio() {
  const textEl = document.getElementById("voiceAudioText");
  if (textEl) textEl.textContent = "ఆడియో లోడ్ అవుతోంది...";
  showToast("స్పష్టమైన తెలుగు ఆడియో బులెటిన్ లోడ్ అవుతోంది... 🔊");

  const audioUrl = `${API_BASE}/api/audio/daily?date=${state.currentDate || ''}`;
  playAudioUrl(audioUrl);
}

window.playArticleAudio = function(articleId) {
  stopAudio();
  showToast("ఈ ఆర్టికల్ తెలుగు ఆడియో ప్లే అవుతోంది 🔊");
  const audioUrl = `${API_BASE}/api/audio/article/${articleId}`;
  playAudioUrl(audioUrl);
};

window.speakText = function(text) {
  stopAudio();
  showToast("తెలుగు ఆడియో ప్లే అవుతోంది 🔊");
  const audioUrl = `${API_BASE}/api/audio?text=${encodeURIComponent(text)}`;
  playAudioUrl(audioUrl);
};

function playAudioUrl(url) {
  if (currentAudioPlayer) {
    currentAudioPlayer.pause();
  }

  currentAudioPlayer = new Audio(url);
  const btn = document.getElementById("voiceAudioBtn");
  const textEl = document.getElementById("voiceAudioText");

  currentAudioPlayer.onplay = () => {
    isPlayingAudio = true;
    if (textEl) textEl.textContent = "ఆపండి (Stop Audio)";
    if (btn) {
      btn.classList.remove("bg-indigo-700");
      btn.classList.add("bg-red-600");
    }
  };

  currentAudioPlayer.onended = () => {
    isPlayingAudio = false;
    if (textEl) textEl.textContent = "వార్తలు వినండి (Audio)";
    if (btn) {
      btn.classList.remove("bg-red-600");
      btn.classList.add("bg-indigo-700");
    }
    showToast("ఆడియో పూర్తయింది!");
  };

  currentAudioPlayer.onerror = (e) => {
    console.error("Audio error:", e);
    isPlayingAudio = false;
    if (textEl) textEl.textContent = "వార్తలు వినండి (Audio)";
    if (btn) {
      btn.classList.remove("bg-red-600");
      btn.classList.add("bg-indigo-700");
    }
    showToast("ఆడియో ప్లే చేయడంలో లోపం ఏర్పడింది.");
  };

  currentAudioPlayer.play().catch(err => {
    console.log("Audio play error:", err);
  });
}

// ==================== FEATURE 2: DARK MODE ====================
function initDarkMode() {
  const toggle = document.getElementById("darkModeToggle");
  const icon = document.getElementById("themeIcon");
  const saved = localStorage.getItem("ca_theme");

  if (saved === "dark") {
    document.body.classList.add("dark");
    if (icon) icon.setAttribute("data-lucide", "sun");
  }

  if (toggle) {
    toggle.addEventListener("click", () => {
      document.body.classList.toggle("dark");
      const isDark = document.body.classList.contains("dark");
      localStorage.setItem("ca_theme", isDark ? "dark" : "light");
      if (icon) {
        icon.setAttribute("data-lucide", isDark ? "sun" : "moon");
      }
      if (window.lucide) lucide.createIcons();
      showToast(isDark ? "నైట్ మోడ్ ఆన్ అయింది 🌙" : "డే మోడ్ ఆన్ అయింది ☀️");
    });
  }
}

// ==================== FEATURE 3: BOOKMARKS ====================
function getSavedBookmarks() {
  try {
    return JSON.parse(localStorage.getItem("ca_bookmarks") || "[]");
  } catch (e) {
    return [];
  }
}

// ==================== FEATURE: NOTES & BOOKMARKS STUDIO ====================
function getSavedBookmarks() {
  return JSON.parse(localStorage.getItem("ca_bookmarks") || "[]");
}

function getPersonalNotes() {
  return JSON.parse(localStorage.getItem("ca_personal_notes") || "[]");
}

window.isBookmarked = function(id) {
  const bks = getSavedBookmarks();
  return bks.some(b => b.id === id);
};

window.toggleBookmark = function(id, title, category, date) {
  let bks = getSavedBookmarks();
  const exists = bks.find(b => b.id === id);
  if (exists) {
    bks = bks.filter(b => b.id !== id);
    showToast("ఆర్టికల్ బుక్‌మార్క్ తొలగించబడింది.");
  } else {
    bks.unshift({ id, title, category, date: date || new Date().toISOString().split("T")[0] });
    showToast("ఆర్టికల్ నోట్స్ లో భద్రపరచబడింది! 🔖");
  }
  localStorage.setItem("ca_bookmarks", JSON.stringify(bks));
  updateNotesStudioBadges();
  renderArticles();
  renderBookmarksList();
};

window.switchNotesStudioTab = function(tab) {
  const bTab = document.getElementById("notesStudioBookmarksTab");
  const nTab = document.getElementById("notesStudioMyNotesTab");
  const bBtn = document.getElementById("tabBookmarksBtn");
  const nBtn = document.getElementById("tabMyNotesBtn");

  if (tab === "bookmarks") {
    bTab.classList.remove("hidden");
    nTab.classList.add("hidden");
    bBtn.className = "px-3 py-2 border-b-2 border-indigo-600 text-indigo-600 dark:text-indigo-400 flex items-center gap-1.5 font-bold";
    nBtn.className = "px-3 py-2 border-b-2 border-transparent text-slate-500 hover:text-slate-800 dark:text-slate-400 flex items-center gap-1.5 font-semibold";
  } else {
    bTab.classList.add("hidden");
    nTab.classList.remove("hidden");
    nBtn.className = "px-3 py-2 border-b-2 border-indigo-600 text-indigo-600 dark:text-indigo-400 flex items-center gap-1.5 font-bold";
    bBtn.className = "px-3 py-2 border-b-2 border-transparent text-slate-500 hover:text-slate-800 dark:text-slate-400 flex items-center gap-1.5 font-semibold";
    renderPersonalNotesList();
  }
};

window.savePersonalNote = function() {
  const titleInput = document.getElementById("newNoteTitle");
  const catInput = document.getElementById("newNoteCategory");
  const contentInput = document.getElementById("newNoteContent");

  const title = titleInput.value.trim();
  const content = contentInput.value.trim();
  const category = catInput.value;

  if (!title || !content) {
    showToast("దయచేసి నోట్ టైటిల్ మరియు వివరాలు నమోదు చేయండి!");
    return;
  }

  const notes = getPersonalNotes();
  const newNote = {
    id: Date.now(),
    title: title,
    category: category,
    content: content,
    date: new Date().toLocaleDateString('te-IN', { year: 'numeric', month: 'short', day: 'numeric' })
  };

  notes.unshift(newNote);
  localStorage.setItem("ca_personal_notes", JSON.stringify(notes));

  titleInput.value = "";
  contentInput.value = "";

  updateNotesStudioBadges();
  renderPersonalNotesList();
  showToast("సొంత నోట్ విజయవంతంగా సేవ్ చేయబడింది! ✍️");
};

window.deletePersonalNote = function(id) {
  let notes = getPersonalNotes();
  notes = notes.filter(n => n.id !== id);
  localStorage.setItem("ca_personal_notes", JSON.stringify(notes));
  updateNotesStudioBadges();
  renderPersonalNotesList();
  showToast("నోట్ తొలగించబడింది.");
};

window.copyPersonalNote = function(id) {
  const notes = getPersonalNotes();
  const note = notes.find(n => n.id === id);
  if (note) {
    navigator.clipboard.writeText(`${note.title} (${note.category})\n\n${note.content}`);
    showToast("నోట్ కాపీ చేయబడింది!");
  }
};

window.exportNotesAsTxt = function() {
  const bks = getSavedBookmarks();
  const notes = getPersonalNotes();

  let text = `========================================================\n`;
  text += `లక్ష్య కరెంట్ అఫైర్స్ - నా వ్యక్తిగత స్టడీ నోట్స్ & బుక్‌మార్క్స్\n`;
  text += `తేదీ: ${new Date().toLocaleDateString('te-IN')}\n`;
  text += `========================================================\n\n`;

  text += `--- ✍️ నా సొంత నోట్స్ (${notes.length}) ---\n\n`;
  notes.forEach((n, idx) => {
    text += `${idx + 1}. [${n.category}] ${n.title} (${n.date})\n`;
    text += `${n.content}\n\n`;
  });

  text += `--- 🔖 సేవ్ చేసిన ఆర్టికల్స్ (${bks.length}) ---\n\n`;
  bks.forEach((b, idx) => {
    text += `${idx + 1}. [${b.category}] ${b.title} (${b.date})\n`;
  });

  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = `lakshya_notes_${new Date().toISOString().split('T')[0]}.txt`;
  a.click();
  showToast("నోట్స్ టెక్స్ట్ ఫైల్ డౌన్‌లోడ్ అయింది! 📄");
};

function updateNotesStudioBadges() {
  const bks = getSavedBookmarks();
  const notes = getPersonalNotes();

  const total = bks.length + notes.length;
  const headerBadge = document.getElementById("bookmarkBadgeCount");
  const tabBksCount = document.getElementById("tabBookmarksCount");
  const tabNotesCount = document.getElementById("tabMyNotesCount");

  if (headerBadge) headerBadge.textContent = total;
  if (tabBksCount) tabBksCount.textContent = bks.length;
  if (tabNotesCount) tabNotesCount.textContent = notes.length;
}

function renderBookmarksList() {
  const container = document.getElementById("bookmarksListContainer");
  const noMsg = document.getElementById("noBookmarksMsg");
  if (!container) return;

  const bks = getSavedBookmarks();
  if (bks.length === 0) {
    container.innerHTML = "";
    if (noMsg) noMsg.classList.remove("hidden");
    return;
  }
  if (noMsg) noMsg.classList.add("hidden");

  container.innerHTML = "";
  bks.forEach(item => {
    const row = document.createElement("div");
    row.className = "p-3.5 bg-slate-50 dark:bg-slate-800 rounded-xl border border-slate-200 dark:border-slate-700 flex justify-between items-start gap-3";
    row.innerHTML = `
      <div class="flex-1">
        <div class="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 mb-1">
          <span class="font-bold text-blue-600 dark:text-blue-400">📅 ${item.date}</span>
          <span class="bg-slate-200 dark:bg-slate-700 px-2 py-0.5 rounded font-semibold text-[11px]">${item.category}</span>
        </div>
        <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-slate-100 leading-snug">${item.title}</h4>
      </div>
      <button class="text-red-500 hover:text-red-700 p-1.5 rounded" onclick="toggleBookmark(${item.id})">
        <i data-lucide="trash" class="w-4 h-4"></i>
      </button>
    `;
    container.appendChild(row);
  });
  if (window.lucide) lucide.createIcons();
}

function renderPersonalNotesList() {
  const container = document.getElementById("personalNotesListContainer");
  if (!container) return;

  const notes = getPersonalNotes();
  if (notes.length === 0) {
    container.innerHTML = `
      <div class="text-center py-8 text-slate-400">
        <i data-lucide="file-text" class="w-8 h-8 mx-auto mb-2 opacity-60"></i>
        <p class="text-xs">ఇంకా ఏ సొంత నోట్స్ రాయలేదు. పైన ఉన్న ఫారంలో మీ నోట్ నమోదు చేయండి.</p>
      </div>
    `;
    if (window.lucide) lucide.createIcons();
    return;
  }

  container.innerHTML = "";
  notes.forEach(note => {
    const div = document.createElement("div");
    div.className = "note-item-card p-3.5 bg-white dark:bg-slate-850 rounded-xl border border-slate-200 dark:border-slate-700 space-y-2 shadow-2xs";
    div.innerHTML = `
      <div class="flex justify-between items-start gap-2">
        <div>
          <span class="text-[10px] font-black px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/50 text-indigo-800 dark:text-indigo-300">
            ${note.category}
          </span>
          <h4 class="text-xs sm:text-sm font-black text-slate-950 dark:text-slate-100 mt-1">${note.title}</h4>
        </div>
        <div class="flex items-center space-x-1 shrink-0">
          <button onclick="copyPersonalNote(${note.id})" class="text-slate-500 hover:text-indigo-600 p-1 rounded" title="కాపీ చేయండి">
            <i data-lucide="copy" class="w-3.5 h-3.5"></i>
          </button>
          <button onclick="deletePersonalNote(${note.id})" class="text-slate-400 hover:text-rose-600 p-1 rounded" title="తొలగించండి">
            <i data-lucide="trash-2" class="w-3.5 h-3.5"></i>
          </button>
        </div>
      </div>
      <p class="text-xs text-slate-700 dark:text-slate-300 whitespace-pre-line leading-relaxed">${note.content}</p>
      <div class="text-[10px] text-slate-400 text-right">📅 సేవ్ చేయబడినది: ${note.date}</div>
    `;
    container.appendChild(div);
  });
  if (window.lucide) lucide.createIcons();
}

function initBookmarks() {
  updateNotesStudioBadges();
  const openBtn = document.getElementById("openBookmarksBtn");
  const closeBtn = document.getElementById("closeBookmarksBtn");
  const modal = document.getElementById("bookmarksModal");
  const clearBtn = document.getElementById("clearBookmarksBtn");

  if (openBtn && modal) {
    openBtn.addEventListener("click", () => {
      renderBookmarksList();
      renderPersonalNotesList();
      modal.classList.remove("hidden");
    });
  }
  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => modal.classList.add("hidden"));
  }
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (confirm("అన్ని బుక్‌మార్క్ నోట్స్ మరియు సొంత నోట్స్ తొలగించాలా?")) {
        localStorage.removeItem("ca_bookmarks");
        localStorage.removeItem("ca_personal_notes");
        updateNotesStudioBadges();
        renderBookmarksList();
        renderPersonalNotesList();
        renderArticles();
        showToast("అన్ని బుక్‌మార్క్స్ & నోట్స్ క్లియర్ చేయబడ్డాయి.");
      }
    });
  }
}

// ==================== FEATURE: PERFORMANCE ANALYTICS & WEAKNESS HEATMAP ====================
function initAnalyticsAndStreak() {
  const todayStr = new Date().toISOString().split("T")[0];
  const lastActive = localStorage.getItem("ca_last_active");
  let streak = parseInt(localStorage.getItem("ca_streak") || "1", 10);

  if (lastActive) {
    const lastDate = new Date(lastActive);
    const currentDate = new Date(todayStr);
    const diffDays = Math.round((currentDate - lastDate) / (1000 * 60 * 60 * 24));

    if (diffDays === 1) {
      streak += 1;
    } else if (diffDays > 1) {
      streak = 1;
    }
  }
  localStorage.setItem("ca_last_active", todayStr);
  localStorage.setItem("ca_streak", streak.toString());

  const streakEl = document.getElementById("statStreak");
  if (streakEl) streakEl.textContent = `${streak} రోజులు 🔥`;

  const anStreak = document.getElementById("analyticsStreakDays");
  if (anStreak) anStreak.textContent = `${streak} రోజులు`;

  const openAnBtn = document.getElementById("openAnalyticsBtn");
  const closeAnBtn = document.getElementById("closeAnalyticsBtn");
  const modal = document.getElementById("analyticsModal");

  if (openAnBtn && modal) {
    openAnBtn.addEventListener("click", () => {
      renderAnalyticsDashboard();
      modal.classList.remove("hidden");
    });
  }
  if (closeAnBtn && modal) {
    closeAnBtn.addEventListener("click", () => modal.classList.add("hidden"));
  }
}

function renderAnalyticsDashboard() {
  const history = JSON.parse(localStorage.getItem("ca_cbt_history") || "[]");
  const streak = localStorage.getItem("ca_streak") || "1";

  const totalTestsEl = document.getElementById("analyticsTotalTests");
  const avgScoreEl = document.getElementById("analyticsAvgScore");
  const accEl = document.getElementById("analyticsAccuracy");
  const topScoreEl = document.getElementById("analyticsTopScore");
  const streakEl = document.getElementById("analyticsStreakDays");

  if (streakEl) streakEl.textContent = `${streak} రోజులు`;

  let totalTests = history.length;
  let avgScore = 0;
  let avgAccuracy = 0;
  let topScore = 0;

  if (totalTests > 0) {
    const sumScore = history.reduce((acc, h) => acc + (h.score || 0), 0);
    const sumAcc = history.reduce((acc, h) => acc + (h.accuracy || 0), 0);
    avgScore = (sumScore / totalTests).toFixed(1);
    avgAccuracy = Math.round(sumAcc / totalTests);
    topScore = Math.max(...history.map(h => h.score || 0)).toFixed(1);
  } else {
    // Default baseline for new students
    totalTests = 0;
    avgScore = "0.0";
    avgAccuracy = 0;
    topScore = "0.0";
  }

  if (totalTestsEl) totalTestsEl.textContent = totalTests;
  if (avgScoreEl) avgScoreEl.textContent = `${avgScore} / 50`;
  if (accEl) accEl.textContent = `${avgAccuracy}%`;
  if (topScoreEl) topScoreEl.textContent = topScore;

  // Level Title Logic
  const levelTitle = document.getElementById("analyticsLevelTitle");
  const levelSub = document.getElementById("analyticsLevelSub");
  if (levelTitle && levelSub) {
    if (avgScore >= 38) {
      levelTitle.textContent = "ర్యాంకర్ లెవెల్ ఆస్పిరెంట్ 🏆";
      levelSub.textContent = "అత్యుత్తమ మార్కులు! మెయిన్స్ & ఇంటర్వ్యూకి సిద్ధంగా ఉన్నారు.";
    } else if (avgScore >= 25) {
      levelTitle.textContent = "గ్రూప్-1 సూపర్ ఆస్పిరెంట్ ⭐";
      levelSub.textContent = "స్థిరమైన పురోగతి! నెగెటివ్ మార్కింగ్ నియంత్రణ బాగుంది.";
    } else {
      levelTitle.textContent = "లక్ష్య ఆస్పిరెంట్ (ప్రారంభ దశ) 🎯";
      levelSub.textContent = "రోజూ మాక్ టెస్టులు రాస్తూ వీక్ ఏరియాలను పునశ్చరణ చేయండి.";
    }
  }

  // Render Visual SVG Trend Chart
  renderScoreTrendChart(history);

  // Render Subject Mastery Bars & Weakness Heatmap
  renderSubjectMasteryAndHeatmap(avgAccuracy);
}

function renderScoreTrendChart(history) {
  const container = document.getElementById("analyticsTrendChartContainer");
  if (!container) return;

  const dataPoints = history.length > 0 ? history.slice(-5) : [
    { score: 20 }, { score: 25 }, { score: 32 }, { score: 38 }, { score: 42 }
  ];

  const maxVal = 50;
  const width = 360;
  const height = 75;
  const stepX = width / (dataPoints.length - 1 || 1);

  const points = dataPoints.map((d, i) => {
    const x = i * stepX;
    const y = height - ((d.score / maxVal) * (height - 15)) - 5;
    return `${x},${y}`;
  }).join(" ");

  let circles = "";
  dataPoints.forEach((d, i) => {
    const x = i * stepX;
    const y = height - ((d.score / maxVal) * (height - 15)) - 5;
    circles += `<circle cx="${x}" cy="${y}" r="4" fill="#2563eb" stroke="#ffffff" stroke-width="2"/>`;
    circles += `<text x="${x}" y="${y - 8}" font-size="10" font-weight="bold" fill="#1e40af" text-anchor="middle">${d.score}</text>`;
  });

  container.innerHTML = `
    <svg viewBox="0 0 ${width} ${height + 5}" class="w-full h-full overflow-visible">
      <defs>
        <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#3b82f6" stop-opacity="0.3"/>
          <stop offset="100%" stop-color="#3b82f6" stop-opacity="0.0"/>
        </linearGradient>
      </defs>
      <polygon points="0,${height} ${points} ${width},${height}" fill="url(#trendGrad)" />
      <polyline fill="none" stroke="#2563eb" stroke-width="2.5" points="${points}" />
      ${circles}
    </svg>
  `;
}

function renderSubjectMasteryAndHeatmap(overallAcc) {
  const subjects = [
    { name: "భారత రాజ్యాంగం & పాలిటీ", pct: Math.min(95, Math.max(55, overallAcc + 8)), cat: "national" },
    { name: "తెలంగాణ & ఏపీ సంక్షేమ పథకాలు", pct: Math.min(98, Math.max(60, overallAcc + 12)), cat: "regional" },
    { name: "భారత ఆర్థిక వ్యవస్థ & బడ్జెట్", pct: Math.max(42, overallAcc - 6), cat: "economy" },
    { name: "సైన్స్, టెక్నాలజీ & ఇస్రో", pct: Math.min(90, Math.max(48, overallAcc + 4)), cat: "science" },
    { name: "అంతర్జాతీయ సంబంధాలు & సదస్సులు", pct: Math.max(40, overallAcc - 10), cat: "international" },
    { name: "క్రీడలు & అవార్డులు", pct: Math.min(92, Math.max(50, overallAcc + 6)), cat: "sports" },
  ];

  // Subject Bars
  const barsContainer = document.getElementById("analyticsSubjectBars");
  if (barsContainer) {
    barsContainer.innerHTML = subjects.map(s => `
      <div>
        <div class="flex justify-between text-xs mb-1">
          <span class="text-slate-800 dark:text-slate-200">${s.name}</span>
          <span class="font-black ${s.pct >= 75 ? 'text-emerald-600' : s.pct >= 50 ? 'text-amber-600' : 'text-rose-600'}">${s.pct}%</span>
        </div>
        <div class="w-full bg-slate-200 dark:bg-slate-700 h-2 rounded-full overflow-hidden">
          <div class="h-full rounded-full transition-all duration-500 ${s.pct >= 75 ? 'bg-emerald-500' : s.pct >= 50 ? 'bg-amber-500' : 'bg-rose-500'}" style="width: ${s.pct}%"></div>
        </div>
      </div>
    `).join("");
  }

  // Weakness Heatmap Grid
  const heatmapContainer = document.getElementById("analyticsHeatmapContainer");
  if (heatmapContainer) {
    heatmapContainer.innerHTML = `
      <div class="p-3 rounded-xl border heatmap-strong space-y-1">
        <span class="font-black flex items-center gap-1">🟢 బలం (>70%):</span>
        <p class="text-[11px] leading-relaxed">సంక్షేమ పథకాలు, పాలిటీ, క్రీడలు. వీటిలో స్కోరు నిలకడగా ఉంది.</p>
      </div>
      <div class="p-3 rounded-xl border heatmap-moderate space-y-1">
        <span class="font-black flex items-center gap-1">🟡 మోడరేట్ (50-70%):</span>
        <p class="text-[11px] leading-relaxed">సైన్స్ & టెక్నాలజీ, జాతీయం. రివిజన్ ఫ్లాష్‌కార్డ్స్ ప్రాక్టీస్ చేయండి.</p>
      </div>
      <div class="p-3 rounded-xl border heatmap-weak space-y-1">
        <span class="font-black flex items-center gap-1">🔴 అత్యవసర ఫోకస్ (<50%):</span>
        <p class="text-[11px] leading-relaxed">ఆర్థిక వ్యవస్థ & బడ్జెట్ గణాంకాలు. నెగెటివ్ మార్కులను తగ్గించండి.</p>
      </div>
    `;
  }
}

// ==================== FEATURE: BOOKLETS (WEEKLY & MONTHLY) MODAL ====================
function initBookletsModal() {
  const openBtn = document.getElementById("openBookletsModalBtn");
  const closeBtn = document.getElementById("closeBookletsBtn");
  const modal = document.getElementById("bookletsModal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", () => {
      modal.classList.remove("hidden");
    });
  }
  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.add("hidden");
    });
  }
}

// ==================== FEATURE: ARTICLE DETAIL MODAL (FROM QUICK REVISION) ====================
function initArticleDetailModal() {
  const modal = document.getElementById("articleDetailModal");
  const closeBtn = document.getElementById("closeArticleDetailBtn");

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) modal.classList.add("hidden");
    });
  }
}

// Open Full Article Detail Modal
window.openArticleDetail = function(art) {
  if (!art) return;
  const modal = document.getElementById("articleDetailModal");
  if (!modal) return;

  const catInfo = CATEGORY_MAP[art.category] || { label: "🏛️ జాతీయం", class: "badge-national" };
  const catBadge = document.getElementById("modalCategoryBadge");
  if (catBadge) {
    catBadge.className = `text-xs font-bold px-2.5 py-1 rounded-md ${catInfo.class}`;
    catBadge.textContent = catInfo.label;
  }

  const srcBadge = document.getElementById("modalSourceBadge");
  if (srcBadge) {
    srcBadge.textContent = `📰 ${art.source ? art.source.split('(')[0].trim() : 'దినపత్రిక'}`;
  }

  const dateEl = document.getElementById("modalArticleDate");
  if (dateEl) dateEl.textContent = `📅 ${art.date || state.currentDate || ''}`;

  const titleEl = document.getElementById("modalArticleTitle");
  if (titleEl) titleEl.textContent = art.title || "కరెంట్ అఫైర్స్ ఆర్టికల్";

  const examTag = document.getElementById("modalExamTag");
  if (examTag) examTag.textContent = `🎯 ${art.exam_relevance || "APPSC / TSPSC / UPSC ప్రత్యేకం"}`;

  const summaryEl = document.getElementById("modalArticleSummary");
  if (summaryEl) summaryEl.textContent = art.summary || "";

  const notesEl = document.getElementById("modalArticleDetailedNotes");
  if (notesEl) {
    notesEl.innerHTML = formatDetailedNotes(art.detailed_notes || art.summary || "మరిన్ని సమగ్ర వివరాలు అందుబాటులో ఉన్నాయి.");
  }

  // Audio Playback Button
  const audioBtn = document.getElementById("modalAudioBtn");
  if (audioBtn) {
    audioBtn.onclick = () => {
      if (art.id) {
        playArticleAudio(art.id);
      } else {
        speakText(`${art.title}. ${art.summary}`);
      }
    };
  }

  // Bookmark Button
  const bmarkBtn = document.getElementById("modalBookmarkBtn");
  if (bmarkBtn) {
    const updateBmarkBtnUI = () => {
      const isB = art.id ? isBookmarked(art.id) : false;
      bmarkBtn.innerHTML = `<i data-lucide="${isB ? 'bookmark-check' : 'bookmark'}" class="w-3.5 h-3.5 ${isB ? 'text-amber-500' : ''}"></i><span>${isB ? 'సేవ్డ్' : 'సేవ్ చేయి'}</span>`;
      if (window.lucide) lucide.createIcons();
    };
    updateBmarkBtnUI();
    bmarkBtn.onclick = () => {
      if (art.id) {
        toggleBookmark(art.id, art.title, art.category, art.date || state.currentDate);
        updateBmarkBtnUI();
      } else {
        showToast("నోట్స్ సేవ్ చేయబడింది!");
      }
    };
  }

  // Go to Articles Tab
  const goToArticlesBtn = document.getElementById("modalGoToArticlesBtn");
  if (goToArticlesBtn) {
    goToArticlesBtn.onclick = () => {
      modal.classList.add("hidden");
      switchTab("articles");
      if (art.category) {
        state.currentCategory = art.category;
        catPills.forEach(p => {
          if (p.getAttribute("data-category") === art.category) {
            p.classList.add("active", "bg-blue-600", "text-white");
            p.classList.remove("bg-white", "text-slate-700");
          } else {
            p.classList.remove("active", "bg-blue-600", "text-white");
            p.classList.add("bg-white", "text-slate-700");
          }
        });
        loadArticles();
      }
    };
  }

  modal.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
};

// ==================== FEATURE: BROWSER DESKTOP PUSH NOTIFICATIONS ====================
function initWebNotifications() {
  const btn = document.getElementById("notificationToggleBtn");
  const text = document.getElementById("notifBtnText");
  if (!btn) return;

  const updateUI = () => {
    if (!("Notification" in window)) {
      btn.style.display = "none";
      return;
    }
    if (Notification.permission === "granted") {
      if (text) text.textContent = "అలర్ట్స్ ఆన్ ✅";
      btn.classList.add("bg-emerald-50", "text-emerald-700", "border-emerald-200");
      btn.classList.remove("bg-slate-100", "text-slate-700");
    } else if (Notification.permission === "denied") {
      if (text) text.textContent = "అలర్ట్స్ ఆఫ్ ❌";
    } else {
      if (text) text.textContent = "నోటిఫికేషన్లు 🔔";
    }
  };

  updateUI();

  btn.addEventListener("click", async () => {
    if (!("Notification" in window)) {
      alert("మీ బ్రౌజర్ డెస్క్‌టాప్ నోటిఫికేషన్లను సపోర్ట్ చేయదు.");
      return;
    }

    if (Notification.permission === "granted") {
      showToast("డైలీ మార్నింగ్ అలర్ట్స్ ఇప్పటికే యాక్టివ్‌గా ఉన్నాయి! 🔔");
      try {
        new Notification("లక్ష్య కరెంట్ అఫైర్స్", {
          body: "🌅 రోజూ ఉదయం తాజా కరెంట్ అఫైర్స్ & ప్రాక్టీస్ క్విజ్ సిద్ధం!",
          icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%232563eb'><path d='M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9'></path><path d='M13.73 21a2 2 0 0 1-3.46 0'></path></svg>"
        });
      } catch (e) {
        console.log(e);
      }
      return;
    }

    const permission = await Notification.requestPermission();
    if (permission === "granted") {
      updateUI();
      showToast("డైలీ మార్నింగ్ అలర్ట్స్ విజయవంతంగా ఎనేబుల్ అయ్యాయి! 🔔");
      try {
        new Notification("లక్ష్య కరెంట్ అఫైర్స్ 🌅", {
          body: "ధన్యవాదాలు! రోజూ ఉదయం 07:00 AM కు తాజా వార్తల నోటిఫికేషన్లు ఇక్కడ అందుతాయి.",
          icon: "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%232563eb'><path d='M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9'></path><path d='M13.73 21a2 2 0 0 1-3.46 0'></path></svg>"
        });
      } catch (e) {
        console.log(e);
      }
    } else {
      showToast("నోటిఫికేషన్ అనుమతి నిరాకరించబడింది.");
      updateUI();
    }
  });
}

// ==================== FEATURE 2: TARGET EXAM PERSONALIZATION ====================
function initTargetExam() {
  const saved = localStorage.getItem("target_exam") || "all";
  state.targetExam = saved;
  updateTargetExamUI(saved);
}

function updateTargetExamUI(examType) {
  const buttons = document.querySelectorAll("#examFilterButtons .exam-btn");
  buttons.forEach(btn => {
    if (btn.getAttribute("data-exam") === examType) {
      btn.classList.add("active", "bg-slate-900", "text-white", "shadow-2xs");
      btn.classList.remove("bg-slate-100", "text-slate-700");
    } else {
      btn.classList.remove("active", "bg-slate-900", "text-white", "shadow-2xs");
      btn.classList.add("bg-slate-100", "text-slate-700");
    }
  });
}

function setTargetExam(examType) {
  state.targetExam = examType;
  localStorage.setItem("target_exam", examType);
  updateTargetExamUI(examType);

  const examNames = {
    all: "మొత్తం పరీక్షలు",
    appsc: "APPSC (Group 1, 2)",
    tspsc: "TSPSC (Group 1, 2, 3)",
    police: "పోలీస్ SI / కానిస్టేబుల్",
    banking: "బ్యాంకింగ్ / SSC / RRB",
    upsc: "UPSC సివిల్స్"
  };

  showToast(`🎯 లక్ష్య పరీక్ష ఎంపికైంది: ${examNames[examType] || examType}`);

  if (state.currentTab === "articles") {
    renderArticles();
  } else if (state.currentTab === "flashcards") {
    loadFlashcards();
  }
}

// ==================== FEATURE 1: 3D REVISION FLASHCARDS ====================
function initFlashcards() {
  // Setup keyboard shortcuts
  window.addEventListener("keydown", (e) => {
    if (state.currentTab !== "flashcards") return;
    if (e.code === "Space") {
      e.preventDefault();
      flipCurrentFlashcard();
    } else if (e.code === "ArrowRight") {
      nextFlashcard();
    } else if (e.code === "ArrowLeft") {
      prevFlashcard();
    }
  });
}

async function loadFlashcards() {
  const countEl = document.getElementById("tabCountFlashcards");
  try {
    const url = `${API_BASE}/api/flashcards?category=${state.fcCategory}&exam=${state.targetExam}&date=${state.currentDate || ''}`;
    const res = await fetch(url);
    const data = await res.json();
    if (data.success) {
      state.flashcards = data.data || [];
      state.filteredFlashcards = state.flashcards;
      state.currentFcIndex = 0;
      state.isFcFlipped = false;
      if (countEl) countEl.textContent = state.flashcards.length;
      renderCurrentFlashcard();
    }
  } catch (err) {
    console.error("Error loading flashcards:", err);
  }
}

function renderCurrentFlashcard() {
  const cardInner = document.getElementById("flashcardInner");
  const frontTitle = document.getElementById("fcFrontTitle");
  const frontCategory = document.getElementById("fcFrontCategory");
  const frontExamTag = document.getElementById("fcFrontExamTag");
  const frontDate = document.getElementById("fcFrontDate");
  const backSummary = document.getElementById("fcBackSummary");
  const backDetails = document.getElementById("fcBackDetails");
  const backSource = document.getElementById("fcBackSource");
  const currentIndexEl = document.getElementById("fcCurrentIndex");
  const totalCardsEl = document.getElementById("fcTotalCards");
  const masteredCountEl = document.getElementById("fcMasteredCount");
  const reviewCountEl = document.getElementById("fcReviewCount");

  if (masteredCountEl) masteredCountEl.textContent = state.fcMastered.length;
  if (reviewCountEl) reviewCountEl.textContent = state.fcReview.length;

  if (!state.filteredFlashcards || state.filteredFlashcards.length === 0) {
    if (frontTitle) frontTitle.textContent = "ఈ విభాగానికి లేదా లక్ష్య పరీక్షకు ఫ్లాష్‌కార్డ్స్ లేవు. పైన 'అన్నీ' ఎంచుకోండి.";
    if (currentIndexEl) currentIndexEl.textContent = "0";
    if (totalCardsEl) totalCardsEl.textContent = "0";
    if (cardInner) cardInner.classList.remove("is-flipped");
    return;
  }

  if (state.currentFcIndex >= state.filteredFlashcards.length) {
    state.currentFcIndex = 0;
  }

  const card = state.filteredFlashcards[state.currentFcIndex];
  if (currentIndexEl) currentIndexEl.textContent = state.currentFcIndex + 1;
  if (totalCardsEl) totalCardsEl.textContent = state.filteredFlashcards.length;

  const catInfo = CATEGORY_MAP[card.category] || { label: "🏛️ జాతీయం" };
  if (frontCategory) frontCategory.textContent = catInfo.label;
  if (frontExamTag) frontExamTag.textContent = `🎯 ${card.exam_tags || "APPSC / TSPSC"}`;
  if (frontDate) frontDate.textContent = `📅 ${card.date || state.currentDate || ""}`;
  if (frontTitle) frontTitle.textContent = card.front;

  if (backSummary) backSummary.textContent = card.back_summary;
  if (backDetails) backDetails.textContent = card.back_details || "పరీక్షల పునశ్చరణ కోసం ఉపయోగపడుతుంది.";
  if (backSource) backSource.textContent = `మూలం: ${card.source || "దినపత్రిక"}`;

  if (cardInner) {
    if (state.isFcFlipped) {
      cardInner.classList.add("is-flipped");
    } else {
      cardInner.classList.remove("is-flipped");
    }
  }

  if (window.lucide) lucide.createIcons();
}

function flipCurrentFlashcard() {
  state.isFcFlipped = !state.isFcFlipped;
  const cardInner = document.getElementById("flashcardInner");
  if (cardInner) {
    cardInner.classList.toggle("is-flipped", state.isFcFlipped);
  }
}

function nextFlashcard() {
  if (state.filteredFlashcards.length === 0) return;
  if (state.currentFcIndex < state.filteredFlashcards.length - 1) {
    state.currentFcIndex++;
  } else {
    state.currentFcIndex = 0;
    showToast("చివరి కార్డ్ పూర్తయింది! మొదటి కార్డ్‌కు చేరుకున్నాం.");
  }
  state.isFcFlipped = false;
  renderCurrentFlashcard();
}

function prevFlashcard() {
  if (state.filteredFlashcards.length === 0) return;
  if (state.currentFcIndex > 0) {
    state.currentFcIndex--;
  } else {
    state.currentFcIndex = state.filteredFlashcards.length - 1;
  }
  state.isFcFlipped = false;
  renderCurrentFlashcard();
}

function markFlashcardMastered() {
  if (state.filteredFlashcards.length === 0) return;
  const card = state.filteredFlashcards[state.currentFcIndex];
  if (!state.fcMastered.includes(card.id)) {
    state.fcMastered.push(card.id);
    localStorage.setItem("fc_mastered", JSON.stringify(state.fcMastered));
  }
  state.fcReview = state.fcReview.filter(id => id !== card.id);
  localStorage.setItem("fc_review", JSON.stringify(state.fcReview));

  showToast("గుర్తుంది! నేర్చుకున్న జాబితాలో చేర్చబడింది ✅");
  nextFlashcard();
}

function markFlashcardReview() {
  if (state.filteredFlashcards.length === 0) return;
  const card = state.filteredFlashcards[state.currentFcIndex];
  if (!state.fcReview.includes(card.id)) {
    state.fcReview.push(card.id);
    localStorage.setItem("fc_review", JSON.stringify(state.fcReview));
  }
  state.fcMastered = state.fcMastered.filter(id => id !== card.id);
  localStorage.setItem("fc_mastered", JSON.stringify(state.fcMastered));

  showToast("మళ్ళీ రివిజన్ చేయాల్సిన లిస్ట్‌లో చేర్చబడింది ❌");
  nextFlashcard();
}

function filterFlashcards(category) {
  state.fcCategory = category;
  const pills = document.querySelectorAll(".fc-filter-pill");
  pills.forEach(p => {
    p.classList.remove("active", "bg-amber-500", "text-white", "shadow-2xs");
    p.classList.add("bg-slate-100", "text-slate-700");
  });
  if (window.event && window.event.target) {
    window.event.target.classList.add("active", "bg-amber-500", "text-white", "shadow-2xs");
    window.event.target.classList.remove("bg-slate-100", "text-slate-700");
  }

  if (category === "all") {
    state.filteredFlashcards = state.flashcards;
  } else {
    state.filteredFlashcards = state.flashcards.filter(c => c.category === category);
  }
  state.currentFcIndex = 0;
  state.isFcFlipped = false;
  renderCurrentFlashcard();
}

function playFlashcardAudio() {
  if (state.filteredFlashcards.length === 0) return;
  const card = state.filteredFlashcards[state.currentFcIndex];
  const text = card.audio_text || `${card.front}. ${card.back_summary}. ${card.back_details || ''}`;
  playNativeAudio(text);
}

// ==================== FEATURE 3: MONTHLY STUDY CALENDAR MODAL ====================
let calendarViewYear = 2026;
let calendarViewMonth = 8; // 0-indexed (8 = September)

const TELUGU_MONTH_NAMES = [
  "జనవరి", "ఫిబ్రవరి", "మార్చి", "ఏప్రిల్", "మే", "జూన్",
  "జూలై", "ఆగస్టు", "సెప్టెంబర్", "అక్టోబర్", "నవంబర్", "డిసెంబర్"
];

function initStudyCalendarModal() {
  const openBtn = document.getElementById("openCalendarBtn");
  const closeBtn = document.getElementById("closeCalendarBtn");
  const modal = document.getElementById("studyCalendarModal");

  if (openBtn) {
    openBtn.addEventListener("click", () => {
      openStudyCalendar();
    });
  }
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      closeStudyCalendar();
    });
  }
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeStudyCalendar();
    });
  }

  // Parse current date to set calendar view
  if (state.currentDate) {
    const parts = state.currentDate.split("-");
    if (parts.length === 3) {
      calendarViewYear = parseInt(parts[0], 10);
      calendarViewMonth = parseInt(parts[1], 10) - 1;
    }
  }
}

function openStudyCalendar() {
  const modal = document.getElementById("studyCalendarModal");
  if (!modal) return;
  renderStudyCalendar();
  modal.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closeStudyCalendar() {
  const modal = document.getElementById("studyCalendarModal");
  if (modal) modal.classList.add("hidden");
}

function changeCalendarMonth(delta) {
  calendarViewMonth += delta;
  if (calendarViewMonth < 0) {
    calendarViewMonth = 11;
    calendarViewYear--;
  } else if (calendarViewMonth > 11) {
    calendarViewMonth = 0;
    calendarViewYear++;
  }
  renderStudyCalendar();
}

function renderStudyCalendar() {
  const titleEl = document.getElementById("calendarMonthTitle");
  const gridEl = document.getElementById("calendarDaysGrid");
  const streakTextEl = document.getElementById("calendarStreakText");

  if (titleEl) {
    titleEl.textContent = `${TELUGU_MONTH_NAMES[calendarViewMonth]} ${calendarViewYear}`;
  }

  // Get available dates from dateSelect options
  const availableSet = new Set();
  if (dateSelect) {
    for (let opt of dateSelect.options) {
      availableSet.add(opt.value);
    }
  }

  // Days in month
  const firstDayOfWeek = new Date(calendarViewYear, calendarViewMonth, 1).getDay(); // 0 = Sunday
  const daysInMonth = new Date(calendarViewYear, calendarViewMonth + 1, 0).getDate();

  gridEl.innerHTML = "";

  // Empty cells before first day
  for (let i = 0; i < firstDayOfWeek; i++) {
    const emptyCell = document.createElement("div");
    emptyCell.className = "py-2.5 text-slate-300 font-normal";
    gridEl.appendChild(emptyCell);
  }

  // Days 1..daysInMonth
  for (let day = 1; day <= daysInMonth; day++) {
    const monthStr = String(calendarViewMonth + 1).padStart(2, "0");
    const dayStr = String(day).padStart(2, "0");
    const dateStr = `${calendarViewYear}-${monthStr}-${dayStr}`;

    const cell = document.createElement("button");
    const isSelected = dateStr === state.currentDate;
    const hasData = availableSet.has(dateStr);

    let baseClass = "p-2 rounded-xl text-center transition flex flex-col items-center justify-center relative ";

    if (isSelected) {
      baseClass += "bg-blue-600 text-white font-extrabold shadow-md ring-2 ring-blue-400";
    } else if (hasData) {
      baseClass += "bg-emerald-50 hover:bg-emerald-100 text-emerald-900 border border-emerald-300 font-bold";
    } else {
      baseClass += "hover:bg-slate-100 text-slate-700 font-medium";
    }

    cell.className = baseClass;
    cell.innerHTML = `
      <span class="text-sm">${day}</span>
      ${hasData && !isSelected ? `<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 mt-0.5"></span>` : ''}
    `;

    cell.addEventListener("click", async () => {
      if (hasData) {
        state.currentDate = dateStr;
        if (dateSelect) dateSelect.value = dateStr;
        const printDateEl = document.getElementById("printDate");
        if (printDateEl) printDateEl.textContent = `తేదీ: ${state.currentDate}`;
        closeStudyCalendar();
        await refreshCurrentView();
        if (state.currentTab === "flashcards") loadFlashcards();
        showToast(`📅 ${dateStr} నాటి కరెంట్ అఫైర్స్ లోడ్ చేయబడ్డాయి!`);
      } else {
        showToast(`ఈ తేదీకి (${dateStr}) వార్తలు ఇంకా అందుబాటులో లేవు.`);
      }
    });

    gridEl.appendChild(cell);
  }

  if (streakTextEl) {
    const streak = localStorage.getItem("ca_streak_count") || "1";
    streakTextEl.textContent = `${streak} రోజులు 🔥`;
  }
}

// ==================== FEATURE: PWA ONE-CLICK APP INSTALL ====================
let deferredInstallPrompt = null;

function initPwaInstall() {
  const installBtn = document.getElementById("installAppBtn");
  
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredInstallPrompt = e;
    if (installBtn) {
      installBtn.classList.remove("hidden");
      installBtn.classList.add("animate-pulse");
    }
  });

  if (installBtn) {
    installBtn.addEventListener("click", async () => {
      if (deferredInstallPrompt) {
        deferredInstallPrompt.prompt();
        const { outcome } = await deferredInstallPrompt.userChoice;
        if (outcome === "accepted") {
          showToast("యాప్ విజయవంతంగా ఇన్‌స్టాల్ చేయబడింది! 📲");
        }
        deferredInstallPrompt = null;
      } else {
        alert("యాప్‌ను ఇన్‌స్టాల్ చేయడానికి:\n• క్రోమ్ బ్రౌజర్ కుడివైపు మెనూ (⋮) పై క్లిక్ చేయండి.\n• 'Install App' లేదా 'Add to Home Screen' ఎంచుకోండి.");
      }
    });
  }

  window.addEventListener("appinstalled", () => {
    showToast("లక్ష్య కరెంట్ అఫైర్స్ యాప్ ఇన్‌స్టాలేషన్ పూర్తయింది! 🎉");
    if (installBtn) installBtn.style.display = "none";
  });
}

// ==================== FEATURE: PERSISTENT AUDIO PODCAST PLAYER ====================
let podcastAudio = null;
let currentPodcastIndex = 0;
let podcastPlaylist = [];
let currentPodcastSpeed = 1.0;

function initPodcastPlayer() {
  podcastAudio = document.getElementById("persistentAudioElement");
  if (!podcastAudio) return;

  podcastAudio.addEventListener("ended", () => {
    if (podcastPlaylist.length > 0 && currentPodcastIndex < podcastPlaylist.length - 1) {
      currentPodcastIndex++;
      playPodcastIndex(currentPodcastIndex);
    } else {
      updatePodcastPlayIcon(false);
    }
  });

  podcastAudio.addEventListener("play", () => updatePodcastPlayIcon(true));
  podcastAudio.addEventListener("pause", () => updatePodcastPlayIcon(false));
}

function startPodcastWithArticle(article) {
  const bar = document.getElementById("podcastPlayerBar");
  if (!bar || !podcastAudio) return;

  podcastPlaylist = state.articles.length > 0 ? state.articles : [article];
  const idx = podcastPlaylist.findIndex(a => a.id === article.id);
  currentPodcastIndex = idx !== -1 ? idx : 0;

  playPodcastIndex(currentPodcastIndex);
  bar.classList.remove("hidden-bar");
  if (window.lucide) lucide.createIcons();
}

function playPodcastIndex(index) {
  if (index < 0 || index >= podcastPlaylist.length) return;
  const art = podcastPlaylist[index];
  const titleEl = document.getElementById("podcastCurrentTrackTitle");
  if (titleEl) titleEl.textContent = art.title;

  const url = `${API_BASE}/api/audio/article/${art.id}`;
  podcastAudio.src = url;
  podcastAudio.playbackRate = currentPodcastSpeed;
  podcastAudio.play().catch(e => console.log("Audio play error:", e));
}

function togglePodcastPlayback() {
  if (!podcastAudio) return;
  if (podcastAudio.paused) {
    if (!podcastAudio.src && state.articles.length > 0) {
      startPodcastWithArticle(state.articles[0]);
    } else {
      podcastAudio.play().catch(e => console.log(e));
    }
  } else {
    podcastAudio.pause();
  }
}

function updatePodcastPlayIcon(isPlaying) {
  const icon = document.getElementById("podcastPlayIcon");
  const wave = document.getElementById("podcastAudioWave");
  if (icon) {
    icon.setAttribute("data-lucide", isPlaying ? "pause" : "play");
    if (window.lucide) lucide.createIcons();
  }
  if (wave) {
    wave.style.opacity = isPlaying ? "1" : "0.3";
  }
}

function skipPodcastTime(seconds) {
  if (!podcastAudio) return;
  podcastAudio.currentTime = Math.max(0, podcastAudio.currentTime + seconds);
}

function cyclePodcastSpeed() {
  if (!podcastAudio) return;
  const speeds = [1.0, 1.25, 1.5, 2.0];
  let curIdx = speeds.indexOf(currentPodcastSpeed);
  currentPodcastSpeed = speeds[(curIdx + 1) % speeds.length];
  podcastAudio.playbackRate = currentPodcastSpeed;
  const textEl = document.getElementById("podcastSpeedText");
  if (textEl) textEl.textContent = `${currentPodcastSpeed}x`;
  showToast(`ఆడియో వేగం: ${currentPodcastSpeed}x కి మార్చబడింది`);
}

function closePodcastBar() {
  if (podcastAudio) podcastAudio.pause();
  const bar = document.getElementById("podcastPlayerBar");
  if (bar) bar.classList.add("hidden-bar");
}

// Override playArticleAudio so clicking on any article starts podcast player
function playArticleAudio(articleId) {
  const art = state.articles.find(a => a.id === articleId);
  if (art) {
    startPodcastWithArticle(art);
  } else {
    playNativeAudioById(articleId);
  }
}

// // ==================== FEATURE: LIVE TIMED CBT EXAM MODE & APPSC GROUP-2 ====================
let cbtQuestions = [];
let cbtCurrentIndex = 0;
let cbtUserAnswers = {};
let cbtMarkedForReview = new Set();
let cbtTimerInterval = null;
let cbtSecondsRemaining = 45 * 60;
let cbtExamMode = "standard"; // "standard", "full", "pyqs", "quick", "section"
let cbtExamSectionId = null;
let cbtActiveSectionFilter = "all";

function initCbtExam() {
  const openBtn = document.getElementById("openCbtExamBtn");
  const exitBtn = document.getElementById("cbtExitBtn");
  const submitBtn = document.getElementById("cbtSubmitBtn");
  const prevBtn = document.getElementById("cbtPrevBtn");
  const clearBtn = document.getElementById("cbtClearBtn");
  const markReviewBtn = document.getElementById("cbtMarkReviewBtn");
  const saveNextBtn = document.getElementById("cbtSaveNextBtn");
  const retakeBtn = document.getElementById("cbtRetakeBtn");

  if (openBtn) openBtn.addEventListener("click", openCbtExamModal);
  if (exitBtn) exitBtn.addEventListener("click", confirmExitCbt);
  if (submitBtn) submitBtn.addEventListener("click", confirmSubmitCbt);
  if (prevBtn) prevBtn.addEventListener("click", prevCbtQuestion);
  if (clearBtn) clearBtn.addEventListener("click", clearCbtAnswer);
  if (markReviewBtn) markReviewBtn.addEventListener("click", markForReviewAndNext);
  if (saveNextBtn) saveNextBtn.addEventListener("click", saveAndNextCbt);
  if (retakeBtn) retakeBtn.addEventListener("click", restartCbtExam);
}

// ==================== APPSC GROUP-2 EXAM HUB INTEGRATION ====================
function initAppscGroup2Hub() {
  const openBtn = document.getElementById("openAppscGroup2Btn");
  const closeBtn = document.getElementById("closeAppscGroup2Btn");
  const modal = document.getElementById("appscGroup2Modal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", () => {
      modal.classList.remove("hidden");
      if (window.lucide) lucide.createIcons();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  // 150 Qs Full Grand Test
  const fullMockBtn = document.getElementById("startAppscFullMockBtn");
  if (fullMockBtn) {
    fullMockBtn.addEventListener("click", () => startAppscExam("full"));
  }

  // Authentic PYQs Test
  const pyqsBtn = document.getElementById("startAppscPyqsBtn");
  if (pyqsBtn) {
    pyqsBtn.addEventListener("click", () => startAppscExam("pyqs"));
  }

  // 50 Qs Mini Grand Test
  const quickBtn = document.getElementById("startAppscQuickBtn");
  if (quickBtn) {
    quickBtn.addEventListener("click", () => startAppscExam("quick"));
  }

  // Section-wise Practice Buttons
  const secButtons = document.querySelectorAll(".appsc-sec-btn");
  secButtons.forEach(btn => {
    btn.addEventListener("click", () => {
      const sec = btn.getAttribute("data-sec");
      startAppscExam("section", sec);
    });
  });
}

async function startAppscExam(mode = "full", sectionId = null) {
  const hubModal = document.getElementById("appscGroup2Modal");
  if (hubModal) hubModal.classList.add("hidden");
  const historyModal = document.getElementById("apHistoryModal");
  if (historyModal) historyModal.classList.add("hidden");

  cbtExamMode = mode;
  cbtExamSectionId = sectionId;
  cbtActiveSectionFilter = "all";

  let url = `${API_BASE}/api/appsc_group2/questions?mode=${mode}`;
  if (mode === "group1" || mode === "group2" || mode === "group3") {
    url = `${API_BASE}/api/appsc_exams?exam=${mode}`;
  } else if (mode === "section" && sectionId) {
    url += `&section=${encodeURIComponent(sectionId)}`;
  }

  try {
    const res = await fetch(url);
    const data = await res.json();
    if (data.success && data.questions && data.questions.length > 0) {
      cbtQuestions = data.questions;
      cbtCurrentIndex = 0;
      cbtUserAnswers = {};
      cbtMarkedForReview = new Set();
      const durMinutes = data.info?.duration_minutes || data.duration_minutes || (mode === "group1" ? 120 : 150);
      cbtSecondsRemaining = durMinutes * 60;

      const headerTitle = document.getElementById("cbtExamHeaderTitle");
      const headerSub = document.getElementById("cbtExamHeaderSubtitle");
      const examTitle = data.info?.title || data.title || "APPSC గ్రాండ్ మాక్ టెస్ట్";
      if (headerTitle) headerTitle.textContent = examTitle;
      if (headerSub) headerSub.textContent = `మొత్తం ${cbtQuestions.length} ప్రశ్నలు (${durMinutes} నిమిషాలు) • APPSC నెగటివ్ మార్కింగ్ (-0.33)`;

      // Setup Section Navigation
      setupSectionNavTabs(data);

      const modal = document.getElementById("cbtExamModal");
      if (modal) modal.classList.remove("hidden");

      startCbtTimer();
      renderCbtPalette();
      renderCbtQuestion();
      if (window.lucide) lucide.createIcons();
    } else {
      showToast("ప్రశ్నలు లోడ్ చేయడంలో సమస్య ఏర్పడింది.");
    }
  } catch (err) {
    console.error("Error loading APPSC exam:", err);
    showToast("టెస్ట్ లోడ్ చేయడంలో సమస్య ఏర్పడింది.");
  }
}

function setupSectionNavTabs(data) {
  const nav = document.getElementById("cbtSectionNav");
  if (!nav) return;

  if (data.mode === "section") {
    nav.classList.add("hidden");
    return;
  }

  nav.classList.remove("hidden");
  const allCountEl = document.getElementById("cbtSecCountAll");
  if (allCountEl) allCountEl.textContent = data.total || cbtQuestions.length;

  const tabs = nav.querySelectorAll(".cbt-sec-tab");
  tabs.forEach(tab => {
    // Reset styling
    tab.className = "cbt-sec-tab px-3 py-1.5 rounded-xl font-extrabold transition bg-slate-700/70 hover:bg-slate-700 text-slate-300";
    if (tab.getAttribute("data-section") === "all") {
      tab.className = "cbt-sec-tab px-3 py-1.5 rounded-xl font-extrabold transition bg-blue-600 text-white shadow-xs";
    }

    tab.onclick = () => {
      tabs.forEach(t => {
        t.className = "cbt-sec-tab px-3 py-1.5 rounded-xl font-extrabold transition bg-slate-700/70 hover:bg-slate-700 text-slate-300";
      });
      tab.className = "cbt-sec-tab px-3 py-1.5 rounded-xl font-extrabold transition bg-blue-600 text-white shadow-xs";

      const sec = tab.getAttribute("data-section");
      cbtActiveSectionFilter = sec;

      if (sec !== "all") {
        const firstIdx = cbtQuestions.findIndex(q => q.section_id === sec);
        if (firstIdx !== -1) {
          cbtCurrentIndex = firstIdx;
        }
      }
      renderCbtPalette();
      renderCbtQuestion();
    };
  });
}

async function openCbtExamModal() {
  const modal = document.getElementById("cbtExamModal");
  if (!modal) return;

  cbtExamMode = "standard";
  cbtExamSectionId = null;
  cbtActiveSectionFilter = "all";

  try {
    const res = await fetch(`${API_BASE}/api/cbt_questions`);
    const data = await res.json();
    if (data.success && data.questions.length > 0) {
      cbtQuestions = data.questions;
      cbtCurrentIndex = 0;
      cbtUserAnswers = {};
      cbtMarkedForReview = new Set();
      cbtSecondsRemaining = (data.duration_minutes || 45) * 60;

      const headerTitle = document.getElementById("cbtExamHeaderTitle");
      const headerSub = document.getElementById("cbtExamHeaderSubtitle");
      if (headerTitle) headerTitle.textContent = "గ్రాండ్ మాక్ టెస్ట్ • ఆన్‌లైన్ CBT ఎగ్జామ్ (50 ప్రశ్నలు)";
      if (headerSub) headerSub.textContent = "APPSC & TSPSC నెగటివ్ మార్కింగ్ విధానం (-0.33 మార్కులు)";

      const nav = document.getElementById("cbtSectionNav");
      if (nav) nav.classList.add("hidden");

      modal.classList.remove("hidden");
      startCbtTimer();
      renderCbtPalette();
      renderCbtQuestion();
      if (window.lucide) lucide.createIcons();
    }
  } catch (err) {
    console.error("Error loading CBT questions:", err);
    showToast("CBT ప్రశ్నలు లోడ్ చేయడంలో సమస్య ఏర్పడింది.");
  }
}

function startCbtTimer() {
  clearInterval(cbtTimerInterval);
  updateTimerDisplay();

  cbtTimerInterval = setInterval(() => {
    cbtSecondsRemaining--;
    updateTimerDisplay();

    if (cbtSecondsRemaining <= 0) {
      clearInterval(cbtTimerInterval);
      alert("సమయం ముగిసింది! మీ పరీక్ష ఆటోమేటిక్‌గా సబ్మిట్ అవుతోంది.");
      submitCbtExam();
    }
  }, 1000);
}

function updateTimerDisplay() {
  const display = document.getElementById("cbtTimerDisplay");
  if (!display) return;

  const mins = Math.floor(cbtSecondsRemaining / 60);
  const secs = cbtSecondsRemaining % 60;
  display.textContent = `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;

  if (cbtSecondsRemaining <= 300) {
    display.classList.add("text-rose-400", "animate-pulse");
    display.classList.remove("text-amber-400");
  } else {
    display.classList.remove("text-rose-400", "animate-pulse");
    display.classList.add("text-amber-400");
  }
}

function renderCbtQuestion() {
  if (cbtQuestions.length === 0) return;
  const q = cbtQuestions[cbtCurrentIndex];

  const currentQNum = document.getElementById("cbtCurrentQNum");
  const totalQs = document.getElementById("cbtTotalQs");
  const categoryTag = document.getElementById("cbtCategoryTag");
  const questionTitle = document.getElementById("cbtQuestionTitle");
  const pyqBadge = document.getElementById("cbtPyqBadge");

  if (currentQNum) currentQNum.textContent = cbtCurrentIndex + 1;
  if (totalQs) totalQs.textContent = cbtQuestions.length;
  if (categoryTag) categoryTag.textContent = q.section_name || q.category || "జనరల్ స్టడీస్";
  if (questionTitle) questionTitle.textContent = `${cbtCurrentIndex + 1}. ${q.question}`;

  if (pyqBadge) {
    if (q.is_pyq) {
      pyqBadge.textContent = `★ APPSC గ్రూప్-2 ${q.pyq_year || ''} PYQ`;
      pyqBadge.classList.remove("hidden");
    } else {
      pyqBadge.classList.add("hidden");
    }
  }

  const container = document.getElementById("cbtOptionsList");
  if (!container) return;
  container.innerHTML = "";

  const options = [
    { key: "A", text: q.option_a },
    { key: "B", text: q.option_b },
    { key: "C", text: q.option_c },
    { key: "D", text: q.option_d }
  ];

  const selectedAnswer = cbtUserAnswers[cbtCurrentIndex];

  options.forEach(opt => {
    const isSelected = selectedAnswer === opt.key;
    const div = document.createElement("div");
    div.className = `cbt-option flex items-center space-x-3 text-xs sm:text-sm font-semibold ${isSelected ? 'selected' : ''}`;
    div.innerHTML = `
      <div class="w-6 h-6 rounded-full border-2 ${isSelected ? 'border-blue-600 bg-blue-600 text-white' : 'border-slate-300 dark:border-slate-600'} flex items-center justify-center font-bold shrink-0">
        ${opt.key}
      </div>
      <div class="flex-1 text-slate-800 dark:text-slate-100">${opt.text}</div>
    `;
    div.addEventListener("click", () => {
      cbtUserAnswers[cbtCurrentIndex] = opt.key;
      cbtMarkedForReview.delete(cbtCurrentIndex);
      renderCbtQuestion();
      updateCbtPaletteButton(cbtCurrentIndex);
      updateCbtLegends();
    });
    container.appendChild(div);
  });

  updateCbtPaletteButton(cbtCurrentIndex);
  updateCbtLegends();
}

function renderCbtPalette() {
  const container = document.getElementById("cbtPaletteContainer");
  if (!container) return;
  container.innerHTML = "";

  cbtQuestions.forEach((q, idx) => {
    // Filter by section if selected
    if (cbtActiveSectionFilter !== "all" && q.section_id !== cbtActiveSectionFilter) {
      return;
    }

    const btn = document.createElement("button");
    btn.id = `cbt-p-${idx}`;
    btn.className = "palette-btn";
    btn.textContent = idx + 1;
    btn.title = `ప్రశ్న ${idx + 1}: ${q.section_name || q.category || ''}`;
    btn.addEventListener("click", () => {
      cbtCurrentIndex = idx;
      renderCbtQuestion();
    });
    container.appendChild(btn);
  });

  updateCbtPaletteButton(cbtCurrentIndex);
}

function updateCbtPaletteButton(idx) {
  const btn = document.getElementById(`cbt-p-${idx}`);
  if (!btn) return;

  btn.classList.remove("current", "answered", "unanswered", "marked");

  if (idx === cbtCurrentIndex) {
    btn.classList.add("current");
  }

  if (cbtMarkedForReview.has(idx)) {
    btn.classList.add("marked");
  } else if (cbtUserAnswers[idx]) {
    btn.classList.add("answered");
  } else {
    btn.classList.add("unanswered");
  }
}

function updateCbtLegends() {
  let answered = 0;
  let marked = cbtMarkedForReview.size;

  Object.keys(cbtUserAnswers).forEach(k => {
    if (!cbtMarkedForReview.has(parseInt(k, 10))) answered++;
  });

  const unanswered = cbtQuestions.length - (answered + marked);

  const elA = document.getElementById("cbtLegendAnswered");
  const elU = document.getElementById("cbtLegendUnanswered");
  const elM = document.getElementById("cbtLegendMarked");

  if (elA) elA.textContent = answered;
  if (elU) elU.textContent = Math.max(0, unanswered);
  if (elM) elM.textContent = marked;
}

function saveAndNextCbt() {
  if (cbtCurrentIndex < cbtQuestions.length - 1) {
    cbtCurrentIndex++;
    renderCbtQuestion();
  } else {
    showToast("చివరి ప్రశ్న చేరుకున్నారు! టెస్ట్ ముగించడానికి 'టెస్ట్ ముగించు' క్లిక్ చేయండి.");
  }
}

function prevCbtQuestion() {
  if (cbtCurrentIndex > 0) {
    cbtCurrentIndex--;
    renderCbtQuestion();
  }
}

function clearCbtAnswer() {
  delete cbtUserAnswers[cbtCurrentIndex];
  cbtMarkedForReview.delete(cbtCurrentIndex);
  renderCbtQuestion();
  showToast("ఈ ప్రశ్నకు ఎంపిక తొలగించబడింది.");
}

function markForReviewAndNext() {
  cbtMarkedForReview.add(cbtCurrentIndex);
  saveAndNextCbt();
}

function confirmSubmitCbt() {
  const answeredCount = Object.keys(cbtUserAnswers).length;
  const unansweredCount = cbtQuestions.length - answeredCount;
  const markedCount = cbtMarkedForReview.size;

  const msg = `పరీక్షను సబ్మిట్ చేయాలనుకుంటున్నారా?\n\n• సమాధానం ఇచ్చినవి: ${answeredCount}\n• ఇవ్వనివి: ${unansweredCount}\n• మార్క్ ఫర్ రివ్యూ: ${markedCount}`;
  if (confirm(msg)) {
    submitCbtExam();
  }
}

function confirmExitCbt() {
  if (confirm("మీరు ఎగ్జామ్ నుండి మధ్యలోనే నిష్క్రమించాలనుకుంటున్నారా? ప్రస్తుతం ఇచ్చిన సమాధానాలు సేవ్ కావు.")) {
    clearInterval(cbtTimerInterval);
    document.getElementById("cbtExamModal").classList.add("hidden");
  }
}

function submitCbtExam() {
  clearInterval(cbtTimerInterval);
  document.getElementById("cbtExamModal").classList.add("hidden");

  let correct = 0;
  let wrong = 0;
  let skipped = 0;

  const reviewList = [];
  const sectionStats = {};

  cbtQuestions.forEach((q, idx) => {
    const userAns = cbtUserAnswers[idx];
    const isCorrect = userAns === q.correct_option;

    // Track section stats
    const secKey = q.section_id || q.category || "జనరల్";
    const secName = q.section_name || q.category || "జనరల్";
    if (!sectionStats[secKey]) {
      sectionStats[secKey] = { name: secName, total: 0, correct: 0, wrong: 0, skipped: 0 };
    }
    sectionStats[secKey].total++;

    if (!userAns) {
      skipped++;
      sectionStats[secKey].skipped++;
    } else if (isCorrect) {
      correct++;
      sectionStats[secKey].correct++;
    } else {
      wrong++;
      sectionStats[secKey].wrong++;
    }

    reviewList.push({
      num: idx + 1,
      question: q.question,
      sectionName: secName,
      isPyq: q.is_pyq,
      pyqYear: q.pyq_year,
      userAns: userAns || "ఏదీ ఎంచుకోలేదు",
      correctAns: q.correct_option,
      isCorrect: isCorrect,
      skipped: !userAns,
      explanation: q.explanation
    });
  });

  const netScore = Math.max(0, (correct * 1.0) - (wrong * 0.33)).toFixed(2);
  const accuracy = (correct + wrong) > 0 ? Math.round((correct / (correct + wrong)) * 100) : 0;

  document.getElementById("cbtResultNetScore").textContent = `${netScore} / ${cbtQuestions.length}`;
  document.getElementById("cbtResultAccuracy").textContent = `${accuracy}%`;
  document.getElementById("cbtResultCorrect").textContent = correct;
  document.getElementById("cbtResultWrong").textContent = wrong;
  document.getElementById("cbtResultSkipped").textContent = skipped;

  let remark = "అద్భుతం! గొప్ప స్కోరు సాధించారు! 🌟";
  if (netScore < (cbtQuestions.length * 0.35)) {
    remark = "మరింత ప్రిపరేషన్ మరియు నెగటివ్ మార్కింగ్ జాగ్రత్తలు అవసరం! 📚";
  } else if (netScore < (cbtQuestions.length * 0.60)) {
    remark = "మంచి ప్రయత్నం! తప్పులను రివ్యూ చేసి ఇంకా మెరుగుపడండి! 👍";
  }
  document.getElementById("cbtResultRemark").textContent = remark;

  // Render Section-wise Breakdown in Scorecard
  const secContainer = document.getElementById("cbtSectionScoresList");
  if (secContainer) {
    secContainer.innerHTML = "";
    Object.values(sectionStats).forEach(s => {
      const secNet = Math.max(0, (s.correct * 1.0) - (s.wrong * 0.33)).toFixed(2);
      const secAcc = (s.correct + s.wrong) > 0 ? Math.round((s.correct / (s.correct + s.wrong)) * 100) : 0;
      const row = document.createElement("div");
      row.className = "p-2.5 bg-white dark:bg-slate-900 rounded-xl border border-slate-200 dark:border-slate-700 flex justify-between items-center";
      row.innerHTML = `
        <div>
          <span class="font-black text-slate-900 dark:text-white block">${s.name}</span>
          <span class="text-[11px] text-slate-500">సరైనవి: <b class="text-emerald-600">${s.correct}</b> | తప్పులు: <b class="text-rose-600">${s.wrong}</b> | వదిలినవి: ${s.skipped}</span>
        </div>
        <div class="text-right">
          <span class="font-black text-xs text-blue-600 dark:text-blue-400 block">${secNet} / ${s.total}</span>
          <span class="text-[10px] px-1.5 py-0.5 rounded font-bold ${secAcc >= 60 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}">${secAcc}% అక్యూరసీ</span>
        </div>
      `;
      secContainer.appendChild(row);
    });
  }

  // Record CBT Exam Attempt in history for Analytics
  try {
    const history = JSON.parse(localStorage.getItem("ca_cbt_history") || "[]");
    history.push({
      date: new Date().toLocaleDateString('te-IN'),
      timestamp: Date.now(),
      mode: cbtExamMode,
      score: parseFloat(netScore),
      total: cbtQuestions.length,
      correct: correct,
      wrong: wrong,
      skipped: skipped,
      accuracy: accuracy
    });
    localStorage.setItem("ca_cbt_history", JSON.stringify(history));
  } catch (e) {
    console.error("Failed to record CBT history:", e);
  }

  // Render Detailed Answers and Explanations
  const container = document.getElementById("cbtReviewList");
  container.innerHTML = "";

  reviewList.forEach(item => {
    const div = document.createElement("div");
    let statusClass = "border-slate-200 bg-slate-50 dark:bg-slate-800/40";
    let badge = `<span class="text-xs font-bold text-slate-500">వదిలేసినది</span>`;

    if (item.isCorrect) {
      statusClass = "border-emerald-300 bg-emerald-50/70 dark:bg-emerald-950/20";
      badge = `<span class="text-xs font-bold text-emerald-700 dark:text-emerald-400">సరైనది (+1.0)</span>`;
    } else if (!item.skipped) {
      statusClass = "border-rose-300 bg-rose-50/70 dark:bg-rose-950/20";
      badge = `<span class="text-xs font-bold text-rose-700 dark:text-rose-400">తప్పు (-0.33)</span>`;
    }

    const pyqTag = item.isPyq ? `<span class="bg-amber-100 text-amber-900 border border-amber-300 text-[10px] font-black px-2 py-0.5 rounded ml-2">★ PYQ ${item.pyqYear || ''}</span>` : '';

    div.className = `p-3.5 rounded-xl border ${statusClass} text-xs sm:text-sm space-y-1.5`;
    div.innerHTML = `
      <div class="flex justify-between items-center">
        <span class="font-bold text-slate-900 dark:text-white">ప్రశ్న ${item.num} <span class="text-[11px] font-normal text-slate-500">(${item.sectionName})</span> ${pyqTag}</span>
        ${badge}
      </div>
      <p class="font-semibold text-slate-800 dark:text-slate-200">${item.question}</p>
      <div class="flex gap-4 font-bold text-xs pt-1">
        <span>మీ ఎంపిక: <b>${item.userAns}</b></span>
        <span class="text-emerald-700 dark:text-emerald-400">సరైన సమాధానం: <b>${item.correctAns}</b></span>
      </div>
      <p class="text-xs text-slate-600 dark:text-slate-400 bg-white/70 dark:bg-slate-800 p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 mt-1 whitespace-pre-line leading-relaxed">
        💡 <b>వివరణ:</b> ${item.explanation}
      </p>
    `;
    container.appendChild(div);
  });

  document.getElementById("cbtResultModal").classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function restartCbtExam() {
  document.getElementById("cbtResultModal").classList.add("hidden");
  if (cbtExamMode === "standard") {
    openCbtExamModal();
  } else {
    startAppscExam(cbtExamMode, cbtExamSectionId);
  }
}

// ==================== FEATURE: TELUGU AI STUDY MENTOR ====================
function initAiMentor() {
  const input = document.getElementById("aiMentorInput");
  if (input) {
    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleAiMentorSubmit(e);
      }
    });
  }
}

function openAiMentorModal() {
  const modal = document.getElementById("aiMentorModal");
  if (modal) {
    modal.classList.remove("hidden");
    const input = document.getElementById("aiMentorInput");
    if (input) input.focus();
    if (window.lucide) lucide.createIcons();
  }
}

function closeAiMentorModal() {
  const modal = document.getElementById("aiMentorModal");
  if (modal) modal.classList.add("hidden");
}

function askAiMentorPrompt(text) {
  const input = document.getElementById("aiMentorInput");
  if (input) {
    input.value = text;
    handleAiMentorSubmit(new Event("submit"));
  }
}

async function handleAiMentorSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  const input = document.getElementById("aiMentorInput");
  if (!input) return;
  const query = input.value.trim();
  if (!query) return;

  appendAiChatMessage("user", query);
  input.value = "";

  const typingId = appendTypingIndicator();

  try {
    const res = await fetch(`${API_BASE}/api/ai_mentor`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query })
    });
    const data = await res.json();
    removeTypingIndicator(typingId);

    if (data.success && data.response) {
      const resp = data.response;
      let formattedHtml = `
        <p class="font-extrabold text-blue-700 dark:text-blue-400 text-xs sm:text-sm mb-1">${resp.header}</p>
        <p class="mb-2 leading-relaxed">${resp.core_point}</p>
        <div class="bg-white/80 dark:bg-slate-800 p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 space-y-1 mb-2">
          <p class="font-bold text-amber-700 dark:text-amber-400 text-xs">🎯 పరీక్షా ముఖ్యాంశాలు (Exam Focus):</p>
          <ul class="list-disc pl-4 space-y-0.5 text-xs text-slate-700 dark:text-slate-300">
            ${resp.exam_tips.map(t => `<li>${t}</li>`).join('')}
          </ul>
        </div>
      `;

      if (resp.related_articles && resp.related_articles.length > 0) {
        formattedHtml += `
          <div class="pt-1.5 border-t border-slate-200 dark:border-slate-700 text-[11px] text-slate-500">
            <span class="font-bold">సంబంధిత ఆర్టికల్:</span> ${resp.related_articles[0].title}
          </div>
        `;
      }

      appendAiChatMessage("ai", formattedHtml);
    } else {
      appendAiChatMessage("ai", "క్షమించండి, మీ సందేహానికి సమాధానం పొందడంలో సమస్య ఎదురైంది. మరొకసారి ప్రయత్నించండి.");
    }
  } catch (err) {
    removeTypingIndicator(typingId);
    console.error("AI Mentor error:", err);
    appendAiChatMessage("ai", "సర్వర్‌తో కనెక్ట్ అవ్వడంలో సమస్య ఎదురైంది. దయచేసి ఇంటర్నెట్ సరిచూసుకోండి.");
  }
}

function appendAiChatMessage(sender, htmlContent) {
  const container = document.getElementById("aiChatMessages");
  if (!container) return;

  const div = document.createElement("div");
  if (sender === "user") {
    div.className = "chat-bubble-user p-3 text-xs sm:text-sm max-w-[85%] ml-auto leading-relaxed shadow-sm font-semibold";
    div.textContent = htmlContent;
  } else {
    div.className = "chat-bubble-ai p-3.5 text-xs sm:text-sm max-w-[90%] mr-auto leading-relaxed shadow-sm space-y-1";
    div.innerHTML = htmlContent;
  }

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
}

function appendTypingIndicator() {
  const container = document.getElementById("aiChatMessages");
  const id = `typing-${Date.now()}`;
  const div = document.createElement("div");
  div.id = id;
  div.className = "chat-bubble-ai p-2.5 max-w-[40%] text-xs text-slate-500 font-bold flex items-center gap-1.5";
  div.innerHTML = `<span>ఆలోచిస్తోంది...</span><span class="animate-bounce">●</span><span class="animate-bounce delay-100">●</span><span class="animate-bounce delay-200">●</span>`;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// ==================== FEATURE: SYLLABUS TRACKER ====================
const SYLLABUS_DATA = {
  appsc_g1: {
    title: "🏛️ APPSC గ్రూప్-1 & 2 సిలబస్",
    topics: [
      { id: "ap_g1_1", text: "జాతీయ & అంతర్జాతీయ సమకాలీన పరిణామాలు (Current Affairs)" },
      { id: "ap_g1_2", text: "భారత రాజ్యాంగం, సమాఖ్య వ్యవస్థ & గవర్నెన్స్ (Polity & Governance)" },
      { id: "ap_g1_3", text: "భారత ఆర్థిక వ్యవస్థ, ప్రణాళికలు & బడ్జెట్ (Indian Economy)" },
      { id: "ap_g1_4", text: "ఆంధ్రప్రదేశ్ విభజన అనంతర ఆర్థిక వ్యవస్థ & ఏపీ బడ్జెట్ (AP Economy)" },
      { id: "ap_g1_5", text: "సైన్స్ & టెక్నాలజీ, ఇన్ఫర్మేషన్ టెక్నాలజీ, ఇస్రో స్పేస్ మిషన్లు (S&T)" },
      { id: "ap_g1_6", text: "పర్యావరణం, సుస్థిర అభివృద్ధి & విపత్తు నిర్వహణ (Environment & Disaster Mgmt)" },
      { id: "ap_g1_7", text: "ఆంధ్రప్రదేశ్ చరిత్ర, సంస్కృతి & సంక్షేమ పథకాలు (AP Schemes & Culture)" }
    ]
  },
  tspsc_g1: {
    title: "🏛️ TSPSC గ్రూప్-1, 2 & 3 సిలబస్",
    topics: [
      { id: "ts_g1_1", text: "ప్రాంతీయ, జాతీయ & అంతర్జాతీయ వర్తమాన వ్యవహారాలు (Current Affairs)" },
      { id: "ts_g1_2", text: "తెలంగాణ ఉద్యమం & రాష్ట్ర ఆవిర్భావం (Telangana Movement)" },
      { id: "ts_g1_3", text: "భారత రాజ్యాంగం, ప్రాథమిక హక్కులు & 73, 74వ సవరణలు (Polity)" },
      { id: "ts_g1_4", text: "తెలంగాణ ఆర్థిక వ్యవస్థ, వ్యవసాయం & పారిశ్రామిక విధానం (Telangana Economy)" },
      { id: "ts_g1_5", text: "తెలంగాణ ప్రభుత్వ సంక్షేమ పథకాలు & పాలసీలు (Telangana Welfare Schemes)" },
      { id: "ts_g1_6", text: "జనరల్ సైన్స్ & దైనందిన జీవితంలో సైన్స్ అనువర్తనాలు (General Science)" },
      { id: "ts_g1_7", text: "తెలంగాణ సమాజం, సంస్కృతి, సాహిత్యం & కళలు (Heritage & Society)" }
    ]
  },
  polity_eco: {
    title: "📈 పాలిటీ & ఎకానమీ స్పెషల్ సిలబస్",
    topics: [
      { id: "pe_1", text: "రాష్ట్రపతి, గవర్నర్, పార్లమెంట్ & సుప్రీంకోర్టు తీర్పులు" },
      { id: "pe_2", text: "ఎన్నికల సంస్కరణలు & ఎన్నికల సంఘం (Election Commission)" },
      { id: "pe_3", text: "ద్రవ్యోల్బణం, రెపో రేటు & ఆర్బీఐ ద్రవ్య పరపతి విధానం (RBI Policy)" },
      { id: "pe_4", text: "కేంద్ర బడ్జెట్, పన్ను విధానం & GST కౌన్సిల్ నిర్ణయాలు" },
      { id: "pe_5", text: "నీతి ఆయోగ్ (NITI Aayog) నివేదికలు & ర్యాంకింగ్స్" }
    ]
  },
  science_tech: {
    title: "🚀 సైన్స్, స్పేస్ & ఎన్విరాన్‌మెంట్",
    topics: [
      { id: "st_1", text: "ఇస్రో ఉపగ్రహ ప్రయోగాలు & గగన్‌యాన్ అంతరిక్ష ప్రాజెక్ట్" },
      { id: "st_2", text: "డీఆర్‌డీవో (DRDO) క్షిపణి ప్రయోగాలు & రక్షణ రంగ ఆవిష్కరణలు" },
      { id: "st_3", text: "కృత్రిమ మేధ (AI), 5G, సైబర్ సెక్యూరిటీ & సూపర్ కంప్యూటర్లు" },
      { id: "st_4", text: "వాతావరణ మార్పులు (COP సమ్మిట్) & భారతదేశ పునరుత్పాదక ఇంధన లక్ష్యాలు" },
      { id: "st_5", text: "జాతీయ పార్కులు, బయోస్పియర్ రిజర్వ్‌లు & ప్రాజెక్ట్ టైగర్/ఎలిఫెంట్" }
    ]
  }
};

let currentSyllabusTab = "appsc_g1";

function initSyllabusTracker() {
  const openBtn = document.getElementById("openSyllabusBtn");
  const closeBtn = document.getElementById("closeSyllabusBtn");
  const modal = document.getElementById("syllabusModal");

  if (openBtn) openBtn.addEventListener("click", openSyllabusModal);
  if (closeBtn) closeBtn.addEventListener("click", closeSyllabusModal);
  if (modal) {
    modal.addEventListener("click", (e) => {
      if (e.target === modal) closeSyllabusModal();
    });
  }
}

function openSyllabusModal() {
  const modal = document.getElementById("syllabusModal");
  if (!modal) return;
  renderSyllabusItems();
  updateSyllabusProgress();
  modal.classList.remove("hidden");
  if (window.lucide) lucide.createIcons();
}

function closeSyllabusModal() {
  const modal = document.getElementById("syllabusModal");
  if (modal) modal.classList.add("hidden");
}

function switchSyllabusTab(tabKey) {
  currentSyllabusTab = tabKey;
  const tabs = document.querySelectorAll(".syllabus-tab");
  tabs.forEach(t => {
    if (t.getAttribute("data-stab") === tabKey) {
      t.classList.add("active", "border-emerald-600", "text-emerald-600");
      t.classList.remove("border-transparent", "text-slate-500");
    } else {
      t.classList.remove("active", "border-emerald-600", "text-emerald-600");
      t.classList.add("border-transparent", "text-slate-500");
    }
  });
  renderSyllabusItems();
}

function renderSyllabusItems() {
  const container = document.getElementById("syllabusItemsList");
  if (!container) return;
  container.innerHTML = "";

  const data = SYLLABUS_DATA[currentSyllabusTab];
  if (!data) return;

  const savedCompleted = JSON.parse(localStorage.getItem("syllabus_completed") || "[]");

  data.topics.forEach(t => {
    const isChecked = savedCompleted.includes(t.id);
    const div = document.createElement("div");
    div.className = `syllabus-item flex items-center justify-between p-3 rounded-xl border ${isChecked ? 'border-emerald-300 bg-emerald-50/50 dark:bg-emerald-950/20' : 'border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/40'} transition`;
    div.innerHTML = `
      <label class="flex items-center space-x-3 cursor-pointer flex-1">
        <input 
          type="checkbox" 
          ${isChecked ? 'checked' : ''} 
          onchange="toggleSyllabusCheckbox('${t.id}', this.checked)"
          class="w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500"
        />
        <span class="font-bold text-slate-800 dark:text-slate-200 ${isChecked ? 'line-through text-slate-400 dark:text-slate-500' : ''}">
          ${t.text}
        </span>
      </label>
      <span class="text-[10px] font-bold px-2 py-0.5 rounded ${isChecked ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-400'} shrink-0 ml-2">
        ${isChecked ? 'పూర్తయింది ✅' : 'చదవాలి ⏳'}
      </span>
    `;
    container.appendChild(div);
  });
}

function toggleSyllabusCheckbox(topicId, isChecked) {
  let saved = JSON.parse(localStorage.getItem("syllabus_completed") || "[]");
  if (isChecked) {
    if (!saved.includes(topicId)) saved.push(topicId);
  } else {
    saved = saved.filter(id => id !== topicId);
  }
  localStorage.setItem("syllabus_completed", JSON.stringify(saved));
  renderSyllabusItems();
  updateSyllabusProgress();
}

function updateSyllabusProgress() {
  const saved = JSON.parse(localStorage.getItem("syllabus_completed") || "[]");
  let totalTopics = 0;
  Object.values(SYLLABUS_DATA).forEach(tab => {
    totalTopics += tab.topics.length;
  });

  const percent = totalTopics > 0 ? Math.round((saved.length / totalTopics) * 100) : 0;
  const percentEl = document.getElementById("syllabusProgressPercent");
  const barEl = document.getElementById("syllabusProgressBar");

  if (percentEl) percentEl.textContent = `${percent}% (${saved.length}/${totalTopics} టాపిక్స్)`;
  if (barEl) barEl.style.width = `${percent}%`;
}

function resetSyllabusProgress() {
  if (confirm("మీ సిలబస్ చెక్‌లిస్ట్ పురోగతిని రీసెట్ చేయాలనుకుంటున్నారా?")) {
    localStorage.removeItem("syllabus_completed");
    renderSyllabusItems();
    updateSyllabusProgress();
    showToast("సిలబస్ ప్రోగ్రెస్ రీసెట్ చేయబడింది.");
  }
}

// ==================== FEATURE: TELUGU VOICE SEARCH ====================
function initVoiceSearch() {
  const btn = document.getElementById("voiceSearchBtn");
  const input = document.getElementById("searchInput");
  if (!btn || !input) return;

  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    btn.addEventListener("click", () => {
      showToast("మీ బ్రౌజర్‌లో వాయిస్ రికగ్నిషన్ సపోర్ట్ లేదు. దయచేసి Google Chrome వాడండి.");
    });
    return;
  }

  let isListening = false;
  const recognition = new SpeechRecognition();
  recognition.lang = "te-IN"; // Telugu (India)
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  btn.addEventListener("click", () => {
    if (isListening) {
      recognition.stop();
      return;
    }

    try {
      recognition.start();
      isListening = true;
      btn.classList.add("voice-recording");
      showToast("🎤 వింటున్నాను... తెలుగులో మాట్లాడండి (ఉదా: పథకాలు, ఇస్రో, బడ్జెట్)");
    } catch (e) {
      console.error("SpeechRecognition start error:", e);
      isListening = false;
      btn.classList.remove("voice-recording");
    }
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript.trim();
    if (transcript) {
      input.value = transcript;
      showToast(`🎙️ శోధించబడింది: "${transcript}"`);
      const inputEvent = new Event("input", { bubbles: true });
      input.dispatchEvent(inputEvent);
    }
  };

  recognition.onerror = (event) => {
    console.warn("Speech recognition error:", event.error);
    isListening = false;
    btn.classList.remove("voice-recording");
    if (event.error === "not-allowed") {
      showToast("మైక్రోఫోన్ అనుమతి నిరాకరించబడింది.");
    } else {
      showToast("వాయిస్ శోధనలో అంతరాయం కలిగింది. మరొకసారి ప్రయత్నించండి.");
    }
  };

  recognition.onend = () => {
    isListening = false;
    btn.classList.remove("voice-recording");
  };
}

// ==================== FEATURE: CONCEPT MINDMAPS ====================
const MINDMAP_DATA = {
  schemes: {
    title: "🌾 AP & TS ప్రభుత్వ సంక్షేమ పథకాల వ్యవస్థ",
    description: "రైతు, మహిళా, విద్యా మరియు ఆరోగ్య సంక్షేమ పథకాల నిర్మాణ క్రమం",
    root: "ప్రభుత్వ సంక్షేమ రంగాలు",
    branches: [
      {
        id: "sch_agri",
        title: "🚜 వ్యవసాయ & రైతు సంక్షేమం",
        takeaway: "రైతు భరోసా (ఏపీలో ఎకరాకు పెట్టుబడి సాయం), తెలంగాణ రైతు రుణమాఫీ (రూ.2 లక్షల వరకు), 24 గంటల ఉచిత విద్యుత్, పంటల బీమా మరియు ఈ-క్రాప్ బుకింగ్.",
        leaves: [
          { name: "రైతు భరోసా / పెట్టుబడి సాయం", info: "ఖరీఫ్, రబీ సీజన్లలో రైతులకు విత్తనాలు, ఎరువుల కొనుగోలుకు ప్రత్యక్ష నగదు బదిలీ (DBT)." },
          { name: "రైతు రుణమాఫీ పథకం", info: "అర్హులైన రైతులకు రూ. 2 లక్షల వరకు పంట రుణాల మాఫీ ప్రక్రియ." },
          { name: "పంటల బీమా (Fasal Bima)", info: "ప్రకృతి వైపరీత్యాల వల్ల నష్టపోయిన రైతులకు పూర్తి ప్రీమియం ప్రభుత్వమే చెల్లించి నష్టపరిహారం." }
        ]
      },
      {
        id: "sch_women",
        title: "👩 మహిళా సాధికారత & సంక్షేమం",
        takeaway: "మహాలక్ష్మి పథకం (తెలంగాణ ఆర్టీసీ బస్సుల్లో మహిళలకు ఉచిత ప్రయాణం), వైఎస్సార్ ఆసరా & చేయూత (డ్వాక్రా మహిళలకు ఆర్థిక చేయూత), గృహజ్యోతి (200 యూనిట్ల ఉచిత విద్యుత్).",
        leaves: [
          { name: "మహాలక్ష్మి ఉచిత బస్సు ప్రయాణం", info: "తెలంగాణ రాష్ట్ర పల్లె వెలుగు, ఎక్స్‌ప్రెస్ బస్సుల్లో మహిళలు, బాలికలకు జీరో టికెట్ ప్రయాణం." },
          { name: "డ్వాక్రా సంఘాల ఆర్థిక సాయం", info: "స్వయం సహాయక సంఘాలకు (SHG) సున్నా వడ్డీ రుణాలు మరియు వ్యాపార ప్రోత్సాహకాలు." },
          { name: "గృహజ్యోతి (ఉచిత విద్యుత్)", info: "పేద, మధ్యతరగతి కుటుంబాలకు నెలకు 200 యూనిట్ల వరకు ఉచిత గృహ విద్యుత్ సరఫరా." }
        ]
      },
      {
        id: "sch_edu",
        title: "🎓 విద్యా రంగం & సంస్కరణలు",
        takeaway: "అమ్మ ఒడి / తల్లికి వందనం (బడికి పంపే తల్లులకు వార్షిక సాయం), మన ఊరు - మన బడి (పాఠశాలల ఆధునికీకరణ), విద్యా దీవెన (పూర్తి ఫీజు రీయింబర్స్‌మెంట్).",
        leaves: [
          { name: "ఫీజు రీయింబర్స్‌మెంట్ & వసతి", info: "ఉన్నత చదువులు చదివే విద్యార్థులకు ట్యూషన్ ఫీజు మరియు మెస్ ఛార్జీల చెల్లింపు." },
          { name: "డిజిటల్ తరగతులు & IFP ప్యానెల్స్", info: "ప్రభుత్వ బడులలో ఇంటరాక్టివ్ ఫ్లాట్ ప్యానెల్స్, ఇంగ్లీష్ మీడియం బోధన." }
        ]
      },
      {
        id: "sch_health",
        title: "🏥 వైద్యం & ఆరోగ్య రక్షణ",
        takeaway: "ఆరోగ్యశ్రీ పరిమితి పెంపు (రూ.25 లక్షల వరకు ఉచిత కార్పొరేట్ చికిత్స), 108/104 అంబులెన్స్ నెట్‌వర్క్, బస్తీ దవాఖానాలు & విలేజ్ క్లినిక్స్.",
        leaves: [
          { name: "రాజీవ్ ఆరోగ్యశ్రీ / వైఎస్సార్ ఆరోగ్యశ్రీ", info: "నిరుపేదలకు గుండె, క్యాన్సర్, కిడ్నీ వంటి క్లిష్టమైన శస్త్రచికిత్సలకు ఉచిత కవరేజీ." },
          { name: "ఫ్యామిలీ డాక్టర్ కాన్సెప్ట్", info: "గ్రామీణ ప్రాంతాలకు క్రమం తప్పకుండా 104 వాహనాల్లో వెళ్లి ప్రాథమిక ఆరోగ్య పరీక్షలు నిర్వహించడం." }
        ]
      }
    ]
  },
  isro: {
    title: "🚀 ఇస్రో స్పేస్ రోడ్‌మ్యాప్ & ప్రాజెక్టులు",
    description: "భారత అంతరిక్ష పరిశోధనా సంస్థ చేపట్టిన మానవ సహిత & గ్రహాంతర మిషన్లు",
    root: "ఇస్రో ప్రధాన మిషన్ల వ్యవస్థ",
    branches: [
      {
        id: "isro_gaganyaan",
        title: "👨‍🚀 గగన్‌యాన్ (Gaganyaan Mission)",
        takeaway: "భారత తొలి మానవ సహిత అంతరిక్ష యాత్ర. 3గురు వ్యోమగాములను 400 కి.మీ లోయర్ ఎర్త్ ఆర్బిట్ (LEO) లోకి పంపి 3 రోజుల తర్వాత సురక్షితంగా బంగాళాఖాతంలో దించడం. రాకెట్: LVM3-HL (Human Rated).",
        leaves: [
          { name: "వ్యోమమిత్ర (Vyommitra)", info: "మానవుల కంటే ముందుగా పంపే మహిళా హ్యూమనాయిడ్ రోబోట్, లైఫ్ సపోర్ట్ సిస్టమ్స్ పరీక్ష." },
          { name: "క్రూ ఎస్కేప్ సిస్టమ్ (CES)", info: "ప్రయోగ సమయంలో ఏదైనా ప్రమాదం జరిగితే వ్యోమగాములను సురక్షితంగా కాపాడే రాకెట్ విభాగాలు." }
        ]
      },
      {
        id: "isro_chandrayaan",
        title: "🌕 చంద్రయాన్-4 (Lunar Sample Return)",
        takeaway: "చంద్రుని ఉపరితలంపై ల్యాండ్ అయి మట్టి, రాళ్ల నమూనాలను సేకరించి భూమికి తీసుకువచ్చే 5-మాడ్యూల్ మిషన్. 2028 ప్రయోగ లక్ష్యం.",
        leaves: [
          { name: "శాంపిల్ రిటర్న్ టెక్నాలజీ", info: "ల్యాండర్, అసెండర్, ట్రాన్స్‌ఫర్, రీ-ఎంట్రీ మాడ్యూల్స్ మధ్య అంతరిక్షంలో డాకింగ్ ప్రక్రియ." },
          { name: "దక్షిణ ధ్రువ అధ్యయనం", info: "చంద్రుని సౌత్ పోల్ వద్ద శాశ్వత చీకటి ప్రాంతాల్లో నీటి మంచు (Water Ice) అన్వేషణ." }
        ]
      },
      {
        id: "isro_aditya",
        title: "☀️ ఆదిత్య L1 (Aditya-L1 Solar Mission)",
        takeaway: "సూర్యుని కరోనా, సౌర తుఫానులు మరియు భూమి-సూర్యుని మధ్య L1 (లాగ్రాంజ్ పాయింట్ 1 - 15 లక్షల కి.మీ) వద్ద పరిభ్రమించే సన్ అబ్జర్వేటరీ. రాకెట్: PSLV-C57.",
        leaves: [
          { name: "VELC & SUIT పేలోడ్స్", info: "సౌర కరోనా నుండి వెలువడే అల్ట్రావయోలెట్ కిరణాలు మరియు కరోనల్ మాస్ ఎజెక్షన్ల విశ్లేషణ." }
        ]
      },
      {
        id: "isro_future",
        title: "🛰️ భారతీయ అంతరిక్ష స్టేషన్ (BAS) & SSLV",
        takeaway: "2035 నాటికి స్వదేశీ అంతరిక్ష స్టేషన్ నిర్మాణం, 2040 నాటికి భారత వ్యోమగామిని చంద్రుడిపైకి పంపే లక్ష్యం. చిన్న ఉపగ్రహాల కోసం SSLV వాణిజ్య ప్రయోగాలు.",
        leaves: [
          { name: "BAS - 2035 లక్ష్యం", info: "భారత పరిశోధకులు నిరంతరం అంతరిక్షంలో పరిశోధనలు చేసుకోవడానికి స్వతంత్ర స్పేస్ స్టేషన్." },
          { name: "SSLV (Small Satellite Launch Vehicle)", info: "500 కిలోల బరువు వరకు ఉపగ్రహాలను వేగంగా మరియు తక్కువ ఖర్చుతో ప్రయోగించే మినీ రాకెట్." }
        ]
      }
    ]
  },
  budget: {
    title: "💰 కేంద్ర బడ్జెట్ 2026-27 & ఆర్థిక ఫ్రేమ్‌వర్క్",
    description: "ఆదాయ వ్యయాలు, మూలధన కేటాయింపులు మరియు ఆర్థిక విధాన సంస్కరణలు",
    root: "కేంద్ర బడ్జెట్ & ఆర్థిక పురోగతి",
    branches: [
      {
        id: "bud_capex",
        title: "🏗️ మూలధన వ్యయం (Capex Push)",
        takeaway: "దేశంలో మౌలిక సదుపాయాల కల్పనకు రికార్డు స్థాయిలో రూ. 11.11 లక్షల కోట్లకు పైగా కేటాయింపులు (GDP లో 3.4%). రోడ్లు, రైల్వేలు, ఎయిర్‌పోర్టులు, డెడికేటెడ్ ఫ్రైట్ కారిడార్లు.",
        leaves: [
          { name: "రైల్వే ఆధునికీకరణ (వందే భారత్ & అమృత్ భారత్)", info: "కొత్త వందే భారత్ స్లీపర్ రైళ్లు, 1,300+ స్టేషన్ల పునర్నిర్మాణం." },
          { name: "నేషనల్ హైవేస్ & భారత్‌మాల", info: "ఎక్స్‌ప్రెస్‌వేలు, లాజిస్టిక్స్ పార్కులు మరియు సరిహద్దు రోడ్ల విస్తరణ." }
        ]
      },
      {
        id: "bud_fiscal",
        title: "📉 ద్రవ్యలోటు లక్ష్యాలు (Fiscal Consolidation)",
        takeaway: "ద్రవ్యలోటును GDP లో 4.5% కంటే తక్కువకు తగ్గించే ప్రణాళిక. విదేశీ రుణాల భారం తగ్గించి స్థిరమైన ఆర్థిక వ్యవస్థ నిర్మాణం.",
        leaves: [
          { name: "ద్రవ్యలోటు (Fiscal Deficit)", info: "ప్రభుత్వ ఆదాయం కంటే వ్యయం ఎక్కువైనప్పుడు తీసుకునే రుణాలు." },
          { name: "ద్రవ్యోల్బణ నియంత్రణ (RBI 4% Target)", info: "ధరల పెరుగుదల అదుపు కోసం రిజర్వ్ బ్యాంక్ ద్రవ్య విధాన కమిటీ (MPC) చర్యలు." }
        ]
      },
      {
        id: "bud_tax",
        title: "💵 పన్ను సంస్కరణలు (Direct & Indirect Tax)",
        takeaway: "నూతన ఆదాయపు పన్ను విధానం (New Tax Regime) లో పన్ను రహిత పరిమితి పెంపు, GST కౌన్సిల్ ద్వారా రేట్ల క్రమబద్ధీకరణ, డిజిటల్ ట్రాన్సాక్షన్స్ ప్రోత్సాహం.",
        leaves: [
          { name: "New Tax Regime సరళీకరణ", info: "స్టాండర్డ్ డిడక్షన్ రూ. 75,000కు పెంపు మరియు పన్ను స్లాబుల పునర్వ్యవస్థీకరణ." },
          { name: "GST సులభతరం", info: "వ్యాపారుల కోసం రిటర్నుల దాఖలు ప్రక్రియ సులభతరం మరియు ఈ-ఇన్‌వాయిస్ తప్పనిసరి." }
        ]
      }
    ]
  },
  polity: {
    title: "⚖️ భారత పాలిటీ & రాజ్యాంగ సంస్కరణలు",
    description: "కీలక రాజ్యాంగ సవరణలు, ఎన్నికల సంస్కరణలు మరియు సమకాలీన తీర్పులు",
    root: "రాజ్యాంగ వ్యవస్థ & సంస్కరణలు",
    branches: [
      {
        id: "pol_onoe",
        title: "🗳️ ఒకే దేశం - ఒకే ఎన్నిక (One Nation One Election)",
        takeaway: "లోక్‌సభ మరియు అన్ని రాష్ట్రాల అసెంబ్లీలకు ఏకకాలంలో ఎన్నికలు నిర్వహించే అంశంపై మాజీ రాష్ట్రపతి రామ్‌నాథ్ కోవింద్ నేతృత్వంలోని ఉన్నత స్థాయి కమిటీ నివేదిక. రాజ్యాంగంలోని ఆర్టికల్ 83, 172 సవరణల ప్రతిపాదన.",
        leaves: [
          { name: "కోవింద్ కమిటీ ప్రధాన సిఫార్సులు", info: "తొలి దశలో లోక్‌సభ మరియు అసెంబ్లీ ఎన్నికలు, తర్వాతి 100 రోజుల్లో స్థానిక సంస్థల ఎన్నికలు." },
          { name: "సవాళ్లు & సమాఖ్య సూత్రం", info: "రాష్ట్రాల శాసనసభల ముందస్తు రద్దు, అవిశ్వాస తీర్మానం సందర్భాలలో వ్యవహరించాల్సిన పద్ధతులు." }
        ]
      },
      {
        id: "pol_women_res",
        title: "👩‍⚖️ మహిళా రిజర్వేషన్ చట్టం (106వ సవరణ)",
        takeaway: "నారీ శక్తి వందన్ అధినియం: లోక్‌సభ మరియు రాష్ట్ర శాసనసభలలో మహిళలకు 33% రిజర్వేషన్ కల్పించే 106వ రాజ్యాంగ సవరణ చట్టం 2023. ఆర్టికల్ 330A, 332A చేరిక.",
        leaves: [
          { name: "అమలు నిబంధనలు", info: "జనాభా లెక్కల సేకరణ (Census) మరియు డీలిమిటేషన్ ప్రక్రియ పూర్తయిన తర్వాత అమల్లోకి వస్తుంది." },
          { name: "కాలపరిమితి (Sunset Clause)", info: "ఈ రిజర్వేషన్ అమల్లోకి వచ్చిన తేదీ నుండి 15 సంవత్సరాల పాటు అమలులో ఉంటుంది." }
        ]
      },
      {
        id: "pol_governor",
        title: "🏛️ గవర్నర్ అధికారాలు & ఆర్టికల్ 200",
        takeaway: "రాష్ట్ర అసెంబ్లీలు ఆమోదించిన బిల్లులపై గవర్నర్లు తీసుకునే నిర్ణయాలు. సుప్రీంకోర్టు తీర్పు: గవర్నర్లు బిల్లులను నిరవధికంగా పెండింగ్‌లో పెట్టకూడదు.",
        leaves: [
          { name: "ఆర్టికల్ 200 కింద గవర్నర్ 4 ఎంపికలు", info: "ఆమోదం తెలపడం, ఆమోదం నిలిపివేయడం, పునఃపరిశీలనకు పంపడం లేదా రాష్ట్రపతికి నివేదించడం." },
          { name: "సహకార సమాఖ్య సూత్రం (Federalism)", info: "ఎన్నికైన ప్రభుత్వాల ప్రజాభీష్టాన్ని గౌరవిస్తూ గవర్నర్లు రాజ్యాంగబద్ధంగా వ్యవహరించాలి." }
        ]
      }
    ]
  }
};

let currentMindmapTopic = "schemes";

function initMindmaps() {
  const openBtn = document.getElementById("openMindmapsBtn");
  const modal = document.getElementById("mindmapsModal");
  if (openBtn && modal) {
    openBtn.addEventListener("click", () => {
      renderMindmapTree(currentMindmapTopic);
      modal.classList.remove("hidden");
    });
  }
}

window.switchMindmapTopic = function(topicKey) {
  currentMindmapTopic = topicKey;
  document.querySelectorAll(".mindmap-tab").forEach(tab => {
    if (tab.getAttribute("data-mtopic") === topicKey) {
      tab.className = "mindmap-tab px-3 py-1.5 rounded-lg bg-amber-500 text-white font-black whitespace-nowrap shadow-sm";
    } else {
      tab.className = "mindmap-tab px-3 py-1.5 rounded-lg text-slate-500 hover:text-slate-900 dark:text-slate-400 font-bold whitespace-nowrap";
    }
  });
  renderMindmapTree(topicKey);
};

function renderMindmapTree(topicKey) {
  const data = MINDMAP_DATA[topicKey];
  const container = document.getElementById("mindmapTreeContainer");
  const details = document.getElementById("mindmapDetailsContent");
  if (!data || !container) return;

  if (details) {
    details.innerHTML = `
      <div class="space-y-2">
        <h5 class="font-extrabold text-indigo-900 dark:text-indigo-200 text-xs sm:text-sm">${data.title}</h5>
        <p class="text-xs leading-relaxed text-slate-700 dark:text-slate-300">${data.description}</p>
        <div class="bg-white/80 dark:bg-slate-900/80 p-3 rounded-lg border border-indigo-100 dark:border-slate-700 mt-2">
          <span class="font-bold text-amber-700 dark:text-amber-400 text-xs">💡 ఎలా చదవాలి:</span>
          <p class="text-xs text-slate-600 dark:text-slate-400 mt-0.5">ఎడమవైపు ఉన్న ఏదైనా బ్రాంచ్ లేదా టాపిక్ పై క్లిక్ చేయండి. ఆ అంశంపై పరీక్షల కోణంలో సమగ్ర విశ్లేషణ ఇక్కడ కనిపిస్తుంది.</p>
        </div>
      </div>
    `;
  }

  let html = `
    <div class="mindmap-node mindmap-root p-3.5 rounded-xl shadow-sm text-center mb-3">
      <span class="text-sm font-black">${data.root}</span>
    </div>
    <div class="space-y-3">
  `;

  data.branches.forEach((b, bIdx) => {
    html += `
      <div class="mindmap-branch space-y-2">
        <div class="mindmap-node bg-white dark:bg-slate-800 p-3 rounded-xl border border-slate-200 dark:border-slate-700 flex justify-between items-center shadow-2xs" onclick="selectMindmapBranch('${topicKey}', ${bIdx})">
          <span class="font-black text-xs sm:text-sm text-slate-900 dark:text-slate-100">${b.title}</span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300">
            ${b.leaves.length} అంశాలు ▾
          </span>
        </div>
        <div id="leaves_${b.id}" class="grid grid-cols-1 sm:grid-cols-2 gap-2 pl-3">
          ${b.leaves.map((l, lIdx) => `
            <div class="mindmap-node bg-slate-100 dark:bg-slate-850 hover:bg-indigo-50 dark:hover:bg-slate-750 p-2.5 rounded-lg border border-slate-200 dark:border-slate-700 text-xs cursor-pointer" onclick="selectMindmapLeaf('${topicKey}', ${bIdx}, ${lIdx})">
              <span class="font-bold text-slate-800 dark:text-slate-200">🔹 ${l.name}</span>
            </div>
          `).join("")}
        </div>
      </div>
    `;
  });

  html += `</div>`;
  container.innerHTML = html;
  if (window.lucide) lucide.createIcons();
}

window.selectMindmapBranch = function(topicKey, bIdx) {
  const b = MINDMAP_DATA[topicKey].branches[bIdx];
  const details = document.getElementById("mindmapDetailsContent");
  if (!b || !details) return;

  details.innerHTML = `
    <div class="space-y-2">
      <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-100 dark:bg-indigo-900/50 text-indigo-800 dark:text-indigo-300">ప్రధాన విభాగం</span>
      <h5 class="font-black text-xs sm:text-sm text-indigo-950 dark:text-indigo-100">${b.title}</h5>
      <div class="bg-white/90 dark:bg-slate-900 p-3 rounded-xl border border-indigo-200 dark:border-slate-700 shadow-2xs space-y-1.5">
        <span class="text-xs font-bold text-amber-700 dark:text-amber-400">🎯 పరీక్షల కీలక అంశాలు (Exam Takeaway):</span>
        <p class="text-xs leading-relaxed text-slate-800 dark:text-slate-200 font-medium">${b.takeaway}</p>
      </div>
    </div>
  `;
};

window.selectMindmapLeaf = function(topicKey, bIdx, lIdx) {
  const b = MINDMAP_DATA[topicKey].branches[bIdx];
  const leaf = b.leaves[lIdx];
  const details = document.getElementById("mindmapDetailsContent");
  if (!leaf || !details) return;

  details.innerHTML = `
    <div class="space-y-2">
      <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-300">${b.title}</span>
      <h5 class="font-black text-xs sm:text-sm text-slate-900 dark:text-slate-100">🔹 ${leaf.name}</h5>
      <div class="bg-white/90 dark:bg-slate-900 p-3 rounded-xl border border-blue-200 dark:border-slate-700 shadow-2xs space-y-1.5">
        <span class="text-xs font-bold text-emerald-700 dark:text-emerald-400">📋 సమగ్ర వివరణ (Key Points):</span>
        <p class="text-xs leading-relaxed text-slate-800 dark:text-slate-200">${leaf.info}</p>
      </div>
      <div class="pt-2 border-t border-indigo-100 dark:border-slate-700">
        <span class="text-[11px] text-slate-500">విభాగం ముఖ్యాంశం: ${b.takeaway.slice(0, 100)}...</span>
      </div>
    </div>
  `;
};

// ==================== MAP POINTING & ATLAS HUB INTEGRATION ====================
let mapPointsData = [];
let mapQuizData = [];
let activeMapDomain = "ap";
let selectedMapPointId = null;
let mapUserQuizAnswers = {};

async function initMapPointingHub() {
  const openBtn = document.getElementById("openMapPointingBtn");
  const closeBtn = document.getElementById("closeMapPointingBtn");
  const modal = document.getElementById("mapPointingModal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", async () => {
      modal.classList.remove("hidden");
      if (!mapPointsData.length) {
        await loadMapPointingData();
      }
      renderMapDomain(activeMapDomain);
      if (window.lucide) lucide.createIcons();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  // Domain Switcher Tabs
  const tabBtns = document.querySelectorAll(".map-tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const domain = btn.getAttribute("data-domain");
      activeMapDomain = domain;

      // Update button active styles
      tabBtns.forEach(b => {
        b.classList.remove("bg-teal-600", "text-white", "shadow-sm", "active");
        b.classList.add("bg-slate-100", "dark:bg-slate-800", "text-slate-700", "dark:text-slate-300");
      });
      btn.classList.remove("bg-slate-100", "dark:bg-slate-800", "text-slate-700", "dark:text-slate-300");
      btn.classList.add("bg-teal-600", "text-white", "shadow-sm", "active");

      if (domain === "quiz") {
        document.getElementById("mapExplorerContainer").classList.add("hidden");
        document.getElementById("mapQuizContainer").classList.remove("hidden");
        renderMapQuiz();
      } else {
        document.getElementById("mapExplorerContainer").classList.remove("hidden");
        document.getElementById("mapQuizContainer").classList.add("hidden");
        renderMapDomain(domain);
      }
      if (window.lucide) lucide.createIcons();
    });
  });

  // Search input filtering
  const searchInput = document.getElementById("mapSearchInput");
  if (searchInput) {
    searchInput.addEventListener("input", (e) => {
      filterMapPointsList(e.target.value.toLowerCase().trim());
    });
  }

  // Test point in quiz button
  const testQuizBtn = document.getElementById("testPointInQuizBtn");
  if (testQuizBtn) {
    testQuizBtn.addEventListener("click", () => {
      const quizTabBtn = document.querySelector('.map-tab-btn[data-domain="quiz"]');
      if (quizTabBtn) quizTabBtn.click();
    });
  }
}

async function loadMapPointingData() {
  try {
    const res = await fetch(`${API_BASE}/api/map_pointing?domain=all`);
    const data = await res.json();
    if (data.success && data.data) {
      mapPointsData = data.data;
    }
    const qRes = await fetch(`${API_BASE}/api/map_pointing/quiz?domain=all`);
    const qData = await qRes.json();
    if (qData.success && qData.questions) {
      mapQuizData = qData.questions;
    }

    // Update Counts on Tabs
    const apCount = mapPointsData.filter(p => p.domain === "ap").length;
    const indCount = mapPointsData.filter(p => p.domain === "india").length;
    const wldCount = mapPointsData.filter(p => p.domain === "world").length;

    const apEl = document.getElementById("mapTabApCount");
    const indEl = document.getElementById("mapTabIndiaCount");
    const wldEl = document.getElementById("mapTabWorldCount");
    if (apEl) apEl.textContent = apCount;
    if (indEl) indEl.textContent = indCount;
    if (wldEl) wldEl.textContent = wldCount;
  } catch (err) {
    console.error("Error loading map pointing data:", err);
  }
}

function renderMapDomain(domain) {
  const domainPoints = mapPointsData.filter(p => p.domain === domain);
  const watermarkEl = document.getElementById("mapWatermarkText");
  const noteEl = document.getElementById("mapDomainNote");
  const countEl = document.getElementById("activePointCounter");

  if (domain === "ap") {
    if (watermarkEl) watermarkEl.textContent = "ANDHRA PRADESH";
    if (noteEl) noteEl.textContent = "🚩 ఆంధ్రప్రదేశ్: పోర్టులు, నదులు, డ్యామ్‌లు & ఖనిజ క్లస్టర్లు";
  } else if (domain === "india") {
    if (watermarkEl) watermarkEl.textContent = "INDIA ATLAS";
    if (noteEl) noteEl.textContent = "🇮🇳 భారతదేశం: హిమాలయ కనుమలు, చానల్స్, అణు & అంతరిక్ష కేంద్రాలు";
  } else {
    if (watermarkEl) watermarkEl.textContent = "WORLD STRAITS";
    if (noteEl) noteEl.textContent = "🌐 ప్రపంచ సమకాలీన అంశాలు: వ్యూహాత్మక జలసంధులు & చోక్‌పాయింట్స్";
  }
  if (countEl) countEl.textContent = `${domainPoints.length} కేంద్రాలు`;

  // Render Map Pins
  const pinsLayer = document.getElementById("mapPinsLayer");
  if (pinsLayer) {
    pinsLayer.innerHTML = "";
    domainPoints.forEach((p, idx) => {
      const pin = document.createElement("div");
      pin.className = "absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition hover:scale-125 z-10 map-pin-marker";
      pin.style.left = `${p.x_pct}%`;
      pin.style.top = `${p.y_pct}%`;
      pin.setAttribute("data-id", p.id);

      let pinColor = domain === "ap" ? "bg-teal-500" : (domain === "india" ? "bg-blue-600" : "bg-purple-600");
      let pingColor = domain === "ap" ? "bg-teal-400" : (domain === "india" ? "bg-blue-400" : "bg-purple-400");
      let num = idx + 1;

      pin.innerHTML = `
        <div class="group relative flex flex-col items-center">
          <span class="relative flex h-5 w-5">
            <span class="animate-ping absolute inline-flex h-full w-full rounded-full ${pingColor} opacity-75"></span>
            <span class="relative inline-flex rounded-full h-5 w-5 ${pinColor} border-2 border-white shadow-md items-center justify-center text-[9px] font-black text-white">${num}</span>
          </span>
          <span class="absolute bottom-6 bg-slate-900/95 text-white text-[10px] font-extrabold px-2 py-0.5 rounded shadow whitespace-nowrap opacity-90 group-hover:opacity-100 group-hover:scale-105 transition pointer-events-none border border-slate-700">
            ${p.telugu_name.split('(')[0].trim()}
          </span>
        </div>
      `;

      pin.addEventListener("click", () => selectMapPoint(p.id));
      pinsLayer.appendChild(pin);
    });
  }

  // Render Quick Select List
  renderQuickSelectList(domainPoints);

  // Auto-select first point
  if (domainPoints.length > 0) {
    selectMapPoint(domainPoints[0].id);
  }
}

function renderQuickSelectList(points) {
  const container = document.getElementById("mapPointsQuickList");
  if (!container) return;
  container.innerHTML = "";

  points.forEach(p => {
    const btn = document.createElement("button");
    btn.className = "map-quick-btn text-xs font-bold px-2.5 py-1 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-200 hover:border-teal-500 hover:bg-teal-50 dark:hover:bg-teal-950/40 transition flex items-center gap-1";
    btn.setAttribute("data-id", p.id);
    btn.innerHTML = `<span>📍</span><span>${p.telugu_name.split('(')[0].trim()}</span>`;
    btn.addEventListener("click", () => selectMapPoint(p.id));
    container.appendChild(btn);
  });
}

function selectMapPoint(pointId) {
  selectedMapPointId = pointId;
  const p = mapPointsData.find(item => item.id === pointId);
  if (!p) return;

  // Highlight active pin
  document.querySelectorAll(".map-pin-marker").forEach(el => {
    if (el.getAttribute("data-id") === pointId) {
      el.classList.add("scale-125", "z-30");
      el.querySelector(".rounded-full")?.classList.add("ring-4", "ring-yellow-300");
    } else {
      el.classList.remove("scale-125", "z-30");
      el.querySelector(".rounded-full")?.classList.remove("ring-4", "ring-yellow-300");
    }
  });

  // Highlight quick list button
  document.querySelectorAll(".map-quick-btn").forEach(el => {
    if (el.getAttribute("data-id") === pointId) {
      el.classList.add("border-teal-500", "bg-teal-100", "dark:bg-teal-900/60", "text-teal-950", "dark:text-teal-200", "font-black");
    } else {
      el.classList.remove("border-teal-500", "bg-teal-100", "dark:bg-teal-900/60", "text-teal-950", "dark:text-teal-200", "font-black");
    }
  });

  // Populate Detail Card
  const catEl = document.getElementById("detailBadgeCat");
  const locEl = document.getElementById("detailBadgeLoc");
  const titleEl = document.getElementById("detailTitle");
  const engEl = document.getElementById("detailEngName");
  const factsEl = document.getElementById("detailKeyFacts");
  const sigEl = document.getElementById("detailSignificance");
  const pyqBox = document.getElementById("detailPyqBox");
  const pyqText = document.getElementById("detailPyqText");

  if (catEl) catEl.textContent = p.category;
  if (locEl) locEl.textContent = p.district || p.state || p.region || "";
  if (titleEl) titleEl.textContent = p.telugu_name;
  if (engEl) engEl.textContent = p.name;
  if (factsEl) factsEl.textContent = p.key_facts;
  if (sigEl) sigEl.textContent = p.exam_significance;

  if (pyqBox && pyqText) {
    if (p.pyq) {
      pyqBox.classList.remove("hidden");
      pyqText.textContent = p.pyq;
    } else {
      pyqBox.classList.add("hidden");
    }
  }
}

function filterMapPointsList(query) {
  const btns = document.querySelectorAll(".map-quick-btn");
  btns.forEach(btn => {
    const text = btn.textContent.toLowerCase();
    if (!query || text.includes(query)) {
      btn.style.display = "inline-flex";
    } else {
      btn.style.display = "none";
    }
  });
}

function renderMapQuiz() {
  const container = document.getElementById("mapQuizQuestionsList");
  if (!container) return;
  container.innerHTML = "";

  mapQuizData.forEach((q, idx) => {
    const card = document.createElement("div");
    card.className = "bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-4 space-y-2.5 shadow-xs";
    
    let optButtons = q.options.map((opt, oIdx) => {
      const optLetter = ["A", "B", "C", "D"][oIdx];
      return `<button class="map-quiz-opt-btn w-full text-left p-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/60 hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-semibold transition" data-qid="${q.id}" data-val="${opt}">
        <b>${optLetter})</b> ${opt}
      </button>`;
    }).join("");

    card.innerHTML = `
      <div class="flex justify-between items-center text-xs font-bold">
        <span class="bg-amber-100 text-amber-900 px-2 py-0.5 rounded-md">ప్రశ్న ${idx + 1}</span>
        <span class="text-slate-500 font-bold">📍 ${q.location_name.split('(')[0].trim()}</span>
      </div>
      <p class="text-xs sm:text-sm font-black text-slate-900 dark:text-white leading-snug">
        ${q.question}
      </p>
      <div class="space-y-1.5" id="optContainer_${q.id}">
        ${optButtons}
      </div>
      <div id="expBox_${q.id}" class="hidden p-2.5 rounded-xl text-xs font-semibold leading-relaxed border mt-2"></div>
    `;

    container.appendChild(card);
  });

  // Attach click listeners to option buttons
  container.querySelectorAll(".map-quiz-opt-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const qid = btn.getAttribute("data-qid");
      const selectedVal = btn.getAttribute("data-val");
      handleMapQuizSelection(qid, selectedVal);
    });
  });

  updateMapQuizScore();
}

function handleMapQuizSelection(qid, selectedVal) {
  const q = mapQuizData.find(item => item.id === qid);
  if (!q || mapUserQuizAnswers[qid] !== undefined) return;

  const isCorrect = (selectedVal === q.answer);
  mapUserQuizAnswers[qid] = { selected: selectedVal, correct: isCorrect };

  const optContainer = document.getElementById(`optContainer_${qid}`);
  const expBox = document.getElementById(`expBox_${qid}`);

  if (optContainer) {
    optContainer.querySelectorAll(".map-quiz-opt-btn").forEach(btn => {
      const val = btn.getAttribute("data-val");
      btn.disabled = true;
      if (val === q.answer) {
        btn.className = "w-full text-left p-2 rounded-xl border border-emerald-500 bg-emerald-50 text-emerald-950 dark:bg-emerald-950/60 dark:text-emerald-200 text-xs font-black";
      } else if (val === selectedVal && !isCorrect) {
        btn.className = "w-full text-left p-2 rounded-xl border border-rose-500 bg-rose-50 text-rose-950 dark:bg-rose-950/60 dark:text-rose-200 text-xs font-bold line-through";
      }
    });
  }

  if (expBox) {
    expBox.classList.remove("hidden");
    if (isCorrect) {
      expBox.className = "p-2.5 rounded-xl text-xs font-semibold leading-relaxed border bg-emerald-50 dark:bg-emerald-950/40 text-emerald-950 dark:text-emerald-200 border-emerald-200 dark:border-emerald-800";
      expBox.innerHTML = `<span>✔ <b>సరైన సమాధానం!</b> ${q.explanation}</span>`;
    } else {
      expBox.className = "p-2.5 rounded-xl text-xs font-semibold leading-relaxed border bg-rose-50 dark:bg-rose-950/40 text-rose-950 dark:text-rose-200 border-rose-200 dark:border-rose-800";
      expBox.innerHTML = `<span>✖ <b>సరైన సమాధానం: ${q.answer}</b> — ${q.explanation}</span>`;
    }
  }

  updateMapQuizScore();
}

function updateMapQuizScore() {
  const correctCount = Object.values(mapUserQuizAnswers).filter(a => a.correct).length;
  const scoreEl = document.getElementById("mapQuizScoreText");
  if (scoreEl) {
    scoreEl.textContent = `${correctCount} / ${mapQuizData.length}`;
  }
}

// ==================== AP HISTORY & APPSC EXAMS HUB ====================
let apHistoryTopicsData = [];
let apHistoryQuestionsData = [];
let apHistoryUserAnswers = {};

async function initApHistoryHub() {
  const openBtn = document.getElementById("openApHistoryBtn");
  const closeBtn = document.getElementById("closeApHistoryBtn");
  const modal = document.getElementById("apHistoryModal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", async () => {
      modal.classList.remove("hidden");
      if (!apHistoryTopicsData.length) {
        await loadApHistoryData();
      }
      renderApHistoryView();
      if (window.lucide) lucide.createIcons();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  // Quick Exam Launcher Buttons inside AP History modal
  const g1Btn = document.getElementById("startGroup1ExamBtn");
  if (g1Btn) {
    g1Btn.addEventListener("click", () => {
      startAppscExam("group1");
    });
  }

  const g2Btn = document.getElementById("startGroup2FromHistoryBtn");
  if (g2Btn) {
    g2Btn.addEventListener("click", () => {
      startAppscExam("group2");
    });
  }

  const g3Btn = document.getElementById("startGroup3ExamBtn");
  if (g3Btn) {
    g3Btn.addEventListener("click", () => {
      startAppscExam("group3");
    });
  }
}

async function loadApHistoryData() {
  try {
    const res = await fetch(`${API_BASE}/api/ap_history`);
    const data = await res.json();
    if (data.success) {
      apHistoryTopicsData = data.topics || [];
      apHistoryQuestionsData = data.questions || [];
    }
  } catch (e) {
    console.error("Error loading AP History data:", e);
  }
}

function renderApHistoryView() {
  const topicsContainer = document.getElementById("apTopicsContainer");
  const questionsContainer = document.getElementById("apHistoryQuestionsContainer");

  if (topicsContainer) {
    topicsContainer.innerHTML = "";
    apHistoryTopicsData.forEach((topic, idx) => {
      const card = document.createElement("div");
      card.className = "p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-850 shadow-xs hover:border-purple-300 dark:hover:border-purple-800 transition";
      
      const factsList = topic.key_facts.map(f => `<li class="leading-relaxed text-slate-700 dark:text-slate-300">🔹 ${f}</li>`).join("");

      card.innerHTML = `
        <div class="flex flex-wrap justify-between items-start gap-2 mb-2">
          <div>
            <span class="text-[10px] font-black uppercase px-2 py-0.5 rounded bg-purple-100 dark:bg-purple-950/60 text-purple-800 dark:text-purple-300 border border-purple-200 dark:border-purple-800">${topic.era}</span>
            <h4 class="text-sm sm:text-base font-black text-slate-900 dark:text-white mt-1">${topic.title}</h4>
          </div>
          <span class="text-xs text-slate-500 font-bold bg-slate-100 dark:bg-slate-800 px-2.5 py-1 rounded-lg">${topic.ruler_info}</span>
        </div>
        <ul class="text-xs space-y-1.5 my-2.5 pl-1">
          ${factsList}
        </ul>
        <div class="mt-3 p-2.5 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800/60 text-xs font-semibold text-amber-900 dark:text-amber-200">
          <span class="font-bold">★ PYQ పరీక్ష ముఖ్యాంశం:</span> ${topic.pyq_note}
        </div>
      `;
      topicsContainer.appendChild(card);
    });
  }

  if (questionsContainer) {
    questionsContainer.innerHTML = "";
    apHistoryQuestionsData.forEach((q, idx) => {
      const card = document.createElement("div");
      card.className = "p-3.5 rounded-2xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-850 text-xs sm:text-sm space-y-2";
      
      const options = [
        { key: "A", text: q.option_a },
        { key: "B", text: q.option_b },
        { key: "C", text: q.option_c },
        { key: "D", text: q.option_d }
      ];

      const optButtons = options.map(opt => `
        <button class="aph-quiz-opt-btn w-full text-left p-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-purple-50 dark:hover:bg-slate-700 font-semibold text-xs flex items-center gap-2 transition" data-qid="${q.id}" data-val="${opt.key}">
          <span class="w-5 h-5 rounded-full border border-slate-300 dark:border-slate-600 flex items-center justify-center font-bold shrink-0 text-[11px]">${opt.key}</span>
          <span class="flex-1">${opt.text}</span>
        </button>
      `).join("");

      card.innerHTML = `
        <div class="flex justify-between items-center text-xs font-bold">
          <span class="bg-purple-100 text-purple-900 px-2 py-0.5 rounded">ప్రశ్న ${idx + 1}</span>
          <span class="text-slate-500 font-bold text-[11px]">${q.pyq_tag || 'APPSC PYQ'}</span>
        </div>
        <p class="font-bold text-slate-900 dark:text-white leading-snug">${q.question}</p>
        <div class="space-y-1.5" id="aphOptContainer_${q.id}">
          ${optButtons}
        </div>
        <div id="aphExpBox_${q.id}" class="hidden p-2.5 rounded-xl text-xs font-semibold leading-relaxed border mt-2"></div>
      `;

      questionsContainer.appendChild(card);
    });

    // Option listeners
    questionsContainer.querySelectorAll(".aph-quiz-opt-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const qid = btn.getAttribute("data-qid");
        const selectedVal = btn.getAttribute("data-val");
        handleApHistoryQuizSelection(qid, selectedVal);
      });
    });
  }
}

function handleApHistoryQuizSelection(qid, selectedVal) {
  const q = apHistoryQuestionsData.find(item => item.id === qid);
  if (!q || apHistoryUserAnswers[qid] !== undefined) return;

  const isCorrect = (selectedVal === q.correct_option);
  apHistoryUserAnswers[qid] = { selected: selectedVal, correct: isCorrect };

  const optContainer = document.getElementById(`aphOptContainer_${qid}`);
  const expBox = document.getElementById(`aphExpBox_${qid}`);

  if (optContainer) {
    optContainer.querySelectorAll(".aph-quiz-opt-btn").forEach(btn => {
      const val = btn.getAttribute("data-val");
      btn.disabled = true;
      if (val === q.correct_option) {
        btn.className = "w-full text-left p-2 rounded-xl border border-emerald-500 bg-emerald-50 text-emerald-950 dark:bg-emerald-950/60 dark:text-emerald-200 text-xs font-black flex items-center gap-2";
      } else if (val === selectedVal && !isCorrect) {
        btn.className = "w-full text-left p-2 rounded-xl border border-rose-500 bg-rose-50 text-rose-950 dark:bg-rose-950/60 dark:text-rose-200 text-xs font-bold line-through flex items-center gap-2";
      }
    });
  }

  if (expBox) {
    expBox.classList.remove("hidden");
    if (isCorrect) {
      expBox.className = "p-2.5 rounded-xl text-xs font-semibold leading-relaxed border bg-emerald-50 dark:bg-emerald-950/40 text-emerald-950 dark:text-emerald-200 border-emerald-200 dark:border-emerald-800";
      expBox.innerHTML = `<span>✔ <b>సరైన సమాధానం!</b> ${q.explanation}</span>`;
    } else {
      expBox.className = "p-2.5 rounded-xl text-xs font-semibold leading-relaxed border bg-rose-50 dark:bg-rose-950/40 text-rose-950 dark:text-rose-200 border-rose-200 dark:border-rose-800";
      expBox.innerHTML = `<span>✖ <b>సరైన సమాధానం: ${q.correct_option}</b> — ${q.explanation}</span>`;
    }
  }
}

// ==================== WELFARE SCHEMES & BUDGET 2026 HUB ====================
let schemesData = [];
let schemesQuizData = [];
let activeSchemeTab = "ap";
let schemesUserAnswers = {};

async function initSchemesHub() {
  const openBtn = document.getElementById("openSchemesBtn");
  const closeBtn = document.getElementById("closeSchemesBtn");
  const modal = document.getElementById("schemesModal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", async () => {
      modal.classList.remove("hidden");
      if (!schemesData.length) {
        await loadSchemesData();
      }
      renderSchemesTab(activeSchemeTab);
      if (window.lucide) lucide.createIcons();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }

  const tabBtns = document.querySelectorAll(".scheme-tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const cat = btn.getAttribute("data-cat");
      activeSchemeTab = cat;

      tabBtns.forEach(b => {
        b.classList.remove("bg-emerald-600", "text-white", "shadow-sm", "active");
        b.classList.add("bg-slate-100", "dark:bg-slate-800", "text-slate-700", "dark:text-slate-300");
      });
      btn.classList.remove("bg-slate-100", "dark:bg-slate-800", "text-slate-700", "dark:text-slate-300");
      btn.classList.add("bg-emerald-600", "text-white", "shadow-sm", "active");

      renderSchemesTab(cat);
      if (window.lucide) lucide.createIcons();
    });
  });
}

async function loadSchemesData() {
  try {
    const res = await fetch(`${API_BASE}/api/schemes?category=all`);
    const data = await res.json();
    if (data.success) {
      schemesData = data.schemes || [];
      schemesQuizData = data.quizzes || [];
    }
  } catch (e) {
    console.error("Error loading schemes data:", e);
  }
}

function renderSchemesTab(cat) {
  const cardsContainer = document.getElementById("schemesCardsContainer");
  const quizContainer = document.getElementById("schemesQuizContainer");

  if (cat === "quiz") {
    if (cardsContainer) cardsContainer.classList.add("hidden");
    if (quizContainer) {
      quizContainer.classList.remove("hidden");
      renderSchemesQuiz();
    }
    return;
  }

  if (quizContainer) quizContainer.classList.add("hidden");
  if (cardsContainer) {
    cardsContainer.classList.remove("hidden");
    cardsContainer.innerHTML = "";

    const filtered = (cat === "all") ? schemesData : schemesData.filter(s => s.category === cat);

    filtered.forEach(s => {
      const card = document.createElement("div");
      card.className = "p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-850 shadow-xs hover:border-emerald-300 dark:hover:border-emerald-700 transition flex flex-col justify-between";

      const catBadge = s.category === "ap" ? "🚩 AP సూపర్ సిక్స్" : (s.category === "telangana" ? "🌾 తెలంగాణ గ్యారెంటీ" : "🇮🇳 కేంద్ర పథకం");
      const catBadgeCls = s.category === "ap" ? "bg-emerald-100 text-emerald-800" : (s.category === "telangana" ? "bg-amber-100 text-amber-900" : "bg-blue-100 text-blue-900");

      card.innerHTML = `
        <div>
          <div class="flex justify-between items-start gap-2 mb-2">
            <div>
              <span class="text-[10px] font-black uppercase px-2 py-0.5 rounded ${catBadgeCls}">${catBadge}</span>
              <h4 class="text-sm sm:text-base font-black text-slate-900 dark:text-white mt-1">${s.telugu_name}</h4>
              <p class="text-[11px] text-slate-500 font-semibold">${s.dept}</p>
            </div>
          </div>
          <div class="bg-slate-50 dark:bg-slate-800/80 p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs space-y-1.5 my-2">
            <div><span class="font-bold text-emerald-700 dark:text-emerald-400">🎁 ప్రయోజనం:</span> <span class="text-slate-800 dark:text-slate-200">${s.benefit}</span></div>
            <div><span class="font-bold text-blue-700 dark:text-blue-400">👥 అర్హత:</span> <span class="text-slate-700 dark:text-slate-300">${s.eligibility}</span></div>
            <div><span class="font-bold text-slate-700 dark:text-slate-300">📋 ముఖ్యాంశాలు:</span> <p class="text-slate-600 dark:text-slate-400 mt-0.5 whitespace-pre-line">${s.key_facts}</p></div>
          </div>
        </div>
        <div class="mt-2 pt-2 border-t border-slate-100 dark:border-slate-800 flex flex-col gap-1 text-[11px]">
          <div class="text-slate-500">💰 <b>బడ్జెట్:</b> ${s.budget_note}</div>
          <div class="text-amber-800 dark:text-amber-300 font-semibold">★ <b>PYQ టిప్:</b> ${s.pyq_note}</div>
        </div>
      `;
      cardsContainer.appendChild(card);
    });
  }
}

function renderSchemesQuiz() {
  const container = document.getElementById("schemesQuizContainer");
  if (!container) return;
  container.innerHTML = "";

  schemesQuizData.forEach((q, idx) => {
    const card = document.createElement("div");
    card.className = "p-4 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-850 shadow-xs space-y-2.5 text-xs sm:text-sm";

    const optButtons = q.options.map((opt, oIdx) => `
      <button class="sch-quiz-opt-btn w-full text-left p-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 hover:bg-emerald-50 dark:hover:bg-slate-700 font-semibold text-xs transition" data-qid="${q.id}" data-val="${opt}">
        ${String.fromCharCode(65 + oIdx)}. ${opt}
      </button>
    `).join("");

    card.innerHTML = `
      <div class="flex justify-between items-center text-xs font-bold">
        <span class="bg-amber-100 text-amber-900 px-2 py-0.5 rounded">పథకాల ప్రశ్న ${idx + 1}</span>
        <span class="text-slate-500 font-bold uppercase text-[10px]">${q.category}</span>
      </div>
      <p class="font-bold text-slate-900 dark:text-white leading-snug">${q.question}</p>
      <div class="space-y-1.5" id="schOptContainer_${q.id}">
        ${optButtons}
      </div>
      <div id="schExpBox_${q.id}" class="hidden p-2.5 rounded-xl text-xs font-semibold leading-relaxed border mt-2"></div>
    `;
    container.appendChild(card);
  });

  container.querySelectorAll(".sch-quiz-opt-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const qid = btn.getAttribute("data-qid");
      const selectedVal = btn.getAttribute("data-val");
      handleSchemesQuizSelection(qid, selectedVal);
    });
  });
}

function handleSchemesQuizSelection(qid, selectedVal) {
  const q = schemesQuizData.find(item => item.id === qid);
  if (!q || schemesUserAnswers[qid] !== undefined) return;

  const isCorrect = (selectedVal === q.answer);
  schemesUserAnswers[qid] = { selected: selectedVal, correct: isCorrect };

  const optContainer = document.getElementById(`schOptContainer_${qid}`);
  const expBox = document.getElementById(`schExpBox_${qid}`);

  if (optContainer) {
    optContainer.querySelectorAll(".sch-quiz-opt-btn").forEach(btn => {
      const val = btn.getAttribute("data-val");
      btn.disabled = true;
      if (val === q.answer) {
        btn.className = "w-full text-left p-2.5 rounded-xl border border-emerald-500 bg-emerald-50 text-emerald-950 dark:bg-emerald-950/60 dark:text-emerald-200 text-xs font-black";
      } else if (val === selectedVal && !isCorrect) {
        btn.className = "w-full text-left p-2.5 rounded-xl border border-rose-500 bg-rose-50 text-rose-950 dark:bg-rose-950/60 dark:text-rose-200 text-xs font-bold line-through";
      }
    });
  }

  if (expBox) {
    expBox.classList.remove("hidden");
    if (isCorrect) {
      expBox.className = "p-2.5 rounded-xl text-xs font-semibold leading-relaxed border bg-emerald-50 dark:bg-emerald-950/40 text-emerald-950 dark:text-emerald-200 border-emerald-200 dark:border-emerald-800";
      expBox.innerHTML = `<span>✔ <b>సరైన సమాధానం!</b> ${q.explanation}</span>`;
    } else {
      expBox.className = "p-2.5 rounded-xl text-xs font-semibold leading-relaxed border bg-rose-50 dark:bg-rose-950/40 text-rose-950 dark:text-rose-200 border-rose-200 dark:border-rose-800";
      expBox.innerHTML = `<span>✖ <b>సరైన సమాధానం: ${q.answer}</b> — ${q.explanation}</span>`;
    }
  }
}

// ==================== MAINS MODEL ANSWERS HUB ====================
let mainsQuestionsData = [];

async function initMainsHub() {
  const openBtn = document.getElementById("openMainsBtn");
  const closeBtn = document.getElementById("closeMainsBtn");
  const modal = document.getElementById("mainsModal");

  if (openBtn && modal) {
    openBtn.addEventListener("click", async () => {
      modal.classList.remove("hidden");
      if (!mainsQuestionsData.length) {
        await loadMainsQuestionsData();
      }
      renderMainsQuestions();
      if (window.lucide) lucide.createIcons();
    });
  }

  if (closeBtn && modal) {
    closeBtn.addEventListener("click", () => {
      modal.classList.add("hidden");
    });
  }
}

async function loadMainsQuestionsData() {
  try {
    const res = await fetch(`${API_BASE}/api/mains/questions`);
    const data = await res.json();
    if (data.success) {
      mainsQuestionsData = data.questions || [];
    }
  } catch (e) {
    console.error("Error loading mains data:", e);
  }
}

function renderMainsQuestions() {
  const container = document.getElementById("mainsQuestionsContainer");
  if (!container) return;
  container.innerHTML = "";

  mainsQuestionsData.forEach((q, idx) => {
    const card = document.createElement("div");
    card.className = "p-5 rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-850 shadow-sm space-y-3.5";

    const a = q.model_answer;
    const bodyPointsHtml = a.body_points.map(p => `<li class="leading-relaxed">${p}</li>`).join("");

    card.innerHTML = `
      <div class="flex flex-wrap justify-between items-center gap-2 border-b border-slate-100 dark:border-slate-800 pb-2.5">
        <div class="flex items-center gap-2">
          <span class="bg-violet-100 text-violet-800 dark:bg-violet-950/60 dark:text-violet-300 text-[10px] font-black px-2.5 py-1 rounded-full uppercase">${q.paper}</span>
          <span class="text-xs font-bold text-slate-500 dark:text-slate-400">${q.subject}</span>
        </div>
        <span class="text-xs font-extrabold text-violet-700 dark:text-violet-400">10 మార్కులు (150 పదాలు)</span>
      </div>

      <h3 class="text-sm sm:text-base font-black text-slate-900 dark:text-white leading-snug">
        ${idx + 1}. ${q.question}
      </h3>

      <div class="space-y-3 pt-2">
        <div class="p-3 rounded-2xl bg-blue-50/70 dark:bg-blue-950/20 border border-blue-100 dark:border-blue-900/40 text-xs sm:text-sm">
          <span class="font-black text-blue-900 dark:text-blue-300 block mb-1">📌 1. పరిచయం (Introduction & Context):</span>
          <p class="text-slate-800 dark:text-slate-200 leading-relaxed">${a.intro}</p>
        </div>

        <div class="p-3.5 rounded-2xl bg-slate-50 dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 text-xs sm:text-sm">
          <span class="font-black text-slate-900 dark:text-slate-100 block mb-1.5">📊 2. ముఖ్య విశ్లేషణ & అంశాలు (Core Body Points):</span>
          <ul class="space-y-2 text-slate-800 dark:text-slate-200 pl-1 list-disc ml-3">
            ${bodyPointsHtml}
          </ul>
        </div>

        <div class="p-3 rounded-2xl bg-emerald-50/70 dark:bg-emerald-950/20 border border-emerald-100 dark:border-emerald-900/40 text-xs sm:text-sm">
          <span class="font-black text-emerald-900 dark:text-emerald-300 block mb-1">🏛️ 3. ప్రభుత్వ చర్యలు & విధానాలు (Government Initiatives):</span>
          <p class="text-slate-800 dark:text-slate-200 leading-relaxed">${a.govt_steps}</p>
        </div>

        <div class="p-3 rounded-2xl bg-purple-50/70 dark:bg-purple-950/20 border border-purple-100 dark:border-purple-900/40 text-xs sm:text-sm">
          <span class="font-black text-purple-900 dark:text-purple-300 block mb-1">🎯 4. ముందున్న సవాళ్లు & ముగింపు (Way Forward & Conclusion):</span>
          <p class="text-slate-800 dark:text-slate-200 leading-relaxed">${a.conclusion}</p>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}


