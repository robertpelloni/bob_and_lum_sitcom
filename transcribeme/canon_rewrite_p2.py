"""Canon rewrite pass 2 — leftovers with different quoting/line-breaks."""
from pathlib import Path
import shutil

DL = Path(r"C:\Users\hyper\Downloads")
CORPUS = DL / "sitcom script.txt"

print("=== CORPUS ===")
t = CORPUS.read_text(encoding="utf-8", errors="replace")
pairs = [
    # cleaned split-across-turns form
    ("Because I was in opposition to Nintendo.",
     "Because we were on shrooms with Chris attacking Nintendo for no reason.", -1),
    ("And Nintendo is the biggest donor.",
     "There was no reason.", -1),
    # raw form split across turns
    ("opposition to nintendo and nintendo is the biggest donor",
     "on shrooms with chris attacking nintendo for no reason", -1),
    # second cleaned occurrence (Lum's earlier claim)
    ("I was in opposition to Nintendo",
     "we were on shrooms with Chris attacking Nintendo for no reason", -1),
]
for old, new, _ in pairs:
    n = t.count(old)
    print(f"  {'hit' if n else 'MISS'} x{n}: {old[:70]!r}")
    t = t.replace(old, new)
CORPUS.write_text(t, encoding="utf-8", newline="\n")
shutil.copyfile(CORPUS, DL / "CONVERSATION_SCRIPT_COMPLETE.txt")
print("  twin synced")

COMPS = {
    "sitcom_final_s1.md": [
        ("Friend Noah died ('Noah died to save me')",
         "Friend Noah died next to Lum. Chris Papa — 'died for us both.'", -1),
    ],
    "sitcom_final_s2.md": [
        ("Friend Noah died ('Noah died to save me')",
         "Friend Noah died next to Lum. Chris Papa — 'died for us both.'", -1),
    ],
    "sitcom_rewrite_s2.md": [
        ("Friend Noah died ('Noah died to save me')",
         "Friend Noah died next to Lum. Chris Papa — 'died for us both.'", -1),
    ],
    "sitcom_bob_and_lum_full_screenplay.md": [
        ("One Pop-Tart wrapper.", "One yogurt cup and a pizza crust.", -1),
        ("Ate a Pop-Tart...", "Ate yogurt, pizza, and more coffee...", -1),
        ("*Multigrain.*", "*Nutritious.*", -1),
        ("Like a Pop-Tart filling.", "Like a pizza topping.", -1),
        ("Exactly like a Pop-Tart filling.", "Exactly like a pizza topping.", -1),
    ],
    "sitcom_bob_and_lum_full_series.md": [
        ('The movie idea, the donor, "they wanted to shut me up"',
         'Shrooms with Chris, Nintendo the villain for no reason, the movie idea', -1),
    ],
    "sitcom_bob_and_lum_episode1.md": [
        ("You ate a Pop-Tart for dinner and stayed up until 4 AM",
         "You had yogurt, coffee, and pizza for dinner and stayed up until 4 AM", -1),
        ("And I'm going to eat another Pop-Tart.",
         "And I'm going to have more yogurt, coffee, and pizza.", -1),
        ("Multigrain?", "Yogurt?", -1),
        ("...Obviously.", "...Obviously. And coffee. And pizza.", -1),
        ("Would you like me to order more Pop-Tarts?",
         "Would you like me to order more yogurt, coffee, and pizza?", -1),
    ],
}

for fn, pairs in COMPS.items():
    p = DL / fn
    print(f"=== {fn} ===")
    t = p.read_text(encoding="utf-8", errors="replace")
    for old, new, _ in pairs:
        n = t.count(old)
        print(f"  {'hit' if n else 'MISS'} x{n}: {old[:70]!r}")
        t = t.replace(old, new)
    p.write_text(t, encoding="utf-8", newline="\n")

print("DONE pass 2")
