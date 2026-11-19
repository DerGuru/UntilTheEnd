import re, json

with open('40 - WorkingStuff/Analytics/General Analytics _ Royal Road-2026-04-13T11-50.html', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'readerActivityData\s*=\s*(\[.*?\]);', content, re.DOTALL)
data = json.loads(m.group(1))
print(f"Chapters: {len(data)}")
total = sum(ch.get('views', 0) for ch in data)
print(f"Total views: {total}")
print()
print("First 5:")
for ch in data[:5]:
    t = ch.get('title', '?')[:35]
    v = ch.get('views', 0)
    print(f"  {t:35s} {v:>5}")
print()
print("Last 10:")
for ch in data[-10:]:
    t = ch.get('title', '?')[:35]
    v = ch.get('views', 0)
    print(f"  {t:35s} {v:>5}")
