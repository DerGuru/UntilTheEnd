# Handoff – Analytics-Auswertung (Stand 07.09.2026)

Kurze Übergabe für einen frischen Chat. Kontext: laufende Pageview-Datenextraktion + geplante Auswertungen für UTE (RoyalRoad).

## Aktueller Task
Pageviews **aller 423 Kapitel** als Zeitreihe extrahieren → daraus Auswertungen fahren (keine CSV zwingend nötig, JSON reicht als Quelle).

## Datenquelle (bestätigt)
- API-Endpunkt (eingeloggt, same-origin): `https://www.royalroad.com/api/data/chapter/{chapterId}` → JSON, Pageview-Zeitreihe pro Kapitel.
- Kapitel-IDs stehen im DOM der Pageview-Seite als `data-chapter` an `a.analytics-chapter-list-item` (z.B. Embers 01 = 3053459, Embers 02 = 3056679).
- Fiction-ID: **152927**. Pageview-Seite: `/author-dashboard/analytics/pageviews/152927`.

## Extraktion
- Skript: `40 - WorkingStuff/Analytics/extract_pageviews.js` (Console-Skript, läuft im eingeloggten Browser, lädt `ute_pageviews_raw.json`).
- Cookie NIE durch das Modell routen – Skript nutzt same-origin credentials, User macht Download selbst (externer Browser).
- **Erwartete Datei:** `40 - WorkingStuff/Analytics/ute_pageviews_raw.json` (sobald der User sie dorthin legt).

## Nächste Schritte (im neuen Chat)
1. Prüfen, ob `ute_pageviews_raw.json` da ist. JSON-Struktur ansehen (Feldnamen für Datum/Views sind noch unbekannt – erst inspizieren, dann parsen).
2. Auswertungsskript (PowerShell/Python) schreiben, das die Rohdaten einliest.
3. Geplante Auswertungen: Funnel/Retention pro Kapitel & Buch, Re-Read-Spikes (Kapitel mit mehr Views als Nachbarn, z.B. Mirrors 02), tägliche Neu-Leser-Akquise (Kapitel 1 über Zeit), Peak-Zuordnung (Trending Mai), Buch-Vergleiche (Views/Kapitel, Absprung an Buchübergängen), Long-Tail (wer ist noch „unterwegs").

## Wichtige bestätigte Fakten (für Kontext)
- Serie **abgeschlossen 19.05.2026**, 423 Kapitel, 7 Bücher (Embers/Roots/Silence/Echoes/Fractures/Mirrors/Clouds).
- Views gesamt ~243k (Stand 05.09). Follower ~229. Rating 3.96 (gefallen von 4.12; AI-Tag zieht Downvotes). Favs ~51. ~195 haben das Ende erreicht.
- Funnel: Ch1→Ch2 −42% (harter, ehrlicher Filter), danach flach; fast kein Verlust am Buchübergang; ~6 % Completion.
- Trending: Peak Mai (#1 in 5 Listen), flippt auch Monate später noch gelegentlich rein. Discovery jetzt: Google (organisch), AI-Tag-Popularitätssuche (UTE #2 der Kategorie, nach Rohzahlen #1), Foren-Referrer.
- CobaltWolf-Review-Saga: abgeschlossen. Zweite PM (Craft-Gespräch, Funnel-Zahlen, Embers-25-Hook) wurde versendet. 1.5-Rating blieb, Reviewtext von RR selbst entfernt.

## Ton/Arbeitsstil des Users
- Deutsch. Ehrliche Einordnung statt Cheerleading. Mag nüchterne, datengetriebene Analyse. Entspannte Sicht auf Zahlen („nichts hängt davon ab").
