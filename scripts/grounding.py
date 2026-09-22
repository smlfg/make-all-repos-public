# Gibt pro Repo die README-Pfade aus, die im Repo nicht existieren: repo<TAB>treue%<TAB>pfad1,pfad2
import os,re,sys
H=os.path.expanduser('~/Projekte')
for d in (l.strip() for l in open(sys.argv[1]) if l.strip()):
  f=os.path.join(H,d,'README.md')
  if not os.path.exists(f): continue
  t=open(f,errors='ignore').read()
  refs=set(x.strip('/') for x in re.findall(r'`([^`\s]+)`',t) if ('/' in x or re.search(r'\.[a-z]{1,5}$',x)) and not x.startswith(('http','-','$','~','/','.env')) and '*' not in x and '…' not in x and len(x)<120)
  miss=sorted(r for r in refs if not os.path.exists(os.path.join(H,d,r.split(':')[0])))
  tr=100*(len(refs)-len(miss))/len(refs) if refs else 100
  print(f"{d}\t{tr:.0f}\t{','.join(miss)}")
