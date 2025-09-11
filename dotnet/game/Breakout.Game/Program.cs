namespace Breakout.Game;

/// <summary>
/// Entry point for the Breakout game
/// </summary>
public class Program
{
    /// <summary>
    /// Main entry point
    /// </summary>
    /// <param name="args">Command line arguments</param>
    public static void Main(string[] args)
    {
        try
        {
            var game = new Game();
            game.Run();
        }
        catch (Exception ex)
        {
            Console.WriteLine($"An error occurred: {ex.Message}");
            Console.WriteLine("Press any key to exit...");
            if (!Console.IsInputRedirected)
            {
                Console.ReadKey();
            }
        }
    }
}