"""
Scene Composition Tool
Composite avatar overlays onto stock footage using FFmpeg
"""

import json
import sys
import subprocess
from pathlib import Path



def composite_infographic_over_stock(stock_video, infographic_video, output_path):
    """Composite stock + infographic (No Avatar)"""
    
    # Simple overlay
    filter_complex = "[0][1]overlay=0:0"
    
    cmd = [
        "ffmpeg",
        "-i", str(stock_video),
        "-i", str(infographic_video),
        "-filter_complex", filter_complex,
        "-c:v", "h264_nvenc",
        "-preset", "fast",
        "-c:a", "copy",
        "-y",
        str(output_path)
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg composition failed: {result.stderr}")
    
    return output_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python composite_scenes.py <scene_timing.json>")
        sys.exit(1)
    
    timing_path = Path(sys.argv[1])
    
    if not timing_path.exists():
        print(f"Error: Timing file not found: {timing_path}")
        sys.exit(1)
    
    # Load scenes
    with open(timing_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    # Filter scenes requiring composition - now only FULL_COMPOSITE
    composite_scenes = [s for s in scenes if s['type'] == 'FULL_COMPOSITE']
    
    print(f"Found {len(composite_scenes)} scenes requiring composition\n")
    
    output_dir = Path("video/scenes/composited_scenes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, scene in enumerate(composite_scenes, 1):
        scene_id = scene['scene_id']
        scene_type = scene['type']
        vis_req = scene['visual_requirements']
        
        print(f"[{i}/{len(composite_scenes)}] Compositing scene {scene_id} ({scene_type})...")
        
        try:
            if scene_type == "FULL_COMPOSITE":
                # Stock + Infographic
                stock_file = vis_req.get('stock_file')
                infographic_id = vis_req.get('infographic_id')
                
                stock_path = Path(f"stock_video/processed/{stock_file}")
                infographic_path = Path(f"video/scenes/infographic_scenes/{infographic_id}.mp4")
                
                if not all([stock_path.exists(), infographic_path.exists()]):
                    print(f"  ✗ Missing assets for full composite")
                    continue
                
                output_path = output_dir / f"scene_{scene_id:03d}_composite.mp4"
                
                composite_infographic_over_stock(
                    stock_video=stock_path,
                    infographic_video=infographic_path,
                    output_path=output_path
                )
                
                print(f"  ✓ Composited: {output_path}")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    print(f"\n✓ Composited {len(composite_scenes)} scenes")

if __name__ == "__main__":
    main()
