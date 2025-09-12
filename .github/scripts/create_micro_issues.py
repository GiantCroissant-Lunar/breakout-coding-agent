#!/usr/bin/env python3
"""
Micro-Issue Creation Script
Replaces complex shell logic in micro-issue-automation.yml with maintainable Python
"""

import os
import sys
import json
import subprocess
from typing import Dict, List, Optional, NamedTuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class MicroIssue(NamedTuple):
    title: str
    body: str
    assign_immediately: bool = False

class GitHubAPI:
    def __init__(self, gh_token: str):
        self.gh_token = gh_token
        
    def run_graphql_query(self, query: str, variables: Dict = None) -> Optional[Dict]:
        """Execute GraphQL query via gh CLI"""
        try:
            cmd = ['gh', 'api', 'graphql', '-f', f'query={query}']
            if variables:
                for key, value in variables.items():
                    cmd.extend(['-f', f'{key}={value}'])
                    
            env = os.environ.copy()
            env['GH_TOKEN'] = self.gh_token
            
            result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.error(f"GraphQL query failed: {e}")
            return None
    
    def get_repository_id(self, owner: str, name: str) -> Optional[str]:
        """Get repository ID for GraphQL mutations"""
        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
          }
        }
        """
        
        result = self.run_graphql_query(query, {'owner': owner, 'name': name})
        if result and 'data' in result:
            return result['data']['repository']['id']
        return None
    
    def get_copilot_bot_id(self, owner: str, name: str) -> Optional[str]:
        """Get Copilot Bot ID dynamically"""
        query = """
        query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            suggestedActors(capabilities: [CAN_BE_ASSIGNED], first: 100) {
              nodes {
                login
                __typename
                ... on Bot {
                  id
                }
              }
            }
          }
        }
        """
        
        result = self.run_graphql_query(query, {'owner': owner, 'name': name})
        if result and 'data' in result:
            actors = result['data']['repository']['suggestedActors']['nodes']
            for actor in actors:
                if actor.get('login') == 'copilot-swe-agent' and actor.get('__typename') == 'Bot':
                    return actor['id']
        return None
    
    def create_issue(self, repo_id: str, title: str, body: str, assignee_ids: List[str] = None) -> Optional[str]:
        """Create issue with optional assignee"""
        assignee_ids = assignee_ids or []
        
        mutation = """
        mutation($repositoryId: ID!, $title: String!, $body: String!, $assigneeIds: [ID!]) {
          createIssue(input: {
            repositoryId: $repositoryId,
            title: $title,
            body: $body,
            assigneeIds: $assigneeIds
          }) {
            issue {
              number
              assignees(first: 10) {
                nodes {
                  login
                }
              }
            }
          }
        }
        """
        
        variables = {
            'repositoryId': repo_id,
            'title': title,
            'body': body,
            'assigneeIds': json.dumps(assignee_ids)
        }
        
        result = self.run_graphql_query(mutation, variables)
        if result and 'data' in result:
            issue_data = result['data']['createIssue']['issue']
            assignees = [node['login'] for node in issue_data['assignees']['nodes']]
            logger.info(f"✅ Created issue #{issue_data['number']}: {title}")
            if assignees:
                logger.info(f"   Assigned to: {', '.join(assignees)}")
            return issue_data['number']
        return None

class MicroIssueTemplates:
    """Templates for decomposing Game-RFCs into micro-issues"""
    
    @staticmethod
    def get_game_rfc_004_templates() -> List[MicroIssue]:
        """Game-RFC-004: Brick System decomposition"""
        return [
            MicroIssue(
                title="Game-RFC-004-1: Create Brick Model Class",
                body="""@copilot Please implement the basic Brick model class for Game-RFC-004.

## Scope
Create a single `Brick` class with:
- Position (x, y) properties
- Color/Type property  
- IsDestroyed flag
- Basic constructor

## Files Expected
- `dotnet/game/Breakout.Game/Models/Brick.cs`

## Definition of Done
- [ ] Brick class compiles without warnings
- [ ] Basic properties implemented (Position, Color, IsDestroyed)
- [ ] Constructor accepts position and type parameters
- [ ] Proper C# documentation comments

