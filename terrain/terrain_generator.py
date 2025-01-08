
from map.map_orchestrator import MapOrchestrator
from .noise_ops import PerlinNoise, VoronoiNoise
from .erosion import Erosion
from utilities.logger import LoggerUtility as log
from config import PERLIN_SCALE, VORONOI_REGIONS

class TerrainGenerator:
    """Generates terrain using noise and erosion."""

    def __init__(self, map_orchestrator: MapOrchestrator) -> None:
        self.map = map_orchestrator
        log.success("Terrain generator initialized.")

    def __repr__(self) -> str:
        return f"TerrainGenerator(map_orchestrator={self.map})"

    def __str__(self) -> str:
        return "TerrainGenerator: generates terrain using noise and erosion"


    @log.log_method
    def generate_heightmap(self) -> None:
        """Generates a heightmap using Perlin and Voronoi noise."""
        perlin = PerlinNoise(scale=PERLIN_SCALE, seed=self.map.seed)
        voronoi = VoronoiNoise(regions=VORONOI_REGIONS, seed=self.map.seed)

        # Combine Perlin and Voronoi noise
        heightmap = (
            perlin.generate(self.map.grid.size) * 0.7 +
            voronoi.generate(self.map.grid.size) * 0.3
        )
        heightmap = Erosion.apply(heightmap, iterations=5)

        # Normalize heightmap to elevation values
        max_height = self.map.grid.max_elevation + self.map.grid.max_depth
        normalized_map = (heightmap * max_height / heightmap.max()).astype(float)

        # Assign heights to the grid
        for x in range(self.map.grid.size[0]):
            for y in range(self.map.grid.size[1]):
                elevation = normalized_map[x, y]
                self.map.grid.set_cell_property(x, y, "elevation", elevation)

        log.success("Heightmap generation complete.")

    @log.log_method
    def generate(self) -> None:
        """Full terrain generation process."""
        log.info("Generating terrain...")
        self.generate_heightmap()
        log.info("Populating graph...")
        self.map.initialize_graph()
        log.success("Graph population complete.")
            