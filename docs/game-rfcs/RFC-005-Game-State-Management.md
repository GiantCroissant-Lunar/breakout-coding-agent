# Game-RFC-005: Game State Management

## Overview

**Objective**: Implement complete game flow with menus, win/lose conditions, game over handling, and state transitions to create a fully playable Breakout game.

**Priority**: Medium  
**Dependencies**: ✅ Game-RFC-001 (Console Game Shell), ✅ Game-RFC-002 (Paddle), ✅ Game-RFC-003 (Ball Physics), ✅ Game-RFC-004 (Brick System)  
**Estimated Implementation**: 1-2 days  

## Specifications

### **Core Requirements**

#### **Enhanced Game State Model**
```csharp
public enum GameState
{
    MainMenu,        // Initial menu screen
    Playing,         // Active gameplay
    Paused,          // Game paused
    GameOver,        // Player lost (ball fell)
    Victory,         // Player won (all bricks destroyed)
    HighScore,       // High score display
    Instructions,    // How to play screen
    Exiting         // Preparing to exit
}

public class GameSession
{
    public GameState State { get; set; }
    public int Lives { get; set; }
    public int Level { get; set; }
    public DateTime StartTime { get; set; }
    public bool IsNewGame { get; set; }
    
    // Session methods
    public void StartNewGame();
    public void LoseLife();
    public void CompleteLevel();
    public void GameOver();
    public void Victory();
}
```

#### **Menu System**
```csharp
public class MenuSystem
{
    public MenuItem[] MainMenuItems { get; set; }
    public int SelectedIndex { get; set; }
    
    public void RenderMainMenu();
    public void RenderInstructions();
    public void RenderGameOver();
    public void RenderVictory();
    public void RenderHighScore();
    public void HandleMenuInput(ConsoleKeyInfo key);
}

public class MenuItem
{
    public string Text { get; set; }
    public Action Action { get; set; }
    public bool IsEnabled { get; set; }
}
```

#### **Lives and Game Over System**
```csharp
public class LivesSystem
{
    public int CurrentLives { get; private set; }
    public int StartingLives { get; set; } = 3;
    
    public void Reset();
    public bool LoseLife();
    public bool HasLivesRemaining();
    public void DisplayLives();
}
```

### **Technical Implementation**

#### **State Management**
```csharp
public class Game
{
    private GameSession session;
    private MenuSystem menuSystem;
    private LivesSystem livesSystem;
    
    public void HandleStateTransition(GameState newState)
    {
        var previousState = session.State;
        session.State = newState;
        
        switch (newState)
        {
            case GameState.MainMenu:
                InitializeMainMenu();
                break;
                
            case GameState.Playing:
                if (previousState == GameState.MainMenu)
                    StartNewGame();
                else
                    ResumeGame();
                break;
                
            case GameState.GameOver:
                HandleGameOver();
                break;
                
            case GameState.Victory:
                HandleVictory();
                break;
                
            case GameState.Paused:
                DisplayPauseMenu();
                break;
        }
    }
}
```

#### **Main Menu Implementation**
```csharp
public void RenderMainMenu()
{
    Console.Clear();
    Console.SetCursorPosition(0, 0);
    
    // Title
    Console.ForegroundColor = ConsoleColor.Cyan;
    Console.WriteLine(centerText("🎮 BREAKOUT GAME 🎮"));
    Console.WriteLine();
    
    // Menu options
    var menuItems = new[]
    {
        "1. New Game",
        "2. Instructions", 
        "3. High Scores",
        "4. Exit"
    };
    
    for (int i = 0; i < menuItems.Length; i++)
    {
        if (i == SelectedIndex)
        {
            Console.BackgroundColor = ConsoleColor.Gray;
            Console.ForegroundColor = ConsoleColor.Black;
        }
        else
        {
            Console.ResetColor();
        }
        
        Console.WriteLine(centerText(menuItems[i]));
    }
    
    Console.ResetColor();
    Console.WriteLine();
    Console.WriteLine(centerText("Use arrow keys to navigate, Enter to select"));
}
```

