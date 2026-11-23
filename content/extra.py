# Extra shots per chapter — the detail that turns an outline into a 15-minute film.
# Keyed by chapter number; each entry is (text, caption, template, props).

EXTRA = {}

EXTRA[1] = [
    ("जुड़ाव और सामान्य संबंध में फ़र्क़ है। दो घड़ियाँ भी एक साथ चल सकती हैं।",
     "Judav aur normal sambandh|do ghariyan bhi", "board",
     dict(title="NOT THE SAME", lines=["two clocks agree", "neither describes the other"])),
    ("घड़ियों की जानकारी अलग अलग है। जुड़े कणों की नहीं।",
     "Ghariyon ki jankari alag|jude kano ki nahi", "pair", dict(left="A", right="B", mid="no separate story")),
    ("इसे ऐसे समझिए: दो कमरे, एक ही ताले की दो चाबियाँ नहीं। एक ही चीज़, दो कमरों में।",
     "Ek hi cheez|do kamron mein", "quote", dict(line="ONE THING, TWO PLACES")),
    ("यही वजह है कि इसे सामान्य जानकारी से नहीं समझाया जा सकता।",
     "Normal jankari se nahi|samjhaya ja sakta", "board",
     dict(title="WHY IT IS ODD", lines=["not two things", "one description"])),
]

EXTRA[2] = [
    ("ऐसी चार मशहूर अवस्थाएँ हैं। इन्हें बेल अवस्थाएँ कहते हैं।",
     "Chaar mashhoor avasthayen|Bell states", "three",
     dict(items=["Φ+", "Φ−", "Ψ+", "Ψ−"], note="four Bell states")),
    ("ऐसी जोड़ी बनाने का आम तरीका है: एक फोटॉन को क्रिस्टल में तोड़ना।",
     "Jodi banane ka tareeka|crystal mein todna", "rig", dict(left="photon", right="pair")),
    ("इस प्रक्रिया को स्पॉन्टेनियस पैरामेट्रिक डाउन कन्वर्ज़न कहते हैं।",
     "SPDC|ek photon se do", "formula", dict(eq="1 photon → 2 photons", note="SPDC")),
    ("अब नाप की बात। कोण बदलो, तो जुड़ाव का पैटर्न भी बदलता है।",
     "Kon badlo|pattern badalta hai", "board",
     dict(title="THE ANGLE MATTERS", lines=["0° → perfect match", "45° → half the time", "90° → always opposite"])),
    ("यही पैटर्न बेल की सीमा और क्वांटम के फ़र्क़ को मापता है।",
     "Yahi pattern|seema aur quantum ka farq", "chart", dict(limit=2.0, peak=2.83, measured=None)),
]

EXTRA[3] = [
    ("EPR ने 'भौतिक वास्तविकता' की एक शर्त दी। अगर बिना छेड़े नतीजा पता चले, तो वो असली है।",
     "EPR ki shart|bina chhede nateeja pata chale", "quote", dict(line="A CRITERION OF REALITY")),
    ("उनका तर्क: दूर के कण का जवाब बिना छेड़े पता चल जाता है। तो वो पहले से तय होगा।",
     "Door ka jawab|pehle se tay hoga", "board",
     dict(title="THE ARGUMENT", lines=["predict without touching", "so it was decided already"])),
    ("इससे दो बातें निकलती हैं: स्थानीयता, और पहले से तय जवाब।",
     "Do baatein|locality aur pre-set values", "levels",
     dict(items=["LOCALITY", "REALISM"], note="EPR's two assumptions")),
    ("बोहर ने कहा कि दोनों कण एक ही अवस्था हैं, इसलिए सवाल ही ग़लत है।",
     "Bohr|dono ek hi avastha hain", "pair", dict(left="A", right="B", mid="one system")),
    ("लेकिन ये जवाब जाँचा नहीं जा सकता था। इसीलिए बहस अटक गई।",
     "Jawab jaancha nahi ja sakta|bahas atak gayi", "quote", dict(line="NO TEST, NO VERDICT")),
]

EXTRA[4] = [
    ("बेल ने चार सेटिंग चुनीं: दो ऐलिस के लिए, दो बॉब के लिए।",
     "Chaar setting|do Alice, do Bob", "rig", dict(left="a1 / a2", right="b1 / b2")),
    ("हर जोड़ी नापो, और चारों का एक जोड़ा हुआ अंक निकालो।",
     "Har jodi naapo|chaaron ka ek ank", "formula", dict(eq="S = E(a1,b1) + E(a1,b2) + E(a2,b1) − E(a2,b2)", note="CHSH")),
    ("स्थानीय सिद्धांत कहते हैं ये अंक दो से ज़्यादा नहीं हो सकता।",
     "S do se zyada nahi|local theory", "chart", dict(limit=2.0, peak=2.83, measured=None)),
    ("क्वांटम कहता है ये दो दशमलव आठ दो आठ तक जा सकता है।",
     "Quantum do dashamlav aath do aath", "chart", dict(limit=2.0, peak=2.83, measured=2.828)),
    ("इस ऊपरी सीमा को सिरेल्सन बाउंड कहते हैं। इससे ऊपर क्वांटम भी नहीं जा सकता।",
     "Tsirelson bound|isse upar quantum bhi nahi", "quote", dict(line="THE CEILING: 2√2")),
    ("बेल का काम यही था: बहस को एक अंक में बदल देना।",
     "Bahas ko ek ank mein|badal dena", "board",
     dict(title="THE MOVE", lines=["a philosophical dispute", "became a number"])),
]

