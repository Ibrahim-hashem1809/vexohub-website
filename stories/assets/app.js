(() => {
  'use strict';
  const key = 'hekaya-tanya:';
  const read = (name, fallback) => { try { return JSON.parse(localStorage.getItem(key + name)) ?? fallback; } catch { return fallback; } };
  const write = (name, value) => { try { localStorage.setItem(key + name, JSON.stringify(value)); return true; } catch { return false; } };
  const status = document.querySelector('[data-status]');
  const announce = text => { if(status) status.textContent = text; };
  let saved = read('saved', []);
  if (!Array.isArray(saved)) saved = [];
  const theme = document.querySelector('[data-theme]');
  const isReader = document.body.hasAttribute('data-reader');
  const themeKey = isReader ? 'reader-light' : 'light';
  const setTheme = light => {
    document.body.classList.toggle('light', light);
    if(theme){
      theme.textContent = light ? 'الخلفية: نهارية ☀' : 'الخلفية: ليلية ☾';
      theme.setAttribute('aria-label', light ? 'تفعيل الخلفية الليلية' : 'تفعيل الخلفية النهارية');
    }
  };
  setTheme(read(themeKey, isReader) === true);
  theme?.addEventListener('click', () => { const light = !document.body.classList.contains('light'); setTheme(light); write(themeKey, light); });
  const syncSaved = () => document.querySelectorAll('[data-save]').forEach(button => {
    const active = saved.includes(button.dataset.save);
    button.setAttribute('aria-pressed', String(active));
    button.textContent = active ? 'محفوظة' : 'احفظ لوقت لاحق';
  });
  let savedOnly = false;
  const normalize = text => text.normalize('NFD').replace(/[\u064B-\u065F\u0670\u0300-\u036f]/g,'').replace(/[أإآ]/g,'ا').replace(/ى/g,'ي').toLowerCase();
  const search = document.querySelector('[data-search]');
  const category = document.querySelector('[data-category]');
  const cards = [...document.querySelectorAll('[data-story-card]')];
  const filter = () => {
    let count = 0;
    cards.forEach(card => {
      const match = normalize(card.dataset.search).includes(normalize(search?.value || '')) && (!category?.value || card.dataset.category === category.value) && (!savedOnly || saved.includes(card.dataset.storyCard));
      card.hidden = !match; if(match) count++;
    });
    const empty = document.querySelector('[data-empty]');
    if(empty) { empty.hidden = count > 0; empty.textContent = savedOnly ? 'لا توجد قصص محفوظة تطابق بحثك. احفظ قصة لتعود إليها لاحقًا.' : 'لا توجد قصص تطابق بحثك. جرّب كلمة أخرى أو تصنيفًا مختلفًا.'; }
    const countLabel = document.querySelector('[data-count]');
    if(countLabel) countLabel.textContent = count === 1 ? 'قصة واحدة للقراءة' : count > 1 ? count + ' قصص للقراءة' : 'لا توجد نتائج';
  };
  document.querySelectorAll('[data-save]').forEach(button => button.addEventListener('click', () => {
    const id = button.dataset.save;
    const next = saved.includes(id) ? saved.filter(item => item !== id) : [...saved, id];
    if(!write('saved', next)) { announce('تعذّر الحفظ على هذا المتصفح. يمكنك الاحتفاظ برابط القصة.'); return; }
    saved = next; syncSaved(); filter();
    announce(saved.includes(id) ? 'حُفظت القصة على هذا المتصفح.' : 'أُزيلت القصة من المحفوظات.');
  }));
  syncSaved();
  search?.addEventListener('input', filter);
  category?.addEventListener('change', filter);
  const savedFilter = document.querySelector('[data-saved-filter]');
  savedFilter?.addEventListener('click', () => { savedOnly = !savedOnly; savedFilter.setAttribute('aria-pressed', String(savedOnly)); filter(); });
  filter();
  let size = Math.max(18, Math.min(30, Number(read('size', 21)) || 21));
  const applySize = () => {
    document.documentElement.style.setProperty('--reading-size', size + 'px');
    const smaller = document.querySelector('[data-size="-1"]');
    const larger = document.querySelector('[data-size="1"]');
    if(smaller) smaller.disabled = size <= 18;
    if(larger) larger.disabled = size >= 30;
  };
  applySize();
  document.querySelectorAll('[data-size]').forEach(button => button.addEventListener('click', () => { size = Math.max(18,Math.min(30,size + Number(button.dataset.size))); applySize(); write('size',size); }));
  document.querySelector('[data-share]')?.addEventListener('click', async () => {
    const url = location.href.split('#')[0];
    try {
      if(navigator.share) { await navigator.share({title:document.title,url}); return; }
      if(navigator.clipboard?.writeText) { await navigator.clipboard.writeText(url); announce('تم نسخ رابط القصة.'); }
      else { announce('لمشاركة القصة، انسخ رابطها من شريط العنوان.'); }
    } catch(error) { if(error.name !== 'AbortError') announce('لمشاركة القصة، انسخ رابطها من شريط العنوان.'); }
  });
  const article = document.querySelector('[data-article]');
  const bar = document.querySelector('[data-progress]');
  if(article && bar) {
    let pending = false;
    const update = () => {
      const rect = article.getBoundingClientRect();
      const total = Math.max(1, rect.height - innerHeight + 100);
      const progress = Math.round(Math.max(0,Math.min(1,(100 - rect.top)/total))*100);
      bar.style.width = progress + '%';
      bar.parentElement.setAttribute('aria-valuenow',String(progress));
      pending = false;
    };
    addEventListener('scroll', () => { if(!pending){pending=true;requestAnimationFrame(update);} },{passive:true});
    addEventListener('resize',update); update();
  }
})();
