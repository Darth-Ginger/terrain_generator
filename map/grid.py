
from typing import Dict, Tuple
import numpy as np

class Grid3D:
    """Represents a 3D grid for terrain."""

    def __init__(self, size: Tuple[int, int], max_elevation: float, max_depth: float) -> None:
        self.size = size  # (X, Y)
        self.max_elevation = max_elevation  # in kilometers
        self.max_depth = max_depth  # in kilometers
        self.z_levels = int((max_elevation + max_depth) * 1000)  # Normalize to meters
        self.grid = np.empty((size[0], size[1], self.z_levels), dtype=object)
        self.initialize_cells()

    def initialize_cells(self) -> None:
        """Populates the 3D grid with default properties."""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                for z in range(self.z_levels):
                    self.grid[x, y, z] = {
                        "elevation": z / 1000,  # Non-normalized (kilometers)
                        "normalized_elevation": z / self.z_levels,  # Normalized
                        "type": "air" if z > self.max_depth * 1000 else "water",
                    }

    def set_cell_property(self, x: int, y: int, z: int, key: str, value: float) -> None:
        """Sets a property for a specific cell."""
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.z_levels:
            self.grid[x, y, z][key] = value

    def get_cell_property(self, x: int, y: int, z: int, key: str) -> float:
        """Gets a property for a specific cell."""
        return self.grid[x, y, z].get(key, None)
            