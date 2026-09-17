# -*- coding: utf-8 -*-
"""
Compiles Supreme Court 30 Landmark Judgments Handbook PDF using Microsoft Edge Headless engine.
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

from sc_judgments_data import get_all_landmark_judgments

pdf_output_path = os.path.join(base_dir, "frontend", "pdfs", "supreme_court_landmark_cases_handbook.pdf")
os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)

judgments = get_all_landmark_judgments()

cards_html = ""
for idx, j in enumerate(judgments, 1):
    cards_html += f"""
    <div style="page-break-inside: avoid; margin-bottom: 20px; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px 16px; background: #ffffff;">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 10px;">
            <div>
                <span style="background: #4f46e5; color: white; font-size: 10px; font-weight: 800; padding: 2px 8px; border-radius: 4px; text-transform: uppercase;">తీర్పు #{idx:02d}</span>
                <span style="font-size: 11px; font-weight: 700; color: #64748b; margin-left: 8px;">📂 {j['category']}</span>
                <h3 style="font-size: 14px; font-weight: 900; color: #0f172a; margin: 6px 0 0 0;">{j['case_name']}</h3>
            </div>
            <span style="background: #f1f5f9; border: 1px solid #cbd5e1; color: #1e293b; font-size: 11px; font-weight: 800; padding: 3px 10px; border-radius: 6px; white-space: nowrap;">సంవత్సరం: {j['year']}</span>
        </div>

        <div style="display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 10px; font-size: 10px;">
            <span style="background: #eef2ff; color: #4338ca; padding: 2px 8px; border-radius: 4px; font-weight: 700;"><b>🏛️ ధర్మాసనం:</b> {j['bench']}</span>
            <span style="background: #ecfdf5; color: #065f46; padding: 2px 8px; border-radius: 4px; font-weight: 700;"><b>⚖️ రేషియో:</b> {j['ratio']}</span>
            <span style="background: #fef3c7; color: #92400e; padding: 2px 8px; border-radius: 4px; font-weight: 700;"><b>📜 ఆర్టికల్స్:</b> {j['articles']}</span>
        </div>

        <div style="background: #f8fafc; border-left: 4px solid #3b82f6; padding: 8px 12px; margin-bottom: 10px; font-size: 11px; line-height: 1.6; color: #1e293b;">
            <b style="color: #1d4ed8;">⚖️ ప్రధాన తీర్పు (Core Ruling):</b><br>
            {j['core_verdict']}
        </div>

        <div style="background: #fffbeb; border: 1px solid #fef3c7; border-radius: 6px; padding: 8px 12px; margin-bottom: 10px; font-size: 10.5px; line-height: 1.5; color: #78350f;">
            <b style="color: #b45309;">🎯 పరీక్షల ప్రాధాన్యత & రాజ్యాంగ ప్రభావం:</b><br>
            {j['exam_significance']}<br>
            <span style="color: #475569; font-size: 10px; margin-top: 4px; display: inline-block;">
                <b>మౌలిక సూత్రాలు:</b> {j['basic_structure_elements']}
            </span>
        </div>

        <div style="background: #f1f5f9; border-radius: 6px; padding: 8px 12px; font-size: 10px; color: #334155;">
            <b>❓ మోడల్ ప్రశ్న:</b> {j['mcq']['q']}<br>
            <span style="color: #047857; font-weight: 700; margin-top: 3px; display: inline-block;">✓ సమాధానం: {j['mcq']['ans']}</span> — <i>{j['mcq']['exp']}</i>
        </div>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>సుప్రీంకోర్టు 30 చారిత్రక తీర్పుల మాస్టర్ హ్యాండ్‌బుక్</title>
    <style>
        @page {{
            size: A4 portrait;
            margin: 14mm 12mm 14mm 12mm;
            @bottom-right {{
                content: counter(page);
            }}
        }}
        body {{
            font-family: 'Nirmala UI', 'Segoe UI', Tahoma, sans-serif;
            color: #0f172a;
            background: #ffffff;
            margin: 0;
            padding: 0;
            -webkit-print-color-adjust: exact;
            print-color-adjust: exact;
        }}
        .cover-header {{
            background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 24px;
        }}
        .cover-header h1 {{
            font-size: 22px;
            margin: 0 0 8px 0;
            font-weight: 900;
            letter-spacing: -0.5px;
        }}
        .cover-header p {{
            font-size: 12px;
            margin: 0;
            color: #c7d2fe;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="cover-header">
        <div style="font-size: 11px; font-weight: 800; color: #fbbf24; text-transform: uppercase; margin-bottom: 4px;">లక్ష్య APPSC / TSPSC 2026 ఎడిషన్</div>
        <h1>⚖️ భారత సుప్రీంకోర్టు 30 చారిత్రక తీర్పులు (1950–2026)</h1>
        <p>రాజ్యాంగ మౌలిక స్వరూప సిద్ధాంతం, ప్రాథమిక హక్కులు, రిజర్వేషన్లు, సమాఖ్య వ్యవస్థ, ఎన్నికల సంస్కరణలపై సంపూర్ణ హ్యాండ్‌బుక్</p>
    </div>

    {cards_html}

    <div style="text-align: center; margin-top: 24px; padding-top: 14px; border-top: 1px solid #cbd5e1; font-size: 10px; color: #64748b;">
        © 2026 లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రిపరేషన్ పోర్టల్ | APPSC Group-1, Group-2, TSPSC & UPSC స్టడీ మెటీరియల్
    </div>
</body>
</html>
"""

temp_html_path = os.path.join(base_dir, "backend", "temp_sc_judgments.html")
with open(temp_html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

print("Temp HTML written, generating PDF via Edge Headless...")
edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
if not os.path.exists(edge_path):
    edge_path = r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"

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
if os.path.exists(pdf_output_path):
    size_mb = os.path.getsize(pdf_output_path) / (1024 * 1024)
    print(f"SUCCESS: Generated PDF at {pdf_output_path} (Size: {size_mb:.2f} MB)")
else:
    print(f"FAILED to generate PDF. Stderr: {res.stderr}")

if os.path.exists(temp_html_path):
    os.remove(temp_html_path)
