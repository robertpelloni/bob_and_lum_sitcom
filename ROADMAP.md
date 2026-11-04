# ROADMAP: Bob & Lum Sitcom Milestones

## Phase 1: Script Canon & Corpus Unification (Current)
- [x] Standardize Season 1 (12 episodes) and Season 2 (8+6 episodes) scripts.
- [x] Consolidate master conversation script (247 sessions, 5.9MB corpus).
- [x] Establish strict character rules (no Pop-Tarts, distinct death narratives, USB vs burner phones).
- [ ] Align older secondary drafts (`sitcom_bob_and_lum_DARK_KLING.md`, `sitcom_bob_and_lum_episode1*.md`, `full_series_kling.md`) to the unified 12-episode canonical standard.
- [ ] Port hardcoded local filesystem paths in pipeline scripts to portable repository paths.

## Phase 2: Kling AI Prompt & Video Asset Orchestration
- [ ] Compile all scene prompts from `sitcom_final_s1.md` and `sitcom_final_s2.md` into structured JSON / SQLite tables.
- [ ] Build automated prompt generation and validation pipeline against Kling AI guidelines (aspect ratio, camera movement, motion vector parameters).
- [ ] Implement batch export tooling for video generation APIs and webhooks.

## Phase 3: Unified Sitcom Web Dashboard & Production Interface
- [ ] Design and implement a consolidated Single-Page Application (SPA) dashboard:
  - Episode & Screenplay Reader with syntax-highlighted character dialogue.
  - Interactive Kling Scene Prompt inspector with copy-to-clipboard and preview features.
  - Raw Transcript Explorer with full-text search across all 247 corpus sessions.
  - Media & Asset Catalog viewer linking generated video/audio files to screenplay scenes.
- [ ] Integrate local system tray controller to launch and manage dashboard services and API watchers.

## Phase 4: Audio Synthesis & Multimodal Rendering
- [ ] Extract character voice samples from raw media transcripts (`transcribeme/*.mp4` / `IMG_*.MOV`).
- [ ] Train/configure ElevenLabs or open-source voice models for Bob and Lum's distinctive Detroit cadence and vocal rhythm.
- [ ] Synchronize synthetic voice tracks with Kling generated video shots.
