"""Alt sayfaları ortak görünüme taşır (2026-09-27, tek seferlik dönüşüm; tekrar koşmak zararsız).

Her sayfada: <style> yerine /ortak.css (+ varsa sayfaya özel küçük ek) · aynı üst başlık
(.bar: wordmark + "Bekleme listesine katıl") · aynı alt bilgi (.foot). İçerik metnine DOKUNMAZ.
404 (davet) ve test sayfalarının gövdesi yeni sınıflarla yeniden yazılır, metinleri aynen korunur.
"""
import re, pathlib
L = pathlib.Path(__file__).resolve().parent.parent

HEAD_LINK = '<link rel="stylesheet" href="/ortak.css">'
BAR = ('<header class="bar"><a class="wordmark" href="/" aria-label="shipship ana sayfa">shipship</a>'
       '<a class="btn btn-sm" href="/#katil" id="barCta">Bekleme listesine katıl</a></header>')
FOOT = ('<footer class="foot"><span>© 2026 shipship</span><span><a href="/destek">Destek</a> · '
        '<a href="/kosullar">Koşullar</a> · <a href="/gizlilik">Gizlilik</a> · <a href="/guvenlik">Güvenlik</a></span></footer>')

def swap_style(s, extra=''):
    return re.sub(r'<style>.*?</style>', HEAD_LINK + (f'\n  <style>\n{extra}\n  </style>' if extra else ''), s, count=1, flags=re.S)

def swap_shell(s):
    s = re.sub(r'<header>.*?</header>', BAR, s, count=1, flags=re.S)
    s = re.sub(r'<footer>.*?</footer>', FOOT, s, count=1, flags=re.S)
    return s

def doc_page(rel, extra=''):
    p = L / rel; s = p.read_text()
    s = swap_shell(swap_style(s, extra))
    s = s.replace('class="callout"', 'class="box"')
    p.write_text(s); print('güncellendi:', rel)

doc_page('gizlilik/index.html')
doc_page('acik-riza/index.html')
doc_page('guvenlik/index.html')
doc_page('destek/index.html')
doc_page('kosullar/index.html',
         '    .caps { margin: 18px 0; padding: 18px 20px; border-radius: 16px; background: var(--tint); font-weight: 600; color: var(--ink); }')

# ─── 404 + davet karşılaması ───
p = L / '404.html'; s = p.read_text()
s = swap_style(s, '    .wrap .btn { margin-top: 28px; }\n    .wrap .hint { margin-top: 14px; }')
body = '''<body>
''' + BAR + '''
<main class="center">
  <div class="wrap" id="invite" hidden>
    <!-- İki varyant (2026-09-20): /invite/yakistirma ya da #y → arkadaşı onu BİRİYLE
         yakıştırmış (uygulamada "Listede yok mu? Davet et" yolu). Linkte ad/kişisel
         veri YOK; aday adı yalnız arkadaşın gönderdiği mesajda geçer. -->
    <h1 id="invTitle">Bir arkadaşın seni shipship'e davet ediyor</h1>
    <p class="lede" id="invSub">Topluluğun yakıştırdığı tanışma uygulaması. Arkadaşlarınla birbirinize aday önerirsiniz; tanışıp tanışmamak senin kararın.</p>
    <a class="btn btn-block" href="https://apps.apple.com/app/id6789615007">App Store'dan indir</a>
    <p class="hint">Kendi numaranla giriş yapman yeter, davet kendiliğinden bağlanır. Numaran kimseyle paylaşılmaz.</p>
  </div>

  <div class="wrap" id="notfound" hidden>
    <h1>Sayfa bulunamadı</h1>
    <p class="lede">Aradığın sayfa burada değil.</p>
    <a class="btn btn-line" href="/">Ana sayfaya dön</a>
  </div>
</main>
''' + FOOT + '''

<script>
  (function () {
    // /invite veya /invite/<herhangi> → davet karşılaması (kod yok; bağlantı
    // telefon eşleşmesiyle kurulur). Diğer yollar → sade 404.
    var invite = /^\\/invite(\\/|$)/.test(location.pathname);
    if (invite && (/^\\/invite\\/yakistirma\\/?$/.test(location.pathname) || location.hash === "#y")) {
      document.getElementById("invTitle").textContent = "Bir arkadaşın seni biriyle yakıştırdı";
      document.getElementById("invSub").textContent = "shipship'te ikilileri topluluk oylar. Uygulamayı indir, kendi numaranla gir; yakıştırıldığın kişiyle oylamaya çık. Tanışıp tanışmamak senin kararın.";
    }
    // Davet karşılamasında tek eylem App Store — üstteki bekleme listesi düğmesi onunla yarışmasın.
    if (invite) document.getElementById("barCta").hidden = true;
    document.getElementById(invite ? "invite" : "notfound").hidden = false;
  })();
</script>
</body>'''
s = re.sub(r'<body>.*</body>', lambda m: body, s, count=1, flags=re.S)
p.write_text(s); print('güncellendi: 404.html')

