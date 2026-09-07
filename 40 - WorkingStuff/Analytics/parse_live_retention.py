"""Parse the live Retention Analytics page (accessibility-tree snapshot dumped by
read_page) into the official current 'User retention table' rows."""
import re
from pathlib import Path

SNAPSHOT = Path(
    r"c:\Users\JakofHe\AppData\Roaming\Code\User\workspaceStorage\2b686f337a99865772cdd545647f1805"
    r"\GitHub.copilot-chat\chat-session-resources\86e3ca1b-be41-4a75-8b26-8daf7faf8714"
    r"\toolu_01MaKbnwr1GxBzAFb329EtA8__vscode-1788786501410\content.txt"
)
text = SNAPSHOT.read_text(encoding="utf-8")
print("total chars:", len(text))

# Parse via individual `cell "..."` entries (6 cells per row), more robust than
# matching the combined row-text (which breaks on the "100%  X.XX%" dual-value cells).
cells = re.findall(r'cell "([^"]*)"', text)
print("total cells found:", len(cells), " -> rows:", len(cells) // 6)

rows = [cells[i:i + 6] for i in range(0, len(cells) - len(cells) % 6, 6)]
print("\nFirst 5 rows:")
for r in rows[:5]:
    print(r)
print("\nLast 5 rows:")
for r in rows[-5:]:
    print(r)

