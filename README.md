# 🎮 Breakout Coding Agent

A classic Breakout game built with .NET, designed to test and validate GitHub Copilot Coding Agent workflows.

## 🤖 Project Purpose

This project implements a **two-track RFC approach**:

### **Track 1: Flow RFCs (Workflow Engineering)**
Solve GitHub Coding Agent workflow issues to enable reliable automation:
- ✅ Flow-RFC-001: Basic PR Merge Cycle
- ⏳ Flow-RFC-002: Conflict Resolution Strategy  
- ⏳ Flow-RFC-003: Quality Gates Integration
- ⏳ Flow-RFC-004: Issue-PR-RFC Linking
- ⏳ Flow-RFC-005: Agent Prompt Engineering

### **Track 2: Game RFCs (Breakout Implementation)**
Once workflow is solid, GitHub Coding Agent implements game features:
- ⏳ Game-RFC-001: Console Game Shell
- ⏳ Game-RFC-002: Paddle Implementation
- ⏳ Game-RFC-003: Ball Physics
- ⏳ Game-RFC-004: Brick System
- ⏳ Game-RFC-005: Game State Management

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository-url>
cd breakout-coding-agent

# Build and run
dotnet restore
dotnet build
dotnet run --project dotnet/game/Breakout.Game
```

## 📋 Current Status

**Flow Engineering Phase**: ✅ Basic PR merge cycle validated - GitHub Coding Agent can complete full development workflow.

**Game Development Phase**: 🎮 Game-RFC-001 (Console Game Shell) in progress - building foundation for Breakout game.

**RFC Coordination**: 📌 [Issue #3 - RFC Coordinator](https://github.com/GiantCroissant-Lunar/breakout-coding-agent/issues/3) (Pinned) - Central hub for all RFC implementations.

## 📚 Documentation

### **For GitHub Coding Agent**
- [AGENTS.md](AGENTS.md) - Instructions and guidelines for game implementation
- [docs/game-rfcs/](docs/game-rfcs/) - Game feature specifications to implement

### **For Local Agents (Claude/GPT)**
- [docs/flow-rfcs/](docs/flow-rfcs/) - Workflow engineering specifications
- [docs/flow-rfcs/Local-Agent-Testing-Guide.md](docs/flow-rfcs/Local-Agent-Testing-Guide.md) - How to test Flow-RFC-001

---

*This project is an experiment in AI-driven development workflows.*