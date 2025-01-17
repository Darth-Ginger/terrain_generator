import numpy as np

from ...maps.grid_map import GridMap

# Test for GridMap
class TestGridMap:
    def test_initialization(self):
        grid_map = GridMap(width=10, height=5, default_value=1.0)
        assert grid_map.width == 10
        assert grid_map.height == 5
        assert np.all(grid_map.grid == 1.0)

    def test_to_dict_and_from_dict(self):
        grid_map = GridMap(width=5, height=5, default_value=0.0)
        serialized = grid_map.to_dict()
        restored_map = GridMap(width=1, height=1)
        restored_map.from_dict(serialized)
        assert np.array_equal(grid_map.grid, restored_map.grid)
        assert grid_map.width == restored_map.width
        assert grid_map.height == restored_map.height