using Breakout.Game.Models;
using Breakout.Game.Systems;
using Breakout.Game.Utilities;

namespace Breakout.Game;

/// <summary>
/// Main game class that manages the game loop and state
/// </summary>
public class Game
{
    /// <summary>
    /// Current game state
    /// </summary>
    public GameState State { get; set; }
    
    /// <summary>
    /// Whether the game is running
    /// </summary>
    public bool IsRunning { get; private set; }
    
    /// <summary>
    /// Maximum runtime for the game in testing scenarios (5 minutes)
    /// </summary>
    private readonly DateTime maxRuntime = DateTime.Now.AddMinutes(5);
    
    /// <summary>
    /// Initializes a new instance of the Game class
    /// </summary>
    public Game()
    {
        State = GameState.Menu;
        IsRunning = false;
    }
    
    /// <summary>
    /// Initializes the game systems
    /// </summary>
    public void Initialize()
    {
        RenderSystem.InitializeConsole();
        IsRunning = true;
    }
    
    /// <summary>
    /// Main game loop - runs continuously until exit
    /// </summary>
    public void Run()
    {
        Initialize();
        
        while (IsRunning && State != GameState.Exiting && DateTime.Now < maxRuntime)
        {
            ProcessInput();
            Update();
            Render();
            
            // Frame rate control - target 60 FPS
            Thread.Sleep(Constants.FRAME_DELAY_MS);
        }
        
        Cleanup();
    }
    
    /// <summary>
    /// Processes input for the current frame
    /// </summary>
    private void ProcessInput()
    {
        var key = InputSystem.GetInput();
        
        // Check for exit request
        if (InputSystem.IsExitRequested(key))
        {
            State = GameState.Exiting;
            return;
        }
        
        // Handle input based on current state
        switch (State)
        {
            case GameState.Menu:
                if (InputSystem.IsSpacePressed(key))
                {
                    State = GameState.Playing;
                }
                break;
                
            case GameState.Playing:
                if (InputSystem.IsSpacePressed(key))
                {
                    State = GameState.Paused;
                }
                // Arrow key handling will be used by paddle in future RFCs
                if (InputSystem.IsLeftPressed(key))
                {
                    // Paddle movement left (placeholder for future RFC)
                }
                if (InputSystem.IsRightPressed(key))
                {
                    // Paddle movement right (placeholder for future RFC)
                }
                break;
                
            case GameState.Paused:
                if (InputSystem.IsSpacePressed(key))
                {
                    State = GameState.Playing;
                }
                break;
                
            case GameState.GameOver:
                if (InputSystem.IsSpacePressed(key))
                {
                    State = GameState.Menu; // Restart to menu
                }
                break;
        }
    }
    
    /// <summary>
    /// Updates the game state for the current frame
    /// </summary>
    private void Update()
    {
        // Game logic updates will be added in future RFCs
        // For now, just maintain current state
        
        switch (State)
        {
            case GameState.Menu:
                // Menu logic (none needed currently)
                break;
                
            case GameState.Playing:
                // Game object updates (ball, paddle, collisions) - future RFCs
                break;
                
            case GameState.Paused:
                // No updates while paused
                break;
                
            case GameState.GameOver:
                // Game over logic (none needed currently)
                break;
        }
    }
    
    /// <summary>
    /// Renders the current frame
    /// </summary>
    private void Render()
    {
        RenderSystem.RenderFrame(State);
    }
    
    /// <summary>
    /// Cleans up resources and restores console
    /// </summary>
    private void Cleanup()
    {
        RenderSystem.Cleanup();
        IsRunning = false;
    }
}