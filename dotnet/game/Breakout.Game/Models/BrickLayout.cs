using Breakout.Game.Utilities;

namespace Breakout.Game.Models;

/// <summary>
/// Manages the layout and organization of bricks
/// </summary>
public class BrickLayout
{
    /// <summary>
    /// List of all bricks in the layout
    /// </summary>
    public List<Brick> Bricks { get; set; }
    
    /// <summary>
    /// Number of rows in the layout
    /// </summary>
    public int Rows { get; set; }
    
    /// <summary>
    /// Number of columns in the layout
    /// </summary>
    public int Columns { get; set; }
    
    /// <summary>
    /// Starting X position for the layout
    /// </summary>
    public int StartX { get; set; }
    
    /// <summary>
    /// Starting Y position for the layout
    /// </summary>
    public int StartY { get; set; }
    
    /// <summary>
    /// Initializes a new brick layout
    /// </summary>
    public BrickLayout()
    {
        Bricks = new List<Brick>();
        Rows = BrickConstants.DefaultRows;
        Columns = BrickConstants.DefaultColumns;
    }
    
    /// <summary>
    /// Generates a standard brick layout with rows and columns
    /// </summary>
    public void GenerateStandardLayout()
    {
        Bricks.Clear();
        
        int brickWidth = BrickConstants.DefaultWidth;
        int brickHeight = BrickConstants.DefaultHeight;
        int spacing = BrickConstants.SpacingX;
        int totalWidth = (brickWidth + spacing) * Columns - spacing;
        
        // Center the layout horizontally
        StartX = (Constants.CONSOLE_WIDTH - totalWidth) / 2;
        StartY = 3; // Below top boundary
        
        for (int row = 0; row < Rows; row++)
        {
            for (int col = 0; col < Columns; col++)
            {
                var brick = new Brick
                {
                    X = StartX + col * (brickWidth + spacing),
                    Y = StartY + row * (brickHeight + BrickConstants.SpacingY),
                    Width = brickWidth,
                    Height = brickHeight,
                    IsDestroyed = false,
                    Type = GetBrickTypeForRow(row),
                    Character = BrickConstants.DefaultCharacter,
                    Color = GetColorForType(GetBrickTypeForRow(row))
                };
                
                Bricks.Add(brick);
            }
        }
    }
    
    /// <summary>
    /// Generates a pattern-based layout
    /// </summary>
    /// <param name="pattern">Layout pattern to generate</param>
    public void GeneratePatternLayout(LayoutPattern pattern)
    {
        switch (pattern)
        {
            case LayoutPattern.Standard:
                GenerateStandardLayout();
                break;
            case LayoutPattern.Rainbow:
                GenerateRainbowLayout();
                break;
            case LayoutPattern.Pyramid:
                GeneratePyramidLayout();
                break;
            case LayoutPattern.Checkerboard:
                GenerateCheckerboardLayout();
                break;
            default:
                GenerateStandardLayout();
                break;
        }
    }
    
    /// <summary>
    /// Gets all active (non-destroyed) bricks
    /// </summary>
    /// <returns>List of active bricks</returns>
    public List<Brick> GetActiveBricks()
    {
        return Bricks.Where(b => !b.IsDestroyed).ToList();
    }
    
    /// <summary>
    /// Checks if all bricks are destroyed
    /// </summary>
    /// <returns>True if all bricks are destroyed</returns>
    public bool AllBricksDestroyed()
    {
        return GetActiveBricks().Count == 0;
    }
    
    /// <summary>
    /// Gets the brick type for a specific row (creates variety)
    /// </summary>
    /// <param name="row">Row number</param>
    /// <returns>Brick type for that row</returns>
    private BrickType GetBrickTypeForRow(int row)
    {
        return row switch
        {
            0 or 1 => BrickType.Bonus,   // Top 2 rows are bonus
            2 or 3 => BrickType.Strong,  // Middle 2 rows are strong
            _ => BrickType.Standard      // Bottom rows are standard
        };
    }
    
    /// <summary>
    /// Gets the color for a brick type
    /// </summary>
    /// <param name="type">Brick type</param>
    /// <returns>Console color for the type</returns>
    private ConsoleColor GetColorForType(BrickType type)
    {
        return type switch
        {
            BrickType.Standard => BrickConstants.StandardColor,
            BrickType.Strong => BrickConstants.StrongColor,
            BrickType.Bonus => BrickConstants.BonusColor,
            _ => BrickConstants.StandardColor
        };
    }
    
    /// <summary>
    /// Generates a rainbow-colored layout
    /// </summary>
    private void GenerateRainbowLayout()
    {
        GenerateStandardLayout();
        var colors = new[] { ConsoleColor.Red, ConsoleColor.Yellow, ConsoleColor.Green, 
                           ConsoleColor.Cyan, ConsoleColor.Blue, ConsoleColor.Magenta };
        
        for (int row = 0; row < Rows; row++)
        {
            var color = colors[row % colors.Length];
            for (int col = 0; col < Columns; col++)
            {
                int index = row * Columns + col;
                if (index < Bricks.Count)
                {
                    Bricks[index].Color = color;
                }
            }
        }
    }
    
    /// <summary>
    /// Generates a pyramid-shaped layout
    /// </summary>
    private void GeneratePyramidLayout()
    {
        Bricks.Clear();
        
        int brickWidth = BrickConstants.DefaultWidth;
        int brickHeight = BrickConstants.DefaultHeight;
        int spacing = BrickConstants.SpacingX;
        
        for (int row = 0; row < Rows; row++)
        {
            int bricksInRow = Columns - row * 2;
            if (bricksInRow <= 0) break;
            
            int rowWidth = (brickWidth + spacing) * bricksInRow - spacing;
            int rowStartX = (Constants.CONSOLE_WIDTH - rowWidth) / 2;
            
            for (int col = 0; col < bricksInRow; col++)
            {
                var brick = new Brick
                {
                    X = rowStartX + col * (brickWidth + spacing),
                    Y = 3 + row * (brickHeight + BrickConstants.SpacingY),
                    Width = brickWidth,
                    Height = brickHeight,
                    IsDestroyed = false,
                    Type = GetBrickTypeForRow(row),
                    Character = BrickConstants.DefaultCharacter,
                    Color = GetColorForType(GetBrickTypeForRow(row))
                };
                
                Bricks.Add(brick);
            }
        }
    }
    
    /// <summary>
    /// Generates a checkerboard pattern layout
    /// </summary>
    private void GenerateCheckerboardLayout()
    {
        GenerateStandardLayout();
        
        // Remove every other brick in a checkerboard pattern
        for (int row = 0; row < Rows; row++)
        {
            for (int col = 0; col < Columns; col++)
            {
                if ((row + col) % 2 == 1)
                {
                    int index = row * Columns + col;
                    if (index < Bricks.Count)
                    {
                        Bricks[index].IsDestroyed = true;
                    }
                }
            }
        }
    }
}

/// <summary>
/// Available layout patterns for bricks
/// </summary>
public enum LayoutPattern
{
    /// <summary>
    /// Uniform rows of bricks
    /// </summary>
    Standard,
    
    /// <summary>
    /// Triangular pattern
    /// </summary>
    Pyramid,
    
    /// <summary>
    /// Alternating pattern
    /// </summary>
    Checkerboard,
    
    /// <summary>
    /// Different colored rows
    /// </summary>
    Rainbow
}