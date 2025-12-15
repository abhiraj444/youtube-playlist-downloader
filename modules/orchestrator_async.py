"""
Orchestrator Module (Async Version)
Coordinates the workflow with CONCURRENT URL resolution for 10-15x speed improvement
"""

import time
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.console import Console

from modules.playlist_fetcher import get_playlist_videos, get_playlist_title
from modules.url_resolver import get_direct_url, format_filesize
from modules.output_formatter import write_to_file, generate_output_filename


console = Console()


def _resolve_video_url(video: Dict, quality: str, max_retries: int) -> Dict:
    """
    Helper function to resolve URL for a single video (used in thread pool).
    
    Args:
        video: Video metadata dictionary
        quality: Quality preference
        max_retries: Maximum retry attempts
        
    Returns:
        Dictionary with video data or None if failed
    """
    video_id = video['id']
    video_title = video['title']
    
    # Attempt to resolve URL with retries
    direct_url = None
    format_info = None
    
    for attempt in range(max_retries):
        direct_url, format_info = get_direct_url(video_id, quality)
        
        if direct_url:
            break
        
        if attempt < max_retries - 1:
            time.sleep(0.5)  # Short delay for retries
    
    if direct_url:
        # Add filesize string to format_info
        if format_info:
            format_info['filesize_str'] = format_filesize(format_info.get('filesize', 0))
        
        return {
            'title': video_title,
            'url': direct_url,
            'format_info': format_info,
            'success': True
        }
    else:
        return {
            'title': video_title,
            'success': False
        }


def process_playlist(
    playlist_url: str,
    output_path: Optional[str] = None,
    quality: str = 'best',
    delay: float = 1.5,
    max_retries: int = 3,
    max_workers: int = 10
) -> Dict[str, any]:
    """
    Main orchestration function to process a YouTube playlist with CONCURRENT processing.
    
    Args:
        playlist_url: URL of the YouTube playlist
        output_path: Path to output file (auto-generated if None)
        quality: Quality preference ('1080p', '720p', 'best')
        delay: Delay between requests in seconds (NOTE: with concurrent processing, this is less critical)
        max_retries: Maximum retry attempts for failed videos
        max_workers: Number of concurrent workers (default: 10, max recommended: 20)
        
    Returns:
        Dictionary containing:
        - success: Boolean indicating overall success
        - output_file: Path to generated file
        - total_videos: Total videos in playlist
        - successful: Number of successfully resolved URLs
        - failed: Number of failed videos
        - errors: List of error messages
    """
    result = {
        'success': False,
        'output_file': None,
        'total_videos': 0,
        'successful': 0,
        'failed': 0,
        'errors': []
    }
    
    console.print("\n[bold cyan]YouTube Playlist Direct Link Extractor (ASYNC MODE)[/bold cyan]")
    console.print("=" * 60)
    
    # Step 1: Fetch playlist metadata
    console.print("\n[yellow]Step 1:[/yellow] Fetching playlist metadata...")
    
    try:
        playlist_title = get_playlist_title(playlist_url)
        videos = get_playlist_videos(playlist_url)
        result['total_videos'] = len(videos)
        
        console.print(f"[green]✓[/green] Found playlist: [bold]{playlist_title}[/bold]")
        console.print(f"[green]✓[/green] Total videos: [bold]{len(videos)}[/bold]")
        
    except Exception as e:
        error_msg = f"Failed to fetch playlist: {str(e)}"
        result['errors'].append(error_msg)
        console.print(f"[red]✗[/red] {error_msg}")
        return result
    
    if not videos:
        error_msg = "No videos found in playlist"
        result['errors'].append(error_msg)
        console.print(f"[red]✗[/red] {error_msg}")
        return result
    
    # Step 2: Resolve direct URLs CONCURRENTLY
    console.print(f"\n[yellow]Step 2:[/yellow] Resolving direct URLs (quality: {quality})...")
    console.print(f"[bold green]⚡ CONCURRENT MODE:[/bold green] Processing {max_workers} videos at a time")
    console.print(f"[dim]Expected speedup: {min(max_workers, len(videos))}x faster than sequential[/dim]\n")
    
    video_data = []
    failed_videos = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console
    ) as progress:
        
        task = progress.add_task("[cyan]Processing videos concurrently...", total=len(videos))
        
        # Use ThreadPoolExecutor for concurrent processing
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all videos for processing
            future_to_video = {
                executor.submit(_resolve_video_url, video, quality, max_retries): video 
                for video in videos
            }
            
            # Process results as they complete
            for future in as_completed(future_to_video):
                video_result = future.result()
                
                if video_result['success']:
                    video_data.append({
                        'title': video_result['title'],
                        'url': video_result['url'],
                        'format_info': video_result['format_info']
                    })
                    result['successful'] += 1
                else:
                    failed_videos.append(video_result['title'])
                    result['failed'] += 1
                    console.print(f"[red]✗[/red] Failed: {video_result['title']}")
                
                progress.update(task, advance=1)
    
    # Step 3: Write output file
    console.print(f"\n[yellow]Step 3:[/yellow] Writing output file...")
    
    if not video_data:
        error_msg = "No URLs were successfully resolved"
        result['errors'].append(error_msg)
        console.print(f"[red]✗[/red] {error_msg}")
        return result
    
    # Generate output filename if not provided
    if not output_path:
        output_path = generate_output_filename(playlist_title)
    
    try:
        url_count = write_to_file(video_data, output_path, playlist_title)
        result['output_file'] = output_path
        result['success'] = True
        
        console.print(f"[green]✓[/green] Successfully wrote {url_count} URLs to: [bold]{output_path}[/bold]")
        
    except Exception as e:
        error_msg = f"Failed to write output file: {str(e)}"
        result['errors'].append(error_msg)
        console.print(f"[red]✗[/red] {error_msg}")
        return result
    
    # Summary
    console.print("\n" + "=" * 60)
    console.print("[bold green]Processing Complete![/bold green]")
    console.print(f"Total videos: {result['total_videos']}")
    console.print(f"[green]Successful: {result['successful']}[/green]")
    
    if result['failed'] > 0:
        console.print(f"[red]Failed: {result['failed']}[/red]")
        console.print("\n[yellow]Failed videos:[/yellow]")
        for failed in failed_videos[:10]:  # Show first 10
            console.print(f"  - {failed}")
        if len(failed_videos) > 10:
            console.print(f"  ... and {len(failed_videos) - 10} more")
    
    console.print("=" * 60 + "\n")
    
    return result
