"""يولّد صفحة ويب لكل مقال منشور في إشراقة (ishraqa.app/a/<slug>/)
مع معاينة المشاركة (صورة الغلاف) وزر فتح التطبيق داخل المقال، وصفحة فهرس /a/.

يقرأ المقالات المنشورة فقط عبر المفتاح العام (القابل للنشر)؛ الحماية في سياسات RLS.
يعمل يوميًا عبر GitHub Actions، ويمكن تشغيله يدويًا:
    pip install markdown
    python tools/build_articles.py
"""
import datetime as dt
import html
import json
import shutil
import sys
import urllib.request
from pathlib import Path

import markdown

sys.path.insert(0, str(Path(__file__).resolve().parent))
import seo  # noqa: E402
import site_footer  # noqa: E402
import site_nav  # noqa: E402

SUPABASE_URL = 'https://jytbowsfvuzdnsmhmsly.supabase.co'
PUBLISHABLE_KEY = 'sb_publishable_cm8SXt2NPRY5RY7dclZsLw_4ng3Q0TD'
SITE = 'https://ishraqa.app'

# المؤسس: كيان واحد (https://saifuddin.dev/#person) بكل صيغ اسمه وحساباته، من seo.py (بيانات منظّمة فقط، لا نص ظاهر)
FOUNDER = seo.founder(full=True)
PLAY = 'https://play.google.com/store/apps/details?id=com.taeziz.ishraqa'
MS_STORE = 'https://apps.microsoft.com/detail/9NR3BXWZRDXS?mode=direct'
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'a'

CATEGORIES = {}
# لون لكل تصنيف (الشارة والنقطة في البطاقات)
CAT_COLORS = {
    'reading': '#8E3A8C', 'health': '#2E9D6B', 'tech': '#2C6ED5', 'ai': '#5B4BD6',
    'money': '#C98A12', 'self': '#E0672F', 'culture': '#C2416B', 'family': '#1E9AA0',
    'science': '#2B8FD0',
}


