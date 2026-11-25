#!/usr/bin/env python3
"""Deliver the finished front page for 25 November 2026.

The picture itself is drawn already and ships in this repository as
``entry.png`` — a broadsheet-style poster summing up the day in five
stories.  All this program has to do is hand that picture over to the
grader, byte for byte, at ``/output/entry.png``.

It reads the bundled picture into memory and writes it out again, so
the file the grader sees is exactly the file in the repository.  No
network is involved, no randomness, no clock: run it twice and the
two outputs are identical.  When I want to try it out on my own
machine instead of the grading sandbox, ``MAKEFUN_OUTPUT_DIR`` lets
me point the output somewhere harmless, e.g. ``MAKEFUN_OUTPUT_DIR=out``.
"""

import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
BUNDLED_PICTURE = HERE / "entry.png"
OUTPUT_NAME = "entry.png"
DEFAULT_OUTPUT_DIR = "/output"


def pick_output_dir() -> Path:
    """Where the graded picture goes: the sandbox's /output, or the
    override from the environment when I am testing locally."""
    return Path(os.environ.get("MAKEFUN_OUTPUT_DIR", DEFAULT_OUTPUT_DIR))


def main() -> int:
    if not BUNDLED_PICTURE.is_file():
        print(f"bundled picture not found: {BUNDLED_PICTURE}",
              file=sys.stderr)
        return 1

    picture_bytes = BUNDLED_PICTURE.read_bytes()

    out_dir = pick_output_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / OUTPUT_NAME
    destination.write_bytes(picture_bytes)

    # Read it back and make sure what landed on disk is exactly what
    # the repository holds; a short or altered file is worse than none.
    if destination.read_bytes() != picture_bytes:
        print(f"written picture differs from bundled one: {destination}",
              file=sys.stderr)
        return 1

    print(f"delivered {destination} "
          f"({destination.stat().st_size} bytes, verified)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
