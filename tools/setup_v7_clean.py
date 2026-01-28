"""
V7 Clean Stack Setup Script
Installs dependencies for Kokoro-82M, LivePortrait, and WhisperX.
"""
import subprocess
import os
import sys

def run(cmd):
    print(f"\n→ {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"⚠️ Warning: Command failed with code {result.returncode}")
    return result.returncode == 0

def main():
    print("=" * 60)
    print("V7 CLEAN STACK SETUP")
    print("=" * 60)

    venv_pip = r"venv_v6\Scripts\pip.exe"
    
    # 1. Kokoro TTS
    print("\n[1/4] Installing Kokoro TTS...")
    run(f"{venv_pip} install kokoro-onnx soundfile")
    
    # 2. LivePortrait
    print("\n[2/4] Installing LivePortrait Dependencies...")
    # Base requirements usually include torch, numpy, etc.
    if os.path.exists("tools/LivePortrait/requirements_base.txt"):
        run(f"{venv_pip} install -r tools/LivePortrait/requirements_base.txt")
    if os.path.exists("tools/LivePortrait/requirements.txt"):
        run(f"{venv_pip} install -r tools/LivePortrait/requirements.txt")
        
    # 3. WhisperX (Subtitle Alignment)
    print("\n[3/4] Installing WhisperX...")
    # WhisperX requires torch audio and acts as a wrapper
    # Using git install for latest or pip if stable
    run(f"{venv_pip} install whisperx")

    # 4. Utilities
    print("\n[4/4] Installing Utilities...")
    run(f"{venv_pip} install huggingface_hub requests")

    print("\n✅ Setup Complete! Use 'venv_v6' for V7 tools.")

if __name__ == "__main__":
    main()
