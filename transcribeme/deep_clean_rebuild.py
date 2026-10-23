"""Deep-clean the three new transcripts, assign speakers, append to combined corpus.

Cleans: word/phrase ASR loops, missing punctuation, capitalization, name canon,
inline Speaker fragments, doubled function words. Speakers mapped per-file
from self-ID and address cues.
"""
import re
import hashlib
from pathlib import Path

SRC = Path(r"C:\Users\hyper\Downloads\transcribeme")
OUT = Path(r"C:\Users\hyper\Downloads\sitcom script.txt")
OUT_COPY = Path(r"C:\Users\hyper\Downloads\CONVERSATION_SCRIPT_COMPLETE.txt")

# Per-file speaker maps from self-ID / address cues.
# October: S2 addresses Bob ("How are we gonna do it, Bob?") -> S2=Lum; S1=Bob;
#          S4 refers to Bob in 3rd person ("Harry more than Bob") -> S4=Lum (split); S3=Bob (tiny fragments).
# 261001:  S1 self-IDs ("I'm Lum. He's Bob.") -> S1=Lum; S4 addresses Bob -> S4=Lum; S2/S3=Bob.
# 261003:  S1 lists Bob's sites ("bob tournamentnexus.site") as self -> S1=Bob;
#          S3 dominant philosophical/God/AI takes (Bob's "adapter" material) -> S3=Bob;
#          S2/S4 question-challenge mode -> Lum.
SPEAKER_MAPS = {
    "October Bob & Lum comedy skit conception were Bob realizes.txt": {
        "1": "Bob", "2": "Lum", "3": "Bob", "4": "Lum",
    },
    "Voice 261001_214337.txt": {
        "1": "Lum", "2": "Bob", "3": "Bob", "4": "Lum",
    },
    "Voice 261003_225020.txt": {
        "1": "Bob", "2": "Lum", "3": "Bob", "4": "Lum",
    },
}

TARGETS = list(SPEAKER_MAPS.keys())

# Name canon + common ASR errors (applied as whole words).
WORD_FIXES = [
    (r"\bLung\b", "Lum"),
    (r"\blung\b", "Lum"),
    (r"\bRob\b", "Bob"),
    (r"\brob\b", "Bob"),
    (r"\bRobert\b", "Bob"),  # only when not "Robert Pelloni" — handled below
    (r"\bShauna\b", "Shonna"),
    (r"\bshauna\b", "Shonna"),
    (r"\bShawna\b", "Shonna"),
    (r"\bAgathy\b", "Agathi"),
    (r"\bAgathie\b", "Agathi"),
    (r"\bChris Papua\b", "Chris Papa"),
    (r"\bPapua\b", "Papa"),
    (r"\bHalalambos\b", "Haralombrose"),
    (r"\bHalalambrose\b", "Haralombrose"),
    (r"\bChristos\b", "Christos"),  # keep
]

MUSIC = re.compile(r"\*music\*|\[music\]|\(music\)", re.I)
TS = re.compile(
    r"\b\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?\b|\b\d+\s*(?:minutes?|seconds?)\b",
    re.I,
)
# Inline broken speaker remnant mid-line ("saker 1", leftover "Speaker 4" mid-text)
INLINE_SP = re.compile(r"(?<![A-Za-z])saker\s*\d+", re.I)


