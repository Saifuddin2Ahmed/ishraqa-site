/* قائمة الهاتف في الشريط الموحّد: تفتح وتغلق بالزر، وتغلق عند اختيار رابط أو لمس خارجها أو Escape */
(function(){
var bar=document.querySelector('.snav'),btn=bar&&bar.querySelector('.snav-btn'),menu=bar&&bar.querySelector('.snav-links');
if(!btn||!menu)return;
function isOpen(){return bar.classList.contains('is-open')}
function set(on,focus){bar.classList.toggle('is-open',on);btn.setAttribute('aria-expanded',on?'true':'false');
  if(on&&focus){var a=menu.querySelector('a');if(a)a.focus()}}
btn.addEventListener('click',function(e){set(!isOpen(),e.detail===0)});
menu.addEventListener('click',function(e){if(e.target.closest&&e.target.closest('a'))set(false)});
document.addEventListener('click',function(e){if(isOpen()&&(e.target===bar||!bar.contains(e.target)))set(false)});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&isOpen()){set(false);btn.focus()}});
bar.addEventListener('focusout',function(e){if(isOpen()&&e.relatedTarget&&!bar.contains(e.relatedTarget))set(false)});
var mq=matchMedia('(min-width:761px)'),f=function(){if(mq.matches)set(false)};
if(mq.addEventListener)mq.addEventListener('change',f);else if(mq.addListener)mq.addListener(f);
addEventListener('pageshow',function(){set(false)});
})();
