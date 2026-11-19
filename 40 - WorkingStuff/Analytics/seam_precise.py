"""Precise local step-size at the Echoes/Fractures boundary vs. Echoes-internal decline,
to check whether drop-off concentrates in Echoes' first half or right at the book seam.
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

def r30(pv):
    cutoff = last_ts - 30 * 86400
    return sum(e["views"] for e in pv if e["unixtime"] >= cutoff)

for c in chapters:
    c["r30"] = r30(c["pv"])

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
echoes = [c for c in story if c["book"] == "Echoes"]
fractures = [c for c in story if c["book"] == "Fractures"]

print("=== Local step at the Echoes/Fractures seam (adjacent-N comparison) ===")
for N in (5, 7, 10, 15, 19):
    pre = echoes[-N:]
    post = fractures[:N]
    avg_pre = sum(c["r30"] for c in pre) / N
    avg_post = sum(c["r30"] for c in post) / N
    step = (avg_post - avg_pre) / avg_pre * 100
    print(f"  N={N:2d}  Echoes last {N:2d} avg={avg_pre:5.2f}   Fractures first {N:2d} avg={avg_post:5.2f}   step={step:+.1f}%")

print("\n=== Echoes internal decline (thirds, 19 chapters each) ===")
first19, mid19, last19 = echoes[:19], echoes[19:38], echoes[38:]
a = sum(c["r30"] for c in first19) / len(first19)
b = sum(c["r30"] for c in mid19) / len(mid19)
c_ = sum(c["r30"] for c in last19) / len(last19)
print(f"  first 19 avg: {a:5.2f}")
print(f"  mid   19 avg: {b:5.2f}   step from first: {(b-a)/a*100:+.1f}%")
print(f"  last  19 avg: {c_:5.2f}   step from mid:   {(c_-b)/b*100:+.1f}%")
print(f"  total first->last: {(c_-a)/a*100:+.1f}%")

print("\n=== Total decline chain: Echoes-start -> Echoes-end -> Fractures-start ===")
fr10 = sum(c["r30"] for c in fractures[:10]) / 10
print(f"  Echoes first-19 avg ({a:.2f}) -> Echoes last-19 avg ({c_:.2f}): {(c_-a)/a*100:+.1f}%  [within Echoes]")
print(f"  Echoes last-19 avg ({c_:.2f}) -> Fractures first-10 avg ({fr10:.2f}): {(fr10-c_)/c_*100:+.1f}%  [at the seam]")
print(f"  Echoes first-19 avg ({a:.2f}) -> Fractures first-10 avg ({fr10:.2f}): {(fr10-a)/a*100:+.1f}%  [total, Echoes-start to Fractures-start]")
