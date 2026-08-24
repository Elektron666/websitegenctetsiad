/* Genç TETSİAD — yavaş ve az fade-in. Başka iş yapmaz. */
(function () {
  'use strict';
  var els = document.querySelectorAll('[data-reveal]');
  if (!els.length) return;

  function showAll() {
    for (var i = 0; i < els.length; i++) els[i].classList.add('shown');
  }

  if (!('IntersectionObserver' in window) ||
      (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches)) {
    showAll();
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add('shown');
      io.unobserve(e.target);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  for (var i = 0; i < els.length; i++) {
    // ilk ekranda görünen öğeleri bekletme
    if (els[i].getBoundingClientRect().top < window.innerHeight * 0.92) {
      els[i].classList.add('shown');
    } else {
      io.observe(els[i]);
    }
  }
})();
