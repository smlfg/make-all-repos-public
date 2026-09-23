# make-all-repos-public

Ein Werkzeug-und-Benchmark-Repo: ~200 eigene Projekte wurden in einer Nacht per Agenten-Pipeline auf GitHub nachgeholt — und derselbe README-Auftrag an neun Modelle vergeben, um messbar zu machen, wie ehrlich LLMs über fremden Code schreiben.

> ~200 Projekte in einem Jahr gebaut, kaum etwas davon auf GitHub. In einer Nacht mit Agenten nachgeholt, und dabei gemessen, wie ehrlich verschiedene LLMs über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in `data/private/` (in `.gitignore` hinterlegt, in diesem Extract nicht enthalten — sie geraten nie in die Historie).

**Herkunft:** extrahiert aus dem Arbeitsverzeichnis make-all-repos-public; entstanden in der Nacht 22./23.09.2026 aus einer Session. Entscheidungen, Drift-Hinweise und Lessons Learned: [`FOR_SMLFLG.md`](FOR_SMLFLG.md).

## Quickstart — erste Dateien

1. [`ANALYSE.md`](ANALYSE.md) — Ergebnistabelle, Metrik-Achsen, Befunde, Vorbehalte.
2. [`FOR_SMLFLG.md`](FOR_SMLFLG.md) — warum privat statt öffentlich, welche Sicherheitsregeln gelten, was noch offen ist.
3. `skill/SKILL.md` — der vollständige Publish-/Polish-Skill des hai-agent.
4. `scripts/polish-section.md` — der Prompt-Abschnitt "Repository Polish Pass", mit dem die Modelle gemessen wurden.
5. Selbst nachrechnen:

```bash
python3 scripts/analyse.py           # Tabelle aus Rohdaten
python3 scripts/grounding.py <liste> # Treue pro Repo
```

**Benchmark-Kern (Details und Vorbehalte in [`ANALYSE.md`](ANALYSE.md)):** gleicher Prompt, 5 Repos, 9 Modell-Arme. GPT-5.5 (Hermes) führt mit 92 % Treue und 2.8 Dichte in 123 s; ling-3.0-flash-fin-free erreicht 90 % und 2.7 in 25 s. Ohne Liefer-Check wären zwei Läufe falsch gut erschienen (3 von 5 unveränderten READMEs, ein gemeldetes „POLISH_DONE 0“). Die offenen Vorbehalte — Konfundierung Harness × Modell, Selection Bias, n = 5 — stehen dort ebenfalls.

## Zwei Teile

1. **Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme → Commit/Push.
2. **Benchmark:** *same task, same harness, different model*. Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Gemessen wird maschinell, nicht per Bauchgefühl. Ergebnisse: [`ANALYSE.md`](ANALYSE.md).

## Struktur

| Pfad | Inhalt |
|---|---|
| `scripts/publish.sh`, `scripts/run-publish.sh` | Repo auf GitHub anlegen, pushen, Remote-HEAD gegen lokal prüfen |
| `scripts/push-all.sh` | Nachträgliche Commits pushen, mit Abgleich |
| `scripts/polish-one.sh` | Eine hai-agent-Session pro Repo, nur `README.md`, Scope-Guard |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt die Liste erfundener Pfade |
| `scripts/h2h-one.sh`, `scripts/oc-one.sh` | Head-to-head in Hermes bzw. OpenCode-Harness |
| `scripts/grounding.py` | Pfad-Treue: existieren die Pfade, die die README nennt? |
| `scripts/analyse.py` | Benchmark-Tabelle aus den Rohdaten |
| `scripts/eval-readme.py`, `scripts/eval3.py` | Aggregat-Eval pro Modell, Repair vorher/nachher |
| `scripts/polish-section.md` | Der "Repository Polish Pass" als Prompt-Vorlage |
| `skill/SKILL.md` | Der Publish-/Polish-Skill des hai-agent (erweitert um Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `FOR_SMLFLG.md` | Entscheidungen, Lessons Learned, offene Punkte |
| `.gitignore` | Hält private Rohdaten, gitleaks-Artefakte, Archive und Python-Caches aus der Historie |

## Grenzen

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Benchmark mit 5 Repos und einer Auswahl, die GPT begünstigt (siehe `ANALYSE.md`, Abschnitt Vorbehalte).
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend.
- Die Pipeline legt Repos privat an und pusht; öffentlich wird einzeln und manuell entschieden (Entscheidung "Privat statt öffentlich" in `FOR_SMLFLG.md`).
- Keine Secrets in diesem Repo. Private Rohdaten bleiben über `.gitignore` unversioniert; Sichtbarkeit ist eine Entscheidung von Samuel, nicht des Agenten.
