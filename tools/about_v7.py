"""«عن» v7 (10 أكتوبر 2026، طلب المؤسس): قسم المطوّر مشهدٌ كامل بلسانه، والمسيرة بصيغة المتكلم.

المطوّر: لافتته (img/dev-banner.webp، خريطة العالم من assets/branding/developer/header.jpg) خلفيةً تتحرك ببطء،
وصورته (img/dev-portrait.webp) تتقدّم فوقها، ونبذة بصوته، ومهاراته، وأيقونات الروابط مع شعار Kwegatta.

    python tools/about_v7.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'about-v7'

KW = ('<svg viewBox="0 0 24 24" aria-hidden="true"><rect width="24" height="24" rx="6" fill="#0B1220"/>'
      '<circle cx="9.6" cy="12" r="4.1" fill="none" stroke="#F5B800" stroke-width="2.3"/>'
      '<circle cx="14.4" cy="12" r="4.1" fill="none" stroke="#14B8A6" stroke-width="2.3"/>'
      '<path d="M12.6 9.2a4.1 4.1 0 0 1 1 3.8" fill="none" stroke="#F5B800" stroke-width="2.3"/></svg>')

SKILLS = ['Flutter · Dart', 'Android · Kotlin', 'الذكاء الاصطناعي', 'السحابة', 'المصادر المفتوحة', 'تصميم التجربة']

CSS = """
/* ── about v7: المطوّر ── */
.dv{position:relative;max-width:1180px;margin:0 auto;border-radius:34px;overflow:hidden;background:#0e0a1c;color:#fff;box-shadow:0 40px 90px rgba(14,10,28,.28)}
.dv-bn{position:relative;height:clamp(240px,34vw,420px);overflow:hidden}
.dv-bn i{position:absolute;inset:-6%;background:url(/img/dev-banner.webp) center/cover;animation:dvkb 26s ease-in-out infinite alternate}
@keyframes dvkb{to{transform:scale(1.12) translate(-2%,1.5%)}}
@keyframes dvspin{to{transform:rotate(360deg)}}
.dv-bn:after{content:'';position:absolute;inset:0;background:linear-gradient(0deg,#0e0a1c 2%,rgba(14,10,28,.35) 45%,rgba(14,10,28,0) 75%)}
.dv-in{position:relative;display:grid;grid-template-columns:auto 1fr;gap:38px;align-items:start;padding:26px 46px 46px}
.dv-ph{margin-top:-130px}
.dv-ph{width:clamp(150px,18vw,210px);aspect-ratio:1/1;border-radius:50%;padding:5px;background:conic-gradient(from 0deg,var(--gold),var(--sun),var(--plum),#2C6ED5,var(--gold));animation:dvspin 14s linear infinite;box-shadow:0 20px 50px rgba(0,0,0,.45)}
.dv-ph img{width:100%;height:100%;border-radius:50%;object-fit:cover;display:block;border:4px solid #0e0a1c;animation:dvspin 14s linear infinite reverse}
.dv h3{margin:0;font-size:clamp(30px,3.6vw,44px);line-height:1.2}
.dv .t{color:var(--gold);font-weight:800;margin:6px 0 14px;font-size:15.5px}
.dv p{margin:0 0 18px;font-size:clamp(17px,1.8vw,19px);line-height:2;color:rgba(255,255,255,.88);max-width:640px}
.dv-sk{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 20px;padding:0;list-style:none}
.dv-sk li{padding:6px 14px;border-radius:999px;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.18);font-size:13.5px;font-weight:700}
.dv .icons{display:flex;flex-wrap:wrap;gap:12px}
.dv .icons a{width:50px;height:50px;border-radius:16px;display:grid;place-items:center;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.2);color:#fff;transition:transform .25s,background .25s,box-shadow .25s}
.dv .icons a svg{width:24px;height:24px}.dv .icons a.kw svg{width:30px;height:30px}
.dv .icons a:hover{transform:translateY(-4px);background:linear-gradient(140deg,var(--plum),var(--sun));box-shadow:0 12px 26px rgba(240,122,74,.4)}
@media (max-width:760px){.dv{border-radius:26px}.dv-in{grid-template-columns:1fr;justify-items:center;text-align:center;padding:0 22px 32px;gap:18px}.dv-ph{margin-top:-80px}
.dv-sk,.dv .icons{justify-content:center}}
@media (prefers-reduced-motion:reduce){.dv-bn i,.dv-ph,.dv-ph img{animation:none}}
"""


def main():
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('about: already v7'); return
    # روابط v6 كما هي، مع شعار Kwegatta بدل الأيقونة العامة
    icons = re.search(r'<div class="icons">.*?</div>', s, re.S).group(0)
    icons = re.sub(r'(<a href="https://kwegatta[^"]*"[^>]*)>(<svg.*?</svg>)', lambda m: m.group(1) + ' class="kw">' + KW, icons, flags=re.S)
    sk = ''.join(f'<li>{k}</li>' for k in SKILLS)
    dev = (f'<section class="{MARK}"><div class="wrap"><div class="dv rv"><div class="dv-bn"><i></i></div><div class="dv-in">'
           '<div class="dv-ph"><img src="/img/dev-portrait.webp" alt="م. سيف الدين أحمد" width="512" height="512" loading="lazy"></div>'
           '<div><h3>م. سيف الدين أحمد</h3><div class="t">مطوّر إشراقة يومية · مؤسس أوتواكس للحلول الرقمية</div>'
           '<p>أبني التطبيقات بـ Flutter وأندرويد والذكاء الاصطناعي، وأؤمن أن شباب أفريقيا قادرون على صناعة أدوات العالم لا استخدامها فقط. '
           'وإشراقة هي المكان الذي التقى فيه حبي للكتب بحبي للبرمجة.</p>'
           f'<ul class="dv-sk">{sk}</ul>{icons}</div></div></div></div></section>')
    a = s.index('<section><div class="wrap ab-dev')
    b = s.index('</section>', a) + len('</section>')
    s = s[:a] + dev + s[b:]
    # المسيرة بصيغة المتكلم
    for old, new in [('تطبيق لقراءة الكتب صمّمه سيف الدين بـ Flutter.', 'تطبيق لقراءة الكتب صمّمتُه بـ Flutter.'),
                     ('وفي سبتمبر جمعه نادي Candle للقراءة', 'وفي سبتمبر جمعني نادي Candle للقراءة'),
                     ('ووقف إلى جانبه أخوه وزميله سعيد حسن', 'ووقف إلى جانبي أخي وزميلي سعيد حسن')]:
        assert old in s, old
        s = s.replace(old, new)
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    p.write_text(s, encoding='utf-8')
    print('about: v7 ok')


if __name__ == '__main__':
    main()
