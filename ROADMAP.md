# ROADMAP: Bob & Lum Sitcom Milestones

## Phase 1: Script Canon & Corpus Unification (Current)
- [x] Standardize Season 1 (12 episodes) and Season 2 (8+6 episodes) scripts.
- [x] Consolidate master conversation script (247 sessions, 5.9MB corpus).
- [x] Establish strict character rules (no Pop-Tarts, distinct death narratives, USB vs burner phones).
- [ ] Align older secondary drafts (`sitcom_bob_and_lum_DARK_KLING.md`, `sitcom_bob_and_lum_episode1*.md`, `full_series_kling.md`) to the unified 12-episode canonical standard.
- [ ] Port hardcoded local filesystem paths in pipeline scripts to portable repository paths.

## Phase 2: Kling AI Prompt & Video Asset Orchestration
- [x] Compile all scene prompts from `sitcom_final_s1.md` and `sitcom_final_s2.md` into structured JSON / SQLite tables (`transcribeme/catalog.db:kling_prompts`).
- [ ] Build automated prompt generation and validation pipeline against Kling AI guidelines (aspect ratio, camera movement, motion vector parameters).
- [ ] Implement batch export tooling for video generation APIs and webhooks.

## Phase 3: Unified Sitcom Web Dashboard & Production Interface
- [x] Design and implement a consolidated Single-Page Application (SPA) dashboard (`dashboard.py`):
  - Episode & Screenplay Reader for Season 1 and Season 2.
  - Interactive Kling Scene Prompt inspector with copy-to-clipboard and keyword filtering across 102 prompts.
  - Raw Transcript Explorer with full-text search across all 247 corpus sessions.
  - Server lifecycle control (graceful `/api/quit` endpoint).
- [x] Integrate local desktop system tray controller (`tray_runner.py`) using `pystray` and `PIL` with actions to launch dashboard, start/stop/restart servers, check corpus integrity, and quit all services.
- [x] v1.5.0 (2026-11-13): one consolidated page ordered by value, live `/api/status`, all 19 docs/screenplays in one viewer, file+script library, honest pipeline job output, tray Windows fix, port 8765, `build.ps1`.
- [x] Index non-final Kling files into `catalog.db` (v1.6.0: `kling_prompts_historical`, 177 prompts, dashboard source toggle) + canon-lint gate + maintained tests.
- [x] Render screenplay markdown properly with Bob/Lum filters (v1.6.0).

## Phase 4: Audio Synthesis & Multimodal Rendering
- [ ] Extract character voice samples from raw media transcripts (`transcribeme/*.mp4` / `IMG_*.MOV`).
- [ ] Train/configure ElevenLabs or open-source voice models for Bob and Lum's distinctive Detroit cadence and vocal rhythm.
- [ ] Synchronize synthetic voice tracks with Kling generated video shots.
