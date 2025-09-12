#!/usr/bin/env python3
"""
Dynamic RFC Parser for Micro-Issue Generation
Automatically analyzes RFC structure to generate appropriate micro-issues
"""

import re
import os
from typing import List, Dict, Optional, NamedTuple
from dataclasses import dataclass
from pathlib import Path

@dataclass
class RFCSection:
    title: str
    level: int  # H2=2, H3=3, H4=4
    content: str
    subsections: List['RFCSection']
    line_start: int
    line_end: int

@dataclass
class MicroIssueTemplate:
    title: str
    body: str
    dependencies: List[str]
    estimated_complexity: str  # "simple", "medium", "complex"
    files_expected: List[str]

class RFCParser:
    def __init__(self, rfc_path: str):
        self.rfc_path = Path(rfc_path)
        self.content = self.rfc_path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        
    def parse_structure(self) -> List[RFCSection]:
        """Parse RFC into hierarchical structure"""
        sections = []
        current_section = None
        
        for i, line in enumerate(self.lines):
            header_match = re.match(r'^(#{2,4})\s+(.+)', line)
            if header_match:
                level = len(header_match.group(1))
                title = header_match.group(2)
                
                if current_section:
                    current_section.line_end = i - 1
                
                current_section = RFCSection(
                    title=title,
                    level=level,
                    content="",
                    subsections=[],
                    line_start=i,
                    line_end=len(self.lines)
                )
                sections.append(current_section)
            elif current_section:
                current_section.content += line + "\n"
        
        if current_section:
            current_section.line_end = len(self.lines)
            
        return sections
    
    def identify_implementation_sections(self, sections: List[RFCSection]) -> List[RFCSection]:
        """Identify sections that represent implementable components"""
        implementation_sections = []
        
        for section in sections:
            # Include Game-RFC micro-issue sections (pattern: Game-RFC-XXX-N: Title)
            import re
            if re.match(r'Game-RFC-\d+-\d+:', section.title):
                implementation_sections.append(section)
                continue
            
            # Look for implementation keywords
            impl_keywords = [
                'object model', 'class', 'system', 'implementation', 
                'integration', 'component', 'service', 'manager'
            ]
            
            if any(keyword in section.title.lower() for keyword in impl_keywords):
                implementation_sections.append(section)
            
            # Look for code blocks (likely implementation specs)
            if '```' in section.content:
                implementation_sections.append(section)
                
        return implementation_sections
    
    def extract_file_paths(self, section: RFCSection) -> List[str]:
        """Extract expected file paths from section content"""
        file_patterns = [
            r'`([^`]+\.cs)`',  # C# files in backticks
            r'\*\*File\*\*:\s*`([^`]+)`',  # **File**: `path`
            r'dotnet/[^\s`]+\.cs',  # Direct dotnet paths
        ]
        
        files = []
        for pattern in file_patterns:
            matches = re.findall(pattern, section.content)
            files.extend(matches)
            
        return list(set(files))  # Remove duplicates
    
    def estimate_complexity(self, section: RFCSection) -> str:
        """Estimate implementation complexity based on section content"""
        content = section.content.lower()
        
        # Count complexity indicators
        complexity_indicators = {
            'simple': ['class', 'property', 'model', 'enum'],
            'medium': ['method', 'system', 'integration', 'collision'],
            'complex': ['algorithm', 'physics', 'optimization', 'performance']
        }
        
        scores = {'simple': 0, 'medium': 0, 'complex': 0}
        
        for complexity, indicators in complexity_indicators.items():
            for indicator in indicators:
                scores[complexity] += content.count(indicator)
        
        # Determine based on highest score
        max_score = max(scores.values())
        if max_score == 0:
            return 'simple'
        
        for complexity, score in scores.items():
            if score == max_score:
                return complexity
        
        return 'simple'
    
    def generate_micro_issues(self, rfc_number: str) -> List[MicroIssueTemplate]:
        """Generate micro-issues from RFC structure"""
        sections = self.parse_structure()
        
        # For Game-RFC documents, only include actual micro-issue sections
        if rfc_number.startswith('Game-RFC-'):
            import re
            impl_sections = [s for s in sections if re.match(r'Game-RFC-\d+-\d+:', s.title)]
        else:
            impl_sections = self.identify_implementation_sections(sections)
        
        micro_issues = []
        
        for i, section in enumerate(impl_sections, 1):
            # Generate title - use section title directly for Game-RFC
            if rfc_number.startswith('Game-RFC-'):
                title = section.title
            else:
                title = f"{rfc_number}-{i}: {section.title}"
            
            # Extract file paths
            files = self.extract_file_paths(section)
            
            # Estimate complexity
            complexity = self.estimate_complexity(section)
            
            # Generate body with RFC reference
            body = self._generate_issue_body(rfc_number, section, files, complexity)
            
            # Determine dependencies (first issue has none, others depend on first)
            dependencies = [f"{rfc_number}-1"] if i > 1 else []
            
            micro_issue = MicroIssueTemplate(
                title=title,
                body=body,
                dependencies=dependencies,
                estimated_complexity=complexity,
                files_expected=files
            )
            
            micro_issues.append(micro_issue)
        
        return micro_issues
    
    def _generate_issue_body(self, rfc_number: str, section: RFCSection, files: List[str], complexity: str) -> str:
        """Generate standardized issue body"""
        
        # Extract code blocks for context
        code_blocks = re.findall(r'```[\w]*\n(.*?)\n```', section.content, re.DOTALL)
        
        body = f"""@copilot Please implement the {section.title} from {self.rfc_path.name}.

## Scope
{section.title} as specified in the RFC document.

## Implementation Reference
**RFC Document**: `{self.rfc_path.name}`
**Section**: {section.title}
**Complexity**: {complexity.title()}

## Key Requirements
{self._extract_requirements(section.content)}

## Files Expected"""

        if files:
            for file_path in files[:5]:  # Limit to 5 files to avoid clutter
                body += f"\n- `{file_path}`"
        else:
            body += f"\n- Files as specified in the RFC section"

        body += f"""

## Definition of Done
- [ ] Implementation matches RFC specifications
- [ ] Code compiles without warnings
- [ ] Basic functionality working
- [ ] Integration tests pass (if applicable)

**Parent RFC**: {rfc_number}
**Dependencies**: {', '.join(section.title for section in []) if hasattr(section, 'dependencies') else 'None'}

---
*This micro-issue was automatically generated from RFC structure analysis*"""

        return body
    
    def _extract_requirements(self, content: str) -> str:
        """Extract key requirements from section content"""
        lines = content.split('\n')
        requirements = []
        
        for line in lines:
            line = line.strip()
            # Look for bullet points, numbered lists, or key statements
            if (line.startswith(('- ', '* ', '1. ', '2. ')) or 
                'must' in line.lower() or 
                'should' in line.lower() or
                'implement' in line.lower()):
                requirements.append(line)
        
        if requirements:
            return '\n'.join(requirements[:5])  # First 5 requirements
        else:
            # Fallback: first few sentences
            sentences = content.split('. ')
            return '. '.join(sentences[:2]) + '.'

# Example usage functions
def parse_rfc_004() -> List[MicroIssueTemplate]:
    """Parse Game-RFC-004 dynamically"""
    parser = RFCParser('docs/game-rfcs/RFC-004-Brick-System.md')
    return parser.generate_micro_issues('Game-RFC-004')

def parse_any_rfc(rfc_path: str, rfc_number: str) -> List[MicroIssueTemplate]:
    """Parse any RFC dynamically"""
    parser = RFCParser(rfc_path)
    return parser.generate_micro_issues(rfc_number)

if __name__ == '__main__':
    # Test with RFC-004
    templates = parse_rfc_004()
    
    print(f"Generated {len(templates)} micro-issues from RFC-004:")
    for template in templates:
        print(f"- {template.title} ({template.estimated_complexity})")
        print(f"  Files: {template.files_expected}")
        print(f"  Dependencies: {template.dependencies}")
        print()