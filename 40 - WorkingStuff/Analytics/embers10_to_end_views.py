"""Same Embers-10 -> end retention/bleed-rate question, but using actual views
from the JSON (all-time totals), not the webpage's per-member dropout count.
Shows raw totals, entry-count-normalized (flawed: API omits zero-view days),
and TRUE calendar-day-normalized (correct fix) for comparison.
"""
import json
import re
from datetime import datetime
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

DATASET_END = datetime(2026, 9, 7)

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    pv = ch["data"]["pageviews"]
    total = sum(e["views"] for e in pv)
    first_date = datetime.strptime(pv[0]["date"][:10], "%Y-%m-%d") if pv else DATASET_END
    true_span_days = (DATASET_END - first_date).days + 1
    vpd_entries = total / len(pv) if pv else 0          # flawed: divides by non-zero days only
    vpd_calendar = total / true_span_days               # corrected: divides by true calendar span
    chapters.append({
        "idx": idx, "book": book, "num": num, "total": total,
        "n_entries": len(pv), "true_span_days": true_span_days,
        "vpd_entries": vpd_entries, "vpd_calendar": vpd_calendar,
    })

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
e10 = next(c for c in story if c["book"] == "Embers" and c["num"] == 10)
last3 = story[-3:]
last_ch = story[-1]

print(f"Embers-10:  total={e10['total']:>6,d}  n_entries={e10['n_entries']:>4d}  true_span={e10['true_span_days']:>4d}d  "
      f"vpd(entries)={e10['vpd_entries']:.2f}  vpd(calendar)={e10['vpd_calendar']:.2f}")
print(f"Clouds-68:  total={last_ch['total']:>6,d}  n_entries={last_ch['n_entries']:>4d}  true_span={last_ch['true_span_days']:>4d}d  "
      f"vpd(entries)={last_ch['vpd_entries']:.2f}  vpd(calendar)={last_ch['vpd_calendar']:.2f}")
last3_total = sum(c['total'] for c in last3) / 3
last3_vpd_cal = sum(c['vpd_calendar'] for c in last3) / 3
print(f"Last 3 chapters avg:  total={last3_total:>6,.1f}   vpd(calendar)={last3_vpd_cal:>6.2f}")

span = last_ch["idx"] - e10["idx"]
print(f"\nSpan Embers-10 -> Clouds-68: {span} chapters\n")

for label, num, denom in [
    ("RAW TOTAL (all-time)", last_ch["total"], e10["total"]),
    ("RAW TOTAL, last-3 avg", last3_total, e10["total"]),
    ("ENTRY-NORMALIZED (flawed, omits zero-days)", last_ch["vpd_entries"], e10["vpd_entries"]),
    ("CALENDAR-NORMALIZED (corrected)", last_ch["vpd_calendar"], e10["vpd_calendar"]),
    ("CALENDAR-NORMALIZED, last-3 avg", last3_vpd_cal, e10["vpd_calendar"]),
]:
    R = num / denom
    rate = 1 - R ** (1 / span)
    print(f"{label}:")
    print(f"  ratio = {R*100:.2f}%   implied constant bleed rate = {rate*100:.4f}%/chapter\n")

print("--- Same calc anchored at Roots-01 instead (post-Embers) ---")
roots1 = next(c for c in story if c["book"] == "Roots" and c["num"] == 1)
span2 = last_ch["idx"] - roots1["idx"]
R_total = last_ch["total"] / roots1["total"]
R_cal = last_ch["vpd_calendar"] / roots1["vpd_calendar"]
print(f"Roots-01: total={roots1['total']:,}  vpd(calendar)={roots1['vpd_calendar']:.2f}  true_span={roots1['true_span_days']}d")
print(f"RAW TOTAL ratio Roots-01->Clouds-68: {R_total*100:.2f}%  bleed={100*(1-R_total**(1/span2)):.4f}%/ch")
print(f"CALENDAR-NORM ratio Roots-01->Clouds-68: {R_cal*100:.2f}%  bleed={100*(1-R_cal**(1/span2)):.4f}%/ch")
