#!/usr/bin/env python3
"""
PR Validation Script for Auto-merge Workflow

Validates Pull Requests for automatic merging based on RFC type and requirements.
More reliable than shell script with better error handling and GitHub API integration.
"""

import os
import sys
import json
import subprocess
import re
from typing import Optional, Dict, List

class PRValidator:
    def __init__(self):
        self.pr_number = os.environ.get('PR_NUMBER')
        self.repo = os.environ.get('GITHUB_REPOSITORY') 
        self.gh_token = os.environ.get('GITHUB_TOKEN')
        
        if not all([self.pr_number, self.repo, self.gh_token]):
            raise ValueError("Required environment variables: PR_NUMBER, GITHUB_REPOSITORY, GITHUB_TOKEN")
    
    def run_gh_command(self, cmd: str) -> str:
        """Execute GitHub CLI command and return output"""
        try:
            result = subprocess.run(
                f"gh {cmd}",
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                env={**os.environ, 'GITHUB_TOKEN': self.gh_token}
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error running 'gh {cmd}': {e}")
            print(f"stderr: {e.stderr}")
            raise
    
    def get_pr_details(self) -> Dict:
        """Get PR details using GitHub CLI"""
        try:
            pr_json = self.run_gh_command(
                f'pr view {self.pr_number} --repo {self.repo} --json title,body,closingIssuesReferences'
            )
            return json.loads(pr_json)
        except Exception as e:
            print(f"Failed to get PR details: {e}")
            raise
    
    def validate_flow_rfc_001(self, pr_details: Dict) -> bool:
        """Validate Flow-RFC-001 specific requirements"""
        print("🔍 Flow-RFC-001 PR detected - applying special validation")
        
        try:
            # Get files changed in this PR
            files_json = self.run_gh_command(
                f'api repos/{self.repo}/pulls/{self.pr_number}/files --jq ".[].filename"'
            )
            files_changed = files_json.strip().split('\n') if files_json else []
            
            # Validate only README.md changed
            if len(files_changed) > 1:
                print(f"❌ Too many files changed ({len(files_changed)}). Flow-RFC-001 should only change README.md")
                return False
            
            # Check if README.md was changed
            if 'README.md' not in files_changed:
                print("❌ README.md not changed. Flow-RFC-001 requires README.md update")
                return False
            
            print("✅ Flow-RFC-001 validation passed")
            return True
            
        except Exception as e:
            print(f"❌ Flow-RFC-001 validation failed: {e}")
            return False
    
    def validate_game_rfc(self, pr_details: Dict) -> bool:
        """Validate Game-RFC specific requirements"""
        print("🔍 Game-RFC PR detected - validating issue reference")
        
        # Check for closing issue references
        closing_refs = pr_details.get('closingIssuesReferences', [])
        if len(closing_refs) > 0:
            print(f"✅ PR properly references {len(closing_refs)} issue(s) via closing keywords")
            return True
        
        # No closing references found - provide helpful guidance
        print("❌ Game-RFC PRs must reference the implementation issue")
        
        title = pr_details.get('title', '')
        suggestion = self._generate_issue_suggestion(title)
        
        self._post_guidance_comment(suggestion)
        return False
    
    def _generate_issue_suggestion(self, title: str) -> str:
        """Generate specific issue suggestion based on RFC number in title"""
        # Extract RFC number from title
        rfc_match = re.search(r'Game-RFC-(\d+)', title)
        if not rfc_match:
            return "Fixes #<issue-number>"
        
        rfc_num = rfc_match.group(1)
        
        try:
            # Find matching open Game-RFC issue
            issues_json = self.run_gh_command(
                f'issue list --repo {self.repo} --state open --label game-rfc --json number,title'
            )
            issues = json.loads(issues_json) if issues_json else []
            
            for issue in issues:
                if f'Game-RFC-{rfc_num}' in issue.get('title', ''):
                    return f"Fixes #{issue['number']}"
            
        except Exception as e:
            print(f"Warning: Could not auto-detect issue number: {e}")
        
        return "Fixes #<issue-number>"
    
    def _post_guidance_comment(self, suggestion: str) -> None:
        """Post helpful guidance comment on PR"""
        comment_body = f"""Hi! This PR looks like a Game-RFC implementation but it doesn't reference its tracking issue. For full automation, please add a closing keyword to the PR description so the workflow can auto-merge it.

Add this line to the PR description:

**{suggestion}**

After updating, the Auto-merge workflow will re-run and merge automatically. Thanks!

---

🤖 *Automated guidance from PR validation workflow*"""
        
        try:
            self.run_gh_command(
                f'pr comment {self.pr_number} --repo {self.repo} --body "{comment_body}"'
            )
            print(f"✅ Posted guidance comment with suggestion: {suggestion}")
        except Exception as e:
            print(f"Warning: Could not post guidance comment: {e}")
    
    def validate(self) -> bool:
        """Main validation logic"""
        print(f"🔍 Validating PR #{self.pr_number} for auto-merge eligibility...")
        
        try:
            pr_details = self.get_pr_details()
            title = pr_details.get('title', '')
            
            print(f"Title: {title}")
            
            if 'Flow-RFC-001' in title:
                return self.validate_flow_rfc_001(pr_details)
            elif 'Game-RFC-' in title:
                return self.validate_game_rfc(pr_details)
            else:
                print("ℹ️ Not a recognized RFC PR, skipping auto-merge")
                return False
                
        except Exception as e:
            print(f"❌ PR validation failed with error: {e}")
            return False

def main():
    """Entry point for the script"""
    try:
        validator = PRValidator()
        success = validator.validate()
        
        if success:
            print("✅ PR validation completed successfully")
            sys.exit(0)
        else:
            print("❌ PR validation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"💥 PR validation script error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()