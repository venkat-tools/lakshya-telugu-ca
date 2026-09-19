# -*- coding: utf-8 -*-
"""
Compiles AP & TS 2026 Government Welfare Schemes & Policies Master Handbook PDF.
Targeted for APPSC Group-1, Group-2 (Paper-2 AP Schemes), Group-3, and TSPSC Exams.
Generates: frontend/pdfs/ap_ts_schemes_master_guide_2026.pdf
"""

import os
import sys
import subprocess
import shutil

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(base_dir, "backend"))

def get_browser():
    for p in [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/usr/bin/chromium-browser"
    ]:
        if os.path.exists(p):
            return p
    for name in ["msedge", "google-chrome", "chromium"]:
        found = shutil.which(name)
        if found:
            return found
    return None

AP_SCHEMES = [
    {
        "name": "దీపం-2 పథకం (Deepam-2 Free LPG Scheme)",
        "dept": "పౌర సరఫరాల శాఖ (Civil Supplies Department)",
        "budget": "రూ. 2,684 కోట్లు వార్షిక కేటాయింపు",
        "beneficiaries": "రాష్ట్రంలోని తెల్ల రేషన్ కార్డు కలిగి ఉన్న అర్హులైన పేద మహిళలు",
        "details": [
            "ఎన్నికల సూపర్ సిక్స్ హామీల్లో భాగంగా అర్హులైన ప్రతి పేద మహిళకు ఏడాదికి 3 ఉచిత ఎల్పీజీ సిలిండర్లు అందిస్తారు.",
            "మొదటి విడత దీపావళి నుండి ప్రారంభమైంది; ప్రతినెలా లేదా నిర్ణీత గడువులో బుకింగ్ చేసుకున్న లబ్ధిదారుల ఖాతాకు సబ్సిడీ మొత్తం నేరుగా జమ (DBT) అవుతుంది.",
            "లబ్ధిదారులకు ఈకేవైసీ (e-KYC) మరియు ఆధార్ సీడింగ్ తప్పనిసరిగా ఉండాలి."
        ]
    },
    {
        "name": "తల్లికి వందనం పథకం (Talliki Vandanam)",
        "dept": "పాఠశాల విద్యా శాఖ (School Education Department)",
        "budget": "రూ. 6,500 కోట్లు",
        "beneficiaries": "ఒకటో తరగతి నుండి ఇంటర్మీడియట్ వరకు పాఠశాలకు వెళ్లే విద్యార్థుల తల్లులు",
        "details": [
            "గతంలో ఉన్న నిబంధనలను సవరించి, ఇంట్లో ఎంతమంది పిల్లలు బడికి వెళ్తుంటే ప్రతి ఒక్కరికీ ఏడాదికి ₹15,000 చొప్పున ఆర్థిక సహాయం అందిస్తారు.",
            "విద్యార్థులకు 75% పాఠశాల హాజరు మరియు ప్రభుత్వ లేదా గుర్తింపు పొందిన ప్రైవేట్ పాఠశాలల్లో నమోదు నిబంధనలు వర్తిస్తాయి.",
            "డబ్బులు నేరుగా విద్యార్థి తల్లి బ్యాంకు ఖాతాలోనే జమ చేయబడతాయి."
        ]
    },
    {
        "name": "అన్నదాత సుఖీభవ (Annadata Sukhibhava)",
        "dept": "వ్యవసాయ & రైతు సంక్షేమ శాఖ (Agriculture Department)",
        "budget": "రూ. 4,500 కోట్లు",
        "beneficiaries": "రాష్ట్రంలోని సన్న, చిన్నకారు మరియు కౌలు రైతులు",
        "details": [
            "ప్రతి రైతు కుటుంబానికి ఏటా ₹20,000 ఆర్థిక సాయం అందించే ప్రతిష్టాత్మక పథకం.",
            "కేంద్ర ప్రభుత్వ 'పీఎం కిసాన్ సమ్మాన్ నిధి' కింద ఇచ్చే ₹6,000 లకు అదనంగా, రాష్ట్ర ప్రభుత్వం ₹14,000 కలిపి మొత్తం ₹20,000 ను మూడు విడతల్లో పంపిణీ చేస్తుంది.",
            "అర్హులైన భూమిలేని ఎస్సీ, ఎస్టీ, బీసీ, మైనారిటీ కౌలు రైతులకు కూడా ఈ పథకం వర్తింపజేస్తారు."
        ]
    },
    {
        "name": "మహిళలకు ఉచిత బస్సు ప్రయాణం (Stree Shakthi Free Bus Travel)",
        "dept": "ఆంధ్రప్రదేశ్ రాష్ట్ర రోడ్డు రవాణా సంస్థ (APSRTC)",
        "budget": "రూ. 1,200 కోట్లు (రీయింబర్స్‌మెంట్)",
        "beneficiaries": "ఆంధ్రప్రదేశ్ నివాసితులైన బాలికలు, మహిళలు మరియు ట్రాన్స్‌జెండర్లు",
        "details": [
            "ఏపీఎస్ఆర్టీసీకి చెందిన పల్లెవెలుగు, అల్ట్రా డీలక్స్ మరియు సిటీ ఆర్డినరీ బస్సుల్లో ఉచిత ప్రయాణ సౌకర్యం.",
            "ఆధార్ లేదా ఇతర అధికారిక నివాస గుర్తింపు కార్డు చూపించి 'జీరో ఫేర్ టికెట్' (Zero Fare Ticket) పొందవచ్చు.",
            "మహిళల ఆర్థిక స్వావలంబన, విద్యా మరియు ఉద్యోగ ప్రయాణ ఖర్చులను తగ్గించడం ప్రధాన లక్ష్యం."
        ]
    },
    {
        "name": "యువగళం నిరుద్యోగ భృతి & నైపుణ్య శిక్షణ (Yuva Galam)",
        "dept": "యువజన సర్వీసులు & నైపుణ్యాభివృద్ధి సంస్థ (APSSDC)",
        "budget": "రూ. 1,800 కోట్లు",
        "beneficiaries": "డిగ్రీ, డిప్లొమా లేదా పీజీ పూర్తి చేసిన నిరుద్యోగ యువతీ యువకులు (18-35 ఏళ్లు)",
        "details": [
            "ఉద్యోగం లేదా ఉపాధి లభించే వరకు అర్హులైన నిరుద్యోగ యువతకు ప్రతి నెలా ₹3,000 నిరుద్యోగ భృతి.",
            "వచ్చే 5 ఏళ్లలో 20 లక్షల ఉద్యోగాల కల్పనే లక్ష్యంగా టాటా, హెచ్‌సీఎల్, గూగుల్ భాగస్వామ్యంతో మండల స్థాయిలో నైపుణ్య కేంద్రాలు ఏర్పాటు."
        ]
    },
    {
        "name": "ఆంధ్రప్రదేశ్ నూతన పారిశ్రామిక విధానం 2024-2029 (Industrial Policy 4.0)",
        "dept": "పరిశ్రమలు & వాణిజ్య శాఖ (Industries & Commerce)",
        "budget": "రూ. లక్ష కోట్ల పెట్టుబడుల లక్ష్యం",
        "beneficiaries": "గ్లోబల్ ఇన్వెస్టర్లు, ఎంఎస్ఎంఈలు మరియు పారిశ్రామికవేత్తలు",
        "details": [
            "'ఈజ్ ఆఫ్ డూయింగ్ బిజినెస్' నుండి 'స్పీడ్ ఆఫ్ డూయింగ్ బిజినెస్' (Speed of Doing Business) నినాదంతో నూతన విధానం.",
            "సింగిల్ విండో పోర్టల్ ద్వారా దరఖాస్తు చేసిన 21 రోజుల్లోనే అన్ని ప్రభుత్వ అనుమతులు మంజూరు.",
            "గ్రీన్ ఎనర్జీ, ఎలక్ట్రానిక్స్, సెమీకండక్టర్లు మరియు ఫార్మా రంగాల్లో భారీ ప్రోత్సాహకాలు."
        ]
    },
    {
        "name": "అమరావతి రాజధాని పునర్నిర్మాణం & పోలవరం నిధుల కేటాయింపు",
        "dept": "CRDA & జలవనరుల శాఖ (Water Resources)",
        "budget": "ప్రపంచ బ్యాంకు & ఏడీబీ ₹15,000 కోట్లు; కేంద్ర జలశక్తి ₹12,157 కోట్లు",
        "beneficiaries": "సమగ్ర రాష్ట్ర ప్రజలు మరియు ఉత్తరాంధ్ర, రాయలసీమ సాగునీటి రంగాలు",
        "details": [
            "ప్రపంచ బ్యాంకు, ఏషియన్ డెవలప్‌మెంట్ బ్యాంక్ (ADB) సహాయంతో ₹15,000 కోట్ల నిధులతో అమరావతిలో మౌలిక వసతుల పనులు పునఃప్రారంభం.",
            "గోదావరి నదిపై పోలవరం ప్రాజెక్టు కొత్త డయాఫ్రమ్ వాల్ నిర్మాణం మరియు మొదటి దశ 41.15 మీటర్ల నీటినిల్వ పనులకు కేంద్రం ₹12,157 కోట్లు మంజూరు."
        ]
    }
]

