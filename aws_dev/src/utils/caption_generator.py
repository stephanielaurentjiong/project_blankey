"""Utility functions for caption generation."""

import os
import base64
import mimetypes
from pathlib import Path
from typing import Optional

# def encode_image_to_base64(image_path: str) -> str:
#     """Encode image file to base64 string."""
#     with open(image_path, "rb") as f:
#         return base64.b64encode(f.read()).decode("utf-8") 


# def detect_mime_type(file_path: str) -> str:
#     """Detect MIME type of file."""
#     guessed, _ = mimetypes.guess_type(file_path)
#     return guessed or "application/octet-stream"

def load_prompt_template(prompt_file: str) -> str:
    """Load prompt template from file with robust path resolution."""
    resolved_path = "~/prompt.txt"
    with open(resolved_path, "r", encoding="utf-8") as f:
        return f.read().strip()


# def resolve_image_path(image_path: str) -> str:
#     """Resolve image path with common fallback locations."""
#     repo_root = get_repo_root()
#     candidates = [
#         image_path,
#         str(repo_root / "phase0" / "samples" / Path(image_path).name),
#         str(repo_root / "samples" / Path(image_path).name),
#     ]
#     return resolve_file_path(image_path, candidates)