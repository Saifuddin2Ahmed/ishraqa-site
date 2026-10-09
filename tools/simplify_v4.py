"""تبسيط وتقليل ما يُكشف (10 أكتوبر 2026، طلب المؤسس: «ممنوع تعرض كل حاجة… هنالك منافسين»).

الرئيسية: بلا فقرة «نعيش في عالم…»، ولا شريط الأرقام، ولا قسم نوادي المطوّرين المكرر، ولا «مكتبات للمدارس قريبًا».
«عن»: المسيرة بلا «توقف العمل فترة».
المختبرون: الصفحة تبقى لمن عنده الرابط، لكن noindex وتُحذف روابطها من القوائم والتذييلات.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]


def drop_section(s, marker):
    if marker not in s:
        return s
    a = s.index(marker)
    st = s.rindex('<section', 0, a)
    en = s.index('</section>', a) + len('</section>')
    return s[:st] + s[en:]


def home():
    p = ROOT / 'index.html'
    s = p.read_text(encoding='utf-8')
    s = drop_section(s, 'class="k-idea')
    s = drop_section(s, '<div class="stats rv"')
    s = drop_section(s, 'نوادي المطوّرين: ابنِ ما يبقى')
    s = s.replace('<li>مكتبات للمدارس<em>قريبًا</em></li>', '')
    p.write_text(s, encoding='utf-8')
    print('home ok')


def about():
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    s = s.replace('وصلت النسخة الأولى إلى Google Play في مرحلة الاختبار، ثم توقف العمل فترة.',
                  'وصلت النسخة الأولى إلى Google Play.')
    s = s.replace('<b>العودة</b><p>في أبريل عاد العمل برؤية أوسع: مساحة تربط القراءة بالحوار والمجتمع والتعاون.</p>',
                  '<b>رؤية أوسع</b><p>في أبريل اتسعت الفكرة: مساحة تربط القراءة بالحوار والمجتمع والتعاون.</p>')
    p.write_text(s, encoding='utf-8')
    print('about ok')


def testers():
    p = ROOT / 'testers' / 'index.html'
    s = p.read_text(encoding='utf-8')
    s = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, nofollow">', s, count=1)
    p.write_text(s, encoding='utf-8')
    n = 0
    for f in ROOT.rglob('*.html'):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(('app/', '.git/', 'testers/')):
            continue
        t = f.read_text(encoding='utf-8')
        u = re.sub(r'
?[ 	]*<a href="/testers/">[^<]*</a>', '', t)
        u = re.sub(r'<a class="nav-link"[^>]*href="/testers/"[^>]*>[^<]*</a>', '', u)
        u = re.sub(r'<a href="/testers/">[^<]*</a>\s*·\s*', '', u)
        u = re.sub(r'\s*·\s*<a href="/testers/">[^<]*</a>', '', u)
        if u != t:
            f.write_text(u, encoding='utf-8'); n += 1
    print('testers: noindex; links removed in', n, 'pages')


if __name__ == '__main__':
    home()
    about()
    testers()
