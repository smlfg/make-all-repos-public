# Brief: README-Bench — a research benchmark website with a swipe gallery

Build `site/index.html`: a cutting-edge research benchmark website in the style of SWE-bench / LMArena pages,
with a **swipeable gallery** where visitors flip through the model-written READMEs — blind first, reveal after.
Language: English. Everything under `site/` only.

## The story (one sentence)
With a file manifest in the prompt and a deterministic path checker, a **free model** wrote the best READMEs —
and blind human judgment and automatic metrics disagree often enough that you need both.

## Data — the ONLY sources. Never invent a number.
- `site/data/results.json` — every entry: benchmark, letter, model, blind verdict (`verdict`, `verdict_score` 0–3,
  `verdict_note` in German → translate faithfully), `fidelity`, `real_paths`, `tool_calls`, `seconds`, `lines`,
  `readme` (path to the Markdown text, only where `readme_texts_public` is true).
- `site/data/readmes/hai-mcp/README_A–H.md`, `site/data/readmes/blindtest-1/README_A–I.md` — gallery texts.
- `results/03-manifest-minitest/ERGEBNIS.md` — manifest effect: fidelity 61 % → 100 %, invented paths 28 → 0.
- `results/05-agent-vs-scanner/ERGEBNIS.md` — LLM reviewer recommended publishing 9 repos with secret-scanner hits.
- `results/01-kopf-an-kopf/ANALYSE.md`, `results/04-benchmark-2/AUSWERTUNG.md` — context and findings.
- `docs/assets/*-light.svg / *-dark.svg` — existing charts, may be embedded.
- FORBIDDEN: anything under `data/` at the repo root (private). Sidecar-ng README texts are private: show its
  numbers and verdicts, never its text.

## Sections
1. **Hero** — name "README-Bench", the one-sentence story, 3 stat tiles: 61 % → 100 % path fidelity ·
   28 → 0 invented paths · winner: muse-spark-1.2 (free). Date 2026-09-23, "1 harness, 8 models, 2 repos, blind".
2. **Leaderboard** — table across benchmark 2 (hai-mcp + Sidecar-ng): model, verdict per repo, fidelity per repo,
   tool calls, time, cost class (free / subscription). Sortable columns. MiniMax row greyed with "excluded (401)".
3. **Swipe gallery (the centerpiece)** — tabs: hai-mcp · blind test 1. One card per README, rendered Markdown
   (client-side renderer is fine; Mermaid blocks rendered). Navigation: swipe on touch, arrow keys, prev/next buttons,
   dots. **Blind mode on by default**: card shows only the letter; visitor picks a verdict (weak / okay / good / top);
   then "Reveal" shows model, the author's blind verdict, fidelity, tool calls, lines. A small tally compares the
   visitor's verdicts with the author's. Toggle to switch blind mode off. Visitor verdicts stay in the browser
   (localStorage, wrapped in try/catch; page must work without it).
4. **Results charts** — for each repo a labeled scatter: x = path fidelity (%), y = blind verdict tier, every point
   labeled with the model name, title = finding as a sentence. Inline SVG, light + dark.
5. **Methodology** — task, same skill section + same manifest for all, one harness (OpenCode), blind letters,
   fidelity metric definition, path checker. A small pipeline diagram (inline SVG).
6. **Findings** — 4 cards: manifest beats model choice · blind verdict ≠ metric · harness skews comparisons
   (first test mixed harnesses and favored paid models; single-harness test did not) · an LLM reviewer is not a
   secret scanner.
7. **Recommended pipeline** — muse-spark writes → checker → deepseek only on checker failure or outage.
8. **Limitations** — n = 2 repos, 1 judge; MiniMax excluded; checker has no notion of placeholders/runtime files
   (hai-mcp original README scores 74 %); verdict of one letter inferred from order (marked in data).
9. **Reproduce & cite** — links to `results/`, scripts, a BibTeX block for "README-Bench (2026)".

## Design
- One self-contained `index.html` (CSS/JS inline). Allowed external: a Markdown renderer and Mermaid from
  cdn.jsdelivr.net/npm only. No web fonts, no build step. Loads `data/results.json` and README files via fetch
  (serve with `python3 -m http.server` from `site/`; show a friendly hint if opened via file://).
- Color tokens on `:root`, dark mode via `@media (prefers-color-scheme: dark)`, explicit `body` background.
  Light: surface #fcfcfb, text #0b0b0b, secondary #52514e, rule #e8e7e3, accent-1 #2a78d6, accent-2 #eb6834.
  Dark: surface #1a1a19, text #ffffff, secondary #c3c2b7, rule #383835, accent-1 #3987e5, accent-2 #d95926.
- Research-paper calm: generous whitespace, tabular numbers, thin rules, no gradients-everywhere, no emoji decor.
- Works at phone width (16 px gutter, no horizontal page scroll; tables may scroll inside their box).
- Text never colored with an accent; charts with direct labels and recessive axes.

## Hard limits
- Create/modify files under `site/` only. No git commit, no git push, no gh calls.
- End with exactly one line: `SITE_DONE <sections>` or `SITE_FAIL <reason>`.
