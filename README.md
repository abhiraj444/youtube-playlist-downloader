# YouTube Playlist Direct Link Extractor

A powerful Python CLI tool that extracts direct, downloadable video URLs from YouTube playlists for use with Internet Download Manager (IDM) and other download managers.

## Features

✨ **Direct URL Extraction** - Resolves direct googlevideo.com URLs for each video  
🎯 **Quality Selection** - Choose between 1080p, 720p, or best available quality  
📝 **IDM Compatible** - Generates text files ready to import into IDM  
⚡ **Smart Rate Limiting** - Configurable delays to avoid YouTube blocks  
🔄 **Retry Logic** - Automatically retries failed videos  
🎨 **Beautiful CLI** - Rich progress bars and colored output  
🛡️ **Error Handling** - Gracefully handles private/deleted videos  

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd youtube-playlist-extractor
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install yt-dlp rich
   ```

## Usage

### Basic Usage

```bash
python playlist_grabber.py "PLAYLIST_URL"
```

Example:
```bash
python playlist_grabber.py "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
```

### Advanced Options

```bash
python playlist_grabber.py "PLAYLIST_URL" [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output FILE` | Output file path | Auto-generated |
| `-q, --quality QUALITY` | Quality preference (best/1080p/720p) | best |
| `-d, --delay SECONDS` | Delay between requests | 1.5 |
| `-r, --retries NUM` | Max retry attempts | 3 |
| `-h, --help` | Show help message | - |
| `-v, --version` | Show version | - |

### Examples

**Specify output file:**
```bash
python playlist_grabber.py "PLAYLIST_URL" -o my_videos.txt
```

**Request 1080p quality:**
```bash
python playlist_grabber.py "PLAYLIST_URL" -q 1080p
```

**Increase delay to 2 seconds (for large playlists):**
```bash
python playlist_grabber.py "PLAYLIST_URL" -d 2.0
```

**Combine options:**
```bash
python playlist_grabber.py "PLAYLIST_URL" -o output.txt -q 720p -d 2.0
```

## Output Format

The tool generates a text file with the following format:

```
================================================================================
YouTube Playlist Direct Download URLs
================================================================================
Playlist: My Awesome Playlist
Generated: 2025-12-16 00:56:00
Total Videos: 25
================================================================================

IMPORTANT NOTES:
- These URLs expire after several hours. Use them promptly.
- Import this file into Internet Download Manager (IDM) for batch downloading.
- Each URL is preceded by the video title as a comment.

================================================================================

# Video 1: Introduction to Python
# Resolution: 1920x1080 | Size: 45.2 MB
https://rr4---sn-xxx.googlevideo.com/videoplayback?expire=...

# Video 2: Python Data Types
# Resolution: 1920x1080 | Size: 38.7 MB
https://rr1---sn-xxx.googlevideo.com/videoplayback?expire=...
```

## Using with IDM

1. Run the tool to generate the URL file
2. Open Internet Download Manager (IDM)
3. Go to **Tasks** → **Import** → **Import from text file**
4. Select the generated `.txt` file
5. IDM will automatically add all URLs to the download queue

## Important Notes

⚠️ **URL Expiration**: Direct YouTube URLs expire after several hours. Generate and use them promptly.

⚠️ **Rate Limiting**: YouTube may block requests if you make too many too quickly. The default 1.5s delay is recommended. Increase it for large playlists.

⚠️ **Private/Deleted Videos**: The tool will skip videos that are private, deleted, or age-restricted and continue with the rest.

⚠️ **YouTube Changes**: YouTube frequently updates their systems. Keep `yt-dlp` updated:
```bash
pip install --upgrade yt-dlp
```

## Troubleshooting

### "Failed to fetch playlist"
- Verify the playlist URL is correct and public
- Check your internet connection
- Ensure the playlist exists and is accessible

### "No URLs were successfully resolved"
- The playlist may contain only private/deleted videos
- Try updating yt-dlp: `pip install --upgrade yt-dlp`
- Increase the delay: `-d 3.0`

### "Rate limiting" errors
- Increase the delay between requests: `-d 2.0` or higher
- Wait a few minutes and try again

### URLs don't work in IDM
- Ensure you're using the URLs promptly (they expire)
- Try regenerating the URLs
- Check that IDM is properly configured

## Project Structure

```
youtube-playlist-extractor/
├── playlist_grabber.py          # Main CLI application
├── modules/
│   ├── __init__.py
│   ├── playlist_fetcher.py      # Playlist metadata extraction
│   ├── url_resolver.py          # Direct URL resolution
│   ├── output_formatter.py      # Output file generation
│   └── orchestrator.py          # Workflow coordination
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── .gitignore
```

## Technical Details

- **Core Engine**: [yt-dlp](https://github.com/yt-dlp/yt-dlp) - The most robust YouTube extraction library
- **CLI Framework**: [rich](https://github.com/Textualize/rich) - Beautiful terminal formatting
- **Format Priority**: MP4 containers with H.264 video codec
- **Quality Tiers**: 1080p (itag 137), 720p (itag 22), or best available

## License

This project is provided as-is for educational purposes. Please respect YouTube's Terms of Service and copyright laws.

## Contributing

Feel free to submit issues or pull requests for improvements!

## Version

Current version: **1.0.0**

---

**Note**: This tool is for personal use only. Always respect content creators' rights and YouTube's Terms of Service.
