"""Edge tracing plus contour census."""

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class StructureReport:
    edge_pixels: int
    edge_ratio: float
    contour_count: int


def trace_structure(bgr, low: int = 60, high: int = 140, blur: int = 7):
    """Blur, run Canny, and count external contours.

    Returns (edge_map, StructureReport).
    """
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    if blur % 2 == 0:
        blur += 1
    soft = cv2.GaussianBlur(grey, (blur, blur), 0)
    edge_map = cv2.Canny(soft, low, high)
    contours, _ = cv2.findContours(
        edge_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    total = int(edge_map.size)
    active = int(np.count_nonzero(edge_map))
    return edge_map, StructureReport(
        edge_pixels=active,
        edge_ratio=round(active / total, 4) if total else 0.0,
        contour_count=len(contours),
    )
