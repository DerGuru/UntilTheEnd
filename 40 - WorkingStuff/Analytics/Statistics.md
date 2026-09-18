# UTE RoyalRoad Analytics — Gesammelte Statistische Befunde

Konsolidierte Zusammenfassung aller Analytics-Untersuchungen (Fiction 152927, "Until the End", RoyalRoad). Ergänzt `HANDOFF.md` (Task-Tracking) und `00 - General/RR-Metrik.md` (RR-Kontext/Ranking). Stand: 08.09.2026.

## 1. Eckdaten

- Serie abgeschlossen **12.05.2026** (Clouds-68, 16:53 Uhr; Afterword selber Tag, 19:12 Uhr — verifiziert via `chapter_publish_dates.csv`), 423 Kapitel, 7 Bücher (Embers, Roots, Silence, Echoes, Fractures, Mirrors, Clouds). Danach nur noch administrative Einträge: "Available on Amazon" (15.05.) und ein Origins-Crosspromo-Post (19.05.) — kein Story-Content.
- Launch: **14. Februar 2026** (Embers-01).
- Datenquelle: `ute_pageviews_raw.json` (per-Kapitel Tages-Views, 2026-03-08 bis 2026-09-07, 184 Tage — Pageview-Tracking begann erst am 7./8. März, nicht beim Launch).
- Stand 18.09.2026 (live Dashboard): **245,626 Views** gesamt (+2,144 seit 08.09., ~214/Tag Ø über 10 Tage), ~229 Follower, Rating ~3.96 (gefallen von 4.12 — AI-Tag zieht Downvotes), ~51 Favs.

## 2. Wachstumsverlauf / Traffic-Geschichte

| Phase | Zeitraum | Tage | Views | Ø/Tag | Multiplikator |
|-------|----------|------|-------|-------|---------------|
| Paid-Baseline | 14. Feb – 20. Mär | 35 | ~17k | ~480 | 1x |
| Trending-Stottern | 21. Mär – 5. Apr | 16 | ~13k | ~810 | 1.7x |
| Trending-Dauerhaft | 6. Apr – 26. Apr | 21 | ~84k | ~4,000 | 8x |

- **21. März – 5. April ("Trending-Stottern"):** UTE flippt sporadisch ins Trending, fällt aber immer wieder raus. Extreme Tages-Varianz (71–2,853 Views/Tag).
- **24. März Spike:** rückblickend per "breiter Engagement"-Metrik (Kapitel gleichzeitig ≥3× eigener Baseline) der Rang-#2-Tag der gesamten 184-Tage-Historie (135 Kapitel gleichzeitig elevated). Exakter Auslöser (welche Trending-Liste/welcher Referrer) nicht mehr rekonstruierbar — Referrer-Daten haben kein Datumsfeld und es existiert kein Snapshot aus der Zeit.
- **6. April = Trending-Durchbruch (Ostermontag):** Rang **#1** der gesamten Historie (143 Kapitel gleichzeitig elevated). Seitdem nie unter 2,161 Views/Tag. Einstieg Main Trending #6, ab 22. April stabil auf #2.
- **Trending durchgehend bis 12. Mai** (User-bestätigt) — blieb ohne Unterbrechung bestehen bis zum Tag des letzten Kapitels (Clouds-68). Damit deckt die Trending-Phase praktisch die gesamte restliche Veröffentlichungszeit der Story ab (6. April – 12. Mai, ~5 Wochen).
- **12. Mai = absoluter Trending-Peak.** Am Tag der Veröffentlichung von Clouds-68 stand UTE laut User erstmals (und wahrscheinlich einzig) auf **#1 in allen relevanten Trending-Listen gleichzeitig** — der Story-Abschluss fiel exakt mit dem Traffic-Höhepunkt zusammen.
- **Ausklingen ~10 Tage danach (bis ca. 22. Mai):** Nach dem 12.-Mai-Peak blieb UTE laut User noch etwa 10 Tage in den Trending-Listen, bevor es endgültig herausfiel — kein abrupter Abbruch, sondern ein Abklingen nach dem letzten Kapitel.
- **Publish-Pause 2.–7. April** (Ostern, bis 283 Kapitel Backlog aufgebaut): Cumulative-Publish-Chart zeigt in diesem Fenster ein flaches Plateau, danach Fortsetzung — der Durchbruch fiel mit dem Ende der Pause zusammen, nicht mit neuem Content.
- Backlog-Vorteil: 350+ Kapitel bedeuten laut RR-Metrik ~50-300 Views pro neuem Trending-Leser statt 5-10 wie bei frischen Fictions.

