namespace Breakout.Game.Utilities;

/// <summary>
/// Game constants and configuration values
/// </summary>
public static class Constants
{
    /// <summary>
    /// Target frames per second for the game loop
    /// </summary>
    public const int TARGET_FPS = 60;
    
    /// <summary>
    /// Milliseconds to sleep per frame to achieve target FPS
    /// </summary>
    public const int FRAME_DELAY_MS = 1000 / TARGET_FPS; // ~16ms
    
    /// <summary>
    /// Console window width
    /// </summary>
    public const int CONSOLE_WIDTH = 80;
    
    /// <summary>
    /// Console window height
    /// </summary>
    public const int CONSOLE_HEIGHT = 25;
    
    /// <summary>
    /// Console background color
    /// </summary>
    public const ConsoleColor BACKGROUND_COLOR = ConsoleColor.Black;
    
    /// <summary>
    /// Console foreground color
    /// </summary>
    public const ConsoleColor FOREGROUND_COLOR = ConsoleColor.White;
}