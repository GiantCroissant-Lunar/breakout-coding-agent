#!/usr/bin/env python3
"""
Micro-Issue Creation Script
Replaces complex shell logic in micro-issue-automation.yml with maintainable Python
"""

import os
import sys
import json
import subprocess
import re
import glob
import tempfile
from typing import Dict, List, Optional, NamedTuple
from pathlib import Path
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
            # Create the GraphQL payload
            payload = {"query": query}
            if variables:
                payload["variables"] = variables
            
            # Write payload to temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(payload, f, indent=2)
                payload_file = f.name
            
            try:
                # Use gh api with JSON input
                cmd = ['gh', 'api', 'graphql', '--input', payload_file]
                
                env = os.environ.copy()
                env['GH_TOKEN'] = self.gh_token
                
                result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
                return json.loads(result.stdout)
            finally:
                # Clean up temp file
                os.unlink(payload_file)
                
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            logger.error(f"GraphQL query failed: {e}")
            if hasattr(e, 'stderr') and e.stderr:
                logger.error(f"Error details: {e.stderr}")
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
        """Create issue with optional assignee using GraphQL"""
        assignee_ids = assignee_ids or []
        
        mutation = """
        mutation($repositoryId: ID!, $title: String!, $body: String!, $assigneeIds: [ID!], $labelIds: [ID!]) {
          createIssue(input: {
            repositoryId: $repositoryId,
            title: $title,
            body: $body,
            assigneeIds: $assigneeIds,
            labelIds: $labelIds
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
            'assigneeIds': assignee_ids,
            'labelIds': []  # We'll skip labels for now to simplify
        }
        
        result = self.run_graphql_query(mutation, variables)
        if result and 'data' in result and result['data']['createIssue']:
            issue_data = result['data']['createIssue']['issue']
            assignees = [node['login'] for node in issue_data['assignees']['nodes']]
            logger.info(f"✅ Created issue #{issue_data['number']}: {title}")
            if assignees:
                logger.info(f"   Assigned to: {', '.join(assignees)}")
            return str(issue_data['number'])
        else:
            if result and 'errors' in result:
                logger.error(f"GraphQL errors: {result['errors']}")
            return None

# Import RFC parser functions
sys.path.append(os.path.dirname(__file__))
from rfc_parser import parse_any_rfc

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
            logger.warning(f"Could not get Copilot Bot ID for {repo_owner}/{repo_name} - will create issues without auto-assignment")
        
        logger.info(f"Repository ID: {self.repo_id}")
        if self.copilot_bot_id:
            logger.info(f"Copilot Bot ID: {self.copilot_bot_id}")
        else:
            logger.info("No Copilot Bot ID - issues will be created unassigned")
    
    def create_micro_issues(self, game_rfc: str) -> List[str]:
        """Create micro-issues for specified Game-RFC using dynamic parsing"""
        logger.info(f"🔧 Creating micro-issues for {game_rfc} using RFC parsing...")
        
        # Extract RFC number and find corresponding file
        rfc_match = re.match(r'Game-RFC-(\d+)', game_rfc)
        if not rfc_match:
            logger.error(f"Invalid Game-RFC format: {game_rfc}")
            return []
            
        rfc_number = rfc_match.group(1)
        rfc_file = f"docs/game-rfcs/RFC-{rfc_number.zfill(3)}-*.md"
        
        # Find RFC file using glob pattern
        import glob
        rfc_files = glob.glob(rfc_file)
        if not rfc_files:
            logger.error(f"RFC file not found for {game_rfc}")
            return []
            
        rfc_path = rfc_files[0]
        logger.info(f"📄 Parsing RFC: {rfc_path}")
        
        # Parse RFC dynamically
        try:
            templates = parse_any_rfc(rfc_path, game_rfc)
            logger.info(f"🎯 Generated {len(templates)} micro-issues from RFC structure")
        except Exception as e:
            logger.error(f"Failed to parse RFC {rfc_path}: {e}")
            return []
        
        created_issues = []
        
        for i, template in enumerate(templates):
            # First issue gets assigned immediately if Bot ID is available, others depend on completion
            assignee_ids = [self.copilot_bot_id] if i == 0 and self.copilot_bot_id else []
            
            issue_number = self.api.create_issue(
                self.repo_id,
                template.title,
                template.body,
                assignee_ids
            )
            
            if issue_number:
                created_issues.append(issue_number)
                if i > 0:
                    logger.info(f"   (Not assigned - depends on completion of previous micro-issues)")
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