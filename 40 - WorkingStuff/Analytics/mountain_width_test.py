"""Is there still a 'mountain' (hump) of active readers before the end, and has it
widened over time? Uses r180 (full available window) for the current robust shape,
then monthly post-trending slices (June/July/Aug/Sep) to check width trend --
30d windows were too noisy (per user), and the dataset only spans 184 days total
so a rolling 180d comparison isn't feasible; monthly slices are the practical fix.
"""
import json
import re
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from math import sqrt

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    chapters.append({"idx": idx, "book": book, "num": num, "pv": ch["data"]["pageviews"]})

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
n = len(story)
last_ts = max(e["unixtime"] for c in story for e in c["pv"])


def window_sum(pv, lo_ts, hi_ts):
    return sum(e["views"] for e in pv if lo_ts <= e["unixtime"] < hi_ts)


def weighted_stats(weights):
    """weights: list aligned with story index -> (mean_idx, std_idx, total)"""
    total = sum(weights)
    if total == 0:
        return None, None, 0
    mean_idx = sum(i * w for i, w in enumerate(weights)) / total
    var_idx = sum(w * (i - mean_idx) ** 2 for i, w in enumerate(weights)) / total
    return mean_idx, sqrt(var_idx), total


def describe(mean_idx, std_idx):
    lo, hi = story[max(0, int(mean_idx - std_idx))], story[min(n - 1, int(mean_idx + std_idx))]
    center = story[min(n - 1, max(0, int(mean_idx)))]
    return (f"center ~{center['book']}{center['num']:>3d} (idx {mean_idx:>5.1f})   "
            f"width(std)={std_idx:>5.1f} ch   1-sigma range ~ {lo['book']}{lo['num']} .. {hi['book']}{hi['num']}")


# --- 1. Current robust shape: r180 (~full window) ---
r180 = [window_sum(c["pv"], last_ts - 180 * 86400, last_ts) for c in story]
mean_i, std_i, total = weighted_stats(r180)
print(f"=== r180 (full available window), total={total:,} views ===")
print("  " + describe(mean_i, std_i))

print("\n  Binned shape (r180), 20-chapter bins:")
for start in range(0, n, 20):
    chunk = r180[start:start + 20]
    s = sum(chunk)
    bar = "#" * int(s / 30)
    lo, hi = story[start], story[min(n - 1, start + len(chunk) - 1)]
    print(f"    ch {start+1:>3d}-{start+len(chunk):<3d} ({lo['book']}{lo['num']}..{hi['book']}{hi['num']}): {s:>5,d}  {bar}")

# --- 2. Monthly post-trending slices: June, July, August, September ---
print("\n=== Monthly slices (post-trending) -- width trend over time ===")
months = [
    ("June", datetime(2026, 6, 1), datetime(2026, 7, 1)),
    ("July", datetime(2026, 7, 1), datetime(2026, 8, 1)),
    ("August", datetime(2026, 8, 1), datetime(2026, 9, 1)),
    ("Sep(partial)", datetime(2026, 9, 1), datetime(2026, 9, 8)),
]
for label, start_dt, end_dt in months:
    lo_ts, hi_ts = start_dt.timestamp(), end_dt.timestamp()
    weights = [window_sum(c["pv"], lo_ts, hi_ts) for c in story]
    mean_i, std_i, total = weighted_stats(weights)
    if total == 0:
        print(f"  {label:14s}: no data")
        continue
    print(f"  {label:14s} (n={total:>4,d} views):  " + describe(mean_i, std_i))
