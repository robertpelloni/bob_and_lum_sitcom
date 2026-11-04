# IDEAS: Creative Expansions & Technical R&D

## 1. Web-Based Consolidated Sitcom Dashboard
- Build a lightweight single-page application (Vue, React, or vanilla Web Components) running locally via a simple backend server or static bundle:
  - **Single Consolidated Page Layout**: Eliminate deep navigation hierarchies. Provide tabs or collapsible split panes:
    - *Screenplay Reader*: Full script presentation with character filters (Bob lines, Lum lines, action prompts).
    - *Prompt Laboratory*: Browse, edit, and batch-export Kling video generation prompts with parameter controls (aspect ratio, cfg scale, motion dynamics).
    - *Corpus Search Engine*: Instant full-text search across 5.9 million characters of conversations with speaker highlights.
    - *Media Gallery*: Map completed video and audio renders directly to corresponding scene cards.
- **Desktop System Tray Controller**:
  - Implement a tray icon using Python (`pystray` / Qt / Tauri) with options to:
    - Launch Dashboard in browser (`localhost:port`).
    - Monitor Kling generation queue.
    - Start / stop background transcription watchers.
    - Safely quit all backend processes.

## 2. Kling AI Video Generation Automation
- Create an automated prompt ingest script that parses `sitcom_final_s1.md` and `sitcom_final_s2.md` and extracts every `**SCENE PROMPT N: ...**` block.
- Feed prompts into an automated rendering queue via unofficial API or headless browser automation with auto-retry and video downloading.
- Store video metadata in `transcribeme/catalog.db` under a `kling_renders` table.

## 3. Detroit Dialect & Voice Cloning Alignment
- Extract clean audio clips from source recordings (`IMG_*.MOV`, `Audio_*.mp3`).
- Train custom voice models capturing Bob's rapid, breathless golden-retriever delivery and Lum's gravelly, slow-paced deadpan timing.
- Generate synchronized multi-character audio dialogue per episode to accompany video renders.

## 4. Comic Book / Storyboard Previsualization
- Convert Kling scene prompts into panel-by-panel comic / storyboard graphics using Flux or Midjourney for fast visual review before full video rendering.
