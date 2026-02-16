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
