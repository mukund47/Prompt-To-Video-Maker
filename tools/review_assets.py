
import os
import shutil
import json
import sys
from pathlib import Path

def list_previews(staging_dir):
    return list(staging_dir.glob("*.[mM][pP]4")) + list(staging_dir.glob("*.[wW][aA][vV]"))

def main():
    base_dir = Path(__file__).parent.parent.resolve()
    staging_dir = base_dir / "staging" / "previews"
    approved_dir = base_dir / "staging" / "approved"
    
    os.makedirs(approved_dir, exist_ok=True)
    
    previews = list_previews(staging_dir)
    
    if not previews:
        print("No assets found in staging/previews.")
        return

    print(f"\nFound {len(previews)} assets pending review:\n")
    
    for i, p in enumerate(previews, 1):
        print(f"[{i}] {p.name}")
        
    print("\nOptions:")
    print("  [ID]   : Approve specific asset (moves to approved/)")
    print("  all    : Approve ALL assets")
    print("  q      : Quit")
    
    choice = input("\nEnter choice: ").strip().lower()
    
    if choice == 'q':
        sys.exit(0)
    
    to_approve = []
    
    if choice == 'all':
        to_approve = previews
    elif choice.isdigit():
        idx = int(choice) - 1
        if 0 <= idx < len(previews):
            to_approve = [previews[idx]]
        else:
            print("Invalid ID.")
            return
    else:
        print("Invalid input.")
        return
        
    for asset in to_approve:
        dest = approved_dir / asset.name
        print(f"Approving {asset.name}...")
        try:
            shutil.move(str(asset), str(dest))
            print(f"✓ Moved to {dest}")
        except Exception as e:
            print(f"❌ Failed to move: {e}")

    print("\nReview session complete.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        # Non-interactive mode for pipeline checks
        base_dir = Path(__file__).parent.parent.resolve()
        staging_dir = base_dir / "staging" / "previews"
        count = len(list_previews(staging_dir))
        print(f"{count} Pending")
        sys.exit(1 if count > 0 else 0)
    else:
        main()
