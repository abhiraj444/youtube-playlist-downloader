"""
FastAPI Web Application for YouTube Playlist Direct Link Extractor
Optimized for Render.com deployment with no timeout limits
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
import os
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import time
import uuid

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))

from modules.playlist_fetcher import get_playlist_videos, get_playlist_title
from modules.url_resolver import get_direct_url, format_filesize

app = FastAPI(title="YouTube Playlist Extractor")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temp directory for generated files
TEMP_DIR = Path(__file__).parent / "temp"
TEMP_DIR.mkdir(exist_ok=True)

# Pydantic models
class PlaylistRequest(BaseModel):
    url: str
    default_quality: str = "best"

class GenerateURLsRequest(BaseModel):
    videos: List[Dict[str, str]]  # [{"id": "...", "title": "...", "quality": "..."}]

class VideoInfo(BaseModel):
    id: str
    title: str
    duration: int
    thumbnail: Optional[str] = None

class PlaylistResponse(BaseModel):
    title: str
    total_videos: int
    videos: List[VideoInfo]

# Helper function to sanitize filename
def sanitize_filename(filename: str) -> str:
    """Remove invalid characters from filename"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename.strip('. ')[:200]

# Helper function to resolve single video URL
def resolve_video_url(video_data: Dict[str, str]) -> Dict:
    """Resolve direct URL for a single video"""
    video_id = video_data['id']
    video_title = video_data['title']
    quality = video_data.get('quality', 'best')
    
    direct_url, format_info = get_direct_url(video_id, quality)
    
    if direct_url:
        # Add video title as URL fragment for IDM auto-naming
        safe_title = sanitize_filename(video_title).replace(' ', '_')
        url_with_title = f"{direct_url}#{safe_title}.mp4"
        
        return {
            'success': True,
            'title': video_title,
            'url': url_with_title,
            'quality': quality,
            'format_info': format_info
        }
    else:
        return {
            'success': False,
            'title': video_title,
            'error': 'Failed to resolve URL'
        }

@app.get("/")
async def read_root():
    """Serve the main HTML page"""
    return FileResponse("webapp/static/index.html")

@app.post("/api/fetch-playlist", response_model=PlaylistResponse)
async def fetch_playlist(request: PlaylistRequest):
    """
    Fetch playlist metadata without resolving URLs
    Fast operation - completes in seconds
    """
    try:
        # Get playlist title
        playlist_title = get_playlist_title(request.url)
        
        # Get video metadata
        videos = get_playlist_videos(request.url)
        
        if not videos:
            raise HTTPException(status_code=404, detail="No videos found in playlist")
        
        # Format response
        video_list = [
            VideoInfo(
                id=video['id'],
                title=video['title'],
                duration=video.get('duration', 0),
                thumbnail=f"https://img.youtube.com/vi/{video['id']}/mqdefault.jpg"
            )
            for video in videos
        ]
        
        return PlaylistResponse(
            title=playlist_title,
            total_videos=len(video_list),
            videos=video_list
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch playlist: {str(e)}")

@app.post("/api/generate-urls")
async def generate_urls(request: GenerateURLsRequest):
    """
    Generate direct URLs for selected videos
    Uses concurrent processing for speed
    """
    try:
        if not request.videos:
            raise HTTPException(status_code=400, detail="No videos selected")
        
        # Process videos concurrently (10 workers for speed)
        results = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(resolve_video_url, video) for video in request.videos]
            results = [future.result() for future in futures]
        
        # Filter successful results
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]
        
        if not successful:
            raise HTTPException(status_code=500, detail="Failed to resolve any URLs")
        
        # Generate text file content
        file_content = "=" * 80 + "\n"
        file_content += "YouTube Playlist Direct Download URLs\n"
        file_content += "=" * 80 + "\n"
        file_content += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        file_content += f"Total Videos: {len(successful)}\n"
        file_content += "=" * 80 + "\n\n"
        
        file_content += "IMPORTANT NOTES:\n"
        file_content += "- These URLs expire after several hours. Use them promptly.\n"
        file_content += "- Import this file into Internet Download Manager (IDM).\n"
        file_content += "- Video titles are included in URLs for auto-naming.\n\n"
        file_content += "=" * 80 + "\n\n"
        
        for idx, video in enumerate(successful, 1):
            file_content += f"# Video {idx}: {video['title']}\n"
            if video.get('format_info'):
                resolution = video['format_info'].get('resolution', 'N/A')
                file_content += f"# Resolution: {resolution} | Quality: {video['quality']}\n"
            file_content += f"{video['url']}\n\n"
        
        # Save to temporary file
        file_id = str(uuid.uuid4())
        file_path = TEMP_DIR / f"{file_id}.txt"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(file_content)
        
        return JSONResponse({
            'success': True,
            'file_id': file_id,
            'download_url': f"/download/{file_id}",
            'total_successful': len(successful),
            'total_failed': len(failed),
            'content': file_content,  # For copy-to-clipboard
            'failed_videos': [f['title'] for f in failed] if failed else []
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate URLs: {str(e)}")

@app.get("/download/{file_id}")
async def download_file(file_id: str):
    """Download generated .txt file"""
    file_path = TEMP_DIR / f"{file_id}.txt"
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    return FileResponse(
        file_path,
        media_type="text/plain",
        filename=f"youtube_playlist_{file_id[:8]}.txt"
    )

@app.get("/health")
async def health_check():
    """Health check endpoint for Render.com"""
    return {"status": "healthy", "service": "YouTube Playlist Extractor"}

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="webapp/static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
