"""صفحات الحِكم والكتب للبحث: ishraqa.otwox.com/q/<id>/ و /k/<slug>/

لكل حكمة: نصها وقائلها، ومعناها وقصتها وكيف تطبّقها اليوم، وحِكم من موضوعها.
لكل كتاب: غلافه ووصفه، وأول ما فيه باختصار، وزر القراءة في التطبيق.
الشروح والملخصات تُقرأ من قاعدة البيانات بمفتاح الإدارة المحلي، فيُشغَّل يدويًا:
    python site/tools/build_wisdom.py <مجلد مستودع الموقع>
"""
import datetime as dt
import json
import os
import pathlib
import shutil
import sys
import urllib.request

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_articles import FOOT, HEAD, PLAY, SITE, esc, open_app  # noqa: E402
import seo  # noqa: E402
from urllib.parse import quote as urlquote  # noqa: E402

APP = pathlib.Path(__file__).resolve().parents[2]
SLUGS = {
    'كليلة ودمنة': 'kalila-wa-dimna', 'طوق الحمامة': 'tawq-al-hamama',
    'حي بن يقظان': 'hayy-ibn-yaqzan', 'البخلاء': 'al-bukhala', 'النظرات': 'al-nazarat',
}
EXTRA_CSS = """<style>
.quote{margin:26px 0 8px;padding:28px 24px;border-radius:26px;background:linear-gradient(140deg,var(--night),var(--plum) 62%,var(--sun));color:#fff;text-align:center}
.quote p,.quote h1{font-size:27px;line-height:1.7;margin:0 0 10px;font-weight:700}.quote span{color:#FFD27A;font-size:16px}
.sec h2{font-size:21px;margin:26px 0 6px}.sec p{font-size:18px;margin:0}
.apply{margin-top:22px;padding:18px;border-radius:18px;background:#FFF1E6;color:#5A2410}.apply h2{margin-top:0}
.chips a{display:inline-block;margin:0 0 10px 8px;padding:6px 14px;border-radius:20px;background:var(--card);border:1px solid var(--line);text-decoration:none;font-size:15px}
.qlist a{display:block;text-decoration:none;padding:14px 16px;border-radius:16px;background:var(--card);border:1px solid var(--line);margin-bottom:10px}
.qlist small{display:block;color:var(--muted)}
.book{display:flex;gap:20px;align-items:flex-start;margin-top:24px}.book img{width:150px;border-radius:12px;box-shadow:0 10px 30px rgba(42,27,94,.25)}
.recap{padding:16px;border-radius:16px;background:var(--card);border:1px solid var(--line);margin-bottom:12px}.recap b{color:var(--plum);font-size:14px}
@media (max-width:560px){.book{flex-direction:column;align-items:center;text-align:center}.quote p,.quote h1{font-size:23px}}
</style>"""


def db(sql):
    tok = (pathlib.Path(os.environ['USERPROFILE']) / '.supabase' / 'access-token').read_text().strip()
    req = urllib.request.Request(
        'https://api.supabase.com/v1/projects/jytbowsfvuzdnsmhmsly/database/query',
        data=json.dumps({'query': sql}).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json', 'User-Agent': 'ishraqa-cli'})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


# موضوعات الحِكم: صفحة لكل موضوع /q/t/<slug>/
TOPICS = {
    'الحكمة': 'wisdom', 'التحفيز': 'motivation', 'النجاح': 'success', 'العلم والمعرفة': 'knowledge',
    'الأمل والصبر': 'hope-and-patience', 'الأخلاق': 'ethics', 'القيادة': 'leadership', 'التكنولوجيا': 'technology',
    'أمثال سودانية': 'sudanese-proverbs', 'الذكاء الاصطناعي': 'artificial-intelligence', 'الصداقة': 'friendship',
    'السعادة والرضا': 'happiness', 'الإعلام': 'media', 'الوقت والعمل': 'time-and-work', 'الأم والأسرة': 'family',
}
GENERIC = ('مثل', 'حكمة')   # «مثل عربي»، «مثل سوداني»، «حكمة»: بلا قائل معروف


def topic_slug(cat):
    import hashlib
    return TOPICS.get(cat) or 'topic-' + hashlib.sha1(cat.encode()).hexdigest()[:8]


def topic_h1(cat):
    return f'{cat} مع معانيها' if cat.startswith('أمثال') else f'حكم وأمثال عن {cat}'


def head(title, desc, url, image=f'{SITE}/img/og.jpg', og_type='article'):
    return HEAD.format(title=esc(title), desc=esc(desc), url=url, og_type=og_type,
                       og_title=esc(title), image=esc(image), open_app=PLAY).replace('</head>', EXTRA_CSS + '</head>')


def cta(text, label='حمّل إشراقة يومية مجانًا', href=None):
    href = href or f'{PLAY}&referrer=' + urlquote('utm_source=web&utm_medium=wisdom')
    return f'<div class="cta"><p>{text}</p><a class="btn main" href="{href}">{label}</a></div>'


def short(s, n=150):
    s = ' '.join((s or '').split())
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0] + '…'


