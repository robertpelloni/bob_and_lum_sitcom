"""Canon pass 3 — remaining Pop-Tarts in full_screenplay.md."""
from pathlib import Path

p = Path(r"C:\Users\hyper\Downloads\sitcom_bob_and_lum_full_screenplay.md")
t = p.read_text(encoding="utf-8", errors="replace")
pairs = [
    ("You ate a Pop-Tart for dinner and stayed up until 4 AM",
     "You had yogurt, coffee, and pizza for dinner and stayed up until 4 AM", -1),
    ("And I'm going to eat another Pop-Tart.",
     "And I'm going to have more yogurt, coffee, and pizza.", -1),
    ("Multigrain?", "Yogurt?", -1),
    ("...Obviously.", "...Obviously. And coffee. And pizza.", -1),
    ("Would you like me to order more Pop-Tarts?",
     "Would you like me to order more yogurt, coffee, and pizza?", -1),
    ("Between Pop-Tarts.", "Between yogurt, coffee, and pizza.", -1),
    ("A single Pop-Tart wrapper.", "A single yogurt cup and a pizza crust.", -1),
    ("*(gesturing at the Pop-Tart wrapper)*", "*(gesturing at the yogurt cup)*", -1),
    ("Coding bugs, friendship, Pop-Tarts",
     "Coding bugs, friendship, yogurt/coffee/pizza", -1),
    ('- **Pop-Tarts** — "It\'s basically a salad"',
     '- **Yogurt, coffee, and pizza** — Bob\'s dinner of choice. Never Pop-Tarts.', -1),
]
for old, new, _ in pairs:
    n = t.count(old)
    print(f"  {'hit' if n else 'MISS'} x{n}: {old[:70]!r}")
    t = t.replace(old, new)
p.write_text(t, encoding="utf-8", newline="\n")
print("done")
