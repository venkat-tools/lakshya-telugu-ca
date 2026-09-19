# -*- coding: utf-8 -*-
"""
Automated News Fetcher & Content Aggregator for Telugu Competitive Exam Current Affairs.
Strictly restricted to:
- Education, Notifications, Syllabus & Jobs
- Government Welfare Schemes & Policies (AP & TS)
- Indian Economy, Banking, RBI & EPFO
- Science & Technology, ISRO Space Missions & Defence
- Indian Polity, Constitution & Supreme Court Verdicts
- Environment, Projects & Water Resources
- National & International Summits (BRICS, G20)
- Sports Championships & National Awards
"""

import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
import re
from datetime import datetime, timedelta
import json

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from db import get_connection, insert_article, insert_quiz, insert_one_liner
from political_filter import is_political_content

# ----------------- Strict Negative Filters (Banned Junk) -----------------
BANNED_EXAM_PATTERNS = [
    # Recipes & Cooking
    r"(వంటకాలు|రెసిపీ|ప్రసాదం|టొమాటో|ఉల్లి|వెల్లుల్లి|బిర్యానీ|రుచి|టిఫిన్|కిలో బియ్యం|వంటల చిట్కాలు|వంటకం)",
    # Local Crimes, Murders, Violence
    r"(నూనె పోసి|సిమెంట్‌ దిమ్మ|హత్య|చంపిన|దాడి|దొంగతనం|చోరీ|అత్యాచారం|గ్యాంగ్‌రేప్‌|కిడ్నాప్|ఉరి|ఆత్మహత్య|పోలీసులు అరెస్ట్|రిమాండ్|బెయిల్|రౌడీషీటర్|గాయపరిచిన|కత్తితో|రక్తపు మడుగు|మృతదేహం|హెలికాప్టర్ క్రాష్|మృత్యువాత|ఖైదీ)",
    # Road Accidents & Deaths
    r"(రోడ్డు ప్రమాదం|లారీని ఢీకొన్న|వాహనం ఢీ|ఆగి ఉన్న లారీ|మృతి|మరణించారు|ప్రాణాలు కోల్పోయారు|బోల్తా పడిన|విద్యుదాఘాతం|మునిగిపోయి)",
    # Cinema, OTT, Reviews & Celebrity Gossip
    r"(సినిమా|మూవీ|షూటింగ్|ట్రైలర్|టీజర్|రివ్యూ|ఓటీటీ|బాక్సాఫీస్|నటుడు|నటి|హీరో|హీరోయిన్|గాసిప్|కలెక్షన్లు|దర్శకుడు|పాటలు|డైరెక్టర్|సూర్య|జ్యోతిక|సంపూర్ణేష్|ఫస్ట్ మూవీ|తుడక్కమ్‌|ధోని జవాబివ్వాలి)",
    # Nav menus, Lifestyle, Astrology & Viral
    r"(మ్యాగజైన్|గ్యాలరీ|వెబ్‌ స్టోరీస్|ఎక్కువ మంది చదివినవి|గ్రహం - అనుగ్రహం|జైజై గణేశా|మహాగణపతిం|సోకులో|స్లీవ్స్‌|భగవద్గీత|అయ్యో బిడ్డా|కంటినిండా నిద్ర|అందాల కిరీటం|బళ్లారి జీన్స్|ఫోను విసిరేయడంతో|గుర్రంపై పోలీసు|స్నేహితురాలి కోసం|వేటా నాదే|చిన్ననాటి టీచరు|రాశిఫలాలు|జ్యోతిష్యం|వైరల్ వీడియో|రీల్స్|బాలుడు శ్రీలంక|గంజాయి)",
    # Political Mudslinging & Bickering
    r"(అడ్డంగా దొరికిపోయిన|మోసం చేశారు|ఫిర్యాదు చేశారు|వాటర్‌మ్యాన్‌ బిరుదుకు|దుమ్మెత్తిపోసిన|తిట్లు|సంచలన వ్యాఖ్యలు|సవాల్ విసిరిన|ఆరోపణలు|విమర్శలు గుప్పించిన|ఆపరేషన్ రీ-ఎంట్రీ|దగ్గుపాటిపై టీడీపీ|వైకాపా|వైసీపీ|మీనాక్షి పై కోర్టులో|పాస్‌పోర్టును జప్తు|ఆస్తుల లెక్కలు తేల్చుదామా|ధైర్యముంటే)"
]

