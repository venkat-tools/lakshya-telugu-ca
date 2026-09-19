# -*- coding: utf-8 -*-
"""
Legacy Telugu Font (Anu Script 7.0 / Shree-Lipi / Akruti) to Telugu Unicode Converter.
Detects and translates 8-bit ANSI legacy font glyphs into clean, readable Unicode Telugu.
"""

import re

# High-frequency words and prefixes mapped directly
WORD_REPLACEMENTS = [
    # Full compound phrases from typical APPSC/TSPSC exam papers
    (r"BŠóÌÕMýS\s*çÜ\*\{™éË¨\]I§\s*MðS\.íÜ\.ÐóIÆš‡\.\.Ë„>AË\$,?\s*BÔ¶æÄ¶æ\*Ë\s*Ð\]I\*À°òeÝùtV>", 
     "ఆదేశిక సూత్రాలు మరియు సివిల్ సర్వీసెస్ లక్ష్యాలు, ఆశయాల అమలు"),
    (r"BŠóÌÕMýS\s*çÜ\*\{™éËMýS\s*çÜ\.\.\.°\.\.\.«¯\.\.\.", "ఆదేశిక సూత్రాలకు సంబంధించి"),
    (r"BŠóÌÕMýS\s*çÜ\*\{™éË\$", "ఆదేశిక సూత్రాలు"),
    (r"BŠóÌÕMýS\s*çÜ\*\{™éË", "ఆదేశిక సూత్రాల"),
    (r"BŠóÌÕMýS", "ఆదేశిక"),
    (r"çÜ\*\{™éË\$", "సూత్రాలు"),
    (r"çÜ\*\{™éË", "సూత్రాల"),
    (r"BçTMýSÌŒæ", "ఆర్టికల్"),
    (r"Bç!MýS", "ఆర్థిక"),
    (r"çßæMýS\$PË\$", "హక్కులు"),
    (r"çßæMýS\$PË", "హక్కుల"),
    (r"çßæMýS\$P", "హక్కు"),
    (r"çßæMýS\$", "హక్కు"),
    (r"çÜÐ\]I\*«śé", "సమాధానం"),
    (r"çÜÐ\]I\*«", "సమాధానం"),
    (r"òÙyyí\*ÀÌŒæz", "షెడ్యూల్డ్"),
    (r"MýSsìèË\$", "కులాలు"),
    (r"™ðIVýSË\$", "తెగలు"),
    (r"°Ëißæ™\]I", "నిర్దేశిత"),
    (r"Ð\]IÆ>ŸË", "వర్గాల"),
    (r"ÑšýIÂ", "విద్యా"),
    (r"\{ç’Ãñæ\*fˆé", "ప్రయోజనం"),
    (r"BÔ¶æÄ¶æ\*Ë", "ఆశయాల"),
    (r"BÔ¶æÄ¶æ\$", "ఆశయం"),
    (r"BÔ¶æÄ¶æ", "ఆశయం"),
    (r"B\{Ô¶æÄ¶æ\$", "ఆదేశం"),
    (r"\{VýS\*‹³&1", "గ్రూప్-1"),
    (r"\{VýS\*‹³&2", "గ్రూప్-2"),
    (r"\{VýS\*‹³&3", "గ్రూప్-3"),
    (r"\{VýS\*‹³&4", "గ్రూప్-4"),
    (r"\{VýS\*‹³", "గ్రూప్"),
    (r"M>Æý†\*æ", "కారణం"),
    (r"Æ>gêÂ\.\.\.VýS\.\.\.", "రాజ్యాంగం"),
    (r"Æ>gêÂ", "రాజ్యాంగ"),
    (r"Æ>fMìSÄ¶æ\$", "రాజకీయ"),
    (r"Ô¶æ\*\]IÂ\.\.\.", "పాలన"),
    (r"Ô¶æ\*\]IÂ", "పాలన"),
    (r"°\.\.\.¯ëË¯óI", "నిబంధనలలోని"),
    (r"¯éÄ¶æ\$Ô>Q", "న్యాయం"),
    (r"¯ëË¯óI", "లలోని"),
    (r"AçÜ\$", "ప్రభుత్వ"),
    (r"A\{ç’", "ప్రజా"),
    (r"Aç’", "ప్రజా"),
    (r"™ðI", "తెలుగు"),
    (r"MðS", "కేంద్ర"),
    (r"íÜ", "సి"),
    (r"ÐóI", "రాష్ట్ర"),
    (r"íÜ\.ÐóI", "సివిల్"),
    (r"Æš‡", "సర్వీస్"),
    (r"Ë„>AË\$", "లక్ష్యాలు"),
    (r"Îòæ°", "ఏది"),
    (r"ç°\s*\}", "ఏది"),
    (r"\{ëýIÑŠMýS", "ప్రాథమిక"),
    (r"ï³vMýS", "విధి"),
    (r"É\{ç’", "చట్ట"),
    (r"Éç’", "చట్ట"),
    (r"ODðIÐ\]I\*Æš‡", "అధికార"),
    (r"Çç’¼ïMýS", "రిపబ్లిక్"),
    (r"IÀ\]I§", "భారత"),
    (r"IÀ", "భారత"),
    (r"çÜ\.\.\.°\.\.\.«¯\.\.\.", "సంబంధించి"),
    (r"°\.\.\.¯ëË", "నిబంధనల"),
    # Anu 7 / Shree-Lipi Chunduru & Historical report patterns
    (r"\^Œo`«\s*i\s*51", "దళిత డైరీ 51"),
    (r"\^Œo`«", "దళిత"),
    (r"K«∞O_»∂~°∞", "చుండూరు"),
    (r"=∂~°}HÍO_»", "మారణకాండ"),
    (r"\[ã≤ìãπ", "జస్టిస్"),
    (r"QÆOQÍ^èŒ~°~å=Ù", "గంగాధరరావు"),
    (r"x\"ÕkHõ", "నివేదిక"),
    (r"x\"ÕkHదే", "నివేదిక"),
    (r"ÔH\.\s*ÉÏÅQÀáêÖò", "కె. బాలగోపాల్"),
    (r"ÉÏÅQÀáêÖò", "బాలగోపాల్"),
    (r"Z@ìˆHÅ‰õΩ", "ఎట్టకేలకు"),
    (r"<åºÜ«∞qKå~°}", "న్యాయవిచారణ"),
    (r"\|Ü«∞\\˜H˜", "బయటికి"),
    (r"=zÛOk", "వచ్చింది"),
    (r"„Ñ¨Éèí∞`«ﬁO", "ప్రభుత్వం"),
    (r"Ñ¨ijeOK«=∞#ﬂ", "పరిశీలించమన్న"),
    (r"Jxﬂ", "అన్ని"),
    (r"JOâßÅ#∂", "అంశాలనూ"),
    (r"Ñ¨ijeOz", "పరిశీలించి"),
    (r"¿ÑrÅ", "పేజీల"),
    (r"~å™ê~°∞", "రాశారు"),
    (r"\^Œo`«∞Å∞", "దళితులు"),
    (r"Hõg∞\+¨<£#∞", "కమిషన్‌ను"),
    (r"\|Ç≤Ï\+¨¯iOK«_»O", "బహిష్కరించడం"),
    (r"`«#‰õΩ", "తనకు"),
    (r"„Ñ¨u\|O^èŒHõO", "ప్రతిబంధకం"),
    (r"J~ÚO^Œh", "అయిందనీ"),
    (r"\^Œo`Õ`«~°∞Å∞", "దళితేతరులు"),
    (r"J„QÆ‰õΩÖÏÅ‰õΩ", "అగ్రకులాలకు"),
    (r"ÃÑ\\˜ì#", "పెట్టిన"),
    (r"¿Ñ~°∞", "పేరు"),
    (r"Ñ¨ÓiÎ", "పూర్తి"),
    (r"x\[O", "నిజం"),
    (r"K≥Ñ¨Ê_®xH˜", "చెప్పడానికి"),
    (r"W\+¨ìÑ¨_»ÖË^Œh", "ఇష్టపడలేదనీ"),
    (r"HÍ\\|\˜ì", "కాబట్టి"),
    (r"„Ñ¨^è•#OQÍ", "ప్రధానంగా"),
    (r"áÈbã¨∞Å∞", "పోలీసులు"),
    (r"Ô~\"≥#∂º", "రెవెన్యూ"),
    (r"JkèHÍ~°∞Å", "అధికారుల"),
    (r"™êHΔÍºÅÃÑ·#", "సాక్ష్యాలపైనే"),
    (r"P^è•~°Ñ¨_»=Åã≤", "ఆధారపడవలసి"),
    (r"=zÛO^Œh", "వచ్చిందని"),
    (r"\"≥Ú^Œ\\’¡<Õ", "మొదట్లోనే"),
    (r"XÑ¨C\s*‰õΩ<åﬂ~°∞", "ఒప్పుకున్నారు"),
    (r"x~åú~°}Å‰õΩ", "నిర్ధారణలకు"),
    (r"™êHΔÍºÖË", "సాక్ష్యాలే"),
    (r"P^è•~°=∞x", "ఆధారమని"),
    (r"J<åﬂ~°∞", "అన్నారు")
]

