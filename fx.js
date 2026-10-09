/* إشراقة fx: حركة موحّدة لكل الصفحات، بلا تعديل على محتوى الصفحات نفسها.
   عناوين كلمة كلمة، وظهور متتابع للبطاقات، وصور كالستارة، وميل البطاقات، وأزرار مغناطيسية،
   وشريط تقدّم القراءة. يتوقف كله مع «تقليل الحركة»، ولا يعمل في نسخة التطبيق /app/. */
(function () {
  if (/^\/app(\/|$)/.test(location.pathname)) return;
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var $ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var skip = '.kc, .kh, .kd, header, nav, footer, .top, .bar, .hero, .hero-a, .hero-i';
  var io = ('IntersectionObserver' in window) && !rm ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('fx-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px' }) : null;
  function watch(el) { if (io) io.observe(el); else el.classList.add('fx-in'); }

  /* ١) العناوين: كلمة كلمة */
  $('main h2, main h3.k-head, section h2').forEach(function (h) {
    if (h.closest(skip) || h.dataset.fx || h.querySelector('img,svg')) return;
    h.dataset.fx = '1';
    var n = 0;
    [].slice.call(h.childNodes).forEach(function (node) {
      if (node.nodeType !== 3 || !node.textContent.trim()) return;
      var frag = document.createDocumentFragment();
      node.textContent.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
        var s = document.createElement('span'); s.className = 'fx-w'; s.style.setProperty('--w', n++); s.textContent = part;
        frag.appendChild(s);
      });
      h.replaceChild(frag, node);
    });
    if (n) watch(h);
  });

  /* ٢) ظهور متتابع لعناصر الشبكات (يعمل مع .rv الموجود في الصفحات) */
  var grids = $('.features, .k-two, .grid, .gallery, .stats, .steps, .shots, .list');
  grids.forEach(function (g) {
    [].slice.call(g.children).forEach(function (c, i) { c.style.transitionDelay = Math.min(i * 70, 420) + 'ms'; });
  });
  /* بعد اكتمال الظهور يُزال التأخير حتى لا يبطئ ميل البطاقات */
  var clear = function (g) { setTimeout(function () { [].slice.call(g.children).forEach(function (c) { c.style.transitionDelay = ''; }); }, 1600); };
  if ('IntersectionObserver' in window) {
    var gio = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { clear(e.target); gio.unobserve(e.target); } }); });
    grids.forEach(function (g) { gio.observe(g); });
  } else grids.forEach(clear);

  /* ٣) الصور: تنكشف كالستارة */
  $('main img').forEach(function (im) {
    if (im.closest(skip + ', .card, .feat, .store, .play, .kg, .avatar, .devcard') || im.width < 120) return;
    im.classList.add('fx-img'); watch(im);
  });

  /* ٤) كلمات بارزة داخل النص */
  $('main p strong, main p b').forEach(function (b) { if (!b.closest(skip)) { b.classList.add('fx-mark'); watch(b); } });

  if (rm) return;

  /* ٥) شريط تقدّم القراءة في الصفحات الطويلة */
  if (!document.querySelector('.progress') && document.body.scrollHeight > innerHeight * 2.2) {
    var bar = document.createElement('div'); bar.className = 'fx-bar'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
    var up = function () { var h = document.documentElement.scrollHeight - innerHeight; bar.style.setProperty('--fxp', h > 0 ? (scrollY / h).toFixed(4) : 0); };
    addEventListener('scroll', up, { passive: true }); up();
  }

  if (!fine) return;

  /* ٦) البطاقات تميل مع المؤشر، وضوء يتبعه */
  $('.f, .card, .feat, .k-col, .kh-card, .devcard, .kd-card, .k-path, .tl > div, .steps > div').forEach(function (c) {
    if (c.closest('.kc')) return;
    c.classList.add('fx-tilt'); if (getComputedStyle(c).position === 'static') c.style.position = 'relative';
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect(), x = (e.clientX - r.left) / r.width, y = (e.clientY - r.top) / r.height;
      c.classList.add('fx-hot');
      c.style.transform = 'perspective(900px) rotateX(' + ((0.5 - y) * 6).toFixed(2) + 'deg) rotateY(' + ((x - 0.5) * 8).toFixed(2) + 'deg) translateY(-3px)';
      c.style.setProperty('--mx', (x * 100).toFixed(1) + '%'); c.style.setProperty('--my', (y * 100).toFixed(1) + '%');
    });
    c.addEventListener('pointerleave', function () { c.classList.remove('fx-hot'); c.style.transform = ''; });
  });

  /* ٧) أزرار مغناطيسية */
  $('.play, .store, .btn.main, .dev-btn, .nav-cta, .kc-rail button').forEach(function (b) {
    b.classList.add('fx-mag');
    b.addEventListener('pointermove', function (e) {
      var r = b.getBoundingClientRect();
      b.style.transform = 'translate(' + ((e.clientX - r.left - r.width / 2) * 0.18).toFixed(1) + 'px,' + ((e.clientY - r.top - r.height / 2) * 0.25).toFixed(1) + 'px)';
    });
    b.addEventListener('pointerleave', function () { b.style.transform = ''; });
  });
})();
