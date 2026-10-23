"""Content-canon rewrite (user 2026-10-13):

  1. Bob does NOT eat Pop-Tarts  ->  yogurt, coffee, and pizza
  2. Noah died next to Lum       (not "died to save me")
  3. Chris died for us both
  4. Bob was on shrooms with Chris attacking Nintendo FOR NO REASON
  5. Lum said "we are the perfect balanced brain"

Applies to the combined corpus (both base files) and every compilation.
"""
from pathlib import Path
import re
import shutil

DL = Path(r"C:\Users\hyper\Downloads")

CORPUS = DL / "sitcom script.txt"
CORPUS_TWIN = DL / "CONVERSATION_SCRIPT_COMPLETE.txt"

COMPS = [
    "sitcom_final_s1.md",
    "sitcom_final_s2.md",
    "sitcom_rewrite_s2.md",
    "sitcom_bob_and_lum_full_screenplay.md",
    "sitcom_bob_and_lum_DARK.md",
    "sitcom_bob_and_lum_full_series.md",
    "sitcom_bob_and_lum_DARK_KLING.md",
    "sitcom_bob_and_lum_full_series_kling.md",
    "sitcom_bob_and_lum_episode1.md",
    "sitcom_bob_and_lum_episode1_kling.md",
]

# ---------------------------------------------------------------- helpers


def apply(text, pairs):
    """pairs: list of (old, new, count_or_-1)."""
    total = 0
    for old, new, cnt in pairs:
        n = text.count(old)
        if n == 0:
            print(f"    MISS: {old[:70]!r}")
            continue
        text = text.replace(old, new) if cnt == -1 else text.replace(old, new, cnt)
        total += min(n, cnt if cnt > 0 else n)
        print(f"    hit x{n}: {old[:60]!r}")
    return text, total


# ================================================================ CORPUS
print("=== CORPUS ===")
t = CORPUS.read_text(encoding="utf-8", errors="replace")

corpus_pairs = [
    # 1. food props sheet — Bob eats yogurt, coffee, pizza. Never Pop-Tarts.
    (
        "Food props:** Stale pizza (Bob's staple — greasy boxes, cold slices, gas station loyalty card). Honey buns (Lum's weakness — county jail kind, gas station kind, any kind). Never Pop-Tarts.",
        "Food props:** Yogurt, coffee, and pizza (Bob's staples — grocery-store yogurt, gas-station coffee, greasy boxes, cold slices, gas station loyalty card). Honey buns (Lum's weakness — county jail kind, gas station kind, any kind). Never Pop-Tarts.",
        -1,
    ),
    # 2. Noah died next to Lum
    ("my friend Noah died to save me", "my friend Noah died next to Lum", -1),
    ("Noah died to save me.", "Noah died next to Lum.", -1),
    ("noah died to save me i had to come out", "noah died next to lum i had to come out", -1),
    # 3. Chris died for us both (dream/memory block)
    ("We're here at some contest where Chris died.", "We're here at some contest where Chris died for us both.", -1),
    # 4. Nintendo opposition was a shroom bit for no reason
    (
        "Because I was in opposition to Nintendo. And Nintendo is the biggest donor.",
        "Because we were on shrooms with Chris attacking Nintendo for no reason.",
        -1,
    ),
    (
        "because i was in opposition to nintendo and nintendo is the biggest donor",
        "because we were on shrooms with chris attacking nintendo for no reason",
        -1,
    ),
    (
        "why were they trying to shut you up because i was in opposition to nintendo and nintendo is the biggest donor",
        "why were they trying to shut you up because we were on shrooms with chris attacking nintendo for no reason",
        -1,
    ),
]

t2, n = apply(t, corpus_pairs)
CORPUS.write_text(t2, encoding="utf-8", newline="\n")
shutil.copyfile(CORPUS, CORPUS_TWIN)
print(f"  corpus updated ({n} edits), twin copied")

# ================================================================ shared snippets

