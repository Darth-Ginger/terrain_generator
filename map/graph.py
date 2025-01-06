
from typing import Tuple
import networkx as nx
from utilities.logger import LoggerUtility as log

class TerrainGraph:
    """Graph structure to manage dynamic relationships."""

    def __init__(self) -> None:
        self.graph = nx.DiGraph()
        log.success("Terrain graph initialized.")

    @log.log_method_stats
    @log.write_debug_output()
    def add_node(self, position: Tuple[int, int, int], **attributes) -> None:
        """Adds a node representing a grid cell."""
        self.graph.add_node(position, **attributes)

    @log.log_method_stats
    @log.write_debug_output()
    def add_edge(self, source: Tuple[int, int, int], target: Tuple[int, int, int], **attributes) -> None:
        """Adds a directed edge between nodes."""
        self.graph.add_edge(source, target, **attributes)

    @log.log_method_stats
    @log.write_debug_output()
    def get_neighbors(self, position: Tuple[int, int, int]) -> list:
        """Returns neighbors of a given node."""
        return list(self.graph.neighbors(position))
            