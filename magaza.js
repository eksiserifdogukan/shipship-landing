/* Uygulama App Store'da (2026-11-09, tasarımcı onayı): iPhone ve bilgisayardan gelene bekleme listesi düğmeleri
   "App Store'dan indir" olur; Android'den gelen bekleme listesinde kalır (Android uygulaması yok, form "önce iPhone"
   notunu zaten gösteriyor). Yerleşim değişmez; yalnız yazı + bağlantı. Betik kapalıysa (JS yok) eski hâl görünür.
   Ana sayfadaki form betiği [data-wl-open] düğmelerine tıklamayı formu açmaya bağlıyor → tıklama belge düzeyinde
   YAKALAMA aşamasında karşılanır, form dinleyicisine hiç ulaşmaz. */
(function () {
  var MAGAZA = 'https://apps.apple.com/tr/app/id6789615007';
  var android = /Android/i.test(navigator.userAgent || '');

  function ceviri() {
    var fin = document.getElementById('finH');
    if (android) {
      if (fin) fin.textContent = 'Android’e yakında';
      return;
    }
    var hedefler = document.querySelectorAll('[data-wl-open], a[href="/#katil"], a[href="#katil"]');
    for (var i = 0; i < hedefler.length; i++) {
      var a = hedefler[i];
      if (a.closest('#wl')) continue;               // formun kendi içi
      if (/Bekleme listesine katıl/.test(a.textContent)) a.textContent = 'App Store’dan indir';
      a.setAttribute('href', MAGAZA);
      a.setAttribute('data-magaza', '');
    }
    if (fin) fin.textContent = 'App Store’da';
    var not = document.getElementById('finNot');
    if (not) not.textContent = 'Şimdilik İstanbul, Ankara, İzmir ve Eskişehir’de';
  }

  if (!android) {
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('[data-magaza]');
      if (!a) return;
      e.preventDefault();
      e.stopImmediatePropagation();
      location.href = MAGAZA;
    }, true);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ceviri);
  else ceviri();
})();
