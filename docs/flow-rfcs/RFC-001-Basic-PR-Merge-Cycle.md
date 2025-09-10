# Flow-RFC-001: Basic PR Merge Cycle

**Status**: 🔄 Implementing  
**Priority**: Critical  
**Dependencies**: None  
**Implementation**: Local Agent (Claude/GPT)

## 🎯 Problem Statement

GitHub Coding Agent cannot complete full development cycles because:
1. PRs are created but not merged automatically
2. No reliable workflow for branch → implement → merge cycle
3. Previous experimental projects failed at the basic PR merge step
4. Need foundation workflow before any Game-RFC implementation

## 🎯 Goal

Establish a reliable, automated PR merge cycle that GitHub Coding Agent can complete without human intervention.

## 📋 Acceptance Criteria

### **Core Workflow**
- [ ] GitHub Coding Agent can create feature branch (`copilot/flow-rfc-001-test`)
- [ ] Can make targeted file changes (update specific line in README.md)
- [ ] Can create PR with proper title and description format
- [ ] GitHub Actions automatically validates and merges PR
- [ ] Feature branch is automatically deleted after merge
- [ ] Main branch contains the merged changes

### **Validation Tests**
- [ ] Manual test: Create GitHub issue asking agent to update README status
- [ ] Agent creates PR that merges successfully without human intervention
- [ ] Workflow handles basic scenarios (single file change, no conflicts)
- [ ] Auto-merge only triggers for Flow-RFC-001 test PRs (safety)

### **Quality Gates**
- [ ] Only README.md is modified (single file change constraint)
- [ ] Change is exactly as specified (no extra modifications)
- [ ] PR title follows format: "Flow-RFC-001: [description]"
- [ ] GitHub Actions logs show successful auto-merge execution

## 🛠️ Implementation

### **1. GitHub Actions Auto-Merge Workflow**
`.github/workflows/auto-merge.yml`:
- Triggers on PRs from `copilot/` branches
- Validates PR contains "Flow-RFC-001" in title
- Confirms only README.md was changed
- Auto-approves and squash merges
- Deletes feature branch

### **2. Test Change Specification**
README.md line change:
```markdown
# FROM:
**Flow Engineering Phase**: Implementing basic PR merge cycle to validate GitHub Coding Agent can complete full development workflow.

# TO:
**Flow Engineering Phase**: ✅ Basic PR merge cycle validated - GitHub Coding Agent can complete full development workflow.
```

### **3. GitHub Coding Agent Instructions**
AGENTS.md updated to focus only on Game-RFCs, not Flow-RFCs.

### **4. Test Protocol**
1. Create GitHub issue: "Update README status for Flow-RFC-001 completion"
2. GitHub Coding Agent should:
   - Create `copilot/flow-rfc-001-test` branch
   - Make the specified README.md change
   - Create PR with title "Flow-RFC-001: Validate basic PR merge cycle"
   - Auto-merge should handle the rest

## 🚨 Risk Mitigation

### **Safety Constraints**
- Auto-merge only for PRs with "Flow-RFC-001" in title
- Single file change validation (reject if multiple files modified)
- Specific branch name pattern (`copilot/flow-rfc-001-test`)

### **Fallback Plan**
If auto-merge fails:
1. Review GitHub Actions logs
2. Manually merge the PR to complete Flow-RFC-001
3. Debug and fix auto-merge for Flow-RFC-002
4. Document specific failure points

## 📊 Success Metrics

### **Technical Success**
- GitHub Coding Agent creates PR ✅
- Auto-merge workflow executes ✅  
- PR merges without human intervention ✅
- Feature branch cleaned up ✅
- No build or lint errors ✅

### **Process Success**
- End-to-end workflow completes in < 5 minutes
- No manual steps required
- Repeatable for future RFCs
- Clear error messages if workflow fails

## 🔄 Next Steps

### **After Flow-RFC-001 Success**
1. **Flow-RFC-002**: Conflict Resolution Strategy
2. **Flow-RFC-003**: Quality Gates Integration (CI/CD)
3. **Flow-RFC-004**: Issue-PR-RFC Linking
4. **Flow-RFC-005**: Agent Prompt Engineering

### **Game-RFC Implementation**
Once Flow RFCs are solid:
1. Create issues for Game-RFC-001 through Game-RFC-005
2. GitHub Coding Agent implements game features
3. Workflow automatically handles all PR merges
4. Working Breakout game emerges from automated development

## 🎯 Definition of Done

Flow-RFC-001 is complete when:
- [ ] GitHub Coding Agent successfully merges at least one PR automatically
- [ ] Auto-merge workflow is tested and validated
- [ ] README.md shows "✅ Basic PR merge cycle validated"
- [ ] Process is documented and repeatable
- [ ] Ready to proceed to Flow-RFC-002

---

**This is the foundation. Everything else depends on proving this works reliably.**