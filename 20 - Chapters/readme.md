# Kapitel-Dateinamen (kanonisch)

Die Kapiteldateinamen sind **Identifier** und bleiben numerisch.

Format:

`[Reiseabschnitt]-[Streckenabschnitt]-[Kapitel im Streckenabschnitt].md`

Kurzform: `X-Y-ZZ.md`

## Bedeutung der Segmente

Alias-Mapping:
- `Reiseabschnitt = 7PS-Overall-Position`
- `Streckenabschnitt = 7PS-Position im Abschnitt`
- `Kapitel im Streckenabschnitt = Kapitelnummer`

- `X` = Position in der **7PS overall**
	- `1=Hook`
	- `2=Plot Turn 1`
	- `3=Pinch 1`
	- `4=Midpoint`
	- `5=Pinch 2`
	- `6=Plot Turn 2`
	- `7=Resolution`
- `Y` = **Streckenabschnitt** (7PS-Position im jeweiligen Abschnitt)
- `ZZ` = **Kapitel im Streckenabschnitt** (laufende Nummer innerhalb dieses Slots)

Beispiel: `2-1-01.md`

## UTE-Hauptserie

In `02 - UTE` tragen die Erzählkapitel zusätzlich die fortlaufende Kapitelnummer
des jeweiligen Buchs: `Buch-Part-Kapitel-im-Part-Kapitel-im-Buch.md`, zum Beispiel
`1-2-03-11.md`. Diese IDs bleiben auch beim Abgleich mit einem RR-Export erhalten.
EPUB-Titel wie `Embers - 11` werden nach Buch und fortlaufender Nummer zugeordnet,
nicht nach ihrer Position im Inhaltsverzeichnis. Fehlende Exportkapitel sind kein
Löschauftrag. Nachwort und Ankündigungen stehen separat unter `8-...`.

### Maße in der englischen UTE-Prosa

- Kurze Zeitspannen: `heartbeats`, `breaths` oder eine passende beobachtbare
  Handlung. Bereits angelegte Zählungen und ihre späteren Rückbezüge müssen
  zusammenpassen; keine Kunstwörter wie `milliheartbeats`.
- Längere Zeitspannen: `watch` (ungefähr zwei Stunden), `half a watch`,
  Tageslicht, Mahlzeiten oder andere passende Alltagsintervalle. Tage, Monate,
  Jahreszeiten und Jahre bleiben; Wochen werden bei Bedarf als Tage angegeben.
- Entfernungen: `paces` und `li`; beim Abgleich ungefähr ein Schritt je Meter
  wie in den RR-Korrekturen, zwei Li je Kilometer. Kleine Abstände werden
  körperbezogen beschrieben, etwa mit Fingerbreite oder Handspanne.
- Gewicht und Volumen: verständliche Lasten, Waren- oder Gefäßmaße im Kontext.
  Mengenverhältnisse, Reisezeiten und Folgen dürfen bei der Übertragung nicht
  verändert werden. Eine Maßeinheit wird nicht allein wegen ihres Wortlauts
  ersetzt: `second` als Ordnungszahl und `feet` als Körperteile bleiben.
- Diese Konvention betrifft die erzählte Welt. Reale Daten, Verkaufsangaben und
  Arbeitszeiten in Nachwort und Ankündigungen werden nicht historisiert.

Die [Schreibregeln](../.github/instructions/) bleiben verbindlich.
Die Origins-Manuskripte gehören nicht zu einem UTE-Abgleich.
