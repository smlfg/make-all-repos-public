# make-all-repos-public

> ~200 Projekte in einem Jahr gebaut, kaum etwas davon auf GitHub. In einer Nacht mit Agenten nachgeholt, und dabei gemessen, wie ehrlich verschiedene LLMs über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in `data/private/` (per `.gitignore` nie in der Historie).

## Zwei Teile

1. **Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme → Commit/Push.
2. **Benchmark:** *same task, same harness, different model*. Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Gemessen wird maschinell, nicht per Bauchgefühl. Ergebnisse: [`ANALYSE.md`](ANALYSE.md).

## Struktur

| Pfad | Inhalt |
|---|---|
| `scripts/publish.sh`, `run-publish.sh` | Repo auf GitHub anlegen, pushen, Remote-HEAD gegen lokal prüfen |
| `scripts/push-all.sh` | Nachträgliche Commits pushen, mit Abgleich |
| `scripts/polish-one.sh` | Eine hai-agent-Session pro Repo, nur `README.md`, Scope-Guard |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt die Liste erfundener Pfade |
| `scripts/h2h-one.sh`, `oc-one.sh` | Head-to-head in Hermes bzw. OpenCode-Harness |
| `scripts/grounding.py` | Pfad-Treue: existieren die Pfade, die die README nennt? |
| `scripts/eval-readme.py`, `eval3.py` | Aggregat-Eval pro Modell, Repair vorher/nachher |
| `skill/SKILL.md` | Der Publish-/Polish-Skill des hai-agent (erweitert um Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `data/private/` | Rohlogs, Queues, Leak-Reports (ignoriert) |

## Grenzen

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Benchmark mit 5 Repos und einer Auswahl, die GPT begünstigt (siehe `ANALYSE.md`, Abschnitt Vorbehalte).
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend.
