"""Fit the expected constant-attrition 'bleed out' decay curve (log-linear in
chapter position) to actual views/day per chapter, then check whether LATER
chapters sit systematically ABOVE that curve (= slow readers arriving late,
adding excess mass beyond pure attrition) or show no such trend (= pure bleed out).
"""
import json
import re
from math import log, exp
from pathlib import Path

SRC = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json")
data = json.loads(SRC.read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    pv = ch["data"]["pageviews"]
    total = sum(e["views"] for e in pv)
    vpd = total / len(pv) if pv else 0
    chapters.append({"idx": idx, "book": book, "num": num, "vpd": vpd})

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
n = len(story)

# Embers has its own extreme early-cliff dynamic (sampling filter) that would bias
# a single global exponential fit. Fit the baseline on Roots-onward only, where a
# constant per-chapter attrition rate is a much more reasonable description
# (established earlier this session: gentle, roughly proportional book-to-book decay).
fit_pool = [c for c in story if c["book"] != "Embers"]
n_fit = len(fit_pool)
base_idx = fit_pool[0]["idx"]

xs = [c["idx"] - base_idx for c in fit_pool]
ys = [log(c["vpd"]) for c in fit_pool]
mx, my = sum(xs) / n_fit, sum(ys) / n_fit
cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / n_fit
varx = sum((x - mx) ** 2 for x in xs) / n_fit
b = cov / varx
a = my - b * mx
print(f"Fitted constant-attrition model (Roots-onward only): ln(views/day) = {a:.4f} + {b:.6f} * (position-in-fit-pool)")
print(f"  => per-chapter attrition rate: {(1 - exp(b)) * 100:.3f}%  (constant-rate bleed-out baseline, post-Embers)")
print(f"  => predicted views/day at Roots-01: {exp(a):.2f}, at Clouds-68: {exp(a + b * (n_fit - 1)):.2f}\n")

for c in story:
    x = c["idx"] - base_idx
    predicted_ln = a + b * x
    c["residual"] = log(c["vpd"]) - predicted_ln  # >0 = actual above fitted decay curve

# --- Residuals binned across the book (40-chapter bins) ---
print("=== Log-residual vs. Roots-onward baseline, 40-chapter bins (Embers shown for context only) ===")
print("(positive = chapter over-performs the pure-attrition baseline; negative = under-performs)")
bin_size = 40
for start in range(0, n, bin_size):
    chunk = story[start:start + bin_size]
    avg_resid = sum(c["residual"] for c in chunk) / len(chunk)
    lo, hi = chunk[0], chunk[-1]
    bar = ("+" if avg_resid > 0 else "-") * int(abs(avg_resid) * 40)
    print(f"  idx {start:>3d}-{start+len(chunk)-1:<3d} ({lo['book']}{lo['num']}..{hi['book']}{hi['num']}): "
          f"avg_log_residual={avg_resid:>+7.4f}  {bar}")

fit_only = [c for c in story if c["book"] != "Embers"]
first_half_avg = sum(c["residual"] for c in fit_only[:n_fit//2]) / (n_fit//2)
second_half_avg = sum(c["residual"] for c in fit_only[n_fit//2:]) / (n_fit - n_fit//2)
print(f"\n(Roots-onward only) First-half avg residual: {first_half_avg:+.4f}")
print(f"(Roots-onward only) Second-half avg residual: {second_half_avg:+.4f}")

# Last 3 books (Fractures/Mirrors/Clouds) vs middle books (Roots/Silence/Echoes) specifically
middle_books = [c for c in story if c["book"] in ("Roots", "Silence", "Echoes")]
late_books = [c for c in story if c["book"] in ("Fractures", "Mirrors", "Clouds")]
print(f"\nRoots+Silence+Echoes avg residual: {sum(c['residual'] for c in middle_books)/len(middle_books):+.4f}")
print(f"Fractures+Mirrors+Clouds avg residual: {sum(c['residual'] for c in late_books)/len(late_books):+.4f}")
print("(if late books are NOT meaningfully above middle books here, that's further evidence against slow-reader arrival)")
