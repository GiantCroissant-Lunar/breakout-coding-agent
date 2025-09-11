# GitHub Actions YAML Debugging Guide

## Issue Discovered: 2025-09-11

When GitHub Actions workflows fail immediately (0s duration), it's usually a YAML syntax error, not a logic error.

## Common Symptoms
- Workflow runs show "conclusion":"action_required" 
- Immediate failure with 0s duration
- Error message: "This run likely failed because of a workflow file issue"

## Root Cause: Multiline String Indentation Issues

### ❌ Problem Pattern 1: HERE Documents in YAML
```yaml
# This breaks YAML parsing:
- name: Comment on PR
  run: |
    gh pr comment "$PR_NUMBER" --body @- <<EOF
    Hi! This is a multiline message.
    
    It spans multiple lines.
    EOF
```

### ✅ Solution 1: Single Line Strings
```yaml
# This works:
- name: Comment on PR  
  run: |
    gh pr comment "$PR_NUMBER" --body "Hi! This is a single line message. It contains all the content in one line."
```

### ❌ Problem Pattern 2: Multiline f-strings in Python
```yaml
# This breaks YAML parsing:
run: |
  python3 << 'EOF'
  comment = f"""This is a multiline
  
  f-string that spans
  multiple lines"""
  EOF
```

### ✅ Solution 2: Single Line f-strings
```yaml
# This works:
run: |
  python3 << 'EOF'
  comment = f"This is a single line f-string with all content in one line."
  EOF
```

### ❌ Problem Pattern 3: Missing Newlines
```yaml
# File ending without newline can cause issues
env:
  GH_TOKEN: ${{ secrets.TOKEN }}[EOF - no newline]
```

### ✅ Solution 3: Ensure Final Newline
```yaml
# File ending with proper newline
env:
  GH_TOKEN: ${{ secrets.TOKEN }}

```

## Debugging Process

1. **Check YAML Syntax Locally**:
   ```bash
   python -c "import yaml; yaml.safe_load(open('.github/workflows/file.yml', 'r', encoding='utf-8'))"
   ```

2. **Look for Error Line Numbers**: The error usually points to the line where YAML parsing fails

3. **Check for Multiline Strings**: Look for `"""`, `<<EOF`, or multiline patterns

4. **Verify File Endings**: Ensure files end with newlines

## Key Lesson

**The issue was NOT Unicode emojis** (as initially suspected). Many GitHub Actions workflows successfully use emojis. The issue was **multiline string indentation** breaking YAML parsing.

## Fixed Files

- `.github/workflows/auto-merge.yml` - Fixed HERE document syntax
- `.github/workflows/rfc-health-monitor.yml` - Fixed multiline f-strings and missing newline

## Verification

After fixes, workflows went from immediate 0s failures to successful execution:
- RFC Health Monitor: ✅ 11s successful run
- Auto-merge: ✅ Ready for testing on next PR

## Prevention

1. Always test YAML syntax locally before committing
2. Prefer single-line strings in workflow scripts  
3. Use `\\n` for line breaks instead of actual line breaks in Python strings
4. Ensure all workflow files end with newlines