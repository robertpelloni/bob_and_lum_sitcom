# DEPLOY: Environment Setup & Pipeline Usage

## Overview
This repository contains the scripts, conversation corpus, and video-generation prompts for the *Bob & Lum Sitcom*. The pipeline processes raw voice transcripts, assigns speaker tags, normalizes historical canon, updates the master script corpus, and generates exportable HTML formats.

## Prerequisites
- **Python 3.10+** (Python 3.12 recommended)
- Standard library modules (`sqlite3`, `pathlib`, `re`, `html`, `hashlib`, `argparse`)
- Modern web browser for viewing `CONVERSATION_SCRIPT_COMPLETE.wordpress.html`

## Directory Structure
```
.
├── CONVERSATION_SCRIPT_COMPLETE.txt          # Master 247-session transcript corpus
├── CONVERSATION_SCRIPT_COMPLETE.wordpress.html# Rendered HTML viewer
├── dashboard.py                              # Unified local SPA web dashboard server
├── tray_runner.py                            # Desktop system tray controller & server manager
├── sitcom script.txt                         # Byte-identical copy of master corpus
├── sitcom_final_s1.md                        # Season 1 Screenplay (12 episodes)
├── sitcom_final_s2.md                        # Season 2 Screenplay (8+6 episodes)
├── transcribeme/                             # Raw transcripts and ingestion tooling
│   ├── deep_clean_rebuild.py                 # Core text cleaning & speaker attribution
│   ├── extract_kling_prompts.py              # Ingests Kling scene prompts into SQLite
│   ├── manage_corpus.py                      # Unified CLI runner for corpus tasks
│   ├── regen_wordpress_html.py               # Re-renders HTML from corpus
│   └── catalog.db                            # SQLite metadata catalog
└── VERSION.md                                # Global version identifier
```

## Running Dashboard, System Tray & Utilities

### 1. Desktop System Tray Controller
Run the background tray icon manager:
```bash
python tray_runner.py [--port 8765] [--headless]
```
Features:
- Right-click menu to Open Sitcom Dashboard in browser
- Start, stop, or restart the dashboard server on demand
- Run instant corpus integrity audit
- Quit all background services cleanly
- Automatic fallback to CLI daemon mode on headless/non-GUI environments

### 2. Unified Local Dashboard Server (Standalone) — USER MANUAL
Start it (exact command):
```powershell
python dashboard.py
```
Then **open http://127.0.0.1:8765 in your browser**. (Default port is 8765 since 2026-11-13: port 8080 on this laptop is another service, `node server/ai_proxy.js` — never kill it for this project. Override with `--port N` if 8765 is taken.)
One page, high-value first, no subpages:
- **Overview** — live metrics from `/api/status` (version from `VERSION.md`, corpus bytes/lines/sessions/sha + byte-parity, Kling counts, Bob/Lum cues, uptime).
- **Screenplays & Docs** — one viewer for all 19 files: final S1/S2, rewrite, full screenplay/series, DARK, episode 1, all Kling source files, and VISION/MEMORY/ROADMAP/TODO/IDEAS/DEPLOY/CHANGELOG/HANDOFF/README.
- **Kling Prompts** — 102 DB prompts, season/keyword filter, copy one or copy-all-filtered.
- **Corpus Search** — substring search over 258,350 lines, speaker highlighting, first-50 note.
- **Library / Files** — every root + `transcribeme/*.py` file with size and role.
- **Pipeline & Scripts** — Check/Stats/Re-index/Rebuild jobs with real output + exit code (never fake success).
- **Canon** — immutable rules summary (full text in MEMORY via the viewer).
- **System** — tray/log/quit controls, `dashboard.log` viewer.
Every ambiguous element has a `?`/tooltip. Quit stops only this dashboard; restart via tray or launcher below.

### 3. Kling AI Prompt Catalog Extraction
Re-index scene prompts from screenplay files into SQLite:
```bash
python3 transcribeme/extract_kling_prompts.py
```

### 4. Corpus Management CLI
Use the unified CLI runner in `transcribeme/`:
```bash
python3 transcribeme/manage_corpus.py --check
```
This performs integrity checks on corpus size, header formats, and file synchronization between `CONVERSATION_SCRIPT_COMPLETE.txt` and `sitcom script.txt`.

### 5. Regenerating HTML Output
To rebuild `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` from the canonical text corpus:
```bash
python3 transcribeme/regen_wordpress_html.py
```
Or via the corpus manager:
```bash
python3 transcribeme/manage_corpus.py --build-html
```

### 6. Syntax & Script Compilation Check
Verify all scripts in the repository:
```bash
for f in dashboard.py tray_runner.py transcribeme/*.py; do python3 -m py_compile "$f"; done
```

### 6. Process Priority (BelowNormal rule, 2026-11-08)
Heavyweight jobs must not hang the desktop. `dashboard.py` and `manage_corpus.py` lower themselves automatically. For anything else (ffmpeg, batch exports, rebuilds), launch then lower:
```powershell
$p = Start-Process python -ArgumentList 'transcribeme/manage_corpus.py --check' -PassThru; $p.PriorityClass = 'BelowNormal'
(Get-Process -Name python,ffmpeg -ErrorAction SilentlyContinue).PriorityClass = 'BelowNormal'
```


### 7. Headless / No-Popup Rule (2026-11-08, port updated 2026-11-13)
- Never auto-open a browser or console popup. Logs go to `dashboard.log` (gitignored).
- Launch hidden: double-click `start_dashboard_hidden.vbs` or run `start_dashboard_hidden.ps1` (pythonw, Hidden, BelowNormal, identity-checked single-instance on port **8765**, binds 127.0.0.1; exits 2 if 8765 is held by something else).
- Build/verify everything: `.\build.ps1` (compile + check + stats + re-index + HTML rebuild; `-SkipHtml` for a fast pass).
- Stop: dashboard **System → Quit**, tray **Quit All**, or `Invoke-RestMethod -Method Post http://127.0.0.1:8765/api/quit`. Nothing in this repo may add itself to Startup without explicit approval.
- Tray icon (v1.5.0 fix): `python tray_runner.py` shows a Windows tray icon (Open/Start/Stop/Restart/Check/View log/Quit All). Pre-1.5.0 it silently fell back to CLI on Windows due to a `$DISPLAY` gate.
- Troubleshooting: `8765 in use` → pick `--port 8766` everywhere; blank prompts → run Re-index in Pipeline; stale HTML → Rebuild WordPress HTML; check `dashboard.log` in System section.

