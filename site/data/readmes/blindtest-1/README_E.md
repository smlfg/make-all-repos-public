# make-all-repos-public

> Lokale Pipeline, die private Git-Repos privat auf GitHub anlegt, plus ein LLM-Benchmark, der misst, wie ehrlich verschiedene Modelle beim README-Polish über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in `data/private/` (per `.gitignore` nie in der Historie).
**Herkunft:** entstanden in einer Nachtsession am 22./23.09.2026. Samuel hat entschieden, der hai-agent und weitere Modelle haben geschrieben; Details in [`FOR_SMLFLG.md`](FOR_SMLFLG.md).

## Erste Dateien zum Lesen

1. [`FOR_SMLFLG.md`](FOR_SMLFLG.md) — Entscheidungen, Lessons Learned, offene Schritte.
2. [`ANALYSE.md`](ANALYSE.md) — Benchmark-Ergebnisse (9 Modelle, gleicher Auftrag, gleiche 5 Repos).
3. [`skill/SKILL.md`](skill/SKILL.md) — der Publish-/Polish-Skill des hai-agent (Repo anlegen, Secret-Scan, Lizenz, Topics, Polish-Pass).
4. [`LICENSE`](LICENSE) — MIT, Copyright (c) 2026 Samuel Fleig.

## Struktur

| Pfad | Inhalt |
|---|---|
| `scripts/publish.sh` | Repo auf GitHub anlegen und pushen |
| `scripts/run-publish.sh` | Publish-Lauf einleiten |
| `scripts/push-all.sh` | Nachträgliche Commits pushen, mit Remote-Abgleich |
| `scripts/polish-one.sh` | Eine hai-agent-Session pro Repo, nur `README.md`, Scope-Guard |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt die Liste erfundener Pfade |
| `scripts/h2h-one.sh` | Head-to-head-Lauf in Hermes |
| `scripts/oc-one.sh` | Head-to-head-Lauf in OpenCode-Harness |
| `scripts/grounding.py` | Pfad-Treue: existieren die in der README genannten Pfade wirklich? |
| `scripts/eval-readme.py` | Aggregat-Eval pro Modell, ein Repository |
| `scripts/eval3.py` | Aggregat-Eval pro Modell, drei Achsen |
| `scripts/analyse.py` | Ergebnistabelle aus Rohdaten für `ANALYSE.md` |
| `scripts/polish-section.md` | Inline-Skill-Sektion für die OpenCode-Harness |
| `skill/SKILL.md` | hai-agent-Skill `local-project-github-publication` |
| `LICENSE` | MIT |
| `data/private/` | Rohlogs, Queues, Leak-Reports (per `.gitignore` nie versioniert) |

## Zwei Teile

1. **Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme → Commit/Push.
2. **Benchmark:** *same task, same harness, different model*. Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Gemessen wird maschinell, nicht per Bauchgefühl. Ergebnisse: [`ANALYSE.md`](ANALYSE.md).

## Grenzen und Sicherheit

- **Skripte enthalten hartkodierte lokale Pfade** und sind vor einer Veröffentlichung zu entpersonalisieren.
- **Benchmark mit 5 Repos und einer Auswahl, die GPT begünstigt** (siehe `ANALYSE.md`, Abschnitt Vorbehalte: Konfundierung Harness × Modell, Selection Bias, n = 5).
- **Secret-Scan mit gitleaks ist notwendig, nicht hinreichend.** Zusätzlich liegt `data/private/` mit privaten Repo-Namen und Rohlogs komplett unter `.gitignore`, damit nichts davon in die Git-Historie gerät.
- **Sichtbarkeit ist eine Samuel-Entscheidung.** Standard ist privat (zählt im Contribution-Graph, ohne Außenwirkung); öffentlich wird einzeln freigegeben.
- **Keine erfundenen Features oder Zahlen im README.** Pfade, Skriptnamen und Benchmark-Achsen in dieser Datei sind alle im Repo bzw. in `ANALYSE.md` belegt.
- **Kein Commit, kein Push durch diesen Polish-Pass.** Änderungen liegen nur im Working Tree; Veröffentlichung erfordert Samuels separate Freigabe.