# Bob & Lum Sitcom

> **DASHBOARD FROZEN (2026-11-19).** The dashboard/tray tooling is feature-complete and frozen — no further dashboard versions. `sitcom_final_s1.md` and `sitcom_final_s2.md` are the canonical scripts; the DARK / full-series / episode-1 files are historical source material, not competing finals. The next milestone is production (Phase 4), not more tooling.

A dark-comedy sitcom derived from hundreds of hours of raw transcribed real-life conversations between Robert Pelloni (Bob) and Lumbros Kourlos (Lum): two lifelong friends in a Detroit apartment, among cold pizza boxes and glowing computer monitors, talking with total candor about addiction, grief, county jail, dead friends, and existential dread — while laughing uncontrollably. The through-line is the broken dashboard that never works and the two men who refuse to quit anyway.

## Status

**Active writing project (v1.7.7; core content v1.7.6, 2026-11-17).** Dashboard consolidated into one page (live status, one viewer for all screenplays/docs, Kling prompts, corpus search, file library, pipeline jobs, canon, system/tray) at `http://127.0.0.1:8765` (8765, not 8080 — 8080 belongs to another local service). See [DEPLOY.md](DEPLOY.md) for the manual. Dashboard/tray are frozen as of 2026-11-19 (see banner above).

No produced episodes are in the repo — this is scripts, transcripts, and video-generation prompts, not a finished show.

## What's in here

- **The corpus** — `CONVERSATION_SCRIPT_COMPLETE.txt` (~5.9 MB) and `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` (~7.6 MB): 247+ transcribed audio/video sessions, per `VISION.md`. (`sitcom script.txt` is a byte-identical copy kept **on purpose** as the parity twin — `dashboard.py` checks the two files against each other for corpus integrity. Decided 2026-11-19: KEEP, do not delete.)
- **Screenplays (canonical)** — `sitcom_final_s1.md` (Season 1, 12 episodes), `sitcom_final_s2.md` (Season 2, 8 episodes + 6 bonus) + `sitcom_rewrite_s2.md`
- **Historical / source material (not finals)** — `sitcom_bob_and_lum_full_screenplay.md`, `sitcom_bob_and_lum_episode1.md`, `sitcom_bob_and_lum_DARK.md`, `sitcom_bob_and_lum_full_series.md`
- **Kling AI video prompts** — `sitcom_bob_and_lum_DARK_KLING.md`, `sitcom_bob_and_lum_episode1_kling.md`, `sitcom_bob_and_lum_full_series_kling.md`: scene-by-scene cinematic generative-video prompts (lighting, camera angles, color grading, emotional cues)
- **Dashboard** — `dashboard.py` (single-page script/transcript portal), `tray_runner.py` (system tray controller), `start_dashboard_hidden.ps1` / `.vbs` (headless launchers)
- `transcribeme/` — transcription tooling
- Working docs: `VISION.md`, `ROADMAP.md`, `TODO.md`, `HANDOFF.md`, `MEMORY.md`, `CHANGELOG.md`, `DEPLOY.md`

Note: root `.tmp_*.txt` scratch files were archived (not deleted) to `archive/tmp_20261113/` on 2026-11-13. Start the dashboard with `python dashboard.py` or `start_dashboard_hidden.vbs`, then open `http://127.0.0.1:8765` in a browser.
