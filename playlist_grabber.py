#!/usr/bin/env python3
"""
YouTube Playlist Direct Link Extractor
A CLI tool to extract direct download URLs from YouTube playlists for use with IDM

Usage:
    python playlist_grabber.py "PLAYLIST_URL" [OPTIONS]

Example:
    python playlist_grabber.py "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"
    python playlist_grabber.py "PLAYLIST_URL" -o output.txt -q 1080p -d 2.0
    python playlist_grabber.py "PLAYLIST_URL" --async --workers 15  # FAST MODE!
"""

import argparse
import sys


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Extract direct download URLs from YouTube playlists',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/playlist?list=PLxxxxx"
  %(prog)s "PLAYLIST_URL" -o my_playlist.txt
  %(prog)s "PLAYLIST_URL" -q 1080p -d 2.0
  %(prog)s "PLAYLIST_URL" --quality 720p --delay 1.0
  %(prog)s "PLAYLIST_URL" --async --workers 15  # 10-15x FASTER!

Quality Options:
  best   - Best available quality (default)
  1080p  - 1080p resolution (Full HD)
  720p   - 720p resolution (HD)

Performance Modes:
  Sequential (default) - Processes videos one at a time
  Async (--async)      - Processes multiple videos concurrently (10-15x faster!)
                        Use --workers to control concurrency (default: 10, max: 20)

Notes:
  - Generated URLs expire after several hours
  - Use the output file with Internet Download Manager (IDM)
  - Larger playlists take longer due to rate limiting
  - Async mode dramatically speeds up processing!
        """
    )
    
    parser.add_argument(
        'playlist_url',
        help='YouTube playlist URL'
    )
    
    parser.add_argument(
        '-o', '--output',
        dest='output_file',
        help='Output file path (auto-generated if not specified)',
        default=None
    )
    
    parser.add_argument(
        '-q', '--quality',
        dest='quality',
        choices=['best', '1080p', '720p'],
        default='best',
        help='Video quality preference (default: best)'
    )
    
    parser.add_argument(
        '-d', '--delay',
        dest='delay',
        type=float,
        default=1.5,
        help='Delay between requests in seconds (default: 1.5, less important in async mode)'
    )
    
    parser.add_argument(
        '-r', '--retries',
        dest='retries',
        type=int,
        default=3,
        help='Maximum retry attempts for failed videos (default: 3)'
    )
    
    parser.add_argument(
        '--async',
        dest='use_async',
        action='store_true',
        help='Enable async mode for 10-15x faster processing (RECOMMENDED for large playlists!)'
    )
    
    parser.add_argument(
        '-w', '--workers',
        dest='workers',
        type=int,
        default=10,
        help='Number of concurrent workers in async mode (default: 10, max recommended: 20)'
    )
    
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='%(prog)s 2.0.0 (Async Edition)'
    )
    
    args = parser.parse_args()
    
    # Validate playlist URL
    if not args.playlist_url.startswith('http'):
        print("Error: Please provide a valid YouTube playlist URL")
        sys.exit(1)
    
    if 'list=' not in args.playlist_url:
        print("Error: URL does not appear to be a playlist (missing 'list=' parameter)")
        sys.exit(1)
    
    # Validate delay
    if args.delay < 0.5:
        print("Warning: Delay less than 0.5s may trigger rate limiting")
        args.delay = 0.5
    
    # Validate workers
    if args.workers < 1:
        print("Error: Workers must be at least 1")
        sys.exit(1)
    
    if args.workers > 20:
        print("Warning: More than 20 workers may trigger YouTube rate limiting. Setting to 20.")
        args.workers = 20
    
    # Import appropriate orchestrator based on mode
    if args.use_async:
        from modules.orchestrator_async import process_playlist
        print(f"\n🚀 ASYNC MODE ENABLED: Processing with {args.workers} concurrent workers")
        print("⚡ Expected speedup: 10-15x faster than sequential mode!\n")
    else:
        from modules.orchestrator import process_playlist
    
    # Process playlist
    try:
        if args.use_async:
            result = process_playlist(
                playlist_url=args.playlist_url,
                output_path=args.output_file,
                quality=args.quality,
                delay=args.delay,
                max_retries=args.retries,
                max_workers=args.workers
            )
        else:
            result = process_playlist(
                playlist_url=args.playlist_url,
                output_path=args.output_file,
                quality=args.quality,
                delay=args.delay,
                max_retries=args.retries
            )
        
        # Exit with appropriate code
        if result['success']:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(130)
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
