#!/usr/bin/env python3
"""
Auto-assign next micro-issue after PR merge
"""
import os
import re
import json
import subprocess
import sys

def run_gh_command(args):
    """Run gh CLI command and return JSON result"""
    try:
        cmd = ['gh'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout) if result.stdout.strip() else None
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return None
    except json.JSONDecodeError:
        print(f"Invalid JSON from command: {' '.join(cmd)}")
        return None

def run_gh_command_text(args):
    """Run gh CLI command and return text result"""
    try:
        cmd = ['gh'] + args
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}")
        print(f"Error: {e.stderr}")
        return None

def find_closed_issue(pr_number, repo):
    """Find the issue that was closed by this PR"""
    # Get PR details
    pr_data = run_gh_command(['pr', 'view', str(pr_number), '--repo', repo, '--json', 'body,title'])
    if not pr_data:
        return None
        
    pr_body = pr_data.get('body', '')
    pr_title = pr_data.get('title', '')
    
    print(f"PR Title: {pr_title}")
    
    # Look for issue reference in PR body (Fixes #123, Closes #456, etc.)
    for text in [pr_body, pr_title]:
        if text:
            match = re.search(r'(?:close[sd]?|fixe?[sd]?|resolve[sd]?)\s+#(\d+)', text, re.IGNORECASE)
            if match:
                return int(match.group(1))
    
    # Try to find issue by matching Game-RFC pattern in title
    match = re.search(r'Game-RFC-(\d+)-(\d+)', pr_title)
    if match:
        rfc_pattern = f"Game-RFC-{match.group(1)}-{match.group(2)}"
        # Find issue with this pattern
        issues = run_gh_command(['issue', 'list', '--repo', repo, '--state', 'all', '--json', 'number,title'])
        if issues:
            for issue in issues:
                if rfc_pattern in issue.get('title', ''):
                    return issue['number']
    
    return None

def extract_rfc_info(issue_number, repo):
    """Extract RFC and micro-issue numbers from issue title"""
    issue_data = run_gh_command(['issue', 'view', str(issue_number), '--repo', repo, '--json', 'title'])
    if not issue_data:
        return None, None
        
    title = issue_data.get('title', '')
    print(f"Issue #{issue_number}: {title}")
    
    match = re.search(r'Game-RFC-(\d+)-(\d+)', title)
    if match:
        return int(match.group(1)), int(match.group(2))
    
    return None, None

def find_next_micro_issue(rfc_num, next_micro, repo):
    """Find the next micro-issue in sequence"""
    issues = run_gh_command(['issue', 'list', '--repo', repo, '--state', 'open', '--json', 'number,title'])
    if not issues:
        return None
        
    pattern = f"Game-RFC-{rfc_num:03d}-{next_micro}:"
    for issue in issues:
        title = issue.get('title', '')
        if pattern in title:
            return issue['number']
    
    return None


