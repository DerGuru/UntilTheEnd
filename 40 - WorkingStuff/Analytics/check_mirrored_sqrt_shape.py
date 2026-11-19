"""Test the user's visual intuition: does the overall Embers->Clouds views-per-chapter
curve fit a mirrored/flipped square-root shape (steep initial decline, progressively
flattening), i.e. views(x) = a - b*sqrt(x), better than e.g. a straight line or
exponential decay? Uses fresh LIVE readerActivityData (Sep 24 2026), all 423 chapters
in true story order (absolute chapter position 1-423)."""
import json
import math
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
    if b in BOOK_ORDER:
        rows.append({"book": b, "num": n, "views": d["views"]})

by_book = {b: sorted([r for r in rows if r["book"] == b], key=lambda r: r["num"]) for b in BOOK_ORDER}
ordered = []
for b in BOOK_ORDER:
    ordered.extend(by_book[b])

xs = list(range(1, len(ordered) + 1))
ys = [r["views"] for r in ordered]
n = len(xs)


def r_squared(y_actual, y_pred):
    mean_y = sum(y_actual) / len(y_actual)
    ss_tot = sum((y - mean_y) ** 2 for y in y_actual)
    ss_res = sum((ya - yp) ** 2 for ya, yp in zip(y_actual, y_pred))
    return 1 - ss_res / ss_tot if ss_tot else 0


# Model A: mirrored sqrt -- y = a - b*sqrt(x)  =>  linear regression of y on sqrt(x)
sx = [math.sqrt(x) for x in xs]
mean_sx, mean_y = sum(sx) / n, sum(ys) / n
b_sqrt = sum((s - mean_sx) * (y - mean_y) for s, y in zip(sx, ys)) / sum((s - mean_sx) ** 2 for s in sx)
a_sqrt = mean_y - b_sqrt * mean_sx
pred_sqrt = [a_sqrt + b_sqrt * s for s in sx]
r2_sqrt = r_squared(ys, pred_sqrt)

# Model B: straight line y = a + b*x
mean_x = sum(xs) / n
b_lin = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys)) / sum((x - mean_x) ** 2 for x in xs)
a_lin = mean_y - b_lin * mean_x
pred_lin = [a_lin + b_lin * x for x in xs]
r2_lin = r_squared(ys, pred_lin)

# Model C: exponential decay -- ln(y) = a + b*x
ly = [math.log(y) for y in ys]
mean_ly = sum(ly) / n
b_exp = sum((x - mean_x) * (l - mean_ly) for x, l in zip(xs, ly)) / sum((x - mean_x) ** 2 for x in xs)
a_exp = mean_ly - b_exp * mean_x
pred_exp = [math.exp(a_exp + b_exp * x) for x in xs]
r2_exp = r_squared(ys, pred_exp)

# Model D: power law -- ln(y) = a + b*ln(x)
lx = [math.log(x) for x in xs]
mean_lx = sum(lx) / n
b_pow = sum((lxx - mean_lx) * (l - mean_ly) for lxx, l in zip(lx, ly)) / sum((lxx - mean_lx) ** 2 for lxx in lx)
a_pow = mean_ly - b_pow * mean_lx
pred_pow = [math.exp(a_pow + b_pow * math.log(x)) for x in xs]
r2_pow = r_squared(ys, pred_pow)

print(f"Model A: y = a - b*sqrt(x)  [mirrored sqrt]   R^2 = {r2_sqrt:.4f}   (a={a_sqrt:.1f}, b={-b_sqrt:.2f})")
print(f"Model B: y = a + b*x        [straight line]    R^2 = {r2_lin:.4f}")
print(f"Model C: y = exp(a+b*x)     [exponential decay] R^2 = {r2_exp:.4f}")
print(f"Model D: y = x^b * exp(a)   [power law]         R^2 = {r2_pow:.4f}")

print("\nSanity check -- predicted vs actual at book-start positions:")
positions = [1, 67, 138, 198, 255, 304, 353]
labels = BOOK_ORDER
for pos, label in zip(positions, labels):
    actual = ys[pos - 1]
    pred = a_sqrt + b_sqrt * math.sqrt(pos)
    print(f"  {label:10s} (chapter #{pos:3d}): actual={actual:5,d}  sqrt-model predicted={pred:7.0f}")
