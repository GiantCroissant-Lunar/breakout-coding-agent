# GitHub Coding Agent Flow: Findings and Fixes

Last updated: 2025-09-11

## Summary
GitHub Coding Agent was not consistently activating, causing Game‑RFC issues to pile up and PRs to stall. We analyzed the workflows and agent activation path, then applied targeted fixes so the agent can run autonomously with minimal maintainer input.

## Symptoms Observed
- New Game‑RFC issues created, but Copilot runner did not start.
- Auto‑merge workflow reported action_required or failed during validation.
- Health monitor could not be manually dispatched.

## Root Causes
1. Assignment gate: Copilot activation depends on the issue being assigned to the Copilot agent. From a maintainer’s local `gh`, assigning `copilot-swe-agent` works (displayed as “Copilot”) and starts the agent. From GitHub Actions `GITHUB_TOKEN`, assignment can be rejected for some repos.
2. Fragile validation: Auto‑merge previously parsed PR body inline, allowing multiline content to break the shell.
3. Dispatch schema: `rfc-health-monitor.yml` specified a `type: boolean` for an input, which is not supported in classic workflow_dispatch inputs, blocking manual dispatch.

## Fixes Applied
- Auto Merge RFC PRs (`.github/workflows/auto-merge.yml`)
  - Trigger: `pull_request_target` with types: opened, synchronize, reopened, ready_for_review, edited.
  - Permissions: `contents: write`, `pull-requests: write`.
  - Validation: Inlined robust logic using `gh pr view --json closingIssuesReferences`.
  - UX: If “Fixes #…” is missing, posts a gentle comment with the exact line to add, then exits cleanly.
  - Auto‑approve/merge: Squash + delete branch once valid.
  - Name: Renamed to “Auto Merge RFC PRs”.

- Assign Copilot to Game‑RFC Issues (`.github/workflows/assign-copilot.yml`)
  - Triggers: issues opened/reopened/labeled/edited (filtered to Game‑RFC).
  - Uses REST to assign `copilot-swe-agent` (fallback to `Copilot`) with `GITHUB_TOKEN`.
  - Always nudges with an `@copilot please start implementation` comment to encourage activation.

- RFC Health Monitor (`.github/workflows/rfc-health-monitor.yml`)
  - Fixed `workflow_dispatch` schema (removed unsupported input type) so manual dispatch works.

- RFC progression (context)
  - Continues to create the next Game‑RFC issue after a successful merge; the separate assign‑copilot workflow now handles activation reliably.

## How to Verify End‑to‑End
1. Create or update a Game‑RFC issue:
   - Expect: “Assign Copilot to Game‑RFC Issues” runs, assigns (or attempts to), and comments `@copilot...`.
   - Result: Copilot workflow appears in Actions within ~1 minute.
2. When Copilot opens a PR from a `copilot/*` branch:
   - If PR description includes `Fixes #<issue>`: auto‑merge validates, approves, and merges.
   - If not: the workflow comments the exact `Fixes #<issue>` to add, then re‑runs on edit.
3. After merge to `main`:
   - RFC progression runs, creates the next Game‑RFC issue.
   - Assign‑copilot workflow triggers on the new issue and activates Copilot again.

## Operator Runbook (Minimal Manual Step)
- Kick Copilot on a specific issue if needed:
  - `gh issue edit <num> --add-assignee copilot-swe-agent`
  - (GitHub maps to “Copilot” and triggers the agent.)
- If auto‑merge comments about missing `Fixes #…`, paste the suggested line into the PR description.
- Manually dispatch health monitor (optional):
  - `gh workflow run 'RFC Health Monitor'`

## Known Limitations & Mitigations
- Assign via Actions may intermittently return `not found` for the Copilot account on some repos using `GITHUB_TOKEN`.
  - Mitigation: We also post an `@copilot` comment. Local maintainer `gh` assignment is a reliable fallback and requires no PAT.
- Auto‑merge scopes to PRs from `copilot/*` branches by design (job‑level `if:`). Non‑Copilot PRs are intentionally ignored by the auto‑merge job.

## FAQ
- Does this require a PAT? No. Local `gh` by a maintainer or our REST + `@copilot` nudge is sufficient.
- What if the agent does not start? Assign via local `gh` or re‑label/edit the issue to re‑trigger the assign‑copilot workflow; confirm the “Copilot” workflow appears in Actions.
- Will this cause unsafe merges? No. Auto‑merge validates closing references and Flow‑RFC constraints before approving/merging.

---

With these fixes, the GitHub Coding Agent should reliably activate on new Game‑RFC issues, progress to PRs, and merge autonomously, with a minimal, well‑documented fallback if assignment from Actions is declined by GitHub.

