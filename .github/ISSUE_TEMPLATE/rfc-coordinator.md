---
name: RFC Coordinator
about: Coordinate and assign RFC implementations
title: 'RFC Coordinator - Request Implementation'
labels: ['coordinator', 'rfc-management']
assignees: []
---

## 🤖 RFC Coordinator

**Purpose**: This is a permanent issue for coordinating RFC implementations with GitHub Coding Agent.

## 📋 How to Request RFC Implementation

### **For Flow-RFCs** (handled by local agents)
Comment with:
```
@copilot please help test Flow-RFC-XXX according to docs/flow-rfcs/Local-Agent-Testing-Guide.md
```

### **For Game-RFCs** (handled by GitHub Coding Agent)
Comment with:
```
@copilot please create an implementation issue for Game-RFC-XXX: [Feature Name]

RFC Specification: docs/game-rfcs/RFC-XXX-[Feature-Name].md
Dependencies: [List any prerequisites]
Priority: [High/Medium/Low]
```

## 📊 Current RFC Status

### **Flow-RFCs** (Workflow Engineering)
- ⏳ **Flow-RFC-001**: Basic PR Merge Cycle - Ready for testing
- 📝 **Flow-RFC-002**: Conflict Resolution Strategy - Draft
- 📝 **Flow-RFC-003**: Quality Gates Integration - Draft
- 📝 **Flow-RFC-004**: Issue-PR-RFC Linking - Draft
- 📝 **Flow-RFC-005**: Agent Prompt Engineering - Draft

### **Game-RFCs** (Feature Implementation)
- 📝 **Game-RFC-001**: Console Game Shell - Ready (pending Flow-RFC-001)
- 📝 **Game-RFC-002**: Paddle Implementation - Draft
- 📝 **Game-RFC-003**: Ball Physics - Draft
- 📝 **Game-RFC-004**: Brick System - Draft
- 📝 **Game-RFC-005**: Game State Management - Draft

## 🔄 Workflow

1. **Comment** on this issue requesting RFC implementation
2. **@copilot creates** specific implementation issue
3. **@copilot implements** the RFC in that issue
4. **PR links** to the implementation issue
5. **RFC status** updates when complete

## 📚 References

- **Flow-RFCs**: `docs/flow-rfcs/`
- **Game-RFCs**: `docs/game-rfcs/`
- **Agent Instructions**: `AGENTS.md`
- **Local Agent Context**: `CLAUDE.md`

---

**Use this issue to coordinate all RFC work. Each comment mentioning @copilot will activate the appropriate agent.**