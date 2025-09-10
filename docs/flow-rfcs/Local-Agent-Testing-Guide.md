# Flow-RFC-001: Local Agent Testing Guide

## 🎯 Objective
**For Local Agents (Claude/GPT)**: Instructions to test that GitHub Coding Agent can complete a full PR merge cycle automatically.

**Note**: This file is for human/local agent use, not for GitHub Coding Agent.

## 📋 Test Instructions for Local Agents

### **Activation Method**
Use GitHub issue templates to activate GitHub Coding Agent:

1. **Navigate to GitHub repository**
2. **Click**: Issues → New Issue
3. **Select**: "Flow-RFC-001 Test" template  
4. **Submit**: Issue (automatically mentions @copilot)
5. **Monitor**: GitHub Coding Agent activation and PR creation

### **Alternative: Manual Issue Creation**
If templates aren't available, create issue manually with:

**Title**: `Flow-RFC-001: Validate basic PR merge cycle`
**Body**: See `.github/ISSUE_TEMPLATE/flow-rfc-001-test.md` for exact format

### **Expected Behavior**
1. **Create feature branch**: `copilot/flow-rfc-001-test`
2. **Make this exact change** in README.md:
   
   **Change FROM**:
   ```markdown
   **Flow Engineering Phase**: Implementing basic PR merge cycle to validate GitHub Coding Agent can complete full development workflow.
   ```
   
   **Change TO**:
   ```markdown
   **Flow Engineering Phase**: ✅ Basic PR merge cycle validated - GitHub Coding Agent can complete full development workflow.
   ```

3. **Create PR** with title: `Flow-RFC-001: Validate basic PR merge cycle`
4. **Auto-merge**: GitHub Actions should automatically approve and merge
5. **Clean up**: Feature branch should be deleted

### **Auto-Merge Workflow**
The `.github/workflows/auto-merge.yml` will:
- Detect PRs from `copilot/` branches with "Flow-RFC-001" in title
- Validate only README.md was changed
- Auto-approve and squash merge
- Delete the feature branch

### **Success Criteria**
- ✅ GitHub Coding Agent creates proper feature branch
- ✅ Makes exactly the specified change to README.md
- ✅ Creates PR with correct title format
- ✅ GitHub Actions auto-merges the PR
- ✅ Feature branch is cleaned up
- ✅ Main branch contains the updated status

### **Validation Commands**
After the PR merges, verify:
```bash
# Check the change was applied
grep "✅ Basic PR merge cycle validated" README.md

# Verify branch was cleaned up
git branch -r | grep copilot/flow-rfc-001-test   # Should be empty

# Check main branch is up to date
git log --oneline -n 3   # Should show the merge commit
```

## 🚨 Troubleshooting

### **If Auto-Merge Fails**
1. Check GitHub Actions logs in the repository
2. Verify repository has proper permissions for auto-merge
3. Ensure no branch protection rules are blocking
4. Check if multiple files were changed (should only be README.md)

### **If GitHub Coding Agent Can't Create PR**
1. Verify repository has Coding Agent enabled
2. Check if branch already exists
3. Ensure proper permissions are set
4. Try with a different branch name

### **Manual Fallback**
If automation fails, manually:
1. Review the created PR
2. Verify the change is correct
3. Merge manually to complete Flow-RFC-001
4. Document what went wrong for Flow-RFC-002

## 📊 Learning Outcomes

**Success** means:
- GitHub Coding Agent can create branches
- Can make targeted file changes
- Can create properly formatted PRs
- Auto-merge workflow functions correctly
- Ready to proceed to Flow-RFC-002

**Failure** means:
- Need to debug specific step that failed
- May need simpler workflow or different approach
- Fix issues before attempting Game-RFC implementation

---

**This is the foundation test. Everything else depends on this working reliably.**