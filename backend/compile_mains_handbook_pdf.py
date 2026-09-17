# -*- coding: utf-8 -*-
"""
Generates the comprehensive, high-yield APPSC & TSPSC Mains Descriptive Answer Writing Handbook PDF
using Microsoft Edge Headless engine.
"""

import os
import sys
import subprocess

# Ensure UTF-8 output
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

base_dir = r"C:\Users\venkat\.gemini\antigravity\scratch\daily_current_affairs_telugu"
sys.path.insert(0, os.path.join(base_dir, "backend"))

from mains_descriptive_data import MAINS_QUESTIONS

pdf_output_path = os.path.join(base_dir, "frontend", "pdfs", "appsc_mains_answer_writing_handbook.pdf")
os.makedirs(os.path.dirname(pdf_output_path), exist_ok=True)

# Generate HTML for PDF
questions_html = ""
for idx, q in enumerate(MAINS_QUESTIONS, 1):
    body_li = "".join([f"<li style='margin-bottom:8px;'>{pt}</li>" for pt in q["model_answer"]["body_points"]])
    
    questions_html += f"""
    <div class="q-block" style="page-break-inside: avoid; margin-bottom: 28px; border: 1px solid #cbd5e1; border-radius: 10px; padding: 18px; background: #ffffff;">
        <div style="display:flex; justify-content:space-between; align-items:center; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 12px;">
            <span style="background:#1e3a8a; color:#ffffff; font-weight:700; font-size:12px; padding: 3px 10px; border-radius: 4px;">{q['paper']}</span>
            <span style="color:#0369a1; font-weight:700; font-size:12px;">🎯 {q['subject']}</span>
            <span style="background:#fef3c7; color:#92400e; font-weight:700; font-size:11px; padding: 3px 8px; border-radius: 4px; border: 1px solid #fcd34d;">ప్రశ్న #{idx}</span>
        </div>
        
        <h3 style="font-size: 15px; font-weight: 800; color: #0f172a; line-height: 1.5; margin-bottom: 14px;">
            {q['question']}
        </h3>
        
        <div style="margin-bottom: 12px; background: #f8fafc; border-left: 4px solid #3b82f6; padding: 10px 14px; border-radius: 4px;">
            <div style="font-weight: 800; font-size: 12px; color: #1e40af; margin-bottom: 4px;">1. పరిచయం (INTRODUCTION):</div>
            <div style="font-size: 13px; color: #334155; line-height: 1.6;">{q['model_answer']['intro']}</div>
        </div>

        <div style="margin-bottom: 12px; background: #f8fafc; border-left: 4px solid #0d9488; padding: 10px 14px; border-radius: 4px;">
            <div style="font-weight: 800; font-size: 12px; color: #0f766e; margin-bottom: 4px;">2. ముఖ్య విశ్లేషణ & అంశాలు (CORE BODY POINTS):</div>
            <ul style="font-size: 13px; color: #334155; line-height: 1.6; padding-left: 18px; margin: 0;">
                {body_li}
            </ul>
        </div>

        <div style="margin-bottom: 12px; background: #f8fafc; border-left: 4px solid #8b5cf6; padding: 10px 14px; border-radius: 4px;">
            <div style="font-weight: 800; font-size: 12px; color: #6d28d9; margin-bottom: 4px;">3. ప్రభుత్వ చర్యలు & రాజ్యాంగ రక్షణలు (GOVT INITIATIVES):</div>
            <div style="font-size: 13px; color: #334155; line-height: 1.6;">{q['model_answer']['govt_steps']}</div>
        </div>

        <div style="background: #f8fafc; border-left: 4px solid #f59e0b; padding: 10px 14px; border-radius: 4px;">
            <div style="font-weight: 800; font-size: 12px; color: #b45309; margin-bottom: 4px;">4. ముగింపు & ముందున్న మార్గం (WAY FORWARD & CONCLUSION):</div>
            <div style="font-size: 13px; color: #334155; line-height: 1.6;">{q['model_answer']['conclusion']}</div>
        </div>
    </div>
    """

