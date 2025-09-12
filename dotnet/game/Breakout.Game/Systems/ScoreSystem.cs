namespace Breakout.Game.Systems;

/// <summary>
/// Manages game scoring and statistics
/// </summary>
public class ScoreSystem
{
    /// <summary>
    /// Current score
    /// </summary>
    public int CurrentScore { get; private set; }
    
    /// <summary>
    /// High score
    /// </summary>
    public int HighScore { get; private set; }
    
    /// <summary>
    /// Number of bricks destroyed
    /// </summary>
    public int BricksDestroyed { get; private set; }
    
    /// <summary>
    /// Initializes a new score system
    /// </summary>
    public ScoreSystem()
    {
        CurrentScore = 0;
        HighScore = 0;
        BricksDestroyed = 0;
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
    }
    
    /// <summary>
    /// Gets a formatted score string for display
    /// </summary>
    /// <returns>Formatted score string</returns>
    public string GetScoreText()
    {
        return $"Score: {CurrentScore} | Bricks: {BricksDestroyed} | High: {HighScore}";
    }
}