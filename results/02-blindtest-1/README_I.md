# make-all-repos-public

> ~200 Projekte in einem Jahr gebaut, kaum etwas davon auf GitHub. In einer Nacht mit Agenten nachgeholt, und dabei gemessen, wie ehrlich verschiedene LLMs über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in `data/private/` (per `.gitignore` nie in der Historie).

## Zwei Teile

1. **Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme → Commit/Push.
2. **Benchmark:** *same task, same harness, different model*. Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Gemessen wird maschinell, nicht per Bauchgefühl. Ergebnisse: [`ANALYSE.md`](ANALYSE.md).

## Erste Dateien zum Lesen

1. [`ANALYSE.md`](ANALYSE.md) — Benchmark-Ergebnisse: Tabelle, Befunde, Vorbehalte, Reproduzier-Befehle.
2. [`FOR_SMLFLG.md`](FOR_SMLFLG.md) — Herkunft, getroffene Entscheidungen, Lessons Learned.
3. `skill/SKILL.md` — der Publish-/Polish-Skill des hai-agent.
4. `scripts/polish-section.md` — der Polish-Auftragstext, den der OpenCode-Arm liest.

## Benchmark in Kürze

Auftrag an jedes Modell: *"Schreibe/überarbeite README.md nach dem Skill-Abschnitt 'Repository Polish Pass'."* Gemessen mit `scripts/analyse.py`; **Treue** = Anteil der in Backticks genannten Pfade, die im Repo existieren, **Dichte** = echte, überprüfbare Pfade pro 10 Zeilen.

- GPT-5.5 (hermes): 5/5 geliefert, 92 % Treue, Dichte 2.8, 27 Tool-Calls, 123 s.
- ling-3.0-flash-fin-free (opencode): 5/5, 90 % Treue, Dichte 2.7, 25 s — bis auf 2 Punkte an GPT heran, fünfmal schneller.
- MiniMax-M3 (hermes): 5/5, 80 % Treue, aber Dichte 1.2 bei 83 Zeilen; im Head-to-head 0 Reasoning-Tokens trotz `reasoning_effort: xhigh`.
- Nicht geliefert: nemotron-3.5-lightning (2/5); muse-spark-1.3 meldete POLISH_DONE 0.
- Ein Repair-Durchgang hob die Pfad-Treue von 61 % auf 82 %: 147 erfundene Pfade gestrichen, 105 echte ergänzt, 43 neue erfunden.

Die vollständige Tabelle mit allen 9 Armen und die Vorbehalte stehen in [`ANALYSE.md`](ANALYSE.md).

## Struktur

| Pfad | Inhalt |
|---|---|
| `scripts/publish.sh`, `scripts/run-publish.sh` | Repo privat auf GitHub anlegen, pushen, Remote-HEAD gegen lokal prüfen |
| `scripts/push-all.sh` | Nachträgliche Commits pushen, mit Abgleich |
| `scripts/polish-one.sh` | Eine hai-agent-Session pro Repo, nur `README.md`, Scope-Guard |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt die Liste erfundener Pfade |
| `scripts/h2h-one.sh`, `scripts/oc-one.sh` | Head-to-head in Hermes bzw. OpenCode-Harness |
| `scripts/polish-section.md` | Der Polish-Auftragstext für den OpenCode-Arm |
| `scripts/grounding.py` | Pfad-Treue: existieren die Pfade, die die README nennt? |
| `scripts/analyse.py`, `scripts/eval3.py`, `scripts/eval-readme.py` | Aggregat-Eval pro Modell, Repair vorher/nachher |
| `skill/SKILL.md` | Der Publish-/Polish-Skill des hai-agent (erweitert um Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `ANALYSE.md`, `FOR_SMLFLG.md` | Benchmark-Ergebnisse; Herkunft, Entscheidungen, Lessons Learned |
| `data/private/` | Rohlogs, Queues, Leak-Reports (ignoriert) |
| `.gitignore` | hält `data/private/`, das gitleaks-Binary und `*.tar.zst` aus der Historie |
| `LICENSE` | MIT |

## Grenzen

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Benchmark mit 5 Repos und einer Auswahl, die GPT begünstigt (siehe `ANALYSE.md`, Abschnitt Vorbehalte).
- Harness × Modell sind konfundiert, n = 5: Hinweis, kein Urteil.
- Die Metrik prüft Existenz, nicht Bedeutung: ob eine Beschreibung stimmt, misst sie nicht.
- Agent-Schritte ändern in den Ziel-Repos nur `README.md` und committen nicht; Commit und Push passieren separat.
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend.
- Rohdaten mit privaten Repo-Namen bleiben lokal: `data/private/` ist per `.gitignore` nie in der Historie.
