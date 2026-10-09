"""«من المعرفة إلى الأثر»: الرئيسية وصفحة «عن إشراقة» (10 أكتوبر 2026، بموافقة المؤسس).

الرئيسية: افتتاحية «حروف تتجمع كتابًا»، فقرة الفكرة، منظومة إشراقة (أربعة مسارات بحالاتها)،
رحلة «كتاب ← فكرة ← حوار ← تعلّم ← تعاون ← أثر»، وخاتمة «المعرفة تكبر عندما تجد من يشاركها».
«عن»: الفلسفة وأبعادها الستة كمنظومة واحدة، لماذا بدأت، المسيرة المصححة كخط زمني يتقدّم، ما نقدّمه وما نطمح إليه.
كل الحركات تحترم «تقليل الحركة»، والنص ظاهر من البداية دون انتظار.

    python tools/knowledge_to_impact.py      (من جذر مستودع الموقع؛ يمكن تشغيله أكثر من مرة)
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'k2i-v1'

I = {  # أيقونات خطية 24×24
    'book': '<path d="M2 4h6a4 4 0 0 1 4 4v12a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v12a3 3 0 0 1 3-3h7z"/>',
    'idea': '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3z"/>',
    'chat': '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 11h7M8.5 14h4"/>',
    'learn': '<path d="m2 9 10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 2.7 3 6 3s6-1.5 6-3v-5"/>',
    'team': '<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6.5 6.5 0 0 1 3.5 6"/>',
    'spark': '<path d="M12 2v4M12 18v4M4.9 4.9l2.8 2.8M16.3 16.3l2.8 2.8M2 12h4M18 12h4M4.9 19.1l2.8-2.8M16.3 7.7l2.8-2.8"/><circle cx="12" cy="12" r="3"/>',
    'code': '<path d="m8 8-5 4 5 4M16 8l5 4-5 4M13.5 5l-3 14"/>',
    'memory': '<path d="M12 3a9 9 0 1 0 9 9"/><path d="M12 7v5l3 2"/><path d="M21 3v6h-6"/>',
    'human': '<circle cx="12" cy="6" r="3"/><path d="M5 21a7 7 0 0 1 14 0"/>',
    'globe': '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
    'chip': '<rect x="6" y="6" width="12" height="12" rx="2"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4"/>',
    'moon': '<path d="M20 14.5A8 8 0 1 1 9.5 4a6.5 6.5 0 0 0 10.5 10.5z"/>',
    'search': '<circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/>',
    'lock': '<rect x="4" y="10" width="16" height="11" rx="3"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
    'build': '<path d="M14.7 6.3a4 4 0 0 0 5 5l-8.4 8.4a2.1 2.1 0 0 1-3-3z"/><path d="M14.7 6.3 17 4l3 3-2.3 2.3"/>',
}


def ic(name, cls='k-ic'):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{I[name]}</svg>')


CSS = """
/* ── من المعرفة إلى الأثر ── */
.k-eyebrow{display:block;text-align:center;color:var(--sun);font-weight:800;font-size:14px;letter-spacing:.4px;margin-bottom:8px}
.k-ic{width:26px;height:26px}
.k-idea{max-width:860px;margin:0 auto;text-align:center}
.k-idea .big{font-size:clamp(22px,3vw,31px);line-height:1.8;font-weight:800;margin:0 0 16px;color:var(--ink);text-wrap:balance}
.k-idea p{font-size:clamp(17px,2vw,20px);color:var(--muted);margin:0;text-wrap:pretty}
.k-paths{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin-top:10px}
.k-path{position:relative;padding:24px 22px 22px;border-radius:24px;background:var(--card);border:1px solid var(--line);overflow:hidden;transition:transform .3s,box-shadow .3s}
.k-path:before{content:'';position:absolute;inset:0 0 auto 0;height:4px;background:var(--c)}
.k-path:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(42,27,94,.12)}
.k-path .k-ic{width:30px;height:30px;color:var(--c)}
.k-path h3{margin:12px 0 2px;font-size:21px}.k-path .k-sub{margin:0 0 12px;color:var(--muted);font-size:14.5px}
.k-path ul{list-style:none;margin:0;padding:0;display:grid;gap:9px}
.k-path li{font-size:14.5px;line-height:1.7;color:var(--ink);display:flex;gap:8px;align-items:flex-start}
.k-path li:before{content:'';flex-shrink:0;width:6px;height:6px;border-radius:50%;margin-top:.75em;background:var(--c)}
.k-st{flex-shrink:0;margin-inline-start:auto;font-size:11.5px;font-weight:800;padding:1px 9px;border-radius:999px;white-space:nowrap;align-self:center}
.k-st.on{background:rgba(46,157,107,.13);color:#2E9D6B}.k-st.soon{background:rgba(240,122,74,.14);color:#D0602F}
@media (max-width:1000px){.k-paths{grid-template-columns:repeat(2,1fr)}}@media (max-width:620px){.k-paths{grid-template-columns:1fr}}
/* رحلة المعرفة: خط يمتلئ مع التمرير وعُقد تضيء */
.k-journey{position:relative;display:grid;grid-template-columns:repeat(6,1fr);gap:10px;max-width:1080px;margin:10px auto 0;padding-top:8px}
.k-journey:before,.k-journey .k-fill{content:'';position:absolute;top:38px;inset-inline:8%;height:3px;border-radius:3px;background:var(--line)}
.k-journey .k-fill{background:linear-gradient(90deg,var(--plum),var(--sun),var(--gold));transform-origin:right;transform:scaleX(var(--p,0));transition:transform .15s linear}
.k-node{position:relative;text-align:center;z-index:1}
.k-dot{width:62px;height:62px;margin:0 auto 12px;border-radius:50%;display:grid;place-items:center;background:var(--card);border:2px solid var(--line);color:var(--muted);transition:all .5s cubic-bezier(.2,.7,.2,1)}
.k-node.lit .k-dot{border-color:transparent;color:#fff;background:linear-gradient(140deg,var(--night),var(--plum),var(--sun));box-shadow:0 10px 28px rgba(142,58,140,.35);transform:scale(1.06)}
.k-node b{display:block;font-size:17px}.k-node span{display:block;color:var(--muted);font-size:13.5px;line-height:1.7;margin-top:2px}
@media (max-width:820px){.k-journey{grid-template-columns:1fr;gap:18px;padding-inline-start:4px}
.k-journey:before,.k-journey .k-fill{top:8px;bottom:8px;inset-inline:auto;inset-inline-start:30px;width:3px;height:auto}
.k-journey .k-fill{transform-origin:top;transform:scaleY(var(--p,0))}
.k-node{display:grid;grid-template-columns:62px 1fr;gap:14px;text-align:start;align-items:center}.k-dot{margin:0}}
/* المنظومة: إشراقة في المركز وأبعادها الستة حولها، تُرسم خطوطها عند الظهور */
.k-orbit{position:relative;max-width:760px;margin:24px auto 0;aspect-ratio:1/1}
.k-orbit svg.k-lines{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.k-orbit .k-lines path{fill:none;stroke:url(#kg);stroke-width:2px;vector-effect:non-scaling-stroke;stroke-linecap:round;opacity:0;transition:opacity 1.2s ease .2s}
.k-orbit.in .k-lines path{opacity:.75}
.k-core{position:absolute;left:50%;top:50%;width:30%;aspect-ratio:1/1;transform:translate(-50%,-50%);border-radius:50%;display:grid;place-items:center;text-align:center;color:#fff;
background:radial-gradient(circle at 35% 30%,var(--gold),var(--sun) 35%,var(--plum) 70%,var(--night));box-shadow:0 20px 60px rgba(240,122,74,.35);font-weight:900;font-size:clamp(15px,2.4vw,22px);line-height:1.5;padding:8px}
.k-dim{position:absolute;width:31%;transform:translate(-50%,-50%) scale(.9);opacity:0;text-align:center;transition:opacity .6s,transform .6s cubic-bezier(.2,.7,.2,1)}
.k-orbit.in .k-dim{opacity:1;transform:translate(-50%,-50%) scale(1)}
.k-dim .k-ic{width:40px;height:40px;padding:8px;border-radius:14px;background:var(--card);border:1px solid var(--line);color:var(--plum);box-shadow:0 8px 20px rgba(42,27,94,.08)}
.k-dim b{display:block;font-size:16px;margin-top:6px}.k-dim span{display:block;font-size:13px;color:var(--muted);line-height:1.65}
@media (max-width:640px){.k-orbit{aspect-ratio:auto;display:grid;grid-template-columns:1fr 1fr;gap:16px}.k-orbit svg.k-lines{display:none}
.k-core{position:static;transform:none;width:auto;aspect-ratio:auto;grid-column:1/-1;border-radius:22px;padding:18px}
.k-dim{position:static;width:auto;transform:none;opacity:1}.k-orbit.in .k-dim{transform:none}}
.k-motto{text-align:center;margin:30px auto 0;font-size:clamp(20px,2.6vw,27px);font-weight:900;line-height:1.7;background:linear-gradient(90deg,var(--plum),var(--sun));-webkit-background-clip:text;background-clip:text;color:transparent}
.k-text{max-width:780px;margin:0 auto;font-size:18px;line-height:2.05;color:var(--muted);text-wrap:pretty}
.k-text p{margin:0 0 16px}.k-text strong{color:var(--ink)}
/* المسيرة: خط يتقدّم مع التمرير */
.k-tl{position:relative;max-width:780px;margin:0 auto;padding-inline-start:46px}
.k-tl:before,.k-tl .k-fill{content:'';position:absolute;inset-inline-start:15px;top:10px;bottom:10px;width:3px;border-radius:3px;background:var(--line)}
.k-tl .k-fill{background:linear-gradient(var(--plum),var(--sun),var(--gold));transform-origin:top;transform:scaleY(var(--p,0))}
.k-step{position:relative;margin-bottom:30px}
.k-step:before{content:'';position:absolute;inset-inline-start:-40px;top:6px;width:18px;height:18px;border-radius:50%;background:var(--cream);border:3px solid var(--line);transition:all .45s}
.k-step.lit:before{border-color:var(--sun);background:var(--sun);box-shadow:0 0 0 6px rgba(240,122,74,.18)}
.k-step time{display:inline-block;font-weight:900;font-size:14px;color:var(--sun);letter-spacing:.3px}
.k-step b{display:block;font-size:19px;margin:2px 0 4px;color:var(--ink)}.k-step p{margin:0;color:var(--muted);font-size:16.5px;line-height:1.95}
.k-two{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:960px;margin:0 auto}
.k-col{padding:26px 24px;border-radius:24px;background:var(--card);border:1px solid var(--line)}
.k-col h3{margin:0 0 12px;font-size:20px;display:flex;align-items:center;gap:10px}
.k-col ul{margin:0;padding:0;list-style:none;display:grid;gap:10px}.k-col li{color:var(--muted);font-size:15.5px;line-height:1.75;padding-inline-start:18px;position:relative}
.k-col li:before{content:'';position:absolute;inset-inline-start:0;top:.7em;width:7px;height:7px;border-radius:50%;background:var(--c)}
@media (max-width:760px){.k-two{grid-template-columns:1fr}}
/* افتتاحية الرئيسية: حروف تتجمع كتابًا ثم تصعد نورًا */
#k-intro{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:1}
@media (prefers-reduced-motion:reduce){.k-orbit .k-lines path{transition:none;opacity:.75}.k-dim,.k-dot,.k-step:before,.k-path{transition:none}#k-intro{display:none}}
"""

JS = """<script>
/* k2i: خطوط تمتلئ مع التمرير، وعُقد تضيء حين يصلها الخط */
(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
function track(box,items,vertical){
  function f(){var r=box.getBoundingClientRect(),vh=innerHeight;
    var p=rm?1:Math.min(1,Math.max(0,(vh*0.75-r.top)/(r.height||1)));
    box.style.setProperty('--p',p.toFixed(3));
    items.forEach(function(n,i){var lim=(i+0.35)/items.length;n.classList.toggle('lit',p>=lim||rm)});}
  addEventListener('scroll',f,{passive:true});addEventListener('resize',f);f();}
document.querySelectorAll('.k-journey').forEach(function(b){track(b,[].slice.call(b.querySelectorAll('.k-node')))});
document.querySelectorAll('.k-tl').forEach(function(b){track(b,[].slice.call(b.querySelectorAll('.k-step')))});
var o=document.querySelectorAll('.k-orbit');
if(rm||!('IntersectionObserver' in window)){o.forEach(function(e){e.classList.add('in')});}
else{var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{threshold:.25});o.forEach(function(e){io.observe(e)});}
})();
</script>"""

INTRO_JS = r"""<script>
/* k2i: افتتاحية — حروف متناثرة تتجمع في كتاب مفتوح يُرسم بالنور، ثم يذوب المشهد صاعدًا فتظهر الصفحة.
   مرة واحدة في الجلسة، نحو ثانيتين، وتُتخطّى بلمسة؛ لا تعمل مع «تقليل الحركة». */
(function(){
if(matchMedia('(prefers-reduced-motion: reduce)').matches)return;
try{if(sessionStorage.getItem('k-intro'))return;sessionStorage.setItem('k-intro','1')}catch(e){}
var hero=document.querySelector('header.hero');if(!hero)return;
var cv=document.createElement('canvas');cv.id='k-intro';cv.setAttribute('aria-hidden','true');
cv.style.cssText='position:absolute;inset:0;width:100%;height:100%;z-index:50;cursor:pointer;pointer-events:auto';
hero.appendChild(cv);
var cx=cv.getContext('2d'),dpr=Math.min(2,devicePixelRatio||1),W,H,pts=[],lines=[],t0=null,skip=false;
var L='ابتثجحخدذرزسشصضطظعغفقكلمنهوي';
cv.addEventListener('click',function(){skip=true});
function size(){var r=hero.getBoundingClientRect();W=r.width;H=r.height;cv.width=W*dpr;cv.height=H*dpr;cx.setTransform(dpr,0,0,dpr,0,0)}
function build(){
  var s=Math.min(W*0.26,H*0.42,250),c={x:W/2,y:H*0.46},h=s*0.66;
  function P(x,y){return {x:c.x+x,y:c.y+y}}
  function top(side,u){return P(side*u*s,-h/2-Math.sin(u*Math.PI)*s*0.09)}
  function bot(side,u){return P(side*u*s,h/2-Math.sin(u*Math.PI)*s*0.05)}
  for(var side=-1;side<=1;side+=2){
    var t=[],b=[],o=[];
    for(var i=0;i<=24;i++){t.push(top(side,i/24));b.push(bot(side,i/24))}
    var a=top(side,1),z=bot(side,1);for(var j=0;j<=10;j++)o.push({x:a.x+(z.x-a.x)*j/10,y:a.y+(z.y-a.y)*j/10});
    lines.push(t,b,o);
    for(var k=1;k<=5;k++){var row=[],yy=-h/2+k*h/6.2;for(var m=2;m<=10;m++){var u=m/12;row.push(P(side*u*s,yy-Math.sin(u*Math.PI)*s*0.05+0.01*s))}lines.push(row)}
  }
  var sp=[];for(var q=0;q<=12;q++)sp.push(P(0,-h/2+q*h/12));lines.push(sp);
  lines.forEach(function(l){l.forEach(function(p){
    var ang=Math.random()*Math.PI*2,d=Math.max(W,H)*(0.3+Math.random()*0.55);
    pts.push({sx:p.x+Math.cos(ang)*d,sy:p.y+Math.sin(ang)*d,tx:p.x,ty:p.y,ch:L[(Math.random()*L.length)|0],d:Math.random()*0.3,r:40+Math.random()*120})})});
}
function E(t){return 1-Math.pow(1-t,3)}
function frame(ts){if(t0===null)t0=ts;var t=(ts-t0)/1000;
  var gather=1.1,hold=0.55,fade=0.75;if(skip&&t<gather+hold){t0=ts-(gather+hold)*1000;t=gather+hold}
  var end=gather+hold+fade,f=Math.max(0,(t-gather-hold)/fade);
  cx.clearRect(0,0,W,H);
  /* ستارة بلون الفجر تذوب في النهاية فتظهر الصفحة تحتها */
  var g=cx.createLinearGradient(0,0,W,H);g.addColorStop(0,'#1d1342');g.addColorStop(.6,'#3a1f5e');g.addColorStop(1,'#5a2a5c');
  cx.globalAlpha=1-E(f);cx.fillStyle=g;cx.fillRect(0,0,W,H);
  var morph=Math.min(1,Math.max(0,(t-gather*0.7)/0.5));
  /* الكتاب يُرسم بالنور حين تكتمل الحروف */
  if(morph>0){cx.globalAlpha=morph*(1-f);cx.strokeStyle='#FFC978';cx.lineWidth=1.6;cx.shadowColor='rgba(255,181,71,.8)';cx.shadowBlur=14;
    lines.forEach(function(l){cx.beginPath();l.forEach(function(p,i){var y=p.y-(f>0?60*E(f):0);if(i)cx.lineTo(p.x,y);else cx.moveTo(p.x,y)});cx.stroke()});cx.shadowBlur=0}
  for(var i=0;i<pts.length;i++){var p=pts[i],k=Math.min(1,Math.max(0,(t-p.d)/gather)),e=E(k);
    var x=p.sx+(p.tx-p.sx)*e,y=p.sy+(p.ty-p.sy)*e,a=Math.min(1,k*1.8)*(1-f);
    if(f>0)y-=p.r*E(f);
    if(a<=0.01)continue;cx.globalAlpha=a;
    if(morph<1){cx.fillStyle='rgba(255,236,210,'+(0.9*(1-morph))+')';cx.font='600 14px Cairo,Tahoma,sans-serif';cx.fillText(p.ch,x-4,y+5)}
    if(morph>0){cx.fillStyle='rgba(255,214,150,'+morph+')';cx.beginPath();cx.arc(x,y,1.3,0,Math.PI*2);cx.fill()}}
  cx.globalAlpha=1;
  if(t<end)requestAnimationFrame(frame);else cv.remove()}
size();build();requestAnimationFrame(frame);
})();
</script>"""


def path_card(c, icon, title, tagline, items):
    lis = ''.join(f'<li><span>{t}</span><span class="k-st {"on" if s else "soon"}">{"متاح" if s else "مخطط له"}</span></li>'
                  for t, s in items)
    return (f'<article class="k-path rv" style="--c:{c}">{ic(icon)}<h3>{title}</h3><p class="k-sub">{tagline}</p>'
            f'<ul>{lis}</ul></article>')


HOME_SECTIONS = f"""
  <section class="{MARK}"><div class="wrap">
    <div class="k-idea rv"><span class="k-eyebrow">لماذا إشراقة؟</span>
      <p class="big">نعيش في عالم تتزايد فيه المعلومات، لكن الوصول إلى المعلومات لا يضمن الفهم، وكثرة المحتوى لا تعني دائمًا كثرة الإنتاج.</p>
      <p>نريد أن نساعد الناس على بناء علاقة أكثر فاعلية مع المعرفة؛ قراءةً وفهمًا ومشاركةً وتعاونًا.</p></div>
  </div></section>

  <section><div class="wrap">
    __STATS__
    <span class="k-eyebrow">منظومة إشراقة</span>
    <h2>مساحة واحدة، أربعة مسارات</h2>
    <p class="sub">ليست أربعة منتجات منفصلة، بل أجزاء من رحلة واحدة تبدأ بالقراءة.</p>
    <div class="k-paths">
      {path_card('#8E3A8C', 'book', 'اقرأ', 'المعرفة في متناولك، كل يوم.', [
          ('مكتبة من روائع الكتب بقارئ يحفظ صفحتك', True),
          ('مقال قصير موثّق كل يوم', True),
          ('«ذكّرني أين وصلت»: ما قرأته دون حرق ما بعده', True),
          ('حكمة يومية مع معناها وقصتها', True)])}
      {path_card('#2C6ED5', 'chat', 'شارك', 'تكبر الفكرة حين تُناقش.', [
          ('نوادي القراءة: تحدٍّ مشترك وحوار يصون متعة الاكتشاف', True),
          ('لقاءات وفعاليات النادي', True),
          ('تحدي المجتمعات: اقرأ باسم مدينتك وجامعتك', True)])}
      {path_card('#2E9D6B', 'build', 'تعلّم واصنع', 'من الفهم إلى ما يُبنى.', [
          ('نوادي المطوّرين: فرق صغيرة مع موجّه خبير', True),
          ('مشاريع مفتوحة المصدر ومعرض للمشاريع', True),
          ('منح وفرص دراسية من مصادرها الرسمية', True)])}
      {path_card('#E0672F', 'memory', 'احفظ الذاكرة', 'حكايات أهلنا لا تضيع.', [
          ('«صدى»: أمثال وحكايات بأصوات أهلها', True),
          ('«ثقافتك»: عادات المناطق وأكلاتها وحكاياتها', True),
          ('مكتبات تفاعلية مع المدارس والجمعيات', False)])}
    </div>
  </div></section>

  <section><div class="wrap">
    <span class="k-eyebrow">من المعرفة إلى الأثر</span>
    <h2>كيف تتحول صفحة إلى أثر؟</h2>
    <p class="sub">رحلة نمشيها معًا: كل خطوة تفتح الباب للتي بعدها.</p>
    <div class="k-journey" role="list"><div class="k-fill" aria-hidden="true"></div>
      <div class="k-node" role="listitem"><div class="k-dot">{ic('book')}</div><div><b>كتاب</b><span>تبدأ بصفحة</span></div></div>
      <div class="k-node" role="listitem"><div class="k-dot">{ic('idea')}</div><div><b>فكرة</b><span>تلمع وأنت تقرأ</span></div></div>
      <div class="k-node" role="listitem"><div class="k-dot">{ic('chat')}</div><div><b>حوار</b><span>تنضج حين تُناقش</span></div></div>
      <div class="k-node" role="listitem"><div class="k-dot">{ic('learn')}</div><div><b>تعلّم</b><span>يصير الحوار فهمًا مشتركًا</span></div></div>
      <div class="k-node" role="listitem"><div class="k-dot">{ic('team')}</div><div><b>تعاون</b><span>يلتقي أصحاب الاهتمام الواحد</span></div></div>
      <div class="k-node" role="listitem"><div class="k-dot">{ic('spark')}</div><div><b>أثر</b><span>مشروع أو مبادرة أو ذاكرة تُحفظ</span></div></div>
    </div>
  </div></section>
"""


def home():
    p = ROOT / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('home: already applied'); return
    s = s.replace('<p class="lead">في زمنٍ يفيض بالمعرفة، تجمعك إشراقة يومية بالكتاب والنادي ومجتمعٍ يقرأ ويتحاور وينتج.</p>',
                  '<p class="lead">ليست المعرفة ما نقرؤه فقط، بل ما نفهمه، وما نتشاركه، وما نستطيع أن نبنيه معًا. اكتشف مساحة تبدأ بالقراءة وتتسع للأفكار والمجتمعات والمشاريع.</p>', 1)
    # قسم «ما الذي ينتظرك» (رموز تعبيرية) يحل محله: الفكرة + المنظومة + الرحلة، مع إبقاء شريط الأرقام
    m = re.search(r'\n  <section>\s*<div class="wrap">\s*(<div class="stats rv".*?</div></div>)\s*<h2>ما الذي ينتظرك في إشراقة</h2>.*?</section>\n', s, re.S)
    assert m, 'features section not found'
    s = s[:m.start()] + HOME_SECTIONS.replace('__STATS__', m.group(1)) + s[m.end():]
    s = s.replace('<h2>من ذاكرة الماضي إلى احتمالات المستقبل، اقرأ معنا</h2>\n      <p class="sub">حمّل إشراقة يومية وابدأ مع ناديك اليوم.</p>',
                  '<h2>المعرفة تكبر عندما تجد من يشاركها</h2>\n      <p class="sub">حمّل إشراقة يومية، وابدأ بكتاب أو نادٍ أو فكرة.</p>', 1)
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + INTRO_JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('home: ok')


DIMS = [  # (أيقونة، البعد، وصف) — الزاوية تُحسب
    ('human', 'الإنسان', 'المعرفة وسيلة لتوسيع الفهم والإمكانات'),
    ('book', 'المعرفة', 'قراءة وفهم وتأمل وتعلّم مستمر'),
    ('team', 'المجتمع', 'لقاء من تجمعهم اهتمامات مشتركة'),
    ('build', 'الإنتاج', 'تحويل التعلّم إلى مشاريع ومبادرات'),
    ('memory', 'الثقافة والذاكرة', 'حفظ الحكايات والأمثال والمعارف المحلية'),
    ('chip', 'التقنية', 'أدوات تسهّل الوصول والمشاركة والتعاون'),
]


def orbit():
    import math
    # حلقة تصل الأبعاد الستة، وأشعة قصيرة من المركز إلى كل بعد (خطوط رفيعة لا تتأثر بتمدد الشكل)
    dims = ''
    lines = ''
    for k, (i_, t, d) in enumerate(DIMS):
        a = -math.pi / 2 + k * 2 * math.pi / len(DIMS)
        x, y = 50 + 38 * math.cos(a), 50 + 38 * math.sin(a)
        sx, sy = 50 + 18 * math.cos(a), 50 + 18 * math.sin(a)
        lx, ly = 50 + 25 * math.cos(a), 50 + 25 * math.sin(a)
        lines += f'<path d="M{sx:.1f} {sy:.1f} L{lx:.1f} {ly:.1f}"/>'
    lines = dims + lines
    dims = ''
    for k, (i_, t, d) in enumerate(DIMS):
        a = -math.pi / 2 + k * 2 * math.pi / len(DIMS)
        x, y = 50 + 38 * math.cos(a), 50 + 38 * math.sin(a)
        dims += (f'<div class="k-dim" style="left:{x:.1f}%;top:{y:.1f}%;transition-delay:{0.25 + k * 0.12:.2f}s">'
                 f'{ic(i_)}<b>{t}</b><span>{d}</span></div>')
    svg = ('<svg class="k-lines" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true"><defs>'
           '<linearGradient id="kg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="100" y2="100"><stop offset="0" stop-color="#8E3A8C"/>'
           '<stop offset="1" stop-color="#F07A4A"/></linearGradient></defs>' + lines + '</svg>')
    return (f'<div class="k-orbit" aria-label="أبعاد إشراقة الستة">{svg}'
            '<div class="k-core">من المعرفة<br>إلى الأثر</div>' + dims + '</div>')


TIMELINE = [
    ('2022', 'بداية التعلّم التقني',
     'بدأ سيف الدين أحمد رحلته في تطوير تطبيقات الهاتف: درس Flutter في دورة نادي مطوري Google بجامعة الخرطوم، '
     'والتحق بمنحة Google للمطورين في أفريقيا (GADS) في مسار أندرويد. كان مشروعه في الدورة تطبيقًا لقراءة الكتب، لم يُنشر يومها.'),
    ('2023', 'قارئٌ على جهاز واحد',
     'بدأت إشراقة تطبيقًا لقراءة الكتب على جهاز مؤسسها وحده. وفي سبتمبر انضم إلى نادي Candle للقراءة، '
     'النادي المجاني الذي أسسته لينة بشير موسى على واتساب، فصارت القراءة مع الآخرين جزءًا من الفكرة.'),
    ('نهاية 2024', 'بوتقة صغيرة',
     'اتسعت الفكرة لتضم الحِكم والمعلومات والكتب المختارة. ووقف إلى جانب المؤسس أخوه وزميله سعيد حسن، '
     'الداعم الأول في هذه المسيرة، فجعل ما بدا مستحيلًا ممكنًا.'),
    ('2025', 'أول نسخة في الاختبار',
     'وصلت النسخة الأولى إلى Google Play في مرحلة الاختبار، ثم توقف التطوير فترة.'),
    ('أبريل 2026', 'العودة برؤية أوسع',
     'عاد العمل على إشراقة لتكون أكثر من قارئ للكتب: مساحة تربط القراءة بالحوار والمجتمع والتعاون.'),
    ('أكتوبر 2026', 'إشراقة للجميع',
     'بعد اجتياز مرحلة الاختبار، أُطلقت إشراقة يومية للجميع على Google Play ومتجر Microsoft.'),
]


def sec(eyebrow, title, sub, body, cls=''):
    return (f'  <section{f" class={chr(34)}{cls}{chr(34)}" if cls else ""}><div class="wrap">'
            f'<span class="k-eyebrow">{eyebrow}</span><h2 class="rv">{title}</h2>'
            + (f'<p class="sub rv">{sub}</p>' if sub else '') + body + '</div></section>\n')


def about():
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('about: already applied'); return
    philosophy = sec('فلسفتنا', 'من المعرفة إلى الأثر', '', (
        '<div class="k-text rv"><p>نؤمن في إشراقة أن المعرفة لا ينبغي أن تنتهي عند الصفحة الأخيرة من الكتاب، ولا أن تبقى الأفكار حبيسة الشاشات. '
        'يمكن لفكرة أن تجمع أشخاصًا لم يلتقوا من قبل، وأن يتحول النقاش إلى تعلّم مشترك، وأن يصبح التعلّم بداية لمبادرة أو مشروع أو عمل يحفظ ذاكرة مجتمع.</p>'
        '<p>لهذا نبني إشراقة لتكون أكثر من مساحة للقراءة؛ نريدها بيئة يلتقي فيها الإنسان بالمعرفة، ويلتقي فيها أصحاب الاهتمامات المشتركة، '
        'وتجد فيها الأفكار فرصة للنمو والتطبيق والمشاركة.</p></div>'
        + orbit()
        + '<p class="k-motto rv">نقرأ لنتعلّم، ونتعلّم لنتشارك، ونتشارك لنصنع أثرًا.</p>'), cls=MARK)
    why = sec('البداية', 'لماذا بدأت إشراقة؟', '', (
        '<div class="k-text rv"><p>بدأت إشراقة من سؤال بسيط: لماذا نحمل في هواتفنا كل هذه المعرفة، ونجد صعوبة في أن نقرأ معًا، أو نتحاور، '
        'أو نبني شيئًا مما نتعلّمه؟</p>'
        '<p>الكاتب في بلد، والقارئ في بلد آخر، والمبرمج المبتدئ يتعلّم وحده، وكثير من مدارسنا وأحيائنا فقدت مكتباتها ونوادي القراءة والبرمجة فيها. '
        'وفي زمن تقودنا فيه الخوارزميات إلى ما نشاهد ونقرأ، أردنا مساحة تعيد للإنسان دوره كاملًا: <strong>أن يقرأ، ويفهم، ويشارك، ويبني.</strong></p></div>'))
    steps = ''.join(f'<div class="k-step"><time>{y}</time><b>{t}</b><p>{d}</p></div>' for y, t, d in TIMELINE)
    journey = sec('المسيرة', 'من قارئ على جهاز واحد، إلى مساحة للجميع', '',
                  f'<div class="k-tl"><div class="k-fill" aria-hidden="true"></div>{steps}</div>')
    today = sec('اليوم وغدًا', 'ما نقدّمه اليوم، وما نطمح إليه', 'نميّز بوضوح بين ما هو متاح الآن وما نعمل عليه.', (
        '<div class="k-two">'
        '<div class="k-col rv" style="--c:#2E9D6B"><h3>' + ic('spark') + 'متاح الآن</h3><ul>'
        '<li>مكتبة من روائع الكتب في الملكية العامة، بقارئ يحفظ صفحتك</li>'
        '<li>مقال قصير موثّق كل يوم، وحكمة مع معناها وقصتها</li>'
        '<li>نوادي القراءة: تحديات وحوار وتصويت ولقاءات</li>'
        '<li>نوادي المطوّرين ومعرض المشاريع المفتوحة المصدر</li>'
        '<li>«صدى» و«ثقافتك» لحفظ الحكايات والذاكرة المحلية</li>'
        '<li>على أندرويد وويندوز وآيفون وماك، مجانًا وبلا إعلانات</li>'
        '</ul></div>'
        '<div class="k-col rv" style="--c:#F07A4A"><h3>' + ic('idea') + 'نطمح إليه</h3><ul>'
        '<li>إشراقة في متجر App Store</li>'
        '<li>واجهة إنجليزية كاملة</li>'
        '<li>مكتبات تفاعلية مع المدارس والجمعيات الأدبية</li>'
        '<li>أن يساهم القارئ من أي مكان في بناء مكتبة حقيقية لأطفال مدينة أخرى</li>'
        '</ul></div></div>'))
    # الترتيب: الكلمة (كما هي) ← ما إشراقة؟ ← الفلسفة ← لماذا ← المسيرة (بدل القديمة) ← المبادئ ← اليوم وغدًا ← من داخل التطبيق ← المطوّر
    m_old = re.search(r'\s*<section><div class="wrap"><h2 class="rv">المسيرة</h2>.*?</section>\n', s, re.S)
    assert m_old, 'old timeline not found'
    s = s[:m_old.start()] + '\n' + s[m_old.end():]
    m_p = re.search(r'\s*<section><div class="wrap"><h2 class="rv">ما نؤمن به</h2>', s)
    assert m_p, 'principles not found'
    s = s[:m_p.start()] + '\n' + philosophy + why + journey + s[m_p.start():]
    m_g = re.search(r'\s*<section><div class="wrap"><h2 class="rv">من داخل التطبيق</h2>', s)
    assert m_g, 'gallery not found'
    s = s[:m_g.start()] + '\n' + today + s[m_g.start():]
    s = s.replace('<p>مؤسس أوتواكس للحلول الرقمية، ومطوّر إشراقة يومية منذ كانت فكرةً على هاتفه إلى أن صارت مجتمعًا للقراءة.</p>',
                  '<p>مطوّر إشراقة يومية ومؤسس أوتواكس للحلول الرقمية. بدأ رحلته مع البرمجة في 2022، ومع القراءة المشتركة في نادي Candle، '
                  'فجمع الطريقين في إشراقة: مساحة تبدأ بكتاب، وتتسع لتصير أثرًا.</p>', 1)
    # أيقونات خطية بدل الرموز التعبيرية في «ما نؤمن به»
    a = s.index('<h2 class="rv">ما نؤمن به</h2>')
    b = s.index('</section>', a)
    names = iter(['book', 'moon', 'search', 'team', 'code', 'lock'])
    blk = re.sub(r'<div class="i">[^<]*</div>', lambda _: '<div class="i">' + ic(next(names)) + '</div>', s[a:b])
    s = s[:a] + blk + s[b:]
    i = s.index('</style>')
    s = s[:i] + CSS + '.f .i .k-ic{width:30px;height:30px;color:var(--plum)}\n' + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('about: ok')


if __name__ == '__main__':
    home()
    about()
