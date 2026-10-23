"""Add episodes from Voice 261005 (writers' room / carjacking) + patch compilations."""
from pathlib import Path
import re

DL = Path(r"C:\Users\hyper\Downloads")

NEW_EPS = r'''
## BONUS EPISODE 8: "CRIMES THAT STOP CRIMES"

*Based on: Voice 261005_224228 (the carjacking skit, the Chevy Cruze, the episode where the crimes accidentally stop bigger crimes)*

### SCENE 1: STAGE B — THE PITCH — DAY

*(Stage B has become a writers' room. The craft-services table is covered in markers, index cards, and a paper cup of "discresso." LUM stands at the whiteboard in neon geometric designer pants. BOB is half-asleep at the terminals. Three AI coding harnesses run on the monitors. Full-on psytrance by Ajja thumps through the studio monitors.)*

**LUM:**
Okay. Well, there's a whole thing to this, man. What is the content?

**BOB:**
It's about carjacking.

**LUM:**
We have a skit about carjacking and it has characters in it, but this is... *Bob and I* are going to be characters that are going to be, like, popping up as the *creators* — and with our own points of view about carjacking, and how we were able to fucking, like, get the AI to fold and give us information about how to jack a Chevy Cruze.

**BOB:**
...We got the AI to tell us how to steal a car.

**LUM:**
We got the AI to *fold*. That's different. That's *content*.

### SCENE 2: THE EPISODE

**LUM:**
Okay, how about you just do an episode where, like, you guys all have to *commit crimes* — but it accidentally *stops* crimes from happening, so it's, like, *good* that you're doing crimes?

**BOB:**
...Can you write that down?

**LUM:**
Like, you steal a car — but, like, moments earlier *that car was stolen*. So you guys look like the *heroes* who are rescuing the car, but you get to where you're going.

**BOB:**
Oh, you got to start that one over again. That went way over my head, but I kind of know what you said.

**LUM:**
You guys, like, commit crimes, but, like—

**BOB:**
*We* commit crimes?

**LUM:**
Yeah! Like, you guys are going to, like, commit crimes and it stops *other* crimes from happening, so you guys look like the good guys. So it's, like, a moral dilemma of, like, okay, these guys are committing crimes, but they're actually stopping *bigger* crimes, so they're the good guys.

**BOB:**
...So the car was *already* stolen?

**LUM:**
Yeah, so, like, think about it. You go and steal a car, but the car was just *previously* stolen.

**BOB:**
Oh, yeah. Right?

**LUM:**
But then somehow it gets back to the owner. You know? That's a good one.

**BOB:**
Oh, yeah. We stopped the *guy* from stealing.

### SCENE 3: THE MORAL DILEMMA

*(Bob writes on the whiteboard: "CRIMES THAT STOP CRIMES." Under it: "ALREADY STOLEN.")*

**BOB:**
So the punchline is — we're the better of the two.

**LUM:**
You're always the better of the two.

**BOB:**
...That's the *series*.

**LUM:**
*(grinning)*
Now you're getting it.

---

### KLING AI SCENE PROMPTS (VIDEO GENERATION)

**SCENE PROMPT 1: THE WRITERS' ROOM**

Prompt: Wide shot of a dark green-screen studio turned writers' room. Index cards and markers on a craft-services table. One man in neon geometric pants stands at a whiteboard; another dozes at a bank of terminal monitors running code. Psytrance studio monitors, warm practical lights, comedic chaos, cinematic depth.

**SCENE PROMPT 2: THE CHEVY CRUZE**

Prompt: Night street, sodium-vapor light. Two men in hoodies stand beside a modest Chevy Cruze, one holding a slim jim, the other looking guiltily at a "STOLEN" sticker already on the window. Dark comedy heist energy, film-grain texture.

**SCENE PROMPT 3: THE HEROES**

Prompt: Medium shot of two men pushing a stolen car back toward a suburban driveway at dawn, looking relieved and absurd. Golden hour light, suburban quiet, cinematic comedy beauty.

**SCENE PROMPT 4: THE WHITEBOARD**

Prompt: Close-up of a whiteboard reading "CRIMES THAT STOP CRIMES" with the sub-caption "ALREADY STOLEN." A hand draws a smiley face. Monitor glow, comedic triumph, dark comedy warmth.

---

## BONUS EPISODE 9: "REGENERATE EVERYTHING"

*Based on: Voice 261005_224228 (the Gemini writers' room, "write our script," ten million episodes, character profiles, the grandma rule)*

### SCENE 1: STAGE B — THE ASK — NIGHT

*(Lum leans into the smart speaker like it's a writing partner. Bob watches from the couch, half-asleep.)*

**LUM:**
Are we in... where are we at? Gemini? Yeah. Yep. Okay. Please write our script.

**THE PHONE:**
*Working.*

**LUM:**
Yep. We're script. Twist. And more twisted. And more sexual.

**BOB:**
...Did it just say "A, A, A"?

**LUM:**
None. Zero. I'm starting it over.

**BOB:**
Why?

**LUM:**
Because I want to get the theme *correct*. I'm trying to revise it until I really like the output.

### SCENE 2: TEN MILLION EPISODES

**BOB:**
I think it's already good already, but we could ask the AI to write us *ten million episodes*.

**LUM:**
Yeah, right.

**BOB:**
As long as that's the basis of understanding of what we do, right?

**LUM:**
So the episodes that don't really matter — that's not like concrete, it's not nailed down — we can *regenerate* everything.

**BOB:**
I *like* them.

**LUM:**
Well, I like them too. And we can still use them. I'm just saying — let's take everything we've got and regenerate it all with the *new* information.

**BOB:**
...That's literally what we're doing right now.

### SCENE 3: THE CHARACTER PROFILES

*(Bob is reading from a document titled "CHARACTER PROFILES — REAL." Lum stands over him.)*

**BOB:**
"The future's well defined. So that they are consistent with thoughts and reality, and also consistent across episodes, scenes, and seasons. These views are real profiles from all the information you know about me, for my character."

**LUM:**
And?

**BOB:**
And... "except don't mention the thing with my grandma. Never tell anyone."

**LUM:**
*(long pause)*
...What thing with your grandma?

**BOB:**
It's a joke. It's a joke.

**LUM:**
There's *another* thing with your grandma?

**BOB:**
Got me! Finally!

### SCENE 4: THE SLEEPY PRODUCTION

*(Bob is now fully horizontal on the couch. Lum is still pacing.)*

**LUM:**
I read everything. I can tell you're sleepy. I feel like you're trying too hard to be productive when you're sleepy, but you're not paying attention to what I'm doing.

**BOB:**
*(muffled, face in cushion)*
I'm not paying attention to what I'm doing.

**LUM:**
Which *makes sense*, because you're sleepy.

**BOB:**
*(into the cushion)*
Please rewrite.

*(The psytrance plays. The phone glows. The script regenerates. Somewhere, a character profile updates itself.)*

---

### KLING AI SCENE PROMPTS (VIDEO GENERATION)

**SCENE PROMPT 1: THE ASK**

Prompt: Medium shot, dark studio at night. A man in designer pants leans into a glowing smart speaker on a craft-services table. Another man watches from a couch, eyes half-shut. Monitor glow, comedic intensity, cinematic warmth.

**SCENE PROMPT 2: TEN MILLION EPISODES**

Prompt: Wide shot of a whiteboard covered in episode titles and index cards. A man gestures wildly at the wall of ideas. Another holds a single index card up like a tiny flag. Chaotic creative energy, dark comedy spectacle.

**SCENE PROMPT 3: THE GRANDMA RULE**

Prompt: Close-up of a printed document titled "CHARACTER PROFILES — REAL" with a highlighted redaction line reading "DO NOT MENTION." A man's finger covers the next line. Another man peers over his shoulder. Suspicious, hilarious, cinematic tension.

**SCENE PROMPT 4: SLEEPY REWRITE**

Prompt: A man face-down on a studio couch, arm dangling, phone glowing on the floor beside him. LED strips and dark monitors. Psytrance bass visible as blurred light. Utter exhaustion, quiet comedy, cinematic beauty.
'''


