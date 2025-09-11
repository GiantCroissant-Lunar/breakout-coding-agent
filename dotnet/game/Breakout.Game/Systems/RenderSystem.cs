using Breakout.Game.Models;
using Breakout.Game.Utilities;

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
        Console.SetCursorPosition(10, 20);
        Console.WriteLine("Use LEFT/RIGHT arrow keys to move paddle (when implemented)");
    }
    
    /// <summary>
    /// Renders the playing game state
    /// </summary>
    private static void RenderGame()
    {
        Console.SetCursorPosition(30, 10);
        Console.WriteLine("🎮 GAME PLAYING 🎮");
        Console.SetCursorPosition(20, 12);
        Console.WriteLine("Game objects will appear here");
        Console.SetCursorPosition(25, 14);
        Console.WriteLine("Press ESC to exit");
        Console.SetCursorPosition(25, 16);
        Console.WriteLine("Press SPACE to pause");
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
}