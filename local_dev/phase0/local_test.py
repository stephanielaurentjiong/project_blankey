#!/usr/bin/env python3
"""Local test script for caption generation."""

import json
import sys
from pathlib import Path
# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
from caption_generator import generate_caption

def load_and_test_samples():
    """Load and test all samples from JSON file."""
    # Base directory of this script
    script_dir = Path(__file__).parent
    samples_dir = script_dir / "samples"
    samples_file = samples_dir / "sample_descriptions.json"

    if not samples_file.is_file():
        print(f"Sample file not found: {samples_file}")
        return

    with open(samples_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print("\n" + "=" * 50)
    print("Testing all samples from JSON:")

    for sample in data.get("samples", []):
        print(f"\n--- Testing {sample.get('id', 'unknown')} ---")
        print(f"Description: {sample.get('description', '')}")

        # Resolve image path using same utils as generator
        image_path = samples_dir / sample.get("image", "")
        if not image_path.is_file():
            print(f"⚠️  Image not found: {image_path}")
            continue

        result = generate_caption(
            image_path=str(image_path),
            video_description=sample.get("description", ""),
            temperature=1.0,
            max_tokens=512,
            show_log=True
        )

        if result.get("success"):
            print(f"✅ Output Text: {result.get('output_text')}")
        else:
            print(f"❌ Error: {result.get('error')}")

if __name__ == "__main__":
    print("Caption Generator - Local Test")
    print("=" * 50)

    load_and_test_samples()

    print("\n" + "=" * 50)
    print("Testing complete!")
