# Workflow Cleanup for Micro-Issue Development - 2025-09-12

## Summary

This cleanup branch removes workflows that are incompatible with the new micro-issue development strategy and replaces them with micro-issue-focused automation.

## Key Findings from Investigation

Based on systematic investigation documented in `docs/flow-rfcs/GITHUB-COPILOT-WORKFLOW-FINDINGS-AND-STRATEGY-2025-09-12.md`:

### Critical Discoveries
1. **GitHub Copilot Bot assignment via API fails for existing issues** (assignments disappear within seconds)
2. **GraphQL createIssue with Bot ID works** for new issues with automatic assignment
3. **PR-Issue associations block new PR creation** even when PRs are closed/failed
4. **Manual Web UI assign/unassign cycle** is the only reliable activation for existing issues
5. **Micro-issue strategy** dramatically improves success rates vs monolithic RFCs

## Workflows Removed

### ❌ assign-copilot.yml
**Reason**: REST API assignment fails reliably. Replaced by GraphQL createIssue approach in micro-issue-automation.yml

**Evidence**: Comprehensive investigation showed 100% assignment failure rate via API despite HTTP 201 responses

### ❌ rfc-progression.yml  
**Reason**: Designed for monolithic Game-RFC progression, incompatible with micro-issue decomposition

**Issue**: Creates large, complex issues that lead to high failure rates and long execution times

### ❌ rfc-health-monitor.yml & rfc-health-monitor-simple.yml
**Reason**: Monitor monolithic RFC health, not applicable to micro-issues

**Better Approach**: Micro-issues fail fast and get replaced, eliminating need for health monitoring

### ❌ copilot-setup-steps.yml
**Reason**: One-time setup workflow, no longer needed with established micro-issue patterns

## Workflows Retained

### ✅ auto-merge.yml (Updated)
**Status**: Modified to recognize micro-issue pattern (Game-RFC-###-#)
**Enhancement**: Fast-track validation for micro-issues since they're small and focused

### ✅ auto-update-branches.yml
**Status**: Compatible with micro-issues (works on any Copilot branch)

### ✅ cleanup-branches.yml  
**Status**: Compatible with micro-issues (general branch maintenance)

### ✅ force-reset-stale-agent-branches.yml
**Status**: Compatible with micro-issues (handles stale PR recovery)

## New Workflow Added

### ✅ micro-issue-automation.yml
**Purpose**: Creates micro-issues with automatic Copilot assignment using GraphQL createIssue
**Features**: 
- Dynamic Bot ID retrieval
- Automatic assignment (bypasses API limitation)
- Decomposed Game-RFC templates
- Dependency management between micro-issues

**Example Usage**: 
```yaml
workflow_dispatch:
  inputs:
    game_rfc: "Game-RFC-004"  # Decomposes into Game-RFC-004-1, Game-RFC-004-2, Game-RFC-004-3
```

## Strategic Benefits

### Reliability Improvements
- **Higher Success Rate**: Small, focused micro-issues vs large monolithic RFCs
- **Faster Recovery**: "Start over" approach takes minutes instead of hours
- **Automatic Assignment**: No manual Web UI intervention needed for new issues

### Development Velocity  
- **Parallel Development**: Multiple micro-issues can be worked on simultaneously
- **Incremental Progress**: Partial completion preserved even if some micro-issues fail
- **Learning Iteration**: Failed micro-issues provide insights for better issue descriptions

### Workflow Automation
- **End-to-End**: GraphQL createIssue → Copilot implementation → Auto-merge
- **Dependency Management**: Sequential micro-issue assignment based on completion
- **Quality Gates**: Fast validation for small, focused changes

## Migration Path

### Phase 1: Validation (Current)
1. Test micro-issue-automation.yml with Game-RFC-004 decomposition
2. Validate GraphQL assignment method works reliably
3. Confirm auto-merge handles micro-issue PRs correctly

### Phase 2: Full Migration
1. Create micro-issue templates for all remaining Game-RFCs
2. Deploy GitHub Projects for visual progress tracking  
3. Implement failure recovery automation

### Phase 3: Optimization
1. Add analytics for micro-issue success rates
2. Implement intelligent batching based on dependencies
3. Cross-project adoption across yokan-projects ecosystem

## Testing Plan

1. **Create test micro-issues**: Use workflow_dispatch to create Game-RFC-004 micro-issues
2. **Monitor assignment**: Verify Copilot gets assigned automatically
3. **Track implementation**: Ensure micro-issues get completed faster than monolithic RFCs
4. **Validate auto-merge**: Confirm micro-issue PRs merge automatically
5. **Test failure recovery**: Verify "start over" approach works efficiently

## Success Metrics

- **Individual micro-issue success rate**: Target >80% (vs ~20% for monolithic RFCs)
- **Average execution time**: Target <10 minutes per micro-issue
- **Recovery time from failure**: Target <5 minutes (delete + recreate)
- **End-to-end automation**: No manual Web UI intervention required

---

This cleanup represents a fundamental shift from brittle monolithic RFC workflows to resilient micro-issue automation, based on systematic investigation of GitHub Copilot workflow limitations and capabilities.