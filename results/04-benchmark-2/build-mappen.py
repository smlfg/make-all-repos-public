#!/usr/bin/env python3
"""Blinde Mappen pro Repo: README_A.. als HTML (eigenes Hell/Dunkel-CSS, Mermaid gerendert),
MESSUNG.md (nur Buchstaben), AUFLOESUNG.md (Zuordnung). Buchstaben-Ordner sind Symlinks auf die
Einträge, damit relative Bilder funktionieren, ohne Modellnamen in der URL zu zeigen."""
import html
import os
import random
import re
import secrets
import subprocess

B = os.path.expanduser("~/Projekte/_bench-hai-sidecar-20260923")
LOG = {l.split("\t")[0]: l.rstrip("\n").split("\t") for l in open(f"{B}/bench.log")}

CSS = """:root{--bg:#fcfcfb;--fg:#0b0b0b;--muted:#52514e;--line:#d0d7de;--code:#f0efec;--link:#2a78d6}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a19;--fg:#f2f1ee;--muted:#c3c2b7;--line:#383835;--code:#262624;--link:#6da7ec}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 system-ui,sans-serif}
main{max-width:860px;margin:0 auto;padding:24px 16px 64px}a{color:var(--link)}
h1,h2,h3{line-height:1.25}h1{border-bottom:1px solid var(--line);padding-bottom:.3em}
table{border-collapse:collapse;display:block;overflow-x:auto}th,td{border:1px solid var(--line);padding:4px 10px;text-align:left}
code{background:var(--code);color:var(--fg);padding:.1em .3em;border-radius:4px;font-size:.92em}
pre{background:var(--code);color:var(--fg);padding:12px;border-radius:6px;overflow-x:auto}pre code{padding:0;background:none}
pre.mermaid{background:transparent;text-align:center}img{max-width:100%}blockquote{border-left:3px solid var(--line);margin:0;padding-left:12px;color:var(--muted)}
.badge{position:fixed;top:8px;right:12px;font:700 32px system-ui;color:var(--muted);opacity:.6}"""


def refs(t):
    return {x.strip("/") for x in re.findall(r"`([^`\s]+)`", t)
            if ("/" in x or re.search(r"\.[a-z]{1,5}$", x))
            and not x.startswith(("http", "-", "$", "~", "/", ".env"))
            and "*" not in x and "…" not in x and len(x) < 120}


def page(letter, body):
    return f"""<!doctype html><html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>README {letter}</title><base href="{letter}/"><style>{CSS}</style></head><body><div class="badge">{letter}</div><main>{body}</main>
<script type="module">import m from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";
m.initialize({{startOnLoad:false,theme:matchMedia("(prefers-color-scheme: dark)").matches?"dark":"default"}});
document.querySelectorAll("pre.mermaid code").forEach(c=>{{c.parentElement.textContent=c.textContent}});
await m.run({{querySelector:"pre.mermaid",suppressErrors:true}});</script></body></html>"""


for repo in ("hai-mcp", "sidecar-ng"):
    out = f"{B}/mappe-{repo}"
    os.makedirs(out, exist_ok=True)
    entries = sorted(e for e in os.listdir(f"{B}/entries")
                     if e.startswith(repo + "--") and "MiniMax" not in e)  # MiniMax: 401, draußen (Samuel 23.09.)
    seed = secrets.randbits(32)
    random.Random(seed).shuffle(entries)
    mess = [f"# Messung {repo} (blind, nur Buchstaben)\n", "| README | geliefert | Pfad-Treue | echte Pfade | Tool-Calls | Zeit | Zeilen |",
            "|---|---|---|---|---|---|---|"]
    aufl = [f"# Auflösung {repo} — erst NACH deinem Urteil öffnen\n", f"Zufalls-Seed: {seed}\n", "| README | Modell |", "|---|---|"]
    for i, e in enumerate(entries):
        L, w = "ABCDEFGHIJ"[i], f"{B}/entries/{e}"
        link = f"{out}/{L}"
        if not os.path.islink(link):
            os.symlink(w, link)
        changed = bool(subprocess.run(["git", "-C", w, "status", "--porcelain", "--", "README.md"],
                                      capture_output=True, text=True).stdout.strip())
        t = open(f"{w}/README.md", errors="ignore").read()
        body = subprocess.run(["pandoc", "-f", "gfm", "-t", "html5"], input=t, capture_output=True, text=True).stdout \
            if changed else "<p><em>(Dieser Teilnehmer hat die README nicht verändert.)</em></p>"
        body = re.sub(r'<pre class="mermaid"><code>', '<pre class="mermaid"><code>', body)
        open(f"{out}/README_{L}.html", "w").write(page(L, body))
        rs = refs(t)
        ok = sum(os.path.exists(os.path.join(w, x.split(":")[0])) for x in rs)
        lg = LOG.get(e, ["", "?", "?", "tools=?"])
        mess.append(f"| {L} | {'ja' if changed else 'NEIN'} | {100 * ok / len(rs) if rs else 100:.0f} % | {ok}/{len(rs)} | "
                    f"{lg[3].split('=')[1]} | {lg[1]} | {t.count(chr(10))} |")
        aufl.append(f"| {L} | {e.split('--', 1)[1].replace('_', '/', 1)} |")
    open(f"{out}/MESSUNG.md", "w").write("\n".join(mess) + "\n")
    open(f"{out}/AUFLOESUNG.md", "w").write("\n".join(aufl) + "\n")
    print(repo, len(entries), "Einträge ->", out)
