# -*- coding: utf-8 -*-
"""
Generates the comprehensive Static GK Master Pocketbook PDF
using Microsoft Edge Headless engine.
"""

import os
import sys
import subprocess

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

base_dir = r"C:\Users\venkat\.gemini\antigravity\scratch\daily_current_affairs_telugu"
sys.path.insert(0, os.path.join(base_dir, "backend"))

from static_gk_data import STATIC_GK_CATEGORIES

pdf_output_path = os.path.join(base_dir, "frontend", "pdfs", "static_gk_master_pocketbook.pdf")
os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)

categories_html = ""
for c in STATIC_GK_CATEGORIES:
    items_rows = ""
    for idx, item in enumerate(c["items"], 1):
        bg = "#ffffff" if idx % 2 == 1 else "#f8fafc"
        items_rows += f"""
        <tr style="background:{bg}; border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 7px 10px; font-weight: 600; color: #334155; font-size: 11px; width: 45%;">{item['label']}</td>
            <td style="padding: 7px 10px; font-weight: 700; color: #0f172a; font-size: 11px;">{item['value']}</td>
        </tr>
        """

    categories_html += f"""
    <div style="page-break-inside: avoid; margin-bottom: 22px; border: 1px solid #cbd5e1; border-radius: 8px; overflow: hidden; background:#ffffff;">
        <div style="background: #1e3a8a; color: #ffffff; padding: 8px 12px; font-size: 13px; font-weight: 800; display:flex; justify-content:space-between; align-items:center;">
            <span>📌 {c['title']}</span>
            <span style="background: rgba(255,255,255,0.2); font-size: 10px; padding: 2px 8px; border-radius: 10px;">{c['badge']}</span>
        </div>
        <table style="width: 100%; border-collapse: collapse; text-align: left;">
            <tbody>
                {items_rows}
            </tbody>
        </table>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>లక్ష్య స్టాటిక్ జీకే మాస్టర్ పాకెట్‌బుక్ 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4;
            margin: 12mm 12mm 12mm 12mm;
        }}
        body {{
            font-family: 'Outfit', 'Mandali', sans-serif;
            color: #1e293b;
            background: #ffffff;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        .cover-page {{
            text-align: center;
            padding: 50px 20px 30px;
            page-break-after: always;
            border: 6px double #0284c7;
            border-radius: 12px;
            margin-bottom: 20px;
        }}
        .watermark {{
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-35deg);
            font-size: 72px;
            font-weight: 900;
            color: rgba(2, 132, 199, 0.04);
            pointer-events: none;
            z-index: -1;
            white-space: nowrap;
        }}
        .header-strip {{
            border-bottom: 2px solid #0284c7;
            padding-bottom: 6px;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            font-size: 10px;
            color: #64748b;
            font-weight: 600;
        }}
        .footer-strip {{
            margin-top: 20px;
            border-top: 1px solid #e2e8f0;
            padding-top: 6px;
            text-align: center;
            font-size: 9px;
            color: #94a3b8;
        }}
    </style>
</head>
<body>
    <div class="watermark">LAKSHYA TELUGU CA 2026</div>

    <!-- Cover Page -->
    <div class="cover-page">
        <div style="font-size: 40px; margin-bottom: 10px;">🇮🇳 ⚡ 📖</div>
        <div style="background:#0284c7; color:#ffffff; display:inline-block; padding: 5px 18px; border-radius: 20px; font-weight:800; font-size:13px; letter-spacing:1px; margin-bottom: 18px;">
            లక్ష్య డిజిటల్ సివిల్స్ అకాడమీ
        </div>
        <h1 style="font-size: 24px; font-weight: 900; color: #0f172a; margin-bottom: 10px; line-height: 1.4;">
            భారతదేశం & ఆంధ్రప్రదేశ్<br>
            <span style="color:#0284c7;">స్టాటిక్ జీకే సూపర్-ఫాస్ట్ మాస్టర్ పాకెట్‌బుక్</span>
        </h1>
        <p style="font-size: 13px; color: #475569; max-width: 480px; margin: 0 auto 25px; line-height: 1.6;">
            APPSC, TSPSC గ్రూప్-1, గ్రూప్-2, SI, కానిస్టేబుల్, SSC CGL మరియు రైల్వే పరీక్షల కోసం రూపొందించిన సమగ్ర, అత్యంత ప్రామాణికమైన రాపిడ్ రివిజన్ పాకెట్ ఎడిషన్.
        </p>

        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 16px; max-width: 460px; margin: 0 auto 25px; text-align: left; font-size: 11px;">
            <div style="font-weight:800; color:#0369a1; margin-bottom: 6px; font-size: 12px;">🌟 ఇందులో పొందుపరచిన 8 ప్రధాన విభాగాలు:</div>
            <div>• 1. భారతదేశం & ఆంధ్రప్రదేశ్ లో ప్రథములు (రాష్ట్రపతులు, సీఎంలు, అవార్డులు)</div>
            <div>• 2. జాతీయ పార్కులు, టైగర్ రిజర్వులు, కొల్లేరు రామ్‌సర్ సైట్</div>
            <div>• 3. ప్రముఖ డ్యాములు, నదీ లోయ ప్రాజెక్టులు & పోలవరం</div>
            <div>• 4. అణు విద్యుత్ కేంద్రాలు, ఇస్రో షార్ (SHAR) & BARC, CCMB</div>
            <div>• 5. 12 మేజర్ పోర్టులు & ఆంధ్రప్రదేశ్ తీరప్రాంత ఓడరేవులు, ఎయిర్‌పోర్టులు</div>
            <div>• 6. యునెస్కో ప్రపంచ వారసత్వ ప్రదేశాలు (43 సైట్లు) & చారిత్రక ఆలయాలు</div>
            <div>• 7. 8 శాస్త్రీయ నృత్యాలు, కూచిపూడి & గిరిజన జాతరలు</div>
            <div>• 8. ఐక్యరాజ్యసమితి, డబ్ల్యూహెచ్‌ఓ, ఐఎంఎఫ్, వరల్డ్ బ్యాంక్ & సార్క్ ప్రధాన కార్యాలయాలు</div>
        </div>

        <div style="font-size: 11px; color: #64748b; font-weight: 600;">
            వెబ్ పోర్టల్: https://lakshya-telugu-ca.onrender.com/static_gk_pocketbook | టెలిగ్రామ్: /staticgk
        </div>
    </div>

    <!-- Header Strip -->
    <div class="header-strip">
        <span>లక్ష్య స్టాటిక్ జీకే సూపర్-ఫాస్ట్ పాకెట్‌బుక్ 2026</span>
        <span>అత్యున్నత పరీక్షా వాస్తవాలు (Ultra-High Yield)</span>
    </div>

    <!-- Main Categories Tables -->
    {categories_html}

    <!-- Footer -->
    <div class="footer-strip">
        © 2026 లక్ష్య తెలుగు కరెంట్ అఫైర్స్ & కాంపిటీటివ్ ఎగ్జామ్స్ పోర్టల్. All Rights Reserved.
    </div>
</body>
</html>
"""

temp_html_path = os.path.join(base_dir, "backend", "temp_static_gk_pdf.html")
with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Temporary HTML written, invoking Edge Headless to compile PDF...")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--disable-gpu",
    "--run-all-compositor-stages-before-draw",
    f"--print-to-pdf={pdf_output_path}",
    "--no-pdf-header-footer",
    temp_html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if os.path.exists(pdf_output_path):
    size_mb = os.path.getsize(pdf_output_path) / (1024 * 1024)
    print(f"SUCCESS: Generated PDF at {pdf_output_path} ({size_mb:.2f} MB)")
else:
    print("FAILED to generate PDF")
    print(res.stderr)

if os.path.exists(temp_html_path):
    os.remove(temp_html_path)
