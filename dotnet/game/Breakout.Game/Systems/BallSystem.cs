using Breakout.Game.Models;
using Breakout.Game.Utilities;

namespace Breakout.Game.Systems;

/// <summary>
/// Handles ball physics and movement
/// </summary>
public static class BallSystem
{
    /// <summary>
    /// Updates ball physics for one frame
    /// </summary>
    /// <param name="ball">Ball to update</param>
    /// <param name="paddle">Paddle for collision detection</param>
    public static void Update(Ball ball, Paddle? paddle = null)
    {
        if (!ball.IsActive) return;
        
        // Add speed multiplier to movement accumulator
        ball.MovementAccumulator += ball.SpeedMultiplier;
        
        // Move ball once if accumulator reaches 1.0 or more
        if (ball.MovementAccumulator >= 1.0)
        {
            // Move ball
            ball.Move();
            
            // Reduce accumulator by 1.0 (but keep fractional part)
            ball.MovementAccumulator -= 1.0;
            
            // Check wall collisions
            HandleWallCollisions(ball);
            
            // Check paddle collision
            if (paddle != null)
            {
                HandlePaddleCollision(ball, paddle);
            }
        }
    }
    
    /// <summary>
    /// Handles collisions with screen boundaries
    /// </summary>
    /// <param name="ball">Ball to check</param>
    public static void HandleWallCollisions(Ball ball)
    {
        // Left and right walls
        if (ball.X <= 0)
        {
            ball.DeltaX = -ball.DeltaX;
            ball.X = 1; // Ensure ball stays inside bounds
        }
        else if (ball.X >= Constants.CONSOLE_WIDTH - 1)
        {
            ball.DeltaX = -ball.DeltaX;
            ball.X = Constants.CONSOLE_WIDTH - 2;
        }
        
        // Top wall
        if (ball.Y <= 1)
        {
            ball.DeltaY = -ball.DeltaY;
            ball.Y = 2;
        }
        
        // Bottom wall (ball lost)
        if (ball.Y >= Constants.CONSOLE_HEIGHT - 1)
        {
            ball.IsActive = false;
        }
    }
    
    /// <summary>
    /// Handles collision with paddle
    /// </summary>
    /// <param name="ball">Ball to check</param>
    /// <param name="paddle">Paddle to check against</param>
    public static void HandlePaddleCollision(Ball ball, Paddle paddle)
    {
        if (!CollisionSystem.CheckPaddleCollision(ball, paddle)) return;
        
        var collisionType = CollisionSystem.GetPaddleCollisionType(ball, paddle);
        
        switch (collisionType)
        {
            case PaddleCollisionType.Top:
                ball.DeltaY = -Math.Abs(ball.DeltaY); // Always bounce up
                ball.Y = paddle.Y - 1; // Position just above paddle
                break;
                
            case PaddleCollisionType.Left:
                ball.DeltaX = -1; // Bounce left
                ball.DeltaY = -Math.Abs(ball.DeltaY); // And up
                break;
                
            case PaddleCollisionType.Right:
                ball.DeltaX = 1; // Bounce right  
                ball.DeltaY = -Math.Abs(ball.DeltaY); // And up
                break;
        }
    }
    
    /// <summary>
    /// Initializes ball to starting position and velocity
    /// </summary>
    /// <param name="ball">Ball to initialize</param>
    public static void InitializeBall(Ball ball)
    {
        ball.X = BallConstants.StartX;
        ball.Y = BallConstants.StartY;
        ball.DeltaX = BallConstants.InitialDeltaX;
        ball.DeltaY = BallConstants.InitialDeltaY;
        ball.Character = BallConstants.DefaultCharacter;
        ball.IsActive = true;
        ball.SpeedMultiplier = 1.0; // Reset to normal speed
        ball.MovementAccumulator = 0.0; // Reset movement accumulator
    }
    
    /// <summary>
    /// Sets the ball speed based on the current level
    /// </summary>
    /// <param name="ball">Ball to update</param>
    /// <param name="level">Current level (1-based)</param>
    public static void SetBallSpeedForLevel(Ball ball, int level)
    {
        // Increase speed more gradually: level 1 = 1.0x, level 2 = 1.1x, level 3 = 1.2x, etc.
        // Capped at 1.5x for very high levels to keep game playable
        ball.SpeedMultiplier = Math.Min(1.0 + (level - 1) * 0.1, 1.5);
    }
}