"""الإصدار الثاني (10 أكتوبر 2026، ملاحظات المؤسس): أقل كلامًا، وعرضٌ يتكلم وحده.

الرئيسية: مشهد سينمائي ثابت يتبدّل في مكانه مع التمرير (كتب ← نوادٍ ← برمجة ← ذاكرة)،
بخلفيات تتحرك ببطء كأنها فيديو (CC0 من StockSnap، img/scene-*.webp، الحقوق في img/scene-credits.json).
«عن»: مجرّة ثلاثية الأبعاد (شعار إشراقة في المركز والأبعاد الستة تدور حوله)، ومسيرة أفقية تتحرك مع التمرير.
تُحذف العناوين التلقينية الصغيرة (eyebrows) والجمل الشارحة. كل الحركات تحترم «تقليل الحركة».

    python tools/knowledge_to_impact_v2.py    (بعد knowledge_to_impact.py؛ يمكن تشغيله أكثر من مرة)
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'k2i-v2'

SCENES = [
    ('read', '01', 'اقرأ', 'مكتبة من روائع الكتب، ومقال قصير كل يوم، وحكمة تعرف معناها وقصتها.',
     [('المكتبة', 0), ('مقال اليوم', 0), ('ذكّرني أين وصلت', 0)]),
    ('share', '02', 'تحاور', 'نوادٍ تقرأ الكتاب نفسه، وتتحاور فيه دون أن تحرق متعته، وتختار معًا ما تقرؤه بعده.',
     [('نوادي القراءة', 0), ('اللقاءات', 0), ('تحدي المجتمعات', 0)]),
    ('build', '03', 'اصنع', 'فرق صغيرة من المطوّرين، وموجّه خبير، ومشروع مفتوح المصدر يراه العالم.',
     [('نوادي المطوّرين', 0), ('معرض المشاريع', 0), ('المنح والفرص', 0)]),
    ('memory', '04', 'احفظ', 'أمثال بأصوات أهلها، وحكايات المدن وعاداتها تُكتب بأسماء أصحابها.',
     [('صدى', 0), ('ثقافتك', 0), ('مكتبات للمدارس', 1)]),
]


def cinema():
    bgs = ''.join(f'<div class="kc-bg{" on" if i == 0 else ""}" style="background-image:url(/img/scene-{k}.webp)"></div>'
                  for i, (k, *_r) in enumerate(SCENES))
    scenes = ''
    for i, (k, n, t, d, chips) in enumerate(SCENES):
        ch = ''.join(f'<li>{c}{"<em>قريبًا</em>" if soon else ""}</li>' for c, soon in chips)
        scenes += (f'<div class="kc-scene{" on" if i == 0 else ""}" data-i="{i}"><span class="kc-num">{n}</span>'
                   f'<h3>{t}</h3><p>{d}</p><ul>{ch}</ul></div>')
    rail = ''.join(f'<button type="button" data-i="{i}"{" class=on" if i == 0 else ""} aria-label="{t}"><i></i><span>{t}</span></button>'
                   for i, (_k, _n, t, *_r) in enumerate(SCENES))
    return (f'\n  <section class="kc {MARK}" aria-label="ما في إشراقة"><div class="kc-stick">{bgs}'
            '<div class="kc-shade"></div><div class="kc-grain"></div>'
            f'<div class="wrap kc-in"><div class="kc-scenes">{scenes}</div><nav class="kc-rail">{rail}</nav></div>'
            '<div class="kc-bar"><i></i></div></div></section>\n')


GALAXY = [('الإنسان', 'المعرفة وسيلة لتوسيع الفهم والإمكانات'), ('المعرفة', 'قراءة وفهم وتأمل وتعلّم مستمر'),
          ('المجتمع', 'لقاء من تجمعهم اهتمامات مشتركة'), ('الإنتاج', 'تحويل التعلّم إلى مشاريع ومبادرات'),
          ('الذاكرة', 'حفظ الحكايات والأمثال والمعارف المحلية'), ('التقنية', 'أدوات تسهّل الوصول والمشاركة والتعاون')]


def galaxy():
    nodes = ''.join(f'<div class="kg-node" data-k="{i}"><b>{t}</b><span>{d}</span></div>' for i, (t, d) in enumerate(GALAXY))
    return ('<div class="kg" aria-label="أبعاد إشراقة"><canvas class="kg-cv" aria-hidden="true"></canvas>'
            '<div class="kg-core"><i></i><i></i><img src="/img/icon-192.png" alt="إشراقة" width="96" height="96"></div>'
            f'{nodes}</div>')


TIMELINE = [
    ('2022', 'البذرة', 'في دورة Flutter مع نادي مطوري Google بجامعة الخرطوم، صمّم سيف الدين تطبيقًا لقراءة الكتب. لم يُنشر يومها، لكن الفكرة بقيت تنتظر وقتها.'),
    ('2023', 'قارئٌ على جهاز واحد', 'صارت إشراقة قارئ كتب على جهاز مؤسسها وحده. وفي سبتمبر جمعه نادي Candle للقراءة، الذي أسسته لينة بشير موسى، بقرّاء من أماكن شتى.'),
    ('2024', 'بوتقة صغيرة', 'اتسعت لتضم الحِكم والمعلومات والكتب المختارة. ووقف إلى جانبه أخوه وزميله سعيد حسن، الداعم الأول في هذه المسيرة، فجعل ما بدا مستحيلًا ممكنًا.'),
    ('2025', 'أول نسخة', 'وصلت النسخة الأولى إلى Google Play في مرحلة الاختبار، ثم توقف العمل فترة.'),
    ('2026', 'العودة', 'في أبريل عاد العمل برؤية أوسع: مساحة تربط القراءة بالحوار والمجتمع والتعاون.'),
    ('اليوم', 'للجميع', 'في أكتوبر 2026 صارت إشراقة يومية متاحة للجميع على Google Play ومتجر Microsoft.'),
]


def hline():
    cards = ''.join(f'<article class="kh-card"><span class="kh-year">{y}</span><b>{t}</b><p>{d}</p></article>' for y, t, d in TIMELINE)
    return (f'\n  <section class="kh {MARK}" aria-label="المسيرة"><div class="kh-stick"><div class="wrap kh-head"><h2>من قارئ على جهاز واحد، إلى مساحة للجميع</h2></div>'
            f'<div class="kh-track">{cards}</div><div class="kh-line"><i></i></div></div></section>\n')


CSS = """
/* ── v2: مشهد سينمائي، مجرّة، مسيرة أفقية ── */
.kc{position:relative;height:420vh;padding:0!important}
.kc-stick{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;background:#0e0a1c;color:#fff}
.kc-bg{position:absolute;inset:-4%;background-size:cover;background-position:center;opacity:0;transform:scale(1.06);transition:opacity 1.3s ease;will-change:transform,opacity}
.kc-bg.on{opacity:1;animation:kb 22s ease-in-out infinite alternate}
@keyframes kb{0%{transform:scale(1.06) translate(0,0)}50%{transform:scale(1.16) translate(-1.5%,1%)}100%{transform:scale(1.1) translate(1.5%,-1%)}}
.kc-shade{position:absolute;inset:0;background:linear-gradient(270deg,rgba(14,10,28,.92) 0%,rgba(14,10,28,.72) 38%,rgba(42,27,94,.25) 70%,rgba(240,122,74,.15) 100%),linear-gradient(0deg,rgba(14,10,28,.85),transparent 45%)}
.kc-grain{position:absolute;inset:0;opacity:.18;mix-blend-mode:overlay;pointer-events:none;background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='160' height='160'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.85' numOctaves='2'/%3E%3C/filter%3E%3Crect width='160' height='160' filter='url(%23n)'/%3E%3C/svg%3E")}
.kc-in{position:relative;height:100%;display:flex;align-items:center;justify-content:space-between;gap:30px}
.kc-scenes{position:relative;flex:1;max-width:640px;min-height:380px}
.kc-scene{position:absolute;inset:auto 0 auto 0;top:50%;transform:translateY(-40%);opacity:0;transition:opacity .7s ease,transform .9s cubic-bezier(.2,.7,.2,1);pointer-events:none}
.kc-scene.on{opacity:1;transform:translateY(-50%);pointer-events:auto}
.kc-num{display:block;font-weight:900;font-size:15px;letter-spacing:3px;color:var(--gold);margin-bottom:6px}
.kc-scene h3{margin:0;font-size:clamp(64px,11vw,140px);line-height:1.05;font-weight:900;letter-spacing:-1px;background:linear-gradient(180deg,#fff 30%,#ffd9b0);-webkit-background-clip:text;background-clip:text;color:transparent;text-shadow:0 20px 60px rgba(0,0,0,.25)}
.kc-scene p{margin:14px 0 22px;font-size:clamp(18px,2.1vw,23px);line-height:1.9;opacity:.92;max-width:560px}
.kc-scene ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px}
.kc-scene li{padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);backdrop-filter:blur(8px);font-weight:700;font-size:14.5px}
.kc-scene li em{font-style:normal;margin-inline-start:8px;font-size:11.5px;padding:1px 8px;border-radius:999px;background:var(--sun);color:#fff}
.kc-scene.on li{animation:chip .6s both}.kc-scene.on li:nth-child(2){animation-delay:.08s}.kc-scene.on li:nth-child(3){animation-delay:.16s}
@keyframes chip{from{opacity:0;transform:translateY(10px)}}
.kc-rail{display:flex;flex-direction:column;gap:18px}
.kc-rail button{text-shadow:0 2px 12px rgba(0,0,0,.7);display:flex;align-items:center;gap:12px;background:none;border:0;color:#fff;opacity:.45;font:inherit;font-weight:800;font-size:15px;cursor:pointer;transition:opacity .3s}
.kc-rail button i{width:10px;height:10px;border-radius:50%;border:2px solid #fff;transition:all .3s}
.kc-rail button.on{opacity:1}.kc-rail button.on i{background:var(--gold);border-color:var(--gold);box-shadow:0 0 0 6px rgba(255,181,71,.2)}
.kc-bar{position:absolute;inset-inline:0;bottom:0;height:3px;background:rgba(255,255,255,.12)}
.kc-bar i{display:block;height:100%;background:linear-gradient(90deg,var(--gold),var(--sun));transform-origin:right;transform:scaleX(var(--p,0))}
@media (max-width:820px){.kc-in{flex-direction:column;justify-content:flex-end;align-items:stretch;padding-bottom:70px}
.kc-scenes{min-height:430px;max-width:none}.kc-scene{top:auto;bottom:0;transform:translateY(20px)}.kc-scene.on{transform:none}
.kc-rail{flex-direction:row;justify-content:center;gap:16px;position:absolute;top:22px;inset-inline:0}.kc-rail span{display:none}
.kc-shade{background:linear-gradient(0deg,rgba(14,10,28,.95) 15%,rgba(14,10,28,.55) 60%,rgba(14,10,28,.35))}}
/* المجرّة */
.kg{position:relative;max-width:900px;height:560px;margin:10px auto 0}
.kg-cv{position:absolute;inset:0;width:100%;height:100%}
.kg-core{position:absolute;left:50%;top:50%;width:150px;height:150px;transform:translate(-50%,-50%);display:grid;place-items:center;z-index:5}
.kg-core img{width:84px;height:84px;border-radius:22px;box-shadow:0 0 0 6px rgba(255,255,255,.6),0 18px 50px rgba(240,122,74,.45);position:relative;z-index:2}
.kg-core i{position:absolute;inset:0;border-radius:50%;border:1.5px dashed rgba(240,122,74,.45);animation:spin 30s linear infinite}
.kg-core i+i{inset:-26px;border:1px solid rgba(142,58,140,.25);animation-duration:46s;animation-direction:reverse}
@keyframes spin{to{transform:rotate(360deg)}}
.kg-node{position:absolute;left:0;top:0;width:200px;text-align:center;transform:translate(-50%,-50%);will-change:transform,opacity;cursor:default}
.kg-node b{display:inline-block;padding:9px 18px;border-radius:999px;background:var(--card);border:1px solid var(--line);font-size:17px;box-shadow:0 10px 28px rgba(42,27,94,.12)}
.kg-node span{display:block;margin-top:8px;font-size:13.5px;color:var(--muted);line-height:1.7;opacity:0;transition:opacity .4s}
.kg-node.front span{opacity:1}
@media (max-width:640px){.kg{height:440px}.kg-node{width:140px}.kg-node b{font-size:14.5px;padding:7px 13px}.kg-node span{display:none}.kg-core{width:110px;height:110px}.kg-core img{width:64px;height:64px}}
/* المسيرة الأفقية */
.kh{position:relative;height:330vh;padding:0!important}
.kh-stick{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;display:flex;flex-direction:column;justify-content:center;gap:34px}
.kh-head h2{margin:0}
.kh-track{display:flex;gap:28px;padding-inline:max(20px,calc((100vw - 1180px)/2));will-change:transform;transform:translateX(var(--x,0px))}
.kh-card{flex:0 0 min(78vw,420px);padding:28px 28px 30px;border-radius:28px;background:var(--card);border:1px solid var(--line);box-shadow:0 18px 44px rgba(42,27,94,.08);position:relative;overflow:hidden}
.kh-year{display:block;font-size:clamp(70px,9vw,112px);line-height:1;font-weight:900;color:transparent;-webkit-text-stroke:2px var(--sun);opacity:.9;margin-bottom:14px;font-variant-numeric:tabular-nums}
.kh-card b{display:block;font-size:22px;margin-bottom:6px}.kh-card p{margin:0;color:var(--muted);font-size:16.5px;line-height:1.95}
.kh-card:last-child{background:linear-gradient(140deg,var(--night),var(--plum) 60%,var(--sun));color:#fff;border:0}
.kh-card:last-child .kh-year{-webkit-text-stroke:2px #fff}.kh-card:last-child p{color:rgba(255,255,255,.9)}
.kh-line{margin:0 auto;width:min(1180px,90vw);height:3px;border-radius:3px;background:var(--line)}
.kh-line i{display:block;height:100%;border-radius:3px;background:linear-gradient(90deg,var(--gold),var(--sun),var(--plum));transform-origin:right;transform:scaleX(var(--p,0))}
@media (prefers-reduced-motion:reduce){.kc-bg.on{animation:none}.kc-scene,.kc-bg{transition:none}.kg-core i{animation:none}
.kh{height:auto}.kh-stick{position:static;height:auto;padding:80px 0}.kh-track{transform:none!important;flex-wrap:wrap;justify-content:center}}
"""

JS = """<script>
/* k2i-v2: المشهد السينمائي، والمسيرة الأفقية، والمجرّة */
(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function prog(el){var r=el.getBoundingClientRect(),h=r.height-innerHeight;return Math.min(1,Math.max(0,-r.top/(h>0?h:1)))}
/* المشهد: يتبدّل في مكانه مع التمرير */
var kc=document.querySelector('.kc');
if(kc){var bg=kc.querySelectorAll('.kc-bg'),sc=kc.querySelectorAll('.kc-scene'),bt=kc.querySelectorAll('.kc-rail button'),cur=0;
  function set(i){if(i===cur)return;[bg,sc,bt].forEach(function(l){l[cur].classList.remove('on');l[i].classList.add('on')});cur=i}
  function f(){var p=prog(kc);kc.style.setProperty('--p',p.toFixed(3));set(Math.min(sc.length-1,Math.floor(p*sc.length*0.999)))}
  bt.forEach(function(b,i){b.addEventListener('click',function(){var r=kc.getBoundingClientRect(),h=r.height-innerHeight;scrollTo({top:scrollY+r.top+h*(i+0.5)/sc.length,behavior:rm?'auto':'smooth'})})});
  addEventListener('scroll',f,{passive:true});addEventListener('resize',f);f()}
/* المسيرة: تتحرك أفقيًا مع التمرير */
var kh=document.querySelector('.kh');
if(kh&&!rm){var tr=kh.querySelector('.kh-track'),ln=kh.querySelector('.kh-line');
  function g(){var p=prog(kh),max=Math.max(0,tr.scrollWidth-innerWidth);tr.style.setProperty('--x',(p*max).toFixed(1)+'px');ln.style.setProperty('--p',p.toFixed(3))}
  addEventListener('scroll',g,{passive:true});addEventListener('resize',g);g()}
/* المجرّة: الأبعاد الستة تدور حول إشراقة بعمق ثلاثي الأبعاد */
var kg=document.querySelector('.kg');
if(kg){var cv=kg.querySelector('.kg-cv'),cx=cv.getContext('2d'),nodes=[].slice.call(kg.querySelectorAll('.kg-node')),dpr=Math.min(2,devicePixelRatio||1),W,H,a0=0,last=null,vis=true,hover=false;
  function size(){W=kg.clientWidth;H=kg.clientHeight;cv.width=W*dpr;cv.height=H*dpr;cx.setTransform(dpr,0,0,dpr,0,0)}
  size();addEventListener('resize',size);
  nodes.forEach(function(n){n.addEventListener('mouseenter',function(){hover=true});n.addEventListener('mouseleave',function(){hover=false})});
  if('IntersectionObserver' in window)new IntersectionObserver(function(es){vis=es[0].isIntersecting;if(vis&&!rm)requestAnimationFrame(draw)}).observe(kg);
  function draw(ts){if(last===null)last=ts;var dt=Math.min(.05,(ts-last)/1000);last=ts;if(!hover&&!rm)a0+=dt*0.16;
    var Rx=Math.min(W*0.42,380),Ry=Math.min(H*0.36,200),c={x:W/2,y:H/2};cx.clearRect(0,0,W,H);
    var pos=nodes.map(function(n,k){var t=a0+k*Math.PI*2/nodes.length,d=(Math.sin(t)+1)/2;return {n:n,x:c.x+Math.cos(t)*Rx,y:c.y+Math.sin(t)*Ry,d:d}});
    /* مدار وخطوط ضوء */
    cx.strokeStyle='rgba(142,58,140,.18)';cx.lineWidth=1;cx.beginPath();cx.ellipse(c.x,c.y,Rx,Ry,0,0,Math.PI*2);cx.stroke();
    pos.forEach(function(p){var gr=cx.createLinearGradient(c.x,c.y,p.x,p.y);gr.addColorStop(0,'rgba(240,122,74,'+(0.15+0.5*p.d)+')');gr.addColorStop(1,'rgba(142,58,140,'+(0.05+0.3*p.d)+')');
      cx.strokeStyle=gr;cx.lineWidth=1+1.4*p.d;cx.beginPath();cx.moveTo(c.x,c.y);cx.lineTo(p.x,p.y);cx.stroke();
      cx.fillStyle='rgba(255,181,71,'+(0.35+0.6*p.d)+')';cx.beginPath();cx.arc(p.x,p.y,3+3*p.d,0,Math.PI*2);cx.fill()});
    pos.forEach(function(p){var s=0.78+0.32*p.d;p.n.style.transform='translate('+(p.x)+'px,'+(p.y)+'px) translate(-50%,-50%) scale('+s.toFixed(3)+')';
      p.n.style.opacity=(0.45+0.55*p.d).toFixed(2);p.n.style.zIndex=p.y>c.y?6:3;p.n.classList.toggle('front',p.d>0.72)});
    if(vis&&!rm)requestAnimationFrame(draw)}
  requestAnimationFrame(draw)}
})();
</script>"""


def home():
    p = ROOT / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('home: already v2'); return
    s = re.sub(r'<span class="k-eyebrow">[^<]*</span>', '', s)
    s = s.replace('<p class="sub">رحلة نمشيها معًا: كل خطوة تفتح الباب للتي بعدها.</p>', '')
    s = s.replace('<h2>كيف تتحول صفحة إلى أثر؟</h2>', '<h2>كيف تكبر فكرة؟</h2>')
    # قسم المسارات الأربعة ← شريط الأرقام + المشهد السينمائي
    a = s.index('<h2>مساحة واحدة، أربعة مسارات</h2>')
    st = s.rindex('<section', 0, a)
    en = s.index('</section>', a) + len('</section>')
    blk = s[st:en]
    stats = re.search(r'<div class="stats rv".*?</div></div>', blk, re.S).group(0)
    s = s[:st] + f'<section style="padding-bottom:10px"><div class="wrap">{stats}</div></section>' + cinema() + s[en:]
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('home: v2 ok')


def about():
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('about: already v2'); return
    s = re.sub(r'<span class="k-eyebrow">[^<]*</span>', '', s)
    s = s.replace('<h2 class="rv">من المعرفة إلى الأثر</h2>', '', 1)
    s = s.replace('<p class="sub rv">نميّز بوضوح بين ما هو متاح الآن وما نعمل عليه.</p>', '')
    s = s.replace('<h2 class="rv">ما نقدّمه اليوم، وما نطمح إليه</h2>', '<h2 class="rv">اليوم، وما نطمح إليه</h2>')
    # المجرّة بدل المخطط الثابت
    a = s.index('<div class="k-orbit"')
    b = s.index('<p class="k-motto')
    s = s[:a] + galaxy() + s[b:]
    # المسيرة الأفقية بدل العمودية
    a = s.index('<h2 class="rv">من قارئ على جهاز واحد، إلى مساحة للجميع</h2>')
    st = s.rindex('<section', 0, a)
    en = s.index('</section>', a) + len('</section>')
    s = s[:st] + hline().strip() + s[en:]
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('about: v2 ok')


if __name__ == '__main__':
    home()
    about()
