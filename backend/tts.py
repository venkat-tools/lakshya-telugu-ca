# -*- coding: utf-8 -*-
"""
Native Telugu Neural Text-To-Speech (TTS) Engine.
Uses Microsoft Azure Neural AI voices for ultra-realistic human Telugu speech:
- te-IN-MohanNeural (పురుష స్వరం - Male Human Voice / News Anchor style)
- te-IN-ShrutiNeural (మహిళా స్వరం - Female Human Voice / Professional presenter style)
Features phonetic pronunciation normalization for exam acronyms and technical terms,
caching for lightning-fast playback, and robust fallback.
"""

import os
import re
import sys
import html
import asyncio
import hashlib
import urllib.request
import urllib.parse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CACHE_DIR = os.path.join(os.path.dirname(__file__), "audio_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

# Microsoft Edge Neural Telugu Voices
NEURAL_VOICES = {
    "mohan": "te-IN-MohanNeural",      # Male - Authoritative, natural, human cadence
    "shruti": "te-IN-ShrutiNeural",    # Female - Clear, crisp, human news presenter
    "male": "te-IN-MohanNeural",
    "female": "te-IN-ShrutiNeural"
}
DEFAULT_VOICE = "mohan"

# Comprehensive phonetic normalization for Telugu exam terms & acronyms
PRONUNCIATION_MAP = [
    (r'&zwnj;|&nbsp;|&zwj;|&amp;|&quot;|&#39;|&lt;|&gt;', ' '),
    (r'\bAPPSC\b', 'ఏపీపీఎస్సీ'),
    (r'\bTSPSC\b', 'టీఎస్పీఎస్సీ'),
    (r'\bUPSC\b', 'యూపీఎస్సీ'),
    (r'\bSSC\b', 'ఎస్ఎస్సీ'),
    (r'\bISRO\b', 'ఇస్రో'),
    (r'\bDRDO\b', 'డీఆర్డీవో'),
    (r'\bRBI\b', 'ఆర్బీఐ'),
    (r'\bCJI\b', 'సీజేఐ'),
    (r'\bCAG\b', 'కాగ్'),
    (r'\bGST\b', 'జీఎస్టీ'),
    (r'\bGDP\b', 'జీడీపీ'),
    (r'\bPESA\b', 'పీసా'),
    (r'\bPVTG\b', 'పీవీటీజీ'),
    (r'\bPVTGs\b', 'పీవీటీజీలు'),
    (r'\bTMC\b', 'టీఎంసీ'),
    (r'\bMSP\b', 'ఎంఎస్పీ'),
    (r'\bPDF\b', 'పీడీఎఫ్'),
    (r'\bEWS\b', 'ఈడబ్ల్యూఎస్'),
    (r'\bIIT\b', 'ఐఐటీ'),
    (r'\bAIIMS\b', 'ఎయిమ్స్'),
    (r'\bITDA\b', 'ఐటీడీఏ'),
    (r'\bNCST\b', 'ఎన్‌సీఎస్టీ'),
    (r'\bFRBM\b', 'ఎఫ్ఆర్బీఎం'),
    (r'\bNASA\b', 'నాసా'),
    (r'\bWHO\b', 'డబ్ల్యూహెచ్‌ఓ'),
    (r'\bIMF\b', 'ఐఎంఎఫ్'),
    (r'\bUN\b', 'ఐక్యరాజ్య సమితి'),
    (r'\bAI\b', 'కృత్రిమ మేధ'),
    (r'\bCEC\b', 'సీఈసీ'),
    (r'\bECs\b', 'ఎన్నికల కమిషనర్లు'),
    (r'\bEC\b', 'ఈసీ'),
    (r'\bADB\b', 'ఏడీబీ'),
    (r'\bWorld Bank\b', 'వరల్డ్ బ్యాంక్'),
    (r'\bSI\b', 'ఎస్సై'),
    (r'\bDSP\b', 'డీఎస్పీ'),
    (r'\bSP\b', 'ఎస్పీ'),
    (r'\bCI\b', 'సీఐ'),
    (r'\bPF\b', 'పీఎఫ్'),
    (r'\bTTD\b', 'టీటీడీ'),
    (r'\bTDP\b', 'టీడీపీ'),
    (r'\bYSRCP\b', 'వైఎస్సార్సీపీ'),
    (r'\bBJP\b', 'బీజేపీ'),
    (r'\bBRS\b', 'బీఆర్ఎస్'),
    (r'\bJSP\b', 'జనసేన'),
    (r'\bTVK\b', 'టీవీకే'),
    (r'\bCBT\b', 'సీబీటీ'),
    (r'\bOMR\b', 'ఓఎంఆర్'),
    (r'\bPYQ\b', 'గత ప్రశ్నలు'),
    (r'\bPYQs\b', 'గత ప్రశ్నలు'),
    (r'\bGS\b', 'జనరల్ స్టడీస్'),
    (r'\bMCQ\b', 'ప్రశ్న'),
    (r'\bMCQs\b', 'ప్రశ్నలు'),
    (r'\bBC\b|\bక్రీ\.పూ\.?\b', 'క్రీస్తు పూర్వం'),
    (r'\bAD\b|\bక్రీ\.శ\.?\b', 'క్రీస్తు శకం'),
    (r'\bINC\b', 'భారత జాతీయ కాంగ్రెస్'),
    (r'\bkm²\b|\bsq km\b|\bsq\.km\b', 'చదరపు కిలోమీటర్లు'),
    (r'\bkm/h\b|\bkmph\b', 'కిలోమీటర్లు ప్రతి గంటకు'),
    (r'\bm/s\b', 'మీటర్లు ప్రతి సెకనుకు'),
    (r'\bMPI\b', 'మల్టీడైమెన్షనల్ పావర్టీ ఇండెక్స్'),
    (r'\bPM-JANMAN\b', 'పీఎం జనమన్'),
    (r'\bLVM-3\b|\bLVM3\b', 'ఎల్వీఎం త్రీ'),
    (r'\bMIRV\b', 'ఎంఐఆర్వీ'),
    (r'\bINS\b', 'ఐఎన్ఎస్'),
    (r'\bGPUs?\b', 'జీపీయూలు'),
    (r'\bAI\b', 'కృత్రిమ మేధస్సు'),
    (r'\bPOCSO\b', 'పోక్సో'),
    (r'\bUCC\b', 'ఉమ్మడి పౌరస్మృతి'),
    (r'₹\s*([0-9,]+)\s*కోట్ల', r'\1 కోట్ల రూపాయల'),
    (r'₹\s*([0-9,]+)\s*కోట్లు', r'\1 కోట్ల రూపాయలు'),
    (r'₹\s*([0-9,]+)', r'\1 రూపాయలు'),
    (r'రూ\.\s*([0-9,]+)\s*కోట్ల', r'\1 కోట్ల రూపాయల'),
    (r'రూ\.\s*([0-9,]+)\s*కోట్లు', r'\1 కోట్ల రూపాయలు'),
    (r'రూ\.\s*([0-9,]+)', r'\1 రూపాయలు'),
    (r'([0-9,]+)\s*రూపాయలు\s*కోట్ల', r'\1 కోట్ల రూపాయల'),
    (r'([0-9,]+)\s*రూపాయలు\s*కు', r'\1 రూపాయలకు'),
    (r'%', ' శాతం '),
    (r'&', ' మరియు '),
    (r'\bvs\.?\b|\bv\.\b', ' వర్సెస్ '),
    (r'\bకి\.మీ\.?\b|\bkm\b', ' కిలోమీటర్లు '),
    (r'\bనం\.?\b|\bNo\.?\b', ' నంబర్ ')
]

def clean_text_for_speech(text):
    """Clean markdown, tags and apply phonetic replacements for natural Telugu human speech"""
    if not text:
        return ""
    # Decode HTML entities
    text = html.unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove URLs
    text = re.sub(r'https?:\/\/\S+', '', text)
    # Remove markdown symbols and brackets
    text = re.sub(r'[*_#`~\[\]\(\)\{\}]', ' ', text)
    
    # Apply phonetic pronunciation mapping for natural Telugu output
    for pattern, repl in PRONUNCIATION_MAP:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        
    # Replace colons and semicolons with natural breathing pauses
    text = re.sub(r'\s*[:;]\s*', '... ', text)
    # Replace hyphens with commas for natural flow
    text = re.sub(r'\s*-\s*', ', ', text)
    # Normalize multiple dots into single ellipsis
    text = re.sub(r'\.{2,}', '... ', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def _fetch_google_tts_fallback(text):
    """Fallback to Google TTS in chunks if Edge TTS is unavailable"""
    try:
        sentences = re.split(r'([।\.\n\?\!])', text)
        chunks = []
        current = ""
        for s in sentences:
            if len(current) + len(s) <= 150:
                current += s
            else:
                if current.strip():
                    chunks.append(current.strip())
                current = s
        if current.strip():
            chunks.append(current.strip())

        audio_data = bytearray()
        headers = {"User-Agent": "Mozilla/5.0"}
        for c in chunks:
            if not c.strip():
                continue
            url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=te&client=tw-ob&q=" + urllib.parse.quote(c.strip())
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=8) as response:
                audio_data.extend(response.read())
        return bytes(audio_data)
    except Exception as e:
        print(f"Fallback TTS Error: {e}")
        return b""

async def _synthesize_edge_tts(text, voice_id, rate="-5%", pitch="+0Hz"):
    """Synthesize speech using edge-tts async API with natural human pacing"""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice_id, rate=rate, pitch=pitch)
    audio_data = bytearray()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_data.extend(chunk["data"])
    return bytes(audio_data)

