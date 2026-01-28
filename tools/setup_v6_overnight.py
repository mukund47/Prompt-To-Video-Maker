"""
V6 Full Stack Setup Script
Run this overnight to install Manim + LivePortrait dependencies
"""
import subprocess
import sys

def run(cmd):
    print(f"\n→ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print(f"⚠️ Warning: {result.stderr}")
    return result.returncode == 0

def main():
    print("=" * 60)
    print("V6 FULL STACK OVERNIGHT SETUP")
    print("=" * 60)
    
    venv_python = r"venv_v6\Scripts\python.exe"
    venv_pip = r"venv_v6\Scripts\pip.exe"
    
    # Phase 1: Core dependencies (numpy-compatible versions)
    print("\n📦 Phase 1: Installing Core Dependencies...")
    run(f"{venv_pip} install numpy==2.1.0 scipy pillow opencv-python soundfile")
    
    # Phase 2: Manim
    print("\n🎨 Phase 2: Installing Manim...")
    run(f"{venv_pip} install manim")
    
    # Phase 3: Audio tools
    print("\n🎙️ Phase 3: Installing Audio Tools...")
    run(f"{venv_pip} install edge-tts pydub")
    
    # Phase 4: LivePortrait dependencies
    print("\n👤 Phase 4: Installing LivePortrait Dependencies...")
    run(f"{venv_pip} install -r tools/LivePortrait/requirements_base.txt")
    
    # Phase 5: Verification
    print("\n✅ Phase 5: Verification...")
    
    # Test Manim
    print("\nTesting Manim...")
    result = subprocess.run(f"{venv_python} -c \"from manim import *; print('✓ Manim OK')\"", 
                          shell=True, capture_output=True, text=True)
    print(result.stdout if result.returncode == 0 else f"❌ Manim failed: {result.stderr}")
    
    # Test Edge-TTS
    print("\nTesting Edge-TTS...")
    result = subprocess.run(f"{venv_python} -c \"import edge_tts; print('✓ Edge-TTS OK')\"",
                          shell=True, capture_output=True, text=True)
    print(result.stdout if result.returncode == 0 else f"❌ Edge-TTS failed: {result.stderr}")
    
    print("\n" + "=" * 60)
    print("✨ V6 Environment Setup Complete!")
    print("=" * 60)
    print(f"\nTo use this environment:")
    print(f"  venv_v6\\Scripts\\activate")
    print(f"  python tools/render_v6_full.py")

if __name__ == "__main__":
    main()