def collapse_repeats(line: str) -> str:
    """Collapse ASR stutter loops while keeping natural doubles."""
    # phrase repeats 3+ ("if it's what, if it's what, if it's what")
    prev = None
    while prev != line:
        prev = line
        line = re.sub(
            r"\b(.{5,40}?)(?:,\s*|\s+)\1(?:,\s*|\s+)\1\b",
            r"\1",
            line,
            flags=re.I,
        )
    # word repeats 3+ ("art art art art") -> single
    line = re.sub(r"\b(\w+)(?:\s+\1){2,}\b", r"\1", line, flags=re.I)
    # doubled function words ("the the", "and and") -> single
    line = re.sub(
        r"\b(the|and|is|to|of|a|in|it|that|you|I|we|they|so|but|or|for|on|with|this|was|are|be|do|does|did|have|has|had|at|as|if|then|than|from|by|not|no|yes|yeah|ok|okay)\s+\1\b",
        r"\1",
        line,
        flags=re.I,
    )
    # "no no no no" / "yeah yeah yeah" chains -> two
    line = re.sub(r"\b([Nn]o|[Yy]eah|[Oo]k(?:ay)?)(?:[,\s]+\1){3,}", r"\1, \1", line)
    # comma stutter "There's a, there's a, there's like" handled by phrase pass
    # repeated "like like"
    line = re.sub(r"\b([Ll]ike)\s+\1\b", r"\1", line)
    # "that that" "what what" mild doubles -> one (ASR noise)
    line = re.sub(r"\b(that|what|when|where|which|who|how|there|here|then|this)\s+\1\b", r"\1", line, flags=re.I)
    return line


def fix_punct_and_caps(line: str) -> str:
    """Restore basic punctuation and capitalization."""
    line = line.replace(" ", " ")
    # standalone i -> I
    line = re.sub(r"\bi\b", "I", line)
    # capitalize after sentence end
    def cap(m):
        return m.group(1) + m.group(2).upper()

    line = re.sub(r"([.!?]\s+)([a-z])", cap, line)
    # capitalize start
    if line and line[0].islower():
        line = line[0].upper() + line[1:]
    # collapse space before punctuation
    line = re.sub(r"\s+([.,!?;:])", r"\1", line)
    # missing space after punctuation
    line = re.sub(r"([.,!?;:])([A-Za-z])", r"\1 \2", line)
    # curly quotes already normalized upstream
    return line


def add_terminal_punct(line: str) -> str:
    if not line:
        return line
    if line[-1] not in ".!?,;:\")'":
        # question heuristics
        if re.search(r"\b(what|who|where|when|why|how|is|are|do|does|did|can|could|would|will|should|have|has)\b", line[:24], re.I) and "?" not in line and len(line) < 80:
            return line + "?"
        return line + "."
    return line


def deep_clean_text(raw: str) -> list[str]:
    lines = raw.splitlines()
    out = []
    for line in lines:
        line = line.replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')
        line = line.replace("\u2014", " - ").replace("\u2013", "-")
        line = MUSIC.sub("", line)
        line = TS.sub("", line)
        line = INLINE_SP.sub("", line)
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        line = collapse_repeats(line)
        for pat, rep in WORD_FIXES:
            if pat == r"\bRobert\b":
                # keep "Robert Pelloni", replace bare Robert
                line = re.sub(r"\bRobert\b(?! Pelloni)", "Bob", line)
                continue
            line = re.sub(pat, rep, line)
        line = fix_punct_and_caps(line)
        # skip pure speaker labels here — handled in render
        if re.match(r"^Speaker\s*\d+$", line, re.I):
            out.append(line)
            continue
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line:
            continue
        out.append(line)
    return out


