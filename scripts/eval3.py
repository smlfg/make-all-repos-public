import os,re,sqlite3,statistics as st
H=os.path.expanduser('~/Projekte'); P=os.path.expanduser('~/ProjekteSnapshots/gh-publish-2026-09-22')
def ground(t,d):
  refs=set(x.strip('/') for x in re.findall(r'`([^`\s]+)`',t) if ('/' in x or re.search(r'\.[a-z]{1,5}$',x)) and not x.startswith(('http','-','$','~','/','.env')) and '*' not in x and '…' not in x and len(x)<120)
  ok=sum(os.path.exists(os.path.join(H,d,r.split(':')[0])) for r in refs); return ok,len(refs)
db=sqlite3.connect(os.path.expanduser('~/.hermes/profiles/hai-agent/state.db'))
q="select cwd,model,tool_call_count,reasoning_tokens,input_tokens,cache_read_tokens,output_tokens,ended_at-started_at from sessions where started_at>strftime('%s','2026-09-22 21:00') and input_tokens>10000 and cwd like ? order by started_at"
first={}; later={}
for r in db.execute(q,(H+'/%',)):
  d=os.path.basename(r[0]); (later if d in first else first).setdefault(d,r)
done=[l.split('\t')[0] for l in open(P+'/repair.log') if 'REPAIR_DONE' in l]
print("## A) Aufgabe 'README schreiben' (polish), gleiche Harness")
agg={}
for d,r in first.items(): agg.setdefault(r[1],[]).append(r)
for m,v in agg.items(): print(f"  {m:20} n={len(v):2}  tools={st.mean(x[2] or 0 for x in v):5.1f}  reason={st.mean(x[3] or 0 for x in v):5.0f}  out={st.mean(x[6] for x in v)/1000:4.1f}k  min={st.mean((x[7] or 0) for x in v)/60:4.1f}")
print("\n## B) deepseek repariert fremde READMEs (Pfad-Treue vorher -> nachher)")
tb=ta=nb=na=0
for d in done:
  pre=open(f"{P}/pre-repair/{d}.md",errors='ignore').read(); post=open(f"{H}/{d}/README.md",errors='ignore').read()
  a,b=ground(pre,d); c,e=ground(post,d); tb+=a; nb+=b; ta+=c; na+=e
  print(f"  {d:28} Autor={first[d][1]:12} {a}/{b} ({100*a/max(b,1):3.0f}%) -> {c}/{e} ({100*c/max(e,1):3.0f}%)")
print(f"  GESAMT {100*tb/max(nb,1):.0f}% -> {100*ta/max(na,1):.0f}%")
rs=[later[d] for d in done if d in later]
if rs: print(f"  deepseek repair: tools={st.mean(x[2] or 0 for x in rs):.1f} reason={st.mean(x[3] or 0 for x in rs):.0f} min={st.mean((x[7] or 0) for x in rs)/60:.1f}")
