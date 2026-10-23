"""Rebuild combined conversation script with new unique sessions from transcribeme."""
import re, hashlib
from pathlib import Path
from collections import defaultdict

SRC = Path(r"C:\Users\hyper\Downloads\transcribeme")
EXISTING = Path(r"C:\Users\hyper\Downloads\sitcom script.txt")
OUT = Path(r"C:\Users\hyper\Downloads\sitcom script.txt")
OUT_COPY = Path(r"C:\Users\hyper\Downloads\CONVERSATION_SCRIPT_COMPLETE.txt")

# --- load existing combined ---
existing = EXISTING.read_text(encoding="utf-8", errors="replace")

# parse existing session names
headers = re.findall(r"^\[\d+\]\s+(.+)$", existing, re.M)
existing_names = []
for h in headers:
    m = re.match(r"\s*(.+?)\s{2,}", h)
    existing_names.append((m.group(1).strip() if m else h.strip()).lower())
existing_stems = {n.replace(".txt", "") for n in existing_names}

skip_re = re.compile(r"\(\d+\)|^(combined_|video_transcripts|transcripts|CONVERSATION|diff_new)")
candidates = [p for p in SRC.glob("*.txt") if not skip_re.search(p.name)]


def is_known(p: Path) -> bool:
    return p.name.strip().lower() in existing_names or p.stem.strip().lower() in existing_stems


# group by content hash
by_hash = defaultdict(list)
for p in candidates:
    by_hash[hashlib.md5(p.read_bytes()).hexdigest()].append(p)

# pick canonical alias: prefer dated YYYYMMDD names, then longer name
def canonical(files):
    dated = [f for f in files if re.match(r"\d{8}[_ ]\d{6}", f.name)]
    if dated:
        return sorted(dated, key=lambda f: f.name)[0]
    return sorted(files, key=lambda f: (-len(f.name), f.name))[0]


new_sessions = []
for h, files in by_hash.items():
    if any(is_known(f) for f in files):
        continue
    # skip empty / near-empty
    p = canonical(files)
    if p.stat().st_size < 20:
        continue
    # skip obvious non-conversation
    if "AnyDesk" in p.name or p.name.startswith("691444"):
        continue
    new_sessions.append(p)

# sort: named undated first (like original), then chronological by name
def sort_key(p: Path):
    name = p.name
    m = re.match(r"(\d{8})[_ ](\d{6})", name)
    if m:
        return (1, m.group(1), m.group(2), name)
    m2 = re.match(r"IMG[_ ]?(\d+)", name, re.I)
    if m2:
        return (2, m2.group(1).zfill(6), "000000", name)
    # Audio / Voice dated
    m3 = re.search(r"(\d{6})[_ ]?(\d{6})", name)
    if m3:
        return (1, m3.group(1), m3.group(2), name)
    return (0, "", "", name)


new_sessions.sort(key=sort_key)

print(f"Appending {len(new_sessions)} new unique sessions")

# --- cleaning ---
TS = re.compile(
    r"\b\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?\b|\b\d+\s*(?:minutes?|seconds?)\b|\b\d+\s+seconds?\b",
    re.I,
)
SPEAKER_LINE = re.compile(r"^(Speaker\s*\d+|Bob|Lum|Rob)\s*$", re.I)
SPEAKER_INLINE = re.compile(r"^(Speaker\s*\d+|Bob|Lum|Rob)\s*[:\-]\s*", re.I)
MUSIC = re.compile(r"\*music\*|\[music\]|\(music\)", re.I)


def clean_text(raw: str) -> str:
    lines = raw.splitlines()
    out = []
    for line in lines:
        line = line.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
        line = line.replace("\u2014", " - ").replace("\u2013", "-")
        line = MUSIC.sub("", line)
        line = TS.sub("", line)
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        # collapse long ASR loops: same token repeated 4+
        line = re.sub(r"\b(\w+)(?:\s+\1){3,}\b", r"\1", line, flags=re.I)
        out.append(line)
    return out


