# 영어판(en/ 폴더) 만들기. build.py 끝에서 run(globals())로 불린다.
# 번역 자료는 works_data_en.py. 새 작품을 넣었는데 영어 제목·소개가 없으면 한국어 제목을 로마자로 옮겨 임시로 쓴다.
import os, re, json, html
import works_data_en as E

SURNAME = {
    "김": "Kim", "이": "Lee", "박": "Park", "최": "Choi", "정": "Jung", "강": "Kang", "조": "Cho", "윤": "Yoon", "장": "Jang",
    "임": "Lim", "한": "Han", "오": "Oh", "서": "Seo", "신": "Shin", "권": "Kwon", "황": "Hwang", "안": "Ahn", "송": "Song",
    "류": "Ryu", "유": "Yoo", "홍": "Hong", "전": "Jeon", "고": "Ko", "문": "Moon", "양": "Yang", "손": "Son", "배": "Bae",
    "백": "Baek", "허": "Heo", "남": "Nam", "노": "Noh", "하": "Ha", "곽": "Kwak", "성": "Sung", "차": "Cha", "주": "Ju",
    "우": "Woo", "구": "Koo", "민": "Min", "나": "Na", "진": "Jin", "지": "Ji", "엄": "Eom", "채": "Chae", "원": "Won",
    "천": "Cheon", "방": "Bang", "공": "Gong", "현": "Hyun", "함": "Ham", "변": "Byun", "염": "Yeom", "여": "Yeo", "추": "Choo",
    "도": "Do", "소": "So", "석": "Seok", "선": "Sun", "설": "Seol", "마": "Ma", "길": "Gil", "연": "Yeon", "위": "Wi", "표": "Pyo",
    "명": "Myung", "기": "Ki", "반": "Ban", "왕": "Wang", "금": "Keum", "옥": "Ok", "육": "Yuk", "인": "In", "맹": "Maeng",
    "제": "Je", "모": "Mo", "탁": "Tak", "국": "Kook", "은": "Eun", "편": "Pyeon", "용": "Yong", "예": "Ye", "경": "Kyung",
    "봉": "Bong", "부": "Boo", "가": "Ka", "태": "Tae", "형": "Hyung", "두": "Doo", "감": "Kam", "동": "Dong", "온": "On",
    "호": "Ho", "승": "Seung", "상": "Sang", "육": "Yuk", "범": "Beom", "왕": "Wang", "라": "Ra", "빈": "Bin", "목": "Mok",
}
DOUBLE = {"남궁": "Namgung", "황보": "Hwangbo", "제갈": "Jegal", "선우": "Sunwoo", "독고": "Dokgo"}

try:
    from korean_romanizer.romanizer import Romanizer
    def _rr(s): return Romanizer(s).romanize()
except Exception:            # 라이브러리가 없으면 아주 단순하게 (음절별)
    def _rr(s): return s

def roman(name):
    """사람 이름 → 영문. NAME에 있으면 그것, 아니면 성 + 이름(로마자)."""
    name = name.strip()
    if name in E.NAME: return E.NAME[name]
    if name in E.ORG: return E.ORG[name]
    if not re.search(r"[가-힣]", name): return name
    if re.fullmatch(r"[가-힣]{2,4}", name):
        for d, r in DOUBLE.items():
            if name.startswith(d) and len(name) > 2:
                return r + " " + _rr(name[2:]).capitalize()
        s = SURNAME.get(name[0])
        if s: return s + " " + _rr(name[1:]).capitalize()
    return " ".join(w.capitalize() for w in _rr(name).split())

def show_en(key):        # '박현지(배우)' → 'Park Hyunji (actor)'
    m = re.match(r"^(.+?)\((.+)\)$", key)
    if m:
        return roman(m.group(1)) + {"배우": " (actor)", "사진": " (photographer)"}.get(m.group(2), "")
    return roman(key)

