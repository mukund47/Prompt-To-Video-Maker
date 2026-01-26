# SadTalker Model Installation Guide

## Official Sources

**Repository:** https://github.com/OpenTalker/SadTalker (Source of truth)

---

## Required Downloads

### 1. SadTalker Checkpoints (~1.5 GB)

**Official Google Drive:**  
https://drive.google.com/drive/folders/1gwvP6zv1E1Z5v0kQyK1VwF3p9x0z4X7E

**What you'll get:**
- `auido2pose/` folder
- `face_recon/` folder
- `mapping/` folder
- `wav2lip/` folder

**Installation:**
1. Download all checkpoint folders
2. Extract to: `models\avatar\SadTalker\checkpoints\`

**Final structure:**
```
models\avatar\SadTalker\checkpoints\
├── auido2pose\
├── face_recon\
├── mapping\
└── wav2lip\
```

---

### 2. GFPGAN Models (Required)

**Official Repository:** https://github.com/TencentARC/GFPGAN

**Direct Model Link:**  
https://drive.google.com/drive/folders/1sK1p8uH0bZ0H3n3Q8Zz5Y2Z2ZJZb9V3E

**Installation:**
1. Download the GFPGAN weights
2. Extract to: `models\avatar\SadTalker\gfpgan\`

**Final structure:**
```
models\avatar\SadTalker\gfpgan\
└── weights\
    └── (model files)
```

**Note:** SadTalker expects GFPGAN. This is non-optional.

---

## Verification

After installation, your directory should look like:

```
models\avatar\SadTalker\
├── checkpoints\
│   ├── auido2pose\
│   ├── face_recon\
│   ├── mapping\
│   └── wav2lip\
├── gfpgan\
│   └── weights\
├── src\
├── inference.py
└── (other files)
```

---

## What This Unlocks

Once these models are in place:
- ✅ The avatar pipeline becomes **runnable**, not theoretical
- ✅ You can render your first talking head video
- ✅ All remaining work is incremental (overlays, infographics, assembly)

---

## Next Step

See `first_test.md` for your first minimal test render.