#### **Game Over and Victory Screens**
```csharp
public void RenderGameOver()
{
    Console.Clear();
    Console.ForegroundColor = ConsoleColor.Red;
    
    Console.WriteLine(centerText("💥 GAME OVER 💥"));
    Console.WriteLine();
    Console.WriteLine(centerText($"Final Score: {scoreSystem.CurrentScore}"));
    Console.WriteLine(centerText($"Bricks Destroyed: {scoreSystem.BricksDestroyed}"));
    Console.WriteLine();
    Console.WriteLine(centerText("Press SPACE to play again"));
    Console.WriteLine(centerText("Press ESC to return to menu"));
}

public void RenderVictory()
{
    Console.Clear();
    Console.ForegroundColor = ConsoleColor.Green;
    
    Console.WriteLine(centerText("🎉 VICTORY! 🎉"));
    Console.WriteLine();
    Console.WriteLine(centerText("All bricks destroyed!"));
    Console.WriteLine(centerText($"Final Score: {scoreSystem.CurrentScore}"));
    Console.WriteLine(centerText($"Time: {GetGameDuration()}"));
    Console.WriteLine();
    Console.WriteLine(centerText("Press SPACE to play again"));
    Console.WriteLine(centerText("Press ESC to return to menu"));
}
```

#### **Lives and Ball Reset System**
```csharp
public void HandleBallLost()
{
    // Ball fell off bottom of screen
    bool hasLives = livesSystem.LoseLife();
    
    if (hasLives)
    {
        // Reset ball and paddle for next life
        ball.Reset(BallConstants.StartX, BallConstants.StartY);
        paddle.Reset();
        
        // Brief pause before resuming
        DisplayLifeLostMessage();
        Thread.Sleep(2000);
        
        // Continue playing
        session.State = GameState.Playing;
    }
    else
    {
        // No lives remaining
        session.State = GameState.GameOver;
    }
}

public void DisplayLifeLostMessage()
{
    Console.SetCursorPosition(0, Console.WindowHeight / 2);
    Console.ForegroundColor = ConsoleColor.Yellow;
    Console.WriteLine(centerText($"Life Lost! Lives remaining: {livesSystem.CurrentLives}"));
    Console.WriteLine(centerText("Press SPACE to continue"));
    Console.ResetColor();
}
```

#### **Instructions Screen**
```csharp
public void RenderInstructions()
{
    Console.Clear();
    Console.ForegroundColor = ConsoleColor.Cyan;
    
    Console.WriteLine(centerText("📋 HOW TO PLAY"));
    Console.WriteLine();
    Console.ResetColor();
    
    var instructions = new[]
    {
        "🎯 OBJECTIVE: Destroy all bricks by bouncing the ball with your paddle",
        "",
        "🎮 CONTROLS:",
        "   ← → Arrow Keys: Move paddle left and right",
        "   SPACE: Pause/Resume game",
        "   ESC: Return to main menu",
        "",
        "📊 SCORING:",
        "   Standard Bricks (Cyan): 10 points",
        "   Strong Bricks (Yellow): 20 points", 
        "   Bonus Bricks (Red): 50 points",
        "",
        "❤️ LIVES: You start with 3 lives",
        "   Lose a life when the ball falls off the bottom",
        "   Game over when all lives are lost",
        "",
        "🏆 WIN: Destroy all bricks to complete the level!"
    };
    
    foreach (var line in instructions)
    {
        Console.WriteLine(centerText(line));
    }
    
    Console.WriteLine();
    Console.WriteLine(centerText("Press any key to return to menu"));
}
```

## Acceptance Criteria

### **Core State Management**
- [ ] Complete game state enum with all necessary states
- [ ] State transitions work correctly between all states
- [ ] Game session tracks lives, level, and timing
- [ ] Menu system with navigation and selection
- [ ] Proper game initialization and cleanup

### **Menu System**
- [ ] Main menu with New Game, Instructions, High Scores, Exit options
- [ ] Arrow key navigation with visual selection indicator
- [ ] Instructions screen with clear game controls and objectives
- [ ] High score display (even if simple)
- [ ] Proper return navigation from all menu screens

### **Game Flow**
- [ ] New game starts with full lives and fresh brick layout
- [ ] Ball loss properly decrements lives and resets ball/paddle
- [ ] Game over triggers when lives reach zero
- [ ] Victory triggers when all bricks are destroyed
- [ ] Pause functionality works during gameplay
- [ ] Clean exit from any state

