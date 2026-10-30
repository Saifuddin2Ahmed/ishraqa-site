/* إشراقة: شارة App Store وأيقونة Windows (Microsoft Store) بجانب كل زر Google Play.
   لا تعمل في: الرئيسية (لها أزرارها الكاملة)، وصفحة المختبرين (الاختبار لأندرويد فقط)، ونسخة التطبيق. */
(function () {
  var path = location.pathname;
  if (/^\/(testers|app|kit|iphone)(\/|$)/.test(path)) return;
  var ua = navigator.userAgent;
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var WIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A84FF" d="M2 2h9.6v9.6H2zM12.4 2H22v9.6h-9.6zM2 12.4h9.6V22H2zM12.4 12.4H22V22h-9.6z"/></svg>';
  var css = document.createElement('style');
  css.textContent = '.plat-ic{display:inline-flex;gap:6px;vertical-align:middle;margin-inline-start:8px}' +
    '.plat-ic a{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:12px;background:#111;color:#fff;' +
    'border:1px solid rgba(255,255,255,.22);box-shadow:0 6px 16px rgba(0,0,0,.18);transition:transform .2s}' +
    '.plat-ic a:hover{transform:translateY(-2px)}.plat-ic svg{width:20px;height:20px}' +
    '.nav-r .plat-ic a,.bar .plat-ic a{width:34px;height:34px;border-radius:10px}.nav-r .plat-ic svg{width:17px;height:17px}' +
    '.plat-ic.big{gap:12px;margin-inline-start:12px}.plat-ic.big a,a.play.ic-only{width:64px;height:64px;border-radius:18px;padding:0;justify-content:center;vertical-align:middle;background:#000;border:0;box-shadow:0 10px 30px rgba(0,0,0,.25)}' +
    '.plat-ic.big svg,a.play.ic-only svg{width:30px;height:30px}a.play.ic-only span{display:none}' +
    'a.play.plat-full,a.play.plat-host{margin:5px;vertical-align:middle}' +
    '.plat-ic a.plat-as,.plat-ic.big a.plat-as{width:auto;height:auto;padding:0;background:none;border:0;border-radius:0;box-shadow:none}' +
    'a.plat-as img{display:block;height:40px;width:auto}.nav-r .plat-ic a.plat-as img,.bar .plat-ic a.plat-as img{height:34px}' +
    '.plat-ic.big a.plat-as img{height:56px}a.plat-as.plat-full{display:inline-block;margin:5px;vertical-align:middle}a.plat-as.plat-full img{height:52px}';
  document.head.appendChild(css);
  var AS = 'https://apps.apple.com/app/id6826877682';
  var en = /^en/i.test(document.documentElement.lang);
  // App Store: الشارة الرسمية دائمًا، لا شعار Apple وحده
  function badge(cls) {
    var a = document.createElement('a');
    a.href = AS; a.title = 'App Store'; a.setAttribute('aria-label', 'App Store');
    a.className = 'plat-as' + (cls ? ' ' + cls : '');
    a.innerHTML = '<img src="/img/badges/app-store-' + (en ? 'en' : 'ar') + '-black.svg" alt="' +
      (en ? 'Download on the App Store' : 'تنزيل من App Store') + '" width="120" height="40">';
    return a;
  }
  function icon(href, label, svg, blank) {
    var a = document.createElement('a');
    a.href = href; a.title = label; a.setAttribute('aria-label', 'إشراقة على ' + label);
    if (blank) { a.target = '_blank'; a.rel = 'noopener'; }
    a.innerHTML = svg;
    return a;
  }
  document.querySelectorAll('a[href*="play.google.com/store/apps/details"]').forEach(function (a) {
    if (a.closest('.stores') || a.dataset.platDone) return;
    // لا أيقونات في الشريط العلوي
    if (a.classList.contains('nav-cta') || a.closest('.nav-r, nav')) return;
    // زر الواجهة (داخل header): أيقونات فقط بحجم واحد
    var big = a.classList.contains('play') && !!a.closest('header');
    a.dataset.platDone = '1';
    // زر Play كامل خارج الواجهة (قسم الدعوة أسفل الصفحة): أزرار كاملة بأسمائها كما في الرئيسية
    if (a.classList.contains('play') && !big) {
      var full = function (href, small, name, svg, label, blank) {
        var b = icon(href, label, svg, blank);
        b.className = 'play plat-full';
        b.innerHTML = svg + '<span><small>' + small + '</small><b>' + name + '</b></span>';
        return b;
      };
      a.classList.add('plat-host');
      var after = a;
      [badge('plat-full'),
       ios ? null : full('https://apps.microsoft.com/detail/9NR3BXWZRDXS?mode=direct', 'احصل عليه من', 'Microsoft Store', WIN, 'ويندوز', true)]
        .forEach(function (b) { if (!b) return; after.insertAdjacentElement('afterend', b); after = b; });
      if (ios) a.style.display = 'none';
      return;
    }
    var box = document.createElement('span');
    box.className = 'plat-ic' + (big ? ' big' : '');
    if (big) a.classList.add('ic-only');
    box.appendChild(badge());
    if (!ios) box.appendChild(icon('https://apps.microsoft.com/detail/9NR3BXWZRDXS?mode=direct', 'ويندوز', WIN, true));
    a.insertAdjacentElement('afterend', box);
    if (ios) a.style.display = 'none';  // لا متجر Play على آيفون
  });
})();