TS_SCHEMES = [
    {
        "name": "మహాలక్ష్మి పథకం (Maha Lakshmi 6 Guarantees)",
        "dept": "రవాణా శాఖ & పౌర సరఫరాల శాఖ (Transport & Civil Supplies)",
        "budget": "రూ. 3,500 కోట్లు",
        "beneficiaries": "తెలంగాణలోని మహిళలు, బాలికలు మరియు ట్రాన్స్‌జెండర్లు",
        "details": [
            "TSRTC పల్లెవెలుగు, ఎక్స్‌ప్రెస్ బస్సుల్లో రాష్ట్ర వ్యాప్తంగా మహిళలకు ఉచిత ప్రయాణం (Free Bus Travel).",
            "అర్హులైన తెల్ల రేషన్ కార్డు మహిళలకు కేవలం ₹500 కే గ్యాస్ సిలిండర్ పంపిణీ; మిగిలిన సబ్సిడీని ప్రభుత్వమే ఆయిల్ కంపెనీలకు చెల్లిస్తుంది.",
            "మహిళా కుటుంబ పెద్దలకు నెలకు ₹2,500 ఆర్థిక సాయం అందించే ప్రక్రియపై కసరత్తు."
        ]
    },
    {
        "name": "రైతు భరోసా & రుణమాఫీ 2024-2026 (Rythu Bharosa)",
        "dept": "వ్యవసాయ శాఖ (Agriculture Department)",
        "budget": "రుణమాఫీకి ₹18,000 కోట్లు; రైతు భరోసాకు ₹15,000 కోట్లు",
        "beneficiaries": "రాష్ట్రంలోని పట్టాదారులు మరియు కౌలు రైతులు",
        "details": [
            "రైతులకు ప్రతి ఎకరాకు సంవత్సరానికి ₹15,000 పెట్టుబడి సహాయం (ఖరీఫ్ ₹7,500 + రబీ ₹7,500).",
            "వరి పంటకు మద్దతు ధరతో పాటు క్వింటాల్‌కు ₹500 బోనస్ (Bonus on Fine Rice Paddy).",
            "రైతులకు ఏకకాలంలో రూ. 2 లక్షల వరకు వ్యవసాయ రుణమాఫీని విజయవంతంగా అమలు చేసిన ప్రభుత్వం."
        ]
    },
    {
        "name": "గృహజ్యోతి పథకం (Gruha Jyothi 200 Units Free Power)",
        "dept": "విద్యుత్ శాఖ (Energy Department / Discoms)",
        "budget": "రూ. 2,400 కోట్లు",
        "beneficiaries": "నెలకు 200 యూనిట్ల లోపు విద్యుత్ వినియోగించే తెల్ల రేషన్ కార్డు కుటుంబాలు",
        "details": [
            "గృహ అవసరాలకు 200 యూనిట్ల వరకు వాడే గృహ వినియోగదారులకు 'జీరో విద్యుత్ బిల్లు' (Zero Electricity Bill).",
            "ప్రజా పాలన దరఖాస్తులను పరిశీలించి మీటర్లకు అనుసంధానించడం ద్వారా ఆటోమేటిక్ రాయితీ వర్తింపు."
        ]
    },
    {
        "name": "ఇందిరమ్మ ఇండ్లు పథకం (Indiramma Indlu)",
        "dept": "గృహనిర్మాణ శాఖ (Housing Department)",
        "budget": "రూ. 7,500 కోట్లు",
        "beneficiaries": "సొంత స్థలం ఉండి ఇల్లు లేని నిరుపేద కుటుంబాలు",
        "details": [
            "సొంత స్థలం ఉన్న లబ్ధిదారులకు ఇంటి నిర్మాణానికి దశలవారీగా ₹5 లక్షల ఆర్థిక సాయం.",
            "స్థలం లేని నిరుపేదలకు ఉచితంగా ఇంటి స్థలంతో పాటు ₹5 లక్షల నిర్మాణ వ్యయం.",
            "ప్రతి అసెంబ్లీ నియోజకవర్గానికి కనీసం 3,500 ఇళ్లు మంజూరు చేసేలా మొదటి విడత కార్యాచరణ."
        ]
    },
    {
        "name": "యువ వికాసం పథకం (Yuva Vikasam)",
        "dept": "ఉన్నత విద్యా శాఖ (Higher Education)",
        "budget": "రూ. 2,000 కోట్లు",
        "beneficiaries": "పోటీ పరీక్షల అభ్యర్థులు మరియు కళాశాల విద్యార్థులు",
        "details": [
            "ఉన్నత విద్య అభ్యసించే పేద విద్యార్థులకు ₹5 లక్షల విద్యా భరోసా కార్డ్ (Vidya Bharosa Card).",
            "ప్రతి మండలంలో తెలంగాణ అంతర్జాతీయ పాఠశాలల (Telangana International Schools) స్థాపన.",
            "గ్రూప్-1, గ్రూప్-2, డీఎస్సీ అభ్యర్థులకు ఉచిత కోచింగ్ మరియు స్టడీ సర్కిళ్ల బలోపేతం."
        ]
    },
    {
        "name": "చేయూత పింఛన్లు (Cheyutha Pension Scheme)",
        "dept": "పంచాయతీరాజ్ & గ్రామీణాభివృద్ధి శాఖ (Rural Development)",
        "budget": "రూ. 12,000 కోట్లు",
        "beneficiaries": "వృద్ధులు, వితంతువులు, ఒంటరి మహిళలు, చేనేత, గీత కార్మికులు మరియు దివ్యాంగులు",
        "details": [
            "ప్రస్తుతం ఉన్న ఆసరా పింఛన్లను పెంచుతూ నెలకు ₹4,000 సామాజిక భద్రతా పింఛను పెంపు.",
            "దివ్యాంగులకు నెలకు ₹6,000 వరకు గౌరవ భృతి పంపిణీ."
        ]
    },
    {
        "name": "తెలంగాణ సమగ్ర కుటుంబ కుల గణన సర్వే 2024-2026",
        "dept": "ప్రణాళికా శాఖ (Planning Department)",
        "budget": "రూ. 150 కోట్లు",
        "beneficiaries": "రాష్ట్రంలోని 1.25 కోట్ల కుటుంబాలు",
        "details": [
            "రాష్ట్రంలో సామాజిక, విద్య, ఆర్థిక, ఉపాధి మరియు రాజకీయ స్థితిగతుల అధ్యయనం కోసం 75 అంశాలతో సమగ్ర ఇంటింటి సర్వే.",
            "స్థానిక సంస్థల ఎన్నికల్లో బీసీ రిజర్వేషన్ల పెంపు మరియు సంక్షేమ పథకాల శాస్త్రీయ పంపిణీకి సర్వే నివేదిక కీలకం."
        ]
    }
]

