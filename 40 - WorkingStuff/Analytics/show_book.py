"""Show per-chapter views for a specific book."""
import re, sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding='utf-8')
m = re.search(r'aria-label="Views".*?fill="none" fill-opacity="0"><path d="(.*?)"', html, re.DOTALL)
points = re.findall(r'[LM]\s*([\d.]+),([\d.]+)', m.group(1))
values = [round((220 - float(y)) * 1200 / 220, 1) for x, y in points]
while len(values) > 1 and values[0] == values[1]:
    values.pop(0)

book = sys.argv[2] if len(sys.argv) > 2 else "embers"
BOOKS = {
    "embers": (0, 66), "roots": (66, 137), "silence": (137, 198),
    "echoes": (198, 255), "fractures": (255, 304), "mirrors": (304, 318),
}
start, end = BOOKS.get(book.lower(), (0, 66))
end = min(end, len(values))

print(f"{book.title()} chapters {start+1}-{end}:")
prev = None
for i in range(start, end):
    v = values[i]
    pct = v / values[0] * 100
    delta = f" ({v - prev:>+.0f})" if prev else ""
    bar = "#" * int(v / 20)
    print(f"  Ch {i-start+1:>2d}: {v:>6.0f}  ({pct:>5.1f}% of ch1){delta:>8s}  {bar}")
    prev = v
