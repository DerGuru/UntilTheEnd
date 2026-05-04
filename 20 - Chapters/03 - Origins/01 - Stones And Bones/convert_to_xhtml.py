"""Convert all chapter markdown files to EPUB-ready XHTML."""
import re
from pathlib import Path

CHAPTER_DIR = Path(__file__).parent.parent
EPUB_DIR = Path(__file__).parent

TEMPLATE_HEAD = '''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
  <title>Stones and Bones {chapter_num}</title>
  <link rel="stylesheet" type="text/css" href="../Styles/style.css" />
</head>
<body>
    <header>
        <h1 style="text-align: center;" epub:type="title">Stones and Bones - {chapter_num_padded}</h1>
    </header>
  <section epub:type="chapter">
'''

TEMPLATE_FOOT = '''  </section>
</body>
</html>
'''


def convert_text_to_xhtml_entities(text: str) -> str:
    """Convert special characters to XML entities and handle inline formatting."""
    # Replace em-dashes (with or without surrounding spaces/thin spaces)
    text = text.replace(' — ', '\u2009\u2014\u2009')
    text = text.replace('—', '\u2014')
    
    # Convert Unicode to XML entities
    text = text.replace('\u2019', '&#x2019;')  # right single quote / apostrophe
    text = text.replace('\u2018', '&#x2018;')  # left single quote
    text = text.replace('\u201C', '&#x201C;')  # left double quote
    text = text.replace('\u201D', '&#x201D;')  # right double quote
    text = text.replace('\u2014', '&#x2014;')  # em-dash
    text = text.replace('\u2009', '&#x2009;')  # thin space
    text = text.replace('\u2026', '&#x2026;')  # ellipsis
    text = text.replace('\u00A0', '&#xA0;')    # non-breaking space
    
    # Handle straight quotes → curly quotes
    # Opening double quotes (after space, start of line, or after tag)
    text = re.sub(r'(?<=\s)"(?=\S)', '&#x201C;', text)
    text = re.sub(r'^"(?=\S)', '&#x201C;', text)
    # Closing double quotes
    text = re.sub(r'(?<=\S)"(?=[\s,.\!?\;\:]|$)', '&#x201D;', text)
    
    # Straight apostrophes → curly
    text = re.sub(r"(?<=\w)'(?=\w)", '&#x2019;', text)
    
    # Handle italic: *text* → <em>text</em>
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    
    return text


def markdown_to_xhtml(md_content: str, chapter_num: int) -> str:
    """Convert markdown content to XHTML."""
    chapter_num_padded = f"{chapter_num:02d}"
    
    lines = md_content.strip().split('\n')
    paragraphs = []
    current_para = []
    
    for line in lines:
        stripped = line.strip()
        if stripped == '':
            if current_para:
                paragraphs.append(' '.join(current_para))
                current_para = []
        else:
            # Skip markdown headers if any
            if stripped.startswith('#'):
                continue
            current_para.append(stripped)
    
    if current_para:
        paragraphs.append(' '.join(current_para))
    
    # Build XHTML
    xhtml = TEMPLATE_HEAD.format(chapter_num=chapter_num, chapter_num_padded=chapter_num_padded)
    
    for para in paragraphs:
        converted = convert_text_to_xhtml_entities(para)
        xhtml += f'\n    <p>{converted}</p>\n'
    
    xhtml += TEMPLATE_FOOT
    return xhtml


def main():
    md_files = sorted(CHAPTER_DIR.glob('*.md'))
    
    for md_file in md_files:
        # Extract chapter number from filename: X-XX-YY.md → YY is overall chapter
        parts = md_file.stem.split('-')
        if len(parts) != 3:
            print(f"Skipping {md_file.name} (unexpected naming)")
            continue
        
        chapter_num = int(parts[2])
        
        # Read markdown
        content = md_file.read_text(encoding='utf-8-sig')  # handle BOM
        
        # Convert
        xhtml_content = markdown_to_xhtml(content, chapter_num)
        
        # Write
        out_file = EPUB_DIR / f"{md_file.stem}.xhtml"
        out_file.write_text(xhtml_content, encoding='utf-8')
        print(f"Created: {out_file.name}")


if __name__ == '__main__':
    main()
