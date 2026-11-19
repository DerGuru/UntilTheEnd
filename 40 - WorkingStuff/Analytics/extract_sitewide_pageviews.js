// UTE "Page Views" (Site-Wide Daily Total) Extraktor
// Ausführen auf einer beliebigen eingeloggten RoyalRoad-Seite (z.B. General Analytics):
//   https://www.royalroad.com/author-dashboard/analytics/general/152927
// F12 -> Console -> dieses Skript einfuegen -> Enter.
// Nutzt denselben API-Stil wie extract_pageviews.js, aber den Endpunkt
// "/api/data/chapterv/{fictionId}" -- liefert die TAGESSUMME ueber ALLE Kapitel
// (identische Struktur wie die Pro-Kapitel-API: date/unixtime/views/previous).
// Kein Hover, kein Pixel-Kalibrieren noetig. Same-origin Cookie, verlaesst nie
// deinen Rechner ausser als Download.

(async () => {
  const FICTION_ID = 152927; // Until the End
  try {
    const r = await fetch(`/api/data/chapterv/${FICTION_ID}`, {
      headers: { Accept: 'application/json' },
      credentials: 'same-origin',
    });
    if (!r.ok) {
      console.error('Request fehlgeschlagen, Status:', r.status);
      return;
    }
    const data = await r.json();
    console.log(`Gefunden: ${data.length} Tage Seiten-weite Page-Views-Daten.`);
    const blob = new Blob([JSON.stringify(data)], { type: 'application/json' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = 'ute_sitewide_pageviews.json';
    document.body.appendChild(a);
    a.click();
    a.remove();
    console.log('FERTIG. Datei "ute_sitewide_pageviews.json" heruntergeladen.');
  } catch (e) {
    console.error('Fehler:', e);
  }
})();
