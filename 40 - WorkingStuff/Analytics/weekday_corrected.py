"""Redo weekday pattern with correct date semantics: a pageview entry's 'date'
field is the boundary (exclusive), so views recorded under date X actually
happened on X-1. Shift every entry back one day before bucketing by weekday.
"""
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))

daily_total_shifted = defaultdict(int)
for ch in data:
    for e in ch["data"]["pageviews"]:
        labeled_date = datetime.strptime(e["date"][:10], "%Y-%m-%d")
        actual_date = labeled_date - timedelta(days=1)  # correction: exclusive-of-day label
        daily_total_shifted[actual_date.strftime("%Y-%m-%d")] += e["views"]

weekday_totals = defaultdict(int)
weekday_counts = defaultdict(int)
for day, total in daily_total_shifted.items():
    wd = datetime.strptime(day, "%Y-%m-%d").strftime("%a")
    weekday_totals[wd] += total
    weekday_counts[wd] += 1

print("=== Average daily views by weekday, CORRECTED (date shifted -1 day) ===")
order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for wd in order:
    avg = weekday_totals[wd] / weekday_counts[wd] if weekday_counts[wd] else 0
    print(f"  {wd}: avg={avg:>7.1f}  (n_days={weekday_counts[wd]})")

# Sanity check: show old (unshifted) side by side
daily_total_raw = defaultdict(int)
for ch in data:
    for e in ch["data"]["pageviews"]:
        daily_total_raw[e["date"][:10]] += e["views"]
weekday_totals_raw = defaultdict(int)
weekday_counts_raw = defaultdict(int)
for day, total in daily_total_raw.items():
    wd = datetime.strptime(day, "%Y-%m-%d").strftime("%a")
    weekday_totals_raw[wd] += total
    weekday_counts_raw[wd] += 1

print("\n=== Side by side: raw (mislabeled) vs corrected ===")
for wd in order:
    raw_avg = weekday_totals_raw[wd] / weekday_counts_raw[wd] if weekday_counts_raw[wd] else 0
    cor_avg = weekday_totals[wd] / weekday_counts[wd] if weekday_counts[wd] else 0
    print(f"  {wd}:  raw={raw_avg:>7.1f}   corrected={cor_avg:>7.1f}")
