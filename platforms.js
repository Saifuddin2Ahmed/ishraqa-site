/* إشراقة: أزرار المتاجر موحّدة في كل الصفحات، بنفس شكل الرئيسية (.stores / .st):
   ثلاث أيقونات متساوية الحجم (Google Play، App Store، Microsoft Store) بلا شارات نصية ولا تكرار.
   كل زر Google Play في محتوى الصفحة يُستبدل بالمجموعة الكاملة، وزر الشريط العلوي يبقى زرًا واحدًا
   (على آيفون يذهب إلى App Store). لا تعمل في: المختبرين (أندرويد فقط)، نسخة التطبيق، عدّة الصحافة، صفحة آيفون. */
(function () {
  var path = location.pathname;
  if (/^\/(testers|app|kit|iphone)(\/|$)/.test(path)) return;
  var ua = navigator.userAgent;
  var ios = /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  var mac = /Macintosh/.test(ua) && !ios;
  var win = /Windows NT/.test(ua);
  // زر واحد: كل جهاز إلى متجره (لا نسخة ويب): آيفون/ماك ← App Store، ويندوز ← Microsoft Store، غيرها ← Google Play
  function route(a) {
    if (ios || mac) { a.href = AS; a.removeAttribute('target'); }
    else if (win) { a.href = MS; a.target = '_blank'; a.rel = 'noopener'; }
  }
  var en = /^en/i.test(document.documentElement.lang);
  var PLAY = 'https://play.google.com/store/apps/details?id=com.taeziz.ishraqa';
  var AS = 'https://apps.apple.com/app/id6826877682';
  var MS = 'https://apps.microsoft.com/detail/9nr3bxwzrdxs';
  var SVG = {
    play: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34A853" d="M3.6 2.2 13.4 12l-9.8 9.8c-.4-.2-.6-.6-.6-1.1V3.3c0-.5.2-.9.6-1.1z"/><path fill="#FBBC04" d="m16.7 15.3-3.3-3.3 3.3-3.3 3.7 2.1c1.1.6 1.1 1.8 0 2.4z"/><path fill="#EA4335" d="M3.6 21.8 13.4 12l3.3 3.3L5 21.9c-.5.3-1 .2-1.4-.1z"/><path fill="#4285F4" d="M3.6 2.2c.4-.3.9-.4 1.4-.1l11.7 6.6L13.4 12z"/></svg>',
    as: '<svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg>',
    ms: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#F25022" d="M2 2h9.6v9.6H2z"/><path fill="#7FBA00" d="M12.4 2H22v9.6h-9.6z"/><path fill="#00A4EF" d="M2 12.4h9.6V22H2z"/><path fill="#FFB900" d="M12.4 12.4H22V22h-9.6z"/></svg>'
  };
  var css = document.createElement('style');
  css.textContent =
    '.stores.plat{display:inline-flex;flex-wrap:wrap;gap:12px;align-items:center;vertical-align:middle;margin:6px 0}' +
    '.stores.plat .st{display:grid;place-items:center;width:58px;height:58px;border-radius:18px;text-decoration:none;' +
    'background:rgba(14,8,22,.82);border:1px solid rgba(255,255,255,.2);box-shadow:0 12px 30px rgba(0,0,0,.28);' +
    'transition:transform .3s cubic-bezier(.2,.7,.2,1),background-color .3s,border-color .3s}' +
    '.stores.plat .st:hover{transform:translateY(-3px);background:rgba(30,16,44,.9);border-color:rgba(248,210,153,.55)}' +
    '.stores.plat .st svg{width:27px;height:27px}' +
    '@media (max-width:480px){.stores.plat{gap:10px}.stores.plat .st{width:54px;height:54px;border-radius:16px}}';
  document.head.appendChild(css);

  function st(kind, href, name, blank) {
    var a = document.createElement('a');
    a.className = 'st'; a.dataset.st = kind; a.href = href; a.title = name;
    a.setAttribute('aria-label', (en ? 'Ishraqa on ' : 'إشراقة يومية على ') + name);
    if (blank) { a.target = '_blank'; a.rel = 'noopener'; }
    a.innerHTML = SVG[kind];
    return a;
  }
  function group() {
    var d = document.createElement('div');
    d.className = 'stores plat';
    d.appendChild(st('play', PLAY, 'Google Play', false));
    d.appendChild(st('as', AS, 'App Store', false));
    d.appendChild(st('ms', MS, 'Microsoft Store', true));
    return d;
  }

  document.querySelectorAll('a[href*="play.google.com/store/apps/details"]').forEach(function (a) {
    if (a.closest('.stores') || a.dataset.platDone) return;
    a.dataset.platDone = '1';
    // الشريط العلوي: زر واحد يبقى كما هو (آيفون ← App Store)
    if (a.classList.contains('nav-cta') || a.closest('.nav-r, nav')) { route(a); return; }
    // رابط نصي داخل فقرة: يبقى رابطًا (آيفون ← App Store)
    if (!a.classList.contains('play') && !a.querySelector('svg')) { route(a); return; }
    // زر متجر في المحتوى: يُستبدل بالمجموعة الموحّدة، ومجموعة واحدة فقط لكل حاوية
    var host = a.parentElement;
    if (host && host.querySelector(':scope > .stores.plat')) { a.remove(); return; }
    a.replaceWith(group());
  });
})();
