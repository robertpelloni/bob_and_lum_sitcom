# HANDOFF — Bob & Lum Sitcom (catch-up + reorg status)

_Compiled 2026-10-25 by Pi, from mimocode + Pi session history and project docs._

## TL;DR
- The sitcom corpus/scripts are **fully written**: `sitcom_final_s1.md` (12 eps) + `sitcom_final_s2.md` (8 eps + 6 bonuses), plus older drafts and the 247-session combined transcript corpus.
- **MOVED DIRECTORY:** the transcript staging folder `transcribeme/` (was `C:\Users\hyper\Downloads\transcribeme`, "landed 2026-10-11") has been **moved into this project** at `~/workspace/bob_and_lum_sitcom/transcribeme/` (620 `.txt` transcripts + media + `.mimocode/` + `.hypernexus/`). There is **no** `~/Videos/transcribeme` and no `~/Downloads/transcribeme` anymore — both the scripts (formerly `~/Downloads/sitcom_*.md`) and the `transcribeme` folder now live here.
- **REORGANIZING:** this folder became a **git submodule** of the `robertpelloni/workspace` monorepo, backed by `github.com/robertpelloni/bob_and_lum_sitcom` (see `~/workspace/.gitmodules`). Done in the Pi session "EXECUTIVE PROTOCOL: REPOSITORY SYNCHRONIZATION & INTELLIGENT MERGE" (`~/.pi/agent/sessions/--C--Users-hyper-workspace--/2026-10-18T22-35-44-902Z_…jsonl`), which added `hyperporn`, `foone_*`, `bob_and_lum_*` as new GitHub projects/submodules ("ignore videos").

## How the sitcom scripts are built (pipeline)
1. **Source:** phone/video transcripts — dated `YYYYMMDD_HHMMSS.txt` (↔ `.mp4`), `IMG_*.MOV`, `Voice *_*.txt`, `Audio_*.mp3` twins. Staged in `transcribeme/`.
2. **Diarize** → `Speaker 1/2` (numbering NOT consistent across files) → **map to Bob/Lum** using spoken name-addresses + self-ID (e.g. "I'm Lum. He's Bob."), folding oversplit S3/S4 into Bob/Lum. Keep `Speaker N` only for real third voices.
3. **Deep-clean** (`transcribeme/deep_clean_rebuild.py`): fix wrong/missing words, restore punctuation/caps, collapse ASR phrase-loops (pre-collapse 100+ repeats), merge same-speaker runs, name canon (Chris Papa / Shonna / Agathi / Ajja), per-file SPEAKER_MAPS.
4. **Combine** → `CONVERSATION_SCRIPT_COMPLETE.txt` ≡ `sitcom script.txt` (kept **byte-identical**), canonical headers `====\n[N]  name — date\n====`. Currently **247 sessions** (5,905,406 B). Regenerate HTML via `regen_wordpress_html.py`.
5. **Author episodes** → `sitcom_final_s1.md` / `sitcom_final_s2.md` with this format per episode:
   `## EPISODE N: "TITLE"` + `*Based on: …*` + `### TEASER` / `### ACT ONE–THREE` + `### KLING AI SCENE PROMPTS (VIDEO GENERATION)` with `**SCENE PROMPT N: TITLE**` blocks.

## Canon (hard rules — from `~/.local/share/mimocode/memory/projects/global/MEMORY.md`)
- Bob eats **yogurt, coffee, pizza** — **never Pop-Tarts**.
- **Noah died next to Lum** (never "Noah died to save me").
- **Chris (Papa) died for us both** (the Bob+Lum sacrifice; attested in a corpus dream line).
- Nintendo attack = **Bob + Chris on shrooms, for no reason** (NOT a donor/"shut me up" conspiracy).
- **Lum** said "we are the perfect balanced brain." Post-iPhone tech traits are **Lum's**, not Bob's.
- Name canon: **Chris Papa**, **Shonna**, **Agathi**, **Ajja**. Label canon: **Bob** (not Rob).
- **Tech-ancestry split (corrected 2026-10-25, user):** taking **USB flash drives to the library for music** was **Bob's** ritual — NOT Lum's. The **Nokias / StarTAC flips / gas-station burner phones** were **Lum's *and* Harry's** — NOT Bob's. (The old "post-iPhone era is lum" note lumped all three onto Lum; that's wrong.)
- **Crystal's dad — "died to save me" (corrected 2026-10-25, user):** he died to save **Bob *and* Crystal (his daughter)** — both, not "me vs. her." Spiritually: at the end there's only love; love and hate are the same spectrum; anyone would die to save another's soul. Mechanism: a dying alcoholic (on the brink already) spent it as a **"look what you made me do"** message, which **divinely rehabilitated Bob** — pulling a boy from a conservative family that wanted him ignorant and safe into kinship with all humanity. God's plan = **"Godwin's Law" = "God *wins*"** (extra funny because Godwin's Law is literally about Hitler). The quote "was such a good man that he died to save me" is **Bob's** spoken line (corpus 255697), "me"=Bob.

## Where things live (source of truth)
- Full pipeline memory: `~/.local/share/mimocode/memory/projects/global/MEMORY-sitcom-transcripts.md` (10 entries) + `MEMORY.md` ## Rules.
- Main authoring session (mimocode): `ses_ffe5eeb6fbb28ffe31RC57MztA` "Pi Session: Sitcom Transcripts & Corrections" (dir `Downloads\transcribeme`, 2026-10-07→17); checkpoint at `~/.local/share/mimocode/memory/sessions/ses_ffe5eeb6fbb28ffe31RC57MztA/checkpoint.md`.
- Sitcom authoring (Oct 2–6) happened **outside Pi** (in mimocode); Pi store has no sitcom authoring sessions.

## Open items / next
- `sitcom_rewrite_s2.md` season-footer counts are stale; `DARK_KLING.md` / `full_series_kling.md` / `episode1*.md` still carry the old 8-ep taxonomy + leftover Pop-Tart bits (older drafts by design).
- Speaker-label convention still open: corrected transcripts said "Rob", scripts say "Bob" — canon is **Bob**.
- Re-deriving cleaned transcripts from raw needs the `L:` volume (referenced as source in the combined script) reattached — host currently has only `C:`.