### Referrer-Entwicklung (7-Tage-Rolling-Snapshots, April 2026)

| Quelle | W1 (7–13) | W2 (13–19) | W3 (20–26) |
|--------|----------:|-----------:|-----------:|
| Trending | 443 | 577 | 669 |
| Google | 271 | 257 | 300 |
| Homepage | 114 | 208 | 185 |
| RR Advertising | 89 | 54 | 45 |
| Weekly Popular | 6 | 27 | 63 |
| Rising Stars | 13 | 46 | 61 |
| Latest Updates | 71 | 72 | 128 |
| **Total** | **1,031** | **1,272** | **1,490** |

- RR-Ad-Kampagne (seit 24.02., ~260k Impressions, 728 Klicks, CTR 0.28%): war nützlicher "Flywheel-Starter" (Paid → Engagement-Velocity → Trending), aber allein ineffizient (93% Bounce, nur ~12% der Follower ad-getrieben). Läuft seit Ende April aus.
- **September-Snapshot (aktuell, undatiert/rollend):** Trending weiterhin präsent, aber klein (5 Sessions) neben generischem royalroad.com-Traffic (64+14 Sessions) und Google (25). Kein Hinweis auf einen zweiten Trending-Schub — Trending "flippt gelegentlich rein", ist aber nicht mehr der Haupttreiber.
- Aktuelle Discovery-Kanäle: Google (organisch), AI-Tag-Popularitätssuche (UTE #2 der Kategorie nach Rang, #1 nach Rohzahlen), Foren-Referrer, vereinzelt "latest-updates"/"reading-history" (bestehende Leser).

## 3. Completion / Leser-Position

- **Funnel Ch1→Ch2: −42%** (harter, ehrlicher Filter — größter Einzelabfall der ganzen Story), danach flacht die Kurve stark ab.
- **Gesamt-Completion (views-basiert): ~6%.**
- **~195 Leser** haben laut offiziellen RR-Retention-Daten das Ende erreicht (absolute Kopfzahl).
- **Views-Ratio ≠ Person-Completion-Rate** (wichtige Unterscheidung): Von Embers-10 bis Ende ist die echte personenbasierte Completion nur **~0.5-0.7%** (offizielle Retention-Kopfzahlen, kleine Stichprobe), während das reine Views-Verhältnis viel optimistischer aussieht — **~18-26%** roh, **~28-40%** kalenderzeit-normalisiert (je nach Anker Embers-10/Roots-01/Silence-01). Der views-basierte Wert überschätzt echte Completion deutlich.
- Gewichteter "wo sind die Leser gerade"-Schwerpunkt (r7/r14/r30-Fenster): ~Silence (~40% durch die Story).
- Fast kein zusätzlicher Verlust exakt an Buchübergängen selbst (Funnel bleibt dort stabil) — siehe Abschnitt 5 für den gegenteiligen, aber kleinen Nebenbefund (Kapitel-1-Bump).

## 4. Bleed-out-Mechanik

- **Kein struktureller "Cliff" irgendwo in der Story.** Der vermutete Echoes→Fractures-Bruch wurde ausführlich untersucht (7 Skripte, mehrere Methoden) und **widerlegt**. Echoes endet bei ~4.0-4.2 Views/Tag, Fractures startet bei ~4.04 — nahtlos.
- Zwei Rausch-/Artefakt-Fallen, die den scheinbaren Cliff erzeugten (Lektion, auch in Agent-Memory dokumentiert):
  1. **r30-Fenster-Rauschen** — zu kleine Fallzahlen für verlässliche %-Änderungen.
  2. **Beobachtungsfenster-Confound** — die RR-API lässt Null-View-Tage komplett aus dem Array; `total ÷ n_entries` überschätzt daher spätere/leserschwächere Kapitel systematisch. **Fix:** Normalisierung durch echte Kalendertage (`Datensatz-Ende − erster_Tracking-Tag`), nicht durch Anzahl der Einträge.
  3. Einzig echter Befund: Echoes hat einen eigenen graduellen ~19-22% internen Rückgang (Buch-intern vorne-lastig), aber keinen Bruch zum nächsten Buch.
- **Bleedout vs. langsames Lesen: überwiegend echtes Bleedout.** Offizielle RR-"User Retention"-Dropout-Kopfzahlen (Mai/Juni-Snapshots + Live-Scrape) zeigen: Dropout-Verteilungsform über 3.5 Monate eingefroren (nur ~+8-10% proportionales Wachstum), und jedes Kapitel (inkl. dem letzten, Clouds-68) peakt im eigenen Publish-/Entdeckungsmonat — keine verzögerte "Aufhol"-Welle späterer Leser.
- **Ursache generell diffus, nicht auf einzelne Kapitel zurückführbar.** Da die Abnahme durchgehend glatt ist (kein Cliff, keine Anomalie), würde eine Suche nach "welches einzelne Kapitel verliert am meisten" mit hoher Wahrscheinlichkeit nur dieselben Rausch-Artefakte reproduzieren. Wahrscheinlichste Treiber (branchenübliches Wissen, keine harten Zahlen): Genre-Tourismus, "Warte-auf-den-Stapel"-Verhalten, wiederkehrende Re-Investitionsentscheidung bei jedem neuen Kapitel, abnehmender Neuleser-Nachschub über Zeit.
- Kein Zugriff auf Vergleichsdaten anderer RR-Serien möglich (keine öffentliche Benchmark-Datenbank; Autoren teilen Analytics praktisch nie).

## 5. Kapitel-1-Bump an Buchübergängen (neu, 08.09.2026)

Kapitel 1 eines neuen Buchs hat bei **5 von 6 Übergängen** mehr Views als sowohl das Ende des vorherigen Buchs als auch die folgenden 2-5 Kapitel:

| Übergang | Ch.1 vs. nächste 4 Kap. | Ch.1 vs. Tail vorheriges Buch |
|---|---:|---:|
| Embers→Roots | +2.5% | -2.8% |
| Roots→Silence | +8.1% | +5.4% |
| Silence→Echoes | +10.0% | +7.5% |
| Echoes→Fractures | +7.2% | +6.4% |
| Fractures→Mirrors | -5.9%* | +17.1% |
| Mirrors→Clouds | **+29.3%** | **+20.3%** |

(*Ausreißer: Mirrors-02 mit 470 Views ist selbst ungewöhnlich hoch und verzerrt den Vergleichswert.)

- **Absolute Bump-Größe bleibt über die ganze Serie flach/rauschend** (+24 bis +67 Views ggü. lokaler Baseline), obwohl die Leserschaft im gleichen Zeitraum um Faktor ~4 schrumpft (Baseline 933 → 229). Die **relative %-Größe wächst nur, weil der Nenner (aktive Leserschaft) schrumpft** — kein Zeichen für ein sich verschärfendes Problem, sondern ein strukturell stabiles, harmloses Artefakt.
- Wahrscheinlichste Ursache: durchlesende Leser pausieren an einem natürlichen Punkt (neues Buch = Stopp-Signal) und klicken beim Wiedereinstieg dasselbe Kapitel erneut an. Eine alternative Theorie (Abbrecher schauen periodisch vorbei) ist mit denselben Daten nicht auszuschließen, aber auch nicht zu bestätigen — RR liefert keine Session-/User-Ebene, nur aggregierte Views pro Kapitel.

## 6. Pre-Tracking-Gap

- Pageview-Tracking begann erst am 7./8. März 2026 — **~232.5 Views** (Range 189-266) fehlen dadurch für Embers-01 gegenüber dem echten RR-Gesamtwert. Über 41 unabhängige historische Snapshots (13.04.-30.06.) verifiziert, bemerkenswert stabil.
- 217 von 420 Story-Kapiteln (alle Embers/Roots/Silence + Echoes 1-20) waren bereits vor Trackingbeginn vollständig veröffentlicht.

## 7. Wochentag-Muster

- Ohne Datums-Shift (verifiziert gegen Ostermontag als hartem Anker): **Dienstag und Donnerstag** sind die traffic-stärksten Wochentage (Ø ~1446 / ~1404 Views), **Sonntag** am schwächsten (~1040), Montag Mittelfeld (~1167).
- Seltene "breite Engagement-Spikes" (viele Kapitel gleichzeitig weit über eigener Baseline, = echte Trending-Ereignisse) clustern dagegen auf **Montag und Samstag** — ein anderes Muster als die gewöhnliche Tagesstärke.

## 8. RR-Kontext-Einordnung

Aus `00 - General/RR-Metrik.md` (verifiziert via RR-Suche, 26.04.2026, 128,711 durchsuchbare Fictions):

| Metrik | UTE-Rang (alle Fictions) | UTE-Rang (nur aktive, 22,122) |
|---|---|---|
| Views (~120k) | Top 3.9% | Top 8.4% |
| Follower (~149) | Top 7.5% | Top 15.8% |
| AVG Views/Kapitel (359) | Top <0.5% | — |

- Follower/1000-Views-Ratio bei UTE ~1.2, RR-Trending-Schnitt ~3-5 — niedrig, typisch für Bulk-Content (353+ Kapitel, Leser folgen oft erst ab Buch 2-3) und XianXia (generell niedrigere Follow-Raten als LitRPG).

## 9. Offene Fragen

- Exakter Auslöser von 24. März / 6. April auf Referrer-Ebene nicht rekonstruierbar (keine historischen Referrer-Snapshots aus dieser Zeit).
- **Sommerloch vs. echter Rückgang (September):** Update 18.09. — Tages-Views (rollendes 31-Tage-Fenster, `/api/data/chapterv/`) zeigen ab 10. September einen klaren Ausschlag nach oben: Sep 3-9 lag durchgehend niedrig (10-252/Tag), Sep 10-17 mehrfach deutlich höher (460, 429, 507, 407 an einzelnen Tagen, dazwischen aber auch wieder Ausreißer nach unten wie 2 und 20). Insgesamt eher volatil-aufwärts als eindeutig stabilisiert — spricht tendenziell FÜR ein Abklingen des Sommerlochs, aber die Tag-zu-Tag-Varianz ist immer noch zu groß für eine sichere Trendaussage. Empfehlung weiterhin: noch 2-3 Wochen beobachten, bevor eine klare Trendaussage getroffen wird.
- **Referrer-Auffälligkeit 18.09. (ungeklärt, zwei Erklärungen möglich):** `fictions/latest-updates` zeigte bei UTE 1 User mit 425 Sessions in 7 Tagen; bei Origins (Fiction 167806, 37 Kapitel) dasselbe Muster mit 39 Sessions. Beide Werte liegen fast exakt bei der jeweiligen Gesamt-Kapitelzahl. Zwei gleich plausible Erklärungen, NICHT sicher unterscheidbar mit den verfügbaren Daten:
  1. Ein einzelner Leser mit altem, gespeichertem "latest-updates"-Link, der die komplette Story an einem Tag durchgelesen hat.
  2. Ein Crawler/automatisiertes Tool, das einen alten Link erneut abgeklappert hat — die "Sessions ≈ Kapitelzahl"-Signatur spricht nicht eindeutig gegen einen Bot (ein systematischer Crawler erzeugt dasselbe Muster, evtl. sogar präziser als ein Mensch). "RR filtert Crawler" gilt vermutlich nur für deklarierte/erkennbare Bots (User-Agent, IP-Listen); ein Tool mit echter Browser-Engine (Puppeteer/Playwright/Selenium) wäre für clientseitiges JS-Tracking nicht von einem echten User zu unterscheiden.
  Fazit: nicht auflösbar, nicht als eindeutiges Engagement-Signal werten.
- Kein Zugriff auf Vergleichszahlen anderer Autoren/Serien (Ursache-Frage fürs Bleedout bleibt daher branchenüblich-spekulativ, nicht hart belegbar).

## 10. Methodik-Hinweise

- **Immer durch echte Kalendertage normalisieren**, nicht durch Anzahl API-Einträge (Null-View-Tage fehlen im Array).
- **Kleine Stichproben (<50 Views) sind Rauschen** — r90/r180/Gesamt-Fenster oder größere Zeiträume verwenden.
- **Views-Ratio ≠ Person-Completion-Rate** — offizielle Retention-Kopfzahlen sind kleiner und literaler.
- **Datums-Semantik nie ungeprüft übernehmen** — gegen einen unabhängig verifizierbaren Anker (z.B. ein erinnertes Datum/Feiertag) gegenchecken, bevor Korrekturen angewendet werden.
