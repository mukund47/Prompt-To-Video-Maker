"""
Scene Composition Tool
Composite avatar overlays onto stock footage using FFmpeg
"""

import json
import sys
import subprocess
from pathlib import Path

def composite_avatar_over_stock(stock_video, avatar_video, output_path, 
                                 position="bottom-right", size_percent=25):
    """Composite avatar overlay on stock footage"""
    
    # Position calculations
    positions = {
        "bottom-right": "W-w-20:H-h-20",
        "bottom-left": "20:H-h-20",
        "top-right": "W-w-20:20",
        "top-left": "20:20",
        "center": "(W-w)/2:(H-h)/2"
    }
    
    overlay_pos = positions.get(position, positions["bottom-right"])
    scale_factor = size_percent / 100.0
    
    # FFmpeg filter complex
    filter_complex = (
        f"[1]scale=iw*{scale_factor}:ih*{scale_factor}[avatar];"
        f"[0][avatar]overlay={overlay_pos}"
    )
    
    cmd = [
        "ffmpeg",
        "-i", str(stock_video),
        "-i", str(avatar_video),
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

def composite_full_scene(stock_video, infographic_video, avatar_video, output_path,
                         avatar_size_percent=15):
    """Composite stock + infographic + avatar"""
    
    scale_factor = avatar_size_percent / 100.0
    
    # Three-layer composition
    filter_complex = (
        f"[0][1]overlay=0:0[base_with_info];"
        f"[2]scale=iw*{scale_factor}:ih*{scale_factor}[small_avatar];"
        f"[base_with_info][small_avatar]overlay=W-w-10:H-h-10"
    )
    
    cmd = [
        "ffmpeg",
        "-i", str(stock_video),
        "-i", str(infographic_video),
        "-i", str(avatar_video),
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
    
    # Filter scenes requiring composition
    composite_scenes = [s for s in scenes if s['type'] in ['AVATAR_OVER_STOCK', 'FULL_COMPOSITE']]
    
    print(f"Found {len(composite_scenes)} scenes requiring composition\n")
    
    output_dir = Path("video/scenes/avatar_overlay_scenes")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    for i, scene in enumerate(composite_scenes, 1):
        scene_id = scene['scene_id']
        scene_type = scene['type']
        vis_req = scene['visual_requirements']
        
        print(f"[{i}/{len(composite_scenes)}] Compositing scene {scene_id} ({scene_type})...")
        
        try:
            if scene_type == "AVATAR_OVER_STOCK":
                # Stock + Avatar
                stock_file = vis_req.get('stock_file')
                stock_path = Path(f"stock_video/processed/{stock_file}")
                
                avatar_video = scene.get('avatar_video')
                if not avatar_video:
                    avatar_video = f"avatar/renders/overlay_segments/scene_{scene_id:03d}_nobg.mp4"
                
                avatar_path = Path(avatar_video)
                
                if not stock_path.exists():
                    print(f"  ✗ Stock video not found: {stock_path}")
                    continue
                
                if not avatar_path.exists():
                    print(f"  ✗ Avatar video not found: {avatar_path}")
                    continue
                
                position = vis_req.get('avatar_position', 'bottom-right')
                size_str = vis_req.get('avatar_size', '25%')
                size = int(size_str.rstrip('%'))
                
                output_path = output_dir / f"scene_{scene_id:03d}_composite.mp4"
                
                composite_avatar_over_stock(
                    stock_video=stock_path,
                    avatar_video=avatar_path,
                    output_path=output_path,
                    position=position,
                    size_percent=size
                )
                
                print(f"  ✓ Composited: {output_path}")
            
            elif scene_type == "FULL_COMPOSITE":
                # Stock + Infographic + Avatar
                stock_file = vis_req.get('stock_file')
                infographic_id = vis_req.get('infographic_id')
                
                stock_path = Path(f"stock_video/processed/{stock_file}")
                infographic_path = Path(f"video/scenes/infographic_scenes/{infographic_id}.mp4")
                avatar_path = Path(scene.get('avatar_video', f"avatar/renders/overlay_segments/scene_{scene_id:03d}_nobg.mp4"))
                
                if not all([stock_path.exists(), infographic_path.exists(), avatar_path.exists()]):
                    print(f"  ✗ Missing assets for full composite")
                    continue
                
                output_path = output_dir / f"scene_{scene_id:03d}_composite.mp4"
                
                composite_full_scene(
                    stock_video=stock_path,
                    infographic_video=infographic_path,
                    avatar_video=avatar_path,
                    output_path=output_path,
                    avatar_size_percent=15
                )
                
                print(f"  ✓ Composited: {output_path}")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    print(f"\n✓ Composited {len(composite_scenes)} scenes")

if __name__ == "__main__":
    main()
