"""ينشئ نسخة إنجليزية من صفحة ثابتة بالتصميم نفسه: يستخرج كل نص عربي (نصوص، وسمات، ونصوص السكربتات)
ويترجمه دفعة واحدة، ثم يقلب اتجاه الصفحة ويضبط الرأس والشريط والتذييل.

    python tools/translate_page_en.py about developers
"""
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_footer  # noqa: E402
import site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
AR = re.compile(r'[؀-ۿ]')
KEY = (Path.home() / '.anthropic' / 'api-key').read_text().strip()

GUIDE = """You translate the Arabic website of the app «إشراقة يومية» into natural, polished English for a global audience.
Rules:
- App name: «إشراقة يومية» = "Ishraqa Daily"; «إشراقة» alone = "Ishraqa". «صدى» = "Echo". «نادي القرّاء» = "Readers' Club".
- Founder: «م. سيف الدين أحمد» = "Eng. Saifuddin Ahmed"; «سيف الدين أحمد عبدالقادر حامد» = "Saifuddin Ahmed Abdelgadir Hamed". «أوتواكس للحلول الرقمية» = "OtwoX Digital Solutions".
- «تطوير سيف الدين أحمد» = "Developed by Saifuddin Ahmed".
- Never use the words: truly, real, genuine, free (as price), every morning, Arab/Arabic (as audience label). «كود» = "code".
- Keep the tone calm, confident and concise; keep short headings short. Do not add or drop meaning, numbers or names.
- Keep any HTML entities, placeholders, emoji, punctuation like · and line structure. If a string mixes Arabic with Latin/code, translate only the Arabic.
- City/university/place names: use their common English names.
Return ONLY a JSON object mapping each input id to its English string."""


FIXES = [('</a> And choose', '</a> and choose'), ('>Open sources<', '>Open source<'),
         ('>Communities Challenge<', '>Cities Challenge<'),
         # المسيرة الأفقية تتحرك يسارًا في الإنجليزية
         ("tr.style.setProperty('--x',(p*max)", "tr.style.setProperty('--x',(-p*max)")]


def ask(batch):
    body = {'model': 'claude-sonnet-5-5', 'max_tokens': 16000, 'system': GUIDE,
            'messages': [{'role': 'user', 'content': json.dumps(batch, ensure_ascii=False)}]}
    req = urllib.request.Request('https://api.anthropic.com/v1/messages', json.dumps(body).encode(),
                                 {'x-api-key': KEY, 'anthropic-version': '2023-06-01',
                                  'content-type': 'application/json'})
    r = json.load(urllib.request.urlopen(req, timeout=600))
    txt = ''.join(b.get('text', '') for b in r['content'] if b.get('type') == 'text')
    return json.loads(txt[txt.index('{'):txt.rindex('}') + 1])


def segments(s):
    """كل المقاطع العربية: نصوص بين الوسوم، وقيم السمات، والسلاسل داخل السكربتات"""
    out = set()
    parts = re.split(r'(<script\b[^>]*>[\s\S]*?</script>|<style\b[^>]*>[\s\S]*?</style>)', s)
    for p in parts:
        if p.startswith('<style'):
            continue
        if p.startswith('<script'):
            for m in re.finditer(r'"((?:[^"\\]|\\.)*)"|\'((?:[^\'\\]|\\.)*)\'', p):
                v = m.group(1) if m.group(1) is not None else m.group(2)
                if AR.search(v):
                    out.add(v)
            continue
        for m in re.finditer(r'>([^<]+)<', p):
            v = m.group(1).strip()
            if AR.search(v):
                out.add(v)
        for m in re.finditer(r'\s[\w:-]+="([^"]*)"', p):
            if AR.search(m.group(1)):
                out.add(m.group(1))
    return sorted(out, key=len, reverse=True)


def translate(segs, cache):
    todo = [x for x in segs if x not in cache]
    for i in range(0, len(todo), 60):
        chunk = todo[i:i + 60]
        res = ask({str(j): t for j, t in enumerate(chunk)})
        for j, t in enumerate(chunk):
            cache[t] = res[str(j)]
        print(f'  translated {min(i + 60, len(todo))}/{len(todo)}')
    return cache


