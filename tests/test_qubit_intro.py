"""Numerical and boundary regressions, with no scene construction or rendering."""

import unittest
import numpy as np

from grover_slides.deck import GroverPresentation
from grover_slides.model import bloch_vector


class QubitIntroTests(unittest.TestCase):
    def test_bloch_poles_and_equator(self):
        for theta, phi, expected in [
            (0, 0, [0, 0, 1]),
            (np.pi, 0, [0, 0, -1]),
            (np.pi/2, 0, [1, 0, 0]),
            (np.pi/2, np.pi, [-1, 0, 0]),
            (np.pi/2, np.pi/2, [0, 1, 0]),
        ]:
            np.testing.assert_allclose(bloch_vector(theta, phi), expected, atol=1e-14)

    def test_half_angle_probabilities_and_phase_invariance(self):
        # Independently compare Bloch z probabilities with state amplitudes.
        for theta in [0, np.pi/4, np.pi/2, np.pi]:
            for phi in [0, np.pi/3, np.pi]:
                amplitudes = np.array([np.cos(theta/2), np.exp(1j*phi)*np.sin(theta/2)])
                bloch = bloch_vector(theta, phi)
                self.assertAlmostEqual(float(bloch @ bloch), 1)
                np.testing.assert_allclose(np.abs(amplitudes)**2,
                                           [(1+bloch[2])/2, (1-bloch[2])/2], atol=1e-14)

    def test_intro_is_not_cleared_before_next_click(self):
        class StopAtClear(Exception):
            pass

        class BoundaryProbe:
            fragment = "qubit_phase"

            def cue(self, name):
                self.fragment = name

            def clear_body(self):
                # Stop before geometry code: observe which fragment owns this fade.
                raise StopAtClear(self.fragment)

        with self.assertRaises(StopAtClear) as result:
            GroverPresentation.problem(BoundaryProbe())
        self.assertEqual(result.exception.args[0], "problem")
