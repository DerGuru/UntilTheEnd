"""Same seam localization, but with larger-N windows (r90, r180, all-time total)
so deltas are based on >=50 views instead of noisy single-digit r30 counts.
"""
import json
import re
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    chapters.append({"idx": idx, "book": book, "num": num, "pv": ch["data"]["pageviews"]})

last_ts = max(e["unixtime"] for c in chapters for e in c["pv"])

def recent(pv, days):
    cutoff = last_ts - days * 86400
    return sum(e["views"] for e in pv if e["unixtime"] >= cutoff)

def total(pv):
    return sum(e["views"] for e in pv)

for c in chapters:
    c["r90"] = recent(c["pv"], 90)
    c["r180"] = recent(c["pv"], 180)
    c["total"] = total(c["pv"])

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
echoes = [c for c in story if c["book"] == "Echoes"]
fractures = [c for c in story if c["book"] == "Fractures"]

window = echoes[-5:] + fractures[:20]
print(f"{'Chapter':14s} {'r90':>5s} {'r180':>5s} {'total(all-time)':>16s}")
for c in window:
    marker = "  <-- book boundary" if c is fractures[0] else ""
    print(f"  {c['book']:9s} {c['num']:>3d}  {c['r90']:>5d} {c['r180']:>5d} {c['total']:>16,d}{marker}")

for label, key in [("r90", "r90"), ("r180", "r180"), ("total (all-time)", "total")]:
    print(f"\nChapter-to-chapter %-change ({label}):")
    for i in range(1, len(window)):
        prev, cur = window[i-1], window[i]
        if prev[key] == 0:
            continue
        pct = (cur[key] - prev[key]) / prev[key] * 100
        min_delta = min(prev[key], cur[key])
        reliable = "" if min_delta >= 50 else "  (n<50, still noisy)"
        label2 = f"{prev['book']}{prev['num']:02d} -> {cur['book']}{cur['num']:02d}"
        flag = "  <==" if abs(pct) > 25 else ""
        print(f"  {label2:24s} {prev[key]:>6,d} -> {cur[key]:>6,d}  {pct:+7.1f}%{flag}{reliable}")
