---
name: local-project-github-publication
description: Use when publishing or polishing a local GitHub repo.
version: 0.1.0
author: hai-agent
license: internal
metadata:
  hermes:
    tags: [github, git, repo-publication, gh]
    related_skills: [github]
---

# Local Project GitHub Publication

## Use When
Use when Samuel asks to make the current local directory a GitHub repository, or to make a just-published/local repo presentable before or after the first push. This includes README polish, repo maps, diagrams, manifest cleanup, and safe publication checks.

## Procedure

1. Establish exact local state and account before changing anything.

   ```bash
   pwd
   git branch --show-current
   git status --short --branch
   git remote -v
   gh auth status
   gh api user --jq '.login'
   ```

2. Inspect what will be published.

   Read `.gitignore`, list tracked/untracked project files, and search publishable text for obvious credential markers before staging. Do not print secrets. Fix exclusions before the initial commit.

   - Worktree check: if `git rev-parse --git-common-dir` is not `.git`, this directory is a worktree of another repo. Do not create a second GitHub repo; push the branch to the main repo's remote.
   - Exclude agent/runtime artifacts before `git add -A`: `.codex/`, `.claude/`, `.env*`, browser profiles (`*/Default/Preferences`, `*-profile*/`), `node_modules/`, `.venv/`. Add them to `.gitignore`, do not rely on memory.
   - Scan the full history, not just the working tree, with a real scanner, and stop on any finding:

     ```bash
     gitleaks git . --no-banner --redact            # existing history
     gitleaks dir . --no-banner --redact            # files about to be added
     ```

     Findings in saved web pages (`*.html`, `*_files/*.js`) are usually site keys, but still block publication until Samuel decides (remove from history or keep local).
   - Block files >50 MB (GitHub hard limit is 100 MB); move them out or to LFS only with Samuel's consent.

3. Verify the project before publishing.

   Run the repo's narrow test/build command. For Python unittest repos, prefer:

   ```bash
   python3 -m unittest discover -s tests -p 'test_*.py' -v
   ```

4. Check for a remote name collision under the active GitHub user.

   ```bash
   GH_USER=$(gh api user --jq '.login')
   gh repo view "$GH_USER/REPO_NAME" --json nameWithOwner,visibility,url 2>/dev/null || true
   ```

5. Create the initial commit and GitHub repo only after the checks pass.

   If there are no commits yet:

   ```bash
   git add -A
   git commit -m "Initial commit"
   git branch -M main
   gh repo create REPO_NAME --private --source=. --remote=origin --push --description "Short description"
   ```

   If commits already exist, do not rewrite history; create the remote and push the current branch deliberately.

6. Verify by reading back both local and GitHub state.

   ```bash
   git status --short --branch
   git remote -v
   git log --oneline -1
   gh repo view "$GH_USER/REPO_NAME" --json nameWithOwner,visibility,url,defaultBranchRef,pushedAt
   ```

   The default branch must equal the local working branch (`git branch --show-current`). `git push --all` can make GitHub pick another branch; only commits on the default branch count in Samuel's contribution graph. Fix with `gh repo edit "$GH_USER/REPO_NAME" --default-branch <branch>`.

7. Add a license.

   - Never overwrite an existing `LICENSE`/`COPYING`. If the repo contains vendored or cloned third-party code, keep the upstream license and do not add a new one.
   - Otherwise default to MIT with `Copyright (c) <year> Samuel Fleig`, unless Samuel names another license. Docs-only repos: CC-BY-4.0.

     ```bash
     gh api /licenses/mit --jq .body | sed "s/\[year\]/$(date +%Y)/; s/\[fullname\]/Samuel Fleig/" > LICENSE
     git add LICENSE && git commit -m "Add MIT license"
     ```

   - Verify: `gh repo view "$GH_USER/REPO_NAME" --json licenseInfo --jq .licenseInfo.spdxId` returns the intended SPDX id after push.

8. Add topics.

   - 3–8 topics, lowercase, hyphenated, derived from evidence in the repo (languages from file extensions, frameworks from manifests like `package.json`/`pyproject.toml`, domain words from README). No invented or aspirational topics.
   - Samuel's recurring domains are fair when the repo really belongs there: `hai`, `hermes-agent`, `ai-agents`, `claude-code`, `codex`, `llm-tooling`.

     ```bash
     gh repo edit "$GH_USER/REPO_NAME" --add-topic python,ai-agents,claude-code
     gh repo view "$GH_USER/REPO_NAME" --json repositoryTopics --jq '[.repositoryTopics[].name]'
     ```

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

## Always-on Rules

- Treat a direct request to make the project a GitHub repo as permission to create the remote, push the initial state, add a license and add topics (steps 7–8), but keep the action narrow: no releases, branch protection, CI, or visibility changes unless asked.
- Prefer `--private` when Samuel does not specify public/private, because the safe default is publication only to the authenticated owner.
- Normalize a new root repository to `main` before the first push, unless the project already has a meaningful branch convention.
- Verify the GitHub repo with `gh repo view` after creation; a successful push alone does not prove intended owner, visibility, or default branch.
- Report the final URL, visibility, remote, branch, commit hash, and test result tersely.

## Pitfalls

- Do not skip the credential-marker pass before `git add -A`; the first commit is the easiest place to accidentally publish local secrets.
- Do not assume the active `gh` account from memory; multiple accounts can be logged in and only one is active.
- Do not create a public repo by default; visibility is an external exposure decision.
- Do not claim GitHub success from local git state; read the remote object back from GitHub.
