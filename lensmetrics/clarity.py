"""Exposure and focus grading."""

from dataclasses import dataclass

import cv2


@dataclass
class ClarityReport:
    luma: float
    exposure_label: str
    blur_score: float
    focus_label: str


def grade_clarity(bgr, dark_cut: float = 55.0, bright_cut: float = 195.0,
                  blur_cut: float = 90.0) -> ClarityReport:
    """Grade exposure from mean luma and focus from Laplacian variance."""
    grey = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    luma = float(grey.mean())
    blur = float(cv2.Laplacian(grey, cv2.CV_64F).var())

    if luma < dark_cut:
        exposure = "Under-exposed"
    elif luma > bright_cut:
        exposure = "Over-exposed"
    else:
        exposure = "Well-exposed"

    focus = "In-focus" if blur >= blur_cut else "Soft-focus"

    return ClarityReport(
        luma=round(luma, 2),
        exposure_label=exposure,
        blur_score=round(blur, 2),
        focus_label=focus,
    )
