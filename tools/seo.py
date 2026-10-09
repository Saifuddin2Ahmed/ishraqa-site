"""أدوات الظهور في محركات البحث وإجابات الذكاء الاصطناعي، مشتركة بين كل مولّدات الموقع.

- finalize(): يكتب رأس الصفحة كله من جديد (العنوان والوصف والرابط الأصلي وhreflang وOpen Graph وبطاقة X
  والبيانات المنظّمة JSON-LD) ويضيف أبعاد الصور المحلية، فيمكن تمريره على صفحة مرة بعد مرة بلا تكرار.
- write_sitemap(): خريطة الموقع كاملة من الصفحات القابلة للفهرسة، مع lastmod يتغيّر فقط حين يتغيّر محتوى الصفحة.
- write_llms(): ملف llms.txt المختصر لمحركات الذكاء الاصطناعي.

يعمل بلا مكتبات خارجية (في GitHub Actions)، ويستعمل Pillow لأبعاد الصور إن وُجدت.
    python tools/seo.py <مجلد مستودع الموقع>      # يحدّث الخريطة وllms.txt فقط
"""
import datetime as dt
import hashlib
import html
import json
import pathlib
import re
import subprocess
import sys
from urllib.parse import urljoin

SITE = 'https://ishraqa.otwox.com'
PLAY = 'https://play.google.com/store/apps/details?id=com.taeziz.ishraqa'
DEV_PLAY = 'https://play.google.com/store/apps/dev?id=6759566582761793518'
APP_NAME = 'إشراقة يومية'
SUFFIX = ' · إشراقة يومية'
OG_IMAGE = SITE + '/img/og.jpg'
OG_ALT = 'شخص يقرأ كتابًا أمام شروق الشمس'

ORG_ID = 'https://otwox.com/#organization'
WEBSITE_ID = SITE + '/#website'
APP_ID = SITE + '/#app'
FOUNDER_ID = SITE + '/about/#founder'

APP_DESC = ('تطبيق مجاني بلا إعلانات للقراءة والمعرفة: حكمة أو مثل مع معناه وقصته، ومقال قصير موثّق، '
            'وكتب تقرؤها مع نادي القرّاء جزءًا جزءًا، وتحديات قراءة بين المدن والجامعات والمدارس، ونوادي بناء للمطوّرين.')

# أبعاد صور /img/ (احتياطًا حين لا تتوفر Pillow، كما في GitHub Actions)
IMG_DIMS = {
    'icon-192.png': (192, 192), 'icon-512.png': (512, 512), 'developer.jpg': (240, 240),
    'og.jpg': (1200, 630), 'og.png': (1200, 630),
}
PHONE_SHOT = (540, 1134)


# ───────────── عُقد البيانات المنظّمة ─────────────

def org():
    return {'@type': 'Organization', '@id': ORG_ID, 'name': 'أوتواكس للحلول الرقمية',
            'alternateName': 'OtwoX Digital Solutions', 'url': 'https://otwox.com',
            'founder': {'@type': 'Person', '@id': FOUNDER_ID, 'name': 'م. سيف الدين أحمد'}}


def website():
    return {'@type': 'WebSite', '@id': WEBSITE_ID, 'url': SITE + '/', 'name': APP_NAME,
            'alternateName': ['إشراقة', 'Ishraqa Daily'], 'inLanguage': 'ar', 'publisher': {'@id': ORG_ID}}


def app():
    return {'@type': 'MobileApplication', '@id': APP_ID, 'name': APP_NAME, 'alternateName': 'Ishraqa Daily',
            'description': APP_DESC, 'operatingSystem': 'Android', 'applicationCategory': 'EducationalApplication',
            'applicationSubCategory': 'القراءة والمعرفة', 'inLanguage': 'ar', 'isAccessibleForFree': True,
            'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
            'url': SITE + '/', 'installUrl': PLAY, 'downloadUrl': PLAY, 'image': SITE + '/img/icon-512.png',
            'screenshot': [f'{SITE}/img/{n}.webp' for n in ('home', 'club', 'club4', 'community', 'library')],
            'featureList': ['حكمة أو مثل مع معناه وقصته', 'مقال قصير موثّق بخلاصة عملية', 'نادي القرّاء',
                            'لقاءات وفعاليات', 'تحدي المدن والجامعات والمدارس', 'نوادي المطوّرين للمطوّرين',
                            'مكتبة كتب مجانية', 'يعمل دون إنترنت', 'بلا إعلانات'],
            'author': {'@type': 'Person', '@id': FOUNDER_ID, 'name': 'م. سيف الدين أحمد'}, 'publisher': {'@id': ORG_ID}}


