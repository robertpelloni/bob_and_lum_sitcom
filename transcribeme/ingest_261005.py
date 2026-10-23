"""Ingest Voice 261005_224228.txt (show-conception tape) as session 247.

Reuses deep_clean_rebuild cleaning. Also collapses the long "So, let's go." tail loop
before the normal pipeline so it cannot bloat the buffer.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, r"C:\Users\hyper\Downloads\transcribeme")
from deep_clean_rebuild import deep_clean_text, render_session, OUT, OUT_COPY

SRC = Path(r"C:\Users\hyper\Downloads\transcribeme\Voice 261005_224228.txt")

# Speaker cues: S1 says "Bob and I are going to be characters" -> Lum.
# S2/S3 co-pitch the same episode idea (diarization split) -> Bob.
# S4 addresses Bob ("Trauma... bob") -> Lum.
SMAP = {"1": "Lum", "2": "Bob", "3": "Bob", "4": "Lum"}


def pre_clean(raw: str) -> str:
    # collapse the enormous "So, let's go." / "let's go" tail loop to one
    raw = re.sub(r"(?:\bSo,?\s*)?(?:let's go\.?\s*){6,}", "So, let's go. ", raw, flags=re.I)
    # collapse "thank you" repeats
    raw = re.sub(r"(Thank you\.\s*){3,}", "Thank you. ", raw, flags=re.I)
    return raw


def main():
    existing = OUT.read_text(encoding="utf-8", errors="replace")
    if "Voice 261005_224228.txt" in existing:
        print("already ingested")
        return

    raw = pre_clean(SRC.read_text(encoding="utf-8", errors="replace"))
    tmp = SRC.parent / "_tmp_261005_preclean.txt"
    tmp.write_text(raw, encoding="utf-8")

    nums = [int(x) for x in re.findall(r"^\[(\d+)\]", existing, re.M)]
    idx = max(nums) + 1 if nums else 1

    rendered = render_session(idx, tmp, SMAP)
    tmp.unlink(missing_ok=True)
    # fix header filename/date to the real source
    rendered = rendered.replace(tmp.name, SRC.name)
    rendered = rendered.replace(f"—   {tmp.stem}", "—   2026-10-05")

    new_doc = existing.rstrip() + "\n" + rendered
    new_doc = new_doc.replace(
        "Updated:   2026-10-13 (deep-cleaned Voice 261001/261003 + October skit; speakers assigned; ASR loops/punct/name canon)",
        "Updated:   2026-10-13 (deep-cleaned Voice 261001/261003/261005 + October skit; speakers assigned; ASR loops/punct/name canon)",
        1,
    )
    OUT.write_text(new_doc, encoding="utf-8")
    OUT_COPY.write_text(new_doc, encoding="utf-8")
    print(f"[{idx}] Voice 261005_224228.txt rendered {len(rendered)} chars")
    print(f"Total sessions now: {idx}")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
