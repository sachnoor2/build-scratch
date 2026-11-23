# Chapters 1-4 — what entanglement is, the mathematics, EPR, Bell.
# Each shot: (Hindi text for the voice, Roman caption, template, props)

CH = []

# ---------------------------------------------------------------- 1. definition
CH.append(dict(
    n=1, title="एक अवस्था, दो कण", accent="cyan", shots=[
        ("दो कण। एक ही क्वांटम अवस्था। इन्हें अलग अलग समझाया नहीं जा सकता।",
         "Do kan|ek hi avastha", "pair", dict(left="A", right="B", mid="one state")),
        ("यही एंटैंगलमेंट है। एक जुड़ी हुई अवस्था, जो दो जगह रहती है।",
         "Yahi entanglement hai|ek judi avastha", "quote", dict(line="ONE STATE, TWO PLACES")),
        ("ध्यान दें, ये सिर्फ़ मिलते जुलते नतीजे नहीं हैं। यहाँ गणित की बनावट बदलती है।",
         "Sirf milte nateeje nahi|ganit ki banawat badalti hai", "board",
         dict(title="NOT JUST MATCHING", lines=["matching results ≠ entanglement", "the joint state is the object"])),
        ("एक कण को नापो, तो दूसरे के बारे में आप ज़्यादा बता सकते हैं।",
         "Ek ko naapo|doosre ke baare mein zyada pata", "pair", dict(left="?", right="?", mid="predict")),
        ("लेकिन दो गोलियाँ भी उल्टी हो सकती हैं। हर उल्टा जोड़ा एंटैंगल नहीं होता।",
         "Do goliyan bhi ulti ho sakti hain|har joda entangled nahi", "board",
         dict(title="THE TRAP", lines=["opposite results can be ordinary", "or they can be quantum"])),
        ("असली फ़र्क़ यह है: क्या जवाब पहले से कणों में लिखा हुआ है?",
         "Asli farq|jawab pehle se likha hai?", "quote", dict(line="PRE-SET, OR NOT?")),
        ("अगर हाँ, तो ये सामान्य जानकारी है। अगर नहीं, तो ये क्वांटम है।",
         "Haan to normal|nahi to quantum", "board",
         dict(title="TWO EXPLANATIONS", lines=["local pre-set values", "a non-separable state"])),
        ("इसी सवाल ने भौतिकी को सौ साल तक उलझाया।",
         "Isi sawaal ne physics ko uljhaya", "timeline",
         dict(years=[("1935", "EPR"), ("1964", "Bell"), ("2022", "Nobel")], at=0)),
        ("चलिए, शुरुआत गणित से करते हैं। यहीं असली बात छिपी है।",
         "Shuruaat ganit se|asli baat yahin hai", "card", dict(n="2", title="गणित की बनावट", sub="THE MATHEMATICS")),
    ]))

# ----------------------------------------------------------------- 2. the maths
CH.append(dict(
    n=2, title="गणित की बनावट", accent="violet", shots=[
        ("किसी भी जोड़ी की अवस्था को गणित में एक चीज़ से लिखा जाता है।",
         "Jodi ki avastha|ek cheez se likhi jaati hai", "formula", dict(eq="|Ψ⟩AB", note="the joint state")),
        ("अगर वो अवस्था दो अलग अवस्थाओं के गुणनफल से बन जाए, तो जोड़ी अलग अलग है।",
         "Product se ban jaaye|to jodi alag alag", "formula", dict(eq="|a⟩A × |b⟩B", note="separable")),
        ("और अगर ऐसा कोई गुणनफल न मिले, तो अवस्था एंटैंगल है।",
         "Koi product na mile|to entangled", "formula", dict(eq="|Ψ⟩AB ≠ |a⟩ × |b⟩", note="entangled")),
        ("ये कोई दार्शनिक बहस नहीं है। ये एक साफ़ परीक्षण है।",
         "Darshanik bahas nahi|saaf test", "board",
         dict(title="A CLEAN TEST", lines=["factor the state?", "yes → separate", "no → entangled"])),
        ("सबसे मशहूर उदाहरण है सिंगलेट अवस्था। दो कण, उल्टे स्पिन, एक अवस्था।",
         "Singlet|do kan, ulte spin", "pair", dict(left="↑", right="↓", mid="singlet")),
        ("इसमें हर दिशा में उल्टापन मिलता है, केवल एक दिशा में नहीं।",
         "Har disha mein ultapan|sirf ek mein nahi", "board",
         dict(title="EVERY AXIS", lines=["not one fixed axis", "the whole frame rotates together"])),
        ("इसीलिए सामान्य 'पहले से तय जवाब' वाली कहानी यहाँ फ़िट नहीं बैठती।",
         "Pehle se tay jawab|kahani fit nahi baithti", "quote", dict(line="NO HIDDEN SCRIPT")),
        ("गणित कहता है: जोड़ी का कोई भी हिस्सा अपनी पूरी कहानी अकेले नहीं रखता।",
         "Koi hissa apni poori kahani|akele nahi rakhta", "levels",
         dict(items=["JOINT STATE", "PART A", "PART B"], note="parts are not independent")),
        ("यही बात आइंस्टीन को हज़म नहीं हुई।",
         "Yahi baat Einstein ko hazam nahi hui", "quote", dict(line="EINSTEIN'S OBJECTION")),
        ("उन्नीस सौ पैंतीस में तीन भौतिकविदों ने इस पर सवाल उठाया।",
         "1935|teen physicists ne sawaal uthaya", "card", dict(n="3", title="EPR, 1935", sub="THE CHALLENGE")),
    ]))