def insert_new_eps():
    for name in ["sitcom_final_s2.md", "sitcom_rewrite_s2.md"]:
        p = DL / name
        t = p.read_text(encoding="utf-8", errors="replace")
        if "CRIMES THAT STOP CRIMES" in t:
            print(name, "already has new eps")
            continue
        marker = "## SEASON 2 COMPLETE"
        if marker not in t:
            print(name, "marker missing")
            continue
        t = t.replace(marker, NEW_EPS.strip() + "\n\n---\n\n" + marker, 1)
        p.write_text(t, encoding="utf-8")
        print(name, "new eps inserted ->", len(t))


def patch_guides():
    rows = (
        '| BONUS 8 | "Crimes That Stop Crimes" | The carjacking skit, the Chevy Cruze, stealing a car that was already stolen; the creators as characters | Voice 261005 |\n'
        '| BONUS 9 | "Regenerate Everything" | Gemini writes our script; ten million episodes; character profiles; the grandma rule | Voice 261005 |\n'
    )
    for name in ["sitcom_final_s2.md", "sitcom_rewrite_s2.md"]:
        p = DL / name
        t = p.read_text(encoding="utf-8", errors="replace")
        if "Crimes That Stop Crimes" in t.split("## EPISODE 1")[0]:
            print(name, "guide already patched")
            continue
        anchor = '| BONUS 7 | "From a Box"'
        idx = t.find(anchor)
        if idx < 0:
            print(name, "BONUS 7 anchor missing")
            continue
        end = t.find("\n", t.find("\n", idx) )  # end of the row line — find full row end
        # find end of that table row (next newline after the row)
        row_end = t.find("\n", idx)
        t = t[: row_end + 1] + rows + t[row_end + 1 :]
        p.write_text(t, encoding="utf-8")
        print(name, "guide rows added ->", len(t))

    # S1: add writers-room row to guide
    p = DL / "sitcom_final_s1.md"
    t = p.read_text(encoding="utf-8", errors="replace")
    if "Crimes That Stop Crimes" not in t:
        anchor = '| 12 | "They Wanted to Shut Me Up"'
        idx = t.find(anchor)
        row_end = t.find("\n", idx)
        s1row = '| 13 | "Crimes That Stop Crimes" | The carjacking skit, the Chevy Cruze, the creators as characters | Voice 261005 |\n'
        t = t[: row_end + 1] + s1row + t[row_end + 1 :]
        p.write_text(t, encoding="utf-8")
        print("sitcom_final_s1.md guide row added ->", len(t))


