(() => {
  const finish = () => document.querySelector('.journey-loader')?.classList.add('is-complete');
  document.addEventListener('DOMContentLoaded', finish, {once:true});
  setTimeout(finish, 1200);
  // Native validation runs before submit. Retain values and the submitter's name/value.
  document.addEventListener('submit', event => {
    const form = event.target;
    if (form.method.toLowerCase() !== 'post' || event.defaultPrevented) return;
    if (form.dataset.submitting) { event.preventDefault(); return; }
    form.dataset.submitting = 'true';
    const button = event.submitter;
    if (button) { button.setAttribute('aria-disabled','true'); button.dataset.originalText=button.textContent; button.textContent='Sending…'; }
    // Restore after a failed or stalled navigation; never trap the visitor indefinitely.
    setTimeout(() => reset(form), 20000);
  });
  function reset(form) {
    delete form.dataset.submitting;
    form.querySelectorAll('[data-original-text]').forEach(button => {
      button.textContent=button.dataset.originalText; button.removeAttribute('aria-disabled'); delete button.dataset.originalText;
    });
  }
  window.addEventListener('pageshow', () => {finish();document.querySelectorAll('form[data-submitting]').forEach(reset);});
  const flexible=document.getElementById('id_flexible_dates');
  const syncDates=()=>{const start=document.getElementById('id_start_date');if(start) start.required=!flexible?.checked;};
  flexible?.addEventListener('change',syncDates);syncDates();
})();
(() => {
  const header=document.querySelector('.mbg-header');
  if(!header)return;
  const toggle=header.querySelector('.mbg-menu-toggle');
  const services=header.querySelector('.mbg-services');
  header.classList.add('nav-ready');
  const updateScroll=()=>header.classList.toggle('is-scrolled',window.scrollY>32);
  updateScroll();window.addEventListener('scroll',updateScroll,{passive:true});
  function closeMenu(){header.classList.remove('is-menu-open');toggle.setAttribute('aria-expanded','false');services.open=false;}
  toggle.addEventListener('click',()=>{const open=header.classList.toggle('is-menu-open');toggle.setAttribute('aria-expanded',String(open));});
  document.addEventListener('click',event=>{if(!header.contains(event.target))closeMenu();});
  header.addEventListener('keydown',event=>{if(event.key==='Escape'){const expanded=services.open;closeMenu();(expanded?services.querySelector('summary'):toggle).focus();}});
  header.querySelectorAll('nav a').forEach(link=>link.addEventListener('click',closeMenu));
  window.matchMedia('(min-width:1051px)').addEventListener('change',closeMenu);
})();
