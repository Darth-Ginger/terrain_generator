
from config import GRID_SIZE, MAX_ELEVATION, MAX_DEPTH, SEED
from map.map_orchestrator import MapOrchestrator
from terrain.terrain_generator import TerrainGenerator

if __name__ == "__main__":
    # Create map orchestrator
    map_orchestrator = MapOrchestrator(
        size=GRID_SIZE, 
        max_elevation=MAX_ELEVATION, 
        max_depth=MAX_DEPTH, 
        seed=SEED
    )

    # Generate terrain
    terrain_generator = TerrainGenerator(map_orchestrator)
    terrain_generator.generate()
    print("Terrain generation complete.")
        