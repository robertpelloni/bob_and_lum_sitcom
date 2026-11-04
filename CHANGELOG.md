# CHANGELOG: Bob & Lum Sitcom

All notable changes to this project are documented in this file.
Version format adheres to Semantic Versioning as defined in `VERSION.md`.

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
