"""Bekleme listesi — site parçalarını üretir (yayın hattı; lab/ yayına girmez).

  build.py page  [TARİH]              legal md -> /bekleme-listesi/index.html
  build.py liste URL KEY              kayıt yönetim sayfası -> /liste/index.html
  build.py inject SRC DST URL KEY [--preview]
                                      formu sayfaya ekler; zaten ekliyse YERİNİ
                                      DEĞİŞTİRİR (WL:BAŞ/WL:SON işaretleri)

URL/KEY: Supabase proje adresi + herkese açık (publishable) anahtar.
Kaynak metinler: crowdmatch-rn/legal/bekleme-listesi-aydinlatma.md (tek ev).
"""
import re, sys, html, pathlib
SP = pathlib.Path(__file__).parent
LAND = pathlib.Path.home() / 'Developer/shipship-landing'
MD = pathlib.Path.home() / 'Developer/crowdmatch-rn/legal/bekleme-listesi-aydinlatma.md'
B, S = 'WL:BAŞ', 'WL:SON'

def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', t)
    t = re.sub(r'\*(.+?)\*', r'<em>\1</em>', t)
    return t

def md_to_article(md, date_label):
    md = md.split('\n---\n')[0]            # hazırlayan notları siteye GİRMEZ
    lines = md.strip('\n').split('\n')
    out, para, i = [], [], 0
    def flush():
        if para: out.append('  <p>' + inline(' '.join(para)) + '</p>'); para.clear()
    while i < len(lines):
        l = lines[i]
        if l.startswith('# '):
            flush(); out.append('  <h1>' + inline(l[2:].replace('shipship — ', '')) + '</h1>')
            out.append(f'  <p class="meta">Son güncelleme: {date_label}</p>')
        elif l.startswith('*Son güncelleme'): pass
        elif l.startswith('## '): flush(); out.append('  <h2>' + inline(l[3:]) + '</h2>')
        elif l.startswith('|'):
            flush(); rows = []
            while i < len(lines) and lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip('|').split('|')]); i += 1
            head, body = rows[0], rows[2:]
            out.append('  <div class="tablewrap"><table>')
            out.append('    <tr>' + ''.join(f'<th>{inline(h)}</th>' for h in head) + '</tr>')
            for r in body:
                out.append('    <tr>' + ''.join(f'<td data-l="{html.escape(h)}">{inline(c)}</td>' for h, c in zip(head, r)) + '</tr>')
            out.append('  </table></div>'); continue
        elif l.startswith('- '):
            flush(); items = []
            while i < len(lines) and lines[i].startswith('- '):
                item = [lines[i][2:]]; i += 1
                while i < len(lines) and lines[i].startswith('  ') and lines[i].strip():
                    item.append(lines[i].strip()); i += 1
                items.append(' '.join(item))
            out.append('  <ul>' + ''.join(f'<li>{inline(x)}</li>' for x in items) + '</ul>'); continue
        elif not l.strip(): flush()
        else: para.append(l.strip())
        i += 1
    flush()
    a = '\n'.join(out)
    a = a.replace('kvkk@shipshipapp.com', '<a href="mailto:kvkk@shipshipapp.com">kvkk@shipshipapp.com</a>')
    return '<article class="doc">\n' + a + '\n</article>'

def from_template(article, title, desc, extra_head='', extra_body=''):
    tpl = (LAND / 'gizlilik/index.html').read_text()
    tpl = re.sub(r'<article class="doc">.*?</article>', lambda m: article, tpl, flags=re.S)
    tpl = re.sub(r'<title>.*?</title>', f'<title>{title}</title>', tpl, flags=re.S)
    tpl = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">', tpl)
    if extra_head: tpl = tpl.replace('</head>', '  <style>\n' + extra_head + '\n  </style>\n</head>', 1)
    if extra_body: tpl = tpl.replace('</body>', extra_body + '\n</body>', 1)
    return tpl

def write(rel, text):
    p = LAND / rel; p.parent.mkdir(exist_ok=True); p.write_text(text); print('yazıldı:', p)

def page(date_label):
    art = md_to_article(MD.read_text(), date_label)
    write('bekleme-listesi/index.html', from_template(
        art, 'Bekleme Listesi Aydınlatma Metni — shipship',
        'shipship bekleme listesi formunda verilerinin nasıl işlendiği.'))

def iller():
    m = re.search(r'var ILLER = (\[.*?\]);', (SP / 'wl.js').read_text())
    return m.group(1)

