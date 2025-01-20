import networkx as nx
from typing import Dict, Any

from generic_map import GenericMap


class VoronoiMap(GenericMap):
    """
    A class for representing Voronoi diagram-based maps using a graph structure.
    """
    map_type = "VoronoiMap"

    def __init__(self):
        """
        Initialize an empty Voronoi map with a graph-based structure.
        """
        self.graph = nx.Graph()

    def add_region(self, node_id: Any, properties: Dict[str, Any]):
        """
        Add a region (node) to the Voronoi graph.

        Args:
            node_id (Any): The unique identifier for the region.
            properties (Dict[str, Any]): Properties associated with the region.
        """
        self.graph.add_node(node_id, **properties)

    def add_boundary(self, node1: Any, node2: Any, properties: Dict[str, Any] = None):
        """
        Add a boundary (edge) between two regions in the Voronoi graph.

        Args:
            node1 (Any): The first region.
            node2 (Any): The second region.
            properties (Dict[str, Any], optional): Properties for the boundary.
        """
        self.graph.add_edge(node1, node2, **(properties or {}))

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize the Voronoi map to a dictionary.

        Returns:
            Dict[str, Any]: A dictionary representation of the Voronoi map.
        """
        return {
            "type": "VoronoiMap",
            "graph": nx.node_link_data(self.graph),  # Serialize graph using NetworkX
        }

    def from_dict(self, data: Dict[str, Any]) -> None:
        """
        Deserialize the Voronoi map from a dictionary.

        Args:
            data (Dict[str, Any]): The serialized Voronoi map data.
        """
        self.graph = nx.node_link_graph(data["graph"])

    def get_data(self, node_id: Any) -> Dict[str, Any]:
        """
        Retrieve properties of a specific region (node).

        Args:
            node_id (Any): The unique identifier of the region.

        Returns:
            Dict[str, Any]: Properties of the region.

        Raises:
            KeyError: If the region is not found.
        """
        if self.graph.has_node(node_id):
            return self.graph.nodes[node_id]
        raise KeyError(f"Node {node_id} not found in the graph.")
