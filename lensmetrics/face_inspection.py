"""Frontal-face inspection using a bundled cascade model."""

import os

import cv2

_BUNDLED = os.path.join(os.path.dirname(__file__), "models",
                        "haarcascade_frontalface_default.xml")


def _cascade_path() -> str:
    if os.path.isfile(_BUNDLED):
        return _BUNDLED
    return cv2.data.haarcascades + "haarcascade_frontalface_default.xml"


def inspect_faces(bgr, scale: float = 1.15, neighbours: int = 6, min_side: int = 30):
    """Return face bounding boxes as a list of (x, y, w, h) tuples."""
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    finder = cv2.CascadeClassifier(_cascade_path())
    if finder.empty():
        raise RuntimeError("Bundled face model failed to initialise.")
    hits = finder.detectMultiScale(
        grey,
        scaleFactor=scale,
        minNeighbors=neighbours,
        minSize=(min_side, min_side),
    )
    return [tuple(map(int, box)) for box in hits]
