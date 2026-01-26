"""
Avatar Rendering Tool
Batch render avatar videos using SadTalker
Processes all AVATAR_ONLY and AVATAR_OVER_STOCK scenes
"""

import json
import sys
import subprocess
import torch
from pathlib import Path

def clear_cuda_cache():
    """Clear CUDA cache between renders to avoid OOM"""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

def render_avatar(audio_path, source_image, output_dir, size=512):
    """Render single avatar video with SadTalker"""
    sadtalker_dir = Path("models/avatar/SadTalker")
    
    cmd = [
        "python",
        str(sadtalker_dir / "inference.py"),
        "--driven_audio", str(audio_path),
        "--source_image", str(source_image),
        "--result_dir", str(output_dir),
        "--still",
        "--preprocess", "full",
        "--size", str(size),
        "--batch_size", "1",
        "--expression_scale", "1.0",
        "--pose_style", "0"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise RuntimeError(f"SadTalker failed: {result.stderr}")
    
    # Find generated video (SadTalker names it automatically)
    output_files = list(output_dir.glob("*.mp4"))
    if output_files:
        return output_files[-1]  # Return most recent
    else:
        raise FileNotFoundError("SadTalker did not generate output video")

def main():
    if len(sys.argv) not in [2, 3]:
        print("Usage: python render_avatars.py <scene_timing.json> [source_image.png]")
        sys.exit(1)
    
    timing_path = Path(sys.argv[1])
    
    if len(sys.argv) == 3:
        source_image = Path(sys.argv[2])
    else:
        source_image = Path("avatar/source_images/female_avatar_reference.png")
    
    if not timing_path.exists():
        print(f"Error: Timing file not found: {timing_path}")
        sys.exit(1)
    
    if not source_image.exists():
        print(f"Error: Source image not found: {source_image}")
        print("Please provide a female avatar reference image (frontal, neutral, well-lit)")
        sys.exit(1)
    
    # Load scenes
    with open(timing_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    # Filter scenes requiring avatar
    avatar_scenes = [s for s in scenes if 'AVATAR' in s['type']]
    
    print(f"Found {len(avatar_scenes)} scenes requiring avatar rendering")
    print(f"Source image: {source_image}")
    print(f"VRAM available: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB\n")
    
    talking_head_dir = Path("avatar/renders/talking_head_segments")
    talking_head_dir.mkdir(parents=True, exist_ok=True)
    
    for i, scene in enumerate(avatar_scenes, 1):
        scene_id = scene['scene_id']
        audio_file = scene.get('audio_file')
        
        if not audio_file or not Path(audio_file).exists():
            print(f"Scene {scene_id}: No audio file, skipping")
            continue
        
        print(f"[{i}/{len(avatar_scenes)}] Rendering scene {scene_id}...")
        print(f"  Audio: {audio_file} ({scene['audio_duration']:.1f}s)")
        
        try:
            # Clear CUDA cache before render
            clear_cuda_cache()
            
            # Render
            output_video = render_avatar(
                audio_path=audio_file,
                source_image=source_image,
                output_dir=talking_head_dir,
                size=512  # Safe for 4GB VRAM
            )
            
            # Rename to standard format
            final_path = talking_head_dir / f"scene_{scene_id:03d}.mp4"
            output_video.rename(final_path)
            
            # Update scene data
            scene['avatar_video'] = str(final_path)
            
            print(f"  ✓ Rendered: {final_path}")
        
        except Exception as e:
            print(f"  ✗ Error: {e}")
            continue
    
    # Save updated timing
    with open(timing_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Rendered {len(avatar_scenes)} avatar videos")
    print(f"✓ Updated timing: {timing_path}")

if __name__ == "__main__":
    main()
