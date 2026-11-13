# 그린피그 영어판 자료. build_en.py가 이 파일과 works_data.py를 함께 읽어 en/ 폴더의 페이지를 만든다.
# 번역은 2026.11 처음 만든 것으로, 손볼 곳이 있으면 여기서 고치고 build.py를 다시 돌리면 된다.
# 사람 이름은 NAME에 없으면 자동으로 로마자로 옮긴다(성 + 이름). 본인이 쓰는 영문 이름이 있으면 NAME에 한 줄 더하면 된다.

NAME = {
    "조웅철": "Cho Woongchul",
    "송김경화": "Song Kim Kyunghwa",
    "황보영": "Hwangbo Young",
    "정나무": "Jung Namu",
    "전성현": "Jeon Sunghyun",
    "박현지": "Park Hyunji",
    "이기석": "Lee Kiseok",
    "강훈구": "Kang Hoongu",
    "윤미현": "Yoon Mihyun",
    "그린피그": "Green Pig",
}

# 한국어로 적힌 외국 작가·인명과 단체
ORG = {
    "폴라 보겔": "Paula Vogel", "피터 바이스": "Peter Weiss", "안톤 체홉": "Anton Chekhov",
    "안토니오 부에로 바예호": "Antonio Buero Vallejo", "에이야드 악타": "Ayad Akhtar", "아야드 악타르": "Ayad Akhtar",
    "조지 오웰 〈1984〉": "George Orwell, 1984", "Jeanette Winterson 〈GODBLOG〉": "Jeanette Winterson, GODBLOG",
    "그린피그 공동창작": "Green Pig (devised)", "극단 여행자": "Theatre Yeohaengja", "K아트플래닛": "K Art Planet",
    "국립정동극장": "Jeongdong Theater", "(재)국립정동극장": "Jeongdong Theater", "남산예술센터": "Namsan Arts Center",
    "두산아트센터": "Doosan Art Center", "드림아트펀드": "Dream Art Fund", "드림아트": "Dream Art", "미미프로젝트": "MiMi Project",
    "서울문화재단": "Seoul Foundation for Arts and Culture", "서울문화재단 서울메세나 지원사업": "Seoul Foundation for Arts and Culture, Seoul Mecenat program",
    "서울사진관": "Seoul Photo Studio", "소리를보여주는사람들": "People Who Show Sound", "수택고등학교 우리 1·2반": "Sutaek High School, Uri classes 1 and 2",
    "이다엔터테인먼트": "Ida Entertainment", "창작주체 예술공간 혜화": "Art Space Hyehwa", "프로젝트 레디메이드": "Project Readymade",
    "프로젝트 세시": "Project Sesi", "한국문화예술위원회": "Arts Council Korea",
    "한국문화예술위원회 공연예술중장기창작지원": "Arts Council Korea, mid- to long-term creation support",
    "한국문화예술위원회 신진예술가 지원": "Arts Council Korea, emerging artist support",
    "한국영상연합": "Korea Video Union", "한국예술창작아카데미": "Korea Arts Creation Academy", "혜화동1번지 5기 동인": "Hyehwa-dong 1beonji, 5th members",
    "다홍디자인": "Dahong Design", "스탭서울": "Staff Seoul", "워크룸": "Workroom", "보통현상": "Botong Hyunsang", "옴브레": "Ombre",
    "온달": "Ondal", "파이카": "Paika", "올림픽(all limpic)": "all limpic", "투바이투": "Two by Two", "죠이매직": "Joy Magic",
    "홀연": "Holyeon", "목소": "Mokso", "루브": "Ruv", "침게": "Chimge", "플랫폼엘": "Platform-L", "공동창작": "devised",
    "거,그,기, / 그린피그 / 미미프로젝트": "Geo, Geu, Gi, / Green Pig / MiMi Project", "연우무대": "Yeonwoo Mudae",
    "인권교육센터 들": "Human Rights Education Center Deul", "공동재구성": "co-adapted", "밴드 얄개들": "band Yalgaedeul",
    "MPICS PRODUCTION": "MPICS PRODUCTION", "NOVEMBER ADVERTISING": "NOVEMBER ADVERTISING", "Mr-Hodol": "Mr-Hodol",
}

ROLE = {
    "작": "Playwright", "작가": "Writer", "연출": "Director", "조연출": "Assistant director", "출연": "Cast", "배우": "Performers",
    "연기": "Performers", "음악": "Music", "음악감독": "Music director", "작곡": "Composer", "조명": "Lighting",
    "조명디자인": "Lighting design", "음향": "Sound", "음향감독": "Sound director", "의상": "Costumes", "의상디자인": "Costume design",
    "의상감독": "Costume director", "분장": "Make-up", "분장디자인": "Make-up design", "분장감독": "Make-up director", "분장팀": "Make-up team",
    "무대": "Set", "무대디자인": "Set design", "무대감독": "Stage manager", "무대 제작": "Set construction", "소품": "Props",
    "영상": "Video", "영상디자인": "Video design", "영상 촬영": "Video recording", "영상 오퍼레이터": "Video operator",
    "영상 프로그래머": "Video programmer", "영상크루": "Video crew", "사진": "Photography", "기획": "Producer", "홍보": "Publicity",
    "마케팅": "Marketing", "홍보마케팅": "Publicity and marketing", "홍보영상": "Promotional video", "홍보동영상": "Promotional video",
    "그래픽디자인": "Graphic design", "그래픽 디자인": "Graphic design", "그래픽": "Graphics", "디자인": "Design",
    "인쇄물디자인": "Print design", "웹디자인": "Web design", "레터링": "Lettering", "일러스트레이션": "Illustration", "포스터": "Poster",
    "드라마터그": "Dramaturg", "드라마터지": "Dramaturgy", "드라마투르기": "Dramaturgy", "드라마투르그": "Dramaturg", "번역": "Translation",
    "원작": "Original work", "글": "Text", "글쓰기": "Text", "구성": "Concept", "공동구성": "Co-devised by", "공동창작": "Devised by",
    "공동연구": "Joint research", "개작": "Adaptation", "안무": "Choreography", "조안무": "Assistant choreographer", "움직임": "Movement",
    "움직임지도": "Movement coach", "연기지도": "Acting coach", "액팅코치": "Acting coach", "노래 지도": "Singing coach",
    "판소리지도": "Pansori coach", "사투리지도": "Dialect coach", "사투리녹음": "Dialect recording", "연변말 지도": "Yanbian dialect coach",
    "몽골어 코치": "Mongolian coach", "복싱지도": "Boxing coach", "오퍼": "Operator", "오퍼레이터": "Operator", "조명 오퍼": "Lighting operator",
    "조명 오퍼레이터": "Lighting operator", "음향 오퍼레이터": "Sound operator", "음향 오퍼": "Sound operator", "자막 오퍼레이터": "Surtitle operator",
    "자막 제작": "Surtitles", "조명 어시스턴트": "Lighting assistant", "조명크루": "Lighting crew", "조명팀": "Lighting crew", "제작": "Production",
    "제작감독": "Production manager", "주최": "Presented by", "주관": "Organized by", "후원": "Sponsored by", "지원": "Supported by",
    "협력": "In cooperation with", "협력기획": "Co-producer", "공동기획": "Co-produced by", "협력연출": "Associate director",
    "공동주최": "Co-presented by", "진행": "Coordination", "진행보조": "Assistant", "티켓": "Ticketing", "촬영": "Filming",
    "기록 촬영": "Documentation", "기록촬영": "Documentation", "기록": "Documentation", "목소리 출연": "Voice", "미술": "Art",
    "공간": "Space", "사운드": "Sound", "연출부": "Directing team", "자문": "Advisor", "프롬프터": "Prompter", "프로듀서": "Producer",
    "해설": "Commentary", "강연": "Lecture", "시": "Poems", "가수": "Singer", "수어통역": "Sign language interpretation", "PD": "PD",
    "접근성매니저": "Accessibility manager", "만나는 사람들": "People we met", "반차별워크숍": "Anti-discrimination workshop",
    "비주얼아트디렉터": "Visual art director", "기계 조작": "Machine operation", "연희": "Traditional performance", "DJ": "DJ",
    "밴드 얄개들": "Band Yalgaedeul", "설치": "Installation", "연주": "Performance", "음향디자인": "Sound design", "바디": "Pansori school",
    "대본": "Script", "공동재구성": "Co-adapted by", "인형 감독": "Puppet director", "주최·주관": "Presented and organized by",
}

