namespace Breakout.Game.Models;

/// <summary>
/// Represents the ball in the Breakout game
/// </summary>
public class Ball
{
    /// <summary>
    /// Current horizontal position
    /// </summary>
    public int X { get; set; }
    
    /// <summary>
    /// Current vertical position
    /// </summary>
    public int Y { get; set; }
    
    /// <summary>
    /// Horizontal velocity (-1, 0, or 1)
    /// </summary>
    public int DeltaX { get; set; }
    
    /// <summary>
    /// Vertical velocity (-1, 0, or 1)
    /// </summary>
    public int DeltaY { get; set; }
    
    /// <summary>
    /// Visual representation
    /// </summary>
    public char Character { get; set; }
    
    /// <summary>
    /// Whether ball is in play
    /// </summary>
    public bool IsActive { get; set; }
    
    /// <summary>
    /// Initializes a new ball
    /// </summary>
    public Ball()
    {
        Character = '●';
        IsActive = true;
    }
    
    /// <summary>
    /// Move the ball by its current velocity
    /// </summary>
    public void Move()
    {
        X += DeltaX;
        Y += DeltaY;
    }
    
    /// <summary>
    /// Bounce the ball in the specified direction
    /// </summary>
    /// <param name="direction">Direction to bounce</param>
    public void Bounce(BounceDirection direction)
    {
        switch (direction)
        {
            case BounceDirection.Horizontal:
                DeltaX = -DeltaX;
                break;
            case BounceDirection.Vertical:
                DeltaY = -DeltaY;
                break;
        }
    }
    
    /// <summary>
    /// Reset ball to starting position
    /// </summary>
    /// <param name="startX">Starting X position</param>
    /// <param name="startY">Starting Y position</param>
    public void Reset(int startX, int startY)
    {
        X = startX;
        Y = startY;
        IsActive = true;
    }
}

/// <summary>
/// Direction for ball bouncing
/// </summary>
public enum BounceDirection
{
    /// <summary>
    /// Bounce off left/right walls or paddle sides
    /// </summary>
    Horizontal,
    
    /// <summary>
    /// Bounce off top/bottom or paddle top
    /// </summary>
    Vertical
}