def generate_telugu_audio(text, voice="mohan"):
    """
    Takes Telugu text, applies phonetic corrections, and generates natural human voice audio.
    Supports voices:
    - 'mohan' / 'male' (te-IN-MohanNeural)
    - 'shruti' / 'female' (te-IN-ShrutiNeural)
    Caches MP3 files locally for instantaneous playback.
    """
    text_clean = clean_text_for_speech(text)
    if not text_clean:
        return b""

    voice_key = voice.lower().strip() if voice else DEFAULT_VOICE
    voice_id = NEURAL_VOICES.get(voice_key, NEURAL_VOICES[DEFAULT_VOICE])

    # Cache check based on text hash + voice
    text_hash = hashlib.md5((text_clean + voice_id).encode('utf-8')).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{text_hash}.mp3")
    if os.path.exists(cache_file) and os.path.getsize(cache_file) > 1000:
        with open(cache_file, "rb") as f:
            return f.read()

    # Attempt Neural Synthesis via edge-tts
    audio_bytes = b""
    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                audio_bytes = pool.submit(asyncio.run, _synthesize_edge_tts(text_clean, voice_id)).result()
        else:
            audio_bytes = asyncio.run(_synthesize_edge_tts(text_clean, voice_id))
    except Exception as e:
        print(f"Edge TTS Synthesis Warning: {e}, attempting Google TTS fallback...")
        audio_bytes = _fetch_google_tts_fallback(text_clean)

    # Save to cache if successful
    if audio_bytes and len(audio_bytes) > 500:
        try:
            with open(cache_file, "wb") as f:
                f.write(audio_bytes)
        except Exception as e:
            print(f"Error caching audio: {e}")
        return audio_bytes

    return b""

