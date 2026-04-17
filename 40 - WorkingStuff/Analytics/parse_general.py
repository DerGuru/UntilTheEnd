"""Parse RR General Analytics HTML for daily pageviews and chapter views."""
import re, sys
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding='utf-8')

# --- Daily Page Views (from SVG tooltip tspans) ---
# Pattern: "Page Views" followed by "YYYY-MM-DD: N,NNN"
daily_pv = re.findall(r'Page Views</tspan></text><text[^>]*><tspan>(\d{4}-\d{2}-\d{2}): ([\d,]+)', html)
if daily_pv:
    print("=== Daily Page Views ===")
    total = 0
    for date, views in daily_pv:
        v = int(views.replace(',', ''))
        total += v
        print(f"  {date}: {v:>6,}")
    print(f"  {'TOTAL':>10}: {total:>6,}")

# --- Chapter Views (from SVG tooltip tspans) ---
# Pattern: "Views for" followed by "BookName - N: NNN"
chapter_views = re.findall(r'Views for</tspan></text><text[^>]*><tspan>(.*?): (\d+)', html)
if chapter_views:
    print(f"\n=== Chapter Views ({len(chapter_views)} chapters) ===")
    books = {}
    for name, views in chapter_views:
        v = int(views)
        # Extract book name
        parts = name.rsplit(' - ', 1)
        book = parts[0].strip() if len(parts) == 2 else 'Unknown'
        chap = parts[1].strip() if len(parts) == 2 else name
        if book not in books:
            books[book] = []
        books[book].append((chap, v))
    
    grand_total = 0
    for book, chapters in books.items():
        book_total = sum(v for _, v in chapters)
        grand_total += book_total
        avg = book_total / len(chapters) if chapters else 0
        print(f"\n  {book}: {len(chapters)} ch, {book_total:,} views, avg {avg:.1f}")
        # Show first 3 and last 3
        if len(chapters) > 8:
            for ch, v in chapters[:3]:
                print(f"    Ch {ch:>3}: {v:>5}")
            print(f"    ...")
            for ch, v in chapters[-3:]:
                print(f"    Ch {ch:>3}: {v:>5}")
        else:
            for ch, v in chapters:
                print(f"    Ch {ch:>3}: {v:>5}")
    
    print(f"\n  GRAND TOTAL: {grand_total:,} views across {len(chapter_views)} chapters")
    print(f"  OVERALL AVG: {grand_total/len(chapter_views):.1f}")

# --- Referrer data (from table rows) ---
referrers = re.findall(r'<tr><td>(https?://[^<]+)</td><td>(\d+)</td><td>(\d+)</td></tr>', html)
if referrers:
    print(f"\n=== Top Referrers ===")
    refs = [(url, int(visits), int(pv)) for url, visits, pv in referrers]
    refs.sort(key=lambda x: -x[2])
    for url, visits, pv in refs[:15]:
        # Shorten URL
        short = url.replace('https://www.royalroad.com/', 'rr/')
        if len(short) > 80:
            short = short[:77] + '...'
        print(f"  {pv:>4} pv | {visits:>3} vis | {short}")
