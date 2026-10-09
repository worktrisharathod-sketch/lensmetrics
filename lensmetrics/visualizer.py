"""Annotation and persistence helpers."""

import os

import cv2


def tag_faces(bgr, boxes):
    """Draw labelled boxes around each face on a copy of *bgr*."""
    marked = bgr.copy()
    for i, (x, y, w, h) in enumerate(boxes, start=1):
        cv2.rectangle(marked, (x, y), (x + w, y + h), (255, 120, 0), 3)
        cv2.putText(
            marked, f"Face #{i}", (x, max(0, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 120, 0), 2,
        )
    return marked


def store_photo(img, path: str) -> str:
    """Write *img* to *path*, creating parent folders as needed."""
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    if not cv2.imwrite(path, img):
        raise IOError(f"Could not write image to: {path}")
    return path
