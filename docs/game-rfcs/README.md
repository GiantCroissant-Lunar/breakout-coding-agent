# Game RFCs - Breakout Implementation

## Purpose

Game RFCs define the specific features and systems for the Breakout game implementation. These are handled by GitHub Coding Agent once the Flow RFCs (workflow issues) are resolved.

## RFC Status Tracking

### ✅ Ready for Implementation

#### **Game-RFC-001: Console Game Shell**
**Status**: 📝 Draft - Ready to Implement  
**Priority**: Critical (Foundation)  
**Dependencies**: None  
**Estimated Time**: 1-2 days  
**Description**: Basic game loop, console setup, input handling

#### **Game-RFC-002: Paddle Implementation**
**Status**: 📝 Draft  
**Priority**: High  
**Dependencies**: Game-RFC-001  
**Estimated Time**: 1 day  
**Description**: Player-controlled paddle with movement

#### **Game-RFC-003: Ball Physics**
**Status**: 📝 Draft  
**Priority**: High  
**Dependencies**: Game-RFC-001, Game-RFC-002  
**Estimated Time**: 1-2 days  
**Description**: Ball movement, bouncing, collision with paddle

#### **Game-RFC-004: Brick System**
**Status**: 📝 Draft  
**Priority**: High  
**Dependencies**: Game-RFC-001, Game-RFC-003  
**Estimated Time**: 2 days  
**Description**: Brick layout, collision detection, scoring

#### **Game-RFC-005: Game State Management**
**Status**: 📝 Draft  
**Priority**: Medium  
**Dependencies**: All previous Game-RFCs  
**Estimated Time**: 1-2 days  
**Description**: Menus, win/lose conditions, game states

## Implementation Guidelines

### **Sequential vs Parallel**
- **Must be Sequential**: Game-RFC-001 → Game-RFC-002 → Game-RFC-003
- **Can be Parallel**: Game-RFC-004 (Bricks) can be implemented alongside Game-RFC-003 (Ball) if Game-RFC-001 is complete

### **Definition of Done**
Each Game-RFC is complete when:
- All acceptance criteria checkboxes are met
- Code compiles without warnings
- Feature works as demonstrated manually
- No regression in existing features
- PR merged to main branch

### **Current Focus**
🎯 **Start with Game-RFC-001** - This provides the foundation for all other features.

### **Assignment Process**
1. Check this README for RFC status
2. Choose an available RFC (status: Draft, dependencies met)
3. Read the full RFC specification in this folder
4. Create GitHub issue: `Implement Game-RFC-XXX: [Feature Name]`
5. Begin implementation according to AGENTS.md guidelines

## Notes

**Flow-RFC Dependency**: Game RFCs can only begin once Flow-RFC-001 (Basic PR Merge Cycle) is validated and working. This ensures GitHub Coding Agent can successfully merge implementation PRs.

**Progress Tracking**: Update this README when RFC status changes (Draft → In Progress → Complete).