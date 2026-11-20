"""Convenience commands for rendering and presenting the Grover deck."""

import argparse
from pathlib import Path
import subprocess
import sys


def main() -> None:
    parser = argparse.ArgumentParser(description="Render or present a Grover deck with a geometry appendix.")
    parser.add_argument("action", choices=["render", "present", "export"], nargs="?", default="render")
    parser.add_argument("-q", "--quality", choices=["l", "m", "h"], default="h",
                        help="render quality: l=480p, m=720p, h=1080p (default)")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[2]
    if not (root / "grover.py").exists():
        parser.error("Run this from an editable checkout (uv sync), with grover.py present.")
    if args.action == "render":
        command = [sys.executable, "-m", "manim", f"-q{args.quality}", "grover.py", "GroverSlides"]
    else:
        if not (root / "slides/GroverSlides.json").exists():
            parser.error("Render first: uv run grover-slides render")
        command = [sys.executable, "-m", "manim_slides", "--silent"]
        if args.action == "present":
            command += ["present", "GroverSlides", "--show-info-window"]
        else:
            (root / "exports").mkdir(exist_ok=True)
            command += ["convert", "GroverSlides", "exports/grover.html", "--offline", "--one-file",
                        "-ctitle=Grover's algorithm — search and geometry", "-cbackground_color=#0B1120"]
    subprocess.run(command, cwd=root, check=True)