def build_conversational_bulletin_script(date, articles, one_liners):
    """
    Builds a human news anchor podcast script with natural cadence,
    conversational transitions, breathing pauses, and sign-offs.
    Eliminates robotic numbered lists ('వార్త 1...', 'వార్త 2...').
    """
    intro = (
        "నమస్కారం అండి! లక్ష్య డైలీ తెలుగు కరెంట్ అఫైర్స్ ఆడియో పాడ్‌కాస్ట్‌కు స్వాగతం... "
        "పోటీ పరీక్షల ప్రత్యేకం... ఈనాటి ముఖ్యమైన వార్తా విశేషాలు ఇప్పుడు విశ్లేషణాత్మకంగా పరిశీలిద్దాం.\n\n"
    )

    transitions_map = {
        "regional": "ఇక తెలుగు రాష్ట్రాల విషయానికి వస్తే... ",
        "national": "అలాగే జాతీయ పరిణామాలను గమనిస్తే... ",
        "international": "ఇక అంతర్జాతీయ ముఖ్యాంశాల్లోకి వెళితే... ",
        "economy": "ఇక ఆర్థిక రంగానికి సంబంధించిన సమాచారాన్ని పరిశీలిస్తే... ",
        "science": "సైన్స్ మరియు టెక్నాలజీ విభాగంలో మరో కీలక పరిణామం... ",
        "sports": "క్రీడా రంగానికి సంబంధించిన విశేషాల్లోకి వెళితే... ",
        "environment": "పర్యావరణం మరియు భౌగోళిక అంశాలను చూస్తే... ",
        "polity": "రాజ్యాంగం మరియు పాలనాపరమైన పరిణామాలను పరిశీలిస్తే... "
    }

    general_transitions = [
        "మొదటిగా నేటి అత్యంత ప్రధానమైన పరీక్షాంశాన్ని పరిశీలిస్తే... ",
        "ఇక మరో ముఖ్యమైన పరిణామం... ",
        "అలాగే పోటీ పరీక్షల కోణంలో కీలకమైన మరో అంశం... ",
        "మరో ముఖ్య సమాచారాన్ని గమనిస్తే... ",
        "ఇక తదుపరి ప్రధాన విశేషం... ",
        "చివరిగా మరో ముఖ్యమైన అంశాన్ని చూస్తే... "
    ]

    used_categories = set()
    body_parts = []

    for idx, a in enumerate(articles[:6]):
        t = clean_text_for_speech(a.get("title", ""))
        s = clean_text_for_speech(a.get("summary", ""))
        
        # Avoid repeating title verbatim if summary starts with title
        if t and s.startswith(t[:25]):
            s = s[len(t):].strip(" .:-")

        # Trim summary gently at natural sentence ending
        if len(s) > 160:
            p_idx = max(s[:160].rfind("."), s[:160].rfind("!"), s[:160].rfind("?"))
            if p_idx > 60:
                s = s[:p_idx + 1]
            else:
                s = s[:160].rsplit(" ", 1)[0] + "..."

        cat = (a.get("category") or "").lower()
        if idx == 0:
            prefix = "మొదటిగా నేటి అత్యంత ప్రధానమైన అంశాన్ని పరిశీలిస్తే... "
        elif cat in transitions_map and cat not in used_categories:
            prefix = transitions_map[cat]
            used_categories.add(cat)
        elif idx < len(general_transitions):
            prefix = general_transitions[idx]
        else:
            prefix = "ఇక తదుపరి అంశం... "

        body_parts.append(f"{prefix}{t}... {s}\n\n")

    one_liners_script = ""
    if one_liners:
        one_liners_script = "ఇక పోటీ పరీక్షల శీఘ్ర పునశ్చరణ కోసం, నేటి వన్-లైనర్స్ క్విక్ రౌండప్ గమనిద్దాం...\n\n"
        ol_pfx = [
            "మొదటి అంశం... ",
            "రెండవది... ",
            "మూడవ అంశం... ",
            "నాల్గవ పరిణామం... ",
            "అలాగే... ",
            "చివరి పాయింట్... "
        ]
        for i, ol in enumerate(one_liners[:5]):
            pt = clean_text_for_speech(ol.get("point", ""))
            p = ol_pfx[i] if i < len(ol_pfx) else "అలాగే... "
            one_liners_script += f"{p}{pt}.\n\n"

    outro = (
        "మిత్రులారా... ఇవి ఈనాటి అత్యంత ముఖ్యమైన కరెంట్ అఫైర్స్ విశేషాలు... "
        "పూర్తి ఈ-పేపర్ పీడీఎఫ్, సిలబస్ గైడ్ మరియు ప్రాక్టీస్ మాక్ టెస్టుల కోసం మన లక్ష్య పోర్టల్‌ను సందర్శించండి... "
        "పోటీ పరీక్షలకు సిద్ధమవుతున్న ప్రతి ఒక్కరికీ ఆల్ ది వెరీ బెస్ట్... ధన్యవాదాలు, నమస్కారం!"
    )

    full_script = intro + "".join(body_parts) + one_liners_script + outro
    return full_script

