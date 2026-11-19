import re, json
from datetime import datetime, timedelta

f = open(r'd:\UntilTheEnd\40 - WorkingStuff\Analytics\General Analytics _ Royal Road-2026-05-03T22-00.html', 'r', encoding='utf-8')
content = f.read()
f.close()

match = re.search(r'var readerActivityData\s*=\s*(\[.*?\]);', content, re.DOTALL)
data = json.loads(match.group(1))

match_readers = re.search(r'var readers\s*=\s*(\[.*?\]);', content, re.DOTALL)
readers_raw = eval(match_readers.group(1))
readers = [count for _, count in readers_raw]

views = [d['views'] for d in data]
titles = [d['title'] for d in data]
n = len(views)

print(f"Total chapters: {len(data)}")
print(f"First: {titles[0]} = {views[0]} views")
print(f"Last: {titles[-1]} = {views[-1]} views")
print(f"Max: {max(views)}, Min: {min(views)}, Avg: {sum(views)//len(views)}")

# === READER POSITION ANALYSIS ===
# readers[i] = number of readers whose LAST READ chapter is i
# This tells us how many people are "stuck" or "paused" at each chapter
total_readers = sum(readers)
print(f"\n=== LESER-POSITIONEN ===")
print(f"Gesamte tracked readers: {total_readers}")

# Cumulative: readers who have AT LEAST reached chapter i
# = total_readers - sum(readers who stopped before chapter i)
reached = []  # reached[i] = readers who read chapter i (at least)
for i in range(n):
    # Everyone who is currently AT chapter i or beyond
    reached.append(sum(readers[i:]))

print(f"Leser die Kap 1 erreicht haben: {reached[0]}")
print(f"Leser die letztes Kap erreicht haben: {reached[-1]}")

# === BEREINIGUNG: "Echte" Retention vs. "Noch unterwegs" ===
# Trending seit ~24.03. = 40 Tage. Leser kommen mit verschiedenen Geschwindigkeiten.
# Annahme: Lesegeschwindigkeiten variieren (5-20 Kap/Tag)
# 
# Ein Leser der heute bei Kap 200 steht hat:
# - ALLE Kapitel bis 200 gelesen (Views beigetragen)
# - Kapitel 201+ NOCH NICHT gelesen
#
# "Bereinigte Retention" für Kap X = views[X] / reached[X]
# = Wie viel % der Leser, die Kap X erreicht haben, haben es auch gelesen?
# (sollte nahe 100% sein, außer bei echtem Skip/Drop)

print(f"\n=== BEREINIGTE RETENTION (Views / Leser die ankamen) ===")
print(f"{'Kap':>4} | {'Titel':<22} | {'Views':>5} | {'Erreicht':>8} | {'Ratio':>6} | {'Roh-%':>6}")
print("-" * 75)

# Show at key points
key_chapters = [0, 7, 19, 49, 66, 99, 137, 165, 197, 224, 254, 303, 352, n-1]
for i in key_chapters:
    if i < n and reached[i] > 0:
        ratio = views[i] / reached[i]
        raw_pct = views[i] / views[0] * 100
        print(f"{i+1:4d} | {titles[i]:<22} | {views[i]:5d} | {reached[i]:8d} | {ratio:5.2f}x | {raw_pct:5.1f}%")

# === NOCH-UNTERWEGS-KORREKTUR ===
# Die "wahre" Viewzahl, wenn alle aktuellen Leser durchgelesen hätten:
# Projected views = views[i] + Leser die noch nicht bei i angekommen sind
# Leser die noch nicht bei i sind = reached[0] - reached[i] (wenn wir annehmen alle starten)
# Aber besser: projected_retention = views[i] / reached[i]
# "Erwartete Endwerte" = projected_retention[i] * reached[0]

