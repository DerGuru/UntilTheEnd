"""Check whether Silence is unusually flat and Echoes unusually steep right after it,
i.e. a genuine slope-change ('kink') at the Silence/Echoes boundary vs. just the
natural continuous decay already established (Echoes has its own gradual ~19-22%
internal decline). Uses fresh LIVE readerActivityData (Sep 24 2026)."""
import json
import re
from pathlib import Path

PATH = Path(
    r"c:\Users\JakofHe\AppData\Roaming\Code\User\workspaceStorage\2b686f337a99865772cdd545647f1805"
    r"\GitHub.copilot-chat\chat-session-resources\86e3ca1b-be41-4a75-8b26-8daf7faf8714"
    r"\toolu_016tsUWbWbE64CuQw8uWp3C9__vscode-1790257520629\content.txt"
)
text = PATH.read_text(encoding="utf-8")
m = re.search(r"Result: (\[.*)", text, re.DOTALL)
data = json.loads(m.group(1))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]


def parse(title):
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    return (mm.group(1).strip(), int(mm.group(2))) if mm else (title, None)


rows = []
for d in data:
    b, n = parse(d["title"])
    rows.append({"book": b, "num": n, "views": d["views"]})

story = [r for r in rows if r["book"] in BOOK_ORDER]
by_book = {b: sorted([r for r in story if r["book"] == b], key=lambda r: r["num"]) for b in BOOK_ORDER}


def linreg_slope_pct(views):
    """Slope as %-of-mean-per-chapter via simple linear regression, so books of
    different chapter counts/absolute-view levels are comparable."""
    n = len(views)
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(views) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, views))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else 0
    return slope, mean_y, (slope / mean_y * 100 if mean_y else 0)


print(f"{'Book':10s} {'n':>4s} {'first':>7s} {'last':>7s} {'mean':>7s} {'slope/ch':>9s} {'slope%/ch':>10s} {'total drop %':>13s}")
for b in BOOK_ORDER:
    views = [r["views"] for r in by_book[b]]
    slope, mean_y, slope_pct = linreg_slope_pct(views)
    total_drop_pct = (views[0] - views[-1]) / views[0] * 100 if views[0] else 0
    print(f"{b:10s} {len(views):4d} {views[0]:7,d} {views[-1]:7,d} {mean_y:7,.0f} {slope:9,.2f} {slope_pct:9.2f}% {total_drop_pct:12.1f}%")

# Zoom: last 20 of Silence vs first 20 of Echoes, fit separate local slopes
print("\n=== Local slope check: last 20 Silence vs first 20 Echoes ===")
sil_tail = by_book["Silence"][-20:]
ech_head = by_book["Echoes"][:20]
s_slope, s_mean, s_pct = linreg_slope_pct([r["views"] for r in sil_tail])
e_slope, e_mean, e_pct = linreg_slope_pct([r["views"] for r in ech_head])
print(f"Silence last 20: mean={s_mean:.0f} slope%/ch={s_pct:.2f}%")
print(f"Echoes first 20: mean={e_mean:.0f} slope%/ch={e_pct:.2f}%")

# Compare against ALL other book-to-book boundaries the same way
print("\n=== Same local-slope check at every other transition (last20 vs first20) ===")
for i in range(len(BOOK_ORDER) - 1):
    b1, b2 = BOOK_ORDER[i], BOOK_ORDER[i + 1]
    tail = by_book[b1][-20:] if len(by_book[b1]) >= 20 else by_book[b1]
    head = by_book[b2][:20] if len(by_book[b2]) >= 20 else by_book[b2]
    _, tm, tp = linreg_slope_pct([r["views"] for r in tail])
    _, hm, hp = linreg_slope_pct([r["views"] for r in head])
    print(f"{b1:10s} tail slope%/ch={tp:7.2f}%   ->   {b2:10s} head slope%/ch={hp:7.2f}%")
