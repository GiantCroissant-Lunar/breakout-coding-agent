using Breakout.Game.Utilities;

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
    
    /// <summary>
    /// Checks if the paddle can move left without going out of bounds
    /// </summary>
    /// <returns>True if paddle can move left</returns>
    public bool CanMoveLeft()
    {
        return X > 0;
    }
    
    /// <summary>
    /// Checks if the paddle can move right without going out of bounds
    /// </summary>
    /// <returns>True if paddle can move right</returns>
    public bool CanMoveRight()
    {
        return X + Width < Constants.CONSOLE_WIDTH;
    }
    
    /// <summary>
    /// Moves the paddle left while respecting left boundary
    /// </summary>
    public void MoveLeft()
    {
        if (CanMoveLeft())
        {
            X = Math.Max(0, X - PaddleConstants.MovementSpeed);
        }
    }
    
    /// <summary>
    /// Moves the paddle right while respecting right boundary
    /// </summary>
    public void MoveRight()
    {
        if (CanMoveRight())
        {
            X = Math.Min(Constants.CONSOLE_WIDTH - Width, X + PaddleConstants.MovementSpeed);
        }
    }
}