def quote_title(q):
    """«الحكمة» معناها وشرحها · إشراقة يومية — في حدود 60 حرفًا، ونقدّم نص الحكمة على اسم الموقع"""
    t = f'«{short(q["quote"], 70)}» معناها وشرحها'
    if len(t + seo.SUFFIX) <= 60:
        return t + seo.SUFFIX
    n = 60 - len('«» معناها وشرحها')
    while n > 10:
        t = f'«{short(q["quote"], n)}» معناها وشرحها'
        if len(t) <= 60:
            return t
        n -= 2
    return t


def quote_page(q, ex, related):
    url = f'{SITE}/q/{q["id"]}/'
    who = q['author'] or 'حكمة'
    cat = q['category']
    turl = f'{SITE}/q/t/{topic_slug(cat)}/'
    title = quote_title(q)
    desc = short(ex['meaning'], 155)
    secs = f'<div class="sec"><h2>المعنى</h2><p>{esc(ex["meaning"])}</p></div>'
    quotation = {'@type': 'Quotation', '@id': url + '#quote', 'text': q['quote'], 'creditText': who,
                 'description': ex['meaning'], 'about': cat, 'genre': 'مثل' if who.startswith('مثل') else 'حكمة',
                 'inLanguage': 'ar', 'url': url, 'isPartOf': {'@id': turl + '#webpage'},
                 'publisher': {'@id': seo.ORG_ID}}
    if not who.startswith(GENERIC):
        quotation['creator'] = {'@type': 'Person', 'name': who.replace('يُنسب إلى ', '').strip()}
    nodes = [seo.webpage(url, title, desc, mainEntity={'@id': url + '#quote'}), quotation,
             seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('الحكم والأمثال', f'{SITE}/q/'), (cat, turl),
                                  (short(q['quote'], 60), url)]),
             seo.org(), seo.website()]
    more = ''.join(f'<a href="/q/{r["id"]}/">{esc(short(r["quote"], 60))}<small>{esc(r["author"] or "")}</small></a>'
                   for r in related)
    page = (head(title, desc, url)
            + '<div class="wrap"><main>'
            + f'<span class="cat"><a href="/q/t/{topic_slug(cat)}/" style="text-decoration:none">{esc(cat)}</a></span>'
            + f'<div class="quote"><h1>«{esc(q["quote"])}»</h1><span>— {esc(who)}</span></div>'
            + secs
            + cta('قصة هذه الحكمة، وكيف تطبّقها في يومك، وحكمة جديدة كل يوم: في تطبيق إشراقة يومية',
                  'اكتشفها في إشراقة')
            + (f'<h2>من {esc(cat)} أيضًا</h2><div class="qlist">{more}</div>' if more else '')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes, og_type='article')


def quotes_index(by_cat):
    chips = ''.join(f'<a href="/q/t/{topic_slug(c)}/">{esc(c)} ({len(v)})</a>' for c, v in by_cat.items())
    body = ''
    for c, items in by_cat.items():
        rows = ''.join(f'<a href="/q/{q["id"]}/">«{esc(short(q["quote"], 90))}»<small>{esc(q["author"] or "")}</small></a>'
                       for q in items)
        body += f'<h2 id="{esc(c)}">{esc(c)}</h2><div class="qlist">{rows}</div>'
    url = f'{SITE}/q/'
    title = 'حكم وأمثال عربية مع معانيها وشرحها' + seo.SUFFIX
    n = sum(len(v) for v in by_cat.values())
    desc = (f'أكثر من {n // 10 * 10} حكمة ومثلًا عربيًا وسودانيًا في {len(by_cat)} موضوعًا، '
            'لكل منها معناها وقصتها وكيف تطبّقها في حياتك اليوم.')
    nodes = [seo.webpage(url, title, desc, 'CollectionPage',
                         hasPart=[{'@id': f'{SITE}/q/t/{topic_slug(c)}/#webpage'} for c in by_cat]),
             seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('الحكم والأمثال', url)]), seo.org(), seo.website()]
    page = (head(title, desc, url, og_type='website')
            + '<div class="wrap"><main><h1>حكم وأمثال مع معانيها</h1>'
            + f'<div class="chips">{chips}</div>{body}'
            + cta('حكمة جديدة كل يوم على هاتفك')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes)