def generate_daily_bulletin_audio(date=None, force_refresh=False, voice="mohan"):
    """
    Generate a natural 3-4 minute spoken Telugu audio bulletin for the day's
    top headlines, one-liners, and exam takeaways using human Neural AI voice.
    Saves to:
    - backend/audio_cache/daily_bulletin_{date}_{voice}.mp3
    - frontend/audio/daily_bulletin_today.mp3
    - frontend/audio/daily_bulletin_{voice}.mp3
    """
    from db import get_articles, get_one_liners_by_date, get_available_dates
    dates = get_available_dates()
    latest_date = dates[0] if dates else "2026-09-16"

    if not date:
        date = latest_date

    voice_key = voice.lower().strip() if voice else DEFAULT_VOICE
    frontend_audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "audio")
    os.makedirs(frontend_audio_dir, exist_ok=True)
    
    today_mp3_path = os.path.join(frontend_audio_dir, "daily_bulletin_today.mp3")
    voice_today_mp3_path = os.path.join(frontend_audio_dir, f"daily_bulletin_{voice_key}.mp3")
    cache_mp3_path = os.path.join(CACHE_DIR, f"daily_bulletin_{date}_{voice_key}.mp3")

    if not force_refresh and os.path.exists(cache_mp3_path) and os.path.getsize(cache_mp3_path) > 10000:
        return cache_mp3_path

    articles = get_articles(date=date)
    # If no articles for given date, fallback to latest date with articles
    if not articles and dates:
        date = latest_date
        articles = get_articles(date=date)
        cache_mp3_path = os.path.join(CACHE_DIR, f"daily_bulletin_{date}_{voice_key}.mp3")
        if not force_refresh and os.path.exists(cache_mp3_path) and os.path.getsize(cache_mp3_path) > 10000:
            return cache_mp3_path

    one_liners = get_one_liners_by_date(date=date)

    # Build human conversational podcast script
    script = build_conversational_bulletin_script(date, articles, one_liners)

    # Generate MP3 via Neural Voice
    audio_bytes = generate_telugu_audio(script, voice=voice_key)
    if audio_bytes and len(audio_bytes) > 5000:
        try:
            with open(cache_mp3_path, "wb") as f:
                f.write(audio_bytes)
            with open(voice_today_mp3_path, "wb") as f:
                f.write(audio_bytes)
            if voice_key == "mohan" or not os.path.exists(today_mp3_path):
                with open(today_mp3_path, "wb") as f:
                    f.write(audio_bytes)
        except Exception as e:
            print(f"Error saving bulletin audio: {e}")
        return cache_mp3_path

    return None

