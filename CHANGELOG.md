# CHANGELOG: Bob & Lum Sitcom

All notable changes to this project are documented in this file.
Version format adheres to Semantic Versioning as defined in `VERSION.md`.

## [1.7.0] - 2026-11-13
### Added
- Corpus search hits now carry their session header (`[N] ...`) in API + UI.
- `transcribeme/validate_prompts.py` Kling validation report (dashboard Pipeline button too): canonical 102 → 85 with camera/lighting cue, 17 weak; historical 177 → 157 with cue, 20 weak. Report-only, non-gating.
- Tray: `Dashboard Status (check)` menu item (notification + tooltip state) and `tray_runner.py --status` CLI.

## [1.6.0] - 2026-11-13
### Added
- Historical Kling indexing: `extract_kling_prompts.py` now parses DARK (table format, 114), episode-1 (14) and full-series (49) into `kling_prompts_historical` (177 total); dashboard prompt explorer gains a Canonical/Historical source toggle.
- `transcribeme/canon_lint.py` canon gate (Pop-Tarts negation, Rob/Lung labels, Noah conflation) wired into `build.ps1`.
- Maintained tests `tests/test_dashboard.py` (5 stdlib unittest cases: search pagination, historical source, traversal guard, canon lint, all three historical formats) run by `build.ps1`.
- Screenplay viewer renders markdown (headings/bold/lists/code/tables) with Plain toggle and Bob/Lum speaker filter; corpus search paginates (total + Previous/Next 50).

## [1.5.0] - 2026-11-13
### Added
- Dashboard consolidated into one high-value-ordered page (Overview → Screenplays & Docs → Kling Prompts → Corpus Search → Library/Files → Pipeline & Scripts → Canon → System) with 36 tooltip/help markers, live `/api/status` (version from `VERSION.md`, corpus sha/parity, DB counts, uptime), one viewer for all 19 screenplays/Kling sources/docs (`/api/doc`, allowlisted), `/api/files` inventory (47 files with roles), real job output for check/stats/re-index/rebuild (exit code + stdout, never faked success), speaker highlighting in corpus search, and `/api/log`.
- `build.ps1`: compile-all + corpus check/stats + prompt re-index + HTML rebuild, non-zero on failure.

### Changed
- Default dashboard port 8080 → **8765** (`127.0.0.1`): 8080 on this laptop is owned by another local service (`node server/ai_proxy.js`, left untouched). Launchers/tray/docs updated; identity-checked single-instance guard.
- Archived root `.tmp_*.txt` CDP scratch files to `archive/tmp_20261113/` (nondestructive move, restorable).

### Fixed
- Tray never appeared on Windows: gate required `$DISPLAY` (Unix-only). Now tray on win32/Darwin/`$DISPLAY`, dashboard child hidden + BelowNormal + logged, external dashboard detected via `/api/status`.
- Dashboard XSS/escaping in prompt cards, broken dead `showTab()` code, hardcoded version/metrics, silent subprocess failures in pipeline actions.
- `manage_corpus.py --stats` byte count undercounted (CRLF translation); now uses file size (6,163,756).

## [1.4.0] - 2026-11-04
### Added
- Created `tray_runner.py`: Cross-platform desktop system tray controller with options to launch the dashboard in a browser, start/stop/restart dashboard processes, run corpus integrity audits, and quit all running services.

## [1.3.0] - 2026-11-04
### Added
- Created `dashboard.py`: Consolidated, single-page application local HTTP dashboard server providing unified access to Screenplay Reader (S1 & S2), Kling AI Scene Prompts explorer with instant clipboard copy, full-text transcript corpus search, and service controls (quit/rebuild).
- Created `transcribeme/extract_kling_prompts.py`: Automated extractor indexing 102 Kling AI video scene prompts into SQLite catalog (`catalog.db:kling_prompts`).

## [1.2.0] - 2026-11-04
### Added
- Created foundational project governance documentation:
  - `VERSION.md`: Single source of truth for repository build version.
  - `VISION.md`: Exhaustive artistic philosophy, narrative themes, and production roadmap.
  - `MEMORY.md`: Immutable character canon rules, technical lore splits, and architectural layout.
  - `ROADMAP.md`: Multi-phase milestone breakdown from script canon to multimodal rendering.
  - `TODO.md`: Granular short-term bug fixes, maintenance tasks, and tooling enhancements.
  - `DEPLOY.md`: Deployment guide, pipeline overview, and CLI execution instructions.
  - `IDEAS.md`: Blue-sky expansion proposals including unified dashboard SPA and system tray app.
  - `CHANGELOG.md`: Repository modification record.
- Added Python bytecode ignores (`__pycache__/`, `*.pyc`) in `.gitignore`.
- Modernized utility scripts in `transcribeme/` (`regen_wordpress_html.py`, `deep_clean_rebuild.py`) to support repository-relative path resolution.
- Added `transcribeme/manage_corpus.py` CLI runner for corpus validation, byte-integrity checks, and HTML rendering.

### Fixed
- Fixed hardcoded Windows path assumptions (`C:\Users\hyper\Downloads\...`) in core pipeline scripts.
