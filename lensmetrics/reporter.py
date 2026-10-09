"""Text + JSON summary writer."""

import json
import os


def save_reports(source: str, faces, stats, clarity, structure, palette,
                 txt_path: str, json_path: str) -> None:
    """Persist human-readable and machine-readable summaries."""
    lines = [
        "LensMetrics Inspection Summary",
        "==============================",
        "",
        f"Source photo : {source}",
        f"Faces marked : {len(faces)}",
        "",
        "[ Geometry ]",
        f"Resolution   : {stats.width} x {stats.height} ({stats.aspect})",
        f"Channels     : {stats.channels}",
        f"Megapixels   : {stats.megapixels}",
        f"Mean luma    : {stats.mean_luma}",
        f"Contrast     : {stats.contrast}",
        "",
        "[ Clarity ]",
        f"Exposure     : {clarity.exposure_label} ({clarity.luma})",
        f"Focus        : {clarity.focus_label} (score {clarity.blur_score})",
        "",
        "[ Structure ]",
        f"Edge pixels  : {structure.edge_pixels} ({structure.edge_ratio * 100:.2f}%)",
        f"Contours     : {structure.contour_count}",
        "",
        "[ Colour ]",
        f"B/G/R means  : {palette['blue']} / {palette['green']} / {palette['red']}",
        f"Dominant     : {palette['dominant']}",
        "",
        "Artefacts    : annotated.jpg + edgemap.jpg alongside this file.",
    ]
    folder = os.path.dirname(txt_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(txt_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    payload = {
        "tool": "LensMetrics",
        "source": source,
        "face_count": len(faces),
        "faces": [list(b) for b in faces],
        "geometry": vars(stats),
        "clarity": vars(clarity),
        "structure": vars(structure),
        "palette": palette,
    }
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2)
