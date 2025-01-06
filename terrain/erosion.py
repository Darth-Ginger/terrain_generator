
import numpy as np
from utilities.logger import LoggerUtility as log

class Erosion:
    """Simulates erosion on a heightmap."""

    @staticmethod
    @log.log_method_stats
    @log.write_debug_output()
    def apply(heightmap: np.ndarray, iterations: int) -> np.ndarray:
        """Applies erosion over multiple iterations."""
        for _ in range(iterations):
            erosion_mask = np.random.rand(*heightmap.shape) * 0.01
            heightmap = np.maximum(heightmap - erosion_mask, 0)  # Prevent negative values
        return heightmap
            