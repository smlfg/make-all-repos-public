# make-all-repos-public

`make-all-repos-public` ist ein lokales Pipeline- und Benchmark-Repo für die Nachtaktion, in der ~200 Projekte sicher nach GitHub gebracht und README-Polish-Agenten auf Pfadtreue gemessen wurden.

> ~200 Projekte in einem Jahr gebaut, kaum etwas davon auf GitHub. In einer Nacht mit Agenten nachgeholt, und dabei gemessen, wie ehrlich verschiedene LLMs über fremden Code schreiben.

**Status:** lokal, nicht veröffentlicht. Rohdaten mit privaten Repo-Namen liegen lokal im per `.gitignore` ignorierten Bereich data/private/ (nie in der Historie).

Entstanden in der Nacht 22./23.09.2026 aus einer einzigen Session: Samuel hat entschieden, Claude hat orchestriert, der hai-agent und andere Modelle haben geschrieben.

## Schnellstart: zuerst lesen

1. `FOR_SMLFLG.md` erklärt Herkunft, Entscheidungen und Lessons Learned.
2. `ANALYSE.md` enthält die Benchmark-Ergebnisse und Vorbehalte.
3. `skill/SKILL.md` und `scripts/polish-section.md` zeigen den genutzten Repository-Polish-Pass.
4. Reproduzierbare Auswertung: `python3 scripts/analyse.py`; Pfadtreue einzelner README-Dateien: `python3 scripts/grounding.py <liste>`.

## Zwei Teile

1. **Pipeline:** lokale Git-Repos inventarisieren → Secret-Scan über die ganze Historie → als private GitHub-Repos anlegen → Lizenz + Topics → README-Polish durch einen Agenten → deterministische Abnahme → Commit/Push.
2. **Benchmark:** *same task, same harness, different model*. Derselbe README-Auftrag, dieselben Repos, verschiedene Modelle. Gemessen wird maschinell, nicht per Bauchgefühl.

## Benchmark in Kürze

`ANALYSE.md` wertet 5 Repos aus. GPT-5.5 (Hermes) lieferte 5/5 READMEs mit 92 % Treue und 2.8 Dichte in 123 s; ling-3.0-flash-fin-free (OpenCode) lag mit 5/5, 90 % Treue und 2.7 Dichte in 25 s knapp dahinter. Die wichtigste Lehre: Erfolgsmeldungen zählen nicht, wenn die README unverändert bleibt; `scripts/grounding.py` prüft Pfade deterministisch.

## Struktur

| Bereich | Pfade | Zweck |
|---|---|---|
| Kontext | `README.md`, `FOR_SMLFLG.md`, `ANALYSE.md` | Einstieg, Herkunft, Benchmark und Vorbehalte |
| Veröffentlichung | `scripts/publish.sh`, `scripts/run-publish.sh`, `scripts/push-all.sh` | Private GitHub-Repos anlegen, pushen und Remote-HEAD gegen lokal prüfen |
| README-Polish | `scripts/polish-one.sh`, `scripts/repair-one.sh`, `scripts/h2h-one.sh`, `scripts/oc-one.sh`, `scripts/polish-section.md` | Agentenläufe starten, Scope begrenzen, Repair- und Head-to-head-Läufe vergleichen |
| Deterministische Checks | `scripts/grounding.py`, `scripts/eval-readme.py`, `scripts/eval3.py`, `scripts/analyse.py` | Pfadtreue, Abdeckung und aggregierte Modellmetriken berechnen |
| Skill-Vertrag | `skill/SKILL.md` | Publish-/Polish-Skill des hai-agent mit Lizenz-, Topics-, gitleaks-, Worktree- und Default-Branch-Regeln |
| Private Daten | `.gitignore` | Rohlogs, Queues und Leak-Reports unter data/private/ bleiben ignoriert und nicht versioniert |

## Grenzen und Sicherheit

- Skripte enthalten hartkodierte lokale Pfade und sind vor einer Veröffentlichung zu entpersonalisieren.
- Sichtbarkeit ist eine Außenwirkungsentscheidung: Default war privat; öffentlich wird einzeln entschieden.
- data/private/ ist für private Repo-Namen und Rohdaten reserviert und bleibt per `.gitignore` außerhalb der Historie.
- Secret-Scan mit gitleaks ist notwendig, nicht hinreichend; keine README darf daraus eine Sicherheitsgarantie ableiten.
- Benchmark mit 5 Repos, GPT-begünstigter Auswahl und vermischtem Harness-/Modell-Effekt; siehe `ANALYSE.md`, Abschnitt Vorbehalte.
- Die Metrik prüft, ob genannte Pfade existieren, nicht ob ihre Beschreibung fachlich richtig ist.
- LLM-Ausgaben werden nicht als Abnahme betrachtet: deterministische Checks wie `scripts/grounding.py` haben Vorrang vor Agenten-Selbstmeldungen.
