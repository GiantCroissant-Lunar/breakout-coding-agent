using Breakout.Game.Models;
using Breakout.Game.Utilities;

namespace Breakout.Game.Systems;

/// <summary>
/// Handles paddle movement logic and boundary checking
/// </summary>
public static class PaddleSystem
{
    /// <summary>
    /// Updates the paddle state
    /// </summary>
    /// <param name="paddle">Paddle to update</param>
    public static void Update(Paddle paddle)
    {
        // Currently no per-frame updates needed for paddle
        // This method is here for future expansion and RFC compliance
    }
    
    /// <summary>
    /// Moves the paddle left if possible
    /// </summary>
    /// <param name="paddle">Paddle to move</param>
    public static void MoveLeft(Paddle paddle)
    {
        if (paddle != null && paddle.CanMoveLeft())
        {
            paddle.MoveLeft();
        }
    }
    
    /// <summary>
    /// Moves the paddle right if possible
    /// </summary>
    /// <param name="paddle">Paddle to move</param>
    public static void MoveRight(Paddle paddle)
    {
        if (paddle != null && paddle.CanMoveRight())
        {
            paddle.MoveRight();
        }
    }
    
    /// <summary>
    /// Initializes the paddle to its starting position
    /// </summary>
    /// <param name="paddle">Paddle to initialize</param>
    public static void InitializePaddle(Paddle paddle)
    {
        if (paddle != null)
        {
            paddle.X = (Constants.CONSOLE_WIDTH - PaddleConstants.DefaultWidth) / 2;
            paddle.Y = Constants.CONSOLE_HEIGHT - 3;
            paddle.Width = PaddleConstants.DefaultWidth;
            paddle.Character = PaddleConstants.DefaultCharacter;
        }
    }
}