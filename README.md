# LensMetrics

## Overview

LensMetrics is a command-line photo inspector built with Python and OpenCV.
Point it at a photograph and it reports faces, geometry, exposure/focus
grades, edge structure, and colour balance — saving annotated visuals plus
text and JSON summaries.

## Capabilities

- Photo loading with type checking (`jpg/jpeg/png/bmp/webp`)
- Frontal-face inspection with labelled boxes
- Geometry readout: resolution, megapixels, orientation, contrast
- Exposure grading (Under/Well/Over-exposed) and focus grading
- Canny structure tracing with contour census and edge density
- Per-channel colour balance with dominant-channel pick
- Dual summaries: `summary.txt` and `summary.json`
- Configurable CLI (`--canny-low/high`, `--blur-cut`, `--outdir`)

## Stack

- Python 3, OpenCV, NumPy, Pytest, argparse

## Layout

```text
LensMetrics/
├── input/
├── output/
├── lensmetrics/
│   ├── cli.py
│   ├── io_handler.py
│   ├── face_inspection.py
│   ├── photo_stats.py
│   ├── clarity.py
│   ├── structure.py
│   ├── palette.py
│   ├── visualizer.py
│   └── reporter.py
├── tests/
├── main.py
└── README.md
```

## Run

```bash
pip install -r requirements.txt
python main.py --input input/image.jpeg --outdir output
python main.py --input input/image.jpeg --outdir output --canny-low 60 --canny-high 140
pytest -q
```
