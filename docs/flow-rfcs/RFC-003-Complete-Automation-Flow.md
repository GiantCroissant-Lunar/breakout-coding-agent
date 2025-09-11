# Flow-RFC-003: Complete Automation Flow

## Problem Statement

**Critical Gap**: The automation workflow is missing the **issue generation** component. While GitHub Coding Agent can implement features and auto-merge works, there's no automated mechanism to create the next Game-RFC issue when the previous one completes.

**Current Broken Flow**:
1. ✅ Human manually creates Game-RFC-001 issue  
2. ✅ GitHub Coding Agent implements → PR → Auto-merge
3. ❌ **MANUAL GAP**: Human must manually create Game-RFC-002 issue
4. ❌ Breaks the "autonomous development cycle" experiment goal

## Root Cause Analysis

### **What Works**
- ✅ GitHub Coding Agent activation (when issue is assigned to Copilot)
- ✅ Implementation and PR creation
- ✅ Auto-merge workflow (Flow-RFC-002 fix)
- ✅ Branch cleanup and issue closure

### **What's Missing**
- ❌ **Automatic issue generation** for next RFC in sequence
- ❌ **Sequential RFC progression** without human intervention
- ❌ **Complete end-to-end automation** as intended by experiment

### **Why This Matters**
The experiment's core hypothesis is: *"GitHub Coding Agent can complete full development cycles autonomously"*

**Without automated issue generation**, the experiment cannot validate this hypothesis because human intervention is required at every step.

## Proposed Solutions

### **Option 1: Workflow-Driven Issue Creation**
**Approach**: Enhance auto-merge workflow to create next Game-RFC issue upon completion

```yaml
- name: Create next Game-RFC issue
  if: contains(github.event.pull_request.title, 'Game-RFC-')
  run: |
    # Extract current RFC number
    CURRENT_RFC=$(echo "$PR_TITLE" | grep -o 'Game-RFC-[0-9]\+' | grep -o '[0-9]\+')
    NEXT_RFC=$((CURRENT_RFC + 1))
    
    # Check if next RFC specification exists
    if [ -f "docs/game-rfcs/RFC-$(printf %03d $NEXT_RFC)*.md" ]; then
      # Create issue for next RFC
      gh issue create --title "Implement Game-RFC-$(printf %03d $NEXT_RFC): [Feature]" \
        --body "Auto-generated issue for next Game-RFC implementation" \
        --assignee Copilot --label game-rfc
    fi
```

**Benefits**:
- ✅ Fully automated progression
- ✅ Uses existing workflow infrastructure
- ✅ Respects RFC dependencies and sequencing

**Challenges**:
- Requires dynamic RFC title parsing
- Need error handling for missing specs
- Complex issue template generation

### **Option 2: GitHub Coding Agent Self-Management**
**Approach**: Instruct GitHub Coding Agent to create next issue upon completion

**Enhancement to AGENTS.md**:
```markdown
## Post-Implementation Tasks
After successfully completing a Game-RFC:
1. Verify all acceptance criteria are met
2. Create issue for next Game-RFC in sequence
3. Assign issue to @Copilot for implementation
4. Reference previous RFC completion in issue body
```

**Benefits**:
- ✅ Leverages GitHub Coding Agent capabilities
- ✅ Natural progression within agent workflow
- ✅ Flexible and adaptive to project needs

**Challenges**:
- Depends on GitHub Coding Agent understanding instructions
- May require iteration to get working reliably
- Less predictable than workflow automation

### **Option 3: RFC Coordinator Issue Pattern**
**Approach**: Use RFC Coordinator issue as central command center

**Pattern**: Add comments to RFC Coordinator to trigger next implementations:
```markdown
## Ready for Implementation
@copilot please implement Game-RFC-002: Paddle Implementation

Reference: docs/game-rfcs/RFC-002-Paddle-Implementation.md
Dependencies: ✅ Game-RFC-001 (COMPLETED)
Previous: Closes #6 via PR #7
```

**Benefits**:
- ✅ Centralized coordination
- ✅ Clear audit trail
- ✅ Uses existing RFC Coordinator infrastructure

**Challenges**:
- Still requires human or workflow trigger
- May not scale to larger projects
- Mixing coordination with implementation

## Recommended Implementation

