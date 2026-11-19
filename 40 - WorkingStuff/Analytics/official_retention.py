"""Extract official RR analytics: userRetention (May 21 snapshot) and
readerActivityData total views (June 30 snapshot) -- the 'standard' funnel analyses
from HANDOFF.md, using RR's own authoritative aggregates instead of derived proxies.
"""
import json
import re
from pathlib import Path

ANALYTICS = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics")
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

# --- 1. userRetention (May 21) ---
retention_html = (ANALYTICS / "Retention Analytics _ Royal Road-2026-05-21T12-15.html").read_text(encoding="utf-8")
m = re.search(r"var userRetention\s*=\s*(\[.*?\]);", retention_html, re.DOTALL)
retention = json.loads(m.group(1))
print(f"userRetention entries: {len(retention)}  (May 21 2026 snapshot)")
print("First 5:", retention[:5])
print("Last 5:", retention[-5:])

def parse_title(t):
    t = t.replace("up to ", "").strip()
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", t)
    return (mm.group(1).strip(), int(mm.group(2))) if mm else (t, None)

for r in retention:
    r["book"], r["num"] = parse_title(r["title"])

print("\n=== Retention per book (May 21 snapshot): count at first vs last chapter ===")
for b in BOOK_ORDER:
    bch = [r for r in retention if r["book"] == b]
    if not bch:
        continue
    print(f"  {b:10s}  first_ch_count={bch[0]['count']:>4d}  last_ch_count={bch[-1]['count']:>4d}  "
          f"n_ch={len(bch)}  drop_within_book={(bch[-1]['count']-bch[0]['count'])/bch[0]['count']*100:+.1f}%")

grand_total_dropout = sum(r["count"] for r in retention)
print(f"\nTotal entries: {len(retention)}   Grand total dropout headcount (sum of all counts): {grand_total_dropout:,}")

print("\n=== SUM of dropout-count per book (where readers permanently stop, absolute headcount) ===")
for b in BOOK_ORDER:
    bch = [r for r in retention if r["book"] == b]
    if not bch:
        continue
    s = sum(r["count"] for r in bch)
    pct = s / grand_total_dropout * 100
    print(f"  {b:10s}  n_entries={len(bch):>3d}  sum_dropouts={s:>4d}  {pct:>5.1f}% of all tracked dropouts")

extras = [r for r in retention if r["book"] not in BOOK_ORDER]
if extras:
    s = sum(r["count"] for r in extras)
    print(f"  {'Extras':10s}  n_entries={len(extras):>3d}  sum_dropouts={s:>4d}  {s/grand_total_dropout*100:>5.1f}%")


print("\n=== First 20 chapters (Ch1->Ch2 drop etc.) ===")
for r in retention[:20]:
    print(f"  {r['title']:16s}  count={r['count']:>4d}")

# --- 2. readerActivityData (June 30, total views per chapter) ---
general_html = (ANALYTICS / "General Analytics _ Royal Road-2026-06-30T10-00.html").read_text(encoding="utf-8")
m2 = re.search(r"var readerActivityData\s*=\s*(\[.*?\]);", general_html, re.DOTALL)
activity = json.loads(m2.group(1))
for a in activity:
    a["book"], a["num"] = parse_title(a["title"])

print(f"\nreaderActivityData entries: {len(activity)}  (June 30 2026 snapshot)")
print("\n=== Views per book (June 30 total views snapshot) ===")
for b in BOOK_ORDER:
    ach = [a for a in activity if a["book"] == b]
    if not ach:
        continue
    total = sum(a["views"] for a in ach)
    print(f"  {b:10s}  n_ch={len(ach):>3d}  total_views={total:>8,d}  avg/ch={total/len(ach):>7.1f}  "
          f"first_ch={ach[0]['views']:>6,d}  last_ch={ach[-1]['views']:>6,d}")
