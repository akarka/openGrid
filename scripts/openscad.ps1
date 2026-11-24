<#
OpenSCAD'i Docker içinde çalıştırır.
- Repo kökü konteynerde /work olarak bağlanır; çalışma dizini /work.
- OPENSCADPATH=/work/vendor  ->  include <BOSL2/std.scad> çalışır.
- Yollar repo köküne göre ve / ile verilir.

Örnek:
  .\scripts\openscad.ps1 -o build/x.stl -p scad/tiles.json -P test_lite_2x2_bant vendor/QuackWorks/openGrid/openGrid.scad
#>
$ErrorActionPreference = 'Stop'
$Image = 'openscad/openscad:dev.2026-11-09'
$Root  = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

docker run --rm -v "${Root}:/work" -w /work -e OPENSCADPATH=/work/vendor $Image `
    openscad --backend=manifold @args
exit $LASTEXITCODE
