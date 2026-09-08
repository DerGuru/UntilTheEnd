"""Sharper test: if readers slowly advance (not bleed out), later chapters should
grow FASTER than Chapter 1's growth rate (fed by trickle-through from the huge
early pools, on top of fresh new starts). Compute each chapter's growth residual
vs. the Ch1 baseline rate, and check whether the residual trends upward with
chapter position (trickle-through signature) or is just flat noise (pure churn).
"""
import json
import re
from pathlib import Path

ANALYTICS = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics")
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

retention_html = (ANALYTICS / "Retention Analytics _ Royal Road-2026-05-21T12-15.html").read_text(encoding="utf-8")
m = re.search(r"var userRetention\s*=\s*(\[.*?\]);", retention_html, re.DOTALL)
may21 = json.loads(m.group(1))


def parse_title(t):
    t = t.replace("up to ", "").strip()
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", t)
    return (mm.group(1).strip(), int(mm.group(2))) if mm else (t, None)


may21_list = []
for r in may21:
    book, num = parse_title(r["title"])
    may21_list.append({"book": book, "num": num, "count": r["count"]})

SNAPSHOT = Path(
    r"c:\Users\JakofHe\AppData\Roaming\Code\User\workspaceStorage\2b686f337a99865772cdd545647f1805"
    r"\GitHub.copilot-chat\chat-session-resources\86e3ca1b-be41-4a75-8b26-8daf7faf8714"
    r"\toolu_01MaKbnwr1GxBzAFb329EtA8__vscode-1788786501410\content.txt"
)
text = SNAPSHOT.read_text(encoding="utf-8")
cells = re.findall(r'cell "([^"]*)"', text)
raw_rows = [cells[i:i + 6] for i in range(0, len(cells) - len(cells) % 6, 6)]
today_map = {}
today_order = []
for title, views, retention, members, pct_members, pct_remaining in raw_rows:
    book, num = parse_title(title)
    today_map[(book, num)] = int(members.replace(",", ""))
    today_order.append((book, num))

GROWTH_RATE = 300 / 274  # Ch1 baseline growth, May21 -> Today

# Global chapter index (story order) for a clean x-axis
global_index = {key: i for i, key in enumerate(today_order)}

print("=== Residual = actual_today - (may21_count * Ch1_growth_rate), binned every 40 chapters ===")
residuals = []
for r in may21_list:
    key = (r["book"], r["num"])
    if key not in today_map or key not in global_index:
        continue
    expected = r["count"] * GROWTH_RATE
    actual = today_map[key]
    residuals.append((global_index[key], r["book"], r["num"], r["count"], expected, actual, actual - expected))

residuals.sort(key=lambda t: t[0])
bin_size = 40
for start in range(0, len(residuals), bin_size):
    chunk = residuals[start:start + bin_size]
    total_may = sum(c[3] for c in chunk)
    total_exp = sum(c[4] for c in chunk)
    total_act = sum(c[5] + c[4] for c in chunk)
    resid_sum = sum(c[6] for c in chunk)
    label_lo, label_hi = chunk[0], chunk[-1]
    print(f"  idx {chunk[0][0]:>3d}-{chunk[-1][0]:<3d} ({label_lo[1]}{label_lo[2]}..{label_hi[1]}{label_hi[2]}): "
          f"May21_sum={total_may:>4d}  expected_today={total_exp:>6.1f}  actual_today={total_act:>6.1f}  "
          f"residual={resid_sum:>+6.1f}")

grand_resid = sum(r[6] for r in residuals)
print(f"\nGrand total residual (actual - expected-from-Ch1-rate): {grand_resid:+.1f}")
print(f"(if near 0 with no positional trend => uniform churn, not trickle-through advancement)")

# Correlation of residual with chapter position (global index)
n = len(residuals)
xs = [r[0] for r in residuals]
ys = [r[6] for r in residuals]
mx, my = sum(xs) / n, sum(ys) / n
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n
varx = sum((x - mx) ** 2 for x in xs) / n
slope = cov / varx if varx else 0
print(f"\nLinear trend of residual vs. chapter position: slope={slope:+.4f} per chapter")
print("(positive & meaningfully large slope = later chapters over-perform Ch1-rate => trickle-through advancement)")
print("(near-zero slope = residual is just flat noise => growth is uniform churn, no advancement)")