# ----------------- Strict Positive Exam Relevance Domains -----------------
KEYWORD_CATEGORIES = {
    "education": [
        "నోటిఫికేషన్", "పరీక్షల క్యాలెండర్", "సిలబస్", "ఉద్యోగ భర్తీ", "ఫలితాలు", "కటాఫ్", "రోస్టర్", 
        "హాల్ టికెట్లు", "appsc", "tspsc", "tgpsc", "upsc", "ssc", "rrb", "dsc", "డీఎస్సీ", "టెట్", "tet", 
        "ibps", "యూనివర్సిటీ", "విద్యా విధానం", "ఎస్సై", "కానిస్టేబుల్", "గ్రూప్-1", "గ్రూప్-2", "గ్రూప్-3",
        "nta", "ugc", "net", "నీట్", "జేఈఈ", "పోస్టుల భర్తీ", "ప్రవేశాలు", "అడ్మిషన్లు", "ఉద్యోగాలు"
    ],
    "regional": [
        "పథకం", "సబ్సిడీ", "క్యాబినెట్ ఆమోదం", "జీవో", "రైతు భరోసా", "అన్నదాత సుఖీభవ", "దీపం-2", 
        "తల్లికి వందనం", "మహాలక్ష్మి", "చేయూత", "ఇందిరమ్మ", "కుల సర్వే", "కుల గణన", 
        "పారిశ్రామిక విధానం", "పోలవరం", "అమరావతి", "ఆంధ్రప్రదేశ్ ప్రభుత్వం", "తెలంగాణ ప్రభుత్వం", 
        "ఏపీ ప్రభుత్వం", "బడ్జెట్ కేటాయింపు", "పెట్టుబడులు", "శాసనసభ", "ఉపాధి అవకాశాలు", "ఒప్పందం"
    ],
    "economy": [
        "ఈపీఎఫ్ఓ", "epfo", "వేతన పరిమితి", "రిజర్వ్ బ్యాంక్", "ఆర్బీఐ", "rbi", "ద్రవ్యోల్బణం", 
        "జీడీపీ", "gdp", "రెపో రేటు", "బడ్జెట్", "సెబీ", "నీతి ఆయోగ్", "ఆర్థిక సర్వే", 
        "యూపీఐ", "upi 123pay", "జీఎస్టీ వసూళ్లు", "ద్రవ్య విధానం", "సామాజిక భద్రతా కోడ్", "వడ్డీ రేట్లు",
        "బ్యాంకింగ్", "ఎకానమీ", "రుణాలు", "డిపాజిట్లు"
    ],
    "science_tech": [
        "ఇస్రో", "isro", "నాసా", "nasa", "చంద్రయాన్", "శుక్రయాన్", "గగన్‌యాన్", "ఉపగ్రహం", 
        "రాకెట్", "క్షిపణి", "డీఆర్‌డీవో", "drdo", "కృత్రిమ మేధ", "ఏఐ నమూనా", "సూపర్ కంప్యూటర్", 
        "రక్షణ రంగం", "సైన్స్ & టెక్నాలజీ", "శాస్త్రవేత్తలు", "అంతరిక్షం", "క్వాంటం", "స్పేస్"
    ],
    "national": [
        "రాజ్యాంగం", "సుప్రీంకోర్టు", "హైకోర్టు", "తీర్పు", "అధికరణ", "ఆర్టికల్", "సవరణ", 
        "చట్టం", "బిల్లు", "కమిషన్", "జమిలి ఎన్నికలు", "కొవింద్ కమిటీ", "ఎన్నికల సంస్కరణలు", 
        "పార్లమెంట్", "కేంద్ర మంత్రివర్గం", "బ్రిక్స్", "brics", "జీ20", "g20", "ఐక్యరాజ్యసమితి",
        "కేంద్ర ప్రభుత్వం", "రాష్ట్రపతి", "ఉపరాష్ట్రపతి", "ప్రధానమంత్రి"
    ],
    "environment": [
        "పోలవరం ప్రాజెక్ట్", "డయాఫ్రమ్ వాల్", "జాతీయ పార్కు", "టైగర్ రిజర్వ్", "రామ్‌సర్ సైట్", 
        "పర్యావరణం", "జీవవైవిధ్యం", "సాగునీటి ప్రాజెక్టు", "నదుల అనుసంధానం", "వాతావరణ సదస్సు",
        "భారీ వర్షాలు", "అల్పపీడనం", "తుఫాను", "వరదలు", "కాలుష్యం"
    ],
    "sports_awards": [
        "భారతరత్న", "పద్మవిభూషణ్", "పద్మభూషణ్", "పద్మశ్రీ", "నోబెల్", "జ్ఞానపీఠ్", 
        "ఒలింపిక్స్", "పారాలింపిక్స్", "చెస్ ఒలింపియాడ్", "గ్రాండ్‌మాస్టర్", "స్వర్ణ పతకం", "ప్రపంచ కప్",
        "ఆసియా క్రీడలు", "ఆసియా గేమ్స్", "ఛాంపియన్‌షిప్", "పతకం", "స్వర్ణం", "రజతం", "కాంస్యం", "అవార్డు"
    ],
    "appointments": [
        "నియామకం", "చైర్మన్", "గవర్నర్", "కమిషనర్", "సీజేఐ", "ముఖ్య న్యాయమూర్తి", "డైరెక్టర్ జనరల్"
    ]
}

