# build.ps1 - verify + refresh generated artifacts (BelowNormal, no popups)
# Usage: .\build.ps1 [-SkipHtml]   Exit non-zero on any failure.
param([switch]$SkipHtml)
$ErrorActionPreference = 'Stop'
$repo = $PSScriptRoot
Set-Location $repo
Write-Host "== Bob & Lum build (repo: $repo) =="
Write-Host "-- py_compile all scripts --"
$failed = $false
Get-ChildItem -File *.py, transcribeme\*.py | ForEach-Object {
  python -m py_compile $_.FullName
  if (-not $?) { Write-Host "FAIL compile $($_.FullName)"; $failed = $true }
}
if ($failed) { exit 1 }
Write-Host "-- corpus integrity check --"
python transcribeme\manage_corpus.py --check
if (-not $?) { exit 1 }
Write-Host "-- canon lint gate --"
python transcribeme\canon_lint.py
if (-not $?) { exit 1 }
Write-Host "-- unit tests --"
python -m unittest discover -s tests
if (-not $?) { exit 1 }
Write-Host "-- corpus stats --"
python transcribeme\manage_corpus.py --stats
Write-Host "-- re-index Kling prompts --"
python transcribeme\extract_kling_prompts.py
if (-not $?) { exit 1 }
if (-not $SkipHtml) {
  Write-Host "-- rebuild WordPress HTML --"
  python transcribeme\regen_wordpress_html.py
  if (-not $?) { exit 1 }
}
Write-Host "== build OK =="
