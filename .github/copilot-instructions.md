# Breakout Coding Agent - Instructions for GitHub Copilot

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Project Overview

You are implementing a classic Breakout game using .NET 8 Console Application. This project uses a **two-track RFC approach**:

1. **Flow RFCs**: Workflow engineering (handled by local agents - NOT your responsibility)
2. **Game RFCs**: Game feature implementation (YOUR responsibility)

Focus ONLY on Game RFCs. Never modify Flow-RFC related files.

## Working Effectively

### Bootstrap and Build Commands
Always run these commands from the repository root directory:

```bash
# Restore dependencies
dotnet restore dotnet/game/Breakout.Game/Breakout.Game.csproj

# Build the project - NEVER CANCEL, takes ~10 seconds, set timeout to 60+ seconds  
dotnet build dotnet/game/Breakout.Game/Breakout.Game.csproj

# Clean build when needed - NEVER CANCEL, set timeout to 60+ seconds
cd dotnet/game/Breakout.Game && dotnet clean && dotnet restore && dotnet build
```

### Running the Application

```bash
# Run from repository root
dotnet run --project dotnet/game/Breakout.Game/Breakout.Game.csproj

# OR run from project directory
cd dotnet/game/Breakout.Game && dotnet run
```

**Note**: The application waits for keyboard input. Press any key to exit cleanly.

### Development Workflow

```bash
# For continuous development with auto-rebuild on changes
cd dotnet/game/Breakout.Game && dotnet watch run
```

## Validation Requirements

### ALWAYS Validate After Changes
After implementing any Game-RFC feature, you MUST:

1. **Build Test**: Ensure code compiles without warnings
   ```bash
   dotnet build dotnet/game/Breakout.Game/Breakout.Game.csproj
   ```

2. **Manual Validation**: Run the application and exercise the new feature
   ```bash
   dotnet run --project dotnet/game/Breakout.Game/Breakout.Game.csproj
   ```

3. **Console Testing Scenarios**:
   - Start the game and verify console displays correctly
   - Test input handling (arrow keys, spacebar, ESC)
   - Verify game objects render properly (paddle, ball, bricks)
   - Ensure smooth animation and responsive controls
   - Test win/lose conditions if implemented
   - Verify clean exit with ESC key

### Expected Build Times
- **dotnet restore**: ~1 second
- **dotnet build**: ~1-2 seconds  
- **Clean + restore + build**: ~10 seconds
- **NEVER CANCEL**: Always set timeouts to 60+ seconds to be safe

## Game RFC Implementation

### RFC Location and Process
1. **Check available RFCs**: `docs/game-rfcs/README.md`
2. **Read full specification**: `docs/game-rfcs/RFC-XXX-YYY.md`
3. **Create GitHub issue**: Title format `Implement Game-RFC-XXX: [Feature Name]`
4. **Implementation order**: Generally sequential (001 → 002 → 003 → 004 → 005)

### Current Game RFCs Available
- **Game-RFC-001**: Console Game Shell (foundation - start here)
- **Game-RFC-002**: Paddle Implementation  
- **Game-RFC-003**: Ball Physics
- **Game-RFC-004**: Brick System
- **Game-RFC-005**: Game State Management

### Project Structure for Implementation
```
dotnet/game/Breakout.Game/
├── Program.cs              # Entry point
├── Game.cs                 # Main game class (RFC-001)
├── Models/                 # Game objects
│   ├── GameState.cs        # Game states (RFC-001)
│   ├── Paddle.cs           # Paddle class (RFC-002)  
│   ├── Ball.cs             # Ball class (RFC-003)
│   └── Brick.cs            # Brick class (RFC-004)
├── Systems/                # Game logic
│   ├── InputSystem.cs      # Input handling (RFC-001)
│   ├── RenderSystem.cs     # Console rendering (RFC-001)
│   ├── PhysicsSystem.cs    # Ball physics (RFC-003)
│   └── CollisionSystem.cs  # Collision detection (RFC-004)
└── Utilities/
    └── Constants.cs        # Game constants
```

### Coding Standards

#### Naming Conventions
- **Namespaces**: `Breakout.Game.{System}`
- **Classes**: PascalCase (`Paddle`, `Ball`, `InputSystem`)
- **Methods**: PascalCase (`MoveLeft`, `CheckCollision`)
- **Properties**: PascalCase (`X`, `Y`, `IsDestroyed`)
- **Local variables**: camelCase (`deltaX`, `ballSpeed`)

#### Console Rendering Patterns
```csharp
// Clear and position cursor
Console.SetCursorPosition(x, y);
Console.Write("█");

// Configure console
Console.CursorVisible = false;
Console.BackgroundColor = ConsoleColor.Black;
Console.ForegroundColor = ConsoleColor.White;
```

#### Game Loop Structure
```csharp
while (game.State == GameState.Playing)
{
    HandleInput();      // Process keyboard
    UpdateGame();       // Update positions/physics  
    RenderFrame();      # Draw everything
    Thread.Sleep(16);   // ~60 FPS
}
```

## Branch and PR Requirements

### Branch Naming
- Use format: `copilot/game-rfc-XXX-description`
- Example: `copilot/game-rfc-001-console-shell`

### PR Requirements  
- **Title**: `Implement Game-RFC-XXX: [Feature Name]`
- **Body**: Include checklist from RFC acceptance criteria
- **Reference**: Must include `Closes #issue-number`
- Auto-merge will handle approval and merging

## Common Commands Output Reference

### Repository Root Structure
```
/home/runner/work/breakout-coding-agent/breakout-coding-agent/
├── .github/workflows/auto-merge.yml
├── .gitignore
├── AGENTS.md
├── README.md
├── docs/
│   ├── flow-rfcs/      # NOT your responsibility
│   └── game-rfcs/      # YOUR implementation specs
└── dotnet/
    └── game/
        └── Breakout.Game/  # YOUR implementation directory
```

### Project File Contents
The `Breakout.Game.csproj` is a standard .NET 8 console project:
```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net8.0</TargetFramework>
    <Nullable>enable</Nullable>
    <ImplicitUsings>enable</ImplicitUsings>
  </PropertyGroup>
</Project>
```

## Critical Constraints

### Scope Limitations
- **ONLY implement assigned Game-RFC** - do not work on multiple RFCs
- **DO NOT modify Flow-RFC files** in `docs/flow-rfcs/` or `.github/workflows/`
- **DO NOT change existing working functionality**
- **Keep it simple**: Console-only, no external libraries, no complex graphics

### Technology Stack
- **.NET 8 Console Application only**
- **ASCII/Unicode characters** for graphics
- **Console.SetCursorPosition** for rendering
- **Console.ReadKey** for input
- **No external dependencies** beyond .NET standard library

## Success Criteria

Each Game-RFC implementation succeeds when:
- ✅ All acceptance criteria checkboxes are completed
- ✅ Code compiles without warnings
- ✅ Feature works as specified when manually tested
- ✅ No regression in existing functionality  
- ✅ PR properly formatted and auto-merged
- ✅ Ready for next RFC in sequence

## Development Environment

### .NET Version Information
- **.NET SDK**: 8.0.119
- **Runtime**: 8.0.19  
- **Platform**: Ubuntu Linux
- **Architecture**: x64

### No Tests Currently
There are no unit tests in this project. Focus on:
- Manual console testing
- Visual verification of game behavior
- Functional validation of each feature

---

**Focus on building a fun, playable Breakout game step by step through the Game-RFCs. Start with Game-RFC-001 to establish the foundation, then proceed sequentially through the remaining RFCs.**