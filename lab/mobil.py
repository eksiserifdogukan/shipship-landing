"""Ana sayfanın MOBİL düzeni (tasarımcı 2026-09-27): telefonda yalnız hero + alt bilgi ("Nasıl çalışıyor"
2026-10-09'da kalktı → lab/arsiv/nasil-calisiyor-2026-10-09, betiğin o anki hâli kaynak/mobil.py); kaydırma telefonun kendi (doğal) kaydırması — sitenin "durak" kaydırması kapalı.
Masaüstü DEĞİŞMEZ. index.html ve lab/site.html'e işaretli bloklar olarak eklenir; tekrar
koşmak bloğu yeniler (zararsız).  Kullanım: python3 lab/mobil.py
"""
import re, pathlib
L = pathlib.Path(__file__).resolve().parent.parent
B, S = 'MOBİL:BAŞ', 'MOBİL:SON'

CSS = """
  /* MOBİL:BAŞ — telefonda yalnız hero + alt bilgi (tasarımcı 09-27; "Nasıl çalışıyor" 10-09'da kalktı → lab/arsiv/nasil-calisiyor-2026-10-09).
     Hero tek ekran (kaydırmayla küçülüp soru soran sahne mobilde yok: cevabı hikâye bölümündeydi).
     Diğer bölümler ve onların sabit renk perdeleri gizli. */
  #mTintBottom{display:none}
  @media (max-width:879px){
    .hero-scroll{height:100vh;height:100svh}
    .hero-say{display:none}
    /* Hero okunurluğu (tasarımcı 09-27, seçenek B): yazı videonun ÜSTÜNE binmez. Video kartta kalan
       alanı doldurur, yazı altında düz koyu zeminde (videodan yumuşak geçişle). Ekran boyundan
       bağımsız: kısa ekranda video küçülür, yazı her karede okunur. Karşılaştırma: lab/hero-mobil-deneme.html */
    .hero-card{display:flex;flex-direction:column}
    .hero-card video,.hero-card .hero-vid-img{flex:1 1 auto;min-height:0;height:auto}
    .hero-card::after{background:linear-gradient(180deg,rgba(27,17,25,.28) 0%,rgba(27,17,25,0) 18%)}
    /* Oran (tasarımcı 09-27): düğme kartın DİBİNDE, yazı ona yaslanır, video kalan yüksekliği alır.
       Altta yalnız "kaydır" işaretine yer: işaret ekranın en altında (hero'daki yukarı kaldırma iptal),
       düğme onun hemen üstünde. Durdur düğmesi bekleme listesi düğmesiyle aynı sırada, ortası hizalı. */
    .hero-copy{position:relative;left:auto;right:auto;bottom:auto;flex:none;margin-top:-72px;
      padding:72px clamp(20px,4vw,48px) 56px;   /* işaret 26 + boyu 29 + ara 15 − kart altı boşluğu 14 */
      background:linear-gradient(180deg,rgba(27,17,25,0) 0,var(--night) 72px)}
    .hero-pause{bottom:63px}   /* 56 + (52 − 38) / 2 → bekleme listesi düğmesiyle aynı hiza */
    .hero-copy p{font-size:15.5px;line-height:1.5;color:rgba(255,247,244,.9)}
    .hero-copy .eyebrow{letter-spacing:.1em}   /* iki satıra kırılıyordu */
    .story,.wheel,.gal,.trust,.fin,.wheel-perde,.yesil-perde,.trust-perde,.fade-dark{display:none !important}
    footer.mega{background:#191a1b;padding-top:40px;padding-bottom:env(safe-area-inset-bottom)}
    /* "KAYDIR" işareti işini hero'da yapar; kaydırma başlayınca metnin üstünde asılı kalmasın. */
    html.wl-bar-on .scroll-cue{opacity:0;pointer-events:none}
    /* Safari 26 alt çubuğu renk için ÖNCE ekranın altına yapışık (≤3px), ≥%80 genişlikte sabit bir öğeye
       bakar, yoksa body öğesinin rengine (html'e DEĞİL; theme-color yok sayılır). Alt bilgi görününce bu ince
       koyu şerit açılır → çubuk koyulaşır. Gizlerken display:none (opaklık değil — Safari yine sayar). */
    #mTintBottom{position:fixed;left:0;bottom:-8px;width:100%;min-height:12px;background:#191a1b;pointer-events:none;display:none}
    html.m-dip #mTintBottom{display:block}
    html.wl-open #mTintBottom{display:none !important}
    /* Mobilde düz beyaz (tasarımcı 09-27) — fark karışımı video üstünde parçalı görünüyordu. */
    .scroll-cue{mix-blend-mode:normal;color:#fff;transform:translateX(-50%);bottom:26px}   /* kartın içinde, alt kenardan 12px */
  }
  /* MOBİL:SON */
"""

