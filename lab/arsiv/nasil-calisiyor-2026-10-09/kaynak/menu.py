"""Masaüstü üst bağlantı ("Nasıl çalışıyor", tıklayınca yumuşak kaydırma) + "başa dön" yüzen düğmesi.
Karar: BACKLOG 45 (tasarımcı 09-27: üç bölüm ortada; 09-28: TEK bağlantı, SAĞDA — "Niyetler" uygulamanın
sözcüğü, "Güven" varış noktası değil; ortada tek kelime yetim kalır, pembe düğmenin yanında ikincil eylem okunur).
İşaretli blok olarak eklenir; tekrar koşmak bloğu yeniler.

  python3 lab/menu.py            → yalnız TASLAK: lab/menu-deneme.html (index.html'in kopyası + blok)
  python3 lab/menu.py --yayin    → index.html + lab/site.html (tasarımcı onayından sonra)
"""
import re, sys, pathlib
L = pathlib.Path(__file__).resolve().parent.parent
B, S = 'MENU:BAŞ', 'MENU:SON'

CSS = """
  /* MENU:BAŞ — masaüstü "Nasıl çalışıyor" bağlantısı + başa dön (tasarımcı 09-27 → 09-28 tek bağlantı, BACKLOG 45).
     Başlık camının DIŞINDA ayrı sabit katman: cam kendi yığın bağlamını kurduğu için içindeki yazı
     alttaki sayfayla karışamazdı; "fark" karışımıyla krem bölümde koyu, koyu bölümde açık (wordmark'la aynı yöntem).
     SAĞDA durur: hero'da tek başına sağ kenarda; cam inince pembe düğmenin soluna kayar. Düğme genişliği
     JS'te ölçülüp --mn-shift'e yazılır; kayma camın inişiyle aynı süre ve eğri → ikisi birlikte yerleşir. */
  .mn-nav{position:fixed;top:0;right:calc(clamp(18px,4vw,40px) + var(--mn-shift, 0px));z-index:83;height:64px;
    display:flex;align-items:center;mix-blend-mode:difference;pointer-events:none}
  .mn-nav a{pointer-events:auto;color:#fff;font-size:15px;font-weight:600;letter-spacing:-.005em;text-decoration:none;
    padding:8px 2px;border-bottom:1.5px solid transparent}
  .mn-nav a:hover{border-bottom-color:#fff}
  .mn-nav a:focus-visible{outline:2px solid #fff;outline-offset:4px}
  html.wl-open .mn-nav{display:none}
  @media (max-width:879px){ .mn-nav{display:none} }
  /* Bekleme listesi düğmesi (tasarımcı 09-28) camın DIŞINDA kendi sabit katmanında (fark karışımı YOK; pembe ters
     dönmesin). Sayfa en üstteyken İKİNCİL (çerçeveli — birincil pembe hero'nun içinde zaten var), cam inince
     BİRİNCİL pembe. Yer değiştirmez, yalnız ağırlığı değişir; cam arkasına iner. Telefonda da aynı (iki düğme
     sorun değil — tasarımcı). Camın kendi düğmesi yok (wl.html); cam yalnız zemin. Çerçevenin koyu rengi hero
     zemini KREMKEN doğru — cam, zemin koyulaşmadan çok önce iner (eşik wl.js'te, ~%15 ekran; koyulaşma ~%70). */
  .mn-cta{position:fixed;top:0;right:clamp(18px,4vw,40px);z-index:83;height:calc(64px + env(safe-area-inset-top));
    padding-top:env(safe-area-inset-top);display:flex;align-items:center}
  .mn-cta .wl-btn{background:transparent;color:#2a1a24;box-shadow:inset 0 0 0 1.5px #2a1a24;
    transition:background-color .35s cubic-bezier(.22,1,.36,1),color .35s cubic-bezier(.22,1,.36,1),box-shadow .35s cubic-bezier(.22,1,.36,1)}
  html.wl-bar-on .mn-cta .wl-btn{background:#E6336E;color:#fff;box-shadow:none}
  html.wl-open .mn-cta{display:none}
  /* Hero'nun kendi üst şeridi camla AYNI yükseklikte: wordmark, bağlantı ve düğme tek çizgide; kart başlığın
     altından başlar (eskiden şerit ~45px'ti — düğmenin altı kartın üstüne biniyordu, wordmark 10px yukarıdaydı). */
  .hero .topbar{min-height:64px}
  @media (max-width:879px){ .mn-cta{height:calc(56px + env(safe-area-inset-top))} .hero .topbar{min-height:56px} }
  @media (prefers-reduced-motion:reduce){ .mn-cta .wl-btn{transition:none} }
  /* Başa dön: ilk ekran geçilince belirir; krem daire (koyu bölümde de seçilir), sağ altta. */
  .mn-fab{position:fixed;right:24px;bottom:24px;z-index:84;width:48px;height:48px;border-radius:999px;border:0;
    display:flex;align-items:center;justify-content:center;background:#fdf7f4;color:#2a1a24;cursor:pointer;
    box-shadow:0 1px 2px rgba(20,12,18,.18),0 10px 28px rgba(20,12,18,.22);
    opacity:0;transform:translateY(10px);pointer-events:none;transition:opacity .25s,transform .25s;
    -webkit-tap-highlight-color:transparent}
  .mn-fab.on{opacity:1;transform:none;pointer-events:auto}
  .mn-fab:active{transform:scale(.94)}
  .mn-fab:focus-visible{outline:2px solid #2a1a24;outline-offset:3px}
  html.wl-open .mn-fab{display:none}
  @media (max-width:879px){ .mn-fab{right:16px;bottom:calc(16px + env(safe-area-inset-bottom));width:44px;height:44px} }
  /* MENU:SON */
"""

