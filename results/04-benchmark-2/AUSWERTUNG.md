# Auswertung Benchmark 2 (23.09.2026) — 1 Harness (OpenCode), 2 Repos, gleiche Dateiliste, blind bewertet

| Modell | hai-mcp (Urteil / Treue / Zeilen) | Sidecar-ng (Urteil / Treue / Zeilen) | kostet |
|---|---|---|---|
| muse-spark-1.2 (free) | **Spitze** / 82 % / 379 | **Spitze** / 100 % / 157 | 0 $ |
| deepseek-v4.1-flash | **Spitze**\* / 81 % / 366 | gut / 100 % / 131 | OpenCode-Go-Abo |
| muse-spark-1.3 (free) | **Spitze** / 80 % / 348 | gut / 100 % / 72 | 0 $ |
| gpt-5.5 | gut / 100 % / 81 | gut / 100 % / 60 | Codex-Abo |
| mimo-v2.6-flash (free) | schwach (zu lang) / 83 % / 373 | gut / 100 % / 132 | 0 $ |
| ling-3.0-flash (free) | gut / 79 % / 360 | schwach (Aufgabe verfehlt)\* / 73 % / 66 | 0 $ |
| nemotron-3-ultra (free) | schwach / 85 % / 188 | mittel / 67 % / 125 | 0 $ |
| nemotron-3.5-lightning (free) | – (nichts geändert) | mittel / 100 % / 69 | 0 $ |
| MiniMax-M3 | ausgeschlossen (401, Token-Plan-Key ungültig) | ausgeschlossen | – |

\* Buchstabe im Transkript nicht gesprochen, Zuordnung aus Reihenfolge.

**Treue bei hai-mcp:** Das Original-README hat selbst 74 % — die "fehlenden" Pfade sind Laufzeit-Artefakte
(`NEXT_STEP.md`) und Platzhalter (`<project>/…`, `HAI_HOME/skills/<skill_id>.json`), die die Modelle
auftragsgemäß übernommen haben. Neu erfunden über alle 8 Einträge: genau 1 Pfad. Prüfer-Grenze, kein Modellfehler.

**Befunde**
1. In einer Harness + mit Dateiliste gewinnt ein **Free-Modell** (muse-spark-1.2) in beiden Repos. Im ersten Test
   (andere Harness-Mischung, ohne Dateiliste, anderes Repo) war es nur "mittel".
2. Samuels Blind-Prognosen "das ist deepseek" lagen beide Male daneben (F und G statt E und H) — der Blindtest wirkt.
3. gpt-5.5 schreibt die kürzesten READMEs (60–81 Zeilen) und hat immer 100 % Treue, aber nie "Spitze".
4. Länge ist ein Urteilskriterium: mimo (373 Zeilen) "zu lang, würde ich nicht lesen".
n = 2 Repos, 1 Bewerter — Tendenz, kein Gesetz.
