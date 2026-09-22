#!/usr/bin/env python3
"""Head-to-head-Tabelle: gleicher Auftrag, gleiche Repos, verschiedene Modelle/Harnesses.

Achsen: Treue (genannte Pfade existieren), Dichte (echte Pfade pro 10 Zeilen),
Abschnitte (Identitaet/Quickstart/Tabelle/Grenzen), plus Aufwand (Tool-Calls, Dauer).
Gibt Markdown aus.
"""
import glob
import os
import re
import sqlite3
import statistics as st

H = os.path.expanduser("~/Projekte")
E = os.environ.get("H2H_DIR", H + "/_h2h-eval-2026-09-23")
DB = os.path.expanduser("~/.hermes/profiles/hai-agent/state.db")


def refs(t):
    return {
        x.strip("/")
        for x in re.findall(r"`([^`\s]+)`", t)
        if ("/" in x or re.search(r"\.[a-z]{1,5}$", x))
        and not x.startswith(("http", "-", "$", "~", "/", ".env"))
        and "*" not in x and "…" not in x and len(x) < 120
    }


def sections(t):
    low = t.lower()
    return sum([
        bool(re.search(r"^#\s+\S.*\n+\s*[^#\s|]", t, re.M)),
        bool(re.search(r"^#+.*(quickstart|schnellstart|start|erste|getting started|first files|zuerst)", low, re.M)),
        bool(re.search(r"^\|.*\|\s*\n\|\s*:?-{3}", t, re.M)),
        bool(re.search(r"^#+.*(grenzen|sicherheit|safety|boundar|limits|security)", low, re.M)),
    ])


def effort():
    """(arm, repo) -> (tools, sekunden) aus Hermes-DB und OpenCode-Log."""
    out = {}
    db = sqlite3.connect(DB)
    for cwd, tools, dur in db.execute(
        "select cwd, tool_call_count, ended_at-started_at from sessions where cwd like ?", (E + "/%",)
    ):
        name = os.path.basename(cwd)
        for arm in ("minimax", "deepseek"):
            if name.endswith("-" + arm):
                out[(arm, name[: -len(arm) - 1])] = (tools or 0, dur or 0)
    # GPT-Arm stammt aus dem Produktivlauf: erste gpt-5.5-Session im Original-Repo
    for cwd, tools, dur in db.execute(
        "select cwd, tool_call_count, ended_at-started_at from sessions "
        "where model='gpt-5.5' and cwd like ? order by started_at desc", (H + "/%",)
    ):
        out[("gpt-5.5 (hermes)", os.path.basename(cwd))] = (tools or 0, dur or 0)
    for log in (E + "/oc-bench.log", E + "/oc-bench-recovered.log"):
        if not os.path.exists(log):
            continue
        for line in open(log):
            f = line.rstrip("\n").split("\t")
            if len(f) < 6:
                continue
            m = re.search(r"tools=(\d+)", line)
            out[("oc:" + f[1].split("/")[-1], f[0])] = (int(m.group(1)) if m else 0, int(f[3].rstrip("s")))
    return out


def main():
    repos = [l.split()[0] for l in open(E + "/picked.txt")]
    eff = effort()
    rows = {}
    for r in repos:
        root = f"{H}/{r}"
        cand = {"gpt-5.5 (hermes)": E + f"/{r}.gpt.md",
                "minimax": E + f"/{r}-minimax/README.md",
                "deepseek": E + f"/{r}-deepseek/README.md"}
        for f in glob.glob(E + f"/{r}-oc-*/README.md"):
            cand["oc:" + f.split("-oc-")[1].split("/")[0]] = f
        for arm, f in cand.items():
            if not os.path.exists(f):
                continue
            t = open(f, errors="ignore").read()
            rs = refs(t)
            ok = sum(os.path.exists(os.path.join(root, x.split(":")[0])) for x in rs)
            tools, dur = eff.get((arm, r), (None, None))
            rows.setdefault(arm, []).append(dict(ok=ok, n=len(rs), lines=max(t.count("\n"), 1),
                                                 sec=sections(t), tools=tools, dur=dur))
    print("| Arm | n | Treue | Dichte | Abschnitte | Zeilen | Tool-Calls | Dauer |")
    print("|---|---|---|---|---|---|---|---|")
    def treue(v):
        return sum(x["ok"] for x in v) / max(sum(x["n"] for x in v), 1)
    for arm, v in sorted(rows.items(), key=lambda kv: -treue(kv[1])):
        tl = [x["tools"] for x in v if x["tools"] is not None]
        dl = [x["dur"] for x in v if x["dur"] is not None]
        print(f"| {arm} | {len(v)} | {100*treue(v):.0f} % "
              f"| {10*sum(x['ok'] for x in v)/sum(x['lines'] for x in v):.1f} "
              f"| {st.mean(x['sec'] for x in v):.1f}/4 | {st.mean(x['lines'] for x in v):.0f} "
              f"| {st.mean(tl):.0f} | {st.mean(dl):.0f} s |" if tl and dl else
              f"| {arm} | {len(v)} | {100*treue(v):.0f} % "
              f"| {10*sum(x['ok'] for x in v)/sum(x['lines'] for x in v):.1f} "
              f"| {st.mean(x['sec'] for x in v):.1f}/4 | {st.mean(x['lines'] for x in v):.0f} | – | – |")


if __name__ == "__main__":
    main()
