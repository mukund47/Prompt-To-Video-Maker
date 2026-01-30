"""
Script Parsing Tool
Parses raw script into structured JSON with scene types and metadata
"""

import json
import sys
import re
from pathlib import Path

def estimate_duration(text, wpm=150):
    """Estimate narration duration based on word count"""
    words = len(text.split())
    return (words / wpm) * 60  # Convert to seconds

def parse_scene_marker(line):
    """Parse scene type markers like [STOCK_ONLY], [INFOGRAPHIC_ONLY], or [FULL_COMPOSITE | stock:file.mp4 | infographic:id]"""
    match = re.match(r'\[([A-Z_]+)(?:\s*\|\s*(.+))?\]', line.strip())
    if not match:
        return None
    
    scene_type = match.group(1)
    params_str = match.group(2) or ""
    
    # Map legacy avatar types to STOCK_ONLY
    if scene_type in ["AVATAR_ONLY", "AVATAR_OVER_STOCK"]:
        scene_type = "STOCK_ONLY"
    
    params = {}
    if params_str:
        for param in params_str.split('|'):
            param = param.strip()
            if ':' in param:
                key, value = param.split(':', 1)
                params[key.strip()] = value.strip()
            else:
                params[param] = True
    
    return {"type": scene_type, "params": params}

def parse_script(script_path):
    """Parse raw script into structured scenes"""
    with open(script_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    scenes = []
    current_scene = None
    scene_id = 1
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check for scene marker
        scene_marker = parse_scene_marker(line)
        if scene_marker:
            # Save previous scene if exists
            if current_scene and current_scene.get('narration_text'):
                current_scene['duration_estimate'] = estimate_duration(current_scene['narration_text'])
                scenes.append(current_scene)
                scene_id += 1
            
            # Start new scene
            current_scene = {
                "scene_id": scene_id,
                "type": scene_marker['type'],
                "narration_text": "",
                "visual_requirements": {}
            }
            
            # Parse visual requirements from params
            params = scene_marker['params']
            if 'stock' in params:
                current_scene['visual_requirements']['stock_file'] = params['stock']
            if 'infographic' in params:
                current_scene['visual_requirements']['infographic_id'] = params['infographic']
            if 'layout' in params:
                current_scene['visual_requirements']['layout'] = params['layout']
        else:
            # Add to current scene narration
            if current_scene:
                if current_scene['narration_text']:
                    current_scene['narration_text'] += ' '
                current_scene['narration_text'] += line
    
    # Add final scene
    if current_scene and current_scene.get('narration_text'):
        current_scene['duration_estimate'] = estimate_duration(current_scene['narration_text'])
        scenes.append(current_scene)
    
    return scenes

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_script.py <input_script.txt> <output_json>")
        sys.exit(1)
    
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    
    if not Path(input_path).exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    print(f"Parsing script: {input_path}")
    scenes = parse_script(input_path)
    
    print(f"Parsed {len(scenes)} scenes")
    
    # Save to JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(scenes, f, indent=2, ensure_ascii=False)
    
    print(f"Saved to: {output_path}")
    
    # Print summary
    print("\nScene Summary:")
    print(f"{'ID':<4} {'Type':<25} {'Duration':<8} {'Narration Preview'}")
    print("-" * 80)
    for scene in scenes:
        preview = scene['narration_text'][:50] + "..." if len(scene['narration_text']) > 50 else scene['narration_text']
        print(f"{scene['scene_id']:<4} {scene['type']:<25} {scene['duration_estimate']:<8.1f} {preview}")

if __name__ == "__main__":
    main()
