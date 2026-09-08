"""Export the complete site-wide daily pageview timeline (08.03.-07.09.), computed
by summing the per-chapter JSON across all chapters per day -- same values as the
live '/api/data/chapterv' endpoint for their 31-day overlap, but covering the full
tracked history instead of just a rolling window.
"""
import csv
import json
from collections import defaultdict
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
OUT_JSON = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_sitewide_pageviews_full.json")
OUT_CSV = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_sitewide_pageviews_full.csv")

data = json.loads(SRC.read_text(encoding="utf-8"))

daily_total = defaultdict(int)
for ch in data:
    for e in ch["data"]["pageviews"]:
        daily_total[e["date"][:10]] += e["views"]

days_sorted = sorted(daily_total.keys())
records = [{"date": d, "views": daily_total[d]} for d in days_sorted]

OUT_JSON.write_text(json.dumps(records, indent=2), encoding="utf-8")
with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["date", "views"])
    w.writeheader()
    w.writerows(records)

print(f"Wrote {len(records)} days: {days_sorted[0]} .. {days_sorted[-1]}")
print(f"  {OUT_JSON}")
print(f"  {OUT_CSV}")
print(f"Total views across full range: {sum(daily_total.values()):,}")
