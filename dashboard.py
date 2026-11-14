#!/usr/bin/env python3
"""Unified Bob & Lum Sitcom Dashboard Server (single page, v1.5.0).

One page, high-value first: Overview/status -> Screenplays & Library docs ->
Kling Prompts -> Corpus Search -> Files -> Pipeline/scripts -> Canon -> System.
Every repo feature is represented here; no subpages.

Usage: python dashboard.py [--port 8765] [--host 127.0.0.1]
Default port 8765 (8080 is contested on this laptop by another local proxy).
All heavy work runs BelowNormal so the desktop never hangs.
"""
import argparse, hashlib, html, http.server, json, os, re, socketserver, sqlite3, subprocess, sys, threading, time, urllib.parse
from pathlib import Path

STARTED = time.time()
def lower_self_priority():
    try:
        if os.name == 'nt':
            import ctypes
            ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000)
        else:
            try: os.nice(10)
            except Exception: pass
    except Exception: pass

REPO_ROOT = Path(__file__).resolve().parent
DB_PATH = REPO_ROOT / "transcribeme" / "catalog.db"
CORPUS_PATH = REPO_ROOT / "CONVERSATION_SCRIPT_COMPLETE.txt"
LOG_PATH = REPO_ROOT / "dashboard.log"

def read_version():
    try: return (REPO_ROOT / "VERSION.md").read_text(encoding="utf-8").strip() or "?"
    except Exception: return "?"

# Allowlisted documents: key -> (filename, label, group, description)
DOCS = {
 "s1": ("sitcom_final_s1.md", "Season 1 (final)", "Screenplay", "12 canonical episodes, 51 Kling prompts. Start here."),
 "s2": ("sitcom_final_s2.md", "Season 2 (final)", "Screenplay", "8 episodes + 6 bonus, 51 Kling prompts."),
 "rewrite_s2": ("sitcom_rewrite_s2.md", "Season 2 rewrite drafts", "Screenplay", "Thematic drafts/breakdown behind final S2."),
 "full_screenplay": ("sitcom_bob_and_lum_full_screenplay.md", "Full screenplay (master draft)", "Screenplay", "Multi-episode master draft, pre-final split."),
 "full_series": ("sitcom_bob_and_lum_full_series.md", "Full series bible", "Screenplay", "Series bible + episode guide."),
 "dark": ("sitcom_bob_and_lum_DARK.md", "DARK cut", "Screenplay", "Darker alternate cut."),
 "episode1": ("sitcom_bob_and_lum_episode1.md", "Episode 1 standalone", "Screenplay", "Standalone pilot draft."),
 "dark_kling": ("sitcom_bob_and_lum_DARK_KLING.md", "DARK Kling prompts", "Kling source", "Kling prompts for the DARK cut (not in DB)."),
 "episode1_kling": ("sitcom_bob_and_lum_episode1_kling.md", "Episode 1 Kling prompts", "Kling source", "Kling prompts for pilot (not in DB)."),
 "full_series_kling": ("sitcom_bob_and_lum_full_series_kling.md", "Full-series Kling prompts", "Kling source", "Kling prompts for full series (not in DB)."),
 "vision": ("VISION.md", "VISION", "Docs", "Ultimate goal, themes, production strategy."),
 "memory": ("MEMORY.md", "MEMORY (canon)", "Docs", "Immutable canon + architecture notes."),
 "roadmap": ("ROADMAP.md", "ROADMAP", "Docs", "Long-term milestones."),
 "todo": ("TODO.md", "TODO", "Docs", "Granular immediate tasks."),
 "ideas": ("IDEAS.md", "IDEAS", "Docs", "Pivots, expansions, R&D."),
 "deploy": ("DEPLOY.md", "DEPLOY / Manual", "Docs", "Setup, run, build, troubleshooting manual."),
 "changelog": ("CHANGELOG.md", "CHANGELOG", "Docs", "Every release, by version."),
 "handoff": ("HANDOFF.md", "HANDOFF", "Docs", "Session state for successor models."),
 "readme": ("README.md", "README", "Docs", "Honest project overview."),
}
SCRIPT_DESCS = {
 "dashboard.py": "This dashboard server (single page, stdlib only).",
 "tray_runner.py": "System-tray controller: open/start/stop/restart/quit dashboard.",
 "transcribeme/manage_corpus.py": "Corpus CLI: --check integrity, --stats, --build-html.",
 "transcribeme/extract_kling_prompts.py": "Re-index 102 Kling prompts from final S1/S2 into catalog.db.",
 "transcribeme/regen_wordpress_html.py": "Rebuild CONVERSATION_SCRIPT_COMPLETE.wordpress.html from corpus.",
 "transcribeme/canon_lint.py": "Canon gate: fails on Pop-Tarts/Rob/Lung/Noah violations in sitcom*.md (runs in build.ps1).",
 "transcribeme/deep_clean_rebuild.py": "Deep-clean new transcripts, assign speakers, append to corpus.",
 "transcribeme/rebuild_combined.py": "Rebuild combined corpus from unique transcribeme sessions.",
 "transcribeme/normalize_headers.py": "Normalize session headers in combined corpus.",
 "transcribeme/diff_new_sessions.py": "Diff new sessions vs combined corpus.",
 "transcribeme/extract_char_quotes.py": "Extract character quotes.",
 "transcribeme/canon_rewrite.py": "Canon rewrite pass 1 (Pop-Tarts/names/deaths).",
 "transcribeme/canon_rewrite_p2.py": "Canon rewrite pass 2 (leftovers).",
 "transcribeme/canon_rewrite_p3.py": "Canon rewrite pass 3 (full_screenplay Pop-Tarts).",
 "transcribeme/patch_characters_v2.py": "Patch character sheets with new transcript facts.",
 "transcribeme/patch_full_series.py": "Update full-series bible cast/episode rows.",
 "transcribeme/patch_historical_cuts.py": "Mark older cuts historical, refresh bible guide.",
 "transcribeme/update_characters_episodes.py": "Update character defs + episode guides in finals.",
 "transcribeme/insert_new_episodes.py": "Insert episode scripts + prompts for guide-only rows.",
 "transcribeme/insert_261005_episodes.py": "Add Voice 261005 episodes + patch compilations.",
 "transcribeme/ingest_261005.py": "Ingest Voice 261005 tape as session 247.",
}

