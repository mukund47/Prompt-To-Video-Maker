# Production Checklist: Phishing Awareness Video

## Prerequisites (MUST complete before production)

### 1. Avatar Reference Image ⚠️ BLOCKING
- [ ] Create or source female avatar reference image
- [ ] Requirements: 1024x1024+, frontal face, neutral expression
- [ ] Save to: `avatar\source_images\female_avatar_reference.png`
- [ ] **Cannot render avatar scenes without this**

### 2. Test Sad Talker First ⚠️ CRITICAL
- [ ] Run first SadTalker smoke test (see `tools/first_test.md`)
- [ ] Verify: MP4 generated, lips sync, no CUDA errors
- [ ] **Must pass before full production**

### 3. Stock Video
- [ ] Download: Person checking email on laptop
- [ ] Save to: `stock_video\raw\email_checking.mp4`
- [ ] Trim to ~5 seconds
- [ ] Or use placeholder initially

### 4. Remotion Infographic Component
- [ ] Build phishing flow animation in Remotion
- [ ] Components: Email → User → Click → Theft
- [ ] Export spec to: `infographics\specs\phishing_flow.json`

---

## Production Workflow

### Phase 1: Script to Audio (Ready Now ✓)

```powershell
# 1. Parse script
python tools\parse_script.py scripts\phishing_awareness.txt scripts\phishing_parsed.json

# 2. Generate TTS narration
python tools\generate_voice.py scripts\phishing_parsed.json voice\tts_output\
```

**Output:** WAV files for each avatar scene + `scene_timing.json`

---

### Phase 2: Generate Captions with Whisper

```powershell
# For each narration file, generate captions
.\venv\Scripts\python.exe -c "
import whisper
model = whisper.load_model('base')

# Process each scene
for scene in ['scene_001', 'scene_004', 'scene_005']:
    audio_path = f'voice/tts_output/{scene}.wav'
    result = model.transcribe(audio_path)
    
    # Save captions with timestamps
    with open(f'video/captions/{scene}.srt', 'w') as f:
        for segment in result['segments']:
            f.write(f\"{segment['id'] + 1}\n\")
            f.write(f\"{format_time(segment['start'])} --> {format_time(segment['end'])}\n\")
            f.write(f\"{segment['text'].strip()}\n\n\")
"
```

**Output:** SRT caption files for each avatar scene

---

### Phase 3: Render Avatar Scenes

⚠️ **Requires: Avatar reference image + SadTalker test passed**

```powershell
cd models\avatar\SadTalker

# Scene 1: Intro
..\..\..\venv\Scripts\python.exe inference.py ^
  --driven_audio ..\..\..\voice\tts_output\scene_001.wav ^
  --source_image ..\..\..\avatar\source_images\female_avatar_reference.png ^
  --result_dir ..\..\..\avatar\renders\talking_head_segments ^
  --still --preprocess full --size 512 ^
  --enhance gfpgan

# Repeat for scenes 4 and 5
```

**Output:** 3 avatar MP4 files with talking head

---

### Phase 4: Create Infographic Animation

```powershell
cd infographics\animations

# Create phishing flow component (Remotion)
npx remotion render PhishingFlow phishing_flow.mp4

# Or export from spec
python ..\..\tools\render_all_infographics.py
```

**Output:** `infographics/renders/phishing_flow.mp4`

---

### Phase 5: Process Stock Video

```powershell
# Trim and resize stock footage
ffmpeg -i stock_video\raw\email_checking.mp4 ^
       -t 5 ^
       -vf scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2 ^
       -c:v h264_nvenc -preset fast ^
       stock_video\processed\email_checking.mp4
```

**Output:** Processed 5-second stock clip

---

### Phase 6: Add Captions to Avatar Scenes

```powershell
# Burn captions into avatar videos
ffmpeg -i avatar\renders\talking_head_segments\scene_001.mp4 ^
       -vf "subtitles=video/captions/scene_001.srt:force_style='FontSize=24,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2'" ^
       -c:v h264_nvenc -preset fast ^
       video\scenes_with_captions\scene_001.mp4
```

**Output:** Avatar videos with burned-in captions

---

### Phase 7: Assemble Final Video

```powershell
python tools\assemble_video.py scripts\scene_timing.json exports\phishing_awareness_final.mp4
```

**FFmpeg concat under the hood:**
```
file 'video/scenes_with_captions/scene_001.mp4'
file 'infographics/renders/phishing_flow.mp4'
file 'stock_video/processed/email_checking.mp4'
file 'video/scenes_with_captions/scene_004.mp4'
file 'video/scenes_with_captions/scene_005.mp4'
```

**Output:** `exports\phishing_awareness_final.mp4` (~30-35 seconds)

---

## Verification Steps

### After Each Phase:
- [ ] Verify files exist in expected locations
- [ ] Check audio sync in avatar scenes
- [ ] Verify caption accuracy and timing
- [ ] Preview assembled video before final render

### Final Quality Check:
- [ ] Audio levels consistent across scenes
- [ ] Captions visible and accurate
- [ ] No visual glitches at scene transitions
- [ ] Avatar lip sync looks natural
- [ ] Total duration: 30-35 seconds

---

## Current Blockers

### Cannot Start Without:
1. **Avatar reference image** - Create/source this first
2. **SadTalker test passed** - Must validate before production
3. **Stock video** - Download or use placeholder
4. **Remotion component** - Build phishing flow animation

### Ready to Use Now:
- ✅ Whisper (caption generation)
- ✅ Piper TTS (narration)
- ✅ FFmpeg (assembly)
- ✅ Script written

---

## Estimated Timeline

| Phase | Time | Dependency |
|-------|------|------------|
| Get avatar image | 5-10 min | Manual |
| SadTalker test | 2 min | Avatar image |
| Parse + TTS | 1 min | None |
| Generate captions | 2 min | TTS done |
| Render avatars | 5-8 min | Test passed |
| Build infographic | 15-30 min | Remotion coding |
| Process stock | 2 min | Video sourced |
| Add captions | 3 min | Avatars done |
| Final assembly | 2 min | All scenes ready |
| **Total** | **40-65 min** | Linear dependencies |

---

## Next Immediate Action

**Priority 1:** Get avatar reference image  
**Priority 2:** Run SadTalker smoke test  
**Priority 3:** Generate TTS narration (can do now)

Once avatar test passes, full production becomes viable.
