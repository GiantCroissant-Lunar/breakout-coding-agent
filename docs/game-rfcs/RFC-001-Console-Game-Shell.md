# Game-RFC-001: Console Game Shell

**Status**: 📝 Draft - Ready to Implement  
**Priority**: Critical (Foundation)  
**Dependencies**: None  
**Estimated Time**: 1-2 days  
**Implementer**: GitHub Coding Agent

## 🎯 Problem Statement

Need a basic game framework with:
- Game loop for continuous execution
- Console setup and configuration
- Input handling system
- Frame rate control
- Clean exit mechanism

This provides the foundation for all other game features.

## 🎯 Goal

Create a working console game shell that can run continuously, handle player input, and provide the structure for adding game objects (paddle, ball, bricks).

## 📋 Acceptance Criteria

### **Core Game Loop**
- [ ] `Game` class with main game loop
- [ ] Loop runs continuously until exit condition
- [ ] Handles input processing each frame
- [ ] Updates game state each frame
- [ ] Renders current state each frame
- [ ] Frame rate limited to ~60 FPS

### **Console Setup**
- [ ] Console window configured (size: 80x25 minimum)
- [ ] Console colors configured (background/foreground)
- [ ] Cursor visibility disabled during gameplay
- [ ] Console buffer setup for smooth rendering

### **Input Handling**
- [ ] Non-blocking keyboard input detection
- [ ] Arrow key detection (Left/Right for paddle)
- [ ] Spacebar detection (for game start/pause)
- [ ] ESC key detection (for exit)
- [ ] Input processed each frame without blocking

### **Game States**
- [ ] `GameState` enum with basic states (Menu, Playing, Paused, Exiting)
- [ ] State transitions work correctly
- [ ] Different behavior for each state

### **Clean Architecture**
- [ ] Separation of concerns (input/update/render)
- [ ] Easy to extend for adding game objects
- [ ] No hardcoded values (use constants)

## 🛠️ Technical Implementation

### **File Structure**
Create these files in `dotnet/game/Breakout.Game/`:

```
├── Program.cs              # Entry point, creates and runs Game
├── Game.cs                 # Main game class with game loop
├── Models/
│   └── GameState.cs        # Game state enum
├── Systems/
│   ├── InputSystem.cs      # Handle keyboard input
│   └── RenderSystem.cs     # Handle console rendering
└── Utilities/
    └── Constants.cs        # Game constants (sizes, speeds, etc.)
```

### **Core Classes**

#### **Game.cs**
```csharp
public class Game
{
    public GameState State { get; set; }
    public bool IsRunning { get; set; }
    
    public void Initialize()
    {
        // Setup console, initialize systems
    }
    
    public void Run()
    {
        Initialize();
        while (IsRunning)
        {
            ProcessInput();
            Update();
            Render();
            Thread.Sleep(16); // ~60 FPS
        }
        Cleanup();
    }
    
    private void ProcessInput() { }
    private void Update() { }
    private void Render() { }
    private void Cleanup() { }
}
```

#### **GameState.cs**
```csharp
public enum GameState
{
    Menu,
    Playing,
    Paused,
    GameOver,
    Exiting
}
```

### **Console Configuration**
```csharp
// Console setup example
Console.WindowWidth = 80;
Console.WindowHeight = 25;
Console.CursorVisible = false;
Console.BackgroundColor = ConsoleColor.Black;
Console.ForegroundColor = ConsoleColor.White;
Console.Clear();
```

### **Input System Example**
```csharp
public static class InputSystem
{
    public static ConsoleKeyInfo? GetInput()
    {
        if (Console.KeyAvailable)
        {
            return Console.ReadKey(true);
        }
        return null;
    }
    
    public static bool IsExitRequested(ConsoleKeyInfo? key)
    {
        return key?.Key == ConsoleKey.Escape;
    }
}
```

## 🧪 Testing Requirements

### **Manual Testing Checklist**
- [ ] Game starts and shows initial state
- [ ] ESC key exits the game cleanly
- [ ] Game loop runs smoothly (no flickering)
- [ ] Input is responsive
- [ ] No exceptions or crashes during normal operation

### **Demo Requirements**
When complete, the game should:
1. Start with a clear console window
2. Show a simple message (e.g., "Press SPACE to start, ESC to exit")
3. Respond to SPACE key (change message or state)
4. Exit cleanly when ESC is pressed
5. Run without consuming excessive CPU

## ✅ Definition of Done

Game-RFC-001 is complete when:
- [ ] All acceptance criteria checkboxes are met
- [ ] Code compiles without warnings
- [ ] Game runs and exits cleanly
- [ ] Code follows project conventions (see AGENTS.md)
- [ ] Ready for Game-RFC-002 (Paddle) implementation
- [ ] PR merged to main branch

## 🔗 Integration Points

### **For Future RFCs**
This RFC provides:
- Game loop structure for adding game objects
- Input system for paddle control
- Render system for drawing game elements
- State management for game flow

### **Next RFC Dependencies**
- **Game-RFC-002 (Paddle)** will extend the input system
- **Game-RFC-003 (Ball)** will use the update/render cycle
- **Game-RFC-005 (Game States)** will extend the state system

---

**Start with this RFC - it's the foundation for everything else!**