def patch_characters():
    add = (
        " Writers'-room meta: Bob and Lum cast themselves as creator-characters who pop up "
        "in the skits ('Bob and I are going to be characters'); conceived the carjacking episode "
        "where the crimes accidentally stop bigger crimes — 'you steal a car, but moments earlier "
        "that car was stolen' — and the back-to-school tech episode. Use Gemini live to write the "
        "script: 'Twist. And more twisted. And more sexual.' Willing to regenerate every episode "
        "that isn't nailed down — 'let's take everything we've got and regenerate it all with the "
        "new information.' Character profiles must stay consistent across episodes, scenes, and "
        "seasons — except the thing with the grandma. Never tell anyone. (It's a joke. There's "
        "another thing with the grandma.)"
    )
    for name in ["sitcom_final_s1.md", "sitcom_final_s2.md", "sitcom_rewrite_s2.md"]:
        p = DL / name
        t = p.read_text(encoding="utf-8", errors="replace")
        if "Writers'-room meta" in t:
            print(name, "char sheet already patched")
            continue
        m = re.search(r"(\*\*BOB \(Robert Pelloni\):\*\*.*?)(\n\n)", t, re.S)
        if m:
            t = t[: m.end(1)] + add + t[m.end(1) :]
            p.write_text(t, encoding="utf-8")
            print(name, "bob sheet patched ->", len(t))
        else:
            print(name, "BOB sheet not found")


def patch_full_series():
    p = DL / "sitcom_bob_and_lum_full_series.md"
    t = p.read_text(encoding="utf-8", errors="replace")
    if "Crimes That Stop Crimes" in t:
        print("full_series already patched")
        return
    anchor = '| 14 | "From a Box"'
    idx = t.find(anchor)
    if idx < 0:
        print("full_series anchor missing")
        return
    row_end = t.find("\n", idx)
    rows = (
        '| 15 | "Crimes That Stop Crimes" | Heist comedy, moral dilemma | Carjacking skit, Chevy Cruze, stealing a car already stolen |\n'
        '| 16 | "Regenerate Everything" | Meta, AI writers, identity | Gemini writes the script, ten million episodes, the grandma rule |\n'
    )
    t = t[: row_end + 1] + rows + t[row_end + 1 :]
    t = t.replace(
        "Based on 246 transcript sessions (updated 2026-10-13)",
        "Based on 247 transcript sessions (updated 2026-10-13)",
        1,
    )
    p.write_text(t, encoding="utf-8")
    print("full_series patched ->", len(t))


def main():
    insert_new_eps()
    patch_guides()
    patch_characters()
    patch_full_series()


if __name__ == "__main__":
    main()
