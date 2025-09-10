# Flow RFCs - GitHub Coding Agent Workflow Engineering

## Purpose

Flow RFCs solve the workflow and process issues that prevent GitHub Coding Agent from completing full development cycles. These must be solved first before Game RFCs can be successfully implemented.

## RFC Status

### ✅ Flow-RFC-001: Basic PR Merge Cycle
**Status**: 🔄 Implementing  
**Goal**: Get GitHub Coding Agent to merge a simple PR  
**Acceptance Criteria**:
- [ ] GitHub Coding Agent creates feature branch
- [ ] Makes trivial change (update README)
- [ ] Creates PR with proper title/description  
- [ ] Merges PR without human intervention
- [ ] Deletes feature branch

### ⏳ Flow-RFC-002: Conflict Resolution Strategy
**Status**: 📝 Draft  
**Goal**: Handle rebasing and merge conflicts automatically  
**Dependencies**: Flow-RFC-001

### ⏳ Flow-RFC-003: Quality Gates Integration  
**Status**: 📝 Draft  
**Goal**: Enforce build/test passing before merge  
**Dependencies**: Flow-RFC-001

### ⏳ Flow-RFC-004: Issue-PR-RFC Linking
**Status**: 📝 Draft  
**Goal**: Clear traceability between issues, PRs, and RFCs  
**Dependencies**: Flow-RFC-001, Flow-RFC-003

### ⏳ Flow-RFC-005: Agent Prompt Engineering
**Status**: 📝 Draft  
**Goal**: Optimize AGENTS.md for reliable behavior  
**Dependencies**: Flow-RFC-001 through Flow-RFC-004

## Implementation Notes

**Current Focus**: Flow-RFC-001 is the foundation. All other workflow improvements depend on proving GitHub Coding Agent can complete basic PR merge cycle.

**Key Learning**: Previous failed projects showed GitHub Coding Agent struggles with complex coordination. Flow RFCs start with simplest possible workflow and add complexity incrementally.

## Testing Flow-RFC-001

See `Local-Agent-Testing-Guide.md` in this folder for step-by-step instructions on how to test the basic PR merge cycle with GitHub Coding Agent.

## Next Steps

1. Complete Flow-RFC-001 (basic merge) - **Use Local-Agent-Testing-Guide.md**
2. Validate with multiple test PRs
3. Move to Flow-RFC-002 (conflict handling)
4. Only start Game RFCs once workflow is solid