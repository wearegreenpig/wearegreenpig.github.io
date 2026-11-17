// 전광판: 글자를 하나씩 바꿔 보여 준다.
// - 소개 페이지(data-from이 있는 상자): 아래 실린 글(.essay)의 문장을 하나씩 보여 주고, 누르면 그 문장으로 간다.
//   문장은 이 파일이 글에서 직접 뽑으므로, 글을 고치거나 새 글을 더하면 전광판에도 저절로 들어간다.
//   각 문장에는 '글 id-번호' 꼴의 주소가 붙는다 (예: about.html#오는-사람-3).
// - 영어판처럼 상자 안에 링크가 미리 들어 있으면 그 링크들을 1초마다 바꾼다.
// 넘어가는 속도는 늘 같다. 볼 때마다 순서를 섞고, 마우스를 올리거나 초점이 가면 멈춘다. 기기에서 '동작 줄이기'를 켰으면 하나만 보여 준다.
(function () {
  var SPEED = 1000;  // 넘어가는 간격(밀리초). 상자에 data-speed="1500"처럼 적으면 그 값을 쓴다
  var still = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;

  function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  // 문단 하나를 문장 단위 <span class="s">로 나눈다. 링크 안의 글자(작품명)는 자르지 않는다.
  var END = /[.?!…]+[”’"'」』)]*(?=\s|$)/g;
  function split(p) {
    var out = [], cur = [];
    function close() {
      if (!cur.length) return;
      var s = document.createElement("span"); s.className = "s";
      cur.forEach(function (n) { s.appendChild(n); }); out.push(s); cur = [];
    }
    [].slice.call(p.childNodes).forEach(function (n) {
      if (n.nodeType !== 3) { cur.push(n); return; }
      var t = n.nodeValue, last = 0, m;
      END.lastIndex = 0;
      while ((m = END.exec(t))) {
        var end = m.index + m[0].length, ws = t.slice(end).match(/^\s*/)[0];
        cur.push(document.createTextNode(t.slice(last, end))); close();
        if (ws) out.push(document.createTextNode(ws));
        last = end + ws.length; END.lastIndex = last;
      }
      if (last < t.length) cur.push(document.createTextNode(t.slice(last)));
    });
    close();
    p.textContent = "";
    out.forEach(function (n) { p.appendChild(n); });
  }

  function plain(el) {  // 각주 번호는 빼고 글자만
    var c = el.cloneNode(true);
    [].slice.call(c.querySelectorAll("sup")).forEach(function (x) { x.remove(); });
    // 본문에서는 파란 글씨가 작품명임을 알려 주지만, 전광판에서는 검은 글씨라 〈 〉를 다시 붙인다
    [].slice.call(c.querySelectorAll('a[href^="w"]')).forEach(function (x) { x.textContent = "〈" + x.textContent + "〉"; });
    return c.textContent.replace(/\s+/g, " ").trim();
  }

  // 주소의 문장을 화면 가운데로 가져오고 칠해 둔다
  function mark(center) {
    var old = document.querySelector(".s.here"); if (old) old.classList.remove("here");
    var id = decodeURIComponent(location.hash.slice(1)), el = id && document.getElementById(id);
    if (!el || !el.classList.contains("s")) return;
    el.classList.add("here");
    if (center) el.scrollIntoView({ block: "center" });
  }

  function sentences(box) {
    var list = [];
    document.querySelectorAll(box.getAttribute("data-from")).forEach(function (essay) {
      var h = essay.querySelector("h3[id]"); if (!h) return;
      var by = essay.querySelector(".byline a"), who = by ? by.textContent : "";
      var n = 0;
      essay.querySelectorAll("p:not(.byline):not(.hash):not(.note)").forEach(function (p) {
        split(p);
        p.querySelectorAll(".s").forEach(function (s) {
          s.id = h.id + "-" + (++n);
          var t = plain(s);
          if (t.length >= 8 && t.length <= 120) list.push({ id: s.id, text: t, from: who + ", 「" + h.textContent + "」" });
        });
      });
    });
    return list;
  }

  function show(box, item) {
    var a = document.createElement("a"), c = document.createElement("small");
    a.href = "#" + item.id; a.textContent = item.text;
    a.className = item.text.length <= 24 ? "l" : item.text.length <= 50 ? "m" : "x";
    c.textContent = item.from;
    box.textContent = ""; box.appendChild(a); box.appendChild(c);
  }

  function run(box, items, step, wait) {
    var n = 0, paused = false;
    step(0);
    if (still || items.length < 2) return;
    box.addEventListener("mouseenter", function () { paused = true; });
    box.addEventListener("mouseleave", function () { paused = false; });
    box.addEventListener("focusin", function () { paused = true; });
    box.addEventListener("focusout", function () { paused = false; });
    (function tick() {
      setTimeout(function () {
        if (!paused && !document.hidden) { n = (n + 1) % items.length; step(n); }
        tick();
      }, wait(n));
    })();
  }

  document.querySelectorAll(".rotator").forEach(function (box) {
    if (box.hasAttribute("data-from")) {
      var items = shuffle(sentences(box));
      if (!items.length) return;
      box.hidden = false;
      run(box, items, function (k) { show(box, items[k]); },
          function () { return +box.getAttribute("data-speed") || SPEED; });
      window.addEventListener("hashchange", function () { mark(true); });
      mark(true);
      return;
    }
    var links = shuffle([].slice.call(box.children));
    if (links.length < 1) return;
    links.forEach(function (el) { box.appendChild(el); el.style.display = "none"; });
    var shown = links[0];
    run(box, links, function (k) { shown.style.display = "none"; shown = links[k]; shown.style.display = "block"; },
        function () { return +box.getAttribute("data-speed") || SPEED; });
  });
})();
