# Grover's algorithm: five-minute talk + geometry appendix

A 16:9 Manim Slides presentation for an IT audience: five core chapters and a
technical closing slide, plus a qubit introduction, and a speaker script embedded in
the presenter view. Dark navy background, blue candidate amplitudes, mint
target, and yellow mean/index guides.

The core talk still lasts five minutes. The optional final geometry slide
adds about 80 seconds, or can be reserved for questions.

To rehearse just the final slide after rendering (fragment indices start at zero):

```sh
uv run python -m manim_slides --silent present GroverSlides --sasn 21 --show-info-window
```

## Run

The project uses Python 3.10+ and `uv`. Install the system dependencies required
by [Manim](https://docs.manim.community/en/stable/installation.html), including
FFmpeg, Cairo/Pango, and LaTeX with `dvisvgm` for mathematical labels. Install
**IBM Plex Sans** for the intended typography (or change `FONT` in `deck.py`).

```sh
uv sync
uv run grover-slides render          # 1080p; default quality is h
uv run grover-slides present
```

Use the right arrow to advance and the left arrow to go back. The presenter
window contains the notes and next-fragment preview. Animations finish and
hold their final frame until you advance: the five-minute timing is a speaking
guide, not five minutes of forced waits. The rendered MP4 alone contains only
the animation time and is not a five-minute narrated video.

For a fast preview or a browser presentation:

```sh
uv run grover-slides render -q l     # 480p preview; m gives 720p
uv run grover-slides export          # exports/grover.html, offline, one file
```

Export uses the most recent render. Render at high quality again before making
your final export. The initial offline export downloads Reveal.js assets;
afterward, the HTML contains the videos and presentation assets. Open it in a
browser, use Space to advance, F for fullscreen, and S for speaker notes.
Serve it locally if the browser restricts presenter features on `file://`:

```sh
uv run python -m http.server 8000 --directory exports
```

Then open `http://localhost:8000/grover.html`.

Equivalent direct commands, useful when changing Manim options:

```sh
uv run python -m manim -qh grover.py GroverSlides
uv run python -m manim_slides --silent present GroverSlides
uv run python -m manim_slides --silent convert GroverSlides exports/grover.html --offline --one-file
```

## Speaking plan

| Chapter | Time | Visual and click builds |
| --- | --- | --- |
| 1. Find one match | 0:00–1:00 | Unsorted grid → classical scan → quantum query comparison |
| 2. Equal possibilities | 1:00–2:00 | Grid morphs into eight equal amplitude bars → one-outcome measurement limit |
| 3. Flip & amplify | 2:00–3:15 | Same bars → oracle → mean guide drops → diffusion → second cycle and measurement probability |
| 4. Database reality check | 3:15–4:15 | Log-scale work plot: scan → Grover → indexed lookup |
| 5. Symmetric key search | 4:15–5:00 | AES-128 exponent → square-root search cost → AES-256 → takeaway |
| 6. Vector geometry (optional) | +1:20 | Unit circle and ket basis → oracle reflection → diffusion reflection → second iteration |

The full script is in [`src/grover_slides/notes.py`](src/grover_slides/notes.py).
Each `cue()` sets the notes for the animation that follows it. Chapter 3 has
the four demonstration clicks described above, after its introductory build.

## Content choices and limits

- The example has one marked state, `101`, among eight candidates. Bar heights
  come from the actual amplitude vector, not hand-picked heights. Target
  probabilities are **12.5% → 78.125% → 94.53125%**. Some non-target amplitudes
  become negative after iteration two. The smooth tween between endpoints is
  an explanatory animation, not a continuous simulation of physical gates.
- Moving the dashed mean guide is a mathematical explanation, not a third
  quantum operation. Diffusion preserves that mean. Squared amplitudes,
  including negative ones, determine measurement probabilities.
- The closing slide uses horizontal `|w⟩ = |101⟩` and vertical
  `|w⊥⟩ = (1/√7) Σ(x≠101)|x⟩`. This is the real, two-dimensional invariant
  search subspace of the eight-state system, not a Bloch sphere or a plot
  of individual computational basis states. The circle has unit norm.
  The initial state is `|s⟩ = sin(θ)|w⟩ + cos(θ)|w⊥⟩`, with
  `θ = arcsin(1/√8)`, measured from the vertical axis. Oracle
  `O = I − 2|w⟩⟨w|` reflects across the vertical axis; diffusion
  `D = 2|s⟩⟨s| − I` reflects across the **fixed initial-state line**.
  In this axis convention, `DO` rotates **clockwise** by `2θ`. After `k`
  iterations, `|ψₖ⟩ = sin((2k+1)θ)|w⟩ + cos((2k+1)θ)|w⊥⟩`.
  The second iteration crosses slightly below the solution axis and gives
  the same 94.5% probability as the bars. Motion along the circle illustrates
  the reflection endpoints; physical gates may leave this real plane during
  their implementation.
- For one match in a million candidates, about **785** Grover iterations
  suffice, using approximately `(π/4)√N` oracle calls. The classical expected
  count is `(N+1)/2`, rounded to 500,000. This compares query models, not total
  runtime or practical hardware performance.
- Superposition prepares candidate labels; it does not load an arbitrary
  classical database for free. The plot shows illustrative `N`, `√N`, and
  `log₂N` growth functions on **two logarithmic axes**. Indexed equality
  lookup assumes an existing suitable index; building and maintaining it is
  additional work. These are different access assumptions.
- The crypto meters encode **bits / the exponent**, not the size of the key
  space. `O(2⁶⁴)` and `O(2¹²⁸)` are idealized serial quantum query estimates
  for generic AES key search, omitting the expensive reversible oracle and
  fault tolerance. “64-bit security” is not a practical equivalence to a
  classical 64-bit key search. AES-256 provides a strong margin against this
  attack; avoid calling it an unconditional guarantee of safety.
- Hash preimage search, collision search, and public-key attacks have distinct
  threat models. Increasing an AES key length does not solve RSA/ECC
  migration, and a blanket “AES-256 and SHA-256 neutralize quantum threats”
  claim would be misleading. This short talk stays focused on symmetric key
  search. The current NIST FAQ does not call for abandoning AES-128 simply
  because of Grover's theoretical speedup.

## Sources

- [IBM Quantum: Grover's algorithm](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/grovers)
  — query scaling, phase oracle, diffusion, and measurement.
- [IBM Quantum: geometric analysis](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms/grover-algorithm/analysis)
  — the invariant search plane, two reflections, and their rotation.
- [NIST: Post-Quantum Cryptography FAQ](https://csrc.nist.gov/Projects/post-quantum-cryptography/faqs)
  — symmetric cryptography, practical costs, and limits to parallelizing Grover.
- [Grassl et al.: Applying Grover's algorithm to AES](https://arxiv.org/abs/1512.04965)
  — quantum resource estimates beyond the query-count shorthand.
- [Manim Slides API](https://manim-slides.eertmans.be/latest/reference/api.html)
  and [HTML export](https://manim-slides.eertmans.be/main/reference/html.html).

## Edit and verify

- [`grover.py`](grover.py): render entry point (`GroverSlides`).
- [`src/grover_slides/deck.py`](src/grover_slides/deck.py): visuals, layout, colors, animation durations.
- [`src/grover_slides/model.py`](src/grover_slides/model.py): the eight-state amplitude model.
- [`manim.cfg`](manim.cfg): resolution and rendering configuration.

```sh
uv run python -m unittest discover -s tests -v
```

Generated `media/`, `slides/`, and `exports/` are ignored by Git. Keep the
`slides/` JSON together with its `files/` directory for native presentation,
or share the single exported HTML file.

## Debug just the qubit introduction

`QubitIntro` is an independent scene that calls the same `qubit_intro()` method
as the full deck. It has its own output and does not replace the full deck's
slide manifest. No environment activation is required.

```sh
# Render only the intro, at low quality, and open its video preview.
uv run python -m manim -pql grover.py QubitIntro

# Present only its four click-controlled builds, after rendering.
uv run python -m manim_slides --silent present QubitIntro --show-info-window

# Render a selected animation range (zero-based play/wait indices).
uv run python -m manim -pql -n 2,3 grover.py QubitIntro

# Save just the final layout as a still image.
uv run python -m manim -ql -s grover.py QubitIntro
```

`-n` selects animation indices, not the pauses created by `next_slide()`.
Earlier code still executes to establish the scene state, but its frames are
skipped. Animation indices are printed in Manim's render log and can change
when you edit the scene. A partial render replaces that scene's slide manifest:
render the entire `QubitIntro` again before presenting all four builds.
A still-image render is for layout inspection; use a normal video render
before presenting with Manim Slides.

To jump to a build of an already rendered scene, use `--sasn INDEX`, for example
`--sasn 3` for the introduction's phase-flip build. It does not render anything.
The full deck must be rendered again before its saved indices and content
reflect source edits. Previously exported HTML also remains unchanged until
rendered and exported again.

The intro is now a **flat front view of the Bloch sphere**: `|0⟩` is north,
`|1⟩` south, `|+⟩` right, and `|−⟩` left. It shows the x–z meridian;
the y direction is perpendicular to the screen. Unlike the Grover search-plane
appendix, these coordinates are Bloch components, not probability amplitudes.
The state formula is `|ψ⟩ = cos(θ/2)|0⟩ + exp(iφ) sin(θ/2)|1⟩`.
Thus `|+⟩` is at **90 degrees**, with amplitudes `1/√2` and probabilities `1/2`.

The first movement is a meridian preparation path from `|0⟩` to `|+⟩`.
The Z gate then changes the relative phase from zero to pi, taking `|+⟩` to
`|−⟩`. A Z rotation goes out of this viewing plane: the slide cross-fades the
endpoints while leaving the probability bars unchanged, rather than tracing
an incorrect path around the meridian. The final view holds until the next
click. In the full deck, clearing the intro belongs to the next section's
fragment, after its `cue()`, so the intro does not end on a blank frame.

See [IBM's Bloch-sphere explanation](https://learning.quantum.ibm.com/course/general-formulation-of-quantum-information/density-matrices)
for the polar-angle and azimuth conventions.
