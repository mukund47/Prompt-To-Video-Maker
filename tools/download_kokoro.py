
import os
import requests
import sys

def download_file(url, dest):
    print(f"Downloading {url} to {dest}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(dest, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print("✓ Done")
    except Exception as e:
        print(f"❌ Failed: {e}")
        sys.exit(1)

def main():
    os.makedirs("models/kokoro", exist_ok=True)
    
    files = {
        "models/kokoro/kokoro-v0_19.onnx": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files/kokoro-v0_19.onnx",
        "models/kokoro/voices-v1.0.bin": "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin"
    }
    
    for path, url in files.items():
        if os.path.exists(path) and os.path.getsize(path) > 1000:
            print(f"✓ {path} already exists")
            continue
        download_file(url, path)

if __name__ == "__main__":
    main()
