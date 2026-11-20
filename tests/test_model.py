"""Check the numerical claims shown to the audience, independently of layout."""

import unittest

import numpy as np

from grover_slides.model import N, TARGET, diffuse, oracle, search_plane, uniform_state


class GroverModelTests(unittest.TestCase):
    def test_oracle_preserves_every_measurement_probability(self):
        state = uniform_state()
        flipped = oracle(state)
        np.testing.assert_allclose(flipped ** 2, state ** 2)
        self.assertLess(flipped[TARGET], 0)
        self.assertEqual(np.count_nonzero(flipped < 0), 1)

    def test_diffusion_is_a_reflection_and_preserves_normalization(self):
        state = oracle(uniform_state())
        reflected = diffuse(state)
        np.testing.assert_allclose((state + reflected) / 2, np.full(N, state.mean()))
        np.testing.assert_allclose(diffuse(reflected), state)
        self.assertAlmostEqual(float(np.linalg.norm(reflected)), 1)

    def test_displayed_probabilities_match_exact_theory(self):
        state = uniform_state()
        for iteration, expected in enumerate([1 / 8, 25 / 32, 121 / 128]):
            self.assertAlmostEqual(float(state[TARGET] ** 2), expected)
            theta = np.arcsin(1 / np.sqrt(N))
            self.assertAlmostEqual(expected, float(np.sin((2 * iteration + 1) * theta) ** 2))
            self.assertAlmostEqual(float(np.sum(state ** 2)), 1)
            state = diffuse(oracle(state))

    def test_two_iterations_leave_negative_non_target_amplitudes(self):
        state = uniform_state()
        for _ in range(2):
            state = diffuse(oracle(state))
        self.assertTrue(np.all(np.delete(state, TARGET) < 0))
        self.assertGreater(state[TARGET], 0)
        # A third iteration overshoots: do not imply that more is always better.
        third = diffuse(oracle(state))
        self.assertLess(float(third[TARGET] ** 2), float(state[TARGET] ** 2))

    def test_search_plane_reflections_match_full_state_and_rotation(self):
        state = uniform_state()
        s = search_plane(state)
        oracle_matrix = np.diag([-1, 1])
        diffusion_matrix = 2 * np.outer(s, s) - np.eye(2)
        theta = np.arcsin(1 / np.sqrt(N))
        clockwise_rotation = np.array([
            [np.cos(2 * theta), np.sin(2 * theta)],
            [-np.sin(2 * theta), np.cos(2 * theta)],
        ])
        np.testing.assert_allclose(diffusion_matrix @ oracle_matrix, clockwise_rotation)
        for k in range(3):
            xy = search_plane(state)
            np.testing.assert_allclose(xy, [np.sin((2*k+1)*theta), np.cos((2*k+1)*theta)])
            self.assertAlmostEqual(float(xy @ xy), 1)
            self.assertAlmostEqual(float(xy[0] ** 2), float(state[TARGET] ** 2))
            flipped = oracle(state)
            np.testing.assert_allclose(search_plane(flipped), oracle_matrix @ xy)
            state = diffuse(flipped)
            np.testing.assert_allclose(search_plane(state), diffusion_matrix @ oracle_matrix @ xy)


if __name__ == "__main__":
    unittest.main()