# Adım görselleri (SHOTS) "Nasıl çalışıyor" bölümüyle birlikte arşivde: lab/arsiv/nasil-calisiyor-2026-10-09/kaynak/mobil.py

# Sayfa sonunda adres çubuğunun altı SAYFA değil KÖK ZEMİN rengidir (krem) → alt bilgi görününce
# kök zemin koyulaşır, yukarı çıkınca kreme döner (kalıcı koyu olsa üstte saat çubuğunun altı kararırdı).
JS = """<div id="mTintBottom" aria-hidden="true"></div><script>/* MOBİL:BAŞ */(function(){
  var mq = window.matchMedia && matchMedia('(max-width: 879px)'), f = document.querySelector('footer.mega'), r = document.documentElement;
  if (!mq || !f) return;
  /* Eşik KÜÇÜK görünür alana (100svh) bağlı, innerHeight'a DEĞİL. 10-06: Safari alt çubuğu kayarken innerHeight
     ~80px oynuyor, eşik onunla kayınca koyu zemin açılıp kapanıyordu. 10-09: o günün 120px'lik kapanış payı, sayfa
     kısalınca (yalnız hero + alt bilgi) alt bilgiyi hiç "uzak" saymıyordu → bir kez koyulaşan zemin en üste
     dönünce de koyu kalıyor, alt kenarda ince koyu şerit duruyordu. Şimdi: alt bilginin 40px'i küçük görünür alana
     girince açılır, neredeyse tamamen çıkınca (8px) kapanır; çubuk hareketi eşiği oynatmaz. */
  var svh = innerHeight;
  function olc(){
    var p = document.createElement('div');
    p.style.cssText = 'position:absolute;top:0;left:0;width:1px;height:100svh;visibility:hidden;pointer-events:none';
    document.body.appendChild(p); svh = p.getBoundingClientRect().height || innerHeight; p.remove();
  }
  var dip = false;
  function s(){
    var top = f.getBoundingClientRect().top;
    var on = mq.matches && (dip ? top < svh - 8 : top < svh - 40);
    dip = on;
    r.classList.toggle('m-dip', on);
    r.style.backgroundColor = on ? '#191a1b' : '';
    document.body.style.backgroundColor = on ? '#191a1b' : '';   // Safari 26 yedek kaynak: body rengi
  }
  addEventListener('scroll', s, {passive: true}); addEventListener('resize', function(){ olc(); s(); }); olc(); s();
})();/* MOBİL:SON */</script>
"""

DURAK_OLD = "var DURAK_ACIK = !/durak=0/.test(location.search);"
DURAK_NEW = ("var DURAK_ACIK = !/durak=0/.test(location.search) && "
             "!(window.matchMedia && matchMedia('(max-width: 879px), (hover: none) and (pointer: coarse)').matches); "
             "/* MOBİL: telefonda doğal kaydırma (tasarımcı 09-27) */")

def apply(path):
    s = path.read_text()
    # eski blokları sök (önce betik — CSS deseni onun içini de yakalayabilir)
    s = re.sub(r'(<div id="mTintBottom" aria-hidden="true"></div>)?<script>/\* ' + B + r' \*/.*?/\* ' + S + r' \*/</script>\n?', '', s, flags=re.S)
    s = re.sub(r'\n\s*/\* ' + B + r'.*?/\* ' + S + r' \*/\n', '\n', s, flags=re.S)
    s = re.sub(r'<!-- ' + B + r' -->.*?<!-- ' + S + r' -->', '', s, flags=re.S)
    # CSS: WL bloğundan ÖNCE (yoksa </style> öncesi)
    anchor = '\n  /* WL:BAŞ */' if '/* WL:BAŞ */' in s else '</style>'
    s = s.replace(anchor, CSS + anchor, 1)
    s = s.replace('</body>', JS + '</body>', 1)
    # Doğal kaydırma
    if DURAK_NEW not in s:
        assert DURAK_OLD in s, path
        s = s.replace(DURAK_OLD, DURAK_NEW, 1)
    path.write_text(s); print('güncellendi:', path.relative_to(L))

for rel in ('index.html', 'lab/site.html'):
    apply(L / rel)
