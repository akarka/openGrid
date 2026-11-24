<#
openGrid karolarını resmi generator ile (vendor/QuackWorks/openGrid/openGrid.scad) üretir.
Karo tipleri scad/tiles.json içinde OpenSCAD parametre seti olarak tanımlıdır.
Çıktı: build/tiles/<set>.stl (binary). Her çıktı scripts/stl_check.py ile kontrol edilir.

Örnek:
  .\scripts\build-tiles.ps1                       # tüm setler
  .\scripts\build-tiles.ps1 test_lite_2x2_bant    # tek set
#>
param([string[]]$Sets)
$ErrorActionPreference = 'Stop'
$Root   = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Params = 'scad/tiles.json'
$Gen    = 'vendor/QuackWorks/openGrid/openGrid.scad'

$all = (Get-Content (Join-Path $Root $Params) -Raw | ConvertFrom-Json).parameterSets.PSObject.Properties.Name
if (-not $Sets) { $Sets = $all }
New-Item -ItemType Directory -Force (Join-Path $Root 'build/tiles') | Out-Null

foreach ($s in $Sets) {
    if ($all -notcontains $s) { throw "Parametre seti yok: $s" }
    $out = "build/tiles/$s.stl"
    Write-Host "== $s -> $out"
    & (Join-Path $PSScriptRoot 'openscad.ps1') --export-format binstl -o $out -p $Params -P $s $Gen
    if ($LASTEXITCODE -ne 0) { throw "OpenSCAD hata verdi: $s" }
    python (Join-Path $PSScriptRoot 'stl_check.py') (Join-Path $Root $out)
}
