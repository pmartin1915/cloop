# 🧪 Ultrathink Self-Testing Guide

## Overview

Ultrathink can now test itself automatically! This means the application can:
- Press its own buttons
- Run through workflows
- Detect errors
- Monitor health
- Self-heal issues

---

## Features

### 1. Automated Test Suite
- **Framework Initialization**: Verifies core system starts correctly
- **File Analysis**: Tests code analysis with sample files
- **Handoff Generation**: Validates prompt creation
- **Knowledge Base**: Checks database operations
- **Error Recovery**: Tests error handling

### 2. Health Monitoring
- Real-time system status
- Component-level checks
- Auto-refresh capability
- Visual status indicators

### 3. AI Error Detection
- Analyzes errors automatically
- Suggests fixes
- Monitors system health
- Predicts potential issues

---

## How to Use

### Method 1: Command Line
```bash
# Run full test suite
python run_self_test.py
```

**Output:**
```
🧠 Ultrathink Self-Test Suite
============================================================
Testing all components...

✓ PASS - Framework Initialization (0.10s)
✓ PASS - File Analysis (1.00s)
✓ PASS - Handoff Generation (0.10s)
✓ PASS - Knowledge Base (0.10s)
✓ PASS - Error Recovery (0.10s)

============================================================
✓ ALL TESTS PASSED - System is healthy!
============================================================
```

### Method 2: Web Dashboard
```bash
# Launch dashboard
launch_ultrathink_safe.bat

# Navigate to "Self-Test" page
# Click "Run Full Test Suite"
```

### Method 3: Programmatic
```python
from ultrathink.framework import Ultrathink
from ultrathink.self_test import SelfTester

ultrathink = Ultrathink("ultrathink.yaml")
tester = SelfTester(ultrathink)

results = await tester.run_full_test_suite()
print(tester.generate_test_report(results))
```

---

## Test Details

### Test 1: Framework Initialization
**What it tests**: Core framework can start
**How**: Calls `ultrathink.initialize()`
**Pass criteria**: No exceptions raised

### Test 2: File Analysis
**What it tests**: Code analysis works
**How**: Creates test file with intentional error, analyzes it
**Pass criteria**: Detects the intentional error

### Test 3: Handoff Generation
**What it tests**: Prompt generation works
**How**: Creates mock analysis result, generates prompt
**Pass criteria**: Prompt contains expected content

### Test 4: Knowledge Base
**What it tests**: Database operations work
**How**: Retrieves stats from knowledge base
**Pass criteria**: Stats structure is valid

### Test 5: Error Recovery
**What it tests**: Error handling works
**How**: Attempts to analyze non-existent path
**Pass criteria**: Raises appropriate exception

---

## Health Monitoring

### Component Checks

**Framework Health:**
- ✓ Initialization successful
- ✓ Configuration loaded
- ✓ All modules available

**Knowledge Base Health:**
- ✓ Database accessible
- ✓ Stats retrievable
- ✓ Findings count: X

**AI Connection Health:**
- ✓ API credentials valid
- ✓ Services reachable
- ✓ Rate limits OK

### Status Levels

| Status | Meaning | Action |
|--------|---------|--------|
| Healthy | All systems operational | None needed |
| Degraded | Some issues detected | Review warnings |
| Unhealthy | Critical failures | Immediate attention |

---

## AI Error Detection

### How It Works

1. **Monitor**: Continuously watches for errors
2. **Analyze**: Uses AI to understand error context
3. **Suggest**: Provides fix recommendations
4. **Apply**: Can auto-fix simple issues

### Example

```
Error Detected: Port 8501 already in use
AI Analysis: Port conflict detected
Suggested Fix: Try ports 8502-8510 or stop existing instance
Confidence: 95%
Auto-Fix: Available ✓
```

---

## Self-Healing Capabilities

### Automatic Fixes

**Port Conflicts:**
- Detects busy ports
- Tries alternative ports
- Suggests manual fixes

**Configuration Issues:**
- Validates config files
- Suggests corrections
- Can auto-repair simple issues

**API Errors:**
- Detects rate limiting
- Implements backoff
- Retries automatically

**File Errors:**
- Validates paths
- Suggests corrections
- Handles missing files

---

## When to Run Tests

### Regular Schedule
- **Daily**: Quick health check
- **Weekly**: Full test suite
- **Monthly**: Comprehensive audit

### Specific Situations
- After updating Ultrathink
- Before important analyses
- When experiencing issues
- After configuration changes
- Before sharing with team

---

## Interpreting Results

### All Tests Pass ✓
```
✓ ALL TESTS PASSED - System is healthy!
```
**Meaning**: Everything works perfectly
**Action**: None needed, continue using

### Some Tests Fail ⚠
```
⚠ SOME TESTS FAILED - Review errors above
```
**Meaning**: Issues detected
**Action**: Review failed tests, apply fixes

### All Tests Fail ✗
```
✗ CRITICAL - System not operational
```
**Meaning**: Major problems
**Action**: Check configuration, reinstall if needed

---

## Advanced Usage

### Custom Tests

Add your own tests to `self_test.py`:

```python
async def _test_custom_feature(self) -> Dict[str, Any]:
    """Test custom feature."""
    try:
        # Your test logic here
        result = await self.ultrathink.custom_function()
        
        return {
            "test": "Custom Feature",
            "passed": result is not None,
            "duration": 0.5,
            "error": None
        }
    except Exception as e:
        return {
            "test": "Custom Feature",
            "passed": False,
            "duration": 0.5,
            "error": str(e)
        }
```

### Continuous Monitoring

Run tests continuously:

```python
import asyncio

async def continuous_monitor():
    while True:
        results = await tester.run_full_test_suite()
        if results['tests_failed'] > 0:
            # Alert or take action
            send_alert(results)
        await asyncio.sleep(3600)  # Every hour
```

---

## Integration with CI/CD

### GitHub Actions

```yaml
name: Ultrathink Self-Test

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run Self-Test
        run: python run_self_test.py
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python run_self_test.py
if [ $? -ne 0 ]; then
    echo "Self-tests failed. Commit aborted."
    exit 1
fi
```

---

## Troubleshooting

### Tests Timeout
**Cause**: AI analysis taking too long
**Fix**: Check internet connection, API limits

### Framework Init Fails
**Cause**: Configuration issues
**Fix**: Verify `ultrathink.yaml` exists and is valid

### Knowledge Base Errors
**Cause**: Database locked or corrupted
**Fix**: Close other instances, rebuild database

### AI Connection Fails
**Cause**: Invalid credentials or network issues
**Fix**: Check `.env` file, verify API keys

---

## Best Practices

1. **Run tests before important work**
2. **Monitor health regularly**
3. **Review failed tests immediately**
4. **Keep test history for trends**
5. **Update tests when adding features**
6. **Automate testing in CI/CD**
7. **Document custom tests**

---

## Summary

**Self-testing makes Ultrathink:**
- ✓ More reliable
- ✓ Easier to debug
- ✓ Self-healing
- ✓ Production-ready
- ✓ Confidence-inspiring

**Run tests regularly to ensure optimal performance!**

---

## Quick Commands

```bash
# Run full test suite
python run_self_test.py

# Run from dashboard
launch_ultrathink_safe.bat
# Navigate to Self-Test page

# Check health only
python -c "from ultrathink.self_test import AIErrorDetector; import asyncio; asyncio.run(AIErrorDetector(None).monitor_health())"
```

---

**Your Ultrathink can now test itself!** 🎉
