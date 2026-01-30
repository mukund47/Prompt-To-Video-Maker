"""
Video Assembly Tool
Assemble all rendered scenes into final video using FFmpeg
"""

import json
import sys
import subprocess
from pathlib import Path

def get_scene_video_path(scene, base_dir=Path(".")):
    """Route to correct rendered scene file based on type"""
    scene_type = scene['type']
    scene_id = scene['scene_id']
    
    # Check for pre-composited scene first
    composite_path = base_dir / f"video/scenes/composited_scenes/scene_{scene_id:03d}_composite.mp4"
    if composite_path.exists():
        return composite_path
    
    # All legacy avatar scenes are now handled as stock or skipped
    if scene_type in ["STOCK_ONLY", "AVATAR_ONLY", "AVATAR_OVER_STOCK"]:
        stock_file = scene['visual_requirements'].get('stock_file', f'scene_{scene_id}.mp4')
        return base_dir / f"stock_video/processed/{stock_file}"
    
    elif scene_type == "INFOGRAPHIC_ONLY":
        infographic_id = scene['visual_requirements'].get('infographic_id', f'scene_{scene_id}')
        return base_dir / f"video/scenes/infographic_scenes/{infographic_id}.mp4"
    
    elif scene_type == "FULL_COMPOSITE":
        # Full composite is Stock + Infographic
        return composite_path
    
    else:
        # Default fallback
        return base_dir / f"video/scenes/scene_{scene_id:03d}.mp4"

def create_concat_file(scenes, output_path, base_dir=Path(".")):
    """Create FFmpeg concat list"""
    lines = []
    
    for scene in scenes:
        video_path = get_scene_video_path(scene, base_dir)
        
        if not video_path.exists():
            print(f"Warning: Scene {scene['scene_id']} video not found: {video_path}")
            continue
        
        # FFmpeg concat format
        lines.append(f"file '{video_path.absolute()}'")
        
        # Duration (optional, for precise timing)
        if 'audio_duration' in scene:
            lines.append(f"duration {scene['audio_duration']}")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    return output_path

def assemble_video(concat_file, output_video, use_nvenc=True):
    """Assemble final video using FFmpeg"""
    codec = "h264_nvenc" if use_nvenc else "libx264"
    preset = "fast" if use_nvenc else "medium"
    
    cmd = [
        "ffmpeg",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_file),
        "-c:v", codec,
        "-preset", preset,
        "-b:v", "8M",
        "-c:a", "aac",
        "-b:a", "192k",
        "-y",  # Overwrite
        str(output_video)
    ]
    
    print(f"Assembling video with {codec}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        # Try fallback to CPU encoding
        if use_nvenc:
            print("NVENC failed, falling back to CPU encoding...")
            return assemble_video(concat_file, output_video, use_nvenc=False)
        else:
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
    return output_video

def main():
    if len(sys.argv) != 3:
        print("Usage: python assemble_video.py <scene_timing.json> <output_video.mp4>")
        sys.exit(1)
    
    timing_path = Path(sys.argv[1])
    output_video = Path(sys.argv[2])
    
    if not timing_path.exists():
        print(f"Error: Timing file not found: {timing_path}")
        sys.exit(1)
    
    # Load scenes
    with open(timing_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    print(f"Assembling {len(scenes)} scenes...")
    
    # Create concat file
    concat_file = Path("video/concat_list.txt")
    concat_file.parent.mkdir(parents=True, exist_ok=True)
    
    create_concat_file(scenes, concat_file)
    print(f"✓ Created concat list: {concat_file}")
    
    # Ensure output directory exists
    output_video.parent.mkdir(parents=True, exist_ok=True)
    
    # Assemble
    assemble_video(concat_file, output_video)
    
    print(f"✓ Final video: {output_video}")
    
    # Get final duration
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
         "-of", "default=noprint_wrappers=1:nokey=1", str(output_video)],
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        duration = float(result.stdout.strip())
        print(f"✓ Duration: {duration:.1f}s ({duration/60:.1f} min)")

if __name__ == "__main__":
    main()
