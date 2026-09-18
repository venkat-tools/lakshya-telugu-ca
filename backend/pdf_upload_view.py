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
                    <button onclick="deleteMaterial({m['id']})" class="bg-rose-50 hover:bg-rose-100 text-rose-600 py-2 px-2.5 rounded-xl text-xs font-bold transition cursor-pointer" title="తొలగించు">
                        <span>🗑️</span>
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
                <a href="/" class="text-xs font-bold text-blue-600 bg-blue-50 hover:bg-blue-100 px-3 py-1.5 rounded-lg transition">
                    🌐 వెబ్‌సైట్ డ్యాష్‌బోర్డ్
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
                        <p class="text-xs text-slate-400 mt-1">గరిష్ట పరిమాణం: 50 MB వరకు • .pdf ఫార్మాట్ మాత్రమే</p>
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
                <div class="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-3">
                    <h4 class="text-xs font-black text-slate-800">⚙️ వెబ్‌సైట్ ఆటో-సింక్ సెట్టింగ్స్:</h4>
                    <div class="flex flex-wrap gap-4 text-xs font-bold text-slate-700">
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="syncArticles" checked class="w-4 h-4 text-blue-600 rounded border-slate-300 focus:ring-blue-500" />
                            <span>PDF లోని ముఖ్య సమాచారాన్ని వెబ్‌సైట్ ఆర్టికల్స్ & వన్‌లైనర్స్‌గా అప్‌డేట్ చేయి</span>
                        </label>
                        <label class="inline-flex items-center gap-2 cursor-pointer">
                            <input type="checkbox" id="syncQuizzes" checked class="w-4 h-4 text-emerald-600 rounded border-slate-300 focus:ring-emerald-500" />
                            <span>PDF లోని ప్రశ్నలను క్విజ్ విభాగానికి జోడించు</span>
                        </label>
                    </div>
                </div>

                <!-- Admin PIN -->
                <div class="flex flex-wrap items-center justify-between gap-4 pt-2">
                    <div class="flex items-center gap-2">
                        <label class="text-xs font-bold text-slate-500">🔒 అడ్మిన్ పిన్:</label>
                        <input type="password" id="adminPin" value="lakshya2026" class="w-32 bg-slate-50 border border-slate-200 rounded-lg px-2.5 py-1 text-xs font-bold outline-none text-slate-700" />
                    </div>

                    <button type="submit" id="uploadSubmitBtn" class="bg-gradient-to-r from-blue-600 to-indigo-700 hover:from-blue-500 hover:to-indigo-600 text-white font-black px-6 py-3 rounded-2xl text-xs sm:text-sm shadow-md transition flex items-center gap-2 cursor-pointer">
                        <span>📤 PDF అప్‌లోడ్ చేసి వెబ్‌సైట్‌ను అప్‌డేట్ చేయండి</span>
                    </button>
                </div>
            </form>

            <!-- Live Status Alert Box -->
            <div id="uploadStatusBox" class="hidden mt-6 p-4 rounded-2xl border text-xs leading-relaxed"></div>
        </div>

        <!-- Digital Library of Uploaded PDFs -->
        <div>
            <div class="flex justify-between items-center mb-4">
                <div>
                    <h3 class="text-lg font-black text-slate-900 flex items-center gap-2">
                        <span>📚</span> అప్‌లోడ్ చేసిన స్టడీ మెటీరియల్స్ లైబ్రరీ ({len(materials)} డాక్యుమెంట్లు)
                    </h3>
                    <p class="text-xs text-slate-500">వెబ్‌సైట్ ద్వారా లైవ్‌గా చదువుకోవచ్చు లేదా PDF డౌన్‌లోడ్ చేసుకోవచ్చు</p>
                </div>
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
            formData.append('admin_pin', document.getElementById('adminPin').value);

            try {{
                const res = await fetch('/api/upload_pdf', {{
                    method: 'POST',
                    body: formData
                }});
                const data = await res.json();

                if (data && data.success) {{
                    statusBox.className = 'mt-6 p-4 rounded-2xl border bg-emerald-50 border-emerald-300 text-emerald-950 text-xs leading-relaxed';
                    statusBox.innerHTML = `
                        <div class="font-black text-sm text-emerald-900 mb-1">🎉 విజయం! PDF విజయవంతంగా అప్‌లోడ్ చేయబడింది!</div>
                        <div>• <b>మెటీరియల్:</b> ${{data.data.title}} (${{data.data.total_pages}} పేజీలు, ${{data.data.file_size_formatted}})</div>
                        <div>• <b>వెబ్‌సైట్ సింక్:</b> ${{data.data.articles_created}} ఆర్టికల్స్ మరియు ${{data.data.quizzes_created}} క్విజ్ ప్రశ్నలు జోడించబడ్డాయి.</div>
                        <div class="mt-2 font-bold text-blue-700">పేజీని 2 సెకన్లలో రీలోడ్ చేస్తున్నాం...</div>
                    `;
                    setTimeout(() => {{
                        window.location.reload();
                    }}, 2000);
                }} else {{
                    statusBox.className = 'mt-6 p-4 rounded-2xl border bg-rose-50 border-rose-300 text-rose-950 text-xs';
                    statusBox.innerHTML = '<b>⚠️ లోపం:</b> ' + (data.error || 'PDF అప్‌లోడ్ చేయడం సాధ్యపడలేదు.');
                    btn.disabled = false;
                    btn.innerHTML = '📤 PDF అప్‌లోడ్ చేసి వెబ్‌సైట్‌ను అప్‌డేట్ చేయండి';
                }}
            }} catch (err) {{
                statusBox.className = 'mt-6 p-4 rounded-2xl border bg-rose-50 border-rose-300 text-rose-950 text-xs';
                statusBox.innerHTML = '<b>❌ సర్వర్ ఎర్రర్:</b> ' + err.message;
                btn.disabled = false;
                btn.innerHTML = '📤 PDF అప్‌లోడ్ చేసి వెబ్‌సైట్‌ను అప్‌డేట్ చేయండి';
            }}
        }}

        async function deleteMaterial(id) {{
            if (!confirm('ఈ స్టడీ PDF ని మరియు దాని లైబ్రరీ ఫైల్‌ను ఖచ్చితంగా తొలగించాలనుకుంటున్నారా?')) return;
            const pin = prompt('అడ్మిన్ పిన్ నమోదు చేయండి:', 'lakshya2026');
            if (!pin) return;

            try {{
                const res = await fetch('/api/uploaded_materials/' + id + '?pin=' + encodeURIComponent(pin), {{
                    method: 'DELETE'
                }});
                const data = await res.json();
                if (data && data.success) {{
                    const el = document.getElementById('mat-card-' + id);
                    if (el) el.remove();
                    alert('✅ స్టడీ మెటీరియల్ విజయవంతంగా తొలగించబడింది.');
                }} else {{
                    alert('⚠️ లోపం: ' + (data.error || 'తొలగించడం సాధ్యపడలేదు.'));
                }}
            }} catch (e) {{
                alert('ఎర్రర్: ' + e.message);
            }}
        }}
    </script>
</body>
</html>
"""
    return html