def render_session(idx: int, p: Path, smap: dict) -> str:
    raw = p.read_text(encoding="utf-8", errors="replace")
    lines = deep_clean_text(raw)

    body = []
    speaker = None
    buf: list[str] = []

    def flush():
        nonlocal speaker, buf
        if speaker and buf:
            text = " ".join(buf)
            text = collapse_repeats(text)
            text = fix_punct_and_caps(text)
            text = add_terminal_punct(text)
            body.append(f"{speaker}: {text}")
        elif buf:
            text = fix_punct_and_caps(" ".join(buf))
            text = add_terminal_punct(text)
            body.append(text)
        buf = []

    for ln in lines:
        m = re.match(r"^Speaker\s*(\d+)\s*$", ln, re.I)
        if m:
            flush()
            speaker = smap.get(m.group(1), f"Speaker {m.group(1)}")
            continue
        m2 = re.match(r"^(Bob|Lum|Rob|Speaker\s*\d+)\s*:\s*(.*)$", ln, re.I)
        if m2:
            flush()
            name = m2.group(1)
            if name.lower() == "rob":
                name = "Bob"
            if re.match(r"Speaker", name, re.I):
                n = re.search(r"\d+", name).group(0)
                name = smap.get(n, f"Speaker {n}")
            speaker = name
            if m2.group(2).strip():
                buf = [m2.group(2).strip()]
            continue
        # stray "saker N" already stripped; accumulate
        buf.append(ln)
    flush()

    # drop consecutive identical speaker labels with empty; merge same-speaker runs
    merged = []
    for item in body:
        if merged:
            m1 = re.match(r"^(Bob|Lum|Speaker \d+): (.*)$", merged[-1], re.S)
            m2 = re.match(r"^(Bob|Lum|Speaker \d+): (.*)$", item, re.S)
            if m1 and m2 and m1.group(1) == m2.group(1):
                merged[-1] = f"{m1.group(1)}: {m1.group(2)} {m2.group(2)}"
                continue
        merged.append(item)

    date = ""
    m = re.match(r"(\d{4})(\d{2})(\d{2})", p.name)
    if m:
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", p.name)
    if m:
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    if not date:
        m = re.search(r"(\d{6})[_ ]?(\d{6})", p.name)
        if m and m.group(1).startswith("26"):
            date = f"2026-{m.group(1)[2:4]}-{m.group(1)[4:6]}"
        elif "October" in p.name:
            date = "2026-10"
        else:
            date = p.stem

    header = (
        f"\n{'=' * 78}\n"
        f"[{idx}]  {p.name}   —   {date}\n"
        f"{'=' * 78}\n"
    )
    return header + "\n\n".join(merged) + "\n"


def main():
    existing = OUT.read_text(encoding="utf-8", errors="replace")
    headers = re.findall(r"^\[\d+\]\s+(.+)$", existing, re.M)
    existing_names = set()
    for h in headers:
        m = re.match(r"\s*(.+?)\s{2,}", h)
        existing_names.add((m.group(1).strip() if m else h.strip()).lower())
    existing_stems = {n.replace(".txt", "") for n in existing_names}

    # also hash-set of existing bodies so we don't re-add a rename
    existing_hashes = set()
    # parse sessions roughly by header
    chunks = re.split(r"^\[\d+\]", existing, flags=re.M)[1:]
    for ch in chunks:
        body = ch.split("\n", 2)[-1]
        existing_hashes.add(hashlib.md5(body.encode("utf-8", "replace")).hexdigest())

    nums = [int(x) for x in re.findall(r"^\[(\d+)\]", existing, re.M)]
    next_i = max(nums) + 1 if nums else 1

    added = []
    parts = [existing.rstrip() + "\n"]
    for name in TARGETS:
        p = SRC / name
        if not p.exists():
            print(f"MISSING {name}")
            continue
        if name.lower() in existing_names or p.stem.lower() in existing_stems:
            print(f"SKIP already present: {name}")
            continue
        rendered = render_session(next_i, p, SPEAKER_MAPS[name])
        # skip if empty-ish
        if len(rendered) < 80:
            print(f"SKIP empty: {name}")
            continue
        parts.append(rendered)
        added.append((next_i, name, len(rendered)))
        next_i += 1

    new_doc = "".join(parts)
    # bump header note
    if "Updated:   2026-10-12" in new_doc:
        new_doc = new_doc.replace(
            "Updated:   2026-10-12 (added new unique sessions from transcribeme)",
            "Updated:   2026-10-13 (deep-cleaned Voice 261001/261003 + October skit; speakers assigned; ASR loops/punct/name canon)",
            1,
        )
    elif "Updated:" not in new_doc[:2000]:
        new_doc = new_doc.replace(
            "Generated: 2026-10-02 15:26:52",
            "Generated: 2026-10-02 15:26:52\nUpdated:   2026-10-13 (deep-cleaned new transcripts; speakers assigned)",
            1,
        )

    OUT.write_text(new_doc, encoding="utf-8")
    OUT_COPY.write_text(new_doc, encoding="utf-8")
    print(f"Added {len(added)} sessions:")
    for i, n, sz in added:
        print(f"  [{i}] {n} ({sz} chars rendered)")
    print(f"Total sessions now: {next_i - 1}")
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
    print(f"Wrote {OUT_COPY} ({OUT_COPY.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
