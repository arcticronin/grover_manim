"""Real amplitudes used by the animation, with one marked candidate."""

import numpy as np

N = 8
TARGET = 5


def bloch_vector(theta: float, phi: float = 0) -> np.ndarray:
    """Pure-state Bloch coordinates; polar theta is twice the amplitude angle."""
    return np.array([np.sin(theta)*np.cos(phi), np.sin(theta)*np.sin(phi), np.cos(theta)])


def uniform_state(n: int = N) -> np.ndarray:
    return np.full(n, 1 / np.sqrt(n))


def oracle(state: np.ndarray, target: int = TARGET) -> np.ndarray:
    result = state.copy()
    result[target] *= -1
    return result


def diffuse(state: np.ndarray) -> np.ndarray:
    return 2 * np.mean(state) - state


def search_plane(state: np.ndarray, target: int = TARGET) -> np.ndarray:
    """Coordinates along the target and the normalized sum of non-targets.

    Grover states have equal non-target amplitudes, so these coordinates
    represent the entire state without losing information.
    """
    return np.array([state[target], np.sum(np.delete(state, target)) / np.sqrt(len(state) - 1)])
