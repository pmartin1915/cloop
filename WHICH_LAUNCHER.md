# 🚀 Which Launcher Should I Use?

## Quick Decision Tree

```
Do you have port conflicts?
│
├─ YES → Use launch_ultrathink_safe.bat ⭐
│
└─ NO → Use launch_ultrathink.bat
```

---

## Visual Comparison

```
┌─────────────────────────────────────────────────────────┐
│  launch_ultrathink_safe.bat  ⭐ RECOMMENDED             │
├─────────────────────────────────────────────────────────┤
│  ✅ Auto-stops old instances                            │
│  ✅ Always uses port 8501 (predictable)                 │
│  ✅ Works every time                                    │
│  ⚠️  Kills ALL Streamlit apps                           │
│                                                         │
│  USE WHEN: You want it to "just work"                  │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  launch_ultrathink.bat                                  │
├─────────────────────────────────────────────────────────┤
│  ✅ Keeps other Streamlit apps running                  │
│  ✅ Smart port detection (8501-8510)                    │
│  ⚠️  Might use different port each time                 │
│                                                         │
│  USE WHEN: You have other Streamlit apps running       │
└─────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────┐
│  stop_ultrathink.bat + launch_ultrathink.bat            │
├─────────────────────────────────────────────────────────┤
│  ✅ Full manual control                                 │
│  ✅ Predictable behavior                                │
│  ⚠️  Two steps instead of one                           │
│                                                         │
│  USE WHEN: You want complete control                   │
└─────────────────────────────────────────────────────────┘
```

---

## Scenarios

### Scenario 1: First Time User
**Situation**: Never used Ultrathink before

**Use**: `launch_ultrathink_safe.bat`

**Why**: Simplest, most reliable

---

### Scenario 2: Daily User
**Situation**: Use Ultrathink every day

**Use**: `launch_ultrathink_safe.bat` in morning

**Why**: Clean start each day

---

### Scenario 3: Multiple Projects
**Situation**: Running other Streamlit apps

**Use**: `launch_ultrathink.bat`

**Why**: Won't kill your other apps

---

### Scenario 4: Port Conflict Error
**Situation**: Seeing "Port already in use"

**Use**: `launch_ultrathink_safe.bat`

**Why**: Auto-fixes the issue

---

### Scenario 5: Developer/Power User
**Situation**: Want full control

**Use**: Manual commands
```bash
stop_ultrathink.bat
poetry run streamlit run ui\Home.py --server.port 8501
```

**Why**: Complete control over behavior

---

## File Locations

All in: `c:\Cloop\ultrathink\`

```
launch_ultrathink_safe.bat    ⭐ Start here
launch_ultrathink.bat          Alternative
stop_ultrathink.bat            Manual stop
```

---

## Quick Reference

| Launcher | Auto-Stop | Port | Best For |
|----------|-----------|------|----------|
| `safe` ⭐ | Yes | 8501 | Everyone |
| `regular` | No | 8501-8510 | Multi-app users |
| `manual` | Manual | 8501 | Power users |

---

## Bottom Line

**99% of users should use**: `launch_ultrathink_safe.bat`

**It just works!** 🎉

---

## Try It Now

```bash
# Double-click this file:
launch_ultrathink_safe.bat
```

**Done!** 🚀
