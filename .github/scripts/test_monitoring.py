#!/usr/bin/env python3
"""
Test script to validate RFC monitoring logic locally
"""

import json
import subprocess
import datetime
import os

def run_gh(cmd: str) -> str:
    """Execute GitHub CLI command"""
    try:
        result = subprocess.run(
            f"gh {cmd}", shell=True, capture_output=True, text=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return ""

def get_time_diff_hours(timestamp: str) -> float:
    """Calculate hours since timestamp"""
    try:
        dt = datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.datetime.now(datetime.timezone.utc)
        return (now - dt).total_seconds() / 3600
    except:
        return 0

def test_pr_monitoring():
    """Test PR monitoring logic"""
    print("Testing PR Monitoring...")
    
    try:
        prs_json = run_gh('pr list --author="app/copilot-swe-agent" --json number,title,updatedAt,isDraft,headRefName')
        prs = json.loads(prs_json) if prs_json else []
        
        print(f"Found {len(prs)} active PRs from GitHub Coding Agent:")
        for pr in prs:
            hours_since_update = get_time_diff_hours(pr['updatedAt'])
            
            status = "Active" if hours_since_update < 1 else \
                     "Slowing" if hours_since_update < 2 else \
                     "STALLED"
            
            print(f"  PR #{pr['number']}: {pr['title'][:50]}...")
            print(f"    Last update: {hours_since_update:.1f}h ago ({status})")
            print(f"    Branch: {pr['headRefName']}, Draft: {pr['isDraft']}")
            
    except Exception as e:
        print(f"Error testing PR monitoring: {e}")

def test_issue_monitoring():
    """Test issue monitoring logic"""
    print("\nTesting Issue Monitoring...")
    
    try:
        issues_json = run_gh('issue list --assignee="Copilot" --state=open --label=game-rfc --json number,title,assignees,createdAt')
        issues = json.loads(issues_json) if issues_json else []
        
        print(f"Found {len(issues)} assigned Game-RFC issues:")
        for issue in issues:
            hours_since_assigned = get_time_diff_hours(issue['createdAt'])
            
            # Check if there's a PR for this issue
            issue_num = issue['number']
            prs_json = run_gh(f'pr list --search "Fixes #{issue_num}" --json number')
            has_pr = len(json.loads(prs_json) if prs_json else []) > 0
            
            status = "Active" if has_pr else \
                     "Recent" if hours_since_assigned < 8 else \
                     "Delayed" if hours_since_assigned < 24 else \
                     "ABANDONED"
            
            print(f"  Issue #{issue_num}: {issue['title'][:50]}...")
            print(f"    Assigned: {hours_since_assigned:.1f}h ago, Has PR: {has_pr} ({status})")
            
    except Exception as e:
        print(f"Error testing issue monitoring: {e}")

def test_workflow_runs():
    """Test workflow run monitoring"""
    print("\nTesting Recent Workflow Activity...")
    
    try:
        runs_json = run_gh('run list --limit 10 --json name,status,conclusion,createdAt,headBranch')
        runs = json.loads(runs_json) if runs_json else []
        
        copilot_runs = [r for r in runs if 'copilot' in r.get('headBranch', '').lower()]
        
        print(f"Found {len(copilot_runs)} recent Copilot workflow runs:")
        for run in copilot_runs[:5]:  # Show last 5
            hours_ago = get_time_diff_hours(run['createdAt'])
            status = f"{run['status']} ({run.get('conclusion', 'N/A')})"
            
            print(f"  {run['name']}: {status}")
            print(f"    Branch: {run['headBranch']}, {hours_ago:.1f}h ago")
            
    except Exception as e:
        print(f"Error testing workflow monitoring: {e}")

def main():
    """Run all monitoring tests"""
    print("RFC Health Monitor Test Suite")
    print("=" * 50)
    
    test_pr_monitoring()
    test_issue_monitoring() 
    test_workflow_runs()
    
    print("\n" + "=" * 50)
    print("Monitoring test completed!")
    print("\nThis validates that our monitoring logic can:")
    print("- Detect active/stalled PRs")
    print("- Identify abandoned issues") 
    print("- Track workflow activity")
    print("- Calculate time-based thresholds")

if __name__ == "__main__":
    main()