def is_exam_worthy_content(text):
    """Strictly evaluates if content is genuine competitive exam material and rejects all political news"""
    if not text or len(text.strip()) < 12:
        return False
    
    # 1. Reject political party news, bickering, and election gossip
    if is_political_content(text):
        return False

    text_lower = text.lower()

    # 2. Reject banned junk (crime, cinema, accidents, recipes, viral)
    for pattern in BANNED_EXAM_PATTERNS:
        if re.search(pattern, text_lower):
            return False

    # 3. Positive match required
    for cat, keywords in KEYWORD_CATEGORIES.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                return True
    return False

def clean_tokens(title):
    cleaned = re.sub(r"[^\w\s\u0C00-\u0C7F]", " ", title.lower())
    words = [w.strip() for w in cleaned.split() if len(w.strip()) > 2]
    stopwords = {"మరియు", "కూడా", "నుంచి", "కోసం", "యొక్క", "ద్వారా", "గారి", "లోని", "చేసిన", "ఉన్న", "అని", "ఇలా"}
    return set(w for w in words if w not in stopwords)

def is_duplicate_article(new_title, existing_titles):
    new_words = clean_tokens(new_title)
    if not new_words:
        return False
    for ext in existing_titles:
        ext_words = clean_tokens(ext)
        if not ext_words:
            continue
        if ext.lower() in new_title.lower() or new_title.lower() in ext.lower():
            return True
        intersection = new_words.intersection(ext_words)
        union = new_words.union(ext_words)
        if union and (len(intersection) / len(union)) >= 0.35:
            return True
    return False

def detect_category(text):
    text_lower = text.lower()
    for cat in ["education", "regional", "economy", "science_tech", "national", "environment", "sports_awards", "appointments"]:
        for kw in KEYWORD_CATEGORIES.get(cat, []):
            if kw.lower() in text_lower:
                return cat
    return "national"

def fetch_google_news_telugu(topic_query, days=2):
    """Fetch live Telugu exam news from Google News Telugu RSS"""
    import urllib.parse
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    query = urllib.parse.quote(f"({topic_query}) when:{days}d")
    url = f"https://news.google.com/rss/search?q={query}&hl=te&gl=IN&ceid=IN:te"
    req = urllib.request.Request(url, headers=headers)
    items = []
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            root = ET.fromstring(resp.read())
            for it in root.findall(".//item"):
                title_elem = it.find("title")
                link_elem = it.find("link")
                desc_elem = it.find("description")
                source_elem = it.find("source")
                
                raw_title = title_elem.text.strip() if (title_elem is not None and title_elem.text) else ""
                link = link_elem.text.strip() if (link_elem is not None and link_elem.text) else ""
                
                # Separate title and publisher (Google News appends ' - SourceName')
                src_name = "తెలుగు దినపత్రికలు"
                if " - " in raw_title:
                    parts = raw_title.rsplit(" - ", 1)
                    title = parts[0].strip()
                    src_name = parts[1].strip()
                else:
                    title = raw_title
                    if source_elem is not None and source_elem.text:
                        src_name = source_elem.text.strip()

                desc = desc_elem.text if (desc_elem is not None and desc_elem.text) else ""
                clean_desc = re.sub(r'<[^>]+>', '', desc).strip()
                
                if len(title) > 12:
                    items.append({
                        "title": title,
                        "link": link,
                        "summary": clean_desc[:280] if len(clean_desc) > 30 else f"{title}. పోటీ పరీక్షల అభ్యర్థుల కోసం సమగ్ర వార్తా విశ్లేషణ.",
                        "source": src_name
                    })
    except Exception as e:
        print(f"Error fetching Google News for query '{topic_query[:25]}': {e}")
    return items

def fetch_rss_feed(feed_url, source_name):
    """Fetch standard RSS feed XML"""
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(feed_url, headers=headers)
    items = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            root = ET.fromstring(resp.read())
            for it in root.findall(".//item"):
                t = it.find("title")
                l = it.find("link")
                d = it.find("description")
                title = t.text.strip() if (t is not None and t.text) else ""
                link = l.text.strip() if (l is not None and l.text) else ""
                desc = d.text if (d is not None and d.text) else ""
                clean_desc = re.sub(r'<[^>]+>', '', desc).strip()
                if len(title) > 12:
                    items.append({
                        "title": title,
                        "link": link,
                        "summary": clean_desc[:280] if len(clean_desc) > 30 else f"{title}. పోటీ పరీక్షల ప్రత్యేకం.",
                        "source": source_name
                    })
    except Exception as e:
        pass
    return items