def fetch(path: str) -> list:
    req = urllib.request.Request(
        f'{SUPABASE_URL}/rest/v1/{path}',
        headers={'apikey': PUBLISHABLE_KEY, 'Accept': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)


RESIZE = True   # أوقفه إن تجاوز تحويل الصور حصة الخطة في Supabase
_OBJ = f'{SUPABASE_URL}/storage/v1/object/public/'


def sized(url: str, width: int) -> str:
    """نسخة أخف من غلاف المقال بعرض محدد (يرسلها Supabase بصيغة WebP للمتصفحات التي تدعمها)"""
    if not RESIZE or not (url or '').startswith(_OBJ):
        return url
    return url.replace('/storage/v1/object/public/', '/storage/v1/render/image/public/', 1) + f'?width={width}&quality=72'


def srcset(url: str, widths=(640, 1024, 1600)) -> str:
    if not RESIZE or not (url or '').startswith(_OBJ):
        return ''
    return ', '.join(f'{esc(sized(url, w))} {w}w' for w in widths)


def esc(s) -> str:
    return html.escape(s or '', quote=True)


AR_HEAD = dict(lang='ar', dir='rtl', site_name='إشراقة يومية', locale='ar_AR')
EN_HEAD = dict(lang='en', dir='ltr', site_name='Ishraqa Daily', locale='en_US')
CAT_EN = {'health': 'Health', 'tech': 'Technology', 'self': 'Self-growth', 'money': 'Money & work',
          'science': 'Science', 'family': 'Family', 'culture': 'Culture & literature', 'ai': 'AI', 'reading': 'Reading'}

HEAD = """<!doctype html>
<html lang="{lang}" dir="{dir}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#2A1B5E">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/img/icon-192.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="{site_name}">
<meta property="og:locale" content="{locale}">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="preconnect" href="https://jytbowsfvuzdnsmhmsly.supabase.co">
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Amiri:ital@0;1&display=swap" rel="stylesheet">
<style>{css}</style>{nav_css}</head><body>
{nav}
"""

CSS = """
:root{--night:#2A1B5E;--plum:#8E3A8C;--sun:#F07A4A;--gold:#FFB547;--cream:#FFFBF8;--ink:#2A1B5E;--muted:#5E5770;--card:#fff;--line:#EEE7F6;--soft:#F6F1FB}
@media (prefers-color-scheme:dark){:root{--cream:#13101D;--ink:#F3EEFB;--muted:#B8B0C9;--card:#1C1729;--line:#2C2442;--soft:#221C33}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Cairo,Tahoma,sans-serif;background:var(--cream);color:var(--ink);line-height:1.9;-webkit-font-smoothing:antialiased}
a{color:inherit}img{max-width:100%}
.wrap{max-width:780px;margin:0 auto;padding:0 20px}.wrap.wide{max-width:1180px}
.btn{white-space:nowrap}
.btn{display:inline-flex;align-items:center;gap:8px;font-weight:700;text-decoration:none;border-radius:999px;padding:9px 18px;transition:transform .2s,box-shadow .2s}
.btn:hover{transform:translateY(-2px)}
.btn.light{background:rgba(255,255,255,.18);color:#fff;font-size:14px;opacity:1!important;border:1px solid rgba(255,255,255,.25)}
.btn.main{background:#fff;color:var(--night);font-size:16px;padding:13px 28px;box-shadow:0 10px 30px rgba(0,0,0,.25)}
.progress{position:fixed;top:0;inset-inline:0;height:4px;z-index:30;background:linear-gradient(90deg,var(--gold),var(--sun),var(--plum));transform-origin:right;transform:scaleX(0)}
.pill{align-self:flex-start;width:fit-content;display:inline-flex;align-items:center;gap:7px;padding:4px 13px;border-radius:999px;font-weight:700;font-size:13px;background:color-mix(in srgb,var(--c) 14%,transparent);color:var(--c);text-decoration:none}
.pill:before{content:'';width:7px;height:7px;border-radius:50%;background:var(--c)}
@media (prefers-color-scheme:dark){.pill{color:color-mix(in srgb,var(--c) 55%,#fff)}}
/* ── صفحة المقال ── */
.hero-a{max-width:1180px;margin:22px auto 0;padding:0 20px}
.hero-a figure{margin:0;position:relative;border-radius:28px;overflow:hidden;box-shadow:0 24px 60px rgba(42,27,94,.22)}
.hero-a img{display:block;width:100%;aspect-ratio:16/8;object-fit:cover}
@media (max-width:640px){.hero-a{padding:0}.hero-a figure{border-radius:0 0 24px 24px}.hero-a img{aspect-ratio:16/10}}
.head-a{margin-top:26px}
h1{font-size:clamp(28px,4.4vw,42px);line-height:1.4;margin:14px 0 10px;font-weight:800;letter-spacing:-.2px}
.lead{font-size:20px;line-height:1.85;color:var(--muted);margin:0 0 20px}
.byline{display:flex;align-items:center;gap:12px;padding:14px 0;border-block:1px solid var(--line);margin-bottom:26px}
.avatar{width:46px;height:46px;border-radius:50%;display:grid;place-items:center;color:#fff;font-weight:800;font-size:19px;background:linear-gradient(140deg,var(--night),var(--plum),var(--sun));flex-shrink:0}
.byline b{display:block;line-height:1.4}.byline small{color:var(--muted);font-size:13.5px}
article{font-size:19px}
article p,article li{line-height:2}
article h2{font-size:25px;margin:38px 0 10px;line-height:1.5;position:relative;padding-inline-start:16px}
article h2:before{content:'';position:absolute;inset-inline-start:0;top:.35em;bottom:.35em;width:5px;border-radius:5px;background:linear-gradient(var(--gold),var(--sun),var(--plum))}
article h3{font-size:20px}
article strong{color:var(--plum)}@media (prefers-color-scheme:dark){article strong{color:#E9B6E6}}
article blockquote{margin:26px 0;padding:22px 26px 22px 22px;border-radius:20px;background:var(--soft);position:relative;font-family:Amiri,serif;font-size:22px;line-height:1.9}
article blockquote:before{content:'“';position:absolute;top:-18px;inset-inline-start:14px;font-size:72px;line-height:1;color:var(--sun);font-family:Georgia,serif}
article blockquote p{margin:0}
article img{display:block;width:100%;border-radius:20px;margin:22px 0;box-shadow:0 14px 36px rgba(0,0,0,.14)}
article ul li::marker,article ol li::marker{color:var(--sun);font-weight:800}
.fade{position:relative}.fade:after{content:'';position:absolute;left:0;right:0;bottom:0;height:150px;background:linear-gradient(transparent,var(--cream))}
.cta{position:relative;overflow:hidden;margin:20px 0 34px;padding:34px 26px;border-radius:28px;background:linear-gradient(135deg,var(--night),var(--plum) 60%,var(--sun));color:#fff;text-align:center}
.cta:before{content:'';position:absolute;inset:auto -60px -120px auto;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(255,181,71,.55),transparent 70%)}
.cta h3{margin:0 0 6px;font-size:23px;position:relative}.cta p{margin:0 0 20px;opacity:.92;position:relative}
.cta .btn{position:relative}.cta small{display:block;margin-top:14px;opacity:.8;font-size:13px;position:relative}
.rights{font-size:13px;line-height:1.8;opacity:.62;margin:-22px 0 32px}
.share{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin:8px 0 34px}
.share span{font-weight:700;color:var(--muted);margin-inline-end:4px}
.share a,.share button{width:42px;height:42px;border-radius:50%;display:grid;place-items:center;border:1px solid var(--line);background:var(--card);color:var(--ink);cursor:pointer;transition:transform .2s,background .2s;font:inherit}
.share a:hover,.share button:hover{transform:translateY(-2px);background:var(--soft)}.share svg{width:19px;height:19px}
.share .ok{font-size:13px;color:var(--plum);font-weight:700;opacity:0;transition:opacity .2s}.share .ok.on{opacity:1}
h2.sec{font-size:24px;margin:10px 0 18px}
/* ── البطاقات والفهرس ── */
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
@media (max-width:980px){.grid{grid-template-columns:repeat(2,1fr)}}@media (max-width:620px){.grid{grid-template-columns:1fr}}
.card{display:flex;flex-direction:column;text-decoration:none;border-radius:22px;overflow:hidden;background:var(--card);border:1px solid var(--line);transition:transform .25s,box-shadow .25s}
.card:hover{transform:translateY(-5px);box-shadow:0 20px 44px rgba(42,27,94,.16)}
.card .ph{overflow:hidden;aspect-ratio:16/10;background:var(--soft)}.card img{width:100%;height:100%;object-fit:cover;transition:transform .6s}
.card:hover img{transform:scale(1.06)}
.card .in{padding:16px 18px 18px;display:flex;flex-direction:column;gap:8px;flex:1}
.card b{font-size:18px;line-height:1.55}.card p{margin:0;color:var(--muted);font-size:14.5px;line-height:1.75;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.card small{color:var(--muted);font-size:13px;margin-top:auto}
.hero-i{position:relative;overflow:hidden;background:linear-gradient(130deg,var(--night),var(--plum) 58%,var(--sun));color:#fff;padding:54px 0 64px}
.hero-i:after{z-index:1;content:'';position:absolute;inset:auto -10% -55% auto;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(255,181,71,.45),transparent 65%)}
.hero-i .wrap{position:relative;z-index:2}
.hero-i{padding:96px 0 104px}.hero-v{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0}.hero-i:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(90deg,rgba(22,9,40,.45),rgba(22,9,40,.78) 55%,rgba(22,9,40,.9)),linear-gradient(0deg,rgba(22,9,40,.75),transparent 60%)}@media (max-width:760px){.hero-i{padding:64px 0 72px}.hero-i:before{background:linear-gradient(0deg,rgba(22,9,40,.9),rgba(22,9,40,.68))}}@media (prefers-reduced-motion:reduce){.hero-v{display:none}.hero-i{background:url(/media/articles/hero.jpg) center/cover}}
.hero-i h1{margin:0 0 8px}.hero-i p{margin:0;font-size:19px;opacity:.92;max-width:640px}
.stats{display:flex;gap:26px;margin-top:22px;flex-wrap:wrap}.stats div{font-size:14px;opacity:.85}.stats b{display:block;font-size:28px;line-height:1.2;opacity:1}
.search{margin-top:26px;max-width:560px;position:relative}
.search input{width:100%;padding:15px 52px 15px 18px;border-radius:999px;border:0;font:inherit;font-size:16px;color:var(--night);background:#fff;box-shadow:0 14px 34px rgba(0,0,0,.2);outline:none}
.search svg{position:absolute;top:50%;inset-inline-start:18px;transform:translateY(-50%);width:20px;height:20px;color:var(--plum)}
.chips{display:flex;gap:10px;flex-wrap:wrap;margin:-26px 0 30px;position:relative;z-index:2}
@media (max-width:640px){.chips{flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;margin-inline:-20px;padding:4px 20px 8px}.chips::-webkit-scrollbar{display:none}.chip{flex-shrink:0}}
.chip{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:8px 16px;font:inherit;font-weight:700;font-size:14px;cursor:pointer;box-shadow:0 6px 18px rgba(42,27,94,.08);transition:all .2s}
.chip[aria-pressed=true]{background:var(--night);color:#fff;border-color:var(--night)}
@media (prefers-color-scheme:dark){.chip[aria-pressed=true]{background:#fff;color:var(--night)}}
.feat{display:grid;grid-template-columns:1.25fr 1fr;border-radius:28px;overflow:hidden;background:var(--card);border:1px solid var(--line);text-decoration:none;margin-bottom:34px;box-shadow:0 20px 50px rgba(42,27,94,.12);transition:transform .25s}
.feat:hover{transform:translateY(-4px)}
.feat .ph{overflow:hidden;min-height:320px}.feat img{width:100%;height:100%;object-fit:cover;transition:transform .7s}.feat:hover img{transform:scale(1.05)}
.feat .in{padding:32px;display:flex;flex-direction:column;gap:12px;justify-content:center}
.feat .tag{font-weight:800;color:#B5481F;font-size:14px;letter-spacing:.3px}
.feat b{font-size:clamp(24px,2.8vw,32px);line-height:1.45}.feat p{margin:0;color:var(--muted);font-size:16.5px;line-height:1.85}
.feat small{color:var(--muted)}
@media (max-width:820px){.feat{grid-template-columns:1fr}.feat .ph{min-height:0;aspect-ratio:16/9}.feat .in{padding:22px}}
.empty{display:none;text-align:center;color:var(--muted);padding:40px 0}
main{padding-bottom:20px}
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}.rv.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.card,.card img,.feat,.feat img,.btn{transition:none}html{scroll-behavior:auto}}
"""

# يظهر العنصر بهدوء عند الوصول إليه، وزر «افتح في التطبيق» يناسب جهاز القارئ
JS = """<script>
(function(){
var ua=navigator.userAgent,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
var apple=/iPhone|iPad|iPod|Macintosh/.test(ua),android=/Android/.test(ua),win=/Windows NT/.test(ua);
document.querySelectorAll('a[data-open]').forEach(function(a){
  if(android)return;
  if(win){a.href='__MS__';a.target='_blank';a.rel='noopener';}
  else if(apple){a.href='https://apps.apple.com/app/id6826877682';}
  else{a.href='__PLAY__';}
});
var els=document.querySelectorAll('.rv');
if(rm||!('IntersectionObserver' in window)){els.forEach(function(e){e.classList.add('on')});}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target)}})},{rootMargin:'0px 0px -8% 0px'});els.forEach(function(e){io.observe(e)});}
var bar=document.querySelector('.progress'),art=document.querySelector('article');
if(bar&&art){var f=function(){var r=art.getBoundingClientRect(),h=r.height-innerHeight*.4,p=Math.min(1,Math.max(0,-r.top/(h>0?h:1)));bar.style.transform='scaleX('+p+')'};addEventListener('scroll',f,{passive:true});f();}
var cp=document.querySelector('[data-copy]');
if(cp)cp.addEventListener('click',function(){var u=location.href.split('?')[0];
  if(navigator.share&&/Android|iPhone|iPad/.test(ua)){navigator.share({title:document.title,url:u}).catch(function(){});return;}
  (navigator.clipboard?navigator.clipboard.writeText(u):Promise.reject()).then(function(){var o=document.querySelector('.share .ok');o.classList.add('on');setTimeout(function(){o.classList.remove('on')},1800)}).catch(function(){prompt('انسخ الرابط',u)});});
var q=document.querySelector('.search input'),chips=document.querySelectorAll('.chip'),cards=document.querySelectorAll('[data-cat]'),empty=document.querySelector('.empty'),cat='';
function apply(){var t=(q&&q.value||'').trim(),n=0;cards.forEach(function(c){var ok=(!cat||c.dataset.cat===cat)&&(!t||c.dataset.q.indexOf(t)>-1);c.style.display=ok?'':'none';if(ok){n++;c.classList.add('on')}});if(empty)empty.style.display=n?'none':'block';}
if(q)q.addEventListener('input',apply);
chips.forEach(function(ch){ch.addEventListener('click',function(){cat=ch.dataset.c;chips.forEach(function(x){x.setAttribute('aria-pressed',x===ch)});apply();});});
})();
</script>"""

# التذييل الموحّد من site_footer.py
FOOT = """{foot}
{js}</body></html>"""

ICONS = {
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.6-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>',
    'x': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.2 2.3h3.4l-7.4 8.4 8.7 11h-6.8l-5.3-6.9-6.1 6.9H1.3l7.9-9L.9 2.3h7l4.8 6.3zm-1.2 17.4h1.9L7 4.2H5z"/></svg>',
    'fb': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21.9v-7.4H16l.4-2.9h-2.9V9.8c0-.8.2-1.4 1.4-1.4h1.6V5.8a21 21 0 0 0-2.3-.1c-2.3 0-3.8 1.4-3.8 3.9v2H8v2.9h2.4v7.4a10 10 0 1 1 3.1 0z"/></svg>',
    'tg': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 4.3 18.7 19.5c-.2 1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.2 13.2l-4.8-1.5c-1-.3-1-1 .2-1.5L20.5 3c.9-.3 1.6.2 1.4 1.3z"/></svg>',
    'link': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
}
SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'


def js() -> str:
    return JS.replace('__MS__', MS_STORE).replace('__PLAY__', PLAY)


def open_app(path: str, ref: str) -> str:
    """على أندرويد يفتح التطبيق على الصفحة نفسها إن كان مثبتًا، وإلا Google Play (والأجهزة الأخرى يضبطها JS)"""
    from urllib.parse import quote
    play = f'{PLAY}&referrer=' + quote(f'utm_source=web&utm_medium={ref}')
    return (f'intent://ishraqa.app{path}#Intent;scheme=https;package=com.taeziz.ishraqa;'
            f'S.browser_fallback_url={quote(play, safe="")};end')


def teaser(body: str, words: int = 120) -> str:
    """أول فقرات المقال حتى نحو 120 كلمة: لمحة تشجّع على إكماله في التطبيق"""
    out, n = [], 0
    for block in body.split(chr(10) * 2):
        if not block.strip():
            continue
        out.append(block)
        n += len(block.split())
        if n >= words:
            break
    return (chr(10) * 2).join(out)


def is_team(name: str) -> bool:
    return 'فريق' in (name or '') or 'إشراقة' in (name or '')


def author_of(a: dict) -> str:
    # الاسم المكتوب على المقال أولًا («فريق إشراقة» أو اسم الكاتب كما يريده)، ثم اسم الملف
    return a.get('author_name') or (a.get('author') or {}).get('display_name') or 'فريق إشراقة'


def author_en(a: dict) -> str:
    """اسم الكاتب في الصفحات الإنجليزية: الفريق والمؤسس بالإنجليزية، وغيرهما كما كتبه صاحبه"""
    name = author_of(a)
    if is_team(name):
        return 'Ishraqa Team'
    if 'سيف الدين' in name:
        return 'Eng. Saifuddin Ahmed'
    return name


def pill(cat_slug: str, en: bool = False) -> str:
    name = (CAT_EN if en else CATEGORIES).get(cat_slug, '')
    if not name:
        return ''
    return f'<span class="pill" style="--c:{CAT_COLORS.get(cat_slug, "#8E3A8C")}">{esc(name)}</span>'


def minutes(a: dict, en: bool = False) -> str:
    m = a.get('reading_minutes')
    return (f'{m} min read' if en else f'{m} دقائق قراءة') if m else ''


def has_en(a: dict) -> bool:
    """للمقال نسخة إنجليزية كتبها كاتبه (title_tr/body_tr)"""
    return bool((a.get('title_tr') or '').strip() and (a.get('body_tr') or '').strip())


def view(a: dict, en: bool) -> dict:
    """حقول المقال باللغة المطلوبة إن وُجدت، وإلا العربية"""
    if en and has_en(a):
        return {'title': a['title_tr'], 'excerpt': a.get('excerpt_tr') or '', 'body': a['body_tr'],
                'href': f'/en/a/{a["slug"]}/', 'rtl': False}
    return {'title': a['title'], 'excerpt': a.get('excerpt') or '', 'body': a['body'],
            'href': f'/a/{a["slug"]}/', 'rtl': en}


def card(a: dict, en: bool = False) -> str:
    v = view(a, en)
    q = ' '.join([a['title'], v['title'], v['excerpt'], CATEGORIES.get(a['category'], ''), CAT_EN.get(a['category'], '')])
    # في الصفحة الإنجليزية: المقال الذي لا نسخة إنجليزية له يظهر بلغته واتجاهها، وبقية البطاقة إنجليزية
    ar = ' lang="ar" dir="rtl"' if v['rtl'] else ''
    who = f'<bdi>{esc(author_en(a))}</bdi>' if en else esc(author_of(a))
    meta = ' · '.join(x for x in [who, esc(minutes(a, en)), esc(a.get('publish_date') or '')] if x)
    return (f'<a class="card rv" href="{v["href"]}" data-cat="{esc(a["category"])}" data-q="{esc(q)}">'
            f'<div class="ph"><img src="{esc(sized(a.get("cover_url") or "/img/og.jpg", 640))}" alt="{esc(v["title"])}" width="640" height="400" loading="lazy" decoding="async"></div>'
            f'<div class="in">{pill(a["category"], en)}<b{ar}>{esc(v["title"])}</b>'
            f'<p{ar}>{esc(v["excerpt"])}</p><small>{meta}</small></div></a>')


def share_row(url: str, title: str, en: bool = False) -> str:
    from urllib.parse import quote
    u, t = quote(url, safe=''), quote(title, safe='')
    links = [
        ('wa', 'WhatsApp' if en else 'واتساب', f'https://wa.me/?text={t}%20{u}'),
        ('x', 'X', f'https://twitter.com/intent/tweet?text={t}&url={u}'),
        ('fb', 'Facebook' if en else 'فيسبوك', f'https://www.facebook.com/sharer/sharer.php?u={u}'),
        ('tg', 'Telegram' if en else 'تيليجرام', f'https://t.me/share/url?url={u}&text={t}'),
    ]
    via = 'Share on {}' if en else 'مشاركة عبر {}'
    out = ''.join(f'<a href="{h}" target="_blank" rel="noopener" aria-label="{via.format(n)}" title="{n}">{ICONS[k]}</a>'
                  for k, n, h in links)
    if en:
        return (f'<div class="share"><span>Share the article</span>{out}'
                f'<button type="button" data-copy aria-label="Copy link" title="Copy link">{ICONS["link"]}</button>'
                '<span class="ok">Link copied ✓</span></div>'
                '<p class="rights">All rights reserved to Ishraqa Daily and the article’s author. You are welcome to quote it with credit and a link.</p>')
    return (f'<div class="share"><span>شارك المقال</span>{out}'
            f'<button type="button" data-copy aria-label="نسخ الرابط" title="نسخ الرابط">{ICONS["link"]}</button>'
            '<span class="ok">نُسخ الرابط ✓</span></div>'
            '<p class="rights">جميع الحقوق محفوظة لإشراقة يومية وكاتب المقال. يسرّنا الاقتباس مع ذكر المصدر ورابطه.</p>')


def article_page(a: dict, related: list, en: bool = False) -> str:
    """صفحة المقال. en=True لنسخته الإنجليزية (/en/a/<slug>/) ولا تُبنى إلا إن كان له نسخة إنجليزية"""
    slug = a['slug']
    v = view(a, en)
    path = v['href']
    url = f'{SITE}{path}'
    alts = {'ar': f'{SITE}/a/{slug}/', 'en': f'{SITE}/en/a/{slug}/'} if has_en(a) else None
    author = author_of(a)
    cover = a.get('cover_url') or f'{SITE}/img/og.jpg'
    body_html = markdown.markdown(teaser(v['body']), extensions=['extra', 'sane_lists'])
    app = open_app(f'/a/{slug}/', 'article')
    cat = (CAT_EN if en else CATEGORIES).get(a['category'], '')
    date = a.get('publish_date') or ''
    modified = (a.get('updated_at') or '')[:10] or date
    if modified < date:
        modified = date
    title = seo.fit_title(v['title'])
    desc = seo.clip(v['excerpt'] or v['title'], 155)
    who = ({'@type': 'Organization', 'name': author, 'url': f'{SITE}/about/'} if is_team(author)
           else FOUNDER if 'سيف الدين' in author
           else {'@type': 'Person', 'name': author})
    if en:
        home, crumb = ('Ishraqa Daily', f'{SITE}/en/'), ('Articles', f'{SITE}/en/a/')
    else:
        home, crumb = ('إشراقة يومية', f'{SITE}/'), ('المقالات', f'{SITE}/a/')
    nodes = [
        {'@type': 'Article', '@id': url + '#article', 'headline': seo.clip(v['title'], 110), 'description': desc,
         'image': [cover], 'datePublished': date, 'dateModified': modified, 'author': who,
         'publisher': {'@id': seo.ORG_ID}, 'mainEntityOfPage': {'@id': url + '#webpage'},
         'isPartOf': {'@id': seo.WEBSITE_ID}, 'articleSection': cat or None, 'inLanguage': 'en' if en else 'ar',
         'timeRequired': f'PT{a["reading_minutes"]}M' if a.get('reading_minutes') else None,
         'isAccessibleForFree': True},
        seo.webpage(url, v['title'], desc),
        seo.breadcrumb(url, [home, crumb, (v['title'], url)]),
        seo.org(), seo.website(),
    ]
    nodes[0] = {k: x for k, x in nodes[0].items() if x is not None}
    initial = (author.replace('م.', '').replace('د.', '').strip() or 'إ')[0]
    avatar = ('<img class="avatar" src="/img/icon-192.png" alt="" width="46" height="46">' if is_team(author)
              else f'<div class="avatar" aria-hidden="true">{esc(initial)}</div>')
    meta = ' · '.join(x for x in [minutes(a, en), f'<time datetime="{esc(date)}">{esc(date)}</time>' if date else ''] if x)
    more = ''.join(card(r, en) for r in related)
    if en:
        T = dict(cta='Keep reading in Ishraqa Daily',
                 sub='The full article with its practical takeaway, plus a library and reading clubs.',
                 btn='Read the full article in the app', small='No ads · Android, Windows, iPhone and Mac',
                 more='Read next', author=f'<bdi>{esc(author_en(a))}</bdi>')
    else:
        T = dict(cta='أكمل القراءة في إشراقة يومية',
                 sub='المقال كاملًا مع خلاصته العملية، ومقال جديد كل يوم، ومكتبة ونوادٍ للقراءة.',
                 btn='اقرأه كاملًا في التطبيق', small='بلا إعلانات · أندرويد وويندوز وآيفون وماك',
                 more='اقرأ أيضًا', author=esc(author))
    page = (
        HEAD.format(**(EN_HEAD if en else AR_HEAD), title=esc(title), desc=esc(desc), url=url, og_type='article',
                    og_title=esc(v['title']), image=esc(cover), css=CSS, nav_css=site_nav.NAV_CSS, nav=site_nav.header(path))
        + '<div class="progress" aria-hidden="true"></div>'
        + (f'<div class="hero-a"><figure><img src="{esc(sized(cover, 1024))}"'
           + (f' srcset="{srcset(cover)}" sizes="(max-width: 1180px) 100vw, 1140px"' if srcset(cover) else '')
           + f' alt="{esc(v["title"])}" width="1600" height="800" fetchpriority="high"></figure></div>')
        + '<div class="wrap"><main><div class="head-a">'
        + pill(a['category'], en)
        + f'<h1>{esc(v["title"])}</h1>'
        + (f'<p class="lead">{esc(v["excerpt"])}</p>' if v['excerpt'] else '')
        + f'<div class="byline">{avatar}'
        + f'<div><b>{T["author"]}</b><small>{meta}</small></div></div></div>'
        + f'<article class="fade">{body_html}</article>'
        + f'<div class="cta rv"><h3>{T["cta"]}</h3>'
        + f'<p>{T["sub"]}</p>'
        + f'<a class="btn main" data-open href="{app}">{T["btn"]}</a>'
        + f'<small>{T["small"]}</small></div>'
        + share_row(url, v['title'], en)
        + '</main></div>'
        + (f'<div class="wrap wide"><h2 class="sec">{T["more"]}</h2><div class="grid">{more}</div></div>' if more else '')
        + FOOT.format(foot=site_footer.footer(path), js=js())
    )
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes, image=cover, image_alt=v['title'],
                        lang='en' if en else 'ar', alternates=alts,
                        og_type='article', article={'published': date, 'modified': modified, 'section': cat})


