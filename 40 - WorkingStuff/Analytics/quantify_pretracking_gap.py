"""Use the 40 saved 'General Analytics' snapshots (readerActivityData = RR's true
lifetime views counter per chapter) to quantify the pre-March-7 gap in the daily
pageviews JSON: compare JSON's cumulative sum up to each snapshot date against
that snapshot's actual reported lifetime total for Embers-01.
"""
import json
import re
from datetime import datetime
from pathlib import Path

ANALYTICS = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics")

# 1. Load JSON daily data for Embers-01
data = json.loads((ANALYTICS / "ute_pageviews_raw.json").read_text(encoding="utf-8"))
e1 = next(c for c in data if c["title"].strip() == "Embers - 01")
pv = e1["data"]["pageviews"]
pv_by_date = {e["date"][:10]: e["views"] for e in pv}
sorted_dates = sorted(pv_by_date.keys())

def json_cumulative_through(cutoff_date_str):
    return sum(v for d, v in pv_by_date.items() if d <= cutoff_date_str)

# 2. Extract readerActivityData 'views' for Embers-01 from every dated General Analytics snapshot
snapshot_files = sorted(ANALYTICS.glob("General Analytics _ Royal Road-*.html"))
results = []
for f in snapshot_files:
    m = re.search(r"General Analytics _ Royal Road-(\d{4}-\d{2}-\d{2})T", f.name)
    if not m:
        continue
    snap_date = m.group(1)
    html = f.read_text(encoding="utf-8", errors="ignore")
    m2 = re.search(r'var readerActivityData\s*=\s*(\[.*?\]);', html, re.DOTALL)
    if not m2:
        continue
    activity = json.loads(m2.group(1))
    e1_snap = next((a for a in activity if a["title"] == "Embers - 01"), None)
    if e1_snap:
        results.append((snap_date, e1_snap["views"]))

results.sort()
print(f"{'Snapshot date':14s} {'RR lifetime views':>18s} {'JSON cumulative thru date':>26s} {'Gap (missing pre-track)':>26s}")
for snap_date, rr_views in results:
    json_cum = json_cumulative_through(snap_date)
    gap = rr_views - json_cum
    print(f"{snap_date:14s} {rr_views:>18,d} {json_cum:>26,d} {gap:>26,d}")
