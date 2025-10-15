# Ultrathink Extension Test Plan

## Pre-Test Setup

1. ✅ Verify Ultrathink CLI works
2. ✅ Install extension dependencies
3. ✅ Create test Python file
4. ✅ Configure extension settings

## Test Cases

### Test 1: Extension Activation
- [ ] Open VS Code in vscode-extension folder
- [ ] Press F5 to launch Extension Development Host
- [ ] Check status bar shows "Ultrathink" icon
- [ ] Check sidebar has Ultrathink icon

### Test 2: Analyze File
- [ ] Open test Python file
- [ ] Right-click → "Ultrathink: Analyze Current File"
- [ ] Wait for progress notification
- [ ] Check Findings panel populates
- [ ] Verify no errors in Debug Console

### Test 3: Learn Patterns
- [ ] Run Command Palette (Ctrl+Shift+P)
- [ ] Type "Ultrathink: Learn Patterns"
- [ ] Enter threshold (2)
- [ ] Check Patterns panel updates
- [ ] Verify success notification

### Test 4: Show Statistics
- [ ] Click status bar Ultrathink icon
- [ ] Verify modal shows stats
- [ ] Check numbers match sidebar

### Test 5: Scaffold Project
- [ ] Run "Ultrathink: Scaffold New Project"
- [ ] Enter project details
- [ ] Verify project created
- [ ] Check "Open Folder" prompt

## Expected Issues

1. **CLI path not found** → Need to set ultrathink.ultrathinkPath
2. **Poetry not found** → Need Poetry in PATH
3. **No findings** → Need to run analyze first
4. **Parse errors** → CLI output format may differ

## Success Criteria

- Extension activates without errors
- Commands execute successfully
- UI updates with data
- No crashes or hangs
