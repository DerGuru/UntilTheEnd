"""Raw-total-views bleed rate anchored at Roots-01 and Silence-01."""
import json
import re
from pathlib import Path

data = json.loads(Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\ute_pageviews_raw.json").read_text(encoding="utf-8"))
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

chapters = []
for idx, ch in enumerate(data):
    title = ch["title"].strip()
    m = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (m.group(1).strip(), int(m.group(2))) if m else (title, None)
    total = sum(e["views"] for e in ch["data"]["pageviews"])
    chapters.append({"idx": idx, "book": book, "num": num, "total": total})

story = sorted([c for c in chapters if c["book"] in BOOK_ORDER], key=lambda c: c["idx"])
last_ch = story[-1]

for bookname in ["Roots", "Silence"]:
    start = next(c for c in story if c["book"] == bookname and c["num"] == 1)
    span = last_ch["idx"] - start["idx"]
    R = last_ch["total"] / start["total"]
    rate = 1 - R ** (1 / span)
    print(f"{bookname}-01: total={start['total']:,}  span={span} ch  ratio={R*100:.2f}%  bleed={rate*100:.4f}%/ch")

print(f"Clouds-68 total={last_ch['total']:,}")
