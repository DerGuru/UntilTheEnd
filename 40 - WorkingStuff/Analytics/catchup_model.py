"""Model chapter views considering reader arrival over time + log-normal reading speed.

Separates true attrition from 'still catching up' effect.
Log-normal is natural for reading speed: always positive, right-skewed (binge-reader tail).
Uses only stdlib + numpy (no scipy).
"""
import numpy as np
from math import erf, sqrt, log, exp
from pathlib import Path
import re, json, sys

def norm_cdf(x, mu=0, sigma=1):
    """Normal CDF using math.erf."""
    return 0.5 * (1 + erf((x - mu) / (sigma * sqrt(2))))

def lognorm_cdf(x, mu_ln, sigma_ln):
    """Log-normal CDF. P(X <= x) where ln(X) ~ N(mu_ln, sigma_ln).
    mu_ln = ln(median), sigma_ln = shape parameter.
    """
    if x <= 0:
        return 0.0
    return norm_cdf(log(x), mu_ln, sigma_ln)

# --- 1. Load actual chapter view data ---
html = Path(r'd:\UntilTheEnd\40 - WorkingStuff\Analytics\General Analytics _ Royal Road-2026-04-21T23-15.html').read_text(encoding='utf-8')
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    m = re.search(r'var readerActivityData\s*=\s*(\[.*?\]);', s, re.DOTALL)
    if m:
        actual_data = json.loads(m.group(1))
        break

actual_views = [ch['views'] for ch in actual_data]
titles = [ch['title'] for ch in actual_data]
n_chapters = len(actual_views)

# --- 2. Daily pageviews (from validated daily_pageviews.py results) ---
# Mar 21 (day 0) to Apr 20 (day 30) = 31 days
daily_views = [
    948, 127, 196, 2853, 797, 1017, 358, 71,     # Mar 21-28
    1492, 1227, 1112, 305, 785, 1887, 220, 311,   # Mar 29 - Apr 5
    2669, 3278, 2430, 4106, 2995, 3121, 2161,     # Apr 6-12
    2816, 3555, 4696, 5230, 4903, 3199, 4528, 4543 # Apr 13-20
]
n_days = len(daily_views)  # 31

# Estimate new reader arrivals proportional to daily views
# Scale so total new readers = Embers Ch01 views (best proxy for unique starters)
total_pv = sum(daily_views)
total_readers = actual_views[0]  # E01 = 1366
arrival_per_day = [v / total_pv * total_readers for v in daily_views]

print(f"Total chapters: {n_chapters}")
print(f"Total estimated unique readers: {total_readers}")
print(f"Pre-trending arrivals (Mar 21-Apr 5): {sum(arrival_per_day[:16]):.0f}")
print(f"Trending arrivals (Apr 6-20): {sum(arrival_per_day[16:]):.0f}")
print()

# --- 3. Vectorized log-normal CDF for numpy arrays ---
def lognorm_cdf_vec(x, mu_ln, sigma_ln):
    """Vectorized log-normal CDF. P(X <= x) where ln(X) ~ N(mu_ln, sigma_ln)."""
    from numpy import log as nlog, sqrt as nsqrt
    safe_x = np.maximum(x, 1e-30)
    return 0.5 * (1 + np.vectorize(erf)((nlog(safe_x) - mu_ln) / (sigma_ln * nsqrt(2))))

# --- 4. Model: expected views (vectorized, log-normal speed) ---
def compute_expected(mu_ln, sigma_ln, arrivals, n_ch, n_days):
    """Expected chapter views with NO attrition, log-normal reading speed."""
    expected = np.zeros(n_ch)
    chapters = np.arange(1, n_ch + 1, dtype=float)
    for day_idx in range(n_days):
        n_readers = arrivals[day_idx]
        days_available = (n_days - 1) - day_idx
        if days_available <= 0:
            expected[0] += n_readers
            continue
        min_speeds = chapters / days_available
        probs = 1.0 - lognorm_cdf_vec(min_speeds, mu_ln, sigma_ln)
        expected += n_readers * probs
    return expected

def compute_with_attrition(mu_ln, sigma_ln, attrition_per_ch, arrivals, n_ch, n_days):
    """Model with catch-up (log-normal) + constant per-chapter attrition."""
    expected = np.zeros(n_ch)
    chapters = np.arange(1, n_ch + 1, dtype=float)
    survival = (1 - attrition_per_ch) ** np.arange(n_ch, dtype=float)
    for day_idx in range(n_days):
        n_readers = arrivals[day_idx]
        days_available = (n_days - 1) - day_idx
        if days_available <= 0:
            expected[0] += n_readers * survival[0]
            continue
        min_speeds = chapters / days_available
        probs = 1.0 - lognorm_cdf_vec(min_speeds, mu_ln, sigma_ln)
        expected += n_readers * probs * survival
    return expected

def loss(params):
    mu_ln, sigma_ln, attrition = params
    if sigma_ln <= 0.1 or sigma_ln > 3.0 or mu_ln < 0 or attrition < 0 or attrition > 0.05:
        return 1e12
    model = compute_with_attrition(mu_ln, sigma_ln, attrition, arrival_per_day, n_chapters, n_days)
    weights = np.array([1.0 / max(1, i**0.3) for i in range(n_chapters)])
    return np.sum(weights * (model - actual_views)**2)

