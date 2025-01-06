
from map.map_orchestrator import MapOrchestrator
from .noise_ops import PerlinNoise, VoronoiNoise
from .erosion import Erosion
from utilities.logger import LoggerUtility as log

class TerrainGenerator:
    """Generates terrain using noise and erosion."""

    def __init__(self, map_orchestrator: MapOrchestrator) -> None:
        self.map = map_orchestrator
        log.success("Terrain generator initialized.")

    @log.log_method_stats
    def generate_heightmap(self) -> None:
        """Generates a heightmap using Perlin and Voronoi noise."""
        perlin = PerlinNoise(scale=0.1, seed=self.map.seed)
        voronoi = VoronoiNoise(regions=50, seed=self.map.seed)

        # Combine Perlin and Voronoi noise
        heightmap = (
            perlin.generate(self.map.grid.size) * 0.7 +
            voronoi.generate(self.map.grid.size) * 0.3
        )
        heightmap = Erosion.apply(heightmap, iterations=5)

        # Normalize heightmap to grid levels
        max_height = self.map.grid.max_elevation + self.map.grid.max_depth
        normalized_map = (heightmap * self.map.grid.z_levels / max_height).astype(int)

        # Assign heights to the grid
        for x in range(self.map.grid.size[0]):
            for y in range(self.map.grid.size[1]):
                max_z = normalized_map[x, y]
                for z in range(max_z):
                    self.map.grid.set_cell_property(x, y, z, "type", "land")

        log.success("Heightmap generation complete.")

    @log.log_method_stats
    def generate(self) -> None:
        """Full terrain generation process."""
        log.info("Generating terrain...")
        self.generate_heightmap()
        log.info("Populating graph...")
        self.map.initialize_graph()
        log.success("Graph population complete.")
            