# 역할 앞에 붙은 단막 제목
SUBTITLE = {"산은 말한다": "The Mountain Speaks", "우린 조화로운 꽃들이야": "We Are Harmonious Flowers",
            "암야": "Dark Night", "추야": "Autumn Night", "밥": "Rice", "맘마": "Mamma"}

TITLE = {
    "01": "Assassins", "02": "I Am Happy", "03": "Days Like a Painting", "04": "Without Vinker I'm Too Lonely",
    "05": "Grief Not Fully Mourned", "06": "Jin and Jun", "07": "Man Is a Wolf to Man", "08": "Step-memory: Return of the Repressed",
    "09": "Who Landed a Missile Punch on Muhammad Ali's Temple?", "10": "I'm the King of Sex", "11": "Yanbian Mother",
    "12": "Anyway, Baek Seok", "13": "Brain Surgery", "14": "Psychopath", "15": "Garden Killer", "16": "Unwanted, Na Hye-seok",
    "17": "Tree Won't Seek for Shoe Store", "18": "Commie: A Study for Rehabilitation (working title)",
    "19": "Desdemona: A Play About a Handkerchief", "20": "Fear", "21": "The Investigation (Oświęcim)", "22": "Young Fucidin",
    "23": "The Way of Story, the Way of Song – Demo Version", "24": "1984", "25": "174517", "26": "Haemun of Jochiwon",
    "27": "Chijeong (Passion)", "28": "Behind Cut", "29": "I'm the King of Acting",
    "30": "At the Pasqueflower Bar, Grandma Said She'd Give Us Melon Seeds", "31": "The Whistleblowers",
    "32": "A History of Wastepaper (I'M F_)", "33": "Dream Culture", "34": "The Way of Story, the Way of Dance – Gong Ok-jin's Byeongsin-chum",
    "35": "A Rainbow Made of Steel", "36": "Phantom Neuro", "37": "Delivery Return", "38": "Labor Landscape 1: Unemployment",
    "40": "Contemporaries", "41": "@GODBLOG", "42": "CAVE-2021 Seoul Version", "43": "Wooden Boat", "44": "Home Sweet Home: Dorothy",
    "45": "Barbaryman: Kill Like I Do", "46": "Ipjeong-hada", "47": "Blooming Station: Traces", "48": "The Who & The What",
    "49": "Home Sweet Home 2: Abandoned Children", "50": "Ill-fated: A Twentieth Birthday Wish", "51": "Fake News 2022: MAPHIKO",
    "52": "Extra Chronicles", "53": "Ju Eungil One-Act Plays", "54": "Ankle", "55": "Snapshot", "56": "Ghost-Gut",
    "57": "The Nightmare Also Gazes Into You", "58": "Shame", "2024-02": "Real Theater: The Immortal Lee Kiseok",
    "59": "The Great Battle of the Sheep Ranch", "60": "In Search of the Lost Body", "2024-05": "History Exploration Lab",
    "61": "A Good Place to Live, OO", "2024-07": "Midsummer Train Game", "62": "Hoo-Ha!", "2024-09": "Liar Game",
    "63": "The Nauseator (It)", "2024-11": "Harry", "64": "Becoming Korean", "65": "Reading Yeom Sang-seop",
    "66": "Fool-Run: The Cherry Orchard", "67": "Tropical Night in Deep Winter",
    "68": "When Chorok Lies, We All Clap", "69": "Fool-Run: In the Burning Darkness", "70": "Wrath 震怒", "71": "Proud Mary",
}
# 공연 기록에서 같은 작품을 다른 제목으로 올린 경우
TITLE_VARIANT = {
    "폐지의 역사": "A History of Wastepaper", "엑스트라 연대기": "Extra Chronicles", "누구와 무엇 The Who &amp; The What": "The Who & The What",
    "마-피-코": "MA-PHI-KO", "마피코 MAPHIKO": "MAPHIKO",
}