SCHEME_MCQS = [
    {
        "q": "ఆంధ్రప్రదేశ్ ప్రభుత్వం అమలు చేస్తున్న 'దీపం-2' పథకం నిబంధనల ప్రకారం అర్హులైన కుటుంబానికి ఏడాదికి ఎన్ని ఉచిత ఎల్పీజీ సిలిండర్లు లభిస్తాయి?",
        "opts": ["A) 2 సిలిండర్లు", "B) 3 సిలిండర్లు", "C) 4 సిలిండర్లు", "D) 6 సిలిండర్లు"],
        "ans": "B) 3 సిలిండర్లు",
        "exp": "ఎన్నికల సూపర్ సిక్స్ హామీలలో ఒకటైన దీపం-2 పథకం కింద అర్హులైన తెల్ల రేషన్ కార్డు కలిగిన ప్రతి మహిళకు ఏడాదికి 3 ఉచిత గ్యాస్ సిలిండర్లు డీబీటీ పద్ధతిలో అందుతాయి."
    },
    {
        "q": "ఆంధ్రప్రదేశ్ 'అన్నదాత సుఖీభవ' పథకం కింద రైతులకు అందే మొత్తం వార్షిక ఆర్థిక సహాయం ఎంత?",
        "opts": ["A) ₹10,000", "B) ₹15,000", "C) ₹20,000", "D) ₹25,000"],
        "ans": "C) ₹20,000",
        "exp": "కేంద్ర ప్రభుత్వ పీఎం కిసాన్ నిధి ₹6,000 కు రాష్ట్ర ప్రభుత్వం ₹14,000 కలిపి మొత్తం ₹20,000 ను రైతులకు అందిస్తుంది."
    },
    {
        "q": "తెలంగాణ ప్రభుత్వ 'మహాలక్ష్మి' పథకంలో భాగంగా మహిళలకు ఏయే ఆర్టీసీ బస్సులలో ఉచిత ప్రయాణం కల్పించారు?",
        "opts": ["A) కేవలం సిటీ బస్సుల్లో మాత్రమే", "B) పల్లెవెలుగు మరియు ఎక్స్‌ప్రెస్ బస్సులలో", "C) గరుడ మరియు వోల్వో బస్సులలో", "D) అన్ని అంతర్రాష్ట్ర ఏసీ బస్సులలో"],
        "ans": "B) పల్లెవెలుగు మరియు ఎక్స్‌ప్రెస్ బస్సులలో",
        "exp": "మహాలక్ష్మి పథకం ద్వారా తెలంగాణ వ్యాప్తంగా TSRTC పల్లెవెలుగు మరియు ఎక్స్‌ప్రెస్ బస్సుల్లో మహిళలకు జీరో టికెట్ ద్వారా ఉచిత ప్రయాణం కల్పించారు."
    },
    {
        "q": "తెలంగాణ 'గృహజ్యోతి' పథకం కింద లబ్ధిదారులకు ఎన్ని యూనిట్ల వరకు ఉచిత విద్యుత్ లభిస్తుంది?",
        "opts": ["A) 100 యూనిట్లు", "B) 150 యూనిట్లు", "C) 200 యూనిట్లు", "D) 300 యూనిట్లు"],
        "ans": "C) 200 యూనిట్లు",
        "exp": "నెలకు 200 యూనిట్ల లోపు విద్యుత్ వినియోగించే గృహాలకు జీరో కరెంట్ బిల్లు వర్తిస్తుంది."
    },
    {
        "q": "ఆంధ్రప్రదేశ్ 'తల్లికి వందనం' పథకం తాజా మార్గదర్శకాల విశేషం ఏమిటి?",
        "opts": ["A) కుటుంబంలో కేవలం ఒక బిడ్డకు మాత్రమే ₹15,000 లభిస్తుంది", "B) ఇంట్లో బడికి వెళ్లే ప్రతి బిడ్డకూ ₹15,000 చొప్పున ఆర్థిక సహాయం అందుతుంది", "C) కేవలం పదో తరగతి విద్యార్థులకు మాత్రమే వర్తిస్తుంది", "D) నగదు బదులుగా పుస్తకాలు మాత్రమే ఇస్తారు"],
        "ans": "B) ఇంట్లో బడికి వెళ్లే ప్రతి బిడ్డకూ ₹15,000 చొప్పున ఆర్థిక సహాయం అందుతుంది",
        "exp": "గతంలోని ఒక్క బిడ్డ నిబంధనను తొలగించి, కుటుంబంలో బడికి వెళ్లే ఎంతమంది పిల్లలున్నా ప్రతి ఒక్కరికీ తల్లికి వందనం కింద ₹15,000 అందిస్తారు."
    },
    {
        "q": "తెలంగాణ 'ఇందిరమ్మ ఇండ్లు' పథకం కింద సొంత స్థలం ఉన్న నిరుపేదలకు ప్రభుత్వం అందించే గృహ నిర్మాణ సహాయం ఎంత?",
        "opts": ["A) ₹2.5 లక్షలు", "B) ₹3.0 లక్షలు", "C) ₹5.0 లక్షలు", "D) ₹10.0 లక్షలు"],
        "ans": "C) ₹5.0 లక్షలు",
        "exp": "సొంత స్థలం ఉన్న లబ్ధిదారులకు పక్కా ఇంటి నిర్మాణానికి 4 విడతలలో మొత్తం ₹5 లక్షల నగదు సాయం ప్రభుత్వం అందజేస్తుంది."
    },
    {
        "q": "ఆంధ్రప్రదేశ్ నూతన పారిశ్రామిక విధానం 2024-2029 (Industrial Policy 4.0) లో దరఖాస్తు చేసిన ఎన్ని రోజుల్లోగా అనుమతులు ఇవ్వాలని నిర్ణయించారు?",
        "opts": ["A) 7 రోజులు", "B) 15 రోజులు", "C) 21 రోజులు", "D) 45 రోజులు"],
        "ans": "C) 21 రోజులు",
        "exp": "'స్పీడ్ ఆఫ్ డూయింగ్ బిజినెస్' సాధనలో భాగంగా సింగిల్ విండో ద్వారా 21 రోజుల్లోనే పరిశ్రమలకు అన్ని శాఖల అనుమతులు మంజూరు చేయాలని చట్టబద్ధం చేశారు."
    },
    {
        "q": "తెలంగాణ 'చేయూత' పథకం కింద వృద్ధులు, వితంతువుల సామాజిక పింఛను మొత్తాన్ని ఎంతకు పెంచాలని నిర్ణయించారు?",
        "opts": ["A) ₹3,016", "B) ₹4,000", "C) ₹5,000", "D) ₹6,000"],
        "ans": "B) ₹4,000",
        "exp": "చేయూత పథకం ద్వారా ఆసరా పింఛన్లను పెంచుతూ నెలకు ₹4,000 చొప్పున సామాజిక భద్రతా పింఛన్లు అందించే ప్రక్రియ చేపట్టారు."
    },
    {
        "q": "ఆంధ్రప్రదేశ్ పునర్వ్యవస్థీకరణ చట్టం 2014 లోని ఏ సెక్షన్ ప్రకారం పోలవరం ప్రాజెక్టుకు జాతీయ ప్రాజెక్ట్ హోదా కల్పించారు?",
        "opts": ["A) సెక్షన్ 45", "B) సెక్షన్ 90", "C) సెక్షన్ 94", "D) సెక్షన్ 108"],
        "ans": "B) సెక్షన్ 90",
        "exp": "ఏపీ పునర్విభజన చట్టం 2014 లోని సెక్షన్ 90 ప్రకారం పోలవరం జాతీయ ప్రాజెక్టుగా గుర్తింపు పొందింది; కేంద్ర ప్రభుత్వం దీని నీటిపారుదల వ్యయాన్ని భరిస్తుంది."
    },
    {
        "q": "తెలంగాణ ప్రభుత్వం చేపట్టిన సమగ్ర కుటుంబ సర్వేలో కుటుంబ స్థితిగతులను ఎన్ని ప్రధాన అంశాల (Indicators) ఆధారంగా నమోదు చేశారు?",
        "opts": ["A) 35 అంశాలు", "B) 50 అంశాలు", "C) 75 అంశాలు", "D) 100 అంశాలు"],
        "ans": "C) 75 అంశాలు",
        "exp": "తెలంగాణ ప్రణాళికా శాఖ రూపొందించిన 75 సూచికల ప్రశ్నావళి ఆధారంగా రాష్ట్రవ్యాప్తంగా సమగ్ర సామాజిక, విద్య, ఆర్థిక, ఉపాధి మరియు కుల గణన సర్వే నిర్వహించారు."
    }
]

