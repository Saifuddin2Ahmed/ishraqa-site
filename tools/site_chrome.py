"""يحدّث الشريط العلوي والتذييل الموحّدين في كل صفحات الموقع الثابتة من site_nav.py و site_footer.py.

    python tools/site_chrome.py          # يكتب التغييرات
    python tools/site_chrome.py --check  # يعرض ما سيتغيّر فقط

يمسّ فقط الصفحات التي فيها الشريط الموحّد (div.snav)، فبطاقات المشاركة والدعوة (c/ club/ u/ i/ event/ v/)
وصفحات 404 وorcid وapp وiphone لا تتغيّر. صفحات المقالات a/ يولّدها build_articles.py بالمكوّنات نفسها.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import site_footer  # noqa: E402
import site_nav  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SNAV = re.compile(r'<div class="snav">[\s\S]*?</nav></div>(?:<script[^>]*></script>)?</div>')
FOOT = re.compile(r'<footer[\s>][\s\S]*?</footer>')
CSS = re.compile(r'<link rel="stylesheet" href="/nav\.css\?v=\d+">')


def page_path(f: Path) -> str:
    rel = f.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return '/'
    assert rel.endswith('/index.html'), rel
    return '/' + rel[:-len('index.html')]


def main(check=False):
    changed, skipped = [], []
    for f in sorted(ROOT.rglob('*.html')):
        if any(p.startswith('.') for p in f.relative_to(ROOT).parts):
            continue
        s = f.read_bytes().decode('utf-8')
        if 'class="snav"' not in s:
            continue
        path = page_path(f)
        if len(SNAV.findall(s)) != 1 or len(FOOT.findall(s)) != 1:
            skipped.append(f'{path} (snav={len(SNAV.findall(s))} footer={len(FOOT.findall(s))})')
            continue
        t = SNAV.sub(lambda m: site_nav.header(path), s)
        t = FOOT.sub(lambda m: site_footer.footer(path), t)
        t = CSS.sub(site_nav.NAV_CSS, t)
        if t != s:
            changed.append(path)
            if not check:
                f.write_bytes(t.encode('utf-8'))
    print(f'{"would change" if check else "changed"}: {len(changed)}')
    for s in skipped:
        print('skipped:', s)


if __name__ == '__main__':
    main('--check' in sys.argv)
