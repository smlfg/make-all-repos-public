# FOR_SMLFLG — make-all-repos-public

Entstanden in der Nacht 22./23.09.2026 aus einer einzigen Session. Samuel hat entschieden, Claude hat orchestriert, der hai-agent und andere Modelle haben geschrieben.

## Entscheidungen

- **Privat statt öffentlich.** Sichtbarkeit ist eine Entscheidung über Außenwirkung und liegt bei Samuel. Privat + "Private contributions" im Profil zählt im Graph, ohne etwas preiszugeben. Öffentlich wird einzeln.
- **MIT als Default**, CC-BY-4.0 für reine Doku. Nicht bei Fremdcode, Team- oder Hochschulprojekten.
- **Topics nur aus Belegen** (Sprache, Manifeste, eigene Beschreibung). Keine erfundenen.
- **Merge statt Rebase** beim öffentlichen Profil-Repo: nichts umschreiben, Sicherungs-Branch vorher.
- **`data/private/` von Anfang an ignoriert**, damit private Repo-Namen nie in die Historie geraten.

## Lessons Learned

1. **Ein LLM, das ein LLM prüft, ist keine Abnahme.** deepseek hat beim Reparieren 43 neue Pfade erfunden. Verlässlich war nur `grounding.py`, weil es deterministisch nachschaut.
2. **Halluzination = zu wenig Hinschauen.** Tool-Calls pro README korrelieren mit Pfad-Treue stärker als der Modellname.
3. **Config gilt nicht automatisch für die Fallback-Kette.** `reasoning_effort: xhigh` kam bei MiniMax nicht an (0 Reasoning-Tokens im Head-to-head). Immer in `state.db` prüfen, wer wirklich geantwortet hat.
4. **Stille Fallbacks verfälschen Benchmarks.** Der deepseek-Lauf war zeitweise MiniMax (401 → Fallback). Pro Session das tatsächliche Modell verifizieren.
5. **Metriken lassen sich austricksen:** durch Streichen oder durch Vagheit (86 Zeilen, 0 Pfade). Deshalb drei Achsen: Treue, Dichte, Abdeckung.
6. **Selection Bias ist leicht gebaut.** Repos danach auszuwählen, dass GPT dort gut war, bevorzugt GPT. Auswahl vorher und unabhängig festlegen.
8. **Nie ein Skript editieren, das gerade läuft.** Bash liest Skripte stückweise während der Ausführung; ein Umschreiben mittendrin zerbricht den laufenden Aufruf (`Dateiende beim Suchen nach »"«`). Fix: neue Version unter neuem Namen anlegen und per `mv` atomar ersetzen, oder warten. Hier gerettet, weil das JSON-Rohlog vollständig war: Rohdaten zuerst schreiben, Statistik danach ableiten.
9. **"Fertig" gemeldet ist nicht geliefert.** 5 von 45 Läufen haben die README nie verändert, einer meldete `POLISH_DONE 0`. Eine Metrik, die das Ergebnis misst statt die Lieferung zu prüfen, bewertet dann das Original. Immer zuerst prüfen: Hat sich überhaupt etwas geändert?
10. **Werkzeug-Versionen driften unter Skripten weg.** OpenCode v2 kennt `--dir` nicht mehr; `archify-swarm/fanout.sh` nutzt es noch. Die Probe hat es gefangen, weil sie nur Exit 0 *plus* echten Text zählt.
7. **Harness-Grenzen sind unsichtbar, bis sie greifen.** Hermes-Schreib-Sandbox (`HERMES_WRITE_SAFE_ROOT`), OpenCode hängt still bei Dateien außerhalb des Projekts. Beides ist Sicherheit, kein Fehler.

## Offen / Nächste Schritte

- Benchmark vollständig laufen lassen (6 Free-Modelle), `ANALYSE.md` final.
- MiniMax in OpenCode-Harness messen: schwaches Modell oder schwache Anbindung?
- Gestreute Repo-Auswahl (Web, Doku, Python-Tool, groß) für eine belastbare Aussage.
- Abdeckungs-Metrik bauen (wichtige Dateien im Repo, die die README erwähnt).
- Öffentliche Version gemeinsam designen: Daten anonymisieren, Skripte entpersonalisieren, auf `skilleval` aufbauen.
