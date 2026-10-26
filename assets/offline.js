(() => {
  'use strict';
  const status = document.getElementById('offline-status');
  if (!('serviceWorker' in navigator) || !window.isSecureContext) return;
  navigator.serviceWorker.register('../sw.js', {scope: '../'}).then(registration => {
    const ready = () => { status.textContent = 'Курс доступен офлайн'; };
    if (registration.waiting) status.textContent = 'Обновление загружено. Закройте окна курса и откройте снова.';
    else if (registration.active && navigator.serviceWorker.controller) ready();
    navigator.serviceWorker.addEventListener('controllerchange', ready);
    const watch = () => {
      const worker = registration.installing;
      if (!worker) return;
      status.textContent = 'Сохраняем курс для чтения офлайн…';
      worker.addEventListener('statechange', () => {
        if (worker.state === 'installed' && navigator.serviceWorker.controller) status.textContent = 'Обновление загружено. Закройте окна курса и откройте снова.';
        if (worker.state === 'redundant') status.textContent = 'Не удалось обновить офлайн-копию. Повторите при подключении к сети.';
      });
    };
    registration.addEventListener('updatefound', watch);
    watch();
  }).catch(() => { status.textContent = 'Офлайн-копия недоступна. Для чтения нужна сеть.'; });
})();
