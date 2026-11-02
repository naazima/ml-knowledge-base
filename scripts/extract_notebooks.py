#!/usr/bin/env python3
"""Extract readable text from course notebooks.

Reads every .ipynb in materials/<course>/ and writes one .txt per notebook to
materials/_extracted/<course>/ (private, gitignored). Source files are never modified.

Usage:
    python scripts/extract_notebooks.py foundations-python-stats
    python scripts/extract_notebooks.py --all
    python scripts/extract_notebooks.py <course> --with-outputs
"""
import argparse
import json
import sys
from pathlib import Path

COURSES = [
    "foundations-python-stats", "data-analysis-visualization", "machine-learning",
    "practical-data-science", "deep-learning", "recommendation-systems", "genai",
    "elective-project", "capstone-project",
]
ROOT = Path(__file__).resolve().parent.parent
MATERIALS = ROOT / "materials"
OUT_ROOT = MATERIALS / "_extracted"


def text_outputs(cell):
    """Return plain-text outputs of a code cell (images and rich output skipped)."""
    chunks = []
    for out in cell.get("outputs", []):
        if out.get("output_type") == "stream":
            chunks.append("".join(out.get("text", [])))
        elif out.get("output_type") in ("execute_result", "display_data"):
            plain = out.get("data", {}).get("text/plain")
            if plain:
                chunks.append("".join(plain))
        elif out.get("output_type") == "error":
            chunks.append(f"{out.get('ename')}: {out.get('evalue')}")
    return "\n".join(chunks).rstrip()


def convert(nb_path, with_outputs):
    nb = json.loads(nb_path.read_text(encoding="utf-8"))
    parts = [f"# NOTEBOOK: {nb_path.name}\n"]
    for i, cell in enumerate(nb.get("cells", []), 1):
        src = "".join(cell.get("source", [])).rstrip()
        kind = cell.get("cell_type")
        if kind == "markdown":
            parts.append(f"[{i}] MARKDOWN\n{src}\n")
        elif kind == "code":
            block = f"[{i}] CODE\n```python\n{src}\n```\n"
            if with_outputs:
                out = text_outputs(cell)
                if out:
                    block += f"OUTPUT:\n{out}\n"
            parts.append(block)
    return "\n".join(parts)


def extract_course(course, with_outputs):
    src_dir = MATERIALS / course
    if not src_dir.is_dir():
        print(f"skip {course}: no folder at {src_dir}")
        return 0
    notebooks = sorted(src_dir.glob("*.ipynb"))
    out_dir = OUT_ROOT / course
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"{course}: {len(notebooks)} notebook(s)")
    for nb_path in notebooks:
        out = out_dir / (nb_path.stem + ".txt")
        out.write_text(convert(nb_path, with_outputs), encoding="utf-8")
        print(f"  {out.name:55s} {out.stat().st_size:>9,} bytes")
    return len(notebooks)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("course", nargs="?", choices=COURSES, help="course slug")
    ap.add_argument("--all", action="store_true", help="process every course folder that exists")
    ap.add_argument("--with-outputs", action="store_true", help="keep text outputs of code cells")
    args = ap.parse_args()
    if not args.course and not args.all:
        ap.error("give a course slug or --all")
    for course in (COURSES if args.all else [args.course]):
        extract_course(course, args.with_outputs)


if __name__ == "__main__":
    sys.exit(main())