EXTRA[5] = [
    ("फोटॉन की ध्रुवीकरण नापी जाती है। यानी उसका कोण।",
     "Photon ka polarization|uska kon", "board",
     dict(title="HOW IT IS MEASURED", lines=["polariser at an angle", "click or no click"])),
    ("दोनों तरफ़ के क्लिक मिलाकर गिने जाते हैं। इसे कोइन्सिडेंस कहते हैं।",
     "Dono taraf ke click|coincidence", "rig", dict(left="click", right="click")),
    ("उन्नीस सौ बहत्तर का नतीजा छह सिग्मा था। यानी साफ़, पर इतना बड़ा नहीं।",
     "1972 ka nateeja|chhe sigma", "quote", dict(line="SIX SIGMA")),
    ("उन्नीस सौ बयासी में ऐस्पे का नतीजा कई दर्जन सिग्मा दूर था।",
     "1982|darjan sigma door", "chart", dict(limit=2.0, peak=2.83, measured=2.6)),
    ("इसीलिए ऐस्पे का प्रयोग इतिहास में गिना जाता है।",
     "Isliye Aspect|itihas mein gina jaata hai", "quote", dict(line="THE CLEANEST RESULT")),
]

EXTRA[6] = [
    ("छेद का मतलब है: एक और कहानी बच सकती है जो नतीजा समझा दे।",
     "Chhed ka matlab|ek aur kahani bach sakti hai", "quote", dict(line="A HOLE IS AN ESCAPE ROUTE")),
    ("स्थानीयता का छेद: सेटिंग बदलने की खबर कण तक पहुँच सकती है।",
     "Locality ka chhed|khbar pahunch sakti hai", "board",
     dict(title="HOLE ONE", lines=["settings must change fast", "faster than light could tell"])),
    ("डिटेक्शन का छेद: जो पकड़े गए, वो सबके नुमाइंदे नहीं हो सकते।",
     "Detection ka chhed|numainde nahi ho sakte", "board",
     dict(title="HOLE TWO", lines=["most photons are lost", "the sample may be biased"])),
    ("दो हज़ार पंद्रह में तीन अलग प्रयोगों ने ये छेद बंद किए।",
     "2015|teen alag prayog", "three",
     dict(items=["DELFT", "NIST", "VIENNA"], note="2015")),
    ("तब से ये नतीजा और मज़बूत हुआ है, कमज़ोर नहीं।",
     "Nateeja mazboot hua|kamzor nahi", "chart", dict(limit=2.0, peak=2.83, measured=2.4)),
]

EXTRA[7] = [
    ("नोबेल का हवाला साफ़ था: जुड़े फोटॉनों के प्रयोग, और बेल की असमानता का उल्लंघन।",
     "Nobel ka hawaala|entangled photons, Bell violation", "quote", dict(line="THE CITATION")),
    ("साथ में ये भी लिखा था: क्वांटम सूचना विज्ञान की शुरुआत।",
     "Quantum information science|shuruaat", "board",
     dict(title="THE SECOND HALF", lines=["experiments", "and a new field"])),
    ("ज़ाइलिंगर के समूह ने टेलीपोर्टेशन दिखाया, और लंबी दूरी के नेटवर्क की नींव रखी।",
     "Zeilinger|teleportation aur network", "channel", dict(left="A", right="B", note="state moved")),
    ("लेकिन नोबेल किसी मशीन का सर्टिफिकेट नहीं है।",
     "Nobel machine ka certificate nahi", "quote", dict(line="NOT A PRODUCT AWARD")),
]

EXTRA[8] = [
    ("गणित में इसे ऐसे लिखते हैं: बॉब की अलग अवस्था वही रहती है।",
     "Bob ki alag avastha|wahi rehti hai", "formula", dict(eq="ρB = Tr A (ρAB)", note="unchanged by her measurement")),
    ("ऐलिस कुछ भी नापे, बॉब के आँकड़े वैसे ही रहते हैं।",
     "Alice kuch bhi naape|Bob ke aankde waise", "board",
     dict(title="THE INVARIANT", lines=["his statistics never change", "so nothing can be read"])),
    ("तभी दोनों अपनी सूचियाँ मिलाते हैं, और जुड़ाव दिखता है।",
     "Suchi milate hain|tab judav dikhta hai", "channel", dict(left="LIST", right="LIST", note="compared")),
    ("ये दो सूचियाँ मिलाना ही वो सामान्य कदम है जो ज़रूरी है।",
     "Do suchiyan milana|normal kadam", "quote", dict(line="TWO LISTS, ONE PHONE CALL")),
    ("इसीलिए कहा जाता है: जुड़ाव संदेश नहीं है।",
     "Judav sandesh nahi|isliye kaha jaata", "quote", dict(line="A LINK, NOT A LINE")),
]

