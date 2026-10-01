"""Does Echoes' internal slope change right at its OWN chapter 20/21 mark (the true
pre-tracking vs. live-tracking cutoff, per check_already_live.py's finding that
chapters 1-20 of Echoes were already published before pageview tracking began on
2026-03-07/08), rather than at the Silence/Echoes book boundary? If so, the
'kink' is a tracking artifact, not a real craft/story difference."""
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

echoes = sorted([r for r in rows if r["book"] == "Echoes"], key=lambda r: r["num"])


def linreg_slope_pct(views):
    n = len(views)
    xs = list(range(n))
    mean_x = sum(xs) / n
    mean_y = sum(views) / n
    num = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, views))
    den = sum((x - mean_x) ** 2 for x in xs)
    slope = num / den if den else 0
    return slope, mean_y, (slope / mean_y * 100 if mean_y else 0)


pre = [r["views"] for r in echoes if r["num"] <= 20]
live = [r["views"] for r in echoes if r["num"] > 20]

_, m1, p1 = linreg_slope_pct(pre)
_, m2, p2 = linreg_slope_pct(live)
print(f"Echoes 1-20  (pre-tracking, published before 07.03.): mean={m1:.0f} slope%/ch={p1:.2f}%")
print(f"Echoes 21-57 (live-tracked, published during tracking): mean={m2:.0f} slope%/ch={p2:.2f}%")

print("\nRaw values Echoes 1-25 for visual check:")
for r in echoes[:25]:
    tag = "pre-tracking" if r["num"] <= 20 else "LIVE"
    print(f"  Echoes-{r['num']:02d}  views={r['views']:>4d}  [{tag}]")
