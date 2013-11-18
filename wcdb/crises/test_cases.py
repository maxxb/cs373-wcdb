CRISIS_A = {
    u"name": u"Cambodian Genocide",
    u"start_date": u"1975-01-01",
    u"end_date": u"1978-01-01",
    u"location": u"Cambodia",
    u"kind": u"Attack",
    u"description": u"Long text description of the Cambodian Genocide",
    u"human_impact": u"Lost 25% of population over three years",
    u"economic_impact": u"Peasant farming society centralized",
    u"maps": [u"http://goo.gl/maps/PKI5L"],
    u"images": [u"http://worldwithoutgenocide.org/wp-content/uploads/2010/01/Cambodia.jpg"],
    # I have an issue on the CS machines where the '=' here causes django to see the 
    # string as a key-value pair when I make a post request when testing 
    # u"videos": [u"http://www.youtube.com/watch?v=1-SI8RF6wDE"],
    u"videos": [u"http://www.youtube.com/watch?v..."],
    u"social_media": [u"https://twitter.com/UN"],
    u"ways_to_help": [u"Donation"],
    u"resources_needed": [u"Monetary donation"],
    u"people": [1],
    u"organizations": [1],
    u"external_links": [u"unfoundation.org"],
    u"citations": [u"http://worldwithoutgenocide.org/genocides-and-conflicts/cambodian-genocide"],
}

CRISIS_B = {        
    u"name": u"Israeli-Palestinian conflict",
    u"id":1,
    u"start_date": u"1960-01-01",
    u"end_date": u"2013-11-01",
    u"location": u"West Bank and Gaza Strip",         
    u"kind": u"political",
    u"description": u"The Israeli\u2013Palestinian conflict is the ongoing struggle between Israelis and Palestinians that began in the mid 20th century. The conflict is wide-ranging, and the term is sometimes also used in reference to the earlier sectarian conflict in Mandatory Palestine, between the Zionist yishuv and the Arab population under British rule. The Israeli\u2013Palestinian conflict has formed the core part of the wider Arab\u2013Israeli conflict.",
    u"human_impact": u"One of the world's longest refugee crisis. Nearly 50 percent of Palestinians in the West Bank and Gaza. 2.1 million people are refugees, many of whom live in crowded camps.",
    u"economic_impact": u"Economic life has suffered and relief organisations have found it difficult to get aid to the Palestinian population.",
    u"maps": [u"http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=west%2Bbank%2C%2Bisrael&ie=UTF8&z=12&t=m&iwloc=near&output=embed"],
    u"images": [u"http://www.globalresearch.ca/wp-content/uploads/2012/11/Israel_Palestine_Flag.png"],
    u"videos": [u"http://www.youtube.com/embed/GdtGOY8T5XE?"],
    u"social_media": [u"https://twitter.com/search?q=isreal+palestine"],
    u"ways_to_help": [u"peaceful negotiations"],
    u"resources_needed": [u"none"],
    u"people": [1, 2],
    u"organizations": [1], 
    u"external_links": [u"http://www.trust.org/spotlight/Israeli-Palestinian-conflict"],
    u"citations": [u"http://en.wikipedia.org/wiki/Israeli%E2%80%93Palestinian_conflict"],
}

PEOPLE_A = {
    u"name":u"Yasser Arafat",
    u"id":1,
    u"DOB":u"1929-08-24",
    u"location":u"Cairo, Egypt",
    u"kind":u"political leader",
    u"description": u"He was Chairman of the Palestine Liberation Organization (PLO), President of the Palestinian National Authority (PNA), and leader of the Fatah political party and former paramilitary group, which he founded in 1959. Arafat spent much of his life fighting against Israel in the name of Palestinian self-determination. Originally opposed to Israel's existence, he modified his position in 1988 when he accepted UN Security Council Resolution 242. Arafat and his movement operated from several Arab countries.",
    u"images": [u"http://upload.wikimedia.org/wikipedia/commons/thumb/3/37/ArafatEconomicForum.jpg/415px-ArafatEconomicForum.jpg",
                u"http://upload.wikimedia.org/wikipedia/commons/9/9a/Flickr_-_Government_Press_Office_%28GPO%29_-_THE_NOBEL_PEACE_PRIZE_LAUREATES_FOR_1994_IN_OSLO..jpg"],
    u"videos":[u"http://www.youtube.com/watch?v=a0tbZ3iYgCs"],
    u"maps":[u"http://goo.gl/maps/oOQCX"],
    u"social_media": [u"http://twitter.com/search?q=yasser+arafat",],
    u"crises":[1],
    u"organizations":[2],
    u"external_links":[u"http://www.nndb.com/people/403/000022337/"],
    u"citations":[u"http://en.wikipedia.org/wiki/Yasser_Arafat"]
}

