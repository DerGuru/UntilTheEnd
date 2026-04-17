"""Extract chapters from RR EPUB and update local markdown files."""
import zipfile
import re
import sys
from pathlib import Path
from html.parser import HTMLParser

EPUB_PATH = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(r"d:\UntilTheEnd\40 - WorkingStuff\Until the End.epub")
CHAPTERS_DIR = Path(r"d:\UntilTheEnd\20 - Chapters")
DRY_RUN = "--dry-run" in sys.argv

# Book folder mapping
BOOK_FOLDERS = {
    "Embers": "1 - Embers",
    "Roots": "2 - Roots",
    "Silence": "3 - Silence",
    "Echoes": "4 - Echoes",
    "Fractures": "5 - Fractures",
    "Mirrors": "6 - Mirrors",
    "Clouds": "7 - Clouds",
}

class HTMLToMarkdown(HTMLParser):
    """Simple HTML to Markdown converter matching UTE chapter style."""
    def __init__(self):
        super().__init__()
        self.result = []
        self.current_tag = None
        self.in_em = False
        self.in_strong = False
        self.skip = False
    
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        if tag == 'em' or tag == 'i':
            self.in_em = True
            self.result.append('*')
        elif tag == 'strong' or tag == 'b':
            self.in_strong = True
            self.result.append('**')
        elif tag == 'br':
            self.result.append('\n')
        elif tag == 'p':
            pass  # handled in endtag
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            pass  # skip chapter titles from HTML
        elif tag in ('head', 'style', 'script', 'title'):
            self.skip = True
    
    def handle_endtag(self, tag):
        if tag == 'em' or tag == 'i':
            self.in_em = False
            self.result.append('*')
        elif tag == 'strong' or tag == 'b':
            self.in_strong = False
            self.result.append('**')
        elif tag == 'p':
            self.result.append('\n\n')
        elif tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            pass
        elif tag in ('head', 'style', 'script', 'title'):
            self.skip = False
        self.current_tag = None
    
    def handle_data(self, data):
        if self.skip:
            return
        # Skip chapter title lines (they're in h tags in the HTML)
        if self.current_tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            return
        self.result.append(data)
    
    def handle_entityref(self, name):
        entities = {'amp': '&', 'lt': '<', 'gt': '>', 'quot': '"', 'apos': "'", 'nbsp': ' '}
        self.result.append(entities.get(name, f'&{name};'))
    
    def handle_charref(self, name):
        if name.startswith('x'):
            self.result.append(chr(int(name[1:], 16)))
        else:
            self.result.append(chr(int(name)))
    
    def get_markdown(self):
        text = ''.join(self.result)
        # Clean up whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]+\n', '\n', text)
        text = text.strip()
        # Ensure consistent line endings
        text = text.replace('\r\n', '\n')
        return text


def html_to_markdown(html_content):
    parser = HTMLToMarkdown()
    parser.feed(html_content)
    return parser.get_markdown()


def parse_toc(epub):
    """Parse toc.ncx to get ordered chapter list with titles."""
    toc = epub.read('toc.ncx').decode('utf-8')
    # navPoints: label + content src
    pattern = r'<navPoint[^>]*>.*?<navLabel>\s*<text>(.*?)</text>.*?<content\s+src="([^"]+)"'
    matches = re.findall(pattern, toc, re.DOTALL)
    return [(label.strip(), src.strip()) for label, src in matches]


def parse_chapter_title(title):
    """Parse 'BookName - N' to (book_name, chapter_number)."""
    m = re.match(r'^(.+?)\s*-\s*(\d+)$', title)
    if m:
        return m.group(1).strip(), int(m.group(2))
    return None, None


def find_local_file(book_folder, chapter_num):
    """Find local .md file where the last number in the filename matches chapter_num."""
    folder = CHAPTERS_DIR / book_folder
    if not folder.exists():
        return None
    for f in folder.glob("*.md"):
        if f.name == "readme.md":
            continue
        # Pattern: {book}-{part}-{chapInPart}-{chapInBook}.md
        m = re.match(r'\d+-\d+-\d+-(\d+)\.md$', f.name)
        if m and int(m.group(1)) == chapter_num:
            return f
    return None


def main():
    epub = zipfile.ZipFile(str(EPUB_PATH))
    chapters = parse_toc(epub)
    
    print(f"EPUB: {EPUB_PATH.name}")
    print(f"Chapters in TOC: {len(chapters)}")
    if DRY_RUN:
        print("MODE: DRY RUN (no files will be changed)\n")
    else:
        print("MODE: LIVE (files will be updated)\n")
    
    updated = 0
    skipped = 0
    not_found = 0
    unchanged = 0
    
    for title, src in chapters:
        book_name, ch_num = parse_chapter_title(title)
        if not book_name or not ch_num:
            skipped += 1
            continue
        
        book_folder = BOOK_FOLDERS.get(book_name)
        if not book_folder:
            print(f"  SKIP: Unknown book '{book_name}' in '{title}'")
            skipped += 1
            continue
        
        local_file = find_local_file(book_folder, ch_num)
        if not local_file:
            print(f"  NOT FOUND: {title} -> no local file for {book_folder}/ch{ch_num}")
            not_found += 1
            continue
        
        # Read and convert EPUB content
        html_content = epub.read(src).decode('utf-8')
        new_content = html_to_markdown(html_content)
        
        # Read existing local content
        old_content = local_file.read_text(encoding='utf-8').strip()
        
        if old_content == new_content:
            unchanged += 1
            continue
        
        if DRY_RUN:
            # Show diff stats
            old_lines = old_content.split('\n')
            new_lines = new_content.split('\n')
            print(f"  WOULD UPDATE: {local_file.name} ({title}) [{len(old_lines)} -> {len(new_lines)} lines]")
        else:
            local_file.write_text(new_content, encoding='utf-8')
            print(f"  UPDATED: {local_file.name} ({title})")
        updated += 1
    
    print(f"\n--- Summary ---")
    print(f"  Updated:   {updated}")
    print(f"  Unchanged: {unchanged}")
    print(f"  Not found: {not_found}")
    print(f"  Skipped:   {skipped}")

if __name__ == '__main__':
    main()