def sha12(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""): h.update(chunk)
    return h.hexdigest()[:12]

_stats_cache = {}
def corpus_stats():
    if not CORPUS_PATH.exists(): return {}
    st = CORPUS_PATH.stat(); key = (st.st_mtime_ns, st.st_size)
    if _stats_cache.get("key") == key: return _stats_cache["val"]
    text = CORPUS_PATH.read_text(encoding="utf-8", errors="replace")
    twin = REPO_ROOT / "sitcom script.txt"
    # Cache by (mtime,size): /api/status is polled and must not re-hash 6MB per call.
    val = {"bytes": st.st_size, "lines": text.count("\n")+1,
      "sessions": len(re.findall(r"^\[\d+\]\s+.+$", text, re.M)),
      "bob_cues": len(re.findall(r"^Bob:\s+", text, re.M)), "lum_cues": len(re.findall(r"^Lum:\s+", text, re.M)),
      "sha12": sha12(CORPUS_PATH), "twin_identical": twin.exists() and sha12(twin) == sha12(CORPUS_PATH)}
    _stats_cache.update({"key": key, "val": val}); return val

def db_stats():
    if not DB_PATH.exists(): return {}
    try:
        c = sqlite3.connect(DB_PATH); out = {}
        out["tables"] = {t[0]: c.execute(f'SELECT count(*) FROM "{t[0]}"').fetchone()[0] for t in c.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        try: out["prompts_by_season"] = dict(c.execute("SELECT season,count(*) FROM kling_prompts GROUP BY season").fetchall())
        except Exception: pass
        c.close(); return out
    except Exception as e: return {"error": str(e)}

def status_payload(port):
    files = {}
    for key, (fn, label, grp, desc) in DOCS.items():
        p = REPO_ROOT / fn; files[key] = {"file": fn, "label": label, "group": grp, "desc": desc, "exists": p.exists(), "bytes": p.stat().st_size if p.exists() else 0}
    return {"app": "bob-and-lum-dashboard", "version": read_version(), "pid": os.getpid(), "port": port,
      "python": sys.version.split()[0], "platform": sys.platform, "uptime_s": int(time.time()-STARTED),
      "repo": str(REPO_ROOT), "corpus": corpus_stats(), "db": db_stats(), "docs": files,
      "transcribeme_txt": len(list((REPO_ROOT/"transcribeme").glob("*.txt"))) if (REPO_ROOT/"transcribeme").exists() else 0,
      "identity": "muse-wonder-1.0 in Muse Code in bob_and_lum_sitcom on laptop"}

def list_files():
    out = []
    for p in sorted(REPO_ROOT.iterdir()):
        if p.is_file() and p.suffix.lower() in {".md",".txt",".html",".py",".ps1",".vbs"} and not p.name.startswith(".tmp") and p.name != "_probe.py":
            out.append({"name": p.name, "bytes": p.stat().st_size, "kind": p.suffix.lower(), "desc": SCRIPT_DESCS.get(p.name, "")})
    tm = REPO_ROOT / "transcribeme"
    if tm.exists():
        for p in sorted(tm.glob("*.py")):
            rel = f"transcribeme/{p.name}"; out.append({"name": rel, "bytes": p.stat().st_size, "kind": ".py", "desc": SCRIPT_DESCS.get(rel, "")})
        if DB_PATH.exists(): out.append({"name": "transcribeme/catalog.db", "bytes": DB_PATH.stat().st_size, "kind": ".db", "desc": "SQLite catalog: kling_prompts (102) + legacy MCP tables."})
    return out

def run_action(argv):
    try:
        r = subprocess.run([sys.executable]+argv, cwd=str(REPO_ROOT), capture_output=True, text=True, timeout=180)
        out = (r.stdout + "\n" + r.stderr).strip()
        return {"ok": r.returncode == 0, "returncode": r.returncode, "output": out[-4000:], "message": "OK" if r.returncode == 0 else f"Exited {r.returncode} - see output"}
    except Exception as e:
        return {"ok": False, "returncode": -1, "output": str(e), "message": str(e)}

HTML_TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Bob &amp; Lum Sitcom - Unified Dashboard</title><style>
:root{--bg:#0d1117;--card:#161b22;--border:#30363d;--text:#c9d1d9;--head:#f0f6fc;--acc:#58a6ff;--danger:#f85149;--ok:#3fb950;--bob:#58a6ff;--lum:#e3b341;--code:#090d13}
*{box-sizing:border-box;margin:0;padding:0}body{font-family:-apple-system,"Segoe UI",Roboto,Arial,sans-serif;background:var(--bg);color:var(--text)}
header{position:sticky;top:0;z-index:10;background:var(--card);border-bottom:1px solid var(--border);padding:10px 20px;display:flex;flex-wrap:wrap;gap:10px;align-items:center;justify-content:space-between}
header h1{font-size:1.15rem;color:var(--head)} .badge{background:#238636;color:#fff;padding:2px 8px;border-radius:12px;font-size:.75rem;font-weight:700}
nav{display:flex;flex-wrap:wrap;gap:6px} nav a{color:var(--text);text-decoration:none;border:1px solid var(--border);padding:5px 10px;border-radius:6px;font-size:.85rem} nav a:hover{background:#21262d;color:var(--head)}
main{max-width:1180px;margin:0 auto;padding:18px} section{scroll-margin-top:80px;margin-bottom:28px}
.card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:18px;margin-bottom:16px}
.card h2{color:var(--head);font-size:1.05rem;margin-bottom:8px;border-bottom:1px solid var(--border);padding-bottom:8px}
.help{cursor:help;color:var(--acc);font-weight:700} .sub{color:#8b949e;font-size:.82rem;line-height:1.5}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin-bottom:16px}
.metric{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:14px}.metric .v{font-size:1.55rem;font-weight:700;color:var(--head);margin:6px 0 2px}
.btn{background:#21262d;border:1px solid var(--border);color:var(--text);padding:6px 12px;border-radius:6px;cursor:pointer;font-size:.85rem}.btn:hover{background:#30363d}.btn-danger{color:var(--danger)}
input,select{background:var(--code);border:1px solid var(--border);color:var(--text);padding:8px 10px;border-radius:6px;font-size:.9rem}
.prompt-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:12px}.prompt-card{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:14px}
.prompt-body{font-family:monospace;font-size:.85rem;background:var(--code);border:1px solid #21262d;border-radius:6px;padding:10px;max-height:150px;overflow:auto;white-space:pre-wrap;margin:8px 0}
.viewer{background:var(--card);border:1px solid var(--border);border-radius:8px;padding:18px;line-height:1.55;max-height:70vh;overflow:auto}
.viewer h1,.viewer h2,.viewer h3{color:var(--head);margin:16px 0 8px}.viewer p{margin:0 0 10px}.viewer ul{margin:0 0 10px 20px}.viewer code{background:var(--code);padding:1px 5px;border-radius:4px}.viewer pre{background:var(--code);padding:12px;border-radius:6px;white-space:pre-wrap;margin:0 0 10px}.viewer hr{border:0;border-top:1px solid var(--border);margin:16px 0}.viewer table{margin:0 0 12px}
table{width:100%;border-collapse:collapse;font-size:.85rem} td,th{border-bottom:1px solid var(--border);padding:6px 8px;text-align:left;vertical-align:top}
.result-item{padding:10px;border-bottom:1px solid var(--border)} .sp-Bob{color:var(--bob);font-weight:700}.sp-Lum{color:var(--lum);font-weight:700}
#action-log{white-space:pre-wrap;background:var(--code);border:1px solid var(--border);border-radius:6px;padding:12px;max-height:260px;overflow:auto;font-size:.8rem}
.pill{font-size:.75rem;border:1px solid var(--border);border-radius:12px;padding:2px 8px}
</style></head><body>
<header><div style="display:flex;gap:10px;align-items:center"><h1>Bob &amp; Lum Sitcom</h1><span class="badge" id="ver" title="Version from VERSION.md (single source of truth)">v?</span><span class="pill" id="livepill" title="Live status from /api/status">loading...</span></div>
<nav>
<a href="#sec-overview" title="Highest value first: live health, counts, parity">Overview</a>
<a href="#sec-read" title="Read every screenplay and project doc in one viewer">Screenplays &amp; Docs</a>
<a href="#sec-prompts" title="Browse/copy all Kling video prompts in catalog.db">Kling Prompts</a>
<a href="#sec-corpus" title="Full-text search the 247-session transcript corpus">Corpus Search</a>
<a href="#sec-files" title="Every file in the repo with size and role">Library / Files</a>
<a href="#sec-pipeline" title="Run corpus/prompt/HTML pipeline jobs and see real output">Pipeline &amp; Scripts</a>
<a href="#sec-canon" title="Immutable canon rules - read before editing scripts">Canon</a>
<a href="#sec-system" title="Tray, launchers, logs, quit/restart">System</a>
</nav>
<div><button class="btn" onclick="loadStatus()" title="Re-fetch /api/status and repaint metrics">Refresh status</button>
<button class="btn btn-danger" onclick="quitServer()" title="Stop this dashboard server process (tray can restart it)">Quit dashboard</button></div></header>
<main>
<section id="sec-overview"><div class="grid" id="metrics"><div class="metric">Loading live status...</div></div>
<div class="card"><h2>What this is <span class="help" title="Dark-comedy sitcom from real Bob & Lum transcripts. Scripts + Kling prompts + searchable corpus, one page, no subpages.">?</span></h2>
<p class="sub">One consolidated page for the whole project, ordered by value: read the final screenplays, copy Kling prompts, search the raw corpus, run the pipeline, check canon. Nothing lives on a separate page anymore. Port 8080 on this laptop belongs to another local service, so this dashboard defaults to <b>8765</b>.</p>
<p class="sub" id="identity" style="margin-top:8px"></p></div></section>

<section id="sec-read"><div class="card"><h2>Screenplays &amp; Docs - one viewer <span class="help" title="Pick any screenplay, Kling source, or governance doc. Final S1/S2 are canonical; DARK/full-series/episode1 are alternate/older cuts. Docs are VISION/MEMORY/ROADMAP/TODO/IDEAS/DEPLOY/CHANGELOG/HANDOFF/README.">?</span></h2>
<p class="sub" style="margin-bottom:10px">All writing in one place - no hunting through the folder. Start with Season 1 (final).</p>
<div style="display:flex;gap:8px;flex-wrap:wrap"><select id="doc-select" title="Choose a screenplay or document to read"></select>
<button class="btn" onclick="loadDoc()" title="Load the selected file into the viewer below">Load</button>
<select id="doc-mode" onchange="renderDoc()" title="Rendered formats headings/bold/lists; Plain shows the raw markdown"><option value="md">Rendered</option><option value="plain">Plain text</option></select>
<select id="doc-speaker" onchange="renderDoc()" title="Filter dialogue: show only Bob lines, only Lum lines, or everything (headings always kept)"><option value="all">All speakers</option><option value="Bob">Bob lines only</option><option value="Lum">Lum lines only</option></select>
<span class="sub" id="doc-meta"></span></div></div>
<div class="viewer" id="doc-viewer">Select a document and press Load.</div></section>

<section id="sec-prompts"><div class="card"><h2>Kling Prompts <span class="help" title="102 prompts indexed in transcribeme/catalog.db (51 per season) from final S1/S2. DARK/episode1/full-series Kling files are readable in the viewer above but not yet indexed - see TODO.">?</span></h2>
<div style="display:flex;gap:8px;flex-wrap:wrap;margin-bottom:10px">
<select id="prompt-source" onchange="loadPrompts()" title="Canonical = 102 prompts from final S1/S2 in catalog.db. Historical = pre-final DARK/episode1/full-series prompts, indexed separately and labelled by source file"><option value="canonical">Canonical (final S1/S2)</option><option value="historical">Historical archive</option></select>
<select id="season-filter" onchange="filterPrompts()" title="Filter by season"><option value="all">All seasons</option><option value="1">Season 1</option><option value="2">Season 2</option></select>
<input id="prompt-search" placeholder="Filter prompts by keyword..." oninput="filterPrompts()" title="Matches title, episode and prompt text" style="flex:1;min-width:200px">
<button class="btn" onclick="copyAllPrompts()" title="Copy every currently filtered prompt to the clipboard">Copy filtered</button>
<span class="sub" id="prompt-count"></span></div>
<div class="prompt-grid" id="prompts-container">Loading prompts...</div></div></section>

<section id="sec-corpus"><div class="card"><h2>Corpus Search <span class="help" title="Case-insensitive substring search over CONVERSATION_SCRIPT_COMPLETE.txt (247 sessions). Returns first 50 hits with line numbers. Try: adapter, Sting Ray, hologram, blazer, dashboard">?</span></h2>
<div style="display:flex;gap:8px"><input id="corpus-query" placeholder="Search 258k lines..." style="flex:1" onkeydown="if(event.key==='Enter')searchCorpus()" title="Type a phrase, press Enter">
<button class="btn" onclick="searchCorpus()" title="Run the search">Search</button></div>
<div class="sub" id="search-status" style="margin:8px 0"></div><div style="display:flex;gap:8px;margin-bottom:8px"><button class="btn" id="search-prev" onclick="pageSearch(-1)" title="Previous 50 hits" disabled>Previous 50</button><button class="btn" id="search-next" onclick="pageSearch(1)" title="Next 50 hits" disabled>Next 50</button></div><div id="search-results"></div></div></section>

<section id="sec-files"><div class="card"><h2>Library / Files <span class="help" title="Every root document/script and every transcribeme pipeline script, with size and role. Raw transcripts (620 .txt in transcribeme/) feed the corpus; they are data, not pages.">?</span></h2>
<input id="file-filter" placeholder="Filter files..." oninput="renderFiles()" title="Filter by name or description" style="width:100%;margin-bottom:10px">
<div style="max-height:420px;overflow:auto"><table><thead><tr><th>File</th><th>Size</th><th>Role</th></tr></thead><tbody id="files-body"></tbody></table></div></div></section>

<section id="sec-pipeline"><div class="card"><h2>Pipeline &amp; Scripts <span class="help" title="Jobs run on the server at BelowNormal priority and return real stdout/stderr + exit code below. Re-index prompts after editing final S1/S2; rebuild HTML after corpus changes; check before committing.">?</span></h2>
<p class="sub" style="margin-bottom:10px">One-click jobs (output appears in the log panel, success is never faked):</p>
<button class="btn" onclick="runAction('/api/check','Corpus integrity check')" title="manage_corpus.py --check: byte-parity, sessions, HTML presence">Check corpus integrity</button>
<button class="btn" onclick="runAction('/api/stats','Corpus stats')" title="manage_corpus.py --stats: lines, sessions, Bob/Lum cues">Corpus stats</button>
<button class="btn" onclick="runAction('/api/extract-prompts','Re-index Kling prompts')" title="extract_kling_prompts.py: rebuild kling_prompts table from final S1/S2">Re-index Kling prompts</button>
<button class="btn" onclick="runAction('/api/rebuild-html','Rebuild WordPress HTML')" title="regen_wordpress_html.py: rebuild the HTML corpus reader">Rebuild WordPress HTML</button>
<p class="sub" style="margin:12px 0 6px">All pipeline scripts (also listed under Library):</p><div id="script-list" class="sub"></div>
<h3 style="color:var(--head);margin:14px 0 6px;font-size:.95rem">Job output</h3><div id="action-log">No job run yet this session.</div></div></section>

<section id="sec-canon"><div class="card"><h2>Canon - do not break <span class="help" title="Full canon in MEMORY.md (viewer above). Violations found by canon_rewrite scripts in the past; check before editing any screenplay.">?</span></h2>
<ul style="margin-left:20px;line-height:1.8;font-size:.9rem">
<li><b>Bob's sacraments:</b> yogurt, coffee, pizza. <i>Never Pop-Tarts.</i> Holds cold pizza like cigarettes.</li>
<li><b>Sacrifices (never conflate):</b> Chris Papa died for <i>both</i>; Noah died <i>next to Lum</i>; Crystal's dad died saving Bob &amp; Crystal.</li>
<li><b>Tech ancestry:</b> USB flash drives = Bob; gas-station burners = Lum &amp; Harry.</li>
<li><b>Names:</b> BOB/LUM never Rob/Lung; Shonna, Agathi, Ajja, Harry (Halalambos), Chris Papa.</li>
<li><b>Motif:</b> the dashboard on Bob's dual-monitor rig is perpetually broken. It is liturgy.</li></ul></div></section>

<section id="sec-system"><div class="card"><h2>System, Tray &amp; Logs <span class="help" title="Tray: run tray_runner.py for a system-tray icon (Open/Start/Stop/Restart/Check/Quit). Hidden launcher: start_dashboard_hidden.vbs (no popup, BelowNormal, single-instance on 8765). Quit here stops only this dashboard process.">?</span></h2>
<div id="sysinfo" class="sub" style="line-height:1.7">Loading...</div>
<div style="margin-top:10px;display:flex;gap:8px;flex-wrap:wrap">
<button class="btn" onclick="loadLog()" title="Show the last lines of dashboard.log">View dashboard.log</button>
<button class="btn" onclick="loadStatus()" title="Re-fetch live status">Refresh status</button>
<button class="btn btn-danger" onclick="quitServer()" title="Stop this dashboard server (POST /api/quit)">Quit dashboard</button></div>
<pre class="viewer" id="log-viewer" style="margin-top:12px;max-height:220px">Log not loaded.</pre>
<p class="sub" style="margin-top:10px">Tray icon: <code>python tray_runner.py</code> (Windows tray; <code>--headless</code> for CLI). Hidden start: double-click <code>start_dashboard_hidden.vbs</code>. Build/check: <code>build.ps1</code>. All project processes run BelowNormal.</p>
</div></section>
</main><script>
const esc=s=>String(s??'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
let allPrompts=[], allFiles=[], statusData=null;
async function loadStatus(){ try{ const r=await fetch('/api/status'); statusData=await r.json();
 document.getElementById('ver').textContent='v'+statusData.version;
 document.getElementById('livepill').textContent='live - pid '+statusData.pid+' - port '+statusData.port;
 const c=statusData.corpus||{}, d=statusData.db||{}, by=d.prompts_by_season||{};
 document.getElementById('metrics').innerHTML=
  [['Corpus',(c.bytes? (c.bytes/1048576).toFixed(2)+' MB':'?'), (c.sessions||'?')+' sessions - '+(c.lines||'?')+' lines - sha '+ (c.sha12||'')],
   ['Corpus parity', c.twin_identical?'100%':'CHECK', 'CONVERSATION_SCRIPT_COMPLETE.txt vs sitcom script.txt byte-identical: '+c.twin_identical],
   ['Kling prompts', (d.tables?d.tables.kling_prompts:'?'), 'S1 '+(by['1']||0)+' - S2 '+(by['2']||0)+' in catalog.db'],
   ['Dialogue cues','Bob '+(c.bob_cues||'?'),'Lum '+(c.lum_cues||'?')+' cues in corpus'],
   ['Transcripts', statusData.transcribeme_txt, '.txt files in transcribeme/ feeding the corpus'],
   ['Uptime', statusData.uptime_s+'s','Python '+statusData.python+' - '+statusData.platform]
  ].map(x=>'<div class="metric"><div class="sub">'+esc(x[0])+'</div><div class="v">'+esc(x[1])+'</div><div class="sub">'+esc(x[2])+'</div></div>').join('');
 document.getElementById('identity').textContent='Session identity: '+statusData.identity;
 document.getElementById('sysinfo').innerHTML='Version <b>'+esc(statusData.version)+'</b> - PID '+statusData.pid+' - port '+statusData.port+' - Python '+esc(statusData.python)+'<br>Repo: '+esc(statusData.repo)+'<br>DB tables: '+esc(JSON.stringify(d.tables||{}));
 const sel=document.getElementById('doc-select'); const cur=sel.value;
 sel.innerHTML=Object.entries(statusData.docs).map(([k,v])=>'<option value="'+k+'">'+esc(v.group)+' - '+esc(v.label)+(v.exists?'':' (missing)')+'</option>').join('');
 if(cur) sel.value=cur;
 }catch(e){ document.getElementById('livepill').textContent='status failed: '+e; } }
let currentDocRaw='';
async function loadDoc(){ const k=document.getElementById('doc-select').value; if(!k) return;
 const r=await fetch('/api/doc?name='+encodeURIComponent(k)); currentDocRaw=await r.text(); renderDoc();
 const d=(statusData&&statusData.docs[k])||{}; document.getElementById('doc-meta').textContent=(d.file||'')+' - '+(d.bytes||0)+' bytes - '+(d.desc||''); }
function filteredDoc(){ const sp=document.getElementById('doc-speaker').value; if(sp==='all') return currentDocRaw;
 return currentDocRaw.split('\n').filter(l=>/^#|^\s*$/.test(l)||l.includes(sp.toUpperCase()+':')||l.includes(sp+':')||l.includes('**'+sp.toUpperCase())).join('\n'); }
function mdInline(s){ return esc(s).replace(/\*\*([^*]+)\*\*/g,'<b>$1</b>').replace(/(^|[^*])\*([^*]+)\*/g,'$1<i>$2</i>').replace(/`([^`]+)`/g,'<code>$1</code>'); }
function renderMarkdown(t){ const out=[]; let inCode=false, list=false;
 for(const line of t.split('\n')){ if(line.trim().startsWith('```')){ out.push(inCode?'</pre>':'<pre>'); inCode=!inCode; continue; }
  if(inCode){ out.push(esc(line)); continue; }
  const h=line.match(/^(#{1,3})\s+(.*)/); if(h){ if(list){out.push('</ul>');list=false;} out.push('<h'+h[1].length+'>'+mdInline(h[2])+'</h'+h[1].length+'>'); continue; }
  if(/^\s*---+\s*$/.test(line)){ if(list){out.push('</ul>');list=false;} out.push('<hr>'); continue; }
  if(/^\|.*\|$/.test(line)){ if(list){out.push('</ul>');list=false;} if(!/^\|[\s:|-]+\|$/.test(line)) out.push('<p>'+mdInline(line.replace(/^\||\|$/g,'').replace(/\|/g,' | '))+'</p>'); continue; }
  const li=line.match(/^\s*[-*]\s+(.*)/); if(li){ if(!list){out.push('<ul>');list=true;} out.push('<li>'+mdInline(li[1])+'</li>'); continue; }
  if(list){ out.push('</ul>'); list=false; }
  if(line.trim()) out.push('<p>'+mdInline(line)+'</p>'); }
 if(list) out.push('</ul>'); if(inCode) out.push('</pre>'); return out.join('\n'); }
function renderDoc(){ const v=document.getElementById('doc-viewer'); if(!currentDocRaw){ v.textContent='Select a document and press Load.'; return; }
 const t=filteredDoc();
 if(document.getElementById('doc-mode').value==='plain'){ v.innerHTML='<pre style="white-space:pre-wrap">'+esc(t)+'</pre>'; }
 else { v.innerHTML=renderMarkdown(t); } }
async function loadPrompts(){ const src=document.getElementById('prompt-source').value; const r=await fetch('/api/prompts?source='+encodeURIComponent(src)); allPrompts=await r.json(); filterPrompts(); }
function filterPrompts(){ const s=document.getElementById('season-filter').value, q=document.getElementById('prompt-search').value.toLowerCase();
 const f=allPrompts.filter(p=>(s==='all'||String(p.season)===s)&&(!q||(p.prompt_title+' '+p.prompt_text+' '+p.episode_title).toLowerCase().includes(q)));
 document.getElementById('prompt-count').textContent=f.length+' / '+allPrompts.length+' prompts';
 document.getElementById('prompts-container').innerHTML=f.map((p,i)=>'<div class="prompt-card"><div><div style="color:var(--acc);font-weight:700;font-size:.85rem">'+(p.source_file? esc(p.episode_title)+' - '+esc(p.episode_num) : 'S'+esc(p.season)+' E'+esc(p.episode_num)+' - '+esc(p.episode_title)+' - Prompt '+esc(p.prompt_num))+'</div><div style="font-weight:700;color:var(--head)">'+esc(p.prompt_title)+'</div><div class="prompt-body">'+esc(p.prompt_text)+'</div></div><button class="btn" onclick="copyOne('+allPrompts.indexOf(p)+')" title="Copy the full raw prompt block">Copy prompt</button></div>').join('')||'<p class="sub">No prompts match.</p>'; }
function copyOne(i){ navigator.clipboard.writeText(allPrompts[i].raw_block); }
function copyAllPrompts(){ const s=document.getElementById('season-filter').value, q=document.getElementById('prompt-search').value.toLowerCase();
 const f=allPrompts.filter(p=>(s==='all'||String(p.season)===s)&&(!q||(p.prompt_title+' '+p.prompt_text+' '+p.episode_title).toLowerCase().includes(q)));
 navigator.clipboard.writeText(f.map(p=>p.raw_block).join('\n\n')); alert('Copied '+f.length+' prompts'); }
let searchOffset=0, searchTotal=0;
function pageSearch(dir){ searchOffset=Math.max(0, searchOffset+dir*50); searchCorpus(true); }
async function searchCorpus(keepOffset){ const q=document.getElementById('corpus-query').value.trim(); if(!q) return;
 if(!keepOffset) searchOffset=0;
 document.getElementById('search-status').textContent='Searching...';
 const r=await fetch('/api/search?q='+encodeURIComponent(q)+'&offset='+searchOffset); const d=await r.json();
 searchTotal=d.total||0; searchOffset=d.offset||0;
 document.getElementById('search-status').textContent='Found '+searchTotal+' hit(s) for "'+q+'" - showing '+(searchTotal? (searchOffset+1)+'-'+(searchOffset+d.matches.length):'0');
 document.getElementById('search-prev').disabled=searchOffset<=0;
 document.getElementById('search-next').disabled=!(searchTotal>searchOffset+d.matches.length);
 document.getElementById('search-results').innerHTML=d.matches.map(m=>{ let t=esc(m.text); t=t.replace(/^Bob:/,'<span class="sp-Bob">Bob:</span>').replace(/^Lum:/,'<span class="sp-Lum">Lum:</span>'); return '<div class="result-item"><span class="sub">Line '+m.line_num+'</span><p>'+t+'</p></div>'; }).join('')||'<p class="sub">No hits.</p>'; }
async function loadFiles(){ const r=await fetch('/api/files'); allFiles=await r.json(); renderFiles();
 document.getElementById('script-list').innerHTML=allFiles.filter(f=>f.kind==='.py').map(f=>'<div><b>'+esc(f.name)+'</b> - '+esc(f.desc||'')+'</div>').join(''); }
function renderFiles(){ const q=(document.getElementById('file-filter').value||'').toLowerCase();
 const f=allFiles.filter(x=>!q||(x.name+' '+(x.desc||'')).toLowerCase().includes(q));
 document.getElementById('files-body').innerHTML=f.map(x=>'<tr><td>'+esc(x.name)+'</td><td>'+x.bytes.toLocaleString()+'</td><td>'+esc(x.desc||x.kind)+'</td></tr>').join(''); }
async function runAction(ep,label){ const log=document.getElementById('action-log'); log.textContent='Running '+label+'...';
 try{ const r=await fetch(ep,{method:'POST'}); const d=await r.json(); log.textContent=label+' - '+(d.ok?'OK':'FAILED')+' (exit '+d.returncode+')\n'+(d.output||d.message||''); if(ep.includes('extract')) loadPrompts(); loadStatus(); }
 catch(e){ log.textContent=label+' failed: '+e; } }
async function loadLog(){ const r=await fetch('/api/log'); document.getElementById('log-viewer').textContent=await r.text(); }
async function quitServer(){ if(confirm('Quit the Bob & Lum dashboard server? The tray/launchers can restart it.')){ await fetch('/api/quit',{method:'POST'}); document.body.innerHTML='<div style="padding:40px;text-align:center"><h2>Dashboard stopped. Restart via tray_runner.py or start_dashboard_hidden.vbs</h2></div>'; } }
document.addEventListener('DOMContentLoaded',()=>{ loadStatus(); loadPrompts(); loadFiles(); });
</script></body></html>"""

class Handler(http.server.BaseHTTPRequestHandler):
    port = 8765
    def log_message(self, fmt, *args):
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f: f.write("%s - %s\n" % (self.address_string(), fmt % args))
        except Exception: pass
    def send_json(self, obj, code=200):
        body = json.dumps(obj).encode("utf-8"); self.send_response(code); self.send_header("Content-Type", "application/json; charset=utf-8"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def send_text(self, text, ctype="text/plain; charset=utf-8", code=200):
        body = text.encode("utf-8", errors="replace"); self.send_response(code); self.send_header("Content-Type", ctype); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path); path = parsed.path; q = urllib.parse.parse_qs(parsed.query)
        if path in ("/", "/index.html"): return self.send_text(HTML_TEMPLATE, "text/html; charset=utf-8")
        if path == "/api/status": return self.send_json(status_payload(self.port))
        if path == "/api/files": return self.send_json(list_files())
        if path == "/api/log":
            if LOG_PATH.exists(): return self.send_text("\n".join(LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()[-120:]))
            return self.send_text("(no dashboard.log yet - server stdout is the log when launched hidden)")
        if path == "/api/prompts":
            data = []
            if DB_PATH.exists():
                conn = sqlite3.connect(DB_PATH); conn.row_factory = sqlite3.Row
                try:
                    if q.get("source", ["canonical"])[0] == "historical":
                        data = [dict(r) for r in conn.execute("SELECT 0 AS season, shot_id AS episode_num, source_file AS episode_title, id AS prompt_num, title AS prompt_title, prompt_text, raw_block, source_file FROM kling_prompts_historical ORDER BY source_file, id").fetchall()]
                    else:
                        data = [dict(r) for r in conn.execute("SELECT season,episode_num,episode_title,prompt_num,prompt_title,prompt_text,raw_block FROM kling_prompts ORDER BY season,prompt_num").fetchall()]
                except Exception: data = []
                conn.close()
            return self.send_json(data)
        if path == "/api/screenplay":
            key = "s1" if q.get("season", ["1"])[0] == "1" else "s2"; return self._doc(key)
        if path == "/api/doc": return self._doc(q.get("name", ["s1"])[0])
        if path == "/api/search":
            query = q.get("q", [""])[0].strip().lower()
            try: offset = max(0, int(q.get("offset", ["0"])[0]))
            except Exception: offset = 0
            all_matches = []
            if query and CORPUS_PATH.exists():
                with open(CORPUS_PATH, encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        if query in line.lower(): all_matches.append({"line_num": i, "text": line.strip()})
            page = all_matches[offset:offset+50]
            return self.send_json({"matches": page, "total": len(all_matches), "offset": offset, "truncated": len(all_matches) > offset + 50})
        return self.send_text("not found", code=404)
    def _doc(self, key):
        if key not in DOCS: return self.send_text("unknown doc", code=404)
        p = REPO_ROOT / DOCS[key][0]
        if not p.exists(): return self.send_text("missing file: " + DOCS[key][0], code=404)
        return self.send_text(p.read_text(encoding="utf-8", errors="replace"))
    def do_POST(self):
        routes = {"/api/check": ["transcribeme/manage_corpus.py", "--check"], "/api/stats": ["transcribeme/manage_corpus.py", "--stats"],
                  "/api/rebuild-html": ["transcribeme/regen_wordpress_html.py"], "/api/extract-prompts": ["transcribeme/extract_kling_prompts.py"]}
        if self.path == "/api/quit":
            self.send_json({"message": "shutting down"})
            threading.Thread(target=lambda: (time.sleep(0.5), os._exit(0)), daemon=True).start(); return
        if self.path in routes: return self.send_json(run_action(routes[self.path]))
        return self.send_text("not found", code=404)

def run_server(port, host):
    lower_self_priority(); Handler.port = port; socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.TCPServer((host, port), Handler)
    except OSError as e:
        print(f"ERROR: cannot bind {host}:{port} ({e}). Is another dashboard/service using it? Try --port 8766.", flush=True); raise SystemExit(2)
    with httpd:
        print(f"Bob & Lum Dashboard v{read_version()} listening on http://{host}:{port}/ (pid {os.getpid()}, BelowNormal)", flush=True)
        try: httpd.serve_forever()
        except KeyboardInterrupt: print("\nShutting down.")

def main():
    ap = argparse.ArgumentParser(description="Bob & Lum Sitcom Unified Dashboard")
    ap.add_argument("--port", type=int, default=8765, help="Port (default 8765; 8080 is used by another service on this laptop)")
    ap.add_argument("--host", type=str, default="127.0.0.1", help="Bind address (default 127.0.0.1, local only)")
    a = ap.parse_args(); lower_self_priority(); run_server(a.port, a.host)
if __name__ == "__main__": main()
