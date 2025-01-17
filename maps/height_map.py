

from typing import Any, Dict
from maps.grid_map import GridMap
import numpy as np


class HeightMap(GridMap):
    """
    A class for 2D grid-based height maps.
    """
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.height_range           : tuple[float, float] = kwargs.get("height_range", (0,10000))
        self.height_range_normalized: tuple[float, float] = kwargs.get("height_range_normalized", (0,1))
        self.normal_grid            : np.ndarray = np.full((self.height, self.width), 0.0)

    #region Properties
    @property
    def min_height(self) -> float:
        return self.height_range[0]

    @property
    def max_height(self) -> float:
        return self.height_range[1]

    #endregion Properties
    
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data.update({
            "type": "HeightMap",
            "height_range": self.height_range,
            "height_range_normalized": self.height_range_normalized,
        })
        return data

    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        self.min_height = data["height_range"]
        self.max_height = data["height_range_normalized"]
        self.normal_grid = (self.grid - self.min_height) / (self.max_height - self.min_height)

    def get_height(self, x: int, y: int) -> float:
        return self.get_data(x, y)

    def set_height(self, x: int, y: int, value: float) -> None:
        self.set_data(x, y, value)
        self.normal_grid[y, x] = (value - self.min_height) / (self.max_height - self.min_height)

    def get_normalized_height(self, x: int, y: int) -> float:
        return self.normal_grid[y, x]