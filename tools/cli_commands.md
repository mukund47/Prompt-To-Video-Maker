# CLI Commands Reference

Quick reference for all pipeline commands.

---

## 1. Script Parsing

```powershell
# Parse raw script into structured JSON
python tools/parse_script.py scripts/raw_script.txt scripts/parsed_script.json

# View parsed output (PowerShell)
Get-Content scripts/parsed_script.json | python -m json.tool

# Or in Git Bash
cat scripts/parsed_script.json | python -m json.tool
```

---

## 2. Infographic Generation

```powershell
# Generate infographic specs from parsed script
python tools/generate_infographic_specs.py scripts/parsed_script.json infographics/specs/llm_generated_infographic_specs.json

# Render all infographics with Remotion
cd infographics/animations
npx remotion render src/index.tsx PhishingFlow ../../video/scenes/infographic_scenes/phishing_flow.mp4 --codec h264

# Batch render all specs
python ../../tools/render_all_infographics.py
```

---

## 3. Voice Synthesis

```powershell
# Generate TTS audio for all scenes
python tools/generate_voice.py scripts/parsed_script.json voice/tts_output/

# Generate single scene audio
echo "This is narration text" | piper --model voice/voice_models/en_US-lessac-medium.onnx --output_file voice/tts_output/scene_001.wav

# Normalize audio levels (apply ONCE on master mix, not per-scene)
# See "Final Assembly" section for proper loudnorm usage
```

---

## 4. Avatar Rendering

```powershell
# Render single talking-head clip
python models/avatar/SadTalker/inference.py \
  --driven_audio avatar/audio_input/scene_001.wav \
  --source_image avatar/source_images/female_avatar_reference.png \
  --result_dir avatar/renders/talking_head_segments/ \
  --still --preprocess full --size 512 --batch_size 1

# Batch render all avatar scenes
python tools/render_avatars.py scripts/scene_timing.json

# Remove background for overlays (frame-by-frame approach)
# Extract frames
ffmpeg -i avatar/renders/talking_head_segments/scene_003.mp4 avatar/temp/frames_%04d.png

# Remove background
rembg p -m u2net avatar/temp/frames avatar/temp/frames_nobg

# Reassemble with transparency
ffmpeg -framerate 30 -i avatar/temp/frames_nobg/%04d.png -c:v h264_nvenc -pix_fmt yuv420p avatar/renders/overlay_segments/scene_003_nobg.mp4
```

---

## 5. Stock Video Processing

```powershell
# Trim stock video
ffmpeg -i stock_video/raw/hacker_typing.mp4 -ss 00:00:05 -t 00:00:10 -c copy stock_video/selected/hacker_typing_trimmed.mp4

# Resize to 1080p
ffmpeg -i stock_video/selected/hacker_typing_trimmed.mp4 -vf scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2 stock_video/processed/hacker_typing.mp4

# Color correction (optional)
ffmpeg -i input.mp4 -vf eq=brightness=0.05:saturation=1.2 output.mp4
```

---

## 6. Scene Composition

```powershell
# Composite avatar over stock footage
ffmpeg -i stock_video/processed/base.mp4 \
       -i avatar/renders/overlay_segments/avatar_nobg.mp4 \
       -filter_complex "[1]scale=iw*0.25:ih*0.25[avatar];[0][avatar]overlay=W-w-20:H-h-20" \
       -c:v h264_nvenc -preset fast \
       video/scenes/avatar_overlay_scenes/scene_003_composite.mp4

# Full composite (stock + infographic + avatar)
ffmpeg -i stock_video/processed/base.mp4 \
       -i video/scenes/infographic_scenes/overlay.mp4 \
       -i avatar/renders/overlay_segments/avatar_nobg.mp4 \
       -filter_complex "[0][1]overlay=0:0[base_with_info];[2]scale=iw*0.15:ih*0.15[small_avatar];[base_with_info][small_avatar]overlay=W-w-10:H-h-10" \
       -c:v h264_nvenc -preset fast \
       video/scenes/full_composite/scene_007.mp4

# Batch composite all scenes
python tools/composite_scenes.py scripts/scene_timing.json
```

---

## 7. Final Assembly

