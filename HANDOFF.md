# HANDOFF — Bob & Lum Sitcom (Session State & Autopilot Summary)

_Updated 2026-11-19 — v1.7.7 (documentation/decisions release; core content is v1.7.6, 2026-11-17, head at update time was the v1.7.6 release commit). This handoff replaces the 2026-11-14 handoff, whose "Next" list asked for work already shipped in v1.6.0/v1.7.0 — that stale list is gone._

## Current state (verified)
- Canonical scripts: `sitcom_final_s1.md` (Season 1, 12 episodes, 51 prompts) and `sitcom_final_s2.md` (Season 2, 8 episodes + 6 bonus, 51 prompts) — 102 canonical Kling prompts, validated 102/102 (v1.7.1).
- Historical material: DARK / full-series / episode-1 files are source material, indexed separately as 177 historical Kling prompts (v1.6.0). They are not competing finals and will not be aligned to canon.
- Corpus: 247 sessions, `CONVERSATION_SCRIPT_COMPLETE.txt` byte-identical to its parity twin `sitcom script.txt` (dashboard parity check). 108 transcripts restored in v1.7.2 sit in `transcribeme/` unfolded.
- Dashboard: single page at `http://127.0.0.1:8765`, tray runner, canon-lint gate, markdown screenplay rendering with Bob/Lum filters, paginated corpus search with session context — all shipped by v1.7.0.

## Decisions made 2026-11-19 (owner-approved fix pass)
1. **Dashboard/tray FROZEN.** Feature-complete. No further dashboard versions; bug fixes only if it stops working.
2. **Parity twin KEPT.** `sitcom script.txt` is intentional — `dashboard.py` uses it as the corpus byte-parity check. Do not delete it as "duplication."
3. **Corpus fold FROZEN at 247 sessions.** No partial fold of the 33 text-assignable restored transcripts, and diarization is not approved. Fold only in one pass when all 108 restored transcripts have speaker assignments (`SPEAKER_CUES.md` is the worklist: 33 text-assignable, 75 need listening/diarization).
4. **Legacy `catalog.db` tables: DROP decided, execution queued.** `published_mcp_servers` (82 rows), `links_backlog` (7), `published_skills` (0) are HyperNexus residue and are not queried by the dashboard. Drop them in a local checkout session with sqlite, re-index, and verify `kling_prompts` = 102 and `kling_prompts_historical` = 177 before pushing the binary DB.

## Not working / not started — the real blockers
1. **Phase 4 has not started.** No voice samples extracted, no TTS/voice model chosen, no Kling account or render pipeline, no generated clips, no produced episodes. This needs owner account/provider choices and spend — it is not a repo fix.
2. **Tray icon** has never been visually confirmed on a desktop by a human (process verified BelowNormal; `Dashboard Status` check shipped v1.7.0).
3. **42 repo transcripts have no audio anywhere found** (see the Vibe backup report referenced in v1.7.2 notes).

## Next (in order)
1. Human: open http://127.0.0.1:8765 once, confirm the tray icon renders.
2. Local session: execute the decided `catalog.db` legacy-table drop with the verification above.
3. Owner: pick the Phase 4 providers (Kling account, TTS/voice route) — production is the only active phase now. Nothing else is queued.
