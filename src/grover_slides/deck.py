"""Five animated chapters and a technical appendix, with speaker notes."""

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arc,
    Arrow,
    Axes,
    Circle,
    Create,
    DashedLine,
    Dot,
    DecimalNumber,
    FadeIn,
    FadeOut,
    Indicate,
    LaggedStart,
    Line,
    ManimColor,
    MathTex,
    MoveAlongPath,
    Rectangle,
    ReplacementTransform,
    RoundedRectangle,
    Rotate,
    Square,
    Text,
    Transform,
    UpdateFromAlphaFunc,
    VGroup,
    VMobject,
    linear,
)
from manim_slides import Slide

from .model import N, TARGET, diffuse, oracle, qubit_amplitudes, search_plane, uniform_state
from .notes import NOTES

BG = "#0B1120"
PANEL = "#131E32"
WHITE = "#EDF2FA"
MUTED = "#96A6BF"
BLUE = "#68A9FF"
GREEN = "#62E6BC"
RED = "#FF7B8A"
YELLOW = "#FFD580"
GRID = "#33445F"
FONT = "IBM Plex Sans"


def text(value, size=26, color=WHITE, **kwargs):
    return Text(value, font=FONT, font_size=size, color=color, **kwargs)


def at_left(mob, x, y):
    return mob.move_to([x + mob.width / 2, y, 0])


