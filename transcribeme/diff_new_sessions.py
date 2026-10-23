import re, hashlib
from pathlib import Path
from collections import defaultdict

src = Path(r"C:\Users\hyper\Downloads\transcribeme")
combined = Path(r"C:\Users\hyper\Downloads\sitcom script.txt").read_text(encoding="utf-8", errors="replace")

headers = re.findall(r"^\[\d+\]\s+(.+)$", combined, re.M)
names = []
for h in headers:
    m = re.match(r"\s*(.+?)\s{2,}", h)
    names.append((m.group(1).strip() if m else h.strip()))

comb_norm = {n.strip().lower() for n in names}
comb_stem = {n.strip().lower().replace(".txt", "") for n in names}

skip_re = re.compile(r"\(\d+\)|^(combined_|video_transcripts|transcripts|CONVERSATION|diff_new)")
candidates = [p for p in src.glob("*.txt") if not skip_re.search(p.name)]

def is_in_combined(p):
    name = p.name.strip().lower()
    stem = p.stem.strip().lower()
    return name in comb_norm or stem in comb_stem

# hash unique content
by_hash = defaultdict(list)
for p in candidates:
    data = p.read_bytes()
    h = hashlib.md5(data).hexdigest()
    by_hash[h].append(p)

# unique new content groups
new_groups = []
old_groups = []
for h, files in by_hash.items():
    # if ANY alias is in combined, treat as known
    if any(is_in_combined(f) for f in files):
        old_groups.append((h, files))
    else:
        new_groups.append((h, files))

print(f"Unique content hashes total: {len(by_hash)}")
print(f"Already in combined: {len(old_groups)}")
print(f"NEW unique content: {len(new_groups)}")

# sort by size
new_groups.sort(key=lambda x: x[1][0].stat().st_size, reverse=True)

print("\n=== NEW UNIQUE SESSIONS ===")
total = 0
for h, files in new_groups:
    size = files[0].stat().st_size
    total += size
    aliases = " | ".join(f.name for f in files)
    print(f"{size:8d}  {aliases}")

print(f"\nTotal unique new bytes: {total}")

# also list audio/video without txt
print("\n=== MEDIA WITHOUT TXT (possible untranscribed) ===")
media = []
for p in list(src.glob("*.m4a")) + list(src.glob("*.mp3")) + list(src.glob("*.mp4")) + list(src.glob("*.mov")) + list(src.glob("*.MOV")):
    stem = p.stem
    # check if a txt exists
    txts = list(src.glob(stem + "*.txt")) + list(src.glob(stem + ".txt"))
    if not txts:
        media.append(p)
for p in sorted(media, key=lambda x: x.name):
    print(f"{p.stat().st_size:8d}  {p.name}")
