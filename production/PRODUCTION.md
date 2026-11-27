# BOB & LUM — Production Tracker

## Ground rules (Robert, Nov 22, 2026)
- Generator of record: **Google Gemini / Veo**, via Robert's signed-in Google account in his own Chrome. Access window: Google AI plan cancelled but active until **Dec 3, 2026**.
- NEVER label Muse Video output as Gemini output. The Nov 20 pilots (v1 live-action, v2 Rick-and-Morty style, v3 original cartoon) were **Muse Video**, not Gemini.
- Source scripts: canonical `sitcom_final_s1.md` / `sitcom_final_s2.md` in repo robertpelloni/bob_and_lum_sitcom (fetched @ f1260543, stored in `scripts/`). Dialogue verbatim; Kling prompts are NOT the script.
- Look: original adult-cartoon style of pilot v3. Character sheets CORRECTED Nov 22, 2026 (Robert: the old ones had Lum completely wrong). Full corrected sheets: `CHARACTER-REFERENCES.md`. Bob — 43, dark hair spiked up, THICK BLACK RECTANGULAR GLASSES always on, light stubble, rounder face, stockier build, black tee + silver chain, hoodie at home (blended from his ShiftBeat commercial presenter look + real portraits). Lum — 44, SLIM/lean, CLEAN-SHAVEN, short black hair slicked back with faded sides, lean angular face, East Asian features, koi tattoo sleeve on right arm, grey V-neck tee at home. Reference images of record are the REAL photos + commercial frames in `refs/` — the v3 cartoon frames (`S1E1/refs/style-*.jpg`) are SUPERSEDED for likeness. E1-01 was rendered with the wrong Lum and must be re-rendered before assembly.
- Title cards are made locally (ffmpeg), never generated — pilot v3's generated card invented "DEADLINE DOOM — Episode 5" and brand logos.
- No purchases/subscriptions. No contacting other people.

## Quota facts (checked Nov 22, 2026)
- Muse Power plan: 16% of weekly limit, resets Nov 28, 3:17 AM EST. (Separate pool — only relevant if Muse Video is ever used, and then it must be labelled as such.)
- Gemini/Veo quota: NOT visible to any Muse tool. Browser verification (Nov 22, 14:29-14:35 EST) read the UI directly: signed in as Robert Pelloni (pelloni.robert@gmail.com), sidebar plan shows **"Ultra"**. Video mode is **"Create videos With Gemini Omni"** — Videos chip, **Duration 10 seconds, Landscape 16:9, model selector "Neon"**. No "Veo 3.1" name shown, and NO usage limit, credit count, or expiry text visible anywhere in the interface. So clips are 10s each: 18 clips ≈ 3.0 min for S1E1.
- E1-01 attempt 1 FAILED (sent ~14:31, after ~3 min): Gemini's exact reply was "Sorry, something went wrong. Please try your request again." No limit message, paywall, CAPTCHA, or sign-in prompt. Clips 2-3 not attempted in that pass. Robert authorized a retry at 14:35 EST (same chat, images still attached; one retry, then one reload+retry, then stop and report).

## S1E1 "Yogurt, Coffee, and Pizza"
- Shot list: `S1E1/SHOTLIST.md` + `S1E1/shotlist.csv` — 18 dialogue/visual clips (~8s each ≈ 2.4 min) + local title card.
- E1-00 title card: DONE (ffmpeg, 4.0s, frame-verified).
- E1-01..03: rendering via Gemini browser pass (launched Nov 22).
- E1-04..18: queued, same pipeline, after first batch verifies (character consistency + dialogue accuracy + download integrity).
- Assembly: ffmpeg concat in clip order, title card first; verify duration, stream specs, frame-check each segment boundary.

## Gemini behavior learned (Nov 22, corrected-refs batch)
- With corrected refs (real photos + commercial frame), likeness is RIGHT: Bob glasses/stubble/hoodie/chain; Lum slim, clean-shaven, grey V-neck, koi sleeve visible.
- Same-chat generations are CUMULATIVE: E1-01 came out 10s, E1-02 20s, E1-03 30s, with later clips replaying earlier dialogue. E1-02's dialogue is present but jumbled/repeated. For clean clips, generate each clip in its OWN fresh chat (refs re-attached), or plan to trim tails.
- Downloads through Robert's device Chrome land on HIS PC; the harness download capture failed both batches (download_unreadable_discarded) — no clip files in the Muse workspace yet. Files must come from Robert's Downloads folder, or future batches should try the cloud browser so downloads are capturable.

