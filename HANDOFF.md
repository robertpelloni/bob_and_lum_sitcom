# HANDOFF — Bob & Lum Sitcom (Session State & Autopilot Summary)

_Updated 2026-11-13 by [muse-wonder-1.0 in Muse Code in C:\Users\hyper\workspace\bob_and_lum_sitcom on laptop] — v1.6.0 (adds: 177 historical Kling prompts indexed with dashboard toggle, canon-lint gate, 5 maintained tests in build.ps1, markdown screenplay viewer with Bob/Lum filter, paginated corpus search, cached /api/status)_

## What changed this session (v1.5.0)
- **Dashboard consolidated to one page** (`dashboard.py`, stdlib only): Overview (live `/api/status`) → Screenplays & Docs (one viewer, 19 allowlisted files) → Kling Prompts (102, filter/copy/copy-filtered) → Corpus Search (speaker highlight) → Library/Files (47 files with roles) → Pipeline & Scripts (real job output) → Canon → System (log/quit/tray help). 36 tooltips. Dead `showTab`, hardcoded metrics/version, and prompt-XSS fixed.
- **Port 8080 → 8765 everywhere**: 8080 is `node server/ai_proxy.js` (another project, PID-owned, BelowNormal) — left running untouched. Dashboard binds `127.0.0.1:8765`.
- **Tray fixed**: Windows `$DISPLAY` gate removed (tray could never appear); child hidden/BelowNormal/logged; menu Open/Start/Stop/Restart/Check/View log/Quit All. Tray process launched and verified BelowNormal this session; icon pixels not visually sighted by agent.
- **Scripts**: new `build.ps1` (compile+check+stats+re-index+HTML); hidden launchers identity-check `/api/status`; `.tmp_*.txt` archived to `archive/tmp_20261113/` (restorable, not deleted); `dashboard.log` gitignored; `manage_corpus --stats` byte count fixed (CRLF undercount).
- **Coordination (Edge CDP 9222)**: tabs confirmed muse.ai, ChatGPT, Gemini. Identity check-in sent to Muse and Gemini. ChatGPT composer contained another lane's unsent HyperNexus draft — deliberately not overwritten/sent.

## Verified live (2026-11-13 evening)
- Corpus: 6,163,756 bytes, 247 sessions, 258,350 lines, sha `c719b1dbd333`, twin byte-identical; `build.ps1 -SkipHtml` green; prompts re-indexed 51+51=102.
- Dashboard `http://127.0.0.1:8765`: `/`, `/api/status|prompts|search|doc|screenplay|files|log`, `POST /api/check` all 200; traversal `/api/doc?name=../../dashboard.py` → 404. Running BelowNormal (pythonw, via hidden launcher). Note: processes started this session stop when the agent session ends — restart with `python dashboard.py` / `start_dashboard_hidden.vbs`, then open http://127.0.0.1:8765 in a browser.
- An external Protocol process committed the code half mid-session as `750beb4 chore: track dirty state (Protocol #291)`; docs/version/archive half is committed separately as v1.5.0. No submodules exist in this repo (no `.gitmodules`); local `main` was already in sync with `origin/main`, Jules/backup branches were already merged (history #281).

## Not working / not running — needs decisions
1. Non-final Kling files (DARK/episode1/full-series) are readable but **not indexed** in `kling_prompts` — index or mark superseded?
2. `catalog.db` legacy HyperNexus tables (82 MCP servers etc.) — keep, export, or drop? (Untouched.)
3. No Kling/TTS keys or render pipeline — Phase 4 needs owner accounts/choices.
4. Screenplays render as plain text; proper markdown + BOB/LUM filters are TODO.
5. Tray icon needs a human glance to confirm it renders on the desktop.

## Next (in order)
1. Human: open http://127.0.0.1:8765, confirm tray icon, skim TODO follow-ups.
2. Index/supersede non-final Kling; canon-lint gate in `build.ps1`.
3. Markdown screenplay rendering; corpus search pagination/session context.
4. Phase 4 scoping: Kling queue + voice table reads (owner picks providers).
