"""Per-channel colour balance."""

import cv2


def channel_balance(bgr) -> dict:
    """Return mean intensity per B/G/R channel plus dominant channel."""
    means = {}
    for idx, name in enumerate(("blue", "green", "red")):
        means[name] = round(float(bgr[:, :, idx].mean()), 2)
    dominant = max(means, key=means.get)
    means["dominant"] = dominant
    return means
