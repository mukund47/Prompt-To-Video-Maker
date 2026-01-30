"""
Voice Generation Tool
Generate TTS audio for all scenes using Piper TTS
Updates scene_timing.json with actual audio durations
"""

import json
import sys
import subprocess
import wave
from pathlib import Path

def get_wav_duration(wav_path):
    """Get duration of WAV file in seconds"""
    with wave.open(str(wav_path), 'r') as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        return frames / float(rate)

def synthesize_speech(text, output_path, model_path):
    """Synthesize speech using Piper TTS"""
    # Piper command
    cmd = [
        "piper",
        "--model", str(model_path),
        "--output_file", str(output_path)
    ]
    
    try:
        # Run Piper with text input
        process = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = process.communicate(input=text)
        
        if process.returncode != 0:
            raise RuntimeError(f"Piper failed: {stderr}")

    except Exception as e:
        print(f"Warning: Piper TTS not available ({e}). Generating silent placeholder.")
        # Generate 3 seconds of silence using wave
        with wave.open(str(output_path), 'w') as wav:
            wav.setnchannels(1)
            wav.setsampwidth(2)
            wav.setframerate(22050)
            # 3 seconds * 22050 samples
            data = b'\x00' * 22050 * 3 * 2
            wav.writeframes(data)
    
    return output_path

def main():
    if len(sys.argv) not in [3, 4]:
        print("Usage: python generate_voice.py <parsed_script.json> <output_dir> [voice_model.onnx]")
        sys.exit(1)
    
    script_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    # Default voice model
    if len(sys.argv) == 4:
        voice_model = Path(sys.argv[3])
    else:
        voice_model = Path("voice/voice_models/en_US-lessac-medium.onnx")
    
    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)
    
    if not voice_model.exists():
        print(f"Error: Voice model not found: {voice_model}")
        print("Download from: https://github.com/rhasspy/piper/releases/")
        sys.exit(1)
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load parsed script
    with open(script_path, 'r', encoding='utf-8') as f:
        scenes = json.load(f)
    
    print(f"Generating TTS for {len(scenes)} scenes...")
    
    # Track timing
    cumulative_time = 0.0
    
    for i, scene in enumerate(scenes, 1):
        scene_id = scene['scene_id']
        text = scene['narration_text']
        
        if not text:
            print(f"Scene {scene_id}: No narration text, skipping")
            continue
        
        output_file = output_dir / f"scene_{scene_id:03d}.wav"
        
        print(f"Scene {scene_id}/{len(scenes)}: Synthesizing... ", end='', flush=True)
        
        try:
            synthesize_speech(text, output_file, voice_model)
            duration = get_wav_duration(output_file)
            
            # Update scene with actual audio info
            scene['audio_file'] = str(output_file)
            scene['audio_duration'] = round(duration, 2)
            scene['start_time'] = round(cumulative_time, 2)
            scene['end_time'] = round(cumulative_time + duration, 2)
            
            cumulative_time += duration
            
            print(f"✓ ({duration:.2f}s)")
        
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
    
    # Save updated timing file
    timing_path = script_path.parent / "scene_timing.json"
    with open(timing_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Generated {len(scenes)} audio files")
    print(f"✓ Total duration: {cumulative_time:.2f}s ({cumulative_time/60:.1f} min)")
    print(f"✓ Updated timing: {timing_path}")

if __name__ == "__main__":
    main()
