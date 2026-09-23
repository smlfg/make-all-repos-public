# Polish-Auftrag für site/index.html (Abnahme-Befunde vom 23.09.2026)

Ändere NUR `site/index.html`. Behalte Sprache (Deutsch), Design, Struktur und alle Zahlen bei. Keine neuen Funktionen.
Quellen zum Nachprüfen: `site/data/results.json`, `results/04-benchmark-2/AUSWERTUNG.md`, `results/01-kopf-an-kopf/ANALYSE.md`.

1. **Erfundene Aussage entfernen.** Im Abschnitt "Was „blind“ hier heißt" steht:
   "…und im ersten Test stufte das blind bewertete Spitzenmodell später zur Mittelmarke ab, als der Modellname dazukam."
   Das ist nie passiert und steht in keiner Quelle. Ersetze den Satz "Zwei Aussagen beweisen, dass das trägt: …" durch
   eine belegte Aussage, z. B.: "Dass das trägt, zeigt eine Beobachtung: Die Blind-Prognosen „das ist deepseek“ lagen
   zweimal daneben — der Bewerter erkannte das Modell nicht am Stil."
2. **Hero-Untertitel korrigieren.** "Einmal, ein Repo, neun Modelle" passt nicht zum Hauptbenchmark: dort waren es
   zwei Repos (hai-mcp, Sidecar-ng) und acht Modelle in einer Harness (MiniMax ausgeschlossen). Formuliere korrekt.
3. **Übertreibung korrigieren.** "muse-spark-1.3 … wird zur besten README gewählt" — bei hai-mcp waren drei Modelle
   "Spitze" (muse-spark-1.2, muse-spark-1.3, deepseek-v4.1-flash). Formuliere: "…und landet trotzdem in der Spitzengruppe."
4. **Kopierfehler.** "Belege zu Lektion 01 und 02" steht zweimal; das zweite Vorkommen muss "Belege zu Lektion 03 und 04" heißen.
5. **Überlappende Diagramm-Beschriftungen.** In den beiden Streudiagrammen überdecken sich Labels (z. B. "ling-3.0"
   liegt auf seinem Punkt; bei hai-mcp stehen "deepseek" und "muse-spark-1.3" gedrängt). Versetze die Labels so,
   dass keines einen Punkt oder ein anderes Label überdeckt. Punktpositionen (Daten) NICHT ändern.

Harte Grenzen: nur `site/index.html` ändern; kein git commit/push, keine gh-Aufrufe.
Zum Schluss genau eine Zeile: `POLISH_DONE <Anzahl behobener Punkte>` oder `POLISH_FAIL <Grund>`.
