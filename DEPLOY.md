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
python3 tray_runner.py [--port 8080] [--headless]
```
Features:
- Right-click menu to Open Sitcom Dashboard in browser
- Start, stop, or restart the dashboard server on demand
- Run instant corpus integrity audit
- Quit all background services cleanly
- Automatic fallback to CLI daemon mode on headless/non-GUI environments

### 2. Unified Local Dashboard Server (Standalone)
Launch the consolidated single-page application dashboard directly:
```bash
python3 dashboard.py --port 8080
```
Open `http://localhost:8080` in your web browser. Features include:
- Screenplay Reader for Season 1 and Season 2
- Kling AI Scene Prompts explorer with 1-click clipboard copy
- Real-time search across 258,350 lines in the transcript corpus
- One-click pipeline actions and graceful server termination via `/api/quit`

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


### 7. Headless / No-Popup Rule (2026-11-08)
- Never auto-open a browser or console popup. `dashboard.py` has no `webbrowser.open` (verified). Logs go to `dashboard.log`.
- Launch hidden: double-click `start_dashboard_hidden.vbs` or run `start_dashboard_hidden.ps1` (pythonw, Hidden, BelowNormal, single-instance guard on port 8080, binds 127.0.0.1).
- Stop: open `http://127.0.0.1:8080/api/quit` or stop the pythonw process. Nothing in this repo may add itself to Startup without explicit approval.

