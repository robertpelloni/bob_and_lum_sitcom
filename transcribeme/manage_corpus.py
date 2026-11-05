#!/usr/bin/env python3
"""Unified CLI tool to manage and verify the Bob & Lum sitcom corpus and pipeline.

Provides commands for:
  - --check: Validates byte equality between master transcripts, checks session count and headers.
  - --build-html: Re-renders the WordPress HTML viewer from canonical text.
  - --stats: Outputs corpus metrics (sessions, line counts, character counts).
"""
import argparse
import hashlib
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_FILE = REPO_ROOT / "CONVERSATION_SCRIPT_COMPLETE.txt"
SITCOM_FILE = REPO_ROOT / "sitcom script.txt"
HTML_FILE = REPO_ROOT / "CONVERSATION_SCRIPT_COMPLETE.wordpress.html"


def file_checksum(path: Path) -> str:
    if not path.exists():
        return ""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def check_corpus_integrity() -> bool:
    print("=== Checking Bob & Lum Corpus Integrity ===")
    errors = []

    if not MASTER_FILE.exists():
        errors.append(f"Missing master file: {MASTER_FILE}")
    if not SITCOM_FILE.exists():
        errors.append(f"Missing sitcom file: {SITCOM_FILE}")

    if MASTER_FILE.exists() and SITCOM_FILE.exists():
        m_hash = file_checksum(MASTER_FILE)
        s_hash = file_checksum(SITCOM_FILE)
        m_size = MASTER_FILE.stat().st_size
        s_size = SITCOM_FILE.stat().st_size

        print(f"Master file: {MASTER_FILE.name} ({m_size:,} bytes, sha256: {m_hash[:12]}...)")
        print(f"Sitcom file: {SITCOM_FILE.name} ({s_size:,} bytes, sha256: {s_hash[:12]}...)")

        if m_hash != s_hash:
            errors.append("Checksum mismatch between CONVERSATION_SCRIPT_COMPLETE.txt and sitcom script.txt!")
        else:
            print("✓ Master and sitcom files are byte-identical.")

        # Header and session checks
        content = MASTER_FILE.read_text(encoding="utf-8", errors="replace")
        sessions = re.findall(r"^\[(\d+)\]\s+(.+)$", content, re.M)
        print(f"✓ Found {len(sessions)} registered session headers.")
        if sessions:
            first_idx = int(sessions[0][0])
            last_idx = int(sessions[-1][0])
            print(f"✓ Session index range: [{first_idx}] to [{last_idx}]")

    if HTML_FILE.exists():
        print(f"✓ HTML reader present: {HTML_FILE.name} ({HTML_FILE.stat().st_size:,} bytes)")
    else:
        errors.append("HTML reader file missing! Run with --build-html to generate.")

    if errors:
        print("\nIntegrity Check FAILED with errors:")
        for err in errors:
            print(f"  ❌ {err}")
        return False

    print("\n✓ All corpus integrity checks passed successfully.")
    return True


def print_stats():
    print("=== Bob & Lum Corpus Statistics ===")
    if not MASTER_FILE.exists():
        print(f"File not found: {MASTER_FILE}")
        return

    content = MASTER_FILE.read_text(encoding="utf-8", errors="replace")
    lines = content.splitlines()
    sessions = re.findall(r"^\[\d+\]\s+.+$", content, re.M)

    bob_cues = len(re.findall(r"^Bob:\s+", content, re.M))
    lum_cues = len(re.findall(r"^Lum:\s+", content, re.M))
    speaker_cues = len(re.findall(r"^Speaker\s*\d+:\s+", content, re.M))

    print(f"Total Bytes:       {len(content.encode('utf-8')):,}")
    print(f"Total Lines:       {len(lines):,}")
    print(f"Total Sessions:    {len(sessions):,}")
    print(f"Bob Dialog Cues:   {bob_cues:,}")
    print(f"Lum Dialog Cues:   {lum_cues:,}")
    print(f"Generic Speakers:  {speaker_cues:,}")


def build_html():
    print("=== Regenerating WordPress HTML Viewer ===")
    import subprocess
    regen_script = REPO_ROOT / "transcribeme" / "regen_wordpress_html.py"
    if not regen_script.exists():
        print(f"Error: {regen_script} not found!")
        sys.exit(1)
    res = subprocess.run([sys.executable, str(regen_script)], check=True)
    if res.returncode == 0:
        print("✓ Successfully regenerated HTML.")


def main():
    parser = argparse.ArgumentParser(description="Manage Bob & Lum sitcom corpus.")
    parser.add_argument("--check", action="store_true", help="Run corpus integrity checks.")
    parser.add_argument("--build-html", action="store_true", help="Regenerate HTML viewer.")
    parser.add_argument("--stats", action="store_true", help="Show corpus statistics.")

    args = parser.parse_args()

    if not (args.check or args.build_html or args.stats):
        # Default behavior: run checks and print stats
        ok = check_corpus_integrity()
        print()
        print_stats()
        sys.exit(0 if ok else 1)

    if args.check:
        ok = check_corpus_integrity()
        if not ok:
            sys.exit(1)
    if args.build_html:
        build_html()
    if args.stats:
        print_stats()


if __name__ == "__main__":
    main()
