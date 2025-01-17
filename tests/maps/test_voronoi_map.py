
# Test for VoronoiMap
from ...maps.voronoi_map import VoronoiMap


class TestVoronoiMap:
    def test_add_region_and_query(self):
        voronoi_map = VoronoiMap()
        voronoi_map.add_region(node_id=1, properties={"type": "land", "elevation": 100})
        data = voronoi_map.get_data(node_id=1)
        assert data["type"] == "land"
        assert data["elevation"] == 100

    def test_to_dict_and_from_dict(self):
        voronoi_map = VoronoiMap()
        voronoi_map.add_region(node_id=1, properties={"type": "land", "elevation": 100})
        voronoi_map.add_region(node_id=2, properties={"type": "water", "elevation": 0})
        voronoi_map.add_boundary(node1=1, node2=2, properties={"weight": 1.0})

        serialized = voronoi_map.to_dict()
        restored_map = VoronoiMap()
        restored_map.from_dict(serialized)

        assert restored_map.graph.has_node(1)
        assert restored_map.graph.has_node(2)
        assert restored_map.graph.has_edge(1, 2)
        assert restored_map.get_data(1)["type"] == "land"