def generate_schemes_handbook():
    pdf_out = os.path.join(base_dir, "frontend", "pdfs", "ap_ts_schemes_master_guide_2026.pdf")
    os.makedirs(os.path.dirname(pdf_out), exist_ok=True)

    ap_cards_html = ""
    for idx, sc in enumerate(AP_SCHEMES, 1):
        pts = "".join([f'<li style="margin-bottom: 6px; font-size: 11px; line-height: 1.5; color: #1e293b;">{p}</li>' for p in sc["details"]])
        ap_cards_html += f"""
        <div style="page-break-inside: avoid; margin-bottom: 14px; border: 1px solid #bfdbfe; border-left: 5px solid #2563eb; border-radius: 8px; padding: 12px 16px; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px;">
                <h3 style="font-size: 13.5px; font-weight: 800; color: #1e3a8a; margin: 0;">#{idx}. {sc['name']}</h3>
                <span style="font-size: 10px; font-weight: 700; color: #1d4ed8; background: #dbeafe; padding: 2px 8px; border-radius: 4px;">{sc['dept']}</span>
            </div>
            <div style="display: flex; gap: 15px; font-size: 10px; color: #475569; margin-bottom: 8px; background: #f8fafc; padding: 6px 10px; border-radius: 6px;">
                <div><b>💰 బడ్జెట్:</b> {sc['budget']}</div>
                <div><b>👥 లబ్ధిదారులు:</b> {sc['beneficiaries']}</div>
            </div>
            <ul style="margin: 0; padding-left: 18px;">
                {pts}
            </ul>
        </div>
        """

    ts_cards_html = ""
    for idx, sc in enumerate(TS_SCHEMES, 1):
        pts = "".join([f'<li style="margin-bottom: 6px; font-size: 11px; line-height: 1.5; color: #1e293b;">{p}</li>' for p in sc["details"]])
        ts_cards_html += f"""
        <div style="page-break-inside: avoid; margin-bottom: 14px; border: 1px solid #fed7aa; border-left: 5px solid #ea580c; border-radius: 8px; padding: 12px 16px; background: #ffffff; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
            <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 6px;">
                <h3 style="font-size: 13.5px; font-weight: 800; color: #9a3412; margin: 0;">#{idx}. {sc['name']}</h3>
                <span style="font-size: 10px; font-weight: 700; color: #c2410c; background: #ffedd5; padding: 2px 8px; border-radius: 4px;">{sc['dept']}</span>
            </div>
            <div style="display: flex; gap: 15px; font-size: 10px; color: #475569; margin-bottom: 8px; background: #f8fafc; padding: 6px 10px; border-radius: 6px;">
                <div><b>💰 బడ్జెట్:</b> {sc['budget']}</div>
                <div><b>👥 లబ్ధిదారులు:</b> {sc['beneficiaries']}</div>
            </div>
            <ul style="margin: 0; padding-left: 18px;">
                {pts}
            </ul>
        </div>
        """

    mcq_html = ""
    for idx, m in enumerate(SCHEME_MCQS, 1):
        opts_rendered = " &nbsp;&nbsp;|&nbsp;&nbsp; ".join(m["opts"])
        mcq_html += f"""
        <div style="page-break-inside: avoid; margin-bottom: 12px; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; background: #f8fafc;">
            <div style="font-size: 11px; font-weight: 800; color: #0f172a; margin-bottom: 5px;">Q{idx}. {m['q']}</div>
            <div style="font-size: 10.5px; color: #334155; margin-bottom: 5px; font-weight: 600;">{opts_rendered}</div>
            <div style="font-size: 10.5px; color: #047857; font-weight: 800; margin-bottom: 3px;">✓ సరైన జవాబు: {m['ans']}</div>
            <div style="font-size: 10px; color: #475569; line-height: 1.4;"><b>వివరణ:</b> {m['exp']}</div>
        </div>
        """

    html = f"""<!DOCTYPE html>
<html lang="te">
<head>
  <meta charset="UTF-8">
  <title>ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రభుత్వ పథకాలు 2026 మాస్టర్ గైడ్</title>
  <style>
    @page {{
      size: A4 portrait;
      margin: 12mm 12mm 12mm 12mm;
      @bottom-right {{ content: "పేజీ " counter(page); font-size: 9px; color: #94a3b8; }}
      @bottom-left {{ content: "లక్ష్య APPSC / TSPSC స్టడీ మెటీరియల్ 2026"; font-size: 9px; color: #94a3b8; }}
    }}
    body {{
      font-family: 'Nirmala UI', 'Segoe UI', sans-serif;
      color: #0f172a;
      background: #ffffff;
      margin: 0;
      padding: 0;
      -webkit-print-color-adjust: exact;
      print-color-adjust: exact;
    }}
    .header-box {{
      background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
      color: white;
      padding: 20px;
      border-radius: 12px;
      text-align: center;
      margin-bottom: 20px;
      border-bottom: 4px solid #f59e0b;
    }}
    .sec-title {{
      font-size: 14.5px;
      font-weight: 900;
      padding: 6px 12px;
      border-radius: 6px;
      margin: 22px 0 12px 0;
    }}
  </style>
</head>
<body>

  <!-- Cover Header -->
  <div class="header-box">
    <div style="font-size: 10px; font-weight: 800; color: #fde68a; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 4px;">
      లక్ష్య APPSC / TSPSC 2026 ప్రత్యేకం • సమగ్ర డిజిటల్ రిఫరెన్స్
    </div>
    <h1 style="font-size: 20px; font-weight: 900; margin: 0 0 6px 0;">
      🎯 ఆంధ్రప్రదేశ్ & తెలంగాణ ప్రభుత్వ సంక్షేమ పథకాలు 2026
    </h1>
    <p style="font-size: 11px; margin: 0; color: #cbd5e1; line-height: 1.4;">
      సూపర్ సిక్స్ పథకాలు, ఆరు గ్యారెంటీలు, పారిశ్రామిక విధానాలు, బడ్జెట్ కేటాయింపులు, అర్హతలు & 30 మోడల్ ప్రాక్టీస్ ప్రశ్నలు
    </p>
  </div>

  <!-- AP Section -->
  <div class="sec-title" style="background: #eff6ff; color: #1e3a8a; border-left: 5px solid #2563eb;">
    🏛️ విభాగం 1: ఆంధ్రప్రదేశ్ సూపర్ సిక్స్ & నూతన సంక్షేమ పథకాలు (AP Flagship Schemes 2026)
  </div>
  {ap_cards_html}

  <!-- TS Section -->
  <div class="sec-title" style="background: #fff7ed; color: #9a3412; border-left: 5px solid #ea580c; page-break-before: always;">
    🌾 విభాగం 2: తెలంగాణ ఆరు గ్యారెంటీలు & ప్రజా పాలన పథకాలు (TS 6 Guarantees & Praja Palana)
  </div>
  {ts_cards_html}

  <!-- Practice MCQs -->
  <div class="sec-title" style="background: #f0fdf4; color: #166534; border-left: 5px solid #16a34a; page-break-before: always;">
    📝 విభాగం 3: పోటీ పరీక్షల ప్రాక్టీస్ మల్టిపుల్ ఛాయిస్ ప్రశ్నలు & వివరణలు (Practice MCQs)
  </div>
  {mcq_html}

  <!-- Footer -->
  <div style="text-align: center; margin-top: 25px; padding-top: 15px; border-top: 1px solid #cbd5e1; font-size: 9.5px; color: #64748b;">
    © 2026 లక్ష్య డైలీ కరెంట్ అఫైర్స్ & ప్రిపరేషన్ పోర్టల్ | వెబ్ పోర్టల్: https://lakshya-telugu-ca.onrender.com | టెలిగ్రామ్: @venkat_telugu_ca_bot
  </div>

</body>
</html>"""

    temp_html = os.path.join(base_dir, "backend", "temp_schemes.html")
    with open(temp_html, "w", encoding="utf-8") as f:
        f.write(html)

    browser = get_browser()
    if not browser:
        print("ERROR: No suitable browser executable found.")
        return None

    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={pdf_out}",
        temp_html
    ]

    print("Generating AP & TS Schemes Master Guide PDF...")
    subprocess.run(cmd, capture_output=True, text=True)

    if os.path.exists(temp_html):
        try:
            os.remove(temp_html)
        except Exception:
            pass

    if os.path.exists(pdf_out) and os.path.getsize(pdf_out) > 1000:
        mb = os.path.getsize(pdf_out) / (1024 * 1024)
        print(f"SUCCESS: Generated Schemes Master PDF at {pdf_out} ({mb:.2f} MB)")
        return pdf_out
    else:
        print("FAILED to generate Schemes Master PDF.")
        return None

if __name__ == "__main__":
    generate_schemes_handbook()