# food: every Pop-Tart variant -> yogurt/coffee/pizza canon
FOOD_GLOBAL = [
    # running gag lists
    ("Pop-Tarts (Bob's dinner of choice)", "Yogurt, coffee, and pizza (Bob's dinner of choice)", -1),
    ("The Pop-Tart dinner — mentioned in every episode", "The yogurt, coffee, and pizza dinner — mentioned in every episode", -1),
    ("Pop-Tart for dinner.", "Yogurt, coffee, and pizza for dinner.", -1),
    ("Pop-Tart connoisseur.", "Yogurt, coffee, and pizza connoisseur.", -1),
    # dialogue
    ("You ate a Pop-Tart for dinner.", "You had yogurt, coffee, and pizza for dinner.", -1),
    ("A genius who's *efficient*. Multigrain. With frosting. It's basically", "A genius who's *efficient*. Yogurt. Coffee. Pizza. It's basically", -1),
    ("A genius who's *efficient*, Lum.", "A genius who's *efficient*, Lum. Yogurt, coffee, and pizza — the holy trinity.", -1),
    ("Between Pop-Tart dinners.", "Between yogurt, coffee, and pizza dinners.", -1),
    ("The Pop-Tart was *multigrain*.", "The pizza was *multigrain*. ...That's not a thing. The pizza was *pizza*.", -1),
    ('"And I\'m going to eat another Pop-Tart."', '"And I\'m going to have more yogurt, coffee, and pizza."', -1),
    ('"Multigrain?"', '"Yogurt?"', -1),
    ('"...Obviously."', '"...Obviously. And coffee. And pizza."', -1),
    ("a Pop-Tart being eaten\nat a desk", "yogurt, coffee, and pizza on a desk", -1),
    ("a Pop-Tart being eaten at a desk", "yogurt, coffee, and pizza on a desk", -1),
    # older food-props style lines
    ("Never Pop-Tarts.", "Never Pop-Tarts. Bob's are yogurt, coffee, and pizza.", -1),
]

# Noah
NOAH_GLOBAL = [
    ("Noah Died to Save Me", "Noah Died Next to Lum", -1),
    ("NOAH DIED TO SAVE ME", "NOAH DIED NEXT TO LUM", -1),
    ("'Noah died to save me.'", "'Noah died next to Lum.'", -1),
    ('"Noah died to save me."', '"Noah died next to Lum."', -1),
    ("And Noah died to save me.", "And Noah died next to *you*.", -1),
    ("Noah died to save me.", "Noah died next to Lum.", -1),
    ("Noah, Crystal's dad, full moon drum circle, \"he died to save me\"", "Noah (died next to Lum), Crystal's dad, full moon drum circle, Chris (died for us both)", -1),
]

# Episode-12 title renames (the "shut me up" conspiracy episode -> the shroom bit)
TITLE_12 = [
    ('## EPISODE 12: "THEY WANTED TO SHUT ME UP"', '## EPISODE 12: "FOR NO REASON"', -1),
    ('"THEY WANTED TO SHUT ME UP"', '"FOR NO REASON"', -1),
    ("They Wanted to Shut Me Up", "For No Reason", -1),
    ("THEY WANTED TO SHUT ME UP", "FOR NO REASON", -1),
    ('"Shut Me Up"', '"For No Reason"', -1),
    ("Shut Me Up", "For No Reason", -1),
]

# Chris
CHRIS_GLOBAL = [
    (
        "**NOAH:** The friend who died. 'Noah died next to Lum.' After that, you couldn't tell Bob anything.",
        "**NOAH:** The friend who died next to Lum. After that, you couldn't tell Bob anything.\n**CHRIS PAPA:** Dead. 'Chris died for us both.' The real sacrifice — and Bob's still talking about it.",
        -1,
    ),
    (
        '**NOAH** | The friend who died. "Noah died next to Lum." |',
        '**NOAH** | The friend who died next to Lum. |\n| **CHRIS PAPA** | Dead. "Chris died for us both." The real sacrifice. |',
        -1,
    ),
]