VENUE = {
    "57th 갤러리": "57th Gallery", "CJ아지트": "CJ Azit", "KOCCA 콘텐츠문화광장 스테이지66": "KOCCA Content Culture Square, Stage 66",
    "TINC(This is not a church)": "TINC (This is not a church)", "강화 내가초등학교": "Naega Elementary School, Ganghwa",
    "경기상상캠퍼스": "Gyeonggi Sangsang Campus", "광명시민회관 대공연장": "Gwangmyeong Civic Hall", "광주 동산아트홀": "Dongsan Art Hall, Gwangju",
    "국립극단 백성희장민호극장": "National Theater Company, Baek Seonghui & Jang Minho Theater", "국립극단 소극장 판": "National Theater Company, Studio Pan",
    "국립극장 별오름극장": "National Theater of Korea, Byeoloreum Theater", "국립아시아문화전당": "Asia Culture Center, Gwangju",
    "국립정동극장 세실": "Jeongdong Theater Cecil", "그린피그 연습실": "Green Pig rehearsal room", "나온씨어터": "Naon Theater",
    "남산예술센터 드라마센터": "Namsan Arts Center Drama Center", "노무현시민센터": "Roh Moo-hyun Citizen Center", "다원예술매개공간": "Dawon Art Space",
    "대학로 선돌극장": "Seondol Theater, Daehangno", "대학로 우리극장": "Uri Theater, Daehangno", "대학로 정보소극장": "Jeongbo Theater, Daehangno",
    "대학로예술극장 대극장": "Daehangno Arts Theater, Main Hall", "대학로예술극장 소극장": "Daehangno Arts Theater, Small Hall",
    "도쿄 니시스가모": "Nishi-Sugamo, Tokyo", "독일 뮌헨 Einstein Kultur": "Einstein Kultur, Munich", "두산아트센터 Space111": "Doosan Art Center Space111",
    "두산아트센터 스페이스111": "Doosan Art Center Space111", "떼아뜨르추": "Theatre Chu", "로쿠스 솔루스": "Locus Solus",
    "말레이시아 Rimbun Dahan": "Rimbun Dahan, Malaysia", "명동 삼일로창고극장": "Samilro Warehouse Theater, Myeongdong",
    "밀양 동강중학교": "Donggang Middle School, Miryang", "삼일로창고극장": "Samilro Warehouse Theater", "상상만발극장 연습실": "Sangsang Manbal Theater rehearsal room",
    "상상의 사무실": "Office of Imagination", "서강대 메리홀 대극장": "Sogang University Mary Hall, Main Stage",
    "서강대 메리홀 소극장": "Sogang University Mary Hall, Small Stage", "소극장 공유": "Theater Gongyu", "신촌극장": "Sinchon Theater",
    "씨어터 디아더": "Theater The Other", "씨어터 조이": "Theater Joy", "아르코미술관·마로니에 공원": "Arko Art Center and Marronnier Park",
    "아르코예술극장 소극장": "Arko Arts Theater, Small Hall", "안동문화예술의전당 백조홀": "Andong Arts Center, Baekjo Hall",
    "안산예술의전당": "Ansan Arts Center", "언더스탠드에비뉴": "Understand Avenue", "연극실험실 혜화동1번지": "Theater Lab Hyehwa-dong 1beonji",
    "연우소극장": "Yeonwoo Theater", "예술공간 혜화": "Art Space Hyehwa", "예술의전당 자유소극장": "Seoul Arts Center, Jayu Theater",
    "요코하마 KAAT": "KAAT, Yokohama", "월드컵경기장": "Seoul World Cup Stadium", "의정부 예술의전당 소극장": "Uijeongbu Arts Center, Small Hall",
    "이너프라운지": "Enough Lounge", "인천아트플랫폼": "Incheon Art Platform", "입정동 일대": "around Ipjeong-dong",
    "전국 12개 지역 순회": "tour of 12 regions", "전남도청 본관 앞": "in front of the former Jeonnam Provincial Office",
    "전태일기념관 울림터": "Jeon Tae-il Memorial Hall, Ullimteo", "정보소극장": "Jeongbo Theater", "중국 선전 난산문화센터": "Nanshan Cultural Center, Shenzhen",
    "창무 포스트극장": "Changmu Post Theater", "춘천 고슴도치섬": "Goseumdochi Island, Chuncheon", "춘천 축제극장몸짓": "Chuncheon Festival Theater Momjit",
    "토탈미술관": "Total Museum of Contemporary Art", "플랫폼엘 머신룸": "Platform-L Machine Room",
    "홍익대 대학로 아트센터 소극장": "Hongik Daehangno Art Center, Small Theater",
    "안산": "Ansan", "안산국제거리극축제": "Ansan Street Arts Festival", "문화역서울284": "Culture Station Seoul 284",
    "한양레파토리극장": "Hanyang Repertory Theater", "서경대 스콘2관": "Seokyeong University SCON 2", "안동 하회마을": "Hahoe Village, Andong",
    "서울연극센터": "Seoul Theater Center", "남산예술센터": "Namsan Arts Center",
}

NOTE = {
    "2023 부산일보 신춘문예 희곡 당선작가": "2023 Busan Ilbo Spring Literary Contest playwriting winner", "ARKO가 주목하는 젊은 예술가": "ARKO Young Artists",
    "SPIELART Festival": "SPIELART Festival", "TPAM 2016": "TPAM 2016", "거,그,기·그린피그·미미프로젝트 제작": "produced by Geo, Geu, Gi, Green Pig and MiMi Project",
    "공연예술창작산실 '올해의 신작'": "Arts Council Korea Changjak Sansil, New Work of the Year", "공연예술창작산실 2차 제작지원": "Arts Council Korea Changjak Sansil, second production support",
    "공연예술창작산실 올해의 레퍼토리": "Arts Council Korea Changjak Sansil, Repertory of the Year", "광주평화연극제": "Gwangju Peace Theater Festival",
    "광주프린지페스티벌 초청": "invited, Gwangju Fringe Festival", "국립정동극장 세실 2026 창작ing": "Jeongdong Theater Cecil 2026 Changjak-ing",
    "권리장전2016_검열각하": "Bill of Rights 2016: Censorship Dismissed", "그린피그 젊은연출가전": "Green Pig Young Directors' Series",
    "기획초청 '세월호'": "invited program 'Sewol'", "대한민국연극대상 작품상 수상 기념": "celebrating the Korea Theater Award for Best Production",
    "덴마크 오르후스 페스티벌 초청": "invited, Aarhus Festival, Denmark", "두산아트랩": "Doosan Art LAB", "두산연강예술상 수상자 신작": "new work by a Doosan Yonkang Arts Award winner",
    "두산연강예술상 신작": "Doosan Yonkang Arts Award new work", "서울국제공연예술제(SPAF)": "Seoul Performing Arts Festival (SPAF)",
    "서울문화재단 예술창작활동지원": "Seoul Foundation for Arts and Culture creation support", "서울변방연극제": "Seoul Marginal Theater Festival",
    "서울아트마켓 PAMS Choice 폐막작": "PAMS Choice closing performance, Performing Arts Market in Seoul", "서울연극제 재공연부문": "Seoul Theater Festival, revival section",
    "서울프린지페스티벌": "Seoul Fringe Festival", "세계국립극장페스티벌 초청": "invited, World National Theater Festival", "수원연극축제 초청": "invited, Suwon Theater Festival",
    "신나는 예술여행": "Exciting Art Journey touring program", "연극 안 하기, 바보런하기": "Not Doing Theater: Fool-Run",
    "연우무대 프로파간다 시리즈": "Yeonwoo Mudae Propaganda Series", "윤영선 연극제": "Yoon Yeongseon Theater Festival",
    "제25회 베세토 페스티벌 한국 공식 초청": "official Korean selection, 25th BeSeTo Festival", "제27회 베세토 연극제, 우수작품상": "27th BeSeTo Festival, Excellence Award",
    "제3회 짧은 연극제 '헌법'": "3rd Short Play Festival 'Constitution'", "제4회 벽산희곡상 수상작": "4th Byeoksan Playwriting Award winner",
    "제7회 벽산희곡상 수상작": "7th Byeoksan Playwriting Award winner", "제9회 벽산희곡상 수상작": "9th Byeoksan Playwriting Award winner",
    "창작 ing_Choice on": "Changjak-ing Choice On", "청년예술가도약지원사업": "Young Artists Leap support", "춘천공연예술제 초청": "invited, Chuncheon Performing Arts Festival",
    "춘천마임축제": "Chuncheon Mime Festival", "페스티벌 도쿄": "Festival/Tokyo", "한국 작고문인 선양사업, 낭독": "reading; program honoring late Korean writers",
}
for _m, _e in zip(["1월", "2월", "3월", "4월", "5월", "6월", "7월", "8월", "9월", "10월", "11월", "12월"],
                  ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]):
    NOTE[f"역사시비프로젝트 {_m}"] = f"History Dispute Project, {_e}"

