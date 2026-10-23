"""Patch character sheets in sitcom finals + rewrite with new transcript facts."""
from pathlib import Path
import re

DL = Path(r"C:\Users\hyper\Downloads")

BOB_ADD = (
    " Late-discovered voice: Lum's pitch that Bob is the analytical right brain and Lum the creative left — "
    "'we're the perfect balanced brain' — with Harry as the membrane that keeps it honest; the two of them "
    "conceive a comedy act / podcast on tape ('in our each bob and lum's fingerprint in this life kind of way'). "
    "Also solves the riddle of Crystal's alcoholic dad — 'was such a good man that he died to save me' — "
    "a sacrifice he ranks beside Jesus and Noah. Grew up around Crystal and Kim at 13-14; knew his sexuality "
    "young. Blackberry-to-flip-phone dream sequence lives in his head. Handheld emulator (SNES, N64, PlayStation, PS2) "
    "for 1990s games. Company pitch discipline: 'explain it in less than five minutes… explain it in 20 seconds.'"
)

LUM_ADD = (
    " Conceived the comedy act and the podcast format on tape with Bob; owns the creative-left half of "
    "'the perfect balanced brain.' Proved he can hold a room — 'I never thought I could do that… I feel like "
    "I could do it when I\'m with you.' Blackberry / flip-phone / 'we started from a box' tech-ancestry monologues; "
    "Harry gave him the songs. Pushes the Shonna safety-net plan: guardrails, professionals, monitoring from a distance."
)

CRYSTAL_SHEET = (
    "**CRYSTAL:** Childhood orbit. Bob knew her at 13-14. Alcoholic father — a good man whose sacrifice "
    "'saved' Bob in Bob's own theology ('Crystal's alcoholic dad. Was such a good man. That he died to save me'). "
    "The relationship was a trap Bob couldn't admit to leaving — 'I didn't want to marry her, but you represented that.' "
    "Her name is one of the passwords in Bob's origin myth, next to Noah and Clyde.\n"
)

SHONNA_ADD = (
    " The October tapes deepen her arc: Bob invested seven years; Lum's plan is a professional safety net "
    "— guardrails, in-home help, monitoring from a distance — so Bob and Lum can build the business while "
    "she is actually supported, not babysat."
)


def patch_file(path: Path, add_bonus_rows: str = "", insert_before: str = "", episodes_md: str = ""):
    t = path.read_text(encoding="utf-8", errors="replace")
    orig = t

    # Bob sheet: insert addendum before the final period of the Bob paragraph if not already patched
    if "perfect balanced brain" not in t:
        t = re.sub(
            r"(\*\*BOB \(Robert Pelloni\):\*\*.*?)(\n\n)",
            lambda m: m.group(1) + BOB_ADD + m.group(2),
            t,
            count=1,
            flags=re.S,
        )

    if "perfect balanced brain" not in t.split("**LUM")[1][:3000] if "**LUM" in t else True:
        t = re.sub(
            r"(\*\*LUM \(Lumbros Korlous\):\*\*.*?)(\n\n)",
            lambda m: m.group(1) + LUM_ADD + m.group(2),
            t,
            count=1,
            flags=re.S,
        )

    if "**CRYSTAL:**" not in t:
        # insert Crystal sheet after Noah sheet (or before THE PHONE / end of sheets)
        if "**NOAH:**" in t:
            t = re.sub(
                r"(\*\*NOAH:\*\*[^\n]*\n)",
                r"\1" + CRYSTAL_SHEET,
                t,
                count=1,
            )
        else:
            t = re.sub(
                r"(\*\*THE PHONE:\*\*)",
                CRYSTAL_SHEET + r"\1",
                t,
                count=1,
            )

    if "seven years; Lum's plan" not in t and "**SHONNA:**" in t:
        t = re.sub(
            r"(\*\*SHONNA:\*\*[^\n]*)",
            r"\1" + SHONNA_ADD,
            t,
            count=1,
        )

    if add_bonus_rows and "The Fingerprint" not in t:
        # add rows to episode guide table (before the closing --- of the guide)
        t = re.sub(
            r"(\| BONUS 4 \|[^\n]*\n)",
            r"\1" + add_bonus_rows,
            t,
            count=1,
        )
        # if no bonus 4, append after last table row
        if "The Fingerprint" not in t:
            t = re.sub(
                r"(\| 12 \|[^\n]*\n)",
                r"\1" + add_bonus_rows,
                t,
                count=1,
            )

    if episodes_md and insert_before and insert_before in t:
        t = t.replace(insert_before, episodes_md + "\n" + insert_before, 1)

    if t != orig:
        path.write_text(t, encoding="utf-8")
        print(f"patched {path.name} ({len(t)} bytes)")
    else:
        print(f"no change {path.name}")


def main():
    # --- S1 ---
    s1 = DL / "sitcom_final_s1.md"
    patch_file(s1)

    # --- S2 ---
    s2 = DL / "sitcom_final_s2.md"
    bonus_rows_s2 = (
        "| BONUS 5 | \"The Fingerprint\" | The comedy act conceived on tape — Bob the analytical right brain, "
        "Lum the creative left, Harry the membrane; 'we're the perfect balanced brain'; the podcast that is really "
        "this sitcom | October Bob & Lum comedy skit conception + Voice 261001 |\n"
        "| BONUS 6 | \"Crystal's Dad\" | The alcoholic father who 'died to save me'; Crystal and Kim at 13-14; "
        "the sacrifice theology; Noah, Clyde, and the men who die so Bob can live | Voice 261001 + Voice 261003 |\n"
        "| BONUS 7 | \"From a Box\" | Blackberry, flip phones, 'we started from a box'; emulator handhelds and "
        "1998 PlayStation games; downloading goes extinct; Lum's post-iPhone ancestry | Voice 261001 + Voice 261003 |\n"
    )
    patch_file(s2, add_bonus_rows=bonus_rows_s2)

    # --- rewrite s2 ---
    rw = DL / "sitcom_rewrite_s2.md"
    patch_file(rw, add_bonus_rows=bonus_rows_s2)

    print("character sheet pass done")


if __name__ == "__main__":
    main()
