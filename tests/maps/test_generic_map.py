from ...maps.generic_map import GenericMap

# Test for GenericMap
class TestGenericMap:
    def test_discover_map_classes(self):
        map_classes = GenericMap.build_map_classes()
        assert "GridMap" in map_classes
        assert "HeightMap" in map_classes
        assert "PrecipitationMap" in map_classes
        assert "VoronoiMap" in map_classes

