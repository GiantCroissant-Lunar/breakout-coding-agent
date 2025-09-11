namespace Breakout.Game.Models;

/// <summary>
/// Represents the different states the game can be in
/// </summary>
public enum GameState
{
    /// <summary>
    /// Main menu state - waiting for user to start game
    /// </summary>
    Menu,
    
    /// <summary>
    /// Active gameplay state
    /// </summary>
    Playing,
    
    /// <summary>
    /// Game is paused
    /// </summary>
    Paused,
    
    /// <summary>
    /// Game over state
    /// </summary>
    GameOver,
    
    /// <summary>
    /// Game is exiting
    /// </summary>
    Exiting
}