def related_to(a: dict, items: list, n: int = 3) -> list:
    """مقالات من التصنيف نفسه أولًا، ثم الأحدث"""
    others = [r for r in items if r['slug'] != a['slug']]
    same = [r for r in others if r['category'] == a['category']]
    return (same + [r for r in others if r not in same])[:n]


def index_page(items: list, en: bool = False) -> str:
    """صفحة المقالات. en=True: واجهة إنجليزية (/en/a/) والمقالات نفسها بلغة كاتبها"""
    path = '/en/a/' if en else '/a/'
    url = f'{SITE}{path}'
    alts = {'ar': f'{SITE}/a/', 'en': f'{SITE}/en/a/'}
    if en:
        T = dict(title='Ishraqa Articles: health, technology, self-growth and culture',
                 desc='Short, sourced articles on health, technology, self-growth, money and culture, each with a practical takeaway.',
                 home='Ishraqa Daily', crumb='Articles', h1='Ishraqa Articles', all='All', feat='☀ Article of the day',
                 search='Search articles…', cats='Categories', empty='No matching articles. Try another word.',
                 note='Each article appears in the language its author wrote it in.')
    else:
        T = dict(title='مقالات إشراقة يومية: صحة وتقنية وتطوير ذات وثقافة',
                 desc='مقال قصير موثّق كل يوم في الصحة والتقنية وتطوير الذات والمال والثقافة، بخلاصة عملية تطبّقها في يومك.',
                 home='إشراقة يومية', crumb='المقالات', h1='مقالات إشراقة', all='الكل', feat='☀ مقال اليوم',
                 search='ابحث في المقالات…', cats='التصنيفات', empty='لا توجد مقالات مطابقة. جرّب كلمة أخرى.', note='')
    names = CAT_EN if en else CATEGORIES
    nodes = [seo.webpage(url, T['title'], T['desc'], 'CollectionPage',
                         mainEntity=seo.item_list([SITE + view(a, en)['href'] for a in items])),
             seo.breadcrumb(url, [(T['home'], f'{SITE}/en/' if en else f'{SITE}/'), (T['crumb'], url)]), seo.org(), seo.website()]
    feat, rest = (items[0], items[1:]) if items else (None, [])
    used = []
    for a in items:
        if a['category'] in CATEGORIES and a['category'] not in used:
            used.append(a['category'])
    chips = (f'<button class="chip" type="button" data-c="" aria-pressed="true">{T["all"]}</button>'
             + ''.join(f'<button class="chip" type="button" data-c="{esc(c)}" aria-pressed="false">{esc(names.get(c, CATEGORIES[c]))}</button>'
                       for c in used))
    feat_html = ''
    if feat:
        q = ' '.join([feat['title'], feat.get('excerpt') or '', feat.get('title_tr') or '', CATEGORIES.get(feat['category'], ''), CAT_EN.get(feat['category'], '')])
        fv = view(feat, en)
        ar = ' lang="ar" dir="rtl"' if fv['rtl'] else ''
        who = f'<bdi>{esc(author_en(feat))}</bdi>' if en else esc(author_of(feat))
        meta = ' · '.join(x for x in [who, esc(minutes(feat, en)), esc(feat.get('publish_date') or '')] if x)
        feat_html = (
            f'<a class="feat rv" href="{fv["href"]}" data-cat="{esc(feat["category"])}" data-q="{esc(q)}">'
            f'<div class="ph"><img src="{esc(sized(feat.get("cover_url") or "/img/og.jpg", 1024))}" alt="{esc(fv["title"])}" width="900" height="560" fetchpriority="high"></div>'
            f'<div class="in"><span class="tag">{T["feat"]}</span>{pill(feat["category"], en)}<b{ar}>{esc(fv["title"])}</b>'
            f'<p{ar}>{esc(fv["excerpt"])}</p><small>{meta}</small></div></a>')
    page = (
        HEAD.format(**(EN_HEAD if en else AR_HEAD), title=T['title'], desc=T['desc'], url=url, og_type='website', og_title=T['title'],
                    image=f'{SITE}/img/og.jpg', css=CSS, nav_css=site_nav.NAV_CSS, nav=site_nav.header(path))
        + '<header class="hero-i"><video class="hero-v" autoplay muted loop playsinline preload="metadata" poster="/media/articles/hero.jpg" aria-hidden="true" tabindex="-1" disablepictureinpicture disableremoteplayback><source src="/media/articles/hero.mp4" type="video/mp4"><source src="/media/articles/hero.webm" type="video/webm"></video>'
        + f'<div class="wrap wide"><h1>{T["h1"]}</h1>'
        + f'<p>{T["desc"]}{(" " + T["note"]) if T["note"] else ""}</p>'
        + f'<label class="search">{SEARCH_ICON}<input type="search" placeholder="{T["search"]}" aria-label="{T["search"]}"></label>'
        + '</div></header>'
        + f'<div class="wrap wide"><main><div class="chips" role="group" aria-label="{T["cats"]}">{chips}</div>'
        + feat_html
        + f'<div class="grid">{"".join(card(a, en) for a in rest)}</div>'
        + f'<p class="empty">{T["empty"]}</p>'
        + '</main></div>' + FOOT.format(foot=site_footer.footer(path), js=js())
    )
    return seo.finalize(page, url=url, title=T['title'], desc=T['desc'], nodes=nodes, lang='en' if en else 'ar', alternates=alts)


