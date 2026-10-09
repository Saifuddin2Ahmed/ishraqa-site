"""«عن إشراقة» بعرض جديد لكل قسم (10 أكتوبر 2026، طلب المؤسس) + حذف شاشات «من داخل التطبيق» من صفحة المطوّرين.

الكلمة: كلمات تضيء مع التمرير ← رزمة الصفحات (كما هي) ← «نقرأ لنتعلّم…» ثلاثة أسطر متتابعة ←
«لماذا بدأت؟» عنوان ثابت وجمل قصيرة تمر ← المسيرة (كما هي، 2022 بلا ذكر الدورة) ← «ما نؤمن به» صفوف مرقّمة ←
المطوّر: صورة كبيرة بإطار الفجر ونصه القديم.

    python tools/about_v5.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'about-v5'

PRINCIPLES = [('المعرفة للجميع', 'المحتوى الأساسي مجاني دائمًا، بلا إعلانات ولا بيع للبيانات.'),
              ('الهدوء لا الضجيج', 'نقيس النجاح بالدقائق المقروءة، لا بالوقت المهدور.'),
              ('الدقة', 'كل حكمة منسوبة لقائلها، وكل مقال بمصادره.'),
              ('المجتمع أولًا', 'القارئ شريك: يقترح ويكتب ويقود ناديه.'),
              ('الانفتاح', 'نوادي المطوّرين تنتج مصادر مفتوحة للعالم.'),
              ('الخصوصية', 'أقل قدر من البيانات، والانتماء لا يظهر إلا مجمّعًا.')]

CSS = """
/* ── about v5 ── */
.ab-scrub{max-width:980px;margin:0 auto;font-size:clamp(26px,3.6vw,46px);line-height:1.75;font-weight:800;text-align:center;color:var(--ink);text-wrap:balance}
.ab-scrub .sw{opacity:.14;transition:opacity .25s linear}.ab-scrub .sw.lit{opacity:1}
.ab-big{display:block;margin-top:30px;font-size:clamp(30px,4.6vw,60px);font-weight:900;line-height:1.5;background:linear-gradient(90deg,var(--plum),var(--sun),var(--gold));-webkit-background-clip:text;background-clip:text;color:transparent}
.ab-motto{display:grid;gap:6px;justify-items:center;margin:20px 0 0;font-size:clamp(30px,5vw,64px);font-weight:900;line-height:1.35}
.ab-motto span{opacity:0;transform:translateY(30px);transition:opacity .9s cubic-bezier(.2,.7,.2,1),transform .9s cubic-bezier(.2,.7,.2,1)}
.ab-motto span:nth-child(2){transition-delay:.25s;color:var(--plum)}.ab-motto span:nth-child(3){transition-delay:.5s;background:linear-gradient(90deg,var(--sun),var(--gold));-webkit-background-clip:text;background-clip:text;color:transparent}
.ab-motto.in span{opacity:1;transform:none}
.ab-why{display:grid;grid-template-columns:.85fr 1.15fr;gap:60px;align-items:start;max-width:1100px;margin:0 auto}
.ab-why h2{position:sticky;top:30vh;text-align:start;font-size:clamp(34px,4.4vw,58px);line-height:1.35;margin:0}
.ab-why h2 em{font-style:normal;background:linear-gradient(90deg,var(--plum),var(--sun));-webkit-background-clip:text;background-clip:text;color:transparent}
.ab-lines{display:grid;gap:22vh;padding:8vh 0 14vh}
.ab-lines p{margin:0;font-size:clamp(22px,2.6vw,32px);line-height:1.8;font-weight:700;color:var(--ink);opacity:.18;transition:opacity .6s}
.ab-lines p.lit{opacity:1}.ab-lines strong{color:var(--sun)}
@media (max-width:820px){.ab-why{grid-template-columns:1fr;gap:10px}.ab-why h2{position:static;text-align:center}.ab-lines{gap:40px;padding:20px 0}.ab-lines p{text-align:center}}
.ab-rows{max-width:1000px;margin:0 auto;border-top:1px solid var(--line)}
.ab-row{display:grid;grid-template-columns:90px 1fr 1.4fr;gap:24px;align-items:center;padding:26px 10px;border-bottom:1px solid var(--line);position:relative;overflow:hidden}
.ab-row:before{content:'';position:absolute;inset:0;background:linear-gradient(90deg,transparent,rgba(240,122,74,.08));transform:scaleX(0);transform-origin:right;transition:transform .5s cubic-bezier(.2,.7,.2,1)}
.ab-row:hover:before{transform:scaleX(1)}
.ab-row span{font-size:46px;font-weight:900;line-height:1;color:transparent;-webkit-text-stroke:1.5px var(--sun)}
.ab-row b{font-size:clamp(20px,2.2vw,26px);position:relative}.ab-row p{margin:0;color:var(--muted);font-size:17px;position:relative}
@media (max-width:700px){.ab-row{grid-template-columns:60px 1fr;gap:6px 14px}.ab-row p{grid-column:2}.ab-row span{font-size:34px;grid-row:span 2}}
.ab-dev{display:grid;grid-template-columns:auto 1fr;gap:46px;align-items:center;max-width:960px;margin:0 auto}
.ab-ph{position:relative;width:min(300px,70vw);aspect-ratio:1/1}
.ab-ph:before{content:'';position:absolute;inset:-14px;border-radius:50% 50% 46% 54%/55% 45% 55% 45%;background:conic-gradient(from 120deg,var(--gold),var(--sun),var(--plum),var(--night),var(--gold));filter:blur(.5px);animation:morph 12s ease-in-out infinite}
.ab-ph img{position:relative;width:100%;height:100%;object-fit:cover;border-radius:50% 50% 46% 54%/55% 45% 55% 45%;border:6px solid var(--cream);animation:morph 12s ease-in-out infinite}
@keyframes morph{50%{border-radius:46% 54% 52% 48%/48% 56% 44% 52%}}
.ab-dev h3{margin:0;font-size:clamp(28px,3.4vw,40px)}.ab-dev .t{color:var(--sun);font-weight:800;margin:6px 0 14px}
.ab-dev p{color:var(--muted);font-size:18px;line-height:1.95;margin:0 0 20px}
.ab-dev .links{display:flex;flex-wrap:wrap;gap:10px}
.ab-dev .links a{padding:9px 18px;border-radius:999px;border:1px solid var(--line);background:var(--card);text-decoration:none;font-weight:700;color:var(--ink);font-size:14.5px}
.ab-dev .links a:hover{border-color:var(--sun)}
@media (max-width:760px){.ab-dev{grid-template-columns:1fr;text-align:center;justify-items:center;gap:26px}.ab-dev .links{justify-content:center}}
@media (prefers-reduced-motion:reduce){.ab-scrub .sw,.ab-lines p{opacity:1}.ab-motto span{opacity:1;transform:none;transition:none}.ab-ph:before,.ab-ph img{animation:none}}
"""

JS = """<script>
/* about v5: كلمات تضيء مع التمرير، وجمل تمر، وسطور الشعار */
(function(){
var rm=matchMedia('(prefers-reduced-motion: reduce)').matches;
var sc=document.querySelector('.ab-scrub');
if(sc&&!rm){var ws=[];
  [].slice.call(sc.childNodes).forEach(function(node){if(node.nodeType!==3)return;var f=document.createDocumentFragment();
    node.textContent.split(/(\\s+)/).forEach(function(p){if(!p)return;if(/^\\s+$/.test(p)){f.appendChild(document.createTextNode(p));return}
      var s=document.createElement('span');s.className='sw';s.textContent=p;ws.push(s);f.appendChild(s)});sc.replaceChild(f,node)});
  var up=function(){var r=sc.getBoundingClientRect(),p=Math.min(1,Math.max(0,(innerHeight*0.85-r.top)/(r.height+innerHeight*0.35)));
    var n=Math.round(p*ws.length);ws.forEach(function(w,i){w.classList.toggle('lit',i<n)})};
  addEventListener('scroll',up,{passive:true});up()}
var lines=[].slice.call(document.querySelectorAll('.ab-lines p'));
if(lines.length&&!rm){var f=function(){lines.forEach(function(l){var r=l.getBoundingClientRect(),c=r.top+r.height/2;l.classList.toggle('lit',c<innerHeight*0.7&&c>innerHeight*0.12)})};
  addEventListener('scroll',f,{passive:true});f()}
var mo=document.querySelector('.ab-motto');
if(mo){if(rm||!('IntersectionObserver' in window))mo.classList.add('in');
  else new IntersectionObserver(function(es,o){if(es[0].isIntersecting){mo.classList.add('in');o.disconnect()}},{threshold:.4}).observe(mo)}
})();
</script>"""


def about():
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('about: already v5'); return
    deck = re.search(r'<div class="kd k2i-v3".*?</article></div></div></div>', s, re.S).group(0)
    kh = re.search(r'<section class="kh k2i-v2".*?</section>', s, re.S).group(0)
    kh = kh.replace('في دورة Flutter مع نادي مطوري Google بجامعة الخرطوم، صمّم سيف الدين تطبيقًا لقراءة الكتب. لم يُنشر يومها، لكن الفكرة بقيت تنتظر وقتها.',
                    'تطبيق لقراءة الكتب صمّمه سيف الدين بـ Flutter. لم يُنشر يومها، لكن الفكرة بقيت تنتظر وقتها.')
    rows = ''.join(f'<div class="ab-row rv"><span>0{i + 1}</span><b>{t}</b><p>{d}</p></div>' for i, (t, d) in enumerate(PRINCIPLES))
    main = f"""<main class="{MARK}">
  <section><div class="wrap"><p class="ab-scrub">إشراقة لحظةٌ تتّسع فيها الرؤية؛ حين تقودنا فكرةٌ إلى فهمٍ جديد، أو تفتح لنا المعرفة أفقًا لم نكن نراه. ما نعرفه يؤثر فيما نختار، وما نختاره يرسم ما نصير إليه. والمعرفة لا ينبغي أن تنتهي عند الصفحة الأخيرة من الكتاب.</p>
  <span class="ab-big" style="text-align:center">أن نرى أبعد، كلما عرفنا أكثر.</span></div></section>
  <section style="padding-top:20px"><div class="wrap">{deck}
  <p class="ab-motto" aria-label="نقرأ لنتعلّم، ونتعلّم لنتشارك، ونتشارك لنصنع أثرًا."><span>نقرأ لنتعلّم،</span><span>ونتعلّم لنتشارك،</span><span>ونتشارك لنصنع أثرًا.</span></p></div></section>
  <section><div class="wrap ab-why"><h2>لماذا بدأت <em>إشراقة</em>؟</h2><div class="ab-lines">
    <p>لماذا نحمل في هواتفنا كل هذه المعرفة، ونجد صعوبة في أن نقرأ معًا، أو نتحاور، أو نبني شيئًا مما نتعلّمه؟</p>
    <p>الكاتب في بلد، والقارئ في بلد آخر، والمبرمج يبني وحده.</p>
    <p>أردنا مساحة تعيد للإنسان دوره كاملًا: <strong>أن يقرأ، ويفهم، ويشارك، ويبني.</strong></p>
  </div></div></section>
  {kh}
  <section><div class="wrap"><h2 class="rv">ما نؤمن به</h2><div class="ab-rows">{rows}</div></div></section>
  <section><div class="wrap ab-dev rv"><div class="ab-ph"><img src="/img/developer.jpg" alt="م. سيف الدين أحمد" width="300" height="300" loading="lazy"></div>
    <div><h3>م. سيف الدين أحمد</h3><div class="t">مؤسس أوتواكس للحلول الرقمية</div>
    <p>مطوّر إشراقة يومية منذ كانت فكرةً على هاتفه، إلى أن صارت مجتمعًا للقراءة.</p>
    <div class="links"><a href="https://play.google.com/store/apps/dev?id=6759566582761793518" rel="me">تطبيقاته على Google Play</a><a href="https://www.linkedin.com/in/saifuddin2ahmed" rel="me">LinkedIn</a><a href="https://github.com/Saifuddin2Ahmed" rel="me">GitHub</a><a href="/contact/">تواصل معنا</a></div></div>
  </div></section>
"""
    a = s.index('<main')
    b = s.index('<section class="cta">')
    s = s[:a] + main + '\n  ' + s[b:]
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('about: v5 ok')


def developers():
    p = ROOT / 'developers' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if '<h2 class="rv">من داخل التطبيق</h2>' in s:
        a = s.index('<h2 class="rv">من داخل التطبيق</h2>')
        st = s.rindex('<section', 0, a)
        en = s.index('</section>', a) + len('</section>')
        s = s[:st] + s[en:]
        p.write_text(s, encoding='utf-8')
        print('developers: screens removed')


if __name__ == '__main__':
    about()
    developers()
