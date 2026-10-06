
/* ─── BEKLEME LİSTESİ (2026-09-27) ─────────────────────────────────────────
   Tablo istemciye kapalı; yalnız üç fonksiyon çağrılır (crowdmatch-rn
   BACKEND.md §waitlist). Anahtar herkese açık "publishable" anahtardır. */
(function(){
  var WL_URL = '__WL_URL__';
  var WL_KEY = '__WL_KEY__';
  var TOKEN_KEY = 'shipship.wl';

  var ILLER = ['Adana','Adıyaman','Afyonkarahisar','Ağrı','Aksaray','Amasya','Ankara','Antalya','Ardahan','Artvin','Aydın','Balıkesir','Bartın','Batman','Bayburt','Bilecik','Bingöl','Bitlis','Bolu','Burdur','Bursa','Çanakkale','Çankırı','Çorum','Denizli','Diyarbakır','Düzce','Edirne','Elazığ','Erzincan','Erzurum','Eskişehir','Gaziantep','Giresun','Gümüşhane','Hakkari','Hatay','Iğdır','Isparta','İstanbul','İzmir','Kahramanmaraş','Karabük','Karaman','Kars','Kastamonu','Kayseri','Kilis','Kırıkkale','Kırklareli','Kırşehir','Kocaeli','Konya','Kütahya','Malatya','Manisa','Mardin','Mersin','Muğla','Muş','Nevşehir','Niğde','Ordu','Osmaniye','Rize','Sakarya','Samsun','Şanlıurfa','Siirt','Sinop','Sivas','Şırnak','Tekirdağ','Tokat','Trabzon','Tunceli','Uşak','Van','Yalova','Yozgat','Zonguldak'];

  var $ = function(id){ return document.getElementById(id); };
  var wl = $('wl'), bar = $('wlBar'), form = $('wlForm'), err = $('wlErr'), err2 = $('wlErr2');
  var root = document.documentElement;
  var lastFocus = null, token = null, city = null;

  function clear(el){ while (el.firstChild) el.removeChild(el.firstChild); }
  function fillCities(sel, selected){
    ILLER.forEach(function(il){
      var o = document.createElement('option'); o.value = il; o.textContent = il;
      if (il === selected) o.selected = true;
      sel.appendChild(o);
    });
  }
  fillCities($('wlCity'));

  /* Hazır şehir düğmeleri: seçili olan dolu görünür; "Başka şehir" 81 şehirlik listeyi açar. */
  var picks = [].slice.call(document.querySelectorAll('input[name="wlCityPick"]'));
  function syncPicks(){
    picks.forEach(function(r){ r.parentNode.classList.toggle('on', r.checked); });
    var other = picks.some(function(r){ return r.checked && r.value === '__diger'; });
    $('wlCity').hidden = !other;
  }
  picks.forEach(function(r){
    r.addEventListener('change', function(){
      syncPicks(); err.textContent = ''; if (r.value !== '__diger') fieldErr('city', false); syncReady();
      if (r.value === '__diger' && r.checked) $('wlCity').focus();
    });
    r.addEventListener('focus', function(){ if (r.matches(':focus-visible')) r.parentNode.classList.add('focus'); });
    r.addEventListener('blur', function(){ r.parentNode.classList.remove('focus'); });
  });
  /* Cinsiyet — İSTEĞE BAĞLI (tasarımcı 09-27): yalnız toplam oran için. Seçiliye yeniden dokununca seçim
     kalkar (boş bırakmak her zaman mümkün; radyo düğmesi normalde bunu yapmaz). */
  var gPicks = [].slice.call(document.querySelectorAll('input[name="wlGender"]'));
  function syncGender(){ gPicks.forEach(function(r){ r.parentNode.classList.toggle('on', r.checked); }); }
  gPicks.forEach(function(r){
    var secili = false;
    r.parentNode.addEventListener('pointerdown', function(){ secili = r.checked; });
    r.addEventListener('click', function(){ if (secili) { r.checked = false; secili = false; } syncGender(); });
    r.addEventListener('change', syncGender);
    r.addEventListener('focus', function(){ if (r.matches(':focus-visible')) r.parentNode.classList.add('focus'); });
    r.addEventListener('blur', function(){ r.parentNode.classList.remove('focus'); });
  });
  function pickedGender(){ var r = gPicks.filter(function(x){ return x.checked; })[0]; return r ? r.value : null; }

  function formReady(){
    return /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test($('wlEmail').value.trim()) && !!pickedCity() && $('wlAdult').checked;
  }
  function syncReady(){
    form.querySelector('button[type=submit]').setAttribute('aria-disabled', formReady() ? 'false' : 'true');
  }
  function pickedCity(){
    var r = picks.filter(function(x){ return x.checked; })[0];
    if (!r) return '';
    return r.value === '__diger' ? $('wlCity').value : r.value;
  }

  function store(){ try { localStorage.setItem(TOKEN_KEY, JSON.stringify({t: token, c: city})); } catch(e){} }
  function unstore(){ try { localStorage.removeItem(TOKEN_KEY); } catch(e){} }
  function restore(){ try { return JSON.parse(localStorage.getItem(TOKEN_KEY) || 'null'); } catch(e){ return null; } }

  /* Kanal (tasarımcı 09-27: "hangi paylaşım işe yarıyor görelim"): YALNIZ kanal adı gider — bağlantıdaki ?k=
     etiketi, yoksa gelinen sitenin alan adı (ref:…). Sekme boyunca saklanır: alt sayfaya gidip oradaki düğmeyle
     dönen de aynı kanaldan sayılır. Veritabanı ayrıca temizler; aydınlatma §3–4. */
  var kanal = (function(){
    var k = null, m = /[?&]k=([^&#]+)/.exec(location.search);
    try { k = sessionStorage.getItem('cm_k'); } catch(e){}
    if (m) { try { k = decodeURIComponent(m[1]); } catch(e){ k = m[1]; } }
    else if (!k && document.referrer) {
      try { var h = new URL(document.referrer).hostname; if (h && h !== location.hostname) k = 'ref:' + h; } catch(e){}
    }
    k = k ? (k.toLowerCase().replace(/[^a-z0-9:._-]/g, '').slice(0, 64) || null) : null;
    try { if (k) sessionStorage.setItem('cm_k', k); } catch(e){}
    return k;
  })();

  function rpc(fn, body){
    return fetch(WL_URL + '/rest/v1/rpc/' + fn, {
      method: 'POST',
      headers: {'apikey': WL_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    }).then(function(r){
      return r.json().then(function(j){
        if (!r.ok) { var e = new Error(j && j.message || 'hata'); e.code = j && j.message; e.pg = j && j.code; e.status = r.status; throw e; }
        return j;
      });
    });
  }

  var MSG = {
    cm_invalid_email: 'E-posta adresini kontrol eder misin?',
    cm_invalid_city: 'Şehrini seçer misin?',
    cm_adult_required: 'Listeye katılmak için 18 yaşından büyük olmalısın.'
  };
  function msg(e){ return MSG[e && e.code] || 'Şu an gönderemedik. Bağlantını kontrol edip tekrar dener misin?'; }

  function show(which){
    form.hidden = which !== 'form';
    $('wlBody').hidden = which === 'form';
    $('wlDone').hidden = which !== 'done';
    $('wlIgFoot').hidden = which !== 'done';
  }
  function showDone(){
    $('wlDoneP').textContent = city + ' açılınca ilk sen duyacaksın.'
      + (token ? ' Onay e-postası yolda; gelmezse gereksiz klasörüne bak.' : '');
    $('wlEdit').hidden = !token;
    $('wlNoEdit').hidden = !!token;
    $('wlCityBox').hidden = true;
    err2.textContent = '';
    show('done');
  }

  /* Form açıkken arkadaki sayfa ETKİLEŞİMSİZ: sekme tuşu arkaya kaçmaz, ekran okuyucu
     arkayı okumaz. */
  function background(off){
    [].forEach.call(document.body.children, function(el){ if (el !== wl && el.tagName !== 'SCRIPT') el.inert = off; });
  }
  function open(){
    if (wl.classList.contains('on')) return;
    lastFocus = document.activeElement;
    var saved = restore();
    if (saved && saved.t) { token = saved.t; city = saved.c; showDone(); } else { show('form'); }
    sc.scrollTop = 0; $('wlBody').scrollTop = 0;
    wl.classList.add('on'); wl.setAttribute('aria-hidden', 'false');
    root.classList.add('wl-open'); background(true); syncBar(); fitVV();
    // Telefonda klavye kendiliğinden açılıp formu kapatmasın: odağı başlığa ver.
    setTimeout(function(){ (form.hidden ? $('wlDoneH') : $('wlH')).focus({preventScroll: true}); }, 60);
  }
  function close(){
    wl.classList.remove('on'); wl.setAttribute('aria-hidden', 'true');
    root.classList.remove('wl-open'); background(false); syncBar();
    wl.style.top = ''; wl.style.height = ''; vvTop = -1; vvH = -1;
    if (location.hash === '#katil') history.replaceState(null, '', location.pathname + location.search);
    if (lastFocus && lastFocus.focus) lastFocus.focus({preventScroll: true});
  }

  /* ─── Kutu GÖRÜNÜR ALANA oturur (visualViewport). iPhone'da klavye açılınca yerleşim
     görünümü küçülmez, yalnız görünür alan küçülür → sabit/yapışık alt öğeler klavyenin
     ARKASINDA kalıyordu. Kutunun üstünü ve boyunu görünür alana eşitleyince alt şerit
     (gönder düğmesi) her durumda klavyenin hemen üstünde durur. ─── */
  var sc = $('wlScroll');
  function keepFocusedInView(){
    var el = document.activeElement;
    if (!el || !sc.contains(el)) return;
    var r = el.getBoundingClientRect(), b = sc.getBoundingClientRect();
    if (r.top < b.top + 8) sc.scrollBy({top: r.top - b.top - 12});
    else if (r.bottom > b.bottom - 8) sc.scrollBy({top: r.bottom - b.bottom + 12});
  }
  /* Kareye bir kez + yalnız değer değişince yaz: iPhone görünür alanı kaydırırken her olayda
     kutuyu yeniden yazmak ekranı titretiyordu (09-27 cihaz bulgusu). "Odaklı alanı görünür tut"
     yalnız klavye açılıp kapanırken (resize) — kaydırma sırasında değil (geri besleme döngüsü). */
  var vvRaf = 0, vvTop = -1, vvH = -1;
  function fitVV(){
    if (vvRaf || !wl.classList.contains('on') || !window.visualViewport) return;
    vvRaf = requestAnimationFrame(function(){
      vvRaf = 0;
      var vv = window.visualViewport, t = Math.max(0, Math.round(vv.offsetTop)), h = Math.round(vv.height);
      if (t !== vvTop) { wl.style.top = t + 'px'; vvTop = t; }
      if (h !== vvH) { wl.style.height = h + 'px'; vvH = h; }
    });
  }
  if (window.visualViewport) {
    visualViewport.addEventListener('resize', function(){ fitVV(); setTimeout(keepFocusedInView, 80); });
    visualViewport.addEventListener('scroll', fitVV);
  }
  sc.addEventListener('focusin', function(){ setTimeout(keepFocusedInView, 60); });

  /* Eksik alana KAYDIR (yalnız formun içinde — arkadaki sayfa kıpırdamaz), sonra odakla. */
  function reveal(box, focusEl){
    var r = box.getBoundingClientRect(), b = sc.getBoundingClientRect();
    var d = r.top - b.top - Math.max(12, (b.height - r.height) / 2);
    sc.scrollBy({top: d, behavior: 'smooth'});
    setTimeout(function(){ focusEl.focus({preventScroll: true}); }, 250);
  }

  /* Ana sayfa kaydırmayı KENDİSİ yönetir (pencereye takılı tekerlek/dokunma dinleyicileri
     varsayılanı engelleyip sayfayı elle kaydırır). Form açıkken bu olaylar pencereye
     ULAŞMAMALI — yoksa arkadaki sayfa kayar, formun kendisi kaymaz. Olayı formda
     durdurmak, formun yerli (native) kaydırmasını serbest bırakır. */
  ['wheel', 'touchstart', 'touchmove', 'touchend'].forEach(function(ev){
    wl.addEventListener(ev, function(e){ e.stopPropagation(); }, {passive: true});
  });
  /* Klavye açıkken form ekrana sığınca sürükleme formu değil GÖRÜNÜR ALANI kaydırıyordu → kutu onu
     kovalıyor, ekran titriyordu. Sürükleme ancak içinde kayacak yer olan bir alanı kaydırabilir;
     alan yoksa ya da uca gelindiyse hareket burada durur (görünür alan hiç kaymaz). */
  var touchY = 0;
  wl.addEventListener('touchstart', function(e){ touchY = e.touches[0].clientY; }, {passive: true});
  wl.addEventListener('touchmove', function(e){
    if (e.touches.length > 1) return;                       // iki parmak yakınlaştırmaya dokunma
    var y = e.touches[0].clientY, dy = y - touchY, box = null; touchY = y;   // anlık yön (geri dönüşü de yakalar)
    for (var n = e.target; n && n !== wl; n = n.parentNode) {
      if (n.nodeType === 1 && n.scrollHeight > n.clientHeight + 1) {
        var oy = getComputedStyle(n).overflowY;
        if (oy === 'auto' || oy === 'scroll') { box = n; break; }
      }
    }
    if (!box) { e.preventDefault(); return; }
    var atTop = box.scrollTop <= 0, atEnd = box.scrollTop + box.clientHeight >= box.scrollHeight - 1;
    if ((dy > 0 && atTop) || (dy < 0 && atEnd)) e.preventDefault();
  }, {passive: false});

  /* Sabit üst başlık: ilk piksele değil, BİRAZ kaydırınca iner (tasarımcı 09-28) — ekranın ~%15'i, en az 80px.
     Küçük histerezis: eşiğin hemen altında ileri-geri sallanınca titremesin. Düğme camın içinde değil, kendi
     katmanında (lab/menu.py .mn-cta): en üstte çerçeveli, cam inince pembe. Zemin koyulaşması hero'nun
     ~%35'inde başlar (ana JS ciz), eşik ondan çok önce → çerçeve hep krem üstünde kalır. */
  var barWm = $('wlBarWm');
  /* Telefonda (tasarımcı 10-06): cam KAYDIRIR KAYDIRMAZ iner. Eşik ekran boyuna bağlıyken (%15) aradaki
     ~100px'te sabit düğme içeriğin üstünde camsız yüzüyordu; Safari çubuğu kayarken innerHeight değişip eşik de
     oynadığından cam inip kalkıyor, üst kısım koyulaşıp açılıyordu. Sabit 4px eşik ekran boyundan bağımsız;
     yalnız en tepede (ve tepedeki esnemede) kalkar. Masaüstü 09-28 kararıyla aynı. */
  var telefonMu = window.matchMedia ? matchMedia('(max-width: 879px)') : null;
  function esik(){
    if (telefonMu && telefonMu.matches) return 4;
    var e = Math.max(80, innerHeight * .15); return bar.classList.contains('on') ? e - 24 : e;
  }
  function syncBar(){
    var on = scrollY > esik() && !wl.classList.contains('on');
    if (bar.classList.contains('on') === on) return;
    bar.classList.toggle('on', on); bar.inert = !on;
    barWm.classList.toggle('on', on); barWm.tabIndex = on ? 0 : -1;
    root.classList.toggle('wl-bar-on', on);
  }
  addEventListener('scroll', syncBar, {passive: true});
  syncBar();

  document.querySelectorAll('[data-wl-open]').forEach(function(b){
    b.addEventListener('click', function(e){ e.preventDefault(); open(); });
  });
  /* Alt sayfalardaki "Bekleme listesine katıl" → /#katil → form kendiliğinden açılır. */
  if (location.hash === '#katil') open();
  addEventListener('hashchange', function(){ if (location.hash === '#katil') open(); });
  wl.querySelectorAll('[data-wl-close]').forEach(function(b){ b.addEventListener('click', close); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && wl.classList.contains('on')) close(); });

  /* Alan hataları alanın kendisine bağlı: kutu kızarır + altında mesaj (18 yaş: yalnız kızarır). */
  var EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;
  function fieldErr(field, on){
    if (field === 'email') {
      $('wlEmail').setAttribute('aria-invalid', on ? 'true' : 'false');
      $('wlEmailErr').textContent = on ? MSG.cm_invalid_email : '';
    } else if (field === 'city') {
      $('wlChips').classList.toggle('bad', on);
      $('wlCity').setAttribute('aria-invalid', on ? 'true' : 'false');
      $('wlCityErr').textContent = on ? MSG.cm_invalid_city : '';
    } else if (field === 'adult') {
      $('wlAdultL').classList.toggle('bad', on);
      $('wlAdult').setAttribute('aria-invalid', on ? 'true' : 'false');
      $('wlAdultErr').textContent = on ? MSG.cm_adult_required : '';
    }
  }
  var FIELD_OF = {cm_invalid_email: 'email', cm_invalid_city: 'city', cm_adult_required: 'adult'};
  $('wlEmail').addEventListener('input', function(){ fieldErr('email', false); err.textContent = ''; syncReady(); });
  // Yazarken değil, alandan ÇIKINCA uyar (yarım adrese kırmızı göstermek kaba durur).
  $('wlEmail').addEventListener('blur', function(){
    var v = this.value.trim(); if (v && !EMAIL_RE.test(v)) fieldErr('email', true);
  });
  $('wlCity').addEventListener('change', function(){ fieldErr('city', false); err.textContent = ''; syncReady(); });
  $('wlAdult').addEventListener('change', function(){ fieldErr('adult', false); err.textContent = ''; syncReady(); });

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var email = $('wlEmail').value.trim(), c = pickedCity(), adult = $('wlAdult').checked;
    var badEmail = !EMAIL_RE.test(email), badCity = !c, badAdult = !adult;
    fieldErr('email', badEmail); fieldErr('city', badCity); fieldErr('adult', badAdult);
    if (badEmail) { reveal($('wlEmailF'), $('wlEmail')); return; }
    if (badCity) { reveal($('wlCityF'), $('wlCity').hidden ? picks[0] : $('wlCity')); return; }
    if (badAdult) { reveal($('wlAdultL'), $('wlAdult')); return; }
    // Sınıf adıyla DEĞİL türüyle bul: 09-27'de görünüm sınıfı değişince gönderim sessizce kırılmıştı.
    var go = form.querySelector('button[type=submit]');
    if (go.getAttribute('aria-busy') === 'true') return;
    go.setAttribute('aria-busy', 'true'); go.textContent = 'Gönderiliyor…';
    var govde = {p_email: email, p_city: c, p_adult: true, p_hp: $('wlHp').value};
    if (kanal) govde.p_source = kanal;
    var cins = pickedGender(); if (cins) govde.p_gender = cins;
    rpc('cm_waitlist_join', govde)
      .catch(function yeniden(x){
        // Veritabanı yeni alanı henüz tanımıyorsa (fonksiyon bulunamadı) o alan düşürülüp yeniden denenir —
        // önce cinsiyet, sonra kanal. Kayıt ASLA isteğe bağlı bir alan yüzünden düşmez; yayın sırası kaçırılsa da güvenli.
        var ek = ['p_gender', 'p_source'].filter(function(k){ return k in govde; })[0];
        if (ek && x && (x.pg === 'PGRST202' || x.status === 404)) { delete govde[ek]; return rpc('cm_waitlist_join', govde).catch(yeniden); }
        throw x;
      })
      .then(function(r){
        token = r.token || null; city = c;
        if (token) store();
        showDone(); $('wlDoneH').focus();
      })
      .catch(function(x){ var f = FIELD_OF[x && x.code]; if (f) fieldErr(f, true); else err.textContent = msg(x); })
      .then(function(){ go.setAttribute('aria-busy', 'false'); go.textContent = 'Listeye katıl'; });
  });

  $('wlShare').addEventListener('click', function(){
    var url = 'https://shipshipapp.com/?k=arkadas';
    if (navigator.share) { navigator.share({title: 'shipship', url: url}).catch(function(){}); return; }
    var b = $('wlShareT');
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function(){
      b.textContent = 'Bağlantı kopyalandı';
      setTimeout(function(){ b.textContent = 'Uygulamayı arkadaşınla paylaş'; }, 2200);
    }).catch(function(){ window.prompt('Bağlantıyı kopyala:', url); });
  });

  $('wlChange').addEventListener('click', function(){
    var sel = $('wlCity2'); clear(sel); fillCities(sel, city);
    $('wlCityBox').hidden = false; sel.focus();
  });
  $('wlCitySave').addEventListener('click', function(){
    var c = $('wlCity2').value; err2.textContent = '';
    rpc('cm_waitlist_set_city', {p_token: token, p_city: c}).then(function(r){
      if (!r.ok) { unstore(); token = null; err2.textContent = 'Kaydını bulamadık. Formu yeniden doldurabilirsin.'; return; }
      city = c; store(); showDone();
    }).catch(function(x){ err2.textContent = msg(x); });
  });
})();