# Grid search over log-normal params
# mu_ln = ln(median speed), sigma_ln = shape
# median speed 5-30 ch/day → mu_ln = ln(5)..ln(30) ≈ 1.6..3.4
# sigma_ln 0.3..2.0 (low=tight, high=wide spread)
print("Fitting log-normal model...")
best_loss = 1e18
best_params = (log(10), 0.8, 0.002)
for median_speed in np.arange(3, 35, 1):
    mu_ln = log(median_speed)
    for sigma_ln in np.arange(0.3, 2.5, 0.05):
        for attr in np.arange(0.0, 0.012, 0.0005):
            l = loss((mu_ln, sigma_ln, attr))
            if l < best_loss:
                best_loss = l
                best_params = (mu_ln, sigma_ln, attr)
mu_ln_fit, sigma_ln_fit, attrition_fit = best_params
median_speed = exp(mu_ln_fit)
mean_speed = exp(mu_ln_fit + sigma_ln_fit**2 / 2)

print(f"\n=== Fitted Parameters (Log-Normal) ===")
print(f"Median reading speed: {median_speed:.1f} ch/day")
print(f"Mean reading speed:   {mean_speed:.1f} ch/day")
print(f"Shape (σ_ln):         {sigma_ln_fit:.2f}")
print(f"  → 68% of readers:  {exp(mu_ln_fit - sigma_ln_fit):.1f} – {exp(mu_ln_fit + sigma_ln_fit):.1f} ch/day")
print(f"  → 95% of readers:  {exp(mu_ln_fit - 2*sigma_ln_fit):.1f} – {exp(mu_ln_fit + 2*sigma_ln_fit):.1f} ch/day")
print(f"Per-chapter attrition: {attrition_fit*100:.3f}%")
print(f"Per-book attrition (60 ch): {(1-(1-attrition_fit)**60)*100:.1f}%")
print(f"Median reader finishes all {n_chapters} ch in {n_chapters/median_speed:.0f} days")
print()

# --- 5. Compute all three curves ---
zero_attrition = compute_expected(mu_ln_fit, sigma_ln_fit, arrival_per_day, n_chapters, n_days)
fitted_model = compute_with_attrition(mu_ln_fit, sigma_ln_fit, attrition_fit, arrival_per_day, n_chapters, n_days)

# --- 6. Output ---
# Book boundaries
books = [
    ("Embers", 0, 66), ("Roots", 66, 137), ("Silence", 137, 198),
    ("Echoes", 198, 255), ("Fractures", 255, 304), ("Mirrors", 304, 332)
]

print(f"{'Ch':>4s}  {'Actual':>6s}  {'NoAttr':>6s}  {'Fitted':>6s}  {'CatchUp%':>8s}  {'Attr%':>6s}  Title")
print("-" * 75)

current_book = ""
for i in range(n_chapters):
    # Book label
    for bname, bstart, bend in books:
        if bstart <= i < bend:
            if bname != current_book:
                current_book = bname
                print(f"\n  --- {bname} ---")
            break
    
    a = actual_views[i]
    z = zero_attrition[i]
    f = fitted_model[i]
    
    # Catch-up effect: what fraction of the "missing" views (vs Ch1) is due to catch-up
    missing_from_ch1 = actual_views[0] - a
    catchup_missing = actual_views[0] - z  # views missing due to catch-up alone
    
    if missing_from_ch1 > 0:
        catchup_pct = min(100, catchup_missing / missing_from_ch1 * 100)
    else:
        catchup_pct = 0
    
    # True attrition component
    attrition_missing = z - a
    if actual_views[0] > 0:
        attr_pct = attrition_missing / actual_views[0] * 100
    else:
        attr_pct = 0
    
    # Only print every 5th chapter + book boundaries + last chapters
    is_book_boundary = any(i == bs or i == be-1 for _, bs, be in books)
    if i % 10 == 0 or is_book_boundary or i < 3 or i >= n_chapters - 3:
        print(f"{i+1:>4d}  {a:>6d}  {z:>6.0f}  {f:>6.0f}  {catchup_pct:>7.1f}%  {attr_pct:>5.1f}%  {titles[i]}")

# --- 7. Summary per book ---
print(f"\n{'='*60}")
print(f"SUMMARY: How much of each book's 'drop' is catch-up vs attrition?\n")
for bname, bstart, bend in books:
    actual_avg = np.mean(actual_views[bstart:bend])
    zero_avg = np.mean(zero_attrition[bstart:bend])
    
    total_drop = actual_views[0] - actual_avg
    catchup_drop = actual_views[0] - zero_avg
    attrition_drop = zero_avg - actual_avg
    
    if total_drop > 0:
        print(f"  {bname:12s}:  actual avg {actual_avg:>5.0f}  |  "
              f"catch-up explains {catchup_drop/total_drop*100:>5.1f}%  |  "
              f"true attrition {attrition_drop/total_drop*100:>5.1f}%  |  "
              f"zero-attrition avg would be {zero_avg:>5.0f}")
    else:
        print(f"  {bname:12s}:  actual avg {actual_avg:>5.0f}")

print(f"\n  Reading speed: LogNormal(median={median_speed:.1f}, σ={sigma_ln_fit:.2f}) ch/day")
print(f"  68% read {exp(mu_ln_fit-sigma_ln_fit):.0f}–{exp(mu_ln_fit+sigma_ln_fit):.0f} ch/day, "
      f"95% read {exp(mu_ln_fit-2*sigma_ln_fit):.0f}–{exp(mu_ln_fit+2*sigma_ln_fit):.0f} ch/day")
print(f"  Median reader finishes all {n_chapters} ch in {n_chapters/median_speed:.0f} days")