# -------------------------------------------------------------------- 3. EPR
CH.append(dict(
    n=3, title="EPR, उन्नीस सौ पैंतीस", accent="gold", shots=[
        ("आइंस्टीन, पोडोल्स्की और रोसेन। तीन नाम, एक पेपर, एक सवाल।",
         "Einstein, Podolsky, Rosen|teen naam, ek sawaal", "three",
         dict(items=["EINSTEIN", "PODOLSKY", "ROSEN"], note="1935")),
        ("सवाल था: क्या क्वांटम सिद्धांत हक़ीक़त का पूरा ब्यौरा देता है?",
         "Kya theory poori tasveer deti hai?", "quote", dict(line="IS QUANTUM COMPLETE?")),
        ("उनका तर्क था कि अगर दूर का कण तुरंत बदल जाए, तो कुछ गड़बड़ है।",
         "Door ka kan turant badle|to kuch gadbad hai", "pair", dict(left="A", right="B", mid="instant?")),
        ("उन्होंने कहा: कण अपना जवाब पहले से लेकर चलते होंगे। छुपे हुए निर्देश।",
         "Chhupe nirdesh|hidden values", "board",
         dict(title="EPR'S ANSWER", lines=["each particle carries its answer", "measurement only reveals it"])),
        ("इस विचार को स्थानीय छुपी हुई चर वाला सिद्धांत कहते हैं।",
         "Local hidden variable theory", "formula", dict(eq="λ", note="a pre-set value per particle")),
        ("इसका मतलब: दूर की घटना यहाँ के नतीजे को प्रभावित नहीं करती।",
         "Door ki ghatna|yahan ka nateeja nahi badalti", "board",
         dict(title="LOCALITY", lines=["no instant influence", "no faster than light"])),
        ("बोहर ने जवाब दिया, पर ये बहस शब्दों में ही चलती रही।",
         "Bohr ne jawab diya|bahas shabdon mein chali", "quote", dict(line="WORDS ONLY, FOR 30 YEARS")),
        ("किसी के पास कोई परीक्षण नहीं था। सवाल खुला रह गया।",
         "Koi test nahi tha|sawaal khula rah gaya", "levels",
         dict(items=["THEORY", "TEST", "VERDICT"], note="the test was missing")),
        ("उन्नीस सौ चौंसठ तक यही हाल रहा।",
         "1964 tak yahi haal raha", "timeline",
         dict(years=[("1935", "EPR"), ("1964", "Bell"), ("2022", "Nobel")], at=1)),
        ("फिर एक आदमी ने इसे एक असमानता में बदल दिया।",
         "Phir ek aadmi ne ise inequality banaya", "card", dict(n="4", title="बेल, 1964", sub="THE INEQUALITY")),
    ]))

# ------------------------------------------------------------------- 4. Bell
CH.append(dict(
    n=4, title="बेल की सीमा", accent="cyan", shots=[
        ("जॉन बेल ने सवाल पूछा: छुपे निर्देश हों, तो नतीजे कैसे बँटेंगे?",
         "John Bell|chhupe nirdesh ho to nateeje kaise", "quote", dict(line="WHAT IF VALUES ARE PRE-SET?")),
        ("उन्होंने चार नापों का जोड़ा हुआ अंक निकाला। हर स्थानीय सिद्धांत के लिए एक सीमा।",
         "Chaar naapon ka joda|local theory ki limit", "formula", dict(eq="S ≤ 2", note="any local pre-set theory")),
        ("ये सीमा दो है। कोई भी स्थानीय, पहले से तय जवाब वाला सिद्धांत दो से ऊपर नहीं जा सकता।",
         "Limit do hai|do se upar nahi", "chart", dict(limit=2.0, peak=2.83, measured=None)),
        ("लेकिन क्वांटम गणित कहता है कि अंक दो दशमलव आठ दो आठ तक पहुँचेगा।",
         "Quantum|do dashamlav aath do aath", "chart", dict(limit=2.0, peak=2.83, measured=2.828)),
        ("यानी क्वांटम नतीजा सीमा के पार जाता है। यहीं फ़ैसला होगा।",
         "Quantum limit ke paar|yahin faisla", "board",
         dict(title="THE DECISION", lines=["below 2 → hidden values win", "above 2 → quantum wins"])),
        ("अब सिर्फ़ एक काम बचा था। प्रयोग करके देखना।",
         "Ab sirf prayog|experiment karna", "quote", dict(line="MEASURE IT")),
        ("बेल ने ये भी साफ़ किया कि सीमा किन मान्यताओं पर टिकी है।",
         "Limit kin manyataon par tiki hai", "levels",
         dict(items=["LOCALITY", "REALISM", "FREE CHOICE"], note="three assumptions")),
        ("अगर कोई मान्यता टूटे, तो सीमा भी टूट सकती है। यही आगे की कहानी है।",
         "Ek manyata toote|limit bhi toot sakti", "board",
         dict(title="THE LOOPHOLES", lines=["locality", "detection", "free choice"])),
        ("उन्नीस सौ बहत्तर में पहला असली परीक्षण हुआ।",
         "1972|pehla asli test", "timeline",
         dict(years=[("1972", "Freedman"), ("1982", "Aspect"), ("2015", "loophole-free")], at=0)),
        ("नतीजा सीमा के पार निकला। लेकिन सवाल अभी पूरा खत्म नहीं हुआ था।",
         "Nateeja limit ke paar|sawaal khatm nahi", "card", dict(n="5", title="पहले प्रयोग", sub="THE EXPERIMENTS")),
    ]))
