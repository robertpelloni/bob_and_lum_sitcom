# Bob & Lum Sitcom

A dark-comedy sitcom derived from hundreds of hours of raw transcribed real-life conversations between Robert Pelloni (Bob) and Lumbros Kourlos (Lum): two lifelong friends in a Detroit apartment, among cold pizza boxes and glowing computer monitors, talking with total candor about addiction, grief, county jail, dead friends, and existential dread — while laughing uncontrollably. The through-line is the broken dashboard that never works and the two men who refuse to quit anyway.

## Status

**Active writing/production project (v1.5.0).** 2026-11-13: dashboard consolidated into one high-value-ordered page (live status, one viewer for all screenplays/docs, Kling prompts, corpus search, file library, pipeline jobs, canon, system/tray) at `http://127.0.0.1:8765` (8765, not 8080 — 8080 belongs to another local service). Tray icon fixed on Windows. See [DEPLOY.md](DEPLOY.md) for the manual.

No produced episodes are in the repo — this is scripts, transcripts, and video-generation prompts, not a finished show.

## What's in here

- **The corpus** — `CONVERSATION_SCRIPT_COMPLETE.txt` (~5.9 MB) and `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` (~7.6 MB): 247+ transcribed audio/video sessions, per `VISION.md`. (`sitcom script.txt` is a byte-identical duplicate of the corpus.)
- **Screenplays** — `sitcom_bob_and_lum_full_screenplay.md`, `sitcom_final_s1.md` (Season 1), `sitcom_final_s2.md` + `sitcom_rewrite_s2.md` (Season 2), `sitcom_bob_and_lum_episode1.md`
- **Dark cuts** — `sitcom_bob_and_lum_DARK.md`, `sitcom_bob_and_lum_full_series.md`
- **Kling AI video prompts** — `sitcom_bob_and_lum_DARK_KLING.md`, `sitcom_bob_and_lum_episode1_kling.md`, `sitcom_bob_and_lum_full_series_kling.md`: scene-by-scene cinematic generative-video prompts (lighting, camera angles, color grading, emotional cues)
- **Dashboard** — `dashboard.py` (single-page script/transcript portal), `tray_runner.py` (system tray controller), `start_dashboard_hidden.ps1` / `.vbs` (headless launchers)
- `transcribeme/` — transcription tooling
- Working docs: `VISION.md`, `ROADMAP.md`, `TODO.md`, `HANDOFF.md`, `MEMORY.md`, `CHANGELOG.md`, `DEPLOY.md`

Note: root `.tmp_*.txt` scratch files were archived (not deleted) to `archive/tmp_20261113/` on 2026-11-13. Start the dashboard with `python dashboard.py` or `start_dashboard_hidden.vbs`, then open `http://127.0.0.1:8765` in a browser.
