# MEMORY: Architectural Guidelines & Lore Canon

## Core Character & Historical Canon (Immutable Rules)
1. **Food Staples & Sacraments**:
   - Bob lives on **yogurt, coffee, and pizza**. He eats yogurt directly from the container with a fork and holds stale pizza slices like cigarettes.
   - **Bob NEVER eats Pop-Tarts.** Pop-Tarts must never be attributed to Bob.
   - Lum loves **county jail honey buns** and gas-station junk food.

2. **The Deceased & Sacrifices (Do Not Conflate)**:
   - **Chris Papa**: Died for **both** Bob and Lum ("Chris died for us both"). Angel investor, wore a different colored blazer in every scene, shroom trips, fought Nintendo for Bob.
   - **Noah**: Died **next to Lum** during a motorcycle night. Not "Noah died to save me" (Bob's recurring factual slip in early drafts).
   - **Crystal's Dad**: An alcoholic on the brink who spent his death as a message ("look what you made me do"), which divinely rehabilitated Bob and saved both Bob and Crystal. "Such a good man that he died to save me" (Bob's quote). Bob knew Crystal at age 13–14 in gifted education (MST/SAGE in Macomb County).

3. **Technological Ancestry & Artifacts**:
   - **USB Flash Drives to the Library**: This was **Bob's** ritual (fitting his music and distributions onto flash drives).
   - **Burner / Flip Phones**: Gas-station burners, Nokias, and Motorola StarTACs belong to **Lum and Harry** (Lum's younger brother, age 42).
   - **The Dashboard**: The dashboard on Bob's dual-monitor rig is perpetually broken, displaying error panels and looping psytrance tracks. It is liturgy.

4. **Name and Labeling Canon**:
   - Character labels in scripts must be **BOB** and **LUM** (never "Rob" or "Lung").
   - Family / Friends: **Chris Papa**, **Shonna** (not Shauna/Shawna), **Agathi** (not Agathie/Agathy), **Ajja**, **Harry** (Halalambos).

## Repository Architecture & File Roles
- `sitcom_final_s1.md`: 12 canonical Season 1 episodes with scene prompts.
- `sitcom_final_s2.md`: 8 canonical Season 2 episodes plus 6 bonus episodes.
- `sitcom_rewrite_s2.md`: Detailed thematic drafts and breakdown for Season 2.
- `sitcom_bob_and_lum_full_screenplay.md`: Full multi-episode master screenplay draft.
- `CONVERSATION_SCRIPT_COMPLETE.txt` / `sitcom script.txt`: Master verbatim 247-session corpus (byte-identical pair).
- `CONVERSATION_SCRIPT_COMPLETE.wordpress.html`: HTML formatted transcript reader.
- `transcribeme/`: Directory containing raw input transcript files, SQLite catalog database, and data cleaning/ingestion utilities.

## Runtime Process Priority Rule (2026-11-08)
- All heavyweight project processes (dashboard server, corpus rebuilds, Kling batch, ffmpeg renders, bulk Python scripts) must run at BelowNormal priority so they never hang the system.
- `dashboard.py` and `transcribeme/manage_corpus.py` self-lower via `lower_self_priority()` (Windows BELOW_NORMAL_PRIORITY_CLASS, Unix nice +10).
- Manual PowerShell launch: `Start-Process python -ArgumentList 'dashboard.py --port 8080'` then `(Get-Process -Name python | Sort-Object StartTime -Descending | Select-Object -First 1).PriorityClass = 'BelowNormal'`.
- Never raise agent runtime (node/codex) above Normal; only lower project workers.

