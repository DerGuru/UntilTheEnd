import codecs

path = r'd:\OneDrive\OneDrive - Jakof\UntilTheEnd\03 - WorkingStuff\Improvements_4-Echoes.md'

with open(path, 'rb') as f:
    raw = f.read()

text = raw.decode('utf-8-sig')

# Check for common mojibake patterns (double-encoded UTF-8)
if '\u00c3' in text or '\u00e2\u0080' in text or '\u00c2' in text:
    # The text was double-encoded: UTF-8 bytes interpreted as Latin-1/CP1252, then re-encoded as UTF-8
    try:
        fixed = text.encode('cp1252').decode('utf-8', errors='replace')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(fixed)
        print('Fixed double-encoding successfully')
        print('Lines:', fixed.count('\n'))
        # Check if it still has issues
        if '\u00c3' in fixed or '\u00c2' in fixed:
            print('WARNING: Still has potential mojibake')
        else:
            print('Clean!')
    except Exception as e:
        print(f'Error during fix: {e}')
else:
    print('No mojibake detected')
    print('Lines:', text.count('\n'))
