# -*- coding: utf-8 -*-
"""
Automated News Fetcher and Content Aggregator for Telugu Exam Current Affairs.
Fetches daily news from ALL major Telugu Newspapers and Media:
1. ఈనాడు (Eenadu)
2. సాక్షి (Sakshi)
3. నమస్తే తెలంగాణ (Namasthe Telangana - NT News)
4. BBC న్యూస్ తెలుగు (BBC News Telugu)
5. ఏషియానెట్ తెలుగు (Asianet News Telugu - AP & TS)
6. ఏబీపీ దేశం (ABP Desam Telugu)
7. టీవీ9 తెలుగు (TV9 Telugu)
8. వన్ ఇండియా తెలుగు (OneIndia Telugu)
"""

import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
import re
from datetime import datetime
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from db import get_connection, insert_article, insert_quiz, insert_one_liner

# Categorization rules for exam topics
KEYWORD_CATEGORIES = {
    "regional": [
        "తెలంగాణ", "ఆంధ్రప్రదేశ్", "అమరావతి", "హైదరాబాద్", "పోలవరం", "రైతు భరోసా", 
        "ఆర్టీసీ", "వైజాగ్", "విశాఖ", "చంద్రబాబు", "రేవంత్", "డిజిటల్ కార్డు", 
        "మూసీ", "ఇందిరమ్మ", "పథకం", "వరద", "కృష్ణా", "గోదావరి", "telangana", "andhra"
    ],
    "economy": [
        "రిజర్వ్ బ్యాంక్", "ఆర్బీఐ", "ద్రవ్యోల్బణం", "జీడీపీ", "బ్యాంక్", "బడ్జెట్", 
        "ఆర్థిక", "రూపాయి", "సెన్సెక్స్", "నిఫ్టీ", "జీఎస్టీ", "rbi", "gdp", "economy"
    ],
    "science_tech": [
        "ఇస్రో", "నాసా", "ఉపగ్రహం", "మిషన్", "రోదసి", "ఏఐ", "కృత్రిమ మేధ", 
        "రాకెట్", "చంద్రయాన్", "గగన్‌యాన్", "సైన్స్", "టెక్నాలజీ", "isro", "ai"
    ],
    "sports_awards": [
        "క్రికెట్", "ఒలింపిక్స్", "పారాలింపిక్స్", "స్వర్ణం", "పతకం", "ట్రోఫీ", 
        "అవార్డు", "రత్న", "విజేత", "వరల్డ్ కప్", "sports", "medal", "award"
    ],
    "appointments": [
        "నియామకం", "చైర్మన్", "గవర్నర్", "జడ్జి", "కమిషనర్", "మంత్రి", "సీజేఐ", 
        "డీజీపీ", "director", "chairman", "governor", "chief"
    ]
}

# Major Telugu Newspapers & Feeds
TELUGU_SOURCES = [
    {
        "name": "ఈనాడు (Eenadu)",
        "type": "html_scraper",
        "url": "https://www.eenadu.net"
    },
    {
        "name": "సాక్షి (Sakshi)",
        "type": "rss",
        "url": "https://www.sakshi.com/rss.xml"
    },
    {
        "name": "నమస్తే తెలంగాణ (Namasthe Telangana)",
        "type": "rss",
        "url": "https://ntnews.com/feed"
    },
    {
        "name": "BBC న్యూస్ తెలుగు (BBC Telugu)",
        "type": "rss",
        "url": "https://feeds.bbci.co.uk/telugu/rss.xml"
    },
    {
        "name": "ఏషియానెట్ ఆంధ్రప్రదేశ్ (Asianet AP)",
        "type": "rss",
        "url": "https://telugu.asianetnews.com/rss/andhra-pradesh"
    },
    {
        "name": "ఏషియానెట్ తెలంగాణ (Asianet TS)",
        "type": "rss",
        "url": "https://telugu.asianetnews.com/rss/telangana"
    },
    {
        "name": "ఏబీపీ దేశం (ABP Desam)",
        "type": "rss",
        "url": "https://telugu.abplive.com/home/feed"
    },
    {
        "name": "వన్ ఇండియా తెలుగు (OneIndia Telugu)",
        "type": "rss",
        "url": "https://telugu.oneindia.com/rss/telugu-news-fb.xml"
    },
    {
        "name": "టీవీ9 తెలుగు (TV9 Telugu)",
        "type": "rss",
        "url": "https://tv9telugu.com/feed"
    }
]

BANNED_EXAM_KEYWORDS = [
    "సినిమా", "షూటింగ్", "సూర్య", "జ్యోతిక", "సంపూర్ణేష్", "బిర్యానీ", "భార్య", "భర్త", 
    "షాక్", "దొంగతనం", "ముక్కు", "చైత్ర", "హత్య", "SPY CAM", "లండన్", "వైకాపా", 
    "వైసీపీ", "ఎమ్మెల్సీ", "గాజువాక", "క్షమాపణ", "బతికుండగానే", "నిమజ్జనం", "కోటీశ్వరుడు",
    "పులస", "రొయ్య", "హెలికాప్టర్ క్రాష్", "శ్రీకాకుళం జిల్లాలో వైకాపా", "ప్రేమ", "వివాహం",
    "పెళ్లి", "ట్రైలర్", "గాసిప్", "రివ్యూ", "ఆత్మహత్య", "చోరీ", "అరెస్ట్", "బంగారం ధర", "పసిడి ధర"
]

def is_exam_worthy_content(text):
    text_lower = text.lower()
    for b in BANNED_EXAM_KEYWORDS:
        if b.lower() in text_lower:
            return False
    return True

