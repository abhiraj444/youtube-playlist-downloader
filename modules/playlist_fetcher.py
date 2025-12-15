"""
Playlist Fetcher Module
Extracts video metadata from YouTube playlists using yt-dlp
"""

import yt_dlp
from typing import List, Dict, Optional


def get_playlist_videos(playlist_url: str) -> List[Dict[str, str]]:
    """
    Extract all video metadata from a YouTube playlist.
    
    Args:
        playlist_url: Full URL of the YouTube playlist
        
    Returns:
        List of dictionaries containing video metadata:
        - id: Video ID
        - title: Video title
        - url: Full video URL
        - duration: Video duration in seconds
        
    Raises:
        Exception: If playlist cannot be accessed or is invalid
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,  # Don't download, just get metadata
        'ignoreerrors': True,  # Skip unavailable videos
    }
    
    videos = []
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract playlist info
            playlist_info = ydl.extract_info(playlist_url, download=False)
            
            if not playlist_info:
                raise Exception("Could not extract playlist information")
            
            # Check if it's actually a playlist
            if 'entries' not in playlist_info:
                raise Exception("URL does not appear to be a valid playlist")
            
            # Extract video metadata
            for entry in playlist_info['entries']:
                if entry is None:  # Skip unavailable videos
                    continue
                    
                video_data = {
                    'id': entry.get('id', ''),
                    'title': entry.get('title', 'Unknown Title'),
                    'url': entry.get('url', f"https://www.youtube.com/watch?v={entry.get('id', '')}"),
                    'duration': entry.get('duration', 0)
                }
                
                videos.append(video_data)
    
    except Exception as e:
        raise Exception(f"Failed to fetch playlist: {str(e)}")
    
    return videos


def get_playlist_title(playlist_url: str) -> Optional[str]:
    """
    Get the title of a YouTube playlist.
    
    Args:
        playlist_url: Full URL of the YouTube playlist
        
    Returns:
        Playlist title or None if unavailable
    """
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': True,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(playlist_url, download=False)
            return playlist_info.get('title', 'Unknown Playlist')
    except:
        return 'Unknown Playlist'
