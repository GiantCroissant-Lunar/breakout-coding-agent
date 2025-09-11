# Game-RFC-002: Paddle Implementation

## Overview

**Objective**: Implement a player-controlled paddle that can move horizontally at the bottom of the screen, providing the foundation for ball interaction in subsequent RFCs.

**Priority**: High  
**Dependencies**: ✅ Game-RFC-001 (Console Game Shell)  
**Estimated Implementation**: 1 day  

## Specifications

### **Core Requirements**

#### **Paddle Object Model**
```csharp
public class Paddle
{
    public int X { get; set; }           // Current horizontal position
    public int Y { get; set; }           // Vertical position (typically near bottom)
    public int Width { get; set; }       // Paddle width in characters
    public char Character { get; set; }  // Visual representation ('█' recommended)
    
    // Movement methods
    public void MoveLeft();
    public void MoveRight();
    public bool CanMoveLeft();
    public bool CanMoveRight();
}
```

#### **Paddle System Integration**
- **File**: `dotnet/game/Breakout.Game/Models/Paddle.cs`
- **System**: `dotnet/game/Breakout.Game/Systems/PaddleSystem.cs`
- **Integration**: Update existing `Game.cs` to include paddle management

#### **Movement Controls**
- **Left Arrow**: Move paddle left
- **Right Arrow**: Move paddle right  
- **Movement Speed**: 1-2 characters per input
- **Boundary Checking**: Prevent paddle from moving outside console window

#### **Visual Requirements**
- **Position**: Bottom portion of screen (Y = Console window height - 3)
- **Width**: 8 characters wide (configurable via Constants)
- **Character**: Use '█' (block character) for solid appearance
- **Color**: Bright color to distinguish from background

### **Technical Implementation**

#### **Console Integration**
```csharp
// Example paddle rendering
public static void DrawPaddle(Paddle paddle)
{
    Console.SetCursorPosition(paddle.X, paddle.Y);
    Console.ForegroundColor = ConsoleColor.Cyan;
    Console.Write(new string(paddle.Character, paddle.Width));
    Console.ResetColor();
}

// Example paddle clearing (for movement)
public static void ClearPaddle(Paddle paddle)
{
    Console.SetCursorPosition(paddle.X, paddle.Y);
    Console.Write(new string(' ', paddle.Width));
}
```

#### **Input Handling Enhancement**
Extend existing `InputSystem.cs` to handle paddle movement:
```csharp
// Add to existing input processing
if (key.Key == ConsoleKey.LeftArrow && paddle.CanMoveLeft())
{
    paddleSystem.MoveLeft();
}
else if (key.Key == ConsoleKey.RightArrow && paddle.CanMoveRight())
{
    paddleSystem.MoveRight();
}
```

#### **Game Loop Integration**
Update the main game loop in `Game.cs`:
```csharp
// Add to Update() method
paddleSystem.Update(paddle);

// Add to Render() method  
renderSystem.DrawPaddle(paddle);
```

## Acceptance Criteria

### **Core Functionality**
- [ ] Paddle class implemented with position and movement properties
- [ ] PaddleSystem class handles movement logic and boundary checking
- [ ] Left/Right arrow keys control paddle movement smoothly
- [ ] Paddle cannot move outside console window boundaries
- [ ] Paddle renders correctly at bottom of screen with visible character

### **Visual & UX**
- [ ] Paddle appears as solid block using '█' character
- [ ] Paddle has distinct color (suggested: Cyan)
- [ ] Movement is smooth without visual artifacts
- [ ] Previous paddle position is properly cleared when moving
- [ ] Paddle remains visible and positioned correctly at all times

### **Integration**
- [ ] No regression in existing Game-RFC-001 functionality
- [ ] Game loop maintains 60 FPS with paddle updates
- [ ] Input system properly integrates paddle controls
- [ ] Console rendering system includes paddle drawing
- [ ] Game state management remains functional

### **Code Quality**
- [ ] Code follows project naming conventions (PascalCase classes, camelCase variables)
- [ ] Proper file organization under Models/ and Systems/ folders
- [ ] Constants used for configurable values (paddle width, position, etc.)
- [ ] Clean separation of concerns (model, system, rendering)

## Technical Notes

### **Configuration Constants**
Add to `Utilities/Constants.cs`:
```csharp
public static class PaddleConstants
{
    public const int DefaultWidth = 8;
    public const char DefaultCharacter = '█';
    public const int MovementSpeed = 2;
    public const ConsoleColor DefaultColor = ConsoleColor.Cyan;
}
```

### **Boundary Logic**
```csharp
public bool CanMoveLeft() => X > 0;
public bool CanMoveRight() => X + Width < Console.WindowWidth;

public void MoveLeft()
{
    if (CanMoveLeft())
        X = Math.Max(0, X - MovementSpeed);
}

public void MoveRight()  
{
    if (CanMoveRight())
        X = Math.Min(Console.WindowWidth - Width, X + MovementSpeed);
}
```

### **Testing Guidance**
Manual testing should verify:
1. Paddle appears at bottom of screen on game start
2. Left arrow moves paddle left until left boundary
3. Right arrow moves paddle right until right boundary  
4. No visual artifacts or screen flicker during movement
5. Paddle position resets properly when returning to menu

## Implementation Priority

**Critical Path**: This RFC is essential for Game-RFC-003 (Ball Physics) as the ball will need to interact with the paddle for bouncing mechanics.

**Next RFC**: Game-RFC-003 will add ball physics and paddle collision detection, building on this foundation.

## Definition of Done

- All acceptance criteria checkboxes completed
- Code compiles without warnings
- Manual testing confirms smooth paddle movement
- No regression in existing game functionality  
- PR merged with proper issue reference
- Foundation ready for Game-RFC-003 ball interaction

---

**Implementation Guide**: See `AGENTS.md` for detailed coding patterns and project structure guidelines.