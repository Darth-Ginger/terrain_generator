
from typing import Tuple
from .grid import Grid3D
from .graph import TerrainGraph

from utilities.logger import LoggerUtility as log

class MapOrchestrator:
    """Handles the synchronization of the grid and graph."""

    def __init__(self, size: Tuple[int, int], max_elevation: float, max_depth: float, seed: int) -> None:
        self.grid = Grid3D(size, max_elevation, max_depth)
        self.graph = TerrainGraph()
        self.seed = seed

        log.success("Map orchestrator initialized.")

    @log.log_method_stats
    def initialize_graph(self) -> None:
        """Populates the graph based on the grid's state."""
        for x in range(self.grid.size[0]):
            for y in range(self.grid.size[1]):
                for z in range(self.grid.z_levels):
                    cell = self.grid.grid[x, y, z]
                    self.graph.add_node((x, y, z), **cell)
                    if z > 0:  # Link vertical neighbors
                        self.graph.add_edge((x, y, z - 1), (x, y, z))
                    if x > 0:  # Link horizontal neighbors
                        self.graph.add_edge((x - 1, y, z), (x, y, z))
            