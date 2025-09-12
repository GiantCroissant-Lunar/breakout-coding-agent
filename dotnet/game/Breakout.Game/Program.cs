using System;
using Breakout.Game;

class Program
{
    static void Main()
    {
        Console.WriteLine("🎮 Breakout Game - Lives System Implemented!");
        Console.WriteLine("Starting with 3 lives - lose a life each time the ball falls off screen");
        Console.WriteLine("Game over when all lives are lost");
        Console.WriteLine("\nPress Enter to start...");
        Console.ReadLine();
        
        var game = new Game();
        game.Run();
    }
}
