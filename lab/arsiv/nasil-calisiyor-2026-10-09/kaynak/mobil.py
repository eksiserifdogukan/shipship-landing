"""Ana sayfanın MOBİL düzeni (tasarımcı 2026-09-27): telefonda yalnız hero + "Nasıl çalışıyor"
+ alt bilgi; kaydırma telefonun kendi (doğal) kaydırması — sitenin "durak" kaydırması kapalı.
Masaüstü DEĞİŞMEZ. index.html ve lab/site.html'e işaretli bloklar olarak eklenir; tekrar
koşmak bloğu yeniler (zararsız).  Kullanım: python3 lab/mobil.py
"""
import re, pathlib
L = pathlib.Path(__file__).resolve().parent.parent
B, S = 'MOBİL:BAŞ', 'MOBİL:SON'

CSS = """
  /* MOBİL:BAŞ — telefonda yalnız hero + "Nasıl çalışıyor" + alt bilgi (tasarımcı 09-27).
     Hero tek ekran (kaydırmayla küçülüp soru soran sahne mobilde yok: cevabı hikâye bölümündeydi).
     Diğer bölümler ve onların sabit renk perdeleri gizli. Adımlar soluk değil; her adımın
     altında kendi uygulama ekranı (masaüstünde telefonun içinde dönen görseller). */
  .step-shot{display:none}
  #mTintBottom{display:none}
  @media (max-width:879px){
    .hero-scroll{height:100svh}
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
    .spine-col{padding:8px 0 56px}
    /* Yapışkan "Nasıl çalışıyor" başlığı kenardan kenara (sütunun boşluklarında içerik görünüyordu). */
    .stage-head{margin:0 calc(-1 * var(--gutter));padding-left:var(--gutter);padding-right:var(--gutter)}
    .step{min-height:0;opacity:1 !important;padding:26px 0 32px}
    .step + .step{border-top:1px solid #eadde3}
    .step-shot{display:block;position:relative;width:min(58vw,232px);aspect-ratio:9/19.5;margin-top:20px;
      border-radius:28px;overflow:hidden;background:#241820;border:6px solid #1b1b20;
      box-shadow:0 2px 3px rgba(20,12,18,.2),0 18px 40px rgba(20,12,18,.18)}
    .step-shot > img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:top}
    .step-shot .k{position:absolute;border-radius:9px;overflow:hidden;box-shadow:0 8px 20px rgba(0,0,0,.4)}
    .step-shot .k img{display:block;width:100%;height:100%;object-fit:cover}
    .step-shot .k.a{left:3.18%;top:11.99%;width:93.56%;height:38.63%}
    .step-shot .k.b{left:3.18%;top:51.46%;width:93.56%;height:38.77%}
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

SHOTS = [
    '<img src="img/s-06b-duzenle.jpg" alt="" loading="lazy" decoding="async">',
    '<img src="img/s-03-adaylar.jpg" alt="" loading="lazy" decoding="async">',
    '<img src="img/oy-zemin.jpg" alt="" loading="lazy" decoding="async">'
    '<span class="k a"><img src="img/oy-kart-a.jpg" alt="" loading="lazy" decoding="async"></span>'
    '<span class="k b"><img src="img/oy-kart-b.jpg" alt="" loading="lazy" decoding="async"></span>',
    '<img src="img/s-04-sira-sende.jpg" alt="" loading="lazy" decoding="async">',
    '<img src="img/s-08-oneri.jpg" alt="" loading="lazy" decoding="async">',
    '<img src="img/s-07-tercihler.jpg" alt="" loading="lazy" decoding="async">',
]

# Sayfa sonunda adres çubuğunun altı SAYFA değil KÖK ZEMİN rengidir (krem) → alt bilgi görününce
# kök zemin koyulaşır, yukarı çıkınca kreme döner (kalıcı koyu olsa üstte saat çubuğunun altı kararırdı).
JS = """<div id="mTintBottom" aria-hidden="true"></div><script>/* MOBİL:BAŞ */(function(){
  var mq = window.matchMedia && matchMedia('(max-width: 879px)'), f = document.querySelector('footer.mega'), r = document.documentElement;
  if (!mq || !f) return;
  /* Histerezis (10-06): Safari alt çubuğu kayarken innerHeight ~80px oynuyor; tek çizgilik eşikte alt bilgi
     sınırda iken koyu zemin açılıp kapanıyor, çubuklar koyulaşıp açılıyordu. Açılış 40px içeride, kapanış 120px
     dışarıda → arada kararsızlık yok. */
  var dip = false;
  function s(){
    var top = f.getBoundingClientRect().top;
    var on = mq.matches && (dip ? top < innerHeight + 120 : top < innerHeight - 40);
    dip = on;
    r.classList.toggle('m-dip', on);
    r.style.backgroundColor = on ? '#191a1b' : '';
    document.body.style.backgroundColor = on ? '#191a1b' : '';   // Safari 26 yedek kaynak: body rengi
  }
  addEventListener('scroll', s, {passive: true}); addEventListener('resize', s); s();
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
    # Adım görselleri: her .step'in </p>'sinden sonra
    steps = list(re.finditer(r'(<div class="step"><h3>.*?</p>)(</div>)', s, flags=re.S))
    assert len(steps) == len(SHOTS), (path, len(steps))
    for m, shot in reversed(list(zip(steps, SHOTS))):
        ins = f'<!-- {B} --><div class="step-shot" aria-hidden="true">{shot}</div><!-- {S} -->'
        s = s[:m.end(1)] + ins + s[m.end(1):]
    s = s.replace('</body>', JS + '</body>', 1)
    # Doğal kaydırma
    if DURAK_NEW not in s:
        assert DURAK_OLD in s, path
        s = s.replace(DURAK_OLD, DURAK_NEW, 1)
    path.write_text(s); print('güncellendi:', path.relative_to(L))

for rel in ('index.html', 'lab/site.html'):
    apply(L / rel)