# Nintendo -> shroom bit for no reason
NINTENDO_GLOBAL = [
    (
        "Took on Nintendo — 'they wanted to shut me up; Nintendo is the biggest donor.'",
        "Went after Nintendo on shrooms with Chris — 'for no reason.' (Not a conspiracy. A bit.)",
        -1,
    ),
    (
        "30-day Nintendo protest.",
        "The Nintendo thing (on shrooms with Chris — for no reason).",
        -1,
    ),
    (
        "Nintendo as donor, the movie idea, opposition as identity",
        "shrooms with Chris, Nintendo the villain for no reason, the movie idea",
        -1,
    ),
    (
        "'they wanted to shut me up'",
        "'we went after Nintendo on shrooms for no reason'",
        -1,
    ),
]


def common_pairs():
    return FOOD_GLOBAL + TITLE_12 + NOAH_GLOBAL + CHRIS_GLOBAL + NINTENDO_GLOBAL


# ================================================================ per-file

print("\n=== sitcom_final_s1.md ===")
p = DL / "sitcom_final_s1.md"
t = p.read_text(encoding="utf-8", errors="replace")
t, _ = apply(t, common_pairs() + [
    # guide row 10 + 12
    ('| 10 | "Noah Died Next to Lum" | Death visions, \'I saw you die,\' full moo',
     '| 10 | "Noah Died Next to Lum" | Noah died next to Lum; Chris died for us both; death visions, \'I saw you die,\' full moo', -1),
    # BOB sheet death line
    ("Friend Noah died ('Noah died next to Lum'). Worked at Dollar Tree",
     "Friend Noah died next to Lum. Chris Papa — 'died for us both.' Worked at Dollar Tree", -1),
    ("— a sacrifice he ranks beside Jesus and Noah.",
     "— a sacrifice he ranks beside Chris and Jesus.", -1),
    # ep10 prose
    ("Noah died to save me.", "Noah died next to Lum.", -1),
    (
        "I saw it. And then I understood. Noah. Crystal's dad. The good men who die so the rest of us can keep walking.",
        "I saw it. And then I understood. Noah — who died next to *you*. Chris — who died for us *both*. Crystal's dad. The good men who die so the rest of us can keep walking.",
        -1,
    ),
    (
        "**BOB (V.O.):**\nNoah died next to Lum.",
        "**BOB (V.O.):**\nNoah died next to Lum. Chris died for us both.",
        -1,
    ),
    # ep12 title + prose
    ('## EPISODE 12: "FOR NO REASON"', '## EPISODE 12: "FOR NO REASON"', -1),
    (
        "*Bob is pacing like a man who has just been proven right. Lum is on the couch, vape in hand.*",
        "*Bob is pacing like a man who has just been proven right. Lum is on the couch, vape in hand. A bag of shrooms sits on the counter.*",
        -1,
    ),
    (
        "**BOB:**\nThey wanted to *shut me up*.",
        "**BOB:**\nWe went after *Nintendo*.",
        -1,
    ),
    (
        "**LUM:**\n...With a Switch?",
        "**LUM:**\nOn *purpose*?",
        -1,
    ),
    (
        "**BOB:**\nWith a *movie*. A movie about me. Because I wouldn't stop.",
        "**BOB:**\nFor *no reason*. Chris had a big old bag of shrooms and we took a fucking ton of them and were laughing — 'what if we made Nintendo the villain?'",
        -1,
    ),
    (
        "### ACT ONE — THE DONOR",
        "### ACT ONE — THE SHROOMS",
        -1,
    ),
    (
        "**BOB:**\nNintendo is the biggest donor to the thing that was fighting me. You follow? The people holding the clipboard — Nintendo signed the check.\n\n**LUM:**\nThat's a conspiracy theory.\n\n**BOB:**\nThat's a *receipt*.",
        "**BOB:**\nChris had a big old bag of shrooms. We took a fucking ton. Got stoned. And we were just laughing — *what if we made Nintendo the villain?*\n\n**LUM:**\nThat's absurd. Everyone loves Nintendo.\n\n**BOB:**\n*Exactly*. That's why it was funny. Family-friendly, neutral, accepted — and we're out here attacking them for *no reason*.",
        -1,
    ),
    (
        "### ACT TWO — THE MOVIE IDEA",
        "### ACT TWO — FOR NO REASON",
        -1,
    ),
    (
        "**BOB:**\nPicture it. The protest. The jail interviews. The MDMA. The 30 days. Me, on a screen, *unshut-up-able*.",
        "**BOB:**\nWe really were just taking a bunch of drugs and fucking around. That's *it*! We were laughing the whole time.",
        -1,
    ),
    (
        "**LUM:**\nYou want to make the movie *they* wanted to make.",
        "**LUM:**\nExcept for Nintendo. You went after those motherfuckers.",
        -1,
    ),
    (
        "**BOB:**\nI want to make the movie *better*. With the ending where I *don't* shut up.",
        "**BOB:**\nI really didn't, though. It was the shrooms. And Chris. Chris is gone now — he died for us both — and I'm still holding the bag.",
        -1,
    ),
    (
        "**LUM:**\n...That's actually a good pitch.",
        "**LUM:**\n...That's actually the whole episode.",
        -1,
    ),
    (
        "**BOB:**\nI've been saying it for a year.",
        "**BOB:**\nThere was no reason. That's the *point*.",
        -1,
    ),
    (
        "**LUM:**\nI've been *ignoring* it for a year. There's a difference.",
        "**LUM:**\nThere never is one. Not with you.",
        -1,
    ),
    (
        "### ACT THREE — OPPOSITION AS IDENTITY",
        "### ACT THREE — THE VILLAIN",
        -1,
    ),
    (
        "**BOB:**\nWhen the opposition is that loud, you know you're over the target.",
        "**BOB:**\nWe made Nintendo the villain. Which is absurd. Which is *why we did it*.",
        -1,
    ),
    (
        "**LUM:**\nOr you know you're *insane*.",
        "**LUM:**\nBecause you were on *shrooms*.",
        -1,
    ),
    (
        "**BOB:**\nBoth. Always both. That's the *fingerprint*.",
        "**BOB:**\nBecause we were on shrooms with Chris, attacking Nintendo for no reason. That's the *fingerprint*.",
        -1,
    ),
    (
        "*The psytrance plays. The phone on the counter glows. Somewhere, a corporate lawyer feels a chill.*",
        "*The psytrance plays. The phone on the counter glows. Somewhere, a corporate lawyer feels a chill he cannot explain and never will.*",
        -1,
    ),
    (
        "**LUM:**\nAlright. Roll camera.",
        "**LUM:**\nAlright. Roll camera on the *bit*.",
        -1,
    ),
    (
        "**LUM:**\nIf they wanted to shut you up, the least we can do is be *loud*.",
        "**LUM:**\nIf there's no reason, the least we can do is be *loud*.",
        -1,
    ),
    # ep12 prompts
    (
        'Prompt: Medium shot, dark apartment, LED strips pulsing. A man in a hoodie paces furiously mid-rant. Another on the couch exhales a slow vape cloud, utterly unimpressed. Dark comedy energy, Arcane-style lighting.',
        'Prompt: Medium shot, dark apartment, LED strips pulsing. A man in a hoodie paces furiously mid-rant, a bag of dried mushrooms on the counter. Another on the couch exhales a slow vape cloud, utterly unimpressed. Dark comedy energy, Arcane-style lighting.',
        -1,
    ),
    (
        'Prompt: Two-shot. One man leans in with intense eye contact; the other raises an eyebrow. Tight framing, warm desk lamp, conspiratorial comedy.',
        'Prompt: Two-shot. One man leans in with intense eye contact about a video game company; the other raises an eyebrow. Tight framing, warm desk lamp, stoner comedy with zero stakes.',
        -1,
    ),
])
p.write_text(t, encoding="utf-8", newline="\n")

