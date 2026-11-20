"""Speaker script. Keys follow the chronological click order of the deck."""

NOTES = {
    "qubit_basis": "A bit stores zero or one. A qubit has a probability amplitude for zero and another for one. We start at ket zero, so measuring gives zero with certainty. The circle is a simple front view of a Bloch meridian; keep the terminology off the slide. It is a map of states, not a plot whose coordinates are the amplitudes.",
    "qubit_superposition": "Move away from ket zero. Both outcomes now have amplitudes: this is a superposition. Measurement still returns just one outcome. First pause at seventy-five percent zero and twenty-five percent one, then at fifty-fifty. The amplitudes there are about 0.707 each. For the real amplitudes shown here, multiplying an amplitude by itself gives its probability. The numbers are rounded for display; probabilities use the full-precision amplitudes.",
    "qubit_probabilities": "Continue clockwise around the circle, through ket one and onto the left side. Probabilities continuously follow the moving state. Stop on the left: the probabilities are fifty-fifty again, but now the zero amplitude is negative and the one amplitude is positive. This differs from the earlier equal superposition. Those relative signs affect interference, which is essential to Grover. The motion illustrates a continuous change of state, not a Grover oracle operation: its intermediate probabilities are allowed to change.",
    "qubit_move": "Continue clockwise past the top and finish on the right again. Amplitudes can be negative but their squared magnitudes are nonnegative and sum to one. After one full Bloch turn both amplitudes have a common minus sign: this is an unobservable global phase, so the north pole still represents ket zero. The final right-side state likewise has both amplitudes negative and is physically the same as the earlier right-side equal superposition. Do not mistake this common sign for the relative sign demonstrated on the left. Keep this subtlety in presenter notes; the introductory takeaway is that Grover uses interference to increase the chance of measuring the answer. The final view remains visible until the next click.",
    "problem": """00:00–00:15 · Chapter 1: the problem
    Imagine an unindexed table with a million records and exactly one match.
    You can test whether a record matches, but there is no ordering or index
    to guide you. How many checks do you need?""",
    "scan": """00:15–00:35 · Click: classical scan
    A classical computer checks candidates one at a time. If the match is
    equally likely to be anywhere, it takes about half a million checks on
    average. The cost grows linearly with the number of candidates.""",
    "speedup": """00:35–01:00 · Click: quantum comparison
    Grover's algorithm reduces this to roughly eight hundred oracle queries:
    square-root scaling. This is a quadratic speedup. We are counting queries
    to a checker, not measuring seconds. Building a quantum checker and
    accessing the data also cost something.""",
    "superposition": """01:00–01:30 · Chapter 2: equal superposition
    Shrink the example to eight candidates, represented by three qubits.
    Hadamard gates prepare an equal superposition. Each bar shows a real
    amplitude, not a probability: its square gives the probability of that
    measurement outcome. All eight start at one eighth probability.""",
    "readout": """01:30–02:00 · Click: the readout limit
    Measurement gives you one candidate, not a list of all eight answers.
    Measuring now would just be a random guess. We need interference to make
    the correct candidate much more likely. Preparing candidate labels is
    easy; it does not magically load an arbitrary database.""",
    "engine": """02:00–02:10 · Chapter 3: flip and amplify
    Keep watching these same eight amplitudes. One Grover iteration has two
    operations: a phase flip, followed by a reflection about the mean.""",
    "oracle": """02:10–02:25 · Click 1: oracle
    The oracle recognizes a valid answer and flips its amplitude negative.
    Think of checking a proposed key against known encrypted data. It checks
    a candidate; it does not tell us which candidate to choose. The sign
    changes, but the probability has not changed yet.""",
    "mean": """02:25–02:35 · Click 2: mean
    With one bar negative, the arithmetic mean is lower. Moving this dashed
    guide is only an explanation of the mathematics, not another quantum
    operation.""",
    "reflect": """02:35–02:55 · Click 3: diffusion
    Reflect every amplitude about that mean: new amplitude equals twice
    the mean minus the old amplitude. The target jumps up; the others shrink.
    Its measurement probability has risen from twelve and a half percent
    to about seventy-eight percent.""",
    "repeat": """02:55–03:15 · Click 4: repeat and measure
    Do the same two operations once more. Now measurement returns the target
    with ninety-four point five percent probability. This is still not
    certainty. Stop at the right iteration count: repeating forever would
    rotate amplitude away from the target again.""",
    "linear": """03:15–03:30 · Chapter 4: database reality check
    Where does this help in IT? This plot compares growth in abstract work,
    not wall-clock benchmarks. A full scan grows linearly. The vertical
    axis is logarithmic so we can see all three curves.""",
    "sqrt": """03:30–03:45 · Click: Grover curve
    Grover's square-root query growth beats an unstructured scan. But it
    assumes coherent access to the checker. Data access, reversible circuits,
    and error correction can dominate the real cost.""",
    "index": """03:45–04:15 · Click: use an index
    An indexed equality lookup exploits structure and can grow logarithmically.
    That is a different setup: someone built and maintains the index. If an
    index answers your query, use it. Grover does not automatically make
    an ordinary database faster. Its advantage is for unstructured search.""",
    "crypto": """04:15–04:25 · Chapter 5: symmetric key search
    A cryptographic key space is a better example: knowing how to verify a
    key does not give you a useful search index. AES-128 has two to the
    hundred-and-twenty-eight possible keys.""",
    "aes128": """04:25–04:35 · Click: halve the exponent
    In the ideal query model, Grover reduces that search to order two to
    the sixty-four quantum queries. We halve the exponent, not the physical
    key or the number of candidate keys.""",
    "aes256": """04:35–04:50 · Click: AES-256
    With AES-256 the same estimate is order two to the hundred-and-twenty-eight
    quantum queries, a much larger margin. These are theoretical query counts,
    not practical attack costs. A quantum AES oracle is expensive.""",
    "takeaway": """04:50–05:00 · Click: takeaway
    Remember: flip, reflect, repeat, measure. Grover speeds up unstructured
    search quadratically. AES-256 gives a strong margin against this generic
    attack; public-key migration is a separate task.""",
    "geometry": """Optional technical appendix · 0:00–0:25 · Initialize
    This is the same eight-state system expressed in a two-dimensional
    invariant subspace. The horizontal basis ket is the solution, w equals
    101. The vertical ket is w perpendicular: the normalized, equal
    superposition of the seven non-solutions, not an individual wrong answer.
    The uniform initial state s has coordinates sine theta and cosine theta,
    with theta measured from the vertical axis. Here theta is about 20.7 degrees.
    The circle represents unit norm in this real search plane, not a Bloch sphere.""",
    "geometry_oracle": """Optional technical appendix · 0:25–0:40 · Oracle
    The oracle is I minus twice the projector onto w. It negates the solution
    component and leaves the perpendicular component unchanged. Geometrically,
    it reflects the arrow across the vertical axis. The horizontal projection
    changes sign, so its square, the solution probability, is unchanged.
    The animated arc illustrates the reflection's endpoints, not the physical
    time evolution inside a gate.""",
    "geometry_diffusion": """Optional technical appendix · 0:40–1:00 · Diffusion
    Diffusion is twice the projector onto s minus I. Its mirror is the fixed
    line through the ORIGINAL initial state s, shown dashed. It reflects the
    oracle output across that line. Oracle first, then diffusion: the product
    D O rotates the state clockwise by twice theta with our axis convention.
    The new state has coefficients sine three theta and cosine three theta.
    Its solution probability is now 78.1 percent, matching the bars.""",
    "geometry_repeat": """Optional technical appendix · 1:00–1:20 · Repeat
    Apply the same oracle and diffusion again, always using the same mirror
    line s. The state is now slightly below the horizontal solution axis.
    Its solution probability is sine squared five theta, or 94.5 percent.
    The vertical component is negative, just like the seven negative bars.
    In general after k iterations, the coefficients are sine and cosine of
    two k plus one times theta. This explains both square-root scaling and
    overshooting if we keep iterating past the optimum.""",
}
