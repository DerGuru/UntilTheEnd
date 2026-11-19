"""Static bar chart: site-wide daily views, one bar per day (2026-03-08 .. 2026-09-07)."""
import json
from pathlib import Path
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_sitewide_pageviews_full.json")
OUT = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\daily_views_bar_chart.png")

records = json.loads(SRC.read_text(encoding="utf-8"))
dates = [datetime.strptime(r["date"], "%Y-%m-%d") for r in records]
views = [r["views"] for r in records]

fig, ax = plt.subplots(figsize=(20, 6), dpi=120)
ax.bar(dates, views, color="#337ab7", width=1.0)
ax.set_title(f"UTE -- Site-wide daily views ({dates[0].strftime('%Y-%m-%d')} to {dates[-1].strftime('%Y-%m-%d')})")
ax.set_xlabel("Date")
ax.set_ylabel("Views")
ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO, interval=2))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
fig.autofmt_xdate(rotation=45)
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT)
print(f"Wrote {OUT}")
