# BOB & LUM — Production Review Hub

Everything for the sitcom production, in one place. Repo: https://github.com/robertpelloni/bob_and_lum_sitcom/tree/main/production
Last updated: Nov 22, 2026.

## Start here
- **Corrected script (Season 1):** `sitcom_final_s1.md` in the repo root — Bob/Lum character sheets corrected Nov 22, 2026 from their actual photos.
- **Character references (the source of truth):** `production/CHARACTER-REFERENCES.md`
  - Bob (43): spiky dark hair, THICK BLACK RECTANGULAR GLASSES (always on), light stubble, stockier build, black tee + silver chain, dark hoodie at home.
  - Lum (44): SLIM, CLEAN-SHAVEN (never a beard), slicked-back black hair with faded sides, grey V-neck tee, Japanese koi tattoo sleeve on his right arm.
- **Reference photos:** `production/refs/` — actual-duo, actual-lum-front, actual-lum-profile, actual-bob-portrait, actual-bob-grin, + 2 ShiftBeat commercial frames.

## Production tracker
- `production/PRODUCTION.md` — ground rules, generator facts, quota facts, lessons learned.
- `production/S1E1/shotlist.csv` + `SHOTLIST.md` — Episode 1: 18 clips, verbatim dialogue, per-clip status.
- `production/S1E2/shotlist.csv` + `SHOTLIST.md` — Episode 2: 14 clips, ready to generate.

## Episode 1 — "Yogurt, Coffee, and Pizza" status
| Clip | Status |
|---|---|
| Title card | ✅ Done locally, correct text — in repo at `production/S1E1/title-card.mp4` |
| E1-01 teaser establishing | ✅ Rendered (Gemini), likeness correct |
| E1-02 "It's four in the morning" | ✅ Regenerated clean — exactly 10s, dialogue in exact order |
| E1-03 "This is my dinner" | ✅ Rendered clean (10s, dialogue exact) |
| E1-04 … E1-10 | ✅ All rendered (10s each, dialogue verified from captions, likeness correct) |
| E1-11 … E1-18 | ⏳ Not yet generated — Gemini's video toggle hit an account quota wall on Nov 22 after 12 successful videos that day; retry after it resets (no reset time shown) |

## Episode 2 — "1,400 Doses" status
- Title card ✅ in repo at `production/S1E2/title-card.mp4`. All 14 clips ⏳ not yet generated.

## Where the rendered clips live
Generated clips are in Robert's Gemini chats and his Chrome Downloads folder (the browser harness cannot pull them into the workspace):
- Corrected batch (E1-01, flawed E1-02/E1-03): https://gemini.google.com/app/8dcb325b6144ec37
- Clean clips: E1-03 cb2d624c3087874d, E1-05 786bfda90cc5fe20, E1-08 6b0153d9be8056f0, E1-09 1bb59644dc798e60, E1-10 9bb0efbaedd83076 (plus E1-04 b09c78997fd62aa5, E1-06 2dcca676178fe55b, E1-07 73da54264e17deec)
- E1-02 clean regeneration: https://gemini.google.com/app/fa5338e057674c65
- E1-03 failed attempts: https://gemini.google.com/app/fb6584e292c622b2

## Method that works (learned Nov 22)
- One FRESH Gemini chat per clip, 4 reference photos attached each time — same-chat generations come out cumulative (10s/20s/30s with replayed dialogue).
- Title cards are made locally with ffmpeg, never generated (generated title cards invent wrong text).
- Generator: Google Gemini video ("Create videos with Gemini Omni", model "Neon"), 10s, 16:9, via Robert's signed-in account (Ultra plan; access per Robert until Dec 3, 2026).