def role_en(k):
    years = re.findall(r"20\d\d", k)
    sub = re.findall(r"〈([^〉]+)〉", k)
    k = re.sub(r"\([^)]*\)|〈[^〉]+〉|20\d\d", "", k).strip()
    if k in E.ROLE: out = E.ROLE[k]
    else: out = " & ".join(E.ROLE.get(p.strip(), p.strip()) for p in k.split("·"))
    if sub: out += ", " + " / ".join(E.SUBTITLE.get(s, s) for s in sub)
    if years: out += " (" + years[0] + ")"
    return out

def low(r):   # 참여 기록의 역할은 소문자로 (고유명사로 시작하면 그대로)
    return r if r.split()[0] in ("Pansori", "Mongolian", "Yanbian", "DJ", "PD", "Band") else r[0].lower() + r[1:]

def title_en(slug, ko=None):
    t = E.TITLE.get(slug)
    if ko and ko in E.TITLE_VARIANT: return E.TITLE_VARIANT[ko]
    return t or " ".join(w.capitalize() for w in _rr(ko or "").split())

def esc(s): return html.escape(s, quote=False)

def run(g):
    SITE = g["SITE"]; EN = os.path.join(SITE, "en"); os.makedirs(EN, exist_ok=True)
    rows, works, order, people, EXTRA = g["rows"], g["works"], g["order"], g["people"], g["EXTRA"]
    page, anchor, person_key, venues_of, vid = g["page"], g["anchor"], g["person_key"], g["venues_of"], g["vid"]
    by_venue, writers, dkey, start_key, pos = g["by_venue"], g["writers"], g["dkey"], g["start_key"], g["pos"]
    T = {s: title_en(s) for s in order}

    def venue(v):
        return "; ".join(E.VENUE.get(x.strip(), x.strip()) for x in re.split(r";\s*", v))
    def names(text, role=""):
        """'고경철, 권효은' 같은 이름 목록 → 영문 이름(참여 기록 링크 포함). 괄호 속 배역은 뺀다."""
        out = []
        for n in re.split(r",\s*", text):
            n = n.strip()
            if not n: continue
            if n in E.ORG: out.append(E.ORG[n]); continue
            n2 = re.sub(r"\(.*?\)", "", n).strip()
            extra = ""
            if n2.endswith(" 외"): n2, extra = n2[:-2], " et al."
            if n2.endswith(" 외삼촌"): n2, extra = n2[:-4], "'s uncle"
            parts = n2.split("·") if re.fullmatch(r"[^\s·]+(·[^\s·]+)+", n2) and all(re.fullmatch(r"[가-힣]{2,4}", p) for p in n2.split("·")) else [n2]
            for p in parts:
                key = person_key(p, role)
                r = roman(p)
                out.append((f'<a href="who.html#{anchor(key)}">{r}</a>' if key in people else r) + extra)
        return ", ".join(out)
    def credit_line(text):
        """PERFORMANCES의 작·연출 줄 → 'Playwright: …<br>Director: …'"""
        text = re.sub(r"〈[^〉]*〉\s*", "", text)
        lines = []
        for piece in re.split(r",\s*(?![^()]*\))| · ", text):
            piece = piece.strip()
            m = re.match(r"^(\S+)\((.+)\)$", piece)
            if m: lines.append(f"{role_en(m.group(1))}: {names(m.group(2))}"); continue
            if piece in ("공동창작", "공동구성", "공동재구성", "그린피그 공동창작", "그린피그 공동구성"):
                lines.append({"공동재구성": "Co-adapted"}.get(piece.split()[-1], "Devised by Green Pig")); continue
            w = piece.split()
            if len(w) >= 2:
                who = " ".join(w[:-1])
                lines.append(f"{role_en(w[-1])}: " + ", ".join(names(x, w[-1]) for x in who.split("·")))
            else:
                lines.append(esc(piece))
        return "<br>\n".join(lines)

    HEAD = ('<!doctype html>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>{t} - Green Pig</title>\n<link rel="stylesheet" href="../style.css">\n')
    def crumb(*parts):
        return '<p><a href="index.html">Green Pig</a> &gt; ' + " &gt; ".join(parts) + "</p>\n"
    def write(name, parts):
        open(os.path.join(EN, name), "w").write("\n".join(parts) if isinstance(parts, list) else parts)
    def perf(r, main):
        s = r["date"]
        if r["title"] != main and r["title"] in E.TITLE_VARIANT: s += f" {E.TITLE_VARIANT[r['title']]}"
        vs = venues_of(r["venue"])
        s += " / " + (", ".join(f'<a href="theaters.html#{vid(v)}">{E.VENUE.get(v, v)}</a>' for v in vs) if vs else venue(r["venue"]))
        if r["note"]: s += " - " + E.NOTE.get(r["note"], r["note"])
        return s

    # ---- 작품 페이지 ----
    for i, slug in enumerate(order):
        w = works[slug]; ex = EXTRA.get(slug, {}); t = T[slug]
        out = [HEAD.format(t=esc(t)), crumb('<a href="archive.html">Archive</a>', esc(t)), f"<h2>{esc(t)}</h2>\n"]
        if os.path.exists(f"{SITE}/w{slug}.jpg"):
            files = [f"w{slug}.jpg"]; n = 2
            while os.path.exists(f"{SITE}/w{slug}-{n}.jpg"): files.append(f"w{slug}-{n}.jpg"); n += 1
            caps = E.POSTER.get(slug, [])
            if len(files) == 1 and not caps:
                out.append(f'<p><img src="../{files[0]}" alt="Poster for {esc(t)}" width="300"></p>\n')
            else:
                cells = []
                for k, f in enumerate(files):
                    cap = caps[k] if k < len(caps) else ""
                    cells.append(f'<span><a href="../{f}"><img src="../{f}" alt="Poster for {esc(t)}' + (f' ({cap})' if cap else "") + f'" title="{cap}" width="200"></a></span>')
                out.append('<p class="posters">\n' + "\n".join(cells) + "\n</p>\n")
        if os.path.exists(f"{SITE}/w{slug}s.jpg"):
            cap = E.PHOTO.get(slug, "")
            out.append(f'<p class="scene"><img src="../w{slug}s.jpg" alt="Production photo of {esc(t)}" width="600" loading="lazy">' + (f"<br><small>{cap}</small>" if cap else "") + "</p>\n")
        if slug in E.INTRO:
            out.append("<h3>About the work</h3>\n<p>" + "</p>\n<p>".join(x.strip() for x in E.INTRO[slug].split("\n\n")) + "</p>\n")
        out.append("<h3>Performances</h3>\n<p>\n" + "<br>\n".join(perf(r, w["title"]) for r in w["rows"]) + "\n</p>\n")
        if "수상" in ex:
            out.append("<h3>Awards</h3>\n<p>\n" + "<br>\n".join(E.AWARD.get(a, a) for a in ex["수상"]) + "\n</p>\n")
        if "크레딧" in ex:
            out.append("<h3>Credits</h3>\n<p>\n" + "<br>\n".join(f"{role_en(k)}: {names(v, k)}" for k, v in ex["크레딧"]) + "\n</p>\n")
        else:
            out.append("<h3>Credits</h3>\n<p>" + credit_line(w["credit"]) + "</p>\n")
        if "리뷰" in ex:
            out.append('<h3>Reviews and articles <small>(in Korean)</small></h3>\n<p>\n' +
                       "<br>\n".join(rev_line_en(rev_en(g["rev"](x))) for x in sorted(ex["리뷰"], key=lambda x: dkey(x[0]), reverse=True)) + "\n</p>\n")
        if "비평" in ex:
            out.append("<h3>Criticism in print</h3>\n<p>\n" + "<br>\n".join(E.CRITIC_NOTE.get(c, c) for c in ex["비평"]) + "\n</p>\n")
        nav = []
        if i > 0: nav.append(f'Previous: <a href="{page(order[i-1])}">{esc(T[order[i-1]])}</a>')
        if i < len(order) - 1: nav.append(f'Next: <a href="{page(order[i+1])}">{esc(T[order[i+1]])}</a>')
        out.append("<hr>\n<p>" + " | ".join(nav) + '<br>\n<a href="archive.html">Back to the archive</a> | <a class="random" href="archive.html">Any work</a></p>\n')
        write(page(slug), out)

    # ---- 아카이브 ----
    years = sorted({r["date"][:4] for r in rows}, reverse=True)
    a = [HEAD.format(t="Archive"), crumb("Archive")]
    a.append("<p>\n" + " | ".join(f'<a href="#y{y}">{y}</a>' for y in years) +
             '\n<br>\n<a href="#other">Other performances and readings</a> | <a href="#awards">Awards</a> | <a href="theaters.html">By theater</a> | <a href="writers.html">By writer</a> | <a class="random" href="archive.html">Any work</a>\n</p>\n')
    all_v = {v for r in rows for v in venues_of(r["venue"])}
    a.append(f"<p>{years[-1]}–{years[0]}: {int(years[0]) - int(years[-1])} years, {len(order)} works, {len(rows)} performance runs, "
             f"{len(all_v)} theaters (5 cities abroad), {len(people)} names in the credits.</p>\n")
    newest = sorted(rows, key=lambda r: start_key(r["date"]), reverse=True)
    for y in years:
        ls = [f'{r["date"]} <a href="{page(r["slug"])}">{esc(E.TITLE_VARIANT.get(r["title"], T[r["slug"]]))}</a> / {venue(r["venue"])}' for r in newest if r["date"][:4] == y]
        a.append(f'<h3 id="y{y}">{y}</h3>\n<p>\n' + "<br>\n".join(ls) + "\n</p>\n")
    oth = []
    for d, title, rest, v, note in sorted(g["other_rows"], key=lambda r: start_key(r[0]), reverse=True):
        tt = re.sub(r"^〈|〉$", "", title)
        en = E.OTHER.get(tt) or E.OTHER_WORD.get(tt, tt)
        word = next((E.OTHER_WORD[k] for k in E.OTHER_WORD if k in rest and k != tt), "")
        oth.append(f"{d} {en}" + (f" {word}" if word else "") + f" / {venue(v)}" + (" - reading" if note == "낭독" else ""))
    a.append('<h3 id="other">Other performances and readings</h3>\n<p>\n' + "<br>\n".join(oth) + "\n</p>\n")
    aw = [
        "2025 33rd Daesan Literary Award, Drama: The Great Battle of the Sheep Ranch (Ju Eungil)",
        "2023 27th BeSeTo Festival, Excellence Award: Tree Won't Seek for Shoe Store",
        "2016 18th Kim Sang-yeol Theater Award (Yoon Hansol)",
        "2016 9th Korea Theater Awards, Best 7 Productions (revival): Ansan Pilgrimage Road 2016",
        "2013 34th Seoul Theater Festival, Young Theater Artist of the Year: Beautiful Companion – Secret Friend (shared)",
        "2012 5th Korea Theater Awards, Best Production: Brain Surgery",
        "2011 2nd Doosan Yonkang Arts Award, Performing Arts (Yoon Hansol)"]
    a.append('<h3 id="awards">Awards</h3>\n<p>\n' + "<br>\n".join(aw) + "\n</p>\n")
    write("archive.html", a)

    # ---- 극장별, 작가별 ----
    tv = [HEAD.format(t="By theater"), crumb('<a href="archive.html">Archive</a>', "By theater"), "<h2>By theater</h2>"]
    for v, rs in sorted(by_venue.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        ls = [f'{r["date"]} <a href="{page(r["slug"])}">{esc(T[r["slug"]])}</a>' + (f' - {E.NOTE.get(r["note"], r["note"])}' if r["note"] else "") for r in rs]
        tv.append(f'<p id="{vid(v)}"><b>{E.VENUE.get(v, v)}</b> ({len(rs)})<br>\n' + "<br>\n".join(ls) + "\n</p>")
    tv.append('\n<hr>\n<p><a href="archive.html">Back to the archive</a></p>\n')
    write("theaters.html", tv)
    WROLE = {"작": "playwright", "원작": "original work", "작가": "writer", "글쓰기": "text", "대본": "script", "글": "text", "작·연출": "playwright and director"}
    wv = [HEAD.format(t="By writer"), crumb('<a href="archive.html">Archive</a>', "By writer"), "<h2>By writer</h2>"]
    for n, ws in sorted(writers.items(), key=lambda kv: (-len(kv[1]), roman(kv[0]))):
        ls = [f'{works[s]["rows"][0]["date"][:4]} <a href="{page(s)}">{esc(T[s])}</a> {", ".join(WROLE.get(x, x) for x in ws[s])}' for s in sorted(ws, key=lambda s: pos[s])]
        nm = f'<a href="who.html#{anchor(n)}">{roman(n)}</a>' if n in people else roman(n)
        wv.append(f"<p><b>{nm}</b> ({len(ws)})<br>\n" + "<br>\n".join(ls) + "\n</p>")
    wv.append('\n<hr>\n<p><a href="archive.html">Back to the archive</a></p>\n')
    write("writers.html", wv)

    # ---- 참여 기록 (영문 이름 알파벳 순) ----
    keys = sorted(people, key=lambda k: show_en(k).lower())
    letters = []
    h = [HEAD.format(t="Credits index"), crumb('<a href="people.html">People</a>', "Credits index"), "<h2>Credits index</h2>"]
    groups = {}
    for k in keys: groups.setdefault(show_en(k)[0].upper(), []).append(k)
    h.append("<p>" + " ".join(f'<a href="#{c}">{c}</a>' for c in groups) + "</p>\n")
    for c, ks in groups.items():
        h.append(f'<h3 id="{c}">{c}</h3>\n<div class="cols">')
        for k in ks:
            items = []
            for s_, roles in people[k].items():
                by_years = {}
                for role, ys in roles.items(): by_years.setdefault(tuple(sorted(ys)), []).append(role)
                for ys, rs in by_years.items():
                    items.append((ys[-1], pos[s_], f'{", ".join(ys)} <a href="{page(s_)}">{esc(T[s_])}</a> {", ".join(low(role_en(r)) for r in rs)}'))
            items.sort(key=lambda x: (x[0], x[1]), reverse=True)
            ko = re.sub(r"\(.*\)", "", k)
            h.append(f'<p id="{anchor(k)}"><b>{show_en(k)}</b> <span lang="ko">{ko}</span><br>\n' + "<br>\n".join(x[2] for x in items) + "\n</p>")
        h.append("</div>")
    h.append('\n<hr>\n<p><a href="people.html">Back to people</a></p>\n')
    write("who.html", h)

    # ---- 사람 (한국어 people.html의 줄을 옮긴다) ----
    pp = open(f"{SITE}/people.html").read()
    RT = {"대표": "Representative", "연출": "Directors", "배우": "Performers"}
    blocks = re.findall(r"<p>\n<b>(.+?)</b><br>\n(.+?)\n</p>", pp)
    pe = [HEAD.format(t="People"), crumb("People"), "<h2>People</h2>\n"]
    for role, line in blocks:
        ns = re.findall(r'<a href="who\.html#([^"]+)">([^<]+)</a>|([가-힣]{2,4})', line)
        items = []
        for a_, label, plain in ns:
            nm = label or plain
            items.append(f'<a href="who.html#{a_}">{roman(nm)}</a>' if a_ else roman(nm))
        pe.append(f"<p>\n<b>{RT.get(role, role)}</b><br>\n" + ", ".join(items) + "\n</p>\n")
    pe.append('<p>\n<a href="who.html">Full credits index</a>\n</p>\n\n<hr>\n<p>greenpig.kr@gmail.com</p>\n')
    write("people.html", pe)

    # ---- 소개 ----
    rot = ('<div class="rotator" aria-label="Works by Green Pig">\n' + "\n".join(f'<a href="{page(s)}">{esc(T[s])}</a>' for s in reversed(order)) +
           '\n</div>\n<script src="../rotator.js" defer></script>\n')
    write("about.html", [HEAD.format(t="About"), crumb("About"), rot, "<h2>Subversive Imagination: Green Pig</h2>\n",
                         f"<p>{E.ABOUT}</p>\n", "<hr>\n<p>greenpig.kr@gmail.com</p>\n"])

    # ---- 첫 페이지 (한국어 첫 페이지의 소식 세 줄을 옮긴다) ----
    ix = open(f"{SITE}/index.html").read()
    news = re.search(r"<!-- 새 소식은.*?-->\n<p>\n(.*?)\n</p>", ix, re.S).group(1)
    nl = []
    for line in news.split("\n"):
        m = re.match(r'(\S+) <a href="w([^"]+)\.html">〈?([^<]*?)〉?</a> / (.*?)(<br>)?$', line)
        if m: nl.append(f'{m.group(1)} <a href="w{m.group(2)}.html">{esc(T.get(m.group(2), m.group(3)))}</a> / {venue(m.group(4))}')
    data = [list(x[:6]) + [T.get(re.sub(r"^w|\.html$", "", x[7]), x[6]), x[7], venue(x[8])] for x in g["today_data"]]
    today = ("<p id=\"today\" hidden></p>\n<script>\n(function(){var P=" + json.dumps(data, ensure_ascii=False) + ";\n"
             "var t=new Date(),Y=t.getFullYear(),M=t.getMonth()+1,D=t.getDate(),open=[],run=[];\n"
             "P.forEach(function(p){if(p[0]>=Y)return;var n=Y-p[0],s=new Date(p[0],p[1]-1,p[2]),e=new Date(p[3],p[4]-1,p[5]),d=new Date(p[0],M-1,D),d2=new Date(p[0]+1,M-1,D);\n"
             "var x=function(k){return k+(k>1?' years':' year')+' ago today, <a href=\"'+p[7]+'\">'+p[6]+'</a> ';};\n"
             "if(p[1]==M&&p[2]==D)open.push(x(n)+'opened ('+p[8]+')');else if(d>s&&d<=e)run.push(x(n)+'was running ('+p[8]+')');else if(d2>s&&d2<=e&&p[0]+1<Y)run.push(x(n-1)+'was running ('+p[8]+')');});\n"
             "var l=open.concat(run).slice(0,2);if(l.length){var el=document.getElementById('today');el.innerHTML=l.join('<br>');el.hidden=false;}})();\n</script>\n")
    write("index.html", [HEAD.format(t="Green Pig").replace("<title>Green Pig - Green Pig</title>", "<title>Green Pig</title>"),
        '<p><button class="night" type="button" title="Switch day and night"><img class="logo" src="../logo.png" alt="Green Pig logo: a pig baring its teeth. Press to switch day and night"></button></p>\n',
        "<h1>Green Pig</h1>", f"<p>{E.SLOGAN}</p>\n",
        '<p>\n<a href="about.html">About</a> |\n<a href="archive.html">Archive</a> |\n<a href="people.html">People</a> |\n<a href="texts.html">Texts</a> |\n'
        '<a class="random" href="archive.html">Any work</a> |\n'
        '<span class="find"><input form="find" type="search" name="q" placeholder="Search" aria-label="Search" enterkeyhint="search" autocomplete="off"><span aria-hidden="true">Search</span></span> |\n'
        '<a href="https://blog.naver.com/greenpig2006">Blog</a> |\n<a href="https://www.instagram.com/wearegreenpig/">Instagram</a> |\n<a href="https://x.com/wearegreenpig">X</a>\n</p>\n'
        '<form id="find" action="search.html" role="search"></form>\n\n<hr>\n',
        "<p>\n" + "<br>\n".join(nl) + "\n</p>\n", today, "<hr>\n\n<p>greenpig.kr@gmail.com</p>\n"])

    # ---- 텍스트 ----
    rv = []
    for r in g["allrev"]:
        slug = re.sub(r"^w|\.html$", "", r["p"]) if r["p"] else ""
        rv.append(rev_en(r, T.get(slug, "History Dispute Project 2024")))
    crit = [roman(w) for w in g["critics"]]
    cnt = g["cnt"]
    groups = {}
    for r in sorted(rv, key=lambda r: dkey(r["d"]), reverse=True):
        groups.setdefault(r["n"], []).append(r)
    static = "\n\n".join(f'<p><b>{(f"<a href={chr(34)}{rs[0][chr(112)]}{chr(34)}>{esc(n)}</a>") if rs[0]["p"] else esc(n)}</b><br>\n' +
                         "<br>\n".join(rev_line_en(r) for r in rs) + "\n</p>" for n, rs in groups.items())
    tx = [HEAD.format(t="Texts"), crumb("Texts"),
          '<p><a href="#reviews">Reviews and articles</a> | <a href="#criticism">Criticism in print</a> | <a href="#essays">Writing on Green Pig</a></p>\n',
          '<h3 id="reviews">Reviews and articles</h3>\n',
          "<p>Links to reviews, criticism and articles about Green Pig's productions. The texts themselves are in Korean.</p>\n",
          '<p class="rvctl noprint" hidden>View: <a href="#" data-v="work">by work</a> · <a href="#" data-v="writer">by writer</a> · <a href="#" data-v="date">latest first</a><br>\n'
          f'Kind: <a href="#" data-k="">all {len(rv)}</a> · <a href="#" data-k="평론">criticism {cnt["평론"]}</a> · <a href="#" data-k="기사">articles {cnt["기사"]}</a> · <a href="#" data-k="관객">audience reviews {cnt["관객"]}</a><br>\n'
          'Critics: <a href="#" data-w="">all</a> · ' + " · ".join(f'<a href="#" data-w="{roman(w)}">{roman(w)} {g["crit"][w]}</a>' for w in g["critics"]) + '</p>\n',
          '<div id="rv">\n' + static + "\n</div>\n",
          "<script>var L={none:'Nothing to show.',other:'Other criticism and articles',aud:'Audience reviews'};var RV=" +
          json.dumps(rv, ensure_ascii=False, separators=(",", ":")) + ",RC=" + json.dumps(crit, ensure_ascii=False) + ';</script>\n<script src="../texts.js" defer></script>\n',
          '<h3 id="criticism">Criticism in print</h3>\n<p>\n' + "<br>\n".join(E.CRITIC_NOTE[k] for k in E.CRITIC_NOTE) + "\n</p>\n",
          '<h3 id="essays">Writing on Green Pig</h3>\n<p>\n2014 <a href="https://www.sfac.or.kr/site/theater/WZ020300/webzine_view.do?wtIdx=10790">Choi Yunwoo, "Uncomfortable Stories, Told Uncomfortably" (Seoul Theater Center webzine Yeongeuk-in, in Korean)</a><br>\n'
          'Park Sanghyun, "Those Who Come, Those Who Go, Those Who Stay" (in the Green Pig portfolio)<br>\nCho Mansu, "Green Pig\'s Uncomfortable Theater" (in the Green Pig portfolio)\n</p>\n',
          "<hr>\n<p>greenpig.kr@gmail.com</p>\n"]
    write("texts.html", tx)

    # ---- 찾기 ----
    idx = []
    for slug in order:
        w = works[slug]; ex = EXTRA.get(slug, {})
        yrs = sorted({r["date"][:4] for r in w["rows"]})
        yr = yrs[0] + (f"–{yrs[-1]}" if len(yrs) > 1 else "")
        nm = " ".join(roman(n) for role, ns in ex.get("크레딧", []) for n in re.split(r",\s*", re.sub(r"\(.*?\)", "", ns)) if n.strip())
        hay = " ".join([T[slug], w["title"], re.sub(r"<[^>]+>", " ", credit_line(w["credit"])), " ".join(venue(r["venue"]) for r in w["rows"]),
                        " ".join(r["date"] for r in w["rows"]), nm, re.sub(r"<[^>]+>", "", E.INTRO.get(slug, ""))])
        idx.append(["Works", T[slug], page(slug), yr, hay])
    for k in sorted(people, key=lambda k: show_en(k).lower()):
        idx.append(["People", show_en(k), f"who.html#{anchor(k)}", f"{len(people[k])} works", show_en(k) + " " + k])
    for v, rs in sorted(by_venue.items()):
        idx.append(["Theaters", E.VENUE.get(v, v), f"theaters.html#{vid(v)}", f"{len(rs)} runs", E.VENUE.get(v, v) + " " + v])
    for n in sorted(writers, key=roman):
        if n not in people: idx.append(["Writers", roman(n), "writers.html", f"{len(writers[n])} works", roman(n) + " " + n])
    write("search.js", "// Search index for en/search.html (made by build.py)\nvar S=" + json.dumps(idx, ensure_ascii=False, separators=(",", ":")) + ";\n")
    s = open(f"{SITE}/search.html").read()
    script = s[s.index("<script>\n// 서버 없이"):s.rindex("</script>") + 9]
    script = (script.replace('["사람", "극장", "작가", "작품"]', '["People", "Theaters", "Writers", "Works"]').replace("찾는 것이 없습니다.", "Nothing found.")
              .replace("// 서버 없이 이 페이지 안에서만 찾는다. 색인은 search.js (build.py가 자동 생성)", "// Searches within this page only. Index: search.js (made by build.py)"))
    write("search.html", [HEAD.format(t="Search"), '<script src="search.js" defer></script>\n', crumb("Search"),
        '<form action="search.html" role="search"><h2 class="find big"><input type="search" name="q" id="q" placeholder="Search" aria-label="Search" enterkeyhint="search" autocomplete="off"><span aria-hidden="true">Type to search</span></h2></form>\n',
        '<p class="note">Searches work titles, descriptions and credits, names and theaters. With several words, only results containing all of them are shown.</p>\n',
        '<div id="results"></div>\n', '<noscript><p>Search needs JavaScript. Try the <a href="archive.html">archive</a> or the <a href="who.html">credits index</a>.</p></noscript>\n', script])

    # ---- 발행인 ----
    write("colophon.html", [HEAD.format(t="Publisher"), '<meta name="robots" content="noindex">\n', crumb("Publisher"),
        "<p>\nThis site was made by Cho Woongchul of Green Pig's directing team.<br>\nNovember 2026, Seoul.\n</p>\n",
        "<p>The English translations were first made in November 2026. Corrections are welcome.</p>\n", "<p>chowoongchul@gmail.com</p>\n"])
    print(len(order) + 11, "English pages")

KIND = {"평론": "Criticism", "기사": "Article", "관객": "Audience review"}
SRC = {"네이버 블로그": "Naver blog", "네이버 카페": "Naver café", "네이버 포스트": "Naver Post", "티스토리": "Tistory", "매일신문": "Maeil Shinmun",
       "경향신문": "Kyunghyang Shinmun", "노컷뉴스": "CBS NoCut News", "이데일리": "Edaily", "뉴데일리": "New Daily", "민중의소리": "Voice of the People",
       "매일노동뉴스": "Maeil Labor News", "오마이스타": "OhmyStar", "액티오 웹진": "Actio webzine", "서울연극센터 웹진": "Seoul Theater Center webzine",
       "대학지성 In&Out": "Daehak Jiseong In&Out", "공연예술통합전산망 블로그": "KOPIS blog", "사이 비평": "Sai Criticism"}
def rev_en(r, title=""):
    return {"d": r["d"], "u": r["u"], "t": KIND[r["k"]], "s": SRC.get(r["s"], r["s"]), "w": roman(r["w"]) if r["w"] else "",
            "k": r["k"], "p": r.get("p", ""), "n": title}

def rev_line_en(r):
    who = ", " + r["w"] if r["w"] else ""
    return f'{r["d"]} <a href="{r["u"]}">{r["t"]}</a>{who}' + (f' ({r["s"]})' if r["s"] else "")
