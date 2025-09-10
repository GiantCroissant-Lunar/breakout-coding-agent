# 🤖 GitHub Copilot Coding Agent Instructions

## Project Overview
You are implementing a classic Breakout game in .NET 8. This project uses a validated workflow where Flow RFCs (handled by local agents) have solved the PR merge cycle, and you focus purely on game implementation.

## 🎮 Game Architecture

### **Simple Console-Based Approach**
- Use .NET 8 Console Application
- ASCII/Unicode characters for graphics
- Console.SetCursorPosition for animation
- Console.ReadKey for input handling

### **Core Game Objects**
```csharp
public class Game
{
    public GameState State { get; set; }
    public Paddle Paddle { get; set; }
    public Ball Ball { get; set; }
    public List<Brick> Bricks { get; set; }
    public int Score { get; set; }
}

public class Paddle
{
    public int X { get; set; }
    public int Y { get; set; }
    public int Width { get; set; }
}

public class Ball
{
    public int X { get; set; }
    public int Y { get; set; }
    public int DeltaX { get; set; }
    public int DeltaY { get; set; }
}

public class Brick
{
    public int X { get; set; }
    public int Y { get; set; }
    public bool IsDestroyed { get; set; }
}
```

## 📋 Code Standards

### **Naming Conventions**
- **Namespaces**: `Breakout.Game.{System}`
- **Classes**: PascalCase, descriptive names
- **Methods**: PascalCase, verb-based names
- **Variables**: camelCase for local, PascalCase for properties

### **File Organization**
```
dotnet/game/Breakout.Game/
├── Program.cs         # Entry point and game loop
├── Models/           # Game objects (Paddle, Ball, Brick)
├── Systems/          # Game logic (Physics, Collision, Rendering)
└── Utilities/        # Helpers (Input, Display)
```

## 📋 Available RFCs

### **Where to Find RFCs**
All Game RFCs are located in: `docs/game-rfcs/`

Check the README in that folder for:
- Current RFC status (Draft/Ready/In Progress/Complete)
- Dependency requirements
- Implementation priority

### **RFC Assignment Process**

**Before starting any RFC**:
1. **Check `docs/game-rfcs/README.md`** for available RFCs
2. **Read the specific RFC document** completely
3. **Verify dependencies** are met (previous RFCs completed)
4. **Create GitHub issue** with title: `Implement Game-RFC-XXX: [Feature Name]`
5. **Assign the issue to yourself**

### **Current Game RFCs Available**

**📋 Quick Reference** (See `docs/game-rfcs/` for full specifications):

1. **Game-RFC-001: Console Game Shell** - Basic game loop and structure
2. **Game-RFC-002: Paddle Implementation** - Player-controlled paddle
3. **Game-RFC-003: Ball Physics** - Ball movement and bouncing
4. **Game-RFC-004: Brick System** - Brick layout and collision
5. **Game-RFC-005: Game State Management** - Menus and win/lose conditions

### **Implementation Order**
RFCs should typically be implemented in order (001 → 002 → 003 → etc.) unless the RFC documentation specifically states otherwise.

## 🔧 Technical Guidelines

### **Console Rendering**
```csharp
// Example rendering pattern
public static void DrawPaddle(Paddle paddle)
{
    Console.SetCursorPosition(paddle.X, paddle.Y);
    Console.Write(new string('█', paddle.Width));
}

public static void DrawBall(Ball ball)
{
    Console.SetCursorPosition(ball.X, ball.Y);
    Console.Write('●');
}
```

### **Input Handling**
```csharp
// Example input pattern
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
```

### **Game Loop Pattern**
```csharp
while (game.State == GameState.Playing)
{
    HandleInput();
    UpdateGame();
    RenderFrame();
    Thread.Sleep(16); // ~60 FPS
}
```

## ✅ Definition of Done

Each Game-RFC is complete when:
- [ ] All acceptance criteria checkboxes are met
- [ ] Code compiles without warnings
- [ ] Game feature works as specified
- [ ] Code follows project naming conventions
- [ ] Feature integrates with existing systems

## 🚫 Important Constraints

### **Scope Limitations**
- **ONLY** implement the specific Game-RFC assigned
- **DO NOT** work on multiple Game-RFCs simultaneously
- **DO NOT** modify Flow-RFC related files
- **DO NOT** change existing working features

### **Keep It Simple**
- No complex graphics libraries
- No external game engines
- No network or multiplayer features
- No save/load functionality (unless specified in Game-RFC)

## 🔄 Workflow

### **Branch Naming**
- Use `copilot/game-rfc-XXX-description` format
- Example: `copilot/game-rfc-001-console-shell`

### **PR Requirements**
- **Title**: `Implement Game-RFC-XXX: [Feature Name]`
- **Body**: Include checklist of acceptance criteria
- Reference the Game-RFC specification
- Demonstrate feature working in console

### **Testing**
- Manual testing in console
- Verify feature works as specified
- Ensure no regression in existing features

## 🎮 Success Criteria

The project succeeds when:
- All 5 Game-RFCs are implemented
- Game is playable from start to finish
- Player can control paddle, bounce ball, destroy bricks
- Score tracking and win/lose conditions work
- Clean, readable code following conventions

---

**Remember**: Focus on game implementation only. Flow RFCs handle the workflow - your job is making a fun, playable Breakout game!