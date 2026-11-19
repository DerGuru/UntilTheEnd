"""Full analysis of the LIVE (today, Sep 7 2026) RR retention table:
book-level views/dropout aggregates, compared against the May 21 / June 30
snapshots used earlier this session, to see what changed since.
"""
import re
from pathlib import Path

SNAPSHOT = Path(
    r"c:\Users\JakofHe\AppData\Roaming\Code\User\workspaceStorage\2b686f337a99865772cdd545647f1805"
    r"\GitHub.copilot-chat\chat-session-resources\86e3ca1b-be41-4a75-8b26-8daf7faf8714"
    r"\toolu_01MaKbnwr1GxBzAFb329EtA8__vscode-1788786501410\content.txt"
)
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

text = SNAPSHOT.read_text(encoding="utf-8")
cells = re.findall(r'cell "([^"]*)"', text)
raw_rows = [cells[i:i + 6] for i in range(0, len(cells) - len(cells) % 6, 6)]


def parse_int(s):
    return int(s.replace(",", "").strip())


def parse_pct(s):
    # strip icon char + extra number, keep the leading percentage (capped-at-100 value)
    m = re.match(r"([\d.]+)%", s.strip())
    return float(m.group(1)) if m else None


rows = []
for title, views, retention, members, pct_members, pct_remaining in raw_rows:
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", title)
    book, num = (mm.group(1).strip(), int(mm.group(2))) if mm else (title.strip(), None)
    rows.append({
        "title": title, "book": book, "num": num,
        "views": parse_int(views), "retention_pct": parse_pct(retention),
        "members": parse_int(members), "pct_members": parse_pct(pct_members),
        "pct_remaining": parse_pct(pct_remaining),
    })

story = [r for r in rows if r["book"] in BOOK_ORDER]
extras = [r for r in rows if r["book"] not in BOOK_ORDER]

print(f"Total rows: {len(rows)}  (story: {len(story)}, extras: {len(extras)})\n")

print("=== LIVE (today) book-level aggregates ===")
grand_views = sum(r["views"] for r in story)
grand_members = sum(r["members"] for r in story)
for b in BOOK_ORDER:
    bch = [r for r in story if r["book"] == b]
    tot_views = sum(r["views"] for r in bch)
    tot_members = sum(r["members"] for r in bch)
    print(f"  {b:10s}  n_ch={len(bch):>3d}  total_views={tot_views:>7,d}  avg_views/ch={tot_views/len(bch):>7.1f}  "
          f"sum_dropout_members={tot_members:>4d} ({tot_members/grand_members*100:>5.1f}%)")

print(f"\nGrand total views (all story chapters): {grand_views:,}")
print(f"Grand total dropout-members tracked: {grand_members:,}")

print("\n=== First 10 chapters (today) ===")
for r in story[:10]:
    print(f"  {r['title']:14s} views={r['views']:>6,d}  retention%={r['retention_pct']:>6.2f}  "
          f"members={r['members']:>4d}  %members={r['pct_members']:>6.2f}  %remaining={r['pct_remaining']:>6.2f}")

print("\n=== Extras (today) ===")
for r in extras:
    print(f"  {r['title']:22s} views={r['views']:>6,d}  members={r['members']:>4d}")
