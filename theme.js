// 밤낮(다크모드) 전환. 처음에는 기기 설정을 따르고, 첫 페이지 로고를 누르면 바뀐다.
// 고른 값은 이 브라우저에만 저장되며, 기기 설정과 같아지면 다시 기기 설정을 따른다.
// 숨은 놀이: 로고를 빠르게 다섯 번 누르면 밤낮을 처음 상태로 되돌리고 돼지 달리기(game.js)를 연다.
(function () {
  var root = document.documentElement;
  try { var t = localStorage.getItem("theme"); if (t) root.setAttribute("data-theme", t); } catch (e) {}
  var taps = [], before = null;
  function saved() { try { return localStorage.getItem("theme"); } catch (e) { return null; } }
  function restore(b) {
    if (b.attr) root.setAttribute("data-theme", b.attr); else root.removeAttribute("data-theme");
    try { if (b.stored) localStorage.setItem("theme", b.stored); else localStorage.removeItem("theme"); } catch (e) {}
  }
  function openGame() {
    if (window.pigGame) { window.pigGame.open(); return; }
    var s = document.createElement("script");
    s.src = "game.js";
    s.onload = function () { if (window.pigGame) window.pigGame.open(); };
    document.head.appendChild(s);
  }
  document.addEventListener("click", function (e) {
    if (!e.target.closest || !e.target.closest(".night")) return;
    var now = Date.now();
    if (!taps.length || now - taps[taps.length - 1] > 600) { taps = []; before = { attr: root.getAttribute("data-theme"), stored: saved() }; }
    taps.push(now);
    var sys = matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    var next = (root.getAttribute("data-theme") || sys) === "dark" ? "light" : "dark";
    try {
      if (next === sys) { root.removeAttribute("data-theme"); localStorage.removeItem("theme"); }
      else { root.setAttribute("data-theme", next); localStorage.setItem("theme", next); }
    } catch (e) { root.setAttribute("data-theme", next); }
    if (taps.length >= 5) { taps = []; restore(before); openGame(); }
  });
})();
