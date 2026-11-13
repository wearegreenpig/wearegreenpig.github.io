// 텍스트 페이지: 리뷰·기사를 작품별 / 글쓴이별 / 최근 순으로, 종류(평론·기사·관객 후기)와 평론가별로 골라 본다.
// 자료(RV, RC)는 build.py가 texts.html 안에 넣는다. 자바스크립트가 꺼져 있으면 작품별 목록이 그대로 보인다.
(function () {
  var box = document.getElementById("rv"), ctl = document.querySelector(".rvctl");
  if (!box || !ctl || !window.RV) return;
  var view = "work", kind = "", who = "";
  try { var s = JSON.parse(sessionStorage.getItem("rv") || "{}"); view = s.v || view; kind = s.k || ""; who = s.w || ""; } catch (e) {}
  if (who && RC.indexOf(who) < 0) who = "";
  var L = window.L || { none: "해당하는 글이 없습니다.", other: "그 밖의 비평·기사", aud: "관객 후기" };   // 영어판은 L을 따로 준다

  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function key(d) { return d.split(".").map(Number); }
  function cmp(a, b) { var x = key(a.d), y = key(b.d); for (var i = 0; i < 3; i++) { var p = x[i] || 0, q = y[i] || 0; if (p !== q) return q - p; } return 0; }
  function work(r) { return esc(r.n) + " "; }   // 작품명은 검은 글씨, 바로 뒤의 파란 글씨가 글로 가는 링크
  function line(r, o) {
    return esc(r.d) + " " + (o.work ? work(r) : "") + '<a href="' + esc(r.u) + '">' + esc(r.t) + "</a>" +
      (o.who && r.w ? ", " + esc(r.w) : "") + (r.s ? " (" + esc(r.s) + ")" : "");
  }
  function para(head, rs, o) { return "<p><b>" + head + "</b><br>\n" + rs.map(function (r) { return line(r, o); }).join("<br>\n") + "\n</p>"; }

  function render() {
    var rs = RV.filter(function (r) { return (!kind || r.k === kind) && (!who || r.w === who); }).sort(cmp), out = [];
    if (view === "work") {
      var order = [], by = {};
      rs.forEach(function (r) { var k = r.n; if (!by[k]) { by[k] = []; order.push(k); } by[k].push(r); });
      order.forEach(function (k) { var r = by[k][0]; out.push(para(r.p ? '<a href="' + r.p + '">' + esc(k) + "</a>" : esc(k), by[k], { who: true })); });
    } else if (view === "writer") {
      RC.forEach(function (w) {
        var g = rs.filter(function (r) { return r.w === w; });
        if (g.length) out.push(para(esc(w) + " " + g.length, g, { work: true }));
      });
      var news = rs.filter(function (r) { return RC.indexOf(r.w) < 0 && r.k !== "관객"; });
      if (news.length) out.push(para(L.other + " " + news.length, news, { work: true, who: true }));
      var aud = rs.filter(function (r) { return RC.indexOf(r.w) < 0 && r.k === "관객"; });
      if (aud.length) out.push(para(L.aud + " " + aud.length, aud, { work: true }));
    } else {
      out.push("<p>" + rs.map(function (r) { return line(r, { work: true, who: true }); }).join("<br>\n") + "</p>");
    }
    box.innerHTML = out.join("\n\n") || "<p>" + L.none + "</p>";
    [].forEach.call(ctl.querySelectorAll("a"), function (a) {
      var on = a.hasAttribute("data-v") ? a.getAttribute("data-v") === view :
               a.hasAttribute("data-w") ? a.getAttribute("data-w") === who : a.getAttribute("data-k") === kind;
      a.className = on ? "on" : "";
    });
    try { sessionStorage.setItem("rv", JSON.stringify({ v: view, k: kind, w: who })); } catch (e) {}
  }

  ctl.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("a");
    if (!a) return;
    e.preventDefault();
    if (a.hasAttribute("data-v")) view = a.getAttribute("data-v");
    else if (a.hasAttribute("data-w")) { who = a.getAttribute("data-w"); if (who) kind = ""; }   // 평론가를 고르면 종류는 전체로
    else kind = a.getAttribute("data-k");
    render();
  });
  ctl.hidden = false;
  render();
})();
