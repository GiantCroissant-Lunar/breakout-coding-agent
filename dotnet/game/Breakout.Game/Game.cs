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
    /// Game ball
    /// </summary>
    public Ball Ball { get; set; }
    
    /// <summary>
    /// Game paddle
    /// </summary>
    public Paddle Paddle { get; set; }
    
    /// <summary>
    /// Game brick layout
    /// </summary>
    public BrickLayout BrickLayout { get; set; }
    
    /// <summary>
    /// Game score system
    /// </summary>
    public ScoreSystem ScoreSystem { get; set; }
    
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
        
        // Initialize game objects
        Ball = new Ball();
        Paddle = new Paddle();
        BrickLayout = new BrickLayout();
        ScoreSystem = new ScoreSystem();
        InitializeGameObjects();
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
    /// Initializes game objects to their starting positions
    /// </summary>
    private void InitializeGameObjects()
    {
        // Initialize ball
        BallSystem.InitializeBall(Ball);
        
        // Initialize paddle
        PaddleSystem.InitializePaddle(Paddle);
        
        // Initialize brick layout
        BrickLayout.GenerateStandardLayout();
        
        // Reset score system
        ScoreSystem.Reset();
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
                    // Reset game objects when starting new game
                    InitializeGameObjects();
                }
                break;
                
            case GameState.Playing:
                if (InputSystem.IsSpacePressed(key))
                {
                    State = GameState.Paused;
                }
                // Handle paddle movement
                if (InputSystem.IsLeftPressed(key))
                {
                    PaddleSystem.MoveLeft(Paddle);
                }
                if (InputSystem.IsRightPressed(key))
                {
                    PaddleSystem.MoveRight(Paddle);
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
                // Store previous ball position for clearing
                int prevBallX = Ball.X;
                int prevBallY = Ball.Y;
                
                // Store previous paddle position for clearing
                int prevPaddleX = Paddle.X;
                int prevPaddleY = Paddle.Y;
                
                // Update paddle system
                PaddleSystem.Update(Paddle);
                
                // Update ball physics
                BallSystem.Update(Ball, Paddle);
                
                // Check for brick collisions
                var hitBrick = BrickSystem.CheckBrickCollisions(Ball, BrickLayout.Bricks);
                if (hitBrick != null)
                {
                    BrickSystem.HandleBrickCollision(Ball, hitBrick, ScoreSystem);
                }
                
                // Check win condition (all bricks destroyed)
                if (BrickSystem.CheckWinCondition(BrickLayout))
                {
                    State = GameState.GameOver; // Will be changed to Win state in future RFC
                }
                
                // Check if ball was lost
                if (!Ball.IsActive)
                {
                    State = GameState.GameOver;
                }
                
                // Clear previous positions (ball)
                RenderSystem.ClearPosition(prevBallX, prevBallY);
                
                // Clear previous paddle position (to prevent artifacts if it moved)
                if (prevPaddleX != Paddle.X)
                {
                    Console.SetCursorPosition(prevPaddleX, prevPaddleY);
                    Console.Write(new string(' ', Paddle.Width));
                }
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
        
        // Render game objects during gameplay
        if (State == GameState.Playing)
        {
            BrickSystem.DrawBricks(BrickLayout.Bricks);
            RenderSystem.DrawPaddle(Paddle);
            RenderSystem.DrawBall(Ball);
            RenderSystem.DrawScore(ScoreSystem);
        }
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