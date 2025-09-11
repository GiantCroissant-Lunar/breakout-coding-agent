# Game-RFC-009: Ball Wall Bounce Only

## Overview

Objective: Add basic wall-bounce physics for the ball (no paddle/bricks yet).

Priority: High  
Dependencies: Game-RFC-008 (Ball Render + Step)

## Scope (Reduced)
- Reverse `DeltaX` on hitting left/right edges
- Reverse `DeltaY` on hitting the top edge
- Do not handle bottom edge yet (no lose condition)
- Keep update loop ~60 FPS, avoid jitter/stuck states at edges

## Acceptance Criteria
- [ ] Ball bounces off left/right edges reliably
- [ ] Ball bounces off top edge reliably
- [ ] No jitter or stuck states when colliding with edges
- [ ] Code compiles without warnings
- [ ] Change is limited to Systems/Physics or equivalent and keeps concerns separated

## Technical Notes
- Ensure calculations clamp ball position inside bounds after a bounce to avoid “double flip” next frame
- Use `Console.WindowWidth/Console.WindowHeight` to determine bounds
- Keep update logic independent from rendering

## File Organization
- `dotnet/game/Breakout.Game/Systems/PhysicsSystem.cs` (or equivalent)
- `dotnet/game/Breakout.Game/Models/Ball.cs` (unchanged model members)

---

This is intentionally small so the Coding Agent can complete quickly and we can move on to brick interactions.
