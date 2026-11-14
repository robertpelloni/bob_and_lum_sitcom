# Hidden headless launcher - no popup, BelowNormal, single-instance (identity-checked)
# Port 8765: 8080 on this laptop belongs to another local service, never kill/assume it.
$ErrorActionPreference = 'SilentlyContinue'
$repo = 'C:\Users\hyper\workspace\bob_and_lum_sitcom'
$log = Join-Path $repo 'dashboard.log'
$port = 8765
try {
  $r = Invoke-RestMethod -TimeoutSec 2 "http://127.0.0.1:$port/api/status"
  if ($r.app -eq 'bob-and-lum-dashboard') { exit 0 }  # already our dashboard
} catch {}
if (Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue) { exit 2 } # held by something else
$pyw = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $pyw) { $pyw = (Get-Command python.exe -ErrorAction SilentlyContinue).Source }
if (-not $pyw) { exit 1 }
$p = Start-Process -FilePath $pyw -ArgumentList @("$repo\dashboard.py", '--port', "$port", '--host', '127.0.0.1') -WindowStyle Hidden -RedirectStandardOutput $log -RedirectStandardError "$log.err" -PassThru
try { $p.PriorityClass = 'BelowNormal' } catch {}
exit 0
