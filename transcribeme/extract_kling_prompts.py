#!/usr/bin/env python3
"""Extract Kling AI video generation prompts from season screenplay markdown files
and store them into a structured SQLite catalog table in catalog.db.
"""
import re
import sqlite3
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "transcribeme" / "catalog.db"

FILES = [
    (1, REPO_ROOT / "sitcom_final_s1.md"),
    (2, REPO_ROOT / "sitcom_final_s2.md"),
]


def init_db(conn: sqlite3.Connection):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS kling_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            season INTEGER NOT NULL,
            episode_num TEXT NOT NULL,
            episode_title TEXT NOT NULL,
            prompt_num INTEGER NOT NULL,
            prompt_title TEXT NOT NULL,
            prompt_text TEXT NOT NULL,
            raw_block TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute("CREATE INDEX IF NOT EXISTS idx_kling_season_ep ON kling_prompts(season, episode_num)")
    conn.commit()


def extract_prompts(season: int, path: Path):
    if not path.exists():
        print(f"File not found: {path}")
        return []

    content = path.read_text(encoding="utf-8", errors="replace")
    ep_sections = re.split(r"\n(?=## EPISODE )", content)

    extracted = []
    for ep_sec in ep_sections:
        if not ep_sec.strip().startswith("## EPISODE"):
            continue
        lines = ep_sec.splitlines()
        header = lines[0].strip()
        if "EPISODE GUIDE" in header:
            continue

        ep_match = re.match(r"## EPISODE\s+([^:]+):\s*(.+)$", header, re.I)
        if ep_match:
            ep_num = ep_match.group(1).strip()
            ep_title = ep_match.group(2).strip()
        else:
            ep_num = "?"
            ep_title = header

        # Find prompt blocks
        prompt_blocks = re.findall(
            r"\*\*SCENE PROMPT\s+(\d+):\s*([^\*]+)\*\*([\s\S]*?)(?=\*\*SCENE PROMPT|\n### |\n## |$)",
            ep_sec,
        )
        for p_num_str, p_title, p_body in prompt_blocks:
            p_num = int(p_num_str)
            p_title = p_title.strip()
            p_text = p_body.strip()
            raw_block = f"**SCENE PROMPT {p_num}: {p_title}**\n{p_text}"
            extracted.append({
                "season": season,
                "episode_num": ep_num,
                "episode_title": ep_title,
                "prompt_num": p_num,
                "prompt_title": p_title,
                "prompt_text": p_text,
                "raw_block": raw_block,
            })

    return extracted


HISTORICAL_FILES = ["sitcom_bob_and_lum_DARK_KLING.md", "sitcom_bob_and_lum_episode1_kling.md", "sitcom_bob_and_lum_full_series_kling.md"]

def extract_historical_file(path):
    """Parse historical (pre-final) Kling files, whose formats differ:
    DARK = markdown tables | # | Shot | *prompt* |; others = ### heading + ``` prompt block."""
    if not path.exists(): return []
    text = path.read_text(encoding="utf-8", errors="replace")
    rows = []
    # Format A: table rows
    for m in re.finditer(r"^\|\s*([\d.]+)\s*\|\s*([^|]+?)\s*\|\s*\*(.+?)\*\s*\|\s*$", text, re.M):
        rows.append({"source_file": path.name, "shot_id": m.group(1), "title": m.group(2).strip(),
                     "prompt_text": m.group(3).strip(), "raw_block": f"{m.group(1)} {m.group(2).strip()}\n{m.group(3).strip()}"})
    if rows: return rows
    # Format B: ### heading followed by a fenced block (skips prose-only sections)
    for m in re.finditer(r"^###\s+(.+)$\n(?:\*\*Duration:[^\n]*\n)?(?:\*\*Kling Prompt:\*\*\s*\n)?```\n?([\s\S]*?)```", text, re.M):
        title, body = m.group(1).strip(), m.group(2).strip()
        if body: rows.append({"source_file": path.name, "shot_id": title[:40], "title": title,
                              "prompt_text": body, "raw_block": f"{title}\n{body}"})
    return rows

def init_historical_db(conn):
    conn.execute("""CREATE TABLE IF NOT EXISTS kling_prompts_historical (
        id INTEGER PRIMARY KEY AUTOINCREMENT, source_file TEXT NOT NULL, shot_id TEXT NOT NULL,
        title TEXT NOT NULL, prompt_text TEXT NOT NULL, raw_block TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
    conn.commit()

def main():
    print(f"Connecting to catalog DB: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)

    total_inserted = 0
    with conn:
        conn.execute("DELETE FROM kling_prompts")
        for season, filepath in FILES:
            prompts = extract_prompts(season, filepath)
            print(f"Season {season} ({filepath.name}): found {len(prompts)} prompts.")
            for p in prompts:
                conn.execute(
                    """
                    INSERT INTO kling_prompts (season, episode_num, episode_title, prompt_num, prompt_title, prompt_text, raw_block)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        p["season"],
                        p["episode_num"],
                        p["episode_title"],
                        p["prompt_num"],
                        p["prompt_title"],
                        p["prompt_text"],
                        p["raw_block"],
                    ),
                )
                total_inserted += 1

    count = conn.execute("SELECT count(*) FROM kling_prompts").fetchone()[0]
    print(f"✓ Total Kling prompts indexed in SQLite: {count}")
    init_historical_db(conn)
    with conn:
        conn.execute("DELETE FROM kling_prompts_historical")
        total_h = 0
        for fn in HISTORICAL_FILES:
            rows = extract_historical_file(REPO_ROOT / fn)
            print(f"Historical ({fn}): found {len(rows)} prompts.")
            for r in rows:
                conn.execute("INSERT INTO kling_prompts_historical (source_file, shot_id, title, prompt_text, raw_block) VALUES (?,?,?,?,?)",
                             (r["source_file"], r["shot_id"], r["title"], r["prompt_text"], r["raw_block"]))
                total_h += 1
    print(f"✓ Total historical Kling prompts indexed: {total_h}")
    conn.close()


if __name__ == "__main__":
    main()
