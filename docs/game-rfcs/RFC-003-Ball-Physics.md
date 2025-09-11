# Game-RFC-003: Ball Physics

## Overview

**Objective**: Implement ball movement, bouncing mechanics, and collision detection with paddle and screen boundaries to create the core gameplay mechanics.

**Priority**: High  
**Dependencies**: ✅ Game-RFC-001 (Console Game Shell), ✅ Game-RFC-002 (Paddle Implementation)  
**Estimated Implementation**: 1-2 days  

## Specifications

### **Core Requirements**

#### **Ball Object Model**
```csharp
public class Ball
{
    public int X { get; set; }           // Current horizontal position
    public int Y { get; set; }           // Current vertical position
    public int DeltaX { get; set; }      // Horizontal velocity (-1, 0, or 1)
    public int DeltaY { get; set; }      // Vertical velocity (-1, 0, or 1)
    public char Character { get; set; }  // Visual representation ('●' recommended)
    public bool IsActive { get; set; }   // Whether ball is in play
    
    // Physics methods
    public void Move();
    public void Bounce(BounceDirection direction);
    public void Reset(int startX, int startY);
}

public enum BounceDirection
{
    Horizontal,  // Bounce off left/right walls or paddle sides
    Vertical     // Bounce off top/bottom or paddle top
}
```

#### **Ball System Integration**
- **File**: `dotnet/game/Breakout.Game/Models/Ball.cs`
- **System**: `dotnet/game/Breakout.Game/Systems/BallSystem.cs`
- **Collision**: `dotnet/game/Breakout.Game/Systems/CollisionSystem.cs`
- **Integration**: Update existing `Game.cs` to include ball physics

#### **Movement Mechanics**
- **Base Speed**: 1 character per frame at 60 FPS
- **Direction**: 8-directional movement (diagonal + cardinal)
- **Bouncing**: Reverse appropriate velocity component on collision
- **Ball Trail**: Clear previous position when moving

#### **Collision Detection**
```csharp
public class CollisionSystem
{
    public static bool CheckWallCollision(Ball ball, int screenWidth, int screenHeight);
    public static bool CheckPaddleCollision(Ball ball, Paddle paddle);
    public static PaddleCollisionType GetPaddleCollisionType(Ball ball, Paddle paddle);
}

public enum PaddleCollisionType
{
    None,
    Top,        // Ball hits top of paddle (normal bounce)
    Left,       // Ball hits left side (angle bounce)
    Right,      // Ball hits right side (angle bounce)
    Bottom      // Ball hits bottom (should not happen in normal play)
}
```

### **Technical Implementation**

#### **Ball Physics Loop**
```csharp
// In BallSystem.Update()
public void Update(Ball ball)
{
    if (!ball.IsActive) return;
    
    // Store previous position for clearing
    int prevX = ball.X;
    int prevY = ball.Y;
    
    // Move ball
    ball.Move();
    
    // Check wall collisions
    HandleWallCollisions(ball);
    
    // Check paddle collision
    HandlePaddleCollision(ball, paddle);
    
    // Clear previous position and render new position
    renderSystem.ClearPosition(prevX, prevY);
    renderSystem.DrawBall(ball);
}
```

#### **Wall Collision Logic**
```csharp
public void HandleWallCollisions(Ball ball)
{
    // Left and right walls
    if (ball.X <= 0 || ball.X >= Console.WindowWidth - 1)
    {
        ball.DeltaX = -ball.DeltaX;
        ball.X = Math.Clamp(ball.X, 1, Console.WindowWidth - 2);
    }
    
    // Top wall
    if (ball.Y <= 1)
    {
        ball.DeltaY = -ball.DeltaY;
        ball.Y = 2;
    }
    
    // Bottom wall (ball lost)
    if (ball.Y >= Console.WindowHeight - 1)
    {
        ball.IsActive = false;
        // Trigger ball lost event
    }
}
```

#### **Paddle Collision Logic**
```csharp
public void HandlePaddleCollision(Ball ball, Paddle paddle)
{
    if (!CheckPaddleCollision(ball, paddle)) return;
    
    var collisionType = GetPaddleCollisionType(ball, paddle);
    
    switch (collisionType)
    {
        case PaddleCollisionType.Top:
            ball.DeltaY = -Math.Abs(ball.DeltaY); // Always bounce up
            ball.Y = paddle.Y - 1; // Position just above paddle
            break;
            
        case PaddleCollisionType.Left:
            ball.DeltaX = -1; // Bounce left
            ball.DeltaY = -Math.Abs(ball.DeltaY); // And up
            break;
            
        case PaddleCollisionType.Right:
            ball.DeltaX = 1; // Bounce right  
            ball.DeltaY = -Math.Abs(ball.DeltaY); // And up
            break;
    }
}
```

