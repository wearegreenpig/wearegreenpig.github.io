// 소개 페이지 첫 화면의 작품 제목을 1초마다 하나씩 바꿔 보여 준다.
// 볼 때마다 순서를 섞고, 마우스를 올리거나 초점이 가면 멈춰서 누를 수 있게 한다.
// 기기에서 '동작 줄이기'를 켰으면 섞기만 하고 바꾸지 않는다.
(function () {
  document.querySelectorAll(".rotator").forEach(function (box) {
    var items = Array.prototype.slice.call(box.children);
    if (items.length < 2) return;
    for (var i = items.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1)), t = items[i]; items[i] = items[j]; items[j] = t;
    }
    items.forEach(function (el, k) { box.appendChild(el); el.style.display = k ? "none" : "block"; });
    if (window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    var n = 0, paused = false;
    function stop() { paused = true; } function go() { paused = false; }
    box.addEventListener("mouseenter", stop); box.addEventListener("mouseleave", go);
    box.addEventListener("focusin", stop); box.addEventListener("focusout", go);
    setInterval(function () {
      if (paused || document.hidden) return;
      items[n].style.display = "none";
      n = (n + 1) % items.length;
      items[n].style.display = "block";
    }, 1000);
  });
})();
