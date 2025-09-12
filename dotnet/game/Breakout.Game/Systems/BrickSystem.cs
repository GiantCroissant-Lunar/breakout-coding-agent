using Breakout.Game.Models;

namespace Breakout.Game.Systems;

/// <summary>
/// Handles brick-related game logic
/// </summary>
public static class BrickSystem
{
    /// <summary>
    /// Checks for brick collisions with the ball
    /// </summary>
    /// <param name="ball">Ball to check</param>
    /// <param name="bricks">List of bricks to check against</param>
    /// <returns>First brick that collides with ball, or null if none</returns>
    public static Brick? CheckBrickCollisions(Ball ball, List<Brick> bricks)
    {
        foreach (var brick in bricks.Where(b => !b.IsDestroyed))
        {
            if (brick.CheckCollision(ball))
            {
                return brick;
            }
        }
        return null;
    }
    
    /// <summary>
    /// Handles collision between ball and brick
    /// </summary>
    /// <param name="ball">Ball involved in collision</param>
    /// <param name="brick">Brick involved in collision</param>
    /// <param name="scoreSystem">Score system to update</param>
    public static void HandleBrickCollision(Ball ball, Brick brick, ScoreSystem scoreSystem)
    {
        // Destroy brick
        brick.Destroy();
        
        // Add score
        scoreSystem.AddPoints(brick.GetPointValue());
        
        // Determine bounce direction based on collision side
        var bounceDirection = GetBounceDirection(ball, brick);
        ball.Bounce(bounceDirection);
    }
    
    /// <summary>
    /// Determines which direction the ball should bounce based on collision
    /// </summary>
    /// <param name="ball">Ball involved in collision</param>
    /// <param name="brick">Brick involved in collision</param>
    /// <returns>Direction to bounce the ball</returns>
    public static BounceDirection GetBounceDirection(Ball ball, Brick brick)
    {
        // Calculate centers
        int ballCenterX = ball.X;
        int ballCenterY = ball.Y;
        int brickCenterX = brick.X + brick.Width / 2;
        int brickCenterY = brick.Y + brick.Height / 2;
        
        // Calculate relative position
        int deltaX = ballCenterX - brickCenterX;
        int deltaY = ballCenterY - brickCenterY;
        
        // Determine collision side based on angle
        if (Math.Abs(deltaX) > Math.Abs(deltaY))
        {
            // Hit from left or right side
            return BounceDirection.Horizontal;
        }
        else
        {
            // Hit from top or bottom
            return BounceDirection.Vertical;
        }
    }
    
    /// <summary>
    /// Checks if the game is won (all bricks destroyed)
    /// </summary>
    /// <param name="brickLayout">Brick layout to check</param>
    /// <returns>True if all bricks are destroyed</returns>
    public static bool CheckWinCondition(BrickLayout brickLayout)
    {
        return brickLayout.AllBricksDestroyed();
    }
}