# Chapters 5-8 — the experiments, the loopholes, the Nobel, the communication limit.
CH = []

# ------------------------------------------------------------ 5. experiments
CH.append(dict(
    n=5, title="पहले प्रयोग", accent="gold", shots=[
        ("पहला असली परीक्षण उन्नीस सौ बहत्तर में हुआ। फ्रीडमैन और क्लॉज़र ने किया।",
         "1972|Freedman aur Clauser", "card", dict(n="5", title="1972", sub="THE FIRST TEST")),
        ("उन्होंने कैल्शियम के परमाणुओं से जोड़ी बनाई और दोनों तरफ़ नापी।",
         "Calcium se jodi|dono taraf naapi", "rig", dict(left="A", right="B")),
        ("डेटा जुटाने में करीब दो सौ घंटे लगे।",
         "Data jutmne mein|do sau ghante", "quote", dict(line="200 HOURS OF DATA")),
        ("नतीजा सीमा के पार था। क्वांटम सही निकला।",
         "Nateeja limit ke paar|quantum sahi", "chart", dict(limit=2.0, peak=2.83, measured=2.4)),
        ("लेकिन एक छेद बचा। सेटिंग पहले से तय थी, तो कणों को पता हो सकता था।",
         "Ek chhed bacha|setting pehle se tay thi", "board",
         dict(title="THE LOCALITY HOLE", lines=["settings were fixed in advance", "the pair could 'know' the question"])),
        ("उन्नीस सौ बयासी में ऐस्पे ने ये छेद बंद किया।",
         "1982|Aspect ne chhed band kiya", "card", dict(n="6", title="1982", sub="ASPECT")),
        ("उन्होंने सेटिंग उसके बाद बदली, जब जोड़ी स्रोत से निकल चुकी थी।",
         "Setting baad mein badli|jodi nikal chuki thi", "rig", dict(left="switch", right="switch")),
        ("दूरी छह मीटर, वक़्त बीस नैनोसेकंड। इतने में ही सेटिंग बदलनी थी।",
         "Chhe meter|bees nanosecond", "quote", dict(line="6 m  ·  20 ns")),
        ("नतीजा वही निकला। क्वांटम जीता, स्थानीय सिद्धांत हारा।",
         "Wahi nateeja|local theory haari", "board",
         dict(title="THE RESULT", lines=["violation confirmed", "local explanation excluded"])),
        ("लेकिन एक और छेद बचा था। वो छेद और भी शातिर था।",
         "Ek aur chhed|aur bhi shatir", "card", dict(n="7", title="छेद", sub="THE LOOPHOLES")),
    ]))

# --------------------------------------------------------------- 6. loopholes
CH.append(dict(
    n=6, title="तीन छेद", accent="magenta", shots=[
        ("तीन बड़े छेद थे। हर एक को बंद करना ज़रूरी था।",
         "Teen bade chhed|sab band karna zaroori", "three",
         dict(items=["LOCALITY", "DETECTION", "FREE CHOICE"], note="three loopholes")),
        ("पहला: सेटिंग बाद में बदलनी चाहिए, वरना कणों को पता हो सकता है।",
         "Pehla|setting baad mein badle", "board",
         dict(title="LOCALITY", lines=["switch after the pair leaves", "no time for a signal"])),
        ("दूसरा: हर फोटॉन पकड़ा नहीं जाता। तो नमूना पूरा नहीं होता।",
         "Doosra|har photon pakda nahi jaata", "rig", dict(left="few", right="few")),
        ("अगर सौ में से दो ही पकड़े जाएँ, तो नतीजा भरोसे के लायक नहीं।",
         "Sau mein do|nateeja bharose ka nahi", "quote", dict(line="THE DETECTION HOLE")),
        ("तीसरा: सेटिंग चुनने वाला खुद प्रभावित हो सकता है। इसे फ्री चॉइस छेद कहते हैं।",
         "Teesra|setting chunne wala prabhavit ho sakta hai", "board",
         dict(title="FREE CHOICE", lines=["who picks the setting?", "could anything bias it?"])),
        ("दो हज़ार पंद्रह में पहली बार बड़े छेद एक साथ बंद हुए।",
         "2015|bade chhed ek saath band", "timeline",
         dict(years=[("1972", "Freedman"), ("1982", "Aspect"), ("2015", "loophole-free")], at=2)),
        ("उस परीक्षण में सीमा टूटी, और कोई आसान बचाव नहीं बचा।",
         "Limit tooti|koi bachav nahi bacha", "chart", dict(limit=2.0, peak=2.83, measured=2.4)),
        ("आज तक हर बड़ा परीक्षण वही कहता है।",
         "Aaj tak har bada test|wahi kehta hai", "quote", dict(line="THE SAME ANSWER, EVERY TIME")),
        ("इसीलिए ये अब बहस नहीं, माप है।",
         "Ab bahas nahi|maap hai", "board",
         dict(title="NOT A DEBATE", lines=["a measured violation", "repeated across labs"])),
        ("इस काम को दो हज़ार बाईस में नोबेल मिला।",
         "2022 mein Nobel", "card", dict(n="8", title="नोबेल", sub="2022")),
    ]))

