"""Full, statistically reliable (all-time total) view of Echoes + Fractures + Mirrors-head
to properly localize any real break, replacing the noisy r30-based seam analysis.
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
    total = sum(e["views"] for e in ch["data"]["pageviews"])
    chapters.append({"idx": idx, "book": book, "num": num, "total": total})

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
echoes = [c for c in story if c["book"] == "Echoes"]
fractures = [c for c in story if c["book"] == "Fractures"]
mirrors = [c for c in story if c["book"] == "Mirrors"]

def show(lst, name):
    print(f"--- {name} (total all-time) ---")
    for c in lst:
        bar = "#" * int(c["total"] / 20)
        print(f"  {c['book']:9s} {c['num']:>3d}  {c['total']:>5,d}  {bar}")

show(echoes, "Echoes (all 57)")
show(fractures, "Fractures (all 49)")
show(mirrors[:10], "Mirrors (first 10)")

# 5-chapter rolling average to see the shape without single-chapter noise
def rolling(seq, window=5):
    vals = [c["total"] for c in seq]
    out = []
    for i in range(len(vals)):
        lo = max(0, i - window // 2)
        hi = min(len(vals), i + window // 2 + 1)
        out.append(sum(vals[lo:hi]) / (hi - lo))
    return out

combined = echoes + fractures
roll = rolling(combined)
print("\n--- 5-chapter rolling average, Echoes+Fractures combined ---")
for c, r in zip(combined, roll):
    print(f"  {c['book']:9s} {c['num']:>3d}  total={c['total']:>5,d}  roll5={r:>7.1f}")
