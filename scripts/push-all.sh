#!/bin/bash
# Pusht lokale Commits (LICENSE, README) aller publizierten Repos und prüft Remote == lokal.
P="$(dirname "$(readlink -f "$0")")"
cut -f1 "$P/lt-repos.tsv" | while read -r d; do
  cd "$HOME/Projekte/$d" || continue; b=$(git branch --show-current)
  [ "$(git rev-list --count "origin/$b..HEAD" 2>/dev/null)" = 0 ] && { echo -e "$d\tUP-TO-DATE"; continue; }
  timeout 120 git push -q origin "$b" 2>&1 | tail -1
  [ "$(git rev-parse HEAD)" = "$(git ls-remote origin "refs/heads/$b" | cut -f1)" ] && echo -e "$d\tOK" || echo -e "$d\tMISMATCH"
done | tee "$P/push-all-$(date +%Y%m%d-%H%M).log"
