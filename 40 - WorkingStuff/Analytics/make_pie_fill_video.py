"""Animated 'filling' pie chart: circle starts empty and fills up to a full circle
as cumulative views approach the final grand total. Within the filled arc, wedges
are subdivided by book share. Day-by-day growth, 2026-03-08 .. 2026-09-07."""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Circle
import numpy as np
import imageio.v2 as imageio

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
OUT = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\views_share_pie_fill_growth.mp4")
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]
BOOK_COLORS = {
    "Embers": "#e07a5f", "Roots": "#81b29a", "Silence": "#3d405b", "Echoes": "#f2cc8f",
    "Fractures": "#5f6caf", "Mirrors": "#9c6644", "Clouds": "#6a994e",
}

data = json.loads(SRC.read_text(encoding="utf-8"))
chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book = m.group(1).strip() if m else title
    chapters.append({"book": book, "pv": ch["data"]["pageviews"]})

story = [c for c in chapters if c["book"] in BOOK_ORDER]
book_idx = {b: i for i, b in enumerate(BOOK_ORDER)}

all_days = sorted({e["date"][:10] for c in story for e in c["pv"]})
n_days = len(all_days)
day_index = {d: i for i, d in enumerate(all_days)}

daily = np.zeros((len(BOOK_ORDER), n_days), dtype=np.int64)
for c in story:
    bi = book_idx[c["book"]]
    for e in c["pv"]:
        daily[bi, day_index[e["date"][:10]]] += e["views"]
cumulative = np.cumsum(daily, axis=1)
grand_total_final = cumulative[:, -1].sum()

fig, ax = plt.subplots(figsize=(8, 8), dpi=110)


def render(day_i):
    ax.clear()
    values = cumulative[:, day_i]
    day_total = values.sum()
    filled_fraction = day_total / grand_total_final if grand_total_final else 0
    filled_degrees = 360 * filled_fraction

    # empty backdrop circle (what's "not yet accumulated")
    ax.add_patch(Circle((0, 0), 1, facecolor="#eeeeee", edgecolor="#cccccc", linewidth=1))

    # filled arc, subdivided by book share WITHIN the filled portion
    start_angle = 90  # 12 o'clock start, like a clock filling clockwise
    angle = start_angle
    if day_total > 0:
        for b in BOOK_ORDER:
            share = values[book_idx[b]] / day_total
            sweep = share * filled_degrees
            if sweep > 0:
                ax.add_patch(Wedge((0, 0), 1, angle - sweep, angle, facecolor=BOOK_COLORS[b],
                                    edgecolor="white", linewidth=0.8))
            angle -= sweep

    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"{all_days[day_i]}  --  {day_total:,} / {grand_total_final:,} views "
                 f"({filled_fraction*100:.1f}% of final total)")
    handles = [plt.Rectangle((0, 0), 1, 1, color=BOOK_COLORS[b]) for b in BOOK_ORDER]
    ax.legend(handles, BOOK_ORDER, loc="lower center", bbox_to_anchor=(0.5, -0.08), ncol=4, fontsize=8, frameon=False)


writer = imageio.get_writer(OUT, fps=12, codec="libx264", quality=8)
for day_i in range(n_days):
    render(day_i)
    fig.canvas.draw()
    frame = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    writer.append_data(frame)
for _ in range(12):
    writer.append_data(frame)
writer.close()
plt.close(fig)
print(f"Wrote {OUT} ({n_days} days -> {n_days + 12} frames)")
