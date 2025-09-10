# 🎮 Breakout Coding Agent - Claude Context

## Project Overview

This is an experimental project to validate GitHub Copilot Coding Agent workflows using a two-track RFC approach:

1. **Flow RFCs** - Solve GitHub Coding Agent workflow issues (handled by local agents like Claude)
2. **Game RFCs** - Implement Breakout game features (handled by GitHub Coding Agent)

## 🤖 For Local Agents (Claude/GPT)

### **Primary Responsibility: Flow RFCs**
Local agents handle workflow engineering to enable GitHub Coding Agent success.

### **Current Task: Flow-RFC-001 Testing**
**Immediate Action Required**: Test the basic PR merge cycle

📋 **See**: 
- [docs/flow-rfcs/Local-Agent-Testing-Guide.md](docs/flow-rfcs/Local-Agent-Testing-Guide.md) - Step-by-step testing
- [docs/flow-rfcs/GitHub-Coding-Agent-Activation-Guide.md](docs/flow-rfcs/GitHub-Coding-Agent-Activation-Guide.md) - Complete workflow explanation

**Summary of Test**:
1. Push this repository to GitHub
2. Enable GitHub Copilot Coding Agent
3. Create GitHub issue asking agent to update README status
4. Verify agent can create PR and auto-merge works
5. Validate complete PR merge cycle

### **Flow-RFC Implementation Status**
- ✅ **Flow-RFC-001**: Auto-merge workflow implemented, ready for testing
- ⏳ **Flow-RFC-002**: Conflict Resolution Strategy (pending Flow-RFC-001 success)
- ⏳ **Flow-RFC-003**: Quality Gates Integration (CI/CD)
- ⏳ **Flow-RFC-004**: Issue-PR-RFC Linking
- ⏳ **Flow-RFC-005**: Agent Prompt Engineering

## 🎮 For GitHub Coding Agent

### **Primary Responsibility: Game RFCs**
GitHub Coding Agent implements game features once workflow is validated.

📋 **See**: [AGENTS.md](AGENTS.md) for complete instructions

**Current Game RFCs Available**:
1. **Game-RFC-001**: Console Game Shell (ready when Flow-RFC-001 complete)
2. **Game-RFC-002**: Paddle Implementation
3. **Game-RFC-003**: Ball Physics
4. **Game-RFC-004**: Brick System
5. **Game-RFC-005**: Game State Management

## 🚨 Critical Dependencies

**Game RFCs CANNOT start** until Flow-RFC-001 is validated. The previous failed projects (`dungeon-coding-agent`, `falling-block-coding-agent`) failed because GitHub Coding Agent couldn't complete the PR merge cycle.

## 📁 File Organization

### **Local Agent Files**
- `docs/flow-rfcs/` - Workflow engineering specifications
- `docs/flow-rfcs/Local-Agent-Testing-Guide.md` - Flow-RFC-001 testing instructions
- `.github/workflows/auto-merge.yml` - Auto-merge implementation

### **GitHub Coding Agent Files**
- `AGENTS.md` - Instructions for game implementation
- `docs/game-rfcs/` - Game feature specifications
- `dotnet/game/` - Game implementation directory

## 🎯 Success Criteria

### **Phase 1: Flow Validation** (Local Agents)
- ✅ Flow-RFC-001 auto-merge cycle works reliably
- ✅ GitHub Coding Agent can merge PRs without human intervention
- ✅ Workflow handles basic edge cases

### **Phase 2: Game Implementation** (GitHub Coding Agent)
- ✅ All 5 Game RFCs implemented successfully
- ✅ Working Breakout game from start to finish
- ✅ Validates AI-driven development workflow

## 🔗 Workspace Integration

This project is part of the `lunar-snake` workspace experiment in AI-driven development. Success here validates the approach for other yokan-projects.

### **Related Projects**
- `dungeon-coding-agent` - Previous failed attempt (too complex)
- `falling-block-coding-agent` - Previous failed attempt (workflow issues)

### **Lessons Applied**
- Simpler scope (Breakout vs complex dungeon crawler)
- Two-track approach (separate workflow and feature development)
- Automated merge (GitHub Actions vs manual coordination)
- Clear separation of responsibilities (local vs GitHub agents)

## 📋 Next Actions for Claude

1. **Immediate**: Review Flow-RFC-001 testing guide and prepare for GitHub testing
2. **After Flow-RFC-001 Success**: Implement Flow-RFC-002 (conflict resolution)
3. **Monitor**: GitHub Coding Agent Game-RFC implementation progress
4. **Document**: Lessons learned for other workspace projects

---

**This project is the foundation for validating AI agent workflows across the entire yokan-projects ecosystem.**