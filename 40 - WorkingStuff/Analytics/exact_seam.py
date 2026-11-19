"""Exact chapter-by-chapter view at the Echoes/Fractures seam (no averaging window)
to see if the drop is a single-chapter cliff, spread over N chapters, or gradual.
Checked across r7/r14/r30 for stability (not just one noisy window).
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

for c in chapters:
    c["r7"] = recent(c["pv"], 7)
    c["r14"] = recent(c["pv"], 14)
    c["r30"] = recent(c["pv"], 30)

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
echoes = [c for c in story if c["book"] == "Echoes"]
fractures = [c for c in story if c["book"] == "Fractures"]

window = echoes[-5:] + fractures[:20]
print(f"{'Chapter':14s} {'r7':>4s} {'r14':>4s} {'r30':>4s}")
for c in window:
    marker = "  <-- book boundary" if c is fractures[0] else ""
    print(f"  {c['book']:9s} {c['num']:>3d}  {c['r7']:>4d} {c['r14']:>4d} {c['r30']:>4d}{marker}")

# Chapter-to-chapter % change within this window (on r30, least noisy)
print("\nChapter-to-chapter %-change (r30):")
for i in range(1, len(window)):
    prev, cur = window[i-1], window[i]
    if prev["r30"] == 0:
        continue
    pct = (cur["r30"] - prev["r30"]) / prev["r30"] * 100
    label = f"{prev['book']}{prev['num']:02d} -> {cur['book']}{cur['num']:02d}"
    flag = "  <==" if abs(pct) > 30 else ""
    print(f"  {label:24s} {pct:+7.1f}%{flag}")
