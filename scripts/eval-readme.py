import os,re,sqlite3,collections,statistics as st,sys
H=os.path.expanduser('~/Projekte')
db=sqlite3.connect(os.path.expanduser('~/.hermes/profiles/hai-agent/state.db'))
rows=db.execute("select cwd,model,input_tokens,cache_read_tokens,output_tokens,ended_at-started_at from sessions where started_at>strftime('%s','2026-09-22 21:00') and input_tokens>5000 and cwd like ?",(H+'/%',)).fetchall()
last={}
for cwd,m,i,c,o,dur in rows: last[os.path.basename(cwd)]=(m,i,c,o,dur)
res=collections.defaultdict(list)
for d,(m,i,c,o,dur) in last.items():
  f=os.path.join(H,d,'README.md')
  if not os.path.exists(f): continue
  t=open(f,errors='ignore').read()
  L=t.lower()
  sec=dict(ident=bool(re.search(r'^#\s+\S.*\n+\s*[^#\s|]',t,re.M)),
           quick=bool(re.search(r'^#+.*(quickstart|schnellstart|start|erste schritte|getting started|first files|zuerst lesen)',L,re.M)),
           table=bool(re.search(r'^\|.*\|\s*\n\|\s*:?-{3}',t,re.M)),
           safety=bool(re.search(r'^#+.*(grenzen|sicherheit|safety|boundar|limits|security)',L,re.M)))
  refs=set(x.strip('/') for x in re.findall(r'`([^`\s]+)`',t) if ('/' in x or re.search(r'\.[a-z]{1,5}$',x)) and not x.startswith(('http','-','$','~','/','.env')) and '*' not in x and '…' not in x and len(x)<120)
  ok=sum(1 for r in refs if os.path.exists(os.path.join(H,d,r.split(':')[0])))
  res[m].append(dict(repo=d,sec=sum(sec.values()),refs=len(refs),ok=ok,lines=t.count('\n'),i=i,c=c,o=o,dur=dur))
print(f"{'modell':18}{'n':>3}{'Abschn./4':>10}{'Pfad-Treue':>11}{'halluz.Pfade':>13}{'Zeilen':>7}{'Input':>8}{'Cache':>8}{'Output':>7}{'Min':>5}")
for m,v in res.items():
  refs=sum(x['refs'] for x in v); ok=sum(x['ok'] for x in v)
  print(f"{m:18}{len(v):>3}{st.mean(x['sec'] for x in v):>10.2f}{(ok/refs*100 if refs else 0):>10.0f}%{refs-ok:>13}{st.median(x['lines'] for x in v):>7.0f}{st.mean(x['i'] for x in v)/1000:>7.0f}k{st.mean(x['c'] for x in v)/1000:>7.0f}k{st.mean(x['o'] for x in v)/1000:>6.1f}k{st.mean(x['dur'] or 0 for x in v)/60:>5.1f}")
if len(sys.argv)>1:
  for m,v in res.items():
    for x in sorted(v,key=lambda x:x['ok']-x['refs'])[:3]: print(m,x['repo'],f"{x['ok']}/{x['refs']} Pfade existieren, {x['sec']}/4 Abschnitte")
