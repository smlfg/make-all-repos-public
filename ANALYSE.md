# Analyse: same task, same harness, different model

Stand 23.09.2026. Auftrag an jedes Modell: *"Schreibe/überarbeite README.md nach dem Skill-Abschnitt 'Repository Polish Pass'."* Gleiche 5 Repos, gleicher Ausgangsstand, gleicher Prompt. Gemessen wird maschinell mit `scripts/analyse.py`.

## Ergebnis

| Arm | geliefert | Treue | Dichte | Abschnitte | Zeilen | Tool-Calls | Dauer |
|---|---|---|---|---|---|---|---|
| gpt-5.5 (hermes) | 5/5 | 92 % | 2.8 | 4.0/4 | 43 | 27 | 123 s |
| nemotron-3-ultra-free (opencode) | 5/5 | 91 % | 2.5 | 4.0/4 | 48 | 12 | 81 s |
| deepseek-v4.1-flash (hermes) | 5/5 | 90 % | 2.5 | 4.0/4 | 60 | 30 | 108 s |
| ling-3.0-flash-fin-free (opencode) | 5/5 | 90 % | 2.7 | 4.0/4 | 48 | 14 | 25 s |
| muse-spark-1.2-contributor-free (opencode) | 4/5 | 90 % | 2.8 | 4.0/4 | 57 | 17 | 66 s |
| nemotron-3.5-lightning-free (opencode) | 2/5 | 89 % | 2.1 | 4.0/4 | 38 | 8 | 292 s |
| muse-spark-1.3-contributor-free (opencode) | 4/5 | 86 % | 2.1 | 4.0/4 | 51 | 15 | 52 s |
| mimo-v2.6-flash-free (opencode) | 5/5 | 83 % | 2.3 | 4.0/4 | 58 | 14 | 88 s |
| MiniMax-M3 (hermes) | 5/5 | 80 % | 1.2 | 3.8/4 | 83 | 17 | 39 s |

**Achsen**
- **geliefert:** README tatsächlich verändert. Unveränderte READMEs zählen nicht in die Treue, sonst misst man das Original.
- **Treue:** Anteil der in Backticks genannten Pfade, die im Repo existieren (Globs, absolute Pfade, `.env` ausgenommen).
- **Dichte:** echte, überprüfbare Pfade pro 10 Zeilen. Bestraft Vagheit, die die Treue nicht sieht.
- **Abschnitte:** Identität, Quickstart, Strukturtabelle, Grenzen (je 1 Punkt).

## Befunde

1. **Ein kostenloses Modell kommt bis auf 2 Punkte an GPT heran, fünfmal schneller.** ling-3.0 liefert 90 % Treue bei 2.7 Dichte in 25 s; GPT-5.5 92 % / 2.8 in 123 s.
2. **Halluzination ist fehlendes Hinschauen.** MiniMax schreibt die längsten READMEs (83 Zeilen) mit der geringsten Dichte (1.2) und nutzt trotz `reasoning_effort: xhigh` im Head-to-head 0 Reasoning-Tokens: Die Einstellung kommt bei diesem Provider nicht an.
3. **Modelle melden Erfolg ohne Lieferung.** nemotron-3.5-lightning hat 3 von 5 READMEs nicht angefasst; muse-spark-1.3 meldete `POLISH_DONE 0`. Ohne Liefer-Check stand nemotron-3.5 mit 92 % gleichauf mit GPT.
4. **Der Reparateur halluziniert selbst.** Im Produktivlauf hob ein deepseek-Repair-Durchgang die Treue von 61 % auf 82 %, strich 147 erfundene Pfade, ergänzte 105 echte, erfand aber 43 neue. Ein LLM prüft ein LLM nicht; `grounding.py` schon.
5. **Stille Fallbacks verfälschen Benchmarks.** Ein als deepseek gestarteter Lauf war nach einem 401 still MiniMax. Jede Hermes-Session wird deshalb gegen `state.db` auf das tatsächliche Modell geprüft.

## Vorbehalte

- **Konfundierung Harness × Modell.** GPT/deepseek/MiniMax liefen in Hermes (Skill geladen), Free-Modelle in OpenCode (Skill-Abschnitt inline im Prompt). Harness-Effekt und Modell-Effekt sind nicht getrennt. Kontrolle offen: dasselbe Modell in beiden Harnesses.
- **Selection Bias.** Die 5 Repos wurden danach ausgewählt, dass GPT dort ≥ 80 % hatte; alphabetisch die ersten, vier davon "Agent*". Begünstigt GPT und einfache Repos.
- **n = 5.** Hinweis, kein Urteil.
- **Metrik prüft Existenz, nicht Bedeutung.** Ob die Beschreibung stimmt, misst sie nicht. Dafür: menschliches Urteil (Blindtest) oder Judge.

## Reproduzieren

```bash
python3 scripts/analyse.py          # Tabelle aus Rohdaten
python3 scripts/grounding.py <liste> # Treue pro Repo
```
Rohdaten (private Repo-Namen) liegen in `data/private/` und sind nicht versioniert.
