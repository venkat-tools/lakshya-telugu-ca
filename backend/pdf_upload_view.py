# -*- coding: utf-8 -*-
"""
HTML View Renderer for Educational PDF Uploader & Digital Library Hub (/pdf_upload_hub)
"""

from db import get_uploaded_materials, get_available_dates
from datetime import datetime

def render_pdf_upload_html():
    materials = get_uploaded_materials()
    dates = get_available_dates()
    today_str = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")

    cat_badge_colors = {
        "education": "bg-blue-100 text-blue-900 border-blue-300",
        "regional": "bg-emerald-100 text-emerald-900 border-emerald-300",
        "economy": "bg-amber-100 text-amber-900 border-amber-300",
        "national": "bg-indigo-100 text-indigo-900 border-indigo-300",
        "science_tech": "bg-purple-100 text-purple-900 border-purple-300",
        "mock_tests": "bg-rose-100 text-rose-900 border-rose-300",
        "history": "bg-orange-100 text-orange-900 border-orange-300"
    }

    materials_cards = ""
    if materials:
        for m in materials:
            cat = m.get("category", "education")
            badge_class = cat_badge_colors.get(cat, "bg-slate-100 text-slate-800 border-slate-300")
            size_mb = round(m["file_size"] / (1024 * 1024), 2) if m.get("file_size") else 0
            materials_cards += f"""
            <div class="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition flex flex-col justify-between" id="mat-card-{m['id']}">
                <div>
                    <div class="flex justify-between items-start gap-2 mb-3">
                        <span class="text-xs font-black px-2.5 py-1 rounded-lg border {badge_class}">
                            {m.get('category', 'విద్యా మెటీరియల్').upper()}
                        </span>
                        <span class="text-[11px] text-slate-400 font-semibold">{m.get('uploaded_at', '')[:16]}</span>
                    </div>
                    <h3 class="text-base font-black text-slate-900 mb-2 leading-snug">
                        {m['title']}
                    </h3>
                    <div class="text-xs text-slate-500 space-y-1 mb-4">
                        <p class="flex items-center gap-1.5">
                            <span>📄 పేజీలు:</span> <b class="text-slate-800">{m.get('total_pages', 1)}</b> | 
                            <span>💾 సైజు:</span> <b class="text-slate-800">{size_mb} MB</b>
                        </p>
                        <p class="flex items-center gap-1.5 text-emerald-700 font-bold">
                            <span>⚡ వెబ్‌సైట్ సింక్:</span> 
                            <span>{m.get('articles_created', 0)} ఆర్టికల్స్ • {m.get('quizzes_created', 0)} క్విజ్ ప్రశ్నలు</span>
                        </p>
                    </div>
                    <div class="bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs text-slate-600 line-clamp-3 mb-4 leading-relaxed">
                        {m.get('extracted_summary', 'ముఖ్య సమాచారం సేకరించబడింది.')}
                    </div>
                </div>
                <div class="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                    <a href="/pdfs/uploads/{m['filename']}" target="_blank" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white py-2 px-3 rounded-xl text-xs font-bold text-center transition flex items-center justify-center gap-1.5 shadow-xs">
                        <span>📖 ఓపెన్</span>
                    </a>
                    <a href="/api/omr_test_print?material_id={m['id']}" target="_blank" class="bg-indigo-50 hover:bg-indigo-100 text-indigo-700 py-2 px-2.5 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1" title="ఈ మెటీరియల్ నుండి OMR మాక్ టెస్ట్ పేపర్ తయారు చేయండి">
                        <span>🖨️ OMR</span>
                    </a>
                    <a href="/pdfs/uploads/{m['filename']}" download class="bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 px-2.5 rounded-xl text-xs font-bold transition flex items-center justify-center" title="డౌన్‌లోడ్">
                        <span>📥</span>
                    </a>
                    <button onclick="confirmDeleteMaterial({m['id']}, '{m.get('title', '').replace(chr(39), '').replace(chr(34), '')[:30]}')" class="admin-only-action hidden bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-700 border border-rose-200 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-1 cursor-pointer" title="ఈ PDF ని డిలీట్ చేయండి">
                        <span>🗑️ డిలీట్</span>
                    </button>
                </div>
            </div>
            """
    else:
        materials_cards = """
        <div class="col-span-full bg-white rounded-2xl border border-dashed border-slate-300 p-12 text-center text-slate-500">
            <div class="w-16 h-16 rounded-full bg-blue-50 text-blue-600 flex items-center justify-center text-2xl mx-auto mb-3">📚</div>
            <h4 class="text-base font-bold text-slate-800">ఇంకా ఎలాంటి స్టడీ PDF లు అప్‌లోడ్ కాలేదు</h4>
            <p class="text-xs text-slate-500 mt-1">పై ఫారమ్ ద్వారా మీ మొదటి నోటిఫికేషన్ లేదా స్టడీ PDF ని అప్‌లోడ్ చేయండి.</p>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📤 స్టడీ PDF అప్‌లోడ్ & వెబ్‌సైట్ ఆటో-సింక్ హబ్ | లక్ష్య కరెంట్ అఫైర్స్</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@400;600;700;800&family=Noto+Sans+Telugu:wght@400;600;700;800;900&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans Telugu', 'Outfit', sans-serif;
            background-color: #f8fafc;
            color: #0f172a;
        }}
    </style>
</head>
<body class="min-h-screen pb-16">

    <!-- Top Navigation Bar -->
    <header class="bg-white border-b border-slate-200 sticky top-0 z-30 shadow-xs">
        <div class="max-w-6xl mx-auto px-4 py-3 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <a href="/" class="w-10 h-10 rounded-xl bg-blue-600 hover:bg-blue-700 flex items-center justify-center text-white font-black transition shadow-sm" title="హోమ్‌కు తిరిగి వెళ్లండి">
                    ←
                </a>
                <div>
                    <h1 class="text-lg font-black text-slate-900 flex items-center gap-2">
                        <span>📤</span> స్టడీ PDF అప్‌లోడ్ & ఆటో-సింక్ హబ్
                    </h1>
                    <p class="text-xs text-slate-500">విద్యా PDF ల అప్‌లోడ్ • ఆటోమేటిక్ వెబ్‌సైట్ & క్విజ్ అప్‌డేట్</p>
                </div>
            </div>
            <div class="flex items-center gap-2">
                <button id="adminAuthBtn" onclick="handleAdminAuthClick()" class="text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-200 px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-2xs">
                    <span id="adminAuthIcon">🔒</span> <span id="adminAuthText">అడ్మిన్ లాగిన్</span>
                </button>
                <a href="/" class="text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-xl transition">
                    🌐 డ్యాష్‌బోర్డ్
                </a>
            </div>
        </div>
    </header>

    <main class="max-w-6xl mx-auto px-4 mt-8 space-y-8">

        <!-- Banner Explaining Auto-Sync -->
        <div class="bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 text-white p-6 rounded-3xl shadow-lg relative overflow-hidden">
            <div class="relative z-10 max-w-3xl">
                <div class="inline-flex items-center gap-1.5 bg-white/20 text-white text-xs font-black px-3 py-1 rounded-full mb-3 backdrop-blur-xs">
                    <span>⚡ ఇంటెలిజెంట్ PDF ఇంజిన్</span>
                </div>
                <h2 class="text-xl sm:text-2xl font-black mb-2">
                    మీరు స్టడీ PDF అప్‌లోడ్ చేయగానే వెబ్‌సైట్ స్వయంచాలకంగా అప్‌డేట్ అవుతుంది!
                </h2>
                <p class="text-xs sm:text-sm text-blue-100 leading-relaxed">
                    APPSC/TSPSC నోటిఫికేషన్లు, ప్రభుత్వ సంక్షేమ జీవోలు, కరెంట్ అఫైర్స్ నోట్స్ లేదా మోడల్ పేపర్స్ PDF ని ఇక్కడ అప్‌లోడ్ చేయండి. పైథాన్ ఇంజిన్ ఆటోమేటిక్‌గా అందులోని సమాచారాన్ని సంగ్రహించి వెబ్‌సైట్‌లోని ఆర్టికల్స్, వన్‌లైనర్స్ మరియు క్విజ్ ప్రశ్నలను తక్షణమే అప్‌డేట్ చేస్తుంది.
                </p>
            </div>
        </div>

        <!-- Font Compatibility & Legacy DTP Guide Box -->
        <div class="bg-amber-50/90 border border-amber-200/80 rounded-2xl p-4 sm:p-5 shadow-xs flex flex-col sm:flex-row items-start gap-3.5">
            <div class="w-10 h-10 rounded-xl bg-amber-500 text-slate-950 font-black flex items-center justify-center text-lg shrink-0 shadow-xs">
                💡
            </div>
            <div class="space-y-1 text-xs sm:text-sm">
                <h4 class="font-black text-amber-950 flex items-center gap-2">
                    <span>తెలుగు PDF ఫాంట్ మార్గదర్శకాలు (PDF Font Compatibility):</span>
                </h4>
                <p class="text-amber-900 leading-relaxed">
                    • <b>డిజిటల్ యూనికోడ్ PDF లు:</b> నేటి వార్తాపత్రికలు, డిజిటల్ నోట్స్, ప్రభుత్వ జీవోలు మరియు ఆధునిక పుస్తకాల PDF లు 100% స్వచ్ఛమైన తెలుగులో ఆటోమేటిక్‌గా అప్‌డేట్ అవుతాయి.<br>
                    • <b>పాత DTP ఫాంట్లు (Anu Script / Shree-Lipi):</b> పాత గ్రూప్స్ ప్రశ్నపత్రాలు లేదా పుస్తకాలలోని పాత 8-బిట్ ఫాంట్లలో ఉన్న టెక్స్ట్‌ను మా సిస్టమ్ ఆటోమేటిక్‌గా గుర్తించి యూనికోడ్ తెలుగులోకి కన్వర్ట్ చేసి చూపిస్తుంది.
                </p>
            </div>
        </div>

        <!-- Uploader Card -->
        <div class="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
            <h3 class="text-lg font-black text-slate-900 mb-4 flex items-center gap-2">
                <span>📁</span> నూతన విద్యా PDF ని అప్‌లోడ్ చేయండి (Upload Educational PDF)
            </h3>

            <form id="pdfUploadForm" onsubmit="handlePdfUpload(event)" class="space-y-6">
                
                <!-- Drag and drop zone -->
                <div id="dropZone" onclick="document.getElementById('pdfFileInput').click()" class="border-2 border-dashed border-blue-300 hover:border-blue-600 bg-blue-50/50 hover:bg-blue-50/80 rounded-2xl p-8 text-center cursor-pointer transition flex flex-col items-center justify-center gap-3">
                    <input type="file" id="pdfFileInput" accept=".pdf,application/pdf" class="hidden" onchange="handleFileSelect(this)" />
                    <div class="w-14 h-14 rounded-2xl bg-blue-600 text-white flex items-center justify-center text-2xl shadow-md">
                        📄
                    </div>
                    <div>
                        <p class="text-sm font-black text-slate-800" id="selectedFileName">
                            ఇక్కడ PDF ఫైల్‌ను డ్రాప్ చేయండి లేదా క్లిక్ చేసి ఎంచుకోండి
                        </p>
                        <p class="text-xs text-slate-400 mt-1">గరిష్ట పరిమాణం: 100 MB వరకు • .pdf ఫార్మాట్ మాత్రమే</p>
                    </div>
                </div>

                <!-- Form Controls Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1.5">
                            📚 మెటీరియల్ శీర్షిక (Title - ఖాళీగా ఉంచితే PDF నుంచి ఆటోమేటిక్‌గా తీసుకుంటుంది):
                        </label>
                        <input type="text" id="pdfTitle" placeholder="ఉదా: APPSC గ్రూప్-2 నోటిఫికేషన్ & సిలబస్ 2026..." class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm font-semibold text-slate-800 outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white" />
                    </div>

                    <div>
                        <label class="block text-xs font-bold text-slate-700 mb-1.5">
                            📂 సబ్జెక్ట్ / విభాగం (Category):
                        </label>
                        <select id="pdfCategory" class="w-full bg-slate-50 border border-slate-200 rounded-xl px-3.5 py-2.5 text-xs sm:text-sm font-bold text-slate-800 outline-none focus:ring-2 focus:ring-blue-500 focus:bg-white cursor-pointer">
                            <option value="education">🎓 విద్యా, ఉద్యోగాలు & నోటిఫికేషన్లు (Education & Notifications)</option>
                            <option value="regional">🌾 ప్రభుత్వ సంక్షేమ పథకాలు & పాలసీలు (AP & TS Schemes)</option>
                            <option value="national">🏛️ భారత రాజ్యాంగం, పాలిటీ & జాతీయం (Polity & National)</option>
                            <option value="economy">📈 భారత & తెలుగు రాష్ట్రాల ఆర్థిక వ్యవస్థ (Economy & Banking)</option>
                            <option value="science_tech">🚀 సైన్స్, టెక్నాలజీ, ఇస్రో & పర్యావరణం (Science & Tech)</option>
                            <option value="history">📜 భారత & ఆంధ్రప్రదేశ్ సమగ్ర చరిత్ర (History)</option>
                            <option value="mock_tests">📝 మాక్ టెస్ట్‌లు & మోడల్ పేపర్స్ (Mock Tests & PYQs)</option>
                        </select>
                    </div>
                </div>

                <!-- Sync Checkboxes -->
                <div class="bg-blue-50/60 p-4 rounded-2xl border border-blue-200 space-y-2">
                    <div class="flex items-center justify-between">
                        <h4 class="text-xs font-black text-blue-950 flex items-center gap-1.5">
                            <span>🛡️</span> డిజిటల్ లైబ్రరీ & భద్రత:
                        </h4>
                        <span class="text-[11px] font-bold text-blue-700 bg-blue-100/80 px-2 py-0.5 rounded-md">కరెంట్ అఫైర్స్ సురక్షితం</span>
                    </div>
                    <p class="text-[11px] text-slate-600 leading-relaxed">
                        అప్‌లోడ్ చేసిన స్టడీ PDF లు ప్రత్యేకంగా <b>డిజిటల్ లైబ్రరీ</b> మరియు <b>1-Click OMR మాక్ టెస్ట్ హబ్</b> లో మాత్రమే భద్రపరచబడతాయి. నేటి ఈ-పేపర్ మరియు డైలీ కరెంట్ అఫైర్స్ ఫీడ్‌తో కలవవు.
                    </p>
                    <div class="flex flex-wrap gap-4 text-xs font-semibold text-slate-600 pt-1">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="syncArticles" class="w-3.5 h-3.5 text-blue-600 rounded border-slate-300 focus:ring-blue-500" />
                            <span>వెబ్‌సైట్ స్టడీ నోట్స్ గా సింక్ చేయి (ఐచ్ఛికం)</span>
                        </label>
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="syncQuizzes" class="w-3.5 h-3.5 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500" />
                            <span>ప్రాక్టీస్ MCQs జనరేట్ చేయి (ఐచ్ఛికం)</span>
                        </label>
                    </div>
                </div>

                <!-- Upload Action & Student Notice -->
                <div class="flex flex-wrap items-center justify-between gap-4 pt-2">
                    <div class="text-xs text-slate-500 flex items-center gap-1.5">
                        <span class="text-base">🎓</span> <span>విద్యార్థులు & అధ్యాపకులు ఎవరైనా తమ స్టడీ PDF లను సులభంగా అప్‌లోడ్ చేయవచ్చు</span>
                    </div>

                    <button type="submit" id="uploadSubmitBtn" class="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white font-black px-6 py-3 rounded-2xl text-xs sm:text-sm shadow-md transition flex items-center gap-2 cursor-pointer">
                        <span>📤 PDF అప్‌లోడ్ చేసి లైబ్రరీకి జోడించండి</span>
                    </button>
                </div>
            </form>

            <!-- Live Status Alert Box -->
            <div id="uploadStatusBox" class="hidden mt-6 p-4 rounded-2xl border text-xs leading-relaxed"></div>
        </div>

        <!-- Digital Library of Uploaded PDFs -->
        <div>
            <div class="flex justify-between items-center mb-4 flex-wrap gap-3">
                <div>
                    <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
                        <span>📚</span> అప్‌లోడ్ చేసిన స్టడీ మెటీరియల్స్ లైబ్రరీ ({len(materials)} డాక్యుమెంట్లు)
                    </h3>
                    <p class="text-xs text-slate-500">వెబ్‌సైట్ ద్వారా లైవ్‌గా చదువుకోవచ్చు లేదా PDF డౌన్‌లోడ్ చేసుకోవచ్చు</p>
                </div>
                {f'''<button onclick="purgeAllMaterials()" class="admin-only-action hidden bg-rose-50 hover:bg-rose-600 hover:text-white text-rose-700 border border-rose-200 px-3 py-2 rounded-xl text-xs font-bold transition flex items-center gap-1.5 cursor-pointer shadow-2xs">
                    <span>🧹 అన్ని PDF లు తొలగించు</span>
                </button>''' if materials else ''}
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5" id="materialsGrid">
                {materials_cards}
            </div>
        </div>

    </main>

    <script>
        function handleFileSelect(input) {{
            if (input.files && input.files[0]) {{
                const file = input.files[0];
                const sizeMB = (file.size / (1024 * 1024)).toFixed(2);
                document.getElementById('selectedFileName').innerHTML = `
                    <span class="text-blue-700 font-black">📄 ${{file.name}}</span> 
                    <span class="text-xs text-slate-500">(${{sizeMB}} MB)</span>
                `;
            }}
        }}

        async function handlePdfUpload(e) {{
            e.preventDefault();
            const fileInput = document.getElementById('pdfFileInput');
            if (!fileInput.files || !fileInput.files[0]) {{
                alert('దయచేసి అప్‌లోడ్ చేయడానికి ఒక PDF ఫైల్‌ను ఎంచుకోండి.');
                return;
            }}
            const file = fileInput.files[0];
            const sizeMB = file.size / (1024 * 1024);
            if (sizeMB > 100) {{
                alert('ఈ PDF ఫైల్ సైజ్ చాలా పెద్దది (' + sizeMB.toFixed(1) + ' MB). వెబ్‌సైట్ అప్‌లోడ్ గరిష్ట పరిమితి 100 MB.\\n\\nచిట్కా: PDF ని ఆన్‌లైన్‌లో కంప్రెస్ చేసి అప్‌లోడ్ చేయండి లేదా నేరుగా టెలిగ్రామ్ బోట్ (@venkat_telugu_ca_bot) కు పంపండి (టెలిగ్రామ్‌లో 2000 MB వరకు అనుమతి ఉంది).');
                return;
            }}

            const btn = document.getElementById('uploadSubmitBtn');
            const statusBox = document.getElementById('uploadStatusBox');
            btn.disabled = true;
            btn.innerHTML = '⏳ PDF ని రీడ్ చేసి వెబ్‌సైట్‌ను అప్‌డేట్ చేస్తోంది... దయచేసి వేచి ఉండండి...';
            statusBox.className = 'mt-6 p-4 rounded-2xl border bg-blue-50 border-blue-200 text-blue-900 text-xs flex items-center gap-2';
            statusBox.innerHTML = '<span>⏳ ఫైల్ అప్‌లోడ్ అవుతోంది, pypdf ద్వారా టెక్స్ట్ విశ్లేషణ మరియు డేటాబేస్ సింకింగ్ జరుగుతోంది...</span>';
            statusBox.classList.remove('hidden');

            const formData = new FormData();
            formData.append('file', fileInput.files[0]);
            formData.append('title', document.getElementById('pdfTitle').value);
            formData.append('category', document.getElementById('pdfCategory').value);
            formData.append('sync_articles', document.getElementById('syncArticles').checked ? '1' : '0');
            formData.append('sync_quizzes', document.getElementById('syncQuizzes').checked ? '1' : '0');

            try {{
                const res = await fetch('/api/upload_pdf', {{
                    method: 'POST',
                    body: formData
                }});

                let data;
                const contentType = res.headers.get("content-type") || "";
                if (contentType.includes("application/json")) {{
                    data = await res.json();
                }} else {{
                    if (res.status === 502 || res.status === 503) {{
                        throw new Error("సర్వర్ నూతన అప్‌డేట్‌తో రీస్టార్ట్ అవుతోంది. దయచేసి 30 సెకన్ల తర్వాత మళ్లీ అప్‌లోడ్ చేయండి.");
                    }} else if (res.status === 504) {{
                        throw new Error("ఫైల్ ప్రాసెస్ కావడానికి సమయం పట్టింది. దయచేసి తక్కువ పేజీలు గల PDF ని అప్‌లోడ్ చేయండి.");
                    }} else if (res.status === 413) {{
                        throw new Error("ఫైల్ పరిమాణం చాలా పెద్దది (గరిష్టంగా 50MB వరకు మాత్రమే).");
                    }} else {{
                        throw new Error("సర్వర్ నుండి సరైన సమాధానం రాలేదు (" + res.status + "). దయచేసి కొద్దిసేపటి తర్వాత మళ్లీ ప్రయత్నించండి.");
                    }}
                }}

                if (data && data.success) {{
                    statusBox.className = 'mt-6 p-4 rounded-2xl border bg-emerald-50 border-emerald-300 text-emerald-950 text-xs leading-relaxed';
                    statusBox.innerHTML = `
                        <div class="font-black text-sm text-emerald-900 mb-1">🎉 విజయం! PDF విజయవంతంగా లైబ్రరీకి జోడించబడింది!</div>
                        <div>• <b>మెటీరియల్:</b> ${{data.data.title}} (${{data.data.total_pages}} పేజీలు, ${{data.data.file_size_formatted}})</div>
                        <div class="mt-2 font-bold text-blue-700">పేజీని 2 సెకన్లలో రీలోడ్ చేస్తున్నాం...</div>
                    `;
                    setTimeout(() => {{
                        window.location.reload();
                    }}, 2000);
                }} else {{
                    statusBox.className = 'mt-6 p-4 rounded-2xl border bg-rose-50 border-rose-300 text-rose-950 text-xs';
                    statusBox.innerHTML = '<b>⚠️ లోపం:</b> ' + (data.error || 'PDF అప్‌లోడ్ చేయడం సాధ్యపడలేదు.');
                    btn.disabled = false;
                    btn.innerHTML = '📤 PDF అప్‌లోడ్ చేసి లైబ్రరీకి జోడించండి';
                }}
            }} catch (err) {{
                statusBox.className = 'mt-6 p-4 rounded-2xl border bg-rose-50 border-rose-300 text-rose-950 text-xs';
                statusBox.innerHTML = '<b>❌ సర్వర్ ఎర్రర్:</b> ' + err.message;
                btn.disabled = false;
                btn.innerHTML = '📤 PDF అప్‌లోడ్ చేసి లైబ్రరీకి జోడించండి';
            }}
        }}

        function getAdminPin() {{
            return sessionStorage.getItem('lakshya_admin_pin') || '';
        }}

        function updateAdminUI() {{
            const pin = getAdminPin();
            const isAdmin = (pin === 'lakshya2026');
            const elements = document.querySelectorAll('.admin-only-action');
            elements.forEach(el => {{
                if (isAdmin) {{
                    el.classList.remove('hidden');
                }} else {{
                    el.classList.add('hidden');
                }}
            }});

            const authBtn = document.getElementById('adminAuthBtn');
            const authIcon = document.getElementById('adminAuthIcon');
            const authText = document.getElementById('adminAuthText');
            if (authBtn && authIcon && authText) {{
                if (isAdmin) {{
                    authBtn.className = 'text-xs font-bold text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-2xs';
                    authIcon.innerText = '🔓';
                    authText.innerText = 'అడ్మిన్ లాగౌట్';
                    authBtn.title = 'అడ్మిన్ మోడ్ నుండి లాగౌట్ అవ్వండి';
                }} else {{
                    authBtn.className = 'text-xs font-bold text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-200 px-3 py-1.5 rounded-xl transition flex items-center gap-1.5 cursor-pointer shadow-2xs';
                    authIcon.innerText = '🔒';
                    authText.innerText = 'అడ్మిన్ లాగిన్';
                    authBtn.title = 'PDF లను తొలగించడానికి అడ్మిన్ లాగిన్ చేయండి';
                }}
            }}
        }}

        function handleAdminAuthClick() {{
            const currentPin = getAdminPin();
            if (currentPin === 'lakshya2026') {{
                if (confirm('అడ్మిన్ మోడ్ నుండి లాగౌట్ అవ్వాలనుకుంటున్నారా?')) {{
                    sessionStorage.removeItem('lakshya_admin_pin');
                    updateAdminUI();
                    alert('అడ్మిన్ మోడ్ లాగౌట్ చేయబడింది. ప్రస్తుతం సాధారణ విద్యార్థి మోడ్ సక్రియంగా ఉంది.');
                }}
                return;
            }}

            const entered = prompt('దయచేసి అడ్మిన్ పిన్ (Admin PIN) నమోదు చేయండి (కేవలం అడ్మిన్ కొరకు మాత్రమే):');
            if (!entered) return;
            if (entered.trim() === 'lakshya2026') {{
                sessionStorage.setItem('lakshya_admin_pin', 'lakshya2026');
                updateAdminUI();
                alert('✅ అడ్మిన్ మోడ్ విజయవంతంగా ఆక్టివేట్ అయింది. ఇప్పుడు మీరు అవసరమైన PDF లను తొలగించవచ్చు.');
            }} else {{
                alert('❌ తప్పుడు పిన్! విద్యార్థులకు PDF లను తొలగించే అనుమతి లేదు.');
            }}
        }}

        async function confirmDeleteMaterial(id, title) {{
            const pin = getAdminPin();
            if (pin !== 'lakshya2026') {{
                alert('⚠️ PDF లను తొలగించడానికి కేవలం అడ్మిన్‌కు మాత్రమే అనుమతి ఉంది. దయచేసి పైన ఉన్న "అడ్మిన్ లాగిన్" ద్వారా లాగిన్ అవ్వండి.');
                return;
            }}

            const displayTitle = title ? '"' + title + '"' : 'ఈ స్టడీ PDF';
            if (!confirm(displayTitle + ' ని సర్వర్ మరియు లైబ్రరీ నుండి ఖచ్చితంగా తొలగించాలనుకుంటున్నారా?')) return;

            try {{
                const res = await fetch('/api/uploaded_materials/' + id + '?pin=' + encodeURIComponent(pin), {{
                    method: 'DELETE'
                }});
                const data = await res.json();
                if (data && data.success) {{
                    const el = document.getElementById('mat-card-' + id);
                    if (el) {{
                        el.style.transition = 'all 0.3s ease';
                        el.style.opacity = '0';
                        el.style.transform = 'scale(0.9)';
                        setTimeout(() => el.remove(), 300);
                    }}
                    alert('✅ స్టడీ మెటీరియల్ విజయవంతంగా తొలగించబడింది.');
                }} else {{
                    alert('⚠️ లోపం: ' + (data.error || 'తొలగించడం సాధ్యపడలేదు.'));
                }}
            }} catch (e) {{
                alert('ఎర్రర్: ' + e.message);
            }}
        }}

        const deleteMaterial = confirmDeleteMaterial;

        async function purgeAllMaterials() {{
            const pin = getAdminPin();
            if (pin !== 'lakshya2026') {{
                alert('⚠️ అన్ని PDF లను తొలగించడానికి కేవలం అడ్మిన్‌కు మాత్రమే అనుమతి ఉంది.');
                return;
            }}

            if (!confirm('లైబ్రరీలోని అన్ని అప్‌లోడ్ చేసిన స్టడీ PDF ఫైళ్లను ఖచ్చితంగా తొలగించాలనుకుంటున్నారా?')) return;

            try {{
                const res = await fetch('/api/uploaded_materials/purge_all?pin=' + encodeURIComponent(pin), {{
                    method: 'POST'
                }});
                const data = await res.json();
                if (data && data.success) {{
                    alert('✅ ' + data.message);
                    window.location.reload();
                }} else {{
                    alert('⚠️ లోపం: ' + (data.error || 'తొలగించడం సాధ్యపడలేదు.'));
                }}
            }} catch (e) {{
                alert('ఎర్రర్: ' + e.message);
            }}
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            const urlParams = new URLSearchParams(window.location.search);
            if (urlParams.get('admin') === 'lakshya2026') {{
                sessionStorage.setItem('lakshya_admin_pin', 'lakshya2026');
            }}
            updateAdminUI();
        }});
    </script>
</body>
</html>
"""
    return html
