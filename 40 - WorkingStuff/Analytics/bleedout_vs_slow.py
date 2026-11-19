"""Test 'bleed out' vs 'reading slowly' by comparing the per-chapter dropout-headcount
distribution at two points in time (May 21 vs today/Sep 7, ~3.5 months apart).

If readers are just slow (not gone): early-chapter dropout counts should SHRINK over
time (as slow readers progress past them) while later-chapter counts grow disproportionately.
If it's real bleed-out: the shape stays proportionally similar; growth is just new
readers churning at the same historical points, not old readers advancing.
"""
import json
import re
from pathlib import Path

ANALYTICS = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics")
BOOK_ORDER = ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]

# --- May 21 snapshot (userRetention, dropout headcount per chapter) ---
retention_html = (ANALYTICS / "Retention Analytics _ Royal Road-2026-05-21T12-15.html").read_text(encoding="utf-8")
m = re.search(r"var userRetention\s*=\s*(\[.*?\]);", retention_html, re.DOTALL)
may21 = json.loads(m.group(1))

def parse_title(t):
    t = t.replace("up to ", "").strip()
    mm = re.match(r"^(.*?)\s*-\s*(\d+)\s*$", t)
    return (mm.group(1).strip(), int(mm.group(2))) if mm else (t, None)

may21_map = {}
for r in may21:
    book, num = parse_title(r["title"])
    may21_map[(book, num)] = r["count"]

# --- Today's live snapshot (already parsed from the browser page earlier) ---
SNAPSHOT = Path(
    r"c:\Users\JakofHe\AppData\Roaming\Code\User\workspaceStorage\2b686f337a99865772cdd545647f1805"
    r"\GitHub.copilot-chat\chat-session-resources\86e3ca1b-be41-4a75-8b26-8daf7faf8714"
    r"\toolu_01MaKbnwr1GxBzAFb329EtA8__vscode-1788786501410\content.txt"
)
text = SNAPSHOT.read_text(encoding="utf-8")
cells = re.findall(r'cell "([^"]*)"', text)
raw_rows = [cells[i:i + 6] for i in range(0, len(cells) - len(cells) % 6, 6)]
today_map = {}
for title, views, retention, members, pct_members, pct_remaining in raw_rows:
    book, num = parse_title(title)
    today_map[(book, num)] = int(members.replace(",", ""))

# --- Compare per book: sum of dropout-count May21 vs Today ---
print("=== Sum of dropout-headcount per book: May 21 vs Today (Sep 7) ===")
grand_may, grand_today = sum(may21_map.values()), sum(today_map.values())
for b in BOOK_ORDER:
    may_sum = sum(v for (bk, n), v in may21_map.items() if bk == b)
    today_sum = sum(v for (bk, n), v in today_map.items() if bk == b)
    delta = today_sum - may_sum
    print(f"  {b:10s}  May21={may_sum:>4d} ({may_sum/grand_may*100:>5.1f}%)   "
          f"Today={today_sum:>4d} ({today_sum/grand_today*100:>5.1f}%)   delta={delta:>+5d}")

print(f"\nGrand total: May21={grand_may}  Today={grand_today}  (growth: {(grand_today-grand_may)/grand_may*100:+.1f}%)")

# --- Chapter 1 specifically, and the tail (Fractures/Mirrors/Clouds) ---
print("\n=== Chapter 1 vs second-half-of-series dropout growth ===")
ch1_may, ch1_today = may21_map.get(("Embers", 1), 0), today_map.get(("Embers", 1), 0)
print(f"  Embers-01:  May21={ch1_may}  Today={ch1_today}  growth={(ch1_today-ch1_may)/ch1_may*100:+.1f}%")

tail_books = ["Fractures", "Mirrors", "Clouds"]
tail_may = sum(v for (bk, n), v in may21_map.items() if bk in tail_books)
tail_today = sum(v for (bk, n), v in today_map.items() if bk in tail_books)
print(f"  Fractures+Mirrors+Clouds combined:  May21={tail_may}  Today={tail_today}  "
      f"growth={(tail_today-tail_may)/tail_may*100:+.1f}%")

front_books = ["Embers"]
front_may = sum(v for (bk, n), v in may21_map.items() if bk in front_books)
front_today = sum(v for (bk, n), v in today_map.items() if bk in front_books)
print(f"  Embers alone:                       May21={front_may}  Today={front_today}  "
      f"growth={(front_today-front_may)/front_may*100:+.1f}%")

# --- Did any INDIVIDUAL chapter's dropout count go DOWN (readers advancing past it)? ---
print("\n=== Chapters where dropout-count DECREASED from May21 to Today (would indicate readers advancing past a stall point) ===")
decreased = []
for key in may21_map:
    if key in today_map:
        d = today_map[key] - may21_map[key]
        if d < 0:
            decreased.append((key, may21_map[key], today_map[key], d))
decreased.sort(key=lambda t: t[3])
print(f"Total chapters with decreased count: {len(decreased)} out of {len(may21_map)} tracked in both")
for (book, num), old, new, d in decreased[:20]:
    print(f"  {book} {num:>3d}:  May21={old:>3d}  Today={new:>3d}  delta={d:>+4d}")
