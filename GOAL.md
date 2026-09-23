# GOAL — make-all-repos-public (Anker, beschlossen 2026-09-23)

Jeder weitere Schritt wird gegen diese Datei geprüft. Was hier nicht steht, gehört nicht in diese Lane.

## Ziel
`make-all-repos-public` wird ein sauberes, öffentliches Repo, mit dem andere ihre vergessenen lokalen
Projekte **sicher** auf GitHub bringen. Der README-Benchmark ist kein eigenes Projekt, sondern der
**Beleg**: so wurde gemessen, welches Modell und welcher Trick gute READMEs liefert.

## Nicht-Ziele
- keine weiteren Benchmark-Runden nach dem laufenden (hai-mcp + Sidecar-ng, 9 Modelle, 1 Harness)
- kein Dashboard, kein Eval-Framework, keine Multi-Harness-Infrastruktur
- keine neue Archify-Karte, keine Vision-Prüfung der Mermaid-Diagramme
- kein Workspace-Übersichts-Test

## Grenzen
- Nichts Privates wird öffentlich: keine privaten Repo-Namen, keine `/home/<user>`-Pfade,
  keine README-Texte privater Repos. Aus Sidecar-ng nur aggregierte Zahlen.
- gitleaks vor Veröffentlichung.
- Den Schalter auf öffentlich legt Samuel um.

## Definition of Done
1. README für Fremde: ein Satz was es tut → Quickstart in wenigen Befehlen → Sicherheits-Tore
   (gitleaks, privat zuerst, Scope-Guard) → eine Ergebnistabelle.
2. Drei Befunde, verständlich aufbereitet:
   - Datei-Manifest im Prompt hebt Pfad-Treue 61 % → 100 % (gleiches Modell, gleiche Repos).
   - Blindurteil und Messung sehen verschiedene Dinge — man braucht beides.
   - Die Harness verzerrt Modellvergleiche — deshalb der Benchmark in einer Harness.
3. Skripte ohne hartcodierte Pfade, `SKILL.md`, `manifest.sh`.
4. Öffentlich auf GitHub nach Samuels Freigabe → Lane **DONE**.

## Ablauf
Benchmark fertig → Samuels Blindurteil (hai-mcp, Sidecar-ng) → Ergebnisse ins Repo →
Samuels Abnahme → öffentlich → DONE.
