"""يولّد صفحة ويب لكل مقال منشور في إشراقة (ishraqa.otwox.com/a/<slug>/)
مع معاينة المشاركة (صورة الغلاف) وزر فتح التطبيق، وصفحة فهرس /a/.

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

SUPABASE_URL = 'https://jytbowsfvuzdnsmhmsly.supabase.co'
PUBLISHABLE_KEY = 'sb_publishable_cm8SXt2NPRY5RY7dclZsLw_4ng3Q0TD'
SITE = 'https://ishraqa.otwox.com'
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


def esc(s) -> str:
    return html.escape(s or '', quote=True)


HEAD = """<!doctype html>
<html lang="ar" dir="rtl"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#2A1B5E">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="/img/icon-192.png">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="إشراقة يومية">
<meta property="og:locale" content="ar_AR">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{image}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&family=Amiri:ital@0;1&display=swap" rel="stylesheet">
<style>{css}</style></head><body>
<div class="top"><div class="wrap wide"><a class="brand" href="/a/"><img src="/img/icon-192.png" width="192" height="192" alt=""> إشراقة يومية</a>
<nav class="tnav"><a href="/a/">المقالات</a>
<a class="btn light" data-open href="{open_app}">افتح في التطبيق</a></nav></div></div>
"""

CSS = """
:root{--night:#2A1B5E;--plum:#8E3A8C;--sun:#F07A4A;--gold:#FFB547;--cream:#FFFBF8;--ink:#2A1B5E;--muted:#5E5770;--card:#fff;--line:#EEE7F6;--soft:#F6F1FB}
@media (prefers-color-scheme:dark){:root{--cream:#13101D;--ink:#F3EEFB;--muted:#B8B0C9;--card:#1C1729;--line:#2C2442;--soft:#221C33}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font-family:Cairo,Tahoma,sans-serif;background:var(--cream);color:var(--ink);line-height:1.9;-webkit-font-smoothing:antialiased}
a{color:inherit}img{max-width:100%}
.wrap{max-width:780px;margin:0 auto;padding:0 20px}.wrap.wide{max-width:1180px}
.top{position:sticky;top:0;z-index:20;background:linear-gradient(120deg,var(--night),var(--plum) 60%,var(--sun));color:#fff;box-shadow:0 6px 24px rgba(42,27,94,.18)}
.top .wrap{display:flex;align-items:center;justify-content:space-between;padding:12px 20px;gap:14px}
.brand{display:flex;align-items:center;gap:10px;font-weight:800;text-decoration:none;white-space:nowrap}.brand img{width:34px;height:34px;border-radius:9px}
.tnav{display:flex;align-items:center;gap:18px}.tnav a{text-decoration:none;font-weight:700;font-size:15px;opacity:.9}.tnav a:hover{opacity:1}
@media (max-width:640px){.tnav a:not(.btn){display:none}}
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
.hero-i:after{content:'';position:absolute;inset:auto -10% -55% auto;width:520px;height:520px;border-radius:50%;background:radial-gradient(circle,rgba(255,181,71,.45),transparent 65%)}
.hero-i .wrap{position:relative;z-index:1}
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
.feat .tag{font-weight:800;color:var(--sun);font-size:14px;letter-spacing:.3px}
.feat b{font-size:clamp(24px,2.8vw,32px);line-height:1.45}.feat p{margin:0;color:var(--muted);font-size:16.5px;line-height:1.85}
.feat small{color:var(--muted)}
@media (max-width:820px){.feat{grid-template-columns:1fr}.feat .ph{min-height:0;aspect-ratio:16/9}.feat .in{padding:22px}}
.get{margin:44px 0 10px;padding:38px 24px;border-radius:28px;text-align:center;background:linear-gradient(135deg,var(--night),var(--plum) 60%,var(--sun));color:#fff}
.get h2{margin:0 0 6px;font-size:26px}.get p{margin:0 auto 22px;max-width:560px;opacity:.92}
.stores{display:flex;flex-wrap:wrap;gap:10px;justify-content:center}
.store{display:inline-flex;align-items:center;gap:10px;background:#000;color:#fff;text-decoration:none;padding:11px 18px;border-radius:14px;box-shadow:0 10px 26px rgba(0,0,0,.25);transition:transform .2s}
.store:hover{transform:translateY(-2px)}.store svg{width:26px;height:26px}.store small{display:block;font-size:11px;opacity:.8;line-height:1.2}.store b{display:block;font-size:17px;line-height:1.3}
.empty{display:none;text-align:center;color:var(--muted);padding:40px 0}
main{padding-bottom:20px}
.rv{opacity:0;transform:translateY(18px);transition:opacity .6s ease,transform .6s ease}.rv.on{opacity:1;transform:none}
@media (prefers-reduced-motion:reduce){.rv{opacity:1;transform:none;transition:none}.card,.card img,.feat,.feat img,.btn{transition:none}html{scroll-behavior:auto}}
footer{color:var(--muted);font-size:13px;text-align:center;padding:34px 0;line-height:2.2;border-top:1px solid var(--line);margin-top:30px}
footer a{color:var(--muted);text-decoration:none}footer nav{margin-bottom:4px}
"""

# يظهر العنصر بهدوء عند الوصول إليه، وزر «افتح في التطبيق» يناسب جهاز القارئ
JS = """<script>
(function(){
var ua=navigator.userAgent,rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
var apple=/iPhone|iPad|iPod|Macintosh/.test(ua),android=/Android/.test(ua),win=/Windows NT/.test(ua);
document.querySelectorAll('a[data-open]').forEach(function(a){
  if(android)return;
  if(win){a.href='__MS__';a.target='_blank';a.rel='noopener';}
  else if(apple){a.href='/app/';}
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

FOOT = """<footer><nav><a href="/a/">المقالات</a> · <a href="/privacy/">سياسة الخصوصية</a> · <a href="/terms/">شروط الاستخدام</a> ·
<a href="/delete-account/">حذف الحساب</a> · <a href="/contact/">تواصل معنا</a></nav><div>© {year} إشراقة يومية<br><a href="https://otwox.com">تطوير أوتواكس للحلول الرقمية</a></div></footer>
{js}</body></html>"""

ICONS = {
    'wa': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.6-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 0 0 1.8-1.2 2.2 2.2 0 0 0 .2-1.2c-.1-.1-.3-.2-.5-.3z"/></svg>',
    'x': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.2 2.3h3.4l-7.4 8.4 8.7 11h-6.8l-5.3-6.9-6.1 6.9H1.3l7.9-9L.9 2.3h7l4.8 6.3zm-1.2 17.4h1.9L7 4.2H5z"/></svg>',
    'fb': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21.9v-7.4H16l.4-2.9h-2.9V9.8c0-.8.2-1.4 1.4-1.4h1.6V5.8a21 21 0 0 0-2.3-.1c-2.3 0-3.8 1.4-3.8 3.9v2H8v2.9h2.4v7.4a10 10 0 1 1 3.1 0z"/></svg>',
    'tg': '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M21.9 4.3 18.7 19.5c-.2 1-.9 1.3-1.8.8l-4.9-3.6-2.4 2.3c-.3.3-.5.5-1 .5l.3-5 9.1-8.2c.4-.4-.1-.6-.6-.2L6.2 13.2l-4.8-1.5c-1-.3-1-1 .2-1.5L20.5 3c.9-.3 1.6.2 1.4 1.3z"/></svg>',
    'link': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M10 14a5 5 0 0 0 7 0l3-3a5 5 0 0 0-7-7l-1 1"/><path d="M14 10a5 5 0 0 0-7 0l-3 3a5 5 0 0 0 7 7l1-1"/></svg>',
}
STORES = (
    '<section class="get rv"><h2>حمّل إشراقة يومية</h2><p>مقال جديد كل يوم، وحكمة مع شرحها، ومكتبة ونوادٍ للقراءة. مجاني وبلا إعلانات.</p><div class="stores">'
    '<a class="store" href="__PLAY__" aria-label="احصل عليه من Google Play"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#34A853" d="M3.6 2.2 13.4 12l-9.8 9.8c-.4-.2-.6-.6-.6-1.1V3.3c0-.5.2-.9.6-1.1z"/><path fill="#FBBC04" d="m16.7 15.3-3.3-3.3 3.3-3.3 3.7 2.1c1.1.6 1.1 1.8 0 2.4z"/><path fill="#EA4335" d="M3.6 21.8 13.4 12l3.3 3.3L5 21.9c-.5.3-1 .2-1.4-.1z"/><path fill="#4285F4" d="M3.6 2.2c.4-.3.9-.4 1.4-.1l11.7 6.6L13.4 12z"/></svg><span><small>احصل عليه من</small><b>Google Play</b></span></a>'
    '<a class="store" href="/app/" aria-label="إشراقة على آيفون وماك"><svg viewBox="0 0 24 24" aria-hidden="true" fill="#fff"><path d="M12.152 6.896c-.948 0-2.415-1.078-3.96-1.04-2.04.027-3.91 1.183-4.961 3.014-2.117 3.675-.546 9.103 1.519 12.09 1.013 1.454 2.208 3.09 3.792 3.039 1.52-.065 2.09-.987 3.935-.987 1.831 0 2.35.987 3.96.948 1.637-.026 2.676-1.48 3.676-2.948 1.156-1.688 1.636-3.325 1.662-3.415-.039-.013-3.182-1.221-3.22-4.857-.026-3.04 2.48-4.494 2.597-4.559-1.429-2.09-3.623-2.324-4.39-2.376-2-.156-3.675 1.09-4.61 1.09zM15.53 3.83c.843-1.012 1.4-2.427 1.245-3.83-1.207.052-2.662.805-3.532 1.818-.78.896-1.454 2.338-1.273 3.714 1.338.104 2.715-.688 3.559-1.701"/></svg><span><small>متوفر على</small><b>آيفون وماك</b></span></a>'
    '<a class="store" href="__MS__" target="_blank" rel="noopener" aria-label="إشراقة على ويندوز"><svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#0A84FF" d="M2 2h9.6v9.6H2zM12.4 2H22v9.6h-9.6zM2 12.4h9.6V22H2zM12.4 12.4H22V22h-9.6z"/></svg><span><small>احصل عليه من</small><b>Microsoft Store</b></span></a>'
    '</div></section><script src="/apple-only.js" defer></script>'
)
SEARCH_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>'


def js() -> str:
    return JS.replace('__MS__', MS_STORE).replace('__PLAY__', PLAY)


def open_app(path: str, ref: str) -> str:
    """على أندرويد يفتح التطبيق على الصفحة نفسها إن كان مثبتًا، وإلا Google Play (والأجهزة الأخرى يضبطها JS)"""
    from urllib.parse import quote
    play = f'{PLAY}&referrer=' + quote(f'utm_source=web&utm_medium={ref}')
    return (f'intent://ishraqa.otwox.com{path}#Intent;scheme=https;package=com.taeziz.ishraqa;'
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


def pill(cat_slug: str) -> str:
    name = CATEGORIES.get(cat_slug, '')
    if not name:
        return ''
    return f'<span class="pill" style="--c:{CAT_COLORS.get(cat_slug, "#8E3A8C")}">{esc(name)}</span>'


def minutes(a: dict) -> str:
    m = a.get('reading_minutes')
    return f'{m} دقائق قراءة' if m else ''


def card(a: dict) -> str:
    q = ' '.join([a['title'], a.get('excerpt') or '', CATEGORIES.get(a['category'], '')])
    meta = ' · '.join(x for x in [author_of(a), minutes(a), a.get('publish_date') or ''] if x)
    return (f'<a class="card rv" href="/a/{esc(a["slug"])}/" data-cat="{esc(a["category"])}" data-q="{esc(q)}">'
            f'<div class="ph"><img src="{esc(a.get("cover_url") or "/img/og.jpg")}" alt="{esc(a["title"])}" width="640" height="400" loading="lazy"></div>'
            f'<div class="in">{pill(a["category"])}<b>{esc(a["title"])}</b>'
            f'<p>{esc(a.get("excerpt") or "")}</p><small>{esc(meta)}</small></div></a>')


def share_row(url: str, title: str) -> str:
    from urllib.parse import quote
    u, t = quote(url, safe=''), quote(title, safe='')
    links = [
        ('wa', 'واتساب', f'https://wa.me/?text={t}%20{u}'),
        ('x', 'X', f'https://twitter.com/intent/tweet?text={t}&url={u}'),
        ('fb', 'فيسبوك', f'https://www.facebook.com/sharer/sharer.php?u={u}'),
        ('tg', 'تيليجرام', f'https://t.me/share/url?url={u}&text={t}'),
    ]
    out = ''.join(f'<a href="{h}" target="_blank" rel="noopener" aria-label="مشاركة عبر {n}" title="{n}">{ICONS[k]}</a>'
                  for k, n, h in links)
    return (f'<div class="share"><span>شارك المقال</span>{out}'
            f'<button type="button" data-copy aria-label="نسخ الرابط" title="نسخ الرابط">{ICONS["link"]}</button>'
            '<span class="ok">نُسخ الرابط ✓</span></div>')


def article_page(a: dict, related: list) -> str:
    slug = a['slug']
    url = f'{SITE}/a/{slug}/'
    author = author_of(a)
    cover = a.get('cover_url') or f'{SITE}/img/og.jpg'
    body_html = markdown.markdown(teaser(a['body']), extensions=['extra', 'sane_lists'])
    app = open_app(f'/a/{slug}/', 'article')
    cat = CATEGORIES.get(a['category'], '')
    date = a.get('publish_date') or ''
    modified = (a.get('updated_at') or '')[:10] or date
    if modified < date:
        modified = date
    title = seo.fit_title(a['title'])
    desc = seo.clip(a.get('excerpt') or a['title'], 155)
    who = ({'@type': 'Organization', 'name': author, 'url': f'{SITE}/about/'} if is_team(author)
           else {'@type': 'Person', 'name': author})
    nodes = [
        {'@type': 'Article', '@id': url + '#article', 'headline': seo.clip(a['title'], 110), 'description': desc,
         'image': [cover], 'datePublished': date, 'dateModified': modified, 'author': who,
         'publisher': {'@id': seo.ORG_ID}, 'mainEntityOfPage': {'@id': url + '#webpage'},
         'isPartOf': {'@id': seo.WEBSITE_ID}, 'articleSection': cat or None, 'inLanguage': 'ar',
         'timeRequired': f'PT{a["reading_minutes"]}M' if a.get('reading_minutes') else None,
         'isAccessibleForFree': True},
        seo.webpage(url, a['title'], desc),
        seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('المقالات', f'{SITE}/a/'), (a['title'], url)]),
        seo.org(), seo.website(),
    ]
    nodes[0] = {k: v for k, v in nodes[0].items() if v is not None}
    initial = (author.replace('م.', '').replace('د.', '').strip() or 'إ')[0]
    avatar = ('<img class="avatar" src="/img/icon-192.png" alt="" width="46" height="46">' if is_team(author)
              else f'<div class="avatar" aria-hidden="true">{esc(initial)}</div>')
    meta = ' · '.join(x for x in [minutes(a), f'<time datetime="{esc(date)}">{esc(date)}</time>' if date else ''] if x)
    more = ''.join(card(r) for r in related)
    page = (
        HEAD.format(title=esc(title), desc=esc(desc), url=url, og_type='article', og_title=esc(a['title']),
                    image=esc(cover), open_app=app, css=CSS)
        + '<div class="progress" aria-hidden="true"></div>'
        + f'<div class="hero-a"><figure><img src="{esc(cover)}" alt="{esc(a["title"])}" width="1600" height="800" fetchpriority="high"></figure></div>'
        + '<div class="wrap"><main><div class="head-a">'
        + pill(a['category'])
        + f'<h1>{esc(a["title"])}</h1>'
        + (f'<p class="lead">{esc(a["excerpt"])}</p>' if a.get('excerpt') else '')
        + f'<div class="byline">{avatar}'
        + f'<div><b>{esc(author)}</b><small>{meta}</small></div></div></div>'
        + f'<article class="fade">{body_html}</article>'
        + '<div class="cta rv"><h3>أكمل القراءة في إشراقة يومية</h3>'
        + '<p>المقال كاملًا مع خلاصته العملية، ومقال جديد كل يوم، ومكتبة ونوادٍ للقراءة.</p>'
        + f'<a class="btn main" data-open href="{app}">اقرأه كاملًا في التطبيق</a>'
        + '<small>مجاني وبلا إعلانات · أندرويد وويندوز وآيفون وماك</small></div>'
        + share_row(url, a['title'])
        + '</main></div>'
        + (f'<div class="wrap wide"><h2 class="sec">اقرأ أيضًا</h2><div class="grid">{more}</div></div>' if more else '')
        + FOOT.format(year=dt.date.today().year, js=js())
    )
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes, image=cover, image_alt=a['title'],
                        og_type='article', article={'published': date, 'modified': modified, 'section': cat})


def related_to(a: dict, items: list, n: int = 3) -> list:
    """مقالات من التصنيف نفسه أولًا، ثم الأحدث"""
    others = [r for r in items if r['slug'] != a['slug']]
    same = [r for r in others if r['category'] == a['category']]
    return (same + [r for r in others if r not in same])[:n]


def index_page(items: list) -> str:
    url = f'{SITE}/a/'
    title = 'مقالات إشراقة يومية: صحة وتقنية وتطوير ذات وثقافة'
    desc = 'مقال قصير موثّق كل يوم في الصحة والتقنية وتطوير الذات والمال والثقافة، بخلاصة عملية تطبّقها في يومك.'
    nodes = [seo.webpage(url, title, desc, 'CollectionPage',
                         mainEntity=seo.item_list([f'{SITE}/a/{a["slug"]}/' for a in items])),
             seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('المقالات', url)]), seo.org(), seo.website()]
    feat, rest = (items[0], items[1:]) if items else (None, [])
    used = []
    for a in items:
        if a['category'] in CATEGORIES and a['category'] not in used:
            used.append(a['category'])
    chips = ('<button class="chip" type="button" data-c="" aria-pressed="true">الكل</button>'
             + ''.join(f'<button class="chip" type="button" data-c="{esc(c)}" aria-pressed="false">{esc(CATEGORIES[c])}</button>'
                       for c in used))
    feat_html = ''
    if feat:
        q = ' '.join([feat['title'], feat.get('excerpt') or '', CATEGORIES.get(feat['category'], '')])
        meta = ' · '.join(x for x in [author_of(feat), minutes(feat), feat.get('publish_date') or ''] if x)
        feat_html = (
            f'<a class="feat rv" href="/a/{esc(feat["slug"])}/" data-cat="{esc(feat["category"])}" data-q="{esc(q)}">'
            f'<div class="ph"><img src="{esc(feat.get("cover_url") or "/img/og.jpg")}" alt="{esc(feat["title"])}" width="900" height="560" fetchpriority="high"></div>'
            f'<div class="in"><span class="tag">☀ مقال اليوم</span>{pill(feat["category"])}<b>{esc(feat["title"])}</b>'
            f'<p>{esc(feat.get("excerpt") or "")}</p><small>{esc(meta)}</small></div></a>')
    page = (
        HEAD.format(title=title, desc=desc, url=url, og_type='website', og_title=title,
                    image=f'{SITE}/img/og.jpg', open_app=PLAY, css=CSS)
        + '<header class="hero-i"><div class="wrap wide"><h1>مقالات إشراقة</h1>'
        + '<p>مقال قصير موثّق كل يوم في الصحة والتقنية وتطوير الذات والمال والثقافة، بخلاصة عملية تطبّقها في يومك.</p>'
        + f'<div class="stats"><div><b>{len(items)}</b>مقالًا</div><div><b>{len(used)}</b>تصنيفات</div><div><b>مجانًا</b>بلا إعلانات</div></div>'
        + f'<label class="search">{SEARCH_ICON}<input type="search" placeholder="ابحث في المقالات…" aria-label="ابحث في المقالات"></label>'
        + '</div></header>'
        + f'<div class="wrap wide"><main><div class="chips" role="group" aria-label="التصنيفات">{chips}</div>'
        + feat_html
        + f'<div class="grid">{"".join(card(a) for a in rest)}</div>'
        + '<p class="empty">لا توجد مقالات مطابقة. جرّب كلمة أخرى.</p>'
        + STORES.replace('__PLAY__', PLAY).replace('__MS__', MS_STORE)
        + '</main></div>' + FOOT.format(year=dt.date.today().year, js=js())
    )
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes)


def main() -> None:
    for c in fetch('article_categories?select=slug,name_ar'):
        CATEGORIES[c['slug']] = c['name_ar']
    today = dt.date.today().isoformat()
    items = fetch(
        'articles?select=slug,title,excerpt,body,cover_url,category,author_name,reading_minutes,sources,publish_date,updated_at,'
        'author:profiles!articles_author_id_fkey(display_name)'
        f'&status=eq.published&publish_date=lte.{today}&order=publish_date.desc,published_at.desc&limit=500'
    )
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for a in items:
        d = OUT / a['slug']
        d.mkdir()
        (d / 'index.html').write_text(article_page(a, related_to(a, items)), encoding='utf-8')
    (OUT / 'index.html').write_text(index_page(items), encoding='utf-8')

    # خريطة الموقع كاملة (كل صفحة قابلة للفهرسة، مع تاريخ آخر تغيير) وملف llms.txt
    n = len(seo.write_sitemap(ROOT))
    seo.write_llms(ROOT)
    print(f'{len(items)} articles, {n} urls in sitemap')


if __name__ == '__main__':
    main()
