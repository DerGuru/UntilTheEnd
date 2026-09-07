"""Fine-grained check: is the Echoes->Fractures activity drop gradual (in-book fatigue)
or a discontinuity at the book boundary (structural/motor-shift effect)?
"""
import json
import re
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
    chapters.append({"idx": idx, "title": title, "book": book, "num": num, "pv": pv})

last_ts = max(e["unixtime"] for c in chapters for e in c["pv"])

def recent_sum(pv, days):
    cutoff = last_ts - days * 86400
    return sum(e["views"] for e in pv if e["unixtime"] >= cutoff)

for c in chapters:
    c["r30"] = recent_sum(c["pv"], 30)

story = [c for c in chapters if c["book"] in BOOK_ORDER]
story.sort(key=lambda c: c["idx"])

echoes = [c for c in story if c["book"] == "Echoes"]
fractures = [c for c in story if c["book"] == "Fractures"]
silence_tail = [c for c in story if c["book"] == "Silence"][-10:]
mirrors_head = [c for c in story if c["book"] == "Mirrors"][:10]

def rolling(seq, key, window=5):
    vals = [c[key] for c in seq]
    out = []
    for i in range(len(vals)):
        lo = max(0, i - window // 2)
        hi = min(len(vals), i + window // 2 + 1)
        out.append(sum(vals[lo:hi]) / (hi - lo))
    return out

print("--- Silence tail (last 10) ---")
for c in silence_tail:
    print(f"  {c['book']:9s} {c['num']:>3d}  r30={c['r30']:>4d}")

print("\n--- Echoes (all, with 5-ch rolling avg) ---")
roll = rolling(echoes, "r30")
for c, r in zip(echoes, roll):
    print(f"  {c['book']:9s} {c['num']:>3d}  r30={c['r30']:>4d}   roll={r:>5.1f}")

print("\n--- Fractures (all, with 5-ch rolling avg) ---")
roll = rolling(fractures, "r30")
for c, r in zip(fractures, roll):
    print(f"  {c['book']:9s} {c['num']:>3d}  r30={c['r30']:>4d}   roll={r:>5.1f}")

print("\n--- Mirrors head (first 10) ---")
for c in mirrors_head:
    print(f"  {c['book']:9s} {c['num']:>3d}  r30={c['r30']:>4d}")

# --- Linear regression: fit trend on Echoes only, extrapolate into Fractures ---
def linreg(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    slope = num / den if den else 0
    intercept = my - slope * mx
    return slope, intercept

xs_e = list(range(len(echoes)))
ys_e = [c["r30"] for c in echoes]
slope_e, intercept_e = linreg(xs_e, ys_e)
print(f"\nEchoes internal trend: slope={slope_e:+.3f} views/chapter per chapter, "
      f"start~{intercept_e:.1f}, end~{intercept_e + slope_e*(len(echoes)-1):.1f}")

# Extrapolate the Echoes trend forward into Fractures' chapter positions
xs_f_extrap = list(range(len(echoes), len(echoes) + len(fractures)))
predicted_fractures = [intercept_e + slope_e * x for x in xs_f_extrap]
actual_fractures = [c["r30"] for c in fractures]

print("\n--- Predicted (Echoes trend continued) vs Actual, first 15 Fractures chapters ---")
for c, pred, act in list(zip(fractures, predicted_fractures, actual_fractures))[:15]:
    gap = act - pred
    print(f"  {c['book']:9s} {c['num']:>3d}  predicted={pred:>6.1f}  actual={act:>4d}  gap={gap:>+6.1f}")

avg_pred_first10 = sum(predicted_fractures[:10]) / 10
avg_act_first10 = sum(actual_fractures[:10]) / 10
print(f"\nAvg predicted (first 10 Fractures ch, Echoes-trend extrapolation): {avg_pred_first10:.1f}")
print(f"Avg actual   (first 10 Fractures ch):                              {avg_act_first10:.1f}")
print(f"Unexplained extra drop at the boundary: {avg_pred_first10 - avg_act_first10:+.1f} views/chapter "
      f"({(avg_pred_first10 - avg_act_first10)/avg_pred_first10*100:.0f}% below trend-line expectation)")

# Also: where inside Echoes does the decline actually start? Split into thirds.
third = len(echoes) // 3
t1 = sum(c["r30"] for c in echoes[:third]) / third
t2 = sum(c["r30"] for c in echoes[third:2*third]) / third
t3 = sum(c["r30"] for c in echoes[2*third:]) / (len(echoes) - 2*third)
print(f"\nEchoes in thirds: first={t1:.1f}  middle={t2:.1f}  last={t3:.1f}")
