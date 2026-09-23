# HAI-MCP

**HAI-MCP is a local-first MCP control plane for Human Agent Interface: it keeps agentic work bounded by explicit contracts, leases, owner gates, and evidence instead of relying on model memory.**

It is model-agnostic and intentionally narrow. MCP clients call tools; the server validates requests, writes confined local state, and returns structured JSON. The server itself never calls an LLM.

- Canonical website: https://www.human-agent-interface.com/
- About Samuel Fleig: https://www.human-agent-interface.com/samuel/
- Package: `hai-mcp` v0.1.0, Python 3.12+, MCP SDK `<2`

## Start here

First read these files in order:

| Step | File | Why |
| --- | --- | --- |
| 1 | `GOAL.md` | Current slice, scope, and active non-goals |
| 2 | `docs/TOOL_CONTRACT.md` | Tool list, mutation boundaries, gates, paths, and error codes |
| 3 | `docs/OWNER_GATE.md` | How owner-gated actions fail closed |
| 4 | `docs/BUILD_HANDOFF.md` | Verified state, unresolved findings, and handoff notes |

Then run the local server from the repository root:

```bash
uv sync --all-extras
uv run hai-mcp
```

By default the server speaks stdio MCP. Ready-made client examples are in `docs/client-snippets/README.md`, `docs/client-snippets/claude-code.mcp.json`, and `docs/client-snippets/cursor.mcp.json`.

For tests, use an isolated `HAI_HOME` rather than live owner state:

```bash
uv run pytest
```

## Repository structure

| Path | Purpose |
| --- | --- |
| `README.md` | Human-readable entry point |
| `GOAL.md` | Canonical current WIP slice |
| `FOR_SMLFLG.md` | Short owner-facing notes |
| `docs/TOOL_CONTRACT.md` | Public tool contract and gate matrix |
| `docs/OWNER_GATE.md` | Owner-gate mechanism and limits |
| `docs/BUILD_HANDOFF.md` | Build state and verification handoff |
| `docs/client-snippets/README.md` | Client configuration guide |
| `docs/visuals/hai-mcp-mission-lifecycle.svg` | Repository-owned lifecycle visual |
| `src/hai_mcp/server.py` | MCP tool registration and transport entry point |
| `src/hai_mcp/mission.py` | Mission contracts, leases, activity policy, and closure |
| `src/hai_mcp/state.py` | Control-plane operations and daily flow tools |
| `src/hai_mcp/owner_gate.py` | Nonce, presence, and legacy owner-gate modes |
| `tests/conftest.py` | Test isolation setup |
| `scripts/stdio_smoke.py` | Stdio smoke helper |

## Workflow and safety boundaries

HAI-MCP is a contract kernel, not an autonomous agent runtime. Its job is explicit scope, explicit leases, explicit gates, and explicit evidence.

It deliberately does **not** provide:

- LLM calls inside the server
- harness execution
- commit, push, deploy, stash, or delete tools
- Git subprocesses or repository mutation
- an OS sandbox or adversarial security layer
- a semantic verifier for whether a model really understood the goal
- cloud sync for `HAI_HOME`

Important operating boundaries:

- Owner gates stay fail-closed; the owner is a separate principal from the agent.
- HAI_HOME must not be synced through Dropbox, Syncthing, Git, or similar file mirroring because it contains local paths and lock-protected state.
- HAI_OWNER_HOME must not be inside HAI_HOME.
- Optional streamable HTTP is for trusted local multi-client access; non-loopback HTTP requires `HAI_HTTP_TOKEN` and is not adversarial owner authentication.
- Git hygiene is based on client telemetry; HAI-MCP never shells out to Git and never changes repository state.
- The skill log is inert: it records manual owner practice and does not enforce mission gates.

## Lineage and drift note

This repository replaces the Hermes-coupled prior control-plane role of ~/.config/hai-agent-mcp. Coexistence is fine until clients are deliberately switched. Keep repository changes separate from live ~/.hermes, live ~/.hai, and unrelated HAI apps.
