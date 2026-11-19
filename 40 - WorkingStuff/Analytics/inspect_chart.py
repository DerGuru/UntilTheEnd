"""Inspect flot-line-chart-multi SVG for pageview data."""
from pathlib import Path
import re, sys

html = Path(sys.argv[1]).read_text(encoding='utf-8')

idx = html.find('id="flot-line-chart-multi"')
print(f"flot-line-chart-multi at position: {idx}")

chunk = html[idx:idx+200000]

# Find ALL tooltip groups - look for groups with visibility attributes
tooltip_groups = re.findall(r'role="tooltip"(.*?)</g></g></g>', chunk, re.DOTALL)
print(f"Tooltip groups: {len(tooltip_groups)}")

for i, tg in enumerate(tooltip_groups):
    tspans = re.findall(r'<tspan>([^<]+)</tspan>', tg)
    if tspans:
        print(f"  Tooltip {i}: {tspans}")

# Find ALL tspan content in the chart
print("\n--- All tspans ---")
tspans = re.findall(r'<tspan>([^<]+)</tspan>', chunk)
for t in tspans:
    print(f"  {t}")

# Look at the chart data structure
print("\n--- aria-label groups ---")
labels = re.findall(r'aria-label="([^"]+)"', chunk)
for l in labels:
    print(f"  {l}")
