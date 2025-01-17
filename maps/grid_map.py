from typing import Any, Dict
import numpy as np
from maps.generic_map import GenericMap


class GridMap(GenericMap):
    """
    A class for 2D grid-based maps (e.g., terrain, temperature).
    """
    def __init__(self, **kwargs) -> None:
        self.width   : int = kwargs.get("width", 10)  # Default to 10 if not provided in kwargs
        self.height  : int = kwargs.get("height", 10)  # Default to 10 if not provided in kwargs
        default_value: float = kwargs.get("default_value", 0)  # Default to 0 if not provided in kwargs
        self.grid    : np.ndarray = np.full((self.height, self.width), default_value)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "GridMap",
            "width": self.width,
            "height": self.height,
            "grid": self.grid.tolist(),
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        self.width  = data.get("width", 10)
        self.height = data.get("height", 10)
        self.grid   = np.array(data.get("grid", np.full((self.height, self.width), 0)))

    def get_data(self, x: int, y: int) -> float:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y, x]
        raise IndexError("Coordinates out of bounds.")