def scrape_eenadu_news():
    """Scrape headlines directly from Eenadu website"""
    url = "https://www.eenadu.net"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    items = []
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            raw_headings = re.findall(r'<h[234][^>]*>(.*?)</h[234]>', html, re.DOTALL)
            for rh in raw_headings:
                clean = re.sub(r'<[^>]+>', '', rh).strip()
                if len(clean) > 15 and re.search(r'[\u0C00-\u0C7F]', clean):
                    items.append({
                        "title": clean,
                        "link": "https://www.eenadu.net",
                        "summary": f"{clean}. సమగ్ర విశ్లేషణ కోసం ఈనాడు ప్రధాన ఎడిషన్ పరిశీలించండి.",
                        "source": "ఈనాడు (Eenadu)"
                    })
    except Exception:
        pass
    return items

def build_exam_detailed_notes(title, summary, category, source, link):
    """Build structured, exam-oriented study notes with key facts and syllabus mapping"""
    syllabus_map = {
        "education": "పోటీ పరీక్షల నోటిఫికేషన్లు, సిలబస్ & రిక్రూట్‌మెంట్ సమాచారం (APPSC / TSPSC / UPSC)",
        "regional": "ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రభుత్వ పథకాలు, పాలసీలు & బడ్జెట్ కేటాయింపులు",
        "economy": "భారత ఆర్థిక వ్యవస్థ, ఆర్బీఐ మానిటరీ పాలసీ, బ్యాంకింగ్ & ద్రవ్యోల్బణం",
        "science_tech": "సైన్స్ & టెక్నాలజీ, ఇస్రో అంతరిక్ష ప్రయోగాలు & రక్షణ రంగం (Defence)",
        "national": "భారత రాజ్యాంగం, సుప్రీంకోర్టు తీర్పులు, పాలిటీ & గవర్నెన్స్",
        "environment": "పర్యావరణం, జీవవైవిధ్యం, వాతావరణ మార్పులు & సాగునీటి ప్రాజెక్టులు",
        "sports_awards": "జాతీయ, అంతర్జాతీయ క్రీడాంశాలు, రికార్డులు & అవార్డులు",
        "appointments": "ముఖ్య నియామకాలు, కమిషన్లు & రాజ్యాంగబద్ధ పదవులు"
    }
    relevance = syllabus_map.get(category, "పోటీ పరీక్షల జనరల్ స్టడీస్ ప్రత్యేకం")
    
    notes = (
        f"• ప్రధానాంశం: {summary}\n"
        f"• పరీక్షా ప్రాముఖ్యత: {relevance}.\n"
        f"• కీలక అంశాలు: పోటీ పరీక్షల ప్రిలిమ్స్ మరియు మెయిన్స్ జనరల్ స్టడీస్ (GS) కోణంలో ఈ సమకాలీన పరిణామం అత్యంత ప్రాధాన్యత కలిగినది.\n"
        f"• వార్తా మూలం: {source}\n"
        f"• మూల కథనం లింక్: {link}"
    )
    return notes, relevance

