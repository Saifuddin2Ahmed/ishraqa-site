/* إشراقة: زر «آيفون وماك» يفتح على أجهزة Apple فقط؛ وعلى غيرها رسالة قصيرة. */
(function () {
  var ua = navigator.userAgent;
  var apple = /iPhone|iPad|iPod|Macintosh/.test(ua);
  if (apple) return;
  var msg = 'متاح لأجهزة Apple فقط';
  var css = document.createElement('style');
  css.textContent = '.ao-toast{position:fixed;inset-inline:16px;bottom:24px;margin:auto;max-width:260px;z-index:9999;' +
    'background:#1b1530;color:#fff;padding:14px 18px;border-radius:14px;box-shadow:0 12px 32px rgba(0,0,0,.35);' +
    'font:500 15px/1.7 inherit;text-align:center;opacity:0;transform:translateY(12px);transition:opacity .25s,transform .25s}' +
    '.ao-toast.on{opacity:1;transform:none}@media (prefers-reduced-motion:reduce){.ao-toast{transition:none}}';
  document.head.appendChild(css);
  var t, timer;
  function toast() {
    if (!t) { t = document.createElement('div'); t.className = 'ao-toast'; t.setAttribute('role', 'status'); document.body.appendChild(t); }
    t.textContent = msg;
    requestAnimationFrame(function () { t.classList.add('on'); });
    clearTimeout(timer);
    timer = setTimeout(function () { t.classList.remove('on'); }, 2500);
  }
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[aria-label="إشراقة على آيفون وماك"]');
    if (!a) return;
    e.preventDefault();
    toast();
  }, true);
})();
