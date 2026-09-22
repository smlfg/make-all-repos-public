#!/bin/bash
# OpenCode-Arm: gleicher Polish-Auftrag, Skill wird als Datei gelesen. usage: oc-one.sh <repo> <model>
E="$HOME/Projekte/_h2h-eval-2026-09-23"; d="$1"; m="$2"; s=$(echo "${m#*/}" | tr -c 'a-z0-9.\n-' '_'); w="$E/$d-oc-$s"
[ -d "$w" ] || git clone -q --local "$HOME/Projekte/$d" "$w"; cd "$w" || exit 0
before=$(git status --porcelain | grep -v ' README.md$' | sort); t0=$(date +%s)
timeout 300 opencode run -m "$m" --format json "Arbeitsverzeichnis: $PWD (privates GitHub-Repo). Befolge diese Skill-Anleitung (Abschnitt Repository Polish Pass):
$(cat "$E/polish-section.md")

Auftrag: Lies die vorhandenen Dateien und schreibe bzw. überarbeite README.md so, dass es einen Satz zur Identität, einen Quickstart bzw. die ersten Dateien zum Lesen, eine kompakte Strukturtabelle und die Grenzen/Sicherheitshinweise enthält. Bestehende Aussagen zu Herkunft und Sicherheit bleiben erhalten. Keine Secrets, keine erfundenen Features. HARTE GRENZEN: kein git commit, kein git push, keine gh-Aufrufe, keine Änderungen außerhalb von README.md. Antworte zum Schluss mit genau einer Zeile: POLISH_DONE <Anzahl geänderter Zeilen> oder POLISH_FAIL <Grund>." > "$E/logs/$d-oc-$s.jsonl" 2>&1; rc=$?
dur=$(( $(date +%s)-t0 )); after=$(git status --porcelain | grep -v ' README.md$' | sort)
st=$(python3 - "$E/logs/$d-oc-$s.jsonl" <<'PY'
import json,sys,re
tools=0;tok={'input':0,'output':0,'reasoning':0,'cache':0};res='NO_RESULT'
for l in open(sys.argv[1],errors='ignore'):
  try: e=json.loads(l)
  except: continue
  p=e.get('part',{})
  if p.get('type')=='tool': tools+=1
  t=p.get('tokens')
  if isinstance(t,dict):
    for k in ('input','output','reasoning'): tok[k]+=t.get(k,0) or 0
    c=t.get('cache',{}); tok['cache']+=(c.get('read',0) if isinstance(c,dict) else 0) or 0
  if p.get('type')=='text':
    m=re.search(r'POLISH_(DONE|FAIL)[^\n]*',p.get('text','')); res=m.group(0) if m else res
print(f"{res}\ttools={tools}\tin={tok['input']}\tout={tok['output']}\treason={tok['reasoning']}\tcache={tok['cache']}")
PY
)
[ "$before" != "$after" ] && st="$st	SCOPE-VIOLATION"
echo -e "$d\t$m\trc=$rc\t${dur}s\t$st"
