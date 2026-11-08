# Hidden headless launcher - no popup, BelowNormal, single instance
$ErrorActionPreference='SilentlyContinue'
$repo='C:\Users\hyper\workspace\bob_and_lum_sitcom'
$log=Join-Path $repo 'dashboard.log'
$up=Get-NetTCPConnection -LocalPort 8080 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if($up){exit 0}
$pyw=(Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if(-not $pyw){$pyw=(Get-Command python.exe -ErrorAction SilentlyContinue).Source}
if(-not $pyw){exit 1}
$p=Start-Process -FilePath $pyw -ArgumentList @("$repo\dashboard.py","--port","8080","--host","127.0.0.1") -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError $log -PassThru
try{$p.PriorityClass='BelowNormal'}catch{}
exit 0