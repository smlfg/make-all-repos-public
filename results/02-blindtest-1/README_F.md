# oc-nemotron-3-ultra-free — Marp Contest Entry

OpenCode-Harness-Benchmark: *same task, same harness, different model*. Neun Modelle schreiben dieselbe README-Polish-Aufgabe an fünf Repos; maschinell ausgewertet auf Pfad-Treue, Dichte und Abdeckung.

**Status:** Contest-Eintrag, lokal. Benchmark-Rohdaten mit privaten Repo-Namen liegen in `data/private/` (per `.gitignore` nie in der Historie).

## Quickstart

```bash
# Ergebnisse ansehen
cat ANALYSE.md

# Rohdaten neu berechnen
python3 scripts/analyse.py

# Pfad-Treue eines Repos prüfen
python3 scripts/grounding.py <repo-liste>
```

**Erste Dateien zum Lesen:** `ANALYSE.md` (Ergebnisse & Befunde), `scripts/analyse.py` (Auswertung), `scripts/grounding.py` (Treue-Prüfung), `skill/SKILL.md` (Polish-Skill).

## Struktur

| Pfad | Inhalt |
|---|---|
| `ANALYSE.md` | Benchmark-Ergebnisse: 9 Modelle × 5 Repos, Tabellen, Befunde, Vorbehalte, Reproduktion |
| `scripts/analyse.py` | Aggregiert Rohdaten → Markdown-Tabelle (Treue, Dichte, Abschnitte, Zeilen, Tool-Calls, Dauer) |
| `scripts/grounding.py` | Deterministische Pfad-Existenz-Prüfung: zählen echte vs. erfundene Pfade in READMEs |
| `scripts/eval-readme.py`, `scripts/eval3.py` | Modell-weite Aggregation, Repair-Vergleich vorher/nachher |
| `scripts/polish-one.sh` | Eine Polish-Session pro Repo (hai-agent, Scope-Guard) |
| `scripts/repair-one.sh` | Nachbesserung: Agent bekommt Liste erfundener Pfade |
| `scripts/h2h-one.sh`, `scripts/oc-one.sh` | Head-to-head in Hermes vs. OpenCode-Harness |
| `scripts/publish.sh`, `scripts/run-publish.sh` | Repo auf GitHub anlegen, pushen, Remote-HEAD abgleichen |
| `scripts/push-all.sh` | Nachträgliche Commits pushen mit Abgleich |
| `skill/SKILL.md` | Der Publish-/Polish-Skill (Lizenz, Topics, gitleaks, Worktree, Default-Branch) |
| `data/private/` | Rohlogs, Queues, Leak-Reports (ignoriert) |
| `FOR_SMLFLG.md` | Architektur, Decisions, Lessons Learned (persönlich) |
| `LICENSE` | MIT |

## Grenzen & Sicherheit

- **Selection Bias:** 5 Repos wurden so ausgewählt, dass GPT ≥ 80 % Treue hatte; vier davon "Agent*". Begünstigt GPT und einfache Repos. Siehe `ANALYSE.md` Abschnitt *Vorbehalte*.
- **Konfundierung Harness × Modell:** GPT/deepseek/MiniMax liefen in Hermes (Skill geladen), Free-Modelle in OpenCode (Skill inline). Harness-Effekt und Modell-Effekt sind nicht getrennt.
- **n = 5:** Hinweis, kein Urteil.
- **Metrik prüft Existenz, nicht Bedeutung:** Ob die Beschreibung stimmt, misst sie nicht. Dafür: menschliches Urteil (Blindtest) oder Judge.
- **Secret-Scan:** `gitleaks` in der Pipeline ist notwendig, nicht hinreichend.
- **Skripte enthalten hartkodierte lokale Pfade** und sind vor einer Veröffentlichung zu entpersonalisieren.
- **Stille Fallbacks verfälschen Benchmarks:** Ein als deepseek gestarteter Lauf war nach 401 still MiniMax. Jede Hermes-Session wird gegen `state.db` auf das tatsächliche Modell geprüft.

## Herkunft

Entstanden in der Nacht 22./23.09.2026 aus einer einzigen Session. Samuel hat entschieden, Claude hat orchestriert, der hai-agent und andere Modelle haben geschrieben. Dieses Repo ist der OpenCode-Eintrag (nemotron-3-ultra-free) für den Marp-Contest 2026-09-23.