## Acceptance Criteria

### **Core Functionality**
- [ ] Ball class implemented with position, velocity, and physics properties
- [ ] BallSystem handles movement, collision detection, and bouncing
- [ ] Ball moves smoothly in 8 directions (diagonal + cardinal)
- [ ] Ball bounces correctly off screen boundaries (left, right, top)
- [ ] Ball collision with paddle works correctly (top, left side, right side)
- [ ] Ball is removed/reset when it hits bottom boundary

### **Physics Behavior**
- [ ] Ball maintains consistent speed during movement
- [ ] Bouncing physics feel responsive and predictable
- [ ] Paddle collision affects ball direction appropriately
- [ ] Ball cannot get stuck or move outside boundaries
- [ ] Ball movement appears smooth without visual artifacts

### **Visual & UX**
- [ ] Ball appears as distinct character ('●' recommended)
- [ ] Ball has distinguishable color from paddle and background
- [ ] Previous ball position is properly cleared during movement
- [ ] Ball renders at correct position after collisions
- [ ] No screen flickering or visual glitches

### **Integration**
- [ ] No regression in existing Game-RFC-001 and Game-RFC-002 functionality
- [ ] Game loop maintains 60 FPS with ball physics
- [ ] Paddle controls remain responsive during ball movement
- [ ] Ball can be reset/respawned for new rounds
- [ ] Game state management handles ball loss appropriately

### **Code Quality**
- [ ] Code follows project naming conventions
- [ ] Proper separation of concerns (Ball model, BallSystem, CollisionSystem)
- [ ] Constants used for configurable values (speed, boundaries, etc.)
- [ ] Clean integration with existing systems

## Technical Notes

### **Configuration Constants**
Add to `Utilities/Constants.cs`:
```csharp
public static class BallConstants
{
    public const char DefaultCharacter = '●';
    public const int StartX = 40;  // Center of typical 80-char console
    public const int StartY = 20;  // Upper portion of screen
    public const int InitialDeltaX = 1;   // Start moving right
    public const int InitialDeltaY = 1;   // Start moving down
    public const ConsoleColor DefaultColor = ConsoleColor.White;
}
```

### **Collision Detection Algorithm**
```csharp
public static bool CheckPaddleCollision(Ball ball, Paddle paddle)
{
    // Simple rectangular collision detection
    return ball.X >= paddle.X && 
           ball.X < paddle.X + paddle.Width &&
           ball.Y >= paddle.Y && 
           ball.Y <= paddle.Y;
}

public static PaddleCollisionType GetPaddleCollisionType(Ball ball, Paddle paddle)
{
    if (!CheckPaddleCollision(ball, paddle)) return PaddleCollisionType.None;
    
    // Determine collision side based on ball's relative position
    int paddleCenter = paddle.X + paddle.Width / 2;
    int ballRelativePos = ball.X - paddleCenter;
    
    if (Math.Abs(ballRelativePos) < 2) return PaddleCollisionType.Top;
    return ballRelativePos < 0 ? PaddleCollisionType.Left : PaddleCollisionType.Right;
}
```

### **Testing Guidance**
Manual testing should verify:
1. Ball starts in center and moves diagonally down
2. Ball bounces off left, right, and top walls correctly
3. Ball bounces off paddle in expected directions
4. Ball is lost when hitting bottom boundary
5. Ball movement is smooth and consistent
6. No visual artifacts or position errors

## Implementation Priority

**Critical Path**: This RFC establishes the core gameplay mechanics. Without ball physics, the game cannot function as Breakout.

**Next RFC**: Game-RFC-004 (Brick System) will add destructible bricks that the ball can collide with for scoring.

## Definition of Done

- All acceptance criteria checkboxes completed
- Code compiles without warnings  
- Ball physics work smoothly and predictably
- Paddle collision behaves correctly
- No regression in existing functionality
- PR merged with proper issue reference
- Foundation ready for Game-RFC-004 brick collision

---

**Implementation Guide**: See `AGENTS.md` for detailed coding patterns and project structure guidelines.