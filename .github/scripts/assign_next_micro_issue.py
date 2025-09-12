#!/usr/bin/env python3
"""
Auto-assign next micro-issue after PR merge
"""
import os
import re
import json
import subprocess
import sys
import urllib.parse

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
    """Find the next micro-issue in sequence with robust matching.

    Tries a paginated local list first, then falls back to server-side search.
    Matches both padded and unpadded RFC numbers, with optional colon or hyphen.
    """
    padded = f"{rfc_num:03d}"
    rx = rf"Game-RFC-(?:{rfc_num}|{padded})-{next_micro}(?:\b|:|\s-)"

    # 1) Local list with higher limit
    issues = run_gh_command(['issue', 'list', '--repo', repo, '--state', 'open', '--limit', '200', '--json', 'number,title'])
    if issues:
        for issue in issues:
            title = issue.get('title', '')
            if re.search(rx, title):
                return issue['number']

    # 2) Fallback to API search (exact phrases)
    candidates = [
        f'"Game-RFC-{rfc_num}-{next_micro}:"',
        f'"Game-RFC-{padded}-{next_micro}:"',
        f'"Game-RFC-{rfc_num}-{next_micro} "',
        f'"Game-RFC-{padded}-{next_micro} "',
    ]
    for phrase in candidates:
        q = f"repo:{repo} is:issue is:open in:title {phrase}"
        encoded = urllib.parse.quote(q, safe='')
        data = run_gh_command(['api', f'/search/issues?q={encoded}'])
        items = (data or {}).get('items', [])
        if items:
            return items[0]['number']

    return None


def assign_issue(issue_number, repo):
    """Assign issue to Copilot via GraphQL addAssigneesToAssignable, per docs.

    Finds the issue node id and the Copilot assignee id from assignableUsers,
    then adds Copilot as an assignee using GraphQL.
    """
    # Resolve issue node id
    issue = run_gh_command(['issue', 'view', str(issue_number), '--repo', repo, '--json', 'id'])
    if not issue or 'id' not in issue:
        print(f"Failed to resolve issue node id for #{issue_number}")
        return False
    assignable_id = issue['id']
    print(f"Issue node id: {assignable_id}")

    # Resolve Copilot id using suggestedActors (per official docs)
    try:
        owner, name = repo.split('/')
    except ValueError:
        print(f"Invalid repo format: {repo}")
        return False

    # Query assignableUsers from repository to find Copilot
    q = f'''
    query {{
      repository(owner: "{owner}", name: "{name}") {{
        assignableUsers(first: 100) {{
          nodes {{ __typename login id }}
        }}
      }}
    }}
    '''
    
    try:
        result = subprocess.run(
            ['gh','api','graphql','-f',f'query={q}'],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        assignable_users = (
            data.get('data', {})
             .get('repository', {})
             .get('assignableUsers', {})
             .get('nodes', [])
        )
        
        copilot_id = None
        # Look for Copilot in assignable users
        for user in assignable_users:
            login = user.get('login', '')
            if login in ['Copilot', 'copilot-swe-agent', 'github-copilot']:
                copilot_id = user.get('id')
                print(f"Found Copilot in assignableUsers: login={login} id={copilot_id}")
                break
        
        if not copilot_id:
            print(f"Could not locate Copilot in assignableUsers. Available users: {[u.get('login') for u in assignable_users]}")
            print("Trying to find Copilot ID from existing assignments...")
            
            # Try to get Copilot ID from recently assigned issues
            try:
                # Check recent issues for Copilot assignments
                issues_data = run_gh_command(['issue', 'list', '--repo', repo, '--state', 'all', '--limit', '20', '--json', 'number,assignees'])
                if issues_data:
                    for issue in issues_data:
                        for assignee in issue.get('assignees', []):
                            if assignee.get('login') in ['Copilot', 'copilot-swe-agent', 'github-copilot']:
                                copilot_id = assignee.get('id')
                                print(f"Found Copilot ID from issue #{issue['number']}: {copilot_id}")
                                break
                        if copilot_id:
                            break
            except Exception as e:
                print(f"Could not search existing assignments: {e}")
            
            # Final fallback to known ID
            if not copilot_id:
                copilot_id = "BOT_kgDOC9w8XQ"  # Last resort fallback
                print(f"Using fallback Copilot ID: {copilot_id}")
    except subprocess.CalledProcessError as e:
        print(f"GraphQL assignableUsers query failed: {e.stderr}")
        return False
    except json.JSONDecodeError:
        print("Invalid JSON from assignableUsers query")
        return False

    # Perform replaceActorsForAssignable mutation (direct format - no variables)
    mutation = f'''
    mutation {{
      replaceActorsForAssignable(input: {{
        assignableId: "{assignable_id}"
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
    try:
        result = subprocess.run(
            ['gh','api','graphql','-f',f'query={mutation}'],
            capture_output=True, text=True, check=True
        )
        data = json.loads(result.stdout)
        ok = data.get('data',{}).get('replaceActorsForAssignable')
        if ok:
            assignees = ok['assignable']['assignees']['nodes']
            print(f"Assigned via GraphQL. Assignees: {[a['login'] for a in assignees]}")
            return True
        print(f"GraphQL replaceActorsForAssignable returned no data: {data}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"GraphQL mutation failed: {e.stderr}")
        return False
    except json.JSONDecodeError:
        print("Invalid JSON from mutation")
        return False

def add_progression_comment(issue_number, repo, prev_issue, rfc_num, current_micro, next_micro, pr_number):
    """Add progression comment to the newly assigned issue"""
    comment = f"""🔄 **Auto-assigned from micro-issue progression**

Previous micro-issue #{prev_issue} completed: Game-RFC-{rfc_num:03d}-{current_micro}
This is the next sequential task: Game-RFC-{rfc_num}-{next_micro} (tolerant match)

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
    print(f"🔍 Looking for next micro-issue: Game-RFC-{rfc_num}-{next_micro} (tolerant match)")
    
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
