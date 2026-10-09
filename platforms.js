/* إشراقة: أيقونتا Apple (آيفون وماك) وWindows (Microsoft Store) بجانب كل زر Google Play.
   لا تعمل في: الرئيسية (لها أزرارها الكاملة)، وصفحة المختبرين (الاختبار لأندرويد فقط)، ونسخة التطبيق. */
(function () {
  var path = location.pathname;
  if (/^\/(testers|app|kit|iphone)(\/|$)/.test(path)) return;
  var ua = navigator.userAgent;
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var APPLE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>';
  var WIN = '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A84FF" d="M2 2h9.6v9.6H2zM12.4 2H22v9.6h-9.6zM2 12.4h9.6V22H2zM12.4 12.4H22V22h-9.6z"/></svg>';
  var css = document.createElement('style');
  css.textContent = '.plat-ic{display:inline-flex;gap:6px;vertical-align:middle;margin-inline-start:8px}' +
    '.plat-ic a{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:12px;background:#111;color:#fff;' +
    'border:1px solid rgba(255,255,255,.22);box-shadow:0 6px 16px rgba(0,0,0,.18);transition:transform .2s}' +
    '.plat-ic a:hover{transform:translateY(-2px)}.plat-ic svg{width:20px;height:20px}' +
    '.nav-r .plat-ic a,.bar .plat-ic a{width:34px;height:34px;border-radius:10px}.nav-r .plat-ic svg{width:17px;height:17px}' +
    '.plat-ic.big{gap:12px;margin-inline-start:12px}.plat-ic.big a,a.play.ic-only{width:64px;height:64px;border-radius:18px;padding:0;justify-content:center;vertical-align:middle;background:#000;border:0;box-shadow:0 10px 30px rgba(0,0,0,.25)}' +
    '.plat-ic.big svg,a.play.ic-only svg{width:30px;height:30px}a.play.ic-only span{display:none}' +
    'a.play.plat-full,a.play.plat-host{margin:5px;vertical-align:middle}';
  document.head.appendChild(css);
  // زرّا آيفون وماك لأجهزة Apple فقط (apple-only.js)
  var ao = document.createElement('script'); ao.src = '/apple-only.js'; ao.defer = true; document.head.appendChild(ao);
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
      [full('/app/', 'متوفر على', 'آيفون وماك', APPLE, 'آيفون وماك'),
       ios ? null : full('https://apps.microsoft.com/detail/9NR3BXWZRDXS?mode=direct', 'احصل عليه من', 'Microsoft Store', WIN, 'ويندوز', true)]
        .forEach(function (b) { if (!b) return; after.insertAdjacentElement('afterend', b); after = b; });
      if (ios) a.style.display = 'none';
      return;
    }
    var box = document.createElement('span');
    box.className = 'plat-ic' + (big ? ' big' : '');
    if (big) a.classList.add('ic-only');
    box.appendChild(icon('/app/', 'آيفون وماك', APPLE));
    if (!ios) box.appendChild(icon('https://apps.microsoft.com/detail/9NR3BXWZRDXS?mode=direct', 'ويندوز', WIN, true));
    a.insertAdjacentElement('afterend', box);
    if (ios) a.style.display = 'none';  // لا متجر Play على آيفون
  });
})();
