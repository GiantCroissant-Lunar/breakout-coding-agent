namespace Breakout.Game.Models;

/// <summary>
/// Represents a destructible brick in the Breakout game
/// </summary>
public class Brick
{
    /// <summary>
    /// Horizontal position
    /// </summary>
    public int X { get; set; }
    
    /// <summary>
    /// Vertical position
    /// </summary>
    public int Y { get; set; }
    
    /// <summary>
    /// Brick width (typically 6-8 chars)
    /// </summary>
    public int Width { get; set; }
    
    /// <summary>
    /// Brick height (typically 1-2 chars)
    /// </summary>
    public int Height { get; set; }
    
    /// <summary>
    /// Whether brick is destroyed
    /// </summary>
    public bool IsDestroyed { get; set; }
    
    /// <summary>
    /// Brick type for different values
    /// </summary>
    public BrickType Type { get; set; }
    
    /// <summary>
    /// Visual representation
    /// </summary>
    public char Character { get; set; }
    
    /// <summary>
    /// Brick color
    /// </summary>
    public ConsoleColor Color { get; set; }
    
    /// <summary>
    /// Initializes a new brick
    /// </summary>
    public Brick()
    {
        Character = '█';
        IsDestroyed = false;
        Type = BrickType.Standard;
        Color = ConsoleColor.Cyan;
    }
    
    /// <summary>
    /// Destroy the brick
    /// </summary>
    public void Destroy()
    {
        IsDestroyed = true;
    }
    
    /// <summary>
    /// Check collision with ball using rectangle collision detection
    /// </summary>
    /// <param name="ball">Ball to check collision with</param>
    /// <returns>True if collision detected</returns>
    public bool CheckCollision(Ball ball)
    {
        if (IsDestroyed) return false;
        
        // Rectangle collision detection
        return ball.X >= X && 
               ball.X < X + Width &&
               ball.Y >= Y && 
               ball.Y < Y + Height;
    }
    
    /// <summary>
    /// Get point value based on brick type
    /// </summary>
    /// <returns>Points awarded for destroying this brick</returns>
    public int GetPointValue()
    {
        return Type switch
        {
            BrickType.Standard => 10,
            BrickType.Strong => 20,
            BrickType.Bonus => 50,
            _ => 10
        };
    }
}

/// <summary>
/// Brick types with different point values
/// </summary>
public enum BrickType
{
    /// <summary>
    /// Standard brick - 10 points
    /// </summary>
    Standard = 1,
    
    /// <summary>
    /// Strong brick - 20 points
    /// </summary>
    Strong = 2,
    
    /// <summary>
    /// Bonus brick - 50 points
    /// </summary>
    Bonus = 3
}