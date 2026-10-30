// إشراقة · بطاقات المشاركة العامة: ishraqa.app/u/<اسم المستخدم> و ishraqa.app/c/<رمز النادي> و ishraqa.app/o/<معرّف الفرصة>
// وحدة صافية (بلا واجهات Worker أو Node) يستعملها العامل لبناء الصفحة على الخادم،
// وتُنسخ كما هي إلى الموقع (share/render.js) لتبني الصفحة الاحتياطية نفسها في المتصفح.
// كل نص من المستخدم يمر عبر esc() قبل دخوله HTML.

export const ORIGIN = 'https://ishraqa.app';
export const SB_URL = 'https://jytbowsfvuzdnsmhmsly.supabase.co';
// مفتاح «قابل للنشر» (publishable)، هو نفسه في التطبيق والموقع (lib/config/supabase_config.dart)
export const SB_KEY = 'sb_publishable_cm8SXt2NPRY5RY7dclZsLw_4ng3Q0TD';
export const PACKAGE = 'com.taeziz.ishraqa';
export const PLAY = `https://play.google.com/store/apps/details?id=${PACKAGE}`;
// المتاجر الثلاثة: الطريق الوحيد إلى التطبيق (لا نسخة ويب للمستخدمين)
export const APP_STORE = 'https://apps.apple.com/app/id6826877682';
export const MICROSOFT_STORE = 'https://apps.microsoft.com/detail/9nr3bxwzrdxs';
export const OG_DEFAULT = `${ORIGIN}/img/og.jpg`;
export const OG_DEFAULT_EN = `${ORIGIN}/img/og-en.jpg`;
export const ogDefault = (lang) => (lang === 'en' ? OG_DEFAULT_EN : OG_DEFAULT);
const STORAGE_PREFIX = `${SB_URL}/storage/v1/object/public/`;

const USER_RE = /^[a-z0-9_][a-z0-9_.]{1,18}[a-z0-9_]$/;
const CODE_RE = /^[a-z0-9]{4,16}$/;
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/;

/** يهرّب النص لـ HTML (محتوى وسمات معًا) */
export function esc(v) {
  return String(v ?? '').replace(/[&<>"'`=]/g, (c) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;', '`': '&#96;', '=': '&#61;',
  })[c]);
}

/** اسم مستخدم صالح بعد التطبيع، أو null (القواعد نفسها في lib/utils/username.dart) */
export function normUser(raw) {
  let s = String(raw ?? '');
  try { s = decodeURIComponent(s); } catch (_) { /* يبقى كما هو */ }
  s = s.trim().replace(/^@+/, '').toLowerCase();
  return USER_RE.test(s) && !s.includes('..') ? s : null;
}

/** رمز نادٍ صالح بعد التطبيع، أو null */
export function normCode(raw) {
  const s = String(raw ?? '').trim().toLowerCase();
  return CODE_RE.test(s) ? s : null;
}

/** معرّف فرصة (uuid) صالح بعد التطبيع، أو null */
export function normId(raw) {
  const s = String(raw ?? '').trim().toLowerCase();
  return UUID_RE.test(s) ? s : null;
}

const NORM = { u: normUser, c: normCode, o: normId };

/**
 * يقرأ المسار: /u/<اسم>، /c/<رمز>، /o/<معرّف>، و/en/… أو ?lang=en للإنجليزية، أو /u/?u=<اسم> و/c/?c=<رمز>.
 * يعيد {type, raw, key, lang} — key = null إن كان الشكل غير صالح (صفحة 404)،
 * أو null إن لم يكن المسار لنا (يمرّ إلى الموقع كما هو).
 */
export function parsePath(pathname, search = '') {
  const seg = String(pathname || '/').split('/').filter(Boolean);
  let lang = null;
  if (seg[0] === 'en') { lang = 'en'; seg.shift(); }
  const type = seg[0];
  if (!Object.hasOwn(NORM, type)) return null;
  if (seg.length > 2) return null;
  const q = new URLSearchParams(search || '');
  if (!lang && q.get('lang') === 'en') lang = 'en';
  const raw = seg[1] ?? q.get(type) ?? '';
  if (!raw) return null;
  const key = NORM[type](raw);
  return { type, raw, key, lang };
}