def topic_page(cat, items, by_cat):
    url = f'{SITE}/q/t/{topic_slug(cat)}/'
    h1 = topic_h1(cat)
    title = seo.fit_title(h1 if 'مع معانيها' in h1 else f'{h1} مع معانيها')
    sample = '، و'.join(f'«{short(q["quote"], 40)}»' for q in items[:2])
    if cat.startswith('أمثال'):
        desc = f'{len(items)} من الأمثال السودانية مع معانيها وقصصها، منها {sample}.'
    else:
        desc = f'{len(items)} من الحكم والأمثال عن {cat} مع معانيها وشرحها، منها {sample}.'
    desc = short(desc, 155)
    rows = ''.join(f'<a href="/q/{q["id"]}/">«{esc(short(q["quote"], 90))}»<small>{esc(q["author"] or "")}</small></a>'
                   for q in items)
    chips = ''.join(f'<a href="/q/t/{topic_slug(c)}/">{esc(c)}</a>' for c in by_cat if c != cat)
    nodes = [seo.webpage(url, title, desc, 'CollectionPage', about=cat,
                         mainEntity=seo.item_list([f'{SITE}/q/{q["id"]}/' for q in items])),
             seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('الحكم والأمثال', f'{SITE}/q/'), (cat, url)]),
             seo.org(), seo.website()]
    page = (head(title, desc, url, og_type='website')
            + '<div class="wrap"><main>'
            + '<span class="cat"><a href="/q/" style="text-decoration:none">الحكم والأمثال</a></span>'
            + f'<h1>{esc(h1)}</h1><div class="qlist">{rows}</div>'
            + cta('حكمة جديدة كل يوم على هاتفك، مع قصتها وكيف تطبّقها')
            + f'<h2>موضوعات أخرى</h2><div class="chips">{chips}</div>'
            + '</main></div>' + FOOT.format(year=dt.date.today().year))
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes)


def book_list(books, skip=None):
    return ''.join(f'<a class="item" href="/k/{SLUGS[b["title"]]}/"><img src="{esc(b["cover_url"])}" '
                   f'alt="غلاف كتاب {esc(b["title"])}" width="120" height="78" loading="lazy">'
                   f'<span><b>{esc(b["title"])}</b><small>{esc(b["author"])} · {b["pages"]} صفحة</small></span></a>'
                   for b in books if b['title'] in SLUGS and b['title'] != skip)


def by_author(author):
    """«للجاحظ»، «لابن طفيل»: لام الجر موصولة بالاسم كما تُكتب"""
    return 'لل' + author[2:] if author.startswith('ال') else 'ل' + author


def book_page(b, recaps, books):
    url = f'{SITE}/k/{SLUGS[b["title"]]}/'
    cover = b.get('cover_url') or f'{SITE}/img/og.jpg'
    title = seo.fit_title(f'كتاب {b["title"]} {by_author(b["author"])}: اقرأه مجانًا')
    desc = short(b['description'], 155)
    book = {'@type': 'Book', '@id': url + '#book', 'name': b['title'],
            'author': {'@type': 'Person', 'name': b['author']}, 'description': b['description'], 'inLanguage': 'ar',
            'isAccessibleForFree': True, 'bookFormat': 'https://schema.org/EBook', 'numberOfPages': b['pages'],
            'image': cover, 'url': url, 'isPartOf': {'@id': f'{SITE}/k/#webpage'},
            'potentialAction': {'@type': 'ReadAction', 'target': PLAY}}
    nodes = [seo.webpage(url, title, desc, 'ItemPage', mainEntity={'@id': url + '#book'}), book,
             seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('مكتبة إشراقة', f'{SITE}/k/'), (b['title'], url)]),
             seo.org(), seo.website()]
    others = book_list(books, skip=b['title'])
    page = (head(title, desc, url, image=cover)
            + '<div class="wrap"><main>'
            + f'<div class="book"><img src="{esc(cover)}" alt="غلاف كتاب {esc(b["title"])}" width="600" height="900" fetchpriority="high">'
            + f'<div><h1>{esc(b["title"])}</h1><div class="meta">{esc(b["author"])} · {b["pages"]} صفحة</div>'
            + f'<p style="font-size:18px">{esc(b["description"])}</p></div></div>'
            + cta(f'اقرأ «{esc(b["title"])}» كاملًا مجانًا في إشراقة، وناقشه مع ناديك جزءًا جزءًا',
                  'اقرأه مجانًا في إشراقة')
            + (f'<h2>كتب أخرى في مكتبة إشراقة</h2><div class="list">{others}</div>' if others else '')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes, image=cover,
                        image_alt=f'غلاف كتاب {b["title"]}', og_type='book')


