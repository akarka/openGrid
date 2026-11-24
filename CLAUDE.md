# Proje kuralları

Ayrıntılı geçmiş ve ölçüler: `docs/devir-2026-11-24.md`. Yapı ve komutlar: `README.md`.

## Çalışma

- Türkçe, kısa ve net. Geri bildirim çoğu zaman ekran görüntüsü üstüne kırmızı eskiz.
- "Önce test edeyim" denince modele dokunma; bulguları bekle.
- Bir şey olmayacaksa nedenini somut geometriyle (gerekirse 2D eskizle) açıkla.
- Fikri uygulamadan önce baskı yönünü, çıkıntıları ve takılma yolunu kontrol et.
- Büyük modelleme işinden önce kısa plan sun.
- `vendor/` altına dokunma; uyarlamalar `scad/`, `blender/` içinde.
- Yerel çalışma klasöründeki `firca_basligi_tutacagi.blend` dosyasına dokunma.

## Donanım ve FDM (kesin)

- Baskı hacmi 160 × 160 × 160 mm. Kapağa vida yok; 3M / çift taraflı bant.
- Çıkıntı ≤ 45°, köprü yok, desteksiz.
- Eğilme yükü katmanların içinde kalmalı (dik basılan pimler katman kökünden kırıldı).
- Uzun-ince dik parçalara 5–8 mm brim. Küçük delik yerine eğim.
- Kapak çarpınca kuvvet kapağa dik; kapak düzleminde yatay kuvvet çok küçük.

## Dolap

- Genişlik 450 mm. Raflar arası net yükseklik (yukarıdan): 195 / 170 / 220 mm, her kenardan ~5 mm tolerans.
- Raflar kapağın hemen arkasında: hiçbir askı kendi bölgesinin dışına taşamaz.

## Tasarım dili

- G2 geçişler: smootherstep g2(t) = t³(10 − 15t + 6t²), açı g2 ile döndürülüp entegre edilir.
- Köşelerde süperelips p = 3. En az sayıda açı; 45° ana açı.
- Sevilmeyen: ani kırık (45°→90°), kaba üçgen payanda/ayak, sonradan yapıştırılmış görünen parçalar.
- Sevilen: tek parça okunan form ("saplanmış" dil), kalp motifi.
- Parametrik kur; indirilmiş STL'ler yalnızca ölçü kaynağı.

## Doğrulama

- Her parçayı gerçek baskı yönünde tara: `python scripts/stl_check.py` (normal.z < −0,7072, alan > 0).
- Takılma yolu: takılan nesnenin hacmini prizma olarak kur, takma yönünün tersine 0→~40 mm adımla, `BVHTree.overlap`.
- Blender boolean: EXACT, her adımda `is_manifold`; yüzleri 0,05–0,5 mm iç içe geçir; `remove_doubles(0.0005)`.
- STL: binary, local koordinat, Z = baskıda yukarı, versiyonlu dosya adı.

## openGrid (doğrulandı, kaynak: vendor/)

- Grid 28 mm. Full 6,8 mm, Lite 4 mm (Full kesitinin ön 4 mm'si). Lite snap 3,4 mm.
- Hücre ağzı 25,0 mm (0,4 pah); 1,4–2,4 mm derinlikte 45° ile 26,4 mm'ye açılır.
- Snap 24,8 × 24,8 mm; tıklama dişleri 0,4 mm. Tipler: normal, directional (ok yukarı), lock.
- Lite `Add_Adhesive_Base`: arkada 0,6 mm dolu taban → bant için düz yüz (toplam 4,6 mm).
- Kenar bağlantı cepleri 2,4 mm yüksek, ön yüzden 1 mm içeride; tavanı ~5 mm köprü.
