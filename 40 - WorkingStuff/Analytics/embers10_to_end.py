"""What % of readers who reached Embers-10 make it to the very end, and what
per-chapter bleed rate would produce that, using the live official RR dropout
(# of Members) histogram.
"""
import json
import re
from pathlib import Path
from math import log

ANALYTICS = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics")
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

SNAPSHOT = Path(
    r"c:\Users\JakofHe\AppData\Roaming\Code\User\workspaceStorage\2b686f337a99865772cdd545647f1805"
    r"\GitHub.copilot-chat\chat-session-resources\86e3ca1b-be41-4a75-8b26-8daf7faf8714"
    r"\toolu_01MaKbnwr1GxBzAFb329EtA8__vscode-1788786501410\content.txt"
)
text = SNAPSHOT.read_text(encoding="utf-8")
cells = re.findall(r'cell "([^"]*)"', text)
raw_rows = [cells[i:i + 6] for i in range(0, len(cells) - len(cells) % 6, 6)]

rows = []
for title, views, retention, members, pct_members, pct_remaining in raw_rows:
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (mm.group(1).strip(), int(mm.group(2))) if mm else (title.strip(), None)
    rows.append({"title": title, "book": book, "num": num, "members": int(members.replace(",", ""))})

story = [r for r in rows if r["book"] in BOOK_ORDER]

# index of Embers-10
e10_idx = next(i for i, r in enumerate(story) if r["book"] == "Embers" and r["num"] == 10)
print(f"Embers-10 is story-index {e10_idx} (0-based), {len(story)} total story chapters")

from_e10 = story[e10_idx:]
reached_e10 = sum(r["members"] for r in from_e10)
print(f"\nPopulation that reached AT LEAST Embers-10 (sum of dropouts from Embers-10 to Clouds-68): {reached_e10}")

# "reached the end": last chapter alone, and last 3 chapters combined (two definitions)
last1 = sum(r["members"] for r in story[-1:])
last3 = sum(r["members"] for r in story[-3:])
last5 = sum(r["members"] for r in story[-5:])
print(f"Dropout count AT Clouds-68 only (strict 'finished'): {last1}")
print(f"Dropout count in last 3 chapters (Clouds 66-68): {last3}")
print(f"Dropout count in last 5 chapters (Clouds 64-68): {last5}")

for label, val in [("last chapter only", last1), ("last 3 chapters", last3), ("last 5 chapters", last5)]:
    pct = val / reached_e10 * 100
    print(f"\n=> % of 'reached Embers-10' population that reaches the end ({label}): {pct:.2f}%")
    n_chapters_span = len(from_e10) - 1  # chapters between Embers-10 and the reference point
    R = val / reached_e10
    if R > 0:
        per_chapter_rate = 1 - R ** (1 / n_chapters_span)
        print(f"   Implied constant per-chapter bleed rate over {n_chapters_span} chapters: {per_chapter_rate*100:.4f}%/chapter")

print(f"\n(For context: total chapters from Embers-10 to Clouds-68 = {len(from_e10)})")

# also overall: total series dropout vs Embers-10 restriction, for framing
grand_total = sum(r["members"] for r in story)
print(f"\nGrand total dropout across ALL chapters (Embers-01 to Clouds-68): {grand_total}")
print(f"Embers 1-9 alone accounts for: {grand_total - reached_e10} ({(grand_total-reached_e10)/grand_total*100:.1f}% of all dropout)")
