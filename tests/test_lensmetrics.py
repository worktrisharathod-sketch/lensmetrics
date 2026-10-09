import json

import cv2
import numpy as np
import pytest

from lensmetrics.photo_stats import describe_photo
from lensmetrics.clarity import grade_clarity
from lensmetrics.structure import trace_structure
from lensmetrics.palette import channel_balance
from lensmetrics.visualizer import tag_faces
from lensmetrics.io_handler import resolve_source
from lensmetrics.reporter import save_reports


def _mid_grey():
    return np.full((80, 120, 3), 128, dtype=np.uint8)


def test_geometry_and_orientation():
    stats = describe_photo(_mid_grey())
    assert (stats.width, stats.height) == (120, 80)
    assert stats.aspect == "landscape"
    assert stats.megapixels == pytest.approx(0.01, abs=0.001)
    assert stats.mean_luma == pytest.approx(128, abs=1.0)


def test_clarity_mid_grey_is_well_exposed():
    report = grade_clarity(_mid_grey())
    assert report.exposure_label == "Well-exposed"
    assert report.focus_label in {"In-focus", "Soft-focus"}
    assert report.luma == pytest.approx(128, abs=1.0)


def test_dark_frame_flags_under_exposed():
    black = np.zeros((40, 40, 3), dtype=np.uint8)
    report = grade_clarity(black)
    assert report.exposure_label == "Under-exposed"
    assert report.focus_label == "Soft-focus"


def test_structure_map_shape_and_census():
    edges, info = trace_structure(_mid_grey())
    assert edges.shape == (80, 120)
    assert info.contour_count >= 0
    assert 0.0 <= info.edge_ratio <= 1.0


def test_palette_reports_dominant_channel():
    img = np.zeros((10, 10, 3), dtype=np.uint8)
    img[:, :, 2] = 200  # strong red
    mix = channel_balance(img)
    assert mix["dominant"] == "red"
    assert mix["red"] > mix["blue"]


def test_face_tagging_keeps_dimensions():
    img = _mid_grey()
    marked = tag_faces(img, [(5, 5, 20, 20)])
    assert marked.shape == img.shape
    assert not np.array_equal(marked, img)


def test_reports_write_txt_and_json(tmp_path):
    stats = describe_photo(_mid_grey())
    clarity = grade_clarity(_mid_grey())
    _, structure = trace_structure(_mid_grey())
    palette = channel_balance(_mid_grey())
    txt = tmp_path / "summary.txt"
    js = tmp_path / "summary.json"
    save_reports("input/image.jpeg", [], stats, clarity, structure,
                 palette, str(txt), str(js))
    assert txt.exists() and js.exists()
    payload = json.loads(js.read_text())
    assert payload["tool"] == "LensMetrics"
    assert payload["face_count"] == 0


def test_bad_paths_raise_helpful_errors(tmp_path):
    with pytest.raises(FileNotFoundError):
        resolve_source(str(tmp_path / "missing.jpg"))
    bad = tmp_path / "notes.txt"
    bad.write_text("hello")
    with pytest.raises(ValueError):
        resolve_source(str(bad))
