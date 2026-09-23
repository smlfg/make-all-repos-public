# make-all-repos-public

> ~200 Projekte in einem Jahr gebaut, kaum etwas davon auf GitHub. In einer Nacht mit Agenten nachgeholt, und dabei gemessen, wie ehrlich verschiedene LLMs über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in `data/private/` (per `.gitignore` nie in der Historie).

## Schnellstart

1. [`ANALYSE.md`](ANALYSE.md) — Benchmark-Ergebnisse aller 9 Modelle (gleicher Auftrag, 5 Repos, gemessen maschinell).
2. [`skill/SKILL.md`](skill/SKILL.md) — Der Publish-/Polish-Skill des hai-agent (Lizenz, Topics, gitleaks, Worktree, Default-Branch).
3. [`scripts/publish.sh`](scripts/publish.sh) — Erster Einstieg: Repo auf GitHub anlegen, pushen, Remote-HEAD prüfen.
4. [`scripts/grounding.py`](scripts/grounding.py) — Pfad-Treue: Existenz der in READMEs genannten Pfade deterministisch prüfen.
5. [`FOR_SMLFLG.md`](FOR_SMLFLG.md) — Entscheidungen, Lessons Learned, offene Fragen.

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
| `scripts/analyse.py` | Benchmark-Tabelle aus Rohdaten generieren |
| `skill/SKILL.md` | Publish-/Polish-Skill des hai-agent (erweitert um Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `ANALYSE.md` | Benchmark-Ergebnisse: 9 Modelle, 5 Repos, gleicher Auftrag |
| `data/private/` | Rohlogs, Queues, Leak-Reports (per `.gitignore` ignoriert) |

## Ablauf

**Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie (`gitleaks`) → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme (`grounding.py`) → Commit/Push.

**Benchmark:** *same task, same harness, different model.* Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Messung via `scripts/analyse.py`. Ergebnisse: [`ANALYSE.md`](ANALYSE.md).

## Grenzen

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Benchmark mit 5 Repos und einer Auswahl, die GPT begünstigt (siehe `ANALYSE.md`, Abschnitt Vorbehalte).
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend.
- `data/private/` bleibt per `.gitignore` immer ausgeschlossen — private Repo-Namen nie in der Historie.
- Kein Secret, kein API-Key, kein privater Pfad in diesem Repo.

## Herkunft

Entstanden in der Nacht 22./23.09.2026 aus einer einzigen Session im Workspace `_contest-marp-20260923/entries/`. Samuel entschied, Claude orchestrierte, hai-agent und andere Modelle schrieben. Aus dem übergeordneten Workspace extrahiert, mit eigener `.gitignore` und `LICENSE`.

## Benchmark

| Arm | Treue | Dichte | Abschnitte | Zeilen | Dauer |
|---|---|---|---|---|---|
| gpt-5.5 (hermes) | 92 % | 2.8 | 4.0/4 | 43 | 123 s |
| nemotron-3-ultra-free (opencode) | 91 % | 2.5 | 4.0/4 | 48 | 81 s |
| deepseek-v4.1-flash (hermes) | 90 % | 2.5 | 4.0/4 | 60 | 108 s |
| **ling-3.0-flash-fin-free (opencode)** | **90 %** | **2.7** | **4.0/4** | **48** | **25 s** |
| muse-spark-1.2-contributor-free (opencode) | 90 % | 2.8 | 4.0/4 | 57 | 66 s |
| nemotron-3.5-lightning-free (opencode) | 89 % | 2.1 | 4.0/4 | 38 | 292 s |
| muse-spark-1.3-contributor-free (opencode) | 86 % | 2.1 | 4.0/4 | 51 | 52 s |
| mimo-v2.6-flash-free (opencode) | 83 % | 2.3 | 4.0/4 | 58 | 88 s |
| MiniMax-M3 (hermes) | 80 % | 1.2 | 3.8/4 | 83 | 39 s |

Siehe `ANALYSE.md` für Details, Vorbehalte und Reproduktion.