def map_speakers(lines, text_blob: str):
    """Return lines with Speaker N rewritten to Bob/Lum when confident."""
    # name cues
    # if someone is addressed as Bob/Rob, the OTHER is the addressee's partner
    # heuristic from earlier work + new material:
    # default: Speaker 1 = Bob, Speaker 2 = Lum  (will override with cues)
    mapping = {"1": "Bob", "2": "Lum", "3": "Speaker 3", "4": "Speaker 4"}

    # cue: "Bob:" or "Lum:" or "Rob:" already present
    if re.search(r"\bLum\b", text_blob) and not re.search(r"\bBob\b", text_blob):
        pass

    # address cues: "Bob," said by one speaker
    # find "you Bob" / "Bob" in Speaker 2 lines -> Speaker 1 is Bob
    # simpler: if text contains "I'm Robert" / "I'm Bob" near Speaker 1, keep mapping
    # flip if Speaker 2 addresses Bob/Rob
    sp2_text = []
    sp1_text = []
    cur = None
    for ln in lines:
        m = re.match(r"^(Speaker\s*(\d+)|Bob|Lum|Rob)\s*$", ln, re.I)
        if m:
            cur = m.group(2) if m.group(2) else m.group(1)
            continue
        if cur == "1":
            sp1_text.append(ln)
        elif cur == "2":
            sp2_text.append(ln)
    sp1 = " ".join(sp1_text)
    sp2 = " ".join(sp2_text)
    if re.search(r"\b(?:Bob|Rob|Robert)\b", sp2, re.I) and not re.search(r"\b(?:Bob|Rob|Robert)\b", sp1, re.I):
        # Speaker 2 addresses Bob -> Speaker 1 is Bob (keep default)
        pass
    if re.search(r"\b(?:Bob|Rob|Robert)\b", sp1, re.I) and not re.search(r"\b(?:Bob|Rob|Robert)\b", sp2, re.I):
        # Speaker 1 talks about Bob in third person or is Lum addressing... ambiguous
        # if "you Bob" pattern
        if re.search(r"\byou\s+(?:Bob|Rob)\b", sp1, re.I):
            mapping = {"1": "Lum", "2": "Bob", "3": "Speaker 3", "4": "Speaker 4"}

    out = []
    for ln in lines:
        m = re.match(r"^Speaker\s*(\d+)\s*$", ln, re.I)
        if m:
            n = m.group(1)
            out.append(mapping.get(n, f"Speaker {n}"))
            continue
        out.append(ln)
    return out


def render_session(idx: int, p: Path) -> str:
    raw = p.read_text(encoding="utf-8", errors="replace")
    lines = clean_text(raw)
    lines = map_speakers(lines, raw)

    # convert "Name" standalone + next line into "Name: text" lightly keep screenplay style
    # Keep original style of combined: "Bob: text" paragraphs
    # If file is Speaker-label style, join label + text as "Name: text"
    body = []
    speaker = None
    buf = []
    def flush():
        nonlocal speaker, buf
        if speaker and buf:
            body.append(f"{speaker}: {' '.join(buf)}".strip())
        elif buf:
            body.append(" ".join(buf))
        buf = []

    for ln in lines:
        m = re.match(r"^(Bob|Lum|Rob|Speaker\s*\d+)\s*$", ln, re.I)
        if m:
            flush()
            name = m.group(1)
            if name.lower() == "rob":
                name = "Bob"
            speaker = name
            continue
        m2 = re.match(r"^(Bob|Lum|Rob|Speaker\s*\d+)\s*:\s*(.*)$", ln, re.I)
        if m2:
            flush()
            name = m2.group(1)
            if name.lower() == "rob":
                name = "Bob"
            speaker = name
            if m2.group(2).strip():
                buf = [m2.group(2).strip()]
            continue
        buf.append(ln)
    flush()

    # date estimate from name
    date = ""
    m = re.match(r"(\d{4})(\d{2})(\d{2})", p.name)
    if m:
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", p.name)
    if m:
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if not date:
        # Voice 260921 -> 2026-09-21
        m = re.search(r"(\d{2})(\d{2})(\d{2})", p.name)
        if m and m.group(1) == "26":
            date = f"20{m.group(1)}-{m.group(2)}-{m.group(3)}"
        elif re.match(r"IMG", p.name, re.I):
            date = p.stem
        elif re.match(r"Audio_(\d{2})_(\d{2})_(\d{4})", p.name):
            mm = re.match(r"Audio_(\d{2})_(\d{2})_(\d{4})", p.name)
            date = f"{mm.group(3)}-{mm.group(1)}-{mm.group(2)}"
        else:
            date = p.stem

    header = (
        f"\n{'='*78}\n"
        f"[{idx}]  {p.name}   —   {date}\n"
        f"{'='*78}\n"
    )
    return header + "\n\n".join(body) + "\n"


# find next index
nums = [int(x) for x in re.findall(r"^\[(\d+)\]", existing, re.M)]
next_i = max(nums) + 1 if nums else 1

parts = [existing.rstrip() + "\n"]
for p in new_sessions:
    parts.append(render_session(next_i, p))
    next_i += 1

new_doc = "".join(parts)

# update header generation note
new_doc = new_doc.replace(
    "Generated: 2026-10-02 15:26:52",
    "Generated: 2026-10-02 15:26:52\nUpdated:   2026-10-12 (added new unique sessions from transcribeme)",
    1,
)

OUT.write_text(new_doc, encoding="utf-8")
OUT_COPY.write_text(new_doc, encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
print(f"Wrote {OUT_COPY} ({OUT_COPY.stat().st_size} bytes)")
print(f"Total sessions now: {next_i - 1}")
