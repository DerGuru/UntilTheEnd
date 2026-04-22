"""Reconstruct daily page views from SVG chart in General Analytics HTML.

Uses x-axis label positions for correct date mapping and tooltip for calibration.
Bar heights are proportional to views; one tooltip gives the scale factor.
Falls back to --total <views> for calibration when no tooltip is present.
"""
from pathlib import Path
import re, sys
from datetime import datetime, timedelta

# Parse args: script.py <html> [--total <views>]
args = sys.argv[1:]
total_override = None
html_path = None
i = 0
while i < len(args):
    if args[i] == '--total' and i + 1 < len(args):
        total_override = int(args[i + 1])
        i += 2
    elif html_path is None:
        html_path = args[i]
        i += 1
    else:
        i += 1

if html_path is None:
    sys.exit("Usage: daily_pageviews.py <html_file> [--total <total_views>]")

html = Path(html_path).read_text(encoding='utf-8')

# --- 1. Extract bars (position + height) from Page Views SVG ---
pv_start = html.find('aria-label="Page Views"')
next_chart = html.find('aria-label="', pv_start + 30)
if next_chart == -1:
    next_chart = len(html)
pv_section = html[pv_start:next_chart]

bars = re.findall(
    r'role="listitem"\s*transform="translate\(([\d.]+),([\d.]+)\)"[^>]*>'
    r'.*?height="([\d.]+)"',
    pv_section, re.DOTALL
)
bars = [(float(x), float(y), float(h)) for x, y, h in bars]
bars.sort()
n = len(bars)

# --- 2. Map bar x-positions to dates via x-axis labels ---
extended = html[pv_start:pv_start + 200000]

# Find each date tspan, then look backwards for the nearest translate(X,0)
date_re = re.compile(r'<tspan>((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d+)</tspan>')
translate_re = re.compile(r'translate\(([\d.]+),0\)')

axis_labels = []
for dm in date_re.finditer(extended):
    chunk = extended[max(0, dm.start() - 300):dm.start()]
    translates = translate_re.findall(chunk)
    if translates:
        x = float(translates[-1])
        month_day = datetime.strptime(f"2026 {dm.group(1)}", "%Y %b %d")
        axis_labels.append((x, month_day))

if len(axis_labels) >= 2:
    # Use first and last label for linear x→date mapping
    lx1, ld1 = axis_labels[0]
    lx2, ld2 = axis_labels[-1]
    px_per_day = (lx2 - lx1) / (ld2 - ld1).days

    # Compute bar[0] date
    days_from_label1 = (bars[0][0] - lx1) / px_per_day
    start_date = ld1 + timedelta(days=round(days_from_label1))
else:
    sys.exit("Could not find enough x-axis labels for date mapping.")

# --- 3. Calibration from tooltip or --total ---
tooltip_match = re.search(r'(\d{4}-\d{2}-\d{2}): ([\d,]+)', html)
if tooltip_match:
    cal_date = datetime.strptime(tooltip_match.group(1), '%Y-%m-%d')
    cal_views = int(tooltip_match.group(2).replace(',', ''))
    cal_index = (cal_date - start_date).days
    if not (0 <= cal_index < n):
        sys.exit(f"Calibration date {cal_date.date()} outside chart range "
                 f"({start_date.date()} .. {(start_date + timedelta(days=n-1)).date()})")
    cal_height = bars[cal_index][2]
    scale = cal_views / cal_height  # views per pixel of bar height
    cal_method = f"tooltip: {cal_date.strftime('%Y-%m-%d')} = {cal_views:,} (bar[{cal_index}], h={cal_height:.1f})"
elif total_override is not None:
    total_height = sum(h for _, _, h in bars)
    scale = total_override / total_height
    cal_method = f"total override: {total_override:,} views / {total_height:.1f} px = {scale:.2f} views/px"
else:
    sys.exit("No tooltip found for calibration. Use --total <total_views> to calibrate from total.")

# --- 4. Output ---
end_date = start_date + timedelta(days=n - 1)
print(f"Chart: {n} days, {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
print(f"Calibration: {cal_method}")
print(f"Scale: {scale:.2f} views/px")
print()

total = 0
for i, (x, y, h) in enumerate(bars):
    date = start_date + timedelta(days=i)
    views = round(h * scale)
    total += views
    marker = "  <- tooltip" if i == cal_index else ""
    print(f"  {date.strftime('%Y-%m-%d %a')}: {views:>6,}{marker}")

print(f"\n  Total: {total:>6,}")
