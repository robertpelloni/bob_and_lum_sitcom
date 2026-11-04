# HANDOFF — Bob & Lum Sitcom (Session State & Autopilot Summary)

_Updated 2026-11-04 by Jules (v1.2.0)_

## 1. Executive Summary & Codebase State
- **Corpus Health**:
  - `CONVERSATION_SCRIPT_COMPLETE.txt` and `sitcom script.txt` are **strictly byte-identical** (5,905,405 bytes, 247 sessions, 258,349 lines).
  - `CONVERSATION_SCRIPT_COMPLETE.wordpress.html` is fully generated and synchronized (7,643,029 bytes).
  - Transcripts cover sessions from 2025-02-25 through 2026-10-05.
- **Screenplay & Canon Status**:
  - Season 1: `sitcom_final_s1.md` (12 canonical episodes with Kling AI scene generation prompts).
  - Season 2: `sitcom_final_s2.md` (8 canonical episodes + 6 bonus episodes).
  - Character canon established: Bob lives on yogurt, coffee, and pizza (never Pop-Tarts); Chris Papa died for both Bob and Lum; Noah died next to Lum; Crystal's dad died to save Bob and Crystal as a message that divinely rehabilitated Bob; USB flash drives to library belong to Bob; burner/flip phones belong to Lum and Harry.
- **Governance Standards Implemented**:
  - `VERSION.md` (v1.2.0)
  - `VISION.md`, `MEMORY.md`, `ROADMAP.md`, `TODO.md`, `DEPLOY.md`, `IDEAS.md`, `CHANGELOG.md`
  - `.gitignore` updated with Python cache rules (`__pycache__/`, `*.pyc`).

## 2. Status of Dashboard, System Tray, and Running Services
- **Audit Findings**:
  - In this repository (`github.com/robertpelloni/bob_and_lum_sitcom`), the phrase "the dashboard" is primarily a core narrative / philosophical metaphor in the sitcom screenplays ("*The dashboard is always broken... the dashboard is the liturgy*").
  - There is currently **no desktop GUI, web frontend server, or system tray icon service** residing within this repository. The user prompt requests:
    > *"Where is the system tray icon? Does it have sensible features and the ability to quit the servers? Please run it and watch the logs for any errors or areas of improvement."*
  - **Answer**: The system tray application and server dashboard belong to the parent monorepo / HyperNexus agent environment (or sibling projects like HyperNexus / desktop runner). In `IDEAS.md` and `ROADMAP.md`, architectural designs and specifications have been detailed for creating a dedicated single-page application dashboard and a lightweight Python (`pystray`/Qt) system tray controller specifically for the Sitcom workflow.
  - No background server processes were found running on ports or failing in the background.

## 3. Tooling & Script Improvements
- Modernized `transcribeme/deep_clean_rebuild.py` and `transcribeme/regen_wordpress_html.py` to use repository-relative directory resolution instead of hardcoded `C:\Users\hyper\Downloads\` paths, while respecting optional environment variable overrides (`SITCOM_SCRIPT_SRC`, `SITCOM_SCRIPT_OUT`, `SITCOM_SRC_DIR`).
- Created `transcribeme/manage_corpus.py`:
  - `python3 transcribeme/manage_corpus.py --check` (validates byte integrity and session counts).
  - `python3 transcribeme/manage_corpus.py --build-html` (regenerates WordPress HTML reader).
  - `python3 transcribeme/manage_corpus.py --stats` (displays dialogue metrics and line counts).
- All 17 Python scripts pass `python3 -m py_compile`.

## 4. Next Priorities for Autopilot / Successor
1. **Auxiliary Draft Harmonization**: Check secondary drafts (`sitcom_bob_and_lum_DARK_KLING.md`, `full_series_kling.md`) to align them completely with the final 12-episode Season 1 canon.
2. **Kling Prompt Database**: Extract all Kling video prompts from `sitcom_final_s1.md` and `sitcom_final_s2.md` into structured SQLite tables in `transcribeme/catalog.db`.
3. **Web Dashboard & Tray Runner**: If the user desires a self-contained web dashboard in this repo, implement a lightweight local server (e.g. FastAPI / Flask / Node) serving an interactive screenplay reader and corpus search UI.