**Parent RFC**: Game-RFC-004: Brick System  
**Dependencies**: None""",
                assign_immediately=True
            ),
            
            MicroIssue(
                title="Game-RFC-004-2: Implement Brick Collision Detection", 
                body="""@copilot Please implement collision detection for bricks.

## Scope
Add collision detection methods to the Brick class:
- CollidesWith(Ball ball) method
- Bounding box calculation
- Collision response logic

## Files Expected
- Update `dotnet/game/Breakout.Game/Models/Brick.cs`
- Possibly new `dotnet/game/Breakout.Game/Physics/CollisionDetection.cs`

## Definition of Done
- [ ] Collision detection methods implemented
- [ ] Works with existing Ball class
- [ ] No compilation errors
- [ ] Basic collision tests pass

**Parent RFC**: Game-RFC-004: Brick System  
**Dependencies**: Game-RFC-004-1""",
                assign_immediately=False
            ),
            
            MicroIssue(
                title="Game-RFC-004-3: Add Brick Rendering System",
                body="""@copilot Please implement brick rendering functionality.

## Scope
Add rendering capabilities for bricks:
- BrickRenderer component
- Integration with existing rendering pipeline
- Color/texture support

## Files Expected  
- `dotnet/game/Breakout.Game/Rendering/BrickRenderer.cs`
- Updates to main game loop

## Definition of Done
- [ ] Bricks visible on screen
- [ ] Different colors render correctly
- [ ] Performance is acceptable
- [ ] Integration with existing rendering system

**Parent RFC**: Game-RFC-004: Brick System  
**Dependencies**: Game-RFC-004-1""",
                assign_immediately=False
            ),
            
            MicroIssue(
                title="Game-RFC-004-4: Create Brick Layout Generator",
                body="""@copilot Please implement brick layout generation.

## Scope
Create system to generate brick layouts:
- BrickLayoutGenerator class
- Support for different patterns (rows, shapes)
- Configurable brick counts and spacing

## Files Expected
- `dotnet/game/Breakout.Game/Layout/BrickLayoutGenerator.cs`
- Configuration/settings for layouts

## Definition of Done
- [ ] Can generate standard brick patterns
- [ ] Configurable rows and columns
- [ ] Different brick types supported
- [ ] Layout generation is deterministic

**Parent RFC**: Game-RFC-004: Brick System  
**Dependencies**: Game-RFC-004-1""",
                assign_immediately=False
            ),
            
            MicroIssue(
                title="Game-RFC-004-5: Integrate Brick System with Game Loop",
                body="""@copilot Please integrate the complete Brick System with the main game.

## Scope
Final integration of all brick components:
- Add bricks to game state
- Handle brick destruction
- Update score when bricks destroyed
- Win condition (all bricks destroyed)

## Files Expected
- Updates to main game loop files
- Score tracking integration
- Game state management updates

## Definition of Done
- [ ] Bricks appear in game
- [ ] Ball destroys bricks on collision
- [ ] Score increases when bricks destroyed
- [ ] Game ends when all bricks destroyed
- [ ] Complete Breakout gameplay working

**Parent RFC**: Game-RFC-004: Brick System  
**Dependencies**: Game-RFC-004-1, Game-RFC-004-2, Game-RFC-004-3, Game-RFC-004-4""",
                assign_immediately=False
            )
        ]
    
    @staticmethod
    def get_game_rfc_005_templates() -> List[MicroIssue]:
        """Game-RFC-005: Game State Management decomposition"""
        return [
            MicroIssue(
                title="Game-RFC-005-1: Create Game State Enum and Manager",
                body="""@copilot Please implement basic game state management.

## Scope
Create foundation for game state management:
- GameState enum (Menu, Playing, Paused, GameOver, Victory)
- GameStateManager class
- State transition methods

## Files Expected
- `dotnet/game/Breakout.Game/State/GameState.cs`
- `dotnet/game/Breakout.Game/State/GameStateManager.cs`

## Definition of Done
- [ ] GameState enum with all required states
- [ ] GameStateManager handles state transitions
- [ ] State change events/notifications
- [ ] Thread-safe state access

