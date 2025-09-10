using System;

namespace Breakout.Game;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine("🎮 Breakout Game - Flow-RFC-001 Test");
        Console.WriteLine("Game structure ready for GitHub Coding Agent implementation.");
        Console.WriteLine("Status: Waiting for Flow-RFC-001 validation...");
        
        // Only wait for input if console is available
        if (!Console.IsInputRedirected)
        {
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}