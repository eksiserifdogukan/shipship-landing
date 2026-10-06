
/* ─── BEKLEME LİSTESİ (2026-09-27) ─────────────────────────────────────────
   Tablo istemciye kapalı; yalnız üç fonksiyon çağrılır (crowdmatch-rn
   BACKEND.md §waitlist). Anahtar herkese açık "publishable" anahtardır. */
(function(){
  var WL_URL = '__WL_URL__';
  var WL_KEY = '__WL_KEY__';
  var TOKEN_KEY = 'shipship.wl';

  var ILLER = ['Adana','Adıyaman','Afyonkarahisar','Ağrı','Aksaray','Amasya','Ankara','Antalya','Ardahan','Artvin','Aydın','Balıkesir','Bartın','Batman','Bayburt','Bilecik','Bingöl','Bitlis','Bolu','Burdur','Bursa','Çanakkale','Çankırı','Çorum','Denizli','Diyarbakır','Düzce','Edirne','Elazığ','Erzincan','Erzurum','Eskişehir','Gaziantep','Giresun','Gümüşhane','Hakkari','Hatay','Iğdır','Isparta','İstanbul','İzmir','Kahramanmaraş','Karabük','Karaman','Kars','Kastamonu','Kayseri','Kilis','Kırıkkale','Kırklareli','Kırşehir','Kocaeli','Konya','Kütahya','Malatya','Manisa','Mardin','Mersin','Muğla','Muş','Nevşehir','Niğde','Ordu','Osmaniye','Rize','Sakarya','Samsun','Şanlıurfa','Siirt','Sinop','Sivas','Şırnak','Tekirdağ','Tokat','Trabzon','Tunceli','Uşak','Van','Yalova','Yozgat','Zonguldak'];

  var $ = function(id){ return document.getElementById(id); };
  var wl = $('wl'), form = $('wlForm'), err = $('wlErr'), err2 = $('wlErr2');
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

  function store(){ try { localStorage.setItem(TOKEN_KEY, JSON.stringify({t: token, c: city})); } catch(e){} }
  function unstore(){ try { localStorage.removeItem(TOKEN_KEY); } catch(e){} }
  function restore(){ try { return JSON.parse(localStorage.getItem(TOKEN_KEY) || 'null'); } catch(e){ return null; } }

  function rpc(fn, body){
    return fetch(WL_URL + '/rest/v1/rpc/' + fn, {
      method: 'POST',
      headers: {'apikey': WL_KEY, 'Content-Type': 'application/json'},
      body: JSON.stringify(body)
    }).then(function(r){
      return r.json().then(function(j){
        if (!r.ok) { var e = new Error(j && j.message || 'hata'); e.code = j && j.message; throw e; }
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
    $('wlDone').hidden = which !== 'done';
    $('wlLeft').hidden = which !== 'left';
  }
  function showDone(){
    $('wlDoneP').textContent = city + ' açıldığında herkesten önce sana haber vereceğiz.';
    $('wlEdit').hidden = !token;
    $('wlNoEdit').hidden = !!token;
    $('wlCityBox').hidden = true;
    err2.textContent = '';
    show('done');
  }

  function open(){
    lastFocus = document.activeElement;
    var saved = restore();
    if (saved && saved.t) { token = saved.t; city = saved.c; showDone(); } else { show('form'); }
    wl.classList.add('on'); wl.setAttribute('aria-hidden', 'false');
    document.documentElement.style.overflow = 'hidden';
    setTimeout(function(){ (form.hidden ? $('wlDoneH') : $('wlEmail')).focus(); }, 60);
  }
  function close(){
    wl.classList.remove('on'); wl.setAttribute('aria-hidden', 'true');
    document.documentElement.style.overflow = '';
    if (lastFocus && lastFocus.focus) lastFocus.focus();
  }

  document.querySelectorAll('[data-wl-open]').forEach(function(b){
    b.addEventListener('click', function(e){ e.preventDefault(); open(); });
  });
  wl.querySelectorAll('[data-wl-close]').forEach(function(b){ b.addEventListener('click', close); });
  document.addEventListener('keydown', function(e){ if (e.key === 'Escape' && wl.classList.contains('on')) close(); });

  ['wlEmail','wlCity','wlAdult'].forEach(function(id){
    $(id).addEventListener('input', function(){ err.textContent = ''; });
    $(id).addEventListener('change', function(){ err.textContent = ''; });
  });

  form.addEventListener('submit', function(e){
    e.preventDefault();
    var email = $('wlEmail').value.trim(), c = $('wlCity').value, adult = $('wlAdult').checked;
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) { err.textContent = MSG.cm_invalid_email; $('wlEmail').focus(); return; }
    if (!c) { err.textContent = MSG.cm_invalid_city; $('wlCity').focus(); return; }
    if (!adult) { err.textContent = MSG.cm_adult_required; $('wlAdult').focus(); return; }
    var go = form.querySelector('.wl-go');
    if (go.getAttribute('aria-busy') === 'true') return;
    go.setAttribute('aria-busy', 'true'); go.textContent = 'Gönderiliyor…';
    rpc('cm_waitlist_join', {p_email: email, p_city: c, p_adult: true, p_hp: $('wlHp').value})
      .then(function(r){
        token = r.token || null; city = c;
        if (token) store();
        showDone(); $('wlDoneH').focus();
      })
      .catch(function(x){ err.textContent = msg(x); })
      .then(function(){ go.setAttribute('aria-busy', 'false'); go.textContent = 'Listeye katıl'; });
  });

  $('wlShare').addEventListener('click', function(){
    var url = 'https://shipshipapp.com';
    if (navigator.share) { navigator.share({title: 'shipship', url: url}).catch(function(){}); return; }
    var b = this;
    (navigator.clipboard ? navigator.clipboard.writeText(url) : Promise.reject()).then(function(){
      b.textContent = 'Bağlantı kopyalandı';
      setTimeout(function(){ b.textContent = 'Bağlantıyı arkadaşına gönder'; }, 2200);
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
  $('wlLeave').addEventListener('click', function(){
    err2.textContent = '';
    rpc('cm_waitlist_leave', {p_token: token}).then(function(){
      unstore(); token = null; city = null; form.reset(); show('left'); $('wlLeftH').focus();
    }).catch(function(x){ err2.textContent = msg(x); });
  });
})();
