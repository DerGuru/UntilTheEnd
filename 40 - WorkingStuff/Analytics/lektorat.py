#!/usr/bin/env python3
"""
Automated editorial linting for Until The End chapters.
Checks against StyleDNA and Writing Rules.
"""
import os, re, sys, json
from pathlib import Path
from collections import Counter

CHAPTERS_DIR = Path(r"d:\UntilTheEnd\20 - Chapters")
BOOK_DIRS = {
    1: "1 - Embers", 2: "2 - Roots", 3: "3 - Silence",
    4: "4 - Echoes", 5: "5 - Fractures", 6: "6 - Mirrors",
}

# ── Severity levels ──
SEV_ERROR = "ERROR"      # Must fix
SEV_WARN  = "WARN"       # Should fix
SEV_INFO  = "INFO"       # Worth reviewing

# ── Pattern definitions ──

# Rule 42: "System" used in-world (not allowed)
SYSTEM_IN_WORLD = re.compile(r'\b[Ss]ystem\b')

# StyleDNA: "taub" should be "abgeklemmt" for Yun's inner state
TAUB_PATTERN = re.compile(r'\bnumb(?:ed|ness|ly)?\b', re.IGNORECASE)

# Rule 30: Via Negativa / Apophasis patterns
VIA_NEGATIVA = re.compile(
    r'(?:Not as a |Not because |Not out of |Not from |'
    r'Not for |Not in |Not to |Not that I |'
    r'It wasn\'t.*?[.]\s*It was(?:n\'t)?)',
    re.IGNORECASE
)

# Anti-melodrama: Telling emotions directly
EMOTION_TELLING = re.compile(
    r'\bI felt (a )?(wave|surge|rush|pang|stab|flood|jolt) of '
    r'(sadness|grief|pain|anger|rage|fury|joy|happiness|sorrow|despair|dread|fear|horror|love|longing)\b',
    re.IGNORECASE
)

# Simpler emotion telling
SIMPLE_TELLING = re.compile(
    r'\bI felt (sad|angry|happy|afraid|scared|terrified|hopeless|hopeful|guilty|ashamed|proud|lonely)\b',
    re.IGNORECASE
)

# Excessive dialog tags (anything beyond said/asked + simple adverbs)
FANCY_TAGS = re.compile(
    r'(?:whispered|murmured|growled|hissed|breathed|exclaimed|declared|announced|stammered|'
    r'snarled|snapped|barked|shouted|yelled|screamed|cried out|pleaded|begged|whimpered|'
    r'croaked|rasped|choked out)'
    r'(?:\s+(?:softly|harshly|gently|quietly|loudly|angrily|sadly|bitterly|coldly))?',
    re.IGNORECASE
)

# Anthropomorphism: Nature/objects with human intent
ANTHROPOMORPHISM = re.compile(
    r'(?:the (?:wind|sun|moon|stars?|rain|river|mountain|tree|forest|sky|clouds?|stones?|ground|earth|fire|flames?|darkness|light|shadows?|silence|night|dawn|dusk))\s+'
    r'(?:wanted|wished|hoped|feared|decided|chose|refused|tried|knew|thought|believed|remembered|forgot|judged|watched.*?with|'
    r'seemed to (?:want|wish|hope|fear|decide|choose|refuse|try|know|think|believe|remember|forget|judge))',
    re.IGNORECASE
)

# Doubled words: "the the", "and and", etc.
DOUBLED_WORDS = re.compile(r'\b(\w+)\s+\1\b', re.IGNORECASE)

# Missing closing quotes (line ends mid-dialog)
# Heuristic: odd number of " on a line with dialog
ORPHAN_QUOTE = re.compile(r'^[^"]*"[^"]*$')

# Common typos/grammar issues in English fiction
COMMON_TYPOS = [
    (re.compile(r'\b(teh|hte|adn|taht|waht|jsut|hwo|whcih|thier|recieve|seperate|definately|occured|untill|alot)\b', re.IGNORECASE), "Common typo"),
    (re.compile(r'\s,'), "Space before comma"),
    (re.compile(r'\s\.(?!\.\.)'), "Space before period"),
    (re.compile(r'[^.!?]\s*\n\s*[a-z]'), None),  # Disabled: too many false positives with markdown
    (re.compile(r',,'), "Double comma"),
    (re.compile(r'\.\.(?!\.)'), "Double period (not ellipsis)"),
    (re.compile(r'  '), "Double space"),
]

# Sentence too long (>50 words) - flag for review
LONG_SENTENCE = 60  # words

# Repeated words in same paragraph (unintentional)
REPEAT_THRESHOLD = 3  # same non-trivial word 3+ times in one paragraph

