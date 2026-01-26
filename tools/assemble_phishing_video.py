
import subprocess
import json
import os
import shutil
from pathlib import Path

def run_ffmpeg(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def main():
    # Paths
    avatar_dir = Path("avatar/renders/talking_head_segments")
    infographic = Path("infographics/renders/phishing_flow.mp4")
    stock_raw = Path("stock_video/raw/email_checking.mp4")
    captions_dir = Path("video/captions")
    output_file = Path("exports/phishing_awareness_final.mp4")
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    temp_dir = Path("video/temp_assembly")
    temp_dir.mkdir(parents=True, exist_ok=True)
    
    # 0. Generate Background
    print("Creating background...")
    bg_stock = temp_dir / "background_stock.mp4"
    run_ffmpeg([
        "ffmpeg", "-y",
        "-stream_loop", "-1",
        "-i", str(stock_raw),
        "-t", "30",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,boxblur=20:10",
        "-c:v", "h264_nvenc", "-preset", "fast",
        "-an",
        str(bg_stock)
    ])

    def process_avatar_scene(scene_id):
        input_mp4 = avatar_dir / f"{scene_id}.mp4"
        srt_original = captions_dir / f"{scene_id}.srt"
        output_mp4 = temp_dir / f"{scene_id}_1080p.mp4"
        
        # Temp SRT in current directory to avoid path issues
        temp_srt = Path(f"temp_{scene_id}.srt")
        
        if not input_mp4.exists():
            print(f"Warning: {input_mp4} missing")
            return None
            
        shutil.copy(srt_original, temp_srt)
        print(f"Compositing {scene_id} using {temp_srt}...")
        
        try:
            # Use simple filename for subtitles filter
            run_ffmpeg([
                "ffmpeg", "-y",
                "-i", str(bg_stock),
                "-i", str(input_mp4),
                "-filter_complex", f"[1:v]scale=512:512[ava];[0:v][ava]overlay=(W-w)/2:(H-h)/2:shortest=1[vcomp];[vcomp]subtitles='{temp_srt.name}':force_style='FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,MarginV=50'[outv]",
                "-map", "[outv]",
                "-map", "1:a",
                "-c:v", "h264_nvenc", "-preset", "fast",
                "-c:a", "aac",
                str(output_mp4)
            ])
        finally:
            if temp_srt.exists():
                os.remove(temp_srt)
                
        return output_mp4

    # 1. Process Scenes
    s1 = process_avatar_scene("scene_001")
    s4 = process_avatar_scene("scene_004")
    s5 = process_avatar_scene("scene_005")

    # 2. Process Infographic
    print("Processing Infographic...")
    info_out = temp_dir / "infographic_1080p.mp4"
    if infographic.exists():
        run_ffmpeg([
            "ffmpeg", "-y",
            "-i", str(infographic),
            "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "h264_nvenc", "-preset", "fast",
            "-c:a", "aac",
            "-shortest",
            str(info_out)
        ])
    else:
        print("Warning: Infographic missing")
        info_out = None

    # 3. Process Stock
    print("Processing Stock...")
    stock_final = temp_dir / "stock_scene.mp4"
    run_ffmpeg([
        "ffmpeg", "-y",
        "-i", str(stock_raw),
        "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100",
        "-t", "5",
        "-vf", "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "h264_nvenc", "-preset", "fast",
        "-c:a", "aac",
        str(stock_final)
    ])

    # 4. Concat
    concat_list = temp_dir / "concat_list.txt"
    with open(concat_list, 'w') as f:
        if s1: f.write(f"file '{s1.name}'\n")
        if info_out: f.write(f"file '{info_out.name}'\n")
        f.write(f"file '{stock_final.name}'\n")
        if s4: f.write(f"file '{s4.name}'\n")
        if s5: f.write(f"file '{s5.name}'\n")
    
    print("Final Assembly...")
    run_ffmpeg([
        "ffmpeg", "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(output_file)
    ])
    
    print(f"✓ DONE: {output_file}")

if __name__ == "__main__":
    main()
