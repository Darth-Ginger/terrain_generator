import sys
import os

# Dynamically add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from ...maps.generic_map import GenericMap

# Test for GenericMap
class TestGenericMap:
    def test_discover_map_classes(self):
        map_classes = GenericMap.discover_map_classes()
        assert "GridMap" in map_classes
        assert "HeightMap" in map_classes
        assert "PrecipitationMap" in map_classes
        assert "VoronoiMap" in map_classes