# Words to ignore in repetition check
STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'shall', 'can', 'not', 'no', 'nor',
    'so', 'yet', 'both', 'each', 'all', 'any', 'few', 'more', 'most',
    'some', 'such', 'than', 'too', 'very', 'just', 'about', 'above',
    'after', 'again', 'against', 'before', 'below', 'between', 'during',
    'into', 'through', 'under', 'until', 'up', 'down', 'out', 'off',
    'over', 'then', 'once', 'here', 'there', 'when', 'where', 'why',
    'how', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
    'those', 'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'you',
    'your', 'yours', 'he', 'him', 'his', 'she', 'her', 'hers', 'it',
    'its', 'they', 'them', 'their', 'theirs', 'if', 'it', 'like',
    'said', 'back', 'one', 'didn', 'don', 'wasn', 'hadn', 'couldn',
    'wouldn', 'isn', 'aren', 'weren', 'hasn', 'won', 'even', 'still',
    'now', 'only', 'much', 'also', 'well', 'way', 'own', 'other',
    'right', 'same', 'make', 'made', 'let', 'get', 'got', 'been',
    'come', 'came', 'went', 'go', 'know', 'knew', 'see', 'saw',
    'take', 'took', 'give', 'gave', 'tell', 'told', 'think', 'thought',
    'look', 'looked', 'say', 'turn', 'turned', 'around', 'long',
    'something', 'nothing', 'everything', 'anything', 'someone',
    'enough', 'never', 'always', 'already', 'ever', 'without',
}

# ── Analysis functions ──

def check_paragraph_repeats(para, line_num):
    """Check for unintentional word repetition within a paragraph."""
    issues = []
    words = re.findall(r"[a-z']+", para.lower())
    words = [w for w in words if w not in STOP_WORDS and len(w) > 3]
    counts = Counter(words)
    for word, count in counts.items():
        if count >= REPEAT_THRESHOLD:
            issues.append((line_num, SEV_INFO, "Repetition",
                          f"'{word}' appears {count}x in paragraph"))
    return issues

def check_long_sentences(text, line_num):
    """Flag sentences over LONG_SENTENCE words."""
    issues = []
    # Split on sentence-ending punctuation
    sentences = re.split(r'[.!?]+', text)
    for sent in sentences:
        words = sent.split()
        if len(words) > LONG_SENTENCE:
            preview = ' '.join(words[:10]) + '...'
            issues.append((line_num, SEV_INFO, "Long sentence",
                          f"{len(words)} words: \"{preview}\""))
    return issues

def check_chapter_opening(lines):
    """Rule 50: Soft chapter openings, not isolated one-sentence hooks."""
    issues = []
    # Find first non-empty line
    first_content = ""
    first_line = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped and not stripped.startswith('#'):
            first_content = stripped
            first_line = i + 1
            break
    
    if first_content:
        # Check if it's a very short isolated sentence (potential hook)
        words = first_content.split()
        # Check if next non-empty line is separated by blank line (isolated)
        next_content_idx = None
        for j in range(first_line, len(lines)):
            if lines[j].strip():
                next_content_idx = j
                break
        
        if len(words) <= 8 and next_content_idx and next_content_idx > first_line:
            # Short first sentence followed by blank line = potential isolated hook
            issues.append((first_line, SEV_INFO, "Chapter opening",
                          f"Short isolated opener ({len(words)} words): \"{first_content}\""))
    return issues

def check_event_reflection_ratio(text):
    """Rule 31: Event:Reflection ratio should be 1:2 (more event than reflection)."""
    # Heuristic: dialog lines + action lines vs. reflection paragraphs
    lines = text.split('\n')
    dialog_lines = sum(1 for l in lines if '"' in l)
    total_lines = sum(1 for l in lines if l.strip())
    if total_lines == 0:
        return []
    
    dialog_ratio = dialog_lines / total_lines
    # If less than 20% dialog/action in a chapter, might be too introspective
    if dialog_ratio < 0.10 and total_lines > 20:
        return [(1, SEV_INFO, "Pacing",
                f"Very low dialog ratio ({dialog_ratio:.0%}). Check event:reflection balance.")]
    return []

