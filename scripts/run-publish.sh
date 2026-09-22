#!/bin/bash
# Publiziert alle Repos aus queue.tsv als PRIVATE nach github.com/smlfg. Idempotent: Repos mit origin werden übersprungen.
P="$(dirname "$(readlink -f "$0")")"
while IFS=$'\t' read -r d n; do echo -e "$d\t$n\t$("$P/publish.sh" "$d" "$n" 2>&1 | tail -1)"; done < "$P/queue.tsv" | tee "$P/publish-$(date +%Y%m%d-%H%M).log"
