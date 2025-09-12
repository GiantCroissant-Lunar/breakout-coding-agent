using Breakout.Game.Models;
using Breakout.Game.Utilities;
using System.Linq;

namespace Breakout.Game.Systems;

/// <summary>
/// Handles console rendering and display
/// </summary>
public static class RenderSystem
{
    /// <summary>
    /// Initializes the console for game rendering
    /// </summary>
    public static void InitializeConsole()
    {
        try
        {
            Console.WindowWidth = Constants.CONSOLE_WIDTH;
            Console.WindowHeight = Constants.CONSOLE_HEIGHT;
        }
        catch (PlatformNotSupportedException)
        {
            // Window resizing not supported on this platform, use default size
        }
        
        Console.CursorVisible = false;
        Console.BackgroundColor = Constants.BACKGROUND_COLOR;
        Console.ForegroundColor = Constants.FOREGROUND_COLOR;
        Console.Clear();
    }
    
    /// <summary>
    /// Clears the console screen
    /// </summary>
    public static void Clear()
    {
        Console.Clear();
    }
    
    /// <summary>
    /// Renders the current game state
    /// </summary>
    /// <param name="gameState">Current game state</param>
    public static void RenderFrame(GameState gameState)
    {
        Clear();
        
        switch (gameState)
        {
            case GameState.Menu:
                RenderMenu();
                break;
            case GameState.Playing:
                RenderGame();
                break;
            case GameState.Paused:
                RenderPaused();
                break;
            case GameState.GameOver:
                RenderGameOver();
                break;
            case GameState.Exiting:
                RenderExiting();
                break;
        }
    }
    
    /// <summary>
    /// Renders the main menu
    /// </summary>
    private static void RenderMenu()
    {
        Console.SetCursorPosition(25, 10);
        Console.WriteLine("🎮 BREAKOUT GAME 🎮");
        Console.SetCursorPosition(20, 12);
        Console.WriteLine("Press SPACE to start playing");
        Console.SetCursorPosition(25, 14);
        Console.WriteLine("Press ESC to exit");
        Console.SetCursorPosition(15, 20);
        Console.WriteLine("Use LEFT/RIGHT arrow keys to move paddle");
    }
    
    /// <summary>
    /// Renders the playing game state
    /// </summary>
    private static void RenderGame()
    {
        // Game objects will be rendered here by the main game loop
        // This method now just renders the UI elements
        Console.SetCursorPosition(25, 1);
        Console.WriteLine("Press ESC to exit | SPACE to pause");
    }
    
    /// <summary>
    /// Draws the score information on the screen
    /// </summary>
    /// <param name="scoreSystem">Score system to display</param>
    public static void DrawScore(ScoreSystem scoreSystem)
    {
        if (scoreSystem == null) return;
        
        // Draw score at top left
        Console.SetCursorPosition(2, 1);
        Console.ForegroundColor = ConsoleColor.White;
        Console.Write(scoreSystem.GetScoreDisplay());
        
        // Draw bricks destroyed next to score
        Console.SetCursorPosition(15, 1);
        Console.Write(scoreSystem.GetBricksDestroyedDisplay());
        
        Console.ResetColor();
    }
    
    /// <summary>
    /// Renders the paused game state
    /// </summary>
    private static void RenderPaused()
    {
        Console.SetCursorPosition(32, 10);
        Console.WriteLine("⏸️ PAUSED ⏸️");
        Console.SetCursorPosition(25, 12);
        Console.WriteLine("Press SPACE to resume");
        Console.SetCursorPosition(25, 14);
        Console.WriteLine("Press ESC to exit");
    }
    
    /// <summary>
    /// Renders the game over state
    /// </summary>
    private static void RenderGameOver()
    {
        Console.SetCursorPosition(30, 10);
        Console.WriteLine("💀 GAME OVER 💀");
        Console.SetCursorPosition(25, 12);
        Console.WriteLine("Press SPACE to restart");
        Console.SetCursorPosition(25, 14);
        Console.WriteLine("Press ESC to exit");
    }
    
    /// <summary>
    /// Renders the exiting state
    /// </summary>
    private static void RenderExiting()
    {
        Console.SetCursorPosition(30, 10);
        Console.WriteLine("👋 Goodbye! 👋");
        Console.SetCursorPosition(25, 12);
        Console.WriteLine("Thanks for playing!");
    }
    
    /// <summary>
    /// Restores console to normal state
    /// </summary>
    public static void Cleanup()
    {
        Console.CursorVisible = true;
        Console.ResetColor();
        Console.Clear();
    }
    
    /// <summary>
    /// Draws a ball at its current position
    /// </summary>
    /// <param name="ball">Ball to draw</param>
    public static void DrawBall(Ball ball)
    {
        if (!ball.IsActive) return;
        
        Console.SetCursorPosition(ball.X, ball.Y);
        Console.ForegroundColor = BallConstants.DefaultColor;
        Console.Write(ball.Character);
        Console.ResetColor();
    }
    
    /// <summary>
    /// Clears a position on the screen
    /// </summary>
    /// <param name="x">X coordinate</param>
    /// <param name="y">Y coordinate</param>
    public static void ClearPosition(int x, int y)
    {
        if (x >= 0 && x < Console.WindowWidth && y >= 0 && y < Console.WindowHeight)
        {
            Console.SetCursorPosition(x, y);
            Console.Write(' ');
        }
    }
    
    /// <summary>
    /// Draws a paddle at its current position
    /// </summary>
    /// <param name="paddle">Paddle to draw</param>
    public static void DrawPaddle(Paddle paddle)
    {
        if (paddle == null) return;
        
        Console.SetCursorPosition(paddle.X, paddle.Y);
        Console.ForegroundColor = PaddleConstants.DefaultColor;
        Console.Write(new string(paddle.Character, paddle.Width));
        Console.ResetColor();
    }
    
    /// <summary>
    /// Clears a paddle from the screen
    /// </summary>
    /// <param name="paddle">Paddle to clear</param>
    public static void ClearPaddle(Paddle paddle)
    {
        if (paddle == null) return;
        
        Console.SetCursorPosition(paddle.X, paddle.Y);
        Console.Write(new string(' ', paddle.Width));
    }
    
    /// <summary>
    /// Draws all non-destroyed bricks efficiently
    /// </summary>
    /// <param name="bricks">List of bricks to render</param>
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
    
    /// <summary>
    /// Clears a destroyed brick from the screen
    /// </summary>
    /// <param name="brick">Brick to clear</param>
    public static void ClearBrick(Brick brick)
    {
        Console.SetCursorPosition(brick.X, brick.Y);
        Console.Write(new string(' ', brick.Width));
    }
}