HTML = """<!-- MENU:BAŞ -->
<nav class="mn-nav" aria-label="Sayfa içi">
  <a href="#nasil" data-mn=".spine">Nasıl çalışıyor</a>
</nav>
<div class="mn-cta"><a class="wl-btn wl-btn-sm" href="#katil" data-wl-open>Bekleme listesine katıl</a></div>
<button class="mn-fab" id="mnFab" type="button" aria-label="Başa dön" tabindex="-1">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5"/><path d="M5 12l7-7 7 7"/></svg>
</button>
<!-- MENU:SON -->
"""

JS = """<script>/* MENU:BAŞ */(function(){
  /* Tıklayınca bölüme yumuşak kaydırma. Durak kaydırması kaydırma olayında hedefini kendisi eşitler
     (animasyon yokken hedef = scrollY) → programla kaydırma onunla çakışmaz. */
  var linkler = [].slice.call(document.querySelectorAll('.mn-nav a'));
  function ust(el){ return Math.round(el.getBoundingClientRect().top + scrollY); }
  function git(y){ scrollTo({top: y, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth'}); }
  linkler.forEach(function(a){
    a.addEventListener('click', function(e){
      var el = document.querySelector(a.getAttribute('data-mn')); if (!el) return;
      e.preventDefault(); git(ust(el));
      try { history.replaceState(null, '', a.getAttribute('href')); } catch(x){}
    });
  });
  /* Adresle gelen (#nasil vb.) doğrudan o bölümde açılır. */
  var ilk = linkler.filter(function(a){ return a.getAttribute('href') === location.hash; })[0];
  if (ilk) addEventListener('load', function(){ var el = document.querySelector(ilk.getAttribute('data-mn')); if (el) scrollTo(0, ust(el)); });
  /* Bağlantı düğmenin 24px solunda durur: düğme genişliği ölçülüp --mn-shift'e yazılır. Yazı tipi geç
     yüklenirse genişlik değişir → fonts.ready'de yeniden ölç. */
  var dugme = document.querySelector('.mn-cta .wl-btn');
  function olc(){ document.documentElement.style.setProperty('--mn-shift', dugme ? (dugme.offsetWidth + 24) + 'px' : '0px'); }
  olc(); addEventListener('resize', olc); addEventListener('load', olc);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(olc);
  var fab = document.getElementById('mnFab');
  fab.addEventListener('click', function(){ git(0); });
  function guncelle(){
    var on = scrollY > innerHeight * .9;
    fab.classList.toggle('on', on); fab.tabIndex = on ? 0 : -1;
  }
  addEventListener('scroll', guncelle, {passive: true}); addEventListener('resize', guncelle); guncelle();
})();/* MENU:SON */</script>
"""

def apply(src, dst):
    s = src.read_text()
    s = re.sub(r'<script>/\* ' + B + r' \*/.*?/\* ' + S + r' \*/</script>\n?', '', s, flags=re.S)
    s = re.sub(r'\n\s*/\* ' + B + r'.*?/\* ' + S + r' \*/\n', '\n', s, flags=re.S)
    s = re.sub(r'<!-- ' + B + r' -->.*?<!-- ' + S + r' -->\n?', '', s, flags=re.S)
    s = s.replace('</style>', CSS + '</style>', 1)
    h = s.index('</head>'); b = s.index('<body>', h) + len('<body>')
    s = s[:b] + '\n' + HTML + s[b:]
    s = s.replace('</body>', JS + '</body>', 1)
    dst.write_text(s); print('yazıldı:', dst.relative_to(L))

if '--yayin' in sys.argv:
    for rel in ('index.html', 'lab/site.html'):
        apply(L / rel, L / rel)
else:
    apply(L / 'index.html', L / 'lab/menu-deneme.html')
