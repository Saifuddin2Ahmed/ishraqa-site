"""«عن» v6 (10 أكتوبر 2026، طلب المؤسس):
١) كل بُعد من الستة يُفتح نافذةً فيها تأمّل معرفي قصير واقتباس، بدل الكلام الجامد.
٢) المطوّر: أيقونات (Google Play، LinkedIn، Facebook، GitHub، Kwegatta) بدل الأزرار النصية، وبلا «منذ كانت فكرة على هاتفه».
٣) بلا تكرار «جهاز واحد/هاتفه» في المسيرة.

    python tools/about_v6.py
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]
MARK = 'about-v6'

THOUGHTS = [
    ('الإنسان', 'لا نقرأ لنملأ رؤوسنا، بل لنتّسع. كل فكرة صادقة تزيح جدارًا في داخلنا، فنرى من أنفسنا ما لم نكن نراه، ونصير أقدر على أن نختار.',
     'ليس العلمُ ما حُفظ، العلمُ ما نفع.', 'الإمام الشافعي'),
    ('المعرفة', 'المعلومة تُجمع، أما المعرفة فتُبنى: سؤال يتبعه سؤال، وقراءة تصحّح أخرى، وتأمل يربط ما تفرّق. لذلك نحب القراءة البطيئة؛ ففيها تنضج الفكرة.',
     'قيمةُ كلِّ امرئٍ ما يُحسنه.', 'يُنسب إلى علي بن أبي طالب'),
    ('المجتمع', 'الفكرة التي تبقى معك وحدك تبقى صغيرة. حين تُقال في نادٍ، وتُختلف فيها الآراء، ويضيف إليها غيرك ما لم تره، تكبر وتصير ملكًا للجميع.',
     'إن أردت أن تسير سريعًا فسِر وحدك، وإن أردت أن تسير بعيدًا فسِر مع الآخرين.', 'مثل أفريقي'),
    ('الإنتاج', 'أن تقرأ عن الجسور شيء، وأن تبني جسرًا شيء آخر. المعرفة تكتمل حين تتحول إلى عمل: مقال يُكتب، أو مشروع يُبنى، أو مبادرة تمسّ حياة أحد.',
     'أفضل طريقة للتنبؤ بالمستقبل هي أن تخترعه.', 'آلان كاي'),
    ('الذاكرة', 'في المثل الذي تقوله جدّتك تاريخٌ كامل: طريقة عيش، وحكمة جيل، ولهجة مكان. ما لا نكتبه ونسمعه ونرويه ينطفئ، وما نحفظه يصير جسرًا بين من كانوا ومن سيأتون.',
     'حين يموت شيخ في أفريقيا، تحترق مكتبة.', 'أمادو هامباتي با'),
    ('التقنية', 'التقنية ليست الغاية، بل الطريق الذي يقرّب الكتاب من القارئ، والقارئ من القارئ. نختار منها ما يفتح الأبواب، ونترك ما يسرق الانتباه.',
     'هذا للجميع.', 'تيم بيرنرز-لي، مخترع الويب'),
]

IC = {  # أيقونات الروابط (24×24)
    'play': '<path fill="currentColor" d="M6 3.2v17.6c0 .8.9 1.3 1.6.9l14.1-8.8c.6-.4.6-1.4 0-1.8L7.6 2.3C6.9 1.9 6 2.4 6 3.2z"/>',
    'in': '<path fill="currentColor" d="M20.4 20.4h-3.6v-5.6c0-1.3 0-3-1.9-3s-2.1 1.4-2.1 2.9v5.7H9.3V9h3.4v1.6h.1a3.8 3.8 0 0 1 3.4-1.9c3.6 0 4.3 2.4 4.3 5.5zM5.3 7.4a2.1 2.1 0 1 1 0-4.2 2.1 2.1 0 0 1 0 4.2zM7.1 20.4H3.5V9h3.6zM22.2 0H1.8C.8 0 0 .8 0 1.7v20.6c0 .9.8 1.7 1.8 1.7h20.4c1 0 1.8-.8 1.8-1.7V1.7C24 .8 23.2 0 22.2 0z"/>',
    'fb': '<path fill="currentColor" d="M13.5 21.9v-7.4H16l.4-2.9h-2.9V9.8c0-.8.2-1.4 1.4-1.4h1.6V5.8a21 21 0 0 0-2.3-.1c-2.3 0-3.8 1.4-3.8 3.9v2H8v2.9h2.4v7.4a10 10 0 1 1 3.1 0z"/>',
    'gh': '<path fill="currentColor" d="M12 .3a12 12 0 0 0-3.8 23.4c.6.1.8-.3.8-.6v-2.2c-3.3.7-4-1.4-4-1.4-.6-1.4-1.4-1.8-1.4-1.8-1.1-.7.1-.7.1-.7 1.2.1 1.8 1.2 1.8 1.2 1.1 1.8 2.8 1.3 3.5 1 .1-.8.4-1.3.8-1.6-2.7-.3-5.5-1.3-5.5-5.9 0-1.3.5-2.4 1.2-3.2-.1-.3-.5-1.5.1-3.2 0 0 1-.3 3.3 1.2a11.5 11.5 0 0 1 6 0c2.3-1.5 3.3-1.2 3.3-1.2.7 1.7.2 2.9.1 3.2.8.8 1.2 1.9 1.2 3.2 0 4.6-2.8 5.6-5.5 5.9.4.4.8 1.1.8 2.2v3.3c0 .3.2.7.8.6A12 12 0 0 0 12 .3"/>',
    'kw': '<g fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><circle cx="7" cy="8" r="3"/><circle cx="17" cy="8" r="3"/><path d="M2.5 20a4.5 4.5 0 0 1 9 0M12.5 20a4.5 4.5 0 0 1 9 0M10 8h4"/></g>',
}
LINKS = [('play', 'تطبيقاته على Google Play', 'https://play.google.com/store/apps/dev?id=6759566582761793518'),
         ('in', 'LinkedIn', 'https://www.linkedin.com/in/saifuddin2ahmed'),
         ('fb', 'Facebook', 'https://www.facebook.com/Saifuddin2Ahmed'),
         ('gh', 'GitHub', 'https://github.com/Saifuddin2Ahmed'),
         ('kw', 'Kwegatta: لنبنِ ونتعلّم معًا', 'https://kwegatta.ai.studio/#/u/6X3HptD8tna8ehAkmIiEzB9QWuT2')]

CSS = """
/* ── about v6: نوافذ الأبعاد، وأيقونات المطوّر ── */
.kd-card{cursor:pointer}
.kd-card:focus-visible{outline:3px solid var(--sun);outline-offset:4px}
.kd-card .kd-more{position:absolute;bottom:16px;inset-inline-end:18px;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;
background:linear-gradient(140deg,var(--plum),var(--sun));color:#fff;font-size:20px;line-height:1;transition:transform .3s}
.kd-card:hover .kd-more{transform:rotate(90deg) scale(1.08)}
dialog.kdlg{border:0;padding:0;border-radius:28px;max-width:min(620px,92vw);width:100%;background:var(--card);color:var(--ink);box-shadow:0 40px 100px rgba(14,10,28,.45);overflow:hidden}
dialog.kdlg::backdrop{background:rgba(14,10,28,.55);backdrop-filter:blur(6px)}
dialog.kdlg[open]{animation:kdin .45s cubic-bezier(.2,.8,.2,1)}
@keyframes kdin{from{opacity:0;transform:translateY(24px) scale(.96)}}
.kdlg-top{position:relative;padding:34px 30px 26px;color:#fff;background:linear-gradient(135deg,var(--night),var(--plum) 60%,var(--sun))}
.kdlg-top span{font-weight:900;font-size:16px;letter-spacing:3px;color:var(--gold)}
.kdlg-top h3{margin:4px 0 0;font-size:clamp(34px,5vw,48px);line-height:1.2}
.kdlg-x{position:absolute;top:16px;inset-inline-end:16px;width:40px;height:40px;border-radius:50%;border:0;background:rgba(255,255,255,.18);color:#fff;font-size:22px;cursor:pointer}
.kdlg-body{padding:26px 30px 32px}
.kdlg-body p{margin:0 0 22px;font-size:19px;line-height:2;color:var(--ink)}
.kdlg-body blockquote{margin:0;padding:18px 22px;border-radius:18px;background:var(--cream);border-inline-start:4px solid var(--sun);font-size:20px;font-weight:700;line-height:1.8}
.kdlg-body cite{display:block;margin-top:8px;font-style:normal;font-size:14px;color:var(--sun);font-weight:700}
.ab-dev .icons{display:flex;flex-wrap:wrap;gap:12px;margin-top:18px}
.ab-dev .icons a{width:50px;height:50px;border-radius:16px;display:grid;place-items:center;background:var(--card);border:1px solid var(--line);color:var(--ink);transition:transform .25s,background .25s,color .25s,box-shadow .25s}
.ab-dev .icons a svg{width:23px;height:23px}
.ab-dev .icons a:hover{transform:translateY(-4px);color:#fff;background:linear-gradient(140deg,var(--plum),var(--sun));box-shadow:0 12px 26px rgba(240,122,74,.35)}
@media (max-width:760px){.ab-dev .icons{justify-content:center}}
@media (prefers-reduced-motion:reduce){dialog.kdlg[open]{animation:none}}
"""

JS = """<script>
/* about v6: كل بُعد يُفتح نافذةً */
(function(){
var dlg=document.querySelector('dialog.kdlg');if(!dlg||!dlg.showModal)return;
var data=JSON.parse(dlg.dataset.t),h=dlg.querySelector('h3'),n=dlg.querySelector('.kdlg-top span'),p=dlg.querySelector('.kdlg-body p'),q=dlg.querySelector('blockquote span'),c=dlg.querySelector('cite');
document.querySelectorAll('.kd-card').forEach(function(card,i){
  card.setAttribute('role','button');card.setAttribute('tabindex','0');card.setAttribute('aria-haspopup','dialog');
  var open=function(){var d=data[i];n.textContent='0'+(i+1);h.textContent=d[0];p.textContent=d[1];q.textContent='«'+d[2]+'»';c.textContent='— '+d[3];dlg.showModal()};
  card.addEventListener('click',open);card.addEventListener('keydown',function(e){if(e.key==='Enter'||e.key===' '){e.preventDefault();open()}});
});
dlg.querySelector('.kdlg-x').addEventListener('click',function(){dlg.close()});
dlg.addEventListener('click',function(e){if(e.target===dlg)dlg.close()});
})();
</script>"""


def main():
    import html
    import json
    p = ROOT / 'about' / 'index.html'
    s = p.read_text(encoding='utf-8')
    if MARK in s:
        print('about: already v6'); return
    # إشارة «+» على كل بطاقة، ونافذة واحدة تُملأ حسب البطاقة
    s = re.sub(r'(<article class="kd-card"[^>]*>)', r'\1<i class="kd-more" aria-hidden="true">+</i>', s)
    data = html.escape(json.dumps(THOUGHTS, ensure_ascii=False), quote=True)
    dlg = (f'<dialog class="kdlg {MARK}" aria-label="تأمّل" data-t="{data}"><div class="kdlg-top"><button class="kdlg-x" type="button" aria-label="إغلاق">×</button>'
           '<span></span><h3></h3></div><div class="kdlg-body"><p></p><blockquote><span></span><cite></cite></blockquote></div></dialog>')
    s = s.replace('<p class="ab-motto"', dlg + '<p class="ab-motto"', 1)
    # المطوّر: أيقونات، وبلا تكرار «هاتفه»
    s = s.replace('<p>مطوّر إشراقة يومية منذ كانت فكرةً على هاتفه، إلى أن صارت مجتمعًا للقراءة.</p>', '')
    icons = ''.join(f'<a href="{u}" rel="me noopener" target="_blank" aria-label="{t}" title="{t}"><svg viewBox="0 0 24 24" aria-hidden="true">{IC[k]}</svg></a>'
                    for k, t, u in LINKS)
    s = re.sub(r'<div class="links">.*?</div>', f'<div class="icons">{icons}</div>', s, count=1, flags=re.S)
    # المسيرة بلا تكرار «جهاز واحد»
    s = s.replace('<h2>من قارئ على جهاز واحد، إلى مساحة للجميع</h2>', '<h2>حكاية إشراقة</h2>')
    s = s.replace('<b>قارئٌ على جهاز واحد</b><p>صارت إشراقة قارئ كتب على جهاز مؤسسها وحده. وفي سبتمبر',
                  '<b>قارئ الكتب</b><p>صارت الفكرة قارئًا للكتب. وفي سبتمبر')
    i = s.index('</style>')
    s = s[:i] + CSS + s[i:]
    j = s.rindex('</body>')
    s = s[:j] + JS + '\n' + s[j:]
    p.write_text(s, encoding='utf-8')
    print('about: v6 ok')


if __name__ == '__main__':
    main()
