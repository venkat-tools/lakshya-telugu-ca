# -*- coding: utf-8 -*-
"""
Compiles AP & TS Tribal Heritage, PVTGs & PESA Handbook PDF via Edge Headless.
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

from tribal_heritage_data import TRIBAL_HERITAGE_DATA

pdf_output_path = os.path.join(base_dir, "frontend", "pdfs", "ap_ts_tribal_heritage_pesa_handbook.pdf")
os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)

data = TRIBAL_HERITAGE_DATA

sections_html = ""
for sec in data["sections"]:
    pts_html = "".join([f'<li style="margin-bottom: 9px; line-height: 1.6; font-size: 10.5px; color: #1e293b;">{pt}</li>' for pt in sec["points"]])
    sections_html += f"""
    <div style="page-break-inside: avoid; margin-bottom: 18px; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px 16px; background: #ffffff;">
        <h2 style="font-size: 13px; font-weight: 800; color: #047857; margin: 0 0 10px 0; border-bottom: 2px solid #d1fae5; padding-bottom: 6px;">
            {sec['title']}
        </h2>
        <ul style="margin: 0; padding-left: 20px;">
            {pts_html}
        </ul>
    </div>
    """

mcqs_html = ""
for idx, m in enumerate(data["mcqs"], 1):
    opt_text = m["options"][m["answer"]]
    mcqs_html += f"""
    <div style="page-break-inside: avoid; margin-bottom: 10px; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; background: #f8fafc;">
        <div style="font-size: 10.5px; font-weight: 700; color: #0f172a; margin-bottom: 5px;">#{idx}. {m['question']}</div>
        <div style="font-size: 10px; color: #047857; font-weight: 700; margin-bottom: 3px;">✓ సరైన సమాధానం: {opt_text}</div>
        <div style="font-size: 9.5px; color: #475569; line-height: 1.4;"><b>వివరణ:</b> {m['explanation']}</div>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>{data['title']}</title>
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
            background: linear-gradient(135deg, #064e3b 0%, #047857 100%);
            color: white;
            padding: 22px 24px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }}
        .cover-title {{
            font-size: 20px;
            font-weight: 900;
            margin-bottom: 6px;
            letter-spacing: -0.5px;
        }}
        .cover-subtitle {{
            font-size: 11.5px;
            color: #d1fae5;
            font-weight: 600;
        }}
        .meta-strip {{
            background: #ecfdf5;
            border: 1px solid #a7f3d0;
            border-radius: 6px;
            padding: 8px 14px;
            margin-bottom: 18px;
            font-size: 10px;
            color: #065f46;
            display: flex;
            justify-content: space-between;
        }}
        .footer-note {{
            margin-top: 25px;
            text-align: center;
            font-size: 9px;
            color: #94a3b8;
            border-top: 1px solid #e2e8f0;
            padding-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="cover-header">
        <div class="cover-title">🏕️ ఆంధ్రప్రదేశ్ & తెలంగాణ గిరిజన సంస్కృతి, PVTGs & PESA హ్యాండ్‌బుక్</div>
        <div class="cover-subtitle">APPSC & TSPSC గ్రూప్-1, గ్రూప్-2 & సమాజ శాస్త్రం (Indian Society) మాస్టర్ మెటీరియల్</div>
    </div>

    <div class="meta-strip">
        <span><b>కంటెంట్:</b> 7 PVTGs, మేడారం & నాగోబా జాతరలు, గుస్సాడి & ధింసా, 5వ షెడ్యూల్, PESA 1996, FRA 2006, సమత కేసు</span>
        <span><b>ప్రాక్టీస్:</b> 30 హై-యీల్డ్ MCQs వివరణలతో</span>
    </div>

    {sections_html}

    <div style="page-break-before: always; margin-top: 20px; margin-bottom: 14px;">
        <h2 style="font-size: 14px; font-weight: 800; color: #065f46; border-bottom: 2px solid #6ee7b7; padding-bottom: 6px;">
            🎯 30 ప్రాక్టీస్ ప్రశ్నలు & సమగ్ర వివరణలు (Tribal Studies MCQs)
        </h2>
    </div>

    {mcqs_html}

    <div class="footer-note">
        లక్ష్య డైలీ కరెంట్ అఫైర్స్ & జనరల్ స్టడీస్ పోర్టల్ | APPSC / TSPSC అభ్యర్థుల ప్రత్యేకం | https://lakshya-telugu-ca.onrender.com
    </div>
</body>
</html>
"""

temp_html_path = os.path.join(base_dir, "frontend", "pdfs", "temp_tribal_heritage.html")
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

if os.path.exists(temp_html_path):
    os.remove(temp_html_path)

if os.path.exists(pdf_output_path) and os.path.getsize(pdf_output_path) > 1000:
    size_mb = os.path.getsize(pdf_output_path) / (1024 * 1024)
    print(f"SUCCESS: Generated PDF at {pdf_output_path} (Size: {size_mb:.2f} MB)")
else:
    print(f"ERROR: PDF generation failed. Edge output: {res.stderr}")
    sys.exit(1)
