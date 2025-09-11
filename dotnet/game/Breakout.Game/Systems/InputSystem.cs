namespace Breakout.Game.Systems;

/// <summary>
/// Handles non-blocking keyboard input detection
/// </summary>
public static class InputSystem
{
    /// <summary>
    /// Gets the next key press if available, without blocking
    /// </summary>
    /// <returns>ConsoleKeyInfo if key is available, null otherwise</returns>
    public static ConsoleKeyInfo? GetInput()
    {
        try
        {
            if (Console.KeyAvailable)
            {
                return Console.ReadKey(true);
            }
        }
        catch (InvalidOperationException)
        {
            // Console input might be redirected or unavailable
            // In this case, we can't use non-blocking input
            return null;
        }
        return null;
    }
    
    /// <summary>
    /// Checks if the exit key (ESC) was pressed
    /// </summary>
    /// <param name="key">The key to check</param>
    /// <returns>True if ESC was pressed</returns>
    public static bool IsExitRequested(ConsoleKeyInfo? key)
    {
        return key?.Key == ConsoleKey.Escape;
    }
    
    /// <summary>
    /// Checks if the left arrow key was pressed
    /// </summary>
    /// <param name="key">The key to check</param>
    /// <returns>True if left arrow was pressed</returns>
    public static bool IsLeftPressed(ConsoleKeyInfo? key)
    {
        return key?.Key == ConsoleKey.LeftArrow;
    }
    
    /// <summary>
    /// Checks if the right arrow key was pressed
    /// </summary>
    /// <param name="key">The key to check</param>
    /// <returns>True if right arrow was pressed</returns>
    public static bool IsRightPressed(ConsoleKeyInfo? key)
    {
        return key?.Key == ConsoleKey.RightArrow;
    }
    
    /// <summary>
    /// Checks if the spacebar was pressed
    /// </summary>
    /// <param name="key">The key to check</param>
    /// <returns>True if spacebar was pressed</returns>
    public static bool IsSpacePressed(ConsoleKeyInfo? key)
    {
        return key?.Key == ConsoleKey.Spacebar;
    }
}