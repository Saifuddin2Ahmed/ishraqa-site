/* إشراقة: لمسات حيّة مشتركة بين صفحات الموقع
   - .phone فيها أكثر من صورة: تتبدّل الشاشات كل بضع ثوانٍ
   - .term[data-lines]: كود يُكتب أمامك سطرًا سطرًا ثم يعيد
   كل ذلك يتوقف لمن فعّل «تقليل الحركة»، ويتوقف حين تكون الصفحة خارج الشاشة. */
(function () {
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;

  function whenVisible(el, cb) {
    if (!('IntersectionObserver' in window)) return cb(true);
    new IntersectionObserver(function (es) { cb(es[0].isIntersecting); }).observe(el);
  }

  // الهاتف: شاشات تتبدّل
  document.querySelectorAll('.phone').forEach(function (ph) {
    var imgs = ph.querySelectorAll('img');
    if (imgs.length < 2) return;
    var i = 0, vis = true, cap = ph.parentElement.querySelector('.phone-cap');
    imgs.forEach(function (im, k) { if (k) im.loading = 'lazy'; });
    whenVisible(ph, function (v) { vis = v; });
    function go() {
      imgs[i].classList.remove('on');
      i = (i + 1) % imgs.length;
      imgs[i].classList.add('on');
      if (cap && imgs[i].dataset.cap) cap.textContent = imgs[i].dataset.cap;
    }
    // لمسة على الهاتف (أو على «المس الشاشة») تُظهر الشاشة التالية فورًا، مع اهتزازة خفيفة
    var timer = null, hint = ph.parentElement.querySelector('.phone-hint');
    function tap() {
      go();
      ph.classList.add('tap');
      setTimeout(function () { ph.classList.remove('tap'); }, 160);
      if (navigator.vibrate) navigator.vibrate(8);
      if (timer) { clearInterval(timer); start(); }
    }
    ph.addEventListener('click', tap);
    if (hint) {
      hint.addEventListener('click', tap);
      hint.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tap(); } });
    }
    function start() {
      timer = setInterval(function () { if (vis && !document.hidden) go(); }, 3600);
    }
    if (rm) return;
    start();
  });

  // الطرفية: كود يُكتب
  document.querySelectorAll('.term[data-lines]').forEach(function (t) {
    var lines;
    try { lines = JSON.parse(t.dataset.lines); } catch (e) { return; }
    function line(l) {
      var d = document.createElement('div');
      d.className = 'ln ' + (l.o ? 'out' : 'cmd');
      if (!l.o) { var p = document.createElement('span'); p.className = 'p'; p.textContent = '$ '; d.appendChild(p); }
      var s = document.createElement('bdi'); d.appendChild(s);
      t.appendChild(d);
      return s;
    }
    if (rm) { lines.forEach(function (l) { line(l).textContent = l.s; }); return; }
    var vis = true, cur = document.createElement('span');
    cur.className = 'cur'; cur.textContent = '▍';
    whenVisible(t, function (v) { vis = v; });
    function run() {
      t.textContent = '';
      var n = 0;
      (function next() {
        if (n >= lines.length) { t.appendChild(cur); return setTimeout(run, 4200); }
        var l = lines[n++], el = line(l);
        if (l.o) { el.textContent = l.s; return setTimeout(next, 380); }
        var c = 0;
        el.parentNode.appendChild(cur);
        (function type() {
          if (!vis || document.hidden) return setTimeout(type, 400);
          el.textContent = l.s.slice(0, ++c);
          if (c < l.s.length) setTimeout(type, 38 + Math.random() * 45);
          else setTimeout(next, 520);
        })();
      })();
    }
    run();
  });
})();
