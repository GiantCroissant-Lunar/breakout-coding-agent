using System;
using Breakout.Game.Systems;
using Breakout.Game.Models;

class ScoreTest
{
    static void Main()
    {
        Console.WriteLine("Testing Score System Implementation...");
        
        var scoreSystem = new ScoreSystem();
        
        Console.WriteLine($"Initial state:");
        Console.WriteLine($"  - Current Score: {scoreSystem.CurrentScore}");
        Console.WriteLine($"  - High Score: {scoreSystem.HighScore}");
        Console.WriteLine($"  - Bricks Destroyed: {scoreSystem.BricksDestroyed}");
        
        // Test adding points for different brick types
        Console.WriteLine("\nAdding points for Standard brick (10 points):");
        scoreSystem.AddPoints(10);
        Console.WriteLine($"  - {scoreSystem.GetScoreDisplay()}");
        Console.WriteLine($"  - {scoreSystem.GetBricksDestroyedDisplay()}");
        
        Console.WriteLine("\nAdding points for Strong brick (20 points):");
        scoreSystem.AddPoints(20);
        Console.WriteLine($"  - {scoreSystem.GetScoreDisplay()}");
        Console.WriteLine($"  - {scoreSystem.GetBricksDestroyedDisplay()}");
        
        Console.WriteLine("\nAdding points for Bonus brick (50 points):");
        scoreSystem.AddPoints(50);
        Console.WriteLine($"  - {scoreSystem.GetScoreDisplay()}");
        Console.WriteLine($"  - {scoreSystem.GetBricksDestroyedDisplay()}");
        Console.WriteLine($"  - {scoreSystem.GetHighScoreDisplay()}");
        
        Console.WriteLine("\n✅ Score System Implementation Test Complete!");
    }
}
