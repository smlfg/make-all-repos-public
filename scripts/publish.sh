#!/bin/bash
# usage: publish.sh <localdir> <reponame>
d="$1"; n="$2"; cd "$HOME/Projekte/$d" || exit 1
git remote get-url origin >/dev/null 2>&1 && { echo "SKIP has-origin"; exit 0; }
timeout 30 gh repo create "smlfg/$n" --private --description "Local project $d (published $(date +%F))" >/dev/null || { echo "FAIL create"; exit 1; }
git remote add origin "https://github.com/smlfg/$n.git"
timeout 300 git push -u origin --all -q 2>&1 | tail -2 || { echo "FAIL push"; exit 1; }
timeout 60 git push origin --tags -q 2>/dev/null
loc=$(git rev-parse HEAD 2>/dev/null); rem=$(git ls-remote origin HEAD "refs/heads/$(git branch --show-current)" | head -1 | cut -f1)
vis=$(gh repo view "smlfg/$n" --json visibility -q .visibility)
[ "$loc" = "$rem" ] && echo "OK $vis $loc" || echo "MISMATCH loc=$loc rem=$rem"