def liste(url, key):
    css = """    .field + .btn { margin-top: 0; }
    .doc > div > p + .btn { margin-top: 16px; }"""
    js = (SP / 'liste.js').read_text().replace('__WL_URL__', url).replace('__WL_KEY__', key).replace('__ILLER__', iller())
    tpl = from_template((SP / 'liste.html').read_text(), 'Bekleme listesi kaydın — shipship',
                        'shipship bekleme listesi kaydını yönet.', css, '<script>' + js + '</script>')
    tpl = tpl.replace('<meta name="robots" content="index,follow">', '<meta name="robots" content="noindex">', 1)
    # Kaydını yöneten kişi zaten listede — üstteki bekleme listesi düğmesi burada anlamsız.
    tpl = re.sub(r'<a class="btn btn-sm" href="/#katil" id="barCta">[^<]*</a>', '', tpl)
    write('liste/index.html', tpl)

def strip(s, url, key):
    """Eski eklemeyi çıkarır: önce işaretliyi, yoksa işaretsiz ilk sürümü (legacy/)."""
    # ÖNCE betik: stil deseni betiğin içini de yakalayıp boş <script></script> bırakıyordu (her koşuda biri birikti).
    s = re.sub(r'<script>/\* ' + B + r' \*/.*?/\* ' + S + r' \*/</script>\n?', '', s, flags=re.S)
    s = re.sub(r'\n?\s*/\* ' + B + r' \*/.*?/\* ' + S + r' \*/\n?', '', s, flags=re.S)
    s = re.sub(r'<script></script>\n?', '', s)
    # [ \t]* : girintili ekleme (hero düğmesi) de tam sökülür — yoksa her koşuda satıra boşluk birikiyordu.
    s = re.sub(r'\n?[ \t]*<!-- ' + B + r' -->.*?<!-- ' + S + r' -->\n?', '', s, flags=re.S)
    s = re.sub(r'(<div class="hero-copy">.*?</p>)[ \t\n]+(</div>)', r'\1\n          \2', s, count=1, flags=re.S)
    L = SP / 'legacy'
    if L.exists():
        ljs = (L / 'wl.js').read_text().replace('__WL_URL__', url).replace('__WL_KEY__', key)
        for old in ((L / 'wl.css').read_text(), (L / 'wl.html').read_text(), '<script>' + ljs + '</script>\n'):
            s = s.replace(old, '', 1)
    return s

def inject(src, dst, url, key, preview):
    s = strip(pathlib.Path(src).read_text(), url, key)
    if 'id="wl"' in s or 'wl-cta' in s: sys.exit('eski ekleme temizlenemedi: ' + src)
    css = f'\n  /* {B} */' + (SP / 'wl.css').read_text() + f'  /* {S} */\n'
    htm = f'\n<!-- {B} -->' + (SP / 'wl.html').read_text() + f'<!-- {S} -->\n'
    js = (SP / 'wl.js').read_text().replace('__WL_URL__', url).replace('__WL_KEY__', key)
    s = s.replace('</style>', css + '</style>', 1)
    # GERÇEK body etiketinin arkasına — stil açıklamasında geçen etiket yazımı ilk eşleşmeyi
    # çalıyordu (09-27: form stilin içine gömüldü).
    h = s.index('</head>'); b = s.index('<body>', h) + len('<body>')
    s = s[:b] + htm + s[b:]
    s = s.replace('</body>', f'<script>/* {B} */' + js + f'/* {S} */</script>\n</body>', 1)
    # Hero'da belirgin düğme — alt metnin hemen altına (ilk ekranda görünür).
    s, n = re.subn(r'(<div class="hero-copy">.*?</p>)',
                   lambda m: m.group(1) + f'\n            <!-- {B} --><a class="wl-hero-btn" href="#katil" data-wl-open>Bekleme listesine katıl</a><!-- {S} -->',
                   s, count=1, flags=re.S)
    if n != 1: sys.exit('hero metni bulunamadı: ' + src)
    s = re.sub(r'<a class="indir" id="finBtn"[^>]*>[^<]*</a>',
               '<a class="indir" id="finBtn" href="#" data-wl-open>Bekleme listesine katıl</a>', s)
    if preview and '<base href="/">' not in s: s = s.replace('<head>', '<head><base href="/">', 1)
    pathlib.Path(dst).write_text(s); print('yazıldı:', dst)

if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'page': page(sys.argv[2] if len(sys.argv) > 2 else 'TASLAK — yayında değil')
    elif cmd == 'liste': liste(sys.argv[2], sys.argv[3])
    elif cmd == 'inject': inject(*sys.argv[2:6], preview='--preview' in sys.argv)
    else: sys.exit(__doc__)