## S1E2 "1,400 Doses"
- Script secured (same file, lines 252-380). Breakdown starts after S1E1 pipeline is proven.
- Content note: episode centres on the 1,400-dose windfall (script's own framing: ate half, threw half away, never glamorized). Watch for generator refusals on drug-adjacent dialogue; log any refusal verbatim in the tracker instead of silently rewriting lines.

## Existing Gemini/Veo assets (prior sessions, for reference)
- `~/workspace/imagine_media/gemini-veo-sitcom-clip-2026-11-21.mp4` — one Gemini sitcom clip (Nov 21).
- Reference frames for style: `S1E1/refs/style-dashboard.jpg`, `style-yogurt.jpg` (frames from pilot v3).

## Gemini quota wall (observed Nov 22, 2026)
- After batch 3's 5 successful generations (8 attempts incl. retries; 12 successful videos across the whole day), the "Create video" toggle went DISABLED account-wide. Reloads, a fresh tab, a 20-minute wait, and model switching (Auto <-> Neon) did not restore it. No limit or reset time is shown anywhere in the UI. Treat video generation as a limited daily/rolling budget: plan batches of ~5, expect a wall, retry the remainder after a reset (timing unknown — check the toggle state first).

## Planned Season 2 arc (logged Nov 22, 2026, Robert's direction via main chat)
- **"BECOMING BOBBI"** — planned Season 2 arc, written into the show bible in `scripts/sitcom_final_s1.md` right after the Episode Guide (done on the script side in main chat; logged here so the production record carries it too).
- Beat: money lands -> Bob transitions (becoming Bobbi, the twin he built first), played straight -> Season 3 opens with Bob back as a male, unexplained, uncommented, and with no gag about the return.
- REVISED Nov 22, 2026 (Robert, twice): (1) detransitioning might be too negative — avoided as a topic entirely. (2) The original mirror-line gag (the arc's first title) was CUT at his direction: the line could hurt the feelings of aging trans women who hold similar self-criticisms, and he doesn't want it landing on them. The phrase is retired from the arc, the title, and the beats.
- Tone rule (recorded with the arc): honest, never mocking, never glamorized; where a joke of Bob's could land on people who share the feeling without sharing the joke, the show leaves it out.
- Status: FUTURE-SEASON plan entry only. It does not change, reorder, or delay any Season 1 production.

## Step-back review (Nov 27, 2026, at Robert's direction: "reevaluating and stepping back")
- STATE: S1E1 title card + E1-01..E1-10 rendered and caption-verified; E1-11..E1-18 (8 clips) remain. Gemini access per Robert runs until Dec 3, 2026 — six days left; finishing S1E1 and starting S1E2 inside that window is the priority.
- WHAT WORKS: fresh chat per clip (no cumulative bleed), corrected photo refs (likeness right: Bob glasses/stubble/hoodie, Lum slim/clean-shaven/koi sleeve), local ffmpeg title cards, verbatim-dialogue prompts, tracker + GitHub sync.
- WHAT'S BROKEN: (1) Downloads through Robert's device Chrome land on HIS PC and the harness cannot read them back — so NO clip file has ever reached the Muse workspace, which means no assembly, no frame-level QC by Muse, and likeness verdicts are secondhand (browser caption/frame reports, not Robert's own eyes). FIX BEING TESTED Nov 27: generate via the CLOUD browser, whose downloads are capturable into the workspace; if the cloud browser is not signed into his Google account, fall back to the device browser and the files stay on his PC. (2) Quota: ~12 successful videos/day observed before the toggle disabled (Nov 22); plan batches of ~5 and expect a wall. (3) Minor flaws on record: E1-04 yogurt cup has a small printed label; E1-05 captions only partly verified; E1-09 captions blur one speaker split. None block assembly.
- ASSEMBLY GATE: an episode can only be assembled once its clip FILES are in the workspace. The moment downloads are capturable, assembly = title card + clips in shot-list order via ffmpeg concat, duration/stream verification, boundary frame checks.
