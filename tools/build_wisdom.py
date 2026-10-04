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
from build_articles import FOOT, HEAD, PLAY, SITE, esc  # noqa: E402

APP = pathlib.Path(__file__).resolve().parents[2]
SLUGS = {
    'كليلة ودمنة': 'kalila-wa-dimna', 'طوق الحمامة': 'tawq-al-hamama',
    'حي بن يقظان': 'hayy-ibn-yaqzan', 'البخلاء': 'al-bukhala', 'النظرات': 'al-nazarat',
}
EXTRA_CSS = """<style>
.quote{margin:26px 0 8px;padding:28px 24px;border-radius:26px;background:linear-gradient(140deg,var(--night),var(--plum) 62%,var(--sun));color:#fff;text-align:center}
.quote p{font-size:27px;line-height:1.7;margin:0 0 10px;font-weight:700}.quote span{color:#FFD27A;font-size:16px}
.sec h2{font-size:21px;margin:26px 0 6px}.sec p{font-size:18px;margin:0}
.apply{margin-top:22px;padding:18px;border-radius:18px;background:#FFF1E6;color:#5A2410}.apply h2{margin-top:0}
.chips a{display:inline-block;margin:0 0 10px 8px;padding:6px 14px;border-radius:20px;background:var(--card);border:1px solid var(--line);text-decoration:none;font-size:15px}
.qlist a{display:block;text-decoration:none;padding:14px 16px;border-radius:16px;background:var(--card);border:1px solid var(--line);margin-bottom:10px}
.qlist small{display:block;color:var(--muted)}
.book{display:flex;gap:20px;align-items:flex-start;margin-top:24px}.book img{width:150px;border-radius:12px;box-shadow:0 10px 30px rgba(42,27,94,.25)}
.recap{padding:16px;border-radius:16px;background:var(--card);border:1px solid var(--line);margin-bottom:12px}.recap b{color:var(--plum);font-size:14px}
@media (max-width:560px){.book{flex-direction:column;align-items:center;text-align:center}.quote p{font-size:23px}}
</style>"""


def db(sql):
    tok = (pathlib.Path(os.environ['USERPROFILE']) / '.supabase' / 'access-token').read_text().strip()
    req = urllib.request.Request(
        'https://api.supabase.com/v1/projects/jytbowsfvuzdnsmhmsly/database/query',
        data=json.dumps({'query': sql}).encode(), method='POST',
        headers={'Authorization': 'Bearer ' + tok, 'Content-Type': 'application/json', 'User-Agent': 'ishraqa-cli'})
    return json.loads(urllib.request.urlopen(req, timeout=120).read())


def head(title, desc, url, image=f'{SITE}/img/og.jpg', og_type='article'):
    return HEAD.format(title=esc(title), desc=esc(desc), url=url, og_type=og_type,
                       og_title=esc(title), image=esc(image), open_app=PLAY).replace('</head>', EXTRA_CSS + '</head>')


def cta(text):
    return f'<div class="cta"><p>{text}</p><a class="btn main" href="{PLAY}">حمّل إشراقة يومية مجانًا</a></div>'


def short(s, n=150):
    s = ' '.join((s or '').split())
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0] + '…'


def quote_page(q, ex, related):
    url = f'{SITE}/q/{q["id"]}/'
    who = q['author'] or 'حكمة'
    title = f'«{short(q["quote"], 70)}» معناها وشرحها'
    secs = f'<div class="sec"><h2>المعنى</h2><p>{esc(ex["meaning"])}</p></div>'
    if ex.get('story'):
        secs += f'<div class="sec"><h2>القصة والسياق</h2><p>{esc(ex["story"])}</p></div>'
    secs += f'<div class="sec apply"><h2>كيف أطبّقها اليوم؟</h2><p>{esc(ex["reflection"])}</p></div>'
    more = ''.join(f'<a href="/q/{r["id"]}/">{esc(short(r["quote"], 60))}<small>{esc(r["author"] or "")}</small></a>'
                   for r in related)
    return (head(title + ' · إشراقة يومية', short(ex['meaning'], 155), url)
            + '<div class="wrap"><main>'
            + f'<span class="cat"><a href="/q/#{esc(q["category"])}" style="text-decoration:none">{esc(q["category"])}</a></span>'
            + f'<div class="quote"><p>«{esc(q["quote"])}»</p><span>— {esc(who)}</span></div>'
            + secs
            + cta('حكمة جديدة كل صباح، مع معناها وكيف تطبّقها، في تطبيق إشراقة يومية')
            + (f'<h2>من {esc(q["category"])} أيضًا</h2><div class="qlist">{more}</div>' if more else '')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))


