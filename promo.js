/* إشراقة: بطاقة صغيرة تقترح مقالًا من مقالات إشراقة (مرة في الجلسة، تُغلق بسهولة).
   عربية فقط لأن المقالات بالعربية. القائمة هنا تُحدَّث يدويًا. */
(function () {
  if ((document.documentElement.lang || '').slice(0, 2) !== 'ar') return;
  var K = 'ishraqa-promo';
  try { if (sessionStorage.getItem(K)) return; } catch (e) {}
  var C = 'https://jytbowsfvuzdnsmhmsly.supabase.co/storage/v1/object/public/article-covers/';
  var A = [
    ['mans-search-for-meaning', 'الإنسان والبحث عن المعنى: الكتاب الذي علّمنا كيف نصمد', 'articles/frankl/cover.jpg'],
    ['timbuktu-manuscripts', 'مخطوطات تمبكتو: مكتبات حرستها العائلات قرونًا', 'articles/2026-10/timbuktu-manuscripts.jpg'],
    ['african-griots-storytelling', 'الغريو: مكتباتٌ تمشي على قدمين', 'articles/2026-10/african-griots-storytelling.jpg'],
    ['remember-what-you-read', 'اقرأ لتتذكّر: كيف يبقى الكتاب فيك بعد أن تغلقه', 'articles/2026-10/remember-what-you-read.jpg'],
    ['cheap-evidence-chain-of-trust', 'كيف تثق بأي شيء حين يمكن تزييف كل شيء؟', 'articles/2026-10/cheap-evidence-chain-of-trust.jpg'],
    ['why-ai-makes-things-up', 'حين يخطئ الذكاء الاصطناعي بثقة: كيف تتحقّق؟', 'articles/2026-10/why-ai-makes-things-up.jpg'],
    ['unmediated-hour-after-2030', 'ما الذي ستأخذه منك التقنية بعد 2030؟', 'articles/2026-10/unmediated-hour-after-2030.jpg'],
    ['moon-phases-explained', 'لماذا يتبدّل وجه القمر؟ رحلة شهرية بين الهلال والبدر', 'articles/2026-10/moon-phases-explained.jpg'],
    ['myth-of-multitasking', 'خرافة تعدد المهام: لماذا تُنجز أكثر حين تفعل شيئًا واحدًا', 'articles/2026-10/myth-of-multitasking.jpg'],
    ['reading-aloud-to-children', 'اقرأ لطفلك بصوت عالٍ: عشر دقائق تبني لغة وحبًّا', 'articles/2026-10/reading-aloud-to-children.jpg'],
    ['english-spaced-repetition', 'ربع ساعة يوميًا: الإنجليزية بالمراجعة المتباعدة', 'articles/2026-10/english-spaced-repetition.jpg'],
    ['sudanese-proverbs-mirror', 'الأمثال السودانية: مرآة مجتمع يحكي نفسه', 'stocksnap/72AMIX2KTZ.jpg']
  ];
  var a = A[Math.floor(Math.random() * A.length)];
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var css = document.createElement('style');
  css.textContent =
    '.ap{position:fixed;z-index:60;inset-inline-start:20px;bottom:20px;width:min(360px,calc(100vw - 32px));display:flex;gap:14px;align-items:center;' +
    'padding:12px 12px 12px 40px;border-radius:20px;background:rgba(18,10,28,.88);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);' +
    'border:1px solid rgba(255,255,255,.14);box-shadow:0 24px 60px rgba(4,1,10,.55);color:#fff;text-decoration:none;font-family:inherit;' +
    'transform:translateY(24px);opacity:0;transition:transform .6s cubic-bezier(.16,.84,.24,1),opacity .6s}' +
    '.ap.in{transform:none;opacity:1}' +
    '.ap img{flex:none;width:72px;height:72px;border-radius:14px;object-fit:cover;background:#2a1b3d}' +
    '.ap b{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;font-size:15px;line-height:1.55;font-weight:700}' +
    '.ap span{display:block;margin-top:4px;font-size:13px;color:#f6c48a;font-weight:700}' +
    '.ap button{position:absolute;top:8px;inset-inline-end:8px;width:28px;height:28px;border:0;border-radius:50%;background:rgba(255,255,255,.1);' +
    'color:#fff;font-size:16px;line-height:28px;cursor:pointer;padding:0}' +
    '.ap button:hover{background:rgba(255,255,255,.2)}.ap:hover{border-color:rgba(248,210,153,.5)}' +
    '@media (max-width:520px){.ap{inset-inline:16px;bottom:16px;width:auto}}' +
    '@media (prefers-reduced-motion:reduce){.ap{transition:none}}';
  document.head.appendChild(css);
  var el = document.createElement('a');
  el.className = 'ap'; el.href = '/a/' + a[0] + '/';
  el.setAttribute('aria-label', 'مقال مقترح: ' + a[1]);
  el.innerHTML = '<img src="' + C + a[2] + '" alt="" loading="lazy" decoding="async"><div><b></b><span>اقرأ المقال ←</span></div><button type="button" aria-label="إغلاق">×</button>';
  el.querySelector('b').textContent = a[1];
  var done = function () { try { sessionStorage.setItem(K, '1'); } catch (e) {} };
  el.querySelector('button').addEventListener('click', function (e) {
    e.preventDefault(); e.stopPropagation(); done();
    el.classList.remove('in'); setTimeout(function () { el.remove(); }, rm ? 0 : 600);
  });
  el.addEventListener('click', done);
  var shown = false;
  var show = function () {
    if (shown) return;
    // الشاشات الضيقة: لا تزاحم فقاعة «حمّل التطبيق»
    var ga = document.querySelector('.ga.in');
    if (ga && innerWidth <= 820) { setTimeout(show, 2500); return; }
    shown = true;
    document.body.appendChild(el);
    requestAnimationFrame(function () { requestAnimationFrame(function () { el.classList.add('in'); }); });
    removeEventListener('scroll', onScroll);
  };
  var onScroll = function () { if (scrollY > innerHeight * 1.1) show(); };
  addEventListener('scroll', onScroll, { passive: true });
  // الشاشات الضيقة: بعد تجاوز الواجهة فقط حتى لا تغطي أزرار المتاجر
  if (innerWidth > 820) setTimeout(show, 12000);
})();
