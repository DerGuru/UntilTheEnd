"""Is the second half of Clouds unusually flat compared to its first half -- consistent
with a survivorship effect (readers who made it 350+ chapters in are highly committed
and won't quit in the final stretch)? Uses the same live data already fetched."""
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


def parse(title):
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    return (mm.group(1).strip(), int(mm.group(2))) if mm else (title, None)


rows = []
for d in data:
    b, n = parse(d["title"])
    rows.append({"book": b, "num": n, "views": d["views"]})

clouds = sorted([r for r in rows if r["book"] == "Clouds"], key=lambda r: r["num"])


def linreg_slope_pct(views):
    n = len(views)
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(views) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, views))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else 0
    return slope, mean_y, (slope / mean_y * 100 if mean_y else 0)


half = len(clouds) // 2
first, second = clouds[:half], clouds[half:]

_, m1, p1 = linreg_slope_pct([r["views"] for r in first])
_, m2, p2 = linreg_slope_pct([r["views"] for r in second])
print(f"Clouds 1st half (ch. 1-{half}):  mean={m1:.0f}  slope%/ch={p1:.2f}%")
print(f"Clouds 2nd half (ch. {half+1}-{len(clouds)}): mean={m2:.0f}  slope%/ch={p2:.2f}%")

# Compare against the last-quarter of every other book, for context
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]
by_book = {b: sorted([r for r in rows if r["book"] == b], key=lambda r: r["num"]) for b in BOOK_ORDER}
print("\n=== 2nd-half slope, every book (context) ===")
for b in BOOK_ORDER:
    chs = by_book[b]
    h = len(chs) // 2
    _, mm, pp = linreg_slope_pct([r["views"] for r in chs[h:]])
    print(f"  {b:10s} 2nd-half slope%/ch = {pp:6.2f}%  (mean={mm:.0f}, n={len(chs)-h})")

print("\nRaw Clouds tail (last 15) for a visual sanity check:")
for r in clouds[-15:]:
    print(f"  Clouds-{r['num']:02d}  views={r['views']:>4d}")
