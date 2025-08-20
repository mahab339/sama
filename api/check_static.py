import os
from pathlib import Path

# Ensure static directories exist
base_dir = Path(__file__).resolve().parent
static_dirs = [
    base_dir / 'static',
    base_dir / 'staticfiles',
]

for static_dir in static_dirs:
    os.makedirs(static_dir, exist_ok=True)
    print(f"Ensured directory exists: {static_dir}")

# List files in static directories
for static_dir in static_dirs:
    if static_dir.exists():
        print(f"\nContents of {static_dir}:")
        for f in static_dir.rglob('*'):
            print(f"- {f.relative_to(static_dir)}")
