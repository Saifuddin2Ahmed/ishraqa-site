// إشراقة · الصفحة الاحتياطية لروابط المشاركة (/u/<اسم> و/c/<رمز>) على GitHub Pages.
// تعمل قبل نشر عامل Cloudflare (أو إن تعذّر): تقرأ المسار أو الاستعلام، وتجلب البطاقة العامة،
// وتبني الصفحة نفسها التي يبنيها العامل (share/render.js منسوخ من tool/web/share-worker في التطبيق).
// المعاينة في واتساب وأخواته هنا عامة (img/og.jpg)؛ المعاينة الشخصية يصنعها العامل على الخادم.
import {
  parsePath,
  canonicalPath,
  pickLang,
  isAndroid,
  fetchCard,
  renderProfile,
  renderClub,
  renderNotFound,
} from './render.js';

function show(html) {
  const d = new DOMParser().parseFromString(html, 'text/html');
  document.replaceChild(document.importNode(d.documentElement, true), document.documentElement);
}

async function main() {
  const r = parsePath(location.pathname, location.search);
  if (!r) return false;
  const langs = (navigator.languages || [navigator.language || '']).join(',');
  const lang = pickLang(r.lang, langs, '');
  const android = isAndroid(navigator.userAgent);
  if (!r.key) {
    show(renderNotFound({ lang, type: r.type }));
    return true;
  }
  const res = await fetchCard(r.type, r.key);
  if (res.status === 'error') return true; // تبقى الصفحة العامة بزر التحميل
  if (res.status === 'missing') {
    show(renderNotFound({ lang, type: r.type }));
    return true;
  }
  const key = r.type === 'u' ? res.card.username || r.key : r.key;
  const want = canonicalPath(r.type, key, r.lang);
  if (location.pathname.replace(/\/+$/, '') !== want) {
    try { history.replaceState(null, '', want); } catch (_) { /* لا بأس */ }
  }
  show(r.type === 'u' ? renderProfile(res.card, { lang, android }) : renderClub(res.card, { lang, android }));
  return true;
}

main().then((mine) => {
  // في 404.html: إن لم يكن المسار لنا تظهر صفحة «لم نجد» العامة كما هي
  document.documentElement.classList.add(mine ? 'share-ready' : 'share-none');
});
