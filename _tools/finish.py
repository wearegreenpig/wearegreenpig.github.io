# 모든 페이지에 공통 머리말(언어, 탭 아이콘, 공유 미리보기)과 발행일를 넣는다.
# build.py 끝에서 자동으로 불리며, 손으로 페이지를 고친 뒤 이것만 따로 돌려도 된다:
#   python3 _tools/finish.py
import os, re, json, glob, hashlib, html
from datetime import datetime, timezone, timedelta

TOOLS = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(TOOLS)
BASE = "https://wearegreenpig.github.io/"
STATE = os.path.join(TOOLS, "수정날짜.json")

DESC = {  # 작품 페이지가 아닌 페이지의 미리보기 설명
    "index.html": "불온한 상상력, 2006년부터. 극단 그린피그의 공연 기록과 소식.",
    "about.html": "생각이 세상을 바꾼다는 신념과 뜨거운 감성을 가진 사람들이 만든 공연단체, 그린피그.",
    "people.html": "그린피그의 대표, 연출, 배우.",
    "texts.html": "그린피그 공연에 관한 관객 리뷰, 기사, 비평.",
    "chronology.html": "그린피그 공연 연보. 2006년부터의 모든 공연과 수상.",
    "theaters.html": "그린피그가 공연한 극장들과 그곳에서 올린 작품.",
    "writers.html": "그린피그가 무대에 올린 작가들과 작품.",
    "who.html": "그린피그 공연에 참여한 사람들과 그들의 작품 목록.",
    "colophon.html": "이 사이트의 발행인.",
    "search.html": "그린피그의 작품, 사람, 극장 찾기.",
    "404.html": "찾으시는 페이지가 없습니다.",
    "archive.html": "2006년부터 지금까지 그린피그의 모든 공연 기록과 수상.",
}

META_RE = re.compile(r"<!-- 공통 머리말 -->.*?<!-- /공통 머리말 -->\n", re.S)
DATE_RE = re.compile(r'\n?<p class="updated">.*?</p>\n?', re.S)

def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def short(s, n=110):
    s = " ".join(s.split())
    return s if len(s) <= n else s[:n - 1].rstrip() + "…"

def describe(name, text):
    if name in DESC:
        return DESC[name]
    m = re.search(r"<h3>작품 소개</h3>\s*<p>(.*?)</p>", text, re.S)
    if m:  # 역사시비 작품은 공통 머리 문장을 빼고 그 달의 설명부터
        return short(re.sub(r"^역사시비프로젝트:.*?올렸다\.\s*", "역사시비프로젝트 ", plain(m.group(1))))
    m = re.search(r"<h3>크레딧</h3>\s*<p>(.*?)</p>", text, re.S)   # 소개가 없는 작품은 크레딧으로
    d = short(plain(m.group(1)).replace("\n", ", ")) if m else ""
    return d or DESC["index.html"]

# 링크가 걸린 작품명은 파란 글씨로 구분되므로 〈 〉를 뺀다 (링크 없는 작품명과 인쇄용 연보는 그대로)
LINK_TITLE_RE = re.compile(r"(<a\b[^>]*>)〈([^〈〉<]*)〉(</a>)")
KEEP_BRACKETS = {"chronology.html"}

CSS_RE = re.compile(r'<link rel="stylesheet" href="((?:\.\./|/)?)style\.css(?:\?v=\w+)?">')
LANG_RE = re.compile(r'<p class="lang noprint">.*?</p>\n', re.S)
DESC_EN = {
    "index.html": "Subversive imagination, since 2006. Performance records and news of the theater company Green Pig.",
    "about.html": "Green Pig, a performance company made by people who believe ideas change the world.",
    "people.html": "Green Pig's representative, directors and performers.", "texts.html": "Reviews, criticism and articles on Green Pig's productions.",
    "theaters.html": "Theaters where Green Pig has performed, and the works staged there.", "writers.html": "Writers whose works Green Pig has staged.",
    "who.html": "Everyone credited in Green Pig's productions, with their works.", "colophon.html": "Who made this site.",
    "search.html": "Search Green Pig's works, people and theaters.", "archive.html": "Every Green Pig performance and award since 2006.",
}

def core(text):  # 날짜 비교용: 자동으로 넣는 부분을 뺀 본문 (스타일 버전 표시도 뺀다)
    text = CSS_RE.sub(r'<link rel="stylesheet" href="\1style.css">', text)
    return LANG_RE.sub("", DATE_RE.sub("", META_RE.sub("", text))).replace('<html lang="ko">\n', "").replace('<html lang="en">\n', "")

