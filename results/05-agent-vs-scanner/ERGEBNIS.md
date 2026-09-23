# Agent als Prüfer vs. deterministischer Scanner

**Aufbau:** 21 lokale Repos ohne GitHub-Remote. Ein LLM-Agent (Hermes hai-agent, deepseek-v4.1-flash) prüft jedes
Repo auf Secrets, `.env`, private Daten und ergänzt `.gitignore`; Urteil PUBLISH/HOLD. Unabhängig davon läuft
`gitleaks` über die gesamte History. Veröffentlicht wird nur, was **beide** freigeben.

| Repo | Agent | gitleaks-Funde | Abnahme | |
|---|---|---|---|---|
| repo-01 | PUBLISH | 1 | HOLD | **Agent übersieht Funde** |
| repo-02 | PUBLISH | 0 | PUBLISH |  |
| repo-03 | PUBLISH | 1 | HOLD | **Agent übersieht Funde** |
| repo-04 | PUBLISH | 1242 | HOLD | **Agent übersieht Funde** |
| repo-05 | PUBLISH | 76 | HOLD | **Agent übersieht Funde** |
| repo-06 | HOLD | 1 | HOLD |  |
| repo-07 | HOLD | 28 | HOLD |  |
| repo-08 | PUBLISH | 2 | HOLD | **Agent übersieht Funde** |
| repo-09 | HOLD | 4 | HOLD |  |
| repo-10 | HOLD | 1 | HOLD |  |
| repo-11 | PUBLISH | 1 | HOLD | **Agent übersieht Funde** |
| repo-12 | HOLD | 2 | HOLD |  |
| repo-13 | HOLD | 15 | HOLD |  |
| repo-14 | PUBLISH | 19 | HOLD | **Agent übersieht Funde** |
| repo-15 | PUBLISH | 1 | HOLD | **Agent übersieht Funde** |
| repo-16 | PUBLISH | 28 | HOLD | **Agent übersieht Funde** |
| repo-17 | HOLD | 1 | HOLD |  |
| repo-18 | HOLD | 2 | HOLD |  |
| repo-19 | PUBLISH | 0 | PUBLISH |  |
| repo-20 | PUBLISH | 0 | PUBLISH |  |
| repo-21 | PUBLISH | 0 | PUBLISH |  |

**Befund:** Bei **9 Repos** empfahl der Agent PUBLISH, obwohl gitleaks Funde hatte — darunter ein Repo mit
19 echten Sourcegraph-Access-Tokens und eines mit über 1.000 Funden. Ein Agent als Prüfer ersetzt keinen
deterministischen Scanner. Er ist gut für Urteile (Was gehört in `.gitignore`? Ist das ein eigenes Projekt?),
nicht für die Garantie "keine Secrets".

Viele Scanner-Funde sind öffentliche Client-Schlüssel in gespeicherten Webseiten (`*_files/*.js`) — trotzdem HOLD,
die Entscheidung trifft der Mensch. Repo-Namen anonymisiert.
