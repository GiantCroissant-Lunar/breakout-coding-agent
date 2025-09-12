# Contributing to Breakout Coding Agent

Thanks for your interest in contributing! This project builds a console Breakout game via Game RFCs. Please follow the guidelines below to keep contributions smooth and consistent.

## How to Contribute

1. Review docs
   - Read `AGENTS.md` for coding patterns, structure, and naming.
   - Check `docs/game-rfcs/README.md` for available Game RFCs.
2. Pick an RFC
   - Work on the next ready RFC in order (001 → 002 → …), unless the RFC states otherwise.
   - Open an issue titled: `Implement Game-RFC-XXX: [Feature Name]`.
   - In the description, reference the RFC document and acceptance criteria.
3. Create a branch
   - Branch name format: `copilot/game-rfc-XXX-short-desc`
   - Example: `copilot/game-rfc-001-console-shell`
4. Implement
   - Scope: One RFC per PR. Don’t change Flow RFC files.
   - Follow code standards in `AGENTS.md`.
   - Target: .NET 8 console app using ASCII rendering.
5. Test
   - Build locally and run the console to verify behavior.
   - Ensure no warnings; no regressions in existing features.
6. Pull Request
   - Title: `Implement Game-RFC-XXX: [Feature Name]`
   - Body: Include a checklist mirroring the RFC acceptance criteria and `Closes #<issue-number>`.
   - Keep PRs focused and small.

## Development Setup

- Prerequisites: .NET 8 SDK on Windows, macOS, or Linux.
- Build scripts: see `build/` for optional helpers.
- Project path: `dotnet/game/Breakout.Game` (see repo for exact structure).

### Build and Run

From the repository root:

```powershell
# Build the solution
dotnet build

# Run the console game (adjust path if needed)
dotnet run --project .\dotnet\game\Breakout.Game
```

## Code Style

- Namespaces: `Breakout.Game.{System}`
- Classes/Methods: PascalCase; locals: camelCase; properties: PascalCase
- Keep implementations simple—no external game engines/libraries for rendering.

## Reporting Bugs or Asking Questions

- Use GitHub Issues. Provide steps to reproduce and environment details.
- For security issues, please see `SECURITY.md`.

## Code of Conduct

Participation is governed by our `CODE_OF_CONDUCT.md`.

## License

By contributing, you agree that your contributions will be licensed under the project’s `LICENSE`.
