namespace Breakout.Game.Models;

/// <summary>
/// Represents the paddle in the Breakout game
/// </summary>
public class Paddle
{
    /// <summary>
    /// Current horizontal position
    /// </summary>
    public int X { get; set; }
    
    /// <summary>
    /// Vertical position (typically near bottom)
    /// </summary>
    public int Y { get; set; }
    
    /// <summary>
    /// Paddle width in characters
    /// </summary>
    public int Width { get; set; }
    
    /// <summary>
    /// Visual representation
    /// </summary>
    public char Character { get; set; }
    
    /// <summary>
    /// Initializes a new paddle
    /// </summary>
    public Paddle()
    {
        Character = '█';
        Width = 8; // Default width
    }
}