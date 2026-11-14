#!/usr/bin/env python3
"""Kling prompt validation report (Phase 2, non-gating).

Checks every indexed prompt (canonical 102 + historical 177) for production
basics: non-trivial length and at least one camera/lighting/motion cue that
Kling responds to. Prints a report; exit 0 unless the DB/table is missing.
Usage: python transcribeme/validate_prompts.py [--json]
"""
import json, re, sqlite3, sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "transcribeme" / "catalog.db"
CUES = re.compile(r"wide|close[- ]?up|medium|shot|camera|light|glow|pan|zoom|track|angle|lens|cinematic|interior|exterior", re.I)

def _report(rows, text_key):
    weak = [r for r in rows if len(r[text_key]) < 40 or not CUES.search(r[text_key])]
    return {"total": len(rows), "with_camera_or_light": len(rows) - len([r for r in rows if not CUES.search(r[text_key])]),
            "weak_count": len(weak), "weak_sample": [str(r[0])[:60] for r in weak[:10]]}

def validate(db_path=None):
    db_path = db_path or DB_PATH
    if not db_path.exists(): raise FileNotFoundError(f"missing {db_path} - run extract_kling_prompts.py")
    c = sqlite3.connect(db_path)
    canon = c.execute("SELECT prompt_title, prompt_text FROM kling_prompts").fetchall()
    try: hist = c.execute("SELECT title, prompt_text FROM kling_prompts_historical").fetchall()
    except Exception: hist = []
    c.close()
    return {"canonical": _report(canon, 1), "historical": _report(hist, 1)}

def main():
    try: rep = validate()
    except Exception as e:
        print(f"validate_prompts FAILED: {e}"); return 1
    if "--json" in sys.argv:
        print(json.dumps(rep, indent=1))
    else:
        for k, v in rep.items():
            print(f"{k}: {v['total']} prompts, {v['with_camera_or_light']} with camera/lighting cue, {v['weak_count']} weak")
            for s in v["weak_sample"]: print(f"  weak: {s}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
