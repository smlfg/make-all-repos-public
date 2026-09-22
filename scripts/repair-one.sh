#!/bin/bash
# Grounding-Nachbesserung: nur README.md, kein commit/push.
IFS=$'\t' read -r d tr miss <<< "$1"; cd "$HOME/Projekte/$d" || exit 0
before=$(git status --porcelain | grep -v ' README.md$' | sort)
r=$(timeout 600 hermes -p hai-agent chat --oneshot -Q ${HAI_MODEL_ARGS} -q "Arbeitsverzeichnis: $PWD. Die README.md in diesem Repo nennt Pfade, die hier NICHT existieren: ${miss//,/, }. Prüfe jeden davon gegen das echte Repo (ls, git ls-files, grep im Code). Pro Pfad: ersetze ihn durch den tatsächlich existierenden Pfad, ODER kennzeichne ihn als 'wird zur Laufzeit erzeugt', wenn der Code ihn nachweislich anlegt, ODER entferne die Aussage. Erfinde nichts Neues. Entferne außerdem generische Abschnitte, die für ein privates Einzelprojekt nicht zutreffen (z.B. 'Mitwirken/Contributing'). HARTE GRENZEN: nur README.md ändern, kein git commit, kein git push, keine gh-Aufrufe. Antworte zum Schluss mit genau einer Zeile: REPAIR_DONE <Anzahl korrigierter Pfade> oder REPAIR_FAIL <Grund>." 2>&1 | grep -oE 'REPAIR_(DONE|FAIL).*' | tail -1)
after=$(git status --porcelain | grep -v ' README.md$' | sort)
[ "$before" != "$after" ] && extra="SCOPE-VIOLATION: $(comm -13 <(echo "$before") <(echo "$after") | tr '\n' ' ')"
echo -e "$d\t${r:-NO_RESULT}\t$extra"
