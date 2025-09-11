# GitHub Copilot Coding Agent Investigation Findings

**Date**: 2025-09-11  
**Context**: Investigating why GitHub Copilot Coding Agent is not creating PRs despite apparent successful assignments

## 🔍 Key Discoveries

### 1. Assignment Username Confusion RESOLVED

**Initial Assumption**: `copilot-swe-agent` was the correct assignment username but suddenly stopped working
**Reality**: 
- **Assignment username**: `"Copilot"` (what shows in issue assignees)
- **PR author**: `"app/copilot-swe-agent"` (the GitHub App that creates PRs)
- `copilot-swe-agent` was **NEVER** used for assignment - only as the PR author

**Historical Evidence**:
- PR #14 (created by `app/copilot-swe-agent`) had assignees: `ApprenticeGC` and `Copilot`
- Assignment timeline shows `Copilot` was assigned at `03:04:53Z`, PR created at `03:04:57Z`
- Fallback workflow (commit ef48202) was added because `copilot-swe-agent` assignments were failing

### 2. Assignment Behavior Analysis

**Test Results**:

#### Issue #15: Copilot Assignment ✅
- Command: `gh api repos/.../issues/15/assignees -X POST -f assignees[]=Copilot`
- Result: `"assignee": {"login": "Copilot", "id": 198982749}`
- Reactions: `"eyes": 1` (👀 emoji added)
- Status: **Assignment successful, GitHub Copilot acknowledged**

#### Issue #21: copilot-swe-agent Assignment ❌
- Command: `gh api repos/.../issues/21/assignees -X POST -f assignees[]=copilot-swe-agent`  
- Result: `"assignee": null, "assignees": []`
- Reactions: `"eyes": 0` (no emoji)
- Status: **Silent failure - assignment doesn't stick**

### 3. Current Problem: No GitHub Actions Runs

**Symptom**: Even successful `Copilot` assignments (with 👀 reactions) are not triggering GitHub Actions runs

**Issues with successful assignments but no activity**:
- Issue #13: Assigned to Copilot, has 👀 reaction, but no PR created
- Issue #15: Assigned to Copilot, has 👀 reaction, but no PR created

**Monitoring Results**: 6 checks over 3 minutes showed only our scheduled workflows, no GitHub Copilot activity

## 🚨 Critical Issues Identified

### Repository Configuration Issues

Based on GitHub Copilot documentation research:

1. **GitHub Actions Dependency**: Copilot requires GitHub-hosted runners (not self-hosted)
2. **Managed User Account Restrictions**: Personal repos with managed accounts can't use Copilot
3. **Workflow Approval**: GitHub Actions workflows need manual "Approve and run workflows" approval
4. **Plan Requirements**: Needs Copilot Pro/Pro+/Business/Enterprise
5. **Repository Setup**: May need `.github/workflows/copilot-setup-steps.yml`

### Potential Root Causes

1. **Missing Repository Setup**: No `copilot-setup-steps.yml` workflow
2. **Plan/Permission Issues**: Account may not have proper Copilot plan access
3. **GitHub Actions Approval**: Copilot's Actions may need manual approval
4. **Enterprise Policy**: Administrator may need to enable Copilot policy

## 📋 Action Items for Resolution

### Immediate Investigation Needed
1. ✅ Verify GitHub Copilot plan access for repository owner
2. ✅ Check if `.github/workflows/copilot-setup-steps.yml` is needed
3. ✅ Confirm GitHub Actions are enabled and working for repository
4. ✅ Check for any pending workflow approval requirements
5. ✅ Verify repository isn't using managed user account restrictions

### Testing Protocol
1. ✅ Create test issue with clear, well-scoped requirements
2. ✅ Assign to `Copilot` (not `copilot-swe-agent`)
3. ✅ Monitor for 👀 reaction (confirms acknowledgment)
4. ✅ Monitor GitHub Actions for coding agent runs
5. ✅ Check for any approval prompts in GitHub Actions tab

## 🔧 Workflow Fixes Applied

### 1. Assignment Workflow Fixed
**File**: `.github/workflows/assign-copilot.yml`
**Change**: Removed `copilot-swe-agent` attempts, use only `Copilot`
**Commit**: f057476

### 2. Force Reset Workflow Fixed  
**File**: `.github/workflows/force-reset-stale-agent-branches.yml`
**Change**: Added check to prevent resetting completed (non-draft) PRs
**Commit**: 2ab611a

### 3. RFC Health Monitor Fixed
**File**: `.github/workflows/rfc-health-monitor.yml`  
**Change**: Fixed assignee query to properly detect Copilot assignments
**Commit**: f17f4f4

## ⚠️ Outstanding Questions

1. **Why did previous Copilot assignments work?** (PR #14, #16 were created successfully)
2. **What changed between working assignments and current non-working ones?**
3. **Are there GitHub Copilot repository-specific settings that need enabling?**
4. **Does the repository need special onboarding for GitHub Copilot coding agent?**

## 📊 Current Status

- ✅ **Assignment mechanism**: Working (`Copilot` username confirmed)
- ✅ **GitHub Copilot acknowledgment**: Working (👀 reactions present)  
- ❌ **GitHub Actions execution**: Not working (no coding agent runs)
- ❌ **PR creation**: Not happening despite successful assignments

**Next Step**: Focus on repository configuration and GitHub Actions setup requirements for GitHub Copilot coding agent.