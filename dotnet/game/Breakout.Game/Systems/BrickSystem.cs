using Breakout.Game.Models;

namespace Breakout.Game.Systems;

/// <summary>
/// Handles brick-related game logic including collision detection and destruction
/// </summary>
public static class BrickSystem
{
    /// <summary>
    /// Checks for collisions between the ball and any active bricks
    /// </summary>
    /// <param name="ball">Ball to check collisions for</param>
    /// <param name="bricks">List of bricks to check against</param>
    /// <returns>First brick that collides with the ball, or null if no collision</returns>
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
        
        // Clear brick from display
        ClearBrick(brick);
    }
    
    /// <summary>
    /// Determines the bounce direction based on which side of the brick was hit
    /// </summary>
    /// <param name="ball">Ball involved in collision</param>
    /// <param name="brick">Brick involved in collision</param>
    /// <returns>Direction the ball should bounce</returns>
    public static BounceDirection GetBounceDirection(Ball ball, Brick brick)
    {
        // Determine which side of brick was hit
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
    /// Draws all active bricks to the console
    /// </summary>
    /// <param name="bricks">List of bricks to draw</param>
    public static void DrawBricks(List<Brick> bricks)
    {
        foreach (var brick in bricks.Where(b => !b.IsDestroyed))
        {
            Console.SetCursorPosition(brick.X, brick.Y);
            Console.ForegroundColor = brick.Color;
            Console.Write(new string(brick.Character, brick.Width));
        }
        Console.ResetColor();
    }
    
    /// <summary>
    /// Clears a brick from the display by overwriting it with spaces
    /// </summary>
    /// <param name="brick">Brick to clear</param>
    public static void ClearBrick(Brick brick)
    {
        Console.SetCursorPosition(brick.X, brick.Y);
        Console.Write(new string(' ', brick.Width));
    }
    
    /// <summary>
    /// Clears all bricks from the display
    /// </summary>
    /// <param name="bricks">List of bricks to clear</param>
    public static void ClearAllBricks(List<Brick> bricks)
    {
        foreach (var brick in bricks)
        {
            ClearBrick(brick);
        }
    }
    
    /// <summary>
    /// Checks if the win condition is met (all bricks destroyed)
    /// </summary>
    /// <param name="layout">Brick layout to check</param>
    /// <returns>True if all bricks are destroyed</returns>
    public static bool CheckWinCondition(BrickLayout layout)
    {
        return layout.GetActiveBricks().Count == 0;
    }
}