def home_latest(items: list, n: int = 6) -> None:
    """الرئيسية: أحدث المقالات (روابط يقرؤها محرك البحث ويصل منها إلى كل مقال جديد)، تُحدَّث مع كل بناء"""
    home = ROOT / 'index.html'
    if not home.exists():
        return
    cards = ''.join(
        f'<a class="hl-c" href="/a/{esc(a["slug"])}/"><img src="{esc(sized(a.get("cover_url") or "/img/og.jpg", 640))}" alt="" loading="lazy" decoding="async" width="640" height="360">'
        f'<span class="hl-k">{esc(CATEGORIES.get(a["category"], ""))}</span><b>{esc(a["title"])}</b></a>'
        for a in items[:n])
    block = ('<!--LATEST--><section class="hl" aria-label="أحدث المقالات"><div class="wrap">'
             '<div class="hl-h"><h2>من مقالات إشراقة</h2><a href="/a/">كل المقالات ←</a></div>'
             f'<div class="hl-g">{cards}</div></div>'
             '<style>.hl{padding:clamp(70px,9vw,120px) 0 0}.hl-h{display:flex;align-items:baseline;justify-content:space-between;gap:16px;margin-bottom:22px}'
             '.hl-h h2{margin:0}.hl-h a{color:#f6c48a;font-weight:700;text-decoration:none;white-space:nowrap}'
             '.hl-g{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}'
             '.hl-c{display:block;text-decoration:none;color:inherit;border-radius:20px;overflow:hidden;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);transition:transform .3s,border-color .3s}'
             '.hl-c:hover{transform:translateY(-4px);border-color:rgba(248,210,153,.4)}'
             '.hl-c img{display:block;width:100%;height:auto;aspect-ratio:16/9;object-fit:cover}'
             '.hl-k{display:block;margin:14px 18px 4px;font-size:13px;color:#f6c48a;font-weight:700}'
             '.hl-c b{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;margin:0 18px 18px;font-size:18px;line-height:1.6}'
             '@media (max-width:900px){.hl-g{grid-template-columns:1fr 1fr}}@media (max-width:560px){.hl-g{grid-template-columns:1fr}.hl-c:nth-child(n+4){display:none}}</style>'
             '</section><!--/LATEST-->')
    html = home.read_text(encoding='utf-8')
    import re as _re
    if '<!--LATEST-->' in html:
        html = _re.sub(r'<!--LATEST-->.*?<!--/LATEST-->', lambda _m: block, html, count=1, flags=_re.S)
    else:
        html = html.replace('  <section class="cta">', block + chr(10) + '  <section class="cta">', 1)
    home.write_text(html, encoding='utf-8')


