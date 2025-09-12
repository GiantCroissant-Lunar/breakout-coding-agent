# Breakout Game – C# Style Guide

This style guide customizes Gemini Code Assist feedback for this repository.
It extends the .NET/C# conventions from Microsoft and emphasizes simplicity for a console game.

## Principles
- Readability: Prefer clear, explicit code over cleverness.
- Simplicity: Keep logic straightforward; avoid premature abstractions.
- Consistency: Follow the naming and folder conventions defined in project docs.

## Project Conventions
- Namespaces: `Breakout.Game.{System}` (e.g., `Breakout.Game.Systems`).
- Classes: PascalCase, descriptive (e.g., `Paddle`, `BallPhysicsSystem`).
- Methods: PascalCase, verb-based (e.g., `UpdateFrame`, `HandleInput`).
- Locals: camelCase; Properties/fields: PascalCase (public), `_camelCase` for private fields.
- Files/Folders:
  - `dotnet/game/Breakout.Game/Program.cs`
  - `dotnet/game/Breakout.Game/Models/*`
  - `dotnet/game/Breakout.Game/Systems/*`
  - `dotnet/game/Breakout.Game/Utilities/*`

## C# Coding Rules
- Target framework: .NET 8; use modern language features when they improve clarity.
- Brace style: Allman; always use braces for conditionals/loops.
- Null checks: Use pattern matching `is null`/`is not null`; avoid double negatives.
- Immutability: Prefer `readonly` where practical.
- LINQ: Fine for clarity; avoid complex chained queries in hot loops.
- Exceptions: Do not use exceptions for control flow; catch narrowly and handle/ log.
- Async: Not required for this console loop unless explicitly needed.

## Console Game Specifics
- Rendering: Use `Console.SetCursorPosition` and minimal allocations per frame.
- Timing: Aim ~60 FPS with `Thread.Sleep(16)`; keep per-frame work predictable.
- Input: Poll `Console.KeyAvailable` and `Console.ReadKey(true)` non-blocking.
- State: Keep `Game` state centralized; update in a consistent order: Input → Update → Render.

## Testing & Reviews – Focus Areas
- Collision correctness (paddle/ball/bricks) and bounds checks.
- No flicker: Erase/redraw order, cursor positioning, and buffer writes.
- Deterministic movement: Respect deltas, frame timing, and boundary reflection.
- Keep RFC scope: Only implement the active Game-RFC; do not bleed features across RFCs.

## Examples
```csharp
// Input
if (Console.KeyAvailable)
{
    var key = Console.ReadKey(true);
    switch (key.Key)
    {
        case ConsoleKey.LeftArrow:
            paddle.MoveLeft();
            break;
        case ConsoleKey.RightArrow:
            paddle.MoveRight();
            break;
    }
}

// Render
Console.SetCursorPosition(paddle.X, paddle.Y);
Console.Write(new string('█', paddle.Width));
```

## What to Avoid
- Introducing external graphics/game libraries.
- Large refactors that change file layout without RFC guidance.
- Excessive allocations or string concatenations inside the main loop.

