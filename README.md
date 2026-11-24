# Banyo dolabı kapağı — openGrid askı sistemi

Banyo dolabı kapağının iç yüzüne bantla yapıştırılan openGrid panoları ve bu panolara takılan
3D baskı askılar (Oral-B fırça başlığı askılığı, Braun Series 3 tarak yuvaları, ileride cihaz mountu).

Tasarım kuralları ve proje geçmişi: [CLAUDE.md](CLAUDE.md), [docs/devir-2026-11-24.md](docs/devir-2026-11-24.md).

## Klasör yapısı

| Yol | İçerik |
|---|---|
| `vendor/` | Dış repolar (git submodule). Değiştirilmez. |
| `vendor/QuackWorks/openGrid/` | Resmi openGrid karo generator'ı (OpenSCAD) ve snap kaynağı |
| `vendor/BOSL2/` | OpenSCAD kütüphanesi (generator'ın bağımlılığı) |
| `vendor/openGrid-docs/` | Resmi openGrid dokümantasyonu |
| `vendor/openGrid-openSCAD/` | Resmi openGrid OpenSCAD reposu (şimdilik beta kanallar) |
| `scad/tiles.json` | Bizim karo tiplerimiz — generator için OpenSCAD parametre setleri |
| `scripts/` | Docker'da OpenSCAD, karo üretimi, STL kontrolü |
| `blender/` | Askılar için Blender (bpy/bmesh) betikleri |
| `stl/` | Baskıya giden, versiyonlu STL'ler (commit edilir) |
| `docs/` | Notlar, kararlar, devir özetleri |
| `build/` | Ara çıktılar (git'e girmez) |

## Kurulum

```powershell
git clone --recurse-submodules <repo-url>
docker pull openscad/openscad:dev.2026-11-09
```

Gereken: Docker Desktop, Python 3, (askılar için) Blender 5.2 + Blender MCP.

## Kullanım

Karoları üret (her çıktı otomatik kontrol edilir: ölçü, manifold, 45° üstü çıkıntı):

```powershell
.\scripts\build-tiles.ps1                      # scad/tiles.json'daki tüm setler
.\scripts\build-tiles.ps1 test_lite_2x2_bant   # tek set
```

Herhangi bir OpenSCAD komutu (repo kökü konteynerde `/work`, `OPENSCADPATH=/work/vendor`):

```powershell
.\scripts\openscad.ps1 -o build/x.stl vendor/QuackWorks/openGrid/openGrid.scad
```

Bir STL'yi kontrol et (Z = baskıda yukarı):

```powershell
python scripts/stl_check.py stl/dosya.stl
```

## Lisans

Bu repo [Creative Commons Attribution-NonCommercial-ShareAlike 4.0](LICENSE) (CC-BY-NC-SA 4.0)
ile lisanslıdır. Ticari olmayan, kişisel kullanım içindir.

Bu repodaki parçalar şu çalışmalardan türetilmiştir:

- openGrid tasarımı — [DavidD](https://www.printables.com/@DavidD), CC-BY-NC-SA 4.0
- openGrid OpenSCAD generator ve snap kaynağı — BlackjackDuck / [QuackWorks](https://github.com/AndyLevesque/QuackWorks)
  ve katkıcıları, CC-BY-NC-SA 4.0

`vendor/` altındaki repolar git submodule'dür; içerikleri bu repoda bulunmaz ve kendi lisanslarına
tabidir (BOSL2: BSD-2-Clause).
