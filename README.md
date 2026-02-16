## UntilTheEnd – Projektstruktur

Dieses Repository ist ein Romanprojekt.  
Die Ordnerstruktur ist **kanonisch** und sollte in Prompts/Dokumenten genau so referenziert werden.

## Kanonische Top-Level-Ordner

- `00 - General/` – Kernbibel (Konzept, Charaktere, Regeln, Weltbau, Meta-Outline)
- `10 - Outlines/` – Beat-/Outline-Dateien + `SzenenOutlines/`
- `20 - Chapters/` – ausgeschriebene Kapitel je Buchband
- `30 - Feedbacks/` – externes/iteratives Feedback
- `40 - WorkingStuff/` – Arbeitsdokumente, Prompts, Improvement-Tracking
- `50 - KDP/` – Export/Publishing-Artefakte
- `60 - Translation/` – Übersetzungsartefakte und Übersetzungsprompts
- `Covers/` – Cover-Dateien

## Wichtige Pfade

- Outlines: `10 - Outlines/`
	- Haupt-Outlines: `1-Hook-Outline.md` bis `7-Resolution-Outline.md`
	- Szenen: `10 - Outlines/SzenenOutlines/<buch>-<part>-Szenen.md`
- Kapitel: `20 - Chapters/<BuchNr> - <Bandname>/`
- Arbeits-/Prompt-Dateien: `40 - WorkingStuff/`

## Benennungsregeln (Kurz)

- Kapitelband-Ordner folgen der numerischen Sortierung (`20 - Chapters/1 - Kindle`, …)
- 7PS-Outlines sind numerisch + Beat benannt (`1-Hook-Outline.md`, …, `7-Resolution-Outline.md`)
- Kapiteldateien nutzen als **kanonischen Identifier** das Schema:
	- `[7PS-Overall-Position]-[7PS-Position im Abschnitt]-[Kapitelnummer]`
	- also: `X-Y-ZZ.md`
	- Beispiel: `2-1-01.md`
	- Mapping Overall-Position: `1=Hook, 2=Plot Turn 1, 3=Pinch 1, 4=Midpoint, 5=Pinch 2, 6=Plot Turn 2, 7=Resolution`
- Neue Pfadangaben in Dokumenten immer auf die 00/10/20/30/40/50/60-Struktur beziehen.
