"""
URL Resolver Module
Resolves direct download URLs for YouTube videos using yt-dlp
"""

import yt_dlp
from typing import Optional, Dict, Tuple


def get_direct_url(video_id: str, quality_preference: str = 'best') -> Tuple[Optional[str], Optional[Dict]]:
    """
    Resolve direct download URL for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        quality_preference: Quality preference ('1080p', '720p', 'best')
        
    Returns:
        Tuple of (direct_url, format_info) or (None, None) if failed
        format_info contains: resolution, filesize, ext, format_note
        
    Note:
        Direct URLs expire after several hours and must be used promptly
    """
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    
    # Define format selection based on quality preference
    format_selectors = {
        '1080p': 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080][ext=mp4]/best[ext=mp4]/best',
        '720p': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[ext=mp4]/best',
        'best': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'
    }
    
    format_string = format_selectors.get(quality_preference, format_selectors['best'])
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'format': format_string,
        'ignoreerrors': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info without downloading
            info = ydl.extract_info(video_url, download=False)
            
            if not info:
                return None, None
            
            # Get the direct URL
            # For merged formats, yt-dlp provides the URL in 'url' field
            # For single formats, it's also in 'url'
            direct_url = info.get('url')
            
            # If url is not directly available, try to get it from requested_formats
            if not direct_url and 'requested_formats' in info:
                # For merged video+audio, we want the video URL
                # IDM can handle the video part
                video_format = info['requested_formats'][0]
                direct_url = video_format.get('url')
            
            # Build format info
            format_info = {
                'resolution': f"{info.get('width', 'N/A')}x{info.get('height', 'N/A')}",
                'filesize': info.get('filesize') or info.get('filesize_approx', 0),
                'ext': info.get('ext', 'mp4'),
                'format_note': info.get('format_note', 'unknown'),
                'vcodec': info.get('vcodec', 'unknown'),
                'acodec': info.get('acodec', 'unknown')
            }
            
            return direct_url, format_info
            
    except Exception as e:
        # Return None for failed videos (private, deleted, age-restricted, etc.)
        return None, None


def format_filesize(size_bytes: int) -> str:
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted string (e.g., "45.2 MB")
    """
    if size_bytes == 0:
        return "Unknown"
    
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    
    return f"{size_bytes:.1f} TB"
