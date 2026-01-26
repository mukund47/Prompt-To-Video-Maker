# AI Cybersecurity Video Production Pipeline

Complete local-first, free-only AI system for producing professional cybersecurity explainer videos.

## Features

- **Animated Infographics:** Remotion-based programmatic animations explaining cybersecurity concepts
- **AI Female Avatar:** SadTalker-powered talking head with overlay capabilities
- **Professional Voiceover:** Piper TTS with female voice (en_US-lessac-medium)
- **Stock Video Integration:** FFmpeg-based compositing
- **Deterministic Assembly:** Script-driven, repeatable video production

## Hardware Requirements

- **RAM:** 16 GB minimum
- **CPU:** Intel i5-12450H or equivalent
- **GPU:** RTX 3050 (4 GB VRAM) with CUDA support
- **Storage:** 50 GB free space

## Quick Start

### 1. Install Dependencies

See [`tools/install_steps.md`](tools/install_steps.md) for complete installation guide.

```powershell
# Core software
winget install Python.Python.3.11 OpenJS.NodeJS.LTS Git.Git Ollama.Ollama

# Setup Python environment
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install piper-tts openai-whisper rembg pillow opencv-python
```

### 2. Download AI Models

```powershell
# LLM for script parsing
ollama pull llama3.2:3b

# TTS voice model
cd voice/voice_models
Invoke-WebRequest -Uri "https://github.com/rhasspy/piper/releases/download/v1.2.0/en_US-lessac-medium.onnx" -OutFile "en_US-lessac-medium.onnx"

# Avatar model (SadTalker)
cd models/avatar
git clone https://github.com/OpenTalker/SadTalker.git
cd SadTalker
pip install -r requirements.txt
python scripts/download_models.py
```

### 3. Create Your Script

Write a script using scene markers in `scripts/raw_script.txt`:

```
[AVATAR_ONLY]
Welcome to Cybersecurity Explained.

[INFOGRAPHIC_ONLY | infographic:phishing_flow]
Phishing attacks follow four stages: reconnaissance, delivery, exploitation, and exfiltration.

[AVATAR_OVER_STOCK | stock:hacker.mp4 | position:bottom-right | size:25%]
These attacks are increasingly sophisticated.
```

See `scripts/raw_script.txt` for example.

### 4. Run Production Pipeline

```powershell
# Parse script
python tools/parse_script.py scripts/raw_script.txt scripts/parsed_script.json

# Generate voice narration
python tools/generate_voice.py scripts/parsed_script.json voice/tts_output/

# Render avatar videos (requires source image)
python tools/render_avatars.py scripts/scene_timing.json

# Composite overlays
python tools/composite_scenes.py scripts/scene_timing.json

# Assemble final video
python tools/assemble_video.py scripts/scene_timing.json exports/final_video.mp4
```

## Folder Structure

```
cybersec_ai_video_pipeline/
├── scripts/              # Script parsing (input → JSON)
├── infographics/         # Animated infographics (specs → Remotion → MP4)
├── stock_video/          # Stock footage (raw → processed)
├── voice/                # TTS narration (text → WAV)
├── avatar/               # AI avatar (image + audio → MP4)
├── video/                # Scene composition and final renders
├── models/               # AI model weights (LLM, TTS, avatar)
├── tools/                # Automation scripts
└── exports/              # Final videos and assets
```

## Scene Types

| Type | Description | Usage |
|------|-------------|-------|
| `AVATAR_ONLY` | Full-screen talking head | Host introduction/outro |
| `INFOGRAPHIC_ONLY` | Animated explanations | Technical concepts |
| `STOCK_ONLY` | B-roll footage | Context setting |
| `AVATAR_OVER_STOCK` | Avatar overlay on footage | Commentary over visuals |
| `FULL_COMPOSITE` | Stock + infographic + avatar | Complex explanations |

## Key Technologies

- **LLM:** Llama 3.2 (3B) for script parsing
- **TTS:** Piper (en_US-lessac-medium) for voiceover
- **Avatar:** SadTalker (optimized for 4 GB VRAM)
- **Infographics:** Remotion (React-based programmatic video)
- **Assembly:** FFmpeg with NVENC hardware encoding

## Documentation

- **Installation:** [`tools/install_steps.md`](tools/install_steps.md)
- **Environment Setup:** [`tools/environment_setup.md`](tools/environment_setup.md)
- **CLI Reference:** [`tools/cli_commands.md`](tools/cli_commands.md)
- **Technical Architecture:** See artifact [`implementation_plan.md`](C:\Users\Mukun\.gemini\antigravity\brain\f696a08f-f59d-4c7b-9e3e-978fde87f58f\implementation_plan.md)

## Performance

**Typical 5-minute video (15 scenes):**
- Script parsing: ~2-3 min
- Voice synthesis: ~1-2 min
- Avatar rendering: ~20-30 min (longest)
- Final assembly: ~3-5 min
- **Total:** ~30-45 minutes

## VRAM Optimization

- SadTalker limited to 512x512 resolution
- Single batch processing to avoid OOM
- CUDA cache clearing between renders
- NVENC hardware encoding for final assembly

## License

All tools are open source. Check individual model licenses:
- Llama 3.2: Meta license
- Piper TTS: MIT
- SadTalker: Custom license
- Remotion: Free for local use

## Support

For detailed technical specifications, see the implementation plan artifact.
