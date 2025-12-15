"""
Output Formatter Module
Formats and writes video URLs to IDM-compatible text files
"""

from datetime import datetime
from typing import List, Dict
import os


def write_to_file(video_data: List[Dict], output_path: str, playlist_title: str = "Unknown Playlist") -> int:
    """
    Write video URLs to a formatted text file compatible with IDM.
    
    Args:
        video_data: List of dictionaries containing video info:
                   - title: Video title
                   - url: Direct download URL
                   - format_info: Optional format details
        output_path: Path to output file
        playlist_title: Title of the playlist
        
    Returns:
        Number of URLs written to file
    """
    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Count successful URLs
    url_count = len([v for v in video_data if v.get('url')])
    
    with open(output_path, 'w', encoding='utf-8') as f:
        # Write header
        f.write("=" * 80 + "\n")
        f.write(f"YouTube Playlist Direct Download URLs\n")
        f.write("=" * 80 + "\n")
        f.write(f"Playlist: {playlist_title}\n")
        f.write(f"Generated: {timestamp}\n")
        f.write(f"Total Videos: {url_count}\n")
        f.write("=" * 80 + "\n")
        f.write("\n")
        
        # Write important notes
        f.write("IMPORTANT NOTES:\n")
        f.write("- These URLs expire after several hours. Use them promptly.\n")
        f.write("- Import this file into Internet Download Manager (IDM) for batch downloading.\n")
        f.write("- Each URL is preceded by the video title as a comment.\n")
        f.write("\n")
        f.write("=" * 80 + "\n")
        f.write("\n")
        
        # Write video URLs
        for idx, video in enumerate(video_data, 1):
            url = video.get('url')
            if not url:
                continue
                
            title = video.get('title', 'Unknown Title')
            format_info = video.get('format_info', {})
            
            # Write video title as comment
            f.write(f"# Video {idx}: {title}\n")
            
            # Write format info if available
            if format_info:
                resolution = format_info.get('resolution', 'N/A')
                filesize = format_info.get('filesize_str', 'Unknown')
                f.write(f"# Resolution: {resolution} | Size: {filesize}\n")
            
            # Write direct URL
            f.write(f"{url}\n")
            f.write("\n")
    
    return url_count


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for all operating systems
    """
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > 200:
        filename = filename[:200]
    
    return filename or "output"


def generate_output_filename(playlist_title: str) -> str:
    """
    Generate a safe output filename based on playlist title.
    
    Args:
        playlist_title: Title of the playlist
        
    Returns:
        Safe filename with .txt extension
    """
    safe_title = sanitize_filename(playlist_title)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{safe_title}_{timestamp}.txt"
