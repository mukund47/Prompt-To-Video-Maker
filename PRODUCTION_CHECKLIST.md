# Production Checklist: Cybersecurity Explainer Video

## Prerequisites (MUST complete before production)

### 1. Stock Video
- [ ] Download relevant B-roll clips
- [ ] Save to: `stock_video/raw/`
- [ ] Process using FFmpeg (resize to 1080p)
- [ ] Move to: `stock_video/processed/`

### 2. Remotion/Manim Infographics
- [ ] Build concepts in Remotion or Manim
- [ ] Export as MP4
- [ ] Save to: `video/scenes/infographic_scenes/`

---

## Production Workflow

### Phase 1: Script to Audio (Ready Now ✓)

```powershell
# 1. Parse script
python tools\parse_script.py scripts\raw_script.txt scripts\parsed_script.json

# 2. Generate TTS narration
python tools\generate_voice.py scripts\parsed_script.json voice\tts_output\
```

**Output:** WAV files for each scene + `scene_timing.json`

---

### Phase 2: Render Infographic Scenes

```powershell
# Render all infographics defined in the script
python tools\render_all_infographics.py
```

**Output:** `video/scenes/infographic_scenes/*.mp4`

---

### Phase 3: Composite Overlays (Optional)

```powershell
# If script uses FULL_COMPOSITE (Stock + Infographic)
python tools\composite_scenes.py scripts\scene_timing.json
```

**Output:** `video/scenes/composited_scenes/*.mp4`

---

### Phase 4: Assemble Final Video

```powershell
python tools\assemble_video.py scripts\scene_timing.json exports\final_video.mp4
```

**Output:** `exports\final_video.mp4`

---

## Verification Steps

### After Each Phase:
- [ ] Verify files exist in expected locations
- [ ] Check audio quality and narration flow
- [ ] Preview assembled video before final render

### Final Quality Check:
- [ ] Audio levels consistent across scenes
- [ ] No visual glitches at scene transitions
- [ ] Total duration matches expectation

---

## Current Status

### Ready to Use Now:
- ✅ Piper TTS (narration)
- ✅ FFmpeg (composition & assembly)
- ✅ Manim/Remotion (infographics)
- ✅ Script parsing logic

---

## Next Immediate Action

**Priority 1:** Prepare `raw_script.txt` with `STOCK_ONLY`, `INFOGRAPHIC_ONLY`, or `FULL_COMPOSITE` markers.
**Priority 2:** Ensure stock footage is processed in `stock_video/processed/`.
**Priority 3:** Run the full pipeline.
