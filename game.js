// 숨은 놀이 「돼지 달리기」: 첫 페이지 로고를 빠르게 다섯 번 누르면 열린다 (theme.js가 불러온다).
// 로고 돼지가 무대로 뛰어내려, 그린피그 공연 기록(pig-data.js, build.py가 만든다)을
// 2006년부터 순서대로 하나씩 뛰어넘는다. 장애물 하나가 공연 하나.
// 끝까지 가면 막이 닫히는데, 돼지는 인사하지 않고 걸어 나가 버린다. 그린피그는 커튼콜을 하지 않는다.
// 부딪히면 처음부터. 그림 파일은 로고 하나뿐이고 장애물은 아래 STROKES로 그린다.
(function () {
  if (window.pigGame) return;

  var W = 600, H = 204, GROUND = H - 26;           // 게임 안 좌표. 폭(W)은 화면에 따라 440~600
  var PIG_H = 50, PIG_X = 36;
  var GRAV = 0.0032, JUMP = 0.70;                  // px/ms², px/ms → 최고 높이 약 77
  var BATTEN = 44;                                 // 무대 위 배튼(조명 파이프) 높이. 위쪽 띠에는 연도와 자막
  var LAMP_BOTTOM = GROUND - PIG_H - 9;            // 매달린 조명의 아랫면: 서 있는 돼지 머리 바로 위
  var LOGO = window.PIG_LOGO || "logo.png";
  var DATA_SRC = "pig-data.js";

  // 장애물 모양: 0~1 좌표의 선들. 손그림처럼 조금씩 흔들어 그린다.
  var STROKES = {
    "의자": { w: 30, h: 34, lines: [
      [[0.15, 0], [0.15, 0.62], [0.95, 0.62]],
      [[0.15, 0.05], [0.85, 0.05], [0.85, 0.35], [0.15, 0.35]],
      [[0.25, 0.62], [0.2, 1]], [[0.85, 0.62], [0.9, 1]],
      [[0.6, 0.48], [0.95, 0.48], [0.95, 0.62]]] },
    "객석": { w: 58, h: 34, lines: [
      [[0.06, 0], [0.06, 0.62], [0.97, 0.62]],
      [[0.06, 0.05], [0.47, 0.05], [0.47, 0.35], [0.06, 0.35]],
      [[0.53, 0.05], [0.94, 0.05], [0.94, 0.35], [0.53, 0.35]],
      [[0.5, 0], [0.5, 0.62]],
      [[0.1, 0.62], [0.08, 1]], [[0.5, 0.62], [0.5, 1]], [[0.92, 0.62], [0.94, 1]]] },
    "조명": { w: 26, h: 50, lines: [
      [[0.5, 0.3], [0.5, 0.82]],
      [[0.5, 0.82], [0.05, 1]], [[0.5, 0.82], [0.95, 1]], [[0.5, 0.82], [0.5, 1]],
      [[0.15, 0.05], [0.85, 0.05], [0.95, 0.3], [0.05, 0.3], [0.15, 0.05]],
      [[0.3, 0.3], [0.2, 0.42]], [[0.7, 0.3], [0.8, 0.42]]] },
    "마이크": { w: 22, h: 44, lines: [
      [[0.5, 0.18], [0.5, 0.86]],
      [[0.15, 1], [0.85, 1]], [[0.5, 0.86], [0.2, 1]], [[0.5, 0.86], [0.8, 1]],
      [[0.4, 0], [0.6, 0], [0.62, 0.18], [0.38, 0.18], [0.4, 0]],
      [[0.5, 0.18], [0.5, 0.22]]] },
    "파 조명": { w: 30, h: 40, top: true, lines: [  // 배튼에 매달린 파 조명. 뛰면 부딪힌다
      [[0.1, 0.62], [0.1, 0.18], [0.9, 0.18], [0.9, 0.62]],         // 요크(ㄷ자 걸이)
      [[0.5, 0], [0.5, 0.18]],
      [[0.22, 0.3], [0.78, 0.3], [0.86, 1], [0.14, 1], [0.22, 0.3]], // 조명 통
      [[0.75, 0.05], [1.1, 0.25], [1.15, 0.55]]] }                   // 늘어진 케이블
  };
  var GROUND_KINDS = ["의자", "객석", "조명", "마이크"];

  function wobble(lines, w, h, seed) {             // 선을 잘게 나눠 손떨림을 준다 (한 번만 계산)
    var r = seed;
    function rnd() { r = (r * 9301 + 49297) % 233280; return r / 233280 - 0.5; }
    return lines.map(function (ln) {
      var out = [];
      for (var i = 0; i < ln.length - 1; i++) {
        var a = ln[i], b = ln[i + 1];
        for (var k = 0; k < 4; k++) {
          var t = k / 4;
          out.push([(a[0] + (b[0] - a[0]) * t) * w + rnd() * 1.4, (a[1] + (b[1] - a[1]) * t) * h + rnd() * 1.4]);
        }
      }
      var last = ln[ln.length - 1];
      out.push([last[0] * w + rnd() * 1.2, last[1] * h + rnd() * 1.2]);
      return out;
    });
  }
  var SHAPES = {};
  Object.keys(STROKES).forEach(function (k, i) {
    var s = STROKES[k]; SHAPES[k] = { w: s.w, h: s.h, top: !!s.top, lines: wobble(s.lines, s.w, s.h, 17 + i * 31) };
  });

  var box, canvas, ctx, status, logoP, raf = 0, last = 0, colorAt = 0, fg = "#000", bg = "#fff", rule = "#888";
  var mask = null, pig = null, pigW = PIG_H, tinted = "";
  var DATA = [], N = 0;
  var state, y, vy, speed, dist, obs, nextGap, spawned, cleared, hitAt, best, frameT, overAt, endT, goneAt, pigX, rng, busy;

  function seeded(seed) { return function () { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; }; }

  function readColors() {
    var cs = getComputedStyle(document.documentElement);
    fg = (cs.getPropertyValue("--fg") || "#000").trim();
    bg = (cs.getPropertyValue("--bg") || "#fff").trim();
    rule = (cs.getPropertyValue("--rule") || "#888").trim();
    if (mask && tinted !== fg) {                   // 로고 선 색을 지금 글자색으로 (밤에는 밝게)
      var c = pig.getContext("2d");
      c.globalCompositeOperation = "source-over";
      c.clearRect(0, 0, pig.width, pig.height);
      c.drawImage(mask, 0, 0);
      c.globalCompositeOperation = "source-in";
      c.fillStyle = fg; c.fillRect(0, 0, pig.width, pig.height);
      tinted = fg;
    }
  }

  function loadPig(done) {
    var img = new Image();
    img.onload = function () {
      var s = 3;
      pigW = Math.round(PIG_H * img.naturalWidth / img.naturalHeight);
      mask = document.createElement("canvas"); mask.width = pigW * s; mask.height = PIG_H * s;
      var m = mask.getContext("2d");
      m.translate(mask.width, 0); m.scale(-1, 1);  // 로고는 왼쪽을 본다. 오른쪽으로 달리게 뒤집는다
      m.drawImage(img, 0, 0, mask.width, mask.height);
      pig = document.createElement("canvas"); pig.width = mask.width; pig.height = mask.height;
      tinted = ""; readColors();
      if (done) done();
    };
    img.onerror = function () { if (done) done(); };
    img.src = LOGO;
  }

  function reset() {
    state = "ready"; y = 0; vy = 0; speed = 0.30; dist = 0; obs = []; nextGap = 300;
    spawned = 0; cleared = 0; hitAt = -1; frameT = 0; overAt = 0; endT = 0; goneAt = -1; pigX = PIG_X;
    rng = seeded(2006);                            // 코스는 매번 똑같다 (외워서 넘을 수 있게)
    setStatus();
  }

  function act() {                                 // 스페이스·화면 누르기
    if (state === "intro" || state === "outro") return;
    if (state === "end" && !(goneAt >= 0 && endT > goneAt + 900)) return;   // 마지막 글자가 뜨기 전에는 다시 시작하지 않는다
    if (state === "over" || state === "end") { if (Date.now() - overAt < 500) return; reset(); state = "run"; setStatus(); return; }
    if (state === "ready") { state = "run"; setStatus(); }
    if (y === 0) vy = JUMP;
  }

  function step(dt) {
    if (state === "end") {                         // 마지막 공연 뒤: 막이 닫히는 동안 돼지는 인사 없이 걸어 나간다
      endT += dt; frameT += dt * 0.6;              // 달리기보다 느린 걸음
      if (y > 0 || vy > 0) { y += vy * dt; vy -= GRAV * dt; if (y <= 0) { y = 0; vy = 0; } }
      if (goneAt < 0) { pigX += 0.2 * dt; if (pigX > W + 10) goneAt = endT; }
      return;
    }
    if (state !== "run") return;
    // 빠르기: 처음 40편까지는 예전(끝없는 버전)과 같은 속도로 빨라지고, 그 뒤로는 끝까지 조금씩 더
    speed = cleared <= 40 ? 0.295 + 0.0076 * cleared : 0.599 + 0.07 * (cleared - 40) / Math.max(1, N - 40);   // 0.295 → 40편째 0.599 → 끝 0.669 (처음 버전보다 4%쯤 느리게)
    dist += speed * dt;
    frameT += dt;
    if (y > 0 || vy > 0) { y += vy * dt; vy -= GRAV * dt; if (y <= 0) { y = 0; vy = 0; } }
    obs.forEach(function (o) {
      o.x -= speed * dt;
      if (!o.done && o.x + o.s.w < pigX + pigW * 0.2) { o.done = true; cleared++; if (cleared > best) saveBest(cleared); }
    });
    obs = obs.filter(function (o) { return o.x + o.s.w > -20; });
    if (spawned < N) {
      nextGap -= speed * dt;
      if (nextGap <= 0) {
        var k = GROUND_KINDS[Math.floor(rng() * GROUND_KINDS.length)];
        if (spawned < 3 && k === "객석") k = "의자";  // 처음 두세 개만 넓은 장애물을 빼 준다
        var lamp = spawned >= 2 && rng() < 0.22;
        if (lamp) k = "파 조명";
        obs.push({ x: W + 10 + (lamp ? 90 : 0), s: SHAPES[k], i: spawned });
        spawned++;
        nextGap = 230 + rng() * 260 + speed * 300 + (lamp ? 140 : 0);
      }
    } else if (cleared >= N && y === 0) {          // 마지막 공연까지 넘었다
      state = "end"; overAt = Date.now(); endT = 0; saveBest(N); setStatus();
      return;
    }
    // 부딪힘: 돼지와 장애물 상자를 조금 안쪽으로 줄여서 잰다 (스치는 건 봐준다)
    var px1 = pigX + pigW * 0.22, px2 = pigX + pigW * 0.8, py2 = GROUND - y - 4, py1 = py2 - PIG_H * 0.6;
    for (var i = 0; i < obs.length; i++) {
      var o = obs[i]; if (o.done) continue;
      var ox1 = o.x + 4, ox2 = o.x + o.s.w - 4;
      var hit = px2 > ox1 && px1 < ox2 && (o.s.top ? py1 < LAMP_BOTTOM - 4 : py2 > GROUND - o.s.h + 5);
      if (hit) { state = "over"; overAt = Date.now(); hitAt = o.i; setStatus(); break; }
    }
  }

  function saveBest(n) { best = Math.max(best, n); try { localStorage.setItem("pigCourse", String(best)); } catch (e) {} }

  function perf(i) { return DATA[Math.max(0, Math.min(N - 1, i))] || ["", "", "", ""]; }
  function esc(t) { return String(t).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var touch = window.matchMedia && matchMedia("(pointer: coarse)").matches;
  function setStatus() {                           // 캔버스 아래 한 줄: 안내, 멈춘 공연(작품 페이지로), 완주
    if (!status) return;
    var close = ' · <a href="#" class="hid" data-close style="text-decoration:underline">닫기</a>';
    var h;
    if (state === "over" && hitAt >= 0) {
      var p = perf(hitAt);
      h = '멈춘 곳: <a href="' + esc(p[3]) + '">' + esc(p[0]) + " 〈" + esc(p[1]) + "〉</a>";
    } else if (state === "end") {
      h = '끝. <a href="archive.html">아카이브</a>에서 다시 보기';
    } else {
      h = touch ? "돼지 달리기 · 화면을 눌러 점프" : "돼지 달리기 · 스페이스·↑·화면 누르기로 점프";   // 휴대폰에서 한 줄로
    }
    status.innerHTML = h + close;
  }

  function line(pts, ox, oy) {
    ctx.beginPath(); ctx.moveTo(ox + pts[0][0], oy + pts[0][1]);
    for (var i = 1; i < pts.length; i++) ctx.lineTo(ox + pts[i][0], oy + pts[i][1]);
    ctx.stroke();
  }

  function fitText(t, max) {                       // 자리가 모자라면 말줄임
    if (ctx.measureText(t).width <= max) return t;
    while (t.length > 1 && ctx.measureText(t + "…").width > max) t = t.slice(0, -1);
    return t + "…";
  }

  function draw() {
    ctx.clearRect(0, 0, W, H);
    ctx.strokeStyle = fg; ctx.fillStyle = fg; ctx.lineWidth = 1.6; ctx.lineCap = "round"; ctx.lineJoin = "round";
    // 바닥
    ctx.beginPath();
    for (var x = 0; x <= W; x += 6) {
      var gx = x + dist, gy = GROUND + Math.sin(gx * 0.05) * 0.6 + Math.sin(gx * 0.013) * 0.8;
      if (x === 0) ctx.moveTo(x, gy); else ctx.lineTo(x, gy);
    }
    ctx.stroke();
    ctx.lineWidth = 1.2;
    for (var p = 0; p < 14; p++) {
      var px = (((p * 97 + (p * 53) % 41) - dist) % (W + 40) + W + 40) % (W + 40) - 20, py = GROUND + 6 + (p * 7) % 12;
      ctx.beginPath(); ctx.moveTo(px, py); ctx.lineTo(px + 3 + (p % 3) * 2, py); ctx.stroke();
    }
    // 배튼
    ctx.lineWidth = 1.6; ctx.beginPath();
    for (var bx = 0; bx <= W; bx += 8) {
      var by = BATTEN + Math.sin((bx + dist) * 0.021) * 0.7;
      if (bx === 0) ctx.moveTo(bx, by); else ctx.lineTo(bx, by);
    }
    ctx.stroke();
    // 장애물
    obs.forEach(function (o) {
      if (o.s.top) {
        var top = LAMP_BOTTOM - o.s.h, cx = o.x + o.s.w / 2;
        ctx.beginPath(); ctx.moveTo(cx, BATTEN); ctx.lineTo(cx + 0.6, top + 1); ctx.stroke();   // 내림 파이프
        ctx.save(); ctx.strokeStyle = rule; ctx.lineWidth = 1; ctx.setLineDash([3, 5]);     // 빛
        ctx.beginPath(); ctx.moveTo(o.x + 5, LAMP_BOTTOM + 2); ctx.lineTo(o.x - 10, GROUND - 2);
        ctx.moveTo(o.x + o.s.w - 5, LAMP_BOTTOM + 2); ctx.lineTo(o.x + o.s.w + 10, GROUND - 2); ctx.stroke(); ctx.restore();
        o.s.lines.forEach(function (l) { line(l, o.x, top); });
      } else {
        o.s.lines.forEach(function (l) { line(l, o.x, GROUND - o.s.h); });
      }
    });
    // 막: 양쪽에서 닫혀 온다
    if (state === "end") {
      var c = Math.min(1, endT / 1600), cw = (W / 2) * (1 - Math.pow(1 - c, 3));
      [[0, cw], [W - cw, W]].forEach(function (r) {
        ctx.fillStyle = bg; ctx.fillRect(r[0], BATTEN + 1, r[1] - r[0], GROUND - BATTEN - 1);
        ctx.strokeStyle = fg; ctx.lineWidth = 1.1;
        for (var fx = r[0] + 6; fx < r[1]; fx += 17) {   // 막의 주름
          ctx.beginPath();
          for (var fy = BATTEN + 2; fy <= GROUND; fy += 8) {
            var wx = fx + Math.sin(fy * 0.09 + fx) * 1.6;
            if (fy === BATTEN + 2) ctx.moveTo(wx, fy); else ctx.lineTo(wx, fy);
          }
          ctx.stroke();
        }
      });
      ctx.strokeStyle = fg; ctx.fillStyle = fg; ctx.lineWidth = 1.6;
    }
    // 돼지
    if (pig && tinted && state !== "intro" && state !== "outro") {
      var run = (state === "run" || state === "end") && y === 0, f = run ? Math.floor(frameT / 110) % 2 : 0;
      var bob = run ? (f ? 2.5 : 0) : 0, tilt = y > 0 ? -0.14 : (f ? -0.05 : 0.02);
      if (state === "over") tilt = 0.25;
      ctx.save();
      ctx.translate(pigX + pigW / 2, GROUND - y - bob - PIG_H / 2 + 2);
      ctx.rotate(tilt);
      if (state === "end") { ctx.fillStyle = bg; ctx.fillRect(-pigW / 2 + 3, -PIG_H / 2 + 2, pigW - 6, PIG_H - 6); }   // 막 앞을 지나가는 돼지
      ctx.drawImage(pig, -pigW / 2, -PIG_H / 2, pigW, PIG_H);
      ctx.restore();
    }
    // 위쪽 띠: 연도, 방금 넘은 공연, 진행
    var cur = cleared > 0 ? perf(cleared - 1) : null;
    ctx.textBaseline = "alphabetic"; ctx.textAlign = "left";
    ctx.font = "bold 24px serif";
    var year = state === "over" && hitAt >= 0 ? perf(hitAt)[0] : (cur ? cur[0] : (DATA[0] ? DATA[0][0] : "2006"));
    ctx.fillText(year, 6, 31);
    var yw = ctx.measureText("2006").width + 16;
    ctx.textAlign = "right"; ctx.font = "15px serif";
    ctx.fillText(cleared + " / " + N, W - 6, 20);
    ctx.font = "12px serif"; ctx.fillStyle = rule;
    if (best) ctx.fillText("최고 " + best, W - 6, 36);
    var rightW = 76;
    ctx.textAlign = "left"; ctx.font = "13px serif"; ctx.fillStyle = fg;
    var cap = "";
    if (state === "over" && hitAt >= 0) cap = "〈" + perf(hitAt)[1] + "〉에서 멈췄다";
    else if (cur) cap = "〈" + cur[1] + "〉 " + cur[2];
    else cap = "그린피그, 2006년부터.";
    ctx.fillText(fitText(cap, W - yw - rightW - 6), yw, 30);
    // 가운데 안내
    ctx.textAlign = "center"; ctx.font = "15px serif"; ctx.fillStyle = fg;
    if (state === "ready") { ctx.fillText("2006년부터 지금까지, 공연 " + N + "편을 넘어 보세요", W / 2, 84); ctx.fillStyle = rule; ctx.fillText(touch ? "화면을 누르면 출발" : "스페이스나 화면을 누르면 출발", W / 2, 106); }
    if (state === "over") { ctx.fillText("부딪혔다!", W / 2, 84); ctx.fillStyle = rule; ctx.fillText("처음부터 다시 하려면 누르세요", W / 2, 106); }
    if (state === "end" && goneAt >= 0 && endT > goneAt + 400) {   // 돼지가 나간 뒤, 닫힌 막 위에 글자판
      var msg = "2006–" + perf(N - 1)[0] + " · 공연 " + N + "편 완주";
      ctx.font = "14px serif"; var mw = Math.max(ctx.measureText(msg).width, 60) + 28;
      ctx.fillStyle = bg; ctx.fillRect(W / 2 - mw / 2, 80, mw, 52); ctx.strokeStyle = fg; ctx.lineWidth = 1.2; ctx.strokeRect(W / 2 - mw / 2, 80, mw, 52);
      ctx.fillStyle = fg; ctx.font = "bold 18px serif"; ctx.fillText("커튼콜 없음", W / 2, 102); ctx.font = "14px serif"; ctx.fillText(msg, W / 2, 122);
    }
  }

  function loop(t) {
    raf = requestAnimationFrame(loop);
    var dt = Math.min(40, t - (last || t)); last = t;
    if (t - colorAt > 400) { readColors(); colorAt = t; }
    step(dt); draw();
  }

  function onKey(e) {
    if (e.key === "Escape") { close(); return; }
    if (e.key === " " || e.key === "ArrowUp" || e.key === "w") {
      var tag = (document.activeElement && document.activeElement.tagName) || "";
      if (/INPUT|TEXTAREA|SELECT/.test(tag)) return;
      e.preventDefault(); if (!e.repeat) act();
    }
  }
  function onKeyUp(e) {                             // 초점 남은 버튼·링크가 스페이스로 눌리지 않게
    if (e.key === " " && !/INPUT|TEXTAREA|SELECT/.test((document.activeElement || {}).tagName || "")) e.preventDefault();
  }
  function onVis() { if (document.hidden) { cancelAnimationFrame(raf); raf = 0; } else if (!raf && box) { last = 0; raf = requestAnimationFrame(loop); } }

  function fit() {                                  // 화면 픽셀에 맞춰 선명하게. 좁은 화면에서는 게임 안 폭을 줄여 그림이 덜 작아지게
    var r = Math.min(4, window.devicePixelRatio || 1), cw = canvas.clientWidth || W;
    W = Math.round(Math.max(440, Math.min(600, cw)));
    canvas.style.aspectRatio = W + "/" + H;
    cw = canvas.clientWidth || cw;
    var scale = cw / W * r;
    canvas.width = Math.round(cw * r); canvas.height = Math.round(H * cw / W * r);
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
  }

  // 로고 돼지가 무대로 뛰어내리고(열 때), 로고 자리로 돌아간다(닫을 때)
  function pigRect() {
    var r = canvas.getBoundingClientRect(), k = r.width / W;
    return { cx: r.left + (pigX + pigW / 2) * k, cy: r.top + (GROUND - PIG_H / 2) * k, h: PIG_H * k };
  }
  function flyer(img, rect) {
    var f = img.cloneNode(false);
    f.removeAttribute("id"); f.alt = "";
    f.style.cssText = "position:fixed;margin:0;z-index:20;pointer-events:none;left:" + rect.left + "px;top:" + rect.top + "px;width:" + rect.width + "px;height:" + rect.height + "px";
    document.body.appendChild(f);
    return f;
  }
  function calm() { return window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches; }

  function start() {
    var btn = document.querySelector(".night"), img = btn && btn.querySelector("img");
    logoP = btn && btn.closest("p");
    var from = img ? img.getBoundingClientRect() : null;
    box = document.createElement("div");
    box.id = "pig-game";
    box.innerHTML = '<canvas role="img" aria-label="돼지 달리기. 그린피그 공연 기록을 장애물로 넘는 게임. 스페이스나 화면을 눌러 점프" style="display:block;width:100%;max-width:600px;aspect-ratio:600/' + H + ';touch-action:manipulation;cursor:pointer;-webkit-user-select:none;user-select:none;-webkit-tap-highlight-color:transparent"></canvas>' +
      '<p class="note" style="margin:4px 0 0"></p>';
    if (logoP && logoP.parentNode) { logoP.parentNode.insertBefore(box, logoP); logoP.style.display = "none"; }
    else document.body.insertBefore(box, document.body.firstChild);
    canvas = box.querySelector("canvas"); ctx = canvas.getContext("2d"); status = box.querySelector("p");
    canvas.addEventListener("pointerdown", function (e) { e.preventDefault(); act(); });
    status.addEventListener("click", function (e) { if (e.target.hasAttribute("data-close")) { e.preventDefault(); close(); } });
    if (document.activeElement && document.activeElement.blur) document.activeElement.blur();
    document.addEventListener("keydown", onKey);
    document.addEventListener("keyup", onKeyUp);
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("resize", fit);
    try { best = parseInt(localStorage.getItem("pigCourse") || "0", 10) || 0; } catch (e) { best = 0; }
    fit(); readColors(); reset();
    last = 0; raf = requestAnimationFrame(loop);
    if (!from || calm() || !img.animate) return;
    state = "intro"; busy = true;
    var to = pigRect(), f = flyer(img, from);
    var dx = to.cx - (from.left + from.width / 2), dy = to.cy - (from.top + from.height / 2), s = to.h / from.height;
    var a = f.animate([
      { transform: "translate(0,0) scale(1,1)" },
      { transform: "translate(" + dx * 0.35 + "px," + (Math.min(0, dy) * 0.35 - 30) + "px) scale(1.06,1.06) rotate(-8deg)", offset: 0.35 },
      { transform: "translate(" + dx + "px," + dy + "px) scale(" + (-s) + "," + s + ")" }
    ], { duration: 700, easing: "ease-in" });
    a.onfinish = function () { f.remove(); busy = false; if (state === "intro") { state = "ready"; setStatus(); } };
  }

  function close() {
    if (!box || busy) return;
    var btn = logoP && logoP.querySelector(".night"), img = btn && btn.querySelector("img");
    var from = (!calm() && img && img.animate && state !== "intro") ? pigRect() : null;
    cancelAnimationFrame(raf); raf = 0;
    document.removeEventListener("keydown", onKey);
    document.removeEventListener("keyup", onKeyUp);
    document.removeEventListener("visibilitychange", onVis);
    window.removeEventListener("resize", fit);
    box.parentNode.removeChild(box); box = null; status = null;
    if (logoP) logoP.style.display = "";
    if (!from) return;
    var to = img.getBoundingClientRect(), f = flyer(img, to);
    img.style.visibility = "hidden"; busy = true;
    var s = from.h / to.height, dx = from.cx - (to.left + to.width / 2), dy = from.cy - (to.top + to.height / 2);
    var a = f.animate([
      { transform: "translate(" + dx + "px," + dy + "px) scale(" + (-s) + "," + s + ")" },
      { transform: "translate(" + dx * 0.6 + "px," + (dy * 0.6 - 40) + "px) scale(0.6,0.6) rotate(10deg)", offset: 0.55 },
      { transform: "translate(0,0) scale(1,1)" }
    ], { duration: 650, easing: "ease-out" });
    a.onfinish = function () { f.remove(); img.style.visibility = ""; busy = false; };
  }

  function open() {
    if (box) { act(); return; }
    if (busy) return;
    busy = true;
    var need = 2, go = function () { if (--need === 0) { busy = false; DATA = window.PIG_DATA || []; N = DATA.length; start(); } };
    if (window.PIG_DATA) go(); else { var s = document.createElement("script"); s.src = DATA_SRC; s.onload = go; s.onerror = go; document.head.appendChild(s); }
    if (mask) go(); else loadPig(go);
  }

  window.pigGame = { open: open, close: close };
})();
