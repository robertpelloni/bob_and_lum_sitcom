"""Update character definitions and episode guides in sitcom_final_s1.md and sitcom_final_s2.md."""
from pathlib import Path

DL = Path(r"C:\Users\hyper\Downloads")

# --- shared additions ---
BOB_ADD = (
    " Father is Gregory — restored a 1964 Corvette Sting Ray by hand from barn-find to award-winner at shows; "
    "Air Force vet; took Bob hunting as a kid; won't talk about Papu's business that was supposed to be his. "
    "Friend Noah died ('Noah died to save me'). "
    "Worked at Dollar Tree about five months at $13.75/hr to help Shauna pay credit cards and utilities. "
    "Took on Nintendo — 'they wanted to shut me up; Nintendo is the biggest donor.' "
    "'God is using me as an adapter.' Christos / Christianity deep-dives. "
    "Full moon drum circles, frequencies, dancing as cure. "
    "Built bob's game, Hyper Beam arcade, the Omni-Workspace and the bob- stack; fueled by 174 BPM DnB and psytrance."
)

# insert before the closing catchphrase
def patch_bob(text: str) -> str:
    old = "The man contains multitudes — most of them contradictory."
    old2 = "The man contains multitudes â€” most of them contradictory."
    # try both encodings of em dash
    for o in (old, old2, "The man contains multitudes"):
        if o in text and BOB_ADD.strip() not in text:
            if o == "The man contains multitudes":
                text = text.replace(
                    "The man contains multitudes",
                    BOB_ADD.strip() + " The man contains multitudes",
                    1,
                )
            else:
                text = text.replace(o, BOB_ADD.strip() + " " + o, 1)
            break
    return text


HARRY_ADD = (
    " Real name in the transcripts: Halalambos — father Christos. "
    "Grew up inside the same family storm as Bob and Agathi; jail, street, and loyalty are native languages. "
    "'I would die for him' runs both ways."
)


def patch_harry(text: str) -> str:
    marker = "Sends game show ideas at 2 AM."
    if marker in text and "Halalambos — father Christos" not in text and "Halalambos" not in text.split("HARRY", 1)[-1][:2000]:
        # append after the Harry paragraph's last sentence before AGATHI
        text = text.replace(
            "The most devout criminal you'll ever meet.",
            "The most devout criminal you'll ever meet." + HARRY_ADD,
            1,
        )
    return text


AGATHI_ADD = (
    " In the raw transcripts she is Agathy — family, not a third party; Bob's protective instinct names her beside Harry."
)


def patch_agathi(text: str) -> str:
    if "Will roast everyone equally." in text and "Agathy" not in text:
        text = text.replace(
            "Will roast everyone equally.",
            "Will roast everyone equally." + AGATHI_ADD,
            1,
        )
    return text


NEW_CAST = """
**GREGORY (Bob's father):** Quiet force. Barn-find 1964 Corvette Sting Ray restored by hand to show-winner condition — bought in his 20s, stored as junk for much of Bob's childhood, then brought back to life. Air Force. Hunting trips, deer meat, 'that's what my dad always used to tell me.' Christmas can go stiff and defensive. Won't talk about Papu's business. The kind of father who starts by taking comfort away — then hands you the keys.

**SHAUNA / SHONNA:** The foreclosure on one end, the apartment and the credit-card bills on the other. Bob's plan to make her financially secure is the quiet engine under half his bad decisions.

**NOAH:** The friend who died. 'Noah died to save me.' After that, you couldn't tell Bob anything.

**HANK (Hank Davis):** Family-or-work gravity. Same name as every workplace Hank. Christmas gifts. A patriot, like Harry and the dads.

**CHRISTINA:** Old orbit. Dominic wanted her. Brooke worked with her at Boston's. The past that still texts back.

**MAMA SHARON:** Aunt who died. Grief filed under 'I'm sorry, I'm very sorry.'

"""


def inject_new_cast(text: str, anchor_line_prefix: str) -> str:
    """Insert NEW_CAST after THE PHONE sheet if not present."""
    if "GREGORY (Bob's father)" in text:
        return text
    # find THE PHONE paragraph and insert after it
    key = "**THE PHONE:**"
    idx = text.find(key)
    if idx < 0:
        return text
    # end of that line
    eol = text.find("\n", idx)
    if eol < 0:
        eol = len(text)
    return text[: eol + 1] + NEW_CAST + text[eol + 1 :]


