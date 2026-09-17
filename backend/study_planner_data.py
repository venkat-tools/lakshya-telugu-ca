# -*- coding: utf-8 -*-
"""
60-Day Smart Daily Study Planner & Syllabus Tracker Data for APPSC Group 1, Group 2 & TSPSC.
Organized into 9 structured weeks covering History, Geography, Indian Society, Mental Ability & Current Affairs.
"""

def get_study_planner_data():
    days = []

    # Week 1 & 2: History (Day 1 - 12)
    hist_topics = [
        ("ప్రాచీన భారతదేశం: సింధు నాగరికత & వేద సంస్కృతి", "హరప్పా, మొహంజొదారో పట్టణ ప్రణాళిక, ఋగ్వేద, మలివేద కాలాల సమాజం & మతం", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("జైన, బౌద్ధ మతాల ఆవిర్భావం & షోడశ మహాజనపదాలు", "వర్ధమాన మహావీరుడు, గౌతమ బుద్ధుడు, తత్వశాస్త్రం, 4 బౌద్ధ సంగీతులు, 16 మహాజనపదాలు", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("మౌర్య సామ్రాజ్యం & అశోకుని ధర్మం", "చంద్రగుప్త మౌర్యుడు, చాణక్యుని అర్థశాస్త్రం, మెగస్తనీస్ ఇండికా, అశోకుని శిలాశాసనాలు", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("గుప్తుల స్వర్ణయుగం & హర్షవర్ధనుడు", "సముద్రగుప్తుడు, చంద్రగుప్త II, నవరత్నాలు, విజ్ఞానశాస్త్రం, కళలు, నలంద విశ్వవిద్యాలయం", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("ఆంధ్రుల ప్రాచీన చరిత్ర: శాతవాహనుల యుగం", "శ్రీముఖుడు, గౌతమీపుత్ర శాతకర్ణి, నాసిక్ శాసనం, హాలుని గాథాసప్తశతి, అమరావతి శిల్పకళ", "/appsc_syllabus#history", "/aphistory"),
        ("ఇక్ష్వాకులు, బృహత్పలాయనులు, సాలంకాయనులు & విష్ణుకుండినులు", "నాగార్జునకొండ శాసనాలు, వీరపురుషదత్తుడు, ఉండవల్లి గుహలు, ఇంద్రవర్మ", "/appsc_syllabus#history", "/aphistory"),
        ("మధ్యయుగ ఆంధ్ర: తూర్పు చాళుక్యులు & కాకతీయులు", "రాజరాజ నరేంద్రుడు, నన్నయ భారతం, కాకతీయ రుద్రమదేవి, ప్రతాపరుద్రుడు, మోటుపల్లి అభయ శాసనం", "/appsc_syllabus#history", "/aphistory"),
        ("రెడ్డిరాజులు & విజయనగర సామ్రాజ్య వైభవం", "శ్రీకృష్ణదేవరాయలు, అముక్తమాల్యద, అష్టదిగ్గజాలు, హంపి కట్టడాలు, తాళికోట యుద్ధం (1565)", "/appsc_syllabus#history", "/aphistory"),
        ("మధ్యయుగ భారతదేశం: ఢిల్లీ సుల్తానులు & మొఘల్ సామ్రాజ్యం", "ఇల్తుత్‌మిష్, అల్లావుద్దీన్ ఖిల్జీ మార్కెట్ సంస్కరణలు, అక్బర్ మత విధానం (దీన్-ఇ-ఇలాహి)", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("ఆధునిక భారతదేశం: యూరోపియన్ల రాక & 1857 తిరుగుబాటు", "బ్రిటిష్ ఈస్ట్ ఇండియా కంపెనీ, ప్లాసీ (1757), బక్సార్ (1764), 1857 ప్రథమ స్వాతంత్ర్య సంగ్రామం", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("భారత జాతీయోద్యమం: గాంధీ శకం (1915-1947)", "సహాయ నిరాకరణ, శాసనోల్లంఘన (దండి మార్చ్), క్విట్ ఇండియా ఉద్యమం, క్యాబినెట్ మిషన్", "/appsc_syllabus#history", "/subject_tests?subject=history"),
        ("ఆంధ్రోద్యమం, పొట్టి శ్రీరాములు బలిదానం & 2014 AP విభజన చట్టం", "ఆంధ్రరాష్ట్రం (1953), విశాలాంధ్ర (1956), AP పునర్విభజన చట్టం 2014 (12 భాగాలు, 108 సెక్షన్లు)", "/ap_bifurcation_guide", "/daily_live_test")
    ]
    for i, (title, points, mat_link, test_link) in enumerate(hist_topics, 1):
        days.append({
            "day": i,
            "week": (i - 1) // 7 + 1,
            "subject": "భారత & AP చరిత్ర",
            "icon": "fa-landmark",
            "color": "amber",
            "title": title,
            "points": points,
            "mat_link": mat_link,
            "test_link": test_link
        })

    # Week 3 & 4: Geography & Disaster Management (Day 13 - 24)
    geo_topics = [
        ("జనరల్ & ఫిజికల్ జాగ్రఫీ: భూగోళ నిర్మాణం & విపత్తులు", "భూఅంతర్భాగ నిర్మాణం (Crust, Mantle, Core), డిస్‌కంటిన్యూటీలు, భూకంపాలు, అగ్నిపర్వతాలు", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("భూస్వరూపాలు & శీతోష్ణస్థితి శాస్త్రం (Climatology)", "వాతావరణ పొరలు (Troposphere, Stratosphere), పీడన పట్టీలు, పవనాలు, సైక్లోన్లు", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("భారతదేశ భౌతిక స్వరూపాలు: హిమాలయాలు & ద్వీపకల్ప పీఠభూమి", "గ్రేటర్, లెస్సర్ హిమాలయాలు, శివాలిక్ శ్రేణులు, పశ్చిమ & తూర్పు కనుమలు, తీర మైదానాలు", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("భారత నదీ వ్యవస్థ: గంగ, సింధు, బ్రహ్మపుత్ర & ద్వీపకల్ప నదులు", "నదుల జన్మస్థానాలు, ఉపనదులు, జాతీయ జలమార్గాలు, కీలక బహుళార్థసాధక ప్రాజెక్టులు", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("భారత శీతోష్ణస్థితి, ఋతుపవనాలు & అడవులు (ISFR 2023)", "నైరుతి, ఈశాన్య ఋతుపవనాలు, ఎల్-నినో/లా-నినా, అటవీ విస్తీర్ణం, మధ్యప్రదేశ్ ప్రథమ స్థానం", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("భారత వ్యవసాయం, పంటలు & కీలక ఖనిజ వనరులు", "ఖరీఫ్, రబీ, జాయెద్, ఆహార & వాణిజ్య పంటలు, ఇనుము, బొగ్గు, మైకా, బాక్సైట్ క్షేత్రాలు", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("ఆంధ్రప్రదేశ్ భౌగోళిక స్వరూపం, తీరరేఖ & కొండలు", "974 కి.మీ తీరరేఖ (రెండవ అతిపొడవైనది), తూర్పు కనుమలు, అరోమా కొండ (ఎత్తైన శిఖరం), శేషాచలం", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("ఆంధ్రప్రదేశ్ నదీ వ్యవస్థ: గోదావరి, కృష్ణా, పెన్నా & పోలవరం", "ధవళేశ్వరం బ్యారేజ్, ప్రకాశం బ్యారేజ్, పోలవరం జాతీయ ప్రాజెక్ట్ విశేషాలు, అంతర్రాష్ట్ర జలవివాదాలు", "/appsc_syllabus#geo", "/subject_tests?subject=geography"),
        ("ఆంధ్రప్రదేశ్ 26 నూతన జిల్లాలు: సమగ్ర అట్లాస్", "26 జిల్లాల సరిహద్దులు, కేంద్రాలు, సహజ వనరులు, పోర్టులు, పరిశ్రమలు, జియోగ్రాఫికల్ ఇండికేటర్లు", "/districts_atlas", "/subject_tests?subject=geography"),
        ("విపత్తు నిర్వహణ: చట్టం 2005, సెండాయ్ ఫ్రేమ్‌వర్క్", "NDMA, SDMA, DDMA నిర్మాణం, సెండాయ్ 4 ప్రాధాన్యతలు, తుఫానులు, కరువుల నివారణ", "/appsc_syllabus#disaster", "/subject_tests?subject=disaster"),
        ("పర్యావరణం, 85 రామ్‌సార్ సైట్లు & ప్రాజెక్ట్ టైగర్/చీతా", "బాకూ COP29, కున్మింగ్ 30x30, కొల్లేరు సరస్సు, 3,682 పులులు, కునో నేషనల్ పార్క్", "/environment_hub", "/subject_tests?subject=disaster"),
        ("జాగ్రఫీ & పర్యావరణ సమగ్ర రివిజన్ టెస్ట్", "భౌగోళికం & విపత్తు నిర్వహణ 50 ప్రాక్టీస్ ప్రశ్నల మాక్ టెస్ట్ సాధన", "/subject_tests?subject=geography", "/daily_live_test")
    ]
    for i, (title, points, mat_link, test_link) in enumerate(geo_topics, 13):
        days.append({
            "day": i,
            "week": (i - 1) // 7 + 1,
            "subject": "భౌగోళికం & పర్యావరణం",
            "icon": "fa-earth-asia",
            "color": "teal",
            "title": title,
            "points": points,
            "mat_link": mat_link,
            "test_link": test_link
        })

    # Week 5 & 6: Indian Society & Welfare (Day 25 - 36)
    soc_topics = [
        ("భారతీయ సమాజం: కుటుంబం & వివాహ వ్యవస్థలు", "ఉమ్మడి vs వ్యష్టి కుటుంబం, అంతర్వివాహం vs బహిర్వివాహం, హిందూ వివాహ చట్టం 1955", "/indian_society_hub#unit_1", "/subject_tests?subject=society"),
        ("బంధుత్వ వ్యవస్థ & కుల వ్యవస్థ సిద్ధాంతాలు", "రక్తసంబంధ vs వైవాహిక బంధుత్వం, ఉత్తర vs దక్షిణ భారత బంధుత్వం (ఇరావతి కార్వే), కుల సిద్ధాంతాలు", "/indian_society_hub#unit_1", "/subject_tests?subject=society"),
        ("సంస్కృతీకరణ (Sanskritization) & ఆధిపత్య కులం", "ఎం.ఎన్. శ్రీనివాస్ సిద్ధాంతాలు, సమాజంలో స్థాన మార్పు vs నిర్మాణ మార్పు, కుల సమీకరణాలు", "/indian_society_hub#unit_1", "/subject_tests?subject=society"),
        ("భారతదేశంలో తెగలు & 75 PVTGs సమగ్ర సమాచారం", "ఆర్టికల్ 342, దేబర్ కమిషన్, ఒడిశా (13 PVTGs), ఆంధ్రప్రదేశ్‌లోని 7 PVTGs (చెంచులు, కొండరెడ్డిలు)", "/indian_society_hub#unit_1", "/subject_tests?subject=society"),
        ("మహిళల స్థితిగతులు, చారిత్రక మార్పులు & 106వ సవరణ", "వేద కాలం నుండి ఆధునిక సంస్కరణలు, కందుకూరి, స్థానిక సంస్థల్లో 50%, నారీ శక్తి వందన్ 33%", "/indian_society_hub#unit_1", "/subject_tests?subject=society"),
        ("సామాజిక సమస్యలు: కులతత్వం, మతతత్వం & ప్రాంతీయతత్వం", "ఓటు బ్యాంకు రాజకీయాలు, బిపిన్ చంద్ర 3 దశలు, భూమిపుత్రుల సిద్ధాంతం (Sons of Soil)", "/indian_society_hub#unit_2", "/subject_tests?subject=society"),
        ("పేదరికం & నిరుద్యోగం: టెండూల్కర్, రంగరాజన్ & MPI సూచీ", "నిరపేక్ష vs సాపేక్ష పేదరికం, నీతి ఆయోగ్ బహుమితీయ పేదరిక సూచీ 12 సూచీలు, ప్రచ్ఛన్న నిరుద్యోగం", "/indian_society_hub#unit_2", "/subject_tests?subject=society"),
        ("మహిళలు & బాలల సమస్యలు: చట్టపరమైన రక్షణలు", "బాల్యవివాహాల చట్టం 2006, వరకట్న నిషేధం 1961, గృహహింస చట్టం 2005, POCSO 2012, బాలకార్మిక చట్టం", "/indian_society_hub#unit_2", "/subject_tests?subject=society"),
        ("బలహీన వర్గాల రాజ్యాంగ రక్షణలు (Articles 15, 16, 17, 330, 332)", "ప్రాథమిక హక్కులు, ఆదేశిక సూత్రాలు (46), విద్యా ఉద్యోగ రిజర్వేషన్లు, రాజకీయ రిజర్వేషన్లు", "/indian_society_hub#unit_3", "/polity_articles"),
        ("చట్టబద్ధ రక్షణలు: SC/ST అత్యాచారాల చట్టం 1989 & PESA 1996", "సెక్షన్ 18A సవరణ, 5వ షెడ్యూల్ గ్రామసభ అధికారాలు, అటవీ హక్కుల గుర్తింపు చట్టం FRA 2006", "/indian_society_hub#unit_3", "/subject_tests?subject=society"),
        ("జాతీయ కమిషన్లు: NCSC, NCST, NCBC (102వ సవరణ) & పథకాలు", "ఆర్టికల్స్ 338, 338A, 338B, మహిళా & బాలల కమిషన్లు, పీఎం జన్-మన్ (PM-JANMAN), స్మైల్", "/indian_society_hub#unit_3", "/central_schemes"),
        ("భారతీయ సమాజం 50 ప్రశ్నల మెగా ప్రాక్టీస్ టెస్ట్", "సమాజం 3 యూనిట్ల సమగ్ర ప్రశ్నల సాధన & టైమ్డ్ టెస్ట్", "/subject_tests?subject=society", "/daily_live_test")
    ]
    for i, (title, points, mat_link, test_link) in enumerate(soc_topics, 25):
        days.append({
            "day": i,
            "week": (i - 1) // 7 + 1,
            "subject": "భారతీయ సమాజం",
            "icon": "fa-users-line",
            "color": "indigo",
            "title": title,
            "points": points,
            "mat_link": mat_link,
            "test_link": test_link
        })

    # Week 7 & 8: Mental Ability & Reasoning (Day 37 - 48)
    math_topics = [
        ("లాజికల్ రీజనింగ్: నంబర్ సిరీస్ & లెటర్ సిరీస్", "మిస్సింగ్ నంబర్స్, ప్రైమ్ నంబర్ ప్యాటర్న్స్, క్యూబ్/స్క్వేర్ తేడాలు, ఆల్ఫాబెట్ పొజిషన్లు", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("కోడింగ్ - డీకోడింగ్ & ఆడ్ వన్ ఔట్ (Odd One Out)", "లెటర్ షిఫ్టింగ్, రివర్స్ కోడింగ్, నంబర్-సింబల్ కోడింగ్, విభిన్న పదం గుర్తింపు", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("రక్త సంబంధాలు (Blood Relations) & పజిల్స్", "ఫ్యామిలీ ట్రీ డ్రాయింగ్ టెక్నిక్, పాయింటింగ్ టువర్డ్స్ పర్సన్ టైప్స్, కోడెడ్ రిలేషన్స్", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("దిశలు (Direction Sense Test) & కోణాలు", "పైథాగరస్ సిద్ధాంతం ద్వారా కనిష్ట దూరం, సూర్యోదయం/సూర్యాస్తమయం నీడ సమస్యలు", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("సిలాజిజమ్ (Syllogism) & వెన్ చిత్రాలు", "All, Some, No నిబంధనలు, వెన్ డయాగ్రామ్ పద్ధతి, కంక్లూజన్స్ నిర్ధారణ షార్ట్‌కట్స్", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("గడియారాలు (Clocks): కోణాలు & రిఫ్లెక్స్ కోణాలు", "ముల్లుల మధ్య కోణం సూత్రం |30H - 11/2 M|, ఏకీభవించే సమయం, లంబంగా ఉండే సమయం", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("క్యాలెండర్స్ (Calendars): ఆడ్ డేస్ షార్ట్‌కట్ పద్ధతి", "లీపు సంవత్సరాలు, శతాబ్దపు ఆడ్ డేస్, ఏదైనా తేదీ ఇచ్చినప్పుడు వారం రోజును కనుగొనడం", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("శాతాలు (Percentages) & లాభనష్టాలు (Profit & Loss)", "ఫ్రాక్షన్ టు పర్సంటేజ్ టేబుల్, డిస్కౌంట్లు, గుర్తించిన వెల (MP), కాస్ట్ ప్రైస్ షార్ట్‌కట్స్", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("నిష్పత్తులు & మిశ్రమాలు (Ratios & Allegations)", "కాంపౌండ్ రేషియో, పాలల్లో నీటి కల్తీ సమస్యలు, అలగేషన్ క్రాస్ పద్ధతి", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("పని - కాలం (Time & Work) & పైపులు - తొట్టెలు", "LCM ఎఫిషియన్సీ మెథడ్, మహిళలు-పురుషులు-పిల్లల పని సామర్థ్యం, లీకేజ్ సమస్యలు", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("వేగం, కాలం & దూరం: రైళ్లు, పడవలు - ప్రవాహాలు", "కి.మీ/గం నుండి మీ/సె (5/18), ఎదురెదురుగా & ఒకే దిశలో సాపేక్ష వేగం (Relative Speed)", "/mental_ability_hub", "/subject_tests?subject=mental_ability"),
        ("డాటా ఇంటర్‌ప్రిటేషన్ (DI) & మెన్సురేషన్ 2D/3D", "పై చార్టులు, బార్ గ్రాఫ్‌లు, టేబుల్స్, వృత్తం, చతురస్రం, శంఖువు, స్థూపం ఫార్ములాలు", "/mental_ability_hub", "/subject_tests?subject=mental_ability")
    ]
    for i, (title, points, mat_link, test_link) in enumerate(math_topics, 37):
        days.append({
            "day": i,
            "week": (i - 1) // 7 + 1,
            "subject": "మెంటల్ ఎబిలిటీ",
            "icon": "fa-calculator",
            "color": "blue",
            "title": title,
            "points": points,
            "mat_link": mat_link,
            "test_link": test_link
        })

    # Week 9: Current Affairs Revision & Grand Mocks (Day 49 - 60)
    ca_topics = [
        ("జాతీయ & అంతర్జాతీయ కరెంట్ అఫైర్స్ మెగా రివిజన్", "గత 6 నెలల అంతర్జాతీయ సదస్సులు, దేశాల అధినేతల పర్యటనలు, ద్వైపాక్షిక ఒప్పందాలు", "/", "/weekly_digest"),
        ("ఆంధ్రప్రదేశ్ కరెంట్ అఫైర్స్ & నూతన పాలసీలు 4.0", "AP ఇండస్ట్రియల్ పాలసీ 4.0, MSME 2030, డ్రోన్ పాలసీ, రాజధాని అమరావతి ప్రాజెక్టులు", "/appsc_syllabus#policies", "/daily_live_test"),
        ("కేంద్ర ప్రభుత్వ ఫ్లాగ్‌షిప్ పథకాలు 2026 రివిజన్", "పీఎం సూర్య ఘర్, ఆయుష్మాన్ 70+, పీఎం విశ్వకర్మ, లఖ్‌పతీ దీదీ, పీఎం ఇంటర్న్‌షిప్", "/central_schemes", "/subject_tests?subject=society"),
        ("ఆంధ్రప్రదేశ్ సూపర్ సిక్స్ & సంక్షేమ పథకాల మేట్రిక్స్", "తల్లికి వందనం, దీపం-2, అన్నదాత సుఖీభవ, యువగళం నిధి అర్హతలు & బడ్జెట్", "/schemes_matrix", "/subject_tests?subject=society"),
        ("కేంద్ర & ఏపీ బడ్జెట్, ఎకనామిక్ సర్వే 2026", "జీడీపీ వృద్ధి రేటు, తలసరి ఆదాయం, ద్రవ్య లోటు, వ్యవసాయ రంగ కేటాయింపులు", "/appsc_syllabus#economy", "/daily_live_test"),
        ("సైన్స్, టెక్నాలజీ & రక్షణ రంగం లేటెస్ట్ డెవలప్‌మెంట్స్", "గగన్‌యాన్, అగ్ని-5 MIRV, సెమీకండక్టర్లు, ఇండియాఏఐ మిషన్, క్వాంటం మిషన్", "/science_tech_hub", "/subject_tests?subject=disaster"),
        ("పర్యావరణం, రామ్‌సార్ సైట్లు & వాతావరణ మార్పులు", "బాకూ COP29, 85 రామ్‌సార్ చిత్తడి నేలలు, గ్రేట్ ఇండియన్ బస్టర్డ్ తీర్పు, పులుల గణన", "/environment_hub", "/subject_tests?subject=disaster"),
        ("APPSC & TSPSC గత ప్రశ్నల (PYQs) సమగ్ర అనలిటిక్స్", "2024 గ్రూప్-2 ప్రిలిమ్స్, 2019 స్క్రీనింగ్ టెస్ట్ కటాఫ్ అనాలిసిస్ & ట్రికీ క్వశ్చన్స్", "/pyqs_explorer", "/daily_live_test"),
        ("ఫుల్ లెంగ్త్ గ్రాండ్ మాక్ టెస్ట్ 1 (150 మార్కులు - నెగెటివ్ మార్కింగ్)", "చరిత్ర (30), భౌగోళికం (30), సమాజం (30), మెంటల్ ఎబిలిటీ (30), CA (30)", "/daily_live_test", "/daily_live_test"),
        ("ఫుల్ లెంగ్త్ గ్రాండ్ మాక్ టెస్ట్ 2 (150 మార్కులు)", "టైమ్డ్ ఎగ్జామ్ మోడ్, తప్పుల సమీక్ష, ఆన్సర్ కీ విశ్లేషణ", "/daily_live_test", "/daily_live_test"),
        ("చివరి నిమిషం షార్ట్ నోట్స్ & వన్-లైనర్స్ ఫాస్ట్ రివిజన్", "500+ వన్ లైనర్స్, ముఖ్యమైన తేదీలు, వ్యక్తులు, అవార్డులు, స్పోర్ట్స్ ముఖ్యాంశాలు", "/", "/daily_live_test"),
        ("పరీక్షా హాల్ వ్యూహం, టైమ్ మేనేజ్మెంట్ & తుది రివిజన్", "-0.33 నెగెటివ్ మార్కింగ్ నియంత్రణ, ఎలిమినేషన్ పద్ధతి, ప్రశాంతమైన మానసిక సంసిద్ధత", "/appsc_syllabus", "/daily_live_test")
    ]
    for i, (title, points, mat_link, test_link) in enumerate(ca_topics, 49):
        days.append({
            "day": i,
            "week": (i - 1) // 7 + 1,
            "subject": "కరెంట్ అఫైర్స్ & మాక్ టెస్ట్స్",
            "icon": "fa-newspaper",
            "color": "rose",
            "title": title,
            "points": points,
            "mat_link": mat_link,
            "test_link": test_link
        })

    return {
        "title": "60 రోజుల స్మార్ట్ డైలీ స్టడీ ప్లానర్ & సిలబస్ ట్రాకర్ (2026)",
        "subtitle": "APPSC గ్రూప్-1, గ్రూప్-2 & TSPSC ప్రిలిమ్స్ సంపూర్ణ క్యాలెండర్ & ప్రోగ్రెస్ డ్యాష్‌బోర్డ్",
        "total_days": 60,
        "total_weeks": 9,
        "days": days
    }
