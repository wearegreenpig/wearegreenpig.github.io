// 숨은 놀이: 첫 페이지 로고를 빠르게 다섯 번 누르면 열리는 달리기 게임.
// 그린피그 로고(logo.png)가 달리며 객석 의자, 조명 스탠드, 마이크 스탠드를 뛰어넘는다.
// theme.js가 필요할 때만 불러온다. 그림 파일은 로고 하나뿐이고 장애물은 아래 STROKES로 그린다.
(function () {
  if (window.pigGame) return;

  var W = 600, H = 170, GROUND = H - 26;           // 게임 안 좌표 (화면 폭에 맞춰 늘고 줄어든다)
  var PIG_H = 50, PIG_X = 36;
  var GRAV = 0.0032, JUMP = 0.70;                  // px/ms², px/ms
  var LOGO = window.PIG_LOGO || "logo.png";

  // 장애물 모양: 0~1 좌표의 선들. 그릴 때 손그림처럼 조금씩 흔든다.
  var STROKES = {
    "의자": { w: 30, h: 34, lines: [
      [[0.15, 0], [0.15, 0.62], [0.95, 0.62]],                 // 등받이, 앉는 판
      [[0.15, 0.05], [0.85, 0.05], [0.85, 0.35], [0.15, 0.35]], // 등받이 판
      [[0.25, 0.62], [0.2, 1]], [[0.85, 0.62], [0.9, 1]],         // 다리
      [[0.6, 0.48], [0.95, 0.48], [0.95, 0.62]]] },              // 팔걸이
    "객석": { w: 58, h: 34, lines: [
      [[0.06, 0], [0.06, 0.62], [0.97, 0.62]],
      [[0.06, 0.05], [0.47, 0.05], [0.47, 0.35], [0.06, 0.35]],
      [[0.53, 0.05], [0.94, 0.05], [0.94, 0.35], [0.53, 0.35]],
      [[0.5, 0], [0.5, 0.62]],
      [[0.1, 0.62], [0.08, 1]], [[0.5, 0.62], [0.5, 1]], [[0.92, 0.62], [0.94, 1]]] },
    "조명": { w: 26, h: 50, lines: [
      [[0.5, 0.3], [0.5, 0.82]],                                   // 기둥
      [[0.5, 0.82], [0.05, 1]], [[0.5, 0.82], [0.95, 1]], [[0.5, 0.82], [0.5, 1]], // 삼발이
      [[0.15, 0.05], [0.85, 0.05], [0.95, 0.3], [0.05, 0.3], [0.15, 0.05]],          // 조명 통
      [[0.3, 0.3], [0.2, 0.42]], [[0.7, 0.3], [0.8, 0.42]]] },     // 빛
    "마이크": { w: 22, h: 44, lines: [
      [[0.5, 0.18], [0.5, 0.86]],
      [[0.15, 1], [0.85, 1]], [[0.5, 0.86], [0.2, 1]], [[0.5, 0.86], [0.8, 1]],
      [[0.4, 0], [0.6, 0], [0.62, 0.18], [0.38, 0.18], [0.4, 0]],   // 마이크 머리
      [[0.5, 0.18], [0.5, 0.22]]] },
    "파 조명": { w: 30, h: 40, top: true, lines: [                // 배튼에 매달린 파 조명. 뛰면 부딪힌다
      [[-0.4, 0], [1.4, 0]],                                      // 배튼(파이프)
      [[0.42, 0], [0.42, 0.12]], [[0.58, 0], [0.58, 0.12]],       // 클램프
      [[0.1, 0.62], [0.1, 0.18], [0.9, 0.18], [0.9, 0.62]],         // 요크(ㄷ자 걸이)
      [[0.22, 0.3], [0.78, 0.3], [0.86, 1], [0.14, 1], [0.22, 0.3]], // 조명 통
      [[0.14, 1], [0.86, 1]],
      [[0.75, 0.05], [1.15, 0.2], [1.2, 0.5]]] }                     // 늘어진 케이블
  };
  var KINDS = Object.keys(STROKES).filter(function (k) { return !STROKES[k].top; });
  var LAMP_BOTTOM = GROUND - PIG_H - 9;             // 서 있는 돼지 머리 바로 위

  function wobble(lines, w, h, seed) {             // 선을 잘게 나눠 손떨림을 준다 (한 번만 계산)
    var r = seed;
    function rnd() { r = (r * 9301 + 49297) % 233280; return r / 233280 - 0.5; }
    return lines.map(function (ln) {
      var out = [];
      for (var i = 0; i < ln.length - 1; i++) {
        var a = ln[i], b = ln[i + 1], n = 4;
        for (var k = 0; k < n; k++) {
          var t = k / n;
          out.push([(a[0] + (b[0] - a[0]) * t) * w + rnd() * 1.4, (a[1] + (b[1] - a[1]) * t) * h + rnd() * 1.4]);
        }
      }
      var last = ln[ln.length - 1];
      out.push([last[0] * w + rnd() * 1.2, last[1] * h + rnd() * 1.2]);
      return out;
    });
  }
  var SHAPES = {};
  Object.keys(STROKES).forEach(function (k, i) { var s = STROKES[k]; SHAPES[k] = { w: s.w, h: s.h, top: !!s.top, lines: wobble(s.lines, s.w, s.h, 17 + i * 31) }; });

  var box, canvas, ctx, note, raf = 0, last = 0, colorAt = 0, fg = "#000", rule = "#888";
  var mask = null, pig = null, pigW = PIG_H, tinted = "";
  var state, y, vy, speed, dist, obs, nextGap, top3, frameT, overAt, groundSeed, form, lastScore;

  function readColors() {
    var cs = getComputedStyle(document.documentElement);
    fg = (cs.getPropertyValue("--fg") || "#000").trim();
    rule = (cs.getPropertyValue("--rule") || "#888").trim();
    if (mask && tinted !== fg) {                   // 로고 선 색을 지금 글자색으로 칠한다 (밤에는 밝게)
      var c = pig.getContext("2d");
      c.globalCompositeOperation = "source-over";
      c.clearRect(0, 0, pig.width, pig.height);
      c.drawImage(mask, 0, 0);
      c.globalCompositeOperation = "source-in";
      c.fillStyle = fg; c.fillRect(0, 0, pig.width, pig.height);
      tinted = fg;
    }
  }

  function loadPig() {
    var img = new Image();
    img.onload = function () {
      var s = 3;                                    // 선명하게 보이도록 3배로 만들어 둔다
      pigW = Math.round(PIG_H * img.naturalWidth / img.naturalHeight);
      mask = document.createElement("canvas"); mask.width = pigW * s; mask.height = PIG_H * s;
      var m = mask.getContext("2d");
      m.translate(mask.width, 0); m.scale(-1, 1);  // 로고는 왼쪽을 본다. 오른쪽으로 달리게 뒤집는다
      m.drawImage(img, 0, 0, mask.width, mask.height);
      pig = document.createElement("canvas"); pig.width = mask.width; pig.height = mask.height;
      tinted = ""; readColors();
    };
    img.src = LOGO;
  }

  function reset() {
    state = "ready"; y = 0; vy = 0; speed = 0.30; dist = 0; obs = []; nextGap = 320; frameT = 0; overAt = 0;
    groundSeed = Math.random() * 1000;
  }

  function jump() {
    if (state === "over") { if (Date.now() - overAt < 450) return; form.hidden = true; reset(); state = "run"; return; }
    if (state === "ready") state = "run";
    if (y === 0) vy = JUMP;
  }

  function step(dt) {
    if (state !== "run") return;
    speed = Math.min(0.62, 0.30 + dist / 60000);
    dist += speed * dt;
    frameT += dt;
    if (y > 0 || vy > 0) { y += vy * dt; vy -= GRAV * dt; if (y <= 0) { y = 0; vy = 0; } }
    obs.forEach(function (o) { o.x -= speed * dt; });
    obs = obs.filter(function (o) { return o.x + o.s.w > -10; });
    nextGap -= speed * dt;
    if (nextGap <= 0) {
      var k = KINDS[Math.floor(Math.random() * KINDS.length)];
      if (dist < 1500 && k === "객석") k = "의자";  // 처음에는 넓은 장애물을 빼 준다
      if (dist > 900 && Math.random() < 0.22) k = "파 조명";
      obs.push({ x: W + 10 + (k === "파 조명" ? 90 : 0), s: SHAPES[k] });   // 조명 앞은 착지할 틈을 더 준다
      nextGap = 230 + Math.random() * 260 + speed * 300 + (k === "파 조명" ? 140 : 0);
    }
    // 부딪힘: 돼지와 장애물 상자를 조금 안쪽으로 줄여서 잰다 (스치는 건 봐준다)
    var px1 = PIG_X + pigW * 0.22, px2 = PIG_X + pigW * 0.8, py2 = GROUND - y - 4, py1 = py2 - PIG_H * 0.6;
    for (var i = 0; i < obs.length; i++) {
      var o = obs[i], ox1 = o.x + 4, ox2 = o.x + o.s.w - 4, oy1 = GROUND - o.s.h + 5;
      var hit = o.s.top ? (px2 > ox1 && px1 < ox2 && py1 < LAMP_BOTTOM - 4) : (px2 > ox1 && px1 < ox2 && py2 > oy1);
      if (hit) {
        state = "over"; overAt = Date.now();
        lastScore = Math.floor(dist / 10);
        if (qualifies(lastScore)) askName(lastScore);
        break;
      }
    }
  }

  function line(pts, ox, oy) {
    ctx.beginPath(); ctx.moveTo(ox + pts[0][0], oy + pts[0][1]);
    for (var i = 1; i < pts.length; i++) ctx.lineTo(ox + pts[i][0], oy + pts[i][1]);
    ctx.stroke();
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = fg; ctx.fillStyle = fg; ctx.lineWidth = 1.6; ctx.lineCap = "round"; ctx.lineJoin = "round";
    // 땅: 흔들리는 선과 지나가는 자갈
    ctx.beginPath();
    for (var x = 0; x <= W; x += 6) {
      var gx = x + dist;
      var gy = GROUND + Math.sin(gx * 0.05 + groundSeed) * 0.6 + Math.sin(gx * 0.013) * 0.8;
      if (x === 0) ctx.moveTo(x, gy); else ctx.lineTo(x, gy);
    }
    ctx.stroke();
    ctx.lineWidth = 1.2;
    for (var p = 0; p < 14; p++) {
      var base = p * 97 + ((p * 53) % 41);
      var px = ((base - dist * 1) % (W + 40) + W + 40) % (W + 40) - 20;
      var py = GROUND + 6 + (p * 7) % 12;
      ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + 3 + (p % 3) * 2, py); ctx.stroke();
    }
    ctx.lineWidth = 1.6;
    ctx.beginPath();                                // 무대 위 배튼: 파 조명이 여기에 매달려 지나간다
    for (var bx = 0; bx <= W; bx += 8) {
      var by = LAMP_BOTTOM - 40 + Math.sin((bx + dist) * 0.021) * 0.7;
      if (bx === 0) ctx.moveTo(bx, by); else ctx.lineTo(bx, by);
    }
    ctx.stroke();
    obs.forEach(function (o) {
      if (o.s.top) {                                // 조명 빛: 바닥까지 흐린 점선
        ctx.save(); ctx.strokeStyle = rule; ctx.lineWidth = 1; ctx.setLineDash([3, 5]);
        ctx.beginPath(); ctx.moveTo(o.x + 5, LAMP_BOTTOM + 2); ctx.lineTo(o.x - 10, GROUND - 2);
        ctx.moveTo(o.x + o.s.w - 5, LAMP_BOTTOM + 2); ctx.lineTo(o.x + o.s.w + 10, GROUND - 2); ctx.stroke(); ctx.restore();
      }
      var oy = o.s.top ? LAMP_BOTTOM - o.s.h : GROUND - o.s.h;
      o.s.lines.forEach(function (l) { line(l, o.x, oy); });
    });
    // 돼지: 달릴 때 통통 튀고 살짝 기운다
    if (pig && tinted) {
      var run = state === "run" && y === 0, f = run ? Math.floor(frameT / 110) % 2 : 0;
      var bob = run ? (f ? 2.5 : 0) : 0, tilt = y > 0 ? -0.14 : (f ? -0.05 : 0.02);
      if (state === "over") tilt = 0.25;
      ctx.save();
      ctx.translate(PIG_X + pigW / 2, GROUND - y - bob - PIG_H / 2 + 2);
      ctx.rotate(tilt);
      ctx.drawImage(pig, -pigW / 2, -PIG_H / 2, pigW, PIG_H);
      ctx.restore();
    }
    // 글자
    ctx.font = "15px serif"; ctx.textBaseline = "top"; ctx.textAlign = "right";
    var sc = Math.floor(dist / 10);
    ctx.fillText((top3.length ? "최고 " + top3[0].s + "   " : "") + sc, W - 6, 6);
    ctx.textAlign = "center";
    if (state === "ready") ctx.fillText("스페이스나 화면을 누르면 달립니다", W / 2, 46);
    if (state === "over") {
      ctx.fillText("부딪혔다!", W / 2, 30); ctx.fillStyle = rule; ctx.fillText("다시 하려면 누르세요", W / 2, 50);
      if (top3.length) {                            // 이 기기에서 세운 기록 3위까지
        ctx.textAlign = "left"; ctx.font = "13px serif";
        ctx.fillText("이 기기 기록", 8, 8); ctx.fillStyle = fg;
        top3.forEach(function (r, i) { ctx.fillText((i + 1) + ". " + r.n + "  " + r.s, 8, 26 + i * 17); });
      }
    }
  }

  function loop(t) {
    raf = requestAnimationFrame(loop);
    var dt = Math.min(40, t - (last || t)); last = t;
    if (t - colorAt > 400) { readColors(); colorAt = t; }
    step(dt); draw();
  }

  function onKey(e) {
    if (e.key === "Escape") { if (!form.hidden && document.activeElement === form.querySelector("input")) { form.hidden = true; document.activeElement.blur(); } else close(); return; }
    if (e.key === " " || e.key === "ArrowUp" || e.key === "w") {
      var tag = (document.activeElement && document.activeElement.tagName) || "";
      if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
      e.preventDefault(); if (!e.repeat) jump();
    }
  }
  function loadTop() {
    try {
      var t = JSON.parse(localStorage.getItem("pigTop") || "[]");
      if (!t.length) { var b = parseInt(localStorage.getItem("pigBest") || "0", 10); if (b) t = [{ n: "?", s: b }]; }
      return t.slice(0, 3);
    } catch (e) { return []; }
  }
  function saveTop() { try { localStorage.setItem("pigTop", JSON.stringify(top3)); } catch (e) {} }
  function qualifies(sc) { return sc >= 30 && (top3.length < 3 || sc > top3[top3.length - 1].s); }
  function askName(sc) {                            // 3위 안에 들면 캔버스 아래에 이름 칸을 띄운다
    var place = top3.filter(function (r) { return r.s >= sc; }).length + 1;
    form.hidden = false;
    form.querySelector("span").textContent = place + "위! " + sc + "점. 이름을 남기세요 ";
    var inp = form.querySelector("input"); inp.value = "";
    setTimeout(function () { try { inp.focus({ preventScroll: true }); } catch (e) {} }, 50);
  }
  function submitName(e) {
    if (e) e.preventDefault();
    var n = form.querySelector("input").value.replace(/\s+/g, " ").trim().slice(0, 10) || "익명";
    top3.push({ n: n, s: lastScore }); top3.sort(function (a, b) { return b.s - a.s; }); top3 = top3.slice(0, 3);
    saveTop(); form.hidden = true;
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
  }
  function onKeyUp(e) {                             // 로고 버튼에 초점이 남아 있으면 스페이스가 밤낮을 바꾸므로 막는다
    if (e.key === " " && !/INPUT|TEXTAREA|SELECT/.test((document.activeElement || {}).tagName || "")) e.preventDefault();
  }
  function onVis() { if (document.hidden && state === "run") { cancelAnimationFrame(raf); raf = 0; } else if (!document.hidden && !raf) { last = 0; raf = requestAnimationFrame(loop); } }

  function fit() {                                  // 화면 픽셀에 맞춰 선명하게
    var r = Math.min(4, window.devicePixelRatio || 1), cw = canvas.clientWidth || W;
    var scale = cw / W * r;
    canvas.width = Math.round(cw * r); canvas.height = Math.round(H * cw / W * r);
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
  }

  function open() {
    if (box) { jump(); return; }
    top3 = loadTop();
    box = document.createElement("div");
    box.id = "pig-game";
    box.innerHTML = '<canvas role="img" aria-label="돼지 달리기 게임. 스페이스나 화면을 눌러 점프" style="display:block;width:100%;max-width:' + W + 'px;aspect-ratio:' + W + '/' + H + ';touch-action:manipulation;cursor:pointer;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent"></canvas>' +
      '<form hidden style="margin:6px 0 0"><span></span><input maxlength="10" size="10" aria-label="이름" autocomplete="off" enterkeyhint="done"> <button type="submit">남기기</button></form>' +
      '<p class="note" style="margin:4px 0 0">돼지 달리기 · 스페이스·↑·화면 누르기로 점프 · <a href="#" class="hid" style="text-decoration:underline">닫기</a></p>';
    var anchor = document.querySelector(".night");
    var at = anchor && anchor.closest("p");
    if (at && at.parentNode) at.parentNode.insertBefore(box, at.nextSibling); else document.body.insertBefore(box, document.body.firstChild);
    canvas = box.querySelector("canvas"); ctx = canvas.getContext("2d");
    form = box.querySelector("form"); form.addEventListener("submit", submitName);
    canvas.addEventListener("pointerdown", function (e) { e.preventDefault(); jump(); });
    box.querySelector("a").addEventListener("click", function (e) { e.preventDefault(); close(); });
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    document.addEventListener("keydown", onKey);
    document.addEventListener("keyup", onKeyUp);
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("resize", fit);
    fit(); if (!mask) loadPig(); readColors(); reset();
    last = 0; raf = requestAnimationFrame(loop);
    box.scrollIntoView({ block: "nearest" });
  }

  function close() {
    if (!box) return;
    cancelAnimationFrame(raf); raf = 0;
    document.removeEventListener("keydown", onKey);
    document.removeEventListener("keyup", onKeyUp);
    document.removeEventListener("visibilitychange", onVis);
    window.removeEventListener("resize", fit);
    box.parentNode.removeChild(box); box = null;
  }

  window.pigGame = { open: open, close: close };
})();
