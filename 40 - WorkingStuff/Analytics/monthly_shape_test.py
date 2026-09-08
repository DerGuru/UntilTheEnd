"""Proper test using cumulative (monotonic) pageviews: for representative chapters
across the book, look at MONTHLY view totals since each chapter's own publish date.

If readers slowly advance (not bleed out): late chapters should show a SUSTAINED or
GROWING monthly trickle over many months post-publication (an aging cohort finally
arriving), not a decay curve.

If it's pure churn (fast readers reach far, slow readers rarely do): late chapters
should show the SAME decaying shape as early chapters -- a burst right after
publication (whoever was fast enough), then flattening to a thin trickle from brand
new fast readers only, with no later resurgence.
"""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = {}
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    chapters[title] = {"idx": idx, "book": book, "num": num, "pv": ch["data"]["pageviews"]}

TARGETS = ["Embers - 01", "Roots - 01", "Silence - 01", "Echoes - 01",
           "Fractures - 01", "Mirrors - 01", "Clouds - 01", "Clouds - 68"]

for title in TARGETS:
    c = chapters[title]
    monthly = defaultdict(int)
    for e in c["pv"]:
        d = datetime.strptime(e["date"][:10], "%Y-%m-%d")
        key = f"{d.year}-{d.month:02d}"
        monthly[key] += e["views"]
    months_sorted = sorted(monthly.keys())
    print(f"=== {title} (published ~{months_sorted[0]}) ===")
    for mo in months_sorted:
        bar = "#" * int(monthly[mo] / 20)
        print(f"    {mo}: {monthly[mo]:>6,d}  {bar}")
    print()
