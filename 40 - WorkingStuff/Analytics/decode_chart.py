"""Decode chapter views from RR General Analytics SVG chart data."""
import re, sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding='utf-8')

# Book boundaries (cumulative chapter counts)
BOOKS = [
    ("Embers", 1, 66),
    ("Roots", 67, 137),
    ("Silence", 138, 198),
    ("Echoes", 199, 255),
    ("Fractures", 256, 304),
    ("Mirrors", 305, 354),   # only 314 published so far
]

def decode_path(path_d, chart_height, max_val):
    """Extract Y values from SVG path d attribute, convert to data values."""
    # Match L x,y or M x,y pairs
    points = re.findall(r'[LM]\s*([\d.]+),([\d.]+)', path_d)
    values = []
    for x_str, y_str in points:
        y = float(y_str)
        val = (chart_height - y) * max_val / chart_height
        values.append(round(val, 1))
    return values

# --- Views series (aria-label="Views") ---
# Chart height = 220, max = 1200 (from Y-axis labels)
views_match = re.search(r'aria-label="Views".*?fill="none" fill-opacity="0"><path d="(.*?)"', html, re.DOTALL)
if views_match:
    views_path = views_match.group(1)
    views = decode_path(views_path, 220, 1200)
    # First point is duplicated (M + duplicate L), skip duplicates at start
    # Remove leading duplicates
    while len(views) > 1 and views[0] == views[1]:
        views.pop(0)
    
    print(f"=== Chapter Views ({len(views)} chapters) ===\n")
    
    # Per-book summary
    for book_name, ch_start, ch_end in BOOKS:
        ch_end_actual = min(ch_end, len(views))
        if ch_start > len(views):
            break
        book_views = views[ch_start-1:ch_end_actual]
        if not book_views:
            continue
        total = sum(book_views)
        avg = total / len(book_views)
        mn = min(book_views)
        mx = max(book_views)
        print(f"  {book_name:12s}: {len(book_views):3d} ch | total {total:>7,.0f} | avg {avg:>6.1f} | min {mn:>5.0f} | max {mx:>5.0f}")
    
    overall_total = sum(views)
    overall_avg = overall_total / len(views)
    print(f"\n  {'TOTAL':12s}: {len(views):3d} ch | total {overall_total:>7,.0f} | avg {overall_avg:>6.1f}")
    
    # Show drop-off curve (every 50 chapters + last)
    print(f"\n  Drop-off curve:")
    checkpoints = list(range(0, len(views), 50)) + [len(views)-1]
    checkpoints = sorted(set(checkpoints))
    for i in checkpoints:
        pct = views[i] / views[0] * 100 if views[0] > 0 else 0
        print(f"    Ch {i+1:>3d}: {views[i]:>6.0f} ({pct:>5.1f}% of ch1)")
    
    # Retention between books
    print(f"\n  Book-to-book retention:")
    prev_avg = None
    for book_name, ch_start, ch_end in BOOKS:
        ch_end_actual = min(ch_end, len(views))
        if ch_start > len(views):
            break
        book_views = views[ch_start-1:ch_end_actual]
        if not book_views:
            continue
        avg = sum(book_views) / len(book_views)
        if prev_avg:
            ret = avg / prev_avg * 100
            print(f"    {book_name:12s}: avg {avg:>6.1f} ({ret:>5.1f}% of prev)")
        else:
            print(f"    {book_name:12s}: avg {avg:>6.1f} (baseline)")
        prev_avg = avg

# --- Comments series (aria-label="Comments") ---
comments_match = re.search(r'aria-label="Comments".*?fill="none" fill-opacity="0"><path d="(.*?)"', html, re.DOTALL)
if comments_match:
    comments_path = comments_match.group(1)
    comments = decode_path(comments_path, 220, 8)
    while len(comments) > 1 and comments[0] == comments[1]:
        comments.pop(0)
    
    # Find chapters with comments
    commented = [(i+1, c) for i, c in enumerate(comments) if c > 0.5]
    print(f"\n=== Comments ({len(commented)} chapters with comments) ===")
    for ch, c in commented:
        # Find book name
        book = "?"
        for bn, cs, ce in BOOKS:
            if cs <= ch <= ce:
                book = bn
                break
        ch_in_book = ch - next(cs for bn, cs, ce in BOOKS if cs <= ch <= ce) + 1
        print(f"    {book} - {ch_in_book:>2d} (ch {ch:>3d}): {c:.0f} comments")