/** المسار المعتمد للبطاقة */
export function canonicalPath(type, key, lang) {
  return `${lang === 'en' ? '/en' : ''}/${type}/${encodeURIComponent(key)}`;
}

/** لغة الصفحة: /en/ صريحة، وروبوتات المعاينة عربية دائمًا، وإلا Accept-Language */
const BOT_RE = /facebookexternalhit|facebot|whatsapp|twitterbot|linkedinbot|telegrambot|slackbot|discordbot|googlebot|bingbot|applebot|skypeuripreview|pinterest|embedly|vkshare|redditbot|snapchat/i;
export function pickLang(explicit, acceptLanguage, userAgent) {
  if (explicit) return explicit;
  if (BOT_RE.test(userAgent || '')) return 'ar';
  const tags = String(acceptLanguage || '')
    .split(',')
    .map((t) => t.split(';')[0].trim().toLowerCase())
    .filter(Boolean);
  if (!tags.length || tags[0].startsWith('ar')) return 'ar';
  return tags.some((t) => t.startsWith('ar')) ? 'ar' : 'en';
}

export const isAndroid = (ua) => /android/i.test(ua || '');

/** نوع الجهاز من User-Agent: android | apple (آيفون وآيباد وماك) | windows | other */
export function platformOf(ua) {
  const s = ua || '';
  if (/android/i.test(s)) return 'android';
  if (/iPhone|iPad|iPod|Macintosh|Mac OS X/.test(s)) return 'apple';
  if (/Windows NT/.test(s)) return 'windows';
  return 'other';
}

/** روبوتات معاينة الروابط ومحركات البحث: تأخذ صفحة OG الكاملة */
export const isPreviewBot = (ua) => BOT_RE.test(ua || '');

const OPP_FIELDS = 'id,title,title_en,organization,type,deadline,deadline_expected,cover_url,fully_funded';