full_html = f"""<!DOCTYPE html>
<html lang="te">
<head>
    <meta charset="UTF-8">
    <title>APPSC & TSPSC మెయిన్స్ ఆన్సర్ రైటింగ్ హ్యాండ్‌బుక్ 2026</title>
    <link href="https://fonts.googleapis.com/css2?family=Mandali&family=Outfit:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        @page {{
            size: A4;
            margin: 15mm 15mm 15mm 15mm;
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
            padding: 60px 20px 40px;
            page-break-after: always;
            border: 8px double #1e3a8a;
            border-radius: 12px;
            margin-bottom: 30px;
        }}
        .watermark {{
            position: fixed;
            top: 45%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-35deg);
            font-size: 72px;
            font-weight: 900;
            color: rgba(30, 58, 138, 0.04);
            pointer-events: none;
            z-index: -1;
            white-space: nowrap;
        }}
        .header-strip {{
            border-bottom: 2px solid #1e3a8a;
            padding-bottom: 8px;
            margin-bottom: 20px;
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: #64748b;
            font-weight: 600;
        }}
        .footer-strip {{
            margin-top: 25px;
            border-top: 1px solid #e2e8f0;
            padding-top: 8px;
            text-align: center;
            font-size: 10px;
            color: #94a3b8;
        }}
    </style>
</head>
<body>
    <div class="watermark">LAKSHYA TELUGU CA 2026</div>

    <!-- Cover Page -->
    <div class="cover-page">
        <div style="font-size: 40px; margin-bottom: 12px;">✍️ 🏆 📚</div>
        <div style="background:#1e3a8a; color:#ffffff; display:inline-block; padding: 6px 20px; border-radius: 30px; font-weight:800; font-size:14px; letter-spacing:1px; margin-bottom: 20px;">
            లక్ష్య డిజిటల్ సివిల్స్ అకాడమీ
        </div>
        <h1 style="font-size: 26px; font-weight: 900; color: #0f172a; margin-bottom: 12px; line-height: 1.4;">
            APPSC & TSPSC గ్రూప్-1 & గ్రూప్-2 మెయిన్స్<br>
            <span style="color:#d97706;">డిస్క్రిప్టివ్ ఆన్సర్ రైటింగ్ మాస్టర్ హ్యాండ్‌బుక్</span>
        </h1>
        <p style="font-size: 14px; color: #475569; max-width: 500px; margin: 0 auto 30px; line-height: 1.6;">
            అధికారిక పరీక్ష ప్రమాణాల ప్రకారం 4-స్టెప్ ఫార్ములా (పరిచయం, ముఖ్య విశ్లేషణ, ప్రభుత్వ చర్యలు, ముగింపు) తో రూపొందించబడిన 12 సమగ్ర మోడల్ సమాధానాలు & మూల్యాంకన వ్యూహం.
        </p>

        <div style="background: #f1f5f9; border-radius: 8px; padding: 18px; max-width: 480px; margin: 0 auto 30px; text-align: left; font-size: 12px;">
            <div style="font-weight:800; color:#1e3a8a; margin-bottom: 8px; font-size: 13px;">📑 కవర్ చేయబడిన కోర్ పేపర్లు:</div>
            <div>• <b>పేపర్-1:</b> భారతీయ సమాజం, సంక్షేమ చట్టాలు & మహిళా సాధికారత</div>
            <div>• <b>పేపర్-2:</b> భారత రాజ్యాంగం, పాలన, న్యాయవ్యవస్థ & ఆధునిక ఆంధ్ర చరిత్ర</div>
            <div>• <b>పేపర్-3:</b> భారత & ఆంధ్రప్రదేశ్ ఆర్థిక వ్యవస్థ, అమరావతి, పోలవరం & విభజన చట్టం 2014</div>
            <div>• <b>పేపర్-4:</b> సైన్స్ & టెక్నాలజీ, గగన్‌యాన్, చంద్రయాన్-4, విపత్తులు & పునరుత్పాదక ఇంధనం</div>
        </div>

        <div style="font-size: 11px; color: #64748b; font-weight: 600;">
            ఆన్‌లైన్ పోర్టల్: https://lakshya-telugu-ca.onrender.com/mains_descriptive_portal | టెలిగ్రామ్: /mains
        </div>
    </div>

    <!-- Content Header -->
    <div class="header-strip">
        <span>లక్ష్య గ్రూప్-1 & గ్రూప్-2 మెయిన్స్ ఆన్సర్ రైటింగ్ హ్యాండ్‌బుక్</span>
        <span>అధికారిక మోడల్ సమాధానాలు & విశ్లేషణ</span>
    </div>

    <!-- Questions Content -->
    {questions_html}

    <!-- Footer -->
    <div class="footer-strip">
        © 2026 లక్ష్య తెలుగు కరెంట్ అఫైర్స్ & కాంపిటీటివ్ ఎగ్జామ్స్ పోర్టల్. All Rights Reserved.
    </div>
</body>
</html>
"""

temp_html_path = os.path.join(base_dir, "backend", "temp_mains_pdf.html")
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