# 작품 페이지의 '사진 …' 설명
PHOTO = {"02": "2007, Jeongbo Theater, Daehangno", "08": "2012, Festival/Tokyo", "13": "Photo: Mr-Hodol", "32": "2019, Doosan Art Center",
         "42": "Photo: Ok Sanghoon", "52": "Photo: Yu Kyungoh"}
POSTER = {
    "17": ["2012 Jeongbo Theater", "2022 Daehangno Arts Theater", "2022 Seoul Performing Arts Festival", "2023 Gwangmyeong Civic Hall", "2023 Shenzhen, BeSeTo Festival"],
    "13": ["2012 Hyehwa-dong 1beonji Spring Festival", "2015 Theater Lab Hyehwa-dong 1beonji", "2019 CJ Azit", "2020 Theater Lab Hyehwa-dong 1beonji", "2020 Andong Arts Center"],
    "20": ["2013 Sogang University Mary Hall", "2014 Sogang University Mary Hall", "2018 Seoul Theater Festival"],
    "38": ["2020 Yeonwoo Theater", "2020 Jeon Tae-il Memorial Hall"], "48": ["2022 Theater Lab Hyehwa-dong 1beonji", "2023 Jeongdong Theater Cecil"],
    "52": ["2023 Daehangno Arts Theater", "2025 Chuncheon Festival Theater Momjit"], "59": ["2024 Art Space Hyehwa", "2026 Jeongdong Theater Cecil"],
    "07": ["2010 National Theater of Korea, Byeoloreum Theater"],
}
AWARD = {
    "2012 제5회 대한민국 연극대상 작품상": "2012 5th Korea Theater Awards, Best Production",
    "2023 제27회 베세토 연극제 우수작품상": "2023 27th BeSeTo Festival, Excellence Award",
    "2025 제33회 대산문학상 희곡 부문": "2025 33rd Daesan Literary Award, Drama",
}
CRITIC_NOTE = {
    "2022 리뷰, 『연극평론』 2022 여름호(105호)": "2022 review, Korean Theatre Review, Summer 2022 (no. 105)",
    "2021 리뷰, 『연극평론』 2021 가을호": "2021 review, Korean Theatre Review, Autumn 2021",
    "2012 리뷰, 이정만": "2012 review by Lee Jeongman", "2012 언론보도 및 리뷰 모음": "2012 press and review collection",
}

YS = ("History Dispute Project: a three-year project that rejects the victors' point of view and rewrites history from our own. "
      "Throughout 2024 Green Pig staged one performance a month, each starting from an event of the same month a year earlier. ")

