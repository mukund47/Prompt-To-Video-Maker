# First Test: Minimal Avatar Render

## Objective

Validate the core avatar pipeline with a 2-3 line script test.

**What this proves:**
- Script parsing works
- Piper TTS generates audio
- SadTalker renders talking head video @ 512x512
- VRAM management works on RTX 3050
- Output MP4 is playable

**Time:** ~5 minutes

---

## Prerequisites

✅ All Python packages installed  
✅ PyTorch with CUDA working  
✅ Piper TTS voice model downloaded  
✅ SadTalker checkpoints installed (see `sadtalker_models_guide.md`)  
✅ Avatar reference image ready

---

## Step 1: Create Test Script

**File:** `scripts/test_script.txt`

```
[AVATAR_ONLY]
Hello, this is a test of the AI avatar system.

[AVATAR_ONLY]
If you can see this video, the pipeline is working correctly.
```

**Save this file.**

---

## Step 2: Create Avatar Reference Image

You need a female avatar source image for SadTalker.

**Requirements:**
- Frontal face (0-5° rotation)
- Neutral expression
- Even lighting
- 1024x1024 or higher resolution
- Professional look

**Save to:** `avatar\source_images\female_avatar_reference.png`

**Options:**
1. Generate with Stable Diffusion: "professional female presenter, frontal portrait, neutral expression, studio lighting"
2. Use royalty-free stock photo (Unsplash, Pexels)
3. Use AI portrait generator

---

## Step 3: Parse Script

```powershell
cd "C:\Users\Mukun\Downloads\Antigravity Projects\3D Models\cybersec_ai_video_pipeline"

.\venv\Scripts\Activate.ps1

python tools\parse_script.py scripts\test_script.txt scripts\test_parsed.json
```

**Expected output:**
```
Parsing script: scripts\test_script.txt
Parsed 2 scenes
Saved to: scripts\test_parsed.json
```

**Verify:** Check `scripts\test_parsed.json` exists and has 2 scenes

---

## Step 4: Generate Voice

```powershell
python tools\generate_voice.py scripts\test_parsed.json voice\tts_output\
```

**Expected output:**
```
Generating TTS for 2 scenes...
Scene 1/2: Synthesizing... ✓ (2.35s)
Scene 2/2: Synthesizing... ✓ (3.12s)

✓ Generated 2 audio files
✓ Total duration: 5.47s (0.1 min)
✓ Updated timing: scripts\scene_timing.json
```

**Verify:** Check `voice\tts_output\` has `.wav` files

---

## Step 5: Render Avatar (First Real Test)

**Method 1: Using render_avatars.py (Batch)**
```powershell
python tools\render_avatars.py scripts\scene_timing.json avatar\source_images\female_avatar_reference.png
```

**Method 2: Manual SadTalker (Direct, Recommended for First Test)**
```powershell
cd models\avatar\SadTalker

# Render first scene
..\..\..\venv\Scripts\python.exe inference.py --driven_audio ..\..\..\..\voice\tts_output\scene_001.wav --source_image ..\..\..\..\avatar\source_images\female_avatar_reference.png --result_dir ..\..\..\..\avatar\renders\talking_head_segments\ --still --preprocess full --size 512 --enhancer gfpgan
```

**Recommended flags (from SadTalker best practices):**
- `--still` - Generates more natural full-body/image video
- `--preprocess full` - Better preprocessing for full image mode
- `--size 512` - Safe resolution for 4GB VRAM
- `--enhancer gfpgan` - Improves output quality

**What happens:**
1. SadTalker loads models (~10-15 seconds first time)
2. VRAM usage climbs to ~3.2 GB
3. Renders talking head video
4. GFPGAN enhancer improves quality
5. Output: MP4 in `avatar\renders\talking_head_segments\`

**Expected duration:** ~1-2 minutes for first scene

**Monitor VRAM (optional):**
```powershell
# In separate terminal
nvidia-smi -l 1
```

---

## Step 6: Verify Output

**Check files exist:**
```powershell
ls avatar\renders\talking_head_segments\
```

**Play the video:**
- Double-click `scene_001.mp4`
- Should show talking head synced to audio
- Resolution: 512x512
- Duration: matches audio (~2-3 seconds per scene)

---

## Success Criteria

✅ Script parsed to JSON  
✅ Audio files generated (clear female voice)  
✅ Avatar videos rendered without VRAM errors  
✅ Lip sync looks reasonable  
✅ Video playback works  

**If all pass:** The core pipeline is validated!

---

## Common Issues

### "SadTalker models not found"
- Check `models\avatar\SadTalker\checkpoints\` exists
- Verify all 4 folders present (auido2pose, face_recon, mapping, wav2lip)

### "CUDA out of memory"
- Close other GPU applications
- Verify using 512x512 (not higher)
- Check `nvidia-smi` shows available VRAM

### "Poor lip sync quality"
- Normal for 512x512 resolution
- Quality improves with better source image
- SadTalker is beta-quality, not production-perfect

---

## Next Steps After Success

Once this works:

1. **Test overlay modes:** Render avatar with transparent background
2. **Test scene composition:** Composite avatar over stock footage
3. **Build Remotion components:** Create first animated infographic
4. **Full pipeline test:** Run complete 5-scene video end-to-end

---

## Troubleshooting Log

If something fails, document:
- Exact error message
- Which step failed
- VRAM usage at failure (if CUDA related)
- File paths verified

This test is designed to be **minimal and fast**. If it works, everything else is incremental.
