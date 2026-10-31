/* إشراقة · صفحة الدعم: النموذج يصل إلى صندوق الفريق في الاستوديو (جدول contact_messages، topic = support).
   تحقق في المتصفح، وحقل فخ، ومهلة دنيا قبل الإرسال؛ والخادم يضيف حدود الإرسال (ترحيل 146). */
(function () {
  var en = /^en/i.test(document.documentElement.lang);
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var $ = function (s, r) { return [].slice.call((r || document).querySelectorAll(s)); };
  var API = 'https://jytbowsfvuzdnsmhmsly.supabase.co/rest/v1/contact_messages';
  var KEY = 'sb_publishable_cm8SXt2NPRY5RY7dclZsLw_4ng3Q0TD';
  var WA = 'https://wa.me/249968033707';
  var T = en ? {
    name: 'Please write your name.',
    reach: 'Add a WhatsApp number or an email so we can reach you.',
    phone: 'Check the WhatsApp number, with the country code (e.g. +249…).',
    email: 'Check the email address.',
    prefWa: 'Add your WhatsApp number to be contacted on WhatsApp.',
    prefEm: 'Add your email to be contacted by email.',
    sending: 'Sending…', send: 'Send',
    rate: 'Several messages were sent in a short time. Please try again in an hour.',
    fail: 'We couldn\'t send it. Check your connection and try again, or ',
    failWa: 'message us on WhatsApp',
    kinds: { financial: 'Financial contribution', partner_org: 'Knowledge partner (organization)', partner_person: 'Knowledge partner (individual)', other: 'Other' },
    prefs: { whatsapp: 'WhatsApp', email: 'Email', meeting: 'A meeting' },
    lType: 'Type', lWa: 'WhatsApp', lEm: 'Email', lPref: 'Preferred contact', lPage: 'Page',
    thanks: function (n) { return 'Thank you' + (n ? ', ' + n : '') + '.'; },
    via: function (p) { return { whatsapp: 'The Ishraqa team will reach you on WhatsApp as soon as possible.', email: 'The Ishraqa team will reach you by email as soon as possible.', meeting: 'The Ishraqa team will reach you to arrange a meeting.' }[p] || 'The Ishraqa team will reach you as soon as possible.'; },
    waText: 'Hello, I\'d like to support Ishraqa Daily.'
  } : {
    name: 'اكتب اسمك من فضلك.',
    reach: 'أضف رقم واتساب أو بريدًا إلكترونيًا لنتواصل معك.',
    phone: 'تأكد من رقم واتساب مع رمز الدولة (مثل ‎+249…).',
    email: 'تأكد من البريد الإلكتروني.',
    prefWa: 'أضف رقم واتساب لنتواصل معك عبره.',
    prefEm: 'أضف بريدك لنتواصل معك عبره.',
    sending: 'جارٍ الإرسال…', send: 'أرسل',
    rate: 'أُرسلت رسائل كثيرة خلال وقت قصير، حاول بعد ساعة.',
    fail: 'تعذّر الإرسال، تحقق من الاتصال وحاول مجددًا، أو ',
    failWa: 'راسلنا على واتساب',
    kinds: { financial: 'مساهمة مالية', partner_org: 'شريك في المعرفة (مؤسسة)', partner_person: 'شريك في المعرفة (فرد)', other: 'أخرى' },
    prefs: { whatsapp: 'واتساب', email: 'البريد الإلكتروني', meeting: 'لقاء' },
    lType: 'النوع', lWa: 'واتساب', lEm: 'البريد', lPref: 'التواصل المفضّل', lPage: 'الصفحة',
    thanks: function (n) { return 'شكرًا لك' + (n ? ' يا ' + n : '') + '.'; },
    via: function (p) { return { whatsapp: 'وصلتنا رسالتك، وسيتواصل معك فريق إشراقة عبر واتساب في أقرب وقت.', email: 'وصلتنا رسالتك، وسيتواصل معك فريق إشراقة عبر البريد في أقرب وقت.', meeting: 'وصلتنا رسالتك، وسيتواصل معك فريق إشراقة لترتيب لقاء.' }[p] || 'وصلتنا رسالتك، وسيتواصل معك فريق إشراقة في أقرب وقت.'; },
    waText: 'مرحبًا، أودّ دعم إشراقة يومية.'
  };

  /* الظهور مع التمرير */
  var rv = $('.rv');
  if ('IntersectionObserver' in window && !rm) {
    var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } }); }, { threshold: .12 });
    rv.forEach(function (el) { io.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('in'); });

  var f = document.getElementById('sf');
  if (!f) return;
  var panel = f.closest('.panel'), btn = f.querySelector('button.go'), msg = document.getElementById('sm');
  var sub = document.getElementById('sub-partner'), t0 = Date.now();

  /* البطاقات الثلاث تختار النوع وتنقل إلى النموذج */
  var ways = $('.way');
  var pick = function (kind) {
    var r = f.querySelector('input[name=kind][value="' + kind + '"]'); if (r) { r.checked = true; sync(); }
  };
  var sync = function () {
    var k = (f.querySelector('input[name=kind]:checked') || {}).value;
    sub.hidden = k !== 'partner';
    ways.forEach(function (w) { w.setAttribute('aria-pressed', String(w.dataset.kind === k)); });
  };
  ways.forEach(function (w) {
    w.addEventListener('click', function () {
      pick(w.dataset.kind);
      document.getElementById('form').scrollIntoView({ behavior: rm ? 'auto' : 'smooth', block: 'start' });
      setTimeout(function () { f.elements.name.focus({ preventScroll: true }); }, rm ? 0 : 650);
    });
    w.addEventListener('pointermove', function (e) { var r = w.getBoundingClientRect();
      w.style.setProperty('--mx', (e.clientX - r.left) + 'px'); w.style.setProperty('--my', (e.clientY - r.top) + 'px'); });
  });
  $('input[name=kind]', f).forEach(function (r) { r.addEventListener('change', sync); });
  sync();

  var bad = function (el, on) { if (el) el.setAttribute('aria-invalid', on ? 'true' : 'false'); };
  var err = function (text, el, link) {
    msg.textContent = text;
    if (link) { var a = document.createElement('a'); a.href = link; a.target = '_blank'; a.rel = 'noopener'; a.textContent = T.failWa; msg.appendChild(a); msg.appendChild(document.createTextNode('.')); }
    msg.className = 'err on';
    if (el) { bad(el, true); el.focus(); }
  };
  $('input,textarea', f).forEach(function (el) { el.addEventListener('input', function () { bad(el, false); if (msg.className.indexOf('on') > -1 && !msg.querySelector('a')) msg.className = 'err'; }); });

  var digits = function (s) { var t = (s || '').trim(); return (t.charAt(0) === '+' ? '+' : '') + t.replace(/[^0-9]/g, ''); };

  f.addEventListener('submit', function (e) {
    e.preventDefault(); msg.className = 'err';
    var name = f.elements.name.value.trim(), phoneRaw = f.elements.phone.value.trim(), email = f.elements.email.value.trim();
    var text = f.elements.message.value.trim();
    var kind = (f.querySelector('input[name=kind]:checked') || {}).value || 'other';
    if (kind === 'partner') kind = (f.querySelector('input[name=who]:checked') || {}).value === 'person' ? 'partner_person' : 'partner_org';
    var pref = (f.querySelector('input[name=pref]:checked') || {}).value || null;
    var phone = phoneRaw ? digits(phoneRaw) : '';

    if (name.length < 2) return err(T.name, f.elements.name);
    if (!phone && !email) return err(T.reach, f.elements.phone);
    if (phone && !/^\+?[0-9]{7,15}$/.test(phone)) return err(T.phone, f.elements.phone);
    if (email && !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return err(T.email, f.elements.email);
    if (pref === 'whatsapp' && !phone) return err(T.prefWa, f.elements.phone);
    if (pref === 'email' && !email) return err(T.prefEm, f.elements.email);

    var done = function () {
      document.getElementById('dt').textContent = T.thanks(name.split(/\s+/)[0]);
      document.getElementById('dp').textContent = T.via(pref || (phone && !email ? 'whatsapp' : email && !phone ? 'email' : null));
      panel.classList.add('sent');
      panel.scrollIntoView({ behavior: rm ? 'auto' : 'smooth', block: 'center' });
    };
    // فخ للبرامج الآلية: حقل مخفي، أو إرسال أسرع من أن يكتبه إنسان؛ نُظهر الشكر ولا نرسل شيئًا
    if (f.elements.website.value || Date.now() - t0 < 2500) return done();

    var head = [T.lType + ': ' + T.kinds[kind]];
    if (phone) head.push(T.lWa + ': ' + phone);
    if (email) head.push(T.lEm + ': ' + email);
    if (pref) head.push(T.lPref + ': ' + T.prefs[pref]);
    head.push(T.lPage + ': ' + location.pathname);
    var body = head.join('\n') + (text ? '\n\n' + text : '');

    var post = function (data) {
      return fetch(API, { method: 'POST', headers: { apikey: KEY, Authorization: 'Bearer ' + KEY, 'Content-Type': 'application/json', Prefer: 'return=minimal' }, body: JSON.stringify(data) });
    };
    btn.disabled = true; btn.textContent = T.sending;
    post({ topic: 'support', support_kind: kind, name: name.slice(0, 80), email: email || null, phone: phone || null, contact_pref: pref, body: body.slice(0, 4000), source: 'web' })
      .then(function (r) {
        if (r.ok) return done();
        return r.text().then(function (x) {
          if (x.indexOf('rate_limited') > -1) return err(T.rate);
          // قبل تطبيق الترحيل 146 على الخادم: نرسل بالشكل القديم إن كان هناك بريد
          if (email) return post({ topic: 'partnership', name: name.slice(0, 80), email: email, body: body.slice(0, 4000), source: 'web' })
            .then(function (r2) { if (r2.ok) return done(); throw 0; });
          throw 0;
        });
      })
      .catch(function () { err(T.fail, null, WA + '?text=' + encodeURIComponent(T.waText + '\n\n' + body)); })
      .then(function () { btn.disabled = false; btn.textContent = T.send; });
  });
})();
