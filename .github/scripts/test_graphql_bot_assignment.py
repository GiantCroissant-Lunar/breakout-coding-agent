#!/usr/bin/env python3
"""
Test script to validate GraphQL API assignment with Bot ID.

This script tests the GraphQL createIssue functionality with correct Bot assigneeIds
as specified in the issue requirements. It validates that Copilot can be assigned
using the Bot entity ID (BOT_kgDOC9w8XQ) instead of User ID.
"""

import os
import json
import subprocess
import requests
from typing import Dict, Any, Optional


class GraphQLBotAssignmentTest:
    def __init__(self, require_token=True):
        self.github_token = os.environ.get('GITHUB_TOKEN')
        self.repo_owner = 'GiantCroissant-Lunar'
        self.repo_name = 'breakout-coding-agent'
        self.bot_id = 'BOT_kgDOC9w8XQ'  # Copilot Bot ID from issue description
        self.graphql_endpoint = 'https://api.github.com/graphql'
        
        if require_token and not self.github_token:
            raise ValueError("GITHUB_TOKEN environment variable is required")

    def run_gh_command(self, cmd: str) -> str:
        """Execute GitHub CLI command and return output"""
        try:
            result = subprocess.run(
                f"gh {cmd}", 
                shell=True, 
                capture_output=True, 
                text=True, 
                check=True,
                env={**os.environ, 'GITHUB_TOKEN': self.github_token}
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running 'gh {cmd}': {e}")
            print(f"stderr: {e.stderr}")
            raise

    def get_repository_id(self) -> str:
        """Get the repository node ID using GraphQL"""
        query = """
        query($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                id
            }
        }
        """
        
        variables = {
            "owner": self.repo_owner,
            "name": self.repo_name
        }
        
        response = self._execute_graphql_query(query, variables)
        if response and 'data' in response and response['data']['repository']:
            return response['data']['repository']['id']
        
        raise ValueError(f"Could not get repository ID for {self.repo_owner}/{self.repo_name}")

    def _execute_graphql_query(self, query: str, variables: Dict[str, Any] = None) -> Optional[Dict]:
        """Execute a GraphQL query against GitHub API"""
        headers = {
            'Authorization': f'Bearer {self.github_token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            'query': query,
            'variables': variables or {}
        }
        
        try:
            response = requests.post(
                self.graphql_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"GraphQL request failed: {e}")
            return None

    def test_graphql_create_issue_with_bot_assignee(self) -> Dict[str, Any]:
        """Test creating an issue via GraphQL with Bot ID assignment"""
        print("🧪 Testing GraphQL createIssue with Bot ID assignment...")
        
        # Get repository ID first
        repo_id = self.get_repository_id()
        print(f"Repository ID: {repo_id}")
        
        # GraphQL mutation to create issue with Bot assignee
        mutation = """
        mutation($repositoryId: ID!, $title: String!, $body: String!, $assigneeIds: [ID!]) {
            createIssue(input: {
                repositoryId: $repositoryId,
                title: $title,
                body: $body,
                assigneeIds: $assigneeIds
            }) {
                issue {
                    id
                    number
                    title
                    url
                    assignees(first: 10) {
                        nodes {
                            id
                            login
                            __typename
                        }
                    }
                }
            }
        }
        """
        
        variables = {
            "repositoryId": repo_id,
            "title": "TEST: GraphQL Bot Assignment Validation",
            "body": "This is a test issue created via GraphQL API to validate Bot ID assignment.\n\n**Bot ID Used**: " + self.bot_id + "\n\nThis issue should be automatically assigned to the Copilot bot.",
            "assigneeIds": [self.bot_id]
        }
        
        print(f"Creating issue with Bot ID: {self.bot_id}")
        response = self._execute_graphql_query(mutation, variables)
        
        if not response:
            return {"success": False, "error": "No response from GraphQL API"}
        
        if 'errors' in response:
            return {"success": False, "error": response['errors']}
        
        if 'data' in response and response['data']['createIssue']:
            issue_data = response['data']['createIssue']['issue']
            return {
                "success": True,
                "issue": issue_data,
                "assignees": issue_data.get('assignees', {}).get('nodes', [])
            }
        
        return {"success": False, "error": "Unexpected response structure"}

    def test_github_cli_assignment_comparison(self) -> Dict[str, Any]:
        """Test the current GitHub CLI assignment approach for comparison"""
        print("🔍 Testing current GitHub CLI assignment approach...")
        
        try:
            # Create issue using GitHub CLI
            issue_title = "TEST: GitHub CLI Bot Assignment Comparison"
            issue_body = "This is a test issue created via GitHub CLI to compare with GraphQL approach.\\n\\nThis tests the current copilot-swe-agent assignment method."
            
            cmd = f'issue create --title "{issue_title}" --body "{issue_body}" --label test'
            result = self.run_gh_command(cmd)
            issue_url = result.strip()
            
            if not issue_url:
                return {"success": False, "error": "Failed to create issue via CLI"}
            
            # Extract issue number
            issue_number = issue_url.split('/')[-1]
            
            # Try to assign using copilot-swe-agent (current working method)
            try:
                assign_cmd = f'issue edit {issue_number} --add-assignee copilot-swe-agent'
                self.run_gh_command(assign_cmd)
                assignment_success = True
                assignment_error = None
            except Exception as e:
                assignment_success = False
                assignment_error = str(e)
            
            # Get assignee information
            assignees_json = self.run_gh_command(f'issue view {issue_number} --json assignees')
            assignees_data = json.loads(assignees_json) if assignees_json else {}
            assignees = assignees_data.get('assignees', [])
            
            return {
                "success": True,
                "issue_number": issue_number,
                "issue_url": issue_url,
                "assignment_success": assignment_success,
                "assignment_error": assignment_error,
                "assignees": assignees
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}

    def cleanup_test_issues(self, issue_numbers: list):
        """Clean up test issues by closing them"""
        print(f"🧹 Cleaning up test issues: {issue_numbers}")
        
        for issue_number in issue_numbers:
            try:
                close_cmd = f'issue close {issue_number} --comment "Test completed - closing automatically"'
                self.run_gh_command(close_cmd)
                print(f"   ✅ Closed issue #{issue_number}")
            except Exception as e:
                print(f"   ⚠️ Could not close issue #{issue_number}: {e}")

    def validate_bot_assignment_capabilities(self) -> Dict[str, Any]:
        """Validate Bot assignment capabilities using GitHub API"""
        print("🔍 Validating Bot assignment capabilities...")
        
        # Check if the Bot ID is valid for assignment
        try:
            # Try to get user info for the Bot ID
            user_query = f"""
            query {{
                node(id: "{self.bot_id}") {{
                    ... on User {{
                        id
                        login
                        __typename
                    }}
                    ... on Bot {{
                        id
                        login
                        __typename
                    }}
                }}
            }}
            """
            
            response = self._execute_graphql_query(user_query)
            
            if response and 'data' in response and response['data']['node']:
                node_data = response['data']['node']
                return {
                    "bot_id_valid": True,
                    "bot_info": node_data
                }
            else:
                return {
                    "bot_id_valid": False,
                    "error": "Bot ID not found or not accessible"
                }
                
        except Exception as e:
            return {
                "bot_id_valid": False,
                "error": str(e)
            }

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run comprehensive test suite for GraphQL Bot assignment"""
        print("🚀 Starting comprehensive GraphQL Bot assignment test...")
        print("=" * 60)
        
        results = {
            "test_started": True,
            "bot_validation": None,
            "graphql_test": None,
            "cli_test": None,
            "comparison": None,
            "cleanup": None
        }
        
        issues_to_cleanup = []
        
        try:
            # 1. Validate Bot capabilities
            results["bot_validation"] = self.validate_bot_assignment_capabilities()
            print(f"Bot validation: {'✅ PASSED' if results['bot_validation'].get('bot_id_valid') else '❌ FAILED'}")
            
            # 2. Test GraphQL approach
            results["graphql_test"] = self.test_graphql_create_issue_with_bot_assignee()
            if results["graphql_test"]["success"] and "issue" in results["graphql_test"]:
                issue_number = results["graphql_test"]["issue"]["number"]
                issues_to_cleanup.append(str(issue_number))
            print(f"GraphQL test: {'✅ PASSED' if results['graphql_test']['success'] else '❌ FAILED'}")
            
            # 3. Test CLI approach for comparison
            results["cli_test"] = self.test_github_cli_assignment_comparison()
            if results["cli_test"]["success"] and "issue_number" in results["cli_test"]:
                issues_to_cleanup.append(results["cli_test"]["issue_number"])
            print(f"CLI test: {'✅ PASSED' if results['cli_test']['success'] else '❌ FAILED'}")
            
            # 4. Compare results
            results["comparison"] = self._compare_assignment_methods(
                results["graphql_test"], 
                results["cli_test"]
            )
            
        except Exception as e:
            results["error"] = str(e)
            print(f"❌ Test suite failed: {e}")
        
        finally:
            # 5. Cleanup test issues
            if issues_to_cleanup:
                self.cleanup_test_issues(issues_to_cleanup)
                results["cleanup"] = {"cleaned_issues": issues_to_cleanup}
        
        return results

    def _compare_assignment_methods(self, graphql_result: Dict, cli_result: Dict) -> Dict:
        """Compare GraphQL and CLI assignment methods"""
        comparison = {
            "graphql_success": graphql_result.get("success", False),
            "cli_success": cli_result.get("success", False),
            "both_successful": False,
            "assignment_comparison": {},
            "recommendation": ""
        }
        
        if comparison["graphql_success"] and comparison["cli_success"]:
            comparison["both_successful"] = True
            
            # Compare assignees
            graphql_assignees = graphql_result.get("assignees", [])
            cli_assignees = cli_result.get("assignees", [])
            
            comparison["assignment_comparison"] = {
                "graphql_assignees": [a.get("login") for a in graphql_assignees],
                "cli_assignees": [a.get("login") for a in cli_assignees],
                "same_result": len(graphql_assignees) == len(cli_assignees)
            }
            
            if comparison["assignment_comparison"]["same_result"]:
                comparison["recommendation"] = "Both methods work equivalently"
            else:
                comparison["recommendation"] = "Methods produce different results - further investigation needed"
        elif comparison["cli_success"]:
            comparison["recommendation"] = "CLI method works, GraphQL needs investigation"
        elif comparison["graphql_success"]:
            comparison["recommendation"] = "GraphQL method works, CLI may have issues"
        else:
            comparison["recommendation"] = "Both methods failed - check Bot ID and permissions"
        
        return comparison

    def print_test_results(self, results: Dict[str, Any]):
        """Print formatted test results"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        if results.get("bot_validation"):
            print(f"🤖 Bot Validation: {'✅ VALID' if results['bot_validation'].get('bot_id_valid') else '❌ INVALID'}")
            if results['bot_validation'].get('bot_info'):
                bot_info = results['bot_validation']['bot_info']
                print(f"   Bot Info: {bot_info.get('login')} ({bot_info.get('__typename')})")
        
        if results.get("graphql_test"):
            success = results["graphql_test"]["success"]
            print(f"📈 GraphQL Test: {'✅ PASSED' if success else '❌ FAILED'}")
            if not success:
                print(f"   Error: {results['graphql_test'].get('error')}")
            else:
                assignees = results["graphql_test"].get("assignees", [])
                print(f"   Assignees: {[a.get('login') for a in assignees]}")
        
        if results.get("cli_test"):
            success = results["cli_test"]["success"]
            print(f"🖥️  CLI Test: {'✅ PASSED' if success else '❌ FAILED'}")
            if success:
                assignment_success = results["cli_test"].get("assignment_success", False)
                print(f"   Assignment: {'✅ SUCCESS' if assignment_success else '❌ FAILED'}")
                assignees = results["cli_test"].get("assignees", [])
                print(f"   Assignees: {[a.get('login') for a in assignees]}")
        
        if results.get("comparison"):
            comp = results["comparison"]
            print(f"🔍 Comparison: {comp.get('recommendation', 'N/A')}")
        
        print("\n" + "=" * 60)


def main():
    """Entry point for the test script"""
    print("🧪 GraphQL Bot Assignment Test Suite")
    print("Testing GitHub GraphQL API assignment with Bot ID")
    print(f"Bot ID: BOT_kgDOC9w8XQ")
    print("=" * 60)
    
    try:
        test_suite = GraphQLBotAssignmentTest()
        results = test_suite.run_comprehensive_test()
        test_suite.print_test_results(results)
        
        # Determine overall success
        overall_success = (
            results.get("graphql_test", {}).get("success", False) or
            results.get("cli_test", {}).get("success", False)
        )
        
        if overall_success:
            print("🎉 Test suite completed successfully!")
            return True
        else:
            print("💥 Test suite failed!")
            return False
            
    except Exception as e:
        print(f"❌ Test suite error: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)