"""التذييل الموحّد للموقع (تنسيقه في /nav.css تحت .sfoot): مصدر واحد تستعمله المولّدات وتحديث الصفحات الثابتة."""
from site_nav import current, is_en, other_lang

YEAR = 2026
AUTHOR = 'https://saifuddin.dev'

# القائمتان متطابقتان ترتيبًا وعددًا؛ المقالات والمكتبة بلغة كاتبها فرابطهما واحد في اللغتين
AR_LINKS = [('/about/', 'عن التطبيق'), ('/a/', 'المقالات'), ('/k/', 'المكتبة'), ('/developers/', 'المطوّرون'),
            ('/wallpapers/', 'خلفيات إشراقة'), ('/support/', 'ادعم إشراقة'), ('/press-kit/', 'حزمة الإعلام'),
            ('/privacy/', 'سياسة الخصوصية'), ('/terms/', 'شروط الاستخدام'), ('/delete-account/', 'حذف الحساب'),
            ('/child-safety/', 'سلامة الأطفال'), ('/contact/', 'تواصل معنا')]
EN_LINKS = [('/en/about/', 'About'), ('/a/', 'Articles'), ('/k/', 'Library'), ('/en/developers/', 'Developers'),
            ('/en/wallpapers/', 'Wallpapers'), ('/en/support/', 'Support Ishraqa'), ('/en/press-kit/', 'Press kit'),
            ('/en/privacy/', 'Privacy Policy'), ('/en/terms/', 'Terms of Use'), ('/en/delete-account/', 'Delete account'),
            ('/en/child-safety/', 'Child safety'), ('/en/contact/', 'Contact us')]


def footer(path='/'):
    """path: مسار الصفحة مثل /about/ أو /en/privacy/ أو /a/<slug>/"""
    if is_en(path):
        links, label = EN_LINKS, 'Site'
        lang = f'<a href="{other_lang(path)}" hreflang="ar" lang="ar">العربية</a>'
        by, rights = 'Developed by Saifuddin Ahmed', f'© {YEAR} Ishraqa Daily. All rights reserved.'
    else:
        links, label = AR_LINKS, 'روابط الموقع'
        lang = f'<a href="{other_lang(path)}" hreflang="en" lang="en">English</a>'
        by, rights = 'تطوير سيف الدين أحمد', f'جميع الحقوق محفوظة © {YEAR} إشراقة يومية'
    items = ''.join(f'<a href="{h}"{current(path, h)}>{t}</a>' for h, t in links) + lang
    return (f'<footer class="sfoot"><nav class="sfoot-links" aria-label="{label}">{items}</nav>'
            f'<p class="sfoot-by"><a href="{AUTHOR}" rel="author">{by}</a></p>'
            f'<p class="sfoot-c">{rights}</p></footer>')