INTRO = {
    "71": "Mary came from Vietnam to Korea dreaming of becoming a K-pop idol. What awaits her is not a glittering stage but Club 'Proud' in Dongducheon. A story set in the camptown that grew around the U.S. military base in Dongducheon. Winner of the 2025 ARKO × Byeoksan Playwriting Award.",
    "70": "In September 1982 a massacre takes place in the Palestinian refugee camps of Beirut, Lebanon. Jean Genet, who was there, walks through Shatila right after the massacre and writes \"Four Hours in Shatila.\" In 2026, unable to enter Gaza themselves, the performers of Wrath walk into Genet's text and draw the landscape of the massacre with their bodies. The work exposes us, who do not belong to that landscape and so cannot help but stand as accused: us, standing before Gaza.",
    "69": "Not Doing Theater: Fool-Run. A gathering to read and try out a play by Antonio Buero Vallejo together. The story begins when a new student, Ignacio, arrives at a school where blind students live as if they could see.",
    "68": "A work that refuses the coming-of-age narrative of youth and puts forward \"the impossibility of growing up.\" It takes apart the linear, well-behaved story structure familiar from youth theater and turns it into an experimental play.",
    "67": "A work that began with the thought, after the martial law declaration of December 2024, that the story of its instigators had to be told. Drawing the villains sometimes roughly as demons and sometimes as ridiculous third-rate comedians, it tries to record in theater a history that must not be forgotten.\n\nYeol, born on the day a comet fell, decides amid his parents' expectations to become a righteous prosecutor. After failing the bar exam eight times he studies nothing but the Constitution for nine years, becomes a \"Constitution master,\" and enters the center of power; passing through the VIP room, the master monk Mangong and Juliet, he is gradually consumed by madness and becomes president. In the end he declares martial law and tries to seize the city. The play is built from the deflated conversations of theater people watching all of this, and the line between reality and fiction collapses.",
    "64": YS + "December. Begun in mid-December 2023, before the month had ended, at a point when no one could know what would happen or which history would be told.",
    "2024-11": YS + "November. On the longest night of the year, five creators write out the everyday text called \"I\": the I who is a perpetrator of discrimination and exclusion. A character analysis of eleven months, written at the height of winter.",
    "63": YS + "October. We catch ourselves, when there is someone we hate, searching the mass media for clues that make it all right to hate them. Starting from the powerful \"aura\" that mass media produces, the piece rereads an event of October a year earlier.",
    "2024-09": YS + "September. It began with the word \"communist totalitarianism.\" Accident or incident? Victim or casualty? The word that wins the clash takes the power. Repeating collisions between statements, the piece casts doubt on the way history is made in a language someone else leads.",
    "62": YS + "August. Taking part in the Jamboree requires a fee, a uniform and plenty of gear. At prices that high, some boys start camping on their own just to get a taste of it from afar. The piece sets the August 2023 Saemangeum World Scout Jamboree fiasco against people enjoying summer outside it.",
    "2024-07": YS + "July. Since 2017, when I started doing theater, every July I have been performing or rehearsing. Can that routine and everyday life become history? Devised by Kang Boreum with Green Pig's performers.",
    "61": YS + "June. In June 2023 Park Hyunji had to move out of the house she had lived in since 1995 because of redevelopment. That same month, police and city hall faced off over road use at the Daegu Queer Culture Festival. A story about private space, public space and their histories.",
    "2024-05": YS + "May. People or anything else, a sigh a second ago or an explosion 13.8 billion years ago: everything leaves traces. A joint research project declaring that only the traces of everything are real history, so that selected history cannot pass itself off as reality.",
    "60": YS + "April. The body reacts sensitively to its surroundings, and the history of one's life piles up in the body. The piece examines the record the body accumulated over a year, between April 2023 and April 2024, and tries to wake a body stiffened by habit.",
    "59": YS + "March. Inspired by Sero, the zebra that escaped from a zoo in March 2023 and was caught three and a half hours later, this is the story of sheep who step outside their peaceful ranch. Borrowing the mouths of non-humans, it asks about the right to refuse and resist, for humans and non-humans alike who live domesticated lives.",
    "2024-02": YS + "February. Who makes \"great figures,\" and why? Who wrote the biographies we read as children? Based on actor Lee Kiseok's February 2023, the piece traces the process by which a great figure is \"made to be born.\"",
    "58": YS + "January. History is the record of the moments when our bodies meet the world, and must be understood as a verb, not a noun. In history, shame tends to fall to survivors and victims rather than perpetrators. The piece records situations of that shame.",
    "53": "A one-act program combining The Mountain Speaks, winner of the 2023 Busan Ilbo Spring Literary Contest for drama, and the short play We Are Harmonious Flowers. The Mountain Speaks is a picaresque in which flawed characters on three mountains in different times move toward what they each want; We Are Harmonious Flowers is about lovers who endlessly repeat parting and reunion.",
    "52": "During the Japanese occupation, an independence fighter occupies the top of a wooden telegraph pole, determined not to go to Manchuria but to stay on this land and remember everything that happens. The occupation passes on to a sergeant occupying an ammunition depot, a believer occupying a confessional, a worker climbing onto a factory roof and an activist up a tree to stop development. Across a hundred years unfold the stories of occupiers, or extras.",
    "50": "On Christmas, a matricide takes place in Choeun-dong. Siyeon, charged with killing her mother, will not speak. In her delusions she becomes Kate, a psychiatrist caring for a patient named Diana and sparring with her colleague Farren, but the tragedy of reality seeps into her head. In scenes where delusion and reality overlap, the work portrays a slice of an age in which a survivor of child abuse who committed parricide lives alongside those who looked away from the abuse or forgot it.",
    "47": "The work deals with social traumas of modern Korean history that happened in April. At a station where the family of a Sewol ferry survivor stays, victims of Jeju 4.3 in 1948, the April 19 Revolution of 1960 and the Sabuk uprising of April 1980 gather one by one. A quiet work of mourning that looks at people who could not catch the bus called history and were left behind like traces. Jung Yujin's first production as director.",
    "45": "In front of Pagoda Park, among the old men, middle-schooler Homi holds a picket sign demanding lower prices. Her family: a grandfather with a secret, a mother blinded by a love that left, and a flasher she does not want to call dad. Her friend Gungjeon is fed up with a mother who only makes money. At the peak of adolescence, an incident cuts across two crooked families. A \"play with songs\" about the feeling of chasing one love for a lifetime, and the gaze that calls it obsession and intervenes.",
    "43": "Every year North Korean wooden boats are found on the east coast and on Japan's shores, and people cross the military line bare-bodied, \"swimming defections\" south and \"swimming defections\" north. The work focuses on the desperation of those who swim and board the boats, and on the contradictory attitudes of the people around them. It depicts today's Korea, where an unforgettable history, those who live forgetting it and those who use it coexist. Winner of the 9th Byeoksan Playwriting Award.",
    "17": "Sets the paradox of civilization's progress and humanity, represented by \"shoes,\" against Yoon Yeongseon's \"tree.\" Over Yoon's poetic, melancholic language, short episodes such as \"Monkey's Flower Shoes,\" \"Fetal Chatter\" and \"Contract\" cross at a quick pace. On a mountain of waste piled from garment-factory scraps, it depicts nuclear power, unstoppable desire and capital, and a collapsing civilization through the eyes of \"a fetus that does not want to be born.\" It began from Yoon's seven-page draft and went through devising and Jeon Sunghyun's additions and restructuring; first staged at the 2012 Yoon Yeongseon Theater Festival and revived ten years later. The start of Green Pig's \"e (environment) trilogy.\"",
    "35": "Moving between a Pyongyang reunified under a federal system in 2048 and the present of 2017, the story digs into the desires and conflicts tangled between South and North. Through a tightly constructed play in which the spell of capitalism and human greed are knotted and unravelled, it asks again about the reality of division and our future. Winner of the 7th Byeoksan Playwriting Award.",
    "13": "A renowned doctor swaps the brains of Sangdo, the simple-minded son of a rich family, and Mugil, a poor but brilliant country youth, and chaos follows. Without altering Jin Uchon's 1945 play, the production adds B-movie thriller staging, a chorus of pro-Japanese songs and a news article reporting \"the happy ending of the brain surgery,\" so that the text itself is objectified and looked at. Yoon Hansol calls this approach \"self-contradictory comedy.\"",
    "40": "Forty-five scenes for two people. The scenes have no order, and the place where each conversation happens is its title. In different places, different characters talk about different subjects such as dream interpretation, math problems and blind dates. Instead of looking for heroes, a play that tries to think the contemporary as contemporary, an age that is neither anyone's nor anything's.",
    "38": "Redefines contemporary labor through the keyword \"unemployment.\" It asks questions aimed at reclaiming labor not as a commodity but as a right to become a human being and a citizen.",
    "19": "While the events of Shakespeare's Othello unfold offstage, a story of the \"hidden schemes\" of three women, Desdemona, Emilia and Bianca, in a back room of the palace. Paula Vogel turns Shakespeare's women from innocent victims of men into people who act in the face of their fates, overturning the tragedy with sharp satire and comic transformation.",
    "03": "A play built from stories drawn from the genre paintings of the late Joseon painter Hyewon Shin Yun-bok. The death-bound love of the gisaeng Haeeosu and the scholar Suseok who is obsessed with her, the love that abandons everything of Seohui, deserted by her husband, and Huiyun who sets out with her, and the story of the maid Dallae who loves in order to live together, follow and cross one another like the pages of an album. The original title was Where Are You Now.",
    "02": "A riverbank at dawn: a father, a son and big suitcases. A child who left the forest and his family and crossed the river for a better life suffers unfair treatment and job loss in a strange land, and goes looking for the factory where Muhammad works with the address his father gave him. From the Koreans who left for the henequen plantations of Mexico a hundred years ago to today's migrant workers, a story that follows, sees off and welcomes the footsteps of those who leave.",
    "25": "A city sunk under water. On one side stands a dam holding back the water; the other is open to the sea. On the last remaining island live the people who rule; on rooftops flooded with water live the ruled. Disasters never stop, so why doesn't the world end? To find the answer, a thought experiment that locks the world inside the theater, causes disasters and watches how people behave in it.",
    "21": "An adaptation, translated from the English version, of The Investigation, the documentary play Peter Weiss wrote from the records of the Frankfurt Auschwitz trials. It follows the form of documentary theater, minimizing artistic technique and putting the testimony itself onstage.",
    "48": "For years Zarina has been writing a novel about Islam and women. Her father Afzal, who runs a large taxi company in Atlanta, secretly posts his elder daughter's photo on a Muslim dating site to find her a husband, and Eli, a white convert to Islam, comes to meet her. A year later Zarina finishes a novel about the origins of the hijab, and the family who read the manuscript reconsider the doctrines and values they had followed. A comedy borrowing the character structure of Shakespeare's The Taming of the Shrew.",
    "51": "Starts from a hypothetical scenario in which Malaysia, the Philippines and Korea unite politically and economically to found a solidarity state, MA-PHI-KO. The three countries, which have all lived through colonial rule, dictatorship and censorship, hold an election for the new nation's leader, and as the candidates' stories gain logic and persuade someone, the piece explores the mechanics of fake news. Part of the Fake News Project.",
    "04": "Before the show the audience receives a cassette tape recording texts about God, and plays it together when the performance begins. Prerecorded lines and the performers' lines sound simultaneously or in turn, and text, movement, live music and song mingle like a carnival. Attempting a philosophical and scientific examination of religion and God's existence through performance, it questions God's existence by doubting the very means of communication through text, space, movement, music, light and video.",
    "06": "A story of triplets in seven scenes: they must meet but are apart, together yet separated. Lovers, North and South, citizens of the world and our history unfold. The sixth production in Seondol Theater's series \"Standing at Seondol.\"",
    "11": "Jeon Huibok, a former army general with dementia; his combative son Jeon Gangdon; a mother obsessed with getting her daughter into medical school; a son who calls himself progressive; and a daughter who wants to go to France. Into their luxury apartment comes Bok Gilsun, a housekeeper from Yanbian, whose goals are to find her daughter, out of touch in Korea, and to earn money for her injured son's surgery. Starting from the likeness between a family and the society around it, it depicts the Jeon household and the cities of the South heading toward ruin like two clocks.",
    "14": "Thirteen scenes in which the story or statements of serial killer Myeongbo continue discontinuously, interrupted by statements from gangsters, prosecutors, chaebol executives, a government spokesperson and the murder victims. A serial play about \"those who wreck\" community, nature, morality and language, and a political comedy jeering at the powerful. But the jeer finally comes back to us, steeped in fetishism.",
    "16": "The second work in Green Pig's \"artist series,\" which looks into the lives of Korean artists. After Anyway, Baek Seok, it takes up Na Hye-seok, Korea's first Western-style woman painter and an artist rejected by her time, as a monodrama. In the life of Na, who went from a rising painter to a thinker who rebelled against male society and to a homeless invalid abandoned by everything, it focuses on the contradictions shown by the gap between her ideas and her work. Selected for the Gyeonggi Cultural Foundation's promising artist project.",
    "08": "Taking \"war\" as its theme, it speaks through soil about the silent pain that has faded beneath the land we live on and about senses that persist, repeat and are forgotten. The third work in Green Pig's series of \"relentless reflections on form,\" it combines acting, music, video and visual art rather than realizing a play script, expressed through the tracing and juxtaposition of severed events, images and oral testimonies. Through testimonies of repressed memory it faces historical events and calls back and mourns those who died wounded, out of unrecorded history.",
    "15": "A family lives in a shoe-repair stall. Jinro's dad and his elder brother, who drink every day waiting for war to really break out; the brother's girlfriend, Agassi; a mother who left home to get double-eyelid surgery; and Grandma Gollum, who keeps the family alive by picking lettuce, squash and peppers from other people's gardens and flowerbeds to sell. In Gollum's mouth are the family's entire fortune: three gold teeth. Like grass that barely sprouts between the paving blocks of the city, the story of an organic family living not in a solid house but in the open. The first work of ARKO's \"Spring Writer, Winter Stage 2012.\"",
    "09": "A \"concertrama\" made by Green Pig and the band Yalgaedeul, in which a concert and a drama put on a show on one stage. Presented by the Seoul Foundation for Arts and Culture, co-produced by Namsan Arts Center and Green Pig.",
    "07": "A woman in her late twenties throws herself onto subway tracks and dies. All that identifies her is a ring and a greeting card; the CCTV footage has vanished, and the high-school girls who witnessed it left before the police arrived. At the same hour, a confrontation over a marriage-fraud case continues at a police station. As seemingly unrelated incidents are woven into one, the play reveals how we come to stand at the end of a tangled skein of guilt regardless of our intentions, as a frog dies from a stone thrown carelessly.",
    "01": "December 1931, a restaurant in the French Concession of Shanghai. Kim Ku and Lee Bong-chang are plotting to kill the Japanese emperor. Just as Bong-chang, with a great purpose in mind, is about to leave, unexpected circumstances keep postponing the attempt, and each time news arrives that the attempts of comrades sent earlier have failed. Why do the bombs always fail to explode? An action drama that leaps across the times and places of Kim Ku, Lee Bong-chang, Yun Bong-gil and those who tell their stories. Green Pig's first work.",
    "20": "Based on Anton Chekhov's short story \"Terror,\" written after his journey to Sakhalin, a play that newly recasts the story's narrator \"I\" as Chekhov himself. Back from Sakhalin, Chekhov visits his friend Silin, who runs a country farm: Silin's wife Marie, whom Chekhov knew before her marriage; the servant Gavrila, once dismissed for his drinking; and Silin, who loves a woman who despises him. Through people confused before incomprehensible lives, it explores human nature and the essence of life.",
    "26": "In 2012, as Jochiwon-eup in Yeongi County, South Chungcheong, was being turned into Sejong Special Self-Governing City, land prices soared and the town was booming. Against this backdrop the play rewrites Shakespeare's Hamlet. With Koreanized characters like \"Haemun\" and \"Opiri,\" thick Chungcheong dialect, ssireum wrestling, shamanic rites and a play within a play, it pokes comically and sharply at the wounds that development policy and fetishism have left on our society. Motifs of \"two\" such as doubling, twins, repetition and mirrors make up its form and structure. Winner of the 4th Byeoksan Playwriting Award, 2014.",
    "05": "A work made to mock and satirize to the full the blindness and undemocratic nature of the power of May 1980. Though full of absurd and comic elements, the performance does not openly reveal that its target is \"the power of May 1980.\" The protagonists keep producing laughter through ridiculous accidents, and through that laughter the audience meets the May 18 Democratic Uprising from a new angle. Part of Arko Arts Theater's \"Praise of Creation.\"",
    "10": "A work reconstructed from a series of humanities texts on narcissism, including Freud's \"On Narcissism: An Introduction.\" Starting from concepts such as autoeroticism, the sexual ideal and the ego ideal, it portrays a person who, despite ample sexual knowledge and desire, cannot form relationships with others.",
    "12": "Tracing the life of the genius poet Baek Seok, it looks for the joints where life becomes art and art becomes life. We will remember not the poems Baek Seok left but the life he left. The first work in Green Pig's \"artist series.\"",
    "18": "Resisting state power through the case of photographer Park Jeonggeun, who served a prison sentence for violating the National Security Act. The performers watch and imitate Okin Collective's video Seoul Decadence, featuring Park, who had to learn acting to stand in court, and an actor, and they talk about the things one performs to be \"rehabilitated,\" like smiling and handing out gimbap and cigarettes.",
    "22": "The actors get angry at every single line throughout. A work that reads situations which can only make you angry before reading the emotions, capturing Korean society's problems of poverty, old age and housing through playwright Yoon Mihyun's distinctive eye.",
    "23": "A work interpreting the pansori Jeokbyeokga through the theme of \"tradition.\" It stages the very process of understanding and expressing pansori: finding the meanings of words to learn Jeokbyeokga, learning dialect, and imitating gestures with exaggeration. In the attitude due to tradition, the performers kneel throughout the show, and if a phone rings or vibrates in the audience, the performance stops. It began at the autumn festival of Hyehwa-dong 1beonji's 5th members and was invited to TPAM in Yokohama in 2016.",
    "24": "Based on George Orwell's novel 1984, it starts from the fact that the future Orwell foresaw was the year 1984. Between a 1984 already lived through and a future yet to come, it gauges our coordinates and seeks the paths of life an individual can take within the whole called the nation or society. A work that showed unbridled imagination in social statement through aesthetic experiment.",
    "27": "\"Chijeong\" (passionate entanglement) is a pun that reverses the syllables of \"jeongchi\" (politics). It shows the power relations hidden behind so-called \"wrong encounters,\" and the lack and excess, violence and disconnection of modern people.",
    "28": "A company that has agreed to perform Oh Jongwoo's A Sculptor and a Detective at a festival of banned plays. During rehearsals the director suddenly disappears, and with only the company members left it becomes unclear whether the show can go on. Part of \"Bill of Rights 2016: Censorship Dismissed,\" which responded to the theater blacklist scandal.",
    "29": "\"What is acting? Why do I act?\" Fourteen actors deliver audition-style monologues, then answer, desperately and honestly, the question of why they act.",
    "36": "Individual anxiety arises from social rules, conventions and standards and appears in the body as symptoms. An immersive performance that explores cases of anxiety such as the violence of the gaze, average income, appearance and pressure to succeed through the performers' bodies, and, by way of Michel Foucault's \"utopian body,\" lets the audience sense the gallery's floor and walls, light and noise strangely with their own bodies. Made with texts by the poet Jang Suyang.",
    "32": "A generation that grew up through the IMF financial crisis of the 1990s talks about the past twenty-odd years of Korean society. Many words show where young people stand now, like \"N-po generation\" and \"working poor.\" Wastepaper, which can be a means of livelihood for the poor, itself symbolizes poverty in Korean society today. The director and performers went out to collect wastepaper and interviewed young people in their twenties and thirties, and on that basis the work looks back on the experience of the financial crisis and examines the discrimination and competition pervading Korean society. Selected for Doosan Art LAB 2019.",
    "34": "A sequel to The Way of Story, the Way of Song – Demo Version (2014). After pansori, this time it explores Gong Ok-jin, master of byeongsin-chum (the \"cripple dance\"), and the one-person changmu-geuk. Starting from the idea of whether byeongsin-chum could be learned through a game using a kinetic sensor, it attends to Gong Ok-jin through the Japanese occupation, liberation, the Korean War and her changgeuk troupe years, and after she became known to the public through her Space Sarang performances. Following what the kinetic sensor can and cannot read, it \"presents\" byeongsin-chum in the now, and Gong's students appear onstage. Part of the 2018 Namsan Arts Center season and an official Korean selection of the 25th BeSeTo Festival.",
    "37": "A delivery job, taken because it was supposedly easier than other work and paid as much as you put in. But accidents keep happening during deliveries, and each time he wakes up it is the moment just before the accident again. Part of the 2019 Yeonwoo Mudae Propaganda Series on the theme of \"labor,\" shining a light on places we may have glimpsed or never seen.",
    "41": "Jeanette Winterson's GODBLOG, commissioned by London's Bush Theatre for the 400th anniversary of the King James Bible, brings Genesis into 2011 Britain with the premise that God is on Twitter. This production rebuilt it around the questions \"What if a God in human form were Korean rather than a white man?\" and \"If God were in Korea, what would God tweet?\" It interprets our old culture through the Bible, the foundation of Western culture, and examines the Korean way of thinking through God's eyes.",
    "42": "About how fake news is made and spreads and the phenomena it causes. Misinformation that spread like an epidemic during COVID-19, rumors that amplify hatred and discrimination, stock-market tip sheets and stories in messenger apps. In a world full of fake news, it asks what we should believe and how we should live. The second work of the Fake News Research Project.",
    "44": "Where do actresses go when they have children? Why do they disappear? Can pregnancy, childbirth, child-rearing and doing theater coexist? A fairy tale that does not end with \"they lived happily ever after,\" looking into the hearts of people who were swept up one day by a sudden whirlwind and dropped into a world they had never known, and who, having barely left Kansas, choose to go back to Kansas.",
    "46": "A promenade performance through Ipjeong-dong in Euljiro, which is disappearing to redevelopment. Following a curator through the alleys, the audience meets objects placed here and there, performers turned into statues and exhibited sounds, and passing through performances and happenings in which several times are mixed, they \"sense\" a vanishing space. The performers become curators, moving statues and excavators of ruins, making a \"living museum\" that holds on to fading traces.",
    "49": "Gretel, abandoned by her parents and waiting alone in the forest for her brother; the Ugly Duckling, driven out of the community and wandering; Pinocchio, setting off to find Geppetto. The three discover that they share being abandoned and unwelcome, and as they try to carry on the story as the author wrote it, they meet a mysterious figure. Through abandoned children spreading learned hatred to others and the process of overcoming it, the piece turns over the world of fairy tales we have taken for granted.",
    "30": "A story of children abused by their stepmother who dream of seeking asylum. It recalls a nation ruled by unjust power with evil intentions, and the children who, far from breathing under it, could only disappear. Part of the invited program \"Sewol 2017\" (2017.7.6–8.13) by the 6th members of Theater Lab Hyehwa-dong 1beonji, co-produced by Green Pig.",
    "31": "\"Will you still come forward as a whistleblower?\" A performance made to put this question to the audience. A corporate executive who finds a massive slush-fund ledger, a professor who learns of a colleague's admissions fraud, a Red Cross employee who discovers mismanagement of blood supplies, a high-school student who refuses the school's religious coercion…. Internal whistleblowers who exposed injustice try and fail to fix things inside their organizations, finally go public, and face pressure and attacks from the press, are pushed out of their organizations and sometimes lose their health and families. Within a non-dramatic structure, the piece makes a triple conflict, inner struggle, ostracism inside the organization and distortion by society and the press, erupt in succession.",
    "54": "It begins from the origin myth of the Göktürks, the tale of a wolf that raised a child whose ankles had been cut off by feeding him meat. Dan, who lost his ankle when his right foot was pulled into a conveyor belt while working for a subcontractor at the Seohae thermal power plant, and Zaya, who came from Mongolia and works at a moving company. Through the love of two people who begin to care for each other's bodies that no one else cares about, playwright Kang Hoongu speaks of industrial accidents among young irregular workers and the problems of migrant workers, and asks about the \"love\" needed for a severed body to become a new body.",
    "55": "A photograph records, in a single image, a moment in which events and emotions are intricately mixed, and we accept it as reality. To a gaze that has lost imagination in a world full of images, the piece adds the gaze of the Little Prince, who sees the world with the eyes of the heart, and talks about the essence of photography. Starting from Cartier-Bresson's \"decisive moment,\" it asks whether documentary photography can be a window onto the world, and whether we can experience the world through photographs.",
    "57": "A perfect plot dreamed in an unfinished world. Nightmares exclude no one. Plots become perfect through exclusion. Instead of following a protagonist swept up in an event, the work tries to bind together a world in which an event and its outside overlap. While Hamlet pretends to be mad for revenge, the people outside the castle must have been trembling at Fortinbras's march. From the thought that when we gaze into a plot the plot also gazes into us, it sets up the hypothesis that a world interpreted through cause and effect is not the only world.\n\nOne day the protagonist wakes and, believing that last night's nightmare holds clues to the things ruining the world, quits his job. The \"Nightmare Removal Association\" he founds interprets each new nightmare to decide what to remove: trash on hiking trails, the urge to cut in line, selfishness between friends. The association's peaceful activities are praised in the press and on social media. Then the new nightmares stop, and a member, interpreting a target to the extreme, commits \"that incident\" and is arrested. The play starts here. The protagonist holds a press conference to convey his sincerity, but public opinion turns and the association splits. Then a new nightmare comes to him.\n\nA work by playwright Jeon Sunghyun, who has experimented with theatrical form through <a href=\"w40.html\">Contemporaries</a> and <a href=\"w52.html\">Extra Chronicles</a>. The more it chooses the most unnatural ways theater can work, with no protagonist, deliberately disrupted narrative and the boundaries of the theater undone, the closer the world onstage comes to reality.",
    "65": "Through Yeom Sang-seop's early short stories, a self-portrait of modern Koreans. Just as Yeom saw Japanese imperialism as something to be overcome, the piece views capitalism as something to be overcome and reflects the age we live in against the Japanese occupation period. The stories Dark Night and Rice were read as theatrical readings of the fiction itself, while Autumn Night (Jeon Sunghyun) and Mamma (Ju Eungil) were read as plays rewritten for today, with a discussion featuring commentary and a lecture by Lee Jongho.",
}

