# 🚀 Launcher Guide - Port Conflict Solutions

## The Problem

When you see:
```
Port 8501 is already in use
```

This means another Streamlit instance is already running on that port.

---

## 3 Solutions (Pick One)

### ✅ Solution 1: Safe Launcher (Recommended)
**Best for**: Most users

```bash
# Double-click this file:
launch_ultrathink_safe.bat
```

**What it does**:
1. Automatically stops old Streamlit instances
2. Finds an available port (8501-8510)
3. Starts fresh dashboard

**Pros**: Fully automatic, no manual steps  
**Cons**: Kills ALL Streamlit instances (not just Ultrathink)

---

### ✅ Solution 2: Smart Launcher
**Best for**: When you want to keep other Streamlit apps running

```bash
# Double-click this file:
launch_ultrathink.bat
```

**What it does**:
1. Tries ports 8501-8510 in order
2. Uses first available port
3. Tells you which port it's using

**Pros**: Doesn't kill other apps  
**Cons**: Might use a different port each time

---

### ✅ Solution 3: Manual Stop
**Best for**: When you want full control

```bash
# Step 1: Stop old instances
stop_ultrathink.bat

# Step 2: Start fresh
launch_ultrathink.bat
```

**What it does**:
1. You manually stop old instances
2. Then start fresh on port 8501

**Pros**: Full control, predictable port  
**Cons**: Two steps instead of one

---

## Quick Reference

| File | Purpose | When to Use |
|------|---------|-------------|
| `launch_ultrathink_safe.bat` | Auto-stop + start | **Use this first!** |
| `launch_ultrathink.bat` | Smart port finder | Other apps running |
| `stop_ultrathink.bat` | Stop all instances | Manual control |

---

## Detailed Behavior

### launch_ultrathink_safe.bat
```
[1/3] Checking for existing instances...
      → Stops all Streamlit processes
      → Waits 2 seconds

[2/3] Finding available port...
      → Checks ports 8501-8510
      → Picks first available

[3/3] Starting Ultrathink Dashboard...
      → Launches on chosen port
      → Opens browser automatically
```

### launch_ultrathink.bat
```
Trying port 8501... busy
Trying port 8502... busy
Trying port 8503... available!
→ Starting on port 8503
```

### stop_ultrathink.bat
```
Stopping Streamlit processes...
→ Kills streamlit.exe
→ Kills Python processes on ports 8501-8510
→ Confirms completion
```

---

## Troubleshooting

### "All ports 8501-8510 are in use!"

**Solution A**: Use safe launcher
```bash
launch_ultrathink_safe.bat
```

**Solution B**: Stop manually
```bash
stop_ultrathink.bat
# Wait 5 seconds
launch_ultrathink.bat
```

**Solution C**: Use custom port
```bash
poetry run streamlit run ui\Home.py --server.port 8520
```

---

### "Access Denied" when stopping

**Cause**: Running as non-admin

**Solution**: Right-click → "Run as Administrator"

Or just use the smart launcher (doesn't need admin):
```bash
launch_ultrathink.bat
```

---

### Dashboard opens but shows old data

**Cause**: Browser cached old session

**Solution**: Hard refresh
- Chrome/Edge: `Ctrl + Shift + R`
- Firefox: `Ctrl + F5`

Or clear browser cache for localhost

---

### Multiple dashboards open

**Cause**: Launched multiple times on different ports

**Solution**: Stop all and start fresh
```bash
stop_ultrathink.bat
launch_ultrathink_safe.bat
```

---

## Best Practices

### Daily Use:
```bash
# Morning: Start dashboard
launch_ultrathink_safe.bat

# Keep it running all day (minimize terminal)

# Evening: Stop when done
stop_ultrathink.bat
```

### Quick Session:
```bash
# Start
launch_ultrathink.bat

# Use it

# Stop (Ctrl+C in terminal)
```

### Multiple Projects:
```bash
# Each project can use different port
cd c:\project1
poetry run streamlit run ui\Home.py --server.port 8501

cd c:\project2
poetry run streamlit run ui\Home.py --server.port 8502
```

---

## Technical Details

### Port Detection Logic:
```batch
for /L %%p in (8501,1,8510) do (
    netstat -ano | findstr ":%%p " >nul
    if errorlevel 1 (
        REM Port is available
        use %%p
    )
)
```

### Process Killing:
```batch
REM Kill by process name
taskkill /F /IM streamlit.exe

REM Kill by port
netstat -ano | findstr ":8501" 
→ Find PID
→ taskkill /F /PID <pid>
```

---

## FAQ

**Q: Which launcher should I use?**  
A: Start with `launch_ultrathink_safe.bat` - it's the easiest.

**Q: Will it kill my other Streamlit apps?**  
A: `launch_ultrathink_safe.bat` will. Use `launch_ultrathink.bat` to avoid this.

**Q: Can I bookmark the URL?**  
A: Yes, but port might change. Use safe launcher for consistent port 8501.

**Q: How do I know which port it's using?**  
A: The launcher prints: "Opening at http://localhost:XXXX"

**Q: Can I change the default port?**  
A: Yes, edit the .bat file and change `8501` to your preferred port.

---

## Summary

**Problem**: Port 8501 already in use  
**Solution**: Use `launch_ultrathink_safe.bat`  
**Result**: ✅ Dashboard starts automatically on available port

**No more port conflicts!** 🎉

---

## Quick Commands

```bash
# Recommended (auto-fix everything)
launch_ultrathink_safe.bat

# Alternative (smart port finder)
launch_ultrathink.bat

# Stop all instances
stop_ultrathink.bat

# Manual port selection
poetry run streamlit run ui\Home.py --server.port 8520
```

---

**Choose your launcher and enjoy Ultrathink!** 🚀
