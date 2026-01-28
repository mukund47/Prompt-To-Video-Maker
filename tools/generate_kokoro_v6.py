"""
V6 High-End Kokoro TTS Audio Generator
Generates clean, human-like narration using Kokoro-82M (af_bella voice)
No SSML tags - pure text only
"""
import os
from kokoro_onnx import Kokoro

# Clean script (exactly as provided in V6 prompt)
SCRIPT = """In today's digital world, your inbox is the primary battlefield. But the threat is evolving. It starts with a sophisticated email. One click leads to a fake site, and your credentials are harvested instantly. It is not just random emails. Be aware of Spear Phishing targeting specific people, and Whaling attacks on executives. A single moment of hesitation can prevent a breach. Security is a shared responsibility."""

def generate_kokoro_audio():
    os.makedirs("voice/v6_kokoro", exist_ok=True)
    
    # Initialize Kokoro with af_bella voice
    kokoro = Kokoro("af_bella")
    
    # Split into scenes
    scenes = [
        "In today's digital world, your inbox is the primary battlefield. But the threat is evolving.",
        "It starts with a sophisticated email. One click leads to a fake site, and your credentials are harvested instantly.",
        "It is not just random emails. Be aware of Spear Phishing targeting specific people, and Whaling attacks on executives.",
        "A single moment of hesitation can prevent a breach.",
        "Security is a shared responsibility."
    ]
    
    for i, text in enumerate(scenes, 1):
        print(f"Generating scene {i}/{len(scenes)}: {text[:50]}...")
        
        # Generate audio
        samples, sample_rate = kokoro.create(text)
        
        # Save to file
        output_path = f"voice/v6_kokoro/scene_{i}_clean.wav"
        
        import soundfile as sf
        sf.write(output_path, samples, sample_rate)
        
        print(f"✓ Saved to {output_path}")
    
    print(f"\n✨ All {len(scenes)} audio clips generated successfully!")
    print("Location: voice/v6_kokoro/")

if __name__ == "__main__":
    generate_kokoro_audio()
