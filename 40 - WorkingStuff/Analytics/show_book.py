"""Show per-chapter views for a specific book."""
import re, sys, json
from pathlib import Path

html = Path(sys.argv[1]).read_text(encoding='utf-8')

# Extract real view counts from readerActivityData JSON
m = re.search(r'var readerActivityData = (\[.*?\]);', html)
data = json.loads(m.group(1))

# Group by book
BOOK_NAMES = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]
books = {}
for ch in data:
    title = ch['title']
    bname = title.rsplit(' - ', 1)[0].strip()
    num = title.rsplit(' - ', 1)[1].strip()
    if bname not in books:
        books[bname] = []
    books[bname].append((num, ch['views']))

book = sys.argv[2] if len(sys.argv) > 2 else "embers"
bkey = next((b for b in books if b.lower() == book.lower()), None)
if not bkey:
    print(f"Book '{book}' not found. Available: {list(books.keys())}")
    sys.exit(1)

chapters = books[bkey]
ch1_views = data[0]['views']  # Embers Ch1 for global %

print(f"{bkey} ({len(chapters)} chapters, {sum(v for _,v in chapters):,} total views, avg {sum(v for _,v in chapters)/len(chapters):.0f}):")
prev = None
for num, v in chapters:
    pct = v / ch1_views * 100
    delta = f" ({v - prev:>+d})" if prev is not None else ""
    bar = "#" * int(v / 20)
    print(f"  Ch {num:>3}: {v:>5}  ({pct:>5.1f}% of E01){delta:>8s}  {bar}")
    prev = v
