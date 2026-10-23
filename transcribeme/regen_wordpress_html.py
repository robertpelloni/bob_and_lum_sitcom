"""Regenerate CONVERSATION_SCRIPT_COMPLETE.wordpress.html from the combined corpus."""
import html
from pathlib import Path

SRC = Path(r"C:\Users\hyper\Downloads\sitcom script.txt")
OUT = Path(r"C:\Users\hyper\Downloads\CONVERSATION_SCRIPT_COMPLETE.wordpress.html")

text = SRC.read_text(encoding="utf-8", errors="replace")

parts = []
parts.append("<b>COMPLETE CONVERSATION SCRIPT</b>\n")
parts.append(
    "<p>Speakers: Robert Pelloni (Bob) &mdash; Lum<br>\n"
    "Ambiguous / undated sessions first, then chronological.<br>\n"
    "Updated: 2026-10-13 &mdash; 246 sessions; deep-cleaned Voice 261001/261003 + October skit; "
    "speakers assigned; ASR loops / punctuation / name canon.</p>\n"
)

import re

# split sessions on the ===== header blocks
chunks = re.split(r"\n(?===+\n+\[\d+\])", text)
header_written = False
for ch in chunks:
    ch = ch.strip("\n")
    if not ch.strip():
        continue
    # first chunk may include the doc header before first session
    if not re.search(r"^\[\d+\]", ch, re.M):
        continue
    lines = ch.splitlines()
    # header lines until first blank after title
    title = ""
    body_start = 0
    for i, ln in enumerate(lines):
        if re.match(r"^\[\d+\]", ln):
            title = ln
            body_start = i + 1
            break
    # skip the === underlines
    while body_start < len(lines) and set(lines[body_start].strip()) <= {"=", "-"}:
        body_start += 1
    body = "\n".join(lines[body_start:])
    t_esc = html.escape(title)
    b_esc = html.escape(body)
    # paragraphs
    b_esc = b_esc.replace("\n\n", "<br><br>\n")
    b_esc = b_esc.replace("\n", "<br>\n")
    parts.append(f"<b>{t_esc}</b>\n")
    parts.append(f"<p>{b_esc}</p>\n")

OUT.write_text("".join(parts), encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
