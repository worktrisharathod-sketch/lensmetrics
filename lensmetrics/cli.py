"""Command-line entry point for LensMetrics."""

import argparse
import os

from .io_handler import read_photo
from .face_inspection import inspect_faces
from .photo_stats import describe_photo
from .clarity import grade_clarity
from .structure import trace_structure
from .palette import channel_balance
from .visualizer import tag_faces, store_photo
from .reporter import save_reports


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lensmetrics",
        description="LensMetrics — inspect faces, quality and structure in a photo.",
    )
    parser.add_argument("--input", "-i", default="input/image.jpeg",
                        help="Path to the source photo.")
    parser.add_argument("--outdir", "-o", default="output",
                        help="Directory for annotated.jpg, edgemap.jpg, reports.")
    parser.add_argument("--canny-low", type=int, default=60)
    parser.add_argument("--canny-high", type=int, default=140)
    parser.add_argument("--blur-cut", type=float, default=90.0,
                        help="Laplacian-variance cutoff for in-focus label.")
    return parser


def run(args) -> dict:
    photo = read_photo(args.input)
    faces = inspect_faces(photo)
    stats = describe_photo(photo)
    clarity = grade_clarity(photo, blur_cut=args.blur_cut)
    edge_map, structure = trace_structure(
        photo, low=args.canny_low, high=args.canny_high)
    palette = channel_balance(photo)

    marked = tag_faces(photo, faces)
    annotated = os.path.join(args.outdir, "annotated.jpg")
    edgemap = os.path.join(args.outdir, "edgemap.jpg")
    store_photo(marked, annotated)
    store_photo(edge_map, edgemap)
    save_reports(
        args.input, faces, stats, clarity, structure, palette,
        os.path.join(args.outdir, "summary.txt"),
        os.path.join(args.outdir, "summary.json"),
    )
    return {
        "faces": len(faces),
        "stats": stats,
        "clarity": clarity,
        "structure": structure,
        "annotated": annotated,
        "edgemap": edgemap,
    }


def main(argv=None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        outcome = run(args)
    except (FileNotFoundError, ValueError, IOError, RuntimeError) as err:
        parser.exit(2, f"lensmetrics: error: {err}\n")
    print("\n===== LensMetrics =====")
    print(f"Photo      : {args.input}")
    print(f"Faces      : {outcome['faces']}")
    print(f"Size       : {outcome['stats'].width} x {outcome['stats'].height}"
          f" ({outcome['stats'].aspect})")
    print(f"Exposure   : {outcome['clarity'].exposure_label}")
    print(f"Focus      : {outcome['clarity'].focus_label}")
    print(f"Contours   : {outcome['structure'].contour_count}")
    print(f"Saved to   : {args.outdir}/ (annotated.jpg, edgemap.jpg,"
          " summary.txt, summary.json)\n")


if __name__ == "__main__":
    main()
