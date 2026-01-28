"""
V6 Fallback: Use Edge TTS with CLEAN text (no SSML)
"""
import os
import edge_tts
import asyncio

# Clean script
SCRIPT = """In today's digital world, your inbox is the primary battlefield. But the threat is evolving. It starts with a sophisticated email. One click leads to a fake site, and your credentials are harvested instantly. It is not just random emails. Be aware of Spear Phishing targeting specific people, and Whaling attacks on executives. A single moment of hesitation can prevent a breach. Security is a shared responsibility."""

async def generate_clean_audio():
    os.makedirs("voice/v6_clean", exist_ok=True)
    
    # Split into scenes
    scenes = [
        "In today's digital world, your inbox is the primary battlefield. But the threat is evolving.",
        "It starts with a sophisticated email. One click leads to a fake site, and your credentials are harvested instantly.",
        "It is not just random emails. Be aware of Spear Phishing targeting specific people, and Whaling attacks on executives.",
        "A single moment of hesitation can prevent a breach.",
        "Security is a shared responsibility."
    ]
    
    communicate = edge_tts.Communicate(text="", voice="en-US-JennyNeural", rate="+0%")
    
    for i, text in enumerate(scenes, 1):
        print(f"Generating scene {i}/{len(scenes)}: {text[:50]}...")
        
        # Create new communicate object with clean text
        comm = edge_tts.Communicate(text=text, voice="en-US-JennyNeural", rate="+0%")
        
        output_path = f"voice/v6_clean/scene_{i}_clean.mp3"
        await comm.save(output_path)
        
        print(f"✓ Saved to {output_path}")
    
    print(f"\n✨ All {len(scenes)} audio clips generated!")

if __name__ == "__main__":
    asyncio.run(generate_clean_audio())
