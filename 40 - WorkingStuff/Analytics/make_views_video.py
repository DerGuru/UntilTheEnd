"""Animated bar chart: cumulative views per chapter, growing day by day
(2026-03-08 .. 2026-09-07). Renders one frame per tracked day and encodes an mp4.
"""
import json
import re
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import imageio.v2 as imageio

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
OUT = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\views_per_chapter_growth.mp4")
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
    pv = ch["data"]["pageviews"]
    chapters.append({"idx": idx, "title": title, "book": book, "pv": pv})

story = [c for c in chapters if c["book"] in BOOK_ORDER]
n = len(story)
colors = [BOOK_COLORS[c["book"]] for c in story]

all_days = sorted({e["date"][:10] for c in story for e in c["pv"]})
n_days = len(all_days)
day_index = {d: i for i, d in enumerate(all_days)}

# daily views matrix [chapter, day], then cumulative sum along days
daily = np.zeros((n, n_days), dtype=np.int64)
for ci, c in enumerate(story):
    for e in c["pv"]:
        daily[ci, day_index[e["date"][:10]]] += e["views"]
cumulative = np.cumsum(daily, axis=1)

y_max = cumulative[:, -1].max() * 1.05

fig, ax = plt.subplots(figsize=(16, 6), dpi=110)
x = np.arange(n)
bars = ax.bar(x, cumulative[:, 0], color=colors, width=1.0, edgecolor="none")
ax.set_ylim(0, y_max)
ax.set_xlim(-1, n)
ax.set_xlabel("Chapter (Embers 01 -> Clouds 68)")
ax.set_ylabel("Cumulative views")
title_txt = ax.set_title(all_days[0])

# book boundary markers + legend
book_starts = []
prev = None
for i, c in enumerate(story):
    if c["book"] != prev:
        book_starts.append((i, c["book"]))
        prev = c["book"]
for i, name in book_starts:
    ax.axvline(i, color="black", alpha=0.15, linewidth=0.8)
handles = [plt.Rectangle((0, 0), 1, 1, color=BOOK_COLORS[b]) for b in BOOK_ORDER]
ax.legend(handles, BOOK_ORDER, loc="upper right", ncol=4, fontsize=8)
fig.tight_layout()

writer = imageio.get_writer(OUT, fps=12, codec="libx264", quality=8)
STEP = 1
for day_i in range(0, n_days, STEP):
    for rect, h in zip(bars, cumulative[:, day_i]):
        rect.set_height(h)
    title_txt.set_text(f"Cumulative views per chapter -- {all_days[day_i]}")
    fig.canvas.draw()
    frame = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]
    writer.append_data(frame)
# hold last frame for a beat
for _ in range(12):
    writer.append_data(frame)
writer.close()
plt.close(fig)
print(f"Wrote {OUT} ({n_days} days -> {n_days // STEP + 12} frames)")
