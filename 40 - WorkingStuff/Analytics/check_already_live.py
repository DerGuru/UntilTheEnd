"""Check exactly how far into the story the 'already tracked from day 1' placeholder
(accurateSince ~2026-03-07/08) extends, vs. real later publish dates -- this would
explain why Echoes shows views very early in the growth video (it may have already
been fully posted before tracking started, not released gradually).
"""
import json
import re
from pathlib import Path

data = json.loads(Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json").read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    pv = ch["data"]["pageviews"]
    first_pv = pv[0]["date"][:10] if pv else None
    chapters.append({"idx": idx, "book": book, "num": num, "first_pv": first_pv})

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])

# Find the boundary: last chapter whose first_pv is still the early placeholder (<=2026-03-09)
early_cutoff = "2026-03-09"
last_early = None
first_late = None
for c in story:
    if c["first_pv"] <= early_cutoff:
        last_early = c
    elif first_late is None:
        first_late = c

print(f"Last chapter with first_pv <= {early_cutoff} (i.e. 'already live before tracking started'):")
print(f"  {last_early['book']} {last_early['num']}  (story idx {last_early['idx']}, first_pv={last_early['first_pv']})")
print(f"\nFirst chapter with a REAL later first_pv (genuinely tracked from its actual later publish moment):")
print(f"  {first_late['book']} {first_late['num']}  (story idx {first_late['idx']}, first_pv={first_late['first_pv']})")

n_already_live = last_early["idx"] + 1
print(f"\n=> {n_already_live} of {len(story)} story chapters were ALREADY live/posted by {early_cutoff},")
print(f"   before pageview tracking even started -- i.e. available to readers from day 1 of the data.")

# Show the transition zone in detail (Echoes chapters specifically)
print("\n=== Echoes chapters: first_pv date per chapter ===")
for c in story:
    if c["book"] == "Echoes":
        flag = "  <- still 'day 1' placeholder" if c["first_pv"] <= early_cutoff else "  <- real later date"
        print(f"  Echoes {c['num']:>2d}: first_pv={c['first_pv']}{flag}")
