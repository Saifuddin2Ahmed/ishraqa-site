/* إشراقة: يفتح الموقع بلغة جهاز الزائر في أول صفحة يزورها في الجلسة،
   إن كان للصفحة نظير بتلك اللغة (link rel=alternate hreflang).
   اختيار الزائر اليدوي (رابط English / العربية) يُحفظ ويُحترم دائمًا. لا يعمل لمحركات البحث. */
(function () {
  try {
    var ua = navigator.userAgent || '';
    if (/bot|crawl|spider|slurp|lighthouse|inspection|preview|facebookexternalhit|whatsapp|telegram|discord|headless/i.test(ua)) return;
    var K = 'ishraqa-lang', S = 'ishraqa-lang-checked';
    var store = function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} };
    var read = function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } };
    // اختيار يدوي: رابطا اللغة في الشريط العلوي والتذييل
    document.addEventListener('click', function (e) {
      var a = e.target && e.target.closest ? e.target.closest('a[hreflang]') : null;
      if (!a) return;
      var t = (a.textContent || '').trim();
      if (t === 'English' || t === 'العربية') store(K, a.getAttribute('hreflang').slice(0, 2));
    }, true);
    var first = false;
    try { first = !sessionStorage.getItem(S); sessionStorage.setItem(S, '1'); } catch (e) { first = false; }
    var pref = read(K);
    if (!pref && !first) return;
    var dev = ((navigator.languages && navigator.languages[0]) || navigator.language || 'ar').slice(0, 2).toLowerCase();
    var want = pref || (dev === 'ar' ? 'ar' : 'en');
    var cur = (document.documentElement.lang || 'ar').slice(0, 2).toLowerCase();
    if (want === cur) return;
    var alt = document.querySelector('link[rel="alternate"][hreflang="' + want + '"]');
    if (!alt) return;
    var href = alt.getAttribute('href');
    if (!href || href.split('?')[0] === location.href.split(/[?#]/)[0]) return;
    location.replace(href.split('?')[0] + location.search + location.hash);
  } catch (e) {}
})();
