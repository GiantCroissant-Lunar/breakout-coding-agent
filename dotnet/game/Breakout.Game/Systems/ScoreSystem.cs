namespace Breakout.Game.Systems;

/// <summary>
/// Manages the game scoring system
/// </summary>
public class ScoreSystem
{
    /// <summary>
    /// Current score for this game session
    /// </summary>
    public int CurrentScore { get; private set; }
    
    /// <summary>
    /// Highest score achieved
    /// </summary>
    public int HighScore { get; private set; }
    
    /// <summary>
    /// Number of bricks destroyed in current session
    /// </summary>
    public int BricksDestroyed { get; private set; }
    
    /// <summary>
    /// Number of lives remaining for the player
    /// </summary>
    public int Lives { get; private set; }
    
    /// <summary>
    /// Initializes a new score system
    /// </summary>
    public ScoreSystem()
    {
        CurrentScore = 0;
        HighScore = 0;
        BricksDestroyed = 0;
        Lives = 3; // Start with 3 lives as specified in RFC
    }
    
    /// <summary>
    /// Adds points to the current score
    /// </summary>
    /// <param name="points">Points to add</param>
    public void AddPoints(int points)
    {
        CurrentScore += points;
        BricksDestroyed++;
        
        if (CurrentScore > HighScore)
        {
            HighScore = CurrentScore;
        }
    }
    
    /// <summary>
    /// Resets the current game score
    /// </summary>
    public void Reset()
    {
        CurrentScore = 0;
        BricksDestroyed = 0;
        Lives = 3; // Reset lives to 3 when starting new game
    }
    
    /// <summary>
    /// Gets a formatted string representation of the current score
    /// </summary>
    /// <returns>Formatted score string</returns>
    public string GetScoreDisplay()
    {
        return $"Score: {CurrentScore:N0}";
    }
    
    /// <summary>
    /// Gets a formatted string representation of the high score
    /// </summary>
    /// <returns>Formatted high score string</returns>
    public string GetHighScoreDisplay()
    {
        return $"High Score: {HighScore:N0}";
    }
    
    /// <summary>
    /// Gets a formatted string representation of bricks destroyed
    /// </summary>
    /// <returns>Formatted bricks destroyed string</returns>
    public string GetBricksDestroyedDisplay()
    {
        return $"Bricks: {BricksDestroyed}";
    }
    
    /// <summary>
    /// Decrements the number of lives remaining
    /// </summary>
    /// <returns>True if lives remain after decrement, false if no lives left</returns>
    public bool DecrementLife()
    {
        if (Lives > 0)
        {
            Lives--;
        }
        return Lives > 0;
    }
    
    /// <summary>
    /// Gets a formatted string representation of lives remaining
    /// </summary>
    /// <returns>Formatted lives string</returns>
    public string GetLivesDisplay()
    {
        // Using hearts for visual appeal as suggested in RFC
        return $"Lives: {new string('♥', Lives)}";
    }
}