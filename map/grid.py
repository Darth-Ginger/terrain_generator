
from typing import Tuple
import numpy as np
from utilities.logger import LoggerUtility as log
from utilities.utils import dict_to_str

class Grid3D:
    """Represents a 3D grid for terrain."""

    def __init__(self, size: Tuple[int, int], max_elevation: float, max_depth: float) -> None:
        self.size: Tuple[int, int] = size  # (X, Y)
        self.max_elevation: float = max_elevation  # in kilometers
        self.max_depth: float = max_depth  # in kilometers
        self.z_levels: int = int((max_elevation + max_depth) * 1000)  # Normalize to meters
        self.grid: np.ndarray = np.empty((size[0], size[1], self.z_levels), dtype=object)
        self.initialize_cells()
        
        log.success("3D grid initialized.")

    @log.log_method
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

    # @log.log_method
    def set_cell_property(self, x: int, y: int, z: int, key: str, value: float) -> None:
        """Sets a property for a specific cell."""
        if 0 <= x < self.size[0] and 0 <= y < self.size[1] and 0 <= z < self.z_levels:
            self.grid[x, y, z][key] = value

    @log.log_method
    def get_cell_property(self, x: int, y: int, z: int, key: str) -> float:
        """Gets a property for a specific cell."""
        return self.grid[x, y, z].get(key, None)


class Grid2D:
    """Represents a 2D grid for terrain."""

    def __init__(self, size: Tuple[int, int], max_elevation: float, max_depth: float) -> None:
        self.size: Tuple[int, int] = size  # (X, Y)
        self.max_elevation: float = max_elevation  # in kilometers
        self.max_depth: float = max_depth  # in kilometers
        self.normalized_sea_level: float = self.max_depth / (self.max_elevation + self.max_depth)
        self.grid: np.ndarray = np.empty(size, dtype=object)
        self.initialize_cells()
        
        log.success("2D grid initialized.")

    
    def __repr__(self) -> str:
        """Returns a concise string representation of the object."""
        return f"{self.__class__.__name__}({', '.join(f'{k}={v}' for k, v in self.__dict__.items())})"

    def __str__(self) -> str:
        """Returns a human-readable string representation of the object."""
        return f"{self.__class__.__name__}(size={self.size}, max_elevation={self.max_elevation}, max_depth={self.max_depth}, normalized_sea_level={self.normalized_sea_level})\n \
Grid:\n" + "\n".join(f"{x},{y} : {dict_to_str(self.grid[x, y])}" for x in range(self.size[0]) for y in range(self.size[1]))

    def elevation_map(self) -> np.ndarray:
        return np.array([[self.grid[x, y]["elevation"] for y in range(self.size[1])] for x in range(self.size[0])])
    def normalized_elevation_map(self) -> np.ndarray:
        return np.array([[self.grid[x, y]["normalized_elevation"] for y in range(self.size[1])] for x in range(self.size[0])])
    def type_map(self) -> np.ndarray:
        return np.array([[self.grid[x, y]["type"] for y in range(self.size[1])] for x in range(self.size[0])])

    @log.log_method
    def initialize_cells(self) -> None:
        """Populates the 2D grid with default properties."""
        for x in range(self.size[0]):
            for y in range(self.size[1]):
                self.grid[x, y] = {
                    "elevation": 0.0,
                    "normalized_elevation": 0.0,
                    "type": "water",
                }

    # @log.log_method
    def set_cell_property(self, x: int, y: int, key: str, value: float) -> None:
        """Sets a property for a specific cell."""
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            if key == "elevation":
                self.grid[x, y]["normalized_elevation"] = value / (self.max_elevation + self.max_depth)
            self.grid[x, y][key] = value
            
    
    @log.log_method
    def set_cell_elevation(self, x: int, y: int, elevation: float) -> None:
        """Sets a property for a specific cell."""
        if 0 <= x < self.size[0] and 0 <= y < self.size[1]:
            normalized_elevation = elevation / (self.max_elevation + self.max_depth)
            self.grid[x, y]["elevation"] = elevation
            self.grid[x, y]["normalized_elevation"] = normalized_elevation
            self.grid[x, y]["type"] = "water" if normalized_elevation < -self.normalized_sea_level else "land"

    @log.log_method
    def get_cell_property(self, x: int, y: int, key: str) -> float:
        """Gets a property for a specific cell."""
        return self.grid[x, y].get(key, None)
