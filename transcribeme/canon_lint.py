#!/usr/bin/env python3
"""Canon lint gate: fail on known canon violations in sitcom screenplays.

Rules (from MEMORY.md, verified manually 2026-11-08, automated 2026-11-13):
 1. Pop-Tarts lines must be negations (Bob NEVER eats Pop-Tarts).
 2. Speaker/name slips: bare 'Rob:' or 'Lung' (never Rob/Lung for BOB/LUM).
 3. Noah conflation: 'Noah died to save/for me/us' (Noah died NEXT TO Lum;
    Chris died for both - that phrasing belongs to Chris).
Scans sitcom*.md at repo root only (docs quoting violations are excluded).
Usage: python transcribeme/canon_lint.py  (exit 1 on any violation)
"""
import re, sys
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parent.parent

def check_text(text, name=""):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if "pop-tart" in line.lower() and not re.search(r"never|not |no pop|n't", line, re.I):
            out.append(f"{name}:{i}: Pop-Tarts without negation: {line.strip()[:100]}")
        if re.match(r"^\s*(Rob|Lung)\s*:", line):
            out.append(f"{name}:{i}: bad speaker label (use BOB/LUM): {line.strip()[:100]}")
        if re.search(r"Noah died (to save|for (me|us|Bob|Lum))", line, re.I):
            out.append(f"{name}:{i}: Noah conflation (Noah died next to Lum): {line.strip()[:100]}")
    return out

def check_repo(root=None):
    root = root or REPO_ROOT
    out = []
    for p in sorted(root.glob("sitcom*.md")):
        out += check_text(p.read_text(encoding="utf-8", errors="replace"), p.name)
    return out

def main():
    errs = check_repo()
    if errs:
        print(f"canon-lint FAILED ({len(errs)}):"); [print("  " + e) for e in errs]; return 1
    print("canon-lint OK: no Pop-Tarts/Rob/Lung/Noah violations in sitcom*.md")
    return 0

if __name__ == "__main__":
    sys.exit(main())