# ─── Test daveti ───
p = L / 'test/index.html'; s = p.read_text()
extra = '''    .kicker { display: inline-block; margin-bottom: 18px; font-size: 12px; font-weight: 700; letter-spacing: .12em;
      text-transform: uppercase; color: var(--soft); background: var(--tint); padding: 7px 14px; border-radius: 999px; }
    .lede + .lede { margin-top: 12px; }
    .facts { list-style: none; padding: 0; display: grid; gap: 12px; }
    .facts li { display: flex; gap: 11px; align-items: flex-start; font-size: 16px; line-height: 1.55; color: var(--soft); }
    .facts .ico { flex: none; width: 22px; text-align: center; }
    .facts b { color: var(--ink); }
    form { margin-top: 34px; }
    .radios { display: flex; gap: 10px; flex-wrap: wrap; }
    .radio { flex: 1 1 140px; display: flex; align-items: center; gap: 10px; min-height: 52px; padding: 0 16px; cursor: pointer;
      background: var(--surface); border: 1px solid var(--line-strong); border-radius: 14px; font-size: 16px; }
    .radio input { width: 20px; height: 20px; margin: 0; accent-color: var(--ink); }
    .radio:has(input:checked) { box-shadow: inset 0 0 0 1.5px var(--ink); border-color: var(--ink); }
    .honey { position: absolute; left: -9999px; opacity: 0; }
    .fineprint { margin-top: 14px; font-size: 13.5px; line-height: 1.55; color: var(--dim); }
    form .btn { margin-top: 8px; }'''
s = swap_style(s, extra)
s = re.sub(r'<div class="aura"></div>\s*', '', s)
s = re.sub(r'<header>.*?</header>', BAR, s, count=1, flags=re.S)
s = re.sub(r'<footer>.*?</footer>', FOOT, s, count=1, flags=re.S)
s = s.replace('<div class="card">', '<div class="box">')
s = s.replace('class="label"', 'class="lbl"')
s = re.sub(r'<label class="lbl" for="ad">Adın <span class="hint">\(isteğe bağlı\)</span></label>',
           '<label class="lbl" for="ad">Adın <span style="font-weight:400;color:var(--dim)">(isteğe bağlı)</span></label>', s)
s = s.replace('<span class="lbl">Telefonun</span>', '<span class="lbl">Telefonun</span>')
s = s.replace('<button type="submit">', '<button class="btn btn-block" type="submit">')
p.write_text(s); print('güncellendi: test/index.html')

p = L / 'test/tesekkurler/index.html'; s = p.read_text()
s = swap_style(s, '    .tick { width: 52px; height: 52px; border-radius: 50%; border: 2px solid var(--ok); color: var(--ok);\n'
                  '      display: flex; align-items: center; justify-content: center; font-size: 24px; margin-bottom: 22px; }\n'
                  '    main.center p { margin-top: 14px; font-size: 17px; line-height: 1.65; color: var(--soft); }\n'
                  '    main.center strong { color: var(--ink); }')
s = re.sub(r'<div class="aura"></div>\s*', '', s)
s = re.sub(r'<header>.*?</header>', BAR, s, count=1, flags=re.S)
s = re.sub(r'<footer>.*?</footer>', FOOT, s, count=1, flags=re.S)
s = s.replace('<main>', '<main class="center">', 1)
p.write_text(s); print('güncellendi: test/tesekkurler/index.html')