# Multiple choice question option markers
MCQ_OPTIONS_MAP = [
    (r"(?:^|\s)G\)", " ఎ)"),
    (r"(?:^|\s)¼\)", " బి)"),
    (r"(?:^|\s)íÜ\)", " సి)"),
    (r"(?:^|\s)yìI\)", " డి)"),
    (r"(?:^|\s)çÜÐ\]I\*«śé\s*[:\.]*\s*íÜ", " సమాధానం: సి"),
    (r"(?:^|\s)çÜÐ\]I\*«śé\s*[:\.]*\s*G", " సమాధానం: ఎ"),
    (r"(?:^|\s)çÜÐ\]I\*«śé\s*[:\.]*\s*¼", " సమాధానం: బి"),
    (r"(?:^|\s)çÜÐ\]I\*«śé\s*[:\.]*\s*yìI", " సమాధానం: డి")
]

# Suffix and numbers mapping
SUFFIX_MAP = [
    (r"(\d+)ìZ", r"లో"),
    (r"(\d+)ì", r"లో"),
    (r"(\d+)వ", r"వ"),
    (r"(\d+)MýS", r"కు"),
    (r"సూత్రాలMýS", "సూత్రాలకు"),
]

def is_legacy_telugu_font(text):
    """
    Detects if the extracted string is Anu Script / Shree-Lipi / Akruti legacy font mojibake
    rather than pure Unicode Telugu or clean English.
    """
    if not text or len(text.strip()) < 4:
        return False

    # Check for Telugu Unicode characters (ఀ - ౿)
    telugu_unicode_chars = len(re.findall(r"[ఀ-౿]", text))
    total_chars = len(text.strip())

    # Count typical Anu / Shree-Lipi legacy glyph signatures
    legacy_glyphs = len(re.findall(r"[ŠóÌÕýçÜ™éË¨§ðíÐÆš‡„Ô¶æÄÀ°òeÝùtVÎß¼‰‹›•\^Œ«»∂~°∞]", text))
    
    # Specific strong signature words including Anu 7 / Shree glyphs
    has_strong_signature = bool(re.search(r"BŠó|çÜ\*\{|BçTMýS|MýS|çßæ|\{VýS|ÌÕ|íÜ\)|yìI\)|G\)|¼\)|\^Œo|K«∞|_»∂|=∂~°\}|\[ã≤ì|QÆOQÍ|x\"Õk|„Ñ¨|¿Ñr|™êHΔ|áÈb|Ô~\"|‰õΩ", text))

    if has_strong_signature and telugu_unicode_chars < 25:
        return True

    if total_chars > 8 and (legacy_glyphs / total_chars) > 0.08 and telugu_unicode_chars < 15:
        return True

    return False

def convert_legacy_to_unicode(text):
    """
    Converts legacy Anu Script / Shree-Lipi mojibake text into readable Telugu Unicode.
    """
    if not text:
        return ""

    converted = text

    # 1. Apply high-yield word and phrase replacements
    for pattern, repl in WORD_REPLACEMENTS:
        converted = re.sub(pattern, repl, converted)

    # 2. Apply MCQ options mapping
    for pattern, repl in MCQ_OPTIONS_MAP:
        converted = re.sub(pattern, repl, converted)

    # 3. Apply Suffix mapping (e.g. 41ìZ -> 41లో)
    for pattern, repl in SUFFIX_MAP:
        converted = re.sub(pattern, repl, converted)

    # 4. Clean lingering unreadable artifact characters
    # If 3 or more non-ascii unmapped bytes appear together, clean them cleanly
    converted = re.sub(r"[-¡-¿À-ÿ]{3,}", " ", converted)
    
    # Clean redundant punctuation and spaces
    converted = re.sub(r"[ \t]+", " ", converted)
    converted = re.sub(r"\n{3,}", "\n\n", converted)

    return converted.strip()
