using Breakout.Game.Models;
using Breakout.Game.Utilities;

namespace Breakout.Game.Systems;

/// <summary>
/// Handles collision detection for game objects
/// </summary>
public static class CollisionSystem
{
    /// <summary>
    /// Checks if ball has collided with screen boundaries
    /// </summary>
    /// <param name="ball">Ball to check</param>
    /// <param name="screenWidth">Screen width</param>
    /// <param name="screenHeight">Screen height</param>
    /// <returns>True if collision detected</returns>
    public static bool CheckWallCollision(Ball ball, int screenWidth, int screenHeight)
    {
        return ball.X <= 0 || ball.X >= screenWidth - 1 || ball.Y <= 1 || ball.Y >= screenHeight - 1;
    }
    
    /// <summary>
    /// Checks if ball has collided with paddle
    /// </summary>
    /// <param name="ball">Ball to check</param>
    /// <param name="paddle">Paddle to check against</param>
    /// <returns>True if collision detected</returns>
    public static bool CheckPaddleCollision(Ball ball, Paddle paddle)
    {
        if (paddle == null) return false;
        
        // Simple rectangular collision detection
        return ball.X >= paddle.X && 
               ball.X < paddle.X + paddle.Width &&
               ball.Y >= paddle.Y && 
               ball.Y <= paddle.Y;
    }
    
    /// <summary>
    /// Determines the type of paddle collision
    /// </summary>
    /// <param name="ball">Ball involved in collision</param>
    /// <param name="paddle">Paddle involved in collision</param>
    /// <returns>Type of collision</returns>
    public static PaddleCollisionType GetPaddleCollisionType(Ball ball, Paddle paddle)
    {
        if (!CheckPaddleCollision(ball, paddle)) return PaddleCollisionType.None;
        
        // Determine collision side based on ball's relative position
        int paddleCenter = paddle.X + paddle.Width / 2;
        int ballRelativePos = ball.X - paddleCenter;
        
        // Top collision if ball is near center of paddle
        if (Math.Abs(ballRelativePos) < 2) return PaddleCollisionType.Top;
        
        // Side collisions
        return ballRelativePos < 0 ? PaddleCollisionType.Left : PaddleCollisionType.Right;
    }
}

/// <summary>
/// Types of paddle collision
/// </summary>
public enum PaddleCollisionType
{
    /// <summary>
    /// No collision
    /// </summary>
    None,
    
    /// <summary>
    /// Ball hits top of paddle (normal bounce)
    /// </summary>
    Top,
    
    /// <summary>
    /// Ball hits left side (angle bounce)
    /// </summary>
    Left,
    
    /// <summary>
    /// Ball hits right side (angle bounce)
    /// </summary>
    Right,
    
    /// <summary>
    /// Ball hits bottom (should not happen in normal play)
    /// </summary>
    Bottom
}