def books_index(books):
    url = f'{SITE}/k/'
    title = 'كتب التراث العربي مجانًا: مكتبة إشراقة' + seo.SUFFIX
    if len(title) > 60:
        title = 'كتب التراث العربي مجانًا · مكتبة إشراقة'
    desc = ('كليلة ودمنة، وطوق الحمامة، وحي بن يقظان، والبخلاء، والنظرات: اقرأها مجانًا بإخراج أنيق، '
            'وناقشها مع نادي القرّاء.')
    nodes = [seo.webpage(url, title, desc, 'CollectionPage', mainEntity=seo.item_list(
                [f'{SITE}/k/{SLUGS[b["title"]]}/' for b in books if b['title'] in SLUGS])),
             seo.breadcrumb(url, [('إشراقة يومية', f'{SITE}/'), ('مكتبة إشراقة', url)]), seo.org(), seo.website()]
    page = (head(title, desc, url, og_type='website')
            + f'<div class="wrap"><main><h1>مكتبة إشراقة</h1><div class="list">{book_list(books)}</div>'
            + cta('اقرأ هذه الكتب مجانًا مع أصحابك في نادي القرّاء')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))
    return seo.finalize(page, url=url, title=title, desc=desc, nodes=nodes)


def main():
    root = pathlib.Path(sys.argv[1])
    quotes = json.load(open(APP / 'assets/data/quotes.json', encoding='utf-8'))
    ex = {r['quote_id']: r for r in db('select quote_id, meaning, story, reflection from public.quote_explanations')}
    by_cat = {}
    for q in quotes:
        by_cat.setdefault(q['category'], []).append(q)

    out = root / 'q'
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    n = 0
    for q in quotes:
        e = ex.get(q['id'])
        if not e:
            continue
        same = [r for r in by_cat[q['category']] if r['id'] != q['id']]
        i = same.index(next(r for r in same if r['id'] > q['id'])) if any(r['id'] > q['id'] for r in same) else 0
        related = (same[i:] + same[:i])[:5]
        d = out / str(q['id'])
        d.mkdir()
        (d / 'index.html').write_text(quote_page(q, e, related), encoding='utf-8')
        n += 1
    (out / 'index.html').write_text(quotes_index(by_cat), encoding='utf-8')
    for c, items in by_cat.items():
        items = [q for q in items if q['id'] in ex]
        if not items:
            continue
        d = out / 't' / topic_slug(c)
        d.mkdir(parents=True)
        (d / 'index.html').write_text(topic_page(c, items, by_cat), encoding='utf-8')

    books = db('select id, title, author, description, pages, cover_url from public.books')
    kout = root / 'k'
    if kout.exists():
        shutil.rmtree(kout)
    kout.mkdir()
    for b in books:
        if b['title'] not in SLUGS:
            continue
        recaps = db("select from_page, to_page, recap from public.book_recaps where book_id = '%s' "
                    "and recap <> 'صفحات تمهيدية' order by from_page limit 2" % b['id'])
        d = kout / SLUGS[b['title']]
        d.mkdir()
        (d / 'index.html').write_text(book_page(b, recaps, books), encoding='utf-8')
    (kout / 'index.html').write_text(books_index(books), encoding='utf-8')
    seo.write_sitemap(root)
    seo.write_llms(root)
    print(f'{n} quote pages, {len(by_cat)} topic pages, {len(SLUGS)} book pages')


if __name__ == '__main__':
    main()
