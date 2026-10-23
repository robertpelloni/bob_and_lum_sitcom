"""Normalize session headers in the combined corpus.

Some sessions use  ==== \\n [N]   and others  ==== \\n\\n [N].  Collapse to one
canonical block so split-based tooling (regen_wordpress_html.py) works:

    ==============================================================================
    [N]  filename   —   date
    ==============================================================================
    <blank line>
    body
"""
from pathlib import Path
import re

DL = Path(r"C:\Users\hyper\Downloads")
FILES = [DL / "sitcom script.txt", DL / "CONVERSATION_SCRIPT_COMPLETE.txt"]

HDR = re.compile(
    r"^[ \t]*(=+)[ \t]*\n+\[(\d+)\]([^\n]*)\n+[ \t]*=+[ \t]*\n+",
    re.M,
)


def m(mo):
    num, rest = mo.group(2), mo.group(3)
    return "=" * 78 + f"\n[{num}]{rest}\n" + "=" * 78 + "\n\n"


a = FILES[0]
t = a.read_text(encoding="utf-8", errors="replace")
t2, n = HDR.subn(m, t)
# also strip trailing spaces on separator-ish lines that aren't pure '='+
a.write_text(t2, encoding="utf-8", newline="\n")
print(a.name, "normalized headers:", n)

b = FILES[1]
b.write_text(t2, encoding="utf-8", newline="\n")
print("wrote twin identical")

# verify
t = a.read_text(encoding="utf-8", errors="replace")
print("headers:", len(re.findall(r"^\[\d+\]", t, re.M)))
print("pure =+ lines:", len(re.findall(r"^=+$", t, re.M)))
print("split chunks:", len(re.split(r"\n(?====+\n\[\d+\])", t)))
print("bytes:", a.stat().st_size, b.stat().st_size)
print("identical:", a.read_bytes() == b.read_bytes())
