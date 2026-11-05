"""الشريط العلوي الموحّد للموقع (تنسيقه في /nav.css وسلوك قائمة الهاتف في /nav.js):
مصدر واحد تستعمله المولّدات وتحديث الصفحات الثابتة (tools/site_chrome.py)."""

VERSION = '20261105'
NAV_CSS = f'<link rel="stylesheet" href="/nav.css?v={VERSION}">'
NAV_JS = f'<script src="/nav.js?v={VERSION}" defer></script>'

AR_LINKS = [('/about/', 'عن التطبيق'), ('/a/', 'المقالات'), ('/developers/', 'المطوّرون')]
EN_LINKS = [('/en/about/', 'About'), ('/a/', 'Articles'), ('/en/developers/', 'Developers')]

# صفحات لها نظيرة في اللغة الأخرى: زر اللغة يذهب إليها مباشرة
PAIRS = ['about', 'developers', 'wallpapers', 'privacy', 'terms', 'contact', 'delete-account', 'child-safety', 'press-kit', 'support']

GLOBE = ('<svg class="snav-globe" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" '
         'stroke-width="1.8" stroke-linecap="round"><circle cx="12" cy="12" r="9"/>'
         '<path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9s-1.3 6.4-3.8 9c-2.5-2.6-3.8-5.6-3.8-9S9.5 5.6 12 3z"/></svg>')
BURGER = '<span class="snav-bars" aria-hidden="true"><i></i><i></i><i></i></span>'
ICON = '<img src="/img/icon-192.png" width="192" height="192" alt="">'


def is_en(path):
    return path == '/en/' or path.startswith('/en/')


def other_lang(path):
    """رابط الصفحة نفسها باللغة الأخرى إن وُجدت، وإلا الرئيسية"""
    if is_en(path):
        rest = path[len('/en/'):].strip('/')
        return f'/{rest}/' if rest in PAIRS else '/'
    rest = path.strip('/')
    return f'/en/{rest}/' if rest in PAIRS else '/en/'


def current(path, href):
    if path == href:
        return ' aria-current="page"'
    if href in ('/a/', '/k/') and path.startswith(href):
        return ' aria-current="true"'
    return ''


def header(path='/'):
    """path: مسار الصفحة مثل /about/ أو /en/privacy/ أو /a/<slug>/"""
    if is_en(path):
        links, home, name, label, menu = EN_LINKS, '/en/', 'Ishraqa Daily', 'Main', 'Menu'
        lang = f'<a class="snav-lang" href="{other_lang(path)}" hreflang="ar" lang="ar"><span>العربية</span></a>'
    else:
        links, home, name, label, menu = AR_LINKS, '/', 'إشراقة يومية', 'الرئيسية', 'القائمة'
        lang = f'<a class="snav-lang" href="{other_lang(path)}" hreflang="en" lang="en"><span>English</span></a>'
    items = ''.join(f'<a href="{h}"{current(path, h)}>{t}</a>' for h, t in links) + lang
    return (f'<div class="snav"><div class="snav-in">'
            f'<a class="snav-brand" href="{home}">{ICON}<span>{name}</span></a>'
            f'<button class="snav-btn" type="button" aria-label="{menu}" aria-expanded="false" aria-controls="snav-menu">{BURGER}</button>'
            f'<nav class="snav-links" id="snav-menu" aria-label="{label}">{items}</nav>'
            f'</div>{NAV_JS}</div>')