### **Lives System**
- [ ] Player starts with configurable number of lives (default 3)
- [ ] Lives display shows current count during gameplay
- [ ] Life loss triggers proper ball/paddle reset
- [ ] Life lost message displays temporarily
- [ ] Game over handled when no lives remain

### **Visual Polish**
- [ ] All screens have consistent visual design
- [ ] Clear navigation instructions on each screen
- [ ] Proper use of colors for different game states
- [ ] Score and lives display during gameplay
- [ ] No visual artifacts during state transitions

### **Integration**
- [ ] No regression in existing Game-RFC functionality (001-004)
- [ ] All game systems work together seamlessly
- [ ] Performance maintained across all game states
- [ ] Memory management proper during state transitions
- [ ] Complete, playable Breakout game experience

### **Code Quality**
- [ ] Code follows project naming conventions
- [ ] State management follows clear patterns
- [ ] Proper separation of concerns for different systems
- [ ] Constants used for configurable game parameters

## Technical Notes

### **Configuration Constants**
Add to `Utilities/Constants.cs`:
```csharp
public static class GameConstants
{
    public const int DefaultLives = 3;
    public const int MenuSelectionDelay = 150; // ms
    public const int LifeLostDisplayTime = 2000; // ms
    public const int VictoryDisplayTime = 3000; // ms
    
    // Menu colors
    public static readonly ConsoleColor MenuTitleColor = ConsoleColor.Cyan;
    public static readonly ConsoleColor MenuSelectedColor = ConsoleColor.Yellow;
    public static readonly ConsoleColor MenuNormalColor = ConsoleColor.White;
    
    // Game state colors
    public static readonly ConsoleColor GameOverColor = ConsoleColor.Red;
    public static readonly ConsoleColor VictoryColor = ConsoleColor.Green;
    public static readonly ConsoleColor PauseColor = ConsoleColor.Yellow;
}
```

### **State Transition Matrix**
```csharp
private static readonly Dictionary<(GameState from, GameState to), bool> ValidTransitions = 
    new Dictionary<(GameState, GameState), bool>
{
    { (GameState.MainMenu, GameState.Playing), true },
    { (GameState.MainMenu, GameState.Instructions), true },
    { (GameState.MainMenu, GameState.HighScore), true },
    { (GameState.MainMenu, GameState.Exiting), true },
    { (GameState.Playing, GameState.Paused), true },
    { (GameState.Playing, GameState.GameOver), true },
    { (GameState.Playing, GameState.Victory), true },
    { (GameState.Playing, GameState.MainMenu), true },
    { (GameState.Paused, GameState.Playing), true },
    { (GameState.Paused, GameState.MainMenu), true },
    { (GameState.GameOver, GameState.MainMenu), true },
    { (GameState.GameOver, GameState.Playing), true },
    { (GameState.Victory, GameState.MainMenu), true },
    { (GameState.Victory, GameState.Playing), true },
    // Add other valid transitions...
};
```

### **Text Centering Utility**
```csharp
private string centerText(string text)
{
    int windowWidth = Console.WindowWidth;
    int padding = Math.Max(0, (windowWidth - text.Length) / 2);
    return new string(' ', padding) + text;
}
```

### **Testing Guidance**
Manual testing should verify:
1. All menu navigation works correctly
2. New game starts with proper initialization
3. Lives system decrements and resets correctly
4. Game over triggers at appropriate time
5. Victory triggers when all bricks destroyed
6. Pause/resume functionality works
7. State transitions are smooth and correct
8. Instructions screen is helpful and clear

## Implementation Priority

**Final RFC**: This completes the Breakout game implementation. After this RFC, the game should be fully playable from start to finish.

**Success Criteria**: A complete, playable Breakout game that demonstrates GitHub Coding Agent's ability to implement a full project through automated workflows.

## Definition of Done

- All acceptance criteria checkboxes completed
- Code compiles without warnings
- Complete game flow from menu to gameplay to end states
- All game systems integrated and working together
- Fully playable Breakout game experience
- No regression in any previous Game-RFC functionality
- PR merged with proper issue reference
- **COMPLETE BREAKOUT GAME IMPLEMENTED**

---

**🎉 Project Completion**: This RFC represents the final step in the Breakout Coding Agent experiment, demonstrating successful automated development workflows using GitHub Coding Agent.**

**Implementation Guide**: See `AGENTS.md` for detailed coding patterns and project structure guidelines.