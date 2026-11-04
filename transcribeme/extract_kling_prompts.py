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
    conn.close()


if __name__ == "__main__":
    main()
