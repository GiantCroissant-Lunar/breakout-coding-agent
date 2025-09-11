# Game-RFC-004: Brick System

## Overview

**Objective**: Implement destructible brick layout with collision detection and scoring system to create the core Breakout gameplay experience.

**Priority**: High  
**Dependencies**: ✅ Game-RFC-001 (Console Game Shell), ✅ Game-RFC-003 (Ball Physics)  
**Estimated Implementation**: 2 days  

## Specifications

### **Core Requirements**

#### **Brick Object Model**
```csharp
public class Brick
{
    public int X { get; set; }           // Horizontal position
    public int Y { get; set; }           // Vertical position  
    public int Width { get; set; }       // Brick width (typically 6-8 chars)
    public int Height { get; set; }      // Brick height (typically 1-2 chars)
    public bool IsDestroyed { get; set; } // Whether brick is destroyed
    public BrickType Type { get; set; }  // Brick type for different values
    public char Character { get; set; }  // Visual representation
    public ConsoleColor Color { get; set; } // Brick color
    
    // Methods
    public void Destroy();
    public bool CheckCollision(Ball ball);
    public int GetPointValue();
}

public enum BrickType
{
    Standard = 1,    // 10 points
    Strong = 2,      // 20 points  
    Bonus = 3        // 50 points
}
```

#### **Brick Layout System**
```csharp
public class BrickLayout
{
    public List<Brick> Bricks { get; set; }
    public int Rows { get; set; }
    public int Columns { get; set; }
    public int StartX { get; set; }
    public int StartY { get; set; }
    
    // Layout methods
    public void GenerateStandardLayout();
    public void GeneratePatternLayout(LayoutPattern pattern);
    public List<Brick> GetActiveBricks();
    public bool AllBricksDestroyed();
}

public enum LayoutPattern
{
    Standard,        // Uniform rows of bricks
    Pyramid,         // Triangular pattern
    Checkerboard,    // Alternating pattern
    Rainbow          // Different colored rows
}
```

#### **System Integration**
- **File**: `dotnet/game/Breakout.Game/Models/Brick.cs`
- **Layout**: `dotnet/game/Breakout.Game/Models/BrickLayout.cs`
- **System**: `dotnet/game/Breakout.Game/Systems/BrickSystem.cs`
- **Collision**: Update `dotnet/game/Breakout.Game/Systems/CollisionSystem.cs`
- **Scoring**: `dotnet/game/Breakout.Game/Systems/ScoreSystem.cs`

### **Technical Implementation**

#### **Brick Layout Generation**
```csharp
public void GenerateStandardLayout()
{
    Bricks.Clear();
    
    int brickWidth = 6;
    int brickHeight = 1;
    int spacing = 1;
    int totalWidth = (brickWidth + spacing) * Columns - spacing;
    
    StartX = (Console.WindowWidth - totalWidth) / 2;
    StartY = 3; // Below top boundary
    
    for (int row = 0; row < Rows; row++)
    {
        for (int col = 0; col < Columns; col++)
        {
            var brick = new Brick
            {
                X = StartX + col * (brickWidth + spacing),
                Y = StartY + row * (brickHeight + spacing),
                Width = brickWidth,
                Height = brickHeight,
                IsDestroyed = false,
                Type = GetBrickTypeForRow(row),
                Character = '█',
                Color = GetColorForType(GetBrickTypeForRow(row))
            };
            
            Bricks.Add(brick);
        }
    }
}
```

#### **Brick Collision Detection**
```csharp
public class BrickSystem
{
    public Brick CheckBrickCollisions(Ball ball, List<Brick> bricks)
    {
        foreach (var brick in bricks.Where(b => !b.IsDestroyed))
        {
            if (brick.CheckCollision(ball))
            {
                return brick;
            }
        }
        return null;
    }
    
    public void HandleBrickCollision(Ball ball, Brick brick, ScoreSystem scoreSystem)
    {
        // Destroy brick
        brick.Destroy();
        
        // Add score
        scoreSystem.AddPoints(brick.GetPointValue());
        
        // Determine bounce direction based on collision side
        var bounceDirection = GetBounceDirection(ball, brick);
        ball.Bounce(bounceDirection);
        
        // Clear brick from display
        renderSystem.ClearBrick(brick);
    }
}
```

#### **Collision Side Detection**
```csharp
public BounceDirection GetBounceDirection(Ball ball, Brick brick)
{
    // Determine which side of brick was hit
    int ballCenterX = ball.X;
    int ballCenterY = ball.Y;
    int brickCenterX = brick.X + brick.Width / 2;
    int brickCenterY = brick.Y + brick.Height / 2;
    
    // Calculate relative position
    int deltaX = ballCenterX - brickCenterX;
    int deltaY = ballCenterY - brickCenterY;
    
    // Determine collision side based on angle
    if (Math.Abs(deltaX) > Math.Abs(deltaY))
    {
        // Hit from left or right side
        return BounceDirection.Horizontal;
    }
    else
    {
        // Hit from top or bottom
        return BounceDirection.Vertical;
    }
}
```

