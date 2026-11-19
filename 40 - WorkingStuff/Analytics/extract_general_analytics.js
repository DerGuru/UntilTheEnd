// UTE General-Analytics-Extraktor (Reader Activity Per Chapter / readerActivityData)
// Ausführen auf der bereits offenen Seite:
//   https://www.royalroad.com/author-dashboard/analytics/general/152927
// F12 -> Console -> dieses Skript einfügen -> Enter.
// Kein Fetch noetig -- "readerActivityData" ist bereits als Variable auf der Seite
// vorhanden (siehe <script>-Tag im Quelltext). Das Skript liest sie nur aus und
// laedt "ute_general_analytics.json" herunter. Verlaesst nie deinen Rechner
// ausser als Download; kein Cookie-Zugriff noetig.

(() => {
  if (typeof readerActivityData === 'undefined') {
    console.error('readerActivityData nicht gefunden. Bist du auf der General-Analytics-Seite, und ist sie fertig geladen?');
    return;
  }
  const out = {
    capturedAt: new Date().toISOString(),
    data: readerActivityData,
  };
  console.log('Gefundene Kapitel:', readerActivityData.length);
  const blob = new Blob([JSON.stringify(out)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'ute_general_analytics.json';
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log(`FERTIG. ${readerActivityData.length} Kapitel exportiert nach "ute_general_analytics.json".`);
  console.log('Falls kein Download kam: JSON.stringify(readerActivityData) manuell kopieren.');
})();
