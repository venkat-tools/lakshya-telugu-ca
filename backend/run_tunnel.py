import subprocess
import re
import time
import urllib.request
import urllib.parse
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLOUDFLARED_EXE = os.path.join(BASE_DIR, "cloudflared.exe")
INFO_FILE = os.path.join(BASE_DIR, "tunnel_info.json")

# Ensure backend directory is in path for telegram notifications
sys.path.insert(0, os.path.join(BASE_DIR, "backend"))

def send_telegram_tunnel_alert(direct_url, tiny_url, clean_url):
    try:
        from telegram_bot import send_telegram_message
        msg = (
            f"🚀 <b>మొబైల్ యాక్సెస్ లింక్ (4G / 5G) సిద్ధంగా ఉంది!</b>\n"
            f"───────────────────────\n"
            f"మీరు మొబైల్ ఫోన్ ద్వారా ఎక్కడి నుంచైనా డ్యాష్‌బోర్డ్, 56 ఆర్టికల్స్ మరియు ఈ-పేపర్స్ చదవడానికి తాజా లింక్స్:\n\n"
            f"🌟 <b>ప్రధాన లింక్ (TinyURL):</b>\n👉 {tiny_url}\n\n"
            f"⚡ <b>ప్రత్యామ్నాయ లింక్ (CleanURI):</b>\n👉 {clean_url}\n\n"
            f"🔗 <b>డైరెక్ట్ క్లౌడ్‌ఫ్లేర్ లింక్:</b>\n👉 {direct_url}\n\n"
            f"<i>(ఈ లింక్ క్లిక్ చేయగానే మొబైల్‌లో యాప్ ఓపెన్ అవుతుంది)</i>"
        )
        send_telegram_message(msg)
        print("Telegram alert sent successfully!")
    except Exception as e:
        print(f"Telegram alert note: {e}")

def get_cleanuri(url):
    try:
        data = urllib.parse.urlencode({'url': url}).encode('utf-8')
        req = urllib.request.Request('https://cleanuri.com/api/v1/shorten', data=data, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            return data.get('result_url')
    except Exception as e:
        print(f"cleanuri error: {e}")
        return None

def get_clck(url):
    try:
        api = f'https://clck.ru/--?url={urllib.parse.quote(url)}'
        req = urllib.request.Request(api, headers={'User-Agent': 'curl/7.68.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.read().decode('utf-8').strip()
    except Exception as e:
        print(f"clck error: {e}")
        return None

def get_tinyurl(url, custom_alias=None):
    if custom_alias:
        try:
            api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}&alias={urllib.parse.quote(custom_alias)}"
            req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=8) as resp:
                res = resp.read().decode('utf-8').strip()
                if "Error" not in res and "tinyurl.com" in res:
                    return res
        except Exception as e:
            print(f"TinyURL alias note: {e}")
    try:
        api_url = f"https://tinyurl.com/api-create.php?url={urllib.parse.quote(url)}"
        req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=8) as resp:
            return resp.read().decode('utf-8').strip()
    except Exception as e:
        print(f"TinyURL fallback error: {e}")
        return url

def run_single_tunnel():
    """Runs a single cloudflared session. Returns True if restarted due to error."""
    if not os.path.exists(CLOUDFLARED_EXE):
        print(f"Error: {CLOUDFLARED_EXE} not found.")
        sys.exit(1)

    print("\n========================================================")
    print("Starting Fresh Cloudflare Tunnel on http://127.0.0.1:5000 ...")
    print("========================================================")
    
    cmd = [CLOUDFLARED_EXE, "tunnel", "--url", "http://127.0.0.1:5000", "--no-autoupdate"]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    tunnel_url = None
    url_pattern = re.compile(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com")
    error_patterns = [
        "Unauthorized: Tunnel not found",
        "Tunnel not found",
        "failed to request new edge connection"
    ]

    for line in iter(process.stdout.readline, ''):
        sys.stdout.write(line)
        sys.stdout.flush()

        # Check for tunnel fatal errors requiring restart
        if any(err in line for err in error_patterns):
            print(f"\n⚠️ Tunnel session expired or disconnected: {line.strip()}")
            print("Restarting fresh tunnel now...")
            process.kill()
            time.sleep(2)
            return True

        match = url_pattern.search(line)
        if match and not tunnel_url:
            tunnel_url = match.group(0)
            print("\n" + "="*60)
            print(f"CLOUDFLARE DIRECT URL: {tunnel_url}")
            print("="*60)

            info = {
                "direct_tunnel_url": tunnel_url,
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "ACTIVE"
            }

            with open(INFO_FILE, "w", encoding="utf-8") as f:
                json.dump(info, f, indent=2)

            print("\n" + "*"*60)
            print(f"🔗 DIRECT CLEAN CLOUDFLARE URL: {tunnel_url}")
            print("*"*60 + "\n")

            # Alert Telegram with direct clean URL
            send_telegram_tunnel_alert(tunnel_url, tunnel_url, tunnel_url)

    process.wait()
    return True

def main():
    while True:
        try:
            run_single_tunnel()
        except KeyboardInterrupt:
            print("\nStopping tunnel service.")
            break
        except Exception as e:
            print(f"Tunnel runner exception: {e}")
            time.sleep(3)

if __name__ == "__main__":
    main()
