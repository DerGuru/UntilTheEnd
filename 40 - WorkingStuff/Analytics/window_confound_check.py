"""Check for observation-window confound: do later chapters have systematically
shorter tracking windows (later accurateSince), which would fake a 'decline'
in raw total views even with zero real attrition?
"""
import json
import re
from datetime import datetime
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    d = ch["data"]
    pv = d["pageviews"]
    first_date = pv[0]["date"][:10] if pv else None
    total = sum(e["views"] for e in pv)
    chapters.append({
        "idx": idx, "book": book, "num": num, "total": total,
        "accurateSince": d.get("accurateSince"), "first_pv": first_date, "n_entries": len(pv),
    })

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
echoes = [c for c in story if c["book"] == "Echoes"]
fractures = [c for c in story if c["book"] == "Fractures"]

print("=== Echoes: first_pv date + entry count per chapter (observation window check) ===")
for c in echoes:
    print(f"  {c['book']:9s} {c['num']:>3d}  first_pv={c['first_pv']}  n_entries={c['n_entries']:>4d}  total={c['total']:>5,d}")

print("\n=== Fractures: first_pv date + entry count per chapter ===")
for c in fractures:
    print(f"  {c['book']:9s} {c['num']:>3d}  first_pv={c['first_pv']}  n_entries={c['n_entries']:>4d}  total={c['total']:>5,d}")

# Normalize: views per day of observation, to strip out the window-length confound
print("\n=== Views PER DAY OF OBSERVATION (total / n_entries) -- window-normalized ===")
combined = echoes + fractures
roll_vals = []
for c in combined:
    vpd = c["total"] / c["n_entries"] if c["n_entries"] else 0
    roll_vals.append(vpd)
for c, vpd in zip(combined, roll_vals):
    print(f"  {c['book']:9s} {c['num']:>3d}  views/day={vpd:>6.2f}")
