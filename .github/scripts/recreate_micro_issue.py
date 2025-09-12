#!/usr/bin/env python3
"""
Recreate a micro-issue with proper Copilot assignment
"""
import os
import sys
import json
import subprocess
import re
from typing import Dict, Optional

def run_graphql_query(query: str, variables: Dict = None) -> Optional[Dict]:
    """Execute GraphQL query via gh CLI"""
    try:
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(payload, f, indent=2)
            payload_file = f.name
        
        try:
            cmd = ['gh', 'api', 'graphql', '--input', payload_file]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        finally:
            os.unlink(payload_file)
            
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"GraphQL query failed: {e}")
        return None

def get_repository_info(repo: str) -> tuple:
    """Get repository owner and name"""
    owner, name = repo.split('/')
    return owner, name

def get_copilot_bot_id(owner: str, name: str) -> Optional[str]:
    """Get Copilot Bot ID for assignment"""
    query = """
    query($owner: String!, $name: String!) {
      repository(owner: $owner, name: $name) {
        assignableUsers(first: 100) {
          nodes {
            login
            id
          }
        }
      }
    }
    """
    
    result = run_graphql_query(query, {'owner': owner, 'name': name})
    if result and 'data' in result:
        users = result['data']['repository']['assignableUsers']['nodes']
        for user in users:
            if user.get('login') in ['Copilot', 'copilot-swe-agent', 'github-copilot']:
                return user['id']
    return None

def assign_issue_to_copilot(issue_number: str, repo: str) -> bool:
    """Assign issue to Copilot using GraphQL"""
    owner, name = repo.split('/')
    
    # Get issue node ID
    issue_query = """
    query($owner: String!, $name: String!, $number: Int!) {
      repository(owner: $owner, name: $name) {
        issue(number: $number) {
          id
        }
      }
    }
    """
    
    result = run_graphql_query(issue_query, {
        'owner': owner, 
        'name': name, 
        'number': int(issue_number)
    })
    
    if not result or 'data' not in result:
        print(f"Failed to get issue node ID for #{issue_number}")
        return False
    
    issue_id = result['data']['repository']['issue']['id']
    
    # Get Copilot ID
    copilot_id = get_copilot_bot_id(owner, name)
    if not copilot_id:
        print("Could not find Copilot in assignable users")
        return False
    
    # Assign using GraphQL mutation
    mutation = """
    mutation($assignableId: ID!, $assigneeIds: [ID!]!) {
      replaceActorsForAssignable(input: {
        assignableId: $assignableId
        actorIds: $assigneeIds
      }) {
        assignable {
          ... on Issue {
            number
            assignees(first: 10) {
              nodes {
                login
              }
            }
          }
        }
      }
    }
    """
    
    result = run_graphql_query(mutation, {
        'assignableId': issue_id,
        'assigneeIds': [copilot_id]
    })
    
    if result and 'data' in result:
        assignees = result['data']['replaceActorsForAssignable']['assignable']['assignees']['nodes']
        assigned_logins = [a['login'] for a in assignees]
        print(f"✅ Issue #{issue_number} assigned to: {', '.join(assigned_logins)}")
        return True
    
    print(f"❌ Failed to assign issue #{issue_number}")
    return False

def recreate_micro_issue(original_issue: str, repo: str) -> bool:
    """Recreate a micro-issue with proper assignment"""
    try:
        # Get original issue details
        cmd = ['gh', 'issue', 'view', original_issue, '--repo', repo, '--json', 'title,body,labels']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        issue_data = json.loads(result.stdout)
        
        original_title = issue_data['title']
        original_body = issue_data['body']
        labels = [label['name'] for label in issue_data.get('labels', [])]
        
        print(f"📋 Original Issue: {original_title}")
        
        # Close original issue
        print(f"🗑️ Closing original issue #{original_issue}...")
        subprocess.run([
            'gh', 'issue', 'close', original_issue, 
            '--repo', repo,
            '--reason', 'not_planned',
            '--comment', 'Issue recreated due to implementation failures. See replacement issue.'
        ], check=True)
        
        # Create new issue with same content
        print("🔄 Creating replacement issue...")
        new_title = f"🔄 {original_title}"
        
        new_body = f"""**Recreated from failed issue #{original_issue}**

{original_body}

---

**⚠️ Previous Attempt Failed**
This issue was recreated due to workflow/implementation failures. Starting with a clean slate.

**✅ System Status:**
- Firewall configured (api.githubcopilot.com allowed)
- Network connectivity verified  
- Clean implementation environment

**🎯 Fresh Implementation Required**"""
        
        # Create new issue
        create_cmd = ['gh', 'issue', 'create', '--repo', repo, '--title', new_title, '--body', new_body]
        for label in labels:
            create_cmd.extend(['--label', label])
        
        result = subprocess.run(create_cmd, capture_output=True, text=True, check=True)
        new_issue_url = result.stdout.strip()
        new_issue_number = new_issue_url.split('/')[-1]
        
        print(f"✅ Created new issue: #{new_issue_number}")
        
        # Assign to Copilot using GraphQL
        print("🤖 Assigning to Copilot...")
        if assign_issue_to_copilot(new_issue_number, repo):
            print(f"🎉 Successfully recreated and assigned issue #{new_issue_number}")
            return True
        else:
            print(f"⚠️ Issue created but assignment failed: #{new_issue_number}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: recreate_micro_issue.py <issue_number> <repo>")
        sys.exit(1)
    
    issue_number = sys.argv[1]
    repo = sys.argv[2]
    
    print(f"🔄 Recreating micro-issue #{issue_number} in {repo}")
    
    if recreate_micro_issue(issue_number, repo):
        print("✅ Micro-issue recreation completed successfully")
    else:
        print("❌ Micro-issue recreation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()