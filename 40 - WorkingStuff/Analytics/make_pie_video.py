"""Animated pie chart: cumulative views SHARE per book, growing day by day
(2026-03-08 .. 2026-09-07)."""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
OUT = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\views_share_pie_growth.mp4")
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

# daily views matrix [book, day] -> cumulative
daily = np.zeros((len(BOOK_ORDER), n_days), dtype=np.int64)
for c in story:
    bi = book_idx[c["book"]]
    for e in c["pv"]:
        daily[bi, day_index[e["date"][:10]]] += e["views"]
cumulative = np.cumsum(daily, axis=1)

fig, ax = plt.subplots(figsize=(8, 8), dpi=110)


def render(day_i):
    ax.clear()
    values = cumulative[:, day_i]
    total = values.sum()
    if total == 0:
        values = np.ones(len(BOOK_ORDER))  # placeholder equal slices before any data
        labels = ["" for _ in BOOK_ORDER]
        autopct = None
    else:
        labels = BOOK_ORDER
        autopct = lambda p: f"{p:.0f}%" if p >= 3 else ""
    colors = [BOOK_COLORS[b] for b in BOOK_ORDER]
    ax.pie(values, labels=labels, colors=colors, autopct=autopct, startangle=90,
           wedgeprops={"edgecolor": "white", "linewidth": 1})
    ax.set_title(f"Cumulative views share per book -- {all_days[day_i]}\ntotal so far: {total:,}")
    ax.set_aspect("equal")


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
