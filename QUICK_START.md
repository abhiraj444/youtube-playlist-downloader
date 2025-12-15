# Quick Start Guide

## ✅ CORRECT Way to Run

**Always use the virtual environment Python:**

```bash
# Windows
.\venv\Scripts\python playlist_grabber.py "PLAYLIST_URL" --async

# Linux/Mac
./venv/bin/python playlist_grabber.py "PLAYLIST_URL" --async
```

## ❌ WRONG Way (Will Cause Errors)

```bash
# This will fail with "ModuleNotFoundError: No module named 'rich'"
python playlist_grabber.py "PLAYLIST_URL" --async
```

**Why?** The system Python doesn't have `yt-dlp` and `rich` installed. Only the virtual environment has these packages.

---

## Alternative: Activate Virtual Environment

If you want to use `python` directly without the full path:

### Windows
```bash
# Activate venv
.\venv\Scripts\Activate.ps1

# Now you can use python directly
python playlist_grabber.py "PLAYLIST_URL" --async

# Deactivate when done
deactivate
```

### Linux/Mac
```bash
# Activate venv
source venv/bin/activate

# Now you can use python directly
python playlist_grabber.py "PLAYLIST_URL" --async

# Deactivate when done
deactivate
```

---

## Quick Examples

### Example 1: Basic Async (10 workers)
```bash
.\venv\Scripts\python playlist_grabber.py "https://www.youtube.com/playlist?list=PLWoFohRKBLPu9ta2hz-zYsofg1QkQ9EM2" --async
```

### Example 2: Fast Mode (15 workers)
```bash
.\venv\Scripts\python playlist_grabber.py "PLAYLIST_URL" --async --workers 15
```

### Example 3: With Custom Output
```bash
.\venv\Scripts\python playlist_grabber.py "PLAYLIST_URL" --async -o my_videos.txt -q 1080p
```

### Example 4: Conservative (5 workers)
```bash
.\venv\Scripts\python playlist_grabber.py "PLAYLIST_URL" --async --workers 5
```

---

## Performance Results (Your Test)

✅ **Just tested with your playlist:**
- **Playlist**: 10 videos
- **Mode**: Async (10 workers)
- **Result**: SUCCESS! All 10 videos processed
- **Output**: Generated `.txt` file ready for IDM

---

## Troubleshooting

### Error: "ModuleNotFoundError: No module named 'rich'"
**Solution**: Use `.\venv\Scripts\python` instead of just `python`

### Error: "ModuleNotFoundError: No module named 'yt_dlp'"
**Solution**: Same as above - use the venv Python

### Want to avoid typing the full path?
**Solution**: Activate the virtual environment first (see "Alternative" section above)

---

## Next Steps

Now that async mode is working, you mentioned wanting a **web application**. 

Based on your HTML example, I can build:

1. **Simple Web App** - Paste URL, get .txt file
2. **Advanced Web App** - Select videos, choose resolutions, custom .txt

Which would you prefer? 🚀
