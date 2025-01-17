
# Test for HeightMap
from ...maps.height_map import HeightMap


class TestHeightMap:
    def test_normalize(self):
        height_map = HeightMap(width=3, height=3, default_value=10.0)
        height_map.grid[1, 1] = 50.0
        height_map.normalize()
        assert height_map.grid.min() == 0.0
        assert height_map.grid.max() == 1.0
