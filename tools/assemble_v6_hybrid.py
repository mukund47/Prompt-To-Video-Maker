"""
V6 Hybrid Production Assembly (Updated with Reference Asset)
Uses: Clean Edge-TTS audio + Professional diagram overlay + Wav2Lip avatar
"""
import os
import subprocess

def run_cmd(cmd):
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
    return result.returncode == 0

def main():
    print("🎬 V6 Hybrid Production Assembly")
    print("=" * 50)
    
    # Step 1: Use the professional reference diagram directly
    print("\n📊 Step 1: Preparing Professional Diagram...")
    
    # Create a 15-second video from the static diagram with zoom effect
    if not os.path.exists("renders/v6_diagram_flow.mp4"):
        print("Creating flow diagram video with zoom...")
        run_cmd('ffmpeg -y -loop 1 -i assets/phishing_flow_reference.png -vf "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,zoompan=z=\'min(zoom+0.001,1.2)\':d=360:x=iw/2-(iw/zoom/2):y=ih/2-(ih/zoom/2):s=1920x1080,fps=24" -t 15 -pix_fmt yuv420p renders/v6_diagram_flow.mp4')
    
    # Use existing circular diagram or render from Remotion
    print("\n📊 Step 2: Circular Diagram...")
    if not os.path.exists("renders/v6_circular.mp4"):
        os.chdir("infographics/animations")
        run_cmd("npx remotion render src/index.js CircularFlow ../../renders/v6_circular.mp4")
        os.chdir("../..")
    
    # Step 3: Extract audio to WAV for Wav2Lip
    print("\n🎙️ Step 3: Converting Clean Audio...")
    for i in range(1, 6):
        if not os.path.exists(f'voice/v6_clean/scene_{i}_clean.wav'):
            run_cmd(f'ffmpeg -y -i voice/v6_clean/scene_{i}_clean.mp3 voice/v6_clean/scene_{i}_clean.wav')
    
    # Step 4: Regenerate Wav2Lip avatars
    print("\n👤 Step 4: Generating Avatar Clips...")
    if not os.path.exists("renders/v6_avatar_intro.mp4"):
        print("Generating intro avatar...")
        run_cmd('venv_v2_polish\\Scripts\\python tools\\wav2lip_inference.py --face "avatar\\source_images\\Female Avatar.png" --audio voice/v6_clean/scene_1_clean.wav --outfile renders/v6_avatar_intro.mp4')
    
    if not os.path.exists("renders/v6_avatar_outro.mp4"):
        print("Generating outro avatar...")
        run_cmd('venv_v2_polish\\Scripts\\python tools\\wav2lip_inference.py --face "avatar\\source_images\\Female Avatar.png" --audio voice/v6_clean/scene_5_clean.wav --outfile renders/v6_avatar_outro.mp4')
    
    # Step 5: Create simple SRT subtitles
    print("\n📝 Step 5: Generating Subtitles...")
    subtitles = [
        ("00:00:00,000", "00:00:06,000", "In today's digital world, your inbox\\nis the primary battlefield."),
        ("00:00:06,000", "00:00:12,000", "It starts with a sophisticated email.\\nOne click leads to a fake site."),
        ("00:00:12,000", "00:00:18,000", "Be aware of Spear Phishing\\ntargeting specific people."),
        ("00:00:18,000", "00:00:22,000", "A single moment of hesitation\\ncan prevent a breach."),
        ("00:00:22,000", "00:00:27,000", "Security is a shared responsibility."),
    ]
    
    with open("renders/v6_subtitles.srt", "w", encoding="utf-8") as f:
        for i, (start, end, text) in enumerate(subtitles, 1):
            f.write(f"{i}\n{start} --> {end}\n{text}\n\n")
    
    # Step 6: Assemble with audio sync
    print("\n🎞️ Step 6: Syncing Audio to Video...")
    
    scenes = [
        ("renders/v6_avatar_intro.mp4", "voice/v6_clean/scene_1_clean.mp3", "intro"),
        ("renders/v6_diagram_flow.mp4", "voice/v6_clean/scene_2_clean.mp3", "flow"),
        ("renders/v6_circular.mp4", "voice/v6_clean/scene_3_clean.mp3", "circular"),
        ("renders/v6_avatar_outro.mp4", "voice/v6_clean/scene_5_clean.mp3", "outro"),
    ]
    
    # Process each with audio
    for video, audio, name in scenes:
        if os.path.exists(video):
            run_cmd(f'ffmpeg -y -i "{video}" -i "{audio}" -c:v libx264 -c:a aac -shortest renders/v6_sync_{name}.mp4')
    
    # Concatenate
    with open("renders/v6_concat.txt", "w") as f:
        for _, _, name in scenes:
            if os.path.exists(f"renders/v6_sync_{name}.mp4"):
                f.write(f"file 'v6_sync_{name}.mp4'\n")
    
    print("\n🎬 Step 7: Final Assembly with Subtitles...")
    run_cmd('ffmpeg -y -f concat -safe 0 -i renders/v6_concat.txt -vf "subtitles=renders/v6_subtitles.srt:force_style=\'FontName=Montserrat,FontSize=28,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,BackColour=&H80000000,BorderStyle=4,Outline=0,Shadow=0,MarginV=60\'" -c:v libx264 -preset slow -crf 18 -c:a copy exports/phishing_v6_final.mp4')
    
    print("\n✨ V6 Production Complete!")
    print(f"📹 Output: exports/phishing_v6_final.mp4")
    print(f"📊 Using Professional Reference Diagram: assets/phishing_flow_reference.png")
    
    # Cleanup
    for _, _, name in scenes:
        temp_file = f"renders/v6_sync_{name}.mp4"
        if os.path.exists(temp_file):
            os.remove(temp_file)

if __name__ == "__main__":
    main()
