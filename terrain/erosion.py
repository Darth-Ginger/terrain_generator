
from typing import Tuple
import numpy as np

class Erosion:
    """Simulates erosion on a heightmap."""

    @staticmethod
    def apply(heightmap: np.ndarray, iterations: int) -> np.ndarray:
        """Applies erosion over multiple iterations."""
        for _ in range(iterations):
            erosion_mask = np.random.rand(*heightmap.shape) * 0.01
            heightmap = np.maximum(heightmap - erosion_mask, 0)  # Prevent negative values
        return heightmap
            