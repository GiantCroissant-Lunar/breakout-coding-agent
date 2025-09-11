# Game-RFC-010: Single Row Bricks Render

## Overview

Objective: Render a single visible row of bricks at the top of the playfield.

Priority: Medium  
Dependencies: Game-RFC-001 (Console Shell)

## Scope (Reduced)
- Create a list of bricks across one row (fixed count, spacing)
- Draw all non-destroyed bricks each frame (no collision yet)
- Keep redraw clean without flicker/overlap

## Acceptance Criteria
- [ ] A single row of bricks renders on screen
- [ ] Bricks maintain spacing/width consistently
- [ ] Redrawing frames does not produce flicker/ghosting
- [ ] Code compiles without warnings

## Technical Notes
- Use a simple `Brick` model with `X`, `Y`, `IsDestroyed`
- Rendering can be in a `RenderSystem` method that iterates bricks and draws only those not destroyed
- Choose a bright color for visibility and reset console color after drawing

## File Organization
- `dotnet/game/Breakout.Game/Models/Brick.cs`
- `dotnet/game/Breakout.Game/Systems/RenderSystem.cs`

---

Keeps scope visual-only to ensure small, quick wins for the Coding Agent.