#### **Scoring System**
```csharp
public class ScoreSystem
{
    public int CurrentScore { get; private set; }
    public int HighScore { get; private set; }
    public int BricksDestroyed { get; private set; }
    
    public void AddPoints(int points)
    {
        CurrentScore += points;
        BricksDestroyed++;
        
        if (CurrentScore > HighScore)
        {
            HighScore = CurrentScore;
        }
    }
    
    public void Reset()
    {
        CurrentScore = 0;
        BricksDestroyed = 0;
    }
}
```

## Acceptance Criteria

### **Core Functionality**
- [ ] Brick class implemented with position, type, and collision properties
- [ ] BrickLayout generates organized brick patterns (rows and columns)
- [ ] Ball collision with bricks works correctly (detection and bouncing)
- [ ] Bricks disappear when hit by ball
- [ ] Score increases when bricks are destroyed
- [ ] Different brick types have different point values

### **Layout and Visual**
- [ ] Bricks arranged in organized grid pattern near top of screen
- [ ] Multiple rows of bricks with proper spacing
- [ ] Different brick types have distinct colors
- [ ] Destroyed bricks are properly cleared from display
- [ ] Brick layout fits within console window boundaries
- [ ] Visual design is clear and distinguishable

### **Physics Integration**
- [ ] Ball bounces correctly off bricks (appropriate direction)
- [ ] Collision detection works reliably for all brick positions
- [ ] Ball physics remain consistent after brick collisions
- [ ] Multiple brick collisions in rapid succession handled correctly
- [ ] Ball speed and behavior unaffected by brick destruction

### **Game Mechanics**
- [ ] Score display shows current points and destroyed brick count
- [ ] All bricks can be destroyed through normal gameplay
- [ ] Game recognizes when all bricks are destroyed (win condition)
- [ ] Scoring system tracks different point values correctly
- [ ] Performance maintained with full brick layout

### **Integration**
- [ ] No regression in existing Game-RFC functionality (001-003)
- [ ] Game loop maintains 60 FPS with brick system active
- [ ] Paddle and ball controls remain responsive
- [ ] Proper integration with existing collision system
- [ ] Memory usage remains reasonable with brick objects

### **Code Quality**
- [ ] Code follows project naming conventions
- [ ] Proper separation of concerns (models, systems, rendering)
- [ ] Constants used for layout configuration
- [ ] Clean integration with existing architecture

## Technical Notes

### **Configuration Constants**
Add to `Utilities/Constants.cs`:
```csharp
public static class BrickConstants
{
    public const int DefaultWidth = 6;
    public const int DefaultHeight = 1;
    public const int DefaultRows = 6;
    public const int DefaultColumns = 10;
    public const int SpacingX = 1;
    public const int SpacingY = 1;
    public const char DefaultCharacter = '█';
    
    // Point values
    public const int StandardPoints = 10;
    public const int StrongPoints = 20;
    public const int BonusPoints = 50;
    
    // Colors for brick types
    public static readonly ConsoleColor StandardColor = ConsoleColor.Cyan;
    public static readonly ConsoleColor StrongColor = ConsoleColor.Yellow;
    public static readonly ConsoleColor BonusColor = ConsoleColor.Red;
}
```

### **Brick Collision Algorithm**
```csharp
public bool CheckCollision(Ball ball)
{
    if (IsDestroyed) return false;
    
    // Rectangle collision detection
    return ball.X >= X && 
           ball.X < X + Width &&
           ball.Y >= Y && 
           ball.Y < Y + Height;
}
```

### **Rendering Optimization**
```csharp
public static void DrawBricks(List<Brick> bricks)
{
    foreach (var brick in bricks.Where(b => !b.IsDestroyed))
    {
        Console.SetCursorPosition(brick.X, brick.Y);
        Console.ForegroundColor = brick.Color;
        Console.Write(new string(brick.Character, brick.Width));
    }
    Console.ResetColor();
}

public static void ClearBrick(Brick brick)
{
    Console.SetCursorPosition(brick.X, brick.Y);
    Console.Write(new string(' ', brick.Width));
}
```

### **Win Condition Check**
```csharp
public bool CheckWinCondition(BrickLayout layout)
{
    return layout.GetActiveBricks().Count == 0;
}
```

### **Testing Guidance**
Manual testing should verify:
1. Brick layout displays correctly at game start
2. Ball bounces off bricks in correct directions
3. Bricks disappear when hit by ball
4. Score increases with appropriate values
5. All bricks can be destroyed
6. Win condition triggers when all bricks destroyed
7. Performance remains smooth with full brick layout

## Implementation Priority

**Critical Path**: This RFC completes the core Breakout gameplay. Players can now destroy bricks to score points and win the game.

**Next RFC**: Game-RFC-005 (Game State Management) will add menus, win/lose conditions, and complete game flow.

## Definition of Done

- All acceptance criteria checkboxes completed
- Code compiles without warnings
- Brick system works reliably with ball physics
- Scoring system functions correctly
- Win condition detection works
- No regression in existing functionality
- PR merged with proper issue reference
- Ready for Game-RFC-005 game state management

---

**Implementation Guide**: See `AGENTS.md` for detailed coding patterns and project structure guidelines.