def assign_issue(issue_number, repo):
    """Assign issue to Copilot using correct GraphQL mutation"""
    # Get the issue's node ID
    try:
        issue_data = run_gh_command(['issue', 'view', str(issue_number), '--repo', repo, '--json', 'id'])
        if not issue_data:
            print(f"Could not get issue #{issue_number} details")
            return False
        issue_node_id = issue_data['id']
        print(f"Issue #{issue_number} node ID: {issue_node_id}")
    except Exception as e:
        print(f"Failed to get issue node ID: {e}")
        return False
    
    # First, query for suggested actors to get Copilot's ID
    try:
        query = f'''
        query {{
          node(id: "{issue_node_id}") {{
            ... on Issue {{
              suggestedActors(first: 10) {{
                nodes {{
                  ... on User {{ login id }}
                  ... on Bot {{ login id }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={query}'], 
                              capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        
        # Find copilot-swe-agent in suggested actors
        copilot_id = None
        if data.get('data', {}).get('node', {}).get('suggestedActors', {}).get('nodes'):
            for actor in data['data']['node']['suggestedActors']['nodes']:
                if actor.get('login') == 'copilot-swe-agent':
                    copilot_id = actor.get('id')
                    print(f"Found Copilot actor ID: {copilot_id}")
                    break
        
        if not copilot_id:
            print("Copilot not found in suggested actors")
            return False
            
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Failed to get suggested actors: {e}")
        return False
    
    # Now assign using replaceActorsForAssignable mutation
    try:
        mutation = f'''
        mutation {{
          replaceActorsForAssignable(input: {{
            assignableId: "{issue_node_id}"
            actorIds: ["{copilot_id}"]
          }}) {{
            assignable {{
              ... on Issue {{
                number
                assignees(first: 10) {{
                  nodes {{
                    login
                  }}
                }}
              }}
            }}
          }}
        }}
        '''
        
        result = subprocess.run(['gh', 'api', 'graphql', '-f', f'query={mutation}'], 
                              capture_output=True, text=True, check=True)
        
        data = json.loads(result.stdout)
        if data.get('data', {}).get('replaceActorsForAssignable'):
            assignees = data['data']['replaceActorsForAssignable']['assignable']['assignees']['nodes']
            assigned_logins = [a['login'] for a in assignees]
            print(f"Successfully assigned issue #{issue_number}. Assignees: {assigned_logins}")
            return True
        else:
            print(f"replaceActorsForAssignable mutation failed: {data}")
            return False
            
    except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
        print(f"Failed to assign via replaceActorsForAssignable: {e}")
        return False

def add_progression_comment(issue_number, repo, prev_issue, rfc_num, current_micro, next_micro, pr_number):
    """Add progression comment to the newly assigned issue"""
    comment = f"""🔄 **Auto-assigned from micro-issue progression**

Previous micro-issue #{prev_issue} completed: Game-RFC-{rfc_num:03d}-{current_micro}
This is the next sequential task: Game-RFC-{rfc_num:03d}-{next_micro}

**Auto-progression**: Assigned after PR #{pr_number} was merged."""
    
    try:
        subprocess.run(['gh', 'issue', 'comment', str(issue_number), '--repo', repo, '--body', comment], 
                      capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    repo = os.environ.get('REPO')
    pr_number = os.environ.get('PR_NUMBER')
    
    if not repo or not pr_number:
        print("❌ Missing required environment variables REPO or PR_NUMBER")
        sys.exit(1)
    
    print(f"🔄 Auto-assigning next micro-issue after PR #{pr_number} merge")
    
    # Find which issue was closed by this PR
    closed_issue = find_closed_issue(pr_number, repo)
    if not closed_issue:
        print("❌ Could not determine which issue was closed by this PR")
        sys.exit(0)
    
    print(f"✅ Found closed issue: #{closed_issue}")
    
    # Extract RFC and micro-issue numbers
    rfc_num, current_micro = extract_rfc_info(closed_issue, repo)
    if not rfc_num or not current_micro:
        print("❌ Could not parse RFC pattern from issue title")
        sys.exit(0)
    
    next_micro = current_micro + 1
    print(f"🔍 Looking for next micro-issue: Game-RFC-{rfc_num:03d}-{next_micro}")
    
    # Find next micro-issue
    next_issue = find_next_micro_issue(rfc_num, next_micro, repo)
    if not next_issue:
        print(f"ℹ️ No more micro-issues found for Game-RFC-{rfc_num:03d} sequence")
        sys.exit(0)
    
    print(f"✅ Found next micro-issue: #{next_issue}")
    
    # Assign to Copilot
    if assign_issue(next_issue, repo):
        print(f"✅ Successfully assigned issue #{next_issue}")
        
        # Add progression comment
        if add_progression_comment(next_issue, repo, closed_issue, rfc_num, current_micro, next_micro, pr_number):
            print("✅ Added progression comment")
        else:
            print("⚠️ Failed to add progression comment, but assignment succeeded")
    else:
        print(f"❌ Failed to assign issue #{next_issue} to Copilot")
        sys.exit(1)

if __name__ == "__main__":
    main()