def lint_chapter(filepath):
    """Run all checks on a single chapter file."""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8-sig') as f:
            text = f.read()
    except Exception as e:
        return [(0, SEV_ERROR, "File", f"Cannot read: {e}")]
    
    lines = text.split('\n')
    
    # Line-level checks
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
            
        # System in-world
        if SYSTEM_IN_WORLD.search(stripped):
            # Exclude if it's clearly not in-world (e.g., "nervous system", "solar system")
            if not re.search(r'(?:nervous|solar|digestive|immune|root|meridian|circulatory)\s+system', stripped, re.IGNORECASE):
                issues.append((i, SEV_WARN, "Rule 42: System",
                              f"'System' used: \"{stripped[:80]}\""))
        
        # Numb/taub pattern
        m = TAUB_PATTERN.search(stripped)
        if m:
            issues.append((i, SEV_INFO, "StyleDNA: numb→abgeklemmt",
                          f"'{m.group()}' found — check if Yun's inner state: \"{stripped[:80]}\""))
        
        # Via Negativa
        m = VIA_NEGATIVA.search(stripped)
        if m:
            issues.append((i, SEV_WARN, "Rule 30: Via Negativa",
                          f"\"{stripped[:100]}\""))
        
        # Emotion telling
        m = EMOTION_TELLING.search(stripped)
        if m:
            issues.append((i, SEV_WARN, "Show don't tell",
                          f"Emotion telling: \"{stripped[:80]}\""))
        m = SIMPLE_TELLING.search(stripped)
        if m:
            issues.append((i, SEV_WARN, "Show don't tell",
                          f"Simple emotion telling: \"{stripped[:80]}\""))
        
        # Fancy dialog tags
        m = FANCY_TAGS.search(stripped)
        if m:
            # Only flag if it's actually a dialog tag context (after closing quote)
            if re.search(r'["\u201d]\s*' + re.escape(m.group()), stripped):
                issues.append((i, SEV_INFO, "Dialog tags",
                              f"Fancy tag '{m.group()}': \"{stripped[:80]}\""))
        
        # Anthropomorphism
        m = ANTHROPOMORPHISM.search(stripped)
        if m:
            issues.append((i, SEV_WARN, "Rule 48: Anthropomorphism",
                          f"\"{stripped[:100]}\""))
        
        # Doubled words
        m = DOUBLED_WORDS.search(stripped)
        if m:
            word = m.group(1).lower()
            if word not in {'that', 'had', 'very', 'so', 'now', 'no'}:
                issues.append((i, SEV_ERROR, "Doubled word",
                              f"'{m.group()}': \"{stripped[:80]}\""))
        
        # Common typos
        for pattern, label in COMMON_TYPOS:
            if label is None:
                continue
            m = pattern.search(stripped)
            if m:
                issues.append((i, SEV_ERROR if label == "Common typo" else SEV_WARN,
                              f"Typo: {label}",
                              f"\"{stripped[:80]}\""))
        
        # Long sentences
        issues.extend(check_long_sentences(stripped, i))
    
    # Paragraph-level checks
    paragraphs = text.split('\n\n')
    line_offset = 1
    for para in paragraphs:
        para_stripped = para.strip()
        if para_stripped and not para_stripped.startswith('#'):
            issues.extend(check_paragraph_repeats(para_stripped, line_offset))
        line_offset += para.count('\n') + 2  # +2 for the \n\n separator
    
    # Chapter-level checks
    issues.extend(check_chapter_opening(lines))
    issues.extend(check_event_reflection_ratio(text))
    
    return issues

def get_book_chapters(book_num):
    """Get all chapter files for a book, sorted."""
    book_dir = CHAPTERS_DIR / BOOK_DIRS[book_num]
    if not book_dir.exists():
        return []
    files = sorted(book_dir.glob("*.md"))
    return files

def main():
    all_issues = {}
    totals = {SEV_ERROR: 0, SEV_WARN: 0, SEV_INFO: 0}
    
    books = range(1, 7)  # Books 1-6 (published)
    if len(sys.argv) > 1:
        books = [int(b) for b in sys.argv[1:]]
    
    for book_num in books:
        book_name = BOOK_DIRS.get(book_num, f"Book {book_num}")
        chapters = get_book_chapters(book_num)
        print(f"\n{'='*60}")
        print(f"  BOOK {book_num}: {book_name} ({len(chapters)} chapters)")
        print(f"{'='*60}")
        
        book_issues = {SEV_ERROR: 0, SEV_WARN: 0, SEV_INFO: 0}
        
        for ch_path in chapters:
            issues = lint_chapter(ch_path)
            if issues:
                all_issues[ch_path.name] = issues
                for _, sev, _, _ in issues:
                    book_issues[sev] += 1
                    totals[sev] += 1
                
                # Only print ERROR and WARN
                important = [i for i in issues if i[1] in (SEV_ERROR, SEV_WARN)]
                if important:
                    print(f"\n  {ch_path.name}:")
                    for line, sev, cat, msg in important:
                        print(f"    L{line:>4} [{sev}] {cat}: {msg}")
        
        print(f"\n  Book {book_num} totals: {book_issues[SEV_ERROR]} errors, "
              f"{book_issues[SEV_WARN]} warnings, {book_issues[SEV_INFO]} info")
    
    # Summary
    print(f"\n{'='*60}")
    print(f"  TOTAL across all books:")
    print(f"    {totals[SEV_ERROR]} ERRORS (must fix)")
    print(f"    {totals[SEV_WARN]} WARNINGS (should fix)")
    print(f"    {totals[SEV_INFO]} INFO (review)")
    print(f"{'='*60}")
    
    # Write full report to file
    report_path = Path(r"d:\UntilTheEnd\40 - WorkingStuff\Analytics\lektorat_report.json")
    report = {}
    for fname, issues in all_issues.items():
        report[fname] = [{"line": l, "severity": s, "category": c, "message": m}
                         for l, s, c, m in issues]
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    print(f"\n  Full report (incl. INFO) saved to: {report_path.name}")

if __name__ == "__main__":
    main()