def quotes_index(by_cat):
    chips = ''.join(f'<a href="#{esc(c)}">{esc(c)} ({len(v)})</a>' for c, v in by_cat.items())
    body = ''
    for c, items in by_cat.items():
        rows = ''.join(f'<a href="/q/{q["id"]}/">«{esc(short(q["quote"], 90))}»<small>{esc(q["author"] or "")}</small></a>'
                       for q in items)
        body += f'<h2 id="{esc(c)}">{esc(c)}</h2><div class="qlist">{rows}</div>'
    return (head('حكم وأمثال عربية مع معانيها وشرحها · إشراقة يومية',
                 'أكثر من 270 حكمة ومثلًا عربيًا وسودانيًا، لكل منها معناها وقصتها وكيف تطبّقها في حياتك اليوم.',
                 f'{SITE}/q/', og_type='website')
            + '<div class="wrap"><main><h1>حكم وأمثال مع معانيها</h1>'
            + f'<div class="chips">{chips}</div>{body}'
            + cta('حكمة كل صباح على هاتفك')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))


def book_page(b, recaps):
    slug = SLUGS[b['title']]
    url = f'{SITE}/k/{slug}/'
    rec = ''.join(f'<div class="recap"><b>الصفحات {r["from_page"]}–{r["to_page"]}</b><p>{esc(r["recap"])}</p></div>'
                  for r in recaps)
    return (head(f'كتاب {b["title"]} لـ{b["author"]}: اقرأه مجانًا · إشراقة يومية', short(b['description'], 155),
                 url, image=b.get('cover_url') or f'{SITE}/img/og.jpg')
            + '<div class="wrap"><main>'
            + f'<div class="book"><img src="{esc(b["cover_url"])}" alt="غلاف {esc(b["title"])}">'
            + f'<div><h1>{esc(b["title"])}</h1><div class="meta">{esc(b["author"])} · {b["pages"]} صفحة</div>'
            + f'<p style="font-size:18px">{esc(b["description"])}</p></div></div>'
            + (f'<h2>من بداية الكتاب</h2>{rec}' if rec else '')
            + cta(f'اقرأ «{esc(b["title"])}» كاملًا مجانًا في إشراقة، وناقشه مع ناديك جزءًا جزءًا')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))


def books_index(books):
    rows = ''.join(f'<a class="item" href="/k/{SLUGS[b["title"]]}/"><img src="{esc(b["cover_url"])}" alt="" loading="lazy">'
                   f'<span><b>{esc(b["title"])}</b><small>{esc(b["author"])} · {b["pages"]} صفحة</small></span></a>'
                   for b in books if b['title'] in SLUGS)
    return (head('كتب التراث العربي مجانًا · إشراقة يومية',
                 'كليلة ودمنة، وطوق الحمامة، وحي بن يقظان، والبخلاء، والنظرات: اقرأها مجانًا بإخراج أنيق.',
                 f'{SITE}/k/', og_type='website')
            + f'<div class="wrap"><main><h1>مكتبة إشراقة</h1><div class="list">{rows}</div>'
            + cta('اقرأ هذه الكتب مجانًا مع أصحابك في نادي القرّاء')
            + '</main></div>' + FOOT.format(year=dt.date.today().year))


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
        (d / 'index.html').write_text(book_page(b, recaps), encoding='utf-8')
    (kout / 'index.html').write_text(books_index(books), encoding='utf-8')
    print(f'{n} quote pages, {len(SLUGS)} book pages')


if __name__ == '__main__':
    main()
