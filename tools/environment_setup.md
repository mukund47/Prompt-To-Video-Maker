# Environment Setup Guide

## Prerequisites

- **Windows 11** (or Windows 10 21H2+)
- **16 GB RAM**
- **RTX 3050** (4 GB VRAM) with latest NVIDIA drivers
- **50 GB free disk space** (models + workspace)

---

## Step 1: Core Dependencies

### Python 3.10+

```powershell
# Download from python.org or use winget
winget install Python.Python.3.11

# Verify
python --version  # Should show 3.11.x
```

### Node.js 18+ (for Remotion)

```powershell
winget install OpenJS.NodeJS.LTS

# Verify
node --version  # Should show v18.x or v20.x
npm --version
```

### Git

```powershell
winget install Git.Git

# Verify
git --version
```

### FFmpeg (with NVENC support)

```powershell
# Download from https://www.gyan.dev/ffmpeg/builds/
# Get the "full" build (includes NVENC)

# Extract to C:\ffmpeg
# Add C:\ffmpeg\bin to PATH

# Verify NVENC support
ffmpeg -codecs | findstr nvenc
# Should show h264_nvenc, hevc_nvenc
```

---

## Step 2: Python Environment

```powershell
cd "C:\Users\Mukun\Downloads\Antigravity Projects\3D Models\cybersec_ai_video_pipeline"

# Create virtual environment
python -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# If execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Upgrade pip
python -m pip install --upgrade pip
```

### Install PyTorch (CUDA 11.8)

```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify CUDA
python -c "import torch; print(torch.cuda.is_available())"  # Should print True
python -c "import torch; print(torch.cuda.get_device_name(0))"  # Should show RTX 3050
```

### Install Core Packages

```powershell
pip install piper-tts openai-whisper rembg pillow opencv-python numpy scipy
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu118
```

---

## Step 3: AI Model Downloads

### 1. LLM (Llama 3.2 3B)

```powershell
# Install Ollama
winget install Ollama.Ollama

# Pull model
ollama pull llama3.2:3b

# Verify
ollama list
```

**Alternative (Manual Download):**
```powershell
# Download GGUF from HuggingFace
# https://huggingface.co/bartowski/Llama-3.2-3B-Instruct-GGUF
# Save to models/llm/
```

### 2. Text-to-Speech (Piper)

```powershell
# Piper is already installed via pip

# Download female voice model
cd voice/voice_models
Invoke-WebRequest -Uri "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx" -OutFile "en_US-lessac-medium.onnx"
Invoke-WebRequest -Uri "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json" -OutFile "en_US-lessac-medium.onnx.json"
cd ../..
```

### 3. AI Avatar (SadTalker)

```powershell
cd models/avatar
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker

pip install -r requirements.txt

# Download checkpoints (~3.5 GB)
# Windows: run manually
python scripts/download_models.py

cd ../../..
```

**VRAM Note:** First run will be slow. Monitor with `nvidia-smi` to ensure VRAM stays under 4 GB.

### 4. Background Removal (rembg)

```powershell
# Already installed, download U2-Net model on first use (automatic)
python -c "from rembg import remove; print('Model downloaded')"
```

### 5. Speech-to-Text (Whisper - Optional)

```powershell
# Already installed via openai-whisper
# Models download automatically on first use

# Pre-download base model
python -c "import whisper; whisper.load_model('base')"
```

---

## Step 4: Remotion Setup

```powershell
cd infographics/animations

# Initialize Node project
npm init -y

# Install Remotion
npm install remotion @remotion/cli react react-dom

# Install additional packages
npm install lucide-react  # Icons

# Verify
npx remotion --version
```

---

## Step 5: Directory Structure Verification

```powershell
tree /F cybersec_ai_video_pipeline
```

Should show all folders created earlier.

---

## Step 6: Test Installation

### Test PyTorch + CUDA

```powershell
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}'); print(f'Device: {torch.cuda.get_device_name(0)}')"
```

### Test Piper TTS

```powershell
echo "This is a test narration" > test.txt
piper --model voice/voice_models/en_US-lessac-medium.onnx --output_file test_output.wav < test.txt

# Play with VLC or Windows Media Player
test_output.wav
```

### Test Ollama

```powershell
ollama run llama3.2:3b "Explain phishing in one sentence"
```

### Test FFmpeg NVENC

```powershell
ffmpeg -f lavfi -i testsrc=duration=5:size=1920x1080:rate=30 -c:v h264_nvenc -preset fast test_nvenc.mp4

# Should complete without errors
```

---

## Troubleshooting

### Issue: CUDA Not Available

**Solution:**
1. Update NVIDIA drivers: `nvidia-smi`
2. Reinstall PyTorch with correct CUDA version
3. Verify GPU is not disabled in Device Manager

### Issue: SadTalker Out of Memory

**Solution:**
1. Lower resolution: use `--size 512` (not 768)
2. Close other GPU applications
3. Add `torch.cuda.empty_cache()` in batch scripts

### Issue: FFmpeg Missing NVENC

**Solution:**
1. Download "full" build from gyan.dev
2. Verify with `ffmpeg -codecs | findstr nvenc`
3. Use CPU encoding as fallback: `-c:v libx264`

### Issue: Ollama Connection Refused

**Solution:**
1. Start Ollama service: `ollama serve` (in separate terminal)
2. Or use llama-cpp-python directly with GGUF files

---

## Next Steps

After setup completion:
1. Run sample script parsing test
2. Generate test infographic
3. Render test avatar clip
4. Assemble short test video

See `tools/cli_commands.md` for usage examples.
