# AI Cybersecurity Video Pipeline (No-Avatar)

Complete local-first, free-only AI system for producing professional cybersecurity explainer videos.

## Features

- **Animated Infographics:** Remotion/Manim-based animations explaining cybersecurity concepts
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
```

### 3. Create Your Script

Write a script using scene markers in `scripts/raw_script.txt`:

```
[STOCK_ONLY | stock:intro.mp4]
Welcome to Cybersecurity Explained.

[INFOGRAPHIC_ONLY | infographic:phishing_flow]
Phishing attacks follow four stages: reconnaissance, delivery, exploitation, and exfiltration.

[FULL_COMPOSITE | stock:hacker.mp4 | infographic:phishing_flow]
These attacks are increasingly sophisticated.
```

See `scripts/raw_script.txt` for example.

### 4. Run Production Pipeline

```powershell
# Parse script
python tools/parse_script.py scripts/raw_script.txt scripts/parsed_script.json

# Generate voice narration
python tools/generate_voice.py scripts/parsed_script.json voice/tts_output/



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

├── video/                # Scene composition and final renders
├── models/               # AI model weights (LLM, TTS)
├── tools/                # Automation scripts
├── exports/              # Final videos and assets
└── stock_video/          # Stock footage (raw → processed)
```

## Scene Types

| Type | Description | Usage |
|------|-------------|-------|
| `INFOGRAPHIC_ONLY` | Animated explanations | Technical concepts |
| `STOCK_ONLY` | B-roll footage | Context setting |
| `FULL_COMPOSITE` | Stock + infographic | Complex explanations |

## Key Technologies

- **LLM:** Llama 3.2 (3B) for script parsing
- **TTS:** Piper (en_US-lessac-medium) for voiceover

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

- Final assembly: ~3-5 min
- **Total:** ~30-45 minutes

## VRAM Optimization


- Single batch processing to avoid OOM
- CUDA cache clearing between renders
- NVENC hardware encoding for final assembly

## License

All tools are open source. Check individual model licenses:
- Llama 3.2: Meta license
- Piper TTS: MIT
- Remotion: Free for local use

## Support

For detailed technical specifications, see the implementation plan artifact.
