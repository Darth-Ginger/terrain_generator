import numpy as np

from config import GRID_SIZE, MAX_ELEVATION, MAX_DEPTH, SEED
from map.map_orchestrator import MapOrchestrator
from terrain.terrain_generator import TerrainGenerator
from utilities.logger import LoggerUtility as log
import matplotlib.pyplot as plt
import json

if __name__ == "__main__":
    log.log_startup_header()
    
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
    print()
    
    
    # Dump all objects to debug_output.json
    print(terrain_generator.map.grid.normalized_elevation_map().shape)
    print(terrain_generator.map.grid.normalized_elevation_map())
    
    # Plot elevation map
    plt.imshow(terrain_generator.map.grid.normalized_elevation_map(), cmap="terrain")
    plt.colorbar()
    plt.title("Terrain Map")
    plt.show()
    
    

    
    
        