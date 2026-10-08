/* إشراقة: أيقونتا «آيفون» و«الحاسوب» بجانب كل زر Google Play (أيقونات فقط؛ الشرح في الرئيسية).
   لا تعمل في: الرئيسية (لها أزرارها الكاملة)، وصفحة المختبرين (الاختبار لأندرويد فقط)، ونسخة التطبيق. */
(function () {
  var path = location.pathname;
  if (/^\/(testers|app|kit|iphone)(\/|$)/.test(path)) return;
  var ua = navigator.userAgent;
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var PHONE = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="6.5" y="2.5" width="11" height="19" rx="2.5"/><path d="M10.5 18.5h3"/></svg>';
  var LAPTOP = '<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4.5" width="16" height="11" rx="1.5"/><path d="M2 19.5h20"/></svg>';
  var css = document.createElement('style');
  css.textContent = '.plat-ic{display:inline-flex;gap:6px;vertical-align:middle;margin-inline-start:8px}' +
    '.plat-ic a{display:inline-grid;place-items:center;width:40px;height:40px;border-radius:12px;background:#111;color:#fff;' +
    'border:1px solid rgba(255,255,255,.22);box-shadow:0 6px 16px rgba(0,0,0,.18);transition:transform .2s}' +
    '.plat-ic a:hover{transform:translateY(-2px)}.plat-ic svg{width:20px;height:20px}' +
    '.nav-r .plat-ic a,.bar .plat-ic a{width:34px;height:34px;border-radius:10px}.nav-r .plat-ic svg{width:17px;height:17px}';
  document.head.appendChild(css);
  function icon(href, label, svg) {
    var a = document.createElement('a');
    a.href = href; a.title = label; a.setAttribute('aria-label', 'إشراقة على ' + label);
    a.innerHTML = svg;
    return a;
  }
  document.querySelectorAll('a[href*="play.google.com/store/apps/details"]').forEach(function (a) {
    if (a.closest('.stores') || a.dataset.platDone) return;
    a.dataset.platDone = '1';
    var box = document.createElement('span');
    box.className = 'plat-ic';
    box.appendChild(icon('/app/', 'آيفون', PHONE));
    if (!ios) box.appendChild(icon('/app/', 'الحاسوب', LAPTOP));
    a.insertAdjacentElement('afterend', box);
    if (ios) a.style.display = 'none';  // لا متجر Play على آيفون
  });
})();
