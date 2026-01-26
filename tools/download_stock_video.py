"""
Pexels Stock Video Downloader
Downloads landscape-oriented stock footage using Pexels API
"""

import requests
import json
import sys
from pathlib import Path

PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")

def search_pexels_video(query, orientation='landscape', per_page=5):
    """Search for videos on Pexels"""
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": per_page,
        "size": "medium"  # medium, large, small
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

def download_video(video_url, output_path):
    """Download video file"""
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    
    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return output_path

def get_best_quality_url(video_files):
    """Get the best quality HD video URL (1920x1080 preferred)"""
    # Prefer 1920x1080 (Full HD)
    for file in video_files:
        if file['width'] == 1920 and file['height'] == 1080:
            return file['link']
    
    # Fallback to highest quality available
    return max(video_files, key=lambda x: x['width'] * x['height'])['link']

def main():
    if len(sys.argv) < 3:
        print("Usage: python download_stock_video.py <search_query> <output_filename>")
        print("Example: python download_stock_video.py 'person checking email' email_checking.mp4")
        sys.exit(1)
    
    query = sys.argv[1]
    output_filename = sys.argv[2]
    output_dir = Path("stock_video/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / output_filename
    
    print(f"Searching Pexels for: '{query}' (landscape only)...")
    
    try:
        results = search_pexels_video(query, orientation='landscape')
        
        if not results.get('videos'):
            print("No videos found. Try a different search term.")
            sys.exit(1)
        
        print(f"Found {len(results['videos'])} videos")
        print("\nTop results:")
        
        for i, video in enumerate(results['videos'][:3], 1):
            duration = video.get('duration', 0)
            width = video['video_files'][0]['width']
            height = video['video_files'][0]['height']
            print(f"{i}. {video.get('user', {}).get('name', 'Unknown')} - {width}x{height} ({duration}s)")
        
        # Use first result (best match)
        selected_video = results['videos'][0]
        video_url = get_best_quality_url(selected_video['video_files'])
        
        print(f"\nDownloading: {selected_video.get('url', video_url)}")
        print(f"Quality: {selected_video['video_files'][0]['quality']}")
        print(f"Saving to: {output_path}")
        
        download_video(video_url, output_path)
        
        print(f"✓ Downloaded successfully!")
        print(f"✓ File: {output_path}")
        print(f"✓ Size: {output_path.stat().st_size / 1024 / 1024:.1f} MB")
        
        # Save metadata
        metadata = {
            'query': query,
            'source': 'pexels',
            'video_id': selected_video['id'],
            'url': selected_video.get('url'),
            'duration': selected_video.get('duration'),
            'width': selected_video['width'],
            'height': selected_video['height'],
            'user': selected_video.get('user', {}).get('name'),
            'downloaded_file': str(output_path)
        }
        
        metadata_path = output_path.with_suffix('.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✓ Metadata saved: {metadata_path}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: Failed to download video: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
