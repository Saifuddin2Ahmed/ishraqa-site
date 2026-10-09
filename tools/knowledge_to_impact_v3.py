"""الإصدار الثالث (10 أكتوبر 2026): الحركة لكل الموقع، وبلا دوائر.

١) «رزمة الصفحات» بدل المجرّة في «عن»: الأبعاد الستة تبدأ مكدّسة كأوراق كتاب،
   وتنفرد مع التمرير حتى تستقر شبكةً مرتبة (على الهاتف: تظهر متتابعة).
٢) نظام الحركة الموحّد (fx.css + fx.js) يُضاف إلى كل صفحات الموقع ما عدا /app/،
   وseo.finalize يضيفه تلقائيًا لكل صفحة تُبنى بعد اليوم.

    python tools/knowledge_to_impact_v3.py
"""
import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'k2i-v3'
spec = importlib.util.spec_from_file_location('k1', ROOT / 'tools' / 'knowledge_to_impact.py')
k1 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(k1)

DIMS = [('human', 'الإنسان', 'المعرفة وسيلة لتوسيع الفهم والإمكانات.'),
        ('book', 'المعرفة', 'قراءة وفهم وتأمل، وتعلّم لا يتوقف.'),
        ('team', 'المجتمع', 'لقاء من تجمعهم اهتمامات وأحلام مشتركة.'),
        ('build', 'الإنتاج', 'ما نتعلّمه يصير مشروعًا ومبادرة.'),
        ('memory', 'الذاكرة', 'حكايات وأمثال ومعارف محلية لا تضيع.'),
        ('chip', 'التقنية', 'أدوات تجعل الوصول والمشاركة أسهل.')]


def deck():
    cards = ''.join(
        f'<article class="kd-card" style="--k:{i}"><span class="kd-n">0{i + 1}</span>{k1.ic(ic)}<b>{t}</b><p>{d}</p></article>'
        for i, (ic, t, d) in enumerate(DIMS))
    return f'<div class="kd {MARK}" aria-label="أبعاد إشراقة"><div class="kd-stick"><div class="kd-stage">{cards}</div></div></div>'


CSS = """
/* ── v3: رزمة الصفحات ── */
.kd{position:relative;height:230vh;margin-top:10px}
.kd-stick{position:sticky;top:0;height:100vh;height:100svh;display:grid;place-items:center}
.kd-stage{position:relative;width:min(1000px,94vw);height:min(560px,78vh)}
.kd-card{position:absolute;left:50%;top:50%;width:min(300px,30%);min-height:190px;padding:24px 22px;border-radius:24px;background:var(--card);border:1px solid var(--line);
box-shadow:0 18px 44px rgba(42,27,94,.12);transform-origin:50% 100%;will-change:transform;backface-visibility:hidden}
.kd-card .k-ic{width:34px;height:34px;color:var(--plum)}
.kd-n{position:absolute;top:16px;inset-inline-end:20px;font-weight:900;font-size:34px;line-height:1;color:transparent;-webkit-text-stroke:1.5px var(--sun);opacity:.7}
.kd-card b{display:block;font-size:22px;margin:12px 0 4px}.kd-card p{margin:0;color:var(--muted);font-size:15.5px;line-height:1.8}
.kd-card:nth-child(odd){background:linear-gradient(160deg,var(--card),var(--soft,var(--card)))}
@media (max-width:760px),(prefers-reduced-motion:reduce){.kd{height:auto}.kd-stick{position:static;height:auto}
.kd-stage{height:auto;width:auto;display:grid;grid-template-columns:1fr 1fr;gap:14px}
.kd-card{position:relative;left:auto;top:auto;width:auto;transform:none!important}}
@media (max-width:480px){.kd-stage{grid-template-columns:1fr}}
"""

JS = """<script>
/* k2i-v3: رزمة الصفحات — مكدّسة كأوراق كتاب، تنفرد مع التمرير حتى تستقر شبكة */
(function(){
var kd=document.querySelector('.kd');if(!kd)return;
var wide=matchMedia('(min-width:761px)'),rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
var cards=[].slice.call(kd.querySelectorAll('.kd-card')),stage=kd.querySelector('.kd-stage');
function ease(t){return t<.5?4*t*t*t:1-Math.pow(-2*t+2,3)/2}
function f(){
  if(!wide.matches||rm){cards.forEach(function(c){c.style.transform=''});return}
  var r=kd.getBoundingClientRect(),h=r.height-innerHeight,p=Math.min(1,Math.max(0,-r.top/(h>0?h:1)));
  var W=stage.clientWidth,H=stage.clientHeight,cw=cards[0].offsetWidth,ch=cards[0].offsetHeight,gx=(W-cw*3)/4,gy=(H-ch*2)/3;
  cards.forEach(function(c,i){
    var t=ease(Math.min(1,Math.max(0,p*1.35-i*0.06)));
    var col=i%3,row=(i/3)|0,tx=W/2-(gx+col*(cw+gx)+cw/2),ty=(gy+row*(ch+gy)+ch/2)-H/2;
    /* الرزمة: كل ورقة مائلة قليلًا ومزاحة كأنها صفحات كتاب */
    var sr=(i-2.5)*5,sx=(i-2.5)*6,sy=-(i)*3;
    var x=sx+(tx-sx)*t,y=sy+(ty-sy)*t,rot=sr*(1-t),ry=(1-t)*(i%2?-18:18);
    c.style.transform='translate(-50%,-50%) translate('+x.toFixed(1)+'px,'+y.toFixed(1)+'px) rotate('+rot.toFixed(2)+'deg) perspective(900px) rotateY('+ry.toFixed(1)+'deg)';
    c.style.zIndex=t>0.5?10+i:10-i;
  });
}
addEventListener('scroll',f,{passive:true});addEventListener('resize',f);wide.addEventListener('change',f);f();
})();
</script>"""

FX = '<link rel="stylesheet" href="/fx.css">'
FXJS = '<script src="/fx.js" defer></script>'


def about():
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('about: already v3'); return
    a = s.index('<div class="kg"')
    b = s.index('<p class="k-motto')
    s = s[:a] + deck() + s[b:]
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('about: deck ok')


def inject_all():
    n = 0
    for f in ROOT.rglob('index.html'):
        rel = f.relative_to(ROOT).as_posix()
        if rel.startswith(('app/', '.git/', 'tools/')):
            continue
        s = f.read_text(encoding='utf-8')
        if '/fx.js' in s or '</head>' not in s or '</body>' not in s:
            continue
        s = s.replace('</head>', FX + '\n</head>', 1)
        j = s.rindex('</body>')
        s = s[:j] + FXJS + '\n' + s[j:]
        f.write_text(s, encoding='utf-8')
        n += 1
    print('fx injected into', n, 'pages')


def patch_seo():
    p = ROOT / 'tools' / 'seo.py'
    s = p.read_text(encoding='utf-8')
    if 'fx.js' in s:
        print('seo: already'); return
    old = "    if 'platforms.js' not in doc"
    assert old in s
    s = s.replace(old, """    # نظام الحركة الموحّد لكل صفحة (ما عدا نسخة التطبيق)
    if '/fx.js' not in doc and '</head>' in doc and '</body>' in doc:
        doc = doc.replace('</head>', '<link rel="stylesheet" href="/fx.css">\\n</head>', 1)
        doc = doc.replace('</body>', '<script src="/fx.js" defer></script>\\n</body>', 1)
""" + old, 1)
    p.write_text(s, encoding='utf-8')
    print('seo: fx injection added')


if __name__ == '__main__':
    about()
    inject_all()
    patch_seo()
