/* إشراقة · الرئيسية v2: فيديو الواجهة، والمشاهد مع التمرير، والاقتباسات، والمشهد السينمائي.
   الفيديو لا يُحمَّل إلا بعد اكتمال الصفحة، ولا يعمل مع «تقليل الحركة» أو «توفير البيانات». */
(function () {
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var en = /^en/i.test(document.documentElement.lang);
  var $ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var clamp = function (v) { return v < 0 ? 0 : v > 1 ? 1 : v; };

  /* ١) فيديو الواجهة: صامت، يعمل وحده، بلا أي أزرار تحكّم.
     الصورة الثابتة تبقى ظاهرة، ولا يظهر الفيديو إلا حين يبدأ فعلًا؛ فإن منعه المتصفح
     (وضع توفير الطاقة في iOS مثلًا) بقيت الصورة بهدوء دون أي علامة تشغيل. */
  var hero = document.querySelector('.hero'), v = document.getElementById('hv');
  var sd = navigator.connection && navigator.connection.saveData;
  if (v) { v.controls = false; v.removeAttribute('controls'); }
  if (hero && v && !rm && !sd) {
    var vis = true, base = v.getAttribute('data-base'), loaded = false;
    var sync = function () {
      if (!loaded) return;
      if (vis && !document.hidden) { var p = v.play(); if (p && p.catch) p.catch(function () {}); }
      else v.pause();
    };
    var start = function () {
      var portrait = matchMedia('(max-aspect-ratio: 4/5)').matches, name = portrait ? 'hero-m' : 'hero-1280';
      v.muted = true; v.defaultMuted = true; v.playsInline = true; v.loop = true;
      v.setAttribute('muted', ''); v.setAttribute('playsinline', '');
      [['webm', 'video/webm'], ['mp4', 'video/mp4']].forEach(function (t) {
        var s = document.createElement('source'); s.src = base + name + '.' + t[0]; s.type = t[1]; v.appendChild(s); });
      v.addEventListener('playing', function () { v.classList.add('on'); }, { once: true });
      loaded = true; v.load(); sync();
    };
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) { vis = es[0].isIntersecting; sync(); }).observe(hero);
    document.addEventListener('visibilitychange', sync);
    if (document.readyState === 'complete') setTimeout(start, 200); else addEventListener('load', function () { setTimeout(start, 200); });
  }

  /* ٢) الظهور عند التمرير */
  var rv = $('.rv');
  if ('IntersectionObserver' in window && !rm) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .15 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  /* ٣) الاقتباسات تتبدّل بهدوء */
  var qb = document.getElementById('quotes');
  if (qb) {
    var q = $('.q', qb), d = $('.dots button', qb), qi = 0, qt;
    var go = function (n) { q[qi].classList.remove('on'); d[qi].classList.remove('on'); d[qi].removeAttribute('aria-current');
      qi = (n + q.length) % q.length; q[qi].classList.add('on'); d[qi].classList.add('on'); d[qi].setAttribute('aria-current', 'true'); };
    var run = function () { clearInterval(qt); if (!rm) qt = setInterval(function () { if (!document.hidden) go(qi + 1); }, 7000); };
    d.forEach(function (x, k) { x.addEventListener('click', function () { go(k); run(); }); });
    qb.addEventListener('focusin', function () { clearInterval(qt); });
    qb.addEventListener('focusout', run);
    run();
  }

  /* ٤) المشهد السينمائي: يتبدّل في مكانه مع التمرير */
  var kc = document.querySelector('.kc'), kcf = null;
  if (kc) {
    var bg = $('.kc-bg', kc), sc = $('.kc-scene', kc), bt = $('.kc-rail button', kc), cur = 0;
    var set = function (i) { if (i === cur) return; [bg, sc, bt].forEach(function (l) { l[cur].classList.remove('on'); l[i].classList.add('on'); });
      bt[cur].removeAttribute('aria-current'); bt[i].setAttribute('aria-current', 'true'); cur = i; };
    bt[0].setAttribute('aria-current', 'true');
    bt.forEach(function (b, i) { b.addEventListener('click', function () {
      var r = kc.getBoundingClientRect(), h = r.height - innerHeight;
      scrollTo({ top: scrollY + r.top + h * (i + 0.5) / sc.length, behavior: rm ? 'auto' : 'smooth' }); }); });
    kcf = function () { var r = kc.getBoundingClientRect(), h = r.height - innerHeight, p = clamp(-r.top / (h > 0 ? h : 1));
      kc.style.setProperty('--p', p.toFixed(3)); set(Math.min(sc.length - 1, Math.floor(p * sc.length * 0.999))); };
  }

  /* ٥) كيف تكبر فكرة: خط يمتلئ وعُقد تضيء */
  var kj = document.querySelector('.k-journey'), kn = kj ? $('.k-node', kj) : [];
  var kjf = function () { if (!kj) return; var r = kj.getBoundingClientRect(), p = rm ? 1 : clamp((innerHeight * .75 - r.top) / (r.height || 1));
    kj.style.setProperty('--p', p.toFixed(3)); kn.forEach(function (n, i) { n.classList.toggle('lit', p >= (i + .35) / kn.length); }); };

  /* ٦) المشاهد بعرض الشاشة، وشريط الشاشات، وحركة الواجهة */
  var scenes = $('.sv-scene'), track = document.querySelector('.sv-track'), band = track && track.parentElement,
      ctaImg = document.querySelector('.cta-scene'), heroIn = document.querySelector('.hero-in > .wrap');
  var rtl = document.documentElement.dir === 'rtl';
  var motion = function () {
    var vh = innerHeight;
    scenes.forEach(function (s) { var r = s.getBoundingClientRect(); if (r.bottom < -50 || r.top > vh + 50) return;
      s.style.setProperty('--k', clamp((vh - r.top) / (vh * .85)).toFixed(3));
      s.style.setProperty('--py', ((r.top + r.height / 2 - vh / 2) * -0.06).toFixed(1) + 'px'); });
    if (track && band) { var b = band.getBoundingClientRect();
      if (b.bottom > 0 && b.top < vh) { var p = clamp((vh - b.top) / (vh + b.height)), span = Math.max(0, track.scrollWidth - innerWidth);
        var x = span / 2 + (.5 - p) * (span + innerWidth * .1); track.style.setProperty('--x', (rtl ? x : -x).toFixed(1) + 'px'); } }
    if (ctaImg) { var c = ctaImg.getBoundingClientRect(); if (c.top < vh && c.bottom > 0)
      ctaImg.style.setProperty('--py', ((c.top + c.height / 2 - vh / 2) * -0.08).toFixed(1) + 'px'); }
    if (heroIn) { var y = Math.min(scrollY, vh); heroIn.style.setProperty('--hy', (y * .25).toFixed(1) + 'px'); heroIn.style.setProperty('--ho', (1 - y / (vh * .7)).toFixed(3)); }
  };

  var ticking = false;
  var frame = function () { ticking = false; if (kcf) kcf(); kjf(); if (!rm) motion(); };
  var onScroll = function () { if (!ticking) { ticking = true; requestAnimationFrame(frame); } };
  addEventListener('scroll', onScroll, { passive: true });
  addEventListener('resize', onScroll);
  frame();

  /* ٧) آيفون وآيباد: متجر App Store وحده */
  var ua = navigator.userAgent;
  if (/iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)) {
    $('.stores a[data-st="play"], .stores a[data-st="ms"]').forEach(function (a) { a.style.display = 'none'; });
    $('a.nav-cta[href*="play.google.com"]').forEach(function (a) { a.href = 'https://apps.apple.com/app/id6826877682'; });
  }
})();