def main():
    today = datetime.now(timezone(timedelta(hours=9)))
    today = f"{today.year}.{today.month}.{today.day}"
    try:
        state = json.load(open(STATE))
    except Exception:
        state = {}
    # style.css가 바뀌면 주소 뒤 번호(?v=)도 바뀌어, 브라우저가 예전 스타일을 붙들고 있지 않게 한다
    css_v = hashlib.sha1(open(os.path.join(SITE, "style.css"), "rb").read()).hexdigest()[:8]
    css_link = f'<link rel="stylesheet" href="style.css?v={css_v}">\n'
    ko_pages = {os.path.basename(p) for p in glob.glob(os.path.join(SITE, "*.html"))}
    en_pages = {os.path.basename(p) for p in glob.glob(os.path.join(SITE, "en", "*.html"))}
    paths = sorted(glob.glob(os.path.join(SITE, "*.html"))) + sorted(glob.glob(os.path.join(SITE, "en", "*.html")))
    for path in paths:
        en = os.path.basename(os.path.dirname(path)) == "en"
        name = os.path.basename(path)
        skey = ("en/" if en else "") + name
        up = "../" if en else ""
        text = open(path, encoding="utf-8").read()
        body = core(text)
        if name not in KEEP_BRACKETS and not en:
            body = LINK_TITLE_RE.sub(r"\1\2\3", body)
        h = hashlib.sha1(body.encode()).hexdigest()
        old = state.get(skey, {})
        date = old.get("date") if old.get("hash") == h else today
        state[skey] = {"hash": h, "date": date}

        title = plain(re.search(r"<title>(.*?)</title>", body, re.S).group(1))
        url = BASE + ("en/" if en else "") + ("" if name == "index.html" else name)
        img = name.replace(".html", ".jpg")
        image = BASE + img if name.startswith("w") and os.path.exists(os.path.join(SITE, img)) else BASE + "og.png"
        if en:
            m = re.search(r"<h3>About the work</h3>\s*<p>(.*?)</p>", body, re.S) or re.search(r"<h3>Credits</h3>\s*<p>(.*?)</p>", body, re.S)
            d = DESC_EN.get(name) or (short(re.sub(r"^History Dispute Project: .*?a year earlier\. ", "History Dispute Project. ", plain(m.group(1)).replace("\n", ", "))) if m else "")
            desc = html.escape(d or DESC_EN["index.html"], quote=True)
        else:
            desc = html.escape(describe(name, body), quote=True)
        other = (name in ko_pages) if en else (name in en_pages)
        alt = ""
        if other:
            alt = (f'<link rel="alternate" hreflang="ko" href="{BASE}{"" if name == "index.html" else name}">\n' if en else
                   f'<link rel="alternate" hreflang="en" href="{BASE}en/{"" if name == "index.html" else name}">\n')
        meta = ("<!-- 공통 머리말 -->\n"
                f'<link rel="icon" href="{up}favicon.png" type="image/png">\n'
                f'<link rel="apple-touch-icon" href="{up}apple-touch-icon.png">\n'
                f'<link rel="author" href="{up}humans.txt">\n'
                f'<script src="{up}random.js" defer></script>\n'
                # 로고를 눌러 고른 밤낮을 페이지가 그려지기 전에 적용 (theme.js)
                f'<script src="{up}theme.js"></script>\n'
                + alt +
                f'<meta name="description" content="{desc}">\n'
                f'<meta property="og:site_name" content="{"Green Pig" if en else "그린피그"}">\n'
                f'<meta property="og:title" content="{html.escape(title, quote=True)}">\n'
                f'<meta property="og:description" content="{desc}">\n'
                f'<meta property="og:image" content="{image}">\n'
                f'<meta property="og:url" content="{url}">\n'
                '<meta property="og:type" content="website">\n'
                '<meta name="twitter:card" content="summary_large_image">\n'
                "<!-- /공통 머리말 -->\n")
        if other:   # 한국어/영어 전환 링크 (오른쪽 위)
            meta += (f'<p class="lang noprint"><a href="../{name}" hreflang="ko" lang="ko">한국어</a></p>\n' if en else
                     f'<p class="lang noprint"><a href="en/{name}" hreflang="en" lang="en">English</a></p>\n')
        lang = "en" if en else "ko"
        out = body.replace("<!doctype html>\n", f'<!doctype html>\n<html lang="{lang}">\n', 1)
        if 'href="/style.css"' in out:   # 404.html은 어느 주소에서나 열리므로 절대 경로만 쓰고 머리말을 넣지 않는다
            out = out.replace('href="/style.css"', f'href="/style.css?v={css_v}"', 1)
        else:
            out = CSS_RE.sub(lambda m: f'<link rel="stylesheet" href="{m.group(1)}style.css?v={css_v}">\n' + meta.rstrip("\n"), out, count=1)
        # '발행일' 글자는 눈에 띄지 않는 '발행인' 페이지 링크
        label = "Published" if en else "발행일"
        out = out.rstrip("\n") + f'\n\n<p class="updated"><a class="hid" href="colophon.html">{label}</a> {date}</p>\n'
        if out != text:
            open(path, "w", encoding="utf-8").write(out)
    json.dump(state, open(STATE, "w"), ensure_ascii=False, indent=0, sort_keys=True)

if __name__ == "__main__":
    main()
