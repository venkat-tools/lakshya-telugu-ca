# -*- coding: utf-8 -*-
"""
Compiles AP & TS Agriculture, Irrigation & Aquaculture Master Guide PDF via Edge Headless.
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

from agri_irrigation_data import get_agri_irrigation_data

pdf_output_path = os.path.join(base_dir, "frontend", "pdfs", "ap_ts_agriculture_irrigation_master.pdf")
os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)

data = get_agri_irrigation_data()

sections_html = ""
for sec in data["core_sections"]:
    pts_html = "".join([f'<li style="margin-bottom: 10px; line-height: 1.6; font-size: 11px; color: #1e293b;">{pt}</li>' for pt in sec["points"]])
    sections_html += f"""
    <div style="page-break-inside: avoid; margin-bottom: 20px; border: 1px solid #cbd5e1; border-radius: 8px; padding: 14px 16px; background: #ffffff;">
        <h2 style="font-size: 13.5px; font-weight: 800; color: #047857; margin: 0 0 10px 0; border-bottom: 2px solid #a7f3d0; padding-bottom: 6px;">
            {sec['title']}
        </h2>
        <ul style="margin: 0; padding-left: 20px;">
            {pts_html}
        </ul>
    </div>
    """

mcqs_html = ""
for idx, m in enumerate(data["mcqs"], 1):
    mcqs_html += f"""
    <div style="page-break-inside: avoid; margin-bottom: 12px; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; background: #f8fafc;">
        <div style="font-size: 11px; font-weight: 700; color: #0f172a; margin-bottom: 6px;">#{idx}. {m['q']}</div>
        <div style="font-size: 10.5px; color: #047857; font-weight: 700; margin-bottom: 3px;">✓ సమాధానం: {m['ans']}</div>
        <div style="font-size: 10px; color: #475569; line-height: 1.4;"><b>వివరణ:</b> {m['exp']}</div>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>ఆంధ్రప్రదేశ్ & తెలంగాణ వ్యవసాయం, సాగునీరు & ఆక్వాకల్చర్ మాస్టర్ గైడ్</title>
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
            background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
            color: white;
            padding: 24px;
            border-radius: 12px;
            text-align: center;
            margin-bottom: 24px;
        }}
        .cover-header h1 {{
            font-size: 21px;
            margin: 0 0 8px 0;
            font-weight: 900;
        }}
        .cover-header p {{
            font-size: 11.5px;
            margin: 0;
            color: #a7f3d0;
            line-height: 1.5;
        }}
    </style>
</head>
<body>
    <div class="cover-header">
        <div style="font-size: 10.5px; font-weight: 800; color: #fde68a; text-transform: uppercase; margin-bottom: 4px;">లక్ష్య APPSC / TSPSC 2026 ఎడిషన్</div>
        <h1>🌾 AP & TS వ్యవసాయం, సాగునీటి ప్రాజెక్టులు & ఆక్వాకల్చర్ మాస్టర్ గైడ్</h1>
        <p>పోలవరం జాతీయ ప్రాజెక్ట్ (సెక్షన్ 90), కృష్ణా-గోదావరి ట్రిబ్యునల్స్ (KWDT/GWDT), 2025-26 MSP ధరలు & ఆక్వా ఎగుమతుల సమగ్ర సమాచారం</p>
    </div>

    {sections_html}

    <div style="page-break-inside: avoid; margin-top: 24px; margin-bottom: 14px; border-bottom: 2px solid #059669; padding-bottom: 6px;">
        <h2 style="font-size: 15px; font-weight: 900; color: #065f46; margin: 0;">
            📝 పరీక్ష ప్రాక్టీస్ ప్రశ్నలు & వివరణలు (Practice MCQs)
        </h2>
    </div>

    {mcqs_html}

    <div style="text-align: center; margin-top: 24px; padding-top: 14px; border-top: 1px solid #cbd5e1; font-size: 10px; color: #64748b;">
        © 2026 లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రిపరేషన్ పోర్టల్ | APPSC Group-1, Group-2, TSPSC & UPSC స్టడీ మెటీరియల్
    </div>
</body>
</html>
"""

temp_html_path = os.path.join(base_dir, "backend", "temp_agri.html")
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
