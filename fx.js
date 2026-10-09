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


  /* ٨) «حمّل التطبيق» في الشريط العلوي: نافذة بالمتاجر الثلاثة */
  (function () {
    var cta = $('a.nav-cta');
    if (!cta.length || !document.createElement('dialog').showModal) return;
    var ua = navigator.userAgent, apple = /iPhone|iPad|iPod|Macintosh/.test(ua);
    var d = document.createElement('dialog'); d.className = 'fx-get'; d.setAttribute('aria-label', 'حمّل إشراقة يومية');
    d.innerHTML = '<button class="x" type="button" aria-label="إغلاق">×</button><img src="/img/icon-192.png" alt="" width="64" height="64"><h3>حمّل إشراقة يومية</h3><div class="gs">' +
      '<a href="https://play.google.com/store/apps/details?id=com.taeziz.ishraqa"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34A853" d="M3.6 2.2 13.4 12l-9.8 9.8c-.4-.2-.6-.6-.6-1.1V3.3c0-.5.2-.9.6-1.1z"/><path fill="#FBBC04" d="m16.7 15.3-3.3-3.3 3.3-3.3 3.7 2.1c1.1.6 1.1 1.8 0 2.4z"/><path fill="#EA4335" d="M3.6 21.8 13.4 12l3.3 3.3L5 21.9c-.5.3-1 .2-1.4-.1z"/><path fill="#4285F4" d="M3.6 2.2c.4-.3.9-.4 1.4-.1l11.7 6.6L13.4 12z"/></svg><span><small>احصل عليه من</small><b>Google Play</b></span></a>' +
      '<a href="/app/" data-apple><svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg><span><small>متوفر على</small><b>آيفون وماك</b><span class="hint" hidden>متاح لأجهزة Apple فقط</span></span></a>' +
      '<a href="https://apps.microsoft.com/detail/9NR3BXWZRDXS?mode=direct" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A84FF" d="M2 2h9.6v9.6H2zM12.4 2H22v9.6h-9.6zM2 12.4h9.6V22H2zM12.4 12.4H22V22h-9.6z"/></svg><span><small>احصل عليه من</small><b>Microsoft Store</b></span></a></div>';
    document.body.appendChild(d);
    d.querySelector('.x').addEventListener('click', function () { d.close(); });
    d.addEventListener('click', function (e) { if (e.target === d) d.close(); });
    var ap = d.querySelector('[data-apple]');
    ap.addEventListener('click', function (e) { if (!apple) { e.preventDefault(); e.stopPropagation(); ap.querySelector('.hint').hidden = false; } }, true);
    cta.forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); d.showModal(); }); });
  })();

  if (rm) return;

  /* ٥) شريط تقدّم القراءة في الصفحات الطويلة */
  if (!document.querySelector('.progress') && document.body.scrollHeight > innerHeight * 2.2) {
    var bar = document.createElement('div'); bar.className = 'fx-bar'; bar.setAttribute('aria-hidden', 'true'); document.body.appendChild(bar);
    var up = function () { var h = document.documentElement.scrollHeight - innerHeight; bar.style.setProperty('--fxp', h > 0 ? (scrollY / h).toFixed(4) : 0); };
    addEventListener('scroll', up, { passive: true }); up();
  }

  if (!fine) return;

  /* ٦) البطاقات تميل مع المؤشر، وضوء يتبعه */
  $('.f, .card, .feat, .k-col, .kh-card, .devcard, .k-path, .tl > div, .steps > div').forEach(function (c) {
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