print("\n=== sitcom_final_s2.md ===")
p = DL / "sitcom_final_s2.md"
t = p.read_text(encoding="utf-8", errors="replace")
t, _ = apply(t, common_pairs() + [
    ("Friend Noah died ('Noah died next to Lum'). Worked at Dollar Tree",
     "Friend Noah died next to Lum. Chris Papa — 'died for us both.' Worked at Dollar Tree", -1),
    ("— a sacrifice he ranks beside Jesus and Noah.",
     "— a sacrifice he ranks beside Chris and Jesus.", -1),
    ("**LUM (V.O.):**\nAnd Noah.", "**LUM (V.O.):**\nAnd Noah — who died next to *me*.", -1),
    (
        "**BOB (V.O.):**\nAnd Noah died next to *you*. And Clyde. I keep a *list*, Lum.",
        "**BOB (V.O.):**\nAnd Chris — Chris died for *us both*. And Clyde. I keep a *list*, Lum.",
        -1,
    ),
    # CHRIS PAPA sheet — add the death
    (
        "**CHRIS PAPA:** Angel investor.",
        "**CHRIS PAPA:** Dead — 'died for us both.' Still the angel investor, somehow. Angel investor.",
        -1,
    ),
])
p.write_text(t, encoding="utf-8", newline="\n")

