"""Update full_series.md season bible with new cast and episode rows."""
from pathlib import Path

p = Path(r"C:\Users\hyper\Downloads\sitcom_bob_and_lum_full_series.md")
t = p.read_text(encoding="utf-8", errors="replace")

old_bob = '| **BOB** (Robert Pelloni) | 42, Detroit-born solo developer and "tech polymath." Intense, fast-talking, prone to grandiose declarations and sudden vulnerability. Wears the same hoodie. Has lived multiple lives — from addiction and jail to building AI companies. Pop-Tart connoisseur. |'
new_bob = '| **BOB** (Robert Pelloni) | 43, Detroit-born solo developer and "tech polymath." Intense, fast-talking, prone to grandiose declarations and sudden vulnerability. Wears the same hoodie. Has lived multiple lives — from addiction and jail to building AI companies. Pop-Tart connoisseur. Father Gregory (1964 Sting Ray). "Noah died to save me." Crystal\'s dad "died to save me." Dollar Tree five months for Shonna\'s bills. Took on Nintendo. "God is using me as an adapter." Conceived the comedy act / podcast with Lum: "we\'re the perfect balanced brain." |'
if old_bob in t:
    t = t.replace(old_bob, new_bob, 1)
    print("bob row updated")
else:
    print("bob row NOT matched")

old_lum = '| **LUM** | Bob\'s best friend and creative partner. Calm, dry-witted counterweight. The one who says "I know" when Bob says "The dashboard is broken." Carries his own heavy history but processes it through humor. |'
new_lum = '| **LUM** | Bob\'s best friend and creative partner. Calm, dry-witted counterweight. The one who says "I know" when Bob says "The dashboard is broken." Carries his own heavy history but processes it through humor. Korean mother + Greek father. Post-iPhone era: gas station burner phones and StarTAC flips, USB flash drives to the library for music. Owns the creative-left half of "the perfect balanced brain." |'
if old_lum in t:
    t = t.replace(old_lum, new_lum, 1)
    print("lum row updated")
else:
    print("lum row NOT matched")

if new_lum in t and "**GREGORY**" not in t:
    extra = (
        "\n| **GREGORY** | Bob's father. Barn-find 1964 Corvette Sting Ray restored by hand to show-winner. Air Force. Hunting trips. Won't talk about Papu's business. |"
        "\n| **SHONNA** | Foreclosure on one end, credit-card bills on the other. Bob's quiet engine. |"
        "\n| **NOAH** | The friend who died. \"Noah died to save me.\" |"
        "\n| **CRYSTAL** | Childhood orbit at 13-14. Alcoholic father whose sacrifice \"saved\" Bob. |"
        "\n| **HARRY** | Street-tech specialist. Real name Halalambos — father Christos. \"Step on the Tongue of the Devil.\" The membrane that keeps Bob and Lum honest. |"
        "\n| **AGATHI** | Family. Greek fire via video call. Deeply protective of Lum. |"
    )
    t = t.replace(new_lum, new_lum + extra, 1)
    print("extra cast added")

old_row8 = '| 8 | "The Dashboard Is Broken Again" | Philosophy, consciousness, meaning | God, enlightenment, simulation theory, purpose, being a "genius" |'
new_rows = old_row8 + (
    '\n| 9 | "The Sting Ray" | Fathers, restoration, silence | Gregory, the 1964 Corvette, Air Force, hunting, Papu\'s business |'
    '\n| 10 | "Noah Died to Save Me" | Sacrifice, death visions, frequencies | Noah, Crystal\'s dad, full moon drum circle, "he died to save me" |'
    '\n| 11 | "Dollar Tree, Baby" | Work, love, quiet heroism | $13.75/hr, Shonna\'s bills, five months, the model that puts you in jail |'
    '\n| 12 | "They Wanted to Shut Me Up" | Opposition, Nintendo, identity | The movie idea, the donor, "they wanted to shut me up" |'
    '\n| 13 | "The Fingerprint" | Comedy, partnership, meta | The act conceived on tape, "perfect balanced brain," the podcast that is this show |'
    '\n| 14 | "From a Box" | Technology ancestry | Blackberry, flip phones, emulator handhelds, downloading goes extinct |'
)
if old_row8 in t and "The Fingerprint" not in t:
    t = t.replace(old_row8, new_rows, 1)
    print("arc rows added")
else:
    print("arc row8 skip:", "Fingerprint" in t, old_row8 in t)

t = t.replace(
    "Based on 8,323 turns of real conversation",
    "Based on 246 transcript sessions (updated 2026-10-13)",
    1,
)

p.write_text(t, encoding="utf-8")
print("full_series.md ->", len(t))
