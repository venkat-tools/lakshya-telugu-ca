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
