# TODO: Immediate Tasks & Granular Fixes

## Script Maintenance & Canon Fixes
- [ ] Scan and eliminate any legacy references attributing Pop-Tarts to Bob in older auxiliary files.
- [ ] Review speaker naming in raw transcripts: normalize legacy "Rob" mentions in scripts to canonical "Bob".
- [ ] Fix stale season footer counts in `sitcom_rewrite_s2.md`.
- [ ] Ensure `CONVERSATION_SCRIPT_COMPLETE.txt` and `sitcom script.txt` remain strictly byte-identical.

## Pipeline & Python Tooling
- [x] Fix path resolution in `transcribeme/deep_clean_rebuild.py` to use repository-relative paths instead of Windows `C:\Users\hyper\Downloads\`.
- [x] Update `transcribeme/regen_wordpress_html.py` to run out of repo root with CLI flags or default local paths.
- [x] Add unified CLI script runner (`transcribeme/manage_corpus.py`) to run integrity checks, header normalizations, and HTML regenerations cleanly.
- [x] Build automated Kling AI scene prompt indexer (`transcribeme/extract_kling_prompts.py`) into SQLite `catalog.db`.
- [x] Implement local unified dashboard server (`dashboard.py`) with screenplay viewer, prompt laboratory, corpus search, and graceful shutdown controls.

## Documentation & Version Governance
- [x] Create core governance suite: `VERSION.md`, `ROADMAP.md`, `VISION.md`, `MEMORY.md`, `DEPLOY.md`, `IDEAS.md`, `CHANGELOG.md`.
- [x] Configure `.gitignore` to prevent Python compilation cache leakage (`__pycache__/`, `*.pyc`).
- [ ] Document all script utilities in `DEPLOY.md`.
