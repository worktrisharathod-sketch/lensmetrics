# Project Statement — LensMetrics

## Problem Statement

Casual photo collections pile up with no quick way to tell which shots are
sharp, well-exposed, structurally rich, or contain people. Opening each file
in an editor to judge brightness, focus, and content is slow and subjective.
A single terminal command that grades a photo and keeps visual proof would
save that effort.

## Project Scope

LensMetrics inspects one photograph per run. It checks the file type, loads
the pixels, marks faces, measures geometry and contrast, grades exposure and
focus, traces edges and counts contours, profiles colour balance, and writes
annotated images plus text/JSON summaries. It is a study project, not a
production photo manager.

## Target Users

- Photography beginners auditing their own shots
- Students practising OpenCV beyond toy blur/edge demos
- Developers needing a tiny pre-check before heavier vision models

## High-Level Features

1. Guarded photo intake with clear errors
2. Face marking with numbered labels
3. Geometry and contrast readout
4. Exposure and focus grading with tunable cutoffs
5. Edge tracing with contour census
6. Colour-balance profile
7. Annotated + edge-map images and dual reports

## Expected Output

Each run drops four files in the output folder:

- `annotated.jpg` — faces boxed and numbered
- `edgemap.jpg` — Canny structure map
- `summary.txt` — readable inspection sheet
- `summary.json` — machine-readable record