# ------------------------------------------------------------------ 7. Nobel
CH.append(dict(
    n=7, title="नोबेल, दो हज़ार बाईस", accent="gold", shots=[
        ("दो हज़ार बाईस। भौतिकी का नोबेल तीन लोगों को मिला।",
         "2022|teen logon ko Nobel", "card", dict(n="9", title="2022", sub="NOBEL PRIZE")),
        ("क्लॉज़र, ऐस्पे और ज़ाइलिंगर।",
         "Clauser · Aspect · Zeilinger", "three",
         dict(items=["CLAUSER", "ASPECT", "ZEILINGER"], note="2022")),
        ("क्लॉज़र ने पहला व्यावहारिक परीक्षण बनाया।",
         "Clauser|pehla practical test", "quote", dict(line="THE FIRST TEST")),
        ("ऐस्पे ने सेटिंग का छेद बंद किया।",
         "Aspect|setting ka chhed band", "quote", dict(line="THE SETTING SWITCH")),
        ("ज़ाइलिंगर ने टेलीपोर्टेशन और क्वांटम नेटवर्क की राह खोली।",
         "Zeilinger|teleportation aur network", "quote", dict(line="TELEPORTATION")),
        ("पर ध्यान रखें: नोबेल प्रयोगों के लिए था, किसी नई मशीन के लिए नहीं।",
         "Nobel prayogon ke liye|machine ke liye nahi", "board",
         dict(title="WHAT IT HONOURED", lines=["the experiments", "not a product"])),
        ("और क्लॉज़र के बाद भी छेद बचे थे। इतिहास एक दिन में पूरा नहीं हुआ।",
         "Clauser ke baad bhi chhed|ek din mein nahi", "timeline",
         dict(years=[("1972", "first test"), ("1982", "locality"), ("2015", "all loopholes")], at=0)),
        ("अब सबसे ज़रूरी बात, जो अक्सर ग़लत बताई जाती है।",
         "Sabse zaroori baat|aksar galat bataayi jaati hai", "card", dict(n="10", title="संदेश नहीं", sub="NO MESSAGE")),
    ]))

# ------------------------------------------------------- 8. no communication
CH.append(dict(
    n=8, title="संदेश नहीं जाता", accent="red", shots=[
        ("एंटैंगलमेंट से आप एक बिट भी नहीं भेज सकते। ये सबसे ज़रूरी बात है।",
         "Ek bit bhi nahi|sabse zaroori baat", "quote", dict(line="NOT ONE BIT")),
        ("बॉब अपने कण पर कुछ नहीं देखता। उसका नतीजा बेतरतीब लगता है।",
         "Bob ko kuch nahi dikhta|nateeja random", "channel", dict(left="ALICE", right="BOB", note="noise")),
        ("वो नहीं जान सकता कि ऐलिस ने नापा भी या नहीं।",
         "Pata nahi chalta|naapa ya nahi", "board",
         dict(title="BOB SEES NOTHING", lines=["his results look random", "unchanged by her choice"])),
        ("जवाब जानने के लिए ऐलिस को अपना नतीजा भेजना पड़ता है। सामान्य चैनल से।",
         "Alice ko result bhejna padta hai|normal channel", "channel", dict(left="ALICE", right="BOB", note="classical")),
        ("तभी दोनों नतीजे मिलाकर देख सकते हैं।",
         "Tabhi milakar dekh sakte hain", "board",
         dict(title="COMPARE NOTES", lines=["two lists", "compared at light speed"])),
        ("यानी जानकारी रोशनी से तेज़ नहीं जाती।",
         "Jankari light se tez nahi", "quote", dict(line="NOT FASTER THAN LIGHT")),
        ("इसीलिए ये सापेक्षता से नहीं टकराता।",
         "Relativity se nahi takrata", "board",
         dict(title="NO CONFLICT", lines=["correlation is real", "no signal is sent"])),
        ("जुड़ाव असली है। संदेश नहीं।",
         "Judav asli hai|sandesh nahi", "quote", dict(line="REAL LINK, NO SIGNAL")),
        ("इस नियम का नाम है नो-कम्युनिकेशन।",
         "Naam hai no-communication", "formula", dict(eq="ρB = Tr A (ρAB)", note="Bob's state is unchanged")),
        ("फिर भी इस जुड़ाव से काम निकलता है। टेलीपोर्टेशन से शुरू करते हैं।",
         "Phir bhi kaam nikalta hai|teleportation", "card", dict(n="11", title="टेलीपोर्टेशन", sub="TELEPORTATION")),
    ]))