class GroverPresentation(Slide):
    """Five core chapters and a geometry appendix, with 21 click builds."""

    def cue(self, name):
        # These notes describe the animations AFTER next_slide().
        self.next_slide(notes=NOTES[name])

    def header(self, chapter, title, subtitle):
        heading = at_left(text(title, 42, GREEN, weight="BOLD"), -6.35, 3.35)
        sub = at_left(text(subtitle, 21, MUTED), -6.35, 2.32)
        rule = Line([-6.35, -3.28, 0], [6.35, -3.28, 0], color=GRID, stroke_width=1)
        footer = at_left(
            text("GROVER'S ALGORITHM  /  FUN GEOMETRIC TOUR", 13, MUTED), -6.35, -3.6
        )
        number = text(f"{chapter:02d} / 06", 15, GREEN).move_to([5.9, -3.6, 0])
        return VGroup(heading, sub, rule, footer, number)

    def change_header(self, chapter, title, subtitle):
        self.play(
            Transform(self.chrome, self.header(chapter, title, subtitle)),
            run_time=0.55,
        )

    def clear_body(self):
        self.play(
            *[FadeOut(m) for m in self.mobjects if m is not self.chrome], run_time=0.45
        )

    def banner(self, message, color=GREEN, y=-2.85):
        line = text(message, 25, color)
        if line.width > 12.2:
            line.scale_to_fit_width(12.2)
        return line.move_to([0, y, 0])

    def card(self, title, formula, detail, color, y):
        box = RoundedRectangle(
            width=5.35,
            height=1.65,
            corner_radius=0.15,
            fill_color=PANEL,
            fill_opacity=1,
            stroke_color=GRID,
            stroke_width=1,
        ).move_to([3.45, y, 0])
        label = at_left(text(title, 19, color), 1.05, y + 0.48)
        eq = MathTex(formula, font_size=41, color=color).move_to([4.9, y + 0.22, 0])
        desc = at_left(text(detail, 24), 1.05, y - 0.33)
        return VGroup(box, label, eq, desc)

    def construct(self):
        self.camera.background_color = ManimColor(BG)
        self.qubit_intro()
        self.problem()
        self.superposition()
        self.engine()
        self.databases()
        self.security()
        self.geometry()

    def qubit_intro(self):
        """Full-circle motion: superposition, Born probabilities, and signed amplitudes."""
        self.cue("qubit_basis")
        self.chrome = self.header(
            0, "From a bit to a qubit.",
            "A bit stores 0 or 1. A qubit can be prepared in a superposition.",
        )
        center, radius = np.array([-3.6, -0.15, 0.0]), 1.6
        circle = Circle(radius=radius, color=GRID, stroke_width=2).move_to(center)
        poles = VGroup(
            MathTex(r"|0\rangle", color=BLUE, font_size=36).move_to([-3.6, 1.9, 0]),
            MathTex(r"|1\rangle", color=GREEN, font_size=36).move_to([-3.6, -2.2, 0]),
        )
        vector = VGroup(
            Arrow(center, center + UP*radius, buff=0, color=YELLOW, stroke_width=5),
            Dot(center + UP*radius, radius=0.065, color=YELLOW),
        )
        readouts = VGroup()
        numbers, bars = [], []
        left, track_width = 0.8, 4.65
        for i, (color, y) in enumerate([(BLUE, 1.15), (GREEN, -0.85)]):
            box = RoundedRectangle(width=5.8, height=1.8, corner_radius=0.15,
                                   stroke_color=GRID, stroke_width=1,
                                   fill_color=PANEL, fill_opacity=1).move_to([3.15, y, 0])
            label = at_left(text(f"Measuring {i}", 25, color, weight="BOLD"), left, y+0.55)
            amp_label = at_left(text("Amplitude", 19, MUTED), left, y)
            chance_label = at_left(text("Probability", 19, MUTED), 3.3, y)
            amp = DecimalNumber(1-i, num_decimal_places=3, include_sign=True, font_size=30, color=color)
            chance = DecimalNumber(100*(1-i), num_decimal_places=1, unit=r"\%",
                                   font_size=30, color=color)
            amp_anchor = np.array([left, y-0.43, 0])
            chance_anchor = np.array([3.3, y-0.43, 0])
            amp.move_to(amp_anchor, aligned_edge=LEFT)
            chance.move_to(chance_anchor, aligned_edge=LEFT)
            track = Rectangle(width=track_width, height=0.12, stroke_width=0,
                              fill_color=GRID, fill_opacity=1).move_to([left+track_width/2, y-0.76, 0])
            bar = track.copy().set_fill(color)
            readouts.add(box, label, amp_label, chance_label, amp, chance, track, bar)
            numbers.append((amp, chance, amp_anchor, chance_anchor))
            bars.append((bar, y-0.76, color))

        def update_values(theta):
            amplitudes = qubit_amplitudes(theta)
            for i, amplitude in enumerate(amplitudes):
                probability = float(abs(amplitude)**2)
                amp, chance, amp_anchor, chance_anchor = numbers[i]
                rounded = round(float(amplitude), 3)
                amp.set_value(rounded if rounded else 0.0).move_to(amp_anchor, aligned_edge=LEFT)
                chance.set_value(100*probability).move_to(chance_anchor, aligned_edge=LEFT)
                bar, y, color = bars[i]
                width = max(track_width*probability, 1e-6)
                bar.become(Rectangle(width=width, height=0.12, stroke_width=0,
                                     fill_color=color, fill_opacity=1 if probability > 1e-12 else 0)
                           .move_to([left+width/2, y, 0]))

        update_values(0)
        stage = self.banner("A qubit has an amplitude for 0 and an amplitude for 1.", WHITE)
        self.play(FadeIn(self.chrome), FadeIn(circle), FadeIn(poles), FadeIn(vector),
                  FadeIn(readouts), FadeIn(stage), run_time=0.8)
        self.wait(0.3)
        angle = 0.0

        def move_to(target, duration=1.6):
            nonlocal angle
            start = angle
            # Both animations share the same easing and angle. The arrow is
            # rotated in place; fixed readout anchors prevent layout jumps.
            self.play(Rotate(vector, angle=-(target-start), about_point=center),
                      UpdateFromAlphaFunc(readouts, lambda _mob, a: update_values(start+a*(target-start))),
                      run_time=duration, rate_func=linear)
            angle = target
            update_values(target)

        self.cue("qubit_superposition")
        self.play(Transform(stage, self.banner("Superposition: both outcomes have an amplitude. Measurement gives just one.", WHITE)), run_time=0.35)
        move_to(np.pi/3)
        self.wait(0.5)
        move_to(np.pi/2)
        self.play(Transform(stage, self.banner("Amplitude × amplitude = probability. Here: about 0.707² = 50% each.", YELLOW)), run_time=0.35)
        self.wait(0.6)

        self.cue("qubit_probabilities")
        # Continue CLOCKWISE through the bottom and onto the left half.
        # The state amplitudes follow the same continuous rotation, including
        # their signs. Do not fold the angle back into the right semicircle.
        self.play(Transform(stage, self.banner("Keep going around: the probabilities change as the state moves.", WHITE)), run_time=0.35)
        move_to(np.pi, duration=1.8)
        self.wait(0.5)
        move_to(3*np.pi/2, duration=1.8)
        self.play(Transform(stage, self.banner("50/50 again — but one amplitude changed sign. Signs matter for interference.", YELLOW)), run_time=0.35)
        self.wait(0.8)

        self.cue("qubit_move")
        self.play(Transform(stage, self.banner("Watch a full turn: amplitudes can be negative; probabilities never are.", WHITE)), run_time=0.35)
        move_to(2*np.pi, duration=1.8)
        self.wait(0.5)
        move_to(5*np.pi/2, duration=1.8)
        self.play(Transform(stage, self.banner("Grover uses interference to increase the chance of measuring the answer.", GREEN)), run_time=0.35)
        self.wait(0.8)

    def problem(self):
        self.cue("problem")
        self.clear_body()
        self.change_header(
            1,
            "Find one match. Search less.",
            "Grover's algorithm: a quadratic speedup for unstructured search.",
        )
        self.grid = (
            VGroup(
                *[
                    Square(
                        side_length=0.35,
                        stroke_width=0.8,
                        stroke_color=GRID,
                        fill_color=GRID,
                        fill_opacity=0.7,
                    )
                    for _ in range(96)
                ]
            )
            .arrange_in_grid(rows=8, cols=12, buff=0.09)
            .move_to([-3.55, -0.1, 0])
        )
        self.grid_label = text("ONE MATCH  /  NO INDEX", 17, MUTED).next_to(
            self.grid, DOWN, buff=0.32
        )
        question = VGroup(
            text("1,000,000", 52, weight="BOLD"),
            text("candidates. Where is the match?", 22, MUTED),
        )
        question.arrange(DOWN, buff=0.2).move_to([3.45, 0.5, 0])
        self.play(
            FadeIn(self.chrome),
            LaggedStart(*[FadeIn(s) for s in self.grid], lag_ratio=0.006),
            FadeIn(self.grid_label),
            FadeIn(question),
            run_time=1.1,
        )
        self.wait(0.2)

        self.cue("scan")
        self.play(FadeOut(question), run_time=0.25)
        self.scan = Square(side_length=0.42, color=RED, stroke_width=3).move_to(
            self.grid[0]
        )
        path = VMobject().set_points_as_corners(
            [s.get_center() for s in self.grid[:67]]
        )
        self.play(FadeIn(self.scan), run_time=0.2)
        self.play(MoveAlongPath(self.scan, path), run_time=3.0, rate_func=linear)
        self.play(
            self.grid[66].animate.set_fill(GREEN, 1),
            self.scan.animate.set_color(GREEN),
            run_time=0.3,
        )
        self.classical = self.card(
            "CLASSICAL SCAN", r"O(N)", "≈ 500,000 checks on average", RED, 0.85
        )
        self.play(FadeIn(self.classical, shift=UP * 0.1), run_time=0.5)

        self.cue("speedup")
        self.quantum = self.card(
            "GROVER SEARCH",
            r"O(\sqrt{N})",
            "≈ 785 quantum oracle queries",
            GREEN,
            -1.05,
        )
        self.query_note = self.banner(
            "Query counts, not a wall-clock benchmark.", MUTED
        )
        self.play(
            FadeIn(self.quantum, shift=UP * 0.1), FadeIn(self.query_note), run_time=0.65
        )
        self.wait(0.2)

    def chart_bars(self, values, marked=False):
        bars = VGroup()
        for i, value in enumerate(values):
            height = max(abs(float(value)) * self.amplitude_scale, 0.001)
            bar = Rectangle(
                width=0.56,
                height=height,
                stroke_width=0,
                fill_color=GREEN if marked and i == TARGET else BLUE,
                fill_opacity=1,
            )
            bar.move_to([self.bar_x[i], self.zero + np.sign(value) * height / 2, 0])
            bars.add(bar)
        return bars

    def animate_bars(self, values, *animations, run_time=1):
        old, new = self.state.copy(), np.array(values)
        # Interpolate signed values, not rectangle geometry, so a phase flip
        # shrinks to zero before growing below it. Every bar stays anchored.
        self.play(
            UpdateFromAlphaFunc(
                self.bars,
                lambda mob, alpha: mob.become(
                    self.chart_bars((1 - alpha) * old + alpha * new, marked=True)
                ),
            ),
            *animations,
            run_time=run_time,
        )
        self.state = new

    def mean_guide(self, value):
        y = self.zero + float(value) * self.amplitude_scale
        line = DashedLine(
            [-5.95, y, 0], [1.65, y, 0], color=YELLOW, stroke_width=2, dash_length=0.09
        )
        label = at_left(text("mean", 16, YELLOW), -6.45, y + 0.17)
        return VGroup(line, label)

    def probability_card(self, probability, caption, color=BLUE):
        label = at_left(text("TARGET PROBABILITY", 16, MUTED), 2.4, 0.95)
        value = at_left(
            text(f"{100 * probability:.1f}%", 56, color, weight="BOLD"), 2.4, 0.25
        )
        desc = at_left(text(caption, 21, MUTED), 2.4, -0.5)
        formula = at_left(
            MathTex(r"P(x)=|a_x|^2", font_size=32, color=WHITE), 2.4, -1.22
        )
        return VGroup(label, value, desc, formula)

    def superposition(self):
        self.cue("superposition")
        self.change_header(
            2,
            "Start with equal possibilities.",
            "8 candidate labels · 3 qubits · Hadamard gates prepare a uniform state.",
        )
        self.zero, self.amplitude_scale = -0.2, 1.9
        self.bar_x = np.linspace(-5.4, 1.1, N)
        self.state = uniform_state()
        self.bars = self.chart_bars(self.state)
        self.axis = Line(
            [-5.95, self.zero, 0], [1.65, self.zero, 0], color=MUTED, stroke_width=1.5
        )
        self.labels = VGroup(
            *[
                text(f"{i:03b}", 18, MUTED).move_to([x, -2.25, 0])
                for i, x in enumerate(self.bar_x)
            ]
        )
        self.axis_title = at_left(text("AMPLITUDE  (signed)", 16, MUTED), -5.95, 1.85)
        self.mean = self.mean_guide(np.mean(self.state))
        self.prob = self.probability_card(1 / N, "One chance in eight.")
        self.stage = self.banner("Equal amplitude ≠ all answers read at once.", BLUE)
        self.play(
            FadeOut(self.classical),
            FadeOut(self.quantum),
            FadeOut(self.query_note),
            FadeOut(self.grid_label),
            FadeOut(self.scan),
            ReplacementTransform(self.grid, self.bars),
            FadeIn(self.axis),
            FadeIn(self.labels),
            FadeIn(self.axis_title),
            FadeIn(self.mean),
            FadeIn(self.prob),
            FadeIn(self.stage),
            run_time=1.1,
        )
        self.wait(0.2)

        self.cue("readout")
        self.play(
            Transform(
                self.stage,
                self.banner(
                    "Measurement returns ONE candidate. We need interference.", WHITE
                ),
            ),
            Indicate(self.prob[1], color=BLUE),
            run_time=0.8,
        )
        self.wait(0.2)

    def engine(self):
        self.cue("engine")
        self.change_header(
            3,
            "The engine: flip & amplify.",
            "One iteration = oracle phase flip + reflection about the mean.",
        )
        self.play(
            Transform(
                self.stage,
                self.banner("Watch candidate 101. The bars are amplitudes.", WHITE),
            ),
            run_time=0.4,
        )

        self.cue("oracle")
        self.animate_bars(
            oracle(self.state),
            self.labels[TARGET].animate.set_color(GREEN),
            Transform(
                self.stage,
                self.banner(
                    "1 / ORACLE   Flip the target's sign. Probability is unchanged.",
                    GREEN,
                ),
            ),
            run_time=0.95,
        )
        self.wait(0.2)

        self.cue("mean")
        self.play(
            Transform(self.mean, self.mean_guide(np.mean(self.state))),
            Transform(
                self.stage,
                self.banner(
                    "The mean drops. This guide is bookkeeping, not a gate.", YELLOW
                ),
            ),
            run_time=0.85,
        )
        self.wait(0.2)

        self.cue("reflect")
        reflected = diffuse(self.state)
        formula = at_left(
            MathTex(r"a'_x = 2\bar{a} - a_x", font_size=33, color=YELLOW), 2.4, -2.05
        )
        self.animate_bars(
            reflected,
            Transform(
                self.prob,
                self.probability_card(
                    reflected[TARGET] ** 2, "After one iteration.", GREEN
                ),
            ),
            FadeIn(formula),
            Transform(
                self.stage,
                self.banner(
                    "2 / DIFFUSION   Reflect every amplitude about the mean.", YELLOW
                ),
            ),
            run_time=1.4,
        )
        self.wait(0.2)

        self.cue("repeat")
        self.animate_bars(
            oracle(self.state),
            Transform(
                self.stage, self.banner("Repeat: flip → reflect → measure.", GREEN)
            ),
            run_time=0.65,
        )
        self.play(
            Transform(self.mean, self.mean_guide(np.mean(self.state))), run_time=0.45
        )
        reflected = diffuse(self.state)
        self.animate_bars(
            reflected,
            Transform(
                self.prob,
                self.probability_card(
                    reflected[TARGET] ** 2, "After two iterations.", GREEN
                ),
            ),
            run_time=1.1,
        )
        self.play(
            Indicate(self.bars[TARGET], color=GREEN, scale_factor=1.06),
            Transform(
                self.stage,
                self.banner(
                    "Measure now: 101 with 94.5% probability. Stop at the right time.",
                    GREEN,
                ),
            ),
            run_time=0.75,
        )
        self.wait(0.2)

    def databases(self):
        self.cue("linear")
        self.clear_body()
        self.change_header(
            4,
            "A comparison of search costs.",
            "2 problems: a square root is not enough, and an unknown number of solutions is bad",
        )

        axes = Axes(
            x_range=[0, 6, 25],
            y_range=[0, 6, 25],
            x_length=8.05,
            y_length=3.35,
            axis_config={"color": GRID, "include_tip": False, "stroke_width": 2},
        )
        axes.move_to([-1.7, 0.05, 0])

        x_ticks = VGroup(
            *[
                MathTex(str(v), font_size=22, color=MUTED).next_to(
                    axes.c2p(v, 0), DOWN, buff=0.15
                )
                for v in [0, 25, 50, 75, 6]
            ]
        )
        y_ticks = VGroup(
            *[
                MathTex(str(v), font_size=22, color=MUTED).next_to(
                    axes.c2p(0, v), LEFT, buff=0.13
                )
                for v in [0, 25, 50, 75, 6]
            ]
        )
        guides = VGroup(
            *[
                Line(axes.c2p(0, v), axes.c2p(6, v), color=GRID, stroke_width=0.7)
                for v in [25, 50, 75, 6]
            ]
        )

        x_label = text("Candidates N  (linear scale)", 18, MUTED).next_to(
            axes, DOWN, buff=0.48
        )
        y_label = at_left(text("Work  (linear scale)", 17, MUTED), -6.35, 1.94)

        linear_curve = axes.plot(lambda x: x, x_range=[0, 6], color=RED, stroke_width=4)
        square_curve = axes.plot(
            lambda x: np.sqrt(x), x_range=[0, 6], color=GREEN, stroke_width=4
        )

        legend1 = self.legend_item("Linear scan", r"O(N)", RED, 1.0)
        legend2 = self.legend_item("Grover queries", r"O(\sqrt{N})", GREEN, -0.3)

        self.play(
            FadeIn(axes),
            FadeIn(x_ticks),
            FadeIn(y_ticks),
            FadeIn(guides),
            FadeIn(x_label),
            FadeIn(y_label),
            run_time=0.5,
        )
        self.play(Create(linear_curve), FadeIn(legend1), run_time=1)

        self.cue("sqrt")
        self.play(Create(square_curve), FadeIn(legend2), run_time=1)

        self.next_slide()
        self.play(
            Indicate(square_curve, color=GREEN, scale_factor=1.03),
            FadeIn(
                self.banner(
                    r"1. $\sqrt{N}$ is still too slow for huge N   |   2. Unknown number of solutions breaks stopping time",
                    YELLOW,
                )
            ),
            run_time=0.8,
        )
        self.wait(0.2)

    def legend_item(self, label, formula, color, y):
        name = at_left(text(label, 22, color), 3.0, y)
        eq = at_left(MathTex(formula, font_size=32, color=color), 3.0, y - 0.48)
        return VGroup(name, eq)

    def key_meter(self, bits, y, color=BLUE):
        # Width encodes the exponent (bits), never the raw number of keys.
        left, width = -5.45, bits / 256 * 10.9
        outline = Rectangle(
            width=width,
            height=0.65,
            stroke_color=color,
            fill_color=color,
            fill_opacity=0.14,
            stroke_width=1.5,
        )
        outline.move_to([left + width / 2, y, 0])
        label = at_left(text(f"AES-{bits}", 27, color, weight="BOLD"), left, y + 0.72)
        space = MathTex(rf"2^{{{bits}}}\ \mathrm{{keys}}", font_size=29, color=MUTED)
        if bits == 128:
            space.next_to(outline, RIGHT, buff=0.3)
        else:
            at_left(space, left + 7.6, y + 0.72)
        return VGroup(outline, label, space)

    def slice_meter(self, meter, bits, y, color):
        left, width = -5.45, bits / 256 * 10.9
        cut_x = left + width / 2
        cut = Line(
            [cut_x, y - 0.5, 0], [cut_x, y + 0.5, 0], color=WHITE, stroke_width=4
        )
        remaining = Rectangle(
            width=width / 2,
            height=0.65,
            stroke_width=0,
            fill_color=color,
            fill_opacity=0.85,
        )
        remaining.move_to([left + width / 4, y, 0])
        estimate = at_left(
            MathTex(
                rf"O(2^{{{bits // 2}}})\ \text{{quantum queries}}",
                font_size=29,
                color=color,
            ),
            cut_x + 0.3,
            y,
        )
        self.play(Create(cut), run_time=0.35)
        self.play(
            FadeIn(remaining),
            meter[0].animate.set_stroke(color=GRID).set_fill(GRID, 0.12),
            FadeOut(meter[2]),
            FadeIn(estimate),
            run_time=0.65,
        )

    def security(self):
        self.cue("crypto")
        self.clear_body()
        self.change_header(
            5,
            "Why security engineers care.",
            "Generic symmetric-key search: Grover halves the exponent of the query cost.",
        )
        scale_note = at_left(
            text("BAR WIDTH = EXPONENT / BITS, NOT NUMBER OF KEYS", 16, MUTED),
            -5.45,
            1.63,
        )
        aes128 = self.key_meter(128, 0.35)
        caveat = self.banner(
            "Idealized quantum queries; real fault-tolerant attacks cost much more.",
            MUTED,
        )
        self.play(FadeIn(scale_note), FadeIn(aes128), FadeIn(caveat), run_time=0.6)

        self.cue("aes128")
        self.slice_meter(aes128, 128, 0.35, RED)

        self.cue("aes256")
        aes256 = self.key_meter(256, -1.35, GREEN)
        self.play(ReplacementTransform(aes128.copy(), aes256), run_time=0.75)
        self.slice_meter(aes256, 256, -1.35, GREEN)
        self.wait(0.2)

        self.cue("takeaway")
        self.play(
            Transform(
                caveat,
                self.banner(
                    "Flip. Reflect. Repeat. Measure.   /   AES-256 offers a strong margin.",
                    GREEN,
                ),
            ),
            run_time=0.65,
        )
        self.wait(0.4)

    def geometry(self):
        """Show the exact two reflections in the (solution, non-solution) basis."""
        self.cue("geometry")
        self.clear_body()
        self.change_header(
            6,
            "Two reflections make a rotation.",
            "The same eight-state example, expressed in its two-dimensional search subspace.",
        )
        center = np.array([-3.6, -0.25, 0.0])
        radius = 1.95
        state = uniform_state()
        initial = search_plane(state)
        theta = float(np.arcsin(initial[0]))
        initial_angle = float(np.arctan2(initial[1], initial[0]))

        def point(angle, length=radius):
            return center + length * np.array([np.cos(angle), np.sin(angle), 0])

        def state_arrow(angle, color):
            return Arrow(
                center,
                point(angle),
                buff=0,
                color=color,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.1,
            )

        def label_at(formula, angle, color):
            return MathTex(formula, font_size=29, color=color).move_to(
                point(angle, radius + 0.4)
            )

        def panel(title, equation, detail, probability, color):
            # The basis definition above this panel stays fixed on every click.
            return VGroup(
                at_left(text(title, 18, color), 0.15, 0.53),
                at_left(MathTex(equation, font_size=32, color=color), 0.15, -0.04),
                at_left(MathTex(detail, font_size=29, color=WHITE), 0.15, -0.72),
                at_left(MathTex(probability, font_size=32, color=color), 0.15, -1.48),
            )

        circle = Circle(radius=radius, stroke_color=GRID, stroke_width=2).move_to(
            center
        )
        horizontal = Arrow(
            center + LEFT * 2.25,
            center + RIGHT * 2.25,
            buff=0,
            color=GRID,
            stroke_width=2,
            tip_length=0.12,
        )
        vertical = Arrow(
            center + DOWN * 2.1,
            center + UP * 1.98,
            buff=0,
            color=MUTED,
            stroke_width=2,
            tip_length=0.12,
        )
        x_ket = MathTex(r"|w\rangle", font_size=32, color=GREEN).move_to(
            [-0.99, -0.25, 0]
        )
        y_ket = MathTex(r"|w^\perp\rangle", font_size=32, color=MUTED).move_to(
            [-3.6, 2.0, 0]
        )
        reference = DashedLine(
            point(initial_angle + np.pi, radius * 1.06),
            point(initial_angle, radius * 1.06),
            color=BLUE,
            stroke_width=2,
            dash_length=0.08,
        )
        angle_arc = Arc(
            radius=0.68,
            start_angle=initial_angle,
            angle=theta,
            arc_center=center,
            color=YELLOW,
            stroke_width=3,
        )
        angle_label = MathTex(r"\theta", font_size=25, color=YELLOW).move_to(
            center + [0.17, 0.92, 0]
        )
        mirror_key = MathTex(
            r"\text{Dashed line: fixed initial state }|s\rangle",
            font_size=19,
            color=BLUE,
        ).move_to([-3.6, -2.49, 0])
        basis = VGroup(
            at_left(text("BASIS / ONE MARKED STATE", 16, MUTED), 0.15, 1.8),
            at_left(
                MathTex(
                    r"|w\rangle=|101\rangle,\quad"
                    r"|w^\perp\rangle=\frac{1}{\sqrt{7}}\!\sum_{x\ne101}|x\rangle",
                    font_size=31,
                    color=WHITE,
                ),
                0.15,
                1.2,
            ),
        )
        constants = at_left(
            MathTex(
                r"N=8,\quad\theta=\arcsin\!\frac{1}{\sqrt{8}}\approx20.7^\circ",
                font_size=26,
                color=MUTED,
            ),
            0.15,
            -2.21,
        )
        info = panel(
            "INITIALIZE / EQUAL SUPERPOSITION",
            r"|s\rangle=\sin\theta|w\rangle+\cos\theta|w^\perp\rangle",
            r"|s\rangle=H^{\otimes3}|000\rangle",
            r"P(w)=\sin^2\theta=12.5\%",
            BLUE,
        )
        arrow = state_arrow(initial_angle, BLUE)
        label = label_at(r"|s\rangle", initial_angle, BLUE)
        stage = self.banner(
            "Unit circle: x = solution amplitude, y = non-solution amplitude.", WHITE
        )
        self.play(
            Create(circle),
            FadeIn(horizontal),
            FadeIn(vertical),
            FadeIn(x_ket),
            FadeIn(y_ket),
            Create(reference),
            Create(angle_arc),
            FadeIn(angle_label),
            FadeIn(mirror_key),
            FadeIn(basis),
            FadeIn(constants),
            FadeIn(info),
            FadeIn(stage),
            run_time=0.8,
        )
        self.play(Create(arrow), FadeIn(label), run_time=0.7)
        self.wait(0.2)

        def reflect_to(new_state, color, ket, *animations, run_time=1.25):
            nonlocal state
            old_xy, new_xy = search_plane(state), search_plane(new_state)
            start = float(np.arctan2(old_xy[1], old_xy[0]))
            end = float(np.arctan2(new_xy[1], new_xy[0]))
            new_label = MathTex(ket, font_size=29, color=color)
            # A unit-circle tween between reflection endpoints, not a model
            # of gate evolution (which can acquire complex amplitudes).
            self.play(
                UpdateFromAlphaFunc(
                    arrow,
                    lambda mob, alpha: mob.become(
                        state_arrow(start + (end - start) * alpha, color)
                    ),
                ),
                UpdateFromAlphaFunc(
                    label,
                    lambda mob, alpha: mob.become(
                        new_label.copy().move_to(
                            point(start + (end - start) * alpha, radius + 0.4)
                        )
                    ),
                ),
                *animations,
                run_time=run_time,
            )
            state = new_state

        self.cue("geometry_oracle")
        reflect_to(
            oracle(state),
            RED,
            r"O|s\rangle",
            vertical.animate.set_color(RED),
            Transform(
                info,
                panel(
                    "1 / ORACLE: REFLECT ABOUT THE VERTICAL AXIS",
                    r"O=I-2|w\rangle\langle w|",
                    r"(a_w,a_\perp)\longmapsto(-a_w,a_\perp)",
                    r"P(w)=\sin^2\theta=12.5\%",
                    RED,
                ),
            ),
            Transform(
                stage,
                self.banner(
                    "Oracle: negate the solution component. Its probability stays the same.",
                    RED,
                ),
            ),
        )
        self.wait(0.2)

        self.cue("geometry_diffusion")
        net_arc = Arc(
            radius=1.02,
            start_angle=initial_angle,
            angle=-2 * theta,
            arc_center=center,
            color=GREEN,
            stroke_width=3,
        )
        turn_label = MathTex(r"2\theta", font_size=25, color=GREEN).move_to(
            point(initial_angle - theta, 1.28)
        )
        reflect_to(
            diffuse(state),
            GREEN,
            r"|\psi_1\rangle",
            vertical.animate.set_color(MUTED),
            reference.animate.set_color(YELLOW),
            mirror_key.animate.set_color(YELLOW),
            Transform(
                info,
                panel(
                    "2 / DIFFUSION: REFLECT ABOUT THE FIXED s LINE",
                    r"D=2|s\rangle\langle s|-I",
                    r"|\psi_1\rangle=DO|s\rangle",
                    r"P(w)=\sin^2(3\theta)\approx78.1\%",
                    GREEN,
                ),
            ),
            Transform(
                stage,
                self.banner(
                    "Oracle, then diffusion: DO rotates clockwise by 2θ toward the solution.",
                    GREEN,
                ),
            ),
            run_time=1.45,
        )
        self.play(Create(net_arc), FadeIn(turn_label), run_time=0.55)
        self.wait(0.2)

        self.cue("geometry_repeat")
        ghost = state_arrow(initial_angle - 2 * theta, GREEN).set_opacity(0.25)
        self.add(ghost)
        reflect_to(
            oracle(state),
            RED,
            r"O|\psi_1\rangle",
            vertical.animate.set_color(RED),
            Transform(
                stage,
                self.banner(
                    "Again: reflect across the vertical axis, then the SAME initial-state line.",
                    YELLOW,
                ),
            ),
            Transform(
                info,
                panel(
                    "REPEAT / ORACLE AGAIN",
                    r"O=I-2|w\rangle\langle w|",
                    r"O|\psi_1\rangle=ODO|s\rangle",
                    r"P(w)\approx78.1\%",
                    RED,
                ),
            ),
            run_time=1.1,
        )
        second_arc = Arc(
            radius=1.02,
            start_angle=initial_angle - 2 * theta,
            angle=-2 * theta,
            arc_center=center,
            color=GREEN,
            stroke_width=3,
        )
        second_turn_label = MathTex(r"2\theta", font_size=25, color=GREEN).move_to(
            point(initial_angle - 3 * theta, 1.3)
        )
        reflect_to(
            diffuse(state),
            GREEN,
            r"|\psi_2\rangle",
            vertical.animate.set_color(MUTED),
            Transform(
                info,
                panel(
                    "REPEAT / SECOND GROVER ITERATION",
                    r"|\psi_k\rangle=(DO)^k|s\rangle",
                    r"=\sin((2k+1)\theta)|w\rangle+\cos((2k+1)\theta)|w^\perp\rangle",
                    r"P_2(w)=\sin^2(5\theta)\approx94.5\%",
                    GREEN,
                ),
            ),
            Transform(
                stage,
                self.banner(
                    "Two reflections → a 2θ rotation. Stop near the solution; further steps overshoot.",
                    GREEN,
                ),
            ),
            run_time=1.45,
        )
        self.play(Create(second_arc), FadeIn(second_turn_label), run_time=0.55)
        self.wait(0.4)
