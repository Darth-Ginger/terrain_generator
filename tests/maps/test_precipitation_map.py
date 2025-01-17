
# Test for PrecipitationMap
from ...maps.precipitation_map import PrecipitationMap


class TestPrecipitationMap:
    def test_clamp(self):
        precipitation_map = PrecipitationMap(width=3, height=3, default_value=1.5)
        precipitation_map.clamp(min_value=0.0, max_value=1.0)
        assert precipitation_map.grid.max() <= 1.0
        assert precipitation_map.grid.min() >= 0.0
