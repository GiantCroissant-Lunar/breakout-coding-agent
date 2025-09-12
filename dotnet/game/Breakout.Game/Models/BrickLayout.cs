using Breakout.Game.Utilities;

namespace Breakout.Game.Models;

/// <summary>
/// Manages the layout and arrangement of bricks in the game
/// </summary>
public class BrickLayout
{
    /// <summary>
    /// List of all bricks in the layout
    /// </summary>
    public List<Brick> Bricks { get; set; }
    
    /// <summary>
    /// Number of brick rows
    /// </summary>
    public int Rows { get; set; }
    
    /// <summary>
    /// Number of brick columns
    /// </summary>
    public int Columns { get; set; }
    
    /// <summary>
    /// Starting X position for the brick layout
    /// </summary>
    public int StartX { get; set; }
    
    /// <summary>
    /// Starting Y position for the brick layout
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
    /// Generates a standard uniform layout of bricks
    /// </summary>
    public void GenerateStandardLayout()
    {
        Bricks.Clear();
        
        int brickWidth = 6;
        int brickHeight = 1;
        int spacing = 1;
        int totalWidth = (brickWidth + spacing) * Columns - spacing;
        
        StartX = (Console.WindowWidth - totalWidth) / 2;
        StartY = 3; // Below top boundary
        
        for (int row = 0; row < Rows; row++)
        {
            for (int col = 0; col < Columns; col++)
            {
                var brick = new Brick
                {
                    X = StartX + col * (brickWidth + spacing),
                    Y = StartY + row * (brickHeight + spacing),
                    Width = brickWidth,
                    Height = brickHeight,
                    IsDestroyed = false,
                    Type = GetBrickTypeForRow(row),
                    Character = '█',
                    Color = GetColorForType(GetBrickTypeForRow(row))
                };
                
                Bricks.Add(brick);
            }
        }
    }
    
    /// <summary>
    /// Generates a layout based on the specified pattern
    /// </summary>
    /// <param name="pattern">Layout pattern to generate</param>
    public void GeneratePatternLayout(LayoutPattern pattern)
    {
        switch (pattern)
        {
            case LayoutPattern.Standard:
                GenerateStandardLayout();
                break;
            case LayoutPattern.Pyramid:
                GeneratePyramidLayout();
                break;
            case LayoutPattern.Checkerboard:
                GenerateCheckerboardLayout();
                break;
            case LayoutPattern.Rainbow:
                GenerateRainbowLayout();
                break;
            default:
                GenerateStandardLayout();
                break;
        }
    }
    
    /// <summary>
    /// Gets all active (not destroyed) bricks
    /// </summary>
    /// <returns>List of active bricks</returns>
    public List<Brick> GetActiveBricks()
    {
        return Bricks.Where(b => !b.IsDestroyed).ToList();
    }
    
    /// <summary>
    /// Checks if all bricks have been destroyed
    /// </summary>
    /// <returns>True if all bricks are destroyed</returns>
    public bool AllBricksDestroyed()
    {
        return Bricks.All(b => b.IsDestroyed);
    }
    
    /// <summary>
    /// Determines the brick type based on the row number
    /// </summary>
    /// <param name="row">Row number (0-based)</param>
    /// <returns>Brick type for the row</returns>
    private BrickType GetBrickTypeForRow(int row)
    {
        // Top rows are stronger/bonus bricks
        return row switch
        {
            0 or 1 => BrickType.Bonus,    // Top 2 rows are bonus (red)
            2 or 3 => BrickType.Strong,   // Next 2 rows are strong (yellow)
            _ => BrickType.Standard       // Bottom rows are standard (cyan)
        };
    }
    
    /// <summary>
    /// Gets the color for the specified brick type
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
    /// Generates a pyramid pattern layout
    /// </summary>
    private void GeneratePyramidLayout()
    {
        Bricks.Clear();
        
        int brickWidth = BrickConstants.DefaultWidth;
        int brickHeight = BrickConstants.DefaultHeight;
        int spacingX = BrickConstants.SpacingX;
        int spacingY = BrickConstants.SpacingY;
        
        StartY = 3;
        
        for (int row = 0; row < Rows; row++)
        {
            // Pyramid shape - fewer bricks at the top
            int bricksInRow = Math.Max(1, Columns - row * 2);
            int rowStartX = (Constants.CONSOLE_WIDTH - (bricksInRow * (brickWidth + spacingX) - spacingX)) / 2;
            
            for (int col = 0; col < bricksInRow; col++)
            {
                var brick = new Brick
                {
                    X = rowStartX + col * (brickWidth + spacingX),
                    Y = StartY + row * (brickHeight + spacingY),
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
        Bricks.Clear();
        
        int brickWidth = BrickConstants.DefaultWidth;
        int brickHeight = BrickConstants.DefaultHeight;
        int spacingX = BrickConstants.SpacingX;
        int spacingY = BrickConstants.SpacingY;
        
        int totalWidth = (brickWidth + spacingX) * Columns - spacingX;
        StartX = (Constants.CONSOLE_WIDTH - totalWidth) / 2;
        StartY = 3;
        
        for (int row = 0; row < Rows; row++)
        {
            for (int col = 0; col < Columns; col++)
            {
                // Skip bricks in checkerboard pattern
                if ((row + col) % 2 == 0)
                {
                    var brick = new Brick
                    {
                        X = StartX + col * (brickWidth + spacingX),
                        Y = StartY + row * (brickHeight + spacingY),
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
    }
    
    /// <summary>
    /// Generates a rainbow pattern layout with different colored rows
    /// </summary>
    private void GenerateRainbowLayout()
    {
        Bricks.Clear();
        
        int brickWidth = BrickConstants.DefaultWidth;
        int brickHeight = BrickConstants.DefaultHeight;
        int spacingX = BrickConstants.SpacingX;
        int spacingY = BrickConstants.SpacingY;
        
        int totalWidth = (brickWidth + spacingX) * Columns - spacingX;
        StartX = (Constants.CONSOLE_WIDTH - totalWidth) / 2;
        StartY = 3;
        
        ConsoleColor[] rainbowColors = { 
            ConsoleColor.Red, ConsoleColor.Yellow, ConsoleColor.Green, 
            ConsoleColor.Cyan, ConsoleColor.Blue, ConsoleColor.Magenta 
        };
        
        for (int row = 0; row < Rows; row++)
        {
            for (int col = 0; col < Columns; col++)
            {
                var brick = new Brick
                {
                    X = StartX + col * (brickWidth + spacingX),
                    Y = StartY + row * (brickHeight + spacingY),
                    Width = brickWidth,
                    Height = brickHeight,
                    IsDestroyed = false,
                    Type = GetBrickTypeForRow(row),
                    Character = BrickConstants.DefaultCharacter,
                    Color = rainbowColors[row % rainbowColors.Length]
                };
                
                Bricks.Add(brick);
            }
        }
    }
}

/// <summary>
/// Different layout patterns for brick arrangements
/// </summary>
public enum LayoutPattern
{
    /// <summary>
    /// Uniform rows of bricks
    /// </summary>
    Standard,
    
    /// <summary>
    /// Triangular pyramid pattern
    /// </summary>
    Pyramid,
    
    /// <summary>
    /// Alternating checkerboard pattern
    /// </summary>
    Checkerboard,
    
    /// <summary>
    /// Different colored rows (rainbow pattern)
    /// </summary>
    Rainbow
}