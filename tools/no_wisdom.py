"""الموقع بلا قسم «الحِكم والأمثال» (طلب المؤسس 9 أكتوبر 2026). كل ما عداه يبقى.

- فهرس /q/ وصفحات المواضيع /q/t/… ← تحويل إلى الرئيسية (noindex).
- صفحات الحِكم الفردية /q/<x>/ تبقى لروابط المشاركة من التطبيق، لكن noindex وخارج خريطة الموقع.
- تُحذف روابط «الحِكم» من القوائم والتذييلات.
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
REDIRECT = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>إشراقة يومية</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://ishraqa.otwox.com/">
<link rel="icon" type="image/png" href="/img/icon-192.png">
<meta http-equiv="refresh" content="0; url=/">
<script>location.replace('/')</script>
<style>body{margin:0;display:grid;place-items:center;min-height:100vh;font-family:Tahoma,sans-serif;background:#2A1B5E;color:#fff}a{color:#FFB547}</style>
</head><body><a href="/">إشراقة يومية</a></body></html>
"""
pages = [root / 'q' / 'index.html'] + list((root / 'q' / 't').glob('*/index.html'))
for f in pages:
    f.write_text(REDIRECT, encoding='utf-8')
print('redirected', len(pages))

n = 0
for f in (root / 'q').glob('*/index.html'):
    if f.parent.name == 't':
        continue
    s = f.read_text(encoding='utf-8')
    if 'noindex' in s:
        continue
    if 'name="robots"' in s:
        s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', s, count=1)
    else:
        s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, follow">', 1)
    f.write_text(s, encoding='utf-8')
    n += 1
print('noindex quote pages', n)

m = 0
for f in root.rglob('*.html'):
    rel = f.relative_to(root).as_posix()
    if rel.startswith(('q/', 'app/', '.git/')):
        continue
    s = f.read_text(encoding='utf-8')
    t = re.sub(r'<a href="/q/">[^<]*</a>\s*·\s*', '', s)
    t = re.sub(r'\s*·\s*<a href="/q/">[^<]*</a>', '', t)
    t = re.sub(r'<a href="/q/">[^<]*</a>', '', t)
    if t != s:
        f.write_text(t, encoding='utf-8')
        m += 1
print('links removed in', m, 'pages')
