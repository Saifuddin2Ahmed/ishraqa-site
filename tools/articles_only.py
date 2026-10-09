"""الموقع للمقالات وحدها (طلب المؤسس 9 أكتوبر 2026).

- الرئيسية والصفحات التعريفية وفهرسا الحِكم والمكتبة ← تحويل إلى /a/ (noindex).
- صفحات الحِكم والكتب الفردية (روابط مشاركة من التطبيق) تبقى تعمل، لكن noindex وخارج خريطة الموقع.
- يبقى كما هو: /a/، /app/، /iphone/، السياسات والتواصل (عربي وإنجليزي)، صفحات المشاركة club/event/v/i.
"""
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
REDIRECT = """<!doctype html>
<html lang="ar" dir="rtl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>مقالات إشراقة يومية</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="https://ishraqa.otwox.com/a/">
<link rel="icon" type="image/png" href="/img/icon-192.png">
<meta http-equiv="refresh" content="0; url=/a/">
<script>location.replace('/a/')</script>
<style>body{margin:0;display:grid;place-items:center;min-height:100vh;font-family:Tahoma,sans-serif;background:#2A1B5E;color:#fff}a{color:#FFB547}</style>
</head><body><a href="/a/">مقالات إشراقة يومية</a></body></html>
"""
redirect = ['.', 'about', 'developers', 'wallpapers', 'partners', 'press', 'media', 'brand',
            'strategy', 'kit', 'testers', 'clubs', 'q', 'k']
for d in redirect:
    f = root / d / 'index.html'
    if f.exists():
        f.write_text(REDIRECT, encoding='utf-8')
        print('→ /a/', d)

n = 0
for sec in ('q', 'k'):
    for f in (root / sec).glob('*/index.html'):
        s = f.read_text(encoding='utf-8')
        if 'name="robots"' in s:
            s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, follow">', s, count=1)
        else:
            s = s.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<meta name="robots" content="noindex, follow">', 1)
        f.write_text(s, encoding='utf-8')
        n += 1
print('noindex share pages:', n)