print(f"\n=== PROJEKTION: Wenn alle aktuellen Leser 'fertig' lesen ===")
print(f"(Annahme: Wer bis Kap X kam, liest es auch; Noch-Unterwegs-Leser folgen dem gleichen Pattern)")
print(f"{'Kap':>4} | {'Titel':<22} | {'Jetzt':>5} | {'Proj.':>6} | {'Echte Ret.':>10}")
print("-" * 70)

# Real retention: Of readers who reached chapter X, what % continued to X+1?
# This eliminates the "haven't arrived yet" noise
ch1_reached = reached[0]
for i in key_chapters:
    if i < n and reached[i] > 0:
        # Projected: if all ch1 readers eventually reach this point at the same rate
        real_retention = reached[i] / ch1_reached * 100  # % who actually get here
        projected_views = views[i] * (ch1_reached / reached[i]) if reached[i] > 0 else 0
        print(f"{i+1:4d} | {titles[i]:<22} | {views[i]:5d} | {projected_views:6.0f} | {real_retention:8.1f}%")

# === SCREE: Where do readers ACTUALLY drop out? ===
print(f"\n=== ECHTE DROP-OUT-PUNKTE (Leser die aufhören) ===")
print(f"(Höchste Konzentration von 'letztes gelesenes Kapitel')")
print(f"{'Kap':>4} | {'Titel':<22} | {'Aufgehört':>9} | {'% aller':>7}")
print("-" * 55)

# Top chapters where readers stop (use min of both arrays)
n_readers = min(len(readers), n)
reader_drops = [(i, readers[i], titles[i]) for i in range(n_readers)]
reader_drops.sort(key=lambda x: -x[1])
for idx, count, title in reader_drops[:20]:
    pct = count / total_readers * 100
    if count > 0:
        print(f"{idx+1:4d} | {title:<22} | {count:9d} | {pct:5.1f}%")

# === BINGE-WELLE SICHTBAR MACHEN ===
print(f"\n=== BINGE-WELLE: Leser-Cluster nach Position ===")
# Group readers by book
book_starts_list = []
for i, title in enumerate(titles):
    for book in ["Embers", "Roots", "Silence", "Echoes", "Fractures", "Mirrors", "Clouds"]:
        if book in title and (not book_starts_list or book_starts_list[-1][1] != book):
            book_starts_list.append((i, book))
            break

# Readers currently in each book
for bi in range(len(book_starts_list)):
    start = book_starts_list[bi][0]
    end = book_starts_list[bi+1][0] if bi+1 < len(book_starts_list) else n
    book_name = book_starts_list[bi][1]
    readers_in_book = sum(readers[start:end])
    print(f"  {book_name:10s}: {readers_in_book:4d} Leser gerade dort ({readers_in_book/total_readers*100:.1f}%)")

# === GESCHWINDIGKEITS-SCHÄTZUNG ===
print(f"\n=== LESEGESCHWINDIGKEITS-VERTEILUNG (geschätzt) ===")
# Trending start: 24.03.2026, today: 03.05.2026 = 40 days
# If someone started day 1 and is now at chapter X, they read X/40 chapters/day
trending_days = 40
print(f"Trending seit ~{trending_days} Tagen")
print(f"Wenn Leser am Tag 1 gestartet wären:")
print(f"  Kap 370 (am Front): ~{370/trending_days:.0f} Kap/Tag = Hardcore-Binger")
print(f"  Kap 200 (Echoes):   ~{200/trending_days:.0f} Kap/Tag = Moderater Leser")
print(f"  Kap 100 (Roots):    ~{100/trending_days:.0f} Kap/Tag = Gemütlich")
print(f"  Kap  50 (Embers):   ~{50/trending_days:.0f} Kap/Tag = Gelegenheitsleser")
print(f"\nAber: Neue Leser kommen TÄGLICH dazu (Trending-Effekt)!")
print(f"Viele der Leser bei Kap 50-150 sind vermutlich erst vor 1-2 Wochen eingestiegen.")
