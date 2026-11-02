# UTE RoyalRoad Analytics — Gesammelte Statistische Befunde

Konsolidierte Zusammenfassung aller Analytics-Untersuchungen (Fiction 152927, "Until the End", RoyalRoad). Ergänzt `HANDOFF.md` (Task-Tracking) und `00 - General/RR-Metrik.md` (RR-Kontext/Ranking). Stand: 08.09.2026.

## 1. Eckdaten

- Serie abgeschlossen **12.05.2026** (Clouds-68, 16:53 Uhr; Afterword selber Tag, 19:12 Uhr — verifiziert via `chapter_publish_dates.csv`), 423 Kapitel, 7 Bücher (Embers, Roots, Silence, Echoes, Fractures, Mirrors, Clouds). Danach nur noch administrative Einträge: "Available on Amazon" (15.05.) und ein Origins-Crosspromo-Post (19.05.) — kein Story-Content.
- Launch: **14. Februar 2026** (Embers-01).
- Datenquelle: `ute_pageviews_raw.json` (per-Kapitel Tages-Views, 2026-03-08 bis 2026-09-07, 184 Tage — Pageview-Tracking begann erst am 7./8. März, nicht beim Launch).
- Stand 24.09.2026 (live Dashboard): **249,017 Views** gesamt (+3,391 seit 18.09., ~565/Tag Ø über 6 Tage, Wachstumsrate beschleunigt sich — siehe Abschnitt 9 "Sommerloch"). **Favs: 55** (von ~51 am 18.09.) — steigen ebenfalls, passt zum Herbst-Comeback.
- **250,000-Views-Marke überschritten: 29.09.2026, 1:25 Uhr CEST** (250,016 Views) — passt gut zur am 24.09. abgegebenen Schätzung ("morgen oder Montag").
- Stand 02.11.2026: **257,246 Views** (+7,230 seit 29.09., ~213/Tag Ø über 34 Tage).

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
- **Trending-Referrer NACH dem Verschwinden aus den Listen (~22.05.) — Einordnung 02.11.:** Der Referrer `fictions/trending` taucht weiter auf (18.06.: 15 Users/38 Sessions, 30.06.: 5/16, 08.09.: 5/5, 02.11.: 5/5), obwohl UTE laut User seit ~22.05. nicht mehr in den Listen stand; Live-Check 02.11.: UTE nicht unter den 100 Einträgen von `/fictions/trending`. "Flippt gelegentlich rein" ist damit **nicht belegt** — die Aussage stützte sich nur auf diese Referrer. Mechanik: Ein Bookmark erzeugt KEINEN Referrer (das passt zur Ad-Zeile, die nur UTM-Parameter ohne URL zeigt); `fictions/trending` als Referrer heißt, die Seite wurde von der Trending-Seite aus geladen. Format unterscheidet nichts: echte Trending-Klicks im April stehen im selben Format (425-603 Users). Plausible Quellen: (a) alte, noch offene Trending-Tabs; (b) alte UTE-Tabs, die ursprünglich über Trending geöffnet wurden und neu geladen/wiederhergestellt werden — Reload behält den ursprünglichen Referrer (das bookmark-ähnliche Szenario); (c) kurzes Wiederauftauchen in einer Liste innerhalb des 7-Tage-Fensters, nicht ausschließbar. Indiz: Sessions/User lag im April bei ~1.2, im Juni bei 2.5-3.2 (wenige Leute, wiederholt — passt zu b), im Sep/Nov bei 1.0 (passt eher zu a oder c). Nicht entscheidbar.
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
- **Gesamtform der Kurve (alle 423 Kapitel, 24.09. bestätigt): gespiegelte Wurzel, nicht linear oder exponentiell.** Kurvenanpassung y = a − b·√(Kapitelposition) ergibt R²=0.92 — besser als Gerade (0.85) oder Exponential-Zerfall (0.91). Steiler Fall am Anfang (Embers), progressive Abflachung danach; **Silence ist mit -0.26%/Kapitel das flachste Buch der Serie** (Silence-Ende sogar bei -0.01%/Kapitel, praktisch komplett flach), was am Buchübergang zu Echoes (-0.86%/Kapitel direkt danach) wie ein optischer "Knick" wirkt — real ist aber nur die Steigung geknickt, nicht der Wert selbst (siehe Cliff-Befund oben: nahtloser Übergang). Einzige große Abweichung von der Wurzel-Kurve: Kapitel 1 (Embers-01) liegt weit über jeder glatten Kurve — bekannter Ch1→Ch2-Launch-Sampling-Effekt (-42%), kein Kurvenfehler. Geprüft und verworfen: der Silence-Flachheit-Knick ist KEIN Tracking-Artefakt der Pre-Tracking-Grenze (Echoes Kapitel 20/21) — die Steigung bleibt innerhalb von Echoes 1-20 vs. 21-57 ähnlich (-0.86% vs. -0.49%), der Bruch sitzt eindeutig an der Buchgrenze Silence/Echoes, nicht an der Tracking-Grenze.
- **Clouds (Finale) 2. Hälfte: einziges Buch mit POSITIVER Steigung (Survivorship-Effekt).** 1. Hälfte (Kap. 1-34) fällt normal (-1.33%/Kapitel), aber die 2. Hälfte (Kap. 35-68) dreht auf **+0.32%/Kapitel** — alle anderen Bücher bleiben in ihrer 2. Hälfte negativ (-0.10% bis -0.45%). Tiefpunkt bei Clouds-56 bis -61 (~154-164 Views), danach wieder ansteigend bis zum Finale-Kapitel Clouds-68 (228 Views, deutlich über dem Tal). Erklärung: wer 350+ Kapitel durchgehalten hat, ist hochgradig committed und bricht nicht mehr ab (Survivorship), plus vermutlich ein zusätzlicher "will das Ende sehen"-Curiosity-Bump genau am letzten Kapitel (Analogon zum Kapitel-1-Bump aus Abschnitt 5, hier am gegenüberliegenden Ende der Story).
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
- **KORREKTUR 02.11.: Die "GELÖST"-Einschätzung vom 24.09. war voreilig.** Oktober-Daten (02.10.-01.11.): Wochen-Ø 48 / 122 / 336 / 202 / 151 Views/Tag, Monats-Ø ~175/Tag — kein nachhaltiger Anstieg, die erste Oktoberwoche lag sogar unter dem September-Tiefpunkt (146/Tag). Verteilung ist stark bimodal: 6 von 31 Tagen (≥400 Views: 910, 852, 520, 484, 440, 431) tragen **67 %** aller Oktober-Views, 5 Tage liegen bei ≤10 Views. Plausibelste Erklärung: organische Grundlast ~10-40/Tag, darauf einzelne Binge-Leser, die an einem Tag Hunderte Kapitel lesen. Die September-Spitzen (460, 429, 507, 818, 715, 1111) passen rückblickend ins selbe Muster — der damalige "Kanal-Wechsel" stützte sich auf mehrere `status=COMPLETED`-Suchanfragen mit je nur 1 Session, also zu dünne Evidenz. Nicht verifiziert: dass die Spitzen tatsächlich einzelne Personen sind (bräuchte Per-Kapitel-Tageswerte für einen Spitzentag).
- **Per-Kapitel-Check 02.11. (Stichprobe: Kapitel 1-144, Embers-01 bis Silence-34): Die Spitzen Ende Oktober sind automatisierte Komplett-Durchläufe, keine Binge-Leser.** 26.10.: 142 von 144 Kapiteln mit exakt 1 View · 29.10.: 142 von 144 mit exakt 2 Views · 01.11.: 134 mit 1, der Rest 2-3 (nur Embers-01 bis -06 erhöht). Tagessummen passen zu ganzzahligen Vielfachen der 423 Kapitel: 431 ≈ 1×423, 852 ≈ 2×423, 440 ≈ 1×423 (+17). Abstand exakt 3 Tage (26.10. → 29.10. → 01.11.). ~~Zwei vollständige Durchläufe an einem Tag (~750k Wörter) und die perfekte Gleichverteilung schließen menschliches Lesen praktisch aus.~~ **Korrektur (User-Einwand):** Die 2 Durchläufe am 29.10. können von 2 verschiedenen Personen/Tools stammen — Views-pro-Kapitel unterscheiden das nicht. Ein einzelner Durchlauf (381.766 Wörter laut RR-Kapitelliste, Ø 903/Kapitel) ist für sehr schnelle Leser/Querleser an einem Tag machbar (~11-16 h). Der 3-Tage-Abstand ist bei 3 Ereignissen schwache Evidenz. Was bleibt: Funnel-Widerspruch — in derselben Woche hat Embers-01 nur ~5 Views über die Durchläufe hinaus (9 gesamt, davon 4 aus den Durchläufen), dem stehen 4 vollständige Lektüren gegenüber, jede innerhalb eines einzigen Kalendertags. Historisch kommt Clouds-68 auf ~7 % der Embers-01-Views (228 vs. 3.281). Ein organischer Mensch-Funnel müsste für 4 Finisher grob 50+ Starter zeigen. Fazit: automatisiert weiterhin wahrscheinlicher, aber nicht "praktisch ausgeschlossen" (mögliche Ausnahme: gezielte Binge-Leser, die schon wissen, dass sie alles lesen wollen).
- **Komplett-Durchläufe gibt es seit Ende Mai regelmäßig** (`find_full_sweeps.py`, Daten bis 07.09.): Tage, an denen JEDES der 423 Kapitel ≥1 View hat, im Juli/August bei Tagessummen von nur 450-930: 11.07., 12.07., 20.07., 29.07., 09.08., 27.08., 29.08. (Juni: weitere, dort aber organisch nicht sauber trennbar). Sauberste Fälle: 27.08. (399 von 423 Kapiteln exakt 1 View) und 29.08. (372 exakt 2 Views) — dasselbe Muster "Einzel-Durchlauf, 2 Tage später Doppel-Durchlauf" wie 26.10. → 29.10. Vor dem 12.05. nicht messbar (damals bekamen alle Kapitel ohnehin organisch Views).
- **Kandidat (User-Hypothese): RR-App selbst.** Laut RR-Knowledge-Base (Artikel 109) bietet die offizielle App für Premium-Nutzer einen "Offline Reading Mode" (Story herunterladen, offline lesen; wird ein Roman entfernt, verschwindet er "within 24 hours" aus den Downloads → die App gleicht heruntergeladene Stories regelmäßig ab). Ob Downloads/Sync als Views zählen, ist nicht dokumentiert. Alternativen: Drittanbieter-Tools (FanFicFare, WebToEpub, FicHub u. ä., auf Reddit für RR verbreitet) oder Scraper/Aggregatoren. Mit den verfügbaren Daten nicht unterscheidbar. Falls App: echte Leser, deren Lesen danach unsichtbar bleibt (offline). User bestätigt aus eigener Nutzung: Die RR-App kann ganze Stories offline laden; User-Hypothese: Leser bereiten sich auf Urlaub ohne Internet vor (Termine Ende August und Ende Oktober passen zeitlich zu typischen Ferienzeiten, Standort/Zweck aber nicht prüfbar).
- **Gegencheck Origins (Fiction 167806, 02.11.):** Origins zeigt dasselbe Durchlauf-Muster, teils an denselben Tagen. 29.08.: 37 von 37 Kapiteln mit 2-3 Views (zeitgleich mit UTE-Doppeldurchlauf). 26.10.: 44 von 45 Kapiteln exakt 1 (zeitgleich mit UTE). 30.10. und 31.10.: je ein Origins-Durchlauf (44 Kapitel), UTE an diesen Tagen 6-7 Views. 29.10. und 01.11.: UTE-Durchläufe, Origins nicht. Heißt: an manchen Tagen werden beide Fictions des Autors gemeinsam geladen, an anderen nur eine — eher mehrere Akteure mit eigenem Rhythmus als ein einziger Scraper mit festem Takt.
- **Gegencheck The Resonant (Fiction 136948, 204 Kapitel in 3 Volumes: V1 = Kap. 1-71, V2 = 72-138, V3 = 139-204, V3 veröffentlicht 27.05.):** Geprüft V1 (Kap. 1-71 + 5 aus V2) und V3 (41 von 66 Kapiteln). **Identisches Muster in V1 und V3:** 29.08.: alle Kapitel mit 2-4 Views (Doppel-Durchlauf) · 26.10.: alle exakt 1 · 29.10.: (fast) alle exakt 1 · 27./28./30./31.10. und 01.11.: keine Durchläufe. Da Kapitel 1 Neulesern ausdrücklich V3 empfiehlt, würde ein Mensch, der online liest, kaum V1 komplett mitlesen — die Durchläufe laden die **gesamte Fiction inkl. aller alten Versionen**. Das spricht klar für Download (RR-App-Offline-Modus oder EPUB-Tool) bzw. Scraper, nicht für Online-Lesen. **Am 29.08. und 26.10. wurden alle drei aktiven Fictions des Autors am selben Tag komplett geladen** (UTE + Origins + The Resonant) — jemand holt sich den gesamten Katalog des Autors. Passt zu einem Fan, der vor einer Reise "alles von diesem Autor" lädt; ein Scraper, der über die Autoren-Profilseite crawlt, erzeugt dasselbe Bild. Centerline (gestubbt, nur noch wenige öffentliche Kapitel) nicht geprüft: zu wenig Kapitel, um einen Download von einem normalen Leser zu unterscheiden. Wahrscheinlich: Download-/EPUB-Tool, Scraper oder Aggregator mit festem Takt. Konsequenz: Die organische Oktober-Grundlast ist niedriger als oben angegeben; die Einschätzung "einzelne Binge-Leser" ist für Ende Oktober widerlegt (frühere Spitzen, z. B. 16.-18.10., noch nicht geprüft). Der 18.09.-Referrer (1 User, 425 Sessions, alle mit `latest-updates`) passt rückblickend besser zu einem Tool mit festem Referrer als zu einem Menschen, der jedes Kapitel in einer neuen Session über dieselbe Seite öffnet.
- **Sommerloch vs. echter Rückgang (September) — ursprüngliche Einschätzung 24.09. (überholt, siehe Korrektur oben):** Wochendurchschnitte (Tages-Views, rollendes 31-Tage-Fenster) zeigen eine klare, sich beschleunigende Erholung: 24.-30. Aug ø229/Tag, 31. Aug-6. Sep ø163/Tag, 7.-13. Sep ø146/Tag (Tiefpunkt), 14.-20. Sep ø340/Tag, 21.-23. Sep ø716/Tag. Gesamt-Views 245,626 (18.09.) → 249,017 (24.09.) = +565/Tag im Schnitt, gegenüber +214/Tag in der Vorwoche — Wachstumsrate hat sich grob verdreifacht. **Ursache identifizierbar:** Referrer-Snapshot 24.09. zeigt einen deutlich anderen Mix als zuvor — Trending taucht gar nicht mehr auf, stattdessen stark hochskaliertes Google (112 Sessions, vorher ~25), rohes royalroad.com (461 Sessions, vorher ~78), `/my/follows` (bestehende Follower checken aktiv rein), und auffällig **mehrere verschiedene `fictions/search?status=COMPLETED&orderBy=last_update`-Anfragen** (nach Tags wie female_lead/cultivation/fantasy/strong_lead gefiltert) — sieht nach echtem "Suche nach fertigen Serien zum Bingen"-Discovery aus, nicht nach Trending-Zufallstreffern. Fazit: Sommerloch ist vorbei, aktueller Zuwachs kommt aus einem anderen (vermutlich gesuönderen, weil evergreen-fähigen) Kanal als der ursprüngliche Trending-Push.
- **Referrer-Snapshot 02.11. (letzte 7 Tage):** erstmals ein externer Social-Referrer: `android-app://com.pinterest/` mit 2 Users / 2 Sessions (Landing-Kapitel nicht erkennbar, `chapterId` immer 0) — **nicht vom Autor gepinnt**, also von Dritten geteilt. Außerdem: Referrer `source=royalroad; medium=advertising` wieder sichtbar (7 Users / 8 Sessions, im September nur 1/1), obwohl die Kampagne längst abgelaufen ist — die UTM-Parameter hängen an der damaligen Ad-Landing-URL, also sehr wahrscheinlich **Bookmarks** von Lesern aus der Ad-Kohorte (alternativ: weitergegebene Links mit diesen Parametern). Kein Hinweis auf neue Ad-Wirkung. Trending 5/5, mehrere Einzel-Klicks über andere Fictions (Similar-Recommendations) und Kommentar-Permalinks (`chapter/comment/21854936`: 4 Users).
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
