"""Check: overall summer slump + recent (Sep) uptick across ALL chapters,
and whether recent activity mix has shifted toward later books (resumers)
vs. staying concentrated early (new readers only).
"""
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
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

# --- 1. Total daily views across ALL chapters (whole-fic traffic timeline) ---
daily_total = defaultdict(int)
for c in chapters:
    for e in c["pv"]:
        day = e["date"][:10]
        daily_total[day] += e["views"]

days_sorted = sorted(daily_total.keys())
print(f"Date range: {days_sorted[0]} .. {days_sorted[-1]}  ({len(days_sorted)} days)\n")

# Weekly aggregation for a readable trend (avoids weekday noise)
weekly = defaultdict(int)
for day in days_sorted:
    dt = datetime.strptime(day, "%Y-%m-%d")
    iso_year, iso_week, _ = dt.isocalendar()
    weekly[(iso_year, iso_week)] += daily_total[day]

print("=== Weekly total pageviews (whole fic, all 423 chapters) ===")
for (y, w), v in sorted(weekly.items()):
    bar = "#" * int(v / 300)
    print(f"  {y}-W{w:02d}  {v:>7,d}  {bar}")

# --- 2. Where does recent activity concentrate, compared 30d-ago-window vs now ---
last_ts = max(e["unixtime"] for c in chapters for e in c["pv"])

def window_sum(pv, start_days_ago, end_days_ago):
    hi = last_ts - end_days_ago * 86400
    lo = last_ts - start_days_ago * 86400
    return sum(e["views"] for e in pv if lo <= e["unixtime"] < hi)

story = [c for c in chapters if c["book"] in BOOK_ORDER]

print("\n=== Per-book share of activity: NOW (last 7d) vs. ~2 months ago (7d window, 60-67d ago) ===")
for c in story:
    c["now7"] = window_sum(c["pv"], 7, 0)
    c["past7"] = window_sum(c["pv"], 67, 60)

grand_now = sum(c["now7"] for c in story)
grand_past = sum(c["past7"] for c in story)
print(f"  (grand totals: now7={grand_now}, past7(~60-67d ago)={grand_past})")
for b in BOOK_ORDER:
    bch = [c for c in story if c["book"] == b]
    now = sum(c["now7"] for c in bch)
    past = sum(c["past7"] for c in bch)
    now_pct = now / grand_now * 100 if grand_now else 0
    past_pct = past / grand_past * 100 if grand_past else 0
    print(f"  {b:10s}  now%={now_pct:5.1f}   ~60-67d-ago%={past_pct:5.1f}   (now abs={now:>4d}, past abs={past:>4d})")