### **Phase 1: Workflow Enhancement (Recommended)**
Implement Option 1 - enhance auto-merge workflow to automatically create next Game-RFC issue:

```yaml
- name: Create next Game-RFC issue
  if: success() && contains(github.event.pull_request.title, 'Game-RFC-')
  run: |
    echo "🔄 Creating next Game-RFC issue..."
    
    # Extract current RFC number
    CURRENT_RFC=$(echo "${{ github.event.pull_request.title }}" | grep -o 'Game-RFC-[0-9]\+' | grep -o '[0-9]\+')
    NEXT_RFC=$(printf "%03d" $((10#$CURRENT_RFC + 1)))
    
    # Find next RFC specification
    RFC_FILE=$(find docs/game-rfcs/ -name "RFC-$NEXT_RFC-*.md" | head -1)
    
    if [ -n "$RFC_FILE" ]; then
      # Extract RFC title
      RFC_TITLE=$(basename "$RFC_FILE" .md | sed 's/RFC-[0-9]\+-//')
      
      # Create next issue
      gh issue create \
        --title "Implement Game-RFC-$NEXT_RFC: $RFC_TITLE" \
        --body "$(cat <<EOF
## 📋 Auto-Generated Game-RFC Implementation

**Previous RFC**: Game-RFC-$(printf "%03d" $CURRENT_RFC) completed via PR #${{ github.event.number }}
**Specification**: \`$RFC_FILE\`
**Status**: Ready for implementation

@copilot please implement this Game-RFC according to the specification.
EOF
)" \
        --assignee Copilot \
        --label game-rfc
        
      echo "✅ Created Game-RFC-$NEXT_RFC issue"
    else
      echo "ℹ️ No next Game-RFC specification found - series complete"
    fi
```

### **Phase 2: Validation**
1. Test workflow with Game-RFC-001 → Game-RFC-002 transition
2. Verify GitHub Coding Agent activates automatically
3. Confirm complete automation loop works

### **Phase 3: Iteration**
1. Refine workflow based on test results  
2. Add error handling and edge cases
3. Document complete automation process

## Success Criteria

### **Complete Automation Achieved When**:
- [ ] Game-RFC-001 completion automatically creates Game-RFC-002 issue
- [ ] GitHub Coding Agent activates without human intervention
- [ ] Game-RFC-002 → Game-RFC-003 → ... progression is fully automated
- [ ] Human only needs to initiate first Game-RFC-001 issue
- [ ] All 5 Game-RFCs can be completed without manual issue creation

### **Validation Test**:
1. **Baseline**: Manually create only Game-RFC-001 issue  
2. **Automation**: All subsequent Game-RFC issues created automatically
3. **Completion**: Game-RFC-005 completes with full Breakout game
4. **Verification**: Zero manual intervention after initial trigger

## Implementation Priority

**Critical**: This is the missing piece that prevents true validation of the experiment's core hypothesis.

**Dependencies**: 
- Flow-RFC-001 ✅ (workflow foundation)
- Flow-RFC-002 ✅ (auto-merge enabled)
- Game-RFC-001 ✅ (implementation foundation)

## Technical Considerations

### **RFC Specification Requirements**
All Game-RFC specifications must exist before automation can work:
- ✅ RFC-001-Console-Game-Shell.md
- ✅ RFC-002-Paddle-Implementation.md
- ❌ RFC-003-Ball-Physics.md (needs creation)
- ❌ RFC-004-Brick-System.md (needs creation)  
- ❌ RFC-005-Game-State-Management.md (needs creation)

### **Error Handling**
- Missing RFC specifications
- GitHub API rate limits
- Invalid RFC numbering
- Circular dependencies

### **Scaling Considerations**
- Works for sequential RFC dependencies
- May need enhancement for parallel RFCs
- Consider branch management for multiple active RFCs

## Impact Assessment

**Without Fix**:
- ❌ Experiment cannot validate core hypothesis
- ❌ Manual intervention required at every RFC transition
- ❌ No true "autonomous development cycle"

**With Fix**:
- ✅ True end-to-end automation validation
- ✅ Proves GitHub Coding Agent can manage full project lifecycle
- ✅ Establishes template for AI-driven development workflows
- ✅ Validates experiment's core value proposition

---

**Next Steps**: Implement workflow enhancement and test with Game-RFC-001 → Game-RFC-002 transition to validate complete automation flow.