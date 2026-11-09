/* Uygulama App Store'da (2026-11-09, tasarımcı onayı): iPhone ve bilgisayardan gelene bekleme listesi düğmeleri
   "App Store'dan indir" olur; Android'den gelen bekleme listesinde kalır (Android uygulaması yok, form "önce iPhone"
   notunu zaten gösteriyor). Yerleşim değişmez; yalnız yazı + bağlantı. Betik kapalıysa (JS yok) eski hâl görünür.
   Ana sayfadaki form betiği [data-wl-open] düğmelerine tıklamayı formu açmaya bağlıyor → tıklama belge düzeyinde
   YAKALAMA aşamasında karşılanır, form dinleyicisine hiç ulaşmaz. */
/* Kampanya bağlantısı (11-09): sitenin kanal etiketi (?k=…, sekme boyunca `cm_k`, yoksa gelinen site ref:…, hiçbiri
   yoksa "site") App Store'a kampanya adı (ct) olarak gider → App Store Connect › Analiz › Kampanyalar'da indirme kanal
   kanal okunur. PT = hesabın sağlayıcı kodu (App Store Connect'te ilk kampanya bağlantısı oluşturulunca çıkar); boşsa
   bağlantı eski düz hâlinde kalır. Kanal okuma kuralı ana sayfadaki form betiğiyle aynı. */
(function () {
  var PT = '129152641';
  var MAGAZA_DUZ = 'https://apps.apple.com/tr/app/id6789615007';
  var android = /Android/i.test(navigator.userAgent || '');

  function kanal() {
    var k = null, m = /[?&]k=([^&#]+)/.exec(location.search);
    try { k = sessionStorage.getItem('cm_k'); } catch (e) {}
    if (m) { try { k = decodeURIComponent(m[1]); } catch (e) { k = m[1]; } }
    else if (!k && document.referrer) {
      try { var h = new URL(document.referrer).hostname; if (h && h !== location.hostname) k = 'ref:' + h; } catch (e) {}
    }
    k = k ? (k.toLowerCase().replace(/[^a-z0-9:._-]/g, '').slice(0, 64) || null) : null;
    try { if (k) sessionStorage.setItem('cm_k', k); } catch (e) {}
    return k;
  }

  // App Store kampanya adı en çok 30 karakter.
  var MAGAZA = PT
    ? MAGAZA_DUZ + '?pt=' + PT + '&ct=' + encodeURIComponent((kanal() || 'site').slice(0, 30)) + '&mt=8'
    : MAGAZA_DUZ;

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
