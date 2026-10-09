/* Değişken tanımları (evoYolKur satırının hemen altında duruyordu) */
  var spineScroll = document.getElementById('spineScroll'), sonAdim = -1;
  var steps = [].slice.call(document.querySelectorAll('.step'));
  var apps  = [].slice.call(document.querySelectorAll('.app'));
  var oyA = document.getElementById('oyA'), oyB = document.getElementById('oyB');
  var oyA2 = document.getElementById('oyA2'), oyB2 = document.getElementById('oyB2');
  var oyRozet = document.getElementById('oyRozet');
  var OY_ADIM = 2;                    // "İkilileri oylamaya başlarsın" adımı
  var TILT = 4.2, CONV = 3.2, KAY = 32;   // derece · yakınsama % · sağa kayma %


/* Kaydırma döngüsünün içi (hikâye bloğunun sonundan, 3b TEKERLEK'ten önce) */
    /* 2 · OMURGA — aktif adım ekran ortasına en yakın olan; telefon ekranı ona eşlik eder */
    // telefon girişi: bölümün üstü ekranın üst %25'ine gelince soldan girer (tek sefer, CSS geçişi)
    var spTop = spineScroll.getBoundingClientRect().top;
    document.querySelector('.spine-sticky').classList.toggle('in', spTop < innerHeight * .25);
    var vc = innerHeight * .38, N = steps.length, merk = steps.map(function(el){ var r = el.getBoundingClientRect(); return r.top + r.height/2; });
    var i = 0, bd = 1e9;
    merk.forEach(function(m, n){ var d = Math.abs(m - vc); if (d < bd){ bd = d; i = n; } });
    steps.forEach(function(el,n){ el.classList.toggle('on', n === i); });
    // ekranlar App Store sırasıyla; aktif adım değişince ekran "titreyerek" değişir (CSS geçişi)
    var ara = merk.length > 1 ? (merk[1] - merk[0]) : innerHeight;
    for (var ai = 0; ai < apps.length; ai++) apps[ai].classList.toggle('on', ai === Math.min(i, apps.length - 1));
    if (i !== sonAdim){                      // adım değişti: telefon titrer (animasyon yeniden başlatılır)
      var ph = document.querySelector('.phone');
      ph.classList.remove('titre'); void ph.offsetWidth; ph.classList.add('titre');
      sonAdim = i;
    }
    /* OY ADIMI — kaydırma oyu VERİR: kartlar sağa gider, birbirine yakınsar,
       "Uygun" rozeti belirir. Sahte sayaç ekranı YOK; pikseller uygulamanın
       kendi Akış ekranından kırpıldı (tasarımcı 2026-08-23). */
    var sOy = c01((vc - merk[OY_ADIM] + ara * .5) / ara);
    /* Zamanlama (tasarımcı 2026-08-23): başlık ekran ortasına OTURANA kadar
       (sOy < .5) hiç oy yok — okur önce cümleyi okur. Sonrasında kısa bir
       kaydırma aralığında oy TAM tamamlanır; yarıda kalmış kart bırakmaz. */
    /* Üç faz (tasarımcı 2026-08-23: oy TAMAMLANIP sıradaki ikiliye geçmeli —
       uygulamadaki gerçek akış): sürükle → kartlar sağa UÇAR → arkadaki
       bulanık ikili netleşip öne gelir. */
    var t = c01((sOy - .50) / .50);
    var drag = c01(t / .42), ucus = c01((t - .42) / .26), gel = c01((t - .52) / .44);
    var yum = 1 - Math.pow(1 - drag, 2);
    if (oyA){
      var dx = yum*KAY + ucus*140, tilt = TILT * c01(yum + ucus*.6);
      oyA.style.transform = 'translate(' + dx + '%,' + (yum*CONV) + '%) rotate(' + tilt + 'deg)';
      oyB.style.transform = 'translate(' + dx + '%,' + (-yum*CONV) + '%) rotate(' + tilt + 'deg)';
      oyA.style.opacity = oyB.style.opacity = String(1 - c01((ucus - .6) / .4));
      var rg = c01((drag - .10) * 2.6) * (1 - ucus);
      oyRozet.style.opacity = String(rg);
      oyRozet.style.transform = 'translate(-50%,-50%) scale(' + (.92 + .08*rg) + ')';
      var gE = 1 - Math.pow(1 - gel, 2);
      [oyA2, oyB2].forEach(function(el){
        el.style.filter = 'blur(' + (6 * (1 - gE)) + 'px)';
        el.style.opacity = String(.35 + .65 * gE);
        el.style.transform = 'scale(' + (.94 + .06 * gE) + ')';
      });
    }