# 기타 공연·낭독 (아카이브 아래)
OTHER = {
    "1963_2007, 그곳": "1963_2007, That Place", "20분간의 재림": "The Twenty-Minute Second Coming", "파수꾼": "The Watchman",
    "죽음의 집": "House of Death", "비밀친구": "Secret Friend", "철수연대기": "Cheolsu Chronicles", "안산순례길": "Ansan Pilgrimage Road",
    "점과 점을, 잇는 선. 으로 이루어진, 육면체. …": "A Hexahedron, Made of, Lines. Connecting Dot to Dot. …",
    "안산순례길 2016": "Ansan Pilgrimage Road 2016", "Teh Internet is Serious Business": "Teh Internet is Serious Business",
    "안산순례길 2017": "Ansan Pilgrimage Road 2017", "오후만 있던 일요일": "A Sunday With Only an Afternoon",
    "안산순례길 2018": "Ansan Pilgrimage Road 2018", "워 아이 차차차": "Wo Ai Cha-Cha-Cha",
    "희미한 옛사랑의 그림자": "Shadow of a Faint Old Love", "안산순례길 2019": "Ansan Pilgrimage Road 2019", "호텔사회": "Hotel Society",
    "여행의 새발견": "Rediscovering Travel", "엑스트라연대기": "Extra Chronicles", "나는 유교다: 더 레알 유교": "I Am Confucianism: The Real Confucianism",
    "나무는 신발가게를 찾아가지 않는다": "Tree Won't Seek for Shoe Store", "등산하는 아이들": "Children Who Climb Mountains",
}
OTHER_WORD = {"낭독": "reading", "쇼케이스": "showcase", "온라인 낭독회": "online reading", "10분희곡 페스티벌": "10-Minute Play Festival"}

ABOUT = ("A performance company made by people with the conviction that ideas change the world and with burning sensibility. "
         "We are people who came together to make theater that diagnoses a civilization proceeding without doubt, or without doubting. "
         "We are people who came together to make theater that thinks about progress in subject matter and artistic form. "
         "Green Pig's work is a manual, or a tool, for resistance or exodus.")
SLOGAN = "Subversive imagination, since 2006."
