# make-all-repos-public

Dieses Repo bündelt Pipeline und Benchmark, mit denen ~200 lokale Repos sicher als private GitHub-Repos veröffentlicht und README-Polish über Modelle verglichen wurde.

> ~200 Projekte in einem Jahr gebaut, kaum etwas davon auf GitHub. In einer Nacht mit Agenten nachgeholt, und dabei gemessen, wie ehrlich verschiedene LLMs über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in `data/private/` (per `.gitignore` nie in der Historie).

## Zwei Teile

1. **Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme → Commit/Push.
2. **Benchmark:** *same task, same harness, different model*. Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Gemessen wird maschinell, nicht per Bauchgefühl. Ergebnisse: [`ANALYSE.md`](ANALYSE.md).

## Benchmark (Stand 23.09.2026, n = 5)

Gleicher Auftrag an jedes Modell (*"Schreibe/überarbeite README.md nach dem Skill-Abschnitt 'Repository Polish Pass'"*), gleiche 5 Repos, Messung mit `scripts/analyse.py`. Details und Vorbehalte in `ANALYSE.md`.

| Arm | geliefert | Treue | Dichte | Dauer |
|---|---|---|---|---|
| gpt-5.5 (hermes) | 5/5 | 92 % | 2.8 | 123 s |
| ling-3.0-flash-fin-free (opencode) | 5/5 | 90 % | 2.7 | 25 s |
| muse-spark-1.3-contributor-free (opencode) | 4/5 | 86 % | 2.1 | 52 s |

Treue = Anteil existierender Pfade in Backticks; Dichte = überprüfbare Pfade pro 10 Zeilen. Befunde: kostenlos nah an GPT, Halluzination ist fehlendes Hinschauen, Repair erfindet selbst neue Pfade, stille Fallbacks verfälschen Läufe.

## Quickstart

Zuerst lesen: `ANALYSE.md`, dann `FOR_SMLFLG.md`, dann `skill/SKILL.md`.

```bash
python3 scripts/analyse.py          # Tabelle aus Rohdaten
python3 scripts/grounding.py <liste> # Treue pro Repo
```

Rohdaten (private Repo-Namen) liegen in `data/private/` und sind nicht versioniert.

## Struktur

| Pfad | Inhalt |
|---|---|
| `README.md` | Diese Übersicht |
| `ANALYSE.md` | Benchmark-Tabelle, Befunde, Vorbehalte |
| `FOR_SMLFLG.md` | Entscheidungen, Lessons Learned, offene Schritte |
| `LICENSE` | MIT-Lizenz |
| `.gitignore` | Schließt u. a. `data/private/` aus |
| `skill/SKILL.md` | Der Publish-/Polish-Skill des hai-agent (erweitert um Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `scripts/publish.sh`, `scripts/run-publish.sh` | Repo auf GitHub anlegen, pushen, Remote-HEAD gegen lokal prüfen |
| `scripts/push-all.sh` | Nachträgliche Commits pushen, mit Abgleich |
| `scripts/polish-one.sh` | Eine hai-agent-Session pro Repo, nur `README.md`, Scope-Guard |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt die Liste erfundener Pfade |
| `scripts/h2h-one.sh`, `scripts/oc-one.sh` | Head-to-head in Hermes bzw. OpenCode-Harness |
| `scripts/grounding.py` | Pfad-Treue: existieren die Pfade, die die README nennt? |
| `scripts/eval-readme.py`, `scripts/eval3.py` | Aggregat-Eval pro Modell, Repair vorher/nachher |
| `scripts/analyse.py` | Baut die Benchmark-Tabelle aus Rohdaten |
| `data/private/` | Rohlogs, Queues, Leak-Reports (ignoriert) |

## Grenzen

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Benchmark mit 5 Repos und einer Auswahl, die GPT begünstigt (siehe `ANALYSE.md`, Abschnitt Vorbehalte).
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend.
- Default ist privat, nicht öffentlich; Sichtbarkeit bleibt eine Einzelfall-Entscheidung (siehe `FOR_SMLFLG.md`).
- Keine Secrets in Repo oder Historie; Funde blockieren die Veröffentlichung bis zur Entscheidung.

## Herkunft

Entstanden in der Nacht 22./23.09.2026 aus einer einzigen Session (siehe `FOR_SMLFLG.md`); dieser Stand ist ein Benchmark-Eintrag aus demselben Harness, keine Produktiv-Pipeline.