# Date-indexed diverse fallback pool to guarantee unique news if live network is completely down
ROTATING_EXAM_ARCHIVE = [
    {
        "category": "education",
        "title": "NTA వార్షిక పరీక్షల క్యాలెండర్ & పబ్లిక్ సర్వీస్ కమిషన్ల నూతన మూల్యాంకన విధానం",
        "summary": "జాతీయ పరీక్షల సంస్థ (NTA) మరియు రాష్ట్ర పబ్లిక్ సర్వీస్ కమిషన్లు 2026-27 విద్యా సంవత్సరానికి కీలక పరీక్షల ప్రవేశ పరీక్షల షెడ్యూల్‌ను, నూతన డిజిటల్ పారదర్శక నిబంధనలను ఖరారు చేశాయి.",
        "detailed_notes": "• ప్రధానాంశం: జాతీయ మరియు రాష్ట్ర స్థాయి పోటీ పరీక్షల నూతన క్యాలెండర్.\n• పారదర్శకత: బయోమెట్రిక్ వెరిఫికేషన్ మరియు డిజిటల్ ఎవల్యూషన్ నిబంధనలు.\n• పరీక్ష ప్రాముఖ్యత: APPSC/TSPSC/UPSC పోటీ పరీక్షల అభ్యర్థులకు మార్గదర్శకం.\n• లింక్: https://nta.ac.in",
        "exam_relevance": "పోటీ పరీక్షల నోటిఫికేషన్లు & అధికారిక విద్యా సమాచారం",
        "source": "జాతీయ పరీక్షల సంస్థ (NTA)"
    },
    {
        "category": "regional",
        "title": "తెలంగాణ సమగ్ర కుటుంబ సర్వే & విద్యా, సామాజిక-ఆర్థిక మార్గదర్శకాల ఆమోదం",
        "summary": "తెలంగాణలోని అన్ని కుటుంబాల సామాజిక, ఆర్థిక స్థితిగతులను లెక్కించేందుకు ప్రణాళికా శాఖ ఇంటింటి సర్వే మార్గదర్శకాలను ఖరారు చేసింది. సంక్షేమ పథకాల శాస్త్రీయ పంపిణీకి ఇది ఆధారంగా నిలుస్తుంది.",
        "detailed_notes": "• సర్వే లక్ష్యం: సమాజంలో అణగారిన వర్గాల సామాజిక, విద్య, ఆర్థిక స్థితిగతుల లెక్కంపు.\n• నోడల్ విభాగం: తెలంగాణ ప్రణాళికా శాఖ (Planning Department).\n• పరీక్ష ప్రాముఖ్యత: టీఎస్‌పీఎస్సీ గ్రూప్స్ (తెలంగాణ సమాజం & సంక్షేమ పాలసీలు).\n• లింక్: https://telangana.gov.in",
        "exam_relevance": "టీఎస్‌పీఎస్సీ గ్రూప్-1, 2, 3 తెలంగాణ సమాజం & సంక్షేమం",
        "source": "తెలంగాణ ప్రణాళికా మండలి"
    },
    {
        "category": "regional",
        "title": "ఆంధ్రప్రదేశ్ దీపం-2 పథకం: అర్హులకు ఏడాదికి 3 ఉచిత గ్యాస్ సిలిండర్ల నిబంధనలు",
        "summary": "ఏపీ ప్రభుత్వం ఎన్నికల సూపర్ సిక్స్ హామీల్లో భాగంగా అర్హులైన ప్రతి పేద మహిళకు ఏడాదికి 3 ఉచిత ఎల్పీజీ సిలిండర్లను అందించే దీపం-2 పథకం అమలుకు నిధులను కేటాయించింది.",
        "detailed_notes": "• పథకం: దీపం-2 ఉచిత ఎల్పీజీ సిలిండర్ల పథకం.\n• లబ్ధిదారులు: తెల్ల రేషన్ కార్డు కలిగి ఉన్న అర్హులైన మహిళలు.\n• బడ్జెట్ వ్యయం: ఏటా సుమారు ₹2,684 కోట్ల కేటాయింపు.\n• పరీక్ష ప్రాముఖ్యత: APPSC గ్రూప్-2 (ఆంధ్రప్రదేశ్ సంక్షేమ పథకాలు).\n• లింక్: https://ap.gov.in",
        "exam_relevance": "APPSC గ్రూప్-2 పేపర్-2 (ఏపీ ప్రభుత్వ సంక్షేమ పథకాలు)",
        "source": "ఆంధ్రప్రదేశ్ పౌర సరఫరాల శాఖ"
    },
    {
        "category": "economy",
        "title": "రిజర్వ్ బ్యాంక్ ఆఫ్ ఇండియా (RBI) ద్రవ్య విధాన సమీక్ష: రెపో రేటు & ద్రవ్యోల్బణ అంచనాలు",
        "summary": "భారతీయ రిజర్వ్ బ్యాంక్ తాజా ద్రవ్య విధాన కమిటీ (MPC) సమావేశంలో ద్రవ్యోల్బణ నియంత్రణ మరియు ఆర్థిక వృద్ధికి మద్దతుగా వడ్డీ రేట్లను సమతుల్యం చేస్తూ కీలక విధాన నిర్ణయాలను వెల్లడించింది.",
        "detailed_notes": "• పాలసీ రేటు: రెపో రేటు (Repo Rate) మరియు రివర్స్ రెపో మార్గదర్శకాలు.\n• ద్రవ్య విధాన కమిటీ (MPC): ఆర్బీఐ గవర్నర్ నేతృత్వంలోని 6 మంది సభ్యుల కమిటీ నిర్ణయం.\n• లక్ష్యం: వినియోగదారుల ధరల సూచీ (CPI) ఆధారిత ద్రవ్యోల్బణాన్ని 4% పరిధిలో ఉంచడం.\n• పరీక్ష ప్రాముఖ్యత: UPSC GS-3, APPSC/TSPSC ఎకానమీ & బ్యాంకింగ్ పరీక్షలు.\n• లింక్: https://www.rbi.org.in",
        "exam_relevance": "భారత ఆర్థిక వ్యవస్థ & బ్యాంకింగ్ (RBI Monetary Policy)",
        "source": "భారతీయ రిజర్వ్ బ్యాంక్ (RBI Bulletin)"
    },
    {
        "category": "science_tech",
        "title": "ఇస్రో చంద్రయాన్-4 శాంపిల్ రిటర్న్ & శుక్రయాన్ ఆర్బిటర్ ప్రాజెక్టుల విస్తరణ",
        "summary": "చంద్రుని ఉపరితలం నుండి మట్టి నమూనాలను భూమికి చేర్చే చంద్రయాన్-4 ప్రాజెక్టు మరియు శుక్ర గ్రహ వాతావరణాన్ని శోధించే శుక్రయాన్ మిషన్లకు కేంద్ర మంత్రివర్గం నిధులను ఆమోదించింది.",
        "detailed_notes": "• చంద్రయాన్-4: లూనార్ శాంపిల్ రిటర్న్ మిషన్ (5 మాడ్యూల్స్ ఆర్కిటెక్చర్).\n• శుక్రయాన్: వీనస్ ఆర్బిటర్ ద్వారా శుక్రుడి ఉపరితల, వాతావరణ అన్వేషణ.\n• స్పేస్ స్టేషన్ లక్ష్యం: 2028 నాటికి భారతీయ అంతరిక్ష స్టేషన్ (BAS) తొలి మాడ్యూల్.\n• పరీక్ష ప్రాముఖ్యత: UPSC / APPSC / TSPSC సైన్స్ & టెక్నాలజీ విభాగం.\n• లింక్: https://www.isro.gov.in",
        "exam_relevance": "UPSC / APPSC / TSPSC సైన్స్, స్పేస్ & టెక్నాలజీ",
        "source": "ఇస్రో (ISRO) & అంతరిక్ష విభాగం"
    },
    {
        "category": "national",
        "title": "సుప్రీంకోర్టు రాజ్యాంగ ధర్మాసనం తీర్పు: ఎస్సీ ఉప-వర్గీకరణపై రాష్ట్రాల అధికారాలు",
        "summary": "షెడ్యూల్డ్ కులాల (SC) వర్గీకరణలో అత్యంత వెనుకబడిన వర్గాలకు ప్రత్యేక కోటా కల్పించే అధికారం రాష్ట్ర ప్రభుత్వాలకు ఉందని భారత ప్రధాన న్యాయమూర్తి నేతృత్వంలోని 7 జడ్జిల రాజ్యాంగ ధర్మాసనం తీర్పునిచ్చింది.",
        "detailed_notes": "• బెంచ్ కూర్పు: CJI నేతృత్వంలోని 7 గురు న్యాయమూర్తుల రాజ్యాంగ ధర్మాసనం (6:1 తీర్పు).\n• రద్దయిన తీర్పు: 2004 నాటి ఈవీ చిన్నయ్య తీర్పును తోసిపుచ్చిన సుప్రీంకోర్టు.\n• రాజ్యాంగ ఆర్టికల్స్: ఆర్టికల్ 16(4), 14, 15 మరియు ఆర్టికల్ 341 పరిధి.\n• పరీక్ష ప్రాముఖ్యత: UPSC & రాష్ట్ర పబ్లిక్ సర్వీస్ కమిషన్ల భారత రాజ్యాంగం & పాలిటీ.\n• లింక్: https://sci.gov.in",
        "exam_relevance": "UPSC / APPSC / TSPSC భారత రాజ్యాంగం & సుప్రీంకోర్టు తీర్పులు",
        "source": "సుప్రీంకోర్టు అధికారిక రికార్డులు"
    },
    {
        "category": "sports_awards",
        "title": "అంతర్జాతీయ చెస్ సమాఖ్య (FIDE) ప్రపంచ ర్యాంకింగ్స్ & ఒలింపియాడ్‌లో భారత ప్రాతినిధ్యం",
        "summary": "ప్రపంచ చెస్ రంగంలో డి.గుకేశ్, అర్జున్ ఎరిగైసి, ఆర్.ప్రజ్ఞానంద అగ్రశ్రేణి రేటింగ్‌లతో భారత కీర్తిని విశ్వవ్యాప్తం చేస్తున్నారు. మహిళల విభాగంలో ఆర్.వైశాలి, దివ్య దేశ్‌ముఖ్ కీలక విజయాలు సాధించారు.",
        "detailed_notes": "• గ్రాండ్‌మాస్టర్లు: ప్రపంచ ఛాంపియన్‌షిప్ పోటీదారు డి.గుకేశ్, 2800+ ఎలో రేటింగ్‌తో అర్జున్ ఎరిగైసి.\n• ఈవెంట్స్: ఫిడే వరల్డ్ చెస్ ఛాంపియన్‌షిప్ మరియు చెస్ ఒలింపియాడ్ వేదికలు.\n• పరీక్ష ప్రాముఖ్యత: అంతర్జాతీయ క్రీడా వేదికలు, ప్రపంచ రికార్డులు & భారత క్రీడాకారులు.\n• లింక్: https://www.fide.com",
        "exam_relevance": "పోటీ పరీక్షల క్రీడా ముఖ్యాంశాలు & అంతర్జాతీయ అవార్డులు",
        "source": "అంతర్జాతీయ చెస్ సమాఖ్య (FIDE Official)"
    },
    {
        "category": "environment",
        "title": "పోలవరం జాతీయ సాగునీటి ప్రాజెక్ట్: నూతన డయాఫ్రమ్ వాల్ నిర్మాణ నిధుల సమీకరణ",
        "summary": "గోదావరి నదిపై ప్రతిష్టాత్మకంగా నిర్మిస్తున్న పోలవరం ప్రాజెక్టు డయాఫ్రమ్ వాల్ నూతన డిజైన్ పనులకు మరియు మొదటి దశ 41.15 మీటర్ల నీటిమట్టం నిర్మాణానికి కేంద్ర జలశక్తి శాఖ పర్యవేక్షణ వేగవంతం చేసింది.",
        "detailed_notes": "• జాతీయ హోదా: ఏపీ పునర్విభజన చట్టం 2014 సెక్షన్ 90 ప్రకారం జాతీయ ప్రాజెక్టు.\n• ప్రాజెక్ట్ నది: గోదావరి నది (పశ్చిమ/తూర్పు గోదావరి జిల్లా సరిహద్దు).\n• మొదటి దశ లక్ష్యం: 41.15 మీటర్ల నీటి నిల్వతో సత్వర సాగునీరు అందించడం.\n• పరీక్ష ప్రాముఖ్యత: AP జాగ్రఫీ, నదులు & నీటిపారుదల ప్రాజెక్టులు.\n• లింక్: https://jalshakti-dowr.gov.in",
        "exam_relevance": "APPSC గ్రూప్-1, గ్రూప్-2 ఆంధ్రప్రదేశ్ జాగ్రఫీ & ప్రాజెక్టులు",
        "source": "కేంద్ర జలశక్తి మంత్రిత్వ శాఖ & PPA"
    }
]

