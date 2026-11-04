"""الشريط العلوي الموحّد للموقع (تنسيقه في /nav.css): مصدر واحد تستعمله المولّدات وتحديث الصفحات الثابتة."""

NAV_CSS = '<link rel="stylesheet" href="/nav.css?v=20261104">'

AR_LINKS = [('/about/', 'عن التطبيق'), ('/a/', 'المقالات'), ('/k/', 'المكتبة'), ('/developers/', 'للمطوّرين')]
EN_LINKS = [('/en/contact/', 'Contact'), ('/en/support/', 'Support')]

# صفحات لها نظيرة في اللغة الأخرى: زر اللغة يذهب إليها مباشرة
PAIRS = ['privacy', 'terms', 'contact', 'delete-account', 'child-safety', 'press-kit', 'support']


def _current(path, href):
    if path == href:
        return ' aria-current="page"'
    if href in ('/a/', '/k/') and path.startswith(href):
        return ' aria-current="true"'
    return ''


def header(path='/'):
    """path: مسار الصفحة مثل /about/ أو /en/privacy/ أو /a/<slug>/"""
    en = path == '/en/' or path.startswith('/en/')
    if en:
        rest = path[len('/en/'):].strip('/')
        other = f'/{rest}/' if rest in PAIRS else '/'
        links = ''.join(f'<a href="{h}"{_current(path, h)}>{t}</a>' for h, t in EN_LINKS)
        links += f'<a href="{other}" hreflang="ar" lang="ar">العربية</a>'
        brand = '<a class="snav-brand" href="/en/"><img src="/img/icon-192.png" width="192" height="192" alt=""><span>Ishraqa Daily</span></a>'
        label = 'Main'
    else:
        rest = path.strip('/')
        other = f'/en/{rest}/' if rest in PAIRS else '/en/'
        links = ''.join(f'<a href="{h}"{_current(path, h)}>{t}</a>' for h, t in AR_LINKS)
        links += f'<a href="{other}" hreflang="en" lang="en">English</a>'
        brand = '<a class="snav-brand" href="/"><img src="/img/icon-192.png" width="192" height="192" alt=""><span>إشراقة يومية</span></a>'
        label = 'الرئيسية'
    return f'<div class="snav"><div class="snav-in">{brand}<nav class="snav-links" aria-label="{label}">{links}</nav></div></div>'
