#!/bin/bash
# README-Benchmark: 9 Modelle x 2 Repos, EINE Harness (OpenCode), gleicher Auftrag, gleiches Manifest.
# Alle Läufe strikt nacheinander (nie 2 OpenCode parallel). Originale werden nie angefasst: rsync-Kopien.
# usage: run-bench.sh [model-filter] [repo-filter]    (Filter = grep-Muster, für Probeläufe)
B="$HOME/Projekte/_bench-hai-sidecar-20260923"
MANIFEST="$HOME/ProjekteSnapshots/gh-publish-2026-09-22/minitest-manifest/manifest.sh"
SECTION="$HOME/Projekte/_h2h-eval-2026-09-23/polish-section.md"
mkdir -p "$B/entries" "$B/logs" "$B/prompts"

REPOS="hai-mcp=$HOME/Projekte/hai-mcp-installed
sidecar-ng=$HOME/Projekte/Sidecar-Workspace/Sidecar-ng"
MODELS="openai/gpt-5.5
opencode-go/deepseek-v4.1-flash
minimax-coding-plan/MiniMax-M3
opencode/ling-3.0-flash-fin-free
opencode/mimo-v2.6-flash-free
opencode/muse-spark-1.2-contributor-free
opencode/muse-spark-1.3-contributor-free
opencode/nemotron-3-ultra-free
opencode/nemotron-3.5-lightning-free"

TASK="Überarbeite README.md so, dass sie einen Satz zur Identität, einen Quickstart bzw. die ersten Dateien zum Lesen, eine kompakte Strukturtabelle und die Grenzen/Sicherheitshinweise enthält. Bestehende Aussagen zu Herkunft und Sicherheit bleiben erhalten. Keine Secrets, keine erfundenen Features oder Zahlen. Jeder Pfad, den du in Backticks nennst, MUSS wörtlich in der Dateiliste unten stehen. HARTE GRENZEN: kein git commit, kein git push, keine gh-Aufrufe, keine Änderungen außerhalb von README.md. Antworte zum Schluss mit genau einer Zeile: POLISH_DONE <Anzahl geänderter Zeilen> oder POLISH_FAIL <Grund>."

run_one() { # $1=model $2=repo-name $3=src
  local model="$1" name="$2" src="$3" id; id="$name--${model//\//_}"
  grep -q "^$id	" "$B/bench.log" 2>/dev/null && return  # schon gelaufen
  local w="$B/entries/$id"; [ -d "$w" ] || rsync -a --exclude node_modules --exclude .venv "$src/" "$w/"
  local before; before=$(git -C "$w" status --porcelain -uall | grep -v ' README.md$' | sort)
  local p="$B/prompts/$id.txt"
  { echo "Arbeitsverzeichnis: $w."; echo; echo "Befolge diese Skill-Anleitung (Abschnitt Repository Polish Pass):"; cat "$SECTION"
    echo; echo "Vollständige Dateiliste dieses Repos (inkl. eingebetteter Repos). Ein Pfad, der hier nicht steht, existiert nicht:"
    echo "<repository_files>"; "$MANIFEST" "$w" 2000; echo "</repository_files>"; echo; echo "Auftrag: $TASK"; } > "$p"
  local t0; t0=$(date +%s)
  (cd "$w" && timeout 900 opencode run -m "$model" --format json "$(cat "$p")" < /dev/null > "$B/logs/$id.jsonl" 2>&1)  # stdin zu, sonst frisst opencode die Modell-Liste der Schleife
  local res; res=$(grep -oE 'POLISH_(DONE|FAIL)[^"\\]*' "$B/logs/$id.jsonl" | tail -1)
  local after; after=$(git -C "$w" status --porcelain -uall | grep -v ' README.md$' | sort)
  local scope=scope-ok; [ "$before" != "$after" ] && scope=SCOPE-VIOLATION
  local tools; tools=$(grep -c '"type":"tool_use"' "$B/logs/$id.jsonl")
  echo -e "$id\t$(( $(date +%s)-t0 ))s\t${res:-NO_RESULT}\ttools=$tools\t$scope" | tee -a "$B/bench.log"
}

echo "$REPOS" | grep -E "${2:-.}" | while IFS='=' read -r name src; do
  echo "$MODELS" | grep -E "${1:-.}" | while read -r model; do run_one "$model" "$name" "$src"; sleep 5; done
done
