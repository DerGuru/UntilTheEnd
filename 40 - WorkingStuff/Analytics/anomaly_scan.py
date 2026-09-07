"""Broad anomaly scan across the ENTIRE 423-chapter series:
1) chapters that deviate strongly from local neighborhood (re-read spikes / crashes)
2) single-day spike events and which chapters drove them
3) weekday pattern check against known RR baseline
Uses views/day (window-normalized) throughout, per the confound found earlier.
"""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    pv = ch["data"]["pageviews"]
    total = sum(e["views"] for e in pv)
    vpd = total / len(pv) if pv else 0
    chapters.append({"idx": idx, "title": title, "book": book, "num": num, "pv": pv, "total": total, "vpd": vpd})

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])

# --- 1. Local neighborhood outlier scan (within same book, +/-6 chapters) ---
print("=== Chapters deviating >=40% from local same-book neighborhood (views/day) ===")
anomalies = []
for b in BOOK_ORDER:
    bch = [c for c in story if c["book"] == b]
    for i, c in enumerate(bch):
        lo, hi = max(0, i - 6), min(len(bch), i + 7)
        neighbors = [bch[j]["vpd"] for j in range(lo, hi) if j != i]
        if not neighbors:
            continue
        local_avg = sum(neighbors) / len(neighbors)
        if local_avg == 0:
            continue
        ratio = c["vpd"] / local_avg
        if ratio >= 1.2 or ratio <= 0.8:
            anomalies.append((c, local_avg, ratio))

anomalies.sort(key=lambda t: -abs(t[2] - 1))
for c, local_avg, ratio in anomalies[:40]:
    kind = "SPIKE" if ratio > 1 else "DROP "
    print(f"  {kind}  {c['book']:9s} {c['num']:>3d}  vpd={c['vpd']:>5.2f}  local_avg={local_avg:>5.2f}  ratio={ratio:>4.2f}x  '{c['title']}'")

print(f"\nTotal anomalies found: {len(anomalies)} out of {len(story)} chapters")

# --- 2. Whole-fic single-day spike events: top 15 days, and which chapters drove them ---
daily_total = defaultdict(int)
daily_by_chapter = defaultdict(lambda: defaultdict(int))
for c in chapters:
    for e in c["pv"]:
        day = e["date"][:10]
        daily_total[day] += e["views"]
        daily_by_chapter[day][c["idx"]] += e["views"]

top_days = sorted(daily_total.items(), key=lambda kv: -kv[1])[:15]
print("\n=== Top 15 single-day spikes (whole fic) + which chapters drove them ===")
for day, total in top_days:
    chapter_shares = sorted(daily_by_chapter[day].items(), key=lambda kv: -kv[1])[:3]
    top_str = ", ".join(f"{chapters[idx]['title']}={v}" for idx, v in chapter_shares)
    weekday = datetime.strptime(day, "%Y-%m-%d").strftime("%a")
    print(f"  {day} ({weekday})  total={total:>6,d}   top: {top_str}")

# --- 3. Weekday pattern check ---
weekday_totals = defaultdict(int)
weekday_counts = defaultdict(int)
for day, total in daily_total.items():
    wd = datetime.strptime(day, "%Y-%m-%d").strftime("%a")
    weekday_totals[wd] += total
    weekday_counts[wd] += 1

print("\n=== Average daily views by weekday (whole fic, all days) ===")
order = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
for wd in order:
    avg = weekday_totals[wd] / weekday_counts[wd] if weekday_counts[wd] else 0
    print(f"  {wd}: avg={avg:>7.1f}  (n_days={weekday_counts[wd]})")

