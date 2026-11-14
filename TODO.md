# TODO: Immediate Tasks & Granular Fixes

## Script Maintenance & Canon Fixes
- [x] Scan legacy Pop-Tarts references (verified 2026-11-08: all hits are `Never Pop-Tarts` canon lines, zero Bob-eats violations).
- [x] Review speaker naming Rob->Bob (verified 2026-11-08: zero `\bRob\b` hits in *.md outside MEMORY/TODO canon notes).
- [x] Fix stale season footer counts (fixed 2026-11-08: `sitcom_final_s1.md` 60->51 prompts to match 51 SCENE PROMPTs; verified `sitcom_final_s2.md` 14 total 8+6 and `sitcom_rewrite_s2.md` 8+6=14 correct).
- [x] Ensure byte-identical corpus (verified 2026-11-08: both 5905406 bytes, Compare-Object clean).

## Pipeline & Python Tooling
- [x] Fix path resolution in `transcribeme/deep_clean_rebuild.py` to use repository-relative paths instead of Windows `C:\Users\hyper\Downloads\`.
- [x] Update `transcribeme/regen_wordpress_html.py` to run out of repo root with CLI flags or default local paths.
- [x] Add unified CLI script runner (`transcribeme/manage_corpus.py`) to run integrity checks, header normalizations, and HTML regenerations cleanly.
- [x] Build automated Kling AI scene prompt indexer (`transcribeme/extract_kling_prompts.py`) into SQLite `catalog.db`.
- [x] Implement local unified dashboard server (`dashboard.py`) with screenplay viewer, prompt laboratory, corpus search, and graceful shutdown controls.
- [x] Implement desktop system tray runner (`tray_runner.py`) using `pystray` and `PIL` with server start/stop/restart/quit and browser launcher.

## Dashboard v1.5.0 follow-ups (2026-11-13)
- [x] Index non-DB Kling files (done 2026-11-13 v1.6.0: 177 historical prompts in `kling_prompts_historical`, dashboard Canonical/Historical toggle).
- [ ] Decide disposition of legacy `catalog.db` tables (`published_mcp_servers` 82 rows, `links_backlog`, `published_skills`) — HyperNexus residue, not sitcom data; do not delete without owner OK.
- [x] Markdown-render screenplays in viewer (done v1.6.0: rendered/plain + Bob/Lum filter).
- [x] Corpus search pagination + session-name context per hit (done v1.6.0/v1.7.0).
- [ ] Tray: visually confirm icon on the desktop (process verified BelowNormal; icon pixels not sighted by agent). Live state done v1.7.0 (`Dashboard Status` menu + `--status`).
- [ ] Strengthen the 17 weak canonical Kling prompts (no camera/lighting cue, per `validate_prompts.py`) — creative edit, needs owner review of wording.

## Documentation & Version Governance
- [x] Create core governance suite: `VERSION.md`, `ROADMAP.md`, `VISION.md`, `MEMORY.md`, `DEPLOY.md`, `IDEAS.md`, `CHANGELOG.md`.
- [x] Configure `.gitignore` to prevent Python compilation cache leakage (`__pycache__/`, `*.pyc`).
- [x] Document all script utilities and dashboard runner in `DEPLOY.md`.