PEOPLE_B = {        
    u"name":u"Warren Anderson",
    u"id":2,
    u"DOB":u"1921-01-01",
    u"location":u"Brooklyn, NY",
    u"kind":u"Former CEO",
    u"description": u"The Bhopal disaster took place in a plant belonging to a Union Carbide's (UCC) Indian subsidiary, Union Carbide India Limited, in the city of Bhopal, Madhya Pradesh, India during 1984. Thousands of people died and thousands more were injured in the disaster. As the UCC CEO, Anderson was charged[citation needed] with manslaughter by Indian authorities. He flew to India with a promise that he would not be arrested; however, Indian authorities placed him in custody. Anderson posted bail, returned to the US, and refused to return to India. He was declared a fugitive from justice by the Chief Judicial Magistrate of Bhopal on February 1, 1992, for failing to appear at the court hearings in a culpable homicide case in which he was named the chief defendant. The chief judicial magistrate of Bhopal, Prakash Mohan Tiwari, issued an arrest warrant for Anderson on July 31, 2009. The United States has declined to extradite him citing a lack of evidence.",
    u"images": [u"http://upload.wikimedia.org/wikipedia/commons/9/9a/Flickr_-_Government_Press_Office_%28GPO%29_-_THE_NOBEL_PEACE_PRIZE_LAUREATES_FOR_1994_IN_OSLO..jpg"],
    u"videos":[u"http://www.youtube.com/watch?v=yhmVRckHHxM"],
    u"maps":[u"http://goo.gl/maps/3tPTc"],
    u"social_media": [u"http://twitter.com/search?q=warren+anderson+bhopal"],
    u"crises":[1],
    u"organizations":[2],
    u"external_links":[u"http://www.cbsnews.com/stories/2009/08/01/national/main5204098.shtml"],
    u"citations":[u"http://en.wikipedia.org/wiki/Warren_Anderson_%28American_businessman%29"]
}

ORG_A = {
    u"id": 1,
    u"name": u"UNSCEAR",
    u"established":u"1955-01-01",
    u"location": u"Sessions are held in Vienna International Centre, Vienna, Austria.",
    u"kind":u"Committee",
    u"description":u"UNSCEAR was established in 1955 by the General Assembly of the United Nations. The organizations purpose in the United Nations system is to assess and report levels and effects of exposure to ionizing radiation. Governments and organizations throughout the world rely on the Committee's estimates as the scientific basis for evaluating radiation risk and for establishing protective measures. UNSCEAR was involved in the assessment of radiation exposures and health effects early on during the Chernobyl accident in 1986.",
    u"images": [u"http://www.irpa.net/images/stories/logo/unscear.gif"],
    u"videos":[u"http://www.youtube.com/embed/gyLDNq3VBMU"],
    u"maps":[u"http://maps.google.com/maps?f=q&source=s_q&hl=en&geocode=&q=west%2Bbank%2C%2Bisrael&ie=UTF8&z=12&t=m&iwloc=near&output=embed"],
    u"social_media":[u"https://twitter.com/search?q=UNSCEAR"],
    u"external_links":[u"http://www.bmeia.gv.at/en/austrian-mission/austrian-mission-vienna/organizations-in-vienna/with-offices-at-the-vic/unscear.html"],
    u"citations":[u"http://www.unscear.org/"],
    u"contact_info": {
        u"name": u"UNSCEAR secretariat",
        u"address": u"UNITED NATIONS Vienna International Centre P.O. Box 500 A-1400 Vienna, AUSTRIA",
        u"email": u"notfound@notfound.com",
        u"phone": u"1260604330"},
    u"people":[2],
    u"crises":[1]
}

ORG_B = {
    u"id": 2,
    u"name": u"PLO",
    u"established":u"1964-06-02",
    u"location": u"Sessions are held in Vienna International Centre, Vienna, Austria.",
    u"kind":u"political party",
    u"description":u"Umbrella political organization claiming to represent the world's Palestinians - those Arabs, and their descendants, who lived in  mandated Palestine before the creation of the State of Israel in 1948. It was formed in 1964 to centralize the leadership of various Palestine groups that previously had operated as clandestine resistance movements. It came into prominence only after the Six-Day War of June 1967, however, and engaged in a protracted guerrilla war against Israel during the 1960s, `70s, and `80s before entering into peace negotiations with that country in the 1990s.",
    u"images": [u"http://www.forbiddensymbols.com/wp-content/uploads/plo_palestinian_liberation_organisation_flag.jpg"],
    u"videos":[u"http://www.youtube.com/embed/gyLDNq3VBMU"],
    u"maps":[u"https://maps.google.com/maps?f=q&amp;source=s_q&amp;hl=en&amp;geocode=&amp;q=palestine&amp;sll=33.238688,34.024658&amp;sspn=9.36671,5.866699&amp;t=h&amp;ie=UTF8&amp;hq=&amp;hnear=Palestine&amp;ll=31.952162,35.233154&amp;spn=1.041069,1.466675&amp;z=9&amp;output=embed"],
    u"social_media":[u"https://twitter.com/search?q=Palestine+Liberation+Organization"],
    u"external_links":[u"http://www.infoplease.com/encyclopedia/history/palestine-liberation-organization.html"],
    u"citations":[u"http://www.unioncarbide.com/"],
    u"contact_info": {
        u"name": u"N/A",
        u"address": u"N/A",
        u"email": u"notfound@notfound.com",
        u"phone": u"N/A"},
    u"people":[1,2],
    u"crises":[1]
}