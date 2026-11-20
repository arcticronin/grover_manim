"""Manim entry point: uv run python -m manim -qm grover.py GroverSlides."""

from grover_slides.deck import GroverPresentation
from manim import ManimColor
from grover_slides.deck import BG


class GroverSlides(GroverPresentation):
    """Five chapters and a geometry appendix, with click-controlled builds."""


class QubitIntro(GroverPresentation):
    """Render the qubit introduction independently for fast iteration."""

    def construct(self):
        self.camera.background_color = ManimColor(BG)
        self.qubit_intro()
