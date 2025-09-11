# GitHub App Setup Guide for Automated Copilot Assignment

## 🎯 Purpose

This guide explains how to set up a GitHub App to enable fully automated assignment of GitHub Coding Agent (`copilot-swe-agent`) to Game-RFC issues.

## 🔍 Problem Solved

**Previous Issue**: 
- `GITHUB_TOKEN` in Actions cannot assign to `copilot-swe-agent`
- Returns "user not found" or "invalid assignee" errors
- Required manual assignment: `gh issue edit X --add-assignee copilot-swe-agent`

**Solution**:
- GitHub App tokens have enhanced permissions
- Can successfully assign to special users like `copilot-swe-agent`
- Enables fully automated workflow: Issue Creation → Assignment → Implementation

## 📋 GitHub App Setup Steps

### Step 1: Create GitHub App (or Reuse Existing)

If you already have a GitHub App from `dungeon-coding-agent`, you can reuse it. Otherwise:

1. **Go to**: GitHub Settings → Developer settings → GitHub Apps
2. **Click**: "New GitHub App"
3. **App Name**: `RFC Automation Bot` (or similar)
4. **Homepage URL**: Your repository URL
5. **Webhook**: Disable (not needed for this use case)

### Step 2: Configure Permissions

**Repository permissions** needed:
- **Issues**: Read and write
- **Contents**: Read (for repository access)
- **Pull requests**: Read and write (for auto-merge)
- **Metadata**: Read (basic repository access)

**Account permissions**: None needed

### Step 3: Install App on Repository

1. **Generate private key** and download the `.pem` file
2. **Note the App ID** (visible on app settings page)
3. **Install app** on your `breakout-coding-agent` repository
4. **Grant all selected permissions**

### Step 4: Add Repository Secrets

In your repository settings → Secrets and variables → Actions:

1. **APP_ID**: Your GitHub App ID (numeric value)
2. **APP_PRIVATE_KEY**: Contents of the `.pem` file (entire file content)

**Example**:
```
APP_ID: 123456
APP_PRIVATE_KEY: -----BEGIN RSA PRIVATE KEY-----
[entire PEM file content here]
-----END RSA PRIVATE KEY-----
```

## ✅ Verification

### Test 1: Manual Workflow Trigger
```bash
gh workflow run "RFC Progression - Auto Create Next Game-RFC Issue" --ref main
```

Check if the workflow runs without the "user not found" error.

### Test 2: Check App Token Generation
Look at workflow run logs for:
```
✅ Get GitHub App token
```

### Test 3: Test Assignment
The workflow should now successfully:
1. Create Game-RFC issue
2. Assign to `copilot-swe-agent` 
3. GitHub displays it as assigned to "Copilot"
4. GitHub Coding Agent activates automatically

## 🔧 Updated Workflow Architecture

### Before (❌ Manual Step Required)
```
PR Merge → Issue Created → [MANUAL: gh issue edit X --add-assignee copilot-swe-agent] → Copilot Works
```

### After (✅ Fully Automated)
```
PR Merge → Issue Created → Auto-assigned via GitHub App → Copilot Works
```

## 🚨 Troubleshooting

### "APP_ID secret not found"
- Verify secret is named exactly `APP_ID` (case sensitive)
- Check the secret is in the correct repository

### "APP_PRIVATE_KEY secret not found"  
- Verify secret is named exactly `APP_PRIVATE_KEY`
- Ensure entire PEM file content is copied (including headers/footers)

### "GitHub App not found"
- Verify the App ID matches your created app
- Ensure app is installed on the repository
- Check app has proper permissions

### "Assignment still fails"
- Verify app has "Issues: write" permission
- Check app installation covers the repository
- Ensure `copilot-swe-agent` user exists in your repository context

## 📊 Expected Results

After setup, the automation workflow should achieve:

- ✅ **Issue Creation**: Fully automated
- ✅ **Assignment**: Fully automated (via GitHub App)
- ✅ **Activation**: GitHub Coding Agent starts immediately
- ✅ **Implementation**: Fully automated
- ✅ **Auto-merge**: Fully automated

**Result**: 100% automated Game-RFC progression cycle! 🎉

## 🔗 Related Documentation

- **[CRITICAL-FINDING-GitHub-Coding-Agent-Activation.md](./CRITICAL-FINDING-GitHub-Coding-Agent-Activation.md)** - Problem analysis
- **[dungeon-coding-agent workflows](../../dungeon-coding-agent/.github/workflows/)** - Working examples
- **[GitHub Apps documentation](https://docs.github.com/en/apps)** - Official documentation

---

**Status**: ✅ **SOLUTION IMPLEMENTED**  
**Date**: 2025-09-11  
**Next**: Test with repository secrets and verify full automation