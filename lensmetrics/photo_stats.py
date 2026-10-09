"""Basic geometry and luminance statistics."""

from dataclasses import dataclass

import cv2


@dataclass
class PhotoStats:
    width: int
    height: int
    channels: int
    megapixels: float
    mean_luma: float
    contrast: float
    aspect: str


def describe_photo(bgr) -> PhotoStats:
    """Summarise dimensions, luminance mean/std-dev and orientation."""
    h, w, ch = bgr.shape
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    mean_val, std_val = cv2.meanStdDev(grey)
    orientation = (
        "landscape" if w > h else ("portrait" if h > w else "square")
    )
    return PhotoStats(
        width=int(w),
        height=int(h),
        channels=int(ch),
        megapixels=round(w * h / 1e6, 3),
        mean_luma=round(float(mean_val[0][0]), 2),
        contrast=round(float(std_val[0][0]), 2),
        aspect=orientation,
    )
