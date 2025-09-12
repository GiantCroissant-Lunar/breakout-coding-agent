# GraphQL Bot Assignment Test

## Overview

This test validates the GraphQL `createIssue` functionality with correct Bot assigneeIds as specified in [Issue #30](https://github.com/GiantCroissant-Lunar/breakout-coding-agent/issues/30).

## Purpose

The test addresses the requirement to validate that **Copilot should be assigned using the Bot entity ID** (`BOT_kgDOC9w8XQ`) instead of User ID when creating issues via GraphQL API.

## Test Components

### 1. `test_graphql_bot_assignment.py`

A comprehensive test script that:

- **Validates Bot ID**: Checks if the Bot ID `BOT_kgDOC9w8XQ` is valid and accessible
- **Tests GraphQL Assignment**: Creates issues via GraphQL API with Bot ID assignment
- **Compares with CLI**: Tests the current GitHub CLI assignment method (`copilot-swe-agent`)
- **Provides Analysis**: Compares both approaches and provides recommendations

### 2. Test Methods

#### GraphQL Approach
```graphql
mutation {
  createIssue(input: {
    repositoryId: "REPO_ID",
    title: "Test Issue",
    body: "Test Content",
    assigneeIds: ["BOT_kgDOC9w8XQ"]
  }) {
    issue {
      id
      assignees {
        nodes {
          id
          login
        }
      }
    }
  }
}
```

#### Current CLI Approach
```bash
gh issue create --title "Test Issue" --body "Test Content"
gh issue edit ISSUE_NUMBER --add-assignee copilot-swe-agent
```

## Key Findings from Research

Based on the repository's chat history and current implementation:

1. **Bot ID Discovery**: The Bot ID `BOT_kgDOC9w8XQ` was identified from successful assignments
2. **Working Solution**: Using `copilot-swe-agent` as assignee name works because GitHub automatically maps it to the Copilot bot
3. **GraphQL vs CLI**: Both approaches should work, but GitHub's internal mapping may handle them differently

## Expected Test Results

### Scenario 1: Both Methods Work
- ✅ GraphQL with Bot ID assigns successfully
- ✅ CLI with `copilot-swe-agent` assigns successfully
- ✅ Both result in Copilot being assigned

### Scenario 2: CLI Works, GraphQL Needs Investigation
- ❌ GraphQL with Bot ID fails (permission/validation issues)
- ✅ CLI with `copilot-swe-agent` works
- 🔍 Recommendation: Stick with CLI approach or investigate GraphQL permissions

### Scenario 3: GraphQL Works, CLI Issues
- ✅ GraphQL with Bot ID works
- ❌ CLI assignment fails
- 🔍 Recommendation: Migrate to GraphQL approach

## Running the Test

### Prerequisites
```bash
export GITHUB_TOKEN="your_github_token_with_issues_write_permission"
pip install requests  # for GraphQL API calls
```

### Execute Test
```bash
cd /path/to/breakout-coding-agent
python3 .github/scripts/test_graphql_bot_assignment.py
```

### Sample Output
```
🧪 GraphQL Bot Assignment Test Suite
Testing GitHub GraphQL API assignment with Bot ID
Bot ID: BOT_kgDOC9w8XQ
============================================================
🧪 Testing GraphQL createIssue with Bot ID assignment...
Repository ID: MDEwOlJlcG9zaXRvcnk...
Creating issue with Bot ID: BOT_kgDOC9w8XQ
🔍 Testing current GitHub CLI assignment approach...
🧹 Cleaning up test issues: ['123', '124']
   ✅ Closed issue #123
   ✅ Closed issue #124

============================================================
📊 TEST RESULTS SUMMARY
============================================================
🤖 Bot Validation: ✅ VALID
   Bot Info: Copilot (Bot)
📈 GraphQL Test: ✅ PASSED
   Assignees: ['Copilot']
🖥️  CLI Test: ✅ PASSED
   Assignment: ✅ SUCCESS
   Assignees: ['Copilot']
🔍 Comparison: Both methods work equivalently

============================================================
🎉 Test suite completed successfully!
```

## Integration with Existing Workflow

This test validates the assignment approach used in:

- `.github/scripts/create_next_rfc_issue.py` (line 252): Uses `copilot-swe-agent`
- `.github/workflows/assign-copilot.yml`: Uses REST API with `Copilot` assignee

## Security Considerations

- Test issues are automatically cleaned up after testing
- Uses test labels to avoid interference with real workflows
- Validates permissions before attempting assignments

## Troubleshooting

### Common Issues

1. **Token Permissions**: Ensure `GITHUB_TOKEN` has `issues:write` permission
2. **Bot Access**: The bot must be available for assignment in the repository
3. **Rate Limits**: GraphQL and REST API calls are subject to GitHub rate limits

### Debug Information

The test provides detailed output for troubleshooting:
- Bot validation results
- API response details
- Assignment success/failure reasons
- Cleanup status

## Related Documentation

- [GitHub GraphQL API Documentation](https://docs.github.com/en/graphql)
- [Issue Assignment via GraphQL](https://docs.github.com/en/graphql/reference/mutations#createissue)
- [Repository Chat History](../../docs/chat-history/copilit-name-transform.md) - Context of Bot ID discovery