**Parent RFC**: Game-RFC-005: Game State Management  
**Dependencies**: None""",
                assign_immediately=True
            ),
            
            MicroIssue(
                title="Game-RFC-005-2: Implement Menu System",
                body="""@copilot Please implement the game menu system.

## Scope
Create menu system for game navigation:
- Main menu with Start/Quit options
- Pause menu with Resume/Quit options
- Menu navigation handling

## Files Expected
- `dotnet/game/Breakout.Game/UI/MainMenu.cs`
- `dotnet/game/Breakout.Game/UI/PauseMenu.cs`

## Definition of Done
- [ ] Main menu displays correctly
- [ ] Menu navigation works with keyboard/mouse
- [ ] Start button transitions to Playing state
- [ ] Pause menu accessible during gameplay

**Parent RFC**: Game-RFC-005: Game State Management  
**Dependencies**: Game-RFC-005-1""",
                assign_immediately=False
            )
        ]

class MicroIssueCreator:
    def __init__(self, gh_token: str, repo_owner: str, repo_name: str):
        self.api = GitHubAPI(gh_token)
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        
        # Get repository and bot IDs
        self.repo_id = self.api.get_repository_id(repo_owner, repo_name)
        self.copilot_bot_id = self.api.get_copilot_bot_id(repo_owner, repo_name)
        
        if not self.repo_id:
            raise RuntimeError(f"Could not get repository ID for {repo_owner}/{repo_name}")
        if not self.copilot_bot_id:
            raise RuntimeError(f"Could not get Copilot Bot ID for {repo_owner}/{repo_name}")
            
        logger.info(f"Repository ID: {self.repo_id}")
        logger.info(f"Copilot Bot ID: {self.copilot_bot_id}")
    
    def create_micro_issues(self, game_rfc: str) -> List[str]:
        """Create micro-issues for specified Game-RFC"""
        logger.info(f"🔧 Creating micro-issues for {game_rfc}...")
        
        # Get templates based on Game-RFC
        if game_rfc == "Game-RFC-004":
            templates = MicroIssueTemplates.get_game_rfc_004_templates()
        elif game_rfc == "Game-RFC-005":
            templates = MicroIssueTemplates.get_game_rfc_005_templates()
        else:
            logger.error(f"No templates defined for {game_rfc}")
            return []
        
        created_issues = []
        
        for template in templates:
            assignee_ids = [self.copilot_bot_id] if template.assign_immediately else []
            
            issue_number = self.api.create_issue(
                self.repo_id,
                template.title,
                template.body,
                assignee_ids
            )
            
            if issue_number:
                created_issues.append(issue_number)
                if not template.assign_immediately:
                    logger.info(f"   (Not assigned - depends on other micro-issues)")
            else:
                logger.error(f"Failed to create issue: {template.title}")
        
        logger.info(f"✅ Created {len(created_issues)} micro-issues for {game_rfc}")
        return created_issues

def main():
    """Main entry point"""
    try:
        gh_token = os.environ['GH_TOKEN']
        game_rfc = os.environ.get('GAME_RFC', '')
        repo_full = os.environ['GITHUB_REPOSITORY']
        
        if not game_rfc:
            logger.error("GAME_RFC environment variable required")
            sys.exit(1)
            
        repo_owner, repo_name = repo_full.split('/')
        
        creator = MicroIssueCreator(gh_token, repo_owner, repo_name)
        created_issues = creator.create_micro_issues(game_rfc)
        
        if created_issues:
            logger.info("🎯 Strategy Benefits:")
            logger.info("- Smaller scope = higher success rate")
            logger.info("- Isolated failures = easier recovery")
            logger.info("- Sequential dependencies = controlled progression")
            logger.info("- Automatic assignment = no manual intervention")
            logger.info("")
            logger.info("📋 Next Steps:")
            logger.info("1. Monitor first micro-issue (assigned to Copilot)")
            logger.info("2. Assign subsequent issues after dependencies complete")
            logger.info("3. Use 'start over' approach if any issue fails")
            
            sys.exit(0)
        else:
            logger.error("No micro-issues were created")
            sys.exit(1)
            
    except KeyError as e:
        logger.error(f"Missing required environment variable: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()