## Repository Polish Pass

Use this pass when Samuel asks to make the repo `huebsch`, presentable, visual, or easier to understand. Keep it small and owner-facing; do not change runtime behavior just to improve presentation.

1. Re-check branch/status before touching docs or assets.

   ```bash
   git branch --show-current
   git status --short --branch
   ```

   If `git status --porcelain -- README.md` is non-empty, Samuel has uncommitted README work: stop and report instead of editing.

2. Read the current README, manifest, docs index, and any repo-map/status file before editing. Every command, file path and feature you write into the README must exist in the repo; no invented quickstarts. Preserve existing lineage, safety, and secret statements rather than replacing them with generic marketing copy.

3. Create a root README flow that gives Samuel and GitHub readers an immediate path:
   - one-sentence identity,
   - quickstart or first files to read,
   - a compact top-level structure table,
   - explicit workflow/safety boundaries,
   - lineage/drift note when the repo was extracted from another workspace.

4. For visual polish, add repository-owned assets under `docs/assets/` and a gallery file such as `docs/DIAGRAMS.md`. Prefer SVG for GitHub/Markdown and generate PNG fallbacks for surfaces that do not render SVG.

   ```bash
   convert docs/assets/name.svg docs/assets/name.png
   ```

   Embed only the most useful graphics in `README.md`; put the full set in `docs/DIAGRAMS.md` to avoid making the README heavy.

5. Update `docs/MANIFEST.md` or the equivalent index when adding diagrams or maps so visual assets remain discoverable.

6. If using Archify for a local visual proof, write outputs under a local project-management path and keep that path out of normal source control unless Samuel explicitly wants the generated evidence tracked. Verify with `validate`, `deliver`, and `visual-check`; a generated HTML file is not done until the browser check passes.

7. Verify presentation edits without overbuilding:
   - parse SVGs as XML,
   - check PNG files exist and are non-empty,
   - scan Markdown image/link targets for missing files,
   - run `git diff --stat` and `git status --short --branch`.

8. When Samuel expects the polished repo to be visible on GitHub, make the local/remote boundary explicit. Untracked assets and README edits are invisible on GitHub until staged, committed, and pushed; after pushing, read back the exact remote branch and asset paths.

   ```bash
   git add README.md docs/DIAGRAMS.md docs/MANIFEST.md docs/REPOSITORY_MAP.md docs/assets
   git commit -m "docs: add repo diagrams"
   git push origin main
   git ls-remote origin refs/heads/main
   git ls-tree -r --name-only origin/main docs/assets README.md docs/DIAGRAMS.md
   gh repo view OWNER/REPO --json nameWithOwner,url,defaultBranchRef,pushedAt
   ```