```powershell
# Assemble all scenes into final video
python tools/assemble_video.py scripts/scene_timing.json exports/final_video.mp4

# Add background music (with loudnorm on master audio)
ffmpeg -i exports/final_video.mp4 \
       -i voice/music/background_ambient.mp3 \
       -filter_complex "[1]volume=0.15[bg];[0:a]loudnorm[norm];[norm][bg]amix=inputs=2:duration=first" \
       -c:v h264_nvenc -preset fast \
       -c:a aac -b:a 192k \
       exports/final_video_with_music.mp4

# Generate captions
whisper exports/final_video.mp4 --model base --output_format srt --output_dir exports/

# Burn captions into video
ffmpeg -i exports/final_video.mp4 \
       -vf subtitles=exports/final_video.srt \
       -c:v h264_nvenc -preset fast \
       exports/final_video_with_subs.mp4
```

---

## 8. Utility Commands

```powershell
# Extract thumbnail at 5 seconds
ffmpeg -i exports/final_video.mp4 -ss 00:00:05 -vframes 1 exports/thumbnails/thumb.jpg

# Get video duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 video.mp4

# Check VRAM usage during rendering
nvidia-smi --query-gpu=memory.used,memory.total --format=csv -l 1

# Monitor GPU utilization
nvidia-smi dmon -s u

# Clear CUDA cache (in Python script)
python -c "import torch; torch.cuda.empty_cache(); print('Cache cleared')"
```

---

## 9. LLM Inference (Ollama)

```powershell
# Interactive mode
ollama run llama3.2:3b

# Single prompt
ollama run llama3.2:3b "Parse this script: [script text]"

# JSON output mode (requires explicit JSON instruction in prompt)
ollama run llama3.2:3b --format json "Generate infographic spec for: phishing attack. Output valid JSON only."

# Note: --format json does not guarantee valid JSON unless prompt explicitly enforces it
```

---

## 10. Debugging

```powershell
# Verify file durations match
ffprobe -v error -select_streams v:0 -show_entries stream=duration -of default=noprint_wrappers=1:nokey=1 scene_001.mp4

# Check audio sync
ffplay -vf "drawtext=text='%{pts\:hms}':x=10:y=10:fontsize=24" video.mp4

# Test concat list
ffmpeg -f concat -safe 0 -i video/concat_list.txt -c copy test_concat.mp4

# Validate FFmpeg NVENC
ffmpeg -hide_banner -encoders | findstr nvenc
```

---

## Golden Workflow (Daily Production)

This is the core loop for day-to-day video production:

```powershell
# 1. Parse script
python tools/parse_script.py scripts/raw_script.txt scripts/parsed_script.json

# 2. Generate narration + timing
python tools/generate_voice.py scripts/parsed_script.json voice/tts_output/

# 3. Generate infographic specs (if using LLM-generated specs)
python tools/generate_infographic_specs.py scripts/parsed_script.json infographics/specs/

# 4. Render visuals
python tools/render_all_infographics.py
python tools/render_avatars.py scripts/scene_timing.json
python tools/composite_scenes.py scripts/scene_timing.json

# 5. Assemble final video
python tools/assemble_video.py scripts/scene_timing.json exports/final_video.mp4
```

**Everything else is debug, test, or exception handling.**

---

## Complete Pipeline Execution (First Time)

```powershell
# 1. Parse script
python tools/parse_script.py scripts/raw_script.txt scripts/parsed_script.json

# 2. Generate voice + update timing
python tools/generate_voice.py scripts/parsed_script.json voice/tts_output/

# 3. Generate infographic specs
python tools/generate_infographic_specs.py scripts/parsed_script.json infographics/specs/

# 4. Render infographics
python tools/render_all_infographics.py infographics/specs/ video/scenes/infographic_scenes/

# 5. Render avatars
python tools/render_avatars.py scripts/scene_timing.json

# 6. Composite scenes
python tools/composite_scenes.py scripts/scene_timing.json

# 7. Assemble final video
python tools/assemble_video.py scripts/scene_timing.json exports/final_video.mp4

# 8. Add captions
whisper exports/final_video.mp4 --model base --output_format srt --output_dir exports/
```

### Quick Test Render

```powershell
# Test single scene end-to-end
echo "This is a test" | piper --model voice/voice_models/en_US-lessac-medium.onnx --output_file test_audio.wav

python models/avatar/SadTalker/inference.py \
  --driven_audio test_audio.wav \
  --source_image avatar/source_images/female_avatar_reference.png \
  --result_dir test_output/ \
  --still --size 512

# View result
test_output/result.mp4
```

---

## Performance Optimization

```powershell
# Use NVENC for faster encoding
-c:v h264_nvenc -preset fast

# Reduce quality for preview renders
-crf 28 -preset ultrafast

# Disable audio for test renders
-an

# Limit threads for CPU encoding
-threads 4
```
