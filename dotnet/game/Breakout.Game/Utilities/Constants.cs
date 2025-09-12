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

/// <summary>
/// Ball-related constants
/// </summary>
public static class BallConstants
{
    /// <summary>
    /// Default ball character
    /// </summary>
    public const char DefaultCharacter = '●';
    
    /// <summary>
    /// Starting X position (center of console)
    /// </summary>
    public const int StartX = 40;
    
    /// <summary>
    /// Starting Y position (upper portion)
    /// </summary>
    public const int StartY = 12;
    
    /// <summary>
    /// Initial horizontal velocity
    /// </summary>
    public const int InitialDeltaX = 1;
    
    /// <summary>
    /// Initial vertical velocity
    /// </summary>
    public const int InitialDeltaY = 1;
    
    /// <summary>
    /// Default ball color
    /// </summary>
    public const ConsoleColor DefaultColor = ConsoleColor.White;
}

/// <summary>
/// Paddle-related constants
/// </summary>
public static class PaddleConstants
{
    /// <summary>
    /// Default paddle width
    /// </summary>
    public const int DefaultWidth = 8;
    
    /// <summary>
    /// Default paddle character
    /// </summary>
    public const char DefaultCharacter = '█';
    
    /// <summary>
    /// Default paddle color
    /// </summary>
    public const ConsoleColor DefaultColor = ConsoleColor.Cyan;
    
    /// <summary>
    /// Paddle movement speed (characters per frame)
    /// </summary>
    public const int MovementSpeed = 1;
}

/// <summary>
/// Brick-related constants
/// </summary>
public static class BrickConstants
{
    /// <summary>
    /// Default brick width
    /// </summary>
    public const int DefaultWidth = 6;
    
    /// <summary>
    /// Default brick height
    /// </summary>
    public const int DefaultHeight = 1;
    
    /// <summary>
    /// Default number of brick rows
    /// </summary>
    public const int DefaultRows = 6;
    
    /// <summary>
    /// Default number of brick columns
    /// </summary>
    public const int DefaultColumns = 10;
    
    /// <summary>
    /// Horizontal spacing between bricks
    /// </summary>
    public const int SpacingX = 1;
    
    /// <summary>
    /// Vertical spacing between bricks
    /// </summary>
    public const int SpacingY = 1;
    
    /// <summary>
    /// Default brick character
    /// </summary>
    public const char DefaultCharacter = '█';
    
    /// <summary>
    /// Standard brick point value
    /// </summary>
    public const int StandardPoints = 10;
    
    /// <summary>
    /// Strong brick point value
    /// </summary>
    public const int StrongPoints = 20;
    
    /// <summary>
    /// Bonus brick point value
    /// </summary>
    public const int BonusPoints = 50;
    
    /// <summary>
    /// Standard brick color
    /// </summary>
    public static readonly ConsoleColor StandardColor = ConsoleColor.Cyan;
    
    /// <summary>
    /// Strong brick color
    /// </summary>
    public static readonly ConsoleColor StrongColor = ConsoleColor.Yellow;
    
    /// <summary>
    /// Bonus brick color
    /// </summary>
    public static readonly ConsoleColor BonusColor = ConsoleColor.Red;
}