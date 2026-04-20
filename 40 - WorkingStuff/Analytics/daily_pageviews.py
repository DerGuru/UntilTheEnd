"""Reconstruct daily page views from SVG chart in General Analytics HTML."""
from pathlib import Path
import re, sys
from datetime import datetime, timedelta

html = Path(sys.argv[1]).read_text(encoding='utf-8')

# Find the Page Views chart section
m = re.search(r'aria-label="Page Views"(.*?)(?:aria-label="|$)', html, re.DOTALL)
pv_section = m.group(1)

# Extract bar positions (transform="translate(x,y)")
items = re.findall(r'role="listitem"\s*transform="translate\(([\d.]+),([\d.]+)\)"', pv_section)
points = [(float(x), float(y)) for x, y in items]
points.sort()

# Calibration: find tooltip value
tooltip_match = re.search(r'(\d{4}-\d{2}-\d{2}): ([\d,]+)', html)
cal_date = datetime.strptime(tooltip_match.group(1), '%Y-%m-%d')
cal_views = int(tooltip_match.group(2).replace(',', ''))

# X-axis date labels
date_labels = re.findall(r'<tspan>((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+)</tspan>', html)

# Determine start date from x-axis labels or infer from count
# If 31 points, likely covers 31 days ending ~today
n = len(points)
# The last point is the most recent day
end_date = datetime(2026, 4, 19)  # approximate
start_date = end_date - timedelta(days=n-1)

# Find calibration point index
cal_index = (cal_date - start_date).days
if 0 <= cal_index < n:
    cal_y = points[cal_index][1]
else:
    # Try adjusting start date
    for offset in range(-5, 6):
        test_start = start_date + timedelta(days=offset)
        idx = (cal_date - test_start).days
        if 0 <= idx < n:
            start_date = test_start
            cal_index = idx
            cal_y = points[cal_index][1]
            break

# Chart bottom (baseline) - highest y value + small margin
chart_bottom = max(y for _, y in points) + 1.0
scale = cal_views / (chart_bottom - cal_y)

print(f"Chart: {n} days, start {start_date.strftime('%Y-%m-%d')}, calibration: {cal_date.strftime('%Y-%m-%d')}={cal_views} at index {cal_index}")
print(f"Scale: {scale:.1f} views/pixel, chart_bottom={chart_bottom:.1f}")
print()

total = 0
for i, (x, y) in enumerate(points):
    date = start_date + timedelta(days=i)
    views = max(0, (chart_bottom - y) * scale)
    total += views
    marker = ""
    if i == cal_index:
        marker = "  <- calibration"
    print(f"  {date.strftime('%Y-%m-%d %a')}: {views:>6,.0f}{marker}")

print(f"\n  Total: {total:>6,.0f}")
