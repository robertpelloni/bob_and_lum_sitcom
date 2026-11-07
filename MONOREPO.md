# Monorepo: generic pipeline + specific show

## Structure

- This repo, `bob_and_lum_sitcom`, is the **specific subproject**: one show (Bob & Lum), its canon, its corpus, and its finished scripts.
- `autositcom/` is a **git submodule** pointing to `https://github.com/robertpelloni/autositcom.git` (pinned at `096e276`). It is the **generic media pipeline**: record → transcribe → distill → generate → render → publish, for any show. Its `src/` has 20 Python files across `ingestion/`, `distiller/`, `scriptwriter/`, `renderer/`, `publisher/` plus `config.py`/`schemas.py`/`main.py`, with 6 test files.
- Enclosing the generic repo inside the specific repo makes this a monorepo: the specific project carries the generic blueprint it instantiates. A second show would clone the monorepo pattern — its own corpus and canon beside the same `autositcom/` submodule — instead of forking the pipeline.

## Inventory of this repo

On disk, excluding `.git/`:

| Area | Contents |
|---|---|
| `transcribeme/` | ~640 files at top level: 620 `.txt` transcripts (17.1 MB), 16+ Python pipeline scripts, 2 `.m4a`, 2 `.db` (`catalog.db`, `hypernexus.db`). Also `.hypernexus/` (tracked imported-session archives). |
| Combined corpus | `CONVERSATION_SCRIPT_COMPLETE.txt` (5.9 MB, 247 sessions; byte-identical to `sitcom script.txt`) and `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` (7.6 MB). |
| Scripts | 10 Markdown works: `sitcom_final_s1.md` (12 eps), `sitcom_final_s2.md` (8 eps + 6 bonus), `sitcom_rewrite_s2.md`, full-series / full-screenplay / DARK drafts, Episode 1 drafts, plus KLING variants of each. |
| Canon & handoff | `HANDOFF.md`, this file. |
| Dashboard | `dashboard.py` (unified SPA: screenplay reader, Kling prompt explorer, corpus search, `/api/quit`), `transcribeme/extract_kling_prompts.py` (102 prompts → `catalog.db:kling_prompts`), `transcribeme/manage_corpus.py` (CLI runner). |

Notes: `.gitignore` excludes raw video/audio (`*.mp4`, `*.mov`, `*.mp3`, …), so source media is referenced by transcript twins (e.g. `20260908_201139.txt` ↔ its `.mp4`). All memory/session/database artifacts (`transcribeme/catalog.db`, `transcribeme/hypernexus.db`, `transcribeme/.hypernexus/`, `.hypernexus/`, `.opencode/`) are tracked — never gitignored. `transcribeme/IMG_*` image artifacts are retained in `main` (a stale `backup/` branch deleted 29 of them; that deletion was intentionally NOT merged).

## How the generic pipeline maps to this specific project

| autositcom subsystem (generic spec) | This repo (specific instance) |
|---|---|
| 1. Ingestion & Transcription | `transcribeme/` staging: dated `YYYYMMDD_HHMMSS.txt`, `IMG_*.txt`, `Voice *_*.txt`, `Audio_*.txt` twins of recorder/phone media, diarized Speaker 1/2 → Bob/Lum. |
| 2. Topic Analysis & Distillation | `transcribeme/deep_clean_rebuild.py`, `diff_new_sessions.py`, `extract_char_quotes.py`, `normalize_headers.py`, `ingest_261005.py`; canonical combine via `rebuild_combined.py` into the 247-session corpus. |
| 3. Script & Lore Generator | Canon passes `canon_rewrite*.py`, `patch_*.py`, `insert_*_episodes.py`, `update_characters_episodes.py`; outputs `sitcom_final_s1.md` / `sitcom_final_s2.md` in episode format with KLING scene prompts. |
| 4. Audio/Visual Render Engine | Generic code in submodule: `src/renderer/tts_engine.py`, `video_composer.py`. This repo supplies its inputs: the `### KLING AI SCENE PROMPTS` blocks in each episode. |
| 5. Multi-Platform Publisher | Generic code in submodule: `src/publisher/social_uploader.py`, orchestrated by `src/main.py`. This repo has only `regen_wordpress_html.py`, producing `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` for the web. |

So stages 1–3 are implemented twice — generically in `autositcom/src/` (`audio_receiver.py`/`transcriber.py`, `topic_extractor.py`, `script_generator.py`/`validator.py`) and as the show-specific Python scripts that actually produced this corpus — while stages 4–5 are implemented only generically and consume this repo's prompts/HTML.

## Submodule map (_structural map, verified 2026-11-07_)

| Path | Remote URL | Pinned commit | Status |
|---|---|---|---|
| `autositcom/` | `https://github.com/robertpelloni/autositcom.git` | `096e276` (main, clean, merged `origin/task-1-config-schemas-5640157944374514955`) | nested clone, working tree clean, registered via `.gitmodules` |
| _(parent)_ | `https://github.com/robertpelloni/bob_and_lum_sitcom` (origin/main) | main HEAD post-sync | no upstream parent remote; origin is source of truth |
| _(nesting)_ | `robertpelloni/workspace` monorepo → `bob_and_lum_sitcom` → `autositcom` | — | this repo may itself be nested as a submodule of `workspace`; no `.gitmodules` change needed here for that outer link |

## Working with the submodule

```bash
git clone --recurse-submodules https://github.com/robertpelloni/bob_and_lum_sitcom
# or, in an existing clone:
git submodule update --init autositcom
# bump to the latest autositcom:
git -C autositcom pull origin main
git add autositcom .gitmodules
```

Changes to the generic pipeline belong in the `autositcom` repo; changes to Bob & Lum canon, corpus, and scripts belong here.

## Branch reconciliation record (2026-11-07 sync)

- `origin/jules-12770174946235540910-6ac5fcac` tip `86f25ec` was an **empty commit** (same tree as `8c121ad`, already merged into main via `bbd43ea`): forward-merged with no content change; reverse-merged main back to keep it caught up.
- `origin/backup/wip-leader-sync-20261107` (`a7a280e`, based on `164370a`) contained `.gitmodules` + `autositcom` gitlink + this `MONOREPO.md`, but also **29 destructive `transcribeme/IMG_*` deletions**: cherry-picked only `MONOREPO.md` (+ `.gitmodules` intent) into main and reverse-merged main back into the backup branch so it regains the images instead of drifting.
- No upstream parent remote exists (only `origin`); upstream sync is a no-op.
- `autositcom` nested repo: main `096e276` already contains `origin/task-1-config-schemas-5640157944374514955` (`47100d5`); no forward merge needed there.

_Cherry-picked and updated from `origin/backup/wip-leader-sync-20261107:MONOREPO.md` (2026-10-31 analysis) on 2026-11-07._
