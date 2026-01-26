# Installation Steps

Follow these steps to set up the AI video production pipeline.

## 1. Verify Prerequisites

- [ ] Windows 11 (or Windows 10 21H2+)
- [ ] 16 GB RAM minimum
- [ ] RTX 3050 GPU with latest NVIDIA drivers
- [ ] 50 GB free disk space

## 2. Install Core Software

```powershell
# Python 3.11
winget install Python.Python.3.11

# Node.js 18 LTS
winget install OpenJS.NodeJS.LTS

# Git
winget install Git.Git

# Ollama (for LLM)
winget install Ollama.Ollama
```

## 3. Install FFmpeg

1. Download from: https://www.gyan.dev/ffmpeg/builds/ (get "full" build)
2. Extract to `C:\ffmpeg`
3. Add `C:\ffmpeg\bin` to PATH
4. Verify: `ffmpeg -codecs | findstr nvenc`

## 4. Set Up Python Environment

```powershell
cd cybersec_ai_video_pipeline
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install PyTorch with CUDA
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Install packages
pip install piper-tts openai-whisper rembg pillow opencv-python numpy scipy
```

## 5. Download AI Models

```powershell
# LLM (Llama 3.2 3B)
ollama pull llama3.2:3b

# TTS Voice Model
cd voice/voice_models
Invoke-WebRequest -Uri "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx" -OutFile "en_US-lessac-medium.onnx"
Invoke-WebRequest -Uri "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx.json" -OutFile "en_US-lessac-medium.onnx.json"
cd ../..

# Avatar Model (SadTalker)
cd models/avatar
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
pip install -r requirements.txt
python scripts/download_models.py
cd ../../..

# Whisper (auto-downloads on first use)
python -c "import whisper; whisper.load_model('base')"
```

## 6. Set Up Remotion

```powershell
cd infographics/animations
npm init -y
npm install remotion @remotion/cli react react-dom lucide-react
cd ../..
```

## 7. Test Installation

```powershell
# Test CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Test TTS
echo "Test narration" | piper --model voice/voice_models/en_US-lessac-medium.onnx --output_file test.wav

# Test LLM
ollama run llama3.2:3b "Say hello"

# Test FFmpeg NVENC
ffmpeg -f lavfi -i testsrc=duration=2:size=1920x1080:rate=30 -c:v h264_nvenc test.mp4
```

## 8. Ready to Use

Pipeline is now ready. See `tools/cli_commands.md` for usage examples.
