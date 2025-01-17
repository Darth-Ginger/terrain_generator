
from typing import Tuple
from .grid import Grid2D
from .graph import TerrainGraph

from utilities.logger import LoggerUtility as log

class MapOrchestrator:
    """Handles the synchronization of the grid and graph."""

    def __init__(self, size: Tuple[int, int], max_elevation: float, max_depth: float, seed: int) -> None:
        self.grid = Grid2D(size, max_elevation, max_depth)
        self.graph = TerrainGraph()
        self.seed = seed

        log.success("Map orchestrator initialized.")

    def __repr__(self) -> str:
        """Returns a concise string representation of the MapOrchestrator."""
        return f"MapOrchestrator(size={self.grid.size}, max_elevation={self.grid.max_elevation}, max_depth={self.grid.max_depth}, seed={self.seed})"

    def __str__(self) -> str:
        """Returns a human-readable string representation of the MapOrchestrator."""
        return (
            f"MapOrchestrator:\n"
            f"  Grid Size: {self.grid.size}\n"
            f"  Max Elevation: {self.grid.max_elevation}\n"
            f"  Max Depth: {self.grid.max_depth}\n"
            f"  Seed: {self.seed}\n"
        )

    @log.log_method
    def initialize_graph(self) -> None:
        """Populates the graph based on the grid's state."""
        for x in range(self.grid.size[0]):
            for y in range(self.grid.size[1]):
                cell = self.grid.grid[x, y]
                self.graph.add_node((x, y), **cell)
                if x > 0:  # Link horizontal neighbors
                    self.graph.add_edge((x - 1, y), (x, y))
                if y > 0:  # Link vertical neighbors
                    self.graph.add_edge((x, y - 1), (x, y))
                if x > 0 and y > 0:  # Link top-left neighbors
                    self.graph.add_edge((x - 1, y - 1), (x, y))
                if x < self.grid.size[0] - 1 and y > 0:  # Link top-right neighbors
                    self.graph.add_edge((x + 1, y - 1), (x, y))
                if x > 0 and y < self.grid.size[1] - 1:  # Link bottom-left neighbors
                    self.graph.add_edge((x - 1, y + 1), (x, y))
                if x < self.grid.size[0] - 1 and y < self.grid.size[1] - 1:  # Link bottom-right neighbors
                    self.graph.add_edge((x + 1, y + 1), (x, y))
            