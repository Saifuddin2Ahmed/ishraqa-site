/* إشراقة: فقاعة «حمّل التطبيق» في الرئيسية بدل زر الشريط العلوي.
   تظهر بعد 6 ثوانٍ، ومرة أخرى عند الوصول إلى آخر الصفحة، ولها زر إغلاق. الزر يأخذ كل جهاز إلى متجره. */
(function () {
  var en = /^en/i.test(document.documentElement.lang);
  var ua = navigator.userAgent;
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var mac = /Macintosh/.test(ua) && !ios, win = /Windows NT/.test(ua);
  var href = (ios || mac) ? 'https://apps.apple.com/app/id6826877682'
    : win ? 'https://apps.microsoft.com/detail/9nr3bxwzrdxs'
    : 'https://play.google.com/store/apps/details?id=com.taeziz.ishraqa';
  var icon = document.querySelector('.brand img');
  var css = document.createElement('style');
  css.textContent =
    '.ga{position:fixed;z-index:70;left:50%;bottom:22px;display:flex;align-items:center;gap:12px;padding:8px 8px 8px 14px;' +
    'border-radius:999px;background:rgba(18,10,28,.86);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);' +
    'border:1px solid rgba(255,255,255,.16);box-shadow:0 22px 60px rgba(4,1,10,.6);color:#fff;font-family:inherit;' +
    'transform:translate(-50%,30px);opacity:0;pointer-events:none;transition:transform .6s cubic-bezier(.16,.84,.24,1),opacity .5s;white-space:nowrap}' +
    '.ga.in{transform:translate(-50%,0);opacity:1;pointer-events:auto}' +
    '.ga img{width:36px;height:36px;border-radius:10px}' +
    '.ga b{font-size:15px;font-weight:800}' +
    '.ga a{display:inline-flex;align-items:center;padding:10px 18px;border-radius:999px;font-weight:800;font-size:14.5px;text-decoration:none;' +
    'color:#1d0f2b;background:linear-gradient(135deg,#ffd59a,#f59e51);box-shadow:0 8px 22px rgba(245,158,81,.35)}' +
    '.ga a:hover{filter:brightness(1.06)}' +
    '.ga button{width:34px;height:34px;border:0;border-radius:50%;background:rgba(255,255,255,.1);color:#fff;font-size:18px;line-height:34px;cursor:pointer;padding:0}' +
    '.ga button:hover{background:rgba(255,255,255,.2)}' +
    '@media (max-width:520px){.ga{bottom:14px;gap:10px;padding:6px 6px 6px 10px}.ga b{display:none}.ga a{padding:9px 16px;font-size:14px}}' +
    '.ap-on .ga.in{transform:translate(-50%,30px);opacity:0;pointer-events:none}' +
    '@media (prefers-reduced-motion:reduce){.ga{transition:opacity .2s}}' +
    'footer.sfoot{padding-bottom:96px}';
  document.head.appendChild(css);
  var el = document.createElement('div');
  el.className = 'ga'; el.setAttribute('role', 'dialog'); el.setAttribute('aria-label', en ? 'Get the app' : 'حمّل التطبيق');
  el.innerHTML = (icon ? '<img src="' + icon.getAttribute('src') + '" alt="">' : '') +
    '<b>' + (en ? 'Ishraqa Daily' : 'إشراقة يومية') + '</b>' +
    '<a href="' + href + '"' + (win ? ' target="_blank" rel="noopener"' : '') + '>' + (en ? 'Get the app' : 'حمّل التطبيق') + '</a>' +
    '<button type="button" aria-label="' + (en ? 'Close' : 'إغلاق') + '">×</button>';
  document.body.appendChild(el);
  var times = 0, open = false;
  function show() { if (open || times >= 2) return; open = true; times++; el.classList.add('in'); }
  function hide() { open = false; el.classList.remove('in'); }
  el.querySelector('button').addEventListener('click', hide);
  // الهاتف: أزرار المتاجر ظاهرة أسفل الواجهة، فلا تظهر الفقاعة فوقها حتى يتجاوزها الزائر
  var narrow = innerWidth <= 820, waited = false;
  var ready = function () { return !narrow || scrollY > innerHeight * 0.6; };
  setTimeout(function () { waited = true; if (ready()) show(); }, 6000);
  addEventListener('scroll', function () { if (waited && times === 0 && ready()) show(); }, { passive: true });
  addEventListener('scroll', function () {
    if (times === 1 && !open && innerHeight + scrollY >= document.documentElement.scrollHeight - 160) show();
  }, { passive: true });
})();
