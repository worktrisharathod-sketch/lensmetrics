"""Input resolution and image loading for LensMetrics."""

import os

import cv2

ALLOWED_TYPES = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def resolve_source(path: str) -> str:
    """Check that *path* exists and has a supported suffix."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"No photo found at: {path}")
    suffix = os.path.splitext(path)[1].lower()
    if suffix not in ALLOWED_TYPES:
        raise ValueError(
            f"File type '{suffix}' is not supported. "
            f"Allowed types: {sorted(ALLOWED_TYPES)}"
        )
    return path


def read_photo(path: str):
    """Load *path* with OpenCV, raising a clear error when undecodable."""
    resolve_source(path)
    photo = cv2.imread(path, cv2.IMREAD_COLOR)
    if photo is None:
        raise ValueError(f"OpenCV could not decode the file: {path}")
    return photo
