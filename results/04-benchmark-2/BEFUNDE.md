# Befunde Benchmark hai-mcp + Sidecar-ng (23.09.2026)

- **MiniMax-M3 ausgeschlossen:** `minimax-coding-plan` in OpenCode antwortet mit 401 "invalid api key" (Token-Plan-Key ungültig/abgelaufen). Kein Modellbefund, sondern Zugangsbefund. Samuel: draußen lassen (23.09.). Im ersten Blindtest (über Hermes, Provider `minimax`) lief MiniMax und landete in der Spitzengruppe.
- **Runner-Bug:** `opencode run` liest stdin und verschluckte die Modell-Liste der `while read`-Schleife → nur 1 Modell pro Repo lief. Fix: `< /dev/null`.
