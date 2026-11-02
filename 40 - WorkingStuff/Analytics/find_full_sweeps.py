"""Scan the stored per-chapter pageview dump (Mar 8 - Sep 7 2026) for 'full sweep' days:
days where EVERY chapter gets >=1 view. Organic low-season traffic does not touch all
chapters on one day, so floor>=1 in quiet months points to complete automated passes."""
import json
from collections import defaultdict
from pathlib import Path

RAW = Path(__file__).with_name("ute_pageviews_raw.json")
data = json.loads(RAW.read_text(encoding="utf-8"))

views = defaultdict(dict)  # date -> {chapter_idx: views}
first_seen = {}
for idx, ch in enumerate(data):
    for e in ch["data"]["pageviews"]:
        d = e["date"][:10]
        if e["views"] > 0:
            views[d][idx] = e["views"]
            first_seen.setdefault(idx, d)

n = len(data)
print(f"{'date':10s} {'total':>6s} {'covered':>7s} {'floor':>5s} {'exact1':>6s} {'exact2':>6s}  total/423")
for d in sorted(views):
    row = views[d]
    covered = len(row)
    floor = min(row.get(i, 0) for i in range(n))
    total = sum(row.values())
    if covered >= n - 5:
        ex1 = sum(1 for v in row.values() if v == 1)
        ex2 = sum(1 for v in row.values() if v == 2)
        print(f"{d:10s} {total:6d} {covered:7d} {floor:5d} {ex1:6d} {ex2:6d}  {total / n:.2f}")
