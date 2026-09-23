# Mini-Test: Datei-Manifest im Prompt

**Frage:** Senkt eine Dateiliste (`git ls-files`) im Reparatur-Auftrag die erfundenen Pfade?

**Aufbau:** 16 READMEs, die am Vortag wegen zu niedriger Pfad-Treue zurückgehalten wurden. Gleiches Modell
(deepseek-v4.1-flash), gleiche Harness (Hermes), gleicher Prüfer. Änderung: Dateiliste + Regel "jeder Pfad in
Backticks muss in der Liste stehen" (zwei Änderungen gebündelt — ehrlich vermerkt).

**Vergleichswert** (Reparatur am Vortag, gleiche 16 Repos, ohne Liste): Treue 60 % → 61 %, 28 neu erfundene Pfade.

| Repo | Treue vorher | Treue nachher | echte Pfade vorher→nachher | fehlend vorher→nachher | neu erfunden | Zeilen |
|---|---|---|---|---|---|---|
| repo-01 | 71 % | 100 % | 5→5 | 2→0 | 0 | 42→42 |
| repo-02 | 75 % | 100 % | 9→8 | 3→0 | 0 | 43→43 |
| repo-03 | 75 % | 100 % | 3→3 | 1→0 | 0 | 45→45 |
| repo-04 | 45 % | 100 % | 5→10 | 6→0 | 0 | 41→41 |
| repo-05 | 29 % | 100 % | 2→2 | 5→0 | 0 | 84→85 |
| repo-06 | 50 % | 100 % | 1→1 | 1→0 | 0 | 31→31 |
| repo-07 | 67 % | 100 % | 6→6 | 3→0 | 0 | 72→72 |
| repo-08 | 67 % | 100 % | 2→2 | 1→0 | 0 | 36→36 |
| repo-09 | 50 % | 100 % | 1→1 | 1→0 | 0 | 60→60 |
| repo-10 | 67 % | 100 % | 2→2 | 1→0 | 0 | 52→52 |
| repo-11 | 33 % | 100 % | 1→1 | 2→0 | 0 | 34→34 |
| repo-12 | 75 % | 100 % | 6→6 | 2→0 | 0 | 84→84 |
| repo-13 | 78 % | 100 % | 7→7 | 2→0 | 0 | 33→33 |
| repo-14 | 50 % | 100 % | 22→2 | 22→0 | 0 | 60→49 |
| repo-15 | 74 % | 100 % | 14→14 | 5→0 | 0 | 130→130 |
| repo-16 | 67 % | 100 % | 6→6 | 3→0 | 0 | 104→102 |

**GESAMT Treue 61 % -> 100 % | echte Pfade 92 -> 76 | fehlend 60 -> 0 | neu erfunden 0 | Zeilen 951 -> 939**

**Gegenmetrik:** Der Rückgang echter Pfade (92 → 76) stammt fast ganz aus einem Repo mit eingebettetem Git-Repo:
`git ls-files` zeigte dessen Inhalt nicht, das Modell hielt sich an die unvollständige Liste und löschte 20 echte
Pfade. Fix: `manifest.sh` löst eingebettete Repos auf. Dieses README wurde auf den Vorstand zurückgesetzt.

Repo-Namen sind anonymisiert (private Repos).
