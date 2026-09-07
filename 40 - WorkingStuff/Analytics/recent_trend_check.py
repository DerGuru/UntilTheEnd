"""Daily (not ISO-week-binned) totals for the last ~50 days, plus Ch1-only trend,
to check the user's claim that views are rising again in the last week,
and whether that rise is new-reader-driven (Ch1) or spread across the back half.
"""
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    chapters.append({"idx": idx, "title": title, "book": book, "num": num, "pv": ch["data"]["pageviews"]})

daily_total = defaultdict(int)
daily_ch1 = defaultdict(int)
daily_by_book = defaultdict(lambda: defaultdict(int))

for c in chapters:
    is_ch1 = (c["book"] == "Embers" and c["num"] == 1)
    for e in c["pv"]:
        day = e["date"][:10]
        daily_total[day] += e["views"]
        if is_ch1:
            daily_ch1[day] += e["views"]
        if c["book"] in BOOK_ORDER:
            daily_by_book[day][c["book"]] += e["views"]

days_sorted = sorted(daily_total.keys())
last_50 = days_sorted[-50:]

print(f"{'Date':10s} {'Total':>6s} {'Ch1':>5s} {'Emb-Ech':>8s} {'Fra-Cl':>7s}")
for day in last_50:
    front = sum(daily_by_book[day][b] for b in ["Embers", "Roots", "Silence", "Echoes"])
    back = sum(daily_by_book[day][b] for b in ["Fractures", "Mirrors", "Clouds"])
    print(f"{day:10s} {daily_total[day]:>6d} {daily_ch1[day]:>5d} {front:>8d} {back:>7d}")

# Explicit last-7d vs prior-7d vs 30-37d-ago comparison (rolling, not ISO week)
def rng(days_list, a, b):
    """sum over days_list[-(b): -(a) or end]"""
    if a == 0:
        return sum(daily_total[d] for d in days_list[-b:])
    return sum(daily_total[d] for d in days_list[-b:-a])

print("\nLast 7 days total (all chapters):        ", rng(days_sorted, 0, 7))
print("Prior 7 days (8-14 days ago):             ", rng(days_sorted, 7, 14))
print("Prior 7 days (15-21 days ago):             ", rng(days_sorted, 14, 21))
print("~30-37 days ago (7d window):               ", rng(days_sorted, 30, 37))
print("~60-67 days ago (7d window):               ", rng(days_sorted, 60, 67))
