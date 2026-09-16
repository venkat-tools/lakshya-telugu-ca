# -*- coding: utf-8 -*-
"""
Native Telugu Text-To-Speech (TTS) Engine.
Fetches high quality, fluent, natural Telugu voice audio
and streams it to the web browser.
"""

import os
import re
import urllib.request
import urllib.parse
import hashlib

CACHE_DIR = os.path.join(os.path.dirname(__file__), "audio_cache")
os.makedirs(CACHE_DIR, exist_ok=True)

def clean_text_for_speech(text):
    # Remove html tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove URLs
    text = re.sub(r'https?://\S+', '', text)
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def split_into_chunks(text, max_len=180):
    """Split long text into sentence/phrase chunks <= max_len"""
    sentences = re.split(r'([।\.\n\?\!])', text)
    chunks = []
    current = ""
    for s in sentences:
        if len(current) + len(s) <= max_len:
            current += s
        else:
            if current.strip():
                chunks.append(current.strip())
            # If a single sentence is too long, split by space/comma
            if len(s) > max_len:
                words = s.split(" ")
                sub = ""
                for w in words:
                    if len(sub) + len(w) + 1 <= max_len:
                        sub += (" " + w if sub else w)
                    else:
                        if sub.strip():
                            chunks.append(sub.strip())
                        sub = w
                current = sub
            else:
                current = s
    if current.strip():
        chunks.append(current.strip())
    return [c for c in chunks if c.strip()]

def fetch_chunk_audio(chunk):
    """Fetch MP3 bytes for a small chunk of Telugu text"""
    url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=te&client=tw-ob&q=" + urllib.parse.quote(chunk)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.read()
    except Exception as e:
        print(f"TTS Chunk Error: {e}")
        return b""

def generate_telugu_audio(text):
    """
    Takes Telugu text, splits into chunks, fetches native Telugu voice audio,
    and returns combined MP3 bytes. Uses local cache for speed.
    """
    text_clean = clean_text_for_speech(text)
    if not text_clean:
        return b""

    # Cache check
    text_hash = hashlib.md5(text_clean.encode('utf-8')).hexdigest()
    cache_file = os.path.join(CACHE_DIR, f"{text_hash}.mp3")
    if os.path.exists(cache_file):
        with open(cache_file, "rb") as f:
            return f.read()

    chunks = split_into_chunks(text_clean, max_len=180)
    audio_data = bytearray()

    for c in chunks:
        chunk_bytes = fetch_chunk_audio(c)
        if chunk_bytes:
            audio_data.extend(chunk_bytes)

    if audio_data:
        try:
            with open(cache_file, "wb") as f:
                f.write(audio_data)
        except Exception as e:
            print(f"Error caching audio: {e}")

    return bytes(audio_data)

if __name__ == "__main__":
    audio = generate_telugu_audio("నమస్కారం! నేటి ముఖ్యమైన కరెంట్ అఫైర్స్ కి స్వాగతం.")
    print("Audio size in bytes:", len(audio))


def generate_daily_bulletin_audio(date=None, force_refresh=False):
    """
    Generate a 3-5 minute spoken Telugu audio bulletin for the day's
    top headlines, one-liners, and exam takeaways.
    Saves to backend/audio_cache/daily_bulletin_{date}.mp3
    and frontend/audio/daily_bulletin_today.mp3
    """
    from db import get_articles, get_one_liners_by_date, get_available_dates
    if not date:
        dates = get_available_dates()
        date = dates[0] if dates else "2026-09-16"

    frontend_audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend", "audio")
    os.makedirs(frontend_audio_dir, exist_ok=True)
    today_mp3_path = os.path.join(frontend_audio_dir, "daily_bulletin_today.mp3")
    cache_mp3_path = os.path.join(CACHE_DIR, f"daily_bulletin_{date}.mp3")

    if not force_refresh and os.path.exists(cache_mp3_path) and os.path.getsize(cache_mp3_path) > 10000:
        return cache_mp3_path

    articles = get_articles(date=date)
    one_liners = get_one_liners_by_date(date=date)

    # Build Telugu voice script
    script = f"నమస్కారం మిత్రులారా. లక్ష్య డైలీ తెలుగు కరెంట్ అఫైర్స్ మరియు పోటీ పరీక్షల ప్రత్యేక ఆడియో బులెటిన్‌కు స్వాగతం. "
    script += f"నేటి తేదీ: {date}. "
    script += "ముందుగా నేటి ప్రధాన పోటీ పరీక్షల ముఖ్యాంశాలు. "

    for idx, a in enumerate(articles[:5], 1):
        t = clean_text_for_speech(a.get("title", ""))
        s = clean_text_for_speech(a.get("summary", ""))[:140]
        script += f"వార్త {idx}: {t}. {s}. "

    if one_liners:
        script += "ఇక శీఘ్ర పునశ్చరణ కోసం ఒక వరుస ముఖ్యాంశాలు. "
        for ol in one_liners[:5]:
            pt = clean_text_for_speech(ol.get("point", ""))
            script += f"{pt}. "

    script += "నేటి పూర్తి ఈ-పేపర్ పిడిఎఫ్, సిలబస్ గైడ్ మరియు ప్రాక్టీస్ క్విజ్ కోసం లక్ష్య పోర్టల్ ను సందర్శించండి. ఆల్ ది బెస్ట్."

    # Generate MP3
    audio_bytes = generate_telugu_audio(script)
    if audio_bytes:
        with open(cache_mp3_path, "wb") as f:
            f.write(audio_bytes)
        try:
            with open(today_mp3_path, "wb") as f:
                f.write(audio_bytes)
        except Exception:
            pass
        return cache_mp3_path
    return None
