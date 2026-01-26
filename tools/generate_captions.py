
import whisper
import os

model = whisper.load_model('base')

def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:06.3f}".replace('.', ',')

for scene_id in ['scene_001', 'scene_004', 'scene_005']:
    audio_path = f'voice/tts_output/{scene_id}.wav'
    output_path = f'video/captions/{scene_id}.srt'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"Transcribing {scene_id}...")
    result = model.transcribe(audio_path)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, segment in enumerate(result['segments']):
            start = format_time(segment['start'])
            end = format_time(segment['end'])
            text = segment['text'].strip()
            
            f.write(f"{i + 1}\n")
            f.write(f"{start} --> {end}\n")
            f.write(f"{text}\n\n")
            
    print(f"Saved: {output_path}")

print("Done!")
