/* Genç TETSİAD — arayüz davranışları */
(function () {
  'use strict';

  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* --- Yıl --- */
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = String(new Date().getFullYear());

  /* --- Mobil menü --- */
  var nav = document.getElementById('nav');
  var toggle = document.getElementById('navToggle');

  if (nav && toggle) {
    toggle.addEventListener('click', function () {
      var open = toggle.getAttribute('aria-expanded') === 'true';
      toggle.setAttribute('aria-expanded', String(!open));
      toggle.setAttribute('aria-label', open ? 'Menüyü aç' : 'Menüyü kapat');
      nav.classList.toggle('open', !open);
    });

    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        toggle.setAttribute('aria-expanded', 'false');
        toggle.setAttribute('aria-label', 'Menüyü aç');
        nav.classList.remove('open');
      }
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && nav.classList.contains('open')) {
        toggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('open');
        toggle.focus();
      }
    });
  }

  /* --- Header gölgesi --- */
  var header = document.getElementById('siteHeader');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('scrolled', window.scrollY > 24);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* --- Reveal animasyonu --- */
  var revealEls = document.querySelectorAll('.reveal');

  if (reduceMotion || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(revealEls, function (el) { el.classList.add('in'); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('in');
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });

    Array.prototype.forEach.call(revealEls, function (el) { io.observe(el); });
  }

  /* --- Üyelik formu (istemci tarafı doğrulama) --- */
  var form = document.getElementById('joinForm');
  var status = document.getElementById('formStatus');

  if (form && status) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      var invalid = null;
      var required = form.querySelectorAll('[required]');

      Array.prototype.forEach.call(required, function (field) {
        var ok = field.value.trim() !== '' && field.checkValidity();
        field.setAttribute('aria-invalid', ok ? 'false' : 'true');
        if (!ok && !invalid) invalid = field;
      });

      if (invalid) {
        status.textContent = 'Lütfen işaretli alanları kontrol edin.';
        status.classList.add('error');
        invalid.focus();
        return;
      }

      status.classList.remove('error');
      status.textContent = 'Teşekkürler — başvurunuz alındı. (Demo: sunucuya gönderilmedi.)';
      form.reset();
      Array.prototype.forEach.call(required, function (field) {
        field.setAttribute('aria-invalid', 'false');
      });
    });
  }
})();
