#!/usr/bin/env python3
"""
Categorize Via Negativa instances by severity and type.
"""
import json, re
from pathlib import Path
from collections import Counter, defaultdict

REPORT = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\lektorat_report.json")
CHAPTERS = Path(r"d:\UntilTheEnd\20 - Chapters")

with open(REPORT, encoding='utf-8') as f:
    report = json.load(f)

# Collect all VN instances with full text context
vn_instances = []

for fname, issues in report.items():
    for issue in issues:
        if "Via Negativa" not in issue["category"]:
            continue
        # Find the file
        for book_dir in CHAPTERS.iterdir():
            fp = book_dir / fname
            if fp.exists():
                with open(fp, encoding='utf-8-sig') as f:
                    lines = f.readlines()
                line_num = issue["line"]
                if line_num <= len(lines):
                    full_line = lines[line_num - 1].strip()
                else:
                    full_line = issue["message"]
                vn_instances.append({
                    "file": fname,
                    "book": fname.split("-")[0],
                    "line": line_num,
                    "text": full_line,
                })
                break

# Categorize by pattern type
categories = {
    "stacked_not": [],      # "Not X. Not Y. Not Z." — worst
    "not_because": [],      # "Not because X — because Y"
    "not_to": [],           # "Not to X — to Y"  
    "not_from": [],         # "Not from X — from Y"
    "not_for": [],          # "Not for X"
    "it_wasnt": [],         # "It wasn't X. It was Y."
    "other_negation": [],   # Other patterns
}

for inst in vn_instances:
    t = inst["text"]
    
    # Count consecutive "Not" sentences
    not_count = len(re.findall(r'(?:^|\. )Not\b', t))
    
    if not_count >= 2:
        categories["stacked_not"].append(inst)
    elif re.search(r'Not because\b', t):
        categories["not_because"].append(inst)
    elif re.search(r'Not to\b', t):
        categories["not_to"].append(inst)
    elif re.search(r'Not from\b', t):
        categories["not_from"].append(inst)
    elif re.search(r'Not for\b', t):
        categories["not_for"].append(inst)
    elif re.search(r"(?:wasn't|was not|weren't)", t, re.IGNORECASE):
        categories["it_wasnt"].append(inst)
    else:
        categories["other_negation"].append(inst)

# Print summary
total = sum(len(v) for v in categories.values())
print(f"Via Negativa Instances: {total}\n")

# Per-book distribution
book_counts = Counter(i["book"] for i in vn_instances)
print("Per Book:")
book_names = {"1": "Embers", "2": "Roots", "3": "Silence", "4": "Echoes", "5": "Fractures", "6": "Mirrors"}
for b in sorted(book_counts):
    print(f"  B{b} ({book_names.get(b, '?')}): {book_counts[b]}")

print(f"\nBy Pattern Type (worst → least):")
severity_order = ["stacked_not", "not_because", "it_wasnt", "not_from", "not_to", "not_for", "other_negation"]
labels = {
    "stacked_not": "STACKED: 'Not X. Not Y. Not Z.'",
    "not_because": "NOT BECAUSE: 'Not because X — because Y'",
    "it_wasnt": "IT WASN'T: 'It wasn't X. It was Y.'",
    "not_from": "NOT FROM: 'Not from X — from Y'",
    "not_to": "NOT TO: 'Not to X — to Y'",
    "not_for": "NOT FOR: 'Not for X'",
    "other_negation": "OTHER negation patterns",
}

for cat in severity_order:
    items = categories[cat]
    if not items:
        continue
    print(f"\n  [{len(items):>3}] {labels[cat]}")
    # Show 3 examples
    for inst in items[:3]:
        text = inst["text"][:120]
        print(f"       {inst['file']}:L{inst['line']}: {text}")
    if len(items) > 3:
        print(f"       ... +{len(items)-3} more")

# Write full categorized list for review
output = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\via_negativa_all.txt")
with open(output, 'w', encoding='utf-8') as f:
    for cat in severity_order:
        items = categories[cat]
        if not items:
            continue
        f.write(f"\n{'='*80}\n")
        f.write(f"  {labels[cat]} ({len(items)} instances)\n")
        f.write(f"{'='*80}\n\n")
        for inst in items:
            f.write(f"  {inst['file']}:L{inst['line']}:\n")
            f.write(f"    {inst['text']}\n\n")

print(f"\nFull list saved to: {output.name}")
