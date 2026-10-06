"""Davet bağlantılarının PAYLAŞIM ÖNİZLEMESİ (tasarımcı 09-27: sitedeki paylaşımla aynı dil; "1 · Arkadaşını davet et" +
"2b · önererek davet, kişisel veri taşımayan").

Mesaj uygulamaları önizlemeyi bağlantının açtığı sayfanın etiketlerinden okur; site sabit dosyalar olduğu için her
bağlantı türüne AYRI sayfa gerekir:
  · /invite/katil/       → arkadaş daveti  (uygulamanın ortak davet bağlantısı)
  · /invite/yakistirma/  → önererek davet  (aday taşıyan ortak davet bağlantısı)
  · 404.html             → tek kullanımlık kodlu bağlantılar (/invite/<kod>) buraya düşer → arkadaş daveti etiketi
İki alt sayfa 404.html'in KOPYASIDIR (aynı davet ekranı; yolu kendisi okur). 404.html değişince bu betik yeniden koşar.
Kullanım: python3 lab/davet-sayfalari.py
"""
import re, pathlib
L = pathlib.Path(__file__).resolve().parent.parent
B, S = 'DAVET-OG:BAŞ', 'DAVET-OG:SON'
BASLIK = 'shipship — Topluluk destekli tanışma uygulaması'
TUR = {
    'katil': dict(yol='/invite/katil/', gorsel='/img/davet-arkadas.jpg',
                  aciklama='Arkadaşın seni davet etti. Uygulamayı kur, kendi numaranla gir; arkadaşlığınız kendiliğinden kurulur.',
                  alt='Birbirine bakan iki kişi, arkalarında arkadaşları; üstünde shipship ve "Arkadaş çevreme katıl."'),
    'yakistirma': dict(yol='/invite/yakistirma/', gorsel='/img/davet-yakistirma.jpg',
                  aciklama='Arkadaşın seni biriyle yakıştırdı. Kim olduğunu uygulamada gör.',
                  alt='Bulanık bir kart ve soru işareti; yanında shipship ve "Sana birini yakıştırdım."'),
}

def og(t):
    d = TUR[t]
    return (f'<!-- {B} — üreten: lab/davet-sayfalari.py -->\n'
            f'  <meta property="og:type" content="website">\n'
            f'  <meta property="og:site_name" content="shipship">\n'
            f'  <meta property="og:locale" content="tr_TR">\n'
            f'  <meta property="og:url" content="https://shipshipapp.com{d["yol"]}">\n'
            f'  <meta property="og:title" content="{BASLIK}">\n'
            f'  <meta property="og:description" content="{d["aciklama"]}">\n'
            f'  <meta property="og:image" content="https://shipshipapp.com{d["gorsel"]}">\n'
            f'  <meta property="og:image:type" content="image/jpeg">\n'
            f'  <meta property="og:image:width" content="1200">\n'
            f'  <meta property="og:image:height" content="630">\n'
            f'  <meta property="og:image:alt" content="{d["alt"]}">\n'
            f'  <meta name="twitter:card" content="summary_large_image">\n'
            f'  <meta name="description" content="{d["aciklama"]}">\n'
            f'  <!-- {S} -->\n  ')

def uygula(s, t):
    s = re.sub(r'<!-- ' + B + r'.*?<!-- ' + S + r' -->\n\s*', '', s, flags=re.S)
    a = '<link rel="stylesheet" href="/ortak.css">'
    assert s.count(a) == 1
    return s.replace(a, og(t) + a, 1)

kaynak = (L / '404.html').read_text()
(L / '404.html').write_text(uygula(kaynak, 'katil')); print('yazıldı: 404.html')
for t in TUR:
    p = L / 'invite' / t / 'index.html'; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(uygula(kaynak, t)); print('yazıldı:', p.relative_to(L))
