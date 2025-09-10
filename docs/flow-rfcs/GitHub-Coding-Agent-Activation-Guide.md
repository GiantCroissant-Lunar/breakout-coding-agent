# GitHub Coding Agent Activation Guide

## 🤖 How GitHub Coding Agent Works

GitHub Coding Agent is **event-driven** - it activates when mentioned (`@copilot`) in:
- Issue descriptions
- Issue comments  
- PR comments
- PR descriptions

**Key Insight**: Each mention creates a new agent instance that works in a GitHub Actions runner.

## 🎯 Activation Methods

### **Method 1: Direct Issue Creation** (Recommended for Flow-RFC-001)

1. **Create GitHub issue** using template: "Flow-RFC-001 Test"
2. **Issue automatically mentions @copilot** with specific instructions
3. **Agent activates** immediately and begins work
4. **Agent creates PR** that references the issue
5. **Auto-merge workflow** handles the PR

**Steps**:
```bash
1. Go to GitHub repository
2. Click "Issues" → "New Issue"  
3. Select "Flow-RFC-001 Test" template
4. Click "Submit new issue"
5. GitHub Coding Agent activates automatically
```

### **Method 2: Coordinator Issue** (For ongoing RFC management)

1. **Create permanent coordinator issue** using template
2. **Comment on coordinator issue**: "@copilot please implement Game-RFC-001"
3. **Agent creates new implementation issue** 
4. **Agent mentions @copilot** in new issue to activate implementation
5. **Implementation agent creates PR** linked to specific issue

## 🔗 RFC-Issue-PR Linking Strategy

### **Flow-RFC-001 (Special Case)**
```
RFC: docs/flow-rfcs/RFC-001-Basic-PR-Merge-Cycle.md
 ↓
Issue: "Flow-RFC-001: Validate basic PR merge cycle" 
       (mentions @copilot with specific task)
 ↓  
PR: "Flow-RFC-001: Validate basic PR merge cycle"
    (auto-created by GitHub Coding Agent)
 ↓
Auto-merge: GitHub Actions validates and merges
```

### **Game-RFCs (Standard Pattern)**
```
RFC: docs/game-rfcs/RFC-001-Console-Game-Shell.md
 ↓
Issue: "Implement Game-RFC-001: Console Game Shell"
       (created from template, mentions @copilot)
 ↓
PR: "Implement Game-RFC-001: Console Game Shell"  
    (created by agent, includes "Closes #issue-number")
 ↓
Auto-merge: GitHub Actions validates Game-RFC PR format
```

## 📋 Issue Templates Available

### **1. Flow-RFC-001 Test** (`flow-rfc-001-test.md`)
- **Purpose**: Test basic PR merge cycle
- **Auto-mentions**: @copilot with exact task instructions
- **Validation**: Only README.md change allowed
- **Auto-merge**: Yes (GitHub Actions)

### **2. Game-RFC Implementation** (`game-rfc-implementation.md`)
- **Purpose**: Implement specific Game-RFC features
- **Requires**: Manual editing to specify RFC number/name
- **Auto-mentions**: @copilot with RFC reference
- **Validation**: Must reference implementation issue
- **Auto-merge**: Yes (if PR format correct)

### **3. RFC Coordinator** (`rfc-coordinator.md`)
- **Purpose**: Ongoing RFC management and assignment
- **Usage**: Comment to request RFC implementations
- **Creates**: New issues for specific RFCs
- **Persistence**: One permanent issue for all coordination

## 🔄 Complete Workflow Example

### **Testing Flow-RFC-001**
```bash
# Step 1: Create Issue
Go to GitHub → Issues → New Issue → "Flow-RFC-001 Test"

# Step 2: Agent Activation  
Issue created → @copilot mentioned → Agent activates in runner

# Step 3: Agent Implementation
Agent creates branch: copilot/flow-rfc-001-test
Agent modifies: README.md (one line change)
Agent creates PR: "Flow-RFC-001: Validate basic PR merge cycle"

# Step 4: Auto-Merge
GitHub Actions validates PR format
GitHub Actions auto-approves PR
GitHub Actions merges and deletes branch

# Step 5: Validation
README.md shows: "✅ Basic PR merge cycle validated"
Issue automatically closed by PR merge
```

### **Implementing Game-RFC-001**  
```bash
# Step 1: Create Issue
Go to GitHub → Issues → New Issue → "Game-RFC Implementation"
Edit template: Replace XXX with 001, add Console Game Shell

# Step 2: Agent Activation
Issue mentions @copilot → Agent reads docs/game-rfcs/RFC-001-Console-Game-Shell.md

# Step 3: Agent Implementation  
Agent creates branch: copilot/game-rfc-001-console-shell
Agent implements: Game loop, input system, console setup
Agent creates PR: "Implement Game-RFC-001: Console Game Shell"
PR body includes: "Closes #[issue-number]"

# Step 4: Auto-Merge
GitHub Actions validates Game-RFC PR format
GitHub Actions auto-approves and merges
Implementation issue automatically closed
```

## 🚨 Critical Success Factors

### **For Auto-Merge to Work**
1. **Branch naming**: Must start with `copilot/`
2. **PR titles**: Must include "Flow-RFC-001" or "Game-RFC-XXX"
3. **Issue linking**: Game-RFC PRs must include "Closes #issue-number"
4. **File constraints**: Flow-RFC-001 only allows README.md changes

### **For Agent Activation**
1. **Clear instructions**: Be specific about what to implement
2. **RFC references**: Always point to specific RFC file
3. **@copilot mention**: Required to activate the agent
4. **Proper templates**: Use issue templates for consistency

## 🎯 Testing Checklist

Before testing Flow-RFC-001:
- [ ] Repository pushed to GitHub
- [ ] GitHub Coding Agent enabled for repository
- [ ] Issue templates are available
- [ ] GitHub Actions auto-merge workflow configured
- [ ] Repository has proper permissions for auto-merge

---

**This workflow solves the core problem from your failed experiments: reliable PR merge cycle with clear RFC-Issue-PR linking.**