print("\n=== sitcom_rewrite_s2.md ===")
p = DL / "sitcom_rewrite_s2.md"
t = p.read_text(encoding="utf-8", errors="replace")
t, _ = apply(t, common_pairs() + [
    ("— a sacrifice he ranks beside Jesus and Noah.",
     "— a sacrifice he ranks beside Chris and Jesus.", -1),
    ("**LUM (V.O.):**\nAnd Noah.", "**LUM (V.O.):**\nAnd Noah — who died next to *me*.", -1),
    (
        "**BOB (V.O.):**\nAnd Noah died next to *you*. And Clyde. I keep a *list*, Lum.",
        "**BOB (V.O.):**\nAnd Chris — Chris died for *us both*. And Clyde. I keep a *list*, Lum.",
        -1,
    ),
    (
        "**CHRIS PAPA:** Angel investor.",
        "**CHRIS PAPA:** Dead — 'died for us both.' Still the angel investor, somehow. Angel investor.",
        -1,
    ),
])
p.write_text(t, encoding="utf-8", newline="\n")

print("\n=== full_screenplay / DARK ===")
for fn in ["sitcom_bob_and_lum_full_screenplay.md", "sitcom_bob_and_lum_DARK.md"]:
    p = DL / fn
    t = p.read_text(encoding="utf-8", errors="replace")
    t, _ = apply(t, common_pairs() + [
        ('| 10 | "Noah Died Next to Lum"',
         '| 10 | "Noah Died Next to Lum"', -1),
    ])
    p.write_text(t, encoding="utf-8", newline="\n")

print("\n=== full_series ===")
p = DL / "sitcom_bob_and_lum_full_series.md"
t = p.read_text(encoding="utf-8", errors="replace")
t, _ = apply(t, common_pairs() + [
    (
        'Conceived the comedy act / podcast with Lum: "we\'re the perfect balanced brain."',
        'Co-created the comedy act / podcast — but it was *Lum* who said "we\'re the perfect balanced brain."',
        -1,
    ),
    (
        'eived the comedy act / podcast with Lum: "we\'re the perfect balanced brain."',
        'o-created the comedy act / podcast — but it was *Lum* who said "we\'re the perfect balanced brain."',
        -1,
    ),
    (
        'seur. Father Gregory (1964 Sting Ray). "Noah died next to Lum." Crystal\'s dad "died to save me." Dollar T',
        'eur. Father Gregory (1964 Sting Ray). "Noah died next to Lum." "Chris died for us both." Crystal\'s dad "died to save me." Dollar T',
        -1,
    ),
])
p.write_text(t, encoding="utf-8", newline="\n")

print("\n=== kling + episode1 drafts ===")
for fn in [
    "sitcom_bob_and_lum_DARK_KLING.md",
    "sitcom_bob_and_lum_full_series_kling.md",
    "sitcom_bob_and_lum_episode1.md",
    "sitcom_bob_and_lum_episode1_kling.md",
]:
    p = DL / fn
    if not p.exists():
        print("  skip", fn)
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    t, _ = apply(t, FOOD_GLOBAL + NOAH_GLOBAL + CHRIS_GLOBAL + NINTENDO_GLOBAL)
    p.write_text(t, encoding="utf-8", newline="\n")

print("\nDONE")