def generate_syllabus_audio_track(track_id, voice="mohan", force_refresh=False):
    """
    Generate or retrieve a high-yield Telugu audio revision track for competitive exam subjects.
    Supports: Indian History, Geography, Indian Society, Polity, Economy, Science & Tech, Aptitude.
    """
    from audio_revision_data import get_track_by_id
    track = get_track_by_id(track_id)
    if not track:
        return None

    voice_key = voice.lower().strip() if voice else DEFAULT_VOICE
    frontend_audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "audio")
    os.makedirs(frontend_audio_dir, exist_ok=True)
    
    tid = track.get("id", track_id)
    cache_file = os.path.join(CACHE_DIR, f"{tid}_{voice_key}.mp3")
    frontend_file = os.path.join(frontend_audio_dir, f"{tid}_{voice_key}.mp3")

    if not force_refresh and os.path.exists(cache_file) and os.path.getsize(cache_file) > 10000:
        return cache_file

    script = track.get("script", "")
    if not script:
        return None

    # Synthesize via Neural Voice
    audio_bytes = generate_telugu_audio(script, voice=voice_key)
    if audio_bytes and len(audio_bytes) > 5000:
        try:
            with open(cache_file, "wb") as f:
                f.write(audio_bytes)
            with open(frontend_file, "wb") as f:
                f.write(audio_bytes)
        except Exception as e:
            print(f"Error saving syllabus audio track {track_id}: {e}")
        return cache_file

    return None

if __name__ == "__main__":
    print("Testing Neural Telugu Voice Engine...")
    test_msg = "నమస్కారం! లక్ష్య డైలీ కరెంట్ అఫైర్స్ కు స్వాగతం. APPSC మరియు TSPSC గ్రూప్స్ కోసం సహజ మానవ స్వరంలో వార్తలు వినండి."
    mohan_bytes = generate_telugu_audio(test_msg, voice="mohan")
    print(f"Mohan Audio size: {len(mohan_bytes)} bytes")
    shruti_bytes = generate_telugu_audio(test_msg, voice="shruti")
    print(f"Shruti Audio size: {len(shruti_bytes)} bytes")
