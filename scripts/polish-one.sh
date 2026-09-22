#!/bin/bash
# Eine hai-agent-Session pro Repo; nur README.md, kein commit/push.
d="$1"; cd "$HOME/Projekte/$d" || exit 0
[ -n "$(git status --porcelain -- README.md)" ] && { echo -e "$d\tSKIP readme-dirty"; exit 0; }
before=$(git status --porcelain | grep -v ' README.md$' | sort)
r=$(timeout 600 hermes -p hai-agent chat --oneshot -Q ${HAI_MODEL_ARGS} -q "Arbeitsverzeichnis: $PWD (privates GitHub-Repo). Nutze deinen Skill local-project-github-publication, Abschnitt 'Repository Polish Pass': Lies die vorhandenen Dateien und schreibe bzw. überarbeite README.md so, dass es einen Satz zur Identität, einen Quickstart bzw. die ersten Dateien zum Lesen, eine kompakte Strukturtabelle und die Grenzen/Sicherheitshinweise enthält. Bestehende Aussagen zu Herkunft und Sicherheit bleiben erhalten. Keine Secrets, keine erfundenen Features. HARTE GRENZEN: kein git commit, kein git push, keine gh-Aufrufe, keine Änderungen außerhalb von README.md. Antworte zum Schluss mit genau einer Zeile: POLISH_DONE <Anzahl geänderter Zeilen> oder POLISH_FAIL <Grund>." 2>&1 | grep -oE 'POLISH_(DONE|FAIL).*' | tail -1)
after=$(git status --porcelain | grep -v ' README.md$' | sort)
[ "$before" != "$after" ] && extra="SCOPE-VIOLATION: $(comm -13 <(echo "$before") <(echo "$after") | tr '\n' ' ')"
echo -e "$d\t${r:-NO_RESULT}\t$extra"