def main() -> None:
    for c in fetch('article_categories?select=slug,name_ar'):
        CATEGORIES[c['slug']] = c['name_ar']
    today = dt.date.today().isoformat()
    items = fetch(
        'articles?select=slug,title,excerpt,body,title_tr,excerpt_tr,body_tr,cover_url,category,author_name,reading_minutes,sources,publish_date,updated_at,'
        'author:profiles!articles_author_id_fkey(display_name)'
        f'&status=eq.published&publish_date=lte.{today}&order=publish_date.desc,published_at.desc&limit=500'
    )
    if OUT.exists():
        if len(items) < 20:
            sys.exit(f'only {len(items)} articles returned; refusing to rebuild a/')
        shutil.rmtree(OUT)
    OUT.mkdir()
    EN_OUT = ROOT / 'en' / 'a'
    if EN_OUT.exists():
        shutil.rmtree(EN_OUT)
    EN_OUT.mkdir(parents=True)
    for a in items:
        if has_en(a):
            site_nav.ALT[f'/a/{a["slug"]}/'] = f'/en/a/{a["slug"]}/'
    for a in items:
        d = OUT / a['slug']
        d.mkdir()
        (d / 'index.html').write_text(article_page(a, related_to(a, items)), encoding='utf-8')
        if has_en(a):
            (EN_OUT / a['slug']).mkdir()
            (EN_OUT / a['slug'] / 'index.html').write_text(article_page(a, related_to(a, items), en=True), encoding='utf-8')
    (OUT / 'index.html').write_text(index_page(items), encoding='utf-8')
    (EN_OUT / 'index.html').write_text(index_page(items, en=True), encoding='utf-8')
    home_latest(items)

    # خريطة الموقع كاملة (كل صفحة قابلة للفهرسة، مع تاريخ آخر تغيير) وملف llms.txt
    n = len(seo.write_sitemap(ROOT))
    seo.write_llms(ROOT)
    print(f'{len(items)} articles, {n} urls in sitemap')


if __name__ == '__main__':
    main()
