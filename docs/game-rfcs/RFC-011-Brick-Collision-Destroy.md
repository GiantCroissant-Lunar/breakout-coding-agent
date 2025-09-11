# Game-RFC-011: Brick Collision Destroy

## Overview

Objective: Remove a brick and increment score when the ball hits it.

Priority: Medium  
Dependencies: Game-RFC-009 (Ball Wall Bounce), Game-RFC-010 (Single Row Bricks Render)

## Scope (Reduced)
- Detect ball/brick intersection (simple AABB or point-in-rect check)
- On hit: mark brick destroyed and increment score
- Reuse wall-bounce behavior; invert ball direction on hit for now

## Acceptance Criteria
- [ ] Ball destroys exactly one brick per hit
- [ ] Score increments on destruction
- [ ] No exceptions under rapid consecutive hits
- [ ] Code compiles without warnings

## Technical Notes
- After collision, clamp ball outside the brick to avoid double-processing next frame
- Keep collision simple and fast; one row of bricks means linear scan is fine
- Update score tracking on the `Game` model

## File Organization
- `dotnet/game/Breakout.Game/Systems/CollisionSystem.cs`
- `dotnet/game/Breakout.Game/Models/Brick.cs` (unchanged shape)
- `dotnet/game/Breakout.Game/Models/Game.cs` (score field)

---

This builds on prior micro-RFCs to make brick destruction work in the smallest useful step.
