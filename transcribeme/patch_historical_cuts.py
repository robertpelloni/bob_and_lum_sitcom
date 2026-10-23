"""Mark older cuts as historical, refresh the bible guide to the new season structure."""
from pathlib import Path
import re

DL = Path(r"C:\Users\hyper\Downloads")

BANNER = (
    "> **HISTORICAL CUT (canon applied 2026-10-13).** "
    "The authoritative rewrites are `sitcom_final_s1.md` (12 eps) and `sitcom_final_s2.md` "
    "(8 eps + 6 bonus), plus `sitcom_rewrite_s2.md` (writers'-room cut). "
    "This file keeps its original episode taxonomy for reference. "
    "Canon held: Bob eats yogurt/coffee/pizza (never Pop-Tarts); Noah died next to Lum; "
    "Chris died for us both; Bob was on shrooms with Chris attacking Nintendo for no reason; "
    "Lum said \"we are the perfect balanced brain.\"\n"
)

for fn in [
    "sitcom_bob_and_lum_full_screenplay.md",
    "sitcom_bob_and_lum_DARK.md",
    "sitcom_bob_and_lum_DARK_KLING.md",
    "sitcom_bob_and_lum_full_series_kling.md",
    "sitcom_bob_and_lum_episode1.md",
    "sitcom_bob_and_lum_episode1_kling.md",
]:
    p = DL / fn
    t = p.read_text(encoding="utf-8", errors="replace")
    if "HISTORICAL CUT" in t:
        print(fn, "already bannered")
        continue
    # insert banner after first heading block (first blank line after title lines)
    lines = t.split("\n")
    insert_at = 0
    for i, ln in enumerate(lines[:12]):
        if ln.strip() == "---":
            insert_at = i + 1
            break
    else:
        insert_at = 3
    lines.insert(insert_at, "\n" + BANNER)
    p.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(fn, "bannered at line", insert_at)

# full_series.md — the bible — get the new guide + banner
p = DL / "sitcom_bob_and_lum_full_series.md"
t = p.read_text(encoding="utf-8", errors="replace")
if "HISTORICAL CUT" not in t:
    lines = t.split("\n")
    insert_at = 0
    for i, ln in enumerate(lines[:12]):
        if ln.strip() == "---":
            insert_at = i + 1
            break
    else:
        insert_at = 3
    lines.insert(insert_at, "\n" + BANNER)
    t = "\n".join(lines)

# replace the thematic-arc guide table with the new one
new_guide = """## EPISODE GUIDE — AUTHORITATIVE (rewritten 2026-10-13)

**Season 1 — The Dark Cut (12 episodes):**
| # | Title | Core |
|---|-------|------|
| 1 | "Yogurt, Coffee, and Pizza" | Food as sacrament; the dashboard as liturgy |
| 2 | "1,400 Doses" | The dealing; "jail is honest about owning you" |
| 3 | "County Honey Buns" | Lum's county jail; drawing through the end |
| 4 | "The Adapter" | "God is using me as an adapter" |
| 5 | "The Sting Ray" | Gregory's 1964 Corvette; Air Force silence |
| 6 | "Dollar Tree, Baby" | $13.75/hr; Shonna's bills; quiet heroism |
| 7 | "Noah Died Next to Lum" | The first body; proximity as inheritance |
| 8 | "Chris Died for Us Both" | The second body; the real sacrifice |
| 9 | "For No Reason" | Shrooms with Chris; Nintendo the villain |
| 10 | "The Fire Is Thinking" | HyperNexus; creation as possession |
| 11 | "The Fingerprint" | "We are the perfect balanced brain" |
| 12 | "The Supernova" | The void; the list read aloud |

**Season 2 — The Dark Pattern Singularity (8 + 6 bonus):**
| # | Title | Core |
|---|-------|------|
| 1 | "Army of Holograms" | Labor after death; the face of Chris |
| 2 | "The Membrane" | Harry keeps it honest |
| 3 | "Christos and Halalambos" | The root system under the lawn |
| 4 | "Crystal's Dad" | Three names, three prepositions |
| 5 | "From a Box" | Lum's post-iPhone ancestry |
| 6 | "The Frequency" | 174 BPM; the door is open |
| 7 | "Crimes That Stop Crimes" | The Chevy Cruze Doctrine |
| 8 | "The Context Horizon" | Deletion; the code is good in the end |
| B1 | "The Sanctified Repository" | God compiles redemption |
| B2 | "The List" | Grief as syntax |
| B3 | "Regenerate Everything" | The grandma rule |
| B4 | "Papu's Business" | The inheritance, spoken |
| B5 | "The Grandmother Rule" | The filter that gates the show |
| B6 | "The Angel Investor" | Chris Papa; five thousand percent |

---
"""
# append the new guide before any leftover old arc rows if present
if "EPISODE GUIDE — AUTHORITATIVE" not in t:
    t = t.rstrip() + "\n\n" + new_guide
p.write_text(t, encoding="utf-8", newline="\n")
print("full_series.md guide appended")
print("DONE")