EXTRA[9] = [
    ("बेल माप का मतलब है: दो कणों को आपस में मिलाकर नापना।",
     "Bell maap|dono ko milakar naapna", "rig", dict(left="A1", right="A2")),
    ("उसके चार में से एक नतीजा आता है। हर नतीजा दो बिट कहता है।",
     "Chaar mein se ek|do bit", "three", dict(items=["00", "01", "10", "11"], note="four outcomes")),
    ("बॉब को वही दो बिट चाहिए, वरना उसे पता नहीं कौन सा सुधार लगाना है।",
     "Do bit chahiye|warna pata nahi", "board",
     dict(title="WHY THE BITS", lines=["four possible fixes", "she must say which"])),
    ("मूल कण की अवस्था मिट जाती है। इसे क्लोनिंग नहीं किया जा सकता।",
     "Mool avastha mit jaati hai|cloning nahi", "formula", dict(eq="no-cloning", note="the original is consumed")),
    ("यानी टेलीपोर्टेशन नकल नहीं है। एक अवस्था एक जगह से दूसरी जगह जाती है।",
     "Teleportation nakal nahi|avastha ek jagah se doosri", "quote", dict(line="A MOVE, NOT A COPY")),
]

EXTRA[10] = [
    ("चाबी बाँटने में फ़ायदा ये है: चोरी पकड़ में आ जाती है।",
     "Chabi baantne mein fayda|chori pakdi jaati hai", "board",
     dict(title="WHY IT IS SAFE", lines=["reading changes the state", "the key is thrown away"])),
    ("क्वांटम कंप्यूटर में जुड़ाव कई क्यूबिट को एक साथ जोड़ता है।",
     "Quantum computer|kai qubit ek saath", "formula", dict(eq="n qubits → 2^n amplitudes", note="entanglement is the fuel")),
    ("नेटवर्क में जुड़ाव को दूर तक भेजना पड़ता है। इसमें फोटॉन सबसे अच्छे हैं।",
     "Network mein door tak|photon sabse achhe", "channel", dict(left="NODE", right="NODE", note="fibre")),
    ("रिपीटर की ज़रूरत पड़ती है, क्योंकि फाइबर में फोटॉन खोते हैं।",
     "Repeater ki zaroorat|photon khote hain", "board",
     dict(title="THE PROBLEM", lines=["loss grows with distance", "no copying allowed"])),
    ("इसीलिए सैटलाइट और फाइबर, दोनों रास्ते चल रहे हैं।",
     "Satellite aur fibre|dono raaste", "three", dict(items=["FIBRE", "FREE SPACE", "SATELLITE"], note="three routes")),
]

EXTRA[11] = [
    ("इस तीसरे स्तर पर चार बड़े विचार हैं। चारों गंभीर हैं।",
     "Chaar bade vichar|chaaron serious", "three",
     dict(items=["COPENHAGEN", "MANY WORLDS", "PILOT WAVE", "QBISM"], note="four readings")),
    ("कुछ भौतिकविद् कहते हैं: माप से अवस्था बदलती है, बस इतना जानना काफ़ी है।",
     "Maap se avastha badalti|bas itna kaafi", "quote", dict(line="SHUT UP AND CALCULATE")),
    ("कुछ कहते हैं: हर नतीजा किसी दुनिया में सच होता है।",
     "Har nateeja|kisi duniya mein sach", "board",
     dict(title="MANY WORLDS", lines=["every outcome happens", "in its own branch"])),
    ("कुछ कहते हैं: छुपी हुई अवस्था है, पर वो ग़ैर-स्थानीय है।",
     "Chhupi avastha hai|par non-local", "board",
     dict(title="PILOT WAVE", lines=["a real guiding wave", "explicitly non-local"])),
    ("फ़िलहाल कोई प्रयोग इनमें से किसी एक को चुन नहीं पाया है।",
     "Koi prayog chun nahi paya|abhi tak", "quote", dict(line="STILL NO EXPERIMENT DECIDES")),
]

EXTRA[12] = [
    ("अगर एक वाक्य याद रखना हो, तो यही: अवस्था एक है, ब्यौरा अलग नहीं होता।",
     "Ek vaakya|avastha ek hai", "quote", dict(line="ONE STATE, NO SEPARATE ACCOUNT")),
    ("और अगर एक ग़लतफ़हमी मिटानी हो: ये संदेश भेजने का ज़रिया नहीं है।",
     "Ek galatfehmi|sandesh ka zariya nahi", "quote", dict(line="NOT A MESSENGER")),
    ("बाक़ी सब इसी एक बात से निकलता है।",
     "Baaki sab isi se nikalta hai", "board",
     dict(title="EVERYTHING ELSE FOLLOWS", lines=["Bell's limit", "the experiments", "the applications"])),
    ("धन्यवाद।",
     "Dhanyavaad", "quote", dict(line="THANK YOU")),
]
