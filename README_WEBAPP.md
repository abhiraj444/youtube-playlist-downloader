# YouTube Playlist Extractor - Web Application

A modern web application to extract direct download URLs from YouTube playlists for use with Internet Download Manager (IDM).

## 🚀 Features

- ✅ **Video Selection**: Choose which videos to download with checkboxes
- ✅ **Quality Control**: Global quality selector + per-video quality override
- ✅ **Bulk Actions**: Select all / Deselect all buttons
- ✅ **Dual Output**: Copy to clipboard OR download .txt file
- ✅ **IDM Auto-Naming**: URLs include video titles for automatic filename detection
- ✅ **Fast Processing**: Concurrent URL resolution (10 workers)
- ✅ **Modern UI**: Beautiful dark theme with animations
- ✅ **Mobile Responsive**: Works on all devices

## 🌐 Live Demo

**Deployed on Render.com**: [Coming Soon]

## 📦 Local Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. **Clone the repository**:
```bash
git clone <your-repo-url>
cd youtube-playlist-extractor
```

2. **Create virtual environment**:
```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Run the application**:
```bash
uvicorn webapp.main:app --reload
```

5. **Open in browser**:
```
http://localhost:8000
```

## 🎯 How to Use

### Step 1: Enter Playlist URL
1. Paste your YouTube playlist URL
2. Select default quality (Best, 1080p, or 720p)
3. Click "Fetch Playlist"

### Step 2: Select Videos
1. Review the fetched videos
2. Use checkboxes to select videos you want
3. Use "Select All" or "Deselect All" for bulk actions
4. Change quality for individual videos if needed

### Step 3: Generate & Download
1. Click "Generate Download Links"
2. Wait for processing (concurrent, very fast!)
3. **Copy to Clipboard** OR **Download .txt File**
4. Import the URLs into IDM

## 💡 IDM Auto-Naming Feature

URLs are formatted with video titles as fragments:
```
https://googlevideo.com/videoplayback?...#Video_Title_Here.mp4
```

When you import these URLs into IDM, it automatically names the downloaded files with the video titles! No manual renaming needed.

## 🚀 Deployment to Render.com

### One-Time Setup

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo>
git push -u origin main
```

2. **Deploy on Render.com**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml` and configure everything
   - Click "Create Web Service"

3. **Done!** Your app will be live at `https://your-app.onrender.com`

### Auto-Deploy
Every time you push to GitHub, Render automatically deploys the latest version!

## 📁 Project Structure

```
youtube-playlist-extractor/
├── webapp/
│   ├── main.py              # FastAPI backend
│   ├── static/
│   │   ├── index.html       # Frontend
│   │   ├── css/
│   │   │   └── style.css    # Styles
│   │   └── js/
│   │       └── app.js       # Frontend logic
│   └── temp/                # Temporary files
├── modules/                 # Python modules
│   ├── playlist_fetcher.py
│   ├── url_resolver.py
│   └── output_formatter.py
├── requirements.txt         # Dependencies
├── render.yaml             # Render.com config
└── README.md               # This file
```

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **YouTube API**: yt-dlp
- **Deployment**: Render.com
- **Styling**: Custom CSS with dark theme

## ⚙️ API Endpoints

### `POST /api/fetch-playlist`
Fetch playlist metadata
```json
{
  "url": "https://youtube.com/playlist?list=...",
  "default_quality": "best"
}
```

### `POST /api/generate-urls`
Generate direct URLs for selected videos
```json
{
  "videos": [
    {"id": "...", "title": "...", "quality": "1080p"}
  ]
}
```

### `GET /download/{file_id}`
Download generated .txt file

## 📝 Notes

- **URL Expiration**: Generated URLs expire after several hours. Use them promptly.
- **Rate Limiting**: The app processes 10 videos concurrently to avoid YouTube rate limiting.
- **Free Tier**: Render.com free tier spins down after 15 minutes of inactivity. First request may take ~30 seconds to wake up.

## 🐛 Troubleshooting

### "Failed to fetch playlist"
- Check if the playlist URL is correct
- Make sure the playlist is public
- Verify the URL contains `list=` parameter

### "Failed to resolve URLs"
- Some videos may be private or deleted
- Try reducing the number of selected videos
- Check your internet connection

### Slow processing
- Large playlists (50+ videos) may take 1-2 minutes
- This is normal due to YouTube's rate limiting
- The app processes 10 videos at a time for optimal speed

## 📄 License

MIT License - feel free to use and modify!

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⭐ Support

If you find this useful, please give it a star on GitHub!
