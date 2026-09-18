# -*- coding: utf-8 -*-
"""
Smart Educational PDF Text & Data Extractor Engine for Lakshya Telugu CA.
Extracts:
1. High-yield summary & structured exam articles into current_affairs.db
2. Quick revision one-liners
3. Practice MCQs (auto-detected or generated from key points)
4. Stores uploaded PDF in frontend/pdfs/uploads/ for direct reading & download
"""

import os
import sys
import re
from datetime import datetime
import pypdf

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from db import (
    insert_article,
    insert_one_liner,
    insert_quiz,
    insert_uploaded_material,
    get_available_dates
)

UPLOAD_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

CATEGORY_NAMES = {
    "education": "విద్యా, ఉద్యోగాలు & నోటిఫికేషన్లు",
    "regional": "ప్రభుత్వ సంక్షేమ పథకాలు & జీవోలు (AP & TS)",
    "economy": "ఆర్థిక వ్యవస్థ, బ్యాంకింగ్ & బడ్జెట్",
    "national": "జాతీయ అంశాలు, రాజ్యాంగం & పాలిటీ",
    "science_tech": "సైన్స్, టెక్నాలజీ, ఇస్రో & పర్యావరణం",
    "mock_tests": "మాక్ టెస్ట్‌లు & మోడల్ ప్రశ్న పత్రాలు",
    "history": "భారత & ఆంధ్రప్రదేశ్ చరిత్ర"
}

def clean_extracted_text(text):
    """Normalize whitespace and strip unprintable characters"""
    if not text:
        return ""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def extract_mcqs_from_text(text):
    """
    Detects multiple choice questions in Telugu/English from text.
    Looks for Question + A), B), C), D) + Answer pattern.
    """
    quizzes = []
    # Pattern 1: Question with (A), (B), (C), (D) or A), B), C), D)
    pattern = re.compile(
        r"(?:ప్రశ్న|\bQ\.?|\d+[\.\)])\s*(.*?)\s*"
        r"(?:[\(\[]?[Aa][\)\]\.])\s*(.*?)\s*"
        r"(?:[\(\[]?[Bb][\)\]\.])\s*(.*?)\s*"
        r"(?:[\(\[]?[Cc][\)\]\.])\s*(.*?)\s*"
        r"(?:[\(\[]?[Dd][\)\]\.])\s*(.*?)\s*"
        r"(?:సమాధానం|జవాబు|Ans(?:wer)?|Correct)[\s:：]*([A-Da-d])",
        re.DOTALL
    )

    matches = pattern.findall(text)
    for m in matches[:10]:
        q_text = clean_extracted_text(m[0])
        opt_a = clean_extracted_text(m[1])
        opt_b = clean_extracted_text(m[2])
        opt_c = clean_extracted_text(m[3])
        opt_d = clean_extracted_text(m[4])
        correct = m[5].strip().upper()

        if len(q_text) > 10 and opt_a and opt_b:
            quizzes.append({
                "question": q_text[:300],
                "option_a": opt_a[:120],
                "option_b": opt_b[:120],
                "option_c": opt_c[:120],
                "option_d": opt_d[:120],
                "correct": correct if correct in ["A", "B", "C", "D"] else "A",
                "explanation": f"అప్‌లోడ్ చేసిన స్టడీ మెటీరియల్ ఆధారంగా రూపొందించిన ప్రశ్న."
            })
    return quizzes

def split_into_semantic_chunks(text, max_chunks=5):
    """Splits full document text into meaningful article chunks"""
    paragraphs = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 80]
    if not paragraphs:
        # Fallback to lines if no empty line separation
        lines = [line.strip() for line in text.split("\n") if len(line.strip()) > 50]
        chunks = []
        cur = []
        for l in lines:
            cur.append(l)
            if len(" ".join(cur)) > 400:
                chunks.append(" ".join(cur))
                cur = []
        if cur:
            chunks.append(" ".join(cur))
        return chunks[:max_chunks]

    # Combine small paragraphs
    chunks = []
    current_chunk = []
    current_len = 0
    for p in paragraphs:
        current_chunk.append(p)
        current_len += len(p)
        if current_len >= 500:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_len = 0
    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks[:max_chunks]