# --- episode guide updates ---
S1_GUIDE_OLD = """| 8 | "The Supernova" | The vision, the void, "the track is the only thing keeping the void at bay" | ALL SOURCE MATERIAL |"""

S1_GUIDE_NEW = """| 8 | "The Supernova" | The vision, the void, "the track is the only thing keeping the void at bay" | ALL SOURCE MATERIAL |
| 9 | "The Sting Ray" | Gregory's 1964 Corvette, barn-find resurrection, Air Force silence, Papu's business, hunting with Dad | corvette chat + Great Lakes 5 + 20260930_213859 |
| 10 | "Noah Died to Save Me" | Death visions, 'I saw you die,' full moon drum circle, frequencies, Up Dog Yoga | Great Lakes 5 + Great Lakes 19 + Bob Lum September full moon + Voice 260925 |
| 11 | "Dollar Tree, Baby" | $13.75/hr, Shauna's bills, the model that puts you in jail, five months of quiet heroism | Voice 260927_192903 + 20260927 191700 + 20260926 060009 + Great Lakes 11 |
| 12 | "They Wanted to Shut Me Up" | Nintendo as donor, the movie idea, MDMA jail interviews, opposition as identity | Naylor St + 20260927 210727 + Voice 260927_205538 |"""


def patch_s1_guide(text: str) -> str:
    if "The Sting Ray" in text:
        return text
    return text.replace(S1_GUIDE_OLD, S1_GUIDE_NEW, 1)


S2_GUIDE_OLD = """| BONUS | "The Sanctified Repository Redemption" | Harry, the car heist, Romans 8:28, God compiles redemption from chaos | Harry + theological musings |"""

S2_GUIDE_NEW = """| BONUS | "The Sanctified Repository Redemption" | Harry, the car heist, Romans 8:28, God compiles redemption from chaos | Harry + theological musings |
| BONUS 2 | "Christos and Halalambos" | Father names, Christos = anointed one, Papu, the lineage under the jokes | Voice 260925_224321 + 20260925 231154 + Voice 260921_194705 |
| BONUS 3 | "The Adapter" | 'God is using me as an adapter,' Nintendo protest, corporations vs the people, Hannibal Lecter government | Voice 260921_211718 + 20260927 114201 |
| BONUS 4 | "Army of Holograms" | AI agents, Muse/Ava faces, virtual employees, building the company of ghosts | Voice 260927_125841 |"""


def patch_s2_guide(text: str) -> str:
    if "Christos and Halalambos" in text:
        return text
    return text.replace(S2_GUIDE_OLD, S2_GUIDE_NEW, 1)


# --- run ---
s1_path = DL / "sitcom_final_s1.md"
s2_path = DL / "sitcom_final_s2.md"

s1 = s1_path.read_text(encoding="utf-8", errors="replace")
s2 = s2_path.read_text(encoding="utf-8", errors="replace")

s1 = patch_bob(s1)
s1 = inject_new_cast(s1, "**THE PHONE:**")
s1 = patch_s1_guide(s1)
# also add header note
if "Updated from new transcripts" not in s1:
    s1 = s1.replace(
        "Based on 134 transcript sessions (2025-02-25 to 2026-09-22)",
        "Based on 243 transcript sessions (2025-02-25 to 2026-10-02) — updated from new transcripts (transcribeme batch: Voice memos, Great Lakes / Bread and Roses / M-53 road sessions, Naylor St, Saint Clair, corvette chat)",
        1,
    )

s2 = patch_bob(s2)
s2 = patch_harry(s2)
s2 = patch_agathi(s2)
s2 = inject_new_cast(s2, "**THE PHONE:**")
s2 = patch_s2_guide(s2)
if "Updated from new transcripts" not in s2:
    s2 = s2.replace(
        "### Sequel to Season 1: \"The Dark Cut\"",
        "### Sequel to Season 1: \"The Dark Cut\"\n<!-- Updated from new transcripts: Voice memos + road sessions + corvette chat (Gregory / 1964 Sting Ray) -->",
        1,
    )

s1_path.write_text(s1, encoding="utf-8")
s2_path.write_text(s2, encoding="utf-8")
print("Updated", s1_path, s1_path.stat().st_size)
print("Updated", s2_path, s2_path.stat().st_size)
print("Bob add in S1:", "1964 Corvette" in s1)
print("Gregory in S1:", "GREGORY" in s1)
print("S1 new eps:", "The Sting Ray" in s1)
print("Harry patch S2:", "Halalambos" in s2 and "father Christos" in s2)
print("S2 new bonus:", "Christos and Halalambos" in s2)