def founder(full=False):
    p = {'@type': 'Person', '@id': FOUNDER_ID, 'name': 'م. سيف الدين أحمد', 'url': SITE + '/about/',
         'jobTitle': 'مؤسس أوتواكس للحلول الرقمية', 'worksFor': {'@id': ORG_ID}}
    if full:
        p.update({'alternateName': ['سيف الدين أحمد', 'Saifuddin Ahmed', 'Eng. Saifuddin Ahmed'],
                  'image': SITE + '/img/developer.jpg',
                  'sameAs': [DEV_PLAY, 'https://www.linkedin.com/in/saifuddin2ahmed', 'https://github.com/Saifuddin2Ahmed',
                             'https://www.facebook.com/Saifuddin2Ahmed', 'https://huggingface.co/saifuddin2ahmed',
                             'https://otwox.com/about-us/founder']})
    return p


def breadcrumb(url, items):
    """items: [(الاسم, الرابط), ...] من الرئيسية إلى الصفحة نفسها"""
    return {'@type': 'BreadcrumbList', '@id': url + '#breadcrumb', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': u} for i, (n, u) in enumerate(items)]}


def webpage(url, name, desc, kind='WebPage', lang='ar', crumbs=True, **extra):
    n = {'@type': kind, '@id': url + '#webpage', 'url': url, 'name': name, 'description': desc,
         'inLanguage': lang, 'isPartOf': {'@id': WEBSITE_ID}}
    if crumbs:
        n['breadcrumb'] = {'@id': url + '#breadcrumb'}
    n.update(extra)
    return n


def item_list(urls):
    return {'@type': 'ItemList', 'numberOfItems': len(urls),
            'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'url': u} for i, u in enumerate(urls)]}


def script(nodes):
    data = json.dumps({'@context': 'https://schema.org', '@graph': list(nodes)}, ensure_ascii=False,
                      separators=(',', ':'))
    return '<script type="application/ld+json">' + data.replace('</', '<\\/') + '</script>'


# ───────────── نصوص الرأس ─────────────

def clip(s, n):
    s = ' '.join((s or '').split())
    return s if len(s) <= n else s[:n - 1].rsplit(' ', 1)[0].rstrip('،,:؛') + '…'


def fit_title(main, suffix=SUFFIX, limit=60):
    main = ' '.join(main.split())
    if len(main) + len(suffix) <= limit:
        return main + suffix
    return clip(main, limit)


def esc(s):
    return html.escape(s or '', quote=True)


_STRIP = [
    r'\s*<!-- معاينة الرابط[^>]*-->',
    r'\s*<meta name="description"[^>]*>',
    r'\s*<meta name="robots" content="max-image-preview[^"]*">',
    r'\s*<meta (?:property|name)="(?:og|twitter|article):[^"]*"[^>]*>',
    r'\s*<link rel="canonical"[^>]*>',
    r'\s*<link rel="alternate" hreflang="[^"]*"[^>]*>',
    r'\s*<script type="application/ld\+json">.*?</script>',
    r'<style>:where\(img\[width\]\[height\]\)\{height:auto\}</style>',
]


def finalize(doc, *, url, title, desc, nodes=(), lang='ar', image=OG_IMAGE, image_alt=None, og_type='website',
             alternates=None, article=None, root=None):
    """يعيد كتابة رأس الصفحة لمحركات البحث. alternates: {'ar': رابط, 'en': رابط} لصفحات لها نسختان.
    article: {'published': ..., 'modified': ..., 'section': ...} لصفحات المقالات."""
    for pat in _STRIP:
        doc = re.sub(pat, '', doc, flags=re.S)
    doc = re.sub(r'<title>.*?</title>', lambda _: f'<title>{esc(title)}</title>', doc, count=1, flags=re.S)
    locale = 'ar_AR' if lang == 'ar' else 'en_US'
    if image == OG_IMAGE:
        image_alt = image_alt or (OG_ALT if lang == 'ar' else 'A person reading a book at sunrise')
    m = [f'<meta name="description" content="{esc(desc)}">',
         '<meta name="robots" content="max-image-preview:large">',
         f'<link rel="canonical" href="{url}">']
    if alternates:
        m += [f'<link rel="alternate" hreflang="{k}" href="{v}">' for k, v in alternates.items()]
        m.append(f'<link rel="alternate" hreflang="x-default" href="{alternates.get("ar", url)}">')
    m += [f'<meta property="og:type" content="{og_type}">',
          f'<meta property="og:site_name" content="{APP_NAME if lang == "ar" else "Ishraqa"}">',
          f'<meta property="og:locale" content="{locale}">']
    if alternates:
        m += [f'<meta property="og:locale:alternate" content="{"en_US" if k == "en" else "ar_AR"}">'
              for k in alternates if k != lang]
    m += [f'<meta property="og:url" content="{url}">',
          f'<meta property="og:title" content="{esc(title)}">',
          f'<meta property="og:description" content="{esc(desc)}">',
          f'<meta property="og:image" content="{esc(image)}">']
    if image == OG_IMAGE:
        m += ['<meta property="og:image:type" content="image/jpeg">',
              '<meta property="og:image:width" content="1200">', '<meta property="og:image:height" content="630">']
    if image_alt:
        m.append(f'<meta property="og:image:alt" content="{esc(image_alt)}">')
    if article:
        for k in ('published', 'modified'):
            if article.get(k):
                m.append(f'<meta property="article:{k}_time" content="{article[k]}">')
        if article.get('section'):
            m.append(f'<meta property="article:section" content="{esc(article["section"])}">')
    m += ['<meta name="twitter:card" content="summary_large_image">',
          f'<meta name="twitter:title" content="{esc(title)}">',
          f'<meta name="twitter:description" content="{esc(desc)}">',
          f'<meta name="twitter:image" content="{esc(image)}">']
    if image_alt:
        m.append(f'<meta name="twitter:image:alt" content="{esc(image_alt)}">')
    if nodes:
        m.append(script(nodes))
    doc = doc.replace('</title>', '</title>\n' + '\n'.join(m), 1)
    doc, sized = size_images(doc, url, root)
    if sized:
        doc = doc.replace('</head>', '<style>:where(img[width][height]){height:auto}</style></head>', 1)
    # أيقونتا آيفون والحاسوب بجانب زر Google Play (ما عدا المختبرين والكِت؛ platforms.js يتجاهل الرئيسية أيضًا)
    if 'platforms.js' not in doc and '/testers/' not in url and '/kit/' not in url and '/a/' not in url and '</body>' in doc:
        doc = doc.replace('</body>', '<script src="/platforms.js" defer></script>\n</body>', 1)
    return re.sub(r'\n{3,}', '\n\n', doc)


def _dims(src, page_url, root):
    if src.startswith(('data:', 'http')) and not src.startswith(SITE):
        return None
    path = urljoin(page_url, src).replace(SITE, '').split('?')[0]
    name = path.rsplit('/', 1)[-1]
    if root is not None:
        f = pathlib.Path(root) / path.lstrip('/')
        if f.is_file():
            try:
                from PIL import Image
                with Image.open(f) as im:
                    return im.size
            except Exception:
                pass
    if path.startswith('/img/'):
        return IMG_DIMS.get(name) or (PHONE_SHOT if name.endswith('.webp') else None)
    return None


def size_images(doc, page_url, root=None):
    """يضيف width/height (النسبة الأصلية) لكل صورة محلية بلا أبعاد، فلا تقفز الصفحة عند التحميل"""
    n = 0

    def fix(m):
        nonlocal n
        tag = m.group(0)
        if ' width=' in tag:
            return tag
        src = re.search(r'src="([^"]+)"', tag)
        d = src and _dims(src.group(1), page_url, root)
        if not d:
            return tag
        n += 1
        return tag[:4] + f' width="{d[0]}" height="{d[1]}"' + tag[4:]
    doc = re.sub(r'<img\s[^>]*>', fix, doc)
    return doc, bool(re.search(r'<img\b[^>]*\swidth=', doc))


# ───────────── الصفحات الثابتة (غير المولّدة يوميًا) ─────────────

def _crumbs(url, name):
    return breadcrumb(url, [(APP_NAME, SITE + '/'), (name, url)])


def static_page(path):
    """إعدادات رأس الصفحات الثابتة: (العنوان، الوصف، العُقد)؛ path مثل '' أو 'about'"""
    url = f'{SITE}/{path}/' if path else SITE + '/'
    if path == '':
        t = 'إشراقة يومية · بوتقةٌ للمعرفة وفضاءٌ للقراءة'
        d = 'إشراقة — بوتقةٌ للمعرفة، وفضاءٌ للقراءة. تطبيق مجاني بلا إعلانات: حكمة مع معناها، ومقال يومي، وكتب تقرؤها مع نادي القرّاء.'
        return t, d, [webpage(url, t, d, crumbs=False, about={'@id': APP_ID}, mainEntity={'@id': APP_ID}),
                      website(), org(), app(), founder()]
    if path == 'about':
        t = 'عن إشراقة يومية: القصة والمبادئ والمطوّر'
        d = 'إشراقة: أن نرى أبعد، كلما عرفنا أكثر. قصة إشراقة يومية ومبادئها ومسيرتها، ومطوّرها م. سيف الدين أحمد.'
        return t, d, [webpage(url, t, d, 'AboutPage', about={'@id': APP_ID}, mainEntity={'@id': FOUNDER_ID}),
                      _crumbs(url, 'عن إشراقة'), founder(full=True), app(), org(), website()]
    if path == 'developers':
        t = 'نوادي المطوّرين للمطوّرين' + SUFFIX
        d = 'فريق صغير، ومرشد خبير، ومشروع مفتوح المصدر يراه العالم. نوادي المطوّرين في إشراقة يومية للمطوّرين والمطوّرات مجانًا.'
        return t, d, [webpage(url, t, d, about={'@id': APP_ID}), _crumbs(url, 'للمطوّرين'), app(), org(), website()]
    if path == 'wallpapers':
        t = 'خلفيات إشراقة: سمات ويندوز ولوحات للهاتف'
        d = 'سمتا ويندوز من إشراقة يومية تتبدّل وحدها، ولوحات 4K للحاسوب والهاتف بلا أي كتابة، مجانًا.'
        return t, d, [webpage(url, t, d, 'CollectionPage', isAccessibleForFree=True), _crumbs(url, 'خلفيات إشراقة'),
                      org(), website()]
    if path == 'testers':
        t = 'كن من روّاد إشراقة: سجّل مختبرًا' + SUFFIX
        d = 'سجّل مختبرًا لإشراقة يومية: لا تحتاج أن تكون مبرمجًا. 14 يومًا تجعلك من روّاد إشراقة بشارة خاصة وحساب موثّق.'
        return t, d, [webpage(url, t, d, about={'@id': APP_ID}), _crumbs(url, 'كن مختبرًا'), app(), org(), website()]
    raise KeyError(path)


def finalize_static(doc, path, root=None):
    t, d, nodes = static_page(path)
    url = f'{SITE}/{path}/' if path else SITE + '/'
    return finalize(doc, url=url, title=t, desc=d, nodes=nodes, root=root)


# ───────────── خريطة الموقع وllms.txt ─────────────

def _git_date(root, f):
    try:
        if subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', str(f)], cwd=root).returncode != 0:
            return None
        out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', str(f)], cwd=root,
                             capture_output=True, text=True).stdout.strip()
        return out or None
    except Exception:
        return None


def pages(root):
    """كل الصفحات القابلة للفهرسة: لها رابط أصلي يطابق مسارها، وليست noindex، وليست /app/"""
    root = pathlib.Path(root)
    out = []
    for f in sorted(root.rglob('index.html')):
        rel = f.parent.relative_to(root).as_posix()
        if rel.split('/')[0] in ('.git', 'app', 'tools', 'node_modules'):
            continue
        s = f.read_text(encoding='utf-8')
        if re.search(r'<meta name="robots" content="[^"]*noindex', s):
            continue
        url = SITE + '/' + ('' if rel == '.' else rel + '/')
        can = re.search(r'<link rel="canonical" href="([^"]+)"', s)
        if not can or can.group(1) != url:
            continue
        out.append((url, f, s))
    return out


def _order(url):
    path = url[len(SITE):]
    top = ['/', '/about/', '/a/', '/q/', '/k/', '/developers/', '/testers/', '/wallpapers/']
    if path in top:
        return (0, top.index(path), '')
    sect = {'a': 1, 'k': 2, 'q': 3}.get(path.strip('/').split('/')[0], 4)
    key = path
    m = re.fullmatch(r'/q/(\d+)/', path)
    if m:
        key = f'/q/{int(m.group(1)):06d}/'
    return (sect, 0, key)


def write_sitemap(root, today=None):
    root = pathlib.Path(root)
    today = today or dt.date.today().isoformat()
    store = root / 'tools' / '.lastmod.json'
    seen = json.loads(store.read_text(encoding='utf-8')) if store.exists() else {}
    rows, fresh = [], {}
    for url, f, s in sorted(pages(root), key=lambda r: _order(r[0])):
        h = hashlib.sha1(re.sub(r'© ?\d{4}', '©', s).encode()).hexdigest()[:16]
        old = seen.get(url)
        if old and old[0] == h:
            date = old[1]
        elif old:
            date = today
        else:
            date = _git_date(root, f) or today
        fresh[url] = [h, date]
        alts = re.findall(r'<link rel="alternate" hreflang="([^"]+)" href="([^"]+)">', s)
        img = re.search(r'<meta property="og:image" content="([^"]+)"', s)
        rows.append((url, date, alts, img.group(1) if img and img.group(1) != OG_IMAGE else None))
    store.write_text(json.dumps(fresh, ensure_ascii=False, indent=0, sort_keys=True), encoding='utf-8')
    xml = ['<?xml version="1.0" encoding="UTF-8"?>',
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml" '
           'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for url, date, alts, img in rows:
        x = f'<url><loc>{url}</loc><lastmod>{date}</lastmod>'
        x += ''.join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{html.escape(u)}"/>' for l, u in alts)
        if img:
            x += f'<image:image><image:loc>{html.escape(img)}</image:loc></image:image>'
        xml.append(x + '</url>')
    xml.append('</urlset>')
    (root / 'sitemap.xml').write_text('\n'.join(xml) + '\n', encoding='utf-8')
    return rows


def _meta(s):
    t = re.search(r'<title>(.*?)</title>', s, re.S)
    d = re.search(r'<meta name="description" content="([^"]*)"', s)
    t = html.unescape(t.group(1)).strip() if t else ''
    for suf in (SUFFIX, ' · Ishraqa'):
        if t.endswith(suf):
            t = t[:-len(suf)]
    return t, html.unescape(d.group(1)) if d else ''


def write_llms(root):
    root = pathlib.Path(root)
    found = {url[len(SITE):]: (f, s) for url, f, s in pages(root)}

    def line(path, name=None):
        if path not in found:
            return ''
        t, d = _meta(found[path][1])
        return f'- [{name or t}]({SITE}{path}): {d}\n'

    arts = []
    for path, (f, s) in found.items():
        if re.fullmatch(r'/a/[^/]+/', path):
            date = re.search(r'"datePublished":"([^"]+)"', s)
            arts.append((date.group(1) if date else '', path))
    arts.sort(reverse=True)
    topics = sorted(p for p in found if p.startswith('/q/t/'))
    books = sorted(p for p in found if re.fullmatch(r'/k/[^/]+/', p))
    out = (f'# {APP_NAME}\n\n'
           f'> {APP_NAME}: {APP_DESC} يعمل على أندرويد، ومتاح على Google Play.\n\n'
           f'- التحميل: [{APP_NAME} على Google Play]({PLAY})\n'
           '- السعر: مجاني بالكامل، بلا إعلانات ولا بيع للبيانات\n'
           f'- المطوّر: [م. سيف الدين أحمد]({SITE}/about/)، مؤسس أوتواكس للحلول الرقمية\n'
           '- الناشر: [أوتواكس للحلول الرقمية](https://otwox.com)\n'
           '- العبارة: من ذاكرة الماضي إلى احتمالات المستقبل\n\n'
           '## صفحات أساسية\n\n'
           + line('/', 'الصفحة الرئيسية') + line('/about/') + line('/developers/') + line('/testers/')
           + line('/wallpapers/') + line('/a/', 'مقالات إشراقة') + line('/q/', 'الحكم والأمثال مع معانيها')
           + line('/k/', 'مكتبة إشراقة')
           + '\n## أحدث المقالات\n\n' + ''.join(line(p) for _, p in arts[:15])
           + '\n## الكتب\n\n' + ''.join(line(p) for p in books)
           + ('\n## موضوعات الحكم والأمثال\n\n' + ''.join(line(p) for p in topics) if topics else '')
           + '\n## السياسات والمساعدة\n\n'
           + line('/privacy/') + line('/terms/') + line('/delete-account/') + line('/contact/'))
    (root / 'llms.txt').write_text(out, encoding='utf-8')
    return out


STATIC = ('', 'about', 'developers', 'wallpapers', 'testers')


def refresh_static(root):
    """يحدّث رأس الصفحات الثابتة في مكانها دون إعادة توليدها (الرئيسية تُحرَّر يدويًا)"""
    root = pathlib.Path(root)
    for path in STATIC:
        f = root / path / 'index.html' if path else root / 'index.html'
        if f.exists():
            s = f.read_text(encoding='utf-8')
            f.write_text(finalize_static(s, path, root), encoding='utf-8', newline='')


if __name__ == '__main__':
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    r = pathlib.Path(args[0] if args else pathlib.Path(__file__).resolve().parents[1])
    if '--static' in sys.argv:
        refresh_static(r)
    print(len(write_sitemap(r)), 'urls in sitemap')
    write_llms(r)
