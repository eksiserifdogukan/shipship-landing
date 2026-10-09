# Arşiv · "Nasıl çalışıyor?" bölümü (omurga) — 2026-10-09'da yayından kalktı

**Karar (tasarımcı, 2026-10-09):** "nasıl çalışıyor alanını tamamen kaldır. arşivde kalsın. sonra tekrar
gösterebiliriz." Gerekçe aynı günkü değerlendirmede: telefon ekranları 2026-08-23/24'ten kalma ve bayattı
(Profil, karar kartı, kart göstergesi o tarihten beri değişti; "Görünürlüğünü gizleyebilirsin" ekranı neredeyse
boştu); bekleme listesi döneminde akışın tamamını göstermek merakı azaltabilir.

**Bu klasör yayına girmez** (`lab/` main'de `.gitignore`'da). Yedeği `lab-yedek` dalında.

## İçerik

| Dosya | Ne |
|---|---|
| `bolum.html` | Bölümün HTML'i (`<section class="spine">`, 6 adım + telefon + oy kartları; mobil adım görselleri `step-shot` içinde) |
| `stil.css` | Bölümün masaüstü stili (telefon gövdesi, ekran geçişi, oy kartları) |
| `kod.js` | Kaydırma kodu: değişkenler + döngüdeki "2 · OMURGA" bloğu (aktif adım, telefon titremesi, oy koreografisi) |
| `kaynak/index-son-hali.html` | Bölüm kalkmadan önceki CANLI ana sayfanın tamamı (landing `cf5df69`) |
| `kaynak/site-son-hali.html` | Aynı anın `lab/site.html` taslağı |
| `kaynak/mobil.py` · `kaynak/menu.py` · `kaynak/wl.css` | Bölümü de üreten üç kaynağın o anki hâli (mobil adım görselleri · üst "Nasıl çalışıyor" bağlantısı · yapışkan bandın cam altı kuralı) |
| `img/` | 10 ekran görüntüsü (2026-08-23; App Store setinden) |

## Geri getirme

En kısa yol: bölümü kaldıran commit'i geri al — landing `main`de **`98dc4b4`** (`git revert 98dc4b4`; img/
dosyalarını da geri getirir). `lab/site.html` taslağı git'te izlenmediği için o dosyaya aşağıdaki adımlar elle
uygulanır. Arada sayfa çok değiştiyse elle:

1. `bolum.html`i hikâye bölümünden sonra, `<!-- ═══ 3b · DEĞER TEKERLEĞİ ═══ -->`ın önüne koy.
2. `stil.css`i `/* ═══ 3b · DEĞER TEKERLEĞİ` stilinin önüne koy.
3. `kod.js`: değişkenleri `evoYolKur(); addEventListener('resize', evoYolKur);` satırının altına, döngü bloğunu
   `/* 3b · TEKERLEK — F20 */` yorumunun önüne koy; `DURAK_SEC` listesine `.spine-scroll` ekle.
4. Üst bağlantı: `kaynak/menu.py`deki `<nav class="mn-nav">` (+ CSS'i) geri gelir.
5. Telefon: `kaynak/mobil.py`deki `.spine-col` · `.stage-head` · `.step` · `.step-shot` kuralları ve adım görselleri;
   telefonda sayfa yeniden "hero + Nasıl çalışıyor + alt bilgi" olur.
6. `kaynak/wl.css`deki `.stage-head` kuralları (bant camın altına uzanır).
7. `img/` dosyalarını kökteki `img/`ye kopyala.
8. Kaldırırken eklenen `.story{overflow:clip}` geri getirmede zararsız, kalabilir (omurga zaten örtüyordu).

⚠️ **Ekranlar bayat.** Yeniden göstermeden önce güncel uygulama ekranlarıyla değiştir (App Store ekran görüntüsü
setiyle aynı kaynak — ürün BACKLOG "TR+EN kare setleri SON UI ile").