/** يجلب البطاقة من Supabase: {status:'ok', card} | {status:'missing'} | {status:'error'} */
export async function fetchCard(type, key, fetchImpl = fetch) {
  if (type === 'o') return fetchOpportunity(key, fetchImpl);
  const fn = type === 'u' ? 'public_profile_card' : 'public_club_card';
  const body = type === 'u' ? { p_username: key } : { p_key: key };
  try {
    const r = await fetchImpl(`${SB_URL}/rest/v1/rpc/${fn}`, {
      method: 'POST',
      headers: {
        apikey: SB_KEY,
        Authorization: `Bearer ${SB_KEY}`,
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(body),
    });
    if (!r.ok) return { status: 'error', code: r.status };
    const card = await r.json();
    if (card && typeof card === 'object' && !Array.isArray(card)) return { status: 'ok', card };
    return { status: 'missing' };
  } catch (_) {
    return { status: 'error' };
  }
}

/**
 * فرصة منشورة عبر REST بالمفتاح العام: سياسة RLS «read published opportunities» تسمح لـ anon
 * بقراءة الصفوف المنشورة وحدها (الترحيل 004)، فلا حاجة إلى دالة جديدة.
 */
export async function fetchOpportunity(id, fetchImpl = fetch) {
  const url = `${SB_URL}/rest/v1/opportunities?select=${OPP_FIELDS}&id=eq.${encodeURIComponent(id)}&status=eq.published&limit=1`;
  try {
    const r = await fetchImpl(url, {
      method: 'GET',
      headers: { apikey: SB_KEY, Authorization: `Bearer ${SB_KEY}`, Accept: 'application/json' },
    });
    if (!r.ok) return { status: 'error', code: r.status };
    const rows = await r.json();
    if (Array.isArray(rows) && rows[0] && typeof rows[0] === 'object') return { status: 'ok', card: rows[0] };
    return { status: 'missing' };
  } catch (_) {
    return { status: 'error' };
  }
}

// ───────────────────────── النصوص ─────────────────────────

const MONTHS = {
  ar: ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'],
  en: ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'],
};

/** تاريخ yyyy-mm-dd مقروء (بلا Intl، فالنتيجة واحدة في العامل وفي المتصفح) */
export function fmtDate(iso, lang) {
  const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(String(iso || ''));
  if (!m) return '';
  const mo = MONTHS[lang][+m[2] - 1];
  if (!mo) return '';
  return lang === 'ar' ? `${+m[3]} ${mo} ${m[1]}` : `${mo} ${+m[3]}, ${m[1]}`;
}

const OPP_TYPES = {
  ar: { scholarship: 'منحة دراسية', grant: 'تمويل ودعم', fellowship: 'زمالة', training: 'تدريب', job: 'وظيفة',
    competition: 'مسابقة', internship: 'تدريب عملي', conference: 'مؤتمر' },
  en: { scholarship: 'Scholarship', grant: 'Grant', fellowship: 'Fellowship', training: 'Training', job: 'Job',
    competition: 'Competition', internship: 'Internship', conference: 'Conference' },
};

const LEVELS = {
  ar: { fajr: 'فجر', shuruq: 'شروق', duha: 'ضحى', zuhr: 'ظهيرة', nur: 'نور' },
  en: { fajr: 'Fajr', shuruq: 'Shuruq', duha: 'Duha', zuhr: 'Noon', nur: 'Nur' },
};

function membersAr(n) {
  if (!n || n < 1) return '';
  if (n === 1) return 'عضو واحد';
  if (n === 2) return 'عضوان';
  const m = n % 100;
  return m >= 3 && m <= 10 ? `${n} أعضاء` : `${n} عضوًا`;
}

export const T = {
  ar: {
    app: 'إشراقة يومية',
    open: 'افتح في التطبيق',
    join: 'انضم من التطبيق',
    get: 'حمّل إشراقة',
    followers: 'متابِعون',
    following: 'يتابِع',
    level: 'المستوى',
    verified: 'حساب موثّق',
    other: 'English',
    members: membersAr,
    // أسماء الأنواع كما في التطبيق (ckKind* في lib/l10n)، و«نادٍ» لأي نوع غير معروف
    kind: (k, lvl) =>
      k === 'build' ? 'نادي مطوّرين' : k === 'language' ? `نادي لغة${lvl ? ` · ${lvl}` : ''}` : k === 'reading' ? 'نادي قراءة' : 'نادٍ',
    official: 'نادٍ رسمي',
    profileDesc: (name) => `تابِع ${name} على إشراقة يومية.`,
    clubDesc: (kind, name) => `${kind} على إشراقة يومية: «${name}». انضم إلينا.`,
    nfTitle: 'لم نجد هذه الصفحة',
    nfUser: 'ربما تغيّر اسم المستخدم، أو لم يعد الحساب متاحًا.',
    nfClub: 'ربما صار النادي خاصًا، أو تغيّر رابطه.',
    nfOpp: 'ربما أُزيلت هذه الفرصة، أو تغيّر رابطها.',
    oppType: (k) => OPP_TYPES.ar[k] || 'فرصة',
    deadline: (d) => `آخر موعد: ${d}`,
    deadlineExpected: (d) => `الموعد المتوقَّع: ${d}`,
    closed: 'انتهى موعد التقديم',
    fullyFunded: 'ممولة بالكامل',
    oppDesc: 'فرصة على إشراقة يومية',
    home: 'إلى الصفحة الرئيسية',
  },
  en: {
    app: 'Ishraqa Daily',
    open: 'Open in the app',
    join: 'Join in the app',
    get: 'Get Ishraqa',
    followers: 'Followers',
    following: 'Following',
    level: 'Level',
    verified: 'Verified account',
    other: 'العربية',
    members: (n) => (!n || n < 1 ? '' : n === 1 ? '1 member' : `${n} members`),
    kind: (k, lvl) =>
      k === 'build' ? 'Developer club' : k === 'language' ? `Language club${lvl ? ` · ${lvl}` : ''}` : k === 'reading' ? 'Reading club' : 'Club',
    official: 'Official club',
    profileDesc: (name) => `Follow ${name} on Ishraqa Daily.`,
    clubDesc: (kind, name) => `${kind} on Ishraqa Daily: “${name}”. Come join us.`,
    nfTitle: "We couldn't find this page",
    nfUser: 'The username may have changed, or the account is no longer available.',
    nfClub: 'The club may have become private, or its link changed.',
    nfOpp: 'This opportunity may have been removed, or its link changed.',
    oppType: (k) => OPP_TYPES.en[k] || 'Opportunity',
    deadline: (d) => `Deadline: ${d}`,
    deadlineExpected: (d) => `Expected deadline: ${d}`,
    closed: 'Applications closed',
    fullyFunded: 'Fully funded',
    oppDesc: 'An opportunity on Ishraqa Daily',
    home: 'Back to the home page',
  },
};

// ───────────────────────── القالب ─────────────────────────

/** رابط صورة آمن للمعاينة: تخزين Supabase العام وحده، وإلا null */
export function safeImage(u) {
  return typeof u === 'string' && u.startsWith(STORAGE_PREFIX) && !/[\s"'<>]/.test(u) ? u : null;
}

const clip = (s, n) => {
  const t = String(s ?? '').replace(/\s+/g, ' ').trim();
  return t.length > n ? `${t.slice(0, n - 1)}…` : t;
};

export const CSS = `:root{--night:#2A1B5E;--plum:#8E3A8C;--sun:#F07A4A;--gold:#FFB547;--ink:#2A1B5E;--muted:#5E5770;--card:#FFFFFF;--line:#EEE7F6;--chip:#F6F1FC}
@media (prefers-color-scheme:dark){:root{--ink:#F3EEFB;--muted:#B8B0C9;--card:#1E1830;--line:#2E2645;--chip:#2A2240}}
*{box-sizing:border-box}
html{background:var(--night)}
body{margin:0;min-height:100vh;font-family:Cairo,Tahoma,sans-serif;background:linear-gradient(160deg,var(--night) 0%,var(--plum) 60%,var(--sun) 100%);color:var(--ink);line-height:1.8;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px 16px;gap:18px}
a{color:inherit}
.card{position:relative;width:100%;max-width:460px;background:var(--card);border-radius:28px;padding:34px 24px 26px;text-align:center;box-shadow:0 30px 70px rgba(0,0,0,.35);animation:rise .7s cubic-bezier(.2,.7,.2,1) both}
.lang{position:absolute;top:14px;inset-inline-end:18px;font-size:13px;color:var(--muted);text-decoration:none}
.lang:hover{text-decoration:underline}
.avatar{width:112px;height:112px;border-radius:50%;margin:0 auto 14px;object-fit:cover;display:flex;align-items:center;justify-content:center;font-size:46px;font-weight:800;color:#fff;background:linear-gradient(140deg,var(--night),var(--plum),var(--sun));box-shadow:0 0 0 5px var(--card),0 0 0 8px rgba(240,122,74,.45),0 14px 30px rgba(42,27,94,.3);animation:glow 4s ease-in-out infinite alternate}
.cover{width:104px;height:104px;border-radius:28px;margin:0 auto 14px;object-fit:cover;display:flex;align-items:center;justify-content:center;font-size:44px;font-weight:800;color:#fff;background:linear-gradient(140deg,var(--night),var(--plum),var(--sun));box-shadow:0 12px 28px rgba(42,27,94,.28)}
h1{font-size:26px;line-height:1.45;margin:0 0 2px;font-weight:800;display:flex;align-items:center;justify-content:center;gap:6px;flex-wrap:wrap}
.tick{width:22px;height:22px;flex:none}
.handle{direction:ltr;unicode-bidi:isolate;color:var(--muted);margin:0 0 10px;font-size:15px}
.bio{margin:0 0 14px;white-space:pre-line;overflow-wrap:anywhere}
.chips{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 18px;padding:0;list-style:none}
.chips li{background:var(--chip);border-radius:999px;padding:3px 12px;font-size:13px;color:var(--muted)}
.stats{display:flex;justify-content:center;gap:34px;margin:0 0 22px}
.stats b{display:block;font-size:22px;font-weight:800;line-height:1.3}
.stats span{font-size:13px;color:var(--muted)}
.btn{display:block;text-decoration:none;font-weight:700;font-size:17px;border-radius:999px;padding:14px 20px;margin-top:10px;transition:transform .2s,box-shadow .2s}
.get{margin:18px 0 0;font-weight:700}
.btn:hover{transform:translateY(-2px);box-shadow:0 10px 24px rgba(42,27,94,.25)}
.primary{background:var(--night);color:#fff}
@media (prefers-color-scheme:dark){.primary{background:linear-gradient(120deg,var(--plum),var(--sun))}}
.secondary{border:1.5px solid var(--line);color:var(--ink)}
.web{display:inline-block;margin-top:14px;font-size:14px;color:var(--muted)}
.foot{color:#fff;opacity:.85;font-size:14px;text-decoration:none;font-weight:700;letter-spacing:.2px}
.foot:hover{opacity:1}
@keyframes rise{from{opacity:0;transform:translateY(18px) scale(.98)}to{opacity:1;transform:none}}
@keyframes glow{to{box-shadow:0 0 0 5px var(--card),0 0 0 9px rgba(255,181,71,.55),0 16px 34px rgba(142,58,140,.35)}}
@media (prefers-reduced-motion:reduce){.card,.avatar{animation:none}.btn{transition:none}}`;

const TICK =
  '<svg class="tick" viewBox="0 0 24 24" role="img" aria-label="%L"><path fill="#F07A4A" d="M12 1.5l2.6 1.9 3.2-.2 1 3.1 2.6 1.9-1 3.1 1 3.1-2.6 1.9-1 3.1-3.2-.2L12 22.5l-2.6-1.9-3.2.2-1-3.1-2.6-1.9 1-3.1-1-3.1 2.6-1.9 1-3.1 3.2.2z"/><path fill="#fff" d="M10.6 15.6l-3.2-3.2 1.4-1.4 1.8 1.8 4.6-4.6 1.4 1.4z"/></svg>';

/** رابط «افتح في التطبيق» لأندرويد: يفتح التطبيق إن كان مثبّتًا، وإلا Google Play */
export function intentLink(appPath, playRef) {
  return `intent://ishraqa.app${appPath}#Intent;scheme=https;package=${PACKAGE};S.browser_fallback_url=${encodeURIComponent(playRef)};end`;
}

function playWithRef(ref) {
  return `${PLAY}&referrer=${encodeURIComponent(ref)}`;
}

/** هيكل الصفحة الكامل (الرأس بمعاينات OG/Twitter، والجسم) */
export function page({ lang, title, desc, image, imageIsDefault, large = false, canonical, alternates, robots, body }) {
  const t = T[lang];
  const dir = lang === 'ar' ? 'rtl' : 'ltr';
  const img = image || ogDefault(lang);
  const card = large || imageIsDefault || !image ? 'summary_large_image' : 'summary';
  const alt = alternates
    ? `<link rel="alternate" hreflang="ar" href="${esc(alternates.ar)}">
<link rel="alternate" hreflang="en" href="${esc(alternates.en)}">
<link rel="alternate" hreflang="x-default" href="${esc(alternates.ar)}">`
    : '';
  return `<!doctype html>
<html lang="${lang}" dir="${dir}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<meta name="robots" content="${esc(robots)}">
<meta name="theme-color" content="#2A1B5E">
${canonical ? `<link rel="canonical" href="${esc(canonical)}">` : ''}
${alt}
<link rel="icon" type="image/png" href="${ORIGIN}/img/icon-192.png">
<meta property="og:type" content="${canonical && canonical.includes('/u/') ? 'profile' : 'website'}">
<meta property="og:site_name" content="${esc(t.app)}">
<meta property="og:locale" content="${lang === 'ar' ? 'ar_AR' : 'en_US'}">
<meta property="og:title" content="${esc(title)}">
<meta property="og:description" content="${esc(desc)}">
${canonical ? `<meta property="og:url" content="${esc(canonical)}">` : ''}
<meta property="og:image" content="${esc(img)}">
<meta property="og:image:alt" content="${esc(title)}">
${img === OG_DEFAULT || img === OG_DEFAULT_EN ? '<meta property="og:image:width" content="1200">\n<meta property="og:image:height" content="630">' : ''}
<meta name="twitter:card" content="${card}">
<meta name="twitter:title" content="${esc(title)}">
<meta name="twitter:description" content="${esc(desc)}">
<meta name="twitter:image" content="${esc(img)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>${CSS}</style>
</head>
<body>
${body}
<a class="foot" href="${ORIGIN}/">☀ ${esc(t.app)}</a>
</body>
</html>`;
}

/** أزرار التطبيق: كل جهاز إلى صفحة متجره الرسمية مباشرة؛ وغير المعروف يرى المتاجر الثلاثة */
function actions(t, { android, platform, appPath, playRef, join }) {
  const p = platform || (android ? 'android' : 'other');
  const playUrl = playWithRef(playRef);
  if (p === 'android') {
    return `<a class="btn primary" href="${esc(intentLink(appPath, playRef))}">${esc(join ? t.join : t.open)}</a>
<a class="btn secondary" href="${esc(playUrl)}">${esc(t.get)}</a>`;
  }
  if (p === 'apple') return `<a class="btn primary" href="${esc(APP_STORE)}">${esc(t.get)}</a>`;
  if (p === 'windows') return `<a class="btn primary" href="${esc(MICROSOFT_STORE)}">${esc(t.get)}</a>`;
  return `<p class="get">${esc(t.get)}</p>
<a class="btn secondary" href="${esc(playUrl)}">Google Play</a>
<a class="btn secondary" href="${esc(APP_STORE)}">App Store</a>
<a class="btn secondary" href="${esc(MICROSOFT_STORE)}">Microsoft Store</a>`;
}

function initial(name) {
  const c = [...String(name || '').trim()][0];
  return c ? esc(c) : '☀';
}

/** صفحة الملف الشخصي */
export function renderProfile(card, { lang = 'ar', android = false, platform } = {}) {
  const t = T[lang];
  const user = normUser(card.username) || '';
  const name = clip(card.display_name, 80) || `@${user}`;
  const bio = String(card.bio ?? '').trim().slice(0, 300);
  const img = safeImage(card.avatar_url);
  const place = [card.region, card.country].map((s) => clip(s, 40)).filter(Boolean);
  const placeTxt = [...new Set(place)].join(lang === 'ar' ? '، ' : ', ');
  const level = LEVELS[lang][card.level] || null;
  const num = (n) => Number.isFinite(+n) && +n >= 0 ? Math.floor(+n).toLocaleString(lang === 'ar' ? 'ar-EG-u-nu-latn' : 'en-US') : '0';
  const appPath = `/u/${user}`;
  const title = `${name} (@${user}) · ${t.app}`;
  const desc = bio ? clip(bio, 200) : t.profileDesc(name);
  const otherLang = lang === 'ar' ? 'en' : 'ar';
  const body = `<main class="card">
<a class="lang" href="${esc(canonicalPath('u', user, otherLang))}" hreflang="${otherLang}">${esc(t.other)}</a>
${img ? `<img class="avatar" src="${esc(img)}" alt="" width="112" height="112">` : `<div class="avatar" aria-hidden="true">${initial(name)}</div>`}
<h1><span>${esc(name)}</span>${card.verified ? TICK.replace('%L', esc(t.verified)) : ''}</h1>
<p class="handle">@${esc(user)}</p>
${bio ? `<p class="bio">${esc(bio)}</p>` : ''}
${level || placeTxt ? `<ul class="chips">${level ? `<li>☀ ${esc(t.level)}: ${esc(level)}</li>` : ''}${placeTxt ? `<li>📍 ${esc(placeTxt)}</li>` : ''}</ul>` : ''}
<div class="stats"><div><b>${num(card.followers)}</b><span>${esc(t.followers)}</span></div><div><b>${num(card.following)}</b><span>${esc(t.following)}</span></div></div>
${actions(t, { android, platform, appPath, playRef: 'utm_source=profile_share&utm_medium=web' })}
</main>`;
  return page({
    lang,
    title,
    desc,
    image: img,
    imageIsDefault: !img,
    canonical: ORIGIN + canonicalPath('u', user, lang),
    alternates: { ar: ORIGIN + canonicalPath('u', user, 'ar'), en: ORIGIN + canonicalPath('u', user, 'en') },
    robots: 'noindex, follow',
    body,
  });
}

/** صفحة النادي */
export function renderClub(card, { lang = 'ar', android = false, platform } = {}) {
  const t = T[lang];
  const code = normCode(card.code) || '';
  const name = clip(card.name, 80) || t.kind(card.kind);
  const kind = t.kind(card.kind, card.level ? clip(card.level, 8) : '');
  const about = String(card.description ?? '').trim().slice(0, 500);
  const img = safeImage(card.cover_url);
  const members = t.members(+card.member_count || 0);
  const appPath = `/c/${code}`;
  const title = `${name} · ${t.app}`;
  const desc = about ? clip(about, 200) : t.clubDesc(kind, name);
  const otherLang = lang === 'ar' ? 'en' : 'ar';
  const chips = [kind, card.official ? t.official : '', members].filter(Boolean);
  const body = `<main class="card">
<a class="lang" href="${esc(canonicalPath('c', code, otherLang))}" hreflang="${otherLang}">${esc(t.other)}</a>
${img ? `<img class="cover" src="${esc(img)}" alt="" width="104" height="104">` : `<div class="cover" aria-hidden="true">${initial(name)}</div>`}
<h1><span>${esc(name)}</span></h1>
<ul class="chips">${chips.map((c) => `<li>${esc(c)}</li>`).join('')}</ul>
${about ? `<p class="bio">${esc(about)}</p>` : ''}
${actions(t, { android, platform, appPath, playRef: `utm_source=club_share&utm_medium=web&club=${code}`, join: true })}
</main>`;
  return page({
    lang,
    title,
    desc,
    image: img,
    imageIsDefault: !img,
    canonical: ORIGIN + canonicalPath('c', code, lang),
    alternates: { ar: ORIGIN + canonicalPath('c', code, 'ar'), en: ORIGIN + canonicalPath('c', code, 'en') },
    robots: 'index, follow',
    body,
  });
}

/** نص الموعد: آخر موعد، أو المتوقَّع، أو «انتهى» إن مضى (today بصيغة yyyy-mm-dd للاختبار) */
export function deadlineText(card, lang, today = new Date().toISOString().slice(0, 10)) {
  const t = T[lang];
  const d = fmtDate(card.deadline, lang);
  if (!d) return '';
  if (String(card.deadline).slice(0, 10) < today) return t.closed;
  return card.deadline_expected ? t.deadlineExpected(d) : t.deadline(d);
}

/** صفحة الفرصة: العنوان بلغة الزائر (title_en للإنجليزية إن وُجد)، والجهة، والموعد، والغلاف */
export function renderOpportunity(card, { lang = 'ar', android = false, platform, today } = {}) {
  const t = T[lang];
  const id = normId(card.id) || '';
  const name = clip((lang === 'en' && card.title_en) || card.title, 120) || t.oppType(card.type);
  const org = clip(card.organization, 100);
  const when = deadlineText(card, lang, today);
  const img = safeImage(card.cover_url);
  const title = `${name} · ${t.app}`;
  const desc = clip([org, when, card.fully_funded ? t.fullyFunded : ''].filter(Boolean).join(' · '), 200) || t.oppDesc;
  const otherLang = lang === 'ar' ? 'en' : 'ar';
  const chips = [t.oppType(card.type), card.fully_funded ? t.fullyFunded : '', when].filter(Boolean);
  const body = `<main class="card">
<a class="lang" href="${esc(canonicalPath('o', id, otherLang))}" hreflang="${otherLang}">${esc(t.other)}</a>
${img ? `<img class="cover" src="${esc(img)}" alt="" width="104" height="104">` : '<div class="cover" aria-hidden="true">☀</div>'}
<h1><span>${esc(name)}</span></h1>
${org ? `<p class="handle" dir="auto">${esc(org)}</p>` : ''}
<ul class="chips">${chips.map((c) => `<li>${esc(c)}</li>`).join('')}</ul>
${actions(t, { android, platform, appPath: `/o/${id}`, playRef: 'utm_source=opportunity_share&utm_medium=web' })}
</main>`;
  return page({
    lang,
    title,
    desc,
    image: img,
    imageIsDefault: !img,
    large: true,
    canonical: ORIGIN + canonicalPath('o', id, lang),
    alternates: { ar: ORIGIN + canonicalPath('o', id, 'ar'), en: ORIGIN + canonicalPath('o', id, 'en') },
    robots: 'noindex, follow',
    body,
  });
}

/** صفحة «لم نجد» للملف أو النادي أو الفرصة */
export function renderNotFound({ lang = 'ar', type = 'u', platform = 'other' } = {}) {
  const t = T[lang];
  const body = `<main class="card">
<div class="cover" aria-hidden="true">☀</div>
<h1>${esc(t.nfTitle)}</h1>
<p class="bio">${esc(type === 'c' ? t.nfClub : type === 'o' ? t.nfOpp : t.nfUser)}</p>
<a class="btn secondary" href="${ORIGIN}/">${esc(t.home)}</a>
${actions(t, { platform, appPath: '/', playRef: 'utm_source=share_404&utm_medium=web' })}
</main>`;
  return page({
    lang,
    title: `${t.nfTitle} · ${t.app}`,
    desc: t.nfTitle,
    image: null,
    imageIsDefault: true,
    canonical: null,
    alternates: null,
    robots: 'noindex',
    body,
  });
}
