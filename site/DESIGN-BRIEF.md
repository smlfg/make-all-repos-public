# Design-Auftrag: site/index.html optisch aufpeppen — Inhalt bleibt König

Die Seite ist inhaltlich fertig und geprüft, wirkt aber zu grau und brav. Gib ihr Energie und Wiedererkennung,
**ohne vom Inhalt abzulenken**. Ein Leser soll schneller verstehen, nicht länger staunen.

## Absolut unverändert (wird maschinell geprüft)
- Jeder sichtbare Text, jede Überschrift, jede Zahl, jeder Link. Keine neuen Aussagen, keine gestrichenen.
- Das Daten-Array `ROUNDS` im Skript (alle 139 Werte) und die Datenpunkte der Streudiagramme.
- Reihenfolge der Abschnitte. Deutsch bleibt Deutsch.

## Was du ändern darfst — Ideen, du entscheidest
- **Hero mit Präsenz:** größere, selbstbewusstere Typografie; die drei Kennzahlen als echte Blickfänger
  (z. B. Vorher-Wert klein und durchgestrichen, Nachher-Wert groß in Akzentfarbe); ein ruhiges grafisches Motiv
  aus Datenpunkten oder einem Raster als Hintergrund — dezent, keine Stock-Deko.
- **Farbe mit Bedeutung:** eine konsistente Farbe pro Kategorie (kostenlos = Akzent 1, Abo = Akzent 2) überall
  gleich, Ergebnisstufen (schwach/mittel/gut/Spitze) als kleine farbige Markierungen statt nur Text.
- **Galerie mit Haptik:** Karten mit Tiefe, Umdreh- oder Aufklapp-Animation beim Aufdecken, der Buchstabe als
  großes Motiv, sichtbarer Fortschritt (z. B. "3 von 9 aufgedeckt").
- **Rhythmus:** Abschnitte klarer voneinander abgesetzt (Hintergrundtöne, Nummern, Trennlinien mit Charakter),
  Lektionen-Karten mit großer Kennzahl als Anker.
- **Diagramme:** kräftigere Punkte, Hervorhebung des Siegers (muse-spark-1.2), Tooltip beim Überfahren.
- **Bewegung sparsam:** dezentes Einblenden beim Scrollen, Zahlen dürfen einmal hochzählen — alles aus bei
  `prefers-reduced-motion: reduce`.

## Leitplanken
- Weiterhin eine Datei, CSS/JS inline, keine externen Bibliotheken, keine Webfonts.
- Hell- und Dunkelmodus müssen beide stimmen (Farben als CSS-Variablen auf `:root`, Dunkel per
  `@media (prefers-color-scheme: dark)`); Text nie in Akzentfarbe auf Akzentfläche mit schwachem Kontrast.
- Funktioniert auf Handybreite (16 px Rand, kein horizontales Scrollen der Seite).
- Kein generischer KI-Look: keine Regenbogen-Verläufe, keine Glassmorphism-Orgie, keine Emojis als Deko.

## Harte Grenzen
- Nur `site/index.html` ändern. Kein git commit, kein git push, keine gh-Aufrufe.
- Zum Schluss genau eine Zeile: `DESIGN_DONE <Anzahl Änderungen>` oder `DESIGN_FAIL <Grund>`.
