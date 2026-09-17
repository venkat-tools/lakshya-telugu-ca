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
    (r'\bUN\b', 'యూఎన్'),
    (r'\bAI\b', 'ఏఐ'),
    (r'\bCBT\b', 'సీబీటీ'),
    (r'\bOMR\b', 'ఓఎంఆర్'),
    (r'\bPYQ\b', 'గత ప్రశ్నలు'),
    (r'\bPYQs\b', 'గత ప్రశ్నలు'),
    (r'\bGS\b', 'జనరల్ స్టడీస్'),
    (r'\bMCQ\b', 'ప్రశ్న'),
    (r'\bMCQs\b', 'ప్రశ్నలు'),
    (r'₹\s*([0-9,]+)', r'\1 రూపాయలు'),
    (r'%', ' శాతం '),
    (r'&', ' మరియు '),
    (r'\bకి\.మీ\.?\b', ' కిలోమీటర్లు '),
    (r'\bనం\.?\b', ' నెంబర్ ')
]

def clean_text_for_speech(text):
    """Clean markdown, tags and apply phonetic replacements"""
    if not text:
        return ""
    # Remove html tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove URLs
    text = re.sub(r'https?:\/\/\S+', '', text)
    # Remove markdown symbols
    text = re.sub(r'[*_#`~]', '', text)
    
    # Apply phonetic pronunciation mapping for natural Telugu output
    for pattern, repl in PRONUNCIATION_MAP:
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
        
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

async def _synthesize_edge_tts(text, voice_id):
    """Synthesize speech using edge-tts async API"""
    import edge_tts
    communicate = edge_tts.Communicate(text, voice_id, rate="-2%", pitch="+0Hz")
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

def generate_daily_bulletin_audio(date=None, force_refresh=False, voice="mohan"):
    """
    Generate a natural 3-5 minute spoken Telugu audio bulletin for the day's
    top headlines, one-liners, and exam takeaways using human Neural AI voice.
    Saves to:
    - backend/audio_cache/daily_bulletin_{date}_{voice}.mp3
    - frontend/audio/daily_bulletin_today.mp3
    """
    from db import get_articles, get_one_liners_by_date, get_available_dates
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else "2026-09-17"

    voice_key = voice.lower().strip() if voice else DEFAULT_VOICE
    frontend_audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "audio")
    os.makedirs(frontend_audio_dir, exist_ok=True)
    
    today_mp3_path = os.path.join(frontend_audio_dir, "daily_bulletin_today.mp3")
    voice_today_mp3_path = os.path.join(frontend_audio_dir, f"daily_bulletin_{voice_key}.mp3")
    cache_mp3_path = os.path.join(CACHE_DIR, f"daily_bulletin_{date}_{voice_key}.mp3")

    if not force_refresh and os.path.exists(cache_mp3_path) and os.path.getsize(cache_mp3_path) > 10000:
        return cache_mp3_path

    articles = get_articles(date=date)
    one_liners = get_one_liners_by_date(date=date)

    # Professional Telugu News Anchor Script
    script = (
        f"నమస్కారం మిత్రులారా. లక్ష్య డైలీ తెలుగు కరెంట్ అఫైర్స్ మరియు పోటీ పరీక్షల ప్రత్యేక ఆడియో బులెటిన్‌కు స్వాగతం. "
        f"నేటి తేదీ: {date}. "
        f"ముందుగా నేటి ప్రధాన పోటీ పరీక్షల ముఖ్యాంశాలు. "
    )

    for idx, a in enumerate(articles[:6], 1):
        t = clean_text_for_speech(a.get("title", ""))
        s = clean_text_for_speech(a.get("summary", ""))[:150]
        script += f"వార్త {idx}: {t}. {s}. "

    if one_liners:
        script += "ఇక శీఘ్ర పునశ్చరణ కోసం ఒక వరుస ముఖ్యాంశాలు. "
        for ol in one_liners[:6]:
            pt = clean_text_for_speech(ol.get("point", ""))
            script += f"{pt}. "

    script += (
        "నేటి పూర్తి ఈ-పేపర్ పీడీఎఫ్, సిలబస్ గైడ్, మాక్ టెస్టులు మరియు ఆన్‌లైన్ ప్రాక్టీస్ కోసం "
        "లక్ష్య పోర్టల్ ను సందర్శించండి. ఆల్ ది బెస్ట్."
    )

    # Generate MP3 via Neural Voice
    audio_bytes = generate_telugu_audio(script, voice=voice_key)
    if audio_bytes and len(audio_bytes) > 5000:
        try:
            with open(cache_mp3_path, "wb") as f:
                f.write(audio_bytes)
            with open(today_mp3_path, "wb") as f:
                f.write(audio_bytes)
            with open(voice_today_mp3_path, "wb") as f:
                f.write(audio_bytes)
        except Exception as e:
            print(f"Error saving bulletin audio: {e}")
        return cache_mp3_path

    return None

if __name__ == "__main__":
    print("Testing Neural Telugu Voice Engine...")
    test_msg = "నమస్కారం! లక్ష్య డైలీ కరెంట్ అఫైర్స్ కు స్వాగతం. APPSC మరియు TSPSC గ్రూప్స్ కోసం సహజ మానవ స్వరంలో వార్తలు వినండి."
    mohan_bytes = generate_telugu_audio(test_msg, voice="mohan")
    print(f"Mohan Audio size: {len(mohan_bytes)} bytes")
    shruti_bytes = generate_telugu_audio(test_msg, voice="shruti")
    print(f"Shruti Audio size: {len(shruti_bytes)} bytes")
