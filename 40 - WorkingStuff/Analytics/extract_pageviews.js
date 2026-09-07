// UTE Pageview-Extraktor
// Ausführen in der eingeloggten RoyalRoad-Analytics-Seite:
//   /author-dashboard/analytics/pageviews/152927
// F12 -> Console -> dieses Skript einfügen -> Enter.
// Es laedt am Ende "ute_pageviews_raw.json" herunter.
// Der Session-Cookie wird vom Browser automatisch mitgeschickt (same-origin).
// Es verlaesst nie deinen Rechner ausser als Download.

(async () => {
  const els = [...document.querySelectorAll('a[data-chapter][data-chapter-title]')];
  const seen = new Set();
  const chapters = [];
  for (const el of els) {
    const id = el.dataset.chapter;
    if (!id || seen.has(id)) continue;
    seen.add(id);
    chapters.push({ id, title: el.dataset.chapterTitle });
  }
  console.log('Gefundene Kapitel:', chapters.length);
  if (!chapters.length) { console.warn('Keine Kapitel gefunden - stimmt die Seite?'); return; }

  const out = [];
  for (let i = 0; i < chapters.length; i++) {
    const c = chapters[i];
    try {
      const r = await fetch(`/api/data/chapter/${c.id}`, { headers: { Accept: 'application/json' }, credentials: 'same-origin' });
      out.push({ id: c.id, title: c.title, status: r.status, data: await r.json() });
    } catch (e) {
      out.push({ id: c.id, title: c.title, error: String(e) });
    }
    if (i % 25 === 0) console.log(`${i + 1}/${chapters.length} ...`);
    await new Promise(res => setTimeout(res, 120)); // hoeflich zum Server
  }

  window.__uteData = out; // Fallback, falls der Download blockiert wird
  const blob = new Blob([JSON.stringify(out)], { type: 'application/json' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'ute_pageviews_raw.json';
  document.body.appendChild(a);
  a.click();
  a.remove();
  console.log(`FERTIG. ${out.length} Kapitel. Datei "ute_pageviews_raw.json" heruntergeladen.`);
  console.log('Falls kein Download kam: JSON.stringify(window.__uteData) manuell kopieren.');
})();
