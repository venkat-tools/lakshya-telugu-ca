# -*- coding: utf-8 -*-
"""
Compiles the Map Pointing Master Atlas PDF using Microsoft Edge Headless engine.
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

from map_pointing_data import get_all_map_points

pdf_output_path = os.path.join(base_dir, "frontend", "pdfs", "map_pointing_master_atlas.pdf")
os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)

all_points = get_all_map_points()
ap_points = [p for p in all_points if p.get("domain") == "ap"]
india_points = [p for p in all_points if p.get("domain") == "india"]
world_points = [p for p in all_points if p.get("domain") == "world"]

def render_points_cards(points, domain_title, domain_icon, color_theme):
    html = f"""
    <div style="page-break-inside: avoid; margin-top: 24px; margin-bottom: 14px; border-bottom: 2px solid {color_theme}; padding-bottom: 6px;">
        <h2 style="font-size: 16px; font-weight: 900; color: {color_theme}; margin: 0; display:flex; align-items:center; gap: 8px;">
            <span>{domain_icon}</span> <span>{domain_title} ({len(points)} అంశాలు)</span>
        </h2>
    </div>
    """
    for idx, p in enumerate(points, 1):
        pyq_html = f"""
        <div style="background: #fef2f2; border-left: 3px solid #ef4444; padding: 5px 10px; margin-top: 6px; font-size: 10px; color: #991b1b; font-weight: 700;">
            <b>🎯 PYQ:</b> {p.get('pyq')}
        </div>
        """ if p.get('pyq') else ""

        html += f"""
        <div style="page-break-inside: avoid; margin-bottom: 14px; border: 1px solid #cbd5e1; border-radius: 8px; padding: 12px; background: #ffffff;">
            <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 1px solid #f1f5f9; padding-bottom: 6px; margin-bottom: 8px;">
                <span style="font-size: 13px; font-weight: 800; color: #0f172a;">#{idx}. {p['telugu_name']} ({p.get('name')})</span>
                <span style="background: #e0f2fe; color: #0369a1; font-size: 10px; font-weight: 700; padding: 2px 8px; border-radius: 4px;">{p.get('district', p.get('state', p.get('country', '')))}</span>
            </div>
            <div style="font-size: 10px; color: #2563eb; font-weight: 700; margin-bottom: 4px;">📂 వర్గం: {p.get('category')}</div>
            <div style="font-size: 11px; color: #334155; line-height: 1.6; margin-bottom: 6px; white-space: pre-line;">{p.get('key_facts')}</div>
            <div style="background: #f8fafc; padding: 6px 10px; border-radius: 4px; font-size: 10px; color: #475569; font-weight: 600;">
                <b style="color:#d97706;">💡 పరీక్షల ప్రాధాన్యత:</b> {p.get('exam_significance')}
            </div>
            {pyq_html}
        </div>
        """
    return html

ap_html = render_points_cards(ap_points, "ఆంధ్రప్రదేశ్ మ్యాప్ పాయింటింగ్ (AP Geography & Resources)", "🚩", "#0284c7")
india_html = render_points_cards(india_points, "భారతదేశం మ్యాప్ పాయింటింగ్ (India Passes, Rivers & Reserves)", "🇮🇳", "#059669")
world_html = render_points_cards(world_points, "ప్రపంచం వ్యూహాత్మక జలసంధులు & ప్రాంతాలు (World Geopolitics)", "🌍", "#7c3aed")

full_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>లక్ష్య మ్యాప్ పాయింటింగ్ మాస్టర్ అట్లాస్ 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@400;600;700;800;900&display=swap" rel="stylesheet">
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
        <div style="font-size: 40px; margin-bottom: 10px;">🗺️ 📍 🌍</div>
        <div style="background:#0284c7; color:#ffffff; display:inline-block; padding: 5px 18px; border-radius: 20px; font-weight:800; font-size:13px; letter-spacing:1px; margin-bottom: 18px;">
            లక్ష్య డిజిటల్ సివిల్స్ అకాడమీ
        </div>
        <h1 style="font-size: 24px; font-weight: 900; color: #0f172a; margin-bottom: 10px; line-height: 1.4;">
            APPSC & TSPSC కాంపిటీటివ్ ఎగ్జామ్స్<br>
            <span style="color:#0284c7;">మ్యాప్ పాయింటింగ్ & జియోగ్రఫీ చీట్-షీట్ మాస్టర్ అట్లాస్</span>
        </h1>
        <p style="font-size: 13px; color: #475569; max-width: 480px; margin: 0 auto 25px; line-height: 1.6;">
            ఆంధ్రప్రదేశ్ 26 జిల్లాలు, భారతదేశం కనుమలు-నదులు మరియు ప్రపంచ వ్యూహాత్మక జలసంధుల దృశ్య విశ్లేషణ & గత పరీక్షల ప్రశ్నల (PYQs) సమగ్ర నిధి.
        </p>

        <div style="background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 8px; padding: 16px; max-width: 460px; margin: 0 auto 25px; text-align: left; font-size: 11px;">
            <div style="font-weight:800; color:#0369a1; margin-bottom: 6px; font-size: 12px;">🌟 ఇందులో పొందుపరిచిన 3 ప్రధాన విభాగాలు:</div>
            <div>• <b>ఆంధ్రప్రదేశ్:</b> ఓడరేవులు, పోలవరం & ధవళేశ్వరం, అరోమా కొండ, మడ అడవులు, బాక్సైట్ బెల్టులు</div>
            <div>• <b>భారతదేశం:</b> హిమాలయ కనుమలు (జోజిలా, నాథూలా), నదీ సంగమాలు, 18 బయోస్పియర్లు, అణు కేంద్రాలు</div>
            <div>• <b>ప్రపంచం:</b> మలక్కా, హోర్ముజ్, బాబ్-ఎల్-మండేబ్ జలసంధులు, సూయజ్ కాలువ, రింగ్ ఆఫ్ ఫైర్</div>
        </div>

        <div style="font-size: 11px; color: #64748b; font-weight: 600;">
            వెబ్ పోర్టల్: https://lakshya-telugu-ca.onrender.com/map_pointing_atlas | టెలిగ్రామ్: /map
        </div>
    </div>

    <!-- Header Strip -->
    <div class="header-strip">
        <span>లక్ష్య మ్యాప్ పాయింటింగ్ మాస్టర్ అట్లాస్ 2026</span>
        <span>భౌగోళిక అంశాలు & గత పరీక్షల ప్రశ్నలు</span>
    </div>

    {ap_html}
    {india_html}
    {world_html}

    <!-- Footer -->
    <div class="footer-strip">
        © 2026 లక్ష్య తెలుగు కరెంట్ అఫైర్స్ & కాంపిటీటివ్ ఎగ్జామ్స్ పోర్టల్. All Rights Reserved.
    </div>
</body>
</html>
"""

temp_html_path = os.path.join(base_dir, "backend", "temp_map_atlas_pdf.html")
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