def detect_category(text):
    text_lower = text.lower()
    for cat, keywords in KEYWORD_CATEGORIES.items():
        for kw in keywords:
            if kw in text_lower:
                return cat
    return "national"

def fetch_rss_feed(feed_url, source_name):
    """Fetch and parse standard RSS feed XML"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(feed_url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            items = []
            for item in root.findall(".//item"):
                title_elem = item.find("title")
                title = title_elem.text if (title_elem is not None and title_elem.text) else ""
                link_elem = item.find("link")
                link = link_elem.text if (link_elem is not None and link_elem.text) else ""
                desc_elem = item.find("description")
                desc = desc_elem.text if (desc_elem is not None and desc_elem.text) else ""
                desc_clean = re.sub(r'<[^>]+>', '', desc).strip() if desc else ""
                if title and len(title.strip()) > 8:
                    items.append({
                        "title": title.strip(),
                        "link": link.strip(),
                        "summary": desc_clean[:300] if desc_clean else title.strip(),
                        "source": source_name
                    })
            return items
    except Exception as e:
        print(f"Error fetching {source_name} ({feed_url}): {e}")
        return []

def scrape_eenadu_news():
    """Scrape top headlines directly from Eenadu website"""
    url = "https://www.eenadu.net"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    items = []
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            # Extract headlines in h2/h3 tags with Telugu characters
            raw_headings = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', html, re.DOTALL)
            for rh in raw_headings:
                clean = re.sub(r'<[^>]+>', '', rh).strip()
                # Ensure it has Telugu characters and meaningful length
                if len(clean) > 12 and re.search(r'[\u0C00-\u0C7F]', clean):
                    items.append({
                        "title": clean,
                        "link": "https://www.eenadu.net",
                        "summary": f"{clean}. సమగ్ర వివరాల కోసం ఈనాడు దినపత్రిక ప్రధాన సంచికను పరిశీలించండి.",
                        "source": "ఈనాడు దినపత్రిక (Eenadu)"
                    })
    except Exception as e:
        print(f"Error scraping Eenadu: {e}")
    return items

def sync_daily_news(target_date=None):
    """
    Sync news for the target date from ALL major Telugu newspapers.
    """
    if not target_date:
        target_date = datetime.now().strftime("%Y-%m-%d")

    conn = get_connection()
    cursor = conn.cursor()

    existing_titles = set()
    cursor.execute("SELECT title FROM articles WHERE date = ?", (target_date,))
    for row in cursor.fetchall():
        existing_titles.add(row["title"].strip())

    added_articles = 0
    all_fetched_news = []

    # 1. Fetch from Eenadu
    print("📰 [ఈనాడు] వార్తలను సేకరిస్తోంది...")
    eenadu_items = scrape_eenadu_news()
    all_fetched_news.extend(eenadu_items[:5])

    # 2. Fetch from RSS Feeds (Sakshi, Namasthe Telangana, BBC, Asianet, ABP, TV9, OneIndia)
    for src in TELUGU_SOURCES:
        if src["type"] == "rss":
            print(f"📰 [{src['name']}] ఫీడ్ నుంచి వార్తలు సేకరిస్తోంది...")
            items = fetch_rss_feed(src["url"], src["name"])
            all_fetched_news.extend(items[:3]) # Take top 3 from each newspaper to keep high quality

    # 3. Filter, Deduplicate, Categorize and Insert
    for item in all_fetched_news:
        title = item["title"]
        if title in existing_titles or len(title) < 10:
            continue

        if not is_exam_worthy_content(title + " " + item["summary"]):
            continue

        cat = detect_category(title + " " + item["summary"])
        exam_rel = "APPSC / TSPSC Group 1, 2, 3, SI & కానిస్టేబుల్ (జనరల్ స్టడీస్)"
        if cat == "regional":
            exam_rel = "ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రాంతీయ అంశాలు, ప్రభుత్వ పాలసీలు"
        elif cat == "economy":
            exam_rel = "భారత ఆర్థిక వ్యవస్థ & బ్యాంకింగ్ అవగాహన"
        elif cat == "science_tech":
            exam_rel = "UPSC / APPSC / TSPSC (సైన్స్ & టెక్నాలజీ)"

        detailed = (
            f"• ప్రధానాంశం: {item['summary']}\n"
            f"• పోటీ పరీక్షల ప్రాధాన్యత: ఈ అంశం సమకాలీన పరిణామాలు మరియు జనరల్ స్టడీస్ విభాగంలో చాలా కీలకం.\n"
            f"• వార్తా మూలం: {item['source']}\n"
            f"• లింక్: {item['link']}"
        )

        insert_article(
            date=target_date,
            category=cat,
            title=title,
            summary=item["summary"],
            detailed_notes=detailed,
            exam_relevance=exam_rel,
            tags="తెలుగు దినపత్రికలు, డైలీ CA",
            source=item["source"]
        )

        # Insert quick revision one-liner
        insert_one_liner(
            target_date, 
            cat, 
            f"[{item['source'].split()[0]}] {title}"
        )

        existing_titles.add(title)
        added_articles += 1

    # Log sync status
    cursor.execute("""
        INSERT INTO sync_logs (synced_at, date, articles_count, status)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(), target_date, added_articles, "SUCCESS"))

    conn.commit()
    conn.close()

    return {
        "date": target_date,
        "articles_added": added_articles,
        "sources_count": len(TELUGU_SOURCES),
        "status": "success"
    }

if __name__ == "__main__":
    import sys
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    res = sync_daily_news()
    print("తెలుగు దినపత్రికల సింక్ పూర్తయింది:", res)
