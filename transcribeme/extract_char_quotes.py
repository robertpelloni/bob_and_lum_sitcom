import re
from pathlib import Path

src = Path(r"C:\Users\hyper\Downloads\transcribeme")
files = [
    "Voice 260921_211718.txt", "Voice 260925_000559.txt", "Voice 260927_125841.txt",
    "Voice 260924_214139.txt", "Voice 260927_205538.txt", "Voice 260927_192903.txt",
    "Voice 260925_224321.txt", "Voice 260926_235812.txt", "Voice 260922_041035.txt",
    "Voice 260921_194705.txt", "Voice 260929_002617.txt",
    "20260927 114201.txt", "20260926 060009.txt", "20260924 221451.txt",
    "Great Lakes 5.txt", "Great Lakes 19.txt", "Great Lakes 11.txt",
    "20260929 190812.txt", "20260927 191700.txt", "20260927 185126.txt",
    "Naylor St.txt", "20260930_213859.txt", "20260908_201139.txt",
    "Bob Lum Starting the journey September full moon.txt",
    "Saint clair river record owner night Bob Lum.txt",
    "corvette chat.txt", "Lockwood Of Clinton 2.txt", "New Recording.txt",
    "20260927 210727.txt", "20260925 231154.txt",
]
pattern = re.compile(
    r".{0,80}(?:Dollar Tree|olive oil|Nintendo|DDR|foreclosure|Shonna|jail|prison|"
    r"Camaro|Corvette|Gregory|my dad|my father|I saw you|died|frequencies|"
    r"full moon|Christ|K-hole|StarTAC|burner|comedy|skit|sitcom|Harry|Agathi|Cliff).{0,120}",
    re.I,
)
for f in files:
    p = src / f
    if not p.exists():
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    hits = [m.group(0).strip().replace("\n", " ") for m in pattern.finditer(t)]
    seen = set()
    uniq = []
    for h in hits:
        k = h[:80]
        if k not in seen:
            seen.add(k)
            uniq.append(h)
    if uniq:
        print(f"\n===== {f} ({len(uniq)} hits) =====")
        for h in uniq[:10]:
            print(" -", h[:240])
