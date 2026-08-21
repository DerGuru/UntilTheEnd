---
description: 'Generische SOLID-Checkliste für Szenen und Kapitel (Single Responsibility, Open/Closed, Liskov, Interface Segregation, Dependency Inversion), übertragen auf Erzählcraft. Schneller Motivations-/Konsistenz-/Nachvollziehbarkeits-Check.'
---

# SOLID-Checklist fürs Schreiben

> Benutze das wie einen schnellen Szenen- und Kapitel-Check. Ziel: Motivation, Konsistenz, Nachvollziehbarkeit – ohne Dogma.

## Schnell-Checkliste für jede Szene (und damit jedes Kapitel)

1) **SRP:** Was ist die *eine* Hauptfunktion dieser Szene?
☐ Plot voran ☐ Charakter vertiefen ☐ Beziehung entwickeln ☐ Spannung erhöhen ☐ Welt zeigen ☐ Thema spiegeln

2) **OCP:** Welche Saat/Setup legst du hier (oder nutzt du)?
☐ Seed gelegt ☐ Seed geerntet ☐ Beides ☐ Weder noch (okay, wenn SRP sauber)

3) **LSP:** Handeln alle Figuren wie „sie selbst" – auch unter Druck?
☐ Ja ☐ Teilweise ☐ Nein (Marionetten-Alarm)

4) **ISP:** Ist jede Figur in der Szene „schlank" eingesetzt (keine Allzweck-Figur)?
☐ Ja ☐ Teilweise ☐ Nein

5) **DIP:** Entsteht das Ergebnis aus **Motivation + Regeln + Konsequenzen**?
☐ Ja ☐ Teilweise ☐ Nein (Deus-Ex/Plot-Zufall)

---

## S — Single Responsibility Principle (SRP)
**Ziel:** Eine Szene hat **eine dominante Aufgabe** (nicht zehn).
- Was soll der Leser am Ende **anders wissen/fühlen/glauben**? Könnte ich die Szene in einem Satz zusammenfassen? Gibt es einen klaren **Einstieg → Wendepunkt → Ausstieg**?
- Warnsignale: Exposition + Streit + Action + Romance in einer Mini-Szene. „Wir sind hier, damit der Autor X erklärt."
- Quick Fix: Alles, was nicht zur Hauptfunktion gehört, **raus oder verschieben**. Wenn du 2 Funktionen brauchst: **splitte** in zwei Szenen.

## O — Open/Closed Principle (OCP)
**Ziel:** Später erweitern, ohne alte Szenen umzuschreiben (Retcon-Schmerz).
- Ist das hier **ein neuer Baustein**, der später genutzt werden kann? Ist die Information **robust** (mehrdeutig genug, um später zu passen)? Passt alles zu bisherigen Regeln/Charakterzügen/Setting-Fakten?
- Warnsignale: „Das muss ich später ändern, wenn ich X entscheide." Neue Regeln tauchen auf, die alte Szenen rückwirkend dumm aussehen lassen.
- Quick Fix: Foreshadowing **klein, konkret, nicht erklärend**. Früh **Verhalten zeigen** statt Mechanik erklären.

## L — Liskov Substitution Principle (LSP)
**Ziel:** Eine Figur bleibt konsistent: Wenn du sie als „Typ" etablierst, muss sie sich in neuen Situationen **typisch** verhalten.
- Würde diese Figur das wirklich tun, **wenn der Plot egal wäre**? Gibt es eine klare **innere Begründung** (Angst, Stolz, Werte, Trauma, Ziel)? Reagiert sie **logisch auf neue Infos**?
- Warnsignale (Marionetten-Alarm): Figur macht das Offensichtliche nicht – ohne Grund. Figur sagt exakt das, was der Leser hören soll. Emotionen wechseln zu schnell (ohne Trigger).
- Quick Fix: Gib der Figur ein **Mini-Ziel** für die Szene (auch wenn sie verliert). Zeig den **Preis** ihrer Entscheidung.

## I — Interface Segregation Principle (ISP)
**Ziel:** Keine Figur ist Allzweck-Werkzeug. Jede Figur erfüllt **eine klare Rolle**.
- Wer bringt **Konflikt**? Wer bringt **Wärme**? Wer bringt **Info**? Hat jede Figur **Eigeninteresse**? Könnte ich eine Figur entfernen, ohne dass sich viel ändert? (Dann ist sie Deko.)
- Warnsignale: Eine Nebenfigur ist gleichzeitig Exposition + Humor + Moral + Plotmotor. Dialog wirkt wie FAQ.
- Quick Fix: Verteile Funktionen: Info kommt z.B. durch **Handlung**, nicht durch einen „Erklärer". Lass Figuren **aneinander vorbeireden**, wenn ihre Ziele kollidieren.

## D — Dependency Inversion Principle (DIP)
**Ziel:** Die Story hängt nicht an Zufällen oder Speziallösungen, sondern an **Prinzipien**: Motivation, Regeln, Konsequenzen.
- Würde der Ausgang auch passieren, wenn der Autor „nicht helfen" dürfte? Gibt es ein klares **Wenn-dann** aus Weltregeln? Sind Zufälle **klein** (Trigger) statt **groß** (Lösung)?
- Warnsignale: Deus ex machina / plötzliche Rettung ohne Setup. „Zum Glück war genau dieses Item hier…" Antagonisten handeln dumm, damit's klappt.
- Quick Fix: Baue Rettungen als **Kette von Kosten** (Preis zahlen). Setze Konsequenzen: Erfolg erzeugt neue Probleme, Misserfolg hat Nachwirkungen.

---

## Mini-Scoring (optional)
Vergib pro Buchstabe 0–2 Punkte (S/O/L/I/D). **Summe / 10.**
- 8–10: sitzt stabil · 5–7: gut, aber ein klarer Fix lohnt · 0–4: Szene neu denken (meist SRP oder LSP)
