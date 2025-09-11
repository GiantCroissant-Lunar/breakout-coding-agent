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

    # Try to suggest the exact issue number based on RFC number in the title
    rfc_num=$(printf "%s" "$PR_TITLE" | sed -nE 's/.*Game-RFC-([0-9]+).*/\1/p' | head -1)
    suggestion=""
    if [ -n "$rfc_num" ]; then
      issue_num=$(gh issue list --repo "$REPO" --state open --label game-rfc --json number,title \
        --jq ".[] | select(.title | test(\"Game-RFC-$rfc_num\\b\")) | .number" | head -1 || true)
      if [ -n "$issue_num" ]; then
        suggestion="# Add this line to the PR description\\n\\nFixes #$issue_num"
      fi
    fi

    gh pr comment "$PR_NUMBER" --repo "$REPO" --body @- <<EOF
Hi! This PR looks like a Game-RFC implementation but it doesn't reference its tracking issue. For full automation, please add a closing keyword to the PR description so the workflow can auto-merge it.

Recommended format:
${suggestion:-Fixes #<issue-number>}

Once updated, the Auto-merge workflow will re-run and proceed automatically. Thanks!
EOF
    exit 1
  fi

  echo "✅ Game-RFC validation passed"
else
  echo "ℹ️ Not a recognized RFC PR, skipping auto-merge"
  exit 0
fi

echo "✅ PR validation completed successfully"
