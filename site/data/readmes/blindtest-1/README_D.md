# make-all-repos-public

> Diese Pipeline inventarisiert ~200 lokale Git-Repos, prüft sie mit Secret-Scan und veröffentlicht sie als private GitHub-Repos, und misst im Head-to-head wie treu verschiedene LLMs beim README-Polish bleiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen in data/private/ (per `.gitignore` nie in der Historie).

## Herkunft

Entstanden in der Nacht 22./23.09.2026 aus einer einzigen Session (Samuel entschieden, Claude orchestriert, hai-agent und andere Modelle geschrieben) — siehe `FOR_SMLFLG.md`. Dieses Entry ist ein extrahierter Stand aus _contest-marp-20260923/entries/oc-muse-spark-1.2-contributor-free, `git log` ab `453ba14` (Initial commit). Drift: hier nur README-Polish, keine Pipeline-Ausführung; Rohlogs/Queues bleiben in data/private/ und sind nicht versioniert.

## Quickstart — zuerst lesen

1. `FOR_SMLFLG.md` — Entscheidungen, Lessons Learned, offene Punkte.
2. `ANALYSE.md` — Benchmark-Tabelle und Vorbehalte (n=5, gleiche Repos, gleicher Prompt).
3. `skill/SKILL.md` — Publish-/Polish-Skill (Abschnitt „Repository Polish Pass" ist der Auftrag).

```bash
cat ANALYSE.md
cat FOR_SMLFLG.md
python3 scripts/analyse.py        # Tabelle aus Rohdaten reproduzieren
python3 scripts/grounding.py <liste>  # Treue der genannten Pfade prüfen
```

## Benchmark (aus `ANALYSE.md`, 23.09.2026)

Gleicher Auftrag — „Schreibe/überarbeite `README.md` nach `skill/SKILL.md` → Repository Polish Pass" — gleiche 5 Repos, gleicher Ausgangsstand, Messung mit `scripts/analyse.py` und `scripts/grounding.py`.

| Arm | geliefert | Treue | Dichte | Abschnitte | Zeilen | Tool-Calls | Dauer |
|---|---|---|---|---|---|---|---|
| gpt-5.5 (hermes) | 5/5 | 92 % | 2.8 | 4.0/4 | 43 | 27 | 123 s |
| muse-spark-1.2-contributor-free (opencode, dieses Entry) | 4/5 | 90 % | 2.8 | 4.0/4 | 57 | 17 | 66 s |

Vollständige Tabelle und Befunde in `ANALYSE.md` — u. a. ling-3.0-flash-fin-free 90 %/2.7 in 25 s (nahe GPT, 5× schneller), MiniMax 83 %/1.2 bei 83 Zeilen.

## Struktur

| Pfad | Inhalt |
|---|---|
| `scripts/publish.sh` | Repo auf GitHub anlegen, pushen, Remote-HEAD gegen lokal prüfen |
| `scripts/run-publish.sh` | Wrapper um `scripts/publish.sh` |
| `scripts/push-all.sh` | Nachträgliche Commits pushen, mit Abgleich |
| `scripts/polish-one.sh` | Eine hai-agent-Session pro Repo, nur `README.md`, Scope-Guard |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt Liste erfundener Pfade |
| `scripts/h2h-one.sh` | Head-to-head in Hermes-Harness |
| `scripts/oc-one.sh` | Head-to-head in OpenCode-Harness |
| `scripts/grounding.py` | Pfad-Treue: existieren die genannten Pfade? |
| `scripts/analyse.py` | Head-to-head-Tabelle aus Rohdaten |
| `scripts/eval-readme.py` | Aggregat-Eval pro Modell |
| `scripts/eval3.py` | Aggregat-Eval Repair vorher/nachher |
| `scripts/polish-section.md` | Prompt-Abschnitt für den Polish-Pass |
| `skill/SKILL.md` | Publish-/Polish-Skill (Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `ANALYSE.md` | Benchmark-Ergebnisse und Vorbehalte |
| `FOR_SMLFLG.md` | Architektur, Entscheidungen, Lessons Learned |
| `LICENSE` | MIT |
| `.gitignore` | Schließt data/private/, gitleaks-Artefakte, __pycache__/ aus |

## Grenzen & Sicherheit

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Benchmark mit n=5 und Auswahl, die GPT begünstigt (erste Repos mit GPT ≥ 80 %, siehe `ANALYSE.md` Abschnitt Vorbehalte); Harness × Modell konfundiert.
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend; data/private/ bleibt per `.gitignore` lokal und nie in der Historie.
- Keine Secrets im Repo, keine Freigabe für Commit/Push ohne Prüfung; `python3 scripts/grounding.py` ist die deterministische Abnahme statt LLM-Selbstprüfung.
