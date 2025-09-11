#!/usr/bin/env bash
set -euo pipefail

PR_NUMBER="${PR_NUMBER:?PR_NUMBER is required}"
REPO="${GITHUB_REPOSITORY:?GITHUB_REPOSITORY is required}"

echo "Validating PR #${PR_NUMBER} for auto-merge eligibility..."

PR_TITLE=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json title --jq .title)

if [[ "$PR_TITLE" == *"Flow-RFC-001"* ]]; then
  echo "ℹ️ Flow-RFC-001 PR detected - applying special validation"

  # Validate only README.md changed
  files_changed=$(gh api repos/"$REPO"/pulls/"$PR_NUMBER"/files --jq '.[].filename' | wc -l)
  if [ "$files_changed" -gt 1 ]; then
    echo "❌ Too many files changed ($files_changed). Flow-RFC-001 should only change README.md"
    exit 1
  fi

  # Check if README.md was changed
  readme_changed=$(gh api repos/"$REPO"/pulls/"$PR_NUMBER"/files --jq '.[] | select(.filename == "README.md") | .filename')
  if [ -z "$readme_changed" ]; then
    echo "❌ README.md not changed. Flow-RFC-001 requires README.md update"
    exit 1
  fi

  echo "✅ Flow-RFC-001 validation passed"

elif [[ "$PR_TITLE" == *"Game-RFC-"* ]]; then
  echo "ℹ️ Game-RFC PR detected"

  # Validate PR references an issue using GitHub's own closing reference detection
  closing_count=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json closingIssuesReferences --jq '.closingIssuesReferences | length' || echo 0)
  if [ "${closing_count:-0}" -gt 0 ]; then
    echo "✅ PR properly references issue (closing keywords detected)"
  else
    echo "❌ Game-RFC PRs must reference the implementation issue (use 'Closes #issue-number' or 'Fixes #issue-number')"
    exit 1
  fi

  echo "✅ Game-RFC validation passed"
else
  echo "ℹ️ Not a recognized RFC PR, skipping auto-merge"
  exit 0
fi

echo "✅ PR validation completed successfully"

