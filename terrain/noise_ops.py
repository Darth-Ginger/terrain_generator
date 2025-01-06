
from typing import Tuple
import noise
import numpy as np

class PerlinNoise:
    """Generates Perlin noise for terrain."""

    def __init__(self, scale: float, seed: int) -> None:
        self.scale = scale
        self.seed = seed

    def generate(self, size: Tuple[int, int]) -> np.ndarray:
        """Generates a 2D array of Perlin noise."""
        np.random.seed(self.seed)
        return np.array([
            [noise.pnoise2(x * self.scale, y * self.scale, base=self.seed) for y in range(size[1])]
            for x in range(size[0])
        ])

class VoronoiNoise:
    """Generates Voronoi noise for terrain."""

    def __init__(self, regions: int, seed: int) -> None:
        self.regions = regions
        self.seed = seed

    def generate(self, size: Tuple[int, int]) -> np.ndarray:
        """Generates Voronoi regions."""
        np.random.seed(self.seed)
        points = np.random.rand(self.regions, 2) * np.array(size)
        grid = np.zeros(size)
        for x in range(size[0]):
            for y in range(size[1]):
                distances = np.linalg.norm(points - np.array([x, y]), axis=1)
                grid[x, y] = np.argmin(distances) / self.regions
        return grid
            