def sync_daily_news(target_date=None):
    """
    Sync news for the target date from live multi-source feeds:
    Google News Telugu, Sakshi, Namasthe Telangana, BBC Telugu, ABP Desam.
    Strictly filters against crime, gossip, and junk.
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
    all_raw_items = []

    # 1. Fetch from Google News Telugu topic feeds (Live & Current)
    topic_queries = [
        ("education", "నోటిఫికేషన్ OR పరీక్షలు OR ఉద్యోగాలు OR ఏపీపీఎస్సీ OR టీఎస్పీఎస్సీ OR డీఎస్సీ OR TGPSC OR NTA OR APPSC"),
        ("regional", "ఆంధ్రప్రదేశ్ ప్రభుత్వం OR తెలంగాణ ప్రభుత్వం OR కేబినెట్ ఆమోదం OR పథకం OR రైతు భరోసా OR అమరావతి OR పోలవరం OR దీపం-2"),
        ("economy", "రిజర్వ్ బ్యాంక్ OR ఆర్బీఐ OR బ్యాంకింగ్ OR జీడీపీ OR ద్రవ్యోల్బణం OR ఆర్థిక OR ఈపీఎఫ్ఓ OR రెపో రేటు"),
        ("science_tech", "ఇస్రో OR నాసా OR డీఆర్‌డీవో OR అంతరిక్షం OR ఉపగ్రహం OR కృత్రిమ మేధ OR సైన్స్ OR శాస్త్రవేత్తలు"),
        ("national", "భారత రాజ్యాంగం OR సుప్రీంకోర్టు రాజ్యాంగ ధర్మాసనం OR కేంద్ర కేబినెట్ ఆమోదం OR పార్లమెంట్ బిల్లు OR ఎన్నికల సంస్కరణలు"),
        ("environment", "పర్యావరణం OR జాతీయ పార్కు OR పోలవరం OR వాతావరణం OR భారీ వర్షాలు OR అల్పపీడనం"),
        ("sports_awards", "క్రీడలు OR ఛాంపియన్‌షిప్ OR ఒలింపిక్స్ OR ఆసియా క్రీడలు OR పతకం OR స్వర్ణం OR గ్రాండ్‌మాస్టర్")
    ]

    print(f"📡 [{target_date}] లైవ్ తెలుగు వార్తల సేకరణ ప్రారంభమైంది...")
    for cat, query in topic_queries:
        try:
            live_items = fetch_google_news_telugu(query, days=2)
            for it in live_items:
                it["category"] = cat
            all_raw_items.extend(live_items)
        except Exception as e:
            print(f"Topic fetch error: {e}")

    # 2. Fetch from major Telugu Newspaper RSS feeds
    rss_sources = [
        ("సాక్షి (Sakshi)", "https://www.sakshi.com/rss.xml"),
        ("నమస్తే తెలంగాణ (Namasthe Telangana)", "https://ntnews.com/feed"),
        ("BBC తెలుగు (BBC Telugu)", "https://feeds.bbci.co.uk/telugu/rss.xml"),
        ("ఏషియానెట్ ఆంధ్రప్రదేశ్ (Asianet AP)", "https://telugu.asianetnews.com/rss/andhra-pradesh"),
        ("ఏబీపీ దేశం (ABP Desam)", "https://telugu.abplive.com/home/feed")
    ]

    for src_name, feed_url in rss_sources:
        try:
            items = fetch_rss_feed(feed_url, src_name)
            all_raw_items.extend(items)
        except Exception:
            pass

    # 3. Filter and Insert High-Yield Exam News
    seen_in_batch = set()
    category_counts = {}

    for it in all_raw_items:
        title = it.get("title", "").strip()
        summary = it.get("summary", "").strip()
        combined_text = title + " " + summary

        if not is_exam_worthy_content(combined_text):
            continue
        if title in existing_titles or title in seen_in_batch:
            continue
        if is_duplicate_article(title, existing_titles) or is_duplicate_article(title, seen_in_batch):
            continue

        cat = it.get("category") or detect_category(combined_text)
        # Cap at max 3 articles per category per day to ensure balanced coverage
        if category_counts.get(cat, 0) >= 3:
            continue

        detailed_notes, exam_relevance = build_exam_detailed_notes(
            title=title,
            summary=summary,
            category=cat,
            source=it.get("source", "తెలుగు దినపత్రికలు"),
            link=it.get("link", "https://epaper.eenadu.net")
        )

        insert_article(
            date=target_date,
            category=cat,
            title=title,
            summary=summary,
            detailed_notes=detailed_notes,
            exam_relevance=exam_relevance,
            tags="లైవ్ డైలీ CA, పోటీ పరీక్షల ప్రత్యేకం",
            source=it.get("source", "తెలుగు దినపత్రికలు")
        )

        insert_one_liner(
            target_date,
            cat,
            f"[{cat.upper()}] {title}"
        )

        existing_titles.add(title)
        seen_in_batch.add(title)
        category_counts[cat] = category_counts.get(cat, 0) + 1
        added_articles += 1

        if added_articles >= 15:
            break

    # 4. Fallback Protection: if live network yielded < 6 items, supplement from rotating archive
    if len(existing_titles) < 6:
        import hashlib
        date_hash = int(hashlib.md5(target_date.encode('utf-8')).hexdigest(), 16)
        start_idx = date_hash % len(ROTATING_EXAM_ARCHIVE)
        
        for i in range(len(ROTATING_EXAM_ARCHIVE)):
            item = ROTATING_EXAM_ARCHIVE[(start_idx + i) % len(ROTATING_EXAM_ARCHIVE)]
            if item["title"] not in existing_titles and not is_duplicate_article(item["title"], existing_titles):
                insert_article(
                    date=target_date,
                    category=item["category"],
                    title=item["title"],
                    summary=item["summary"],
                    detailed_notes=item["detailed_notes"],
                    exam_relevance=item["exam_relevance"],
                    tags="పోటీ పరీక్షల ప్రత్యేకం, జీరో నాన్‌ఎగ్జామ్",
                    source=item["source"]
                )
                insert_one_liner(
                    target_date,
                    item["category"],
                    f"[{item['category'].upper()}] {item['title']}"
                )
                existing_titles.add(item["title"])
                added_articles += 1
                if len(existing_titles) >= 8:
                    break

    cursor.execute("""
        INSERT INTO sync_logs (synced_at, date, articles_count, status)
        VALUES (?, ?, ?, ?)
    """, (datetime.now().isoformat(), target_date, added_articles, "SUCCESS"))

    conn.commit()
    conn.close()

    print(f"✅ [{target_date}] పోటీ పరీక్షల లైవ్ వార్తలు విజయవంతంగా సింక్ అయ్యాయి: {added_articles} తాజా వార్తలు చేర్చబడ్డాయి.")
    return {
        "date": target_date,
        "articles_added": added_articles,
        "status": "success"
    }

if __name__ == "__main__":
    res = sync_daily_news()
    print("ఫలితం:", res)

