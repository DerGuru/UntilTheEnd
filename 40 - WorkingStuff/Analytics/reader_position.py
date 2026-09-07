"""Where in the 7 books are currently active readers? (not geography - story position)

Uses recent pageview windows (7/14/30d) per chapter as a proxy for "how many readers
are currently active around this chapter", since cumulative totals are dominated by
the April/May trending spike and early-chapter funnel mass.
"""
import json
import re
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
    pv = ch["data"]["pageviews"]
    chapters.append({
        "idx": idx, "title": title, "book": book, "num": num, "pv": pv,
    })

last_date = max(datetime.fromisoformat(e["date"].replace("Z", "+00:00"))
                 for c in chapters for e in c["pv"])

def recent_sum(pv, days):
    cutoff = last_date.timestamp() - days * 86400
    return sum(e["views"] for e in pv if e["unixtime"] >= cutoff)

def total_sum(pv):
    return sum(e["views"] for e in pv)

for c in chapters:
    c["total"] = total_sum(c["pv"])
    c["r7"] = recent_sum(c["pv"], 7)
    c["r14"] = recent_sum(c["pv"], 14)
    c["r30"] = recent_sum(c["pv"], 30)

print(f"Latest data point: {last_date.date()}\n")

# --- Per-book aggregation (story chapters only, excludes Afterword/Amazon/Origins) ---
story = [c for c in chapters if c["book"] in BOOK_ORDER]
extras = [c for c in chapters if c["book"] not in BOOK_ORDER]

print("=== Per book: recent activity vs. all-time total ===")
print(f"{'Book':10s} {'Chapters':>8s} {'Total(all-time)':>16s} {'Last30d':>8s} {'/chapter':>8s} {'Last14d':>8s} {'Last7d':>7s} {'%ofR30':>7s}")
grand_r30 = sum(c["r30"] for c in story)
for b in BOOK_ORDER:
    bch = [c for c in story if c["book"] == b]
    tot = sum(c["total"] for c in bch)
    r30 = sum(c["r30"] for c in bch)
    r14 = sum(c["r14"] for c in bch)
    r7 = sum(c["r7"] for c in bch)
    pct = r30 / grand_r30 * 100 if grand_r30 else 0
    print(f"{b:10s} {len(bch):>8d} {tot:>16,d} {r30:>8,d} {r30/len(bch):>8.1f} {r14:>8,d} {r7:>7,d} {pct:>6.1f}%")

print()
print("=== Weighted 'center of mass' of CURRENT reading activity ===")
for label, key in [("last 7d", "r7"), ("last 14d", "r14"), ("last 30d", "r30")]:
    w = sum(c[key] for c in story)
    if w == 0:
        continue
    mean_idx = sum(c["idx"] * c[key] for c in story) / w
    # map mean_idx (global 0-based index within story chapters) back to book/chapter
    story_sorted = sorted(story, key=lambda c: c["idx"])
    lo = int(mean_idx)
    target = story_sorted[min(lo, len(story_sorted)-1)]
    print(f"  {label:10s}: weighted mean chapter index = {mean_idx:6.1f}  ->  ~{target['book']} {target['num']:02d}")

print()
print("=== Distribution of last-30d views across the story (bins of 20 chapters) ===")
story_sorted = sorted(story, key=lambda c: c["idx"])
bin_size = 20
for start in range(0, len(story_sorted), bin_size):
    bin_chs = story_sorted[start:start+bin_size]
    r30 = sum(c["r30"] for c in bin_chs)
    bar = "#" * int(r30 / 20)
    label_first, label_last = bin_chs[0], bin_chs[-1]
    print(f"  ch {start+1:>3d}-{start+len(bin_chs):<3d} "
          f"({label_first['book']}{label_first['num']:>3d}..{label_last['book']}{label_last['num']:>3d}): "
          f"{r30:>5,d}  {bar}")

print()
print("=== Top 15 chapters by last-30d views (raw, unnormalized) ===")
top30 = sorted(story, key=lambda c: -c["r30"])[:15]
for c in top30:
    print(f"  {c['book']:10s} {c['num']:>3d}  r30={c['r30']:>5,d}  r7={c['r7']:>4,d}  total={c['total']:>6,d}")

print()
print("=== Recent views on Chapter 1 vs. final story chapter (new starters vs. finishers) ===")
ch1 = story_sorted[0]
last_ch = story_sorted[-1]
print(f"  {ch1['book']} {ch1['num']:02d} (first):  r7={ch1['r7']:>4,d}  r14={ch1['r14']:>4,d}  r30={ch1['r30']:>5,d}  total={ch1['total']:>6,d}")
print(f"  {last_ch['book']} {last_ch['num']:02d} (last):   r7={last_ch['r7']:>4,d}  r14={last_ch['r14']:>4,d}  r30={last_ch['r30']:>5,d}  total={last_ch['total']:>6,d}")

print()
print("=== Extras ===")
for c in extras:
    print(f"  {c['title']:24s}  r7={c['r7']:>4,d}  r14={c['r14']:>4,d}  r30={c['r30']:>5,d}  total={c['total']:>6,d}")
