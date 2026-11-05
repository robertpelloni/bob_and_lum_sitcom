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
├── sitcom script.txt                         # Byte-identical copy of master corpus
├── sitcom_final_s1.md                        # Season 1 Screenplay (12 episodes)
├── sitcom_final_s2.md                        # Season 2 Screenplay (8+6 episodes)
├── transcribeme/                             # Raw transcripts and ingestion tooling
│   ├── deep_clean_rebuild.py                 # Core text cleaning & speaker attribution
│   ├── regen_wordpress_html.py               # Re-renders HTML from corpus
│   ├── manage_corpus.py                      # Unified CLI runner for corpus tasks
│   └── catalog.db                            # SQLite metadata catalog
└── VERSION.md                                # Global version identifier
```

## Running Corpus Utilities

### 1. Corpus Management CLI
Use the unified CLI runner in `transcribeme/`:
```bash
python3 transcribeme/manage_corpus.py --check
```
This performs integrity checks on corpus size, header formats, and file synchronization between `CONVERSATION_SCRIPT_COMPLETE.txt` and `sitcom script.txt`.

### 2. Regenerating HTML Output
To rebuild `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` from the canonical text corpus:
```bash
python3 transcribeme/regen_wordpress_html.py
```
Or via the corpus manager:
```bash
python3 transcribeme/manage_corpus.py --build-html
```

### 3. Syntax & Script Compilation Check
Verify all scripts in the repository:
```bash
for f in transcribeme/*.py; do python3 -m py_compile "$f"; done
```
