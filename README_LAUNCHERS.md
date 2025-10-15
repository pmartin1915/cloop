# 🚀 Ultrathink Launchers - Complete Guide

## TL;DR

**Port conflict error?** → Double-click `launch_ultrathink_safe.bat`

---

## Available Launchers

### 1. launch_ultrathink_safe.bat ⭐ RECOMMENDED
**The "Just Works" Launcher**

```bash
# Double-click this file
launch_ultrathink_safe.bat
```

**Features**:
- ✅ Auto-stops old instances
- ✅ Finds available port
- ✅ Always works
- ✅ No manual steps

**Perfect for**: Everyone, especially first-time users

---

### 2. launch_ultrathink.bat
**The "Smart Port Finder" Launcher**

```bash
# Double-click this file
launch_ultrathink.bat
```

**Features**:
- ✅ Tries ports 8501-8510
- ✅ Keeps other apps running
- ⚠️ Might use different port

**Perfect for**: Users with multiple Streamlit apps

---

### 3. stop_ultrathink.bat
**The "Manual Stop" Tool**

```bash
# Double-click to stop all instances
stop_ultrathink.bat
```

**Features**:
- ✅ Stops all Streamlit processes
- ✅ Frees up all ports
- ✅ Clean slate

**Perfect for**: Manual control before launching

---

## Common Issues & Solutions

### Issue: "Port 8501 is already in use"
**Solution**: Use `launch_ultrathink_safe.bat`

### Issue: Multiple dashboards open
**Solution**: Run `stop_ultrathink.bat`, then launch again

### Issue: Dashboard shows old data
**Solution**: Hard refresh browser (Ctrl+Shift+R)

### Issue: "Access Denied" when stopping
**Solution**: Right-click → Run as Administrator

---

## Workflow Recommendations

### Daily Use:
```bash
Morning:  launch_ultrathink_safe.bat
          (Keep running all day)
Evening:  Ctrl+C in terminal or stop_ultrathink.bat
```

### Quick Session:
```bash
Start:    launch_ultrathink.bat
Use:      Analyze your code
Stop:     Ctrl+C in terminal
```

### Development:
```bash
Stop:     stop_ultrathink.bat
Start:    poetry run streamlit run ui\Home.py --server.port 8501
```

---

## Technical Details

### Port Detection Algorithm:
```
1. Check port 8501
2. If busy, try 8502
3. If busy, try 8503
4. ... continue to 8510
5. If all busy, show error
```

### Process Management:
```
1. Find all streamlit.exe processes
2. Kill them (taskkill /F)
3. Wait 2 seconds
4. Start fresh instance
```

---

## Files Reference

| File | Size | Purpose |
|------|------|---------|
| `launch_ultrathink_safe.bat` | 1 KB | Auto-fix launcher |
| `launch_ultrathink.bat` | 1 KB | Smart port finder |
| `stop_ultrathink.bat` | 1 KB | Stop all instances |
| `LAUNCHER_GUIDE.md` | 8 KB | Detailed guide |
| `WHICH_LAUNCHER.md` | 3 KB | Decision helper |
| `PORT_FIX_COMPLETE.md` | 3 KB | Fix summary |
| `README_LAUNCHERS.md` | This file | Quick reference |

---

## Quick Commands

```bash
# Recommended (auto-fix everything)
launch_ultrathink_safe.bat

# Alternative (smart port finder)
launch_ultrathink.bat

# Stop all instances
stop_ultrathink.bat

# Manual with custom port
poetry run streamlit run ui\Home.py --server.port 8520
```

---

## Documentation

- **Quick Start**: `START_HERE_PHASE1.md`
- **Launcher Guide**: `LAUNCHER_GUIDE.md`
- **Which Launcher**: `WHICH_LAUNCHER.md`
- **Port Fix**: `PORT_FIX_COMPLETE.md`

---

## Summary

**Problem**: Port conflicts when launching  
**Solution**: 3 launcher options  
**Best Choice**: `launch_ultrathink_safe.bat`  
**Result**: ✅ Always works!

---

## Get Started

```bash
# Right now, double-click:
launch_ultrathink_safe.bat
```

**That's it!** 🎉

---

**No more port conflicts. Ever.** 🚀
