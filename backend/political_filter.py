# -*- coding: utf-8 -*-
"""
Political News & Sensationalism Filter for Competitive Exam Current Affairs.
Strictly eliminates:
- Political Party Names & Fronts (YSRCP, TDP, Congress, BJP, BRS, JSP, TMC, etc.)
- Partisan Politics, Defections, Disqualifications, and Inner-party Rivalry
- Election Campaigning, Bypolls, Surveys, Ticket Allotments & Rallies
- Political Mudslinging, Attacks, Counter-attacks, and Controversial Statements
Preserves:
- Official Government Schemes, Cabinet Decisions, State Policies, Constitutional Verdicts & Welfare Programs
"""

import re

POLITICAL_PATTERNS = [
    # 1. Political Party Names & Fronts
    r"(వైసీపీ|వైకాపా|వైఎస్సార్సీపీ|వైఎస్సార్ కాంగ్రెస్|\bYSRCP\b|\bYCP\b)",
    r"(టీడీపీ|టిడిపి|తెలుగుదేశం|\bTDP\b)",
    r"(కాంగ్రెస్|కాంగ్రెస్‌|ఏఐసీసీ|పీసీసీ|టీపీసీసీ|ఏపీపీసీసీ|\bCongress\b|\bAICC\b|\bTPCC\b|\bPCC\b|\bINC\b)",
    r"(బీజేపీ|బిజెపి|భాజపా|కమలం పార్టీ|\bBJP\b)",
    r"(బీఆర్ఎస్|బిఆర్ఎస్|టీఆర్ఎస్|టిఆర్ఎస్|గులాబీ పార్టీ|\bBRS\b|\bTRS\b)",
    r"(జనసేన|సేనాని|పవన్‌ కల్యాణ్‌ పార్టీ|\bJSP\b)",
    r"(తృణమూల్|టీఎంసీ|టిఎంసి|దీదీకి షాక్|\bTMC\b)",
    r"(\bAAP\b|ఆమ్ ఆద్మీ|ఆమ్‌ ఆద్మీ)",
    r"(డీఎంకే|\bDMK\b|అన్నాడీఎంకే|\bAIADMK\b)",
    r"(మజ్లిస్|ఎంఐఎం|\bAIMIM\b)",
    r"(సీపీఐ|సీపీఎం|సిపిఐ|సిపిఎం|\bCPI\b|\bCPM\b)",
    r"(సమాజ్‌వాదీ|ఎస్పీ|\bSamajwadi\b|\bBSP\b|బీఎస్పీ)",

    # 2. Elections, Bypolls, Campaigns & Polling Gossip
    r"(ఉప\s*ఎన్నిక|బైపోల్|\bby-?election\b|\bbypoll\b)",
    r"(పార్టీ గుర్తు|గుర్తు కేటాయింపు|గుర్తు రద్దు)",
    r"(ఎన్నికల ప్రచారం|రోడ్‌షో|పాదయాత్ర|ట్రాక్టర్ ర్యాలీ|బహిరంగ సభ|మాక్ అసెంబ్లీ)",
    r"(ఏ పార్టీ గెలవబోతుంది|ఎవరు గెలుస్తారు|గెలుపు ఓటములు|ఒపీనియన్ పోల్|ఎగ్జిట్ పోల్|కామెంట్ రూపంలో|కామెంట్ చేయండి)",
    r"(టికెట్ దక్కని|సీట్ల సర్దుబాటు|సీట్ల కేటాయింపు|అభ్యర్థులు వీళ్లే|అభ్యర్థిత్వం)",
    r"(ఓట్ల రాజకీయం|ఓటు బ్యాంకు|ఓటర్లను ఆకట్టుకునే|ఎన్నికల స్టంట్)",

    # 3. Party Defections, Inner Rivalry & Disqualifications
    r"(అనర్హత వేటు|స్పీకర్‌‌‌‌ తీర్పు|పార్టీ ఫిరాయింపు|పార్టీ మారిన|కండువా కప్పిన|చేరికలు|జంపింగ్)",
    r"(అంతర్గత పోరు|వర్గ పోరు|వర్గ విభేదాలు|అసమ్మతి నేత|తిరుగుబాటు నేత)",
    r"(పార్టీకి రాజీనామా|పదవికి రాజీనామా|నేత రాజీనామా|రావత్‌ రాజీనామా|రాజీనామా లేఖ|రాజీనామా చేశారు)",
    r"(హై టెన్షన్|చుట్టుముట్టిన కాంగ్రెస్|చుట్టుముట్టిన నేతలు|తీవ్ర ఉద్రిక్తత|ముట్టడి|ధర్నా|ఘెరావ్)",

    # 4. Political Mudslinging, Attacks & Sensational Bickering
    r"(మాటల యుద్ధం|విమర్శల వర్షం|ప్రశంసల వర్షం|దుమ్మెత్తిపోసిన|కౌంటర్ ఇచ్చ|కౌంటర్..!|కౌంటర్ ఇచ్చారు)",
    r"(సంచలన వ్యాఖ్యలు|వివాదాస్పద వ్యాఖ్యలు|మాటల తూటాలు|నిప్పులు చెరిగిన|ఆగ్రహం వ్యక్తం|తీవ్రంగా మండిపడ్డ)",
    r"(టార్గెట్ చేస్తున్న|టార్గెట్ చేసిన|సవాల్ విసిరిన|సవాల్ స్వీకరించిన|తిప్పికొట్టిన|కడిగిపారేసిన|ఏకిపారేసిన)",
    r"(యూటర్న్|ఝలక్|షాకిచ్చిన|బిగ్ షాక్|బిగ్‌ షాక్‌|షాక్ ఇచ్చిన|షాకింగ్|సెటైర్లు)",
    r"(రాజకీయ రచ్చ|రాజకీయ దుమారం|రాజకీయ ప్రకంపనలు|పొలిటికల్|రాజకీయాలు|రాజకీయ నేత|రాజకీయ పార్టీ|రాజకీయ విమర్శలు)",

    # 5. Leader vs Leader Political Clashes
    r"(సీఎం రేవంత్‌పై కేటీఆర్|కేటీఆర్‌పై రేవంత్|జగన్‌పై చంద్రబాబు|చంద్రబాబుపై జగన్|పవన్‌పై వైసీపీ|బాబును టార్గెట్|మోదీపై రాహుల్|రాహుల్‌పై బీజేపీ)",
    r"(దానం నాగేందర్|దానంపై)"
]

_COMPILED_POLITICAL_REGEX = [re.compile(p, re.IGNORECASE) for p in POLITICAL_PATTERNS]

def is_political_content(text):
    """
    Returns True if the text contains political party references, election gossip,
    or political mudslinging unsuitable for competitive exams.
    """
    if not text:
        return False
    clean_text = str(text).strip()
    if not clean_text:
        return False
    for regex in _COMPILED_POLITICAL_REGEX:
        if regex.search(clean_text):
            return True
    return False

def filter_exam_articles(articles):
    """Filter out political articles from a list of article dicts/objects"""
    return [
        a for a in articles 
        if not is_political_content(f"{a.get('title', '')} {a.get('category', '')} {a.get('summary', '')}")
    ]

def filter_exam_one_liners(one_liners):
    """Filter out political one-liners"""
    return [
        ol for ol in one_liners 
        if not is_political_content(ol.get("point", ""))
    ]

def filter_exam_quizzes(quizzes):
    """Filter out political quizzes"""
    return [
        q for q in quizzes 
        if not is_political_content(f"{q.get('question', '')} {q.get('explanation', '')}")
    ]
