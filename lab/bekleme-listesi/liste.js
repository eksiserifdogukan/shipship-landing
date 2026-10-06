
/* Bekleme listesi kaydını yönet (e-postadaki bağlantılar buraya gelir).
   Token URL'nin # kısmında durur — sunucu kayıtlarına düşmez.
   Bağlantıyı AÇMAK hiçbir şey silmez: e-posta tarayıcıları bağlantıları
   önceden açabildiği için silme yalnız düğmeye basınca olur. */
(function(){
  var WL_URL = '__WL_URL__';
  var WL_KEY = '__WL_KEY__';
  var ILLER = __ILLER__;
  var $ = function(id){ return document.getElementById(id); };
  var q = {};
  location.hash.replace(/^#/, '').split('&').forEach(function(kv){
    var p = kv.split('='); if (p[0]) q[p[0]] = decodeURIComponent(p[1] || '');
  });
  var token = /^[0-9a-f-]{36}$/i.test(q.t || '') ? q.t : null;

  function rpc(fn, body){
    return fetch(WL_URL + '/rest/v1/rpc/' + fn, {
      method: 'POST', headers: {'apikey': WL_KEY, 'Content-Type': 'application/json'}, body: JSON.stringify(body)
    }).then(function(r){ return r.json().then(function(j){ if (!r.ok) throw new Error(j && j.message); return j; }); });
  }
  function show(id){ ['lsLoading','lsOk','lsLeft','lsBad'].forEach(function(x){ $(x).hidden = x !== id; }); }
  var NET = 'Şu an bağlanamadık. Bağlantını kontrol edip tekrar dener misin?';

  if (!token) { show('lsBad'); return; }
  rpc('cm_waitlist_get', {p_token: token}).then(function(r){
    if (!r.ok) { show('lsBad'); return; }
    $('lsCity').textContent = r.city;
    var sel = $('lsSel');
    ILLER.forEach(function(il){
      var o = document.createElement('option'); o.value = il; o.textContent = il;
      if (il === r.city) o.selected = true; sel.appendChild(o);
    });
    show('lsOk');
    if (q.a === 'cik') { $('lsLeaveH').scrollIntoView({block: 'center'}); $('lsLeave').focus(); }
    else if (q.a === 'sehir') { sel.focus(); }
  }).catch(function(){ show('lsLoading'); $('lsLoading').firstElementChild.textContent = NET; });

  $('lsSave').addEventListener('click', function(){
    var c = $('lsSel').value; $('lsMsg').textContent = '';
    rpc('cm_waitlist_set_city', {p_token: token, p_city: c}).then(function(r){
      if (!r.ok) { show('lsBad'); return; }
      $('lsCity').textContent = c; $('lsMsg').textContent = 'Kaydettik. ' + c + ' açıldığında sana haber vereceğiz.';
    }).catch(function(){ $('lsMsg').textContent = NET; });
  });
  $('lsLeave').addEventListener('click', function(){
    $('lsMsg2').textContent = '';
    rpc('cm_waitlist_leave', {p_token: token}).then(function(){
      try { var s = JSON.parse(localStorage.getItem('shipship.wl') || 'null'); if (s && s.t === token) localStorage.removeItem('shipship.wl'); } catch(e){}
      show('lsLeft'); $('lsLeftH').focus();
    }).catch(function(){ $('lsMsg2').textContent = NET; });
  });
})();