def build(name):
    src = (ROOT / name / 'index.html').read_text(encoding='utf-8')
    cache_f = ROOT / 'tools' / f'.en_{name}.json'
    cache = json.loads(cache_f.read_text(encoding='utf-8')) if cache_f.exists() else {}
    segs = segments(src)
    print(name, len(segs), 'segments')
    translate(segs, cache)
    cache_f.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding='utf-8')

    s = src
    # استبدال آمن: الأطول أولًا، داخل حدود النص/السمة/السلسلة
    for ar in segs:
        en = cache[ar]
        s = s.replace('>' + ar + '<', '>' + en + '<')
        s = re.sub(r'>(\s*)' + re.escape(ar) + r'(\s*)<', lambda m: '>' + m.group(1) + en + m.group(2) + '<', s)
        s = s.replace('="' + ar + '"', '="' + en.replace('"', '&quot;') + '"')
        s = s.replace('"' + ar + '"', json.dumps(en, ensure_ascii=False)[1:-1].join('""'))
        s = s.replace("'" + ar + "'", "'" + en.replace("'", "\\'") + "'")
    s = s.replace('<html lang="ar" dir="rtl">', '<html lang="en" dir="ltr">')
    s = s.replace('transform-origin:right', 'transform-origin:left')
    s = s.replace('"inLanguage":"ar"', '"inLanguage":"en"').replace('content="ar_AR"', 'content="en_US"')
    url_ar, url_en = f'https://ishraqa.app/{name}/', f'https://ishraqa.app/en/{name}/'
    s = s.replace(f'<link rel="canonical" href="{url_ar}">',
                  f'<link rel="canonical" href="{url_en}">\n'
                  f'<link rel="alternate" hreflang="ar" href="{url_ar}">\n'
                  f'<link rel="alternate" hreflang="en" href="{url_en}">\n'
                  f'<link rel="alternate" hreflang="x-default" href="{url_ar}">')
    s = s.replace(f'content="{url_ar}"', f'content="{url_en}"').replace(f'"url":"{url_ar}"', f'"url":"{url_en}"')
    s = s.replace(f'"@id":"{url_ar}#', f'"@id":"{url_en}#').replace('"item":"https://ishraqa.app/"', '"item":"https://ishraqa.app/en/"')
    s = s.replace(f'"item":"{url_ar}"', f'"item":"{url_en}"')
    # لقطات الهاتف من نسخة التطبيق الإنجليزية
    shots = {'culture': ('en-home', 'Your day'), 'explain': ('en-phenomenon', 'Phenomenon of the day'),
             'community': ('en-library', 'Library'), 'grandma': ('en-book', 'A book to read')}
    for ar_img, (en_img, cap) in shots.items():
        s = re.sub(r'src="/img/' + ar_img + r'\.webp" alt="[^"]*" data-cap="[^"]*"',
                   f'src="/img/{en_img}.webp" alt="{cap}" data-cap="{cap}"', s)
    s = re.sub(r'(<div class="phone-cap"[^>]*>)[^<]*', r'Your day', s)
    for a_, b_ in FIXES:
        s = s.replace(a_, b_)
    path = f'/en/{name}/'
    s = re.sub(r'<div class="snav">[\s\S]*?</nav></div>(?:<script[^>]*></script>)?</div>', lambda m: site_nav.header(path), s, 1)
    s = re.sub(r'<footer[\s>][\s\S]*?</footer>', lambda m: site_footer.footer(path), s, 1)
    left = sorted({m for m in re.findall(r'[^<>"\']*[؀-ۿ][^<>"\']*', s)})
    out = ROOT / 'en' / name / 'index.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(s, encoding='utf-8', newline='')
    print(name, '→', out.relative_to(ROOT), '| Arabic left:', len(left))
    for x in left[:40]:
        print('   ', x.strip()[:100])


if __name__ == '__main__':
    for n in sys.argv[1:]:
        build(n)