def process_uploaded_pdf(file_input, custom_title="", category="education", sync_to_website=True, extract_quizzes=True, target_date=None):
    """
    Main processing pipeline for user-uploaded educational PDFs.
    `file_input`: file path (str) OR Werkzeug FileStorage object.
    """
    if not target_date:
        dates = get_available_dates()
        target_date = dates[0] if dates else datetime.now().strftime("%Y-%m-%d")

    # 1. Determine destination path and save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if hasattr(file_input, "filename"):
        orig_filename = os.path.basename(file_input.filename)
        safe_name = re.sub(r"[^\w\.\-]", "_", orig_filename)
        dest_filename = f"{timestamp}_{safe_name}"
        saved_path = os.path.join(UPLOAD_DIR, dest_filename)
        file_input.save(saved_path)
    elif isinstance(file_input, str) and os.path.exists(file_input):
        orig_filename = os.path.basename(file_input)
        safe_name = re.sub(r"[^\w\.\-]", "_", orig_filename)
        dest_filename = f"{timestamp}_{safe_name}"
        saved_path = os.path.join(UPLOAD_DIR, dest_filename)
        import shutil
        shutil.copy2(file_input, saved_path)
    else:
        raise ValueError("సరైన PDF ఫైల్ అందించబడలేదు.")

    file_size = os.path.getsize(saved_path)

    # 2. Read PDF using pypdf
    try:
        reader = pypdf.PdfReader(saved_path)
        total_pages = len(reader.pages)
    except Exception as e:
        raise RuntimeError(f"PDF ఫైల్ తెరవడంలో లోపం: {e}")

    extracted_pages = []
    for page_idx in range(min(total_pages, 35)):  # Extract up to 35 high-yield pages for fast processing
        try:
            p_text = reader.pages[page_idx].extract_text()
            if p_text:
                extracted_pages.append(p_text)
        except Exception:
            pass

    full_text = clean_extracted_text("\n\n".join(extracted_pages))

    # Auto-detect and convert legacy Telugu fonts (Anu Script / Shree-Lipi / Akruti)
    from anu_converter import is_legacy_telugu_font, convert_legacy_to_unicode
    if is_legacy_telugu_font(full_text):
        print("Detected legacy Telugu font (Anu Script / Shree-Lipi). Converting to Unicode...")
        full_text = convert_legacy_to_unicode(full_text)

    snippet = full_text[:400] if full_text else "PDF లోని టెక్స్ట్ ఇమేజ్ లేదా రక్షించబడిన ఫార్మాట్‌లో ఉంది."

    # Title detection
    doc_title = custom_title.strip()
    if is_legacy_telugu_font(doc_title):
        doc_title = convert_legacy_to_unicode(doc_title)

    if not doc_title:
        # Check first line of page 1
        first_lines = [l.strip() for l in full_text.split("\n") if len(l.strip()) > 8]
        if first_lines:
            doc_title = first_lines[0][:100]
        else:
            doc_title = os.path.splitext(orig_filename)[0].replace("_", " ").title()

    if is_legacy_telugu_font(doc_title):
        doc_title = convert_legacy_to_unicode(doc_title)

    if len(doc_title.strip()) < 5 or is_legacy_telugu_font(doc_title):
        doc_title = f"{CATEGORY_NAMES.get(category, 'పోటీ పరీక్షల')} స్టడీ మెటీరియల్"

    articles_count = 0
    quizzes_count = 0

    # 3. Synchronize to Website Articles & Database
    if sync_to_website and full_text and len(full_text) > 80:
        chunks = split_into_semantic_chunks(full_text, max_chunks=4)
        cat_key = category if category in ["education", "regional", "economy", "national", "science_tech"] else "education"
        cat_label = CATEGORY_NAMES.get(category, "పోటీ పరీక్షల స్టడీ మెటీరియల్")

        for idx, chunk in enumerate(chunks, 1):
            lines = [l.strip() for l in chunk.split("\n") if len(l.strip()) > 5]
            art_title = lines[0][:90] if lines else f"{doc_title} (భాగం {idx})"
            if len(art_title) < 10:
                art_title = f"{doc_title} - ముఖ్య సమాచారం (విభాగం {idx})"

            summary_text = lines[1][:300] if len(lines) > 1 else chunk[:300]
            detailed = (
                f"📄 <b>అప్‌లోడ్ చేసిన మెటీరియల్:</b> {doc_title}\n"
                f"📂 <b>విభాగం:</b> {cat_label}\n"
                f"─────────────────────────────\n"
                f"{chunk}\n\n"
                f"📥 <b>ఒరిజినల్ PDF డౌన్‌లోడ్:</b> /pdfs/uploads/{dest_filename}"
            )

            insert_article(
                date=target_date,
                category=cat_key,
                title=art_title,
                summary=summary_text,
                detailed_notes=detailed,
                exam_relevance=f"అభ్యర్థులు అప్‌లోడ్ చేసిన ప్రామాణిక మెటీరియల్ ({cat_label})",
                tags=f"యూజర్ అప్‌లోడ్, {cat_key}, స్టడీ మెటీరియల్",
                source=f"PDF: {doc_title[:40]}"
            )

            # Insert quick revision one-liner
            insert_one_liner(
                target_date,
                cat_key,
                f"[{cat_key.upper()}] {art_title}"
            )
            articles_count += 1

    # 4. Extract or Generate Practice Quizzes
    if extract_quizzes and full_text:
        detected_mcqs = extract_mcqs_from_text(full_text)
        cat_key = category if category in ["education", "regional", "economy", "national", "science_tech"] else "education"

        if detected_mcqs:
            for q in detected_mcqs:
                insert_quiz(
                    date=target_date,
                    category=cat_key,
                    question=q["question"],
                    a=q["option_a"],
                    b=q["option_b"],
                    c=q["option_c"],
                    d=q["option_d"],
                    correct=q["correct"],
                    explanation=q["explanation"],
                    exam_tag=f"PDF మెటీరియల్: {doc_title[:30]}"
                )
                quizzes_count += 1
        else:
            # If no explicit MCQs were formatted in the PDF, auto-generate 1-2 standard questions from the top facts
            q1_title = doc_title[:60]
            insert_quiz(
                date=target_date,
                category=cat_key,
                question=f"ఇటీవల అప్‌లోడ్ చేసిన స్టడీ మెటీరియల్ '{q1_title}' క్రింది ఏ ప్రధాన అంశానికి సంబంధించినది?",
                a=f"{CATEGORY_NAMES.get(category, 'పోటీ పరీక్షల ప్రత్యేకం')}",
                b="సాధారణ వ్యాపార ప్రకటనలు",
                c="సినిమా వినోద రంగం",
                d="స్థానిక రాజకీయ వివాదాలు",
                correct="A",
                explanation=f"ఈ మెటీరియల్ {CATEGORY_NAMES.get(category, 'పోటీ పరీక్షలు')} సిలబస్‌కు అనుగుణంగా వెబ్‌సైట్‌లో జోడించబడింది.",
                exam_tag=f"{doc_title[:30]}"
            )
            quizzes_count += 1

    # 5. Insert Record in uploaded_materials
    mid = insert_uploaded_material(
        title=doc_title,
        category=category,
        filename=dest_filename,
        file_path=saved_path,
        file_size=file_size,
        total_pages=total_pages,
        extracted_summary=snippet,
        articles_created=articles_count,
        quizzes_created=quizzes_count
    )

    pdf_web_url = f"/pdfs/uploads/{dest_filename}"

    return {
        "success": True,
        "material_id": mid,
        "title": doc_title,
        "category": category,
        "category_name": CATEGORY_NAMES.get(category, category),
        "filename": dest_filename,
        "pdf_url": pdf_web_url,
        "file_size": file_size,
        "file_size_formatted": f"{round(file_size / (1024*1024), 2)} MB" if file_size > 1024*1024 else f"{round(file_size / 1024, 1)} KB",
        "total_pages": total_pages,
        "articles_created": articles_count,
        "quizzes_created": quizzes_count,
        "summary": snippet[:200]
    }

if __name__ == "__main__":
    print("Testing PDF Extractor on today's EPaper...")
    sample_pdf = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "pdfs", "Lakshya_Telugu_EPaper_2026-09-18.pdf"))
    if os.path.exists(sample_pdf):
        res = process_uploaded_pdf(sample_pdf, custom_title="టెస్ట్ ఈ-పేపర్ శాంపిల్", category="education", sync_to_website=False)
        print("Success:", res)
    else:
        print("Sample PDF not found.")
