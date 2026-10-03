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
import urllib.request
from pathlib import Path

import markdown

SUPABASE_URL = 'https://jytbowsfvuzdnsmhmsly.supabase.co'
PUBLISHABLE_KEY = 'sb_publishable_cm8SXt2NPRY5RY7dclZsLw_4ng3Q0TD'
SITE = 'https://ishraqa.otwox.com'
PLAY = 'https://play.google.com/store/apps/details?id=com.taeziz.ishraqa'
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'a'

CATEGORIES = {}


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
<link href="https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
:root{{--night:#2A1B5E;--plum:#8E3A8C;--sun:#F07A4A;--gold:#FFB547;--cream:#FFFBF8;--ink:#2A1B5E;--muted:#5E5770;--card:#fff;--line:#EEE7F6}}
@media (prefers-color-scheme:dark){{:root{{--cream:#14101F;--ink:#F3EEFB;--muted:#B8B0C9;--card:#1E1830;--line:#2E2645}}}}
*{{box-sizing:border-box}}body{{margin:0;font-family:Cairo,Tahoma,sans-serif;background:var(--cream);color:var(--ink);line-height:1.9}}
a{{color:inherit}}.wrap{{max-width:760px;margin:0 auto;padding:0 20px}}
.top{{background:linear-gradient(140deg,var(--night),var(--plum) 60%,var(--sun));color:#fff}}
.top .wrap{{display:flex;align-items:center;justify-content:space-between;padding:14px 20px}}
.brand{{display:flex;align-items:center;gap:10px;font-weight:800;text-decoration:none}}.brand img{{width:34px;height:34px;border-radius:9px}}
.btn{{display:inline-block;font-weight:700;text-decoration:none;border-radius:30px;padding:9px 18px}}
.btn.light{{background:rgba(255,255,255,.18);color:#fff;font-size:14px}}
.btn.main{{background:var(--sun);color:#fff;font-size:16px;padding:12px 26px}}
.cover{{width:100%;aspect-ratio:16/9;object-fit:cover;border-radius:0 0 26px 26px;display:block}}
.cat{{display:inline-block;margin-top:22px;padding:3px 14px;border-radius:20px;background:#F3EEFB;color:#4B2E83;font-weight:700;font-size:13px}}
h1{{font-size:32px;line-height:1.45;margin:12px 0}}
.meta{{color:var(--muted);font-size:14px;margin-bottom:18px}}
article h2{{font-size:23px;margin:28px 0 8px}}article h3{{font-size:19px}}
article p,article li{{font-size:18px}}
article blockquote{{margin:18px 0;padding:14px 18px;border-radius:14px;background:#FFE6DA;color:#5A2410}}
.cta{{margin:36px 0;padding:26px;border-radius:24px;background:linear-gradient(140deg,var(--night),var(--plum));color:#fff;text-align:center}}
.cta p{{margin:0 0 14px;font-size:17px}}
.list a.item{{display:flex;gap:14px;align-items:center;text-decoration:none;padding:12px;border-radius:18px;background:var(--card);border:1px solid var(--line);margin-bottom:12px}}
.list img{{width:120px;height:78px;object-fit:cover;border-radius:12px;flex-shrink:0}}
.list b{{display:block;line-height:1.5}}.list small{{color:var(--muted)}}
.src{{font-size:13px;color:var(--muted);border-top:1px solid var(--line);margin-top:26px;padding-top:12px;white-space:pre-line}}
footer{{color:var(--muted);font-size:13px;text-align:center;padding:30px 0;line-height:2.2}}
footer a{{color:var(--muted);text-decoration:none}} footer nav{{margin-bottom:4px}}
</style></head><body>
<div class="top"><div class="wrap"><a class="brand" href="/"><img src="/img/icon-192.png" alt=""> إشراقة يومية</a>
<a class="btn light" href="{open_app}">افتح في التطبيق</a></div></div>
"""

FOOT = """<footer><nav><a href="/privacy/">سياسة الخصوصية</a> · <a href="/terms/">شروط الاستخدام</a> ·
<a href="/contact/">تواصل معنا</a></nav><a href="https://otwox.com">بواسطة أوتواكس للحلول الرقمية</a></footer></body></html>"""


def article_page(a: dict) -> str:
    slug = a['slug']
    url = f'{SITE}/a/{slug}/'
    author = (a.get('author') or {}).get('display_name') or a['author_name']
    cover = a.get('cover_url') or f'{SITE}/img/og.jpg'
    body_html = markdown.markdown(a['body'], extensions=['extra', 'sane_lists'])
    cat = CATEGORIES.get(a['category'], '')
    date = a.get('publish_date') or ''
    return (
        HEAD.format(title=esc(a['title']) + ' · إشراقة يومية', desc=esc(a.get('excerpt')), url=url,
                    og_type='article', og_title=esc(a['title']), image=esc(cover),
                    open_app=PLAY)
        + '<div class="wrap" style="padding:0">'
        + f'<img class="cover" src="{esc(cover)}" alt="">'
        + '</div><div class="wrap"><main>'
        + (f'<span class="cat">{esc(cat)}</span>' if cat else '')
        + f'<h1>{esc(a["title"])}</h1>'
        + f'<div class="meta">بقلم {esc(author)} · {a["reading_minutes"]} دقائق قراءة · {esc(date)}</div>'
        + f'<article>{body_html}</article>'
        + '<div class="cta"><p>اقرأ مقالًا جديدًا كل يوم، وحكمة كل صباح، في تطبيق إشراقة يومية</p>'
        + f'<a class="btn main" href="{PLAY}">حمّل التطبيق مجانًا</a></div>'
        + (f'<div class="src">المراجع:\n{esc(a.get("sources"))}</div>' if a.get('sources') else '')
        + '</main></div>' + FOOT.format(year=dt.date.today().year)
    )


def index_page(items: list) -> str:
    rows = ''.join(
        f'<a class="item" href="/a/{esc(a["slug"])}/"><img src="{esc(a.get("cover_url") or "/img/og.jpg")}" alt="" loading="lazy">'
        f'<span><b>{esc(a["title"])}</b><small>{esc(CATEGORIES.get(a["category"], ""))} · {esc(a.get("publish_date"))}</small></span></a>'
        for a in items
    )
    return (
        HEAD.format(title='مقالات إشراقة يومية', desc='مقال يومي يستحق القراءة في الصحة والتقنية وتطوير الذات والثقافة.',
                    url=f'{SITE}/a/', og_type='website', og_title='مقالات إشراقة يومية',
                    image=f'{SITE}/img/og.jpg', open_app=PLAY)
        + '<div class="wrap"><main><h1>مقالات إشراقة</h1><div class="list">' + rows
        + '</div></main></div>' + FOOT.format(year=dt.date.today().year)
    )


def main() -> None:
    for c in fetch('article_categories?select=slug,name_ar'):
        CATEGORIES[c['slug']] = c['name_ar']
    today = dt.date.today().isoformat()
    items = fetch(
        'articles?select=slug,title,excerpt,body,cover_url,category,author_name,reading_minutes,sources,publish_date,'
        'author:profiles!articles_author_id_fkey(display_name)'
        f'&status=eq.published&publish_date=lte.{today}&order=publish_date.desc&limit=500'
    )
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    for a in items:
        d = OUT / a['slug']
        d.mkdir()
        (d / 'index.html').write_text(article_page(a), encoding='utf-8')
    (OUT / 'index.html').write_text(index_page(items), encoding='utf-8')

    urls = [f'{SITE}/', f'{SITE}/a/'] + [f'{SITE}/a/{a["slug"]}/' for a in items]
    (ROOT / 'sitemap.xml').write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        + ''.join(f'<url><loc>{u}</loc></url>' for u in urls) + '</urlset>\n', encoding='utf-8')
    print(f'{len(items)} articles')


if __name__ == '__main__':
    main()
