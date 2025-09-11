#!/usr/bin/env python3
"""
Intelligent Game-RFC Issue Generator

Analyzes current project state and creates the next Game-RFC issue automatically.
This enables true end-to-end automation for GitHub Coding Agent workflows.
"""

import os
import re
import json
import glob
import subprocess
from pathlib import Path
from typing import Optional, Dict, List

class RfcIssueGenerator:
    def __init__(self):
        self.repo_root = Path(__file__).parent.parent.parent
        self.game_rfcs_dir = self.repo_root / "docs" / "game-rfcs"
        self.gh_token = os.environ.get('GITHUB_TOKEN')
        
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

    def get_completed_game_rfcs(self) -> List[int]:
        """Get list of completed Game-RFC numbers by checking closed issues"""
        try:
            # Get all closed issues with game-rfc label
            issues_json = self.run_gh_command(
                'issue list --state closed --label game-rfc --json number,title,state'
            )
            issues = json.loads(issues_json) if issues_json else []
            
            completed_rfcs = []
            for issue in issues:
                # Extract RFC number from title like "Implement Game-RFC-001: Console Game Shell"
                title = issue.get('title', '')
                match = re.search(r'Game-RFC-(\d+)', title)
                if match:
                    completed_rfcs.append(int(match.group(1)))
                    
            return sorted(completed_rfcs)
        except Exception as e:
            print(f"Error getting completed RFCs: {e}")
            return []

    def get_in_progress_game_rfcs(self) -> List[int]:
        """Get list of in-progress Game-RFC numbers by checking open issues"""
        try:
            # Get all open issues with game-rfc label
            issues_json = self.run_gh_command(
                'issue list --state open --label game-rfc --json number,title,state'
            )
            issues = json.loads(issues_json) if issues_json else []
            
            in_progress_rfcs = []
            for issue in issues:
                title = issue.get('title', '')
                match = re.search(r'Game-RFC-(\d+)', title)
                if match:
                    in_progress_rfcs.append(int(match.group(1)))
                    
            return sorted(in_progress_rfcs)
        except Exception as e:
            print(f"Error getting in-progress RFCs: {e}")
            return []

    def get_available_rfc_specs(self) -> Dict[int, Path]:
        """Get available RFC specification files"""
        rfc_specs = {}
        
        # Find all RFC-XXX-*.md files
        rfc_pattern = self.game_rfcs_dir / "RFC-*.md"
        for rfc_file in glob.glob(str(rfc_pattern)):
            rfc_path = Path(rfc_file)
            # Extract RFC number from filename like "RFC-002-Paddle-Implementation.md"
            match = re.search(r'RFC-(\d+)', rfc_path.name)
            if match:
                rfc_number = int(match.group(1))
                rfc_specs[rfc_number] = rfc_path
                
        return rfc_specs

    def parse_rfc_metadata(self, rfc_file: Path) -> Dict:
        """Parse RFC file to extract metadata"""
        try:
            content = rfc_file.read_text(encoding='utf-8')
            
            # Extract title from first heading
            title_match = re.search(r'^# Game-RFC-\d+:\s*(.+)', content, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else "Unknown Feature"
            
            # Extract dependencies
            deps_match = re.search(r'\*\*Dependencies\*\*:\s*(.+)', content)
            dependencies_text = deps_match.group(1) if deps_match else ""
            
            # Parse dependencies to find required RFC numbers
            dep_numbers = []
            for match in re.finditer(r'Game-RFC-(\d+)', dependencies_text):
                dep_numbers.append(int(match.group(1)))
            
            # Extract priority
            priority_match = re.search(r'\*\*Priority\*\*:\s*(\w+)', content)
            priority = priority_match.group(1) if priority_match else "Medium"
            
            return {
                'title': title,
                'dependencies': dep_numbers,
                'priority': priority,
                'file_path': str(rfc_file.relative_to(self.repo_root))
            }
        except Exception as e:
            print(f"Error parsing RFC {rfc_file}: {e}")
            return {
                'title': 'Unknown Feature',
                'dependencies': [],
                'priority': 'Medium',
                'file_path': str(rfc_file.relative_to(self.repo_root))
            }

    def find_next_rfc_to_implement(self) -> Optional[Dict]:
        """Find the next RFC that should be implemented"""
        completed_rfcs = set(self.get_completed_game_rfcs())
        in_progress_rfcs = set(self.get_in_progress_game_rfcs())
        available_specs = self.get_available_rfc_specs()
        
        print(f"📊 RFC Status Analysis:")
        print(f"   Completed RFCs: {sorted(completed_rfcs)}")
        print(f"   In Progress RFCs: {sorted(in_progress_rfcs)}")
        print(f"   Available Specs: {sorted(available_specs.keys())}")
        
        # Find RFCs that are ready to implement
        candidates = []
        for rfc_num, rfc_file in available_specs.items():
            # Skip if already completed or in progress
            if rfc_num in completed_rfcs or rfc_num in in_progress_rfcs:
                continue
                
            # Parse metadata to check dependencies
            metadata = self.parse_rfc_metadata(rfc_file)
            metadata['number'] = rfc_num
            
            # Check if all dependencies are completed
            deps_satisfied = all(dep in completed_rfcs for dep in metadata['dependencies'])
            
            if deps_satisfied:
                candidates.append(metadata)
                print(f"   ✅ RFC-{rfc_num:03d} ({metadata['title']}) - Ready (deps: {metadata['dependencies']})")
            else:
                missing_deps = [dep for dep in metadata['dependencies'] if dep not in completed_rfcs]
                print(f"   ⏳ RFC-{rfc_num:03d} ({metadata['title']}) - Waiting (missing deps: {missing_deps})")
        
        if not candidates:
            print("   🎉 No more RFCs to implement - series may be complete!")
            return None
        
        # Sort by RFC number (implement in order) and priority
        candidates.sort(key=lambda x: (x['number'], x['priority'] != 'High'))
        
        next_rfc = candidates[0]
        print(f"   🎯 Next RFC to implement: RFC-{next_rfc['number']:03d} ({next_rfc['title']})")
        
        return next_rfc

    def create_game_rfc_issue(self, rfc_metadata: Dict) -> str:
        """Create GitHub issue for the next Game-RFC"""
        rfc_num = rfc_metadata['number']
        title = rfc_metadata['title']
        file_path = rfc_metadata['file_path']
        dependencies = rfc_metadata['dependencies']
        priority = rfc_metadata['priority']
        
        # Format dependencies status
        dep_status = []
        if dependencies:
            completed_rfcs = set(self.get_completed_game_rfcs())
            for dep in dependencies:
                status = "✅ COMPLETED" if dep in completed_rfcs else "❌ PENDING"
                dep_status.append(f"- Game-RFC-{dep:03d}: {status}")
            deps_text = "\\n".join(dep_status)
        else:
            deps_text = "None (foundation RFC)"
        
        # Create comprehensive issue body
        issue_body = f"""## 📋 Auto-Generated Game-RFC Implementation

**RFC Specification**: `{file_path}`
**Priority**: {priority}
**Auto-Generated**: This issue was created automatically by the RFC progression workflow

### **📚 Implementation Requirements**

Please implement Game-RFC-{rfc_num:03d} according to the specification in `{file_path}`.

### **🔗 Dependencies**
{deps_text}

### **🎯 Assignment**
@copilot please implement this Game-RFC according to the specification.

### **🔧 Implementation Guidelines**
- Follow the acceptance criteria in the RFC specification
- Use the architecture patterns from previous Game-RFCs
- Ensure no regression in existing functionality
- Create PR with title: `Implement Game-RFC-{rfc_num:03d}: {title}`
- Include `Fixes #[this-issue-number]` in PR description

### **✅ Definition of Done**
- All acceptance criteria from RFC specification completed
- Code compiles without warnings
- Feature works as demonstrated manually
- Follows project conventions (see AGENTS.md)
- Ready for next Game-RFC implementation

---

**🤖 Generated by RFC Automation Workflow**"""

        # Create the issue
        issue_title = f"Implement Game-RFC-{rfc_num:03d}: {title}"
        
        try:
            # Create issue with proper escaping for shell command
            issue_body_escaped = issue_body.replace('"', '\\"').replace('`', '\\`')
            cmd = f'issue create --title "{issue_title}" --body "{issue_body_escaped}" --label game-rfc --assignee Copilot'
            
            result = self.run_gh_command(cmd)
            
            # Extract issue URL from result
            issue_url = result.strip() if result else "Unknown"
            
            print(f"✅ Created issue: {issue_url}")
            return issue_url
            
        except Exception as e:
            print(f"❌ Error creating issue: {e}")
            raise

    def run(self) -> bool:
        """Main execution - analyze state and create next RFC issue if needed"""
        print("🔍 Analyzing current Game-RFC state...")
        
        try:
            next_rfc = self.find_next_rfc_to_implement()
            
            if next_rfc is None:
                print("🎉 No more Game-RFCs to implement - series complete or all in progress!")
                return True
            
            print(f"🚀 Creating issue for Game-RFC-{next_rfc['number']:03d}...")
            issue_url = self.create_game_rfc_issue(next_rfc)
            
            print(f"✅ Successfully created next Game-RFC issue: {issue_url}")
            return True
            
        except Exception as e:
            print(f"❌ Error in RFC issue generation: {e}")
            return False

def main():
    """Entry point for the script"""
    if not os.environ.get('GITHUB_TOKEN'):
        print("❌ Error: GITHUB_TOKEN environment variable is required")
        return False
    
    generator = RfcIssueGenerator()
    success = generator.run()
    
    if success:
        print("🎯 RFC issue generation completed successfully")
    else:
        print("💥 RFC issue generation failed")
        exit(1)